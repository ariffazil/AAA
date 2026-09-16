# LoRA Stacking & Model Ecosystem Guide (2026)

Covers LoRA selection, weight ranges, trigger tokens, architecture compatibility, face consistency toolchains, and recommended stacks for SDXL, Pony, Illustrious, Flux, and SD 1.5.

## Architecture Compatibility Rules

1. **Pony ≠ SDXL ≠ Illustrious** — LoRAs load across branches without error but produce garbage output. Always match architecture tags on the model card.
2. **CLIP skip:** Pony derivatives = 2, vanilla SDXL = 1, Flux = N/A. Wrong skip = plastic skin.
3. **CFG ranges:** Pony 3.5–5.0, SDXL 5–7, Flux 3.5–4.0 (guidance-based).
4. **Total combined LoRA weight:** Keep under 2.0. Example proven stack: Detail Tweaker (0.7) + Skin Realism (0.5) + Lighting (0.4) = 1.6.
5. **Max concurrent LoRAs:** 1–3 at once. More risks style collapse.
6. **Pony prompt system:** Uses `score_` prefix tags: `score_9, score_8_up, score_7_up`.

## NSFW Unlock / Base LoRAs (Load FIRST)

### SDXL / Pony / Illustrious
| LoRA | Architecture | Trigger | Weight | CivitAI |
|------|-------------|---------|--------|---------|
| NSFW POV All In One SDXL | SDXL 1.0 | Per-pose: BLOWJOB, COWGIRL, POV, MISSIONARY (19 categories) | 0.6 (full 1.8GB) / 0.8–1.0 (mini 74MB) | civitai.com/models/245888 |
| Pony Diffusion V6 XL | Pony V6 XL | score_ prefix system | Base checkpoint | civitai.com/models/257749 |
| WAI-Nsfw-Illustrious-17 | Illustrious XL | N/A (checkpoint) | Base checkpoint | civitai.com/models/827184 |

### Flux.1 Dev
| LoRA | Trigger | Weight | Downloads |
|------|---------|--------|-----------|
| aidmaNSFWunlock | `aidmaNSFWunlock` | 0.5–1.0 (start 0.8) | 130k+ |
| Nude Style V2 | No trigger (tokens `nsfw`, `nude` help) | ~1.0 | 130k+ |
| Fluxed Up 7.1 | N/A (checkpoint) | N/A | 95.9k favs, 8.3M gens |

**Flux stack order:** checkpoint → aidmaNSFWunlock (0.8) → Nude Style V2 (1.0) → Detail enhancer (0.5–1.0)

## Aesthetic / Quality LoRAs

| LoRA | Arch | Weight | CivitAI |
|------|------|--------|---------|
| Detail Tweaker XL | SDXL 1.0 | -3 to +3 (bidirectional; typical 0.5–1.0) | civitai.com/models/122359 |
| Detail Tweaker | SD 1.5 | 0.5–1.0 | civitai.com/models/58390 |
| Add More Details XL | SDXL | 0.6–0.9 | civitai.com |
| Skin Realism (Acne/Details/Imperfections) | SDXL | 0.5 (1.0 distorts anatomy) | civitai.com/models/248951 |
| Realistic Skin Texture ZBase v2.1 | SDXL+Flux+Pony+Illustrious+SD1.5 | 0.4–0.7 | civitai.com/models/580857 |
| Real Skin Slider | Pony | 0.3–0.7 | civitai.com/models/1486921 |
| Sweat LoRA | Pony/SDXL | 0.4–0.7 | civitai.com/models/608351 |
| Realistic Photos Detailed Skin&Textures Flux V3 | Flux.1 Dev | 0.5–0.8 | civitai.com/models/1173967 |
| Detail Enhancer FLUX V1 | Flux.1 Dev | 0.5–1.0 | CivitAI |

**Proven portrait stack:** Detail Tweaker XL (0.7) + Skin Realism (0.5) + Lighting LoRA (0.4)

## Face Consistency Toolchain

### Comparison (2026)

| Method | Arch | Fidelity | Diversity | VRAM | Best For |
|--------|------|----------|-----------|------|----------|
| IP-Adapter FaceID v2 | SDXL | 80–90% | Medium | ~2GB extra | General face lock |
| InstantID | SDXL ONLY | 90–95% | Lower (frontal bias) | ~3GB extra | Studio portraits |
| PuLID | SDXL | 85–95% | Highest | ~2GB extra | Diverse poses/styles |
| PuLID Flux | Flux.1 Dev | 90–95% | High | ~2GB extra | Best Flux-native face lock |

### IP-Adapter FaceID v2 (SDXL)
- Model: `ip-adapter-faceid-plusv2_sdxl` (187cb962)
- IP-Adapter weight: **0.70–0.80**; Companion LoRA weight: **0.55–0.65**
- Sampler: DPM++ 2M SDE Karras, 30–35 steps, CFG 5–6
- Requires: InsightFace `antelopev2` model
- Source: HuggingFace `h94/IP-Adapter-FaceID`

### InstantID (SDXL only)
- Main model: `ip-adapter.bin` from HuggingFace `InstantX/InstantID`
- Face analysis: InsightFace `antelopev2` → `ComfyUI/models/insightface/models/antelopev2/`
- IP-Adapter weight: **0.6–0.8**; ControlNet weight: **0.5–0.7**
- ComfyUI node: `cubiq/ComfyUI_InstantID`
- Limitation: biased toward frontal portraits

### PuLID (SDXL)
- Model: `ComfyUI/models/pulid/`
- Fidelity parameter: lower = higher resemblance to reference
- Source: `cubiq/PuLID_ComfyUI`
- Best for: diverse outputs (close-ups, wide shots, anime, different lighting)

### PuLID Flux
- Weight: **0.8–0.95** (PuLID 0.9.0); **0.9–1.0** (PuLID 0.9.1)
- Source: HuggingFace `guozinan/PuLID` or `Fayens/Pulid-Flux2`
- ComfyUI nodes: `balazik/ComfyUI-PuLID-Flux` or `sipie800/ComfyUI-PuLID-Flux-Enhanced`
- **Best Flux face lock as of 2026**

### Recommended Face Consistency Stack (80–95% consistency)
1. IP-Adapter FaceID (0.75) — face lock
2. ControlNet OpenPose (0.4) — pose/body lock
3. ADetailer — face refinement in inpaint pass
4. For Flux: PuLID Flux (0.85–0.95) instead of IP-Adapter

## ControlNet for Body/Pose (Not LoRAs, but essential)

| Model | Arch | Weight | Source |
|-------|------|--------|--------|
| ControlNet OpenPose SDXL | SDXL 1.0 | 0.35–0.55 | HuggingFace `xinsir/controlnet-openpose-sdxl-1.0` |
| ControlNet Depth | SDXL/SD1.5 | 0.35–0.55 | HuggingFace |
| DWPose (preprocessor) | All | N/A | ComfyUI nodes |

Stack OpenPose + Depth for best anatomy control.

## Hand/Foot Fix

- **ControlNet OpenPose `full`** preprocessor: extracts body + hands + face joints simultaneously
- **ADetailer**: automatic hand/face inpainting post-process
- **Negative embeddings** (SD 1.5): BadHandsV4, negative_hand in negative prompt
- Flux models generally handle hands better than SDXL/SD1.5

## Negative Embeddings

### SD 1.5
| Embedding | Purpose |
|-----------|---------|
| EasyNegative | All-rounder quality boost |
| BadHandsV4 | Hand correction |
| negative_hand | Hand quality skeleton |
| BadPrompt | General quality |
| FastNegativeEmbedding | Speed + quality |

### SDXL
- Ultimate Text Embeddings SDXL Pack (CivitAI models/148131)
- SDXL needs fewer negative prompts; some models perform worse with long lists
- Use ClipG/ClipL splitting for more control

### Flux
- Flux does NOT benefit from traditional negative embeddings
- Use natural language negative guidance in prompt itself

## Download Sources
- **CivitAI** (civitai.com) — largest LoRA/embedding library, account required
- **HuggingFace** (huggingface.co) — face consistency models, ControlNet, uncensored checkpoints
- **HuggingFace checkpoint catalog** — see `references/hf-uncensored-checkpoints.md` for verified direct-download URLs for SDXL/Flux NSFW checkpoints (no token required)
- **Tensor.Art** (tensor.art) — mirrors + originals
- **GitHub** — ComfyUI custom nodes

## Pitfalls

1. **Architecture mismatch loads silently** — Pony LoRA on vanilla SDXL produces garbage without error. Always check model card architecture.
2. **CLIP skip 2 is mandatory for Pony** — forgetting this produces plastic skin even with perfect LoRAs.
3. **Combined weight > 2.0 causes artifacts** — always sum weights across all active LoRAs.
4. **InstantID forces frontal faces** — use PuLID or IP-Adapter FaceID if you need diverse angles.
5. **Flux negative embeddings are useless** — don't waste time on them; engineer the positive prompt instead.
6. **aidmaNSFWunlock has typo variants** — CivitAI sometimes spells it "aidmaNSWFunlock"; always copy from the creator block.

---
*Researched August 2026. Sources: CivitAI, HuggingFace, Reddit r/StableDiffusion, r/comfyui.*