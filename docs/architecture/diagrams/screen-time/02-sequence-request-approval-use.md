# Sequence diagram — screen-time — request, approval and use

> **Feature**: screen-time domain, UC-S1, UC-S2 (with UC-P1), UC-S3 (with extension 4a in V2)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-S1, UC-S2, UC-S3, UC-P1)
> **Related ADRs**: ADR-0001 (D8), ADR-0002 (D2)
> **Decisions captured**: Q1, Q4, P0, P1, P3, Conversion

## Context

The full path from earned minutes to a finished timer. The balance is replayed from the credits, oldest first (ADR-0002 D2). Only one request is open at a time (domain C12).

Progressive disclosure: with a reserve of 0 the child sees only "Start a session". The duration picker appears only when minutes are available, "Ask" only once a duration is picked, "Start the timer" only once the request is approved, "Stop" only while the timer runs.

## Diagram

```mermaid
sequenceDiagram
  autonumber
  actor Learner
  actor Guardian
  participant UI as «boundary» ScreenTimeScreen
  participant PUI as «boundary» ParentScreen
  participant Ctl as «control» ScreenTimeHandler
  participant Reserve as «entity» Reserve aggregate
  participant Inst as «entity» Installation aggregate
  participant Clock as «port» Clock and TimeGuard
  participant Alarm as «port» OS alarm
  actor DeviceOS

  Learner->>UI: open screen time
  UI->>Ctl: available minutes
  Ctl->>Clock: trusted now
  Ctl->>Reserve: replay balance, daily cap left
  alt balance is 0
    Ctl->>UI: only "Start a session" (UC-L1)
  else daily cap reached
    Ctl->>UI: "enough for today"
  else minutes available
    Ctl->>UI: duration picker up to min(balance, cap left)
    Learner->>UI: pick duration, then tap Ask (shown once a duration is picked)
    UI->>Ctl: request(duration)
    Ctl->>Reserve: create request PENDING (one open request)
  end

  Guardian->>PUI: open the pending request
  PUI->>Guardian: ask for the PIN
  Guardian->>PUI: PIN
  PUI->>Ctl: unlock (UC-P1)
  Ctl->>Inst: check PIN, lockout
  alt wrong PIN
    Ctl-->>PUI: progressive lockout, nothing changes
  else PIN correct
    Ctl->>Reserve: balance and daily cap left still cover the request
    Ctl->>PUI: child, duration, reserve, then Approve and Refuse
    alt Guardian approves
      Guardian->>PUI: tap Approve
      PUI->>Ctl: approve
      Ctl->>Reserve: request APPROVED
      Ctl->>UI: show Start the timer
    else Guardian refuses
      Guardian->>PUI: tap Refuse
      PUI->>Ctl: refuse
      Ctl->>Reserve: request REFUSED, reserve unchanged
      Ctl->>UI: neutral message
    end
  end
  opt request APPROVED
    Learner->>UI: tap Start the timer
    UI->>Ctl: start
    Ctl->>Reserve: balance and daily cap left still cover it, request IN_USE, use startedAt (hold full minutes)
    Ctl->>Alarm: schedule end alarm, and the 5-minute warning if longer than 5 minutes
    Ctl->>UI: countdown and Stop only
    alt Learner taps Stop (2a)
      UI->>Ctl: stop
      Ctl->>Reserve: endedAt, usedMinutes exact, request USED, EARLY_STOP note (V1.1)
      Ctl->>Alarm: cancel
      Ctl->>UI: back to the gauge
    else alarm rings at the end
      Alarm-->>Ctl: timer ended
      Ctl->>Reserve: endedAt, request USED
      opt V2 blocking permission granted (4a)
        Ctl->>DeviceOS: block other apps for the child's user
        DeviceOS-->>Ctl: confirmed, or refused and the alarm stays the only signal
      end
      Ctl->>UI: back to the gauge
    end
  end
```

## Notes

- App killed or device restarted (UC-S3 *a): on return the handler reads `startedAt`, debits `min(minutes, now − startedAt)` and closes a timer whose end has passed. A backwards clock debits the full minutes and raises a CLOCK_CHANGED note (domain C16).
- A request PENDING or APPROVED at the end of its day becomes EXPIRED with no debit.
- The alarm is an OS port scheduled at start, so it rings even if the app is closed.
- DeviceOS appears only in V2 (ADR-0001 D8: former UC-S4).
