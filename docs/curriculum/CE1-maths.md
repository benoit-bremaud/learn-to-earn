# CE1 mathematics — curriculum mapping for the skill graph

Purpose: keep the app aligned with the French national curriculum. This is our own paraphrase, not a copy of the official text. Re-check the sources before every release.

## Sources

- Programme de mathématiques du cycle 2, arrêté du 22-10-2024, BO n° 41 du 31 octobre 2024 (applies to CP, CE1 and CE2 from the 2025–2026 school year onwards; some secondary sources mention 2026–2027 for CE1/CE2, which is already the current year, so both dates lead to the same conclusion today).
- Éduscol, *Mathématiques — Livret d'accompagnement de programme 2025, CE1*: <https://eduscol.education.gouv.fr/sites/default/files/document/2025livretaccompagnementmathce1pdf-116325.pdf>
- Éduscol, *Repères annuels de progression et attendus de fin d'année*: <https://eduscol.education.gouv.fr/6910/reperes-annuels-de-progression-et-attendus-de-fin-d-annee-du-cp-la-troisieme>
- National diagnostic evaluations *Repères CE1* (start of year): potential source for the initial placement test, not yet studied.

## Scope and priority

The cycle 2 priority is numeration, calculation and arithmetic problem solving: at least two thirds of maths teaching time goes to the "Numbers, calculation and problem solving" strand. V1 covers only this strand. Measurement and geometry are out of scope for now, and so are division and any other topic not listed below (to verify in the full programme text).

The school year has five periods (P1 to P5). The livret gives indicative periods, and the actual pace depends on the teacher.

## Skill graph (V1 candidates)

| Strand | Skill | Period / source note |
|---|---|---|
| Numeration | Read, write, compare and order numbers up to 100 (reinforced), then 100–1000, introduced progressively from P1 | Whole year |
| Mental calculation | Addition facts both ways, doubles and halves of usual numbers (CP, kept alive) | Whole year |
| Mental calculation | Add tens to a number (48 + 30) | CP prerequisite |
| Mental calculation | Add 9, then 19, then 29 (add 10/20/30 then subtract 1); skip the trick when the units digit is 0 or 1 | From P2 |
| Written calculation | Column addition (learnt in CP, reused in CE1) | Whole year |
| Written calculation | Column subtraction, introduced at the latest in P3 | By P3 |
| Multiplication | Symbol ×, commutativity, distributivity over addition, multiply by 10 a number under 100 | P1–P2 |
| Multiplication | Tables of 1, 2, 3, 4, 5, 6 and 10, both directions | P1–P2 |
| Multiplication | Table of 7, product of a number from 11 to 19 by a number under 10 by decomposing | P3 |
| Multiplication | Table of 8 | P4 |
| Multiplication | All multiplication tables | P5 |
| Multiplication | Fluence target at end of CE1: 8 multiplication equalities in 1 minute | End of year |
| Fractions | Words "half", "demi" and "quart" in everyday situations | P1 |
| Fractions | Unit fractions: interpret, represent, read | P2 |
| Fractions | Non-unit fractions up to 1 | P3 |
| Fractions | Compare unit fractions or fractions with the same denominator; add and subtract fractions with the same denominator | P4 |
| Fractions | Review in varied settings | P5 |
| Problem solving | Additive and mixed part-whole problems, one or two steps (two-step problems are CE1 content), numbers under 100 at the start of the year, then all available numbers; bar model; add/remove situations where the initial value is the unknown | P3–P4 sequence |

## Fluence benchmarks (end of CE1)

- 12 addition-table equalities in 1 minute.
- 8 multiplication equalities in 1 minute.
- 12 mental calculations in 3 minutes.

They complement the child-relative timing (M2) and appear as milestones in the parent dashboard (C2). The programme stresses fluence routines without stress: no visible countdown by default, speed shown as a personal record.

## Prerequisite graph and remediation (decided 2026-10-20)

The skill graph is a DAG of prerequisites that goes down through CP to cycle 1 (maternelle):

1. Cycle 1: count and compare collections, cardinality, compose/decompose numbers up to 10, part-whole problems with objects, groupings and equal sharing.
2. CP: addition facts to 20, subtraction, tens and units, doubles and halves, first tables intuition.
3. CE1: +/- with carries, tables, two-step problems.

V1.0 nodes and prerequisite edges (stable IDs; a node is reached only after its prerequisites; R4 walks these edges back):

| ID | Skill | Grade | Base | Period | Prerequisites |
|---|---|---|---|---|---|
| `c1.count` | Count and compare collections up to 10 | Cycle 1 | Easy | — | — |
| `c1.decompose10` | Compose and decompose numbers up to 10 | Cycle 1 | Easy | — | `c1.count` |
| `cp.add10` | Addition facts up to 10 | CP | Easy | — | `c1.decompose10` |
| `cp.sub10` | Subtraction facts up to 10 | CP | Easy | — | `c1.decompose10` |
| `cp.tens` | Tens and units | CP | Easy | — | `c1.count` |
| `cp.skipcount` | Count by 2, 5 and 10 | CP | Easy | — | `cp.tens` |
| `cp.doubles` | Doubles and halves | CP | Easy | — | `cp.add10` |
| `cp.add20` | Addition facts up to 20 | CP | Easy | — | `cp.add10`, `cp.tens` |
| `cp.sub20` | Subtraction facts up to 20 | CP | Easy | — | `cp.sub10`, `cp.tens` |
| `ce1.mental-addsub` | Mental +/- with small numbers | CE1 | Medium | 1 | `cp.add20`, `cp.sub20` |
| `ce1.table2` | Table x2 | CE1 | Easy | 1 | `cp.doubles`, `cp.skipcount` |
| `ce1.table5` | Table x5 | CE1 | Easy | 1 | `cp.skipcount` |
| `ce1.table10` | Table x10 | CE1 | Easy | 1 | `cp.tens`, `cp.skipcount` |

Period: the school period (P1–P5) from which a CE1 node is open under the default ceiling (ADR-0004 D19); the default ceiling is the period of the current date in a fixed table in configuration (P1 Sep–Oct, P2 Nov–Dec, P3 Jan–Feb, P4 Mar–Apr, P5 May–Aug: July and August stay in P5 until the Guardian changes the class level or the ceiling), and the Guardian can change it (UC-P3). Cycle 1 and CP nodes have no period: they are below the class and always open. The four V1.0 CE1 nodes take the first period of their livret range (tables of 1–6 and 10 in P1–P2, mental +/- the whole year), so all are P1.

Cold start (ADR-0004 D2): skills of a grade below the child's class level start at 70 % mastery (the unlock threshold), so a CE1 child starts on CE1 nodes; real errors walk down these edges: in V1.0 the picker itself does it (a skill dropping under 70 % is again the lowest unmastered one), R4 applies from V1.1.

Later nodes (posed calculation with carries, other tables, two-step problems) are added with their edges by the skill-node procedure, in V1.1+.

The programme asks for revision "as you go, only for pupils who need it", and for problems whose wording does not match the operation (for example "de plus" hiding a subtraction). Hints go concrete, then pictorial, then symbolic.

## Consequences for the engine

1. Each skill carries a base difficulty level taken from this table (decision C4 = A; base category to score: Easy 0, Medium 2, Hard 3, Very hard 5, the lower bound of each level band in `docs/CADRAGE.md`, so a skill with no modifier stays at its own level): for example ×2, ×5 and ×10 easy, ×3/×4 medium, ×7 to ×9 hard, then modifiers for number size and carries. No flat operation bonus.
2. Fluence benchmarks define "automatised" in the dashboard; scoring stays relative to the child using the app.
3. Skills unlock along the calendar ceiling set by the parent plus mastery, with prudent look-ahead probes inside a challenge slot (ADR-0001 D9) (C1 = A).
4. Remediation is reactive (R4 = C, from V1.1; in V1.0 the picker does the walk-down, a skill under 70 % being again the lowest unmastered one): the 3-error rule (3 exercises in a row failed at the first try, ADR-0004 D3) or failed reviews walk back the DAG, the weak prerequisite enters the 20 % review share, and the parent has a "go back to X" button. No placement test: the cold start gives the skills below the class level a starting mastery of 70 % instead (ADR-0004 D2).
5. V1.0 skills (C3 = C): mental additive core (decompositions to 10, facts to 20, +/- small numbers) and tables x2/x5/x10, with the prerequisite nodes of cycle 1 and CP already modelled. Posed calculation, other tables and two-step problems follow in V1.1+.
6. Problems need a bar-model UI and wording with distractors (V1.1 or later).
7. Spaced revisiting of tables matches the 20 % review share.
