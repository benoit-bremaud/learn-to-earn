# Learn To Earn — design dossier

Conception comes first (UML-first): code conforms to this dossier, never the reverse. Product brief: [../CADRAGE.md](../CADRAGE.md). Curriculum mapping: [../curriculum/CE1-maths.md](../curriculum/CE1-maths.md).

## Standards and method

- UML 2.5 for every diagram, written in Mermaid (docs-as-code). Use cases follow Cockburn's goal-level rules. Mermaid cannot draw native UML use-case shapes: actors are rectangles tagged «actor», use cases are circles, include and extend are dashed arrows labelled with guillemets.
- Layout inspired by arc42 and the C4 model (context, containers, components, code). Decisions recorded as MADR files under `decisions/`.
- Every choice between solutions is analysed with an MCDA matrix (weights /100, scores 0–5, total /500, sensitivity check), recorded in the matching ADR.
- Every study is reviewed at least twice before it is considered stable. Review logs live in `reviews/`: pass 1 checks UML and method conformance, pass 2 checks traceability and coverage against the product decisions. A study is "validated" only after both passes have no open Must Have and the owner has approved it.
- Language: English.

## Contents and status

| # | Item | Location | Status |
|---|---|---|---|
| 1 | Use-case modelling approach | [decisions/0001-use-case-modelling.md](decisions/0001-use-case-modelling.md) | proposed |
| 2 | Use-case specifications (29 use cases) | [specs/use-cases.md](specs/use-cases.md) | draft, in review |
| 3 | Use-case diagram, learning | [diagrams/learning/01-use-case.md](diagrams/learning/01-use-case.md) | draft, in review |
| 4 | Use-case diagram, screen-time | [diagrams/screen-time/01-use-case.md](diagrams/screen-time/01-use-case.md) | draft, in review |
| 5 | Use-case diagram, parent-space | [diagrams/parent-space/01-use-case.md](diagrams/parent-space/01-use-case.md) | draft, in review |
| 6 | Traceability matrix | [traceability-matrix.md](traceability-matrix.md) | started (use cases only) |
| 7 | Reviews | [reviews/](reviews/) | see log |
| 8 | Sequence, component, class, state, data-flow diagrams | `diagrams/<feature>/` | not started |
| 9 | Local pre-push review report | [review-local.md](review-local.md) | maintained by the review gate |

## Planned studies (order)

1. Use cases (this study).
2. Sequence diagrams for non-trivial flows only: learning session with adaptive choice, screen-time request and approval, remediation walk-back, anti-cheat confidence scoring.
3. Component diagram (containers and boundaries: UI, engine, storage, parent space, OS bridge).
4. Class diagram (domain: Skill, Exercise, Attempt, MasteryScore, ConfidenceScore, Reserve, Request).
5. State diagrams (session, screen-time request, reserve lifecycle).
6. Data-flow diagram with sensitive fields flagged (privacy review).
