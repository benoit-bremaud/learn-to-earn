# Sequence study — adversarial review 1 (2026-10-23)

Scope: issue #13 resolutions (ADR-0001 D8–D12), OQ-5 (ADR-0002 D12, D13) and the six sequence diagrams. Reviewer: adversarial subagent (Opus), asked to break the design. All Must and Should findings are fixed in the same PR.

| ID | Level | Finding | Fix |
|---|---|---|---|
| M1 | Must | Progress bonus re-credited at every interruption | Bonus credited once at the final close, unique by `weightedUpTo` (domain C7) |
| M2 | Must | Dropping credits on restore reset the crediting checkpoints and day counters | Credits kept as history with their minutes forfeited, open requests closed (ADR-0002 D13) |
| M3 | Must | Screen-time sequence missed the request message, the PIN entry and the gate on "Start the timer" | Messages added, use wrapped in `opt request APPROVED` |
| M4 | Must | No wrong-PIN branch in erase and restore | `alt wrong PIN` with lockout in both |
| S1 | Should | Storage port talked to the screen at key loss | «control» StartUp drives the key-loss screen |
| S2 | Should | Set-aside database never deleted after a restore | Deleted once the restore succeeded |
| S3 | Should | Erase not crash-safe | Key deleted first, resumable "erase in progress" marker |
| S4 | Should | Approval and start did not re-check the daily cap | Balance and daily cap left checked at both |
| S5 | Should | Early stop left the request open | Request USED, screen back to the gauge |
| S6 | Should | Challenge acceptance not forwarded, no decline branch | `UI->>Ctl: accept` and an `else declined` branch |
| N1–N4 | Nice | Remediation actor and loop guard, average time source, exported files not erased, UC-L1 5b return point | Fixed |
| N5 | Nice | Older review logs still name UC-S4 | Kept as history: UC-S4 is retired by ADR-0001 D8 |
