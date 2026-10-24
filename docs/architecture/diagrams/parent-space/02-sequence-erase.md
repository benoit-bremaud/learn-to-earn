# Sequence diagram — parent-space — erase all data

> **Feature**: parent-space domain, UC-P9 (with UC-P8 offered first)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-P8, UC-P9, UC-P14)
> **Related ADRs**: ADR-0002 (D12), ADR-0003
> **Decisions captured**: S1, V1, §4 privacy baseline

## Context

OQ-5 part 1 is decided by ADR-0002 D12: the erase removes everything the app stored, then the app restarts on the set-up.

Progressive disclosure: the screen first shows one "Erase everything" button. The export offer and "Cancel" appear after it, and the PIN confirmation only after "Erase anyway".

## Diagram

```mermaid
sequenceDiagram
  title sd — UC-P9 Erase all data
  autonumber
  actor Guardian
  participant PUI as «boundary» ParentScreen
  participant Ctl as «control» EraseAll
  participant Inst as «entity» Installation aggregate
  participant Store as «port» Storage
  participant Keys as «port» Key store

  Guardian->>PUI: tap Erase everything
  PUI->>Guardian: offer an export first (UC-P8), Erase anyway, Cancel
  alt Guardian cancels
    Guardian->>PUI: tap Cancel
    PUI-->>Guardian: nothing deleted
  else Guardian exports first
    Guardian->>PUI: tap Export first
    Note over PUI: UC-P8 runs, then the erase screen comes back
  else Guardian taps Erase anyway
    PUI->>Guardian: ask for the PIN
    Guardian->>PUI: PIN
    PUI->>Ctl: erase(PIN)
    Ctl->>Inst: check PIN (lockout applies)
    alt wrong PIN
      Ctl-->>PUI: progressive lockout, nothing deleted
    else PIN correct
      Ctl->>Store: write the marker "erase in progress" outside the database
      Ctl->>Keys: delete the database key
      Ctl->>Store: delete the database and every set-aside database (PII: all child data)
      Ctl->>Store: remove the marker
      Ctl->>PUI: confirmation, then restart on UC-P14 step 1
    end
  end
```

## Notes

- Static data (skills, strands, companion catalogue) ships with the app and is not stored data, so nothing remains.
- The key goes first, so any file left behind by a crash is already unreadable. The marker makes the erase resumable: a start-up that finds it finishes the deletion before showing UC-P14.
- Export files the Guardian already saved outside the app (UC-P8) are not erased: the confirmation says so.
- After the restart, the Guardian confirms consent again for the child (UC-P14 step 1).
