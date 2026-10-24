# Sequence diagram — learning — confidence scoring

> **Feature**: learning domain, UC-L2 extensions 3b and 3c, UC-L1 extension 4c (V1.1)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-L1, UC-L2)
> **Related ADRs**: ADR-0002 (D3, D8)
> **Decisions captured**: T2, M2

## Context

Detail of the "record attempt" step of [02-sequence-learning-session.md](02-sequence-learning-session.md) once confidence exists (V1.1). Confidence starts at 1.0 in every session and is never shown to the child as an accusation.

Progressive disclosure: the neutral message appears only when confidence is below 0.6, the pause screen only below 0.3. Nothing about confidence is shown otherwise.

## Diagram

```mermaid
sequenceDiagram
  title sd — UC-L2 Confidence scoring (3b, 3c) and UC-L1 4c
  autonumber
  actor Learner
  participant UI as «boundary» SessionScreen
  participant Ctl as «control» RunSession
  participant Conf as «control» ConfidenceScorer
  participant Practice as «entity» Session aggregate
  participant Progress as «entity» Progress aggregate
  participant Notes as «entity» ParentNote

  Learner->>UI: type answer, tap OK
  UI->>Ctl: answer and responseTimeMs
  Ctl->>Progress: personal averageTimeMs of the skill
  Ctl->>Conf: score (responseTimeMs, averageTimeMs)
  alt faster than 40 % of the average and under 1.5 s
    Conf-->>Ctl: confidence lowered
  else plausible time
    Conf-->>Ctl: confidence unchanged or recovering
  end
  Ctl->>Practice: record attempt with confidenceAtAnswer and weightedMinutes frozen
  alt confidence below 0.3
    Ctl->>Practice: status PAUSED
    Ctl->>Notes: LOW_CONFIDENCE_PAUSE note (neutral wording)
    Ctl->>UI: 2-minute calm pause, no button but the timer
    Note over Ctl,UI: 2 minutes of app time (clock port)
    Ctl->>Practice: status RUNNING
  else confidence below 0.6
    Ctl->>UI: neutral message, next exercise easier
  else confidence 0.6 or more
    Ctl->>UI: normal feedback
  end
```

## Notes

- Points of a correct answer are multiplied by the confidence factor; a wrong answer earns 0 (ADR-0002 D11).
- PAUSED time counts in the session length, so a pause never lengthens the session (domain C6), and `workedSeconds` does not grow during it.
- The note is for the Guardian (UC-P6); the child never sees a word about speed or cheating.
