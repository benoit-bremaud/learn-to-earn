# Use-case specifications — Learn To Earn

Format: Cockburn textual specs (goal level). Diagrams: `docs/architecture/diagrams/<domain>/01-use-case.md`. Modelling rules: ADR-0001. Decisions referenced (C1, M4, P3…) are the IDs of `docs/CADRAGE.md`.

## Actors

| Actor | Kind | Description |
|---|---|---|
| Learner | Primary | The child using the app (CE1 now, any child later). Never authenticates with a secret. |
| Guardian | Primary | The parent. Acts only inside the PIN-protected parent space. |
| DeviceOS | Secondary (V2) | The Android system that can block other apps when screen time ends. |

Not actors: the clock, the engine, the TTS library, storage (internal), and any LLM (none receives child data).

## Glossary

- **Reserve**: earned screen-time minutes saved, capped, expiring after 7 days (Q4).
- **Ceiling**: the school period (P1–P5) the class is at, set by the Guardian (C1).
- **Skill**: a node of the prerequisite graph (`docs/curriculum/CE1-maths.md`).

## Conventions

Every Guardian use case of the parent space has the precondition **parent space unlocked (UC-P1)**. Versions follow the roadmap of `docs/CADRAGE.md` §5.

---

## Learning domain

### UC-L1 — Complete a learning session (V1.0)
- Primary actor: Learner. Stakeholders: Guardian wants real progress, Learner wants a short fair session.
- Preconditions: a child profile exists.
- Minimal guarantee: answers already given are kept; no points are removed.
- Success guarantee: the session recap shows progress and the screen-time minutes earned, and the reserve is credited.
- Main success scenario:
  1. Learner starts a session.
  2. The app proposes an easy warm-up exercise.
  3. Learner answers it (include UC-L2).
  4. The app repeats steps 2–3 following the 70 % acquiring / 20 % review / 10 % challenge mix (M3), using the base level of each skill (C4), under the calendar ceiling (C1).
  5. The app proposes a final challenge, then shows the recap and the earned minutes (E3).
- Extensions:
  - 4a. A weak prerequisite is detected (3 errors in a row, or a failed review): the app lowers the level, then proposes UC-L5 (M4, R4). The parent is alerted (read in UC-P6).
  - 4b. The challenge slot comes up: UC-L6.
  - 4c. The confidence score falls below 0.3: 2-minute pause and neutral note for the parent (T2).
  - *a. Learner stops early: the partial recap is shown, earned minutes are credited for work done.
- Postcondition: mastery scores updated, reserve credited.
- Relationships: «include» UC-L2; «extend» by UC-L5 (extension point: weak prerequisite) and UC-L6 (extension point: challenge slot).

### UC-L2 — Answer an exercise (V1.0)
- Primary actor: Learner.
- Preconditions: an exercise is displayed.
- Success guarantee: the answer is recorded (correctness, response time) and feedback is shown, effort first (E2).
- Main success scenario:
  1. The app shows a statement and a numeric keypad (free numeric entry in V1.0).
  2. Learner types an answer and confirms.
  3. The app records correctness and time, updates the mastery score and the confidence score (M1, M2, T2).
  4. The app shows encouraging feedback with progress.
- Extensions:
  - 1a. Learner taps the read-aloud button: UC-L3.
  - 3a. The answer is wrong: the app proposes UC-L4.
  - 3b. The answer is faster than 40 % of her own average and under 1.5 s: the confidence score drops, no message accuses the child.
- Relationships: «extend» by UC-L3 (extension point: statement shown) and UC-L4 (extension point: wrong answer).

### UC-L3 — Listen to an exercise statement (V1.2)
- Primary actor: Learner. Preconditions: an exercise is displayed.
- Main scenario: Learner taps the speaker button; the statement is read aloud in French with the local voice (E4).
- Extensions: 1a. No French voice is available: the button is hidden.
- Success guarantee: nothing leaves the device (V4).

### UC-L4 — Retry with a hint (V1.0)
- Primary actor: Learner. Preconditions: the last answer was wrong.
- Main scenario:
  1. The app shows a hint following concrete, then picture, then symbol.
  2. Learner tries again.
- Extensions: 2a. Still wrong after 3 errors in a row: handled in UC-L1 step 4a.
- Success guarantee: no harsh red, no punishing sound (E2).

### UC-L5 — Rework an earlier skill (V1.1)
- Primary actor: Learner (the engine selects, the Learner works).
- Preconditions: a weak prerequisite exists in the skill graph (cycle 1, CP or CE1 level).
- Main scenario:
  1. The app presents a short run of exercises on the weak prerequisite inside the 20 % review share (R4).
  2. Learner answers them.
  3. Once the prerequisite recovers, the session returns to the target skill.
- Extensions: 1a. The Guardian forced this skill through UC-P7: it comes first in the next session.
- Success guarantee: the child is never told she is "behind", only that she is "warming up".

### UC-L6 — Take on a challenge exercise (V1.1)
- Primary actor: Learner. Preconditions: the challenge share (10 %) is due.
- Main scenario: the app proposes an exercise one notch higher, possibly a prudent look-ahead probe of a later period (C1), the Learner answers it.
- Extensions: 1a. A look-ahead probe succeeds repeatedly: only a neutral note to the Guardian is created (never a label).
- Success guarantee: the child is never pushed ahead of the class.

### UC-L7 — Calibrate keypad comfort (V1.2)
- Primary actor: Learner. Preconditions: first launch, or the Guardian requests a re-test.
- Main scenario: the Learner follows a 2-minute playful keypad task, the app records time to first key, inter-key time, neighbour-key errors, reversed digits and self-corrections (T1).
- Postcondition: the answer format is chosen from the measures. Statistics only, no diagnosis.

### UC-L8 — Check my progress and screen-time gauge (V1.0)
- Primary actor: Learner. Main scenario: the Learner opens the progress view and sees the gauge (reserve), streak and earned time. Never shows other children, never shows red.

### UC-L9 — Customise my companion (V1.2)
- Primary actor: Learner. Preconditions: a customisation item is unlocked by a day streak (E1).
- Main scenario: the Learner chooses an unlocked item for the mascot.

## Screen-time domain

### UC-S1 — Request screen time (V1.0)
- Primary actor: Learner. Preconditions: reserve above 0.
- Success guarantee: a pending request exists, nothing is spent yet.
- Main scenario: the Learner picks a duration up to the reserve and taps "Ask" (P3).
- Extensions: 1a. Reserve is 0: the app suggests a session instead. 1b. The daily cap (30 min of screen) is reached: the app says "enough for today".

### UC-S2 — Approve a screen-time request (V1.0)
- Primary actor: Guardian. Stakeholder: Learner wants her time quickly.
- Success guarantee: the request is approved or refused, never silently lost.
- Main scenario:
  1. Guardian sees the pending request.
  2. Guardian enters the PIN (include UC-P1).
  3. Guardian approves the duration.
  4. The timer is ready for UC-S3.
- Extensions: 3a. Guardian refuses: the reserve is unchanged. 2a. Wrong PIN: progressive lockout (P1).
- V2 note: approval from the parent's phone is an open question, not yet a separate use case.
- Relationships: «include» UC-P1.

### UC-S3 — Use approved screen time (V1.0)
- Primary actor: Learner. Preconditions: an approved request.
- Main scenario:
  1. Learner starts the timer, then plays or watches in another app.
  2. The app warns 5 minutes before the end.
  3. The timer ends with an alarm.
  4. The reserve is debited.
- Extensions: 1a. Learner stops early: only the time used is debited. 3a. In V2, the end is enforced: UC-S4.
- Note: in V1 this is declarative, the app cannot block other apps (Q1).
- Relationships: «extend» by UC-S4.

### UC-S4 — Enforce the end of screen time on the device (V2)
- Primary actor: Learner (via UC-S3). Secondary actor: DeviceOS (Android).
- Main scenario: at the end of UC-S3 the app asks the OS to block the other apps for the child's user.
- Extensions: 1a. Permission was not granted: fall back to the declarative behaviour.

### UC-S5 — Configure screen-time rules (V1.1)
- Primary actor: Guardian. Preconditions: parent space unlocked.
- Main scenario: the Guardian changes the conversion rate, the daily cap, the reserve cap and expiry (defaults: 1:1 up to 20 min of work then 2:1, 30 min per day, 7 days).
- Extensions: 1a. A value is outside safe bounds: the app refuses and explains.

## Parent-space domain

### UC-P1 — Unlock the parent space (V1.0)
- Primary actor: Guardian. Success guarantee: the parent space is open for a short session.
- Main scenario: the Guardian enters the 6-digit PIN (P1).
- Extensions: 1a. Wrong PIN: progressive lockout. 1b. Biometrics are not offered (the tablet is the child's).
- Open question OQ-1: recovery when the PIN is forgotten, without letting the child reset it.

### UC-P2 — Create the child profile (V1.0)
- Primary actor: Guardian. Main scenario: the Guardian enters a first name or pseudonym and a birth year, and the class level (V3).
- Extensions: 1a. A surname or photo is requested by mistake: the form has no such field.

### UC-P3 — Set the class calendar ceiling (V1.1)
- Primary actor: Guardian. Main scenario: the Guardian selects the current school period P1–P5 (C1).
- Postcondition: the engine caps unlocking below that period.
- Relationships: «extend» by UC-P4.

### UC-P4 — Allow skills beyond the class period (V1.1)
- Primary actor: Guardian. Preconditions: a ceiling is set.
- Main scenario: the Guardian authorises going ahead for chosen strands, accepting the risk of boredom at school.

### UC-P5 — Review the traffic-light dashboard (V1.0 minimal)
- Primary actor: Guardian. Main scenario: the Guardian sees one colour per skill (green at 80 % or more, orange 50–79 %, red below 50 % or falling) and the official fluence milestones (P2, C2).
- Relationships: «extend» by UC-P6.

### UC-P6 — Review alerts and the to-do-together list (V1.1)
- Primary actor: Guardian. Main scenario: the Guardian reads alerts (stuck skills, pauses, look-ahead facility note) and a "to do together" line.
- Extensions: 1a. Persistent keypad-comfort signals appear as a neutral note, never a diagnosis.

### UC-P7 — Send the child back to an earlier skill (V1.1)
- Primary actor: Guardian. Main scenario: the Guardian picks a skill and the engine schedules it first (R4).

### UC-P8 — Export the child's data (V1.0)
- Primary actor: Guardian. Success guarantee: a complete file the Guardian can keep (S1, V3).

### UC-P9 — Erase all data (V1.0)
- Primary actor: Guardian. Main scenario: the Guardian confirms erasure in one PIN-protected gesture; everything is deleted.
- Extensions: 1a. The Guardian cancels: nothing is deleted.

### UC-P10 — Change the PIN (V1.0)
- Primary actor: Guardian. Main scenario: the Guardian enters the current PIN then a new one twice.

### UC-P11 — Choose anonymous crash reporting (V1.1)
- Primary actor: Guardian. Main scenario: the Guardian enables or disables anonymous crash reports (V4). Default: off.

## Open questions

- OQ-1 PIN recovery.
- OQ-2 Remote approval on the parent's phone (V2): new use case or variant of UC-S2?
- OQ-3 Several children per Guardian (not in scope now).
