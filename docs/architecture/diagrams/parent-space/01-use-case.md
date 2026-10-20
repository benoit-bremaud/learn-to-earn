# Use case diagram — parent-space — set-up, monitoring and data control

> **Feature**: parent-space domain of Learn To Earn (Guardian side)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-P1 to UC-P11)
> **Related ADRs**: ADR-0001
> **Decisions captured**: P1, P2, C1, C2, R4, S1, V1, V3, V4

## Context

Everything the Guardian does inside the PIN-protected parent space. Approving a request and the screen-time rules are in the `screen-time` diagram. Every use case here has the precondition "parent space unlocked" (UC-P1).

## Diagram

```mermaid
flowchart LR
  Guardian(("Guardian - parent"))
  subgraph SYSTEM ["Learn To Earn"]
    subgraph Access ["Parent-space domain - access"]
      P1(("UC-P1 Unlock the parent space"))
      P10(("UC-P10 Change the PIN"))
    end
    subgraph Plan ["Parent-space domain - learning plan"]
      P2(("UC-P2 Create the child profile"))
      P3(("UC-P3 Set the class calendar ceiling"))
      P4(("UC-P4 Allow skills beyond the class period"))
      P7(("UC-P7 Send the child back to an earlier skill"))
    end
    subgraph Monitor ["Parent-space domain - monitoring"]
      P5(("UC-P5 Review the traffic-light dashboard"))
      P6(("UC-P6 Review alerts and the to-do-together list"))
    end
    subgraph Data ["Parent-space domain - data and privacy"]
      P8(("UC-P8 Export the child data"))
      P9(("UC-P9 Erase all data"))
      P11(("UC-P11 Choose anonymous crash reporting"))
    end
  end
  Guardian --> P1
  Guardian --> P10
  Guardian --> P2
  Guardian --> P3
  Guardian --> P7
  Guardian --> P5
  Guardian --> P8
  Guardian --> P9
  Guardian --> P11
  P4 -.->|"extend: ceiling set"| P3
  P6 -.->|"extend: dashboard open"| P5
```

## Notes

- UC-P4 and UC-P6 are extensions with no direct actor link, for the same reason as in the learning diagram.
- UC-P9 (erase) and UC-P8 (export) are legal baselines (privacy by design), not optional features.
- Open point: PIN recovery without letting the child reset it (OQ-1).
- UC-P3, UC-P4, UC-P6, UC-P7 and UC-P11 ship in V1.1, the others in V1.0.
