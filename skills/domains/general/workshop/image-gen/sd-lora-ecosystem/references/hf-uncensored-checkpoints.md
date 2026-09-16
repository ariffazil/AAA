# HuggingFace Uncensored/Uncurated SDXL & Flux Checkpoints

Verified August 2026. All URLs HEAD-tested (HTTP 200 with correct Content-Length). No HF access token required for any.

## URL Pattern

```
https://huggingface.co/{repo_id}/resolve/main/{file_path}
```

Download with wget/curl. ComfyUI `comfy model download --url <URL> --relative-path models/checkpoints` also works.

## SDXL Checkpoints

| Repo | File | Size | Aesthetic | Notes |
|------|------|------|-----------|-------|
| `RunDiffusion/Juggernaut-XL-v9` | `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors` | 7.11 GB | Photorealism | Top-tier realistic portraits, no safety filter in weights |
| `SG161222/RealVisXL_V4.0` | `RealVisXL_V4.0.safetensors` | 6.94 GB | Photorealism | Mature, widely used |
| `SG161222/RealVisXL_V5.0` | `RealVisXL_V5.0_fp16.safetensors` | 6.94 GB | Photorealism | Latest RealVisXL |
| `pbxadb/sdxl-models` | `epicrealismXL_v8Kiss.safetensors` | 6.94 GB | Photorealism | EpicRealism XL v8, natural skin |
| `pbxadb/sdxl-models` | `Juggernaut_X_RunDiffusion.safetensors` | 7.11 GB | Photorealism | Juggernaut X (older generation) |
| `xingren23/comfyflow-models` | `checkpoints/sdxl/juggernaut-xl_v8.safetensors` | 7.11 GB | Photorealism | Juggernaut XL v8 mirror (commit-pinned) |
| `hassanblend/Hassan-SDXL-Pruned` | `HassanSDXLPruned.safetensors` | 6.94 GB | NSFW-focused | HassanBlend, pruned |
| `andro-flock/LUSTIFY-SDXL-NSFW-checkpoint-v2-0-INPAINTING` | `lustifySDXLNSFW_v20-inpainting.safetensors` | 6.94 GB | NSFW photorealism | Explicitly NSFW, inpainting variant |
| `guy39/wai-nsfw-illustrious-sdxl-v11.0` | `waiNSFWIllustrious_v110.safetensors` | 6.94 GB | NSFW / Illustrious | WAI NSFW Illustrious style |
| `mirroring/civitai_mirror` | `models/Stable-diffusion/SDXL/nsfw/icbinpXL_v20.safetensors` | 6.94 GB | NSFW photorealism | CivitAI mirror, "ICBINP" XL |

## Flux Checkpoints

| Repo | File | Size | Notes |
|------|------|------|-------|
| `HurdyThirty/FluxedUp` | `fluxedUpFluxNSFW_40DevFp8.safetensors` | 12.1 GB | Flux NSFW checkpoint, FP8 (Dev-based). CivitAI has FP16 (22 GB) but not on HF |

## Flux LoRAs (apply on top of flux1-dev base)

| Repo | File | Size | Notes |
|------|------|------|-------|
| `datasets/hvai/fluxlora` | `Flux-NSFW-uncensored.safetensors` | 687 MB | Flux NSFW LoRA — pair with any flux1-dev checkpoint |

## Repo Type Patterns

- **Official creators** (SG161222, RunDiffusion, hassanblend): most trustworthy, maintained
- **Mirror repos** (pbxadb, mirroring/civitai_mirror, xingren23, guy39): community re-uploads, verify file integrity if possible
- **Dataset-hosted** (hvai, tyDiffusion): checkpoints/LoRAs stored in HF datasets — same download URL pattern works

## Pitfalls

1. **HEAD-verify before reporting**: always test HEAD on the `/resolve/main/` URL before telling a user it works. Some repos are gated (401), removed (404), or have non-obvious filenames
2. **CivitAI FP16 vs HF FP8**: popular Flux NSFW checkpoints (Fluxed Up) often only have FP8 on HF; FP16 is CivitAI-only
3. **Commit-pinned repos** (xingren23, mirroring/civitai_mirror): use the full commit hash in the URL, not `main`/`latest`
4. **Official base SDXL is safety-aligned**: `stabilityai/stable-diffusion-xl-base-1.0` filters NSFW — always use a community fine-tune for uncensored work
5. **Some HF NSFW repos are gated**: returned 401 Unauthorized — excluded from this catalog
6. **LoRA vs Checkpoint**: the hvai Flux-NSFW-uncensored (687 MB) is a LoRA, not a full checkpoint — it must be applied ON TOP of a base flux model

---

*Verified August 2026 via HTTP HEAD requests.*
