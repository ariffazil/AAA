---
title: P2-A Orphan Cron Retirement -- First Chamber Test Case
date: 2026-08-11
f13_directive: "Use P2-A to prove the chamber works. Do not solve P2-A -- use P2-A as test case."
stage_at_forge: 0.5_of_5 (sanitized, awaiting OpenClaw route)
---

# P2-A Orphan Cron Retirement -- First Chamber Test Case

## Background

On 2026-08-11, during a session to clean up the federation's 23-cron list (3 killed, 20 lane-annotated), a duplicate cron pair was discovered:

- **Hermes** `vault-data-refresh` (in `/root/HERMES/cron/jobs.json`) -- writes `/var/www/html/arif/999/vault-data.json` every 15 min
- **system** `/etc/cron.d/arifos-vault-tail` -- writes `/var/www/html/999/vault-data.json` every 1 min

## Receipt-First Verification (V2)

### Checks

| Check | Value | Evidence |
|---|---|---|
| `schedule_match` | PARTIAL | Hermes 15m vs cron.d 1m |
| `deliver_target_match` | PARTIAL | Both write `vault-data.json` but to different paths |
| `data_source_match` | false | Hermes: `/root/arifOS/VAULT999/outcomes.jsonl`. cron.d: `/root/.local/share/arifos/vault999/seal_chain.jsonl` |
| `output_match` | PARTIAL | Same JSON format `{receipts: [...]}` |

### Verdict: DUPLICATE_WRITER

The cron.d writes to `/var/www/html/999/` -- **a path with no Caddy route**. The Hermes writes to `/var/www/html/arif/999/` -- **Caddy-served** via `@validation strip_prefix /999 -> root /var/www/html/arif/999`.

The cron.d log claims success every 6 minutes, but the orphan file's mtime shows it last wrote 13 hours ago. Cron misfiring silently.

### Fitness comparison

| Cron | Fitness |
|---|---|
| Hermes vault-data-refresh | Canonical. Caddy-served. 15m cadence. No orphans. |
| cron.d arifos-vault-tail | Orphan. No consumer. Stale. Higher cost (1m). |

**Winner: Hermes vault-data-refresh.** Retire cron.d.

## Chamber Cycle Initiated

Per F13 advisory, this became the **first chamber test case** for the new protocol. Hermes was not to execute directly -- it must observe, prepare proposal, post to AAA chamber, and stand down.

## Stage 0: Hermes Proposal (sanitized)

`/root/forge_work/chamber_proposals/2026-08-11/P2-A-orphan-cron-retirement.sanitized.md`

Size: 6,280 bytes, all ASCII, 171 lines.

### Key sections preserved
- Header (proposal_id, chamber_role, risk_tier)
- Observation (with file paths, mtimes, Caddy config)
- Recommendation (survival-of-the-fittest verdict)
- Affected Files table (with backup paths)
- Rollback Path (full reversibility declared)
- Proposed Chamber Flow (5 stages with Hermes DONE)

### What got sanitized
- em-dash `--` (10 occurrences) -- originally `—`
- arrow `->` (2 occurrences) -- originally `→`
- checkmark `[OK]` (1 occurrence) -- originally `✅`

## Stage 0.5 VAULT999 Receipts

| ts (UTC) | event | verdict | chain_hash |
|---|---|---|---|
| 01:53:05 | chamber_proposal_post | POSTED | 4d4fd49de84827cf |
| 02:00:57 | chamber_proposal_sanitized | POSTED | c7ad2dae31852d6c |

Both receipts chained forward; prev_hash verified against last valid entry.

### Anomaly documented

A prior receipt (entry 47258) had `prev_hash=0000000000000000` due to a first-attempt miss when constructing the chain. VAULT999's `chattr +a` prevented removal. Mitigation: `chain_reconciliation NOTICE` receipt appended (entry 47260), explaining that 47259 is canonical and 47258 is vestigial.

## Stage 1+: Awaiting chamber route

After sanitization + receipt, **Hermes stood down**. The remaining 4 stages depend on:
- **OpenClaw** to route to 555-ASI
- **555-ASI** to independently verify V2 evidence (or live probe cron.d file state)
- **888-APEX** to judge via apex-judge isolate
- **777-FORGE** to execute via A-FORGE
- **VAULT999** to close with final chain_hash

## Why P2-A is the right test case

Per F13 advisory:
- **Low risk** -- T2, system cron, reversible
- **Reversible** -- full restore from `/root/forge_work/retired_cron/2026-08-11/`
- **Evidence-backed** -- V2 verification receipts already filed
- **Operational** -- tests real cron.d retirement, not synthetic action
- **Non-constitutional** -- does not cross F1-F13 thresholds; failure doesn't collapse the federation

If the loop fails:
- Federation learns the chamber's failure mode
- Cron.d keeps running harmlessly (writes to orphan)
- Hermes can re-propose after diagnosis

## Anti-pattern prevented

Before the chamber protocol, Hermes was preparing to:
1. `mv /etc/cron.d/arifos-vault-tail` directly
2. `rm /usr/local/bin/arifos-vault-tail-refresh.sh`
3. Delete orphan file
4. Stop service
5. Declare success

This would have been the **four-stage collapse**: OBSERVE -> DECIDE -> EXECUTE -> CERTIFY.

Instead, Hermes prepared one proposal, sealed it to VAULT999, and stood down. The chamber cycle starts.

## Lessons captured

1. **Sanitize before post.** First chamber proposal must be ASCII-clean. Variation selectors / zero-width chars trigger security scanners and pollute receipt lineage.

2. **VAULT999 append-only is the witness invariant.** Don't try to remove broken entries. Document anomaly and chain forward.

3. **Hermes' authority ceiling is below infra level.** Cron.d retirement is infrastructure mutation -> 777-FORGE domain, not Hermes. Even if Hermes sees the obvious win.

4. **Receipt-first verification beats "looks redundant".** Survival of the fittest means measuring, not eyeballing. V1 (digest pair) was NOT a duplicate despite sharing schedule -- different data sources + different outputs. V2 (vault pair) WAS a duplicate writer despite different schedules -- only one has a consumer.

5. **The chamber is the test, not the cron.** Real success metric: complete governance cycle without role collapse. P2-A orphan retirement is the test payload.

## Reference

- Skill: `aaa-chamber-protocol` (this skill)
- Proposal: `/root/forge_work/chamber_proposals/2026-08-11/P2-A-orphan-cron-retirement.sanitized.md`
- V2 verification receipt: `/root/forge_work/verification/2026-08-11-verification-receipts.json`
- Related skills: `apex-judge`, `seal-session`, `nusantara-action-spiral`, `l0-l4-cascade-doctrine`
