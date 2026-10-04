# GPU Rental & Shadow Pipeline (uncensored content)

Arif session 2026-08-10 — dark mirrors → ComfyUI setup evaluation → RunPod deployment.

## The routing doctrine (why)

Mainstream API keys (Gemini, OpenAI, MiniMax, Qwen/Bailian) are all aligned-gated — cloud providers filter NSFW at output. Attempting filter bypass risks API key revocation, burning keys needed for legitimate work (Gemini shared credit pool already tight). The uncensored ecosystem is local-first BY DESIGN: no API key involved, hardware only.

**Lines drawn (F5/F9, Malaysia law):** non-consensual deepfakes of real people = criminal (CMA 1998 §233, Penal Code §420, Computer Crimes Act 1997; Gobind tightening announced June 2026); anything involving minors = zero tolerance, no exceptions. Consensual adult fictional content via open models = the shadow lane.

## Shadow stack (all open-source, no keys)

| Layer | Tools | Hardware |
|---|---|---|
| Image T2I | ComfyUI + Pony V6 XL / Illustrious XL / Juggernaut XL / RealVisXL / FLUX.1 / Chroma1-HD / Z-Image | GPU ≥24GB VRAM |
| LLM text | Dolphin (Mistral), Abliterated models | GPU or CPU+RAM |
| Voice | RVC (Retrieval-based Voice Conversion) | CPU OK |
| Video | Wan 2.1, Hunyuan Video, LTX | GPU ≥24GB VRAM |

**Production NSFW pattern:** Pony V6 XL (anime) + Juggernaut XL / RealVisXL (realistic) behind a router. ComfyUI has **no built-in safety filter** — uncensored by default when loaded locally.

## GPU cloud comparison (Aug 2026 prices)

| Platform | GPU | Price/hr | VRAM | Notes |
|---|---|---|---|---|
| **RunPod** | RTX 4090 | **$0.69–0.74** | 24GB | **Sweet spot.** Per-second billing. Consumer GPUs in "Community Cloud" tab. |
| RunPod | RTX 3090 | $0.50 | 24GB | Older, slower, cheapest option |
| RunPod | L4 | $0.49 | 24GB | Ada Lovelace data center, low performance |
| RunPod | RTX A6000 | $0.53 | 48GB | Best value per GB VRAM |
| RunPod | A100 SXM | $1.59 | 80GB | Headroom for multi-model (image + LLM) |
| RunPod | H100 SXM | $3.29 | 80GB | Overkill for image gen |
| RunPod | H200 SXM | $4.59 | 141GB | Extreme overkill — 6.6x RTX 4090 for same images |
| Vast.ai | RTX 3090 | ~$0.22–0.35 | 24GB | Cheapest raw but host-by-host reliability; budget 20-40% overhead |
| Vast.ai | RTX 4090 | ~$0.40–0.80 | 24GB | |
| Google Colab | T4 | Free (12h sessions) | 16GB | ⚠️ Free tier **bans stable-diffusion-webui/A1111**. NSFW SD on Colab risks Google account ban. |
| Google Colab Pro | T4/A100 | $9.99/mo (100 CU) | varies | A100 burns ~15 CU/hr = only ~7 hrs. Runtime not guaranteed. |
| Google Colab Pro+ | A100 | $49.99/mo (500 CU) | varies | Best runtime, still no GPU guarantee. |
| **Comfy Cloud** (comfy.org/mcp) | RTX 6000 Pro | ~$20/mo sub + credits | 24GB | **Cloud-gated content policy — NOT for uncensored.** Standard $20/mo; GPU at 0.266 credits/sec. Free tier = no API access. |
| Spheron | A100 | $1.48/hr | 80GB | |
| Clore.ai | RTX 4090 | varies (marketplace) | 24GB | P2P, ultra-low fees, reliability varies |

## GPU selection guidance for image gen

- **Sweet spot:** RTX 4090 (24GB, $0.69–0.74/hr) — fastest per-image inference for SDXL/FLUX/Pony, mature ComfyUI driver support
- **Headroom:** A6000 (48GB, $0.53/hr) or A100 SXM (80GB, $1.59/hr) — multi-model pipelines (image gen + uncensored LLM on same pod)
- **Overkill:** H100/H200 — designed for training 70B+ models, not image gen. H200 at $4.59/hr = 6.6x the cost of RTX 4090 for identical images
- **Image models use 8–24GB VRAM:** SDXL/Pony/RealVisXL ~6–8GB; FLUX.1 dev fp8 ~12GB; FLUX.2 32B ~30GB
- **If Arif iterates rapidly** ("redo/nope/push" pattern), inference speed matters — pick fastest GPU per dollar, not cheapest

## Comfy Cloud MCP facts (comfy.org/mcp, Aug 2026)

- `comfy.org/mcp` = marketing page; actual MCP server behind OAuth (not a public URL you can curl)
- Base API: `https://cloud.comfy.org`, auth: `X-API-Key` header, paid tiers only
- Free tier = 400 credits/mo, **no API access** (browse only)
- Standard = ~$20/mo, ~4.4 hrs GPU time; Pro = ~$60/mo
- Concurrency: Standard 1, Creator 3, Pro 5
- Same ComfyUI workflow JSON format as local — write once, deploy anywhere
- **Shadow path:** NOT suitable (cloud content policy gates explicit content)
- **SFW path:** Useful for design/branding/MakcikGPT creative work via official tools
- Full docs: `https://docs.comfy.org/development/cloud/overview`

## RunPod agent setup (docs.runpod.io/agent-setup.md)

```bash
# Step 1: Install RunPod skills + MCP server
npx -y skills add runpod/runpod-plugins-official --skill '*' --yes --global

# Step 2: Register hosted MCP server (triggers OAuth on first tool use — user browser step)
npx @runpod/mcp-server@latest add
```

**Result observed 2026-08-10:** Step 1 copies 6 skills to `~/.agents/skills/` (runpod, runpod-mcp, runpodctl, flash, runpod-usage, companion-clis). PromptScript reports "does not support global skill installation" for all 6 but the files land on disk. Step 2 was not run in this session (user interrupted).

**MCP server URL:** `https://mcp.getrunpod.io/` — OAuth triggers on first RunPod tool use; user approves in the browser. Agent cannot perform OAuth autonomously.

**Hermes integration:** `npx @runpod/mcp-server@latest add` auto-detects the agent type and configures the hosted MCP server. Verify after with a pod-list tool call.

## Shadow governance shape

```
Shadow Box (isolated)
├── GPU: rented on RunPod (RTX 4090) or own workstation
├── ComfyUI installed manually (or RunPod ComfyUI template)
├── Models: downloaded from HuggingFace/CivitAI (Pony V6 XL, Juggernaut XL, FLUX.1 fp8, etc.)
├── NO MCP surface (REST API only, port 8188)
├── NO lane memory crossover
├── Tailscale private mesh for sovereign access only (no public exposure)
└── Outputs: exported as files, imported to federation only via explicit manual copy
```

**Never attempt shadow content on the arifOS VPS** (CPU-only anyway, plus production box with all main API keys).

## RunPod Storage Trap (verified 2026-08-10)

**The pod shows 2.3PB on `/workspace` (MFS mount) but `/tmp` and `~/.cache` default to the 30GB root overlay.** Downloads via curl/wget buffer through `/tmp` on the overlay, hitting "Failure writing body" or "Disk quota exceeded" even when the file is hundreds of MBs.

**Root cause:** RunPod per-container overlay is ~30GB. After ComfyUI + pip packages (~13GB), only ~17GB remains. Any download buffering to `/tmp` chokes.

**Fix — Emergency Overlay Purge + Env Override:**

```bash
# 1. Clear root overlay junk
rm -rf /tmp/* ~/.cache/pip ~/.cache/huggingface

# 2. Re-create workspace cache dirs (609TB MFS mount)
mkdir -p /workspace/tmp /workspace/.cache/huggingface /workspace/.cache/torch /workspace/.cache/pip

# 3. Force env overrides in ALL sessions (add to .bashrc on pod)
export TMPDIR=/workspace/tmp
export HF_HOME=/workspace/.cache/huggingface
export PIP_CACHE_DIR=/workspace/tmp/pip
```

**Download method — Python huggingface_hub API (bypasses curl redirect + quota traps):**

```python
import os
os.environ["TMPDIR"] = "/workspace/tmp"
os.environ["HF_HOME"] = "/workspace/.cache/huggingface"

from huggingface_hub import hf_hub_download

path = hf_hub_download(
    repo_id="SG161222/RealVisXL_V4.0",
    filename="RealVisXL_V4.0.safetensors",
    local_dir="/workspace/ComfyUI/models/checkpoints",
    local_dir_use_symlinks=False
)
```

**Why this works:** `hf_hub_download` streams directly to `/workspace` (MFS mount), never touches `/tmp`. Handles LFS redirects, chunked downloads, and resume automatically.

**Gated repos (e.g., FLUX.1 dev):** Need `HF_TOKEN` properly exported on the pod — NOT via heredoc placeholder (`__TOKEN__` won't expand inside `<< 'HEREDOC'`). Use `export HF_TOKEN=$(printenv HF_TOKEN)` or write the token to a file first.

**Disk quota management:** After downloading a large checkpoint (e.g., FLUX FP8 14GB), deleting it frees quota for other models. A 24GB VRAM pod typically has ~15-20GB usable quota on `/workspace`.

## Model download links (HuggingFace)

| Model | URL | Size | Use case |
|---|---|---|---|
| RealVisXL V4.0 | `https://huggingface.co/SG161222/RealVisXL_V4.0` | ~6.5GB | Realistic sado/bodybuilder |
| FLUX.1 dev fp8 | `https://huggingface.co/Comfy-Org/flux1-dev` | ~12GB | Premium quality, best anatomy |
| Pony Diffusion V6 XL | CivitAI (set API token first) | ~6.5GB | Anime/explicit-trained, largest LoRA ecosystem |
| Illustrious XL | CivitAI | ~6.5GB | Anime, native 1536×1536 |
| Chroma1-HD | HuggingFace | ~8.9GB | Released without safety alignment |
| Juggernaut XL | CivitAI | ~6.5GB | Realistic production standard |
