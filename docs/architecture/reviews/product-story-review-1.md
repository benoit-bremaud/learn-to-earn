# Product story review 1 — 2026-10-24

Adversarial end-to-end read of the dossier on `main` at b589800 (issue #22): the child's first week, then the parent's path. Out of scope: #16–#20. `dm` = `diagrams/domain/01-class-domain-model.md`. The Resolution column is filled as each finding is fixed or decided.

| # | Level | Finding | Owner decision | Resolution |
|---|---|---|---|---|
| 1 | Must | Weighted minutes grow with response time: an idle exercise earns as much as work (C9 vs CADRAGE "slow is never a signal") | yes | decided: ADR-0004 D1, CADRAGE Conversion and §3, spec UC-L1, dm C9, session sequence |
| 2 | Must | No cold start: nothing mastered on day 1, no placement test, prerequisites gate every node, so a CE1 child starts on `c1.count` | yes | decided: ADR-0004 D2, CADRAGE §3, curriculum, dm C1 |
| 3 | Must | The UC-L4 hint loop (4 tries per exercise) trips M4 "3 errors in a row" on most hard exercises | yes | decided: ADR-0004 D3, CADRAGE M4, curriculum, spec UC-L1 4a and UC-L4 2c, dm C4, remediation sequence |
| 4 | Must | V1.0 earning formula, minimum-time rule and exercise picker are undefined (multipliers and mix are V1.1) | yes | decided: ADR-0004 D4, CADRAGE §3 and §5, spec UC-L1 and UC-L2, dm C9, session sequence |
| 5 | Should | Earning numbers: reaching the 30-min cap needs about an hour of maths a day, against the 1 min = 1 min promise | yes | decided: ADR-0004 D5, CADRAGE Conversion and §6, spec UC-L1 and UC-S5 |
| 6 | Should | `progressBonusRatio` has no default nor editor; "mastery rose" undefined | yes | decided: ADR-0004 D6, CADRAGE Conversion, spec UC-L1 and UC-S5, dm ScreenTimeRules, SkillProgress, C1, C7, crediting sequence, ADR-0002 D11 note |
| 7 | Should | Confidence resets to 1.0 with a new session: stop and restart erases it | yes | decided: ADR-0004 D7, CADRAGE §3, spec UC-L2, dm C6, confidence sequence, ADR-0002 D3 note |
| 8 | Should | CADRAGE applies the confidence factor below 0.6 only, C9 and ADR-0002 D8 always | no | fixed: CADRAGE §3, domain C9, confidence sequence |
| 9 | Should | The fast-answer penalty punishes real fluency on automatised facts | yes | decided: ADR-0004 D8, CADRAGE §3, spec UC-L2 3b, confidence sequence |
| 10 | Should | Frozen clock never unfreezes; moving the clock forward opens a new daily cap | yes | decided: ADR-0004 D9, CADRAGE §3, spec glossary and time rule, UC-S3, dm TimeGuard, C11, C16 |
| 11 | Should | Elapsed time runs while the app is closed, so resume is pointless; C7 and UC-L1 \*b disagree on expiry | yes | decided: ADR-0004 D10, CADRAGE §3, spec UC-L1 step 4 and \*b, dm C6, C7, session sequence |
| 12 | Should | CADRAGE E3 still promises a final challenge (D9 spreads challenge slots) | no | fixed: CADRAGE E3 |
| 13 | Should | "Look-ahead" means under the ceiling in the sequence, above it in C8 | no | fixed: CADRAGE C1, UC-L6, session sequence, domain C8 |
| 14 | Should | UC-P7 "go back to X" first in next session vs remediation only in the review share; no target for a parent remediation | yes | decided: ADR-0004 D11, CADRAGE R4, spec UC-L1 4b, UC-L5, UC-P7, dm Remediation, C4, C14, session and remediation sequences |
| 15 | Should | Remediation threshold, graph floor and minimum exercises undefined | yes | decided: ADR-0004 D12, CADRAGE R4, spec UC-L5, dm C4, NoteKind, remediation sequence |
| 16 | Should | Dashboard colours leave a gap (85 % and rising); no minimum attempts before a colour | no | fixed: CADRAGE P2, UC-P5 (80 % unless falling, 5 attempts minimum) |
| 17 | Should | PIN lockout has no numbers and can be abused by the child | yes | decided: ADR-0004 D13, CADRAGE P1, spec UC-P1, dm C17, approval sequence |
| 18 | Should | PIN typed on the child's tablet in front of her (shoulder-surfing) | yes | decided: ADR-0004 D14, CADRAGE P1, spec UC-P1, approval sequence |
| 19 | Should | OQ-1 forgotten PIN still open for V1.0 while erase is the legal baseline | yes | decided: ADR-0004 D15, CADRAGE P1 and §6, spec UC-P1 1b, UC-P12, OQ-1 closed, dm ParentCredential, ADR-0003 note |
| 20 | Should | Which PIN applies after a restore while unlocked is unstated | no | fixed: UC-P15, restore sequence note |
| 21 | Should | V1.0 writes CLOCK_CHANGED notes that only V1.1 can show | yes | decided: ADR-0004 D16, CADRAGE §5, spec UC-P6, dm ParentNote version, C15 |
| 22 | Should | A second child can be created in V1 from the parent space | no | fixed: UC-P2 business rule, OQ-3 |
| 23 | Should | The set-aside database has no way back and is kept forever (check #18) | yes | decided: ADR-0004 D17, spec UC-P14 \*a and storage rule, dm C18, key-loss sequence, ADR-0003 D3 note |
| 24 | Should | Streak "active day" undefined | yes | decided: ADR-0004 D18, CADRAGE E1, spec glossary and UC-L8, dm C13 |
| 25 | Should | Document statuses disagree (use cases, domain "awaiting validation" vs sequences validated) | no | fixed: README statuses and planned steps |
| 26 | Should | ADR-0003 reasons on a 4-digit PIN, P1 fixed 6 digits | no | fixed: ADR-0003 D3 |
| 27 | Nice | The progress bonus credit of a session closed next day has no LocalDay | no | fixed: domain C7 |
| 28 | Nice | A balance under 1 minute shows a 0-minute picker | no | fixed: UC-S1 step 2 |
| 29 | Nice | OQ-4 and OQ-5 cited but missing from the spec's OQ list | no | fixed: spec OQ list |
| 30 | Nice | Domain header says D1–D8; ADR-0002 consequence about CADRAGE already done | no | fixed: domain header, ADR-0002 consequences |
| 31 | Nice | Aggregates note still says "erasing a child" | no | fixed: domain aggregates note |
| 32 | Nice | "Weekly expiry" reads as a calendar week (rolling 7 days) | no | fixed: CADRAGE Q4 |
| 33 | Nice | "Points" survives after the single-currency decision | no | fixed: CADRAGE, spec, confidence sequence |
| 34 | Nice | Ceiling default needs a period calendar; V1.0 nodes have no period | yes | decided: ADR-0004 D19, CADRAGE C1, curriculum periods, spec UC-P3 2a, dm C14 |
| 35 | Nice | Confidence sequence draws one signal out of five | no | fixed: confidence sequence note |

Re-review 2026-10-24: 1 Must, 8 Should, 6 Nice on the propagation, all fixed (clarifications of D4, D6, D12, D13, D15, D17, D9).
