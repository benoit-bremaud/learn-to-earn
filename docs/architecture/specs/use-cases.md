# Use-case specifications — Learn To Earn

Format: Cockburn textual specs. Diagrams: `diagrams/<domain>/01-use-case.md`. Modelling rules: [ADR-0001](../decisions/0001-use-case-modelling.md). References like "dec. M3" are decision IDs of `docs/CADRAGE.md` §2. "Period 1–5" are the school periods; "UC-" prefixes use cases.

## Actors

| Actor | Kind | Description |
|---|---|---|
| Learner | Primary | The child using the app (CE1 now, any child later). Never authenticates with a secret. |
| Guardian | Primary | The parent. Acts only inside the PIN-protected parent space. |
| DeviceOS | Secondary (V2) | The Android system that can block other apps when screen time ends (UC-S3 extension 4a). |

Not actors: the clock, the engine, the TTS library, storage (internal), any LLM (none receives child data).

## Glossary

- **Reserve**: earned screen-time minutes saved, capped, expiring after 7 days (dec. Q4).
- **Ceiling**: the school period (1–5) the class is at, set by the Guardian (dec. C1).
- **Skill**: a node of the prerequisite graph (`docs/curriculum/CE1-maths.md`).
- **Difficulty level**: Easy, Medium, Hard, Very hard (dec. D1, C4).
- **Standard time**: the minutes a correct answer earns before its factors, one base value of 35 s per correct answer in configuration, multiplied from V1.1 by the difficulty multiplier (ADR-0004 D1, D5).
- **Trusted time**: the last trusted instant advanced by the device's monotonic elapsed time (ADR-0004 D9); it sets the LocalDay.
- **Mastered**: a skill whose mastery is 70 % or more, the unlock threshold (ADR-0004 D4).
- **Active day**: a LocalDay with at least 10 correct answers, across sessions (ADR-0004 D18).
- **Level**: Cockburn goal level, *user goal* or *subfunction* (a step reused by other goals, kept as a use case because it traces to its own product decision).

## Conventions

- Every use case of the parent space except UC-P1, UC-P2, UC-P12 and UC-P14 has the precondition **parent space unlocked (UC-P1)**. UC-P2 states its own precondition, because UC-P14 also includes it at first launch.
- Versions follow the roadmap (`docs/CADRAGE.md` §5). A step or extension that ships later than its use case is tagged inline, for example *(V1.1)*.
- Moving between profiles (dec. P0): a parent entry point is visible on every child screen and leads to UC-P1. Leaving the parent space, or 2 minutes without activity, locks it and returns to the child profile. Setting up an Android user or an Ubuntu session for the child is done outside the app and is not a use case.
- An extension has a direct actor link in the diagrams only if the actor can start it on their own (ADR-0001 D2).

---

## Learning domain

### UC-L1 — Complete a learning session
- Level: user goal. Primary actor: Learner. Version: V1.0. Decisions: E3, M3, M4, C1, C3, C4, T2, Conversion, ADR-0004 D1–D6, D10, D11.
- Stakeholders: Guardian wants real progress, Learner wants a short fair session.
- Preconditions: a child profile exists.
- Minimal guarantee: answers already given are kept and no earned minutes are removed.
- Success guarantee: the recap shows progress and the minutes earned, and the reserve is credited.
- Main success scenario:
  1. Learner starts a session.
  2. The app proposes an easy warm-up exercise on a mastered skill.
  3. Learner answers it (include UC-L2).
  4. After the warm-up, the app keeps proposing exercises that the Learner answers (step 3) on the V1.0 skill set (dec. C3) until the session's target duration is reached: 15 minutes (dec. E3), fixed in V1.0 and set by the Guardian between 10 and 20 in UC-S5 *(V1.1)*, counted from the start of the warm-up, only while the app is open (RUNNING or PAUSED, ADR-0004 D10). The exercise in progress is finished, then the session moves to step 5. In V1.0 the app picks the lowest unmastered skill (ties: lowest grade, then graph depth, then table order) whose prerequisites are all at 70 % or more (ADR-0004 D4); step-down rule: after 3 exercises in a row failed at the first try on a skill (D3 counting), each of its prerequisites that still holds its seeded starting mastery (no real attempt yet) drops to 60 %, below mastered, so the picker serves the lowest of them next; no parent alert or Remediation in V1.0. *(V1.1)* Exercises follow the 70 % acquiring / 20 % review / 10 % challenge mix (dec. M3); the 10 % challenge share is served only through the challenge slots of step 5, never as engine-imposed challenge exercises (ADR-0001 D9), the base difficulty level of each skill (dec. C4) and the ceiling (dec. C1). In V1.0 there is no ceiling: the fixed skill set stands in for it.
  5. *(V1.1)* When a challenge slot comes up (about one exercise in ten), the app offers a challenge exercise (extension point `challenge slot offered`). The offer is a single button shown only at that moment.
  6. The app shows the recap and the earned minutes, and credits the reserve.
- Extensions:
  - 4a. *(V1.1)* A weak prerequisite is detected (3 exercises in a row failed at the first try, ADR-0004 D3, or a failed review): the app lowers the level, raises an alert for the Guardian (read in UC-P6) and continues with UC-L5 (extension point `weak prerequisite detected`).
  - 4b. *(V1.1)* The Guardian scheduled a skill through UC-P7: right after the warm-up, the app continues with UC-L5 for a block of 5 exercises on that skill, which then joins the review share (same extension point, ADR-0004 D11).
  - 4c. *(V1.1)* The confidence score falls below 0.3: the app pauses for 2 minutes and leaves a neutral note for the Guardian (dec. T2).
  - 5a. The offer is taken up: UC-L6 runs, starting with its own acceptance step. 5b. Learner declines or ignores the offer: the slot is filled by an ordinary exercise and the session resumes at step 4.
  - *a. Learner stops early: the partial recap is shown and minutes for the work done are credited.
  - *b. The session is interrupted (app closed, call, battery): answers are kept and the session length stops counting; the app time already spent is saved, so a resumed session keeps its target (ADR-0005 D4). On a launch the same LocalDay the app offers to resume or shows the partial recap; after the end of its LocalDay the session is closed as stopped early and credited (ADR-0004 D10).
- Business rule: only correct answers earn work minutes: the base standard time, weighted by difficulty, confidence and hints, never her real response time (ADR-0004 D1; V1.0 uses multiplier 1 and confidence factor 1, D4). Standard times are set so a 15-minute session at 80 % success earns about 15 minutes (D5); the base standard time is 35 s per correct answer in configuration (24 correct out of 30 in 15 min, 900 s / 24 is about 37 s, rounded to 35); from V1.1 it is multiplied by the difficulty multiplier (Medium 52.5 s, Hard 70 s, Very hard 105 s credited), which reflects the longer exercises, so the session earns about 15 min at any level; V1.0 uses 35 s for every skill. Each skill whose mastery beats its own best by 5 points or more during the session adds a fixed progress bonus, 2 minutes by default (D6); the best starts at the skill's initial mastery (70 for a cold-started skill, 0 otherwise) and is updated at each final close (owner 2026-10-21: the goal is learning results that are good and rising, not time spent). Minutes credited follow the degressive conversion (1 min of work = 1 min of screen up to 20 min of work, then 2:1), up to the reserve cap. The 20-minute threshold counts the work of the whole day, across sessions, so splitting the work into several sessions never changes the minutes earned.
- Extension points: `weak prerequisite detected`, `challenge slot offered`.
- Postcondition: mastery scores updated, reserve credited.
- Relationships: «include» UC-L2. «extend» from UC-L5 and UC-L6.

### UC-L2 — Answer an exercise
- Level: subfunction (included by UC-L1). Primary actor: Learner. Version: V1.0. Decisions: M1, M2, T1, T2, E2, ADR-0004 D4, D7, D8.
- Preconditions: an exercise is displayed.
- Success guarantee: the answer is recorded (correctness, response time) and effort-first feedback is shown.
- Main success scenario:
  1. The app shows a statement and a numeric keypad (free numeric entry in V1.0).
  2. Learner types an answer and confirms it.
  3. The app records correctness and time and updates the mastery score. Speed counts only after a correct answer and never removes earned minutes (dec. M2): a wrong or slow answer never lowers the timing part of mastery. V1.0 has no minimum-time rule (ADR-0004 D4). *(V1.1)* The confidence score is updated; the first session of a LocalDay starts at 1.0, a later one from the day's last value (ADR-0004 D7). *(V1.2)* Keypad signals are recorded (dec. T1).
  4. The app shows feedback. *(V1.2)* Feedback is effort-first with progress (dec. E2).
- Extensions:
  - 1a. Learner taps the read-aloud button: UC-L3 (extension point `statement shown`).
  - 3a. The answer is wrong: UC-L4 (extension point `wrong answer`).
  - 3b. *(V1.1)* The answer is faster than 40 % of her own average and under 1.5 s, on a skill mastered below 80 %: the confidence score drops and no message accuses the child. On a skill mastered at 80 % or more a fast answer is fluency, never penalised (ADR-0004 D8).
  - 3c. *(V1.1)* The confidence score is below 0.6: earned minutes are multiplied by the confidence (factor 1 from 0.6 up), the next exercise is easier, and a neutral message is shown.
- Extension points: `statement shown`, `wrong answer`.
- Relationships: «extend» from UC-L3 and UC-L4.

### UC-L3 — Listen to an exercise statement
- Level: subfunction. Primary actor: Learner. Version: V1.2. Decisions: E4, V4.
- Preconditions: an exercise is displayed and a French voice is available.
- Success guarantee: the statement is read aloud with the local voice, nothing leaves the device (dec. V4).
- Main success scenario:
  1. Learner taps the speaker button.
  2. The app reads the statement aloud.
- Extensions: 2a. Learner taps again: the reading restarts.
- Business rule: no French voice means the button is not shown.

### UC-L4 — Retry with a hint
- Level: subfunction. Primary actor: Learner (actor inherited from UC-L2). Version: V1.0. Decisions: M4, E2, ADR-0004 D3.
- Preconditions: the last answer was wrong.
- Success guarantee: the Learner retries without a punishing signal.
- Main success scenario:
  1. The app shows a hint (concrete, then picture, then symbol).
  2. Learner tries again on the same exercise (back to UC-L2 step 2).
- Extensions:
  - 2a. The answer is still wrong and a hint stage is left: back to step 1 with the next stage.
  - 2b. The answer is still wrong after the third hint: the app shows the correct answer with the worked step, nothing is earned, and the session moves on (ADR-0002 D14).
  - 2c. *(V1.1)* This is the third exercise in a row failed at the first try: UC-L1 extension 4a. The tries inside one exercise count as one error (ADR-0004 D3).
- Business rules: no harsh red, no punishing sound. A correct answer after hints earns a decreasing fraction of its weighted minutes, set in configuration (default ×0.5 after one hint, ×0.25 after two, 0 after three, ADR-0002 D15).

### UC-L5 — Rework an earlier skill
- Level: user goal segment. Primary actor: Learner (actor inherited from UC-L1). Version: V1.1. Decisions: R4, M4, C3, ADR-0004 D11, D12.
- Selected by the system as a conditional segment of UC-L1; the Learner does the work.
- Preconditions: a weak prerequisite exists in the skill graph (cycle 1, CP or CE1 level), or the Guardian scheduled a skill.
- Success guarantee: the prerequisite is exercised inside the 20 % review share and the child is told she is "warming up", never "behind".
- Main success scenario:
  1. The app presents a short run (at least 5 exercises) on the prerequisite.
  2. Learner answers them (UC-L2).
  3. After at least 5 exercises, the prerequisite mastery is back at 70 % (the unlock threshold) and the session returns to the target skill, or, for a skill the Guardian scheduled, to the normal mix (no target, ADR-0004 D11, D12).
- Extensions:
  - 3a. After at least 5 exercises the prerequisite is still below 70 %: the app goes one more node down the graph, restarts the exercise count at 0 (each node gets at least 5 exercises) and an alert is raised for the Guardian.
  - 3b. After at least 5 exercises the prerequisite is still below 70 % and has no prerequisite of its own (graph floor): the app stays on it and raises a "to do together" note for the Guardian (ADR-0004 D12).

### UC-L6 — Take on a challenge exercise
- Level: user goal. Primary actor: Learner. Version: V1.1. Decisions: M3, C1.
- Preconditions: the challenge slot is offered (UC-L1 step 5). This use case owns the acceptance (ADR-0001 D11).
- Success guarantee: the child is never pushed ahead of the class beyond the Guardian's ceiling settings.
- Main success scenario:
  1. Learner accepts the offered challenge.
  2. The app proposes an exercise one notch higher, possibly a prudent look-ahead probe: a skill of a period above the ceiling, allowed only inside a challenge slot.
  3. Learner answers it (UC-L2).
- Extensions: 3a. Look-ahead probes succeed repeatedly: a neutral note for the Guardian is created, never a label.
- Business rule: the child chooses only within the challenge share; the engine picks every other exercise (`docs/CADRAGE.md` §3).

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
- Success guarantee: the Learner sees the reserve and earned time, never another child, never red.
- Main success scenario:
  1. Learner opens the progress view.
  2. The app shows the gauge and the recent progress. *(V1.1)* Personal fluence records are shown, with no countdown. *(V1.2)* The day streak is shown.
  3. *(V1.1)* Minutes expiring within 2 days are shown neutrally with their real expiry day, 7 days after they were earned ("use them before Tuesday 28").
- Extensions: 2a. No session yet: the app invites the Learner to start one.
- Business rule: a broken streak is never shown as a loss. An active day is a LocalDay with at least 10 correct answers, across sessions (ADR-0004 D18).

### UC-L9 — Customise the companion
- Level: user goal. Primary actor: Learner. Version: V1.2. Decision: E1.
- Preconditions: at least one item is unlocked by a day streak; the wardrobe entry is not shown before that.
- Main success scenario:
  1. Learner opens the companion wardrobe.
  2. Learner picks an unlocked item. Only unlocked items are shown, plus the next one to unlock with the streak days still missing.
  3. The app shows the companion with the item.

## Screen-time domain

### UC-S1 — Request screen time
- Level: user goal. Primary actor: Learner. Version: V1.0. Decisions: Q1, P3, Conversion.
- Success guarantee: a pending request exists and nothing is spent.
- Main success scenario:
  1. Learner opens the screen-time request.
  2. Learner picks a duration up to the smaller of the reserve and the daily cap left today. The picker is shown only when that limit is at least 1 minute (balance rounded down).
  3. Learner taps "Ask".
  4. The app records a pending request for the Guardian.
- Extensions:
  - 2a. Reserve is 0: the request controls are not shown; the app only suggests starting a session (UC-L1) and no request is created.
  - 2b. The daily cap (30 min of screen) is reached: the app says "enough for today".
- Business rule: later sessions the same day keep crediting the reserve up to its cap, but spending is limited by the daily cap.

### UC-S2 — Approve a screen-time request
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decisions: P1, P3, ADR-0005 D1.
- Stakeholder: Learner wants her time quickly.
- Preconditions: a pending request exists.
- Success guarantee: the request is approved or refused, never silently lost.
- Main success scenario:
  1. Guardian opens the pending request.
  2. Guardian enters the PIN (include UC-P1).
  3. The app shows the child, the duration and the reserve.
  4. Guardian approves.
  5. The timer is ready for UC-S3.
- Extensions:
  - 3a. The balance or the daily cap left no longer covers the request (ADR-0005 D1): the app shows the minutes still possible, and approving grants only those. With nothing left, the request closes as expired with no debit, the Learner sees "No more screen time today" with one OK button, and a note is raised for the Guardian.
  - 4a. Guardian refuses: the reserve is unchanged and the Learner sees a neutral message.
- Business rules: wrong-PIN handling is owned by UC-P1. One open request at a time (pending, approved or in use), so an approved request cannot be followed by a second one against the same reserve. From its start, the timer holds the requested minutes, so an expiry during the timer cannot lower them. A request not answered, or approved but not started, expires at the end of the day, with no debit.
- Relationships: «include» UC-P1. V2 note: approval on the parent's phone is open (OQ-2).

### UC-S3 — Use approved screen time
- Level: user goal. Primary actor: Learner. Version: V1.0 (extension 4a V2). Decisions: Q1, P3, P0, ADR-0005 D1.
- Secondary actor: DeviceOS *(V2)*.
- Preconditions: an approved request.
- Success guarantee: the used time is debited from the reserve.
- Main success scenario:
  1. Learner starts the timer.
  2. Learner plays or watches in another app.
  3. For a timer longer than 5 minutes, the app warns 5 minutes before the end; a shorter timer has no warning.
  4. The timer ends with an alarm. The alarm is scheduled with the OS when the timer starts, so it rings even if the app was suspended or closed.
- Extensions:
  - 1a. The balance or the daily cap left no longer covers the approved minutes (ADR-0005 D1): the gauge shows the minutes still possible with one Start button, and the timer runs for those, with no new PIN because less than approved is granted. With nothing left, the screen says "No more screen time today" with one OK button and the request closes as expired with no debit. Either case raises a note for the Guardian. The Learner is never asked a question.
  - 2a. Learner stops early: only the time used is debited and the stop is visible to the Guardian *(V1.1)* in the alerts history (UC-P6).
  - 4a. *(V2)* Blocking permission was granted on this Android user: the app asks DeviceOS to block the other apps for the child's user, and DeviceOS confirms. If DeviceOS refuses, the declarative alarm stays the only signal (ADR-0001 D8, dec. Q1, P0).
  - *a. The app is suspended or killed, or the device restarts, while the timer runs: the timer's start time is stored when it starts. On return or next launch, the elapsed time is the current trusted time minus that start (ADR-0004 D9), capped at the approved minutes, and it is debited; a timer whose end has passed is closed with that debit. Closing the app therefore never stops the countdown. If the device clock went backwards, the full approved minutes are debited and a neutral note is created for the Guardian.
- Postcondition: the reserve is debited.
- Business rule: in V1 the app cannot block other apps (declarative, dec. Q1). The child could stop the timer and keep playing: this residual risk is accepted in V1 and removed by extension 4a in V2.

### UC-S5 — Configure screen-time rules
- Level: user goal. Primary actor: Guardian. Version: V1.1. Decisions: Q4, Conversion.
- Preconditions: parent space unlocked.
- Main success scenario:
  1. Guardian opens the rules.
  2. Guardian edits conversion rate, daily cap, reserve cap, expiry or session duration (defaults: 1:1 up to 20 min of work then 2:1, 30 min a day, reserve cap 60 min, 7 days, 15 min session within 10–20; the V1.0 engine uses these defaults before this screen exists). The base standard time (35 s per correct answer, multiplied from V1.1 by the difficulty multiplier) and the progress bonus (2 min) are configuration, like the multipliers, not Guardian settings in V1 (ADR-0004 D1, D5, D6).
  3. The app saves the rules.
- Extensions: 2a. A value is outside safe bounds: the app refuses and explains.

## Parent-space domain

### UC-P1 — Unlock the parent space
- Level: user goal (also included by UC-S2). Primary actor: Guardian. Version: V1.0. Decisions: P1, ADR-0004 D13–D15.
- Preconditions: a PIN exists (set during UC-P14).
- Success guarantee: the parent space is open for a short session.
- Main success scenario:
  1. Guardian enters the 6-digit PIN on a pad whose digits are scrambled each time, with no digit echoed (ADR-0004 D14).
  2. The app opens the parent space.
- Extensions:
  - 1a. Wrong PIN: progressive lockout. The first 3 tries are free, then the pad waits 30 s, 1 min, 5 min, then 15 min after each wrong PIN; a correct PIN or recovery code resets the count (ADR-0004 D13).
  - 1b. Guardian forgot the PIN: Guardian types the recovery code shown at set-up (UC-P12; 12 characters, digits and capital letters without ambiguous ones), then a new PIN twice. A wrong code follows the same lockout (ADR-0004 D15).
- Business rules: no biometrics (the tablet is the child's). The parent space locks after 2 minutes without activity and when the Guardian leaves it. Every PIN entry uses the same scrambled pad, and every PIN check (UC-S2, UC-P9, UC-P10, UC-P15) the same lockout.

### UC-P2 — Create the child profile
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decisions: V3, P0.
- Preconditions: the parent space is unlocked (UC-P1), or UC-P14 includes this use case at first launch, right after the PIN is set (ADR-0001 D10).
- Success guarantee: a profile with first name or pseudonym, birth year and class level exists.
- Main success scenario:
  1. Guardian opens profile creation.
  2. Guardian enters a first name or pseudonym, a birth year and the class level.
  3. The app saves the profile.
- Extensions: 2a. A field is missing or invalid: the app asks again.
- Business rules: the form has no field for surname, photo or child e-mail. In V1 one child per Guardian (OQ-3): once a child profile exists, profile creation is hidden in the parent space; UC-P14 creates the first one.

### UC-P3 — Set the class calendar ceiling
- Level: user goal. Primary actor: Guardian. Version: V1.1. Decision: C1.
- Success guarantee: the engine caps skill unlocking below the chosen period.
- Main success scenario:
  1. Guardian opens the calendar.
  2. Guardian selects the school period (1–5) the class is at.
  3. The app saves the ceiling.
- Extensions: 2a. Guardian never sets it: the default is the period of the current date in a fixed table in configuration (P1 Sep–Oct, P2 Nov–Dec, P3 Jan–Feb, P4 Mar–Apr, P5 May–Aug: July and August stay in P5, the year just finished, until the Guardian changes the class level or the ceiling, ADR-0004 D19).

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
  2. The app shows green (80 % or more unless falling), orange (50–79 %) or red (below 50 % or falling) per skill. A skill shows no colour before 5 attempts.
  3. *(V1.1)* The app shows the fluence milestones next to the personal records.
- Extensions: 2a. No data yet: the app explains that results appear after the first sessions.

### UC-P6 — Review alerts and the to-do-together list
- Level: user goal. Primary actor: Guardian. Version: V1.0 minimal (note list with an unread badge, ADR-0004 D16), full V1.1. Decisions: P2, M4, T1, C1, ADR-0004 D16.
- Preconditions: parent space unlocked.
- Main success scenario:
  1. Guardian opens the alerts.
  2. The app lists the notes, newest first. *(V1.1)* Stuck skills and pauses are grouped, with a "to do together" line.
  3. Guardian marks alerts as read.
- Extensions: 2a. Persistent keypad-comfort signals appear as a neutral note, never a diagnosis. 2b. A look-ahead facility note appears, never a label.

### UC-P7 — Send the child back to an earlier skill
- Level: user goal. Primary actor: Guardian. Version: V1.1. Decisions: R4, ADR-0004 D11.
- Preconditions: parent space unlocked.
- Success guarantee: the next session opens, right after the warm-up, with a block of 5 exercises on the chosen skill through UC-L5, then the skill joins the review share (ADR-0004 D11).
- Main success scenario:
  1. Guardian opens the skill list.
  2. Guardian picks a skill.
  3. The app schedules it as a remediation with no target skill.

### UC-P8 — Export the child's data
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decisions: S1, §4 privacy baseline, ADR-0003 D3.
- Preconditions: parent space unlocked.
- Success guarantee: a complete encrypted file the Guardian can keep; the app never uploads it.
- Main success scenario:
  1. Guardian asks for an export.
  2. Guardian chooses a passphrase of at least 12 characters, or accepts one the app suggests, and types it twice.
  3. The app builds the file, encrypted with a key derived from the passphrase.
  4. The app hands the file to the Guardian and reminds the Guardian that a forgotten passphrase makes it unreadable.
- Extensions:
  - 2a. The two entries differ or the passphrase is shorter than 12 characters: the app asks again.
  - 3a. Export fails: nothing is changed and the app says so.

### UC-P9 — Erase all data
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decisions: S1, V1, §4 privacy baseline.
- Preconditions: parent space unlocked.
- Success guarantee: everything the app stored is deleted (ADR-0002 D12): child data, PIN, consent, rules, time guard, the database key and any database set aside after a key loss. The app restarts on the set-up (UC-P14).
- Main success scenario:
  1. Guardian asks to erase everything. The app offers an export first (UC-P8).
  2. Guardian confirms in one PIN-protected gesture.
  3. The app deletes the database key first, then the database and every set-aside database, so a crash leaves nothing readable and the next start finishes the erase. It shows a confirmation, says that export files already saved outside the app are not erased, and restarts on UC-P14 step 1.
- Extensions: 2a. Guardian cancels: nothing is deleted.

### UC-P10 — Change the PIN
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decision: P1.
- Preconditions: parent space unlocked.
- Main success scenario:
  1. Guardian enters the current PIN, then the new PIN twice.
  2. The app stores it hashed.
- Extensions: 1a. The current PIN is wrong or the two new entries differ: the app asks again.

### UC-P11 — Choose anonymous crash reporting
- Level: user goal. Primary actor: Guardian. Version: V1.1. Decision: V4.
- Preconditions: parent space unlocked.
- Main success scenario:
  1. Guardian opens the privacy settings.
  2. Guardian enables or disables anonymous crash reports.
- Business rule: default is off.

### UC-P12 — Set the parent PIN
- Level: subfunction (included by UC-P14 only, ADR-0001 D12). Primary actor: Guardian (inherited from UC-P14). Version: V1.0. Decisions: P1, ADR-0004 D15.
- Preconditions: first launch, no PIN yet.
- Success guarantee: a hashed 6-digit PIN and a hashed recovery code exist and the parent space can be unlocked.
- Main success scenario:
  1. Guardian chooses a 6-digit PIN twice.
  2. The app stores it hashed.
  3. The app shows a recovery code once (12 characters, digits and capital letters without ambiguous ones), asks the Guardian to write it down away from the tablet, and stores only its hash (ADR-0004 D15).
- Extensions: 1a. The two entries differ or the PIN is trivial (000000, 123456): the app asks again.

### UC-P13 — Request keypad re-calibration
- Level: user goal. Primary actor: Guardian. Version: V1.2. Decision: T1.
- Preconditions: parent space unlocked.
- Main success scenario:
  1. Guardian asks for a re-test.
  2. The app marks the next launch to run UC-L7. The two use cases are linked by data, not by a UML relationship.

### UC-P14 — Set up the app for a child
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decisions: P0, P1, V3, V4, §4 parental consent, ADR-0003.
- Preconditions: first launch, or the database key is lost (storage rule).
- Success guarantee: a PIN, a child profile and the privacy defaults exist. The app opens on the child profile.
- Main success scenario:
  1. The app explains what it stores, that nothing leaves the device, and asks the Guardian to confirm they are the child's parent or legal guardian.
  2. Guardian sets the PIN (include UC-P12).
  3. Guardian creates the child profile (include UC-P2).
  4. The app sets crash reports to off (changeable in UC-P11).
  5. *(V1.2)* The app proposes the keypad calibration (UC-L7) for the child.
- Extensions:
  - *a. The database key is lost: the unreadable database is set aside before the set-up starts (ADR-0003 D3). Each start retries opening it for 30 days; if it does not open, it is deleted at day 30 and a note is raised (ADR-0004 D17). If no set-up or restore was completed by then, there is no database for the note: a flag in a set-aside status file outside the database (not the erase marker) makes the start screen show "The old data could not be opened and was deleted." until the next set-up or restore (ADR-0005 D3).
  - *a1. The set-aside database opens again within the 30 days: the start screen offers "Bring back the old data". Guardian confirms with the PIN stored in the old database, or with that credential's recovery code instead, then sets a new PIN (its own credential, the same lockout applies). The old database replaces the current data in one transaction with the same rules as UC-P15 (reserve forfeited, open requests closed, trusted time = the later of both, ADR-0002 D13), and the replaced data is deleted. If no new set-up was completed yet, the old database simply becomes the database again. UC-P15 is not used: it needs a file and a passphrase.
  - 1a. Guardian declines: the app stays closed and stores nothing.
- Relationships: «include» UC-P12, UC-P2.

### UC-P15 — Restore the child's data from a file
- Level: user goal. Primary actor: Guardian. Version: V1.0. Decisions: S1, ADR-0003 D3.
- Preconditions: an export file from UC-P8, and either the parent space is unlocked or the database key is lost (see the storage rule below).
- Success guarantee: the data from the file replaces the current data, or nothing changes. The screen-time reserve is never restored: it starts at 0 (ADR-0002 D13).
- Main success scenario:
  1. Guardian chooses an export file.
  2. Guardian types the passphrase of that file.
  3. The app decrypts and checks the file and shows what it contains, with a line saying that saved screen-time minutes are not restored.
  4. Guardian confirms with the PIN.
  5. The app replaces the data and encrypts it with the device key (a new key is generated if it was lost). While the parent space is unlocked, the current credential (PIN hash, recovery code hash and lockout) is kept and the file's applies only after a key loss. The file's credits stay as history with their remaining minutes forfeited, and its open requests are closed, so no minute already spent can come back and no session is credited twice. The trusted time becomes the later of the file's and the device's.
- Extensions:
  - 3a. Wrong passphrase: nothing changes and the Guardian can try again.
  - 3b. The file is invalid or from a newer version: the app refuses and nothing changes.
  - 4a. The database key was lost: there is no current credential, so the PIN to type is the one stored in the file, which becomes the credential; the Guardian may give the file credential's recovery code instead, then sets a new PIN (same lockout). Without an unlocked parent space, the passphrase is the only proof that the actor is the Guardian (risk noted in ADR-0003).

## Covered elsewhere (not use cases)

| Decision or rule | Where it lives |
|---|---|
| D1 multipliers, 70 % level unlock, D1 empirical recalibration (V2) | Engine rules, class and sequence diagrams |
| T2 hidden control questions (V1.5) | Future extension of UC-L2 |
| T1 keypad mini-games (V1.5) | Future use case, learning domain |
| S1 sync across devices (V1.5) | Future use case, parent-space domain |
| Q3 reading (V2) | Same use cases with a new skill strand |
| V1 90-day retention, weekly aggregates | Background behaviour (ADR-0001 D4), state and data-flow diagrams |
| Q1 V2 blocking of other apps | UC-S3 extension 4a (former UC-S4, ADR-0001 D8) |
| Q4 7-day expiry | Background behaviour (ADR-0001 D4), reserve state diagram |
| No LLM receives child data | Business rule for the whole system, data-flow diagram |

## Cross-cutting business rules

- Parent settings (UC-P3, UC-P4, UC-P11, UC-S5) share one flow: open, edit, check bounds, save. The parent-space auto-lock applies. Not modelled as a generalization (ADR-0001 D7).

- Timers, expiry and the daily cap use trusted time (ADR-0004 D9): the last trusted instant advanced by the device's monotonic elapsed time, not the wall clock. The LocalDay changes only when trusted time passes midnight. A forward jump of the device clock of more than 10 minutes is ignored and creates a neutral note. Trusted time follows monotonic uptime, so a backwards wall-clock change has no effect while the uptime reference holds. Only after a device restart (no monotonic reference), when the device time is earlier than the last trusted instant, expiry and the daily cap freeze until the device clock catches up, a running timer is debited in full and a neutral note is created; otherwise the device time is accepted (residual risk, covered by the note). An interrupted timer (UC-S3 *a) is debited by trusted time since its stored start. A session length counts only while the app is open (UC-L1 *b). Expiry days shown to the Learner (UC-L8) are computed from the earning time with this same rule.

- Storage (ADR-0003): the whole database is encrypted with a random key kept in the device key store; the app refuses to open a database that SQLCipher does not protect. A key-store error is tried 3 times in all, 1 s then 2 s apart (ADR-0005 D2). If the key is definitely missing or does not open the database, the unreadable database is set aside (the next key is created under a new key-store alias; the old alias is kept for the 30 days and deleted with the set-aside database, or the new one is deleted if the old data is brought back) (retried at each start for 30 days, if it opens again, the Guardian can bring the old data back with the old PIN (UC-P14 *a1); otherwise deleted with a note, ADR-0004 D17), and the app shows only two choices: restore from a file (UC-P15) or set up again (UC-P14). The PIN lives in the encrypted database, so it cannot gate this screen (risk and OQ-6 in ADR-0003). The web build stores no child data.

## Open questions

- OQ-1 PIN recovery without letting the child reset it: closed, recovery code shown once at set-up (ADR-0004 D15, UC-P1 1b).
- OQ-2 Remote approval on the parent's phone (V2): new use case or variant of UC-S2.
- OQ-3 Several children per Guardian (not in scope now; V1 hides profile creation once a child exists, UC-P2).
- OQ-4 Scope of the full-rate threshold: closed, per day (ADR-0002 D10).
- OQ-5 Scope of the erase and restore guard: closed (ADR-0002 D12 erase, D13 restore, sequence study issue #13).
- OQ-6 Device-level protection of the app (pinning, Android user or parental controls) against reinstalling it or setting it up again after a key loss.
