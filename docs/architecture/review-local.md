# Local review — learn-to-earn (CI workflow, issue #5)

- Date: 2026-10-22
- Commit: on top of beee542 (`chore/sonarqube-setup`)
- Scope: `.github/workflows/ci.yml`, `Makefile` (`ci` target), README and PROJECT_LOG lines
- Checks run: security + correctness (opus subagent) · design, docs, tests inline (tooling-only diff, no code under test)
- Verdict: ship after fixes · Must 1 (fixed) · Should 3 (2 fixed) · Nice 3 (1 fixed)

## Pre-merge gate (push mode, QA step not applicable)
| Step | Result |
|---|---|
| 1 Tests | ✅ unit tests of `scripts/` · ✅ Mermaid render · ✅ `check_docs.py` 0 errors |
| 2 Coverage | tests 100 % lines / 100 % branches (floor 80) · docs n/a (no new code) |
| 3 SonarQube | ✅ PASSED (local instance) |
| 4 Secrets | ✅ gitleaks git (34 commits) and dir clean · no tracked .env · diff read: only a public SHA-256 |
| 5 QA pass | n/a — tooling diff; the workflow itself is proven by its first run on PR #4 |

## 🔴 Must Have
- `.github/workflows/ci.yml` `[security]` · gitleaks downloaded without checksum · **fixed**: SHA-256 from the release's checksums.txt, `sha256sum -c`.

## 🟡 Should Have
- `.github/workflows/ci.yml` `[correctness]` · extract to `/usr/local/bin` without sudo · **fixed**: `$RUNNER_TEMP/bin` + `$GITHUB_PATH`.
- `.github/workflows/ci.yml` `[security]` · puppeteer downloads its own Chrome · **fixed**: `PUPPETEER_SKIP_DOWNLOAD=true`.
- `requirements-dev.txt` `[security]` · no hash pinning, no npm lockfile for mermaid-cli · open: follow-up, low risk (one pinned package, exact mermaid-cli version).

## 🔵 Nice to Have
- `.github/workflows/ci.yml` `[correctness]` · workflow name in the concurrency group · **fixed**.
- `.github/workflows/ci.yml` `[correctness]` · explicit `PUPPETEER_EXECUTABLE_PATH` redundant · **fixed** (removed, the script finds Chrome).
- `scripts/render_mermaid.sh:9` `[docs]` · comment could cite the Ubuntu 24.04 AppArmor reason for `--no-sandbox` · open.

## ⚪ Disagree / Intentional
- SonarQube not in CI · owner decision on issue #5 (MCDA B 440).

## Per-dimension summary
- Design: one job, no duplication with `make check` (reuses targets) · Docs: README + log updated · Tests: workflow runs the existing suite · Security: least-privilege, SHA-pinned actions, verified binary · Correctness: first CI run on PR #4 is the proof.
