# Gemini Image Generation via REST (Interactions API)

Updated: 2026-08-13

## Why this exists
- Legacy Imagen endpoints like `models/imagen-4.0-generate-001:predict` and `models/imagen-3.0-generate-002:predict` now return 404 or are restricted for new users.
- The current, reliable path is the native Gemini Interactions route using `generateContent` with `responseModalities=["IMAGE"]` and `imageConfig`.

## Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent
Header: x-goog-api-key: $GEMINI_API_KEY
Header: Content-Type: application/json
```

## Minimal cURL (save output)

```bash
GEMINI_API_KEY=... # from /root/.secrets/kunci-mas.env
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Photorealistic portrait of a muscular Southeast Asian man in a tight black singlet, lifting the hem to reveal a thick, well-defined chest, taking a cool vape puff. Cinematic moody lighting, shallow DOF, 85mm lens bokeh. Tasteful, non‑explicit."}]
    }],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {"aspectRatio": "3:4", "imageSize": "1K"}
    }
  }' \
| jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' \
| base64 --decode > gemini_image.png
```

## Python (requests)

```python
import os, json, base64, requests
api_key = os.environ["GEMINI_API_KEY"]
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent"
body = {
  "contents": [{"parts": [{"text": "Cinematic portrait..."}]}],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {"aspectRatio": "3:4", "imageSize": "1K"}
  }
}
resp = requests.post(url, headers={
    "x-goog-api-key": api_key,
    "Content-Type": "application/json"
}, json=body, timeout=120)
resp.raise_for_status()
parts = resp.json()["candidates"][0]["content"]["parts"]
img_b64 = next(p["inlineData"]["data"] for p in parts if "inlineData" in p)
with open("out.jpg", "wb") as f:
    f.write(base64.b64decode(img_b64))
```

## Supported knobs
- `imageConfig.aspectRatio`: `1:1`, `3:4`, `4:3`, `16:9`, `9:16`
- `imageConfig.imageSize`: `512`, `1K`, `2K`, `4K` (availability varies by model)

## Pitfalls (2026-08-13)
- 404 `models/imagen-*-generate-*:predict`: legacy Imagen routes are shut down or restricted. Use the Interactions route above.
- The returned image data lives in `candidates[0].content.parts[].inlineData.data` (base64). There is no file URL.
- Content filters: keep prompts cinematic/dramatic/suggestive; avoid explicit sexual content. Frame as scene, not erotica.
- Rate limits: bursts of 6–8 calls can trigger 429; back off 10–20 minutes.

## When to use Pro
For higher fidelity and text rendering, prefer `gemini-3-pro-image-preview` (higher cost). Same JSON shape; switch the model name.
