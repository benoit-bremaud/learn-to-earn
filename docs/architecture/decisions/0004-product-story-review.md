# ADR-0004 — Product story review decisions

- Status: accepted (owner, 2026-10-24)
- Date: 2026-10-24

## Context and problem statement

The product story review ([reviews/product-story-review-1.md](../reviews/product-story-review-1.md), issue #22) read the dossier end to end as the child's first week, then the parent's path. It raised 35 findings: 16 were fixed directly, 19 needed an owner decision. This ADR records those 19 decisions (D1–D19), each with the review finding it answers.

Scores: 0–5, weights sum to 100, total out of 500. Scores are estimates. Sensitivity is checked one criterion at a time, the other weights scaled.

## D1 — Earning per correct answer (finding 1)

| Criterion (weight) | A. Counted time capped at 2x her own average on the skill | B. Standard time per difficulty level in configuration, real time no longer counts | C. Active time only, with idle detection |
|---|---|---|---|
| Pushes work (30) | 4 | 4 | 3 |
| Anti-gaming (25) | 4 | 5 | 3 |
| Simplicity (20) | 4 | 5 | 1 |
| Child experience (25) | 4 | 4 | 3 |
| **Total /500** | 400 | **445** | 260 |

B vs A: A still pays slowness up to the cap, B pays the exercise and not the clock, which matches "slow is never a signal". Sensitivity: B scores at least as high as A and C on every criterion, so no reweighting changes the winner.
**Decision: B** (owner, 2026-10-24). Weighted minutes of a correct answer = standard time of its difficulty level × difficulty multiplier × confidence factor × hint factor. Supersedes the "response time" term of ADR-0002 D8.

## D2 — Cold start (finding 2)

| Criterion (weight) | A. Skills below `classLevel` start at 70 % mastery (unlock threshold), errors walk down through R4 | B. Short probe in the first session | C. The Guardian ticks the known skills at set-up |
|---|---|---|---|
| Accuracy (35) | 3 | 5 | 3 |
| Child experience (30) | 4 | 3 | 3 |
| Simplicity (20) | 5 | 3 | 3 |
| Consistency with "no placement test" (15) | 5 | 2 | 4 |
| **Total /500** | **400** | 355 | 315 |

A vs B: B is more accurate but is a placement test in disguise; A starts the child on her own class and lets real errors correct the guess. Sensitivity: B leads only if accuracy weighs more than about 47 %.
**Decision: A** (owner, 2026-10-24).

## D3 — What counts as an error for the 3-error rule (finding 3)

| Criterion (weight) | A. An exercise failed at the first try is one error, the rule fires after 3 such exercises in a row | B. Only exercises ending without a correct answer | C. Every wrong try (status quo) |
|---|---|---|---|
| Pedagogy (35) | 5 | 3 | 2 |
| Child experience (30) | 4 | 5 | 1 |
| Parent noise (20) | 4 | 5 | 1 |
| Simplicity (15) | 4 | 4 | 5 |
| **Total /500** | **435** | 415 | 195 |

A vs B: B waits until three exercises end on the shown answer, which is late for a weak prerequisite; A counts the exercise, not the tries inside the hint loop. Sensitivity: B leads if child experience weighs more than about 42 % or parent noise more than about 34 %.
**Decision: A** (owner, 2026-10-24).

## D4 — V1.0 rules (finding 4)

| Criterion (weight) | A. D1 formula with multiplier 1 and confidence factor 1, no minimum-time rule, picker = warm-up on a mastered skill, then the lowest unmastered skill whose prerequisites are all at 70 % or more | B. Multipliers and the 70/20/10 mix moved into V1.0 | C. Like A, plus no earning under 1 s |
|---|---|---|---|
| Small V1.0 scope (30) | 5 | 2 | 4 |
| Coherent earning (30) | 4 | 5 | 4 |
| Anti-gaming (20) | 4 | 4 | 5 |
| Simplicity (20) | 5 | 2 | 3 |
| **Total /500** | **450** | 330 | 400 |

A vs C: the 1-s floor adds a rule that the V1.1 confidence score replaces anyway; V1.0 is a family test. Sensitivity: C leads only if anti-gaming weighs more than about 47 %.
**Decision: A** (owner, 2026-10-24). The "simple minimum-time rule" of the V1.0 roadmap is removed.
Clarification (re-review 2026-10-24): "mastered" means mastery at 70 % or more; ties for the lowest unmastered skill are broken by lowest grade, then graph depth, then table order; in V1.0 the picker itself does the walk-down (a skill under 70 % is again the lowest unmastered one), R4 and UC-L5 apply from V1.1.

## D5 — Earning volume (finding 5)

| Criterion (weight) | A. Standard times calibrated so a 15-min session at 80 % success earns about 15 min, cap unchanged (30 screen min needs 40 weighted min) | B. Same, daily cap lowered to 20 min | C. Drop the 2:1 step |
|---|---|---|---|
| Keeps the 1 min = 1 min promise (35) | 5 | 4 | 3 |
| Pushes work (30) | 4 | 3 | 3 |
| Simplicity (20) | 4 | 4 | 5 |
| Child experience (15) | 4 | 3 | 4 |
| **Total /500** | **435** | 355 | 355 |

A vs B: B cuts screen time to fix an earning problem; A fixes the earning itself. Sensitivity: C leads only if simplicity weighs more than about 56 %.
**Decision: A** (owner, 2026-10-24).
Clarification (review 2026-10-24): Initial standard times (configuration, not Guardian-editable): Easy 35 s, Medium 50 s, Hard 70 s, Very hard 90 s per correct answer, before the V1.1 multiplier. Derivation: an easy exercise takes about 30 s, so a 15-min session at 80 % success gives 24 correct answers out of 30, and 900 s / 24 is about 37 s, rounded to 35; the other levels scale up. To be calibrated after one week of real use.

## D6 — Progress bonus (finding 6)

| Criterion (weight) | A. 10 % of the session's minutes if mastery rose 5 points from start to end | B. Fixed 2 min per skill whose mastery beats its own previous best by 5 points or more | C. No bonus |
|---|---|---|---|
| Pushes progress (35) | 4 | 4 | 1 |
| Anti-gaming (25) | 3 | 5 | 5 |
| Simplicity (20) | 3 | 5 | 5 |
| Clarity for the child (20) | 3 | 5 | 3 |
| **Total /500** | 335 | **465** | 320 |

B vs A: A pays again a mastery that fell and came back; B pays only a new personal best, which cannot be farmed. Sensitivity: B scores at least as high as A and C on every criterion.
**Decision: B** (owner, 2026-10-24). `progressBonusRatio` is replaced by a configured `bonusMinutes` (default 2) and a per-skill `bestMastery`. The bonus is still credited once at the final close, as its own credit (domain C7). Supersedes the bonus rule of ADR-0002 D11.

## D7 — Confidence across sessions (finding 7)

| Criterion (weight) | A. A new session starts from the day's last confidence and recovers normally (+0.05 per plausible correct answer) | B. 30-min gap before a new session | C. Reset to 1.0 |
|---|---|---|---|
| Anti-gaming (35) | 5 | 3 | 1 |
| Child experience (30) | 4 | 2 | 5 |
| Simplicity (20) | 4 | 4 | 5 |
| Fairness (15) | 4 | 3 | 2 |
| **Total /500** | **435** | 290 | 315 |

A vs C: C lets a stop and restart wipe the score; A keeps it for the day only, so a bad day still does not follow her. Sensitivity: C leads only if child experience weighs more than about 69 %.
**Decision: A** (owner, 2026-10-24). Supersedes "starts at 1.0 in every session" of ADR-0002 D3: the first session of a LocalDay starts at 1.0.

## D8 — Fast-answer penalty (finding 9)

| Criterion (weight) | A. No fast-answer penalty on a skill mastered at 80 % or more | B. Only when the fast answer is wrong | C. At most one per session |
|---|---|---|---|
| Fairness to fluency (35) | 5 | 5 | 3 |
| Anti-cheat (30) | 4 | 2 | 3 |
| Simplicity (20) | 4 | 5 | 4 |
| Consistency with the fluency goal (15) | 5 | 3 | 4 |
| **Total /500** | **450** | 380 | 335 |

A vs B: B misses a fast correct guess on a new skill; A spares only facts that are already automatised. Sensitivity: B leads only if simplicity weighs more than about 53 %.
**Decision: A** (owner, 2026-10-24).

## D9 — Device clock changes (finding 10)

| Criterion (weight) | A. Trusted time from monotonic elapsed time (details below) | B. Network time when online | C. Accept forward jumps, note only |
|---|---|---|---|
| Anti-gaming (35) | 4 | 5 | 1 |
| Local-first and privacy (25) | 5 | 3 | 5 |
| Simplicity (20) | 3 | 3 | 5 |
| Robustness (20) | 4 | 3 | 4 |
| **Total /500** | **405** | 370 | 340 |

A vs B: B is stronger but sends requests out and fails offline; A stays on the device. Sensitivity: B leads if anti-gaming weighs more than about 52 %; C if simplicity weighs more than about 40 %.
**Decision: A** (owner, 2026-10-24). Trusted time = `lastTrustedAt` advanced by monotonic elapsed time (uptime). LocalDay changes only when trusted time passes midnight. A forward jump of the device clock of more than 10 min is ignored and raises a CLOCK_CHANGED note. The freeze after a backwards change lifts when the device clock catches up with `lastTrustedAt`. After a reboot (uptime reset) the device time is accepted if it is not earlier than `lastTrustedAt`: residual risk, covered by the note.

## D10 — Interrupted session (finding 11)

| Criterion (weight) | A. Session length counts only while the app is open (RUNNING or PAUSED), resume until the end of its LocalDay, then STOPPED_EARLY | B. Keep the device-time count and drop resume | C. Resume within 30 min only |
|---|---|---|---|
| Child experience (30) | 5 | 2 | 4 |
| Anti-gaming (30) | 4 | 5 | 4 |
| Simplicity (20) | 4 | 5 | 3 |
| Consistency (20) | 4 | 3 | 3 |
| **Total /500** | **430** | 370 | 360 |

A vs B: B makes resume pointless (finding 11); A makes it real and bounded. Sensitivity: B leads only if anti-gaming weighs more than about 57 %.
**Decision: A** (owner, 2026-10-24). It also settles the expiry disagreement between domain C7 and UC-L1 \*b: an interrupted session expires at the end of its LocalDay.

## D11 — Parent "go back to X" (finding 14)

| Criterion (weight) | A. X first in the review share | B. Next session, after the warm-up, opens with a 5-exercise block on X, then X joins the review share; a parent remediation has no target | C. X only added to the review queue |
|---|---|---|---|
| Pedagogy (35) | 4 | 5 | 3 |
| Parent expectation (25) | 3 | 5 | 2 |
| Simplicity (20) | 4 | 3 | 5 |
| Consistency (20) | 5 | 3 | 4 |
| **Total /500** | 395 | **420** | 335 |

B vs A: the Guardian asked for X now; A dilutes it in 20 % of the session. Sensitivity: A leads if consistency weighs more than about 29 % or simplicity more than about 37 %.
**Decision: B** (owner, 2026-10-24).

## D12 — Remediation exit (finding 15)

| Criterion (weight) | A. Exit at 70 % (unlock threshold) after at least 5 exercises; at the graph floor it stays on the node and raises a "to do together" note | B. 80 %, 8 exercises | C. Like A but simply ends at the floor |
|---|---|---|---|
| Pedagogy (35) | 4 | 5 | 3 |
| Consistency (25) | 5 | 3 | 5 |
| Child experience (20) | 4 | 3 | 4 |
| Simplicity (20) | 4 | 4 | 5 |
| **Total /500** | **425** | 390 | 410 |

A vs C: C leaves a child stuck on `c1.count` with no help; A asks the Guardian to step in. Sensitivity: C leads if simplicity weighs more than about 31 %.
**Decision: A** (owner, 2026-10-24).

## D13 — PIN lockout (finding 17)

| Criterion (weight) | A. 3 free tries, then waits of 30 s, 1 min, 5 min, capped at 15 min, reset after a correct PIN | B. 5 tries, then 1 h | C. Doubling wait, no cap |
|---|---|---|---|
| Security (35) | 4 | 4 | 5 |
| Resistance to abuse by the child (30) | 5 | 2 | 1 |
| Simplicity (20) | 4 | 5 | 4 |
| Parent experience (15) | 4 | 2 | 2 |
| **Total /500** | **430** | 330 | 315 |

A vs B: B lets the child lock the parent out for an hour with five taps. Sensitivity: C leads only if security weighs more than about 70 %.
**Decision: A** (owner, 2026-10-24).

## D14 — PIN typed in front of the child (finding 18)

| Criterion (weight) | A. Scrambled PIN pad each time, no digit echoed | B. Approval from the parent's phone (V2) | C. Risk accepted and documented |
|---|---|---|---|
| Effectiveness (35) | 4 | 5 | 1 |
| V1 scope (25) | 5 | 1 | 5 |
| Parent experience (20) | 3 | 5 | 5 |
| Simplicity (20) | 4 | 2 | 5 |
| **Total /500** | **405** | 340 | 360 |

A vs C: watching finger positions no longer gives the PIN, for one screen of work. Sensitivity: C leads if parent experience weighs more than about 35 %.
**Decision: A** (owner, 2026-10-24).

## D15 — Forgotten PIN (finding 19, closes OQ-1)

| Criterion (weight) | A. Recovery code shown once at set-up, to be written down, lets the Guardian set a new PIN | B. Erase everything without PIN after a confirmation | C. Uninstall documented as the only way out |
|---|---|---|---|
| Parent can recover (35) | 5 | 4 | 2 |
| Child cannot abuse it (30) | 4 | 1 | 5 |
| Stays local (20) | 5 | 5 | 5 |
| Simplicity (15) | 3 | 4 | 5 |
| **Total /500** | **440** | 330 | 395 |

A vs C: C loses all progress for a forgotten PIN; A keeps it at the cost of one code on paper. Sensitivity: C leads if simplicity weighs more than about 31 %.
**Decision: A** (owner, 2026-10-24). Only a hash of the code is stored. OQ-1 is closed.

## D16 — Parent notes in V1.0 (finding 21)

| Criterion (weight) | A. Minimal note list with an unread badge in the V1.0 parent space; full UC-P6 alerts stay V1.1 | B. No note in V1.0 | C. Notes stored in V1.0, shown in V1.1 |
|---|---|---|---|
| Parent informed (35) | 5 | 1 | 2 |
| V1 scope (25) | 3 | 5 | 4 |
| Consistency (20) | 5 | 4 | 3 |
| Simplicity (20) | 4 | 5 | 4 |
| **Total /500** | **430** | 340 | 310 |

A vs B: V1.0 already writes CLOCK_CHANGED notes; B hides them. Sensitivity: B leads only if V1 scope weighs more than about 49 %.
**Decision: A** (owner, 2026-10-24). ParentNote moves to V1.0.

## D17 — Set-aside database (finding 23)

| Criterion (weight) | A. Each start retries opening it for 30 days, then deletes it and raises a note | B. Deleted once the new set-up completes | C. Retried at every start, no limit |
|---|---|---|---|
| Recover data (35) | 4 | 1 | 4 |
| No orphan data (30) | 4 | 5 | 2 |
| Simplicity (20) | 3 | 5 | 4 |
| Consistency with issue #18 (15) | 4 | 4 | 4 |
| **Total /500** | **380** | 345 | 340 |

A vs B: B throws away a database a returning key could still open; A gives it a month. Sensitivity: B leads if simplicity weighs more than about 32 %.
**Decision: A** (owner, 2026-10-24). Supersedes "kept, never deleted, until a restore succeeds or the Guardian erases it" of ADR-0003 D3.
Clarification (review 2026-10-24): bringing it back is its own flow (UC-P14 *a1) with the PIN of the old database, not UC-P15.

## D18 — Streak active day (finding 24)

| Criterion (weight) | A. At least one COMPLETED session | B. 10 correct answers in the LocalDay, across sessions | C. Any session started |
|---|---|---|---|
| Rewards effort (35) | 4 | 5 | 1 |
| Fairness (25) | 3 | 4 | 5 |
| Simplicity (20) | 5 | 4 | 5 |
| Anti-gaming (20) | 4 | 5 | 1 |
| **Total /500** | 395 | **455** | 280 |

B vs A: an interrupted but real day of work still counts with B. Sensitivity: A leads only if simplicity weighs more than about 51 %.
**Decision: B** (owner, 2026-10-24).

## D19 — Period calendar for the default ceiling (finding 34)

| Criterion (weight) | A. Fixed table of 5 periods in configuration (Sep–Oct, Nov–Dec, Jan–Feb, Mar–Apr, May–Aug), the Guardian can change the ceiling; each V1.0 node gets its period | B. The Guardian picks the ceiling at set-up | C. Real school calendar of the zone |
|---|---|---|---|
| Accuracy (30) | 4 | 4 | 5 |
| Simplicity (30) | 5 | 4 | 2 |
| Parent effort (20) | 5 | 2 | 3 |
| Privacy (20) | 5 | 5 | 2 |
| **Total /500** | **470** | 380 | 310 |

A vs C: C needs the school zone and a yearly data update for a few days of accuracy. Sensitivity: C leads only if accuracy weighs more than about 74 %.
**Decision: A** (owner, 2026-10-24).
Clarification (review 2026-10-24): July and August map to P5 (the year just finished) until the Guardian changes the class level or the ceiling.

## Decision outcome

D1 = B (445), D2 = A (400), D3 = A (435), D4 = A (450), D5 = A (435), D6 = B (465), D7 = A (435), D8 = A (450), D9 = A (405), D10 = A (430), D11 = B (420), D12 = A (425), D13 = A (430), D14 = A (405), D15 = A (440), D16 = A (430), D17 = A (380), D18 = B (455), D19 = A (470).

## Consequences

- ADR-0002 D3 (confidence per session), D8 (response time term) and D11 (bonus ratio) are superseded in part by D7, D1 and D6; ADR-0003 D3 (set-aside database kept) by D17. Those ADRs keep their text and point here.
- `ScreenTimeRules` holds `bonusMinutes` (replacing `progressBonusRatio`) and the standard time per level lives in configuration with the multipliers; `SkillProgress` holds `bestMastery`; `ParentCredential` holds `recoveryCodeHash`; `TimeGuard` holds a monotonic reference (domain model).
- V1.0 grows by a minimal note list (D16), the PIN recovery code (D15), the scrambled PIN pad (D14) and the lockout numbers (D13); it loses the minimum-time rule (D4).
- Standard times are calibrated against D5 (about 15 min earned for a 15-min session at 80 % success), then re-checked after one week of real use (CADRAGE §6).
