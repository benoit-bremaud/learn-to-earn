# Sequence diagram — screen-time — approve a request

> **Feature**: screen-time domain, UC-S2 (with UC-P1)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-S2, UC-P1)
> **Related ADRs**: ADR-0001 (D8), ADR-0002 (D2), ADR-0004 (D13, D14), ADR-0005 (D1)
> **Decisions captured**: Q1, Q4, P0, P1, P3, Conversion

## Context

The Guardian answers on the same tablet. The balance and the daily cap are checked again because they may have changed since the request (C11, C12).

Progressive disclosure: the parent screen shows the PIN pad first, the request details and the Approve and Refuse buttons only after a correct PIN.

## Diagram

```mermaid
sequenceDiagram
  title sd — UC-S2 Approve a screen-time request (with UC-P1)
  autonumber
  actor Guardian
  participant PUI as «boundary» ParentScreen
  participant Ctl as «control» ScreenTimeHandler
  participant Inst as «entity» Installation aggregate
  participant Reserve as «entity» Reserve aggregate
  participant UI as «boundary» ScreenTimeScreen

  Guardian->>PUI: open the pending request
  PUI->>Guardian: ask for the PIN (scrambled pad)
  Guardian->>PUI: PIN
  PUI->>Ctl: unlock (UC-P1)
  Ctl->>Inst: check PIN, lockout
  alt wrong PIN
    Ctl-->>PUI: progressive lockout (3 free tries, then 30 s to 15 min), nothing changes
  else PIN correct
    Ctl->>Reserve: minutes still covered by the balance and the daily cap left
    alt nothing is covered (ADR-0005 D1)
      Ctl->>Reserve: request EXPIRED, no debit, REQUEST_NOT_COVERED note
      Ctl->>PUI: no time left today, request closed
      Ctl->>UI: No more screen time today, one OK button
    else some or all minutes covered
      Ctl->>PUI: child, duration (shortened if less is covered), reserve, then Approve and Refuse
      alt Guardian approves
        Guardian->>PUI: tap Approve
        PUI->>Ctl: approve
        Ctl->>Reserve: request APPROVED for the covered minutes, REQUEST_NOT_COVERED note if fewer
        Ctl->>UI: show Start the timer
      else Guardian refuses
        Guardian->>PUI: tap Refuse
        PUI->>Ctl: refuse
        Ctl->>Reserve: request REFUSED, reserve unchanged
        Ctl->>UI: neutral message
      end
    end
  end
```

## Notes

- A shortened approval grants less than requested, so the Guardian's tap is enough. The child screen shows only the gauge or one short sentence (ADR-0005 D1).
- Wrong-PIN handling is owned by UC-P1. Remote approval on the parent's phone stays open (OQ-2).
