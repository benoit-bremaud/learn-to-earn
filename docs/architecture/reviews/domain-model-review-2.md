# Review 2 — domain model, coverage and traceability

- Date: 2026-10-20
- Reviewer: independent agent (Claude Opus 5.5), read-only
- Scope: domain model against the 29 use cases, `docs/CADRAGE.md`, `docs/curriculum/CE1-maths.md`, at commit d66a713
- Result: 3 Must, 11 Should, 6 Nice. No orphan class. All Must and Should resolved; one open question raised (OQ-4).

| # | Sev. | Finding | Resolution |
|---|---|---|---|
| 1 | Must | Composition note contradicts the drawing (same as review 1 #1) | Resolved there |
| 2 | Must | `NoteKind`, `Trend`, `AnswerFormat`, value types undefined | Enumerations traced to M4, T1, T2, C1, UC-S3, clock rule, UC-L5; value types listed |
| 3 | Must | UC-P13 re-calibration request has no data | `KeypadProfile.recalibrationRequested` |
| 4 | Should | No version tags on concepts; confidence mandatory in V1.0 | Version column in the dictionary; `confidence [0..1]`, V1.1 |
| 5 | Should | Multipliers and points × confidence have no home | `Attempt./points` derived, values in configuration |
| 6 | Should | Minutes of work not computable (pauses) | `Session.workedMinutes`; per-session vs per-day threshold left as OQ-4 for the owner |
| 7 | Should | Spaced review has no scheduling data | `SkillProgress.lastPractisedAt`, `nextReviewAt` |
| 8 | Should | FluenceBenchmark spans several skills | `Skill "1..*" -- "0..1" FluenceBenchmark`, `label` |
| 9 | Should | `period` meaningless for prerequisite nodes | `period [0..1]` |
| 10 | Should | Locked companion items not expressible | CompanionItem is a static catalogue, unlock derived, `equipped` association |
| 11 | Should | `0..*` attempts (interrupted exercise) | Fixed (review 1 #10) |
| 12 | Should | Floating classes | Fixed (review 1 #9) |
| 13 | Should | No proof of parental consent | `PrivacySettings.consentConfirmedAt` |
| 14 | Should | Incomplete "Decisions captured"; no self-correction measure | Header completed; `KeypadProfile.selfCorrectionRate` |
| 15 | Nice | "7 days" hard-coded in the dictionary | "after `expiryDays` (default 7)" |
| 16 | Nice | One pending request at a time | Constraint in the Reserve note |
| 17 | Nice | `GradeLevel.CYCLE1` is a cycle | Note added |
| 18 | Nice | Strand subject for reading | Accepted limit (YAGNI), noted |
| 19 | Nice | Integer answers vs fractions | Accepted limit, noted |
| 20 | Nice | Note not traceable to its session | `ParentNote -- Session : raisedIn` |

The "Class" column of `traceability-matrix.md` is filled from this review's proposal, adjusted to the final names.
