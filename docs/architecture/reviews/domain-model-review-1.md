# Review 1 — domain model, UML and analysis conformance

- Date: 2026-10-20
- Reviewer: independent agent (Claude Opus 5.5), read-only
- Scope: `diagrams/domain/01-class-domain-model.md`, `decisions/0002-domain-model.md` at commit d66a713
- Result: 3 Must, 10 Should, 5 Nice. All Must and Should resolved.

| # | Sev. | Finding | Resolution |
|---|---|---|---|
| 1 | Must | Note claims composition under ChildProfile, diagrams draw plain associations | Every child-owned part is a composition; note states that static data survives |
| 2 | Must | `Session.earnedMinutes` duplicates `Credit.minutes`; `Attempt.correct` is derivable | `earnedMinutes` removed; `/correct` derived |
| 3 | Must | Reserve balance not derivable: no link between a use and the credits it consumes | `ScreenTimeUse "*" -- "1..*" Credit : drawsFrom`, `Credit./remainingMinutes`, derivation note |
| 4 | Should | D2 sensitivity claim false | Rewritten: A first for any expiry weight; D4, D5, D6 sensitivities added |
| 5 | Should | SkillProgress note inaccurate for a reified class | "reified association class {unique (child, skill)}" |
| 6 | Should | `trend`, `averageTimeMs` derived or stored? `RequestStatus.USED` duplicates ScreenTimeUse | Stored on purpose (attempts folded after 90 days), stated; `USED` removed |
| 7 | Should | `Trend`, `AnswerFormat`, `NoteKind` and value types undeclared | Enumerations added; value types listed in Notes |
| 8 | Should | Ranges written as types | Typed attributes; ranges as `{…}` constraints in notes (Mermaid rejects braces in class bodies) |
| 9 | Should | Three floating classes | "one per installation" notes |
| 10 | Should | `Exercise *-- 1..* Attempt` too strict | `0..*` |
| 11 | Should | Constraints written as labels | `{ordered}`, `{unique stage}`, `{acyclic}` |
| 12 | Should | Real generalization Credit / ScreenTimeUse missing | ADR-0002 D7 (B, 475): abstract ReserveEntry |
| 13 | Should | WeeklyAggregate duplicates the child × skill pair | `SkillProgress *-- WeeklyAggregate` |
| 14 | Nice | ConfidenceScore class with one attribute | Inlined as `Session.confidence [0..1]` (ADR-0002 D3 note) |
| 15 | Nice | Mixed navigability | Arrows dropped; note says navigability is a design decision |
| 16 | Nice | Unnamed associations | Verb names added |
| 17 | Nice | `pseudonym` vs CADRAGE V3 | Renamed `displayName` |
| 18 | Nice | Home classes per area not listed | Listed in Context |

Render check after fixes: the rewards and parent-space diagram was tangled (the inheritance line ran through Strand), so it was split into Diagram 3 (rewards) and Diagram 4 (parent space), ADR-0002 D6 updated.
