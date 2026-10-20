# Project brief — Learn To Earn

Status: brainstorming complete on 2026-10-20, UML-first design is the next step. Every decision below comes from an MCDA matrix (weights /100, scores 0–5, total /500) validated by the owner.

## 1. Vision

A mobile/web app that helps a CE1 child (7–8 years old) master reading, writing and arithmetic. The app adapts to the child (correctness + response speed), insists on weak skills, and converts good work into earned screen time (YouTube, Roblox…). Merit-based: the better you work, the more you may watch or play. The app also limits screen time (declarative in V1, automatic blocking on Android in V2).

Guiding principle (owner, 2026-10-20): effort first, comfort after. The name says it: the child learns that screen time is earned by work, never given up front. Every flow (session, reserve, validation, wording) must respect that order.

Primary user: the owner's daughter (CE1). Secondary: other parents, later (distribution decision deferred).

## 2. Decision log

| # | Topic | Decision | Score |
|---|---|---|---|
| Q1 | Screen-time control | Staged: V1 declarative (parent validates), V2 automatic Android blocking | 415 |
| Q2 | Platform | Expo (React Native): Android, iOS, web (Ubuntu PC runs the web build) | 440 |
| Q3 | V1 subject | Arithmetic (CE1). Reading comes in V2 on the same engine | 460 |
| Q4 | Points | Capped savings, weekly expiry (7 days) | 450 |
| — | Conversion | Degressive: 1 min work = 1 min screen up to 20 min of work, then 2:1, cap 30 min screen/day | 430 |
| M1 | Mastery | 0–100 % score per skill, weighted moving average (correctness + speed) | 400 |
| M2 | Response time | Compared with the child's own average on that skill; only after a correct answer; never removes points | 450 |
| M3 | Next exercise | 70 % skills being acquired (~80 % success zone), 20 % spaced review, 10 % challenge | 450 |
| M4 | Stuck | After 3 errors in a row: drop one level, visual hint, encouraging message, parent alert | 450 |
| D1 | Difficulty | Rule-based scale (below), coefficients configurable, empirical recalibration in V2 | 415 |
| D2 | Multipliers | Easy 1 / Medium 1.5 / Hard 2 / Very hard 3 | 400 |
| T1 | Answer format | Format driven by numeric-keypad comfort (detection V1, keypad mini-games V1.5) | 440 |
| T2 | Anti-cheat | Multi-signal confidence score in V1; hidden control questions added later | 415 |
| E1 | Universe | Light companion: mascot, always-visible screen-time gauge, modest customisation unlocked by day streaks | 410 |
| E2 | Feedback | Effort and progress first, errors = hint + retry, no harsh red or sound, points in the background | 440 |
| E3 | Session | Short framed session (10–20 min): easy warm-up, core, final challenge, recap with screen time earned | 455 |
| E4 | Audio | Optional read-aloud button on every statement (native French TTS) | 475 |
| P1 | Parent space | 6-digit PIN, progressive lockout; validation on the parent's phone targeted for V2 | 385 |
| P2 | Parent dashboard | Traffic-light view per skill (green ≥ 80 %, orange 50–79 %, red < 50 % or falling), alerts, "to do together" line | 465 |
| P3 | Validation | Reserve → child asks → parent PIN → timer → 5-min warning → alarm → reserve debited | 395 |
| P0 | Profiles | In-app child/parent profiles (base) + dedicated OS session where available (Android user, Ubuntu session) | 405 |
| S1 | Data | Local-first (export/import); optional encrypted sync in V1.5 | 425 |
| S2 | Distribution | Family first, decision deferred (decide after 4–6 weeks of real use); open source is the likely next step | 425 |
| V1 | Retention | Detailed answers 90 days, then weekly aggregates | 420 |
| V3 | Identity | First name or pseudonym + birth year; no surname, photo or child e-mail | 435 |
| V4 | Third parties | Zero trackers, zero child data sent out, local TTS, anonymous crash reports only if the parent opts in | 425 |
| R1 | Slicing | Minimal vertical slice first | 435 |
| R2 | Order | V1.1 complete engine + anti-cheat together, then V1.2 experience | 420 |
| R3 | Tests | TDD for the engine (pure domain), test-after for the UI | 435 |

Name: **Learn To Earn**, validated by the owner on 2026-10-20 (same as the repository name).

### Curriculum alignment (2026-10-20)

Details in `docs/curriculum/CE1-maths.md`.

| # | Topic | Decision | Score |
|---|---|---|---|
| C1 | Unlocking | Parent sets the calendar ceiling; mastery unlocks below it; prudent look-ahead probes in the challenge share; never label giftedness, neutral parent note only | 430 |
| C2 | Fluence | Hybrid: score relative to the child using the app; official benchmarks as dashboard milestones | 480 |
| C3 | V1.0 skills | Additive core + tables x2/x5/x10 + prerequisite graph down to cycle 1/CP | 400 |
| C4 | Difficulty | Base level per skill (official table schedule) + modifiers | 425 |
| R4 | Remediation | Reactive, inside the 20 % review share, plus parent "go back to X" button | 460 |

Multiplication is core CE1 content; two-step problems are CE1 content (corrected).

### Architecture principles (owner rule 2026-10-20)

Clean Architecture (dependency rule, proportional layering), SOLID, no anti-patterns, DRY and YAGNI are binding. Detail in `docs/architecture/README.md`.

## 3. Engine rules (all values configurable)

Difficulty score = operation (+0, −1, ×3) + size of largest number (≤20: 0, ≤100: 2, ≤1000: 3) + 1 per carry/borrow/tens crossing + 2 per extra step − 1 for round numbers.
Note (2026-10-20): this formula now only provides modifiers; the base level comes from each skill (C4).
Levels: 0–1 Easy, 2 Medium, 3–4 Hard, 5+ Very hard. A level unlocks once the previous one reaches 70 % mastery. The engine picks the level, the child only picks within the 10 % challenge share.

Confidence score (starts at 1.0): −0.2 answer faster than 40 % of her own average (and under 1.5 s); −0.2 three fast errors in a row; −0.2 repeated identical answer; −0.1 success on new but failure on review; +0.05 per plausible correct answer. Below 0.6: points × confidence, easier exercise, neutral message. Below 0.3: 2-minute pause and parent note. Slow is never a signal.

Numeric-keypad comfort: measure time to first key, inter-key time, neighbour-key errors, reversed or mirrored digits, self-correction. It is a skill like any other. Statistics only, never a diagnosis and never health data; persistent signals show up as a neutral note to the parent.

## 4. Privacy and compliance

- French digital majority is 15: parental consent is required below that age (not legal advice, check with the CNIL before publishing).
- PIN stored hashed. Parent can export and erase everything in one gesture (PIN-protected), a legal baseline rather than a choice.
- No LLM receives the child's answers: exercises are generated by rules in code.

## 5. Roadmap

| Version | Content |
|---|---|
| V0 | Repository, CI, Expo structure, UML validated, exercise generator + mastery engine unit-tested without UI |
| V1.0 | Profiles + PIN, framed session, simple addition/subtraction, free numeric entry (no multiple choice), simple minimum-time rule, mastery score, points and reserve, parent validation + timer, minimal traffic-light view, local storage |
| V1.1 | 4-level scale + multipliers, 70/20/10 mix, spaced review, 3-error rule, full confidence score, calendar ceiling, alerts, warning before reserve minutes expire, opt-in anonymous crash reports |
| V1.2 | Keypad comfort + driven format, light companion, audio, effort-first feedback |
| V1.5 | Sync across devices, keypad mini-games, hidden control questions |
| V2 | Android automatic blocking, automatic difficulty recalibration, reading |

## 6. Open questions

- Making the app official later (children's-data regulation, GDPR, store rules): deliberately postponed by the owner until the family-first phase has proven the concept (S2).
- Device where she plays Roblox (decides the V2 blocking target); no official Linux Roblox client to my knowledge, to be checked.
- Tablet model (Android multi-user support varies).
- Success-rate hypotheses used in the multiplier simulation (95/80/65/40 %) and every threshold above are to be calibrated after one week of real use.
- Licence if open-sourced (MIT or AGPL).

## 7. Next steps

1. UML-first: use-case, sequence, component, class, state and data-flow diagrams (Mermaid) under `docs/architecture/diagrams/<feature>/`.
2. Validate diagrams, then start V0.
