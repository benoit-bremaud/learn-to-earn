# Class diagram — domain — analysis-level domain model

> **Feature**: whole product, cross-cutting vocabulary
> **Source specs**: `docs/architecture/specs/use-cases.md`, `docs/curriculum/CE1-maths.md`, `docs/CADRAGE.md` §2–4
> **Related ADRs**: ADR-0001, ADR-0002
> **Decisions captured**: CADRAGE Q1, Q4, Conversion, M1–M4, D1, D2, T1, T2, E1, E3, P0–P3, S1, V1, V3, V4, C1–C4, R4; ADR-0002 D1–D8

## Context

Analysis level: concepts, attributes, associations, multiplicities and constraints only. No operations, no interfaces, no persistence or framework types (Clean Architecture: this is the inner domain). Split in four areas (ADR-0002 D6):

- Diagram 1, curriculum and progress: Strand, Skill, FluenceBenchmark, ChildProfile, SkillProgress, FluenceRecord, Remediation, KeypadProfile, WeeklyAggregate.
- Diagram 2, practice: Session, Exercise, Attempt.
- Diagram 3, rewards: Reserve, ReserveBucket, ScreenTimeRequest, ScreenTimeUse, ScreenTimeRules.
- Diagram 3b, companion: Streak, CompanionItem.
- Diagram 4, parent space and installation: Installation, LearningPlan, ParentNote, ParentCredential, PrivacySettings, TimeGuard.

A class drawn without attributes is a stub whose home is another area.

## Diagram 1 — curriculum and progress

```mermaid
classDiagram
  direction LR
  class Strand {
    name : String
  }
  class Skill {
    id : SkillId
    label : String
    gradeLevel : GradeLevel
    period : Integer [0..1]
    baseLevel : DifficultyLevel
  }
  class FluenceBenchmark {
    label : String
    items : Integer
    seconds : Integer
  }
  class ChildProfile {
    displayName : String
    birthYear : Integer
    classLevel : GradeLevel
  }
  class SkillProgress {
    mastery : Real
    trend : Trend
    averageTimeMs : Integer
    personalRecordMs : Integer
    /unlockedLevel : DifficultyLevel
    lastPractisedAt : Instant
    nextReviewAt : Instant [0..1]
  }
  class FluenceRecord {
    bestItems : Integer
    bestSeconds : Integer
    achievedAt : Instant
  }
  class Remediation {
    origin : RemediationOrigin
  }
  class KeypadProfile {
    firstKeyMs : Integer
    interKeyMs : Integer
    neighbourErrorRate : Ratio
    reversedDigitRate : Ratio
    selfCorrectionRate : Ratio
    answerFormat : AnswerFormat
    recalibrationRequestedAt : Instant [0..1]
  }
  class WeeklyAggregate {
    weekStart : Date
    attempts : Integer
    correctRate : Ratio
    averageTimeMs : Integer
  }
  class GradeLevel {
    <<enumeration>>
    CYCLE1
    CP
    CE1
  }
  class DifficultyLevel {
    <<enumeration>>
    EASY
    MEDIUM
    HARD
    VERY_HARD
  }
  class Trend {
    <<enumeration>>
    RISING
    STABLE
    FALLING
  }
  class AnswerFormat {
    <<enumeration>>
    FREE_ENTRY
  }
  class RemediationOrigin {
    <<enumeration>>
    AUTO
    GUARDIAN
  }
  Strand "1" *-- "1..*" Skill : contains
  Skill "*" -- "*" Skill : requires
  Skill "*" -- "*" FluenceBenchmark : measuredBy
  ChildProfile "1" *-- "*" SkillProgress : progresses
  Skill "1" -- "*" SkillProgress : trackedBy
  SkillProgress "1" *-- "*" WeeklyAggregate : summarisedBy
  ChildProfile "1" *-- "*" FluenceRecord : achieves
  FluenceBenchmark "1" -- "*" FluenceRecord : recordedAs
  ChildProfile "1" *-- "*" Remediation : revisits
  Remediation "*" -- "1" Skill : target
  Remediation "*" -- "1" Skill : current
  ChildProfile "1" *-- "0..1" KeypadProfile : types
  note for Skill "{period 1..5} {requires acyclic}"
  note for SkillProgress "{unique (child, skill)} C1–C3"
  note for Remediation "{current in prerequisites of target} C4"
  note for FluenceRecord "association class, V1.1, C5"
```

## Diagram 2 — practice

```mermaid
classDiagram
  direction LR
  class ChildProfile
  class Skill
  class Session {
    day : LocalDay
    startedAt : Instant
    endedAt : Instant [0..1]
    workedSeconds : Integer
    status : SessionStatus
    confidence : Real
    /weightedMinutes : Real
  }
  class Exercise {
    statement : String
    expectedAnswer : Integer
    difficultyScore : Integer
    /difficulty : DifficultyLevel
    slot : SlotKind
    isLookAhead : Boolean
    hints : HintStage [0..3]
  }
  class Attempt {
    answer : Integer
    /correct : Boolean
    responseTimeMs : Integer
    answeredAt : Instant
    confidenceAtAnswer : Real
    weightedMinutes : Real
  }
  class SlotKind {
    <<enumeration>>
    WARM_UP
    ACQUIRING
    REVIEW
    CHALLENGE
  }
  class HintStage {
    <<enumeration>>
    CONCRETE
    PICTURE
    SYMBOL
  }
  class SessionStatus {
    <<enumeration>>
    RUNNING
    PAUSED
    INTERRUPTED
    STOPPED_EARLY
    COMPLETED
  }
  ChildProfile "1" *-- "*" Session : practises
  Session "1" *-- "1..*" Exercise : {ordered}
  Exercise "*" -- "1" Skill : trains
  Exercise "1" *-- "0..*" Attempt : answeredBy
  note for Session "C6, C7"
  note for Exercise "C8"
  note for Attempt "{frozen snapshots} C9"
```

## Diagram 3 — rewards

```mermaid
classDiagram
  direction TB
  class Installation
  class ChildProfile
  class Reserve {
    /balanceMinutes : Integer
  }
  class ReserveBucket {
    day : LocalDay
    creditedMinutes : Integer
    remainingMinutes : Integer
    forfeitedMinutes : Integer
  }
  class ScreenTimeRequest {
    day : LocalDay
    minutes : Integer
    createdAt : Instant
    status : RequestStatus
  }
  class ScreenTimeUse {
    startedAt : Instant
    usedMinutes : Integer
    stoppedEarly : Boolean
  }
  class ScreenTimeRules {
    fullRateMinutes : Integer
    reducedRatio : Ratio
    dailyCapMinutes : Integer
    reserveCapMinutes : Integer
    expiryDays : Integer
  }
  class RequestStatus {
    <<enumeration>>
    PENDING
    APPROVED
    IN_USE
    USED
    REFUSED
    EXPIRED
  }
  ChildProfile "1" *-- "1" Reserve : owns
  Reserve "1" *-- "*" ReserveBucket : holds
  Reserve "1" *-- "*" ScreenTimeRequest : receives
  ScreenTimeRequest "1" *-- "0..1" ScreenTimeUse : grants
  Installation "1" *-- "1" ScreenTimeRules : configuredBy
  note for ReserveBucket "C10"
  note for Reserve "C11"
  note for ScreenTimeRequest "{at most one open request} C12"
```

## Diagram 3b — companion

```mermaid
classDiagram
  direction LR
  class ChildProfile
  class Streak {
    days : Integer
    bestDays : Integer
    lastActiveDay : LocalDay
  }
  class CompanionItem {
    name : String
    requiredStreakDays : Integer
  }
  ChildProfile "1" *-- "1" Streak : keeps
  ChildProfile "*" -- "0..1" CompanionItem : equipped
  note for CompanionItem "unlocked from bestDays, C13"
```

## Diagram 4 — parent space and installation

```mermaid
classDiagram
  direction LR
  class Installation
  class ChildProfile
  class Session
  class Skill
  class Strand
  class ScreenTimeUse
  class LearningPlan {
    ceilingPeriod : Integer [0..1]
  }
  class ParentNote {
    kind : NoteKind
    createdAt : Instant
    read : Boolean
  }
  class ParentCredential {
    pinHash : Hash
    failedAttempts : Integer
    lockedUntil : Instant [0..1]
  }
  class PrivacySettings {
    crashReportsEnabled : Boolean
    consentConfirmedAt : Instant
  }
  class TimeGuard {
    lastTrustedAt : Instant
    frozenSince : Instant [0..1]
  }
  class NoteKind {
    <<enumeration>>
    STUCK_SKILL
    LOW_CONFIDENCE_PAUSE
    KEYPAD_SIGNAL
    LOOK_AHEAD_FACILITY
    EARLY_STOP
    CLOCK_CHANGED
    PREREQUISITE_STILL_WEAK
  }
  Installation "1" *-- "1..*" ChildProfile : serves
  Installation "1" *-- "1" ParentCredential : securedBy
  Installation "1" *-- "1" PrivacySettings : governedBy
  Installation "1" *-- "1" TimeGuard : trusts
  ChildProfile "1" *-- "1" LearningPlan : follows
  LearningPlan "*" -- "*" Strand : advanceAllowed
  ChildProfile "1" *-- "*" ParentNote : concerns
  ParentNote "*" -- "0..1" Skill : about
  ParentNote "*" -- "0..1" Session : raisedIn
  ParentNote "*" -- "0..1" ScreenTimeUse : raisedAfter
  note for LearningPlan "{ceilingPeriod 1..5} C14"
  note for ParentNote "C15"
  note for TimeGuard "clock rule, C16"
  note for Installation "V1: one child (OQ-3)"
```

## Constraints

Referenced from the diagrams by number (Mermaid notes stay short to keep the diagrams readable).

- C1. SkillProgress is a reified association class, one per child and skill. `mastery` is a Real from 0 to 100, rounded only for display.
- C2. `/unlockedLevel` is the level after the highest one already passed; a level is passed when the skill mastery reaches 70 % (ADR-0002 D9). It is never below `Skill.baseLevel`.
- C3. `averageTimeMs` counts correct answers only (M2). `trend` and `averageTimeMs` are stored on purpose, because attempts are folded after 90 days.
- C4. Remediation: `current` is a prerequisite, direct or indirect, of `target`. Origin GUARDIAN is the "go back to X" button (UC-P7), AUTO comes from the 3-error rule (UC-L5). It is removed once the mastery of `target` is back at the threshold.
- C5. FluenceRecord is the association class child × benchmark. It is measured on a timed window, with no visible countdown.
- C6. `confidence` is a Real from 0 to 1, starts at 1.0 in every session, from V1.1 (ADR-0002 D3). `workedSeconds` accumulates only while RUNNING. `/weightedMinutes` is the sum of the attempts' `weightedMinutes`.
- C7. PAUSED is the confidence pause (UC-L1 4c), INTERRUPTED means the app was closed and the session can resume, STOPPED_EARLY means the child ended it. An interrupted session untouched for a day becomes STOPPED_EARLY.
- C8. `difficultyScore` is the skill base level plus the modifiers (C4 of CADRAGE); the level is mapped from it in configuration. `hints` lists the stages already shown, in order, never repeated. `isLookAhead` is a snapshot taken at generation (skill period above the ceiling).
- C9. `correct` is derived: the answer equals `expectedAnswer`. `confidenceAtAnswer` and `weightedMinutes` are frozen at answer time (ADR-0002 D8): response time × difficulty multiplier × confidence factor, values in configuration. Attempts are kept 90 days with their session and exercises, then folded into WeeklyAggregate. `AnswerFormat` gets further values with UC-L7 (V1.2).
- C10. One ReserveBucket per day on which minutes were earned. It expires `expiryDays` after its day and whatever remains is lost. `creditedMinutes` is cut by `reserveCapMinutes`; the cut part is recorded in `forfeitedMinutes`. Uses debit the oldest unexpired bucket first (ADR-0002 D2).
- C11. `/balanceMinutes` is the sum of `remainingMinutes` of the unexpired buckets. At approval, `request.minutes` must not exceed the balance. Rule changes (UC-S5) apply to new movements only.
- C12. At most one request is PENDING, APPROVED or IN_USE. The day's used minutes plus its open approved minutes never exceed `dailyCapMinutes`. A USED request has exactly one use, and `usedMinutes` never exceeds `request.minutes`.
- C13. CompanionItem is a static catalogue. An item is unlocked when `Streak.bestDays` reaches `requiredStreakDays`, so a broken streak never locks an item again.
- C14. The skill the Guardian wants first is a Remediation with origin GUARDIAN (C4).
- C15. A note of kind EARLY_STOP has a ScreenTimeUse. Links to a session or a use are cleared when those are folded after 90 days.
- C16. Expiry and day changes use the larger of now and `lastTrustedAt`. A backwards clock change sets `frozenSince` and raises a CLOCK_CHANGED note.

## Concept dictionary

| Concept | Meaning | Traces to | Version |
|---|---|---|---|
| Installation | Root owning the child profiles and every installation-wide object | OQ-3, UC-P8, P9, P15 | V1.0 |
| Strand, Skill | Curriculum node and its strand, static data from the programme | C3, C4, curriculum file | V1.0 |
| FluenceBenchmark, FluenceRecord | Official milestone over one or more skills and the child's best result against it | C2, UC-L8, UC-P5 | V1.1 |
| ChildProfile | Display name (first name or pseudonym), birth year, class level only | V3, P0, UC-P2 | V1.0 |
| SkillProgress | Mastery, trend, personal average time and record, review schedule of one child on one skill. The unlocked level is derived | M1, M2, M3, C4 | V1.0 (review schedule V1.1) |
| Remediation | A skill the child goes back to, automatic or set by the Guardian | R4, UC-L5, UC-P7 | V1.1 |
| KeypadProfile | Statistics from calibration and daily use, never a diagnosis; time of the re-calibration request | T1, UC-L7, UC-P13 | V1.2 |
| WeeklyAggregate | Folded answers of one child on one skill after 90 days | V1 | V1.0 |
| Session, Exercise, Attempt | One framed session, its ordered exercises (with the hints shown) and the answers | E3, M3, M4, D1, D2, UC-L1, UC-L2, UC-L4 | V1.0 (confidence, REVIEW and CHALLENGE slots, look-ahead V1.1) |
| Reserve, ReserveBucket | Screen-time minutes earned per day, each day expiring after `expiryDays` (default 7) | Q4, P3, ADR-0002 D2 | V1.0 |
| ScreenTimeRequest, ScreenTimeUse | A request the Guardian approves or refuses, and its use | P3, UC-S1, UC-S2 | V1.0 |
| ScreenTimeRules | Conversion, daily cap, reserve cap, expiry | Conversion, UC-S5 | V1.0 defaults, editing V1.1 |
| Streak, CompanionItem | Day streak and the companion catalogue it unlocks | E1, UC-L9 | V1.2 |
| LearningPlan | Ceiling and strands allowed ahead | C1, UC-P3, UC-P4 | V1.1 |
| ParentNote | Neutral alerts and notes for the Guardian | M4, T1, T2, C1, UC-P6 | V1.1 |
| ParentCredential | PIN hash and lockout state | P1, UC-P1, UC-P10, UC-P12 | V1.0 |
| PrivacySettings | Parental consent date, crash-report opt-in off by default | V4, §4 consent, UC-P11, UC-P14 | V1.0 (crash opt-in V1.1) |
| TimeGuard | Last trusted instant, protects expiry and daily rules against clock changes | clock rule (use cases cross-cutting) | V1.0 |

## Aggregates

Each aggregate is loaded and saved as one unit. Aggregates refer to each other by identifier, never by loaded object (Clean Architecture: this is what the storage port will persist).

| Aggregate | Root and parts | Consistency rule kept together |
|---|---|---|
| Practice | Session, its Exercises and Attempts | one answer updates the attempt, the session confidence and the worked time |
| Progress | SkillProgress and its WeeklyAggregates, Remediation, FluenceRecord | mastery, trend and unlocked level of a skill |
| Reserve | Reserve, its buckets, requests and uses | balance, daily cap, one open request |
| Child | ChildProfile identity, Streak, KeypadProfile, LearningPlan, ParentNote | identity and plan |
| Installation | Installation, ParentCredential, PrivacySettings, ScreenTimeRules, TimeGuard | PIN lockout, clock trust, rules |

Between aggregates the consistency is eventual: closing a session credits the reserve afterwards, a stopped-early use may raise a note afterwards. Erasing a child (UC-P9) cascades over every aggregate that carries its identifier.

## Notes

- No operations on purpose: responsibilities are assigned in the sequence diagrams, then drawn in the design class diagram.
- Composition (filled diamond) means the part dies with the whole. Skill, Strand and CompanionItem are static data and survive an erase.
- No generalization remains in the model (ADR-0002 D7): the reserve is now a set of day buckets, so credits and uses are no longer two kinds of the same thing.
- Derived attributes (`/`) are computed, never stored (DRY). Frozen snapshots taken at event time (confidence at answer, weighted minutes, isLookAhead) are stored on purpose, because their inputs change afterwards.
- Currency (ADR-0002 D8): one quantity feeds the reserve, the weighted minutes. Per attempt: response time x difficulty multiplier x confidence factor. At the end of a session, the day's weighted minutes are converted at the full rate up to `fullRateMinutes` per day, then at `reducedRatio` (OQ-4, decided per day), and credited to the bucket of that day within the reserve cap.
- Day: `LocalDay` is the local calendar day computed from the trusted time (TimeGuard). It is used by the daily cap, the buckets, the streak and the conversion threshold.
- Value types: `SkillId`, `Ratio` (0 to 1), `Hash`, `Instant`, `Date`, `LocalDay` are primitive value types, not entities.
- `GradeLevel.CYCLE1` names a cycle, not a class level; a child profile only uses CP or CE1.
- Navigability is left out at analysis level; it is decided in the design class diagram. `{ordered}` and `{unique}` are drawn as association labels because Mermaid cannot place a constraint at an association end.
- Thresholds and multipliers live in configuration, not in these classes.
- Not in the model: the exported file (an adapter artefact), the clock and TTS (adapters), the OS (external).
- Known limits, accepted (YAGNI): `answer` is an integer (fractions come later); a Strand has no subject until reading arrives in V2.
- Open question OQ-5: does UC-P9 (erase) also remove the PIN, the consent and the rules, or only the child's data? And a restore (UC-P15) of an old export would bring back minutes already spent: the sequence study must decide the guard (refuse an export older than the current data, or recompute the buckets against TimeGuard).
