# QA — design backlog (issue #26)

No running product yet (design phase), so the QA is the no-UI variant: every diagram touched by the design-backlog PR is rendered with `mmdc` (width 1400, white background) and inspected visually, then checked against the spec, the domain model and ADR-0005.

| Render | Issue | Checked |
|---|---|---|
| `domain-01-class-domain-model-1..5.png` | #17, #24, QA-9 | Prerequisite reified (no self-association ending on an empty point), C14 next to LearningPlan, `appSeconds`, REQUEST_NOT_COVERED |
| `learning-02-sequence-learning-session.png` | N1, QA-6 | app time checked before the next pick, hint note removed |
| `learning-04-sequence-remediation.png` | QA-5, N3 | SessionScreen declared second, graph-floor exit |
| `learning-05-sequence-crediting.png` | QA-7 | `creditedAt` named |
| `parent-space-01-use-case.png` | QA-6 | «include» arrows no longer cross UC-P1 |
| `parent-space-02-sequence-erase.png` | QA-7 | Guardian taps Cancel and Export first |
| `parent-space-03-sequence-restore.png` | #16, QA-6 | rules on Reserve and Installation, inside one transaction, `alt` label clear of the actor |
| `parent-space-04-sequence-key-loss-start.png` | #18, #24 | erase marker checked first, bounded loop, deletion sentence |
| `screen-time-03-sequence-approval.png` | #17 | nothing covered / shortened branches |
| `screen-time-04-sequence-use.png` | #17, QA-3 | gauge and one Start button, Learner taps Stop |

Child screens touched (owner rule 2026-10-24): the gauge with one Start button, "No more screen time today", the existing countdown and Stop. None asks the child a question. The deletion sentence is on the Guardian's start screen.

All sequences stay at 7 lifelines or fewer and no message contains `;`.

Opus adversarial self-review (2026-10-24): 2 Must, 6 Should, 3 Nice. Fixed: restore reuses the key alias created at the key-loss start; erase marker drawn as an `alt`; deletion flag kept in a set-aside status file distinct from the erase marker; key-store reply inside the bounded loop with the "3 errors" outcome; note kind renamed REQUEST_NOT_COVERED and linked to its request; Prerequisite and `appSeconds` in the concept dictionary; ADR-0005 D2 and D3 in the traceability cells; "loaded in memory" wording in the restore; D4 sensitivity line; one OK button on "No more screen time today". Kept: the removed hint note, already stated in the session Context.
