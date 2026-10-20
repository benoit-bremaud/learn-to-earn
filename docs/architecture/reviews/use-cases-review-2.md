# Review pass 2 — use-case study (coverage and traceability against the product)

- Date: 2026-10-20. Reviewer: independent agent (Opus), read-only, adversarial, without access to pass 1. Lens: coverage of every CADRAGE decision, roadmap versions, matrix, missing goals, child safety and privacy, cross-file consistency.
- Target: commit 1a2e466. Result: 6 Must, 17 Should, 8 Nice. Verdict at the time: not ready to validate.

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | Must | UC-L1 steps ship in V1.1 but the use case is V1.0 | Fixed: inline version tags, V1.0 runs the fixed C3 skill set |
| 2 | Must | UC-L2 describes V1.1 and V1.2 rules | Fixed: V1.0 simple time rule, later rules tagged |
| 3 | Must | No goal or rule to move between child and parent profiles (P0) | Fixed: convention (entry point, auto-lock, OS session out of scope) |
| 4 | Must | No first-launch onboarding, parental consent missing | Fixed: UC-P14 Set up the app for a child («include» UC-P12, UC-P2) |
| 5 | Must | Confidence pause placed in two use cases | Fixed: ADR-0001 D4 points to UC-L1 4c |
| 6 | Must | No import use case | Fixed: UC-P15 Restore the child's data from a file |
| 7 | Should | Confidence below 0.6 band missing | Fixed: UC-L2 3c |
| 8 | Should | Degressive conversion not stated | Fixed: UC-L1 business rule |
| 9 | Should | Daily cap vs reserve | Fixed: duration up to min(reserve, cap left), crediting rule |
| 10 | Should | 7-day expiry not modelled | Fixed: ADR D4 row, UC-L8 step 3 |
| 11 | Should | Device clock change | Fixed: cross-cutting rule (elapsed time, freeze, neutral note) |
| 12 | Should | Early timer stop lets the child bypass control | Partly agreed: stopping early is desirable and stays debit-by-use, but it is now visible to the Guardian, and the residual V1 risk is documented (removed by UC-S4 in V2) |
| 13 | Should | No parent-space auto-lock, PIN change without current PIN | Fixed: 2-minute auto-lock, current PIN required |
| 14 | Should | Interrupted session not covered | Fixed: UC-L1 *b |
| 15 | Should | Fluence milestones too early | Fixed: tagged V1.1 |
| 16 | Should | Streak shown in V1.0 | Fixed: tagged V1.2 |
| 17 | Should | Ceiling cited in V1.0 | Fixed: V1.0 has no ceiling |
| 18 | Should | Decisions with no home | Fixed: "Covered elsewhere" table |
| 19 | Should | UC-P11 not in the roadmap | Fixed: roadmap V1.1 updated in CADRAGE |
| 20 | Should | UC-P1 level contradicts its diagram | Fixed: user goal, also included by UC-S2 |
| 21 | Should | UC-L4 2a needs a V1.1 rule | Fixed: tagged |
| 22 | Should | No source for persistent keypad signals | Fixed: UC-L2 step 3 (V1.2) |
| 23 | Should | Pending request lifecycle undefined | Fixed: one at a time, expires at end of day |
| 24 | Nice | Matrix and spec cite different decisions | Fixed |
| 25 | Nice | Diagram headers miss decisions | Fixed |
| 26 | Nice | "Level" ambiguous | Fixed: glossary entry "difficulty level" |
| 27 | Nice | ADR D4 placement | Fixed |
| 28 | Nice | Streak shame | Fixed: business rule in UC-L8 |
| 29 | Nice | Personal fluence records invisible to the child | Fixed: UC-L8 (V1.1) |
| 30 | Nice | Challenge choice rule | Fixed: UC-L6 business rule |
| 31 | Nice | No export prompt before erase | Fixed: UC-P9 step 1 |

The reviewer found no wording that shames the child or diagnoses anything.
