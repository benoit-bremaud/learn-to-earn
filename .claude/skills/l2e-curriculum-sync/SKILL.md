---
name: l2e-curriculum-sync
description: Re-check Learn To Earn's skill graph against the official French programme (cycle 1, CP, CE1). Use before every release, when the school year changes, when a programme or Éduscol document is updated, or when asked whether the app is still aligned with the national curriculum.
---

# Curriculum sync

The app must stay aligned with the national programme. Our mapping lives in `docs/curriculum/CE1-maths.md`; it is our own paraphrase, never a copy of the official text.

## Sources (re-fetch, do not trust memory)

- Programme cycle 2, arrêté du 22-10-2024, BO n° 41 du 31-10-2024.
- Éduscol livret d'accompagnement CE1 (and CP when the graph goes down) and the *repères annuels de progression*.
- Cycle 1 programme (maternelle), maths part, for the lowest nodes of the graph.
- Download PDFs into a fresh scratch directory and extract with `pdftotext -layout`. WebFetch cannot parse PDFs and the Éduscol HTML pages may return 403.

## Procedure

1. Re-download the sources and note their publication date or BO number.
2. For each row of the skill graph and each fluence benchmark, confirm the period, the number range and the wording still match. Primary sources (programme, livret) beat secondary sites when they disagree.
3. List differences as: added / removed / moved period / changed benchmark.
4. Update `docs/curriculum/CE1-maths.md`, then the dependent skill nodes (see `l2e-skill-node-new`), then `docs/CADRAGE.md` if a decision changes.
5. Log the sync in `PROJECT_LOG.md` (date, sources checked, differences).

## Guardrails

- Cite sources by name and date, quote at most a few words, paraphrase the rest.
- A changed benchmark or period is a decision: present it with an MCDA matrix before editing the engine.
- Never invent a period or benchmark; mark unknowns "to verify".
