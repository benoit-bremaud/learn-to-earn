# Project log

## 2026-10-20 — Brainstorming and repository bootstrap

- Brainstorming session with MCDA matrices for every choice: staged screen-time control, Expo, arithmetic first, capped savings, adaptive engine, difficulty scale, anti-cheat, child experience, parent dashboard, local-first data, privacy, roadmap. Full decision log in `docs/CADRAGE.md`.
- Curriculum alignment added after the owner's request: skill graph derived from the 2025 CE1 livret d'accompagnement (programme of 22-10-2024). See `docs/curriculum/CE1-maths.md`.
- Repository created public under a provisional name. Next: choose the name, then UML-first design.

## 2026-10-21 — SonarQube quality gate

- Owner decision (MCDA A 435 / CI job 405 / SonarCloud 340): project `learn-to-earn` on the shared local SonarQube instance, scanned from the dev machine with the global analysis token before every push and merge. A CI job is added when V0 code starts.
- `sonar-project.properties` added; first scan auto-provisioned the project, quality gate PASSED.
- Owner rule: every unit and regression test runs right before SonarQube. `make check` = unit tests with coverage (floor 80 %) → Mermaid render of every diagram → MCDA totals and link checks → gitleaks → SonarQube with the quality-gate wait. The MCDA check catches the ADR-0002 D2 error found by Codex on PR #3.

## 2026-10-21 — Review rounds on the stacked docs PRs (handover state)

PR stack: #1 `docs/curriculum-decisions` → main; #2 `docs/uml-use-cases` → #1; #3 `docs/domain-model` → #2; #4 `chore/sonarqube-setup` → main (independent). Each upper branch has its base merged in (plain merges, no rebase). Merge order: #4, then #1, #2, #3.

- #1 (Codex): difficulty formula starts from the skill base level, operation term removed; V1.0 roadmap includes tables x2/x5/x10; V1.0 prerequisite DAG with stable node IDs and edges in `docs/curriculum/CE1-maths.md`.
- #2 (Codex): per-day 20-min threshold, M2 guard, one open request with a timer hold, 5-min warning only for longer timers.
- #3 (Codex, five passes): ADR-0002 D2 totals were wrong (375/440/430 instead of 380/425/430); owner re-voted C, so the reserve is replayed credits (`ReserveCredit`, no buckets). Also: `highestPassedLevel`, remediation closes on `current`, Real amounts, idempotent crediting (`sourceSession`, `weightedUpTo`), cap headroom ignores holds, day split at midnight, frozen `expiresAt`, monotonic `elapsedSeconds`, level cap at VERY_HARD. All logged in `docs/architecture/reviews/domain-model-joint-review.md`.
- Owner decisions: ADR-0002 D11 = B (only correct answers earn, plus a mastery-gain bonus `progressBonusRatio`; MCDA 380 / 345 / 330); default reserve cap 60 min (tie 400/400 with 120 min, broken by the incentive to work). Product goal: rewards push work and rising learning results, never stored screen time.
- #4: pre-push review findings fixed (unique Mermaid names, MCDA parser fails on unparsable or total-less matrices, full-history gitleaks, coverage without test files); `make check` green, quality gate PASSED.

Open at handover:
- Codex re-reviews pending on the last commits of #1–#4; Copilot never reviewed #4. No open review thread on #1–#4.
- No CI in the repo (owner choice): the owner must say whether local `make check` counts as "CI" for the merge question.
- After #4 merges: run `make check` (incl. SonarQube) on #1, #2, #3 before each merge.
- Still waiting for the owner: ADR-0001/0002 validation, OQ-1 to OQ-3, OQ-5 (erase scope, restore replay guard, for the sequence study).
- Next study after the merges: sequence diagrams.

## 2026-10-22 — GitHub Actions CI

- Owner decision (MCDA B 440 / C CI + SonarCloud 410 / A local `make check` as CI 250): minimal workflow `.github/workflows/ci.yml` running `make ci` (unit tests with coverage, Mermaid render, MCDA and link checks, full-history gitleaks) on every push to main and every PR. SonarQube stays local through `make check`, so the merge question still needs a local gate run. Issue #5, delivered in PR #4.
