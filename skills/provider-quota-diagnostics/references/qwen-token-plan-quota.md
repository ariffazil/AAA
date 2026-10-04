# Qwen Token Plan Quota — Federation Reference

## The 3-key shared pool

All three Qwen Token Plan keys in `/root/.secrets/kunci-mas.env` share **one underlying credit pool**:

| Env var | Key prefix | Role | Purpose |
|---|---|---|---|
| `QWEN_API_KEY` | `sk-sp-H.DIEXP` | Primary | Chat/completions, all 9 text models |
| `QWEN_INDIVIDUAL_API_KEY` | `sk-sp-H.DIIYD` | Individual Pro | Multimodal: image (wan2.7), video (happyhorse-1.1), audio (qwen-audio-3.0-tts-plus) |
| `QWEN_BAILIAN_KEY` | `sk-sp-H.IEHM` | Team/Bailian | Fallback for chat/completions |

**Endpoints (both hosted on Alibaba Cloud Singapore):**
- OpenAI-compatible: `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- Anthropic-compatible: `https://token-plan.ap-southeast-1.maas.aliyuncs.com/apps/anthropic`

## Individual Pro quota mechanics

| Window | Credits | Reset behavior |
|---|---|---|
| 5-hour rolling | 12,000 | Rolling window, can be temporarily lifted (promo) |
| 7-day rolling | 40,000 | Calendar reset at portal-designated time |

**Monthly cost:** $68/mo (Individual Pro subscription).

**Auto-renew:** ON, expires 2026-09-01 (24 days from 2026-08-07).

**Manual reset:** Portal shows "Reset Usage Limit: N available". Each reset returns full credits instantly. Resets are earned periodically (not unlimited).

## Live probe (2026-08-07 11:26 MYT) — exhausted state

```bash
# All 3 keys returned HTTP 200 on /models (valid)
# All 3 keys returned insufficient_quota on chat/completions (exhausted)
```

**Portal state at probe time:**
- 5h Usage Limit: Temporarily Lifted (∞ remaining)
- 7d Usage Limit: 0.0% remaining, 0/40,000 credits
- Reset time: 2026-08-07 15:38 MYT (~4h 12m from probe)
- Reset Usage Limit: 1 available (manual)

**Error messages by key:**
- `QWEN_API_KEY` (primary): `"Your token-plan quota has been exhausted."`
- `QWEN_INDIVIDUAL_API_KEY` (Indiv): `"Your token-plan 1-week quota has been exhausted. The quota will reset at 08-07 07:38:00 UTC."`
- `QWEN_BAILIAN_KEY` (team): `"Your token-plan quota has been exhausted."`

## Portal-only quota visibility

**Qwen Token Plan has NO public quota API.** All these paths return 404:

```
/v1/dashboard/billing/credit    → 404
/v1/quota                        → 404
/v1/account/quota                → 404
/dashboard/billing/credit        → 404
/quota                           → 404
/account/quota                   → 404
```

**Only way to see remaining credits:** https://home.qwencloud.com → Login → Individual tab → Credit Usage card.

## Manual reset is async — re-probe recipe

**Trap:** When the user clicks "Reset Usage Limit" on the portal, the very first chat probe may still return `insufficient_quota`. Don't declare the reset failed yet — the portal-to-backend propagation takes seconds, not minutes.

**Verification pattern (2026-08-07, proved by session):**

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

# 1. First probe right after click — may still be 429
curl -s -o /tmp/p.json -w "HTTP %{http_code}\n" --max-time 30 "$QWEN_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $QWEN_INDIVIDUAL_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3.8-max","messages":[{"role":"user","content":"OK"}],"max_tokens":5}'

# 2. Wait 2-5 seconds, re-probe
sleep 3 && curl ... # expect HTTP 200 now

# 3. Full sweep across 3 keys × 7 text models
for key_label in "QWEN_API_KEY|$QWEN_API_KEY" "QWEN_INDIVIDUAL_API_KEY|$QWEN_INDIVIDUAL_API_KEY" "QWEN_BAILIAN_KEY|$QWEN_BAILIAN_KEY"; do
  label="${key_label%%|*}"; key="${key_label#*|}"
  for model in qwen3.8-max qwen3.7-max qwen3.7-plus qwen3.6-flash deepseek-v4-pro glm-5.2; do
    code=$(curl -s -o /tmp/p.json -w "%{http_code}" --max-time 30 "$QWEN_BASE_URL/chat/completions" \
      -H "Authorization: Bearer $key" -H "Content-Type: application/json" \
      -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"OK\"}],\"max_tokens\":5}")
    [ "$code" = "200" ] && echo "✅ $label | $model" || echo "❌ $label | $model → $code"
  done
done
```

**Expected after reset:** all 3 keys × 7 text models = 21 ✅ lines.

**Image/TTS endpoints return 400/500 on chat endpoint — that's correct:**
- `wan2.7-image` → `/v1/images/generations` (not chat)
- `qwen-audio-3.0-tts-plus` → `/v1/audio/speech` (not chat)
- `wan2.7-image-pro`, `happyhorse-1.1-*` (video), `qwen-audio-3.0-realtime-plus` — same, different endpoints

## Federation usage patterns

**`/root/.hermes/model-picker.yaml` (2026-08-03 snapshot):**
- `qwen_token_plan_pro: 9` — 9 text models on Pro plan
- `qwen_token_plan_alive: 9` — 9 currently reachable
- `bailian_fallback: 20` — 20 Bailian fallback models
- `total_token_plan: 29` — total reachable via this plan

**Tier assignments (model-picker.yaml):**
| Tier | Primary | Fallback |
|---|---|---|
| bulk | qwen3.6-flash | deepseek-v4-flash → ollama |
| default | qwen3.7-plus | 7-entry cross-provider chain |
| heavy | deepseek-v4-pro | qwen3.8-max → ollama |
| apex | glm-5.2 | deepseek-v4-pro → ollama |

**Note:** When Qwen Token Plan is exhausted, federation must fall back to:
- DeepSeek direct (paid: $0.435/$0.87 per 1M)
- MiniMax (provider sub)
- OpenRouter
- Qwen Team plan
- Ollama local (qwen2.5-coder:3b) — blind survival

## `hermes-asi` cascade after Individual Pro reset

The LiteLLM cascade is in `/root/A-FORGE/litellm-config.yaml`. The `hermes-asi` alias already has Qwen Token Plan Individual Pro routes wired (orders 3 and 4) — they were already configured but couldn't serve while quota was at 0%.

```yaml
# MiMo SGP - fastest, primary
- model_name: hermes-asi
  litellm_params: { model: openai/mimo-v2.5, api_base: https://token-plan-sgp.xiaomimimo.com/v1, api_key: os.environ/MIMO_API_KEY, order: 1 }
# DeepSeek direct - cross-provider, same order as MiMo (parallel)
- model_name: hermes-asi
  litellm_params: { model: openai/deepseek-v4-flash, api_base: https://api.deepseek.com/v1, api_key: os.environ/DEEPSEEK_API_KEY, order: 1 }
# MiniMax M3 - cross-provider
- model_name: hermes-asi
  litellm_params: { model: openai/MiniMax-M3, api_base: https://api.minimax.io/v1, api_key: os.environ/MINIMAX_API_KEY, order: 2 }
# Qwen 3.8 Max via Individual Pro - CROSS-NETWORK via Alibaba Cloud Singapore
- model_name: hermes-asi
  litellm_params: { model: openai/qwen3.8-max, api_base: https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1, api_key: os.environ/QWEN_INDIVIDUAL_API_KEY, order: 3 }
# Qwen 3.7 Flash via Individual Pro - last Qwen route
- model_name: hermes-asi
  litellm_params: { model: openai/qwen3.7-flash, api_base: https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1, api_key: os.environ/QWEN_INDIVIDUAL_API_KEY, order: 4 }
```

**Confirm cascade is live by checking the resolved upstream:**

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s -o /tmp/h.json -w "HTTP %{http_code}\n" --max-time 40 http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H "Content-Type: application/json" \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"OK"}],"max_tokens":10}'

# Confirm it routed through Qwen Individual Pro:
cat /tmp/h.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('system_fingerprint',''))"
# Expected: fp_a18b46594c_prod0820_fp8_kvcache_20260402 (DashScope/Aliyun Qwen signature)
# If you see a different fingerprint, it routed via MiMo or DeepSeek instead.
```

**To force Individual Pro as PRIMARY** (not just fallback), bump `order: 0` on the Qwen entries and `systemctl restart litellm-federation`. Note: this can increase latency since Alibaba SGP is farther than Xiaomi SGP for some routing paths.

## Recovery procedure

When quota hits 0:

1. **Check portal** (https://home.qwencloud.com) — verify reset time and manual-reset count
2. **Option A:** Wait for calendar reset (visible on portal card)
3. **Option B:** Click "Reset Usage Limit" if 1+ available (instant after 2-5s propagation)
4. **Option C:** Add credit pack ($15 / 20K credits × 5 packs available per portal)
5. **Fallback routing:** If immediate inference is needed, route through fallback chain — but watch costs on paid alternatives

## Key rotation context

From `/root/AAA/federation/seats.yaml` (2026-08-01):
- Individual seat: `sk-sp-H.DIIYD.e****FaO4oIcIZUbnXlo` (preview only, full key in vault)
- Team seat: `sk-sp-D.IPRH` (legacy, rotated 2026-08-04 to `sk-sp-H.IEHM`)
- Rotation status: "OVERDUE — keys wired from vault, rotation pending Arif decision"

Vault: `/root/.secrets/kunci-mas.env` (mode 600, root-only)
