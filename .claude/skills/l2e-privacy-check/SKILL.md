---
name: l2e-privacy-check
description: Privacy and child-safety checklist for Learn To Earn changes. Use before every push or PR that touches data storage, analytics, network calls, dependencies, the parent PIN, exports or exercise generation, and whenever the app is reviewed for the public release or an official compliance step.
---

# Privacy check

The app is used by a child of 7-8. Decisions V1, V3, V4, P1 are binding. This is an engineering checklist, not legal advice (French digital majority is 15; check with the CNIL before any public distribution).

## Checklist (answer yes/no with evidence from the diff)

1. No tracker, ad SDK, analytics or fingerprinting dependency added (check `package.json` and lockfile diff).
2. No network call sends child data. Local TTS only. Crash reports only if the parent opted in, and anonymous.
3. Identity data is limited to first name or pseudonym plus birth year. No surname, photo or child e-mail.
4. Detailed answers are kept 90 days, then aggregated weekly. Retention job and tests still pass.
5. PIN: 6 digits, stored hashed, progressive lockout, no biometrics.
6. Parent can export and erase everything in one PIN-protected gesture; the change did not break it.
7. No LLM or external service receives the child's answers; exercises come from rules in code.
8. Keypad-comfort and anti-cheat signals stay statistics only: no diagnosis, no health data, neutral wording to the parent.
9. No secrets or personal data in the repo, logs, fixtures or screenshots (`gitleaks detect --source . --verbose`).
10. UI wording stays effort-first: no shaming, no harsh red or sound.

## Output

A short table of the ten items with pass / fail / n.a. and the file or line backing each. Any fail is a Must Have before push; also run `security-policy` for code-level rules.
