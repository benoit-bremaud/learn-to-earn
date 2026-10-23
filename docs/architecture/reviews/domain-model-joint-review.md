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
| 5 | `forfeitedMinutes` (then on ReserveBucket, now on ReserveCredit) | Keep | — |
| 6 | Frozen snapshots (`confidenceAtAnswer`, `weightedMinutes`) | Keep both | — |
| 7 | Remediation end rule | Improve | C4/C14: AUTO closes by itself at the threshold; GUARDIAN closes at the threshold and raises a `REMEDIATION_COMPLETED` note |
| 8 | Interrupted session crediting | Improve | C6/C7: each interruption credits the earned weighted minutes as a credit of the current day; a resumed session credits the rest at its end |

Render check: all five diagrams re-rendered with `mmdc` and inspected after the changes.

## Follow-up after the Codex review of PR #3

| Finding | Resolution |
|---|---|
| D2 totals wrong (375 / 440 / 430 instead of 380 / 425 / 430) | Recomputed; owner re-voted C (credits and uses, balance replayed). ReserveBucket replaced by ReserveCredit; all matrices re-checked by script |
| `/unlockedLevel` not derivable after folding | `SkillProgress.highestPassedLevel` stored (C2) |
| Remediation closed on `target` | End rule reads the mastery of `current`, the skill practised (C4) |
| Fractional weighted minutes in integer amounts | Reserve amounts are Real, display rounds down (C10) |
| Credit expiring under an approved request | Balance re-checked at use start, IN_USE request held in the replay, unstarted APPROVED request expires with its day (C11) |
| Second Codex pass: interrupted session could credit attempts twice | Checkpoint first on Session, then moved into ReserveCredit (`sourceSession`, `weightedUpTo`) by the third pass |
| Second Codex pass: credit expiry by day, retroactive `expiryDays` | `ReserveCredit.expiresAt` frozen at creation (C10) |
| Second Codex pass: integer `usedMinutes` on early stop | `ScreenTimeUse.endedAt`, `usedMinutes : Real` (C11) |
| Third Codex pass: crediting not idempotent across aggregates | Checkpoint carried by ReserveCredit, one write in the Reserve, unique `(sourceSession, weightedUpTo)` (C7) |
| Third Codex pass: active hold opened room under the reserve cap | Cap headroom ignores IN_USE holds (C10) |
| Third Codex pass: session crossing midnight credited to one day | Uncredited attempts split by the day of `answeredAt`, one credit per day (C7) |
| Fourth Codex pass: PENDING request never expired | PENDING and APPROVED both expire at day end (C11) |
| Fourth Codex pass: timer debit from wall clock | `ScreenTimeUse.elapsedSeconds` monotonic, `/usedMinutes` derived (C11) |
| 2026-10-23 owner decision on UC-S3 *a (MCDA D 455) | Supersedes the row above: `elapsedSeconds` removed, `/usedMinutes` from device time since `startedAt`, full debit on a backwards clock (C11, C16) |
| Fourth Codex pass: no level after VERY_HARD | `/unlockedLevel` capped at VERY_HARD (C2) |
| Fifth Codex pass: split credits expired from the crediting time | `expiresAt` from the latest `answeredAt` of the credit's attempts (C10) |
| Owner, 2026-10-21: reward learning results, not time spent | ADR-0002 D11 = B: correct answers only plus a mastery-gain bonus (C9, `progressBonusRatio`); default reserve cap 60 min |
