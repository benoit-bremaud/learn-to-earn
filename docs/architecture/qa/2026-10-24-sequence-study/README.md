# QA pass — sequence study (PR #15), 2026-10-24

Post-merge check on `main` at ac943f9. PR #15 was merged before this pass and before the `review-local` gate, against the pre-merge rule; this pass makes up for it. No running product exists yet (design phase), so the QA is the no-UI variant: every diagram touched by PR #15 (plus `learning/01-use-case`, unchanged, as a baseline) is rendered with `mmdc` (width 1400, white background) and inspected visually, then checked against the spec and the domain model. The renders are the PNG files of this folder.

## Inspected

| Render | Visual verdict |
|---|---|
| learning-01-use-case | clean |
| learning-02-sequence-learning-session | hint label and note touch the fragment borders |
| learning-03-sequence-confidence-scoring | clean |
| learning-04-sequence-remediation | SessionScreen drawn last: the Learner and UI arrows cross every lifeline |
| learning-05-sequence-crediting | clean |
| screen-time-01-use-case | clean |
| screen-time-02-sequence-request | clean |
| screen-time-03-sequence-approval | clean |
| screen-time-04-sequence-use | clean |
| parent-space-01-use-case | «include» UC-P14 → UC-P2 crosses the UC-P1 oval, very tall diagram |
| parent-space-02-sequence-erase | clean |
| parent-space-03-sequence-restore | the first `alt` label overlaps the Guardian actor name |
| parent-space-04-sequence-key-loss-start | clean |
| domain-01-class-domain-model-1 (learning content and progress) | the `Skill requires Skill` self-association ends on an empty point at the right |
| domain-01-class-domain-model-2 (practice) | clean |
| domain-01-class-domain-model-3 (reserve and screen time) | clean, `forfeitedMinutes` present on ReserveCredit |
| domain-01-class-domain-model-4 (streak) | clean |
| domain-01-class-domain-model-5 (parent space) | the C14 and C15 notes sit far from LearningPlan and ParentNote, so their anchor is ambiguous |

## Findings

Every finding is tracked as a GitHub issue on project #65 (see Backlog below).

| ID | Level | Finding |
|---|---|---|
| QA-1 | Should | Restore: the controller forfeits credits, closes requests and checks the PIN itself (self-messages), so domain rules sit in a «control» instead of the Reserve and Installation entities |
| QA-2 | Should | Approval and timer start check "balance and daily cap still cover it" but no branch says what happens when they no longer do (product rule missing in UC-S2, UC-S3) |
| QA-3 | Should | Use: the Stop branch starts with `UI->>Ctl: stop` without the Learner's tap |
| QA-4 | Should | Key-loss start: the retry is an `alt` with no bound; the number of retries is not specified anywhere |
| QA-5 | Should | Remediation: lifeline order makes the Learner and UI arrows cross the whole diagram |
| QA-6 | Nice | Visual overlaps: session hint label and note, restore `alt` label over the actor, parent-space «include» arrow over UC-P1 |
| QA-7 | Nice | Erase: the Cancel and Export branches have no Guardian message; crediting: `trusted now` result is not named (creditedAt) |
| QA-9 | Nice | Domain model: dangling `requires` self-association end, C14 and C15 notes far from their class |
| QA-8 | Process | PR #15 merged without `review-local` and without this visual QA |

## review-local gate (on `main` at ac943f9)

`make check` green (coverage 100 %, 18 diagrams rendered, gitleaks clean, SonarQube passed). Must 0, Should 4, Nice 3.

| ID | Level | Finding |
|---|---|---|
| RL-S1 | Should | Approval: no failing branch for the balance and cap re-check (same as QA-2) |
| RL-S2 | Should | Traceability: UC-P8 and UC-P14 point to sequences that do not model them |
| RL-S3 | Should | Key-loss start: the Context says an unfinished erase is resumed, the diagram never checks the marker |
| RL-S4 | Should | Restore: forfeit and request closing happen before the single transaction |
| RL-N1 | Nice | Session: next exercise picked before the elapsed-time check |
| RL-N2 | Nice | Key-loss start: retry should be a bounded `loop` (same as QA-4) |
| RL-N3 | Nice | Remediation: no exit when the walk-back reaches the bottom of the graph |

## Backlog

| Issue | Findings |
|---|---|
| [#16](https://github.com/benoit-bremaud/learn-to-earn/issues/16) | QA-1, RL-S4 |
| [#17](https://github.com/benoit-bremaud/learn-to-earn/issues/17) | QA-2, RL-S1 (needs an owner MCDA) |
| [#18](https://github.com/benoit-bremaud/learn-to-earn/issues/18) | RL-S3, QA-4, RL-N2 |
| [#19](https://github.com/benoit-bremaud/learn-to-earn/issues/19) | RL-S2 |
| [#20](https://github.com/benoit-bremaud/learn-to-earn/issues/20) | QA-3, QA-5, QA-6, QA-7, QA-9, RL-N1, RL-N3 |

QA-8 (process) is fixed by this pass and the PROJECT_LOG entry.
