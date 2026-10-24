# Sequence diagram — learning — remediation walk-back

> **Feature**: learning domain, UC-L1 extensions 4a and 4b, UC-L5, UC-P7 (V1.1)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-L1, UC-L4, UC-L5, UC-P7)
> **Related ADRs**: ADR-0002 (D9), ADR-0004 (D3, D11, D12)
> **Decisions captured**: R4, M4, C3

## Context

How the session walks down the prerequisite graph when a prerequisite is weak, or when the Guardian scheduled a skill (UC-P7), and how it comes back. Domain constraint C4: exercises practise `current`, and the remediation closes when the mastery of `current` is back at the threshold.

Progressive disclosure: the child sees only "warming up" and the usual exercise screen; the Guardian alert is shown in UC-P6, never on the child screen.

## Diagram

```mermaid
sequenceDiagram
  title sd — UC-L5 Rework an earlier skill (UC-L1 4a, 4b)
  autonumber
  actor Learner
  participant UI as «boundary» SessionScreen
  participant Ctl as «control» RunSession
  participant Sel as «control» ExercisePicker
  participant Progress as «entity» Progress aggregate
  participant Graph as «entity» Skill graph (static)
  participant Notes as «entity» ParentNote

  alt 3 exercises in a row failed at the first try, or a failed review (4a)
    Ctl->>Graph: weakest prerequisite of the target skill
    Ctl->>Progress: open Remediation (origin AUTO, target, current)
    Ctl->>Notes: STUCK_SKILL alert
  else Guardian scheduled a skill (4b, UC-P7)
    Ctl->>Progress: open Remediation already stored (origin GUARDIAN, no target)
    Note over Ctl,Sel: right after the warm-up, a block of 5 exercises on current, then the review share
  end
  Ctl->>UI: "warming up" message, level lowered
  loop until the remediation closes or the session ends, inside the 20 % review share
    Ctl->>Sel: exercise on current
    Ctl->>UI: show the exercise
    Learner->>UI: answer (UC-L2)
    UI->>Ctl: answer
    Ctl->>Progress: mastery of current
    alt at least 5 exercises and mastery of current back at 70 %
      Ctl->>Progress: close Remediation, practice returns to target or the normal mix
      opt origin GUARDIAN
        Ctl->>Notes: REMEDIATION_COMPLETED note
      end
    else at least 5 exercises, still below 70 % and current has no prerequisite (UC-L5 3b)
      Ctl->>Notes: TO_DO_TOGETHER note (once), practice stays on current until the session ends, Remediation kept open
    else at least 5 exercises and still below 70 % (UC-L5 3a)
      Ctl->>Graph: one more node down (cycle 1, CP or CE1)
      Ctl->>Progress: move current down
      Ctl->>Notes: PREREQUISITE_STILL_WEAK alert
    end
  end
```

## Notes

- `exercisesDone` resets to 0 at each step-down, so every node gets at least 5 exercises. The step-down and the TO_DO_TOGETHER branches fire only after at least 5 exercises (exercisesDone >= 5) still below 70 %; the TO_DO_TOGETHER note is raised once per remediation.
- The walk-back never leaves the 20 % review share, so the session mix is unchanged, except the 5-exercise opening block of a Guardian request (ADR-0004 D11).
- The 3-error rule counts exercises, not tries: the hint loop of one exercise is one error (ADR-0004 D3).
- At the graph floor (UC-L5 3b) the loop ends only with the session; the Remediation stays open for the Guardian (UC-P6), so the walk-back never goes below the floor.
- An open Remediation survives the end of the session and continues in the next one.
- The graph is static data (curriculum), read only.
