# Use case diagram — parent-space — set-up, monitoring and data control

> **Feature**: parent-space domain of Learn To Earn (Guardian side)
> **Source specs**: `docs/architecture/specs/use-cases.md` (UC-P1 to UC-P15)
> **Related ADRs**: ADR-0001
> **Decisions captured**: P0, P1, P2, C1, C2, M4, R4, S1, T1, V1, V3, V4

## Context

Everything the Guardian does inside the PIN-protected parent space. Approving a request and the screen-time rules are in the `screen-time` diagram. Every use case here except UC-P1, UC-P12 and UC-P14 has the precondition "parent space unlocked" (UC-P1).

## Diagram

```mermaid
flowchart LR
  Guardian["«actor» Guardian - parent"]
  subgraph SYSTEM ["Learn To Earn"]
    subgraph Access ["Parent-space domain - access and set-up"]
      P14(("UC-P14 Set up the app for a child"))
      P12(("UC-P12 Set the parent PIN"))
      P1(("UC-P1 Unlock the parent space"))
      P10(("UC-P10 Change the PIN"))
    end
    subgraph Plan ["Parent-space domain - learning plan"]
      P2(("UC-P2 Create the child profile"))
      P3(("UC-P3 Set the class calendar ceiling"))
      P4(("UC-P4 Allow skills beyond the class period"))
      P7(("UC-P7 Send the child back to an earlier skill"))
      P13(("UC-P13 Request keypad re-calibration"))
    end
    subgraph Monitor ["Parent-space domain - monitoring"]
      P5(("UC-P5 Review the traffic-light dashboard"))
      P6(("UC-P6 Review alerts and the to-do-together list"))
    end
    subgraph Data ["Parent-space domain - data and privacy"]
      P8(("UC-P8 Export the child's data"))
      P9(("UC-P9 Erase all data"))
      P11(("UC-P11 Choose anonymous crash reporting"))
      P15(("UC-P15 Restore the child's data from a file"))
    end
  end
  Guardian --- P14
  Guardian --- P12
  Guardian --- P1
  Guardian --- P10
  Guardian --- P2
  Guardian --- P3
  Guardian --- P4
  Guardian --- P7
  Guardian --- P13
  Guardian --- P5
  Guardian --- P6
  Guardian --- P8
  Guardian --- P9
  Guardian --- P11
  Guardian --- P15
  P14 -.->|"«include»"| P12
  P14 -.->|"«include»"| P2
```

## Notes

- The only relationships are UC-P14 «include» UC-P12 and UC-P2 (first-launch set-up always performs both). Shared access is expressed as the precondition "parent space unlocked" (ADR-0001 D2). UC-P4 and UC-P6 were extensions in a first draft and became standalone goals after review pass 1 (extension points were navigation or states, not points of a scenario).
- UC-P13 and UC-L7 (learning domain) are linked by data, not by a UML relationship.
- UC-P8 (export) and UC-P9 (erase) are legal baselines (privacy by design), not optional features.
- Open point: PIN recovery without letting the child reset it (OQ-1).
- Versions: UC-P3, UC-P4, UC-P6, UC-P7, UC-P11 in V1.1, UC-P13 in V1.2, the others in V1.0 (UC-P14 and UC-P15 included).
