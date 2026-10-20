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
| Mental calculation | Add 9, then 19, then 29 (add 10/20/30 then subtract 1); skip the trick when the units digit is 0 or 1. Fluence target: 12 calculations in 3 minutes | From P2 |
| Written calculation | Column addition (learnt in CP, reused in CE1) | Whole year |
| Written calculation | Column subtraction, introduced at the latest in P3 | By P3 |
| Multiplication | Symbol ×, commutativity, distributivity over addition, multiply by 10 a number under 100 | P1–P2 |
| Multiplication | Tables of 1, 2, 3, 4, 5, 6 and 10, both directions | P1–P2 |
| Multiplication | Table of 7, product of a number from 11 to 19 by a number under 10 by decomposing | P3 |
| Multiplication | Table of 8 | P4 |
| Multiplication | All multiplication tables | P5 |
| Multiplication | Fluence target at end of CE1: 8 results in 1 minute | End of year |
| Fractions | Words "half", "demi" and "quart" in everyday situations | P1 |
| Fractions | Unit fractions: interpret, represent, read | P2 |
| Fractions | Non-unit fractions up to 1 | P3 |
| Fractions | Compare unit fractions or fractions with the same denominator; add and subtract fractions with the same denominator | P4 |
| Fractions | Review in varied settings | P5 |
| Problem solving | Additive part-whole problems, one or several steps, numbers under 100 at the start of the year, then all available numbers; bar model; add/remove situations where the initial value is the unknown | P3–P4 sequence |

## Consequences for the engine

1. The skill graph comes from this table, not from our earlier illustrative examples. In particular, multiplication is core CE1 content (all tables by P5), so its difficulty must depend on the table (for example ×2, ×5 and ×10 are easy, ×7, ×8 and ×9 are hard), not on a flat bonus.
2. Official fluence benchmarks give an absolute definition of "automatised": 8 table results per minute (about 7.5 s each), and 12 mental additions of 9/19/29 in 3 minutes. They complement the child-relative timing decided in M2.
3. Skills should unlock along the school calendar as a ceiling (a parent setting says where the class is), combined with mastery-based unlocking. Pending decision.
4. Problems need a bar-model representation in the UI (V1.1 or later).
5. Spaced revisiting of tables is explicitly recommended by the programme material (retrieval practice at growing intervals), which matches the 20 % review share.
