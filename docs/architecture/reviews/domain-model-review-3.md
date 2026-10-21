# Review 3 — domain model, re-check and adversarial critique

- Date: 2026-10-21
- Reviewers: independent agents (Claude Opus 5.5), read-only: a re-check of reviews 1–2 and an adversarial domain-modelling critique
- Scope: commit 39433e0
- Result: re-check found no residual Must (2 Should, 4 Nice). The adversarial critique found 8 Must, 10 Should, 5 Nice, mostly semantic: engine rules that the model could not express. Four owner decisions taken on 2026-10-21 (ADR-0002 D2 revised, D8, D9, D10).

| # | Sev. | Finding | Resolution |
|---|---|---|---|
| A-M1 | Must | Points and minutes were two disconnected currencies | ADR-0002 D8: one currency, weighted minutes |
| A-M2 | Must | `/points` not derivable, confidence moves during a session | `Attempt.confidenceAtAnswer` and `weightedMinutes` stored as frozen snapshots |
| A-M3 / R-S1 | Must | Use-to-credit allocation without amounts | ADR-0002 D2 revised: day buckets (B, 440); no allocation needed |
| A-M4 | Must | No day concept, request lifecycle could break the daily cap | `LocalDay`, full `RequestStatus`, constraint C12 |
| A-M5 | Must | Clock-change rule not expressible | `TimeGuard` (C16) |
| A-M6 | Must | 70 % unlock rule had no per-level mastery | ADR-0002 D9: rule restated per skill, `/unlockedLevel` derived (C2), CADRAGE §3 edited |
| A-M7 | Must | Difficulty reduced to the enum | `Exercise.difficultyScore`, `/difficulty` (C8) |
| A-M8 | Must | No aggregate boundaries, ChildProfile as god composite | "Aggregates" section; references by identifier between aggregates |
| A-S1 | Should | Session lifecycle unclear | `STOPPED_EARLY`, `workedSeconds`, `day`, C6–C7 |
| A-S2 | Should | OQ-4 and silent loss at the reserve cap | ADR-0002 D10 (per day); `forfeitedMinutes` (C10) |
| A-S3 | Should | Rule changes retroactive? | C11: new movements only |
| A-S4 | Should | Fluence measurement missing | `FluenceRecord` (C5) |
| A-S5 | Should | Retention only for attempts | C9, C15: sessions and exercises fold with attempts, note links cleared |
| A-S6 | Should | Remediation state missing | `Remediation` (C4); replaces `scheduledFirst` (C14) |
| A-S7 | Should | Broken streak re-locks items | `Streak.bestDays` (C13) |
| A-S8 | Should | EARLY_STOP note wrongly anchored | `ParentNote -- ScreenTimeUse : raisedAfter` (C15) |
| A-S9 | Should | Export, restore, erase scopes; restore replays minutes | `Installation` root; scope and restore guard left as OQ-5 for the sequences |
| A-S10 | Should | Mastery precision, average time scope | `mastery : Real`, C1, C3 |
| A-N1 | Nice | Hint is a value | `Exercise.hints : HintStage [0..3]`, class removed |
| A-N2 | Nice | Command flag | `recalibrationRequestedAt` |
| A-N3 | Nice | Benchmark multiplicity | `*` to `*` |
| A-N4 | Nice | isLookAhead derived? | Kept as a snapshot at generation (C8) |
| A-N5 | Nice | Language drift (gauge, core, requestedFrom) | `receives` instead of `requestedFrom`; gauge vs reserve and core vs ACQUIRING left to the joint review |
| A-ADR | — | Strawman options and rigged D7 weights | D7 redone on substitutability (A, 460): no generalization; limits of D1, D3, D5, D6 stated in the ADR |
| R-S2 | Should | ScreenTimeRequest not composed | `Reserve *-- ScreenTimeRequest` |
| R-N3–N6 | Nice | Constraint placement, `[0..1]` ambiguity, D-code header, matrix versions | Constraints C1–C16 section, header prefixes "ADR-0002", versions in the matrix |

Render check: notes moved to a numbered constraint list because long notes shrank the diagrams; the companion was split into Diagram 3b to remove crossing lines. All five diagrams inspected.
