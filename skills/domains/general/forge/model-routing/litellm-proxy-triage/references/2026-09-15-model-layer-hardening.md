# 2026-09-15 — Model-layer hardening census (KVM8 `forge`)

Measured 2026-09-15 01:42–02:05 MYT. Method: tiny calls (`max_tokens 8`, `temperature 0`, `seed 8`),
**per-model nonce in the prompt to defeat the Redis response cache** (`namespace litellm-fed`, `ttl 1800`),
`curl -4`. Full report + scripts: `/root/forge_work/harden-20260915/model/`.

## Provider reachability (4 of 19 lanes live)

| Lane | Base (as configured) | Verdict | Body truth |
|---|---|---|---|
| Qwen TP team-owner / hermes / arifos | `token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | ❌ 429 | `insufficient_quota` — no reset given |
| Qwen TP individual | same | ⚠️ flap | 429 "1-week quota… resets 09-18 04:10 UTC" at 01:42 → **200** at 01:52 |
| DashScope PAYG / DashScope | `dashscope-intl.aliyuncs.com/compatible-mode/v1` | ❌ 403 | `AllocationQuota.FreeTierOnly` on **every** model — provider-wide |
| Z.ai coding (`ZAI_API_BASE`) | `api.z.ai/api/coding/paas/v4` | ❌ 429 | code `1310`, resets 2026-09-15 16:13 |
| Z.ai paas | `api.z.ai/api/paas/v4` | ❌ 429 | code `1113` insufficient balance |
| MiniMax | `api.minimax.io/v1` | ✅ 200 | M3 live; video `Hailuo-2.3` → `Success`; **H3 not entitled** (`400 code 2013`) |
| MiMo Token Plan | `token-plan-sgp.xiaomimimo.com/v1` | ✅ 200 | both keys OK; `/mimo/models` has `mimo-v2.5-asr/-tts/-tts-voiceclone` |
| DeepSeek | `api.deepseek.com/v1` | ✅ 200 | flash + v4-pro |
| Kimi | `api.kimi.com/coding/v1` | ❌ 403 | monthly quota. **`/v1` is an nginx-404 path trap** |
| OpenCode Go | `opencode.ai/zen/go/v1` | ❌ 429 | `GoUsageLimitError` weekly, ~6 days. **`/zen/v1` is a 401 path trap** |
| SEA-LION | `api.sea-lion.ai/v1` | ✅ 200 | returns `PONG.` |
| Gemini | `generativelanguage.googleapis.com` | ❌ 429 | **"prepayment credits are depleted" — payment, not rate** |
| Groq | `api.groq.com/openai/v1` | ❌ 404 | `llama-3.3-70b-versatile` not on the account |
| MuleRouter | — | ❌ | zero references in `litellm-config.yaml` |

## Endpoint surface

`127.0.0.1:4013` = KVM8 litellm, **45** ids (401 unauth; `/health/liveliness` 200 unauth).
`127.0.0.1:4000` = HAProxy `fed_gateway` → KVM4, **47** ids, md5 stable 6/6.
`127.0.0.1:4012` = HAProxy `fed_zen` → `127.0.0.1:4013`, **45** ids (identical md5).
`127.0.0.1:4000/health` → **HTTP 000 / 0 bytes** (heavy endpoint via HAProxy) — use `/health/liveliness`.
`100.64.0.5:4000` = KVM4, **401 without a key** → safe for caller-key tests.

## Two master keys, both live

`kunci-root.env`'s `LITELLM_MASTER_KEY` (**55** chars) and `/etc/haproxy/fed-auth.cfg`'s bearer
(**56** chars) are **different keys** and **both** authenticate against KVM4 and KVM8. Rotation hazard:
revoking one 401s whichever node still holds it.

## The dangling rung — live log signature

```
litellm.BadRequestError: You passed in model=qwen3.7-plus.
                        There are no healthy deployments for this model
No fallback model group found for lookup_groups=qwen3.7-plus.
```
`qwen3.7-plus` was not a registered `model_name` nor an alias, yet sat first in
`fallbacks['qwen3.6-plus']`. No config-time error. **Grep the router log for
`There are no healthy deployments` — it is the definitive detector of a dangling rung.**
The deploy mirror carried two more of an older generation (`forge-777`/`opencode → deepseek-v4-pro`).

## Recursive fallbacks

`fed/audio-asr` (two dead Gemini rungs) answered `200` from `qwen3.8-max` in **24.5 s** by walking into
`gemini-2.5-flash`'s own fallback list. **A lane's declared rungs are not its hop count.**
`gemini-3.6-flash` is the terminal node of **18** chains and escapes nowhere — yet the sealed contract
`/root/AAA/canon/FEDERATION_CONFIG_CONTRACT.v1.json` declares
`gemini_dormancy: DORMANT_IN_PLACE, parsed_active_count: 0`. Measured: **16 active, 18 references**.
`validate_litellm_config.py` fails on exactly this.

## Attribution caveat

The response `model` field is **not** a reliable attribution key — some lanes echo the model-group name
(`apex-888`, `hermes-asi`, `opencode`, `fed/sealion`). Trust: response `id` prefix (`chatcmpl-` = Qwen
token-plan, `<uuid>_<hex>` = Xiaomi), latency, and `docker logs litellm-federation`.

## Where the latency actually is

`i-arif`'s seven own deployments **all** failed; it answered from its **first fallback** (`deepseek-flash`).
Same for `agi-333`, `forge-777`. `glm-5.3` / `glm-5.2` / `qwen3.6-plus` took **17–46 s**, all landing on
`mimo-v2.5` — a single-deployment model now de-facto load-bearing for the federation. `kimi-k3` did not
answer inside the 60 s `request_timeout`.

## Quota ≠ auth ≠ payment (all arrive as 429/403)

`insufficient_quota` (window, auto-resets) · `resets at <ts>` (read the timestamp out of the body) ·
`AllocationQuota.FreeTierOnly` (billing action) · z.ai `1310` (plan, resets) vs `1113` (**balance gone,
same provider, different endpoint**) · Gemini `prepayment credits are depleted` (**payment wearing 429**)
· `access_terminated_error` (plan) · `GoUsageLimitError` (weekly) · `401 Model X is not supported` and
`404 nginx` (**path errors, not outages**) · `402 subscription` (lapsed, no auto-reset) ·
`400 code 2013` (plan tier excludes model).

## Repair receipts

- `/etc/haproxy/haproxy.cfg` — was `haproxy -c` **FATAL** (`'server' not allowed because frontend
  'fed_gateway' has no backend capability`); repaired to a valid config reproducing running reality;
  both bearer literals had been masked to a 14-char placeholder and were re-sourced from
  `/etc/haproxy/fed-auth.cfg`. **No reload performed.**
- `litellm-config.yaml` + `deploy/fed/litellm-config.yaml` — dangling rung removed, mirror synced
  (mirror had forked to 124 models vs 114). Not loaded — needs a restart.
- `FEDERATION_CONFIG_CONTRACT.v1.json` — 3 sha256 pins reconciled; validator now reports
  `[PASS] 3/3 SOT contract hash parity verified`.
- `/root/scripts/haproxy-auth-regen.sh` — hardened (all-bearer rewrite, tolerant regex,
  `haproxy -c` gate, dry-run default, key proven against both nodes before install).

## Re-runnable probes

`/root/forge_work/harden-20260915/model/probe-model-layer.sh` (litellm edge, cache-defeating nonce,
exits non-zero on any non-OK) and `probe-providers.sh` (direct upstream, classifies the body).
Probe `/health/liveliness`, never `/health`.
