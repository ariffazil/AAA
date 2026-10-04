# QwenCloud Token Plan — Individual Pro (Knowledge Bank)

> Source: https://docs.qwencloud.com/token-plan/personal/token-plan-personal-overview
> Probed: 2026-08-08 | Account: arifb*@gmail.com | Billing: $73.45 paid 2026-07-31

## Allowed models (EXACT string match — no variant inference)

| Model ID | Capability |
|---|---|
| `qwen3.8-max` | Reasoning, vision, text gen — **flagship** |
| `qwen3.7-max` | Reasoning, text gen |
| `qwen3.7-plus` | Reasoning, vision, text gen |
| `qwen3.6-flash` | Reasoning, vision, text gen |
| `deepseek-v4-pro` | Reasoning, text gen |
| `deepseek-v4-flash-0731` | Reasoning, text gen (Responses API not supported) |
| `glm-5.2` | Reasoning, text gen |
| `qwen-audio-3.0-tts-plus` | Speech synthesis |
| `qwen-audio-3.0-realtime-plus` | Realtime voice conversation |
| `wan2.7-image` | Image generation |
| `wan2.7-image-pro` | Image generation |

`qwen3.8-max-preview` auto-routes to `qwen3.8-max`. Rates apply as `qwen3.8-max`.

## Billing mechanism

- **Unified Credits** — single balance consumed by ALL models and harness tools.
- **Dual-window:** 5-hour rolling (currently unlimited, lifted for limited time) + 7-day fixed window.
- **Both windows active simultaneously** — hitting either pauses the service.
- **Tiered deduction coefficients by model** — video = huge credits per call; text = modest.
- **5hr limit is currently UNLIMITED** (limited-time lift). 7-day is the real constraint.
- **Unused 7-day quota does NOT carry over** to the next cycle.

## Plans (pricing, 2026-08-08)

| | Lite | Standard | Pro | Credit Pack |
|---|---|---|---|---|
| **Price** | ~~$8~~ → $6/mo | ~~$25~~ → $18/mo | ~~$80~~ → $68/mo | $15/pack (20K credits) |
| **5-hr limit** | Unlimited (promo) | Unlimited (promo) | Unlimited (promo) | Unlimited |
| **7-day limit** | 2,500 | 10,000 | **40,000** | +unlimited (stacks) |
| **Concurrency** | 1-2 | 3-4 | 6-8 | — |
| **Max credit packs** | — | — | — | 5 simultaneous |

Arif has: **Individual Pro** ($68/mo) + no Credit Pack purchased.

## qwen3.8-max limited-time promotions

1. **Night discount (22:00-08:00 UTC+8/MYT):** 50% off Credits on qwen3.8-max invocations.
2. **Preview → GA migration:** `qwen3.8-max-preview` redirects to `qwen3.8-max`; same rates.
3. **Credit Packs:** $15 per pack = 20,000 additional credits (stacks on top of window). Up to 5 concurrent packs.

## Harness tools (included, no extra cost)

`web_search` · `t2i_search` · `i2i_search` · `web_extractor` · `code_interpreter`

## Terms restrictions

1. **No API automation** — interactive agent use only (Claude Code, Cursor, OpenClaw, etc.). Automated scripts/backend/batch = subscription suspension risk.
2. **Singapore region, Global deployment** — cross-border data transfer.
3. **Personal use only** — sharing prohibited.
4. **One subscription per account** — can hold Individual + Team simultaneously.

## Quota reset

Use Reset Usage Limit benefit (if available) to clear 7-day quota instantly. Otherwise wait for the 7-day window to expire. Unused quota does not roll over.

## Relationship to Team plan

| | Individual Pro | Team Pro |
|---|---|---|
| Credits/7-day | 40,000 | 100,000 (per seat) |
| Seats | 1 | 3 (ariffazil + aliyun + arifOS) |
| 5-hr window | Unlimited (promo) | Unlimited (promo) |
| Current status | **LIVE (94.5%)** | **EXHAUSTED (0%)** |
| Reset | 2026-08-14 | 2026-09-01 |
| API key | `QWEN_INDIVIDUAL_API_KEY` | `QWEN_API_KEY` |
| Endpoint | Same SG endpoint | Same SG endpoint |
| LiteLLM order | 2-4 (fallback for all 6 aliases) | Not primary anymore |

Both keys hit the same endpoint (`token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`). Different quota pools. Individual key works when Team is 429.
