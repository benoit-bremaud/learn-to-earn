# ADR-0002 — Domain model (analysis level)

- Status: proposed (owner validates weights and choices)
- Date: 2026-10-20

## Context and problem statement

The domain model is the analysis class diagram that fixes the vocabulary before the sequence diagrams (study order in `docs/architecture/README.md`). It shows concepts, attributes, associations and multiplicities, and no operations. It must respect the binding principles: Clean Architecture (these classes are the inner domain, free of any framework), SOLID, DRY, YAGNI and data minimisation (`docs/CADRAGE.md` §4).

Scores: 0–5, weights sum to 100, total out of 500. Scores are estimates.

## D1 — Where the per-skill mastery of a child lives

| Criterion (weight) | A. Association class SkillProgress (child × skill) | B. Attribute on Skill | C. Separate MasteryScore history entity |
|---|---|---|---|
| Correctness: mastery belongs to the pair, not to the skill (35) | 5 | 1 | 4 |
| Simplicity, YAGNI (25) | 4 | 5 | 2 |
| Room for related data (average time, personal record, unlocked level) (20) | 5 | 1 | 4 |
| Supports several children later (OQ-3) without redesign (20) | 5 | 0 | 5 |
| **Total /500** | **475** | 180 | 370 |

B is wrong as soon as a second child exists and mixes curriculum data (static) with learner data (dynamic). C keeps a full history that the weekly aggregates already cover.
Sensitivity: A stays first unless simplicity carries more than about 80 % of the weight (others scaled: A = 500 − w, B ≈ 73 + 4.3w).
**Decision: A.**

## D2 — How the screen-time reserve is modelled

| Criterion (weight) | A. Ledger: credits with expiry, debits as uses | B. Single balance number | C. Event log of every change |
|---|---|---|---|
| Supports 7-day expiry per credit (35) | 5 | 1 | 5 |
| Simplicity (25) | 4 | 5 | 2 |
| Auditability for the Guardian (20) | 4 | 1 | 5 |
| Data minimisation (20) | 4 | 5 | 2 |
| **Total /500** | **435** | 280 | 365 |

With a single balance, a credit earned on Monday cannot expire on the next Monday. The event log stores more than needed.
Sensitivity: A stays first for any expiry weight; with expiry at 0 and the other weights scaled, A ≈ 400 and B ≈ 377.
**Decision: A.** The balance is derived (`/balanceMinutes` = sum of the non-expired credits' `/remainingMinutes`), never stored twice (DRY). Each use records the credits it draws from, oldest first.

## D3 — Scope of the confidence score

| Criterion (weight) | A. One score per session, starting at 1.0 | B. One persistent score per child | C. Per session plus a persistent trend |
|---|---|---|---|
| Fits CADRAGE "starts at 1.0" (30) | 5 | 2 | 4 |
| Child-friendly: a bad day does not follow her (30) | 5 | 1 | 3 |
| Detection power for the Guardian (20) | 3 | 5 | 5 |
| Simplicity (20) | 5 | 4 | 2 |
| **Total /500** | **460** | 270 | 350 |

Repeated low-confidence sessions already reach the Guardian through notes, so A loses little detection power.
Sensitivity: C overtakes A only if detection power weighs more than about 48 % (others scaled: A = 500 − 2d, C ≈ 312 + 1.9d).
**Decision: A.** At analysis level the score is a session attribute `confidence` (a one-attribute class would be YAGNI); it exists from V1.1.

## D4 — How the prerequisite graph is modelled

| Criterion (weight) | A. Self-association on Skill ("requires") | B. Prerequisite edge class with attributes | C. Graph stored outside the model |
|---|---|---|---|
| Expresses the DAG (30) | 5 | 5 | 2 |
| YAGNI: no edge attribute is needed today (30) | 5 | 2 | 3 |
| Readability (20) | 5 | 3 | 2 |
| Extensible (weights later) (20) | 3 | 5 | 2 |
| **Total /500** | **460** | 370 | 230 |

The acyclic constraint is written as an OCL-style note: `{acyclic}`. An edge class is added only if edges get attributes one day.
Sensitivity: B overtakes A only if extensibility weighs more than about 45 %.
**Decision: A.**

## D5 — What is stored about the Guardian

| Criterion (weight) | A. Credential only (PIN hash, lockout state) | B. Guardian person (name, e-mail) | C. Nothing, PIN in OS keystore only |
|---|---|---|---|
| Data minimisation (35) | 5 | 1 | 5 |
| Supports UC-P1, P10, P12 (30) | 5 | 5 | 3 |
| Simplicity (20) | 5 | 3 | 3 |
| Future remote approval (OQ-2) (15) | 3 | 5 | 1 |
| **Total /500** | **470** | 320 | 340 |

C hides the lockout state the domain needs; the storage of the hash itself is an adapter concern (component diagram).
Sensitivity: B overtakes A only if future remote approval weighs more than about 51 %.
**Decision: A.** The Guardian stays an actor, not a persisted person.

## D6 — How the diagram is split

| Criterion (weight) | A. One diagram, about 22 classes | B. One diagram per area with shared stubs | C. One diagram per class cluster of 3–4 |
|---|---|---|---|
| Readability (35) | 1 | 5 | 4 |
| Overall coherence (25) | 5 | 4 | 2 |
| Maintainability (20) | 4 | 4 | 2 |
| Reviewability (20) | 2 | 5 | 3 |
| **Total /500** | 280 | **455** | 290 |

Sensitivity: A overtakes B only if overall coherence weighs more than about 73 %.
**Decision: B.** Four areas: curriculum and progress, practice, rewards, parent space (rewards and parent space were split after the render check showed a tangled layout). A class shared by two areas (ChildProfile, Skill, Strand, Session) appears as a stub without attributes outside its home area.

## D7 — Generalization in the reserve ledger

Credit (minutes added) and ScreenTimeUse (minutes removed) are both movements of the same reserve, each with an amount and a time. The owner rule asks to model inheritance where it really exists.

| Criterion (weight) | A. No generalization | B. Abstract ReserveEntry, Credit and ScreenTimeUse inherit | C. One Entry class with a kind enum |
|---|---|---|---|
| Faithful to the domain: a credit and a use are both movements (30) | 3 | 5 | 3 |
| Simplicity, YAGNI (25) | 5 | 4 | 4 |
| DRY: amount and time defined once (20) | 3 | 5 | 5 |
| Owner rule: inheritance where it really exists (25) | 1 | 5 | 2 |
| **Total /500** | 300 | **475** | 340 |

C hides that only a credit expires and only a use can stop early, so it needs optional attributes that depend on the kind.
Sensitivity: A overtakes B only if simplicity weighs more than about 73 %.
**Decision: B.** No other real generalization exists in the domain: Skill, Exercise and the notes have no sub-kinds with their own attributes today.

## Decision outcome

D1 = A (475), D2 = A (435), D3 = A (460), D4 = A (460), D5 = A (470), D6 = B (455), D7 = B (475).

## Consequences

- These classes form the pure domain layer: no Expo, storage or OS type may appear in them.
- Thresholds (80 % success zone, 0.6 / 0.3 confidence, 70 % unlock, caps) stay in configuration, not as class constants.
- Operations, ports and design-level generalizations (generators, adapters) are decided in the design class diagram, after the sequences.
