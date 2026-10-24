# Traceability matrix

Proves coverage: every use case traces to product decisions, a diagram and a roadmap version. Class names refer to the domain model (`diagrams/domain/01-class-domain-model.md`). Columns for later studies (sequence, component, state, data-flow) are filled as those studies are produced. Sequence entries are `<feature>/<NN>` files under `diagrams/`. UC-S4 was folded into UC-S3 (ADR-0001 D8).

| UC | Goal | Actor | Version | CADRAGE decisions | Use-case diagram | Sequence | Component | Class | State | Data-flow |
|---|---|---|---|---|---|---|---|---|---|---|
| UC-L1 | Complete a learning session | Learner | V1.0 | E3, M3, M4, C1, C3, C4, T2, Conversion, ADR-0004 D1–D6, D10, D11, ADR-0005 D4 | learning | learning/02, 03, 04, 05 | — | Session, Exercise, SkillProgress, Skill, LearningPlan, Reserve, ReserveCredit, ScreenTimeRules, ParentNote, TimeGuard | — | — |
| UC-L2 | Answer an exercise | Learner | V1.0 | M1, M2, T1, T2, E2, ADR-0004 D4, D7, D8 | learning | learning/02, 03 | — | Exercise, Attempt, Session, SkillProgress, KeypadProfile (V1.2) | — | — |
| UC-L3 | Listen to an exercise statement | Learner | V1.2 | E4, V4 | learning | — | — | Exercise (statement; TTS is an adapter) | — | — |
| UC-L4 | Retry with a hint | Learner | V1.0 | M4, E2, ADR-0004 D3 | learning | learning/02 | — | Exercise (hints), Attempt | — | — |
| UC-L5 | Rework an earlier skill | Learner | V1.1 | R4, M4, C3, ADR-0004 D11, D12 | learning | learning/04 | — | Remediation, Skill, Prerequisite, SkillProgress, Exercise, ParentNote | — | — |
| UC-L6 | Take on a challenge exercise | Learner | V1.1 | M3, C1 | learning | learning/02 | — | Exercise (isLookAhead), LearningPlan, ParentNote | — | — |
| UC-L7 | Calibrate keypad comfort | Learner | V1.2 | T1 | learning | — | — | KeypadProfile | — | — |
| UC-L8 | Check progress and the screen-time gauge | Learner | V1.0 | E1, Q4, ADR-0004 D18 | learning | — | — | Reserve, ReserveCredit, SkillProgress, FluenceRecord (V1.1), FluenceBenchmark (V1.1), Streak (V1.2) | — | — |
| UC-L9 | Customise the companion | Learner | V1.2 | E1, ADR-0004 D18 | learning | — | — | CompanionItem, Streak | — | — |
| UC-S1 | Request screen time | Learner | V1.0 | Q1, P3, Conversion | screen-time | screen-time/02 | — | ScreenTimeRequest, Reserve, ReserveCredit, ScreenTimeRules, ScreenTimeUse | — | — |
| UC-S2 | Approve a screen-time request | Guardian | V1.0 | P1, P3, ADR-0004 D13, D14, ADR-0005 D1 | screen-time | screen-time/03 | — | ScreenTimeRequest, Reserve, ParentCredential (C17), ParentNote | — | — |
| UC-S3 | Use approved screen time (ext. 4a V2: DeviceOS blocking, former UC-S4) | Learner, DeviceOS (V2) | V1.0 | Q1, P3, P0, ADR-0004 D9, ADR-0005 D1 | screen-time | screen-time/04 | — | ScreenTimeUse, ScreenTimeRequest, ReserveCredit, ParentNote | — | — |
| UC-S5 | Configure screen-time rules | Guardian | V1.1 | Q4, Conversion, ADR-0004 D5, D6 | screen-time | — | — | ScreenTimeRules | — | — |
| UC-P1 | Unlock the parent space | Guardian | V1.0 | P1, ADR-0004 D13–D15 | parent-space, screen-time | screen-time/03 | — | ParentCredential (C17) | — | — |
| UC-P2 | Create the child profile | Guardian | V1.0 | V3, P0 | parent-space | — | — | ChildProfile, Installation | — | — |
| UC-P3 | Set the class calendar ceiling | Guardian | V1.1 | C1, ADR-0004 D19 | parent-space | — | — | LearningPlan | — | — |
| UC-P4 | Allow skills beyond the class period | Guardian | V1.1 | C1 | parent-space | — | — | LearningPlan, Strand | — | — |
| UC-P5 | Review the traffic-light dashboard | Guardian | V1.0 | P2, C2 | parent-space | — | — | SkillProgress, Skill, FluenceRecord (V1.1), FluenceBenchmark (V1.1) | — | — |
| UC-P6 | Review alerts and the to-do-together list | Guardian | V1.0 minimal, V1.1 | P2, M4, T1, C1, ADR-0004 D16 | parent-space | — | — | ParentNote, SkillProgress | — | — |
| UC-P7 | Send the child back to an earlier skill | Guardian | V1.1 | R4, ADR-0004 D11 | parent-space | learning/04 | — | Remediation (origin GUARDIAN), Skill | — | — |
| UC-P8 | Export the child's data | Guardian | V1.0 | S1, §4, ADR-0003 | parent-space | parent-space/02 (offer only) | — | Installation and its parts | — | — |
| UC-P9 | Erase all data | Guardian | V1.0 | S1, V1, §4 | parent-space | parent-space/02 | — | Installation and its parts (all of it, ADR-0002 D12) | — | — |
| UC-P10 | Change the PIN | Guardian | V1.0 | P1 | parent-space | — | — | ParentCredential | — | — |
| UC-P11 | Choose anonymous crash reporting | Guardian | V1.1 | V4 | parent-space | — | — | PrivacySettings | — | — |
| UC-P12 | Set the parent PIN | Guardian (via UC-P14) | V1.0 | P1, ADR-0004 D15 | parent-space | — | — | ParentCredential | — | — |
| UC-P13 | Request keypad re-calibration | Guardian | V1.2 | T1 | parent-space | — | — | KeypadProfile (recalibrationRequestedAt) | — | — |
| UC-P14 | Set up the app for a child | Guardian | V1.0 | P0, P1, V3, V4, §4, ADR-0003, ADR-0004 D17, ADR-0005 D2, D3 | parent-space | parent-space/02, 04 (entry only) | — | Installation, ParentCredential, ChildProfile, PrivacySettings, ParentNote | — | — |
| UC-P15 | Restore the child's data from a file | Guardian | V1.0 | S1, ADR-0003, ADR-0005 D2 | parent-space | parent-space/03, 04 | — | Installation and its parts, Reserve emptied by forfeit (ADR-0002 D13), TimeGuard | — | — |
