---
name: vision-direct-api-fallback
description: When Hermes vision_analyze fails (provider declares vision but active model rejects image input), call a vision-capable API directly via Python. Covers Gemini direct API, curl ARG_MAX pitfall, and model-level vs provider-level vision capability.
tags: [vision, image, fallback, gemini, multimodal, workaround]
triggers:
  - vision_analyze fails
  - invalid_parameter_error image
  - Unexpected item type in content
  - image analysis error
  - provider vision but model rejects
  - vision module broken
source: hermes
synthesized: 2026-08-11
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Vision Direct API Fallback

When `vision_analyze` fails because the active model doesn't support image input, call a known-vision provider directly via Python.

## When This Applies

`vision_analyze` returns one of:
- `400 invalid_parameter_error: Unexpected item type in content`
- `Unexpected item type in content`
- Any 400/404 where the provider declares `vision` but the specific model rejects `image_url`

**Root cause**: Provider-level `capabilities: [vision]` in Hermes config is a blanket declaration — NOT every model within that provider supports image input. Example: `opencode-go` declares vision, but `qwen3.7-max` and `deepseek-v4-pro` are text-only. Only `kimi-k3` and `minimax-m3` within opencode-go accept images.

## The Fix: Gemini Direct API

**Always use Python `urllib`, NOT `curl`.** Base64-encoded images produce payloads >100KB which exceed shell `ARG_MAX` (~128KB). `curl -d "$HUGE_STRING"` fails with `Argument list too long`. Python passes data through `Request` object, no shell limit.

```python
import json, base64, os, urllib.request, ssl

img_path = "/path/to/image.jpg"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

api_key = os.environ["GEMINI_API_KEY"]
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [
        {"text": "Describe this image in detail"},
        {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
    ]}],
    "generationConfig": {"maxOutputTokens": 4096}
}

ctx = ssl.create_default_context()
req = urllib.request.Request(url, data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req, context=ctx)
result = json.loads(resp.read())
print(result["candidates"][0]["content"]["parts"][0]["text"])
```

**Prerequisite**: `source /root/.secrets/kunci-mas.env` before running, or use `subprocess.run` to source it from Python.

## Known Vision-Capable Providers (always have image support)

| Provider | API | Env var | Notes |
|---|---|---|---|
| **Gemini** | `generativelanguage.googleapis.com/v1beta` | `GEMINI_API_KEY` | Most reliable — native base64 inline, generous free tier |
| Qwen Token Plan | `token-plan.ap-southeast-1.maas.aliyuncs.com` | `QWEN_INDIVIDUAL_API_KEY` | `qwen-vl-max` or `qwen3.7-plus` only |
| MiniMax | `api.minimax.io/v1` | `MINIMAX_API_KEY` | M3 supports vision |

## Diagnosis Pattern

1. `vision_analyze` fails → check which model is serving the session
2. If model is text-only (qwen3.7-max, deepseek-v4-pro/flash, etc.) → use direct fallback
3. If model IS vision-capable but still fails → check provider routing (see `hermes-gateway-image-routing` skill)

## Pitfalls

- **Do NOT retry `vision_analyze`** — the model hasn't changed, retry will fail the same way
- **Do NOT use `curl`** for base64 images — ARG_MAX will kill it for any image >~90KB
- **Source secrets first** — `GEMINI_API_KEY` lives in kunci-mas.env, not in shell env by default
- **Gemini quota**: ~5-10 rapid calls before 429. RPD has daily limit. For batch work, space calls.
- **Model selection**: `gemini-2.5-flash` is fast + free tier. Use `gemini-3.1-pro` for detailed analysis if quota allows.
