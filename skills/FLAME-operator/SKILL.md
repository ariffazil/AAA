# 🔥 FLAME-operator — Operate & Maintain FLAME

> **Skill ID:** FLAME-operator · **Version:** 1.0.0 · **Axis:** ops
> **Load when:** Probing FLAME health, checking hit-rates, reordering tiers, debugging model failures.
> **Do NOT load for:** Adding paid models (constitutional boundary), changing agent cascade.

## Quick Ops

```bash
# Health probe — all 8 models, latency + content sanity
free-llm --mode probe

# Hit-rate dashboard — calls, success rate, avg latency per model
free-llm --mode stats

# Integrity seal — SHA256 of hit-rate state
free-llm --mode seal

# Batch inference — one prompt per line
free-llm --batch /path/to/prompts.txt

# Single inference with JSON output
free-llm "prompt" --json
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

**Promote a model:**
1. Verify model is healthy: probe it directly
2. If hit-rate > 80% and latency < benchmark: it auto-promotes next cycle
3. Manual: edit `flame_config.json` → increase weight

**Demote a model:**
1. If hit-rate < 30% for 10+ calls: auto-demoted
2. Manual: edit `flame_config.json` → decrease weight or set `active: false`

**Add a new free model:**
1. Verify model works: `curl` test the endpoint
2. Add to `flame_config.json` under provider → tiers
3. Health probe: `free-llm --mode probe` (will include new model)
4. Propagate to OpenCode/OpenClaw/Hermes if needed

**Remove a dead model:**
1. Confirm dead: 3+ consecutive probe failures
2. Remove from `flame_config.json` tiers
3. Health probe to verify
4. Remove from agent configs if present

## Hit-Rate File

```
Location: /root/.local/share/arifos/flame_hitrate.jsonl
State:    /root/.local/share/arifos/flame_state.json
Seal:     /root/A-FORGE/flame/flame_seal.txt
```

Each line in hitrate.jsonl is a call record with provider, model, success, latency, timestamp.

## Debugging Model Failures

```bash
# Direct model test (bypass FLAME)
curl -s "PROVIDER_BASE/chat/completions" \
  -H "Authorization: Bearer $KEY" \
  -d '{"model":"MODEL_ID","messages":[{"role":"user","content":"Reply READY"}],"max_tokens":10}'

# Check if model is in FLAME config
python3 -c "
import json
cfg = json.load(open('/root/A-FORGE/flame/flame_config.json'))
for t in cfg['chains']['RM0-TOOLS-FREELOOP']['tiers']:
    print(f'{t[\"provider\"]}/{t[\"model\"]}')
"

# Check hit-rate for specific model
python3 -c "
from flame_router import FlameEngine
e = FlameEngine()
stats = e.stats()
for k,v in stats.items():
    if 'MODEL_NAME' in k: print(f'{k}: {v}')
"
```

## Constitutional Boundary

FLAME-operator is a **maintenance skill**, not a governance skill. It does not:
- Change which models are in the agent cascade (arifOS kernel domain)
- Add paid models (RM0 hard gate)
- Modify F1-F13 thresholds

For governance decisions (adding providers, changing cascade order), use the agent lane with `arif_judge`.
