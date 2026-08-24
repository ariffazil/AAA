---
name: aaa-image-editing
version: 2.0.0-2026.08.13
owner: 333-AGI
risk_tier: T1
floor_scope: [F2, F4, F7]
autonomy_tier: T1
description: "Image editing vs generation — route the right model for the task. Covers identity-preserving edits, multi-model ensemble runs, endpoint fallback, and Gemini Nano Banana family best practices. Triggers when user provides a real photo and asks to edit/transform/place-in-scene."
required_tools: ['image_generate', 'vision_analyze']
tool_gate: strict
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# AAA Image Editing v2.0

The umbrella skill for image work that requires **editing a real photo** (identity
preservation) vs generating from scratch. These are fundamentally different tasks.

## CRITICAL DISTINCTION: Generation ≠ Editing

| | Generation | Editing |
|---|---|---|
| **Input** | Text prompt only | Reference image + edit prompt |
| **Output** | Imagined from scratch | Transformed from real photo |
| **Identity** | Generic/abstract | Must preserve subject identity |
| **Models** | MiniMax `image-01`, Qwen `qwen-image-2.0` | Gemini Nano Banana family, Qwen img2img |
| **Skill** | `minimax-image-gen` | This skill + `token-plan-image` |

**The #1 mistake** (corrected by F13 2026-08-12): using a generation model when the
user provided a real photo and wants to "place this person in a scene." The model
will fabricate a different person. Always classify first.

## The Nano Banana Family (verified live 2026-08-13)

Google's native image editing models, all accessible via our API key.
**All generated images include an invisible SynthID watermark.**

| Model | Nickname | Model ID | Best For | Resolution | Multi-person | Status |
|---|---|---|---|---|---|---|
| Nano Banana 2 Lite | NB2-Lite | `gemini-3.1-flash-lite-image` | High-volume, cheapest, fastest iteration | up to 2K | Limited | ✅ Available |
| Nano Banana 2 | NB2 | `gemini-3.1-flash-image` | Best all-rounder, multi-reference, good text | up to 4K | Up to 4 chars | ✅ Available |
| Nano Banana Pro | NB-Pro | `gemini-3-pro-image` | Hardest edits, legible text, 4K, brand consistency | up to 4K | Up to 5 chars | ✅ Available |
| Nano Banana (legacy) | NB | `gemini-2.5-flash-image` | Legacy workhorse, fast/cheap | up to 2K | Small sets | ⚠️ Legacy — migrate to NB2-Lite |

### Model Selection Decision Tree

```
User provides real photo + wants edit?
  ├─ Quick iteration (try 3-5 variants)? → NB2-Lite or NB (fastest, cheapest)
  ├─ Single edit, identity matters? → NB2 (best all-rounder)
  ├─ Hero asset, text in image, 4K needed? → NB-Pro
  └─ Ensemble (run multiple, pick best)? → NB + NB2 + NB-Pro in parallel

Text-only generation (no reference photo)?
  ├─ Fast/cheap? → NB2-Lite
  ├─ Best quality? → NB2
  └─ Complex composition? → NB-Pro
```

### Pricing (as of June 2026)

| Model | 1K | 2K | 4K |
|---|---|---|---|
| NB2-Lite | Lowest tier | Lowest tier | Lowest tier |
| NB (legacy) | Free tier | Free tier | N/A |
| NB-Pro | ~$0.039 | ~$0.134 | ~$0.24 |

## Endpoints and Auth (verified 2026-08-13)

### Gemini Nano Banana (ALL variants via same key)
- **Script:** `/root/HERMES/scripts/gemini-image.py`
- **Key:** `$GEMINI_API_KEY` from `/root/.secrets/kunci-mas.env`
- **API:** `https://generativelanguage.googleapis.com/v1beta`
- **Models:** `gemini-3.1-flash-lite-image`, `gemini-3.1-flash-image`, `gemini-3-pro-image`, `gemini-2.5-flash-image`
- **Semantic Mask:** `--semantic-mask "man's face, physique, pose"` — auto-prepends preservation clause
- **All 4 models confirmed HTTP 200 on 2026-08-13**

### Qwen Bailian PAYG (alternative for editing)
- **URL:** `https://ws-wlab8klalfojzq7i.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- **Key:** `$DASHSCOPE_API_KEY`
- **Model:** `wan2.7-image-pro`
- **Why PAYG:** Token Plan hits `Throttling.AllocationQuota` frequently.

## THE 6 IRON RULES OF GEMINI IMAGE EDITING

These are field-tested from production pipelines. Violate any one and the edit fails.

### Rule 1: Image First, Text Second (Parts Ordering)

In the API payload, **always put the image part BEFORE the text prompt**.
Flipping the order causes the model to treat text as primary request and
the image as a loose style reference → identity lost.

```python
# ✅ CORRECT
parts = [
    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}},  # image FIRST
    {"text": prompt}                                                  # text SECOND
]

# ❌ WRONG — text before image
parts = [
    {"text": prompt},
    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
]
```

### Rule 2: MIME Type Must Match Actual Bytes

If you label a JPEG as `image/png`, the decode step can silently drop the image.
Always detect MIME from file header, not extension.

```python
# ✅ Correct
mime = "image/png" if path.endswith(".png") else "image/jpeg"
# Even better: use python-magic or check first bytes
```

### Rule 3: Image Size Sweet Spot (1024–1568px longest side)

Images outside this range cause silent failures:
- **Too large** (e.g., 4K): API downscales, losing fine details → edit ignores reference
- **Too small** (≤128px): Model behaves as if no image was attached

**Fix:** Pre-resize before sending.

```python
from PIL import Image
img = Image.open(path).convert("RGB")  # Convert strips alpha channel!
longest = max(img.size)
if longest > 1568:
    ratio = 1568 / longest
    img = img.resize((int(img.size[0]*ratio), int(img.size[1]*ratio)))
```

### Rule 4: Strip Alpha Channels from PNGs

PNGs with alpha channels cause the model to repaint transparent regions with
new backgrounds → effectively rewrites the composition. Always convert to RGB.

```python
img = Image.open(path).convert("RGB")
```

### Rule 5: Stateless Iteration (Never Trust Multi-Turn)

**Multi-turn chat sessions are unreliable for image editing.** Google's own API
has documented intermittent 404s and `thought_signature` errors on turn 2+.

**Always re-attach the latest output image as fresh input each call.**

```python
# ✅ CORRECT — stateless, each call independent
result1 = edit(original_image, "add woman on left side")
result2 = edit(result1.image_bytes, "make her dress red")
result3 = edit(result2.image_bytes, "add warm lighting")

# ❌ WRONG — chat session, loses context after turn 2
session = create_chat_session()
session.send("add woman on left side")
session.send("make her dress red")  # may lose reference to original
```

### Rule 6: One Change Per Turn

Asking for multiple changes at once causes the model to "average" them → loss
of control over each individual edit.

```
# ✅ CORRECT — one change at a time
Turn 1: "Add a woman standing on his left side, wearing a black dress"
Turn 2: "Now make her hand rest on his chest"
Turn 3: "Add warm rim lighting to both subjects"

# ❌ WRONG — multiple changes
"Add a woman on his left in a black dress with her hand on his chest
and add warm rim lighting and change the background to dark blue"
```

## The Prompt Architecture

### The Preservation Clause (MOST IMPORTANT)

**Every edit prompt MUST explicitly state what to keep AND what to change.**
Without the keep-list, the model is free to redraw everything.

```
Using the provided image as the base, change only [WHAT TO CHANGE].
Keep [WHAT TO PRESERVE] exactly as shown in the original image.
Do not alter, regenerate, smooth, or modify those preserved elements.
```

### Identity Preservation Prompt Pattern

```
Place this man at [SCENE]. Keep his face and body exactly as shown.
Same [hair description], same [jawline/face description], same person.
[Scene details]. Photorealistic. No text.
```

**Key prompt rules:**
- Always start with "Place this man/woman" or "Using the provided image as the base"
- NEVER say "Transform into" or "Change to" — triggers generation mode, not edit mode
- Always include "Keep his face and body exactly as shown"
- Describe specific features: "same short spiky hair, same jawline"
- Specify scene details AFTER identity preservation clause
- End with "Photorealistic. No text."

### Semantic Mask Flag

The `gemini-image.py` script supports `--semantic-mask` for automatic
preservation clause injection:

```bash
python3 /root/HERMES/scripts/gemini-image.py \
  "Add a beautiful woman in black dress standing close to him" \
  --image /path/to/syed.jpg \
  --output /path/to/output.jpg \
  --model gemini-3.1-flash-image \
  --semantic-mask "man's face, muscular physique, pose, the single glowing white light tube, dark backdrop"
```

This auto-prepends:
> "Using the provided image, change only the elements described below.
> Keep man's face, muscular physique, pose, the single glowing white light tube, dark backdrop
> exactly as shown in the original image. Do not alter, regenerate, smooth, or modify
> those preserved elements in any way.
> Edit instruction: Add a beautiful woman in black dress standing close to him"

### Google's Official Prompt Best Practices (from dev blog, 2026-08-13)

1. **Be hyper-specific:** The more detail, the more control. Instead of "fantasy armor," describe: "ornate elven plate armor, etched with silver leaf patterns, with a high collar and pauldrons shaped like falcon wings."
2. **Provide context and intent:** Explain the purpose. "Create a logo for a high-end, minimalist skincare brand" > just "Create a logo."
3. **Fix character consistency drifts:** If features begin to drift after iterative edits, restart a fresh call with a detailed description rather than continuing the chain.
4. **Aspect ratio control:** When editing, model generally preserves input aspect ratio. If it doesn't, be explicit: "Do not change the input aspect ratio." For multi-image inputs, model adopts aspect ratio of the LAST image provided.
5. **Camera control language:** `wide-angle shot`, `macro shot`, `low-angle perspective`, `85mm portrait lens`, `Dutch angle`, `shallow depth of field`, `bokeh`.

### Common Failure Modes from Official Docs

- **Asking for many changes at once** → model averages them, lose control. One change per turn.
- **Not saying what to keep** → without explicit keep-list, model redraws everything. State the keep-list every time.
- **Expecting long in-image text on Flash models** → NB/NB2 warp logos/paragraphs. Use NB-Pro for legible text, or add text layer in external editor.
- **Not saving intermediates** → if iteration 7 is worse than 4, you want 4 still on disk. Download as you go.

### Federation Deployment Note (2026-08-13)

**This skill is profile-local** (`aaa-hermes/skills/media/aaa-image-editing/`).
It is NOT in `/root/AAA/skills/` (the shared federation directory). Other agents
(OpenClaw, OpenCode) cannot discover or use it.

**To promote to federation-wide:**
1. Copy or symlink to `/root/AAA/skills/aaa-image-editing/`
2. Ensure `gemini-image.py` script path is absolute (`/root/HERMES/scripts/gemini-image.py`)
3. Future architecture: expose via arifOS MCP as a governed tool (see
   `federated-skill-architecture` skill — Skill Execution Gateway pattern)

**RBAC consideration:** Image editing tools that call external APIs (Gemini, Qwen)
should be gated by agent identity + SCT verification at the MCP layer before
exposing the tool surface. Unrestricted access = blast radius risk (F1).

## Identity Preservation — Known Limits

### HARD RULE: Never Alter a Human's Face (F13 directive, 2026-08-12)
**User ruling:** "Hang jangan ubah muka manusia." When user provides a real photo
and asks to edit, the person's face, body, skin tone MUST survive 100%.

### Why Identity Preservation Is Technically Hard
All current image-edit models tend to generate "idealized bodybuilder templates"
when editing muscular subjects — overriding actual identity. The more muscular
the input, the stronger the pull toward generic output.

### Composite Workaround — What Failed (2026-08-12)

| Approach | Result | Failure Mode |
|---|---|---|
| rembg cutout + Pillow composite | "So fake. Dagu hilang." | Background removal crops chin/jawline |
| Gemini 3 Pro edit (img2img) | 6/10 realism | Regenerates face → different person |
| Gemini Flash edit | 6/10 realism | Best "stage feel" but face drifts |
| Qwen wan2.7 edit | 5/10 realism | Over-idealized, plastic skin |

**Best result achieved:** Gemini 2.5 Flash Image ("nano banana") — 5/10 identity,
6/10 realism. Best stage photo feel of all models tried.

### Honest Workflow for Identity-Critical Edits

1. Run ensemble: NB2 + NB-Pro + Qwen with strong identity prompts
2. Verify each with `vision_analyze` — flag if face differs
3. Present all to user with **honest realism ratings**
4. Let user pick — or acknowledge "ini semua edit, bukan you sebenar"

## Post-Generation Validation Checklist

Before delivering ANY edited image to user:

- [ ] **Face check:** Does the subject's face match the original? (use `vision_analyze`)
- [ ] **Body check:** Is the physique preserved? (not idealized/generic)
- [ ] **Prop count:** Are all original props present and correct count? (e.g., 1 light tube, not 2)
- [ ] **No extra objects:** Did the model hallucinate additional elements?
- [ ] **No skin smoothing:** Is skin texture preserved vs over-smoothed?
- [ ] **No text/watermarks:** Did "No text" instruction work?
- [ ] **Aspect ratio:** Does output match input aspect ratio?
- [ ] **Resolution:** Is output at expected resolution?

## Ensemble Editing (best results for identity-critical work)

When identity preservation matters, run multiple models in parallel:

1. Nano Banana 2 (`gemini-3.1-flash-image`) — best all-rounder
2. Nano Banana Pro (`gemini-3-pro-image`) — highest fidelity
3. Nano Banana legacy (`gemini-2.5-flash-image`) — proven stage photo feel

Dispatch each as a separate `terminal(background=true, notify_on_complete=true)`,
wait for all, then verify with `vision_analyze` and present all to user.

## Script Usage

```bash
# Basic edit
python3 /root/HERMES/scripts/gemini-image.py "Add woman on left" \
  --image /path/to/ref.jpg --output /path/to/out.jpg

# With semantic mask (recommended for identity preservation)
python3 /root/HERMES/scripts/gemini-image.py "Add woman on left" \
  --image /path/to/ref.jpg --output /path/to/out.jpg \
  --semantic-mask "man's face, physique, pose, light tube"

# Choose model
python3 /root/HERMES/scripts/gemini-image.py "prompt" \
  --model gemini-3.1-flash-image --image ref.jpg --output out.jpg
```

**Script features (v2.0):**
- Exponential backoff retry (3 attempts, 5s/10s/20s)
- Specific HTTP error handling (429 → retry, 400/403 → fail, 5xx → retry)
- Network error retry with backoff
- Semantic mask flag for automatic preservation clause
- Structured error output for programmatic handling

## Known Failure Modes & Triage Order

When an edit goes wrong, check in this fixed order:

1. **`responseModalities` includes IMAGE?** (80% of "only text returned" bugs)
2. **Parts ordered image-then-text?** (wrong order → model ignores reference)
3. **MIME type matches actual bytes?** (wrong MIME → silent drop)
4. **Image size 1024–1568px longest side?** (too big/small → silent failure)
5. **Prompt names what to preserve AND what to change?** (vague → redrawing)
6. **Stateless calls (not multi-turn chat)?** (chat sessions lose context after turn 2)
7. **Alpha channel stripped?** (PNG alpha → model repaints transparent regions)

## Endpoint Troubleshooting

| Error | Meaning | Fix |
|---|---|---|
| `Throttling.AllocationQuota` (Qwen) | Token Plan seat exhausted | Switch to Bailian PAYG |
| HTTP 429 (Gemini) | Rate limited | Wait for backoff, retry |
| HTTP 400 (Gemini) | Bad request / safety filter | Check prompt, check MIME type |
| HTTP 403 (Gemini) | Quota exhausted / key issue | Check API key, billing |
| HTTP 404 (model) | Model not on endpoint | Use correct model ID |
| `thought_signature` errors | Multi-turn state issue | Switch to stateless calls |
| Connection reset | Network/rate limiting | Wait 30s, retry |

## Open-Source Alternatives (not yet deployed)

| Model | Strength | Deployed? |
|---|---|---|
| `qwen-image-edit-2511` | Best identity preservation, character consistency | ❌ 404 on both endpoints |
| FLUX.2 [klein] 9B | Unified gen+edit, sub-second on consumer GPU | ❌ Not confirmed |
| FLUX.2 [dev] Turbo | 8-step distilled, speed-focused | ❌ Not confirmed |
| LongCat-Image-Edit | Bilingual CN/EN, preserves non-edited regions | ❌ Not confirmed |

## Session Reference
- `references/mrkl-2026-identity-preservation-session.md` — detailed MR KL 2026
  bodybuilder case (5 approaches, model comparison, "Hang jangan ubah muka manusia")
- `references/image-edit-models.md` — open-source model landscape
- `references/image-edit-deep-research-2026-08-13.md` — compiled research:
  semantic inpainting, identity-preservation prompt patterns, over-smoothing root cause
  (AAAI 2026), client-side compositing (arXiv:2608.02841), latent-space mask engineering,
  and Nano Banana model lineage

## Member Skills
- `minimax-image-gen` — generation only (image-01 via MCP :18100)
- `token-plan-image` — generation + basic editing (Qwen)
- This skill — editing with identity preservation + ensemble routing
