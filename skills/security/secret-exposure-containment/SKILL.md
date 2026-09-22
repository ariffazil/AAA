---
name: secret-exposure-containment
id: secret-exposure-containment
version: 1.0.0
risk_tier: medium
description: 'Use when a secret leaked or services over-share keys.'
owner: HERMES
floor_scope:
- F1
- F2
- F4
- F11
- F12
- F13
autonomy_tier: T2
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Secret Exposure Containment

Name-only inspection, exposure classification, per-service secret scoping, rotation ordering.
Companion to `forge-secret-hygiene` (which audits file age and plaintext). This skill covers the
**inspection** and **blast-radius** half: how to look without leaking, and how to stop one
service's compromise from becoming every service's compromise.

## Rule 1 — a scan must never format a value into output

Names and fingerprints only. Fingerprint that is safe to print:
`printf '%s' "$VAL" | sha256sum | cut -c1-12`.

- **Never grep `KEY=VALUE` dumps.** A line-level regex runs against the whole line, so it
  matches on the *value* too. Real case (2026-09-21): `grep -iE 'chron|store|db|path'` over
  `/proc/<pid>/environ` matched a provider API key whose value contained `db`, printing it
  into an agent tool transcript. The pattern was not the defect — reading `environ` as text is.
- **Use the wrapper:** `/root/scripts/secretsafe.py` — `env <pid|unit>`, `file <path>`,
  `units`, `agentcheck`. Name-only by default; raw mode needs both `ARIFOS_SECRETSAFE_RAW=1`
  **and** a real tty, so agent/pipe contexts are refused. Regression test:
  `/root/scripts/tests/test_secretsafe.py` asserts names surface and zero values are emitted.
- **Never `cat`/`echo` an `EnvironmentFile`, `.env`, or secret store.** Names via
  `grep -oE '^[A-Z_][A-Z0-9_]*'` or the wrapper.

## Rule 2 — classify exposure by mechanism, not by what you noticed first

If a process environment was emitted in full, **every** credential in that process is
`POTENTIALLY_EXPOSED`. Never assume only the variable you happened to notice.

Also audit the write side: values persist in `~/.hermes/state.db-wal`, `cache/terminal/`
snapshots, agent session directories, and search indices — not just the log you were reading.
A file-count + occurrence-count sweep over the agent directories measures the real blast radius
without printing anything.

## Rule 3 — broadcast `EnvironmentFile=` is the structural defect

`EnvironmentFile=/root/.secrets/<flat>.env` hands **every** secret in that file to **every**
unit loading it. One env dump, core dump, or memory bug anywhere on that list exposes the whole
file.

```
secret(service_i) ∩ unnecessary_credentials = ∅      # target invariant
```

Scoping is **A3 work, not A1** — per-unit audit, not a bulk edit. Per service:
`SECRETS_PRESENT` (from its EnvironmentFiles) minus `SECRETS_ACTUALLY_REQUIRED` (scan that
service's own code tree for variable names) = `EXCESS`. A pure-computation organ referencing no
provider key should load no provider key.

Enumerate unique canonical units via `systemctl show <unit> -p FragmentPath --value`. A
filesystem glob over `/etc/systemd/system/**` follows `.wants/` symlinks, double-counts units,
and inflates the work estimate.

**De-scoping is reversible and safe:** back up the unit file, comment out the
`EnvironmentFile`, `daemon-reload`, restart, then verify `/health` plus that the service's own
counters still advance. A missing credential surfaces as an attributable error on the feature
that needs it — not as a silent boot failure.

## Rule 4 — incident ordering

A leaked credential is **burned until rotated**. Log redaction is secondary containment, not
repair.

1. Identify issuer → issue replacement → update canonical store.
2. **Rotate before de-scoping config.** Rotating first means a config error cannot leave a
   service with no working credential.
3. Revoke the old credential; test that it no longer works where that is safe.
4. Preserve the forensic evidence needed to establish what happened.

**Rotation is issuer-side.** An agent cannot mint a key inside the principal's provider
account — that is an F13 decision. Bundle rotation and de-scoping into **one** decision:
rotation alone leaves the exposure path intact; de-scoping alone leaves a live,
already-on-disk credential.

## Receipt shape

Report `EXPOSED_COUNT · ROTATED_COUNT · REVOKED_COUNT · SERVICES_DE-SCOPED ·
EXCESS_SECRET_EDGES_REMOVED · REGRESSION_TEST=PASS|FAIL`. Never the values.

DITEMPA BUKAN DIBERI
