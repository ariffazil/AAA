# Qwen PAYG Image Generation — Endpoint Reference

## Two Endpoint Paths (confirmed 2026-08-20)

Keys are **NOT interchangeable**. Each key type only works on its own endpoint.

| Key type | Prefix | Endpoint | Env var |
|----------|--------|----------|---------|
| **Token Plan** | `sk-sp-H.*` | `token-plan.ap-southeast-1.maas.aliyuncs.com` | `$QWEN_BAILIAN_KEY` |
| **PAYG** | `sk-ws-H.*` | `dashscope-intl.aliyuncs.com` | `$QWEN_PAYG_API_KEY` or `$DASHSCOPE_API_KEY` |

### Common Error: InvalidApiKey across endpoints

- Token Plan key on dashscope endpoint → `InvalidApiKey` (NOT expired — wrong endpoint)
- PAYG key on token-plan endpoint → `InvalidApiKey` (NOT expired — wrong endpoint)
- `Throttling.AllocationQuota` on token-plan → Token Plan credits exhausted (top up or use PAYG)

## PAYG Image Generation API

**Endpoint:** `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

```bash
source /root/.secrets/kunci-mas.env
curl -s -X POST "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $QWEN_PAYG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wan2.7-image-pro",
    "input": {
      "messages": [
        { "role": "user", "content": [ { "text": "your prompt here" } ] }
      ]
    },
    "parameters": { "size": "1280*1920", "n": 1 }
  }'
```

### Response shape
```json
{
  "output": {
    "choices": [{
      "message": {
        "content": [{ "image": "https://signed-url.png", "type": "image" }]
      }
    }]
  },
  "usage": { "image_count": 1, "total_tokens": 102 }
}
```

## Available Image Models on PAYG

| Model | Name | Notes |
|-------|------|-------|
| `wan2.7-image-pro` | Wan 2.7 Image Pro | Best quality, ~30s, 1280×1920 |
| `wan2.7-image` | Wan 2.7 Image | Faster, lighter |
| `qwen-image-3.0-pro` | Qwen Image 3.0 Pro | Newest generation |
| `qwen-image-3.0` | Qwen Image 3.0 | Newest, fast |
| `qwen-image-2.0-pro` | Qwen Image 2.0 Pro | Solid, proven |
| `qwen-image-2.0` | Qwen Image 2.0 | Fastest |

## Size presets
- `"1024*1024"`, `"1280*1280"`, `"720*1280"`, `"1280*1920"`
- `"1K"` (~1024×1024), `"2K"` (~2048×2048)

## Quota
- PAYG billing: per-image cost deducted from balance
- Check dashboard: https://modelstudio.console.alibabacloud.com
- Token Plan quota is SEPARATE from PAYG quota
