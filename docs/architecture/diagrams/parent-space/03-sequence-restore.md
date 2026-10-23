# Sequence diagram — parent-space — restore from a file

> **Feature**: parent-space domain, UC-P15, including the key-loss start screen
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-P14, UC-P15, storage rule)
> **Related ADRs**: ADR-0002 (D13), ADR-0003 (D3)
> **Decisions captured**: S1

## Context

OQ-5 part 2 is decided by ADR-0002 D13: a restore brings back everything except the screen-time reserve, so no minute already spent can come back.

Progressive disclosure: after a key loss the start screen shows only "Restore from a file" and "Set up again". The passphrase field appears once a file is chosen, the content summary once it decrypts, the PIN only after "Restore".

## Diagram

```mermaid
sequenceDiagram
  autonumber
  actor Guardian
  participant PUI as «boundary» ParentScreen
  participant Start as «control» StartUp
  participant Ctl as «control» RestoreFromFile
  participant File as «port» Export file
  participant Store as «port» Storage
  participant Keys as «port» Key store
  participant Clock as «port» Clock and TimeGuard

  alt database key lost at start-up
    Start->>Keys: read the database key (retried on error)
    Keys-->>Start: missing, or does not open the database
    Start->>Store: set the unreadable database aside
    Start->>PUI: show only Restore from a file and Set up again (UC-P14)
  else parent space unlocked
    Guardian->>PUI: open Restore
  end
  Guardian->>PUI: choose a file
  PUI->>Guardian: ask for the passphrase
  Guardian->>PUI: passphrase
  PUI->>Ctl: decrypt and check
  Ctl->>File: decrypt with the key derived from the passphrase
  alt wrong passphrase, invalid or newer file
    Ctl-->>PUI: refused, nothing changes
  else valid file
    Ctl->>PUI: summary and "saved screen-time minutes are not restored"
    Guardian->>PUI: tap Restore
    PUI->>Guardian: ask for the PIN (the file's PIN after a key loss)
    Guardian->>PUI: PIN
    PUI->>Ctl: restore(PIN)
    Ctl->>Ctl: check PIN against the current credential, or the file's after a key loss
    alt wrong PIN
      Ctl-->>PUI: progressive lockout, nothing changes
    else PIN correct
      Ctl->>Ctl: forfeit the remaining minutes of every credit (balance 0, checkpoints kept)
      Ctl->>Ctl: close open requests (PENDING or APPROVED to EXPIRED, IN_USE debited in full)
      Ctl->>Clock: lastTrustedAt = later of the file's and the device's
      opt key lost
        Ctl->>Keys: generate a new database key
      end
      Ctl->>Store: replace the data in one transaction
      opt a database was set aside
        Ctl->>Store: delete the set-aside database
      end
      Ctl->>PUI: done, back to the child profile
    end
  end
```

## Notes

- Forfeiting the reserve closes the replay hole for every case, key loss included (ADR-0002 D13). Credits stay as history, so the crediting checkpoints (domain C7) and the day's full-rate and cap counters are unchanged and an interrupted session in the file is never credited twice. The cost is at most the reserve cap in a rare case.
- After a key loss the lockout counter starts from the file's credential; the passphrase is the stronger gate.
- The set-aside database is deleted only once the restore succeeded (ADR-0003 D3).
- Trusted time never moves back, so restoring an old file cannot reopen expired days or reset the daily cap.
- After a key loss, the passphrase is the only proof of the Guardian (risk in ADR-0003, OQ-6).
