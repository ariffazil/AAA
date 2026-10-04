---
id: vault999-audit-forensics
name: vault999-audit-forensics
version: 1.0.0
description: "VAULT999 audit forensics — field schema variations across vault files, automated probe attribution gaps, forward-fix vs backfill decisions, and orphaned entry patterns."
owner: HERMES
risk_tier: high
floor_scope: ['F1', 'F2', 'F11']
autonomy_tier: T1
tags: [vault999, audit, forensics, schema, governance, forensic-scan]
related_skills: [FORGE-vault999-witness, audit-seal, arifos-kernel-eurekas]
---

# VAULT999 Audit Forensics

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose

Audit VAULT999 files for orphaned entries, schema drift, and automated probe attribution gaps. This is the *forensic* companion to `FORGE-vault999-witness` (which covers writing and chain verification).

## When to Use

- Scanning VAULT999 for unknown/orphaned actor entries
- Cross-referencing automated pipeline outputs against vault entries
- Deciding whether to backfill or forward-fix orphaned entries
- Investigating unexpected entries (wrong actor, wrong tool, wrong time)

## When NOT to Use

- Writing new seal entries (use `FORGE-vault999-witness`)
- Verifying chain hash integrity (use `FORGE-vault999-witness`)
- High-frequency monitoring (use Postgres telemetry)

## Critical Pitfall: Different JSON Schemas Across Vault Files

**VAULT999 files do NOT share a uniform schema.** Different writers produce different field names for the same concepts:

| Field Concept | `outcomes.jsonl` | `institutional_ledger.jsonl` | `seal_chain.jsonl` |
|---|---|---|---|
| Who acted | `actor` | `doer` | `actor` |
| What happened | `event` | `action_type` | `tool` |
| Assessment | `verdict` | `verdict` | `judge_decision` |
| Session | `session` | (absent) | (absent) |
| Classification | (absent) | `classification` | (absent) |
| Detail | `detail` | `raw` | `payload` |

**When auditing, always check the actual field names of the specific file you're reading.** Don't assume `type` exists — check for `event`, `action_type`, `tool`. Don't assume `actor` exists — check for `doer`. A scan looking for the wrong field name produces false negatives (V1 severity overreporting).

## Decision Pattern: Forward-Fix vs Backfill

When orphaned entries are found in VAULT999:

| Option | Action | When to use | Risk |
|---|---|---|---|
| **Forward-fix** ✅ | Fix the pipeline NOW, leave orphaned entries as historical artifact | **Almost always** | Low — orphaned entries are scar, not bug |
| **Backfill** ❌ | Patch existing entries with correct actor attribution | Almost never | High — violates append-only covenant (F1 AMANAH) |

**Default: FORWARD-FIX.** VAULT999 is append-only by covenant. Backfilling mutates immutable truth. The orphaned entries are *historical truth* — they happened, they just lack attribution. That's a scar. Live with it. Fix forward.

## Automated Probe Attribution Pattern

Automated pipelines (cron jobs, liveness probes, stability probes) call arifOS kernel tools and write receipts to VAULT999 without setting proper `actor` or `session` identifiers.

**Root cause identification:**
1. Take 3-5 orphaned entries with exact timestamps
2. Cross-reference against cron job execution logs (`/root/HERMES/cron/jobs.json`, systemd timers, crontab)
3. Match timestamps to identify the specific pipeline
4. Common culprits: arifOS liveness cron, arifFlow FQ pulse, organ health probes, A-FORGE test suite

**Fix pattern:**
```python
# BAD (produces orphaned entries):
result = arif_observe(subject="health_check", frame="ok")

# GOOD (attributed entries):
result = arif_observe(
    subject="health_check",
    frame="ok",
    actor_id="liveness_probe",
    session_id="probe-2026-08-11-0600"
)
```

## Severity Classification

| Finding | Severity | Action |
|---|---|---|
| Orphaned entries from automated probes | LOW | Forward-fix pipeline |
| Entries with wrong actor (not unknown) | MEDIUM | Investigate impersonation |
| Entries that shouldn't exist at all | HIGH | Potential breach — apex-judge |
| Chain hash mismatch | CRITICAL | VAULT999 integrity failure — 888_HOLD |

## Verification After Fix

```bash
# Count orphaned entries before fix
grep -c '"actor": "unknown"' /root/arifOS/VAULT999/outcomes.jsonl

# After pipeline fix, check last 10 entries for proper attribution
tail -10 /root/arifOS/VAULT999/outcomes.jsonl | python3 -c "
import json, sys
for line in sys.stdin:
    d = json.loads(line.strip())
    actor = d.get('actor', 'MISSING')
    session = d.get('session', 'MISSING')
    print(f'actor={actor} session={session}')
"
```

## Methodology Lesson (2026-08-11)

When scanning vault files, always probe the first entry's actual keys before writing a bulk scan:

```python
with open('/root/arifOS/VAULT999/outcomes.jsonl') as f:
    line = json.loads(f.readline().strip())
    print(f'keys: {list(line.keys())}')  # Check actual schema FIRST
```

Assuming the wrong field names leads to V1→V2 severity misclassification. The `institutional_ledger.jsonl` entries that looked "unclassified" were actually properly classified — the scan looked for `type` but the field is `action_type`.

## References

- Canonical skill: `FORGE-vault999-witness` (write + chain verification)
- Audit chain: `audit-seal` (decision logging)
- Substrate honesty: `arifos-kernel-eurekas` K1-K3 (vault reader behavior)
