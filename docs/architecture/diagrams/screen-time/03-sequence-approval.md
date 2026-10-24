# Sequence diagram — screen-time — approve a request

> **Feature**: screen-time domain, UC-S2 (with UC-P1)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-S2, UC-P1)
> **Related ADRs**: ADR-0001 (D8), ADR-0002 (D2)
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
```

## Notes

- Wrong-PIN handling is owned by UC-P1. Remote approval on the parent's phone stays open (OQ-2).
