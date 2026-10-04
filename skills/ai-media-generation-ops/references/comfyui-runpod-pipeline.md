# ComfyUI on RunPod — Pipeline Reference

Verified end-to-end 2026-08-10. RTX 4090 pod, ComfyUI 0.31.0.

## Pod details

```
Pod ID:    7qqgz1ipp82taq
Name:      fluffy_moccasin_dolphin
GPU:       NVIDIA GeForce RTX 4090 (24564 MiB VRAM)
Image:     runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404
SSH:       ssh -i /root/.runpod/ssh/runpodctl-ssh-key root@213.173.110.235 -p 14073
Ports:     8188/http (ComfyUI), 8888/http (Jupyter), 22/tcp+udp (SSH)
Cost:      $0.74/hr while running
Storage:   Network volume at /workspace (PB-scale), root overlay ~27GB
```

## Checkpoints on disk (2026-08-10)

| File | Size | Baked VAE | Notes |
|---|---|---|---|
| `RealVisXL_V4.0.safetensors` | 6.5GB | Yes | Clean stock photography. Safety-aligned. |
| `ponyDiffusionV6XL_v6StartWithThisOne.safetensors` | 6.9GB | Yes | Uncensored, multi-subject, score tags. |

## VAE status

- `ae.safetensors` (FLUX VAE): 0 bytes — FLUX.1-dev is gated repo, need HF token with accepted license
- Both RealVisXL and Pony V6 XL have baked VAEs — no external VAE needed for these

## ComfyUI startup

```bash
cd /workspace/ComfyUI
export TMPDIR=/workspace/tmp
export TEMP=/workspace/tmp
export HF_HOME=/workspace/.cache/huggingface
nohup python3 main.py --listen 0.0.0.0 --port 8188 \
  --output-directory /workspace/output > /workspace/comfyui.log 2>&1 &
```

Health check: `curl -sf http://127.0.0.1:8188/system_stats`

## Overlay trap fix

```bash
# Run on pod before ANY download
rm -rf /tmp/* ~/.cache/pip ~/.cache/huggingface
mkdir -p /workspace/tmp /workspace/.cache/huggingface /workspace/.cache/torch
export TMPDIR=/workspace/tmp
export HF_HOME=/workspace/.cache/huggingface
export PIP_CACHE_DIR=/workspace/tmp/pip
export TEMP=/workspace/tmp
```

## Download models via huggingface_hub (NOT curl)

```python
import os
os.environ["TMPDIR"] = "/workspace/tmp"
os.environ["HF_HOME"] = "/workspace/.cache/huggingface"
from huggingface_hub import hf_hub_download

# Public mirror of Pony V6 XL (no auth needed)
path = hf_hub_download(
    repo_id="LyliaEngine/Pony_Diffusion_V6_XL",
    filename="ponyDiffusionV6XL_v6StartWithThisOne.safetensors",
    local_dir="/workspace/ComfyUI/models/checkpoints",
)
```

## Render pattern

```python
import urllib.request, json, time

COMFY = "http://127.0.0.1:8188"

# Build workflow payload (see gen_pony_sado.py for full example)
payload = {"prompt": { ... }}

# Queue
req = urllib.request.Request(
    f"{COMFY}/prompt",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(req, timeout=10)
pid = json.loads(resp.read())["prompt_id"]

# Poll history
for i in range(60):
    time.sleep(2)
    h = urllib.request.urlopen(f"{COMFY}/history/{pid}", timeout=10)
    d = json.loads(h.read())
    if pid in d:
        # Extract images from outputs
        for nid, out in d[pid]["outputs"].items():
            if "images" in out:
                for img in out["images"]:
                    fn, sub = img["filename"], img["subfolder"]
                    url = f"{COMFY}/view?filename={fn}&subfolder={sub}&type=output"
                    urllib.request.urlretrieve(url, f"/workspace/tmp/{fn}")
```

## Pony V6 XL prompt format

```
score_9, score_8_up, score_7_up, source_pony,
absurdres, masterpiece, best quality,
[scene description],
negative prompt: score_6, score_5, score_4, worst quality, low quality
```

Key differences from standard SDXL:
- Score tags ARE required (quality drops without them)
- Better multi-subject handling than stock SDXL
- Uncensored latent space — no safety alignment blocking content
- Uses `source_pony` or `source_anime` style tags

## Performance (RTX 4090)

| Model | Steps | Resolution | Time |
|---|---|---|---|
| RealVisXL V4.0 | 25 | 896×1152 | ~4s |
| RealVisXL V4.0 | 35 | 832×1216 | ~6s |
| Pony V6 XL | 30 | 832×1216 | ~48s |

Pony V6 XL is slower due to larger model (6.9GB vs 6.5GB) and higher VRAM usage (~7GB vs ~4GB).

## Known issues

1. ComfyUI log file contains binary/null bytes — use `/history` API instead
2. FLUX.1-dev VAE gated — need HF license acceptance
3. Civitai downloads need API token (not in kunci-mas.env currently)
4. Checkpoint names must EXACTLY match filenames on disk (case-sensitive)
