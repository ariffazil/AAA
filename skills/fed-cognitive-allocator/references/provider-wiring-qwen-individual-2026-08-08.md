# Provider Wiring — Qwen Individual Pro (2026-08-08)

Session transcript of wiring `qwen-token-plan-individual` into FED, with exact commands, SQL, and failure modes. Reuse as the recipe template for any future provider integration.

## Context

- Qwen Cloud Token Plan **Team** (`QWEN_API_KEY`) — 3 seats EXHAUSTED (0/150,000 credits, reset 2026-09-01). Qwen-native models 429.
- Qwen Cloud Token Plan **Individual Pro** (`QWEN_INDIVIDUAL_API_KEY`) — LIVE: 94.5% of 40K 7-day window remaining, 5hr limit temporarily removed by QwenCloud, auto-renew, expires 2026-09-01, paid $73.45 on 2026-07-31.
- LiteLLM (`/root/A-FORGE/litellm-config.yaml`) was **already** on `os.environ/QWEN_INDIVIDUAL_API_KEY` for all 7 qwen entries — the execution path was fine; FED's registry metadata was the stale part.

## Step 1 — Live probe (F2 evidence)

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

# Auth + model list
curl -s https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/models \
  -H "Authorization: Bearer $QWEN_INDIVIDUAL_API_KEY"

# Quota reality check per model (max_tokens:5, "say OK")
curl -s https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $QWEN_INDIVIDUAL_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3.8-max","messages":[{"role":"user","content":"say OK"}],"max_tokens":5}'
```

Probed OK: qwen3.6-flash (1.74s), qwen3.8-max (1.53s), deepseek-v4-pro. 11 models visible: qwen3.6-flash, qwen3.7-max, qwen3.7-plus, qwen3.8-max, deepseek-v4-flash-0731, deepseek-v4-pro, glm-5.2, wan2.7-image[-pro], qwen-audio-3.0-realtime-plus/tts-plus.

## Step 2 — DB provider row + route health

```sql
INSERT INTO providers (provider_name, track_type, balance_usd, last_updated, confidence_score, last_probed_at, notes)
VALUES ('qwen-token-plan-individual', 'A', 0.0, '<now>', 1.0, '<now>',
  'LIVE 2026-08-08 — Arif directive. Key: QWEN_INDIVIDUAL_API_KEY. 94.5% of 40K 7-day window remaining. '
  '| BILLING_MODEL=monthly_token_plan_credit');  -- tag is LOAD-BEARING, see balance gate

INSERT INTO route_health (provider_name, model_id, status, last_checked) VALUES ('qwen-token-plan-individual', 'qwen3.8-max', 'LIVE', '<now>');
-- ... one row per probed model
```

Backup first: `cp /root/.local/share/arifos/token_bank.db /root/forge_work/backups/token_bank-pre-individual-wire-<ts>.db`

## Step 3 — Code changes (`/root/AAA/scripts/fed_router.py`)

- Pricing: add `"qwen-token-plan-individual": DEEPSEEK_PRICING` to BOTH `_estimate_cost` and `_estimate_cost_per_1k` tables.
- `MODEL_ROUTES`: qwen-individual as `direct`, priority 2 under deepseek-v4-pro/flash (after native direct), priority 1 for qwen3.6-flash/qwen3.7-plus/qwen3.7-max/qwen3.8-max; glm-5.2 priority 1. `"constitutional": True` on deepseek-v4-pro, glm-5.2, qwen3.8-max entries.
- Balance gate: added `is_monthly_plan` exemption —

```python
notes = str(bal.get("notes", "") or "") if bal else ""
is_monthly_plan = any(tag in notes.lower() for tag in
    ("monthly_token_plan", "credit pack", "credit-based", "monthly plan", "credit_plan"))
if track == "A" and confidence >= 0.95 and not is_monthly_plan:
    # hard gate <$1.00
```

## Step 4 — Failure modes encountered

1. **Duplicate provider rows.** A sibling agent had already inserted `qwen-token-plan-individual` (notes: "LIVE 2026-08-08T06:48Z — Arif directive"). I inserted `qwen-individual` → duplicate. Fix: `DELETE FROM providers WHERE provider_name='qwen-individual'` + same for route_health, then `sed -i 's/"qwen-individual"/"qwen-token-plan-individual"/g' fed_router.py federation-models.json`.
2. **Phantom `alive_pools`.** `_meta.alive_pools` contained `qwen-token-plan-individual` with no matching provider entry. Reconciled: `d['_meta']['alive_pools'] = sorted([p['provider_id'] for p in d['providers'] if p.get('status')=='ACTIVE'])`.
3. **Balance-gate demotion.** After wiring, tier 666/999 qwen3.8-max ranked #1 BUT flagged `LOW_BALANCE_HARD` (balance_usd=0.0). Fixed by notes tag + code exemption → `balance_flag=None`, clean rank 1.
4. **`effort_level` overrides model.** First verification returned deepseek-v4-pro routes even though I asked for qwen3.8-max — Effort Dial replaces `model`. Re-test with `effort_level` omitted to verify a specific model's routes.

## Step 5 — Verification (post-restart)

- Tier 666 qwen3.8-max → rank 1 `qwen-token-plan-individual/qwen3.8-max` direct, flag=None ✅
- Tier 999 SEAL qwen3.8-max → rank 1 same ✅
- Tier 333 deepseek-v4-pro cascade → deepseek direct → mulerouter gateway → qwen-individual direct ✅

## Seal note

`arif_seal` via anonymous curl → `888_HOLD: Capability 'kernel.seal' requires SOVEREIGN authority. Actor: anonymous.` Sealing requires a proper `arif_init` session with SOVEREIGN actor (Arif's ACK), not a raw MCP probe.
