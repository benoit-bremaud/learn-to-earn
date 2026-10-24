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

Revised after the adversarial review (docs/architecture/reviews/domain-model-review-3.md): the first matrix compared a ledger with a single number and an event log, which is the same thing as the ledger. The real alternatives are below.

| Criterion (weight) | A. Credits and uses with an allocation class Draw | B. Remaining minutes per earning day (at most 7 buckets) | C. Credits and uses, balance replayed oldest first |
|---|---|---|---|
| Exact expiry of each earned minute (30) | 5 | 4 | 5 |
| Simplicity (25) | 2 | 5 | 4 |
| Auditability for the Guardian (15) | 5 | 2 | 4 |
| Data minimisation (15) | 3 | 5 | 5 |
| Testability of the engine (15) | 4 | 5 | 3 |
| **Total /500** | 380 | 425 | **430** |

B expires a whole day at once (day granularity instead of the minute), which is invisible for a 7-day rule. Uses are still recorded, so the Guardian sees what was watched; only the per-credit allocation disappears.
Sensitivity (totals recomputed after review of PR #3; the first version read 375 / 440 / 430 by mistake): C leads by 5 points, a near tie. B wins if simplicity weighs at least 29 %, testability at least 18 %, auditability at most 12 % or exact expiry at most 26 % (others scaled); A never leads.
**Decision (owner, 2026-10-21, revised after the corrected totals): C.** The first decision (B) rested on the wrong totals. The model keeps ReserveCredit and ScreenTimeUse; `/balanceMinutes` is replayed oldest first over the unexpired credits. Minutes cut by the reserve cap are recorded in `forfeitedMinutes`, not lost silently.

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
**Decision: B.** Areas: curriculum and progress, practice, rewards, companion (3b), parent space and installation. Rewards, companion and parent space were split after render checks showed crossing lines; long constraints moved to a numbered list outside the diagrams. A class shared by two areas (ChildProfile, Skill, Strand, Session) appears as a stub without attributes outside its home area.

## D7 — Generalization in the reserve

The first version of this decision (abstract ReserveEntry over Credit and ScreenTimeUse, 475) used weights that rewarded the conclusion twice (faithfulness and the owner rule measured the same thing) and no rule used the supertype polymorphically. The test that counts is substitutability: does a rule treat both kinds uniformly?

| Criterion (weight) | A. No generalization | B. Abstract ReserveEntry |
|---|---|---|
| A rule uses both kinds uniformly (substitutability) (40) | 5 | 1 |
| Faithful to the domain (25) | 4 | 3 |
| Simplicity, YAGNI (20) | 5 | 3 |
| Owner rule: inheritance where it really exists (15) | 4 | 2 |
| **Total /500** | **460** | 205 |

With D2 = C, credits and uses are both reserve movements, but they share no rule: a credit is capped and expires, a use is bounded by its request. A common superclass would carry no behaviour.
**Decision: A, no generalization in the domain.** Inheritance will be re-examined in the design class diagram (generators, adapters), where it may be real.

## D8 — Which quantity feeds the reserve (owner, 2026-10-21)

| Criterion (weight) | A. Weighted minutes: response time x difficulty multiplier x confidence factor | B. Raw minutes only | C. Two currencies (points and minutes) |
|---|---|---|---|
| Consistent with CADRAGE D2, T2, Conversion (35) | 5 | 3 | 1 |
| Simplicity (25) | 3 | 5 | 1 |
| Real effect of effort and anti-cheat (25) | 5 | 1 | 3 |
| Testability of the engine (15) | 4 | 5 | 2 |
| **Total /500** | **435** | 330 | 165 |

**Decision: A.** Each attempt stores two frozen snapshots, `confidenceAtAnswer` and `weightedMinutes`, because the confidence changes during the session (snapshots taken at event time are the stated exception to "derive, never store"). The conversion uses the weighted minutes of the day.

## D9 — Rule for unlocking a difficulty level (owner, 2026-10-21)

| Criterion (weight) | A. Skill mastery at least 70 % unlocks the next level | B. Mastery tracked per level |
|---|---|---|
| Faithful to the text of CADRAGE (30) | 3 | 5 |
| Simplicity, YAGNI (30) | 5 | 2 |
| Testability (20) | 4 | 5 |
| Data minimisation (20) | 5 | 3 |
| **Total /500** | **420** | 370 |

**Decision: A.** `unlockedLevel` becomes derived. CADRAGE §3 ("a level unlocks once the previous one reaches 70 % mastery") is restated as a skill-level rule and must be edited accordingly. Sensitivity: B overtakes A only if fidelity to the text weighs more than about 44 % (others scaled).

## D10 — Scope of the full-rate threshold (OQ-4, owner, 2026-10-21)

| Criterion (weight) | A. Per day | B. Per session |
|---|---|---|
| Resists splitting work into many sessions (40) | 5 | 2 |
| Simplicity (30) | 3 | 5 |
| Fairness for the child (30) | 3 | 4 |
| **Total /500** | **380** | 350 |

**Decision: A.** It adds the day notion (`LocalDay`, from the trusted time).

## D11 — What earns screen time (owner, 2026-10-21)

Raised by the owner after D8: the goal is to make the child work and learn, with learning results that are good and rising, not to pay time spent watching videos.

| Criterion (weight) | A. Keep D8: response time x difficulty x confidence, wrong answers included | B. Correct answers only, plus a bonus when mastery rises | C. Mastery gain only |
|---|---|---|---|
| Learning results good and rising (35) | 2 | 4 | 5 |
| Fair to a struggling child, effort rewarded (25) | 4 | 4 | 2 |
| Resistance to gaming (20) | 3 | 4 | 4 |
| Simplicity (20) | 5 | 3 | 2 |
| **Total /500** | 330 | **380** | 345 |

Sensitivity: C leads only if learning results weigh more than about 50 % (others scaled); a plateau would then earn nothing, against "effort first".
**Decision (owner, 2026-10-21): B.** It refines D8 (one currency, weighted minutes): a wrong attempt earns 0, and at session end each skill whose mastery rose adds `progressBonusRatio` x the weighted minutes earned on it. The same day the owner set the default reserve cap to 60 min (reserve-cap matrix: 60 min 400, 120 min 400, 210 min 320; the 60/120 tie was broken by the incentive to work).

## D12 — Scope of the erase (UC-P9, OQ-5 part 1)

| Criterion (weight) | A. Child data only (PIN, consent, rules kept) | B. Everything, set-aside databases and key included, then back to UC-P14 | C. The Guardian chooses at erase time |
|---|---|---|---|
| Privacy and completeness (35) | 3 | 5 | 5 |
| Consistent states (`Installation` serves 1..* children) (25) | 3 | 5 | 2 |
| Progressive disclosure, few controls (20) | 5 | 5 | 1 |
| Guardian convenience (20) | 4 | 3 | 5 |
| **Total /500** | 360 | **460** | 345 |

A leaves an Installation with no child and a consent given for another child. Sensitivity: A leads only if convenience weighs more than about 55.
**Decision: B** (owner, 2026-10-23). The erase deletes the database, every database set aside after a key loss, and the key, then restarts on the set-up.

## D13 — Restore guard (UC-P15, OQ-5 part 2)

An old export holds minutes that may have been spent since.

| Criterion (weight) | A. Refuse an export older than the current data | B. Replay the balance against TimeGuard | C. Restore without the reserve (balance 0, progress restored) |
|---|---|---|---|
| No minute spent twice (35) | 2 | 3 | 5 |
| Fairness on a genuine restore (20) | 4 | 5 | 2 |
| Simplicity (25) | 4 | 3 | 5 |
| Consistency with the domain (20) | 3 | 5 | 4 |
| **Total /500** | 310 | 380 | **420** |

A is void after a key loss (no current data to compare). B still brings back minutes spent after the export. C loses at most the reserve cap (60 min by default) in a rare case. Sensitivity: B leads if fairness weighs more than about 45.
**Decision: C** (owner, 2026-10-23). The file's credits are kept as history with all their remaining minutes moved to `forfeitedMinutes` (balance 0), so the crediting checkpoints (C7) and the day's full-rate and cap counters survive and an interrupted session is never credited twice. Open requests are closed: PENDING or APPROVED become EXPIRED, an IN_USE request is closed with its full minutes debited. `TimeGuard.lastTrustedAt` becomes the later of the file's and the device's, so a restore can never move trusted time back.

## D14 — Answer still wrong after the third hint (UC-L4, sequence review)

| Criterion (weight) | A. Show the correct answer with the worked step, then move on, no point | B. Retry until correct | C. Move on silently |
|---|---|---|---|
| Learning value (40) | 5 | 2 | 1 |
| No frustration (30) | 4 | 1 | 4 |
| Simplicity (15) | 4 | 5 | 5 |
| Resistance to gaming (15) | 4 | 5 | 3 |
| **Total /500** | **440** | 260 | 280 |

Sensitivity: A leads under any plausible weighting. **Decision: A** (owner, 2026-10-24).

## D15 — Earning of a correct answer after hints (sequence review)

| Criterion (weight) | A. 0, only a first-try answer earns | B. Decreasing fraction per hint stage, in configuration (×0.5, ×0.25, 0) | C. Full value |
|---|---|---|---|
| Pushes real learning, the product goal (40) | 3 | 5 | 1 |
| Resistance to guessing through hints (25) | 5 | 4 | 0 |
| Recognises the child's effort (20) | 1 | 4 | 5 |
| Simplicity (15) | 5 | 3 | 5 |
| **Total /500** | 340 | **425** | 215 |

A discourages the hints, which are the learning tool. Sensitivity: A leads only if resistance to gaming weighs more than about 45. **Decision: B** (owner, 2026-10-24). The factor is a frozen part of `Attempt.weightedMinutes` (C9).

## Decision outcome

D1 = A (475), D2 = C (430), D3 = A (460), D4 = A (460), D5 = A (470), D6 = B (455), D7 = A (460), D8 = A (435), D9 = A (420), D10 = A (380), D11 = B (380), D12 = B (460), D13 = C (420), D14 = A (440), D15 = B (425).

Honest limits found by the adversarial review: D1 option C, D3 option B and D5 option C were weak alternatives (D3 B contradicts CADRAGE and should have been excluded, not scored); D6 is a layout choice that did not need a matrix. They do not change their outcomes. Aggregate boundaries, the time policy and the retention scopes are now part of the model (see "Aggregates" in the diagram file) and should get their own ADR when the component diagram fixes the storage boundary.

## Consequences

- These classes form the pure domain layer: no Expo, storage or OS type may appear in them.
- Thresholds (80 % success zone, 0.6 / 0.3 confidence, 70 % unlock, caps, multipliers) stay in configuration, not as class constants.
- CADRAGE §3 must be edited for D9 and for the weighted-minutes currency (D8).
- Operations, ports and design-level generalizations (generators, adapters) are decided in the design class diagram, after the sequences.
- All persisted aggregates, `ParentCredential.pinHash` included, are encrypted at rest (owner requirement, ADR-0003): a storage adapter concern, not a domain attribute.
- 2026-10-23 alignment with the use-case spec: `ScreenTimeRules.sessionTargetMinutes` (session end), `/usedMinutes` derived from device time since `startedAt` with a full debit on a backwards clock (`elapsedSeconds` removed), base level scores and the dotted `SkillId` format stated in the diagram notes.
- OQ-5 closed by D12 and D13 (sequence study, issue #13).
