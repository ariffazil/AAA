# MiniMax-Music3 — Federation Capability Registration

**Registered:** 2026-08-20T00:23Z | **FI-008 Kimi Code** | **Band 3 (Capability Intel)**

## What

Open-weights text-to-music model by MiniMax. Generates complete songs up to 5 minutes at 32 kHz, 16-bit stereo WAV from lyrics + structured caption.

- **Architecture:** Hybrid-LM (8B Global + 0.6B Local) → 2.4B Flow Matching → 123M Flow-VAE
- **Control:** Lyrics with section tags ([Verse], [Chorus], etc.) + Structured Caption (Global Metadata, Vocal Details, Arrangement)
- **Repo:** https://github.com/MiniMax-AI/MiniMax-Music3
- **Weights:** https://huggingface.co/MiniMaxAI/MiniMax-Music3
- **License:** Community License — commercial OK with attribution; >$20M revenue needs written authorization
- **Released:** 2026-08-13 | **Stars:** 613 | **Forks:** 49

## Federation Status

| Dimension | Status |
|-----------|--------|
| **Existing API** | DEAD — `v1/music_generation` returns 410 Gone |
| **Self-host path** | Requires 2× CUDA GPU (SGLang-Omni) |
| **VPS capability** | NO — AMD EPYC CPU-only, 31GB RAM |
| **Runpod path** | VIABLE — needs GPU pod with ≥48GB VRAM total |
| **Single-GPU path** | diffusers pipeline under 24GB VRAM, ~22GB with CPU offload, 8GB with group offloading |
| **ComfyUI path** | Native template with FP16/INT8 weights from Comfy-Org |

## Federation Integration Surface

### Somatic Music Intelligence (F10)
- Music3 is a **generative engine** (lyrics → complete song), distinct from parametric engines in `AAA-somatic-engine-catalog`
- Fits the **composer lens** slot — full song generation from structured input
- Output: 32 kHz stereo WAV — compatible with existing TTS/audio pipeline

### Existing Overlap
- `mcp__minimax-media__music_generation` — DEAD (410). This was the API path; Music3 replaces it.
- `mcp__minimax-media__text_to_audio` — ALIVE (TTS, different tool)
- `AAA-tts-engine-catalog` — TTS engines, not music generation

### Potential MCP Surface
If served (Runpod or local GPU):
- `mcp__minimax-music3__generate_song` — lyrics + caption → WAV
- `mcp__minimax-music3__caption_rewriter` — short prompt → structured caption
- Could route through `forge-multimodal-router` as music generation capability

## Action Path

1. **Immediate:** Register capability gap. API path dead, self-host only.
2. **Short-term:** Provision Runpod GPU (2× A10/RTX 4090 or single A100) → deploy SGLang-Omni → expose as MCP endpoint
3. **Medium-term:** Wire into federation multimodal router → `AAA-somatic-music-doctrine` composer lane
4. **Do NOT:** Attempt CPU inference. Architecture requires CUDA.

## Evidence

- [OBS] GitHub README confirms 2-GPU requirement, architecture, API shape
- [OBS] `curl https://api.minimax.io/v1/music_generation` → 410 Gone (2026-08-20)
- [OBS] VPS `nvidia-smi` → not found, CPU-only
- [DER] Music3 is MiniMax's replacement for the deprecated music API endpoint
