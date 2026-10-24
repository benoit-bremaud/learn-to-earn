# Sequence diagram — parent-space — key-loss start

> **Feature**: parent-space domain, start-up when the database key is lost (storage rule, UC-P14 *a and *a1, UC-P15)
> **Source specs**: `docs/architecture/specs/use-cases.md` (storage rule, UC-P14, UC-P15)
> **Related ADRs**: ADR-0003 (D1, D3), ADR-0004 (D17)
> **Decisions captured**: S1

## Context

Referenced from [03-sequence-restore.md](03-sequence-restore.md). The PIN lives in the encrypted database, so it cannot gate this screen (ADR-0003, OQ-6). An unfinished erase (marker found) is completed before anything else ([02-sequence-erase.md](02-sequence-erase.md)).

Progressive disclosure: only two buttons, "Restore from a file" and "Set up again".

## Diagram

```mermaid
sequenceDiagram
  title sd — Key-loss start (storage rule)
  autonumber
  actor Guardian
  participant PUI as «boundary» StartScreen
  participant Start as «control» StartUp
  participant Keys as «port» Key store
  participant Store as «port» Storage

  Start->>Keys: read the database key
  alt key-store error
    Start->>Keys: retry
  end
  Keys-->>Start: missing, or the key does not open the database
  Start->>Store: set the unreadable database aside (retried at each start for 30 days)
  Start->>PUI: show only Restore from a file and Set up again
  alt Guardian taps Restore from a file
    Guardian->>PUI: tap Restore from a file
    Note over PUI: continues in sd UC-P15 Restore
  else Guardian taps Set up again
    Guardian->>PUI: tap Set up again
    Note over PUI: continues in UC-P14, the set-aside database is retried for 30 days
  end
```

## Notes

- At each later start the set-aside database is retried with the key store; if it opens again within the 30 days, the app offers "Bring back the old data" (UC-P14 *a1: PIN of the old database, its own lockout, one transaction with the UC-P15 rules, replaced data deleted; if no new set-up was completed it simply becomes the database again), otherwise it keeps waiting; after 30 days it is deleted and a SET_ASIDE_DELETED note is raised (ADR-0004 D17).
- A database that SQLCipher does not protect is refused at start-up (ADR-0003 D1), never opened in clear.
