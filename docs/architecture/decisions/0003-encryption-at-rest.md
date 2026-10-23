# ADR-0003 — Encryption of stored data

- Status: accepted (owner, 2026-10-23)
- Date: 2026-10-23
- Issue: #11

## Context and problem statement

Owner requirement (2026-10-22): every sensitive datum is stored encrypted, and ideally the whole database. The data is about a CE1 child (answers, timings, progression, screen-time usage) and the parent settings. The primary target is an Android tablet; iPad is secondary.

Facts (source: <https://docs.expo.dev/versions/latest/sdk/sqlite/>):

- expo-sqlite ships SQLCipher on Android and iOS through the `useSQLCipher` config plugin; the key is set with `PRAGMA key` right after opening the database.
- SQLCipher is not available in Expo Go. Without it, `PRAGMA key` is silently ignored and the database stays in plain text.
- The web build of expo-sqlite has no documented encryption.

## Considered options and decision drivers

Scores: 0–5 per criterion, weights sum to 100, total out of 500. Scores are our estimates, not measured facts.

## D1 — Encryption on native platforms

| Criterion (weight) | A. SQLCipher, whole database | B. Field-level encryption | C. A and B |
|---|---|---|---|
| Meets the requirement (35) | 5 | 2 | 5 |
| Simplicity and maintenance (25) | 4 | 2 | 1 |
| Robustness against omissions (20) | 5 | 2 | 3 |
| Performance on a low-end tablet (10) | 4 | 4 | 3 |
| Developer friction (10) | 3 | 5 | 3 |
| **Total /500** | **445** | 250 | 320 |

A vs B: B leaves every field nobody thought of in plain text, plus indexes and temporary files, and encrypted columns cannot be sorted or filtered in SQL. A vs C: one key in one place opens both layers, so C adds work without protection.
Sensitivity: B overtakes A only if developer friction carries more than half of the total weight.
**Decision: A.** At start-up the app reads `PRAGMA cipher_version` and refuses to open the database when it is empty, so a build without SQLCipher can never write plain data. Expo Go is not used; development runs on a development build.

## D2 — Web

| Criterion (weight) | A. No child data stored on web | B. App-level encryption (WebCrypto) | C. Plain web storage |
|---|---|---|---|
| Meets the requirement (40) | 5 | 3 | 0 |
| Simplicity (25) | 5 | 2 | 5 |
| Product fit, Android first (20) | 4 | 3 | 3 |
| Key safety (15) | 5 | 2 | 0 |
| **Total /500** | **480** | 260 | 185 |

A vs B: a browser has no hardware key store, so a key kept there is as exposed as the data, and asking the parent for it on each visit breaks the minimal-UI rule.
Sensitivity: A stays first for any realistic weighting.
**Decision: A.** The web build only runs with sample or in-memory data, for demos and development. A real web parent space would reopen this decision.

## D3 — Key management and recovery

| Criterion (weight) | A. Keystore key, no recovery | B. Key derived from the parent PIN | C. Keystore key plus passphrase-encrypted export |
|---|---|---|---|
| Security (30) | 5 | 1 | 5 |
| Child use without typing a PIN (20) | 5 | 1 | 5 |
| Recovery and device change (20) | 0 | 3 | 4 |
| Privacy, no cloud (15) | 5 | 5 | 5 |
| Simplicity (15) | 5 | 3 | 3 |
| **Total /500** | 400 | 230 | **450** |

C vs A: A loses the whole progression when the tablet breaks or is replaced, which would discourage a reluctant child; C costs one screen in the parent space. B is out: a 4-digit PIN has 10,000 values and is brute-forced in seconds on a copied database, and the child would need the PIN at each launch.
Sensitivity: moving s points from recovery to simplicity gives A = 400 + 5s and C = 450 − s; A overtakes C only when recovery weighs less than about 12.
**Decision: C.**

- The database key is 256 random bits generated on first launch and stored with expo-secure-store (Android Keystore, iOS Keychain). Nobody, the parent included, ever sees it.
- In the parent space, "Export a backup" asks for a passphrase, derives a key with Argon2id and writes an encrypted file that the parent stores where they want. The app never uploads it.
- "Restore" on a new device reads the file and the passphrase. A forgotten passphrase means that backup cannot be read.
- If the stored key is missing or invalid at start-up, the app does not overwrite the database: it offers a restore or, after the parent PIN, a reset.

## Decision outcome

D1 A, D2 A, D3 C, chosen by the owner on 2026-10-23.

## Consequences

- Native modules are needed: development and tests use a development build, never Expo Go.
- The storage adapter owns the key handling and the `cipher_version` guard; the domain model stays unaware of encryption (ADR-0002).
- Export and restore are parent-space use cases to add to the use-case spec and diagrams (scheduled V1 or V1.1, tracked in its own issue).
- Unit tests cover the guard (start-up refused without SQLCipher) and an export/restore round trip.
