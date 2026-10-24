# Sequence diagram — parent-space — restore from a file

> **Feature**: parent-space domain, UC-P15, including the key-loss start screen
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-P14, UC-P15, storage rule)
> **Related ADRs**: ADR-0002 (D13), ADR-0003 (D3)
> **Decisions captured**: S1

## Context

OQ-5 part 2 is decided by ADR-0002 D13: a restore brings back everything except the screen-time reserve, so no minute already spent can come back.

Progressive disclosure: after a key loss the start screen shows only "Restore from a file" and "Set up again". The passphrase field appears once a file is chosen, the content summary once it decrypts, the PIN only after "Restore".

The key-loss start screen is in [04-sequence-key-loss-start.md](04-sequence-key-loss-start.md).

## Diagram

```mermaid
sequenceDiagram
  title sd — UC-P15 Restore the child's data from a file
  autonumber
  actor Guardian
  participant PUI as «boundary» ParentScreen
  participant Ctl as «control» RestoreFromFile
  participant File as «port» Export file
  participant Store as «port» Storage
  participant Inst as «entity» Installation aggregate
  participant Reserve as «entity» Reserve aggregate

  alt parent space unlocked
    Guardian->>PUI: open Restore
  else after a key loss
    Note over PUI,Ctl: ref sd Key-loss start, see 04-sequence-key-loss-start
  end
  Guardian->>PUI: choose a file
  PUI->>Guardian: ask for the passphrase
  Guardian->>PUI: passphrase
  PUI->>Ctl: decrypt and check
  Ctl->>File: decrypt with the key derived from the passphrase
  File-->>Ctl: content (PII: displayName, birthYear, results) or failure
  alt wrong passphrase, invalid or newer file
    Ctl-->>PUI: refused, nothing changes
  else valid file
    Ctl->>PUI: summary and "saved screen-time minutes are not restored"
    Guardian->>PUI: tap Restore
    PUI->>Guardian: ask for the PIN (the file's PIN after a key loss)
    Guardian->>PUI: PIN
    PUI->>Ctl: restore(PIN)
    Ctl->>Inst: check PIN against the current credential, or the file's after a key loss
    alt wrong PIN
      Ctl-->>PUI: progressive lockout, nothing changes
    else PIN correct
      Ctl->>Store: begin one transaction
      Ctl->>Reserve: on the file's data loaded in memory, forfeit the remaining minutes of every credit (balance 0, checkpoints kept)
      Ctl->>Reserve: on the file's data loaded in memory, close open requests (PENDING or APPROVED to EXPIRED, IN_USE debited in full)
      Ctl->>Inst: TimeGuard lastTrustedAt = later of the file's and the device's
      Ctl->>Store: replace the data with the file's and commit (after a key loss, under the key alias created at the key-loss start)
      opt a database was set aside
        Ctl->>Store: delete the set-aside database
      end
      Ctl->>PUI: done, back to the child profile
    end
  end
```

## Notes

- Forfeiting the reserve closes the replay hole for every case, key loss included (ADR-0002 D13). Credits stay as history, so the crediting checkpoints (domain C7) and the day's full-rate and cap counters are unchanged and an interrupted session in the file is never credited twice. The cost is at most the reserve cap in a rare case.
- While unlocked, the current credential (PIN hash, recovery code hash, lockout) is kept; the file's credential applies only after a key loss, and then the lockout counter starts from it. The passphrase is the stronger gate.
- The set-aside database is deleted once the restore succeeded, or after 30 days (ADR-0004 D17).
- The forfeit, the request closing and the trusted-time rule apply to the file's data inside the one transaction, so a crash leaves either the current data untouched or the restored data complete. The rules belong to the Reserve and Installation aggregates, not to the control.
- Trusted time never moves back, so restoring an old file cannot reopen expired days or reset the daily cap.
- After a key loss, the passphrase is the only proof of the Guardian (risk in ADR-0003, OQ-6).
