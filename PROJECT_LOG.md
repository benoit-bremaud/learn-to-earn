# Project log

## 2026-10-20 — Brainstorming and repository bootstrap

- Brainstorming session with MCDA matrices for every choice: staged screen-time control, Expo, arithmetic first, capped savings, adaptive engine, difficulty scale, anti-cheat, child experience, parent dashboard, local-first data, privacy, roadmap. Full decision log in `docs/CADRAGE.md`.
- Curriculum alignment added after the owner's request: skill graph derived from the 2025 CE1 livret d'accompagnement (programme of 22-10-2024). See `docs/curriculum/CE1-maths.md`.
- Repository created public under a provisional name. Next: choose the name, then UML-first design.

## 2026-10-21 — SonarQube quality gate

- Owner decision (MCDA A 435 / CI job 405 / SonarCloud 340): project `learn-to-earn` on the shared local SonarQube instance, scanned from the dev machine with the global analysis token before every push and merge. A CI job is added when V0 code starts.
- `sonar-project.properties` added; first scan auto-provisioned the project, quality gate PASSED.
- Owner rule: every unit and regression test runs right before SonarQube. `make check` = unit tests with coverage (floor 80 %) → Mermaid render of every diagram → MCDA totals and link checks → gitleaks → SonarQube with the quality-gate wait. The MCDA check catches the ADR-0002 D2 error found by Codex on PR #3.
