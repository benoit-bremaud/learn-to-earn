# Use-case specifications — Learn To Earn

Format: Cockburn textual specs. Diagrams: `diagrams/<domain>/01-use-case.md`. Modelling rules: [ADR-0001](../decisions/0001-use-case-modelling.md). References like "dec. M3" are decision IDs of `docs/CADRAGE.md` §2. "Period 1–5" are the school periods; "UC-" prefixes use cases.

## Actors

| Actor | Kind | Description |
|---|---|---|
| Learner | Primary | The child using the app (CE1 now, any child later). Never authenticates with a secret. |
| Guardian | Primary | The parent. Acts only inside the PIN-protected parent space. |
| DeviceOS | Secondary (V2) | The Android system that can block other apps when screen time ends. |

Not actors: the clock, the engine, the TTS library, storage (internal), any LLM (none receives child data).

## Glossary

- **Reserve**: earned screen-time minutes saved, capped, expiring after 7 days (dec. Q4).
- **Ceiling**: the school period (1–5) the class is at, set by the Guardian (dec. C1).
- **Skill**: a node of the prerequisite graph (`docs/curriculum/CE1-maths.md`).
- **Level**: Cockburn goal level, *user goal* or *subfunction* (a step reused by other goals, kept as a use case because it traces to its own product decision).

## Conventions

- Every use case of the parent space except UC-P1 and UC-P12 has the precondition **parent space unlocked (UC-P1)**.
- Versions follow the roadmap (`docs/CADRAGE.md` §5).
- An extension has a direct actor link in the diagrams only if the actor can start it on their own (ADR-0001 D2).

---

## Learning domain

### UC-L1 — Complete a learning session
- Level: user goal. Primary actor: Learner. Version: V1.0. Decisions: M3, M4, E3, C1, C4.
- Stakeholders: Guardian wants real progress, Learner wants a short fair session.
- Preconditions: a child profile exists.
- Minimal guarantee: answers already given are kept and no points are removed.
- Success guarantee: the recap shows progress and the minutes earned, and the reserve is credited.
- Main success scenario:
  1. Learner starts a session.
  2. The app proposes an easy warm-up exercise.
  3. Learner answers it (include UC-L2).
  4. The app repeats steps 2–3 following the 70 % acquiring / 20 % review / 10 % challenge mix (dec. M3), with the base level of each skill (dec. C4) under the ceiling (dec. C1).
  5. At the challenge slot the app offers a challenge exercise (extension point `challenge slot offered`).
  6. The app shows the recap and the earned minutes, and credits the reserve.
- Extensions:
  - 4a. A weak prerequisite is detected (3 errors in a row, or a failed review): the app lowers the level, raises an alert for the Guardian (read in UC-P6) and continues with UC-L5 (extension point `weak prerequisite detected`).
  - 4b. The Guardian scheduled a skill through UC-P7: the app continues with UC-L5 (same extension point).
  - 4c. The confidence score falls below 0.3: the app pauses for 2 minutes and leaves a neutral note for the Guardian (dec. T2).
  - 5a. Learner accepts the offer: UC-L6. 5b. Learner declines: the session goes on to step 6.
  - *a. Learner stops early: the partial recap is shown and minutes for the work done are credited.
- Extension points: `weak prerequisite detected`, `challenge slot offered`.
- Postcondition: mastery scores updated, reserve credited.
- Relationships: «include» UC-L2. «extend» from UC-L5 and UC-L6.

### UC-L2 — Answer an exercise
- Level: subfunction (included by UC-L1). Primary actor: Learner. Version: V1.0. Decisions: M1, M2, T2, E2.
- Preconditions: an exercise is displayed.
- Success guarantee: the answer is recorded (correctness, response time) and effort-first feedback is shown.
- Main success scenario:
  1. The app shows a statement and a numeric keypad (free numeric entry in V1.0).
  2. Learner types an answer and confirms it.
  3. The app records correctness and time and updates the mastery and confidence scores.
  4. The app shows encouraging feedback with progress.
- Extensions:
  - 1a. Learner taps the read-aloud button: UC-L3 (extension point `statement shown`).
  - 3a. The answer is wrong: UC-L4 (extension point `wrong answer`).
  - 3b. The answer is faster than 40 % of her own average and under 1.5 s: the confidence score drops and no message accuses the child.
- Extension points: `statement shown`, `wrong answer`.
- Relationships: «extend» from UC-L3 and UC-L4.

### UC-L3 — Listen to an exercise statement
- Level: subfunction. Primary actor: Learner. Version: V1.2. Decision: E4.
- Preconditions: an exercise is displayed and a French voice is available.
- Success guarantee: the statement is read aloud with the local voice, nothing leaves the device (dec. V4).
- Main success scenario:
  1. Learner taps the speaker button.
  2. The app reads the statement aloud.
- Extensions: 2a. Learner taps again: the reading restarts.
- Business rule: no French voice means the button is not shown.

### UC-L4 — Retry with a hint
- Level: subfunction. Primary actor: Learner (actor inherited from UC-L2). Version: V1.0. Decisions: M4, E2.
- Preconditions: the last answer was wrong.
- Success guarantee: the Learner retries without a punishing signal.
- Main success scenario:
  1. The app shows a hint (concrete, then picture, then symbol).
  2. Learner tries again (back to UC-L2 step 2).
- Extensions: 2a. Three errors in a row: UC-L1 extension 4a.
- Business rule: no harsh red, no punishing sound.

### UC-L5 — Rework an earlier skill
- Level: user goal segment. Primary actor: Learner (actor inherited from UC-L1). Version: V1.1. Decisions: R4, M4, C3.
- Selected by the system as a conditional segment of UC-L1; the Learner does the work.
- Preconditions: a weak prerequisite exists in the skill graph (cycle 1, CP or CE1 level), or the Guardian scheduled a skill.
- Success guarantee: the prerequisite is exercised inside the 20 % review share and the child is told she is "warming up", never "behind".
- Main success scenario:
  1. The app presents a short run of exercises on the prerequisite.
  2. Learner answers them (UC-L2).
  3. The prerequisite score recovers and the session returns to the target skill.
- Extensions: 3a. The prerequisite is still weak: the app goes one more node down the graph and an alert is raised for the Guardian.

### UC-L6 — Take on a challenge exercise
- Level: user goal. Primary actor: Learner. Version: V1.1. Decisions: M3, C1.
- Preconditions: the challenge slot is offered (UC-L1 step 5).
- Success guarantee: the child is never pushed ahead of the class beyond the Guardian's ceiling settings.
- Main success scenario:
  1. Learner accepts the offered challenge.
  2. The app proposes an exercise one notch higher, possibly a prudent look-ahead probe of a later period.
  3. Learner answers it (UC-L2).
- Extensions: 3a. Look-ahead probes succeed repeatedly: a neutral note for the Guardian is created, never a label.

### UC-L7 — Calibrate keypad comfort
- Level: user goal. Primary actor: Learner. Version: V1.2. Decision: T1.
- Preconditions: first launch, or the Guardian requested a re-test (UC-P13).
- Success guarantee: the answer format is chosen from the measures. Statistics only, no diagnosis.
- Main success scenario:
  1. The app explains a short playful task.
  2. Learner types the requested numbers for about 2 minutes.
  3. The app records time to first key, inter-key time, neighbour-key errors, reversed digits and self-corrections.
  4. The app picks the answer format.
- Extensions: 2a. Learner stops: the partial measures are kept and the default format is used.

### UC-L8 — Check progress and the screen-time gauge
- Level: user goal. Primary actor: Learner. Version: V1.0. Decisions: E1, Q4.
- Success guarantee: the Learner sees reserve, streak and earned time, never another child, never red.
- Main success scenario:
  1. Learner opens the progress view.
  2. The app shows the gauge, the streak and the recent progress.
- Extensions: 2a. No session yet: the app invites the Learner to start one.

### UC-L9 — Customise the companion
- Level: user goal. Primary actor: Learner. Version: V1.2. Decision: E1.
- Preconditions: at least one item is unlocked by a day streak.
- Main success scenario:
  1. Learner opens the companion wardrobe.
  2. Learner picks an unlocked item.
  3. The app shows the companion with the item.
- Extensions: 2a. Learner picks a locked item: the app shows how many streak days are missing.

## Screen-time domain

### UC-S1 — Request screen time
- Level: user goal. Primary actor: Learner. Version: V1.0. Decisions: Q1, P3, Conversion.
- Success guarantee: a pending request exists and nothing is spent.
- Main success scenario:
  1. Learner opens the screen-time request.
  2. Learner picks a duration up to the reserve.
  3. Learner taps "Ask".
  4. The app records a pending request for the Guardian.
- Extensions:
  - 2a. Reserve is 0: the app suggests starting a session (UC-L1) and no request is created.
  - 2b. The daily cap (30 min of screen) is reached: the app says "enough for today".

### UC-S2 — Approve a screen-time request
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decisions: P1, P3.
- Stakeholder: Learner wants her time quickly.
- Preconditions: a pending request exists.
- Success guarantee: the request is approved or refused, never silently lost.
- Main success scenario:
  1. Guardian opens the pending request.
  2. Guardian enters the PIN (include UC-P1).
  3. The app shows the child, the duration and the reserve.
  4. Guardian approves.
  5. The timer is ready for UC-S3.
- Extensions: 4a. Guardian refuses: the reserve is unchanged and the Learner sees a neutral message.
- Business rule: wrong-PIN handling is owned by UC-P1.
- Relationships: «include» UC-P1. V2 note: approval on the parent's phone is open (OQ-2).

### UC-S3 — Use approved screen time
- Level: user goal. Primary actor: Learner. Version: V1.0. Decisions: Q1, P3.
- Preconditions: an approved request.
- Success guarantee: the used time is debited from the reserve.
- Main success scenario:
  1. Learner starts the timer.
  2. Learner plays or watches in another app.
  3. The app warns 5 minutes before the end.
  4. The timer ends with an alarm (extension point `timer ended`).
- Extensions: 2a. Learner stops early: only the time used is debited.
- Extension points: `timer ended`.
- Postcondition: the reserve is debited.
- Business rule: in V1 the app cannot block other apps (declarative, dec. Q1).
- Relationships: «extend» from UC-S4.

### UC-S4 — Enforce the end of screen time on the device
- Level: user goal segment. Primary actor: Learner (actor inherited from UC-S3, the Guardian is the beneficiary). Secondary actor: DeviceOS. Version: V2. Decisions: Q1, P0.
- Preconditions: blocking permission was granted on this Android user.
- Main success scenario:
  1. The timer ends (UC-S3 extension point).
  2. The app asks DeviceOS to block the other apps for the child's user.
  3. DeviceOS confirms.
- Extensions: 3a. DeviceOS refuses: the app falls back to the declarative alarm.

### UC-S5 — Configure screen-time rules
- Level: user goal. Primary actor: Guardian. Version: V1.1. Decisions: Q4, Conversion.
- Preconditions: parent space unlocked.
- Main success scenario:
  1. Guardian opens the rules.
  2. Guardian edits conversion rate, daily cap, reserve cap or expiry (defaults: 1:1 up to 20 min of work then 2:1, 30 min a day, 7 days).
  3. The app saves the rules.
- Extensions: 2a. A value is outside safe bounds: the app refuses and explains.

## Parent-space domain

### UC-P1 — Unlock the parent space
- Level: subfunction (included by UC-S2). Primary actor: Guardian. Version: V1.0. Decision: P1.
- Preconditions: a PIN exists (UC-P12).
- Success guarantee: the parent space is open for a short session.
- Main success scenario:
  1. Guardian enters the 6-digit PIN.
  2. The app opens the parent space.
- Extensions: 1a. Wrong PIN: progressive lockout.
- Business rule: no biometrics (the tablet is the child's).
- Open question OQ-1: recovery when the PIN is forgotten, without letting the child reset it.

### UC-P2 — Create the child profile
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decisions: V3, P0.
- Success guarantee: a profile with first name or pseudonym, birth year and class level exists.
- Main success scenario:
  1. Guardian opens profile creation.
  2. Guardian enters a first name or pseudonym, a birth year and the class level.
  3. The app saves the profile.
- Extensions: 2a. A field is missing or invalid: the app asks again.
- Business rule: the form has no field for surname, photo or child e-mail.

### UC-P3 — Set the class calendar ceiling
- Level: user goal. Primary actor: Guardian. Version: V1.1. Decision: C1.
- Success guarantee: the engine caps skill unlocking below the chosen period.
- Main success scenario:
  1. Guardian opens the calendar.
  2. Guardian selects the school period (1–5) the class is at.
  3. The app saves the ceiling.
- Extensions: 2a. Guardian never sets it: the default is the current school period computed from the date.

### UC-P4 — Allow skills beyond the class period
- Level: user goal. Primary actor: Guardian. Version: V1.1. Decision: C1.
- Preconditions: a ceiling is set.
- Success guarantee: chosen strands may be unlocked ahead of the class.
- Main success scenario:
  1. Guardian opens the advance settings and reads the warning that the child may get bored at school.
  2. Guardian chooses the strands.
  3. The app saves the choice.
- Extensions: 2a. Guardian chooses none: the ceiling stays strict.

### UC-P5 — Review the traffic-light dashboard
- Level: user goal. Primary actor: Guardian. Version: V1.0 minimal. Decisions: P2, C2.
- Preconditions: parent space unlocked.
- Success guarantee: the Guardian sees one colour per skill and the official fluence milestones.
- Main success scenario:
  1. Guardian opens the dashboard.
  2. The app shows green (80 % or more, stable), orange (50–79 %) or red (below 50 % or falling) per skill.
  3. The app shows the fluence milestones next to the personal records.
- Extensions: 2a. No data yet: the app explains that results appear after the first sessions.

### UC-P6 — Review alerts and the to-do-together list
- Level: user goal. Primary actor: Guardian. Version: V1.1. Decisions: P2, M4, T1, C1.
- Preconditions: parent space unlocked.
- Main success scenario:
  1. Guardian opens the alerts.
  2. The app lists stuck skills, pauses and notes, and a "to do together" line.
  3. Guardian marks alerts as read.
- Extensions: 2a. Persistent keypad-comfort signals appear as a neutral note, never a diagnosis. 2b. A look-ahead facility note appears, never a label.

### UC-P7 — Send the child back to an earlier skill
- Level: user goal. Primary actor: Guardian. Version: V1.1. Decision: R4.
- Preconditions: parent space unlocked.
- Success guarantee: the chosen skill comes first in the next session through UC-L5.
- Main success scenario:
  1. Guardian opens the skill list.
  2. Guardian picks a skill.
  3. The app schedules it.

### UC-P8 — Export the child's data
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decisions: S1, V3.
- Preconditions: parent space unlocked.
- Success guarantee: a complete file the Guardian can keep.
- Main success scenario:
  1. Guardian asks for an export.
  2. The app builds the file.
  3. The app hands the file to the Guardian.
- Extensions: 2a. Export fails: nothing is changed and the app says so.

### UC-P9 — Erase all data
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decisions: S1, V1.
- Preconditions: parent space unlocked.
- Success guarantee: all child data is deleted.
- Main success scenario:
  1. Guardian asks to erase everything.
  2. Guardian confirms in one PIN-protected gesture.
  3. The app deletes all data and shows a confirmation.
- Extensions: 2a. Guardian cancels: nothing is deleted.

### UC-P10 — Change the PIN
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decision: P1.
- Preconditions: parent space unlocked.
- Main success scenario:
  1. Guardian enters the new PIN twice.
  2. The app stores it hashed.
- Extensions: 1a. The two entries differ: the app asks again.

### UC-P11 — Choose anonymous crash reporting
- Level: user goal. Primary actor: Guardian. Version: V1.1. Decision: V4.
- Preconditions: parent space unlocked.
- Main success scenario:
  1. Guardian opens the privacy settings.
  2. Guardian enables or disables anonymous crash reports.
- Business rule: default is off.

### UC-P12 — Set the parent PIN
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decision: P1.
- Preconditions: first launch, no PIN yet.
- Success guarantee: a hashed 6-digit PIN exists and the parent space can be unlocked.
- Main success scenario:
  1. Guardian chooses a 6-digit PIN twice.
  2. The app stores it hashed.
- Extensions: 1a. The two entries differ or the PIN is trivial (000000, 123456): the app asks again.

### UC-P13 — Request keypad re-calibration
- Level: user goal. Primary actor: Guardian. Version: V1.2. Decision: T1.
- Preconditions: parent space unlocked.
- Main success scenario:
  1. Guardian asks for a re-test.
  2. The app marks the next launch to run UC-L7. The two use cases are linked by data, not by a UML relationship.

## Open questions

- OQ-1 PIN recovery without letting the child reset it.
- OQ-2 Remote approval on the parent's phone (V2): new use case or variant of UC-S2.
- OQ-3 Several children per Guardian (not in scope now).
