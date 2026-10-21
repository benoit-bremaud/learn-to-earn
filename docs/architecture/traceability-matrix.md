# Traceability matrix

Proves coverage: every use case traces to product decisions, a diagram and a roadmap version. Class names refer to the domain model (`diagrams/domain/01-class-domain-model.md`). Columns for later studies (sequence, component, state, data-flow) are filled as those studies are produced.

| UC | Goal | Actor | Version | CADRAGE decisions | Use-case diagram | Sequence | Component | Class | State | Data-flow |
|---|---|---|---|---|---|---|---|---|---|---|
| UC-L1 | Complete a learning session | Learner | V1.0 | E3, M3, M4, C1, C3, C4, T2, Conversion | learning | — | — | Session, Exercise, SkillProgress, Skill, LearningPlan, Reserve, ReserveBucket, ScreenTimeRules, ParentNote, TimeGuard | — | — |
| UC-L2 | Answer an exercise | Learner | V1.0 | M1, M2, T1, T2, E2 | learning | — | — | Exercise, Attempt, Session, SkillProgress, KeypadProfile (V1.2) | — | — |
| UC-L3 | Listen to an exercise statement | Learner | V1.2 | E4, V4 | learning | — | — | Exercise (statement; TTS is an adapter) | — | — |
| UC-L4 | Retry with a hint | Learner | V1.0 | M4, E2 | learning | — | — | Exercise (hints), Attempt | — | — |
| UC-L5 | Rework an earlier skill | Learner | V1.1 | R4, M4, C3 | learning | — | — | Remediation, Skill (requires), SkillProgress, Exercise, ParentNote | — | — |
| UC-L6 | Take on a challenge exercise | Learner | V1.1 | M3, C1 | learning | — | — | Exercise (isLookAhead), LearningPlan, ParentNote | — | — |
| UC-L7 | Calibrate keypad comfort | Learner | V1.2 | T1 | learning | — | — | KeypadProfile | — | — |
| UC-L8 | Check progress and the screen-time gauge | Learner | V1.0 | E1, Q4 | learning | — | — | Reserve, ReserveBucket, SkillProgress, FluenceRecord (V1.1), FluenceBenchmark (V1.1), Streak (V1.2) | — | — |
| UC-L9 | Customise the companion | Learner | V1.2 | E1 | learning | — | — | CompanionItem, Streak | — | — |
| UC-S1 | Request screen time | Learner | V1.0 | Q1, P3, Conversion | screen-time | — | — | ScreenTimeRequest, Reserve, ReserveBucket, ScreenTimeRules, ScreenTimeUse | — | — |
| UC-S2 | Approve a screen-time request | Guardian | V1.0 | P1, P3 | screen-time | — | — | ScreenTimeRequest, Reserve, ParentCredential | — | — |
| UC-S3 | Use approved screen time | Learner | V1.0 | Q1, P3 | screen-time | — | — | ScreenTimeUse, ScreenTimeRequest, ReserveBucket, ParentNote | — | — |
| UC-S4 | Enforce the end of screen time on the device | Learner (inherited), DeviceOS | V2 | Q1, P0 | screen-time | — | — | ScreenTimeUse | — | — |
| UC-S5 | Configure screen-time rules | Guardian | V1.1 | Q4, Conversion | screen-time | — | — | ScreenTimeRules | — | — |
| UC-P1 | Unlock the parent space | Guardian | V1.0 | P1 | parent-space, screen-time | — | — | ParentCredential | — | — |
| UC-P2 | Create the child profile | Guardian | V1.0 | V3, P0 | parent-space | — | — | ChildProfile, Installation | — | — |
| UC-P3 | Set the class calendar ceiling | Guardian | V1.1 | C1 | parent-space | — | — | LearningPlan | — | — |
| UC-P4 | Allow skills beyond the class period | Guardian | V1.1 | C1 | parent-space | — | — | LearningPlan, Strand | — | — |
| UC-P5 | Review the traffic-light dashboard | Guardian | V1.0 | P2, C2 | parent-space | — | — | SkillProgress, Skill, FluenceRecord (V1.1), FluenceBenchmark (V1.1) | — | — |
| UC-P6 | Review alerts and the to-do-together list | Guardian | V1.1 | P2, M4, T1, C1 | parent-space | — | — | ParentNote, SkillProgress | — | — |
| UC-P7 | Send the child back to an earlier skill | Guardian | V1.1 | R4 | parent-space | — | — | Remediation (origin GUARDIAN), Skill | — | — |
| UC-P8 | Export the child's data | Guardian | V1.0 | S1, §4 | parent-space | — | — | Installation and its parts | — | — |
| UC-P9 | Erase all data | Guardian | V1.0 | S1, V1, §4 | parent-space | — | — | Installation and its parts (scope OQ-5) | — | — |
| UC-P10 | Change the PIN | Guardian | V1.0 | P1 | parent-space | — | — | ParentCredential | — | — |
| UC-P11 | Choose anonymous crash reporting | Guardian | V1.1 | V4 | parent-space | — | — | PrivacySettings | — | — |
| UC-P12 | Set the parent PIN | Guardian | V1.0 | P1 | parent-space | — | — | ParentCredential | — | — |
| UC-P13 | Request keypad re-calibration | Guardian | V1.2 | T1 | parent-space | — | — | KeypadProfile (recalibrationRequestedAt) | — | — |
| UC-P14 | Set up the app for a child | Guardian | V1.0 | P0, P1, V3, V4, §4 | parent-space | — | — | Installation, ParentCredential, ChildProfile, PrivacySettings | — | — |
| UC-P15 | Restore the child's data from a file | Guardian | V1.0 | S1 | parent-space | — | — | Installation and its parts (guard OQ-5) | — | — |
