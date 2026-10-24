# ADR-0005 — Design backlog decisions after the story review

- Status: accepted (owner, 2026-10-24)
- Date: 2026-10-24

## Context and problem statement

After the product story review (ADR-0004), issues #16–#20 and #24 held the remaining design debt (issue #26). Four points needed an owner decision: an approved request that the balance or the daily cap no longer covers (#17), the key-store retry bound (#18), the notice when a set-aside database is deleted with no new set-up (#24), and how a resumed session keeps its target (#24).

Owner rule (2026-10-24): the users are young children (CE1, 7–8). A child screen uses one short sentence, pictures or the gauge, and one obvious button; it never asks the child to arbitrate. Anything complex goes to the parent.

Scores: 0–5, weights sum to 100, total out of 500. Scores are estimates. Sensitivity is checked one criterion at a time, the other weights scaled.

## D1 — Approved request no longer covered (issue #17)

The balance (C11) and the daily cap (C12) are checked again at approval and when the use starts. Credits may have expired, or other minutes been used, since the request.

| Criterion (weight) | A. Shorten to the minutes still covered: the gauge shows them with one Start button, no new PIN; nothing left closes the request with a short neutral message | B. Silent cap: the timer runs for what is covered, nothing is shown | C. The request expires and the child asks again |
|---|---|---|---|
| Child fairness (30) | 5 | 3 | 2 |
| Rule integrity (30) | 5 | 5 | 5 |
| Simplicity (20) | 3 | 5 | 4 |
| Child experience (20) | 4 | 3 | 3 |
| **Total /500** | **440** | 400 | 350 |

A vs B: both keep the rules; B hides why the timer is shorter, A shows the number on the gauge. Sensitivity: B leads only if simplicity weighs more than about 33 %.
**Decision: A** (owner, 2026-10-24). No new PIN, because less than the parent approved is granted. The child never gets a question: the gauge shows the minutes ("12 minutes") and one Start button. With nothing left, the screen says "No more screen time today" with one OK button back to the gauge, and the request closes as EXPIRED with no debit. Either case raises a REQUEST_NOT_COVERED note for the Guardian, linked to the request, (V1.0 note list, ADR-0004 D16). At approval the Guardian sees the shortened minutes before tapping Approve.

## D2 — Key-store retry bound (issue #18)

| Criterion (weight) | A. 3 tries in all, waiting 1 s then 2 s | B. One retry | C. 5 tries with backoff |
|---|---|---|---|
| Avoid a false key loss (40) | 4 | 2 | 5 |
| Start-up delay (30) | 4 | 5 | 2 |
| Simplicity (30) | 4 | 5 | 4 |
| **Total /500** | **400** | 380 | 380 |

A vs B: a key store still busy just after boot often fails once; A covers that for about 3 s. Sensitivity: B leads only if start-up delay weighs more than about 42 %.
**Decision: A** (owner, 2026-10-24). A key-store error (not "key missing") is tried 3 times in all, 1 s then 2 s apart; only then is the key treated as lost (ADR-0003 D3).

## D3 — Set-aside database deleted with no new set-up (issue #24)

When no set-up or restore was completed, there is no database to hold a ParentNote at day 30.

| Criterion (weight) | A. One sentence on the start screen, from a flag in a set-aside status file outside the database (not the erase marker), until the next set-up or restore | B. No notice | C. A plain-text note kept outside the database |
|---|---|---|---|
| Parent informed (40) | 4 | 1 | 4 |
| Privacy (30) | 4 | 5 | 1 |
| Simplicity (30) | 4 | 5 | 3 |
| **Total /500** | **400** | 340 | 280 |

A vs C: the flag holds no child data, only "deleted"; C would keep a note in clear. Sensitivity: B leads only if simplicity weighs more than about 56 %.
**Decision: A** (owner, 2026-10-24). The key-loss start screen shows "The old data could not be opened and was deleted." above its two buttons. The screen is for the Guardian, never the child.

## D4 — Accumulated session duration (issue #24)

`workedSeconds` counts only RUNNING and `startedAt` includes the closed interval, so neither gives a resumed session its remaining time.

| Criterion (weight) | A. `appSeconds` on Session: app time RUNNING or PAUSED, saved with each write | B. Store the pause intervals and recompute | C. Recompute from `startedAt` minus the closed time |
|---|---|---|---|
| Reliable resume (40) | 5 | 5 | 3 |
| Simplicity (30) | 5 | 2 | 3 |
| Model consistency (30) | 4 | 3 | 2 |
| **Total /500** | **470** | 350 | 270 |

A vs B: same reliability, one counter instead of a list. Sensitivity: A scores at least as high as B and C on every criterion, so no reweighting changes the winner.
**Decision: A** (owner, 2026-10-24). The session ends when `appSeconds` reaches `sessionTargetMinutes` (domain C6, UC-L1 *b).

## Decision outcome

D1 = A (440), D2 = A (400), D3 = A (400), D4 = A (470).

## Consequences

- `NoteKind` gains REQUEST_NOT_COVERED, `Session` gains `appSeconds` (domain model C6, C12, C18).
- UC-S2, UC-S3, UC-P14 *a, UC-L1 *b and the storage rule state the decisions; the approval, use and key-loss start sequences draw them.
- ADR-0003 D3 keeps its text; the retry bound in D2 completes its "a key-store error is retried first".
