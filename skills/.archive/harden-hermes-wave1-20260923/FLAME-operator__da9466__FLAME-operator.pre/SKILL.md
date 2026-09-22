---
id: FLAME-operator
name: FLAME-operator
version: "2026.08.04"
description: >
  Probe FLAME health, inspect hit rates, diagnose model failures, recover
  demoted tiers, and maintain free-tier routing state within the RM0 and
  constitutional boundaries.
owner: AAA
risk_tier: medium
autonomy_tier: T2
floor_scope:
  - F1
  - F2
  - F11
  - F13
---
# 🔥 FLAME-operator — Operate & Maintain FLAME

> **Skill ID:** FLAME-operator · **Version:** 2.0.0 · **Axis:** ops
> **Load when:** Probing FLAME health, checking hit-rates, recovering demoted tiers,
>   debugging model failures.
> **Do NOT load for:** Adding paid models (constitutional boundary), changing agent cascade.

## Quick Ops

```bash
# Health probe — all 12 tiers, latency + content sanity
free-llm --mode probe

# Hit-rate dashboard — calls, success rate, avg latency per model
free-llm --mode stats

# Integrity snapshot — SHA256 of hit-rate state (NOT a seal)
free-llm --mode snapshot-checksum

# S5 Auto-recovery — attempt to re-promote demoted tiers after cooldown
free-llm --mode recover
free-llm --mode recover --json   # machine-readable

# Batch inference — one prompt per line
free-llm --batch /path/to/prompts.txt

# Single inference with JSON output
free-llm "prompt" --json
```

## Tier Architecture (12 tiers, 2026-08-04)

FLAME runs 12 tiers of free/cheap models across Groq, SEA-LION, Gemini, Cerebras,
OpenRouter, and Ollama. Auto-demotion fires at 3 consecutive fails. Auto-recovery
attempts re-promotion after a 30-minute cooldown.

```bash
# List all tiers
python3 -c "
import json
cfg = json.load(open('/root/A-FORGE/flame/flame_config.json'))
for t in cfg['chains']['RM0-TOOLS-FREELOOP']['tiers']:
    w = t.get('weight', 1)
    print(f'{t[\"provider\"]}/{t[\"model\"]}  (weight={w})')
"
```

## Health Probe Interpretation

| Signal | Meaning | Action |
|--------|---------|--------|
| ✅ 200 + content | Model healthy | None |
| ❌ HTTP 4xx | Auth/key/config broken | Check vault.env, verify key |
| ❌ HTTP 429 | Rate limited | Model auto-demoted, wait 5 min |
| ❌ Empty content | Safety filter or model issue | Mark as degraded in hit-rate |
| ⚠️ >5s latency | Model slow | Demote in next reorder cycle |

## Dynamic Reordering

FLAME auto-reorders every 5 minutes based on:
1. **Latency:** Faster models promoted
2. **Hit-rate:** Higher success rate weighted higher
3. **Weight:** Config-defined preference multiplier

```bash
# Force immediate reorder
python3 -c "
from flame_router import FlameEngine
e = FlameEngine()
new_order = e.reorder_by_latency()
for t in new_order: print(f'{t[\"provider\"]}/{t[\"model\"]}')
"
```

## Tier Management

### Auto-Demotion (L5)
- **Trigger:** 3 consecutive fails on any tier
- **Effect:** tier marked inactive, skipped in cascade
- **Escalation:** 10 total fails → permanent removal (requires manual re-probe)
- **S5 fix (2026-08-04):** caller-fault (reasoning model with starved token budget)
  is detected via heuristic (>100 chars reasoning OR `<think>` markers) and does NOT
  increment consecutive_fails. Only genuine model-faults trigger demotion.

### Auto-Recovery (S5 Part 2)
```bash
# Attempt recovery of all demoted tiers (30-min cooldown per tier)
free-llm --mode recover
```

- **Cooldown:** 30 minutes before re-probe attempt
- **Probe:** "Say OK" with 80 max_tokens, 5s timeout
- **Success:** tier reactivated, consecutive_fails reset, promoted_at recorded
- **Failure:** demoted_at reset to now (cooldown extended another 30m)
- **Cron:** install a 5-minute timer to auto-run recovery
  ```bash
  # Already installed at:
  systemctl status flame-recover.timer
  ```

### Manual Recovery (when auto-recovery fails 3+ times)
1. Direct probe the provider: `curl` test the endpoint
2. If provider is dead/expired: mark in FED, update config
3. If provider is healthy but tier still failing: check model ID, key rotation, rate limits
4. Force-reactivate: edit `flame_config.json` → set `active: true` on the tier
5. Run `free-llm --mode probe` to verify

## Hit-Rate File

> **2026-08-04 path correction** — verified live. Doc referenced wrong directory for 9 days
> (state file zeroed since 2026-07-26 because no FLAME process was writing to that path).
> Canonical paths below. A compat symlink was created at the legacy path so old monitoring
> tools keep working.

```
Hit-Rate: /root/.local/share/flame/flame_hitrate.jsonl
State:    /root/.local/share/flame/flame_state.json     ← canonical (FLAME writes here)
Seal:     /root/A-FORGE/flame/flame_seal.txt
Compat:   /root/.local/share/arifos/flame_state.json → ../flame/flame_state.json
```

**If you see the legacy path returning zeros or missing**: it was the bug. Read the canonical
path above. Do NOT edit the legacy file — it's a symlink.

Each line in hitrate.jsonl is a call record with provider, model, success, latency, timestamp.

## Debugging Model Failures

```bash
# Direct model test (bypass FLAME)
curl -s "PROVIDER_BASE/chat/completions" \
  -H "Authorization: Bearer $KEY" \
  -d '{"model":"MODEL_ID","messages":[{"role":"user","content":"Reply READY"}],"max_tokens":10}'

# Check current tier state (active/inactive/demoted)
python3 -c "
from flame_router import FlameEngine
e = FlameEngine()
for k,v in e.hitrates.items():
    status = '🟢' if v.active else '🔴'
    demoted = f' (demoted {v.demoted_at})' if v.demoted_at > 0 else ''
    print(f'{status} {k}: {v.calls}c {v.hit_rate:.0%}hr {v.avg_latency_ms:.0f}ms{demoted}')
"

# Attempt recovery
free-llm --mode recover

# Force reorder
python3 -c "
from flame_router import FlameEngine
e = FlameEngine()
new_order = e.reorder_by_latency()
for t in new_order: print(f'{t[\"provider\"]}/{t[\"model\"]}')
"
```

## Constitutional Boundary

FLAME-operator is a **maintenance skill**, not a governance skill. It does not:
- Change which models are in the agent cascade (arifOS kernel domain)
- Add paid models (RM0 hard gate)
- Modify F1-F13 thresholds

For governance decisions (adding providers, changing cascade order), use the agent lane with `arif_judge`.
