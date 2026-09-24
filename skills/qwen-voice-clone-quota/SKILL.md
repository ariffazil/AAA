---
name: qwen-voice-clone-quota
description: Use when picking a Qwen voice-clone target_model.
type: reference
---

# Qwen Voice Cloning — Quota Reference (Sept 2026)

## Sources

- Live probe: `GET https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models` (Authorization Bearer) → 172 models, 39 voice-capable.
- Pricing page: `https://www.alibabacloud.com/help/en/model-studio/model-pricing` (last updated 2026-09-11).
- Provider docs: https://dashscope-intl.aliyuncs.com

## Region caveat

Free quota applies only to Singapore international scope. Mainland China deployment (`dashscope.aliyuncs.com`, China Beijing) has its own pricing and generally no overlapping free grant.

## Free quota (Singapore international, Sept 2026)

### Voice enrollment (one-time per voice)

| Enrollment model | Free voices | Paid rate |
|---|---|---|
| `qwen-voice-enrollment` | **1,000 voices / account** | $0.01 / voice |
| `qwen-voice-design` (CosyVoice) | **10 voices / account** | $0.20 / voice |

### TTS synthesis with cloned voice

| Synthesis model | Free quota | Paid rate |
|---|---|---|
| `qwen-audio-3.0-tts-flash` | 10,000 chars | $0.15 / 10k chars |
| `qwen-audio-3.0-tts-plus` | 10,000 chars | $0.20 / 10k chars |
| `cosyvoice-v3-flash` | 10,000 chars | $0.13 / 10k chars |
| `cosyvoice-v3-plus` | 10,000 chars | $0.26 / 10k chars |
| `qwen3-tts-flash` / `qwen3-tts-flash-2025-11-27` | **110,000 chars** | $0.10 / 10k chars |
| `qwen3-tts-vc-2026-01-22` | **110,000 chars** | $0.115 / 10k chars |
| `qwen3-tts-instruct-flash` | 10,000 chars | $0.115 / 10k chars |

### Omni realtime (voice-to-voice)

| Model | Free quota | Paid rate |
|---|---|---|
| `qwen3-omni-flash-realtime` / dated variants | **1,000,000 tokens** (any modality) | $0.43/M text in, $3.81/M audio out |
| `qwen3.5-omni-flash-realtime` | (rolling) | same tier |
| `qwen3.5-omni-plus-realtime` | (rolling) | higher tier |

Quota expires **90 days** from Model Studio activation, model release, or app approval (whichever is later).

## Practical sizing

- 10,000 chars ≈ 3 minutes of natural speech → a 90-day free window of TTS-flash ≈ 3 short narrations total. Use `qwen3-tts-flash` (110k chars) when bulk narration is the goal.
- Omni-realtime audio tokens are billed ~4x text tokens → 1M free tokens ≈ 10–15 min of spoken output, depending on silence ratio.
- Voice-design at 10 voices / account is the binding constraint for CosyVoice identity work — pick the names carefully because re-creating consumes quota.

## Checking remaining balance

No working REST endpoint as of Sept 2026:

- `GET /api/v1/dashscope/quota` → 404
- `GET /api/v1/account/balance` → 404
- `POST /api/v1/services/audio/tts/account/quota` → "InvalidParameter: Request method 'GET' is not supported"

Programmatic signal that DOES exist:

```bash
curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"voice-enrollment","input":{"action":"list_voice","page_index":0,"page_size":10}}'
# → returns "usage": {"count": N} — counts API calls, NOT remaining chars/tokens
```

The full inventory endpoint:

```bash
curl -G https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
# returns paginated list with "data": [{id, object, created, owned_by}, ...]
```

For an actual remaining balance the user must check the DashScope console. Do not claim an API number when one is not available.

## Picking a target_model at enrollment time

1. **Decide use class first** — voice-to-voice realtime → Omni realtime; batch high-quality → CosyVoice; bulk cheap TTS → qwen3-tts-flash or qwen-audio-3.0-tts-flash.
2. **Probe inventory** with `/compatible-mode/v1/models` to confirm the exact model id is still listed — model IDs rotate (e.g. `qwen3-tts-flash` ↔ `qwen3-tts-flash-2025-11-27`); the dated variant is what free quota binds to.
3. **Check voice_id format returned by `list_voice`** — `<target_model>-<prefix>-<hash32>`. If the prefix starts with the wrong target_model, the prior enrollment was for a different model and reuse will fail.
4. **Allocate CosyVoice quota sparingly** — 10 voices / account is the binding ceiling for the CosyVoice identity pipeline.

## Voice_id decoding

Provider returns the handle with target_model literally embedded in the id:

```
cosyvoice-v3-plus-iarif2026-fc37c2ff31f04ebaa17d5a63a0fdd1b1
└──target──┘ └──prefix──┘ └────hash32────────────────────────┘
```

Use `voice_id.split('-')[0:3]` (joined back) to read the binding for any audit/receipt — no need to query the API again.

## Enumeration verbs

The customization endpoint accepts these input actions (verified Sept 2026):

| Action | Behaviour |
|---|---|
| `create` (with `qwen-voice-enrollment`) | Creates Omni/Qwen-TTS voice, returns `output.voice` |
| `create_voice` (with `voice-enrollment`) | Creates CosyVoice / Qwen-Audio-TTS voice, returns `output.voice` |
| `list_voice` | Returns `output.voice_list[]` + `output.page_index/page_size/total_count` + `usage.count` |
| `list` | **Invalid** — returns `InvalidParameter: invalid action` |
| `query` / `delete` | Not verified; provider docs vary by region |

Do NOT try `list`. Use `list_voice`.