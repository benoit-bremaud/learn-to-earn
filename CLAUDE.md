# learn-to-earn — project rules

Global rules apply first: `~/.claude/CLAUDE.md` and `~/.agent-rules/common.md`. This file only adds what is specific to this repository.

## Context

- CE1 arithmetic app that turns learning results into earned screen time. Brief: `docs/CADRAGE.md`; curriculum: `docs/curriculum/CE1-maths.md`.
- Product goal: rewards push work and rising learning results, never stored screen time.
- Privacy by design: local-first, no trackers, no child data sent to third parties.
- UI: keep the number of visible buttons and fields to a minimum. A control appears only once the previous choice or action makes it relevant (progressive disclosure), on every screen, mockup and state diagram.

## Phase

- Design phase, UML-first: no app code before the relevant diagrams are validated (`docs/architecture/diagrams/<feature>/<NN>-<type>.md`, Mermaid).
- Every choice between options gets an MCDA matrix (totals /500, checked by `scripts/check_docs.py`).

## Quality gate

- `make check` before every push and every merge: unit tests with coverage (floor 80 %), Mermaid render, MCDA and link checks, gitleaks, then SonarQube on the local instance (`SONAR_TOKEN` = global analysis token).
- GitHub Actions runs `make ci` (same checks without SonarQube) on every PR.

## Workflow

- Kanban: GitHub Project "learn-to-earn" (#65). Milestone: "V0 conception".
- Reviewers: Codex (re-triggered with `@codex review` on each new head) plus the local gate (`review-local`, `make check`). No Copilot reviewer on this repo.
- One issue per PR (`Closes #N`), one chat per issue, chat titled `#N <issue title>`.
- Stacked PRs are kept in sync with plain merges of their base, never rebase or force-push.
- `PROJECT_LOG.md` is updated after every merge.
