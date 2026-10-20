# Learn To Earn — design dossier

Conception comes first (UML-first): code conforms to this dossier, never the reverse. Product brief: [../CADRAGE.md](../CADRAGE.md). Curriculum mapping: [../curriculum/CE1-maths.md](../curriculum/CE1-maths.md).

## Standards and method

- UML 2.5 for every diagram, written in Mermaid (docs-as-code). Use cases follow Cockburn's goal-level rules. Mermaid cannot draw native UML use-case shapes: actors are rectangles tagged «actor», use cases are circles, include and extend are dashed arrows labelled with guillemets.
- Layout inspired by arc42 and the C4 model (context, containers, components, code). Decisions recorded as MADR files under `decisions/`.
- Every choice between solutions is analysed with an MCDA matrix (weights /100, scores 0–5, total /500, sensitivity check), recorded in the matching ADR.
- Every study is reviewed at least twice before it is considered stable. Review logs live in `reviews/`: pass 1 checks UML and method conformance, pass 2 checks traceability and coverage against the product decisions. Every diagram is also rendered (`mmdc`) and inspected visually before each commit: overlapping titles, unreadable labels and crossing arrows are defects. A study is "validated" only after both passes have no open Must Have and the owner has approved it.
- Language: English.

## Design principles (binding, owner rule 2026-10-20)

Every diagram and every line of code must respect these principles. Reviews check them explicitly.

- **Clean Architecture, dependency rule.** The domain (skill graph, exercise generators, mastery, confidence, reserve, conversion) is pure TypeScript and imports nothing from Expo, React Native, storage or the OS. Use cases depend on the domain only. Adapters (storage, text-to-speech, clock, OS blocking in V2) implement ports owned by the inner layers. Frameworks stay at the edge.
- **Proportional layering.** A port/adapter seam is added only where a real boundary exists (storage, clock, TTS, OS, export file). No empty layers, no interface with a single trivial implementation unless it isolates an external system or makes the domain testable.
- **SOLID.** One reason to change per module (S). New skills and generators are added without editing the engine (O, for example a registry of skill nodes). Adapters are substitutable (L). Small ports (I). Inner layers depend on abstractions they own (D).
- **No anti-patterns.** Refused: god objects or god services, business rules in UI components or hooks, framework types leaking into the domain, mutable global singletons, service locators, magic numbers (thresholds live in configuration, CADRAGE §3), copy-pasted generators, speculative generality.
- **DRY.** One source of truth per rule: thresholds and weights in configuration, the skill graph in one data structure, decisions in `docs/CADRAGE.md` and ADRs. A little duplication beats the wrong abstraction.
- **YAGNI.** Build only what the current roadmap version needs. Future features (sync, reading, Android blocking) are kept as ports or notes, not as code.

## Contents and status

| # | Item | Location | Status |
|---|---|---|---|
| 1 | Use-case modelling approach | [decisions/0001-use-case-modelling.md](decisions/0001-use-case-modelling.md) | proposed |
| 2 | Use-case specifications (29 use cases) | [specs/use-cases.md](specs/use-cases.md) | reviewed twice, awaiting owner validation |
| 3 | Use-case diagram, learning | [diagrams/learning/01-use-case.md](diagrams/learning/01-use-case.md) | reviewed twice, awaiting owner validation |
| 4 | Use-case diagram, screen-time | [diagrams/screen-time/01-use-case.md](diagrams/screen-time/01-use-case.md) | reviewed twice, awaiting owner validation |
| 5 | Use-case diagram, parent-space | [diagrams/parent-space/01-use-case.md](diagrams/parent-space/01-use-case.md) | reviewed twice, awaiting owner validation |
| 6 | Traceability matrix | [traceability-matrix.md](traceability-matrix.md) | use cases and classes |
| 7 | Reviews | [reviews/](reviews/) | see log |
| 8 | Domain model approach | [decisions/0002-domain-model.md](decisions/0002-domain-model.md) | proposed |
| 9 | Domain model (analysis class diagrams) | [diagrams/domain/01-class-domain-model.md](diagrams/domain/01-class-domain-model.md) | reviewed twice, awaiting owner validation |
| 10 | Sequence, component, design class, state, data-flow diagrams | `diagrams/<feature>/` | not started |
| 11 | Local pre-push review report | [review-local.md](review-local.md) | maintained by the review gate |

## Planned studies (order)

Order follows Larman (Unified Process) and ICONIX: an analysis-level domain model fixes the vocabulary before the sequences, and the design class diagram comes after them (owner decision 2026-10-20, MCDA 500/500).

1. Use cases (done, in review).
2. Domain model: analysis class diagram, concepts, attributes, associations, multiplicities, no methods (done, in review).
3. Sequence diagrams for non-trivial flows only: learning session with adaptive choice, screen-time request and approval, remediation walk-back, confidence scoring.
4. Component diagram (layers and boundaries: UI, application, domain, adapters for storage, clock, TTS, OS).
5. Design class diagram: operations, ports and adapters, dependencies, generalization where real.
6. State diagrams (session, screen-time request, reserve lifecycle).
7. Data-flow diagram with sensitive fields flagged (privacy review).
8. User stories for V0 and V1.0, derived from the use cases, with Given/When/Then acceptance criteria (they become the engine's TDD tests), reviewed twice. Stories of later versions are written just before each version (owner decision 2026-10-20, MCDA 460/500).
9. GitHub issues (one per story or brick) and the project board, then V0 code.
