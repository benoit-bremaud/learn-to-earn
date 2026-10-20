# Review pass 1 — use-case study (UML 2.5 and Cockburn conformance)

- Date: 2026-10-20. Reviewer: independent agent (Opus), read-only, adversarial. Lens: UML 2.5, Cockburn, ADR arithmetic.
- Target: commit 58b0b94. Result: 7 Must, 14 Should, 9 Nice. Verdict at the time: not ready to validate.

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | Must | 24 use cases announced, 25 defined | Fixed (27 after the additions of row 19) |
| 2 | Must | UC-L3 version wrong in the learning note | Fixed (V1.2) |
| 3 | Must | UC-P8 name differs between diagram and spec | Fixed ("Export the child's data" everywhere) |
| 4 | Must | UC-P6 extends UC-P5 on a navigation point | Fixed: standalone use case, Guardian link |
| 5 | Must | UC-L6 should be include (condition always true) | Fixed differently: the Learner can accept or decline the offered challenge, so the extension is a real optional guard and has an actor link |
| 6 | Must | UC-S1 precondition contradicts extension 1a | Fixed: precondition removed, 2a guards |
| 7 | Must | D2 and D3 lacked sensitivity checks, D1 figure inaccurate | Fixed (D1: about 70 %, D2 tie at s = 15, D3 tie at s = 10) |
| 8 | Should | D1 sensitivity figure | Same as 7 |
| 9 | Should | UC-S4 primary actor | Fixed: actor inherited from UC-S3, beneficiary stated |
| 10 | Should | UC-S4 extend condition mixes release and guard | Fixed: "timer ended and blocking permission granted" |
| 11 | Should | Extension points not declared on bases | Fixed: field added to UC-L1, L2, S3 |
| 12 | Should | UC-L5 extension 1a is a second trigger | Fixed: UC-L1 extensions 4a and 4b share the point |
| 13 | Should | Wording for UC-L5 and UC-L6 actors | Fixed (inherited actor stated) |
| 14 | Should | "No actor link" rule is a house convention | Fixed: ADR-0001 D2 rephrased as convention |
| 15 | Should | UC-P4 extends UC-P3 on a state | Fixed: standalone use case |
| 16 | Should | Granularity: UC-L3, L4, P1 are subfunctions | Fixed: Level field and ADR D5 justification |
| 17 | Should | Constraints written as extensions | Fixed: moved to business rules |
| 18 | Should | Cockburn fields missing, steps not numbered | Fixed: every spec rewritten with the full template |
| 19 | Should | Missing use cases (set PIN, request re-calibration) | Fixed: UC-P12 and UC-P13 added |
| 20 | Should | Actors and use cases look alike | Fixed: «actor» rectangles, README note on Mermaid limits |
| 21 | Should | "P1" clash (decision, period, use case) | Fixed: "dec. P1", "period 1–5", "UC-P1" |
| 22 | Nice | Actor links with arrowheads | Fixed (undirected) |
| 23 | Nice | No guillemets on relationships | Fixed |
| 24 | Nice | UC-S2 extensions out of order, PIN logic duplicated | Fixed |
| 25 | Nice | Reserve debit as a step | Fixed: postcondition |
| 26 | Nice | Circular precondition note | Fixed ("except UC-P1 and UC-P12") |
| 27 | Nice | Non-ID in decisions header | Fixed ("Conversion") |
| 28 | Nice | Naming "my", joined outcomes in UC-L8 | Fixed |
| 29 | Nice | ADR not in MADR layout | Fixed: headings added |
| 30 | Nice | Long labels in circles | Disagree: all three diagrams render cleanly with `mmdc`, kept as is |

Arithmetic of all MCDA totals was checked by the reviewer and found correct.
