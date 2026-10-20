# ADR-0001 — Use-case modelling approach

- Status: proposed (owner validates weights and choices)
- Date: 2026-10-20
## Context and problem statement

First conception study of Learn To Earn (see `docs/CADRAGE.md`). Conception drives code (UML-first rule). Standards followed: UML 2.5 (use cases, include, extend, actors), Cockburn *Writing Effective Use Cases* (goal-level, verb + observable outcome, textual specs), C4/arc42 for the dossier layout, MADR for this record.

## Considered options and decision drivers

Scores: 0–5 per criterion, weights sum to 100, total out of 500. Scores are our estimates, not measured facts.

## D1 — How to split the use-case diagrams

| Criterion (weight) | A. One global diagram | B. One diagram per domain (3) | C. One diagram per actor |
|---|---|---|---|
| Readability, about 27 use cases (30) | 1 | 5 | 4 |
| UML orthodoxy: group by domain, not by actor or backend (25) | 3 | 5 | 2 |
| Traceability to spec and later diagrams (20) | 4 | 4 | 3 |
| Maintainability (15) | 4 | 3 | 3 |
| Reviewability (10) | 1 | 4 | 3 |
| **Total /500** | 255 | **440** | 305 |

B vs A: A puts 27 ovals and 2 actors in one picture, which nobody can review. B vs C: C regroups by actor, which hides the domain boundaries (the Learner appears in two domains).
Sensitivity (other weights rescaled proportionally): A overtakes B only if maintainability carries about 70 % of the total weight. B stays first for any realistic weighting.
**Decision: B.** Folders `learning/`, `screen-time/`, `parent-space/`, each with `01-use-case.md`.

## D2 — How to use include and extend

| Criterion (weight) | A. Model include/extend where true | B. Flat diagram, no relationships | C. Relationships only in the textual spec |
|---|---|---|---|
| UML fidelity (35) | 5 | 2 | 3 |
| Diagram readability (25) | 3 | 5 | 4 |
| Spec-to-diagram traceability (20) | 5 | 2 | 4 |
| Simplicity (20) | 3 | 5 | 4 |
| **Total /500** | **410** | 335 | 365 |

Sensitivity: moving s weight points from fidelity to simplicity gives A = 410 − 2s, B = 335 + 3s, C = 365 + s. The three tie at 380 for s = 15 (fidelity 20, simplicity 35). A stays first for any s below 15.

**Decision: A**, with strict rules:
- «include»: the base use case always performs the included one (example: approve a request always includes entering the PIN).
- «extend»: a conditional add-on at a named extension point (example: retry with a hint extends answering an exercise when the answer is wrong). The arrow points from the extension to the base.
- A precondition shared by every use case of a package (parent space unlocked) is written as a precondition, not drawn as 10 «include» arrows. «include» is drawn only when the step happens inside the scenario.
- "Then the screen opens" is navigation, never a relationship.
- Linking convention (house rule, not a UML requirement): an extension is linked to an actor only if the actor can start it on their own (read-aloud tap, accepting a challenge). A conditional segment of a goal already started has no direct link and inherits the actor of its base use case.
- Each base use case declares its extension points in the spec, with names identical to the diagram labels.
- An extend condition must be a runtime guard, never a release (V2 is a version tag, not a condition).

## D3 — Which secondary actors to model

| Criterion (weight) | A. TTS engine and device OS | B. None | C. Device OS only (V2 blocker) |
|---|---|---|---|
| UML fidelity (30) | 4 | 3 | 5 |
| Scope fit: no component-level detail in the use-case diagram (30) | 2 | 5 | 4 |
| Usefulness for later diagrams (20) | 4 | 3 | 4 |
| Low clutter (20) | 3 | 5 | 4 |
| **Total /500** | 320 | 400 | **430** |

The native TTS is a library inside the app, not an actor that pursues a goal: it belongs to the component diagram. The device OS that enforces blocking in V2 is a real external system taking part in a scenario.
Sensitivity: moving weight from fidelity to scope fit, C = 430 − s and B = 400 + 2s: they tie at 420 for s = 10 (fidelity 20, scope fit 40), beyond which B wins.

**Decision: C.**

## D4 — System events are not use cases

The following are triggers or behaviours inside scenarios, never ovals (UML 2.5, Cockburn):

| Not a use case | Where it lives instead |
|---|---|
| Receive a parent alert after 3 errors | Extension 4a of UC-L1; read by the Guardian in UC-P6 |
| Pause after a low confidence score | Extension in UC-L2; note read through UC-P6 |
| 5-minute warning, end-of-time alarm | Steps of UC-S3 |
| Debit the reserve | Postcondition of UC-S3 |
| Drop one difficulty level after 3 errors | Step of UC-L1 (engine behaviour, sequence diagram later) |
| Weekly aggregation of old answers | Background behaviour (component and state diagrams later) |
| Send crash report | Consequence of UC-P11, never an actor goal |

## D5 — Goal level

Each use case states its Cockburn level. *Subfunction* use cases (UC-L2, UC-L3, UC-L4, UC-P1) are kept as ovals only because each traces to its own product decision (answering, read-aloud E4, hints M4, PIN P1) and is reused or extended. All others are user goals, or conditional goal segments inheriting the actor of their base (UC-L5, UC-S4).

## D6 — Version tags

Each use case carries the roadmap version where it ships (V1.0, V1.1, V1.2, V2). Diagrams show all use cases; versions appear in the textual spec and the traceability matrix.

## Decision outcome

D1 = B (440), D2 = A (410), D3 = C (430), D4 = table above, D5 = levels as stated, D6 = versions in specs and matrix.

## Consequences

- Diagrams are reviewed per domain and recorded in `docs/architecture/reviews/`.
- Any new use case needs a verb + outcome name, a primary actor and a textual spec before it is drawn.
- Open questions stay listed in `docs/architecture/specs/use-cases.md`.
