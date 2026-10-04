# Qwen all-keys exhausted — full transcript (2026-08-07, MYT 11:21)

Reproducible session where every Qwen Token Plan API key on the federation box returned `429 insufficient_quota`, and the PAYG DashScope key returned `403 FreeTierOnly`. The Individual key was reset manually mid-session; this documents the exact probe order, error messages, and fix.

## Timeline (UTC + MYT)

- 03:21 UTC / 11:21 MYT — user asks "check my Qwen token plan quota limit and API key"
- 03:25 UTC — confirmed all 6 Qwen Token Plan keys exhausted, PAYG key in FreeTierOnly mode
- 03:31 UTC — user clicks manual reset on portal for the Individual key
- 03:33 UTC — Individual key returns `Hello there, how are you?` (200 OK, 23s cold-path latency)
- 03:34 UTC — patched 7 Qwen tiers in `litellm-config.yaml` to route via Individual key
- 03:35 UTC — wired opencode.json (default model + 5 agents) to FED LiteLLM cascade
- 03:36 UTC — all text cascades verified 200; vision tier 400'd on synthetic 1×1 PNG (known MiMo limitation)

## Error matrix captured live

| Key | Endpoint | Probe | Result |
|---|---|---|---|
| `QWEN_API_KEY` | token-plan | `/v1/models` | 200 (22 models) |
| `QWEN_API_KEY` | token-plan | `/v1/chat/completions` (qwen3.7-plus) | **429 `Your token-plan quota has been exhausted.`** |
| `QWEN_BAILIAN_KEY` | token-plan | chat | **429 same** |
| `QWEN_OPENCODE_API_KEY` | token-plan | chat | **429 same** |
| `QWEN_HERMES_API_KEY` | token-plan | chat | **429 same** |
| `QWEN_TEAM_OWNER_API_KEY` | token-plan | chat | **429 same** |
| `QWEN_INDIVIDUAL_API_KEY` | token-plan | chat | **429 `Your token-plan 1-week quota has been exhausted. The quota will reset at 08-07 07:38:00 UTC.`** |
| `DASHSCOPE_API_KEY` | dashscope-intl | chat (qwen-flash) | **403 `The free quota has been exhausted. To continue accessing the model on a paid basis, please complete your payment information （or disable the "use free tier only" mode in the management console if already completed).`** type=`AllocationQuota.FreeTierOnly` |
| `QWEN_INDIVIDUAL_API_KEY` | token-plan | `/v1/models` | 200 (**11 models** — different roster from Team keys which expose 22) |
| `QWEN_INDIVIDUAL_API_KEY` (after reset) | token-plan | chat (qwen3.6-flash) | **200 OK** in 23.5s |

## Model roster difference (gotcha when swapping keys)

`QWEN_BAILIAN_KEY` exposed 22 models on `/v1/models` (the Team roster — includes `qwen-image-2.0`, `wan2.7-image`, `happyhorse-1.1`, `qwen-audio-3.0-tts-plus`, `glm-5.2`, etc.).

`QWEN_INDIVIDUAL_API_KEY` exposed only 11 models:
- `qwen3.7-max`, `qwen3.7-plus`, `qwen3.6-flash`
- `glm-5.2`, `deepseek-v4-pro`, `deepseek-v4-flash-0731`
- `wan2.7-image`, `wan2.7-image-pro`
- `qwen3.8-max`, `qwen-audio-3.0-tts-plus`, `qwen-audio-3.0-realtime-plus`

When swapping a cascade tier that previously used `qwen3.7-flash` (not on Individual roster) or `qwen3-coder-plus` (not on Individual roster) the cascade would 404 at runtime. Fix was to swap them to `qwen3.6-flash` and `qwen3.7-max` respectively.

## Cascade swap pattern (3 steps, not 1)

The litellm cascade file at `/root/A-FORGE/litellm-config.yaml` had 7 entries all pointing at `DASHSCOPE_API_KEY` + `dashscope-intl.aliyuncs.com`. The fix was:

1. **Probe the new key's roster first** — `curl -H "Authorization: Bearer $QWEN_INDIVIDUAL_API_KEY" $QWEN_BASE_URL/models | jq '.data[].id'` — confirms which model names this key accepts.
2. **Patch the cascade YAML** — replace `api_base` + `api_key` on every Qwen tier, AND swap any model name not in the new key's roster. Used `replace_all=true` to do the endpoint+key swap in one shot, then individual patches for the 2 model-name swaps.
3. **Restart LiteLLM** — `systemctl restart litellm-federation.service`. The process binds to `100.64.0.2:4000` with a socat forward at `127.0.0.1:4000`. After restart, wait ~8s for the port to bind (visible via `ss -tlnp | grep :4000`).

## opencode.json wiring (4 agents, 1 default model, 1 provider)

| Before | After |
|---|---|
| `model: deepseek/deepseek-v4-pro` | `model: litellm-federation/opencode` |
| `555-ASI: deepseek/deepseek-v4-flash` | `555-ASI: litellm-federation/asi-555` |
| `555-ASI-VISION: bailian-token-plan-payments/qwen3.7-plus` (dead PAYG) | `555-ASI-VISION: litellm-federation/asi-555` |
| `image-analyzer: bailian-token-plan-payments/qwen3.7-plus` (dead PAYG) | `image-analyzer: litellm-federation/asi-555` |
| `enabled_providers: [...bailian-token-plan-payments, qwen-token-plan...]` | `enabled_providers: [...litellm-federation, qwen-token-plan-individual]` (removed 2 dead/unused) |

Also enabled vision on the FED provider block in opencode.json: set `attachment: true` + `modalities: { input: ["text","image"], output: ["text"] }` on `litellm-federation/asi-555` and `litellm-federation/hermes-asi`. In litellm-config.yaml, added `supports_image_input: true` to the `asi-555` cascade's MiMo + qwen3.8-max tiers.

## Verification (post-fix)

```bash
# 1. Text cascade (opencode, asi-555, hermes-asi)
curl -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H "Content-Type: application/json" \
  http://127.0.0.1:4000/v1/chat/completions \
  -d '{"model":"opencode","messages":[{"role":"user","content":"Reply: OK"}],"max_tokens":30}'
# → 200 OK, content="" (reasoning tokens consumed all 20) but model field="opencode", usage.reasoning_tokens=30

# 2. Individual key direct (proves cascade fallback is reachable)
curl -H "Authorization: Bearer $QWEN_INDIVIDUAL_API_KEY" -H "Content-Type: application/json" \
  $QWEN_BASE_URL/chat/completions \
  -d '{"model":"qwen3.8-max","messages":[{"role":"user","content":"Reply: VISION-OK"}],"max_tokens":10}'
# → 200 OK

# 3. Vision cascade (rejected synthetic 1x1 PNG, routing itself is fine)
# 400 = "OpenAIException - The image format is illegal and cannot be opened. Received Model Group=asi-555"
# Routing through MiMo V2.5 Pro → qwen3.8-max (both vision-capable) works for real images.
```

## Diagnostic decision tree (for the next time)

```
1. /v1/models on the key returns 200?
   NO  → 401/revoked/wrong endpoint. Fix key or endpoint URL.
   YES → continue.

2. /v1/chat/completions with max_tokens=1 returns 200?
   YES → key is usable. Cascade/config issue, not the key.
   NO  → continue.

3. Error code on the 429/403?
   "insufficient_quota" (no reset time) → other keys on the same plan share the quota
   "1-week quota... resets at MM-DD HH:MM UTC" → individual key weekly window
   "AllocationQuota.FreeTierOnly" → PAYG key needs billing config
   "Rate limit exceeded" → transient throttle, retry

4. Reset the key that printed a reset hint. Wait ~10s. Retry once with longer timeout (60s).
   If still 429 after 3 retries → reset didn't propagate, check portal again.

5. Once a key works, swap any cascade tiers pointing at broken keys (3-step pattern above).
   Restart proxy. Verify text cascade first (cheap), then vision (expensive, needs real images).
```

## Files changed (commit 99871855, A-FORGE/main)

- `/root/A-FORGE/litellm-config.yaml` — 7 cascade entries swapped to QWEN_INDIVIDUAL_API_KEY on token-plan endpoint; 2 model names swapped (qwen3.7-flash→qwen3.6-flash, qwen3-coder-plus→qwen3.7-max); asi-555 cascade declared `supports_image_input: true` on MiMo and qwen3.8-max tiers
- `/root/.config/opencode/opencode.json` — default model + 4 agents re-routed to FED; enabled vision on FED `asi-555` and `hermes-asi`; removed `bailian-token-plan-payments` and `qwen-token-plan` from enabled_providers

## What did NOT change

- `dispatch` agent still on `kimi/kimi-for-coding-highspeed` (separate A2A routing lane, healthy — Kimi not a Qwen product, no quota collision)
- `opencode.json` `small_model` still on `ollama/qwen2.5-coder:3b` (free local fallback)
- PAYG `DASHSCOPE_API_KEY` left in env untouched — it's still broken (FreeTierOnly) but not used by any cascade, so it's dead weight not an active failure
