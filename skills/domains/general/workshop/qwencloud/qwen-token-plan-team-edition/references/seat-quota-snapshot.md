# Qwen Token Plan Seat Quota Snapshots

> **Append-only.** Each entry is a probed-at-moment snapshot, never overwritten. Future agents append, never rewrite history.

## 2026-08-18 01:24 UTC (probed during shadow session)

Probe command:
```bash
set -a && source /root/.secrets/kunci-root.env && set +a
for label in "OWNER:QWEN_BAILIAN_KEY" "INDIVIDUAL:QWEN_INDIVIDUAL_API_KEY" "ARIFOS:QWEN_API_KEY" "HERMES:QWEN_HERMES_API_KEY"; do
  var="${label##*:}"
  key="${!var}"
  curl -s -m 8 -H "Authorization: Bearer $key" -H "Content-Type: application/json" \
    -d '{"model":"qwen3.7-plus","messages":[{"role":"user","content":"ping"}],"max_tokens":3}' \
    "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
    -w "\n[$label] HTTP=%{http_code}\n"
done
```

| Seat | env key | HTTP | Body code | Verdict |
|---|---|---|---|---|
| OWNER aliyun | `QWEN_BAILIAN_KEY` = `QWEN_TEAM_OWNER_API_KEY` | 200 | success | ✅ LIVE (chat only) |
| INDIVIDUAL Pro | `QWEN_INDIVIDUAL_API_KEY` | 429 | `quota exhausted, resets 21 Aug 03:30 UTC` | ⚠️ WEEKLY quota drained |
| arifOS Admin | `QWEN_API_KEY` | 429 | `quota exhausted` | ❌ DEAD (0/100000 used) |
| ariffazil Admin | `QWEN_HERMES_API_KEY` | 429 | `quota exhausted` | ❌ DEAD (0/25000 used) |

Image gen probe (same session, 01:26 UTC):
```bash
curl -s -m 10 -H "Authorization: Bearer $QWEN_BAILIAN_KEY" -H "Content-Type: application/json" \
  -d '{"model":"wan2.7-image-pro","prompt":"test","size":"1024x1024","n":1}' \
  "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/images/generations"
# Result: HTTP 404 — even OWNER seat blocks /images/generations endpoint
# Use /api/v1/services/aigc/multimodal-generation/generation instead (proven working on Individual)
```

Vision LLM probe (same session, 01:25 UTC):
- `qwen-vl-max` on all 4 seats → HTTP 404 `{"code":"model_not_found"}` — model dead across all seats
- `qwen3-vl-plus` not in any seat's `/models` listing as of 2026-08-18
- Workaround: use `qwen3.8-max` multimodal chat model with `attachment: true` for image inputs

## 2026-08-18 15:27 UTC (image gen session — CORRECTION)

**Critical correction to 01:24 probe:** The Owner seat (`QWEN_BAILIAN_KEY`) **CAN** generate images. The 01:24 probe tested the wrong endpoint (`/compatible-mode/v1/images/generations`) which returns 404 on ALL seats — it's not a valid API path. The correct endpoint is `/api/v1/services/aigc/multimodal-generation/generation`.

Probe (successful):
```bash
source /root/.secrets/kunci-root.env
curl -s -X POST "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $QWEN_BAILIAN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"wan2.7-image-pro","input":{"messages":[{"role":"user","content":[{"text":"test"}]}]},"parameters":{"size":"1024*1024","n":1}}'
# Result: HTTP 200, image URL returned, downloaded successfully (1.87MB PNG, 1024x1024)
```

| Seat | env key | Image gen (multimodal-generation endpoint) | Model tested | Credits remaining |
|---|---|---|---|---|
| OWNER aliyun | `QWEN_BAILIAN_KEY` | ✅ LIVE | `wan2.7-image-pro` | ~15,902 (from dashboard) |
| INDIVIDUAL | `QWEN_INDIVIDUAL_API_KEY` | ⚠️ 429 weekly quota | N/A | exhausted, resets 21 Aug 03:30 UTC |

**Lesson:** `/compatible-mode/v1/images/generations` is a dead endpoint (OpenAI-compatible path that Qwen doesn't actually serve). Always use `/api/v1/services/aigc/multimodal-generation/generation` for image gen. The 404 on the OpenAI-compatible path does NOT mean the seat lacks image gen capability.

Available multimodal models on Owner seat (as of 2026-08-18):
- `wan2.7-image` (lighter, faster)
- `wan2.7-image-pro` (higher quality, slower)
- `qwen-image-2.0`
- `qwen-image-2.0-pro`
- `qwen-audio-3.0-realtime-plus`
- `qwen-audio-3.0-tts-plus`
