---
name: sd-lora-ecosystem
description: "Use when selecting LoRAs for Stable Diffusion pipelines."
version: 1.0.0
tags: [stable-diffusion, sdxl, flux, pony, lora, civitai, comfyui, nsfw, face-consistency, controlnet]
metadata:
  hermes:
    category: creative
    related: [comfyui, photorealistic-human-image-gen]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# SD LoRA Ecosystem Guide

Select, stack, and configure LoRAs, negative embeddings, face consistency tools, and ControlNets for Stable Diffusion image generation pipelines.

## When to Use

- Building an SD pipeline and need to select LoRAs for a specific task
- Resolving architecture mismatches (Pony LoRA on SDXL, etc.)
- Configuring face consistency (IP-Adapter, InstantID, PuLID)
- Tuning LoRA weights to avoid artifacts
- Setting up negative embeddings for quality improvement
- Planning ControlNet stacking for pose/anatomy control

## Architecture Compatibility Rules

1. **Pony ≠ SDXL ≠ Illustrious** — LoRAs load across branches without error but produce garbage. Always match architecture tags.
2. **CLIP skip:** Pony = 2, SDXL = 1, Flux = N/A. Wrong skip = plastic skin.
3. **CFG ranges:** Pony 3.5–5.0, SDXL 5–7, Flux 3.5–4.0 (guidance-based).
4. **Combined LoRA weight:** Keep under 2.0 total. Example: 0.7 + 0.5 + 0.4 = 1.6.
5. **Max concurrent LoRAs:** 1–3 at once. More = style collapse.
6. **Pony prompt system:** Uses `score_` prefix tags: `score_9, score_8_up`.

## LoRA Selection by Category

### NSFW Unlock (Load FIRST)
- **SDXL:** NSFW POV All In One (0.6 weight, 19 pose triggers) — pair with uncensored base checkpoint (see Checkpoint Selection below)
- **Pony:** Pony Diffusion V6 XL checkpoint (base)
- **Flux:** aidmaNSFWunlock (0.8) → Nude Style V2 (1.0) — pair with Fluxed Up or flux1-dev + Flux-NSFW-uncensored LoRA

### Aesthetic / Quality
- **Detail Tweaker XL** (SDXL): bidirectional -3 to +3, typical 0.5–1.0. The universal detail slider.
- **Skin Realism** (SDXL): 0.5 (1.0 distorts anatomy). Pores, blemishes, imperfections.
- **Detail Enhancer FLUX V1** (Flux): 0.5–1.0
- **Realistic Photos Detailed Skin V3** (Flux): 0.5–0.8

### Face Consistency Toolchain (2026)

| Method | Arch | Fidelity | Best For |
|--------|------|----------|----------|
| IP-Adapter FaceID v2 | SDXL | 80–90% | General face lock |
| InstantID | SDXL ONLY | 90–95% | Frontal portraits |
| PuLID | SDXL | 85–95% | Diverse poses/styles |
| PuLID Flux | Flux | 90–95% | Best Flux face lock |

Key weights:
- IP-Adapter FaceID: adapter 0.70–0.80, companion LoRA 0.55–0.65
- InstantID: adapter 0.6–0.8, ControlNet 0.5–0.7
- PuLID Flux: 0.8–0.95 (v0.9.0) or 0.9–1.0 (v0.9.1)

### ControlNet for Pose/Anatomy
- OpenPose SDXL + Depth stacked at 0.35–0.55 each
- Use `openpose_full` preprocessor for body + hands + face joints

### Hand Fix
- ControlNet OpenPose `full` preprocessor
- ADetailer for automatic inpainting post-process
- Flux handles hands better than SDXL/SD1.5

### Negative Embeddings
- **SD 1.5:** EasyNegative + BadHandsV4
- **SDXL:** Ultimate Text Embeddings Pack (fewer negatives needed)
- **Flux:** No traditional negative embeddings; use natural language

## Recommended Stacks

### SDXL Realistic Portrait
```
Detail Tweaker XL (0.7) + Skin Realism (0.5) + Lighting LoRA (0.4)
Total: 1.6
```

### Flux NSFW Pipeline
```
checkpoint → aidmaNSFWunlock (0.8) → Nude Style V2 (1.0) → Detail Enhancer (0.7)
+ PuLID Flux (0.9) for face consistency
```

### Character Consistency (80–95%)
```
IP-Adapter FaceID (0.75) + ControlNet OpenPose (0.4) + ADetailer
For Flux: PuLID Flux (0.9) replaces IP-Adapter
```

## Sources
- CivitAI (civitai.com) — LoRA/embedding library
- HuggingFace — face consistency models, ControlNet, uncensored checkpoints (see reference below)
- Tensor.Art (tensor.art) — mirrors + originals
- GitHub — ComfyUI custom nodes

## Detailed Reference
- `references/lora-stacking-guide.md` — full tables with CivitAI links, download counts, version-specific details
- `references/hf-uncensored-checkpoints.md` — verified HuggingFace download URLs for SDXL/Flux NSFW checkpoints (HEAD-tested Aug 2026)

## Checkpoint Selection (Base Models for LoRA Stacking)

LoRAs need a good base checkpoint. Community fine-tunes remove safety filters and improve realism. Always check the base before stacking.

### SDXL Uncensored (HF direct, no token)
See `references/hf-uncensored-checkpoints.md` for full catalog with verified URLs.

**Top picks for realistic portraits:**
- **Juggernaut-XL-v9** (RunDiffusion) — 7.11 GB, top photorealism
- **RealVisXL V4.0 / V5.0** (SG161222) — 6.94 GB, mature and widely used
- **EpicRealism XL v8** (pbxadb mirror) — 6.94 GB, natural skin

**NSFW-specific:**
- **LUSTIFY v2.0** (andro-flock) — 6.94 GB, explicitly NSFW
- **Hassan-SDXL-Pruned** (hassanblend) — 6.94 GB, NSFW-focused
- **WAI NSFW Illustrious v11** (guy39) — 6.94 GB, Illustrious-style NSFW

### Flux Uncensored
- **Fluxed Up 7.1** (HurdyThirty) — 12.1 GB FP8, Flux NSFW checkpoint (only FP8 on HF; FP16 is CivitAI-only)
- **Flux-NSFW-uncensored LoRA** (hvai) — 687 MB, apply on top of flux1-dev base

⚠️ The official `stabilityai/stable-diffusion-xl-base-1.0` is safety-aligned (refuses NSFW). Always use a community fine-tune for uncensored work.

## Pitfalls
1. Architecture mismatch loads silently — always verify model card tags
2. CLIP skip 2 mandatory for Pony — forgetting = plastic skin
3. Combined weight > 2.0 = artifacts — always sum across active LoRAs
4. InstantID forces frontal faces — use PuLID for diverse angles
5. Flux negative embeddings are useless — engineer positive prompt instead
6. aidmaNSFWunlock has CivitAI typo variant "aidmaNSWFunlock" — copy trigger from creator block
7. Official SDXL base is safety-aligned — `stabilityai/stable-diffusion-xl-base-1.0` refuses NSFW in outputs. Always use a community fine-tune checkpoint for uncensored work
8. HF download URLs must be HEAD-verified before reporting — repos can be gated (401), removed (404), or renamed. Use `curl -I "https://huggingface.co/{repo}/resolve/main/{file}"` to confirm accessibility
9. CivitAI FP16 Flux checkpoints often not mirrored to HF — only FP8 variants available on HuggingFace (e.g., Fluxed Up 7.1)