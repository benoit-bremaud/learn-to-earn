# Joint critical review — domain model (owner + Claude)

- Date: 2026-10-21
- Participants: owner (Benoît Bremaud), Claude Opus 5.5
- Scope: domain model after review 3 (commit cf62ab6)
- Format: keep / refute / improve questionnaire, each option MCDA-scored, recommended option first (owner rule 2026-10-21)

| # | Question | Answer | Change |
|---|---|---|---|
| 1 | `Installation` as aggregate root | Keep | — |
| 2 | `TimeGuard` as a domain class | Keep | — |
| 3 | `SlotKind` naming | Improve | Literal renamed `CORE` (was ambiguous with the ACQUIRING trend) |
| 4 | Aggregate boundaries | Improve | Child aggregate split: Child (identity, Streak, KeypadProfile), LearningPlan, ParentNote |
| 5 | `ReserveBucket.forfeitedMinutes` | Keep | — |
| 6 | Frozen snapshots (`confidenceAtAnswer`, `weightedMinutes`) | Keep both | — |
| 7 | Remediation end rule | Improve | C4/C14: AUTO closes by itself at the threshold; GUARDIAN closes at the threshold and raises a `REMEDIATION_COMPLETED` note |
| 8 | Interrupted session crediting | Improve | C6/C7: each interruption credits the earned weighted minutes to the current day's bucket; a resumed session credits the rest at its end |

Render check: all five diagrams re-rendered with `mmdc` and inspected after the changes.
