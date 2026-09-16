# Nano Banana 3.1 Flash — Gemini Interactions API (session log 2026-08-26)

## Why this lane exists

When Wan 2.7 image-edit hits `AllocationQuota.FreeTierOnly` 403 (Aug 2026) and Gemini 2.5-flash-image drifts the reference face, **Gemini 3.1 Flash Image** (`gemini-3.1-flash-image`) is the live lane that holds identity on a reference image. Use `client.interactions` (the steps-based endpoint), not `client.models.generate_content`.

## Endpoint

- Model: `gemini-3.1-flash-image` (also called "Nano Banana 2" workhorse). For highest fidelity use `gemini-3-pro-image`.
- Auth: `GEMINI_API_KEY` or `GOOGLE_API_KEY` in env.
- SDK: `google-genai` 2.8.0+ (verified 2026-08-26).
- Endpoint: `client.interactions.create(...)` (NOT `client.models.generate_content`).

## Reference image content block — exact schema

```python
{"type": "image", "data": "<base64>", "mime_type": "image/jpeg"}
```

NOT `{"type": "image", "source": {"type": "base64", "mime_type": ..., "data": ...}}` — that nested form was in some docs, the SDK rejects it with `400 Unknown parameter 'source'`.

`mime_type` accepted: `image/png | image/jpeg | image/webp | image/heic | image/heif | image/gif | image/bmp | image/tiff`.

## Input MUST be step_list

```python
input=[{"type": "user_input", "content": [...]}]
```

NOT `[{"role": "user", "content": [...]}]` (turn_list). SDK rejects: `400 'When using the steps-based API version, use step_list input format instead of turn_list'`.

## response_format — mime_type restricted

```python
response_format={"type": "image", "mime_type": "image/jpeg",
                 "aspect_ratio": "9:16", "image_size": "2K"}
```

`response_format.mime_type` only accepts `image/jpeg` — `image/png` 400s. The *output* image bytes come back as JPEG even if you request image/png output, so just save whatever you get.

`image_size` values: `512` (0.5K) / `1K` / `2K` / `4K`. Uppercase `K` mandatory.
`aspect_ratio` values: `1:1 | 1:4 | 1:8 | 2:3 | 3:2 | 3:4 | 4:1 | 4:3 | 4:5 | 5:4 | 8:1 | 9:16 | 16:9 | 21:9`.

## Working script (verified 2026-08-26)

```python
import base64, os, sys
from pathlib import Path
from google import genai

api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

REF = "/root/.hermes/cache/images/img_4b3ac64182bb.jpg"
OUT = "/root/.hermes/cache/images/abang_sado_nano_alpha.png"
PROMPT = "Transform this man into an alpha male bodybuilder..."

with open(REF, "rb") as f:
    ref_b64 = base64.b64encode(f.read()).decode()

interaction = client.interactions.create(
    model="gemini-3.1-flash-image",
    input=[{"type": "user_input", "content": [
        {"type": "image", "data": ref_b64, "mime_type": "image/jpeg"},
        {"type": "text", "text": PROMPT},
    ]}],
    response_format={"type": "image", "mime_type": "image/jpeg",
                     "aspect_ratio": "9:16", "image_size": "2K"},
)

img_data = None
if hasattr(interaction, "output_image") and interaction.output_image:
    img_data = interaction.output_image.data
elif hasattr(interaction, "outputs"):
    for o in interaction.outputs:
        if getattr(o, "type", None) == "image":
            img_data = o.data
            break

if not img_data:
    sys.exit("no image")

Path(OUT).parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "wb") as f:
    f.write(base64.b64decode(img_data) if isinstance(img_data, str) else img_data)
```

## Live errors hit this session (chronological)

| Error | Cause | Fix |
|---|---|---|
| `GEMINI_API_KEY not set` | subprocess env empty | `set -a && source /root/.secrets/kunci-root.env && set +a` before running (5-R Protocol). |
| `mime_type 'image/png' not supported for response_format.mime_type` | API rejects png for output | Use `image/jpeg`. |
| `Unknown parameter 'source' at input[0].content[0]` | nested source object form | Flatten to top-level `data` + `mime_type`. |
| `'steps-based API version, use step_list input format'` | `role: user` turn_list | Use `[{"type": "user_input", ...}]`. |

## Face-lock result vs Gemini 2.5-flash-image

Same reference image, same prompt:

- `gemini-2.5-flash-image` (legacy NB, used via `gemini-image.py`): face drifted to generic SEA face. Pose, low angle, arms crossed landed. Physique OK. Face ≠ reference. **Fail identity-lock floor.**
- `gemini-3.1-flash-image` (Nano Banana 2 via `client.interactions`): face matched reference. Smirk landed. Physique, sweat, veins, dark gym all correct. **Pass.**

Rule: identity-preserving I2I/edit → 3.1 Flash. Quick T2I without reference → 2.5 Flash is fine.

## Capabilities not exercised this session

- `image_search` / `web_search` grounding via `tools=[{"type": "google_search"}]`.
- Up to 14 reference images (10 objects + 4 characters) for multi-subject / character sheet workflows.
- `previous_interaction_id` for stateful multi-turn editing / inpainting.
- `thinking_level: minimal | high` on 3.1 Flash.
- Pro model `gemini-3-pro-image` for text rendering + 3 style references.

## Quota / cost notes

No quota hit in this session. Expect per-image billing on DashScope-style payg. Don't loop on 429s — exponential backoff in script (already in `gemini-image.py`'s `_request` helper).
