## Quick-start — Qwen Image Edit (Bailian Singapore)

**Model:** `qwen-image-edit-max-2026-01-16`
**Key:** `BAILIAN_PAYG_API_KEY` (= `DASHSCOPE_API_KEY`, starts with `sk-ws-*`)
  - ⚠️ NOT `QWEN_API_KEY` (sk-sp-*, Token Plan) — that key returns 401 on image-edit
**Endpoint:** `POST https://{workspace}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
  - From `BAILIAN_PAYG_BASE_URL`: workspace = first segment before `.ap-southeast-1`
  - Full example: `https://ws-wlab8klalfojzq7i.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
  - **NOT** the `/compatible-mode/v1/chat/completions` endpoint — that returns empty content

### Call pattern
```python
import os, subprocess, base64, requests, json

# Load keys with bash expansion (BAILIAN_PAYG_API_KEY is set to ${DASHSCOPE_API_KEY})
result = subprocess.run(
    ["bash", "-c", "source /root/.secrets/kunci-mas.env && env | grep BAILIAN_PAYG_API_KEY"],
    capture_output=True, text=True, check=True
)
KEY = result.stdout.strip().split("=", 1)[1]
BASE = "https://ws-wlab8klalfojzq7i.ap-southeast-1.maas.aliyuncs.com"
ENDPOINT = f"{BASE}/api/v1/services/aigc/multimodal-generation/generation"

# Base64 encode source image
with open("source.png", "rb") as f:
    data_uri = f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"

# Call
r = requests.post(ENDPOINT, headers={
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json"
}, json={
    "model": "qwen-image-edit-max-2026-01-16",
    "input": {"messages": [{"role": "user", "content": [
        {"image": data_uri},
        {"text": "Your edit prompt here"}
    ]}]},
    "parameters": {"n": 1, "watermark": False}
}, timeout=300)

resp = r.json()
# Response: output.choices[0].message.content = [{"image": "https://...oss...png?Expires=..."}]
```

### Response format
```json
{
  "output": {
    "choices": [{
      "finish_reason": "stop",
      "message": {
        "content": [{"image": "https://dashscope-*.oss-ap-southeast-1.aliyuncs.com/...png?Expires=...&Signature=..."}],
        "role": "assistant"
      }
    }]
  },
  "usage": {"height": 768, "image_count": 1, "width": 1376},
  "request_id": "..."
}
```
The OSS URL is pre-signed and expires (~7 days). Download immediately.

### Model variants
| Model | Description |
|---|---|
| qwen-image-edit-max-2026-01-16 | Strongest for design/geometry/character consistency. Max resolution 2048×2048. |
| qwen-image-edit-plus-2025-12-15 | Plus series, multi-image input, customizable resolution. |
| qwen-image-2.0-pro | Pro: text rendering + editing (same endpoint, same key). |

### Pricing
Billable per image output. Check Qwen Token Plan portal for current rates.

### Gotcha: empty content on wrong endpoint
Using `/compatible-mode/v1/chat/completions` returns `{"choices":[{"message":{"role":"assistant"}}]}` with empty content — the API key is valid but the model won't produce images via the chat endpoint. Must use the dedicated multimodal-generation endpoint.

### Gotcha: BAILIAN_PAYG_BASE_URL includes /compatible-mode/v1 (verified 2026-08-09)
The env var `BAILIAN_PAYG_BASE_URL` is set to `https://ws-wlab8klalfojzq7i.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`. Using this directly as the base URL for the image edit endpoint returns **HTTP 404** — the `/compatible-mode/v1` suffix must be stripped:
```python
# WRONG — returns 404:
ENDPOINT = f"{os.environ['BAILIAN_PAYG_BASE_URL']}/api/v1/services/aigc/multimodal-generation/generation"

# CORRECT — strip the /compatible-mode/v1 suffix:
base = os.environ["BAILIAN_PAYG_BASE_URL"].replace("/compatible-mode/v1", "")
ENDPOINT = f"{base}/api/v1/services/aigc/multimodal-generation/generation"
```

### Gotcha: multi-image content array order matters
For multi-image edit (identity merge), the FIRST image is treated as the primary identity source. Put the face/identity image first, body reference second, prompt text last. The model interprets positionally, not by label.
