# Use case diagram — screen-time — request, approve, use, enforce

> **Feature**: screen-time domain of Learn To Earn (reward conversion and control)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-S1 to UC-S5, UC-P1)
> **Related ADRs**: ADR-0001
> **Decisions captured**: Q1, Q4, Conversion, P0, P1, P3

## Context

Covers how earned minutes become authorised screen time. UC-P1 (parent space) is shown only because UC-S2 includes it. It is defined in the `parent-space` diagram. Does not cover how minutes are earned (see `learning`).

## Diagram

```mermaid
flowchart LR
  Learner["«actor» Learner - child using the app"]
  Guardian["«actor» Guardian - parent"]
  DeviceOS["«actor» DeviceOS - Android, V2"]
  subgraph SYSTEM ["Learn To Earn"]
    subgraph ST ["Screen time"]
      S1(("UC-S1 Request screen time"))
      S2(("UC-S2 Approve a screen-time request"))
      S3(("UC-S3 Use approved screen time"))
      S4(("UC-S4 Enforce the end of screen time on the device"))
      S5(("UC-S5 Configure screen-time rules"))
    end
    subgraph PS ["Parent space"]
      P1(("UC-P1 Unlock the parent space"))
    end
  end
  Learner --- S1
  Learner --- S3
  Guardian --- S2
  Guardian --- S5
  S4 --- DeviceOS
  S2 -.->|"«include»"| P1
  S4 -.->|"«extend» timer ended and blocking permission granted"| S3
```

## Notes

- UC-S1 and UC-S2 are linked by data (a pending request), not by a UML relationship: two actors pursue two separate goals.
- UC-S5 has the precondition "parent space unlocked" (ADR-0001 D2), so no include arrow is drawn.
- UC-S4 is an extension with no direct Learner link (actor inherited from UC-S3, the Guardian is the beneficiary). DeviceOS is its secondary actor. It ships in V2. In V1 the timer is declarative.
- The extension point `timer ended` is declared on UC-S3. The 5-minute warning, the alarm and the reserve debit are steps or postconditions of UC-S3, not use cases (ADR-0001 D4).
- Open point: remote approval on the parent's phone (OQ-2).
