# Vision Bypass — Direct Gemini API via Python

> **Forged:** 2026-08-11
> **Workaround for:** `vision_analyze` failing on session model that lacks vision support (e.g., `qwen3.7-max` via `opencode-go`)

---

## Symptom

`vision_analyze` tool returns:

```
Error code: 400 - invalid_parameter_error
"Unexpected item type in content."
```

Or some other upstream rejection of the `image_url` content part. Even though the provider (`opencode-go`) has been patched to declare `vision` capability, the underlying `qwen3.7-max` model does not accept image content parts at its API.

---

## Root cause (verified 2026-08-11)

Two layers must both declare vision support:

| Layer | Check |
|---|---|
| Provider config | `HERMES/config.yaml` — provider `opencode-go` lists `vision` capability ✅ |
| Model runtime | `qwen3.7-max` API gateway — accepts text ONLY ❌ |

The provider layer is configurable, but the model API endpoint itself is what rejects. Adding more capability declarations won't help when the model API returns 400 on `image_url` content parts. Some Qwen-via-third-party gateways route the call but the model itself has no multimodal weights loaded.

---

## Reality-first workaround

When `vision_analyze` fails and you genuinely need image analysis (food photos for calorie counting, doc/screenshot OCR, badge verification, etc.), call Gemini directly via Python stdlib.

### Why Python, not shell?

`base64` image data routinely exceeds 100KB. Linux `curl` rejects arg lists > ~128KB with `Argument list too long`. Python's urllib handles big payloads natively.

### Recipe (verbatim, copy/run)

```python
import json, base64, os, urllib.request, ssl

img_path = "/path/to/cached/image.jpg"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

api_key = os.environ["GEMINI_API_KEY"]  # source /root/.secrets/kunci-mas.env first
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [
            {"text": "<your prompt — what to look for / extract / count>"},
            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
        ]
    }],
    "generationConfig": {"maxOutputTokens": 4096}
}

ctx = ssl.create_default_context()
req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                             headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req, context=ctx)
print(json.loads(resp.read())["candidates"][0]["content"]["parts"][0]["text"])
```

Source keys FIRST:
```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
python3 << 'PYEOF'
... recipe above ...
PYEOF
```

### Why `gemini-2.5-flash`?

- Free tier via `GEMINI_API_KEY` (already provisioned in kunci-mas.env)
- Supports `inline_data` image parts via native REST (not OpenAI-compat)
- 1M context window allows huge `inline_data` payloads
- Faster than `gemini-pro`, accurate enough for counting/identification tasks
- For higher-accuracy tasks (medical imaging, fine OCR), use `gemini-2.5-pro` instead

### Other supported formats

For non-JPEG images, change `mime_type`:
- `image/png`
- `image/webp`
- `image/heic`
- `image/gif` (first frame)

---

## Configuration fix (preference-layer, not just workaround)

Patched `HERMES/config.yaml` (2026-08-11) to add `vision` to `opencode-go` capabilities:

```yaml
opencode-go:
  capabilities:
    - chat
    - function_calling
    - reasoning
    - vision        # added
```

This doesn't fix the Qwen 3.7 Max rejection (model API is independent of capability declarations), but it signals to the routing layer that the provider COULD do vision when paired with a vision-capable model like `kimi-k3`, `minimax-m3`, or `mimo-v2.5-pro` (all of which the `opencode-go` provider lists).

To USE vision with `opencode-go`: switch model to a vision-capable one (`kimi-k3`, `MiniMax-M3`) for vision-heavy tasks. For text-only work, `qwen3.7-max` is still preferred (reasoning speed).

---

## Pitfalls

- **`browser_vision` can hallucinate content** in long pages. Saw this happen on a 28KB meal-plan page: first vision call reported "mie instan" overflowing on every card, but a second vision pass + curl content check confirmed layout was clean. Always pair with a sanity check before declaring visual regression.
- **Image too large for Gemini inline_data.** Max inline payload ~20MB (base64-encoded). For larger, upload to GCS first or use Files API. Most Telegram images are < 5MB.
- **Image orientation.** JPEG EXIF orientation isn't respected by Gemini in inline mode. Rotate via `convert input.jpg -auto-orient output.jpg` (ImageMagick) before encoding if camera images look wrong.
- **Don't put keys in chat or VAULT999.** Always `source /root/.secrets/kunci-mas.env` before the python block. Audit `/root/.secrets/INDEX.md` if keys are missing.

---

## When NOT to use this workaround

- When `vision_analyze` works fine (don't waste tokens bypassing it)
- For public/web images where you have the URL — prefer `web_extract` (zero cost)
- For batch processing (>50 images) — use Gemini Files API or Vertex AI batch
- For privacy-sensitive content where Gemini shouldn't see it — use local model (Ollama, qwen-vl) instead
