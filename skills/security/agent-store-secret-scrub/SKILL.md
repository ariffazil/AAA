---
name: agent-store-secret-scrub
description: "Use when scrubbing a leaked secret out of stored logs."
version: 1.0.0
tags: [secrets, containment, sqlite, redaction, verification, incident, forensics]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Agent Store Secret Scrub

A credential printed into a chat, a tool result, a transcript or a database row is **burned**.
Redacting it afterwards is containment, not repair — the value already existed somewhere it was not
supposed to be. This skill is the procedure for removing it, and for reporting what actually remains
instead of claiming a clean sweep.

Distinct from *classifying* an exposure (which services could read the file, blast radius,
rotation order). This is the write side: get the value out of the stores and prove what is left.

## When to use

- A key, session token, password, or signed URL has appeared in a message body, tool output, log line,
  or database column and you are asked to clean it.
- You are about to scan for exposed secrets — read Rule 0 first, because the scan itself is how most
  of these leaks get a second copy.

## Rule 0 — The scan must never format the value into output

Names and fingerprints only.

```bash
printf '%s' "$VAL" | sha256sum | cut -c1-12     # safe to print
```

- **Never print a matched secret while searching for secrets.** A scan that echoes its matches writes
  the credential into the very transcript you are cleaning, one layer deeper and harder to reach.
  Print `row id`, `length`, and `sha256[:12]` — never the value, never a truncation of it.
- **Never `grep 'KEY=VALUE'` a config or environ dump.** A line-level regex matches on the value
  too. Read the name column only (`grep -oE '^[A-Z_][A-Z0-9_]*'`), or use the dedicated
  name-only wrapper.
- When you need to show a human *which* secret leaked, show the fingerprint and the label. That is
  enough to identify it and useless to an attacker.

## Rule 1 — A shape-based scrubber has blind spots; scan for the token, not the pattern

Platform and gateway redactors typically match `KEY=value` and short `sk-…` style credentials. A
long base64 parameter inside a signed URL — an `…-Security-Token=` in an S3 presigned link — can pass
straight through while a sibling parameter (`…-Credential=`) on the *same line* is redacted.

Consequence: **do not conclude "the scrubber handled it".** Scan for the parameter name you care
about and check whether what follows it is a redaction marker or real entropy:

```
match = value following the parameter name
value starts with '[' + 'REDACTED'  -> handled
value is long base64/alnum          -> leaked, keep hunting
```

## Rule 2 — Enumerate every surface before you scrub one

Count them, because the receipt has to name them:

| Surface | Typical path shape |
|---|---|
| live store | `state.db` (messages/content columns) |
| write-ahead log | `state.db-wal` — holds recent pages the main file does not yet |
| session dumps | agent/session directories, JSON transcripts |
| logs | service logs, cron logs, error logs |
| backups / quarantine | pre-migration copies, `*.pre-*` snapshots |

A backup made with default umask is often world-readable. Tighten it (`chmod 600`) even when you
cannot yet remove its contents — that is a one-second reduction in blast radius.

## Rule 3 — Scrub at row level, then verify at BYTE level

These are two different facts and the first one is the weaker:

```
rows with an unredacted value  = 0     <- row-level query says clean
raw bytes in the file          > 0     <- because SQLite keeps pages
```

Procedure:

1. `UPDATE` each affected row, substituting a stable marker (`[REDACTED:<CLASS>]`) via a parameterised
   query. Match the value with a bound regex so you do not have to print it.
2. `PRAGMA wal_checkpoint(TRUNCATE)` — otherwise the pre-edit pages sit in the WAL.
3. Re-run the row query: `WHERE content LIKE '%PARAM=%' AND content NOT LIKE '%PARAM=[REDACTED%'`.
4. **Scan the file bytes** with a compiled regex over `open(path,'rb').read()`. This is the only
   check that speaks for the artifact rather than the index.
5. Report both numbers. "0 rows, N byte-residual in free pages" is a true statement. "Cleaned" is not.

## Rule 4 — `VACUUM` alone does not reclaim the bytes

- `PRAGMA secure_delete=ON` zeroes deleted cell content as it is freed, which helps but does not
  guarantee the old page image is gone from the file or the WAL.
- `VACUUM` rewrites the database, yet a byte scan can still find the value afterwards (observed
  directly: 8 byte-hits in the main file after `secure_delete=ON` + `wal_checkpoint` + `VACUUM`).
- **True removal needs `VACUUM INTO new.db` with no writer holding the database**, then replace the
  file. That means stopping the process that owns it — a runtime interruption with its own
  consequences. Do not do that silently mid-session, and do not claim you did.
- The honest end state for a live store is: *all rows redacted, residual bytes in freelist pages,
  recorded, with the credential already expired or rotated.* Reach for that sentence, not "clean".

## Rule 5 — Establish whether the credential is still alive before escalating

Compute expiry from the credential's own issuance data, not from vibes. A signed URL carries an
issue timestamp and a TTL:

```
issued + ttl  <  now   -> EXPIRED: the leak is a hygiene defect, not live access
issued + ttl  >= now   -> LIVE: rotation is urgent and belongs to the issuer/principal
```

This changes the report substantially and honestly. "Four session tokens were stored; all four
had expired hours before discovery; no live credential is exposed, the defect is that they were
stored at all" is a different message from "rotate now".

## Rule 6 — Do not fight the live writer

- Set `busy_timeout` generously and open read-write; a scrub is a handful of `UPDATE`s.
- **Do not kill or restart the runtime that owns the store to make the scrub easier.** You will
  trade a dormant token for an outage, and the session you are talking to the principal in is
  probably served by that process.
- Reading a multi-gigabyte database into memory is fine for a byte scan; looping a per-line regex
  over a whole tree is not. Bound it: target the specific files, compile the pattern once.

## Receipt shape

```
SURFACES_SCANNED   · n
ROWS_REDACTED      · n        ROWS_RAW_REMAINING · 0
BYTE_RESIDUAL      · n hits in <file> (freelist), <file2> (backup, perms tightened)
DISTINCT_VALUES    · n        (fingerprints only, never values)
LIVE_CREDENTIALS   · 0 | n    (computed from issue time + ttl)
REMAINING_ACTION   · rotate at issuer | none
```

Close with the structural fix: the store keeps what was pasted into it, so the durable control is
never pasting a signed URL into a chat or a report — reference the file, not the live link.

## Pitfalls

- **Scrubbing while scanning.** Running an exploratory regex that prints matches *while* looking for
  leaks converts one incident into two. Write the scan to emit names and fingerprints only, the
  first time.
- **Trusting the row query.** `SELECT count(*) … AND NOT LIKE '%[REDACTED%'` returning 0 is evidence
  about the index, not the artifact. Byte-scan the file or you have not verified removal.
- **Forgetting the WAL.** Recent writes live in `-wal`; checkpoint before you believe the main file.
- **Forgetting the backup.** A `.pre-*` snapshot taken before the scrub still contains the plaintext
  and often carries looser permissions than the live file.
- **A redaction marker collision.** If the marker text itself appears inside a search pattern, a
  second pass will re-match its own output. Match on `PARAM=` followed by non-marker entropy.
- **Reporting "cleaned" for a live store.** The only defensible closure for a store you cannot take
  offline is: rows redacted, residual recorded, credential expired or rotated.

## See also

`hermes-state-db-forensics` (querying the same store for history and cost),
`secret-exposure-containment` (exposure classification, per-service scoping, rotation order),
`probe-instrument-trust` (verifying the check itself).
