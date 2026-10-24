# Sequence diagram — screen-time — use approved time

> **Feature**: screen-time domain, UC-S3 (with extension 4a in V2)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-S3)
> **Related ADRs**: ADR-0001 (D8), ADR-0002 (D2), ADR-0005 (D1)
> **Decisions captured**: Q1, Q4, P0, P1, P3, Conversion

## Context

From its start the use holds the full requested minutes (C11). DeviceOS appears only in V2 (ADR-0001 D8: former UC-S4).

Progressive disclosure: "Start the timer" appears only once the request is approved, under the gauge with the minutes still possible (never a question, ADR-0005 D1), then only the countdown and "Stop" are shown.

## Diagram

```mermaid
sequenceDiagram
  title sd — UC-S3 Use approved screen time
  autonumber
  actor Learner
  participant UI as «boundary» ScreenTimeScreen
  participant Ctl as «control» ScreenTimeHandler
  participant Reserve as «entity» Reserve aggregate
  participant Alarm as «port» OS alarm
  actor DeviceOS

  Learner->>UI: open the gauge, a request is APPROVED
  UI->>Ctl: show the approved request
  Ctl->>Reserve: minutes still covered by the balance and the daily cap left
  alt nothing is covered (1a, ADR-0005 D1)
    Ctl->>Reserve: request EXPIRED, no debit, REQUEST_NOT_COVERED note
    Ctl->>UI: No more screen time today, one OK button
  else some or all minutes covered
    Ctl->>UI: gauge with the minutes still possible and one Start button
    Learner->>UI: tap Start the timer
    UI->>Ctl: start
    Ctl->>Reserve: request IN_USE for those minutes (REQUEST_NOT_COVERED note if fewer), use startedAt (hold them in full)
    Ctl->>Alarm: schedule end alarm, and the 5-minute warning if longer than 5 minutes
    Ctl->>UI: countdown and Stop only
    alt Learner taps Stop (2a)
      Learner->>UI: tap Stop
      UI->>Ctl: stop
      Ctl->>Reserve: endedAt, usedMinutes exact, request USED, EARLY_STOP note (V1.1)
      Ctl->>Alarm: cancel
    else alarm rings at the end
      Alarm-->>Ctl: timer ended
      Ctl->>Reserve: endedAt, request USED
      opt V2 blocking permission granted (4a)
        Ctl->>DeviceOS: block other apps for the child's user
        DeviceOS-->>Ctl: confirmed, or refused and the alarm stays the only signal
      end
    end
    Ctl->>UI: back to the gauge
  end
```

## Notes

- App killed or device restarted (UC-S3 *a): on return the handler reads `startedAt`, debits `min(minutes, now − startedAt)` and closes a timer whose end has passed. A backwards clock debits the full minutes and raises a CLOCK_CHANGED note (domain C16).
- The alarm is an OS port scheduled at start, so it rings even if the app is closed.
