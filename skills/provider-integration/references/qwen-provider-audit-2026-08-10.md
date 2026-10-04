# Qwen Token Plan vs DashScope PAYG — Audit (2026-08-10)

## Live Probe Results

### Token Plan Endpoint
- **URL:** `token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **Key:** `sk-sp-H.DIEXP...` (Individual) / `sk-sp-H.IEHM...` (Team)
- **Models (22):** deepseek-v3.2, deepseek-v4-flash, deepseek-v4-flash-0731, deepseek-v4-pro, glm-5, glm-5.1, glm-5.2, kimi-k2.5, kimi-k2.6, kimi-k2.7-code, qwen-audio-3.0-realtime-plus, qwen-audio-3.0-tts-plus, qwen-image-2.0, qwen-image-2.0-pro, qwen3.6-flash, qwen3.6-plus, qwen3.7-max, qwen3.7-plus, qwen3.8-max, wan2.7-image, wan2.7-image-pro
- **Image gen:** `/images/generations` returns 404 — endpoint NOT exposed
- **Vision:** No qwen-vl-max

### DashScope PAYG Endpoint
- **URL:** `ws-wlab8klalfojzq7i.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **Key:** `sk-ws-H.YLXYLM...`
- **Models (156):** All Token Plan models + qwen-vl-max, qwen-image-3.0-pro, qwen3.5-flash, qwen3-tts-*, qwen3-asr-*, qwq-plus, text-embedding-v3/v4, etc.
- **Image gen:** Works via chat completions with `qwen-image-3.0-pro` (modalities: ["text", "image"])
- **Vision:** qwen-vl-max available and verified working

### Native DashScope Endpoint
- **URL:** `dashscope.aliyuncs.com/compatible-mode/v1`
- **Status:** Returns `invalid_api_key` for PAYG keys — NOT USABLE with our keys

## Key Format Taxonomy

| Key Prefix | Type | Endpoint | Notes |
|---|---|---|---|
| `sk-sp-H.DI...` | Individual Token Plan | token-plan.ap-southeast-1 | User-specific, 5-hour rolling windows |
| `sk-sp-H.IE...` | Team Token Plan (Bailian) | token-plan.ap-southeast-1 | Team seat, shared Credits Pool |
| `sk-ws-H.YL...` | PAYG (DashScope) | ws-wlab8klalfojzq7i.ap-southeast-1 | Pay-as-you-go, 156 models |
| `sk-xxx` (standard) | ModelStudio Pay-As-You-Go | dashscope.aliyuncs.com | ❌ Throws 401 on Token Plan endpoints |

## Spec Hallucination Alert

Multiple integration specs claim `dashscope.aliyuncs.com/compatible-mode/v1` as the universal endpoint. This is WRONG for our setup. The actual endpoints are tenant-specific subdomains. Always verify with a live probe:

```bash
curl -s "https://<endpoint>/models" -H "Authorization: Bearer $KEY" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('data',[])))"
```

## Model Availability Matrix

| Model | Token Plan | PAYG | Role |
|---|---|---|---|
| qwen3.8-max | ✅ | ✅ | Flagship reasoning |
| qwen3.7-max | ✅ | ✅ | Fast execution |
| qwen3.5-turbo | ❌ | ❌ | DOES NOT EXIST |
| qwen3.5-flash | ❌ | ✅ | Fast runner (use this instead) |
| qwen-vl-max | ❌ | ✅ | Vision-language |
| qwen-image-3.0-pro | ❌ | ✅ | Image generation |
| wan2.7-image | ✅ | ✅ | Image generation (Alibaba Wan) |
| deepseek-v4-pro | ✅ | ✅ | Deep reasoning |
