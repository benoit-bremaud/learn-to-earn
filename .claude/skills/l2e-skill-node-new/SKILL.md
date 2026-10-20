---
name: l2e-skill-node-new
description: Add or change a skill node in Learn To Earn's prerequisite graph (a learnable skill such as "table of 7" or "add 9 mentally"). Use when adding a skill to the graph, defining its prerequisites, base difficulty level, exercise generator, tests or fluence benchmark.
---

# New skill node

A node is a pure-domain object. Decisions it implements: C3 (V1.0 scope), C4 (base level per skill), R4 (remediation walks back the graph).

## Fields (all required)

- `id`: stable kebab-case (`mult-table-7`).
- `strand`, `period`: from `docs/curriculum/CE1-maths.md` (or CP / cycle 1 for lower nodes). Cite the source row.
- `prerequisites`: ids of the nodes it depends on. The graph is a DAG: no cycles, and every CE1 node must reach a cycle 1 or CP node.
- `baseLevel`: Easy / Medium / Hard / Very hard, taken from the official schedule (for example x2/x5/x10 easy, x7 to x9 hard), then modifiers for number size and carries. No flat operation bonus.
- `fluenceTarget`: official benchmark if one exists, otherwise none.
- `generator`: rule-based exercise generator (no LLM, no child data). Include a visual hint chain concrete, then picture, then symbol.

## Procedure

1. Check the node is in scope for the current version (V1.0: additive core and tables x2/x5/x10).
2. Write the failing unit tests first (engine is TDD): generator output ranges, level, prerequisite validity, no cycle.
3. Implement the node, run the graph validator.
4. Update `docs/curriculum/CE1-maths.md` if the node is new, and the class/state diagrams if the model changed.
5. Note the node in `PROJECT_LOG.md` only if it changes scope.

## Guardrails

- Prerequisites must exist before the node; never reference an unmodelled id.
- Weights, thresholds and levels stay configurable, not hard-coded in the generator.
