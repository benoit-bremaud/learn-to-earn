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
- Argon2id is not part of the Expo SDK: it needs a native library (for example libsodium `crypto_pwhash` through a React Native binding), to confirm at implementation time. This cost is counted in the D3 simplicity score.

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
**Decision: A.** At start-up the app reads `PRAGMA cipher_version` and refuses to open the database when it is empty, so a build without SQLCipher can never write plain data. It also refuses a database file whose header is the plain `SQLite format 3`, so an unencrypted file is never reused. `PRAGMA temp_store = MEMORY` keeps temporary tables off the disk; SQLCipher also encrypts the WAL. Expo Go is not used; development runs on a development build.

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

C vs A: A loses the whole progression when the tablet breaks or is replaced, which would discourage a reluctant child; C costs one screen in the parent space. B is out: a 6-digit PIN (P1) has 10^6 values and is still brute-forced offline on a copied database (our estimate: minutes to hours, whatever the lockout), and the child would need the PIN at each launch.
Sensitivity: moving s points from recovery to simplicity gives A = 400 + 5s and C = 450 − s; A overtakes C only when recovery weighs less than about 12.
**Decision: C.**

- The database key is 256 random bits generated on first launch and stored with expo-secure-store (Android Keystore, iOS Keychain), without user authentication (a change of screen lock or biometrics must not invalidate it) and, on iOS, readable after first unlock on this device only. Nobody, the parent included, ever sees it.
- Android Auto Backup is disabled for the app, so the database is never restored to a device without its key.
- In the parent space, "Export a backup" asks for a passphrase of at least 12 characters (the app can suggest a generated one), derives a key with Argon2id (at least 64 MiB, 3 passes, tuned on the target tablet) and writes the file with authenticated encryption (XChaCha20-Poly1305 or AES-256-GCM). A header holds the format version, the Argon2id settings, the random salt and the nonce, and is authenticated with the content, so a tampered or truncated file is rejected. The file is written straight to the place the parent picks, never as a plain temporary file, and the app never uploads it.
- "Restore" on a new device reads the file and the passphrase. A forgotten passphrase means that backup cannot be read.
- Key loss: a key-store error at start-up is retried first. Only when the key is definitely missing or does not open the database does the app show the key-loss screen, with two choices: restore (UC-P15) or set up again (UC-P14). The unreadable database is renamed and kept, never deleted, until a restore succeeds or the Guardian erases it later. Superseded by ADR-0004 D17: retried at each start for 30 days, then deleted with a note; bringing it back uses UC-P14 *a1. The PIN hash lives in the encrypted database, so the PIN cannot gate this screen.
Clarification (review 2026-10-24): "Set up again" creates the new database key under a new key-store alias. The old alias is kept for the 30-day window and deleted together with the set-aside database, or, once UC-P14 *a1 succeeds, the new alias is deleted instead (whichever key is replaced).

## Risks

- Key-loss take-over: on the key-loss screen, the child could choose "set up again" and pick a new PIN. This is the same risk as uninstalling and reinstalling the app, which no in-app control can stop; it is covered by the device-level protection of the app (OQ-1, OQ-6). The old database is kept (30 days, ADR-0004 D17), so the parent can still restore from an export.
- Restore after key loss brings back the PIN stored in the file, which ties into OQ-1 (PIN recovery, closed by ADR-0004 D15: the file's credential carries its recovery code hash).

## Decision outcome

D1 A, D2 A, D3 C, chosen by the owner on 2026-10-23.

## Consequences

- Native modules are needed: development and tests use a development build, never Expo Go.
- The storage adapter owns the key handling and the `cipher_version` guard; the domain model stays unaware of encryption (ADR-0002).
- Export (UC-P8) and restore (UC-P15) already exist in V1.0; their specs now include the passphrase, and UC-P15 also covers key loss.
- No child data in logs; crash reports (UC-P11) carry no database content.
- The export screen tells the Guardian to keep the file off unencrypted cloud folders.
- UC-P8, UC-P14 and UC-P15 specs and the cross-cutting storage rule were updated on 2026-10-23.
- Unit tests cover the guards (start-up refused without SQLCipher or on a plain file), an export/restore round trip, a tampered file and a wrong passphrase.
