# Sequence diagram — learning — remediation walk-back

> **Feature**: learning domain, UC-L1 extensions 4a and 4b, UC-L5, UC-P7 (V1.1)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-L1, UC-L4, UC-L5, UC-P7)
> **Related ADRs**: ADR-0002 (D9)
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
  participant Ctl as «control» RunSession
  participant Sel as «control» ExercisePicker
  participant Progress as «entity» Progress aggregate
  participant Graph as «entity» Skill graph (static)
  participant Notes as «entity» ParentNote
  participant UI as «boundary» SessionScreen

  alt 3 errors in a row or a failed review (4a)
    Ctl->>Graph: weakest prerequisite of the target skill
    Ctl->>Progress: open Remediation (origin AUTO, target, current)
    Ctl->>Notes: STUCK_SKILL alert
  else Guardian scheduled a skill (4b, UC-P7)
    Ctl->>Progress: open Remediation already stored (origin GUARDIAN)
  end
  Ctl->>UI: "warming up" message, level lowered
  loop until the remediation closes or the session ends, inside the 20 % review share
    Ctl->>Sel: exercise on current
    Ctl->>UI: show the exercise
    Learner->>UI: answer (UC-L2)
    UI->>Ctl: answer
    Ctl->>Progress: mastery of current
    alt mastery of current back at the threshold
      Ctl->>Progress: close Remediation, practice returns to target
      opt origin GUARDIAN
        Ctl->>Notes: REMEDIATION_COMPLETED note
      end
    else still weak after the short run (UC-L5 3a)
      Ctl->>Graph: one more node down (cycle 1, CP or CE1)
      Ctl->>Progress: move current down
      Ctl->>Notes: PREREQUISITE_STILL_WEAK alert
    end
  end
```

## Notes

- The walk-back never leaves the 20 % review share, so the session mix is unchanged.
- An open Remediation survives the end of the session and continues in the next one.
- The graph is static data (curriculum), read only.
