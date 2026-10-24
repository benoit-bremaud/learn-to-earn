# Sequence diagram — learning — credit the reserve

> **Feature**: learning domain, crediting step of UC-L1 (main scenario step 6, extensions *a and *b)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-L1 business rule)
> **Related ADRs**: ADR-0002 (D2, D8, D10, D11), ADR-0004 (D1, D6, D10)
> **Decisions captured**: Conversion, Q4

## Context

Referenced from [02-sequence-learning-session.md](02-sequence-learning-session.md) at every session close or interruption. Domain constraints C7 and C10 hold the rules. No UI: the recap is shown by the caller.

## Diagram

```mermaid
sequenceDiagram
  title sd — Credit the reserve (UC-L1 step 6, *a, *b)
  autonumber
  participant Ctl as «control» RunSession
  participant Practice as «entity» Session aggregate
  participant Progress as «entity» Progress aggregate
  participant Reserve as «entity» Reserve aggregate
  participant Clock as «port» Clock and TimeGuard
  participant Store as «port» Storage

  Ctl->>Reserve: checkpoint of this session
  Reserve-->>Ctl: highest weightedUpTo of its credits, 0 if none
  Ctl->>Practice: attempts after the checkpoint
  Practice-->>Ctl: weighted minutes split per LocalDay of answeredAt
  opt final close (COMPLETED or STOPPED_EARLY), never at an interruption
    Ctl->>Progress: skills whose mastery beats bestMastery by 5 points or more
    Progress-->>Ctl: progress bonus (bonusMinutes per skill, ADR-0004 D6)
  end
  Ctl->>Clock: trusted now
  loop each LocalDay with uncredited minutes
    Ctl->>Reserve: credit(day, weighted minutes, weightedUpTo)
    Reserve->>Reserve: convert (full rate up to fullRateMinutes for the day, then reducedRatio)
    Reserve->>Reserve: cut to reserveCapMinutes headroom, the rest to forfeitedMinutes
  end
  Ctl->>Store: save Reserve (credits and checkpoint in one write)
```

## Notes

- Idempotent (C7): `(sourceSession, weightedUpTo)` is unique, so a retry after a kill writes nothing twice. The bonus is its own credit at the final close, so killing the app never multiplies it.
- The full-rate threshold counts the whole day across sessions, so splitting work never changes the minutes earned.
- `expiresAt` is frozen per credit from its own earning day (C10).
