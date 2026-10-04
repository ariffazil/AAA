# ComfyUI API Workflow Patterns (RunPod, verified 2026-08-10)

## LoadImage node — on-disk files

When the image is already on disk in `/workspace/ComfyUI/input/`, reference by filename only. **Do NOT include the `upload` field** — that triggers multipart form upload mode and causes 400 errors.

```json
{"1": {"inputs": {"image": "my_image.png"}, "class_type": "LoadImage"}}
```

**Wrong (causes 400):**
```json
{"1": {"inputs": {"image": "my_image.png", "upload": "image"}, "class_type": "LoadImage"}}
```

## LoadImageMask — requires `channel` parameter

`LoadImageMask` always requires a `channel` field. Without it:
```
"required_input_missing", "input_name": "channel"
```

Valid channels: `"red"`, `"green"`, `"blue"`, `"alpha"`. For black-and-white masks, use `"red"`.

```json
{"2": {"inputs": {"image": "mask.png", "channel": "red"}, "class_type": "LoadImageMask"}}
```

## VAEEncodeForInpaint — multi-subject composition

SDXL has a **single-subject attention bias** — cross-attention maps bleed multi-subject prompts into a single dominant figure. To enforce spatial hierarchy:

### Technique: Inpainting mask pass

1. Generate the hero figure as a full image (V2)
2. Create a mask (bottom 30% white, rest black) for the secondary subject
3. Run inpainting with denoise 0.40-0.50 on the masked region

**Workflow nodes:**
```
LoadImage (base) -> VAEEncodeForInpaint (with mask) -> KSampler (denoise 0.45) -> VAEDecode -> SaveImage
LoadImageMask (mask, channel=red) ↗
CheckpointLoaderSimple ↗
CLIPTextEncode (positive/negative) ↗
```

**Key parameters:**
- `denoise`: 0.40-0.50 (preserves hero, regenerates worshipper region)
- `grow_mask_by`: 8 (feather edge to avoid hard seams)
- `cfg`: 7.0
- `sampler`: dpmpp_2m + karras (sharper than euler_ancestral)

**Mask creation (Python):**
```python
from PIL import Image
w, h = 896, 1152
mask = Image.new("L", (w, h), 0)  # black = keep
for y in range(int(h * 0.70), h):  # bottom 30% = inpaint
    for x in range(w):
        mask.putpixel((x, y), 255)  # white = regenerate
mask.save("worshipper_mask.png")
```

## ComfyUI API endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/system_stats` | GET | Health check, VRAM |
| `/prompt` | POST | Queue workflow |
| `/history/{prompt_id}` | GET | Completion status + output filenames |
| `/queue` | GET | Queue status |
| `/object_info` | GET | All available nodes + input specs |
| `/object_info/{node}` | GET | Specific node spec |
| `/view?filename={name}&subfolder={dir}&type=output` | GET | Download generated image |

**RunPod proxy:** `https://{pod-id}-8188.proxy.runpod.net`

**ComfyUI 0.31.0 verified nodes:** VAEEncodeForInpaint, LoadImageMask, InpaintModelConditioning, ControlNetInpaintingAliMamaApply

## Render time benchmarks (RTX 4090)

| Checkpoint | Resolution | Steps | Sampler | Time |
|---|---|---|---|---|
| RealVisXL V4.0 | 896x1152 | 25 | dpmpp_2m karras | ~18s |
| RealVisXL V4.0 | 896x1152 | 30 | euler_ancestral karras | ~20s |
| Inpainting (same) | 896x1152 | 25 | dpmpp_2m karras | ~15s |
