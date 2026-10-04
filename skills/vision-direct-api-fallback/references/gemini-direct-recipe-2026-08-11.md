# Gemini Direct Vision API — Proven Working Recipe (2026-08-11)

## Session: Sushi calorie counting via Telegram image

**Problem**: `vision_analyze` returned `400 invalid_parameter_error: Unexpected item type in content` because session was served by `qwen3.7-max` via `opencode-go` provider, which doesn't support image input despite provider declaring `vision` capability.

**Solution**: Direct Gemini API call via Python `urllib` with base64 image.

## Working Code

```python
import json, base64, os, urllib.request, ssl

img_path = "/usr/local/lib/hermes-agent/profiles/aaa-hermes/cache/images/img_a45cc9cd8e1b.jpg"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

api_key = os.environ["GEMINI_API_KEY"]
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [
            {"text": "Count every piece of sushi on the plate. List each: type (nigiri/maki/gunkan), fish/topping, size. Then calculate total estimated calories. Also note any sauces or garnishes. Keep it concise but complete. Write the response in Bahasa Melayu."},
            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
        ]
    }],
    "generationConfig": {"maxOutputTokens": 4096}
}

ctx = ssl.create_default_context()
req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req, context=ctx)
result = json.loads(resp.read())
text = result["candidates"][0]["content"]["parts"][0]["text"]
print(text)
```

## Result (actual output)

```
Terdapat 8 keping sushi kesemuanya di atas pinggan.

* Pinggan Merah (kiri): 2x Nigiri Tuna (Akami) + daun bawang & ikura
* Pinggan Merah (tengah): 1x Nigiri Udang (Ebi), 1x Nigiri Salmon (Sake)
* Pinggan Hitam (kanan): 4x Maki Negitoro (tuna cincang) nipis

Jumlah Keseluruhan Anggaran Kalori: 325 kalori
Sos dan Hiasan: Kicap soya (Sushiro brand) + penyepit.
```

## Why this worked and `curl` didn't

- Image was 151KB JPEG → ~200KB base64 after encoding
- `curl -d "$B64_STRING"` → `Argument list too long` (exceeds ARG_MAX ~128KB)
- Python `urllib.Request(data=...)` passes data through the request body, no shell limit
- Gemini native API accepts `inline_data` with base64 directly — no URL indirection needed

## opencode-go vision gap

The `opencode-go` provider (2026-08-11 config) declares `vision` in capabilities but:
- **Vision-capable models**: `kimi-k3`, `minimax-m3`
- **Text-only models**: `qwen3.7-max`, `deepseek-v4-pro`, `deepseek-v4-flash`, `glm-5.2`, `kimi-k2.7-code`, `mimo-v2.5-pro`, `minimax-m2.7`

When a text-only model serves the session, `vision_analyze` WILL fail. The fix was applied to config (added `vision` to capabilities) but the real fix is either routing to a vision model or using this direct API fallback.
