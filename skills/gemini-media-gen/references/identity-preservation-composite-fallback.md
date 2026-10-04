# Identity Preservation — Composite Fallback

**Discovered:** 2026-08-12
**Trigger:** User asked to edit real photo of named bodybuilder "Syed" into MR KL 2026 backstage scene. **"Hang jangan ubah muka manusia."**

## The Problem

All current image-to-image edit models regenerate the subject's face, producing an idealized "template" version. Tested models:

| Model | Endpoint | Face preserved? | Notes |
|---|---|---|---|
| Qwen wan2.7-image-pro | Bailian PAYG | ❌ No | Muscle template, idealized |
| Gemini 3 Pro Image | gemini-3-pro-image | ❌ No | Mirror geometry wrong, face generic |
| Gemini 2.5 Flash Image ("nano banana") | gemini-2.5-flash-image | ⚠️ Best effort | Closest to original but still regenerates |
| Qwen-Image-Edit-2511 | Bailian PAYG | ❌ Not available | 404 "Model not exist" |

**Pattern observed:** Model interprets "keep the same" as "generate a similar-looking person in that context." This is fundamental AI image-to-image behavior, not a prompt-engineering fixable issue. The model cannot pixel-preserve a face while transforming surroundings.

**Output tells:** Mirror geometry inconsistent, hand anatomy fused, skin texture unrealistically smooth, "wow factors" added to muscles that weren't in the source.

**User verdict on edit results:** "So fake" → edit models inadequate for named real person at this time.

## Edit Model Prompt Template (best effort)

```
"Place this man at [LOCATION]. Keep his face and body EXACTLY as shown.
Same short spiky hair, same jawline, same expression, same person.
[Setting description]. He wears [outfit]. Photorealistic. No text."
```

Be **specific** about features to preserve: hair texture, jawline, skin tone, expression.

## The Composite Fallback

When facial identity MUST be preserved:

### Step 1: Cutout subject (0% pixel alteration)

```bash
pip install --break-system-packages rembg
python3 -c "
from rembg import remove; from PIL import Image
img = Image.open('ref.jpg')
remove(img).save('ref_nobg.png')
"
```

- Output: PNG with RGBA (transparent background)
- Subject pixels unchanged — only background removed
- Auto-downloads u2net.onnx model (~176MB) on first run

### Step 2: Generate empty background

```bash
python3 /root/HERMES/scripts/gemini-image.py \
  "Empty backstage pumping room. Concrete walls, warm tungsten pendant lights, dumbbell rack. No people. No text. Cinematic warm lighting." \
  --output bg.jpg --model gemini-2.5-flash-image
```

**Critical:** Prompt must contain "no people" or "empty" — otherwise model generates a person and we'll have two people on the composite.

### Step 3: PIL composite

```python
from PIL import Image, ImageFilter

syed = Image.open("ref_nobg.png").convert("RGBA")
bg = Image.open("bg.jpg").convert("RGBA")

# Crop to tight bounding box (remove transparent edges)
syed = syed.crop(syed.getbbox())

# Scale: target height ~75% of background
target_h = int(bg.height * 0.75)
syed = syed.resize((int(target_h * syed.width / syed.height), target_h), Image.LANCZOS)

# Position: center horizontally, near bottom (standing on floor)
x = (bg.width - syed.width) // 2
y = bg.height - syed.height - int(bg.height * 0.02)

# Paste using alpha as mask
result = bg.copy()
result.paste(syed, (x, y), syed)

# Optional: add subtle shadow under figure
shadow = Image.new("RGBA", result.size, (0, 0, 0, 0))
sw, sh = int(syed.width * 0.7), int(syed.height * 0.05)
sl = Image.new("RGBA", (sw, sh), (0, 0, 0, 80))
shadow.paste(sl, (x + (syed.width - sw)//2, y + syed.height - sh//2))
shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
result = Image.alpha_composite(result, shadow)

result.convert("RGB").save("final.jpg", quality=95)
```

## ⚠️ Known Composite Failure (verified 2026-08-12)

**rembg U2Net clips into jawline/chin for side-lit portraits.** When a person
is lit from the side (strong shadow contrast on jawline), rembg treats the
shadow edge as background and cuts into the face. Result: "dagu hilang" —
chin/jawline disappears, person looks like they have a different face shape.

**Symptoms:** vision_analyze shows "facial structure different", jawline
appears "rounded off" or "truncated", person looks "softer" than original.

**Root cause:** U2Net segmentation model threshold — shadow regions on skin
are misclassified as background. This is model-inherent, not fixable via
prompt.

**Workaround:** When compositing side-lit portraits:
1. Pre-process with higher threshold: use `alpha_matting=True` in rembg
2. Or: crop the person more tightly (avoid shadow jawline area)
3. Or: accept composite as-is with "approximate identity" label

**Decision:**
| Scenario | Use composite? |
|---|---|
| Front-lit photo (even lighting) | ✅ Yes — clean cutout |
| Side-lit photo (strong jaw shadow) | ⚠️ Test first, verify jawline |
| Face is CRITICAL (portrait, ID photo) | ❌ No — use edit model, accept identity is approximate |
| Face is secondary (full-body, crowd) | ✅ Yes — small enough that clipping is invisible |

## Session-Specific Verification

After the session, user verified all 3 composites:
- V1 (backstage pumping room) — jawline clipped, "So fake"
- V2 (competition stage) — jawline clipped
- V3 (backstage trophy) — jawline clipped

All rejected. Edit models were tried as alternative, also rejected.
**Final status:** No satisfactory output produced for this session.
The limitation is fundamental to 2026-era image models, not an agent error.

## Approach Decision Tree

```
User asks to "place this person in scene X"
    │
    ├─ Face identity is CRITICAL (named real person, friend, family)
    │   │
    │   ├─ Try edit model first (gemini-2.5-flash-image / "nano banana")
    │   │  with explicit preservation prompt
    │   │  If face regenerated → FALLBACK below
    │   │
    │   └─ Composite fallback (rembg cutout + empty bg + PIL paste)
    │      ⚠️ WARNING: rembg may clip into jawline for side-lit portraits
    │      Verify with vision_analyze before delivery.
    │      If jawline disappears → report BLOCKED, do not ship
    │
    └─ Identity is NORMAL (generic person, illustration, artistic)
        Use edit model directly
```

## Model Routing (credentials)

| Model | Key | Endpoint | Notes |
|---|---|---|---|
| Gemini 3 Pro / Flash | `GEMINI_API_KEY` | `generativelanguage.googleapis.com` | Edit + generation |
| Qwen wan2.7-image-pro | `DASHSCOPE_API_KEY` | `ws-wlab8klalfojzq7i...maas.aliyuncs.com` | Edit (best effort) |
| Qwen (Token Plan) | `QWEN_API_KEY` | `token-plan.ap-southeast-1...maas.aliyuncs.com` | Generation only, quota unreliable |
| MiniMax image-01 | `MINIMAX_API_KEY` | `127.0.0.1:18100` MCP | Generation only, NOT edit |

## Limitations

- Cutout quality depends on `rembg` u2net model — fine details (wispy hair, transparent edges) may be slightly clipped
- **Side-lit portraits:** jawline/chin clips (see Known Failure above)
- Compositing produces "pasted" look if lighting/color temperatures don't match between subject and background
- For perfect lighting match, post-process with PIL `ImageEnhance` (brightness, contrast, color balance)
