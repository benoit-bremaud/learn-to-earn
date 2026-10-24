# Project log

## 2026-10-20 — Brainstorming and repository bootstrap

- Brainstorming session with MCDA matrices for every choice: staged screen-time control, Expo, arithmetic first, capped savings, adaptive engine, difficulty scale, anti-cheat, child experience, parent dashboard, local-first data, privacy, roadmap. Full decision log in `docs/CADRAGE.md`.
- Curriculum alignment added after the owner's request: skill graph derived from the 2025 CE1 livret d'accompagnement (programme of 22-10-2024). See `docs/curriculum/CE1-maths.md`.
- Repository created public under a provisional name. Next: choose the name, then UML-first design.

## 2026-10-20 — Curriculum decisions

- Read the cycle 1, CP and CE1 programme texts. Decisions C1–C4 and R4 recorded in `docs/CADRAGE.md`; prerequisite graph and fluence figures in `docs/curriculum/CE1-maths.md`.
- Corrections: multiplication and two-step problems are CE1 content.
- Name validated: Learn To Earn (`docs/CADRAGE.md`). Next: UML-first design.

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

- PR #4 merged 2026-10-23 (9fc03a7) after three Codex rounds (gate serialised under make -j, nested .env guard, unclosed Mermaid fence guard, check_docs docstrings 9/9). Codex quota ran out on the last head; merged on the owner's conditional approval with the local gate green (13 tests, 100 % coverage, SonarQube PASSED) and CI green.

## 2026-10-22 — Repository conformity (issue #9)

- Owner decision (MCDA A 450 / B 375 / C 195): one umbrella issue. GitHub Project "learn-to-earn" (#65), milestone "V0 conception", label `ci`, tracking issues #6-#8 for PRs #1-#3, Copilot review requested on #4.
- This PR: project `CLAUDE.md`, Dependabot (github-actions, pip), dependency review workflow. Ruleset on main and LICENSE are separate owner decisions.
- LICENSE: owner decision (MCDA A all rights reserved 445 / D PolyForm Noncommercial 385 / B MIT 320 / C AGPL-3.0 305), compatible with going private at the first production deployment.
- Codex follow-up on #1 (owner MCDA A 480 / B 390 / C 270): base category scored Easy 0 / Medium 2 / Hard 3 / Very hard 5, Base column in the V1.0 graph; node IDs use the dotted `<grade>.<name>` format.

## 2026-10-23 — Use-case spec follow-ups (PR #2)

- Codex follow-ups on #2 (owner MCDAs): session ends on a target duration, 15 min by default, 10-20 set by the Guardian (A 455 / C 400 / B 360); an interrupted timer is debited by device time since its start, capped, with a full debit if the clock went backwards (D 455 / B 400 / A 380 / C 260); expiry warnings show the real day.
- Domain model (#3) aligned with these decisions: `sessionTargetMinutes`, timer debit from device time since `startedAt` (`elapsedSeconds` removed), base level scores, dotted `SkillId`, encryption at rest as an adapter concern (#11).
- Dependabot #12 merged (c09fe79): coverage 7.6.1 → 7.16.2, local gate green.

## 2026-10-23 — Encryption at rest (ADR-0003, issue #11)

- Owner MCDAs: native whole-database SQLCipher with a start-up `cipher_version` guard (A 445 / C 320 / B 250); no child data stored on web (A 480 / B 260 / C 185); random key in Keystore/Keychain plus a passphrase-encrypted local export for recovery (C 450 / A 400 / B 230).

## 2026-10-23 — Sequence study and use-case review points (issue #13)

- Owner MCDAs on the #13 points (ADR-0001): UC-S4 folded into UC-S3 as V2 extension 4a, number retired (C 450 / B 355 / A 330); the 10 % challenge share is served only through challenge slots (A 470 / B 290 / C 250); UC-P2 states its own precondition (A 470 / B 365 / C 265); UC-L6 step 1 owns the acceptance (A 460 / B 440 / C 270); no direct Guardian link to UC-P12, now a subfunction of UC-P14 (A 480 / C 270 / B 240).
- OQ-5 closed (ADR-0002): erase removes everything, set-aside databases and key included, then restarts on the set-up (B 460 / A 360 / C 345); restore never brings back the reserve (credits kept as forfeited history, open requests closed), trusted time never moves back (C 420 / B 380 / A 310).
- Joint sequence review with the owner (2026-10-24): a wrong answer is retried on the same exercise; after the third hint the correct answer is shown with its worked step and earns nothing (ADR-0002 D14, A 440 / C 280 / B 260); a correct answer after hints earns a decreasing configured fraction (D15, B 425 / A 340 / C 215); an open request shows only its status.
- Ten analysis-level sequence diagrams (at most 7 lifelines each, `sd` titles, PII flagged): learning session, confidence scoring, remediation, crediting, screen-time request, approval, use, erase, restore, key-loss start. Spec (28 use cases), use-case diagrams, traceability matrix and README updated.
- Owner validated the ten sequence diagrams (2026-10-24).

## 2026-10-24 — Post-merge QA of the sequence study (PR #15, ac943f9)

- PR #15 was merged before `review-local` and the visual QA, against the pre-merge rule. Made up for on `main`: 18 renders inspected (13, plus the 5 domain model blocks after the Codex review), `review-local` run (`make check` green, Must 0, Should 4, Nice 3).
- Report and renders: `docs/architecture/qa/2026-10-24-sequence-study/`. Findings filed as issues #16–#20 on project #65.

## 2026-10-24 — Product story review (issue #22)

- Adversarial end-to-end read of the dossier (child's first week, then the parent's path): 35 findings in `docs/architecture/reviews/product-story-review-1.md`. 16 fixed directly, 19 decided by the owner in ADR-0004 (D1–D19).
- Main decisions: earning uses a standard time per level, never the real response time (D1 B 445); cold start at 70 % below the class level (D2 A 400); the 3-error rule counts exercises failed at the first try (D3 A 435); V1.0 rules without a minimum-time rule (D4 A 450); progress bonus of 2 min per new best mastery (D6 B 465); trusted time from monotonic elapsed time (D9 A 405); interrupted session resumable until the end of its day (D10 A 430); PIN lockout, scrambled pad and recovery code, OQ-1 closed (D13–D15); minimal parent note list in V1.0 (D16 A 430); streak active day = 10 correct answers (D18 B 455).
- CADRAGE, curriculum, use-case spec, domain model, sequences, traceability matrix and README updated; ADR-0002 D3, D8, D11 and ADR-0003 D3 point to the decisions that supersede them.
- Two totals shown in the chat were miscounted: D5 B shown 360 and D6 A shown 345, correct 355 and 335. Winners unchanged.
