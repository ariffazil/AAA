---
name: cloud-gpu-provisioning
description: "Provision cloud GPU compute for the arifOS federation — RunPod, Google Colab, serverless GPU APIs (fal.ai/Replicate/RunPod serverless), and local CPU ComfyUI fallback. Covers the decision matrix (which GPU for which workload), billing economics (per-ms vs hourly, network volume costs), setup paths, and the federation's current GPU state. Trigger: 'set up runpod', 'google colab', 'which GPU', 'cloud gpu', 'H200 vs A100', 'need GPU for comfyui/video/LLM', 'billed per millisecond', provisioning a pod, or any decision between local CPU vs cloud GPU generation."
version: "2026-08-10-v1"
---

# Cloud GPU Provisioning — arifOS Federation

## Federation GPU Reality (verified 2026-08-10)

- **This box has NO GPU.** AMD EPYC 9354P 8 vCPU, 31GB RAM, CPU-only (no nvidia-smi, no /dev/dri, no /dev/kfd). Local LLM inference is capped at small models (ollama `qwen2.5:3b`, `bge-m3:latest`).
- **ComfyUI local is installed CPU-only** at `/root/comfy/ComfyUI` (comfy-cli 1.15.0, torch 2.13.0+cpu, SD1.5 pruned-emaonly 4GB downloaded). Functional but slow: SD1.5 ≈ 1–3 min/image, SDXL/Flux ≈ 5–15 min. Do NOT promise cloud-grade speed from it.
- **Gemini image/video gen is the current default** (Pro/Flash image, Omni Flash video, Veo 3.1) — shares ONE prepayment credit pool; budget it.
- **MiniMax MCP (:18100)** and **Qwen edit (Bailian)** are live media routes (see `ai-media-generation` skill for model-level routing).

## Decision Matrix — Route per Workload

| Workload | Route | Cost | Verdict |
|---|---|---|---|
| Image gen, worship/sensual visuals, quick iterate | Gemini Pro (`gemini-3-pro-image`) | $0.13–0.24/img | ✅ default (verified 8.5/10 quality) |
| Image gen, cheap volume | Gemini Flash (`gemini-2.5-flash-image`) | $0.039/img | ✅ until Oct 2026 shutdown; then Nano Banana 2 (~$0.045–0.15) |
| Video, no infra | Gemini Omni Flash / Veo 3.1 | shared pool | ✅ (credit pool is the constraint) |
| Video/LLM, serious, sovereign, uncensored | **RunPod H200** | $4.60/hr per-ms | ✅ if video models ≥30GB (Wan 2.2, Hunyuan) or 70B LLM |
| Image gen on GPU cloud (cheap) | **RunPod A100 80GB** community | $1.19–1.64/hr | ✅ best value for image-focused |
| Image gen on GPU cloud (cheapest) | RunPod L40S / 4090-class | $0.30–0.60/hr | ✅ image-only workloads |
| Zero-setup GPU, ephemeral | **Google Colab free** | $0 | ⚠️ T4, 12h session, 90min idle kick, no guaranteed GPU, env resets each session |
| Colab paid | Colab Pro/Pro+ | $9.99/100 CU / $49.99/500 CU | ⚠️ compute-unit burn (T4 ≈ 1.2–2 CU/hr, A100 ≈ 5.4–15 CU/hr) |
| Serverless image API | fal.ai FLUX | $0.025–0.055/img | ✅ predictable per-output pricing |
| Serverless image API | Replicate FLUX | $0.025–0.092/img | ⚠️ cold starts 10–60s; 2.5–4× bare-metal GPU hourly |
| Serverless video API | fal.ai Wan | ~$0.05/sec | ✅ per-second, no idle cost |
| LLM inference (70B+) | RunPod serverless / pod | GPU-time | ✅ `flash` skill for `@remote` Python |

## Billing Discipline (F1 reversible-first, F13 sovereign)

1. **Per-ms billing = stop pods when idle.** RunPod charges GPU only while RUNNING. A stopped pod costs ~$0 (network volume $0.005/hr ≈ $3.6/mo).
2. **Network volume persists models** across pod spin-up/down — NEVER re-download SDXL/Flux/Wan per session.
3. **H200 is overkill for image-gen-only.** A100 80GB (1/4 price) or L40S (1/9 price) produce identical SDXL/Flux output. H200 justified ONLY for 30GB+ video models or 70B+ LLM.
4. **New paid API > $10/mo = 888_HOLD** (T3). Cloud GPU subscriptions need explicit F13 sovereign consent — NEVER auto-subscribe.
5. **Colab free tier is not reliable infra** — 90min idle timeout, environment resets, GPU not guaranteed. Treat as disposable experimentation, never as an organ.

## Setup Paths

| Route | Steps |
|---|---|
| RunPod | See `references/runpod-setup.md` (full verified transcript) |
| Colab + ComfyUI | `github.com/Moksh45/Run-and-Share-ComfyUI-on-Google-Colab` notebook + Pinggy tunnel; ephemeral by nature |
| ComfyUI local CPU | Already installed at `/root/comfy/ComfyUI`; launch: `/root/comfy/ComfyUI/.venv/bin/python main.py --listen 127.0.0.1 --port 8188 --cpu --disable-auto-update` |

## Pitfalls

1. **OAuth is always a user step.** `hermes mcp add <name> --url <hosted> --auth oauth` returns 401 until the human signs in via browser. Report as "⚠ needs user action", never as a failure.
2. **`npx skills add ... --global` fails for some skills** with "PromptScript does not support global skill installation" — the files still land in `~/.agents/skills/`; missing ones can be copied from the git repo directly (see runpod-setup reference).
3. **Verify reality before refusing.** The box has no GPU — but ComfyUI CPU install IS possible and free. Never say "no ComfyUI on this box" when a CPU install exists; say "CPU-only, slow".
4. **Don't run unaudited external `npx` installs blindly** — fetch the docs, evaluate, then execute the documented commands with inspection. The RunPod `agent-setup.md` is official and verifiable (docs.runpod.io domain), but always state what the commands do before running them.
5. **Disk budget:** 80GB pod disk fits SD1.5+SDXL+Flux fp8 but NOT +Wan/Hunyuan video models. Upgrade pod disk or store video models on the network volume.
6. **🔴 RunPod Storage Trap (verified 2026-08-10):** `/workspace` shows PB-scale (2.3PB via MinIO FUSE) BUT the container overlay at `/` is only 30GB. `/tmp`, `~/.cache/pip`, `~/.cache/huggingface` all live on the overlay. HuggingFace/Civitai LFS downloads buffer through `/tmp` → **"Failure writing output to destination"** or **"Disk quota exceeded"** even with 600TB+ free on /workspace. **Fix:** (1) `rm -rf /tmp/* ~/.cache/pip ~/.cache/huggingface` to purge overlay junk (pip unpack dirs can eat 6GB+). (2) `export TMPDIR=/workspace/tmp HF_HOME=/workspace/.cache/huggingface PIP_CACHE_DIR=/workspace/tmp/pip` to redirect all temp/cache layers to /workspace. (3) Use `huggingface_hub.hf_hub_download()` Python API instead of curl/wget — it handles LFS redirects, chunk streaming, and writes directly to the target path without overlay buffering. Curl/wget follow the HuggingFace 302→CDN redirect but fail to write the body (shows 100% then 0-byte file).
7. **FLUX.1 dev is gated on HuggingFace (verified 2026-08-10):** `black-forest-labs/FLUX.1-dev` returns 401 without authenticated access. Requires HF_TOKEN + accepting the gate agreement on the model page. If no HF_TOKEN is available, skip FLUX and use ungated alternatives (RealVisXL, DreamShaper XL, etc.).
8. **Civitai API downloads may require auth (verified 2026-08-10):** `https://civitai.com/api/download/models/<id>` without a token returns 404 or empty body for some models. Civitai has been tightening API access. Always have a CIVITAI_TOKEN in kunci-mas.env, or use HuggingFace mirrors where available.
9. **Per-user disk quota on RunPod MFS (verified 2026-08-10):** Even after cleaning overlay, large model files (14GB FLUX FP8) can consume the per-user quota on the MinIO FUSE mount. Check `du -sh /workspace/ComfyUI/models/checkpoints/` before downloading — if >10GB, delete unused models before pulling new ones. The quota is invisible (no `quota` command, `df` shows PB-scale).

## References
- `references/runpod-setup.md` — full RunPod agent setup transcript (skills, MCP, key wiring, user steps pending)
