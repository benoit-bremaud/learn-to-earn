# Local review — learn-to-earn (branch docs/curriculum-decisions vs main)

- Date: 2026-10-20
- Commit: 0e2e571 (+ README fix)
- Scope: branch diff main...HEAD, mode `--push` (no QA pass)
- Checks run: secrets, diff read, doc consistency. Design, tests and security agents skipped: the diff holds no code (docs, 3 skill files, log).
- Verdict: ship · Must 0 · Should 1 (fixed) · Nice 0

## Pre-merge gate (not a merge candidate yet)
| Step | Result |
|---|---|
| 1 Tests | n.a. (no code yet) |
| 2 Coverage | n.a. (no code yet) |
| 3 SonarQube | n.a. (no code, no Sonar project) |
| 4 Secrets | gitleaks clean (main..HEAD, 3 commits) · no tracked .env · diff read: nothing sensitive |
| 5 QA pass | skipped (`--push`) |

## 🔴 Must Have
_None._

## 🟡 Should Have
- `README.md:1,5` `[docs]` · title and text still said "working title" / "name is provisional" · fixed (name is Learn To Earn).

## 🔵 Nice to Have
_None._

## ⚪ Disagree / Intentional
- `PROJECT_LOG.md:7` `[docs]` · the earlier entry says "provisional name": it is a dated log line, kept as history.

## Per-dimension summary
- Design: n.a. · Docs: consistent after README fix · Tests: n.a. · Security: no secrets, privacy skill added · Correctness: fluence figures and tables schedule match the official text read earlier.
