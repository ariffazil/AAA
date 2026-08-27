---
name: AAA-shadow-mode
id: AAA-shadow-mode
risk_tier: low
description: 'Shadow mode multimodal compute & generation doctrine for sovereign human needs. Governs out-of-band GPU execution (A100/Hostinger/RunPod), asynchronous batch processing, privacy isolation, and zero-clutter offloading.'
version: 1.0.0
tags:
- shadow-mode
- gpu-compute
- multimodal
- human-needs
- comfyui
- flux
- sdxl
- video-generation
- privacy
- federation
- F13
floor_scope:
- F01
- F02
- F10
- F11
- F13
owner: AAA
autonomy_tier: T1
capability_tier: fed-shadow-compute
ecology_state: WARM
mirror_paths:
- /root/AAA/skills/AAA-shadow-mode/SKILL.md
- /root/HERMES/skills/AAA-shadow-mode/SKILL.md
- /root/.agents/skills/AAA-shadow-mode/SKILL.md
forged: 2026-08-26
forged_by: 333-AGI (Antigravity)
f13_directive: "Shadow GPU handles heavy generation and human needs asynchronously; VPS remains lean and governed."
constitutional_floor: F13 SOVEREIGN — total privacy isolation for human needs; F1 AMANAH — no unmetered or surprise drift
---

# AAA-shadow-mode — Sovereign Shadow Multimodal Compute

## 1. Purpose & Doctrine

The **Shadow Mode** architecture establishes an out-of-band, high-performance compute plane dedicated to heavy multimodal AI generation (Image, Video, Audio) and sovereign human needs.

In accordance with the **Zen Doctrine** and **F13 Sovereignty**:
1. **Machine Peace**: The primary VPS remains lean and uncluttered. Heavy CUDA/PyTorch tensor computation is offloaded entirely to dedicated shadow instances (e.g., A100 80GB on Hostinger/RunPod).
2. **Agent Peace**: Jobs are dispatched asynchronously via REST API / worker queues with task receipts. Agents do not block or freeze waiting on generation.
3. **Human Peace & Privacy**: All personal creative, artistic, and exploratory tasks execute in secure, sovereign isolation with zero external telemetry leakage.

```
┌────────────────────────────────────────────────────────┐
│                   PRIMARY VPS (Lean)                  │
│   arifOS (8088) ── arifFLOW (7073) ── HERMES / AAA    │
└──────────────────────────┬─────────────────────────────┘
                           │ Async Job Dispatch (SSH / REST)
                           ▼
┌────────────────────────────────────────────────────────┐
│               SHADOW GPU INSTANCE (Heavy)              │
│   • NVIDIA A100 (80GB VRAM) / Headless Daemon          │
│   • ComfyUI REST API (:8188)                           │
│   • Flux.1-dev/schnell, SDXL, Wan2.1, CosyVoice        │
│   • Isolated Output Cache (/home/ubuntu/ComfyUI/output)│
└────────────────────────────────────────────────────────┘
```

---

## 2. The Three Invariants of Shadow Mode

### Invariant 1: Physical & Process Isolation (F1 AMANAH)
* Never run multi-gigabyte diffusion/video model inference directly on the primary VPS.
* All heavy weights (`.safetensors`, `.gguf`, checkpoints, UNETs) live on the shadow instance storage.
* Network access between the VPS and Shadow instance is authenticated via dedicated Ed25519 keys (`/root/.ssh/hostinger_ed25519`).

### Invariant 2: Sovereign Discretion & Human Needs (F13 SOVEREIGN)
* The shadow plane exists to fulfill the sovereign operator's creative, artistic, visual, and personal needs without external SaaS censorship, throttling, or telemetry snooping.
* Generative tasks respect legal boundaries, fictional character domains, and sovereign consent.
* Generated artifacts are stored in private directories with explicit lifecycle management (retain or auto-purge).

### Invariant 3: Asynchronous EMD Contract (Encode → Metabolize → Decode)
* **Encode**: Hermes/AAA captures the user prompt, style constraints, resolution, and seed, encoding them into a standardized JSON workflow.
* **Metabolize**: The task is queued out-of-band. The primary agent returns immediate confirmation with a Task ID / Receipt.
* **Decode**: The shadow GPU renders the batch, posts back completion, and provides the output URL or directly streams the final media artifact.

---

## 3. Supported Multimodal Capabilities

| Modality | Primary Models | Hardware Target | Use Case |
| :--- | :--- | :--- | :--- |
| **High-Fidelity T2I** | Flux.1-dev (FP8), SDXL Base 1.0 | A100 (16–24GB allocation) | Photorealism, artistic compositions, complex prompt adherence (Canon: KSampler CFG=1.0, FluxGuidance=2.5–3.5, avoid burnt latents) |
| **Fast Draft T2I** | Flux.1-schnell, SDXL Turbo/Lightning | A100 (8–12GB allocation) | 4–8 step rapid visual prototyping |
| **Control & Consistency** | ControlNet (Depth, OpenPose, Canny), InstantID, PuLID | A100 (20–32GB allocation) | Pose transfer, facial identity preservation, structural framing |
| **Video Generation** | Wan2.1 / Wan2.5, CogVideoX, HunyuanVideo | A100 (40–80GB allocation) | Text-to-video, image-to-video, character animation |
| **Audio & Voice** | ChatTTS, CosyVoice, Fish Speech, MiniMax | A100 / Local | High-fidelity voice synthesis, expressive cadence |

---

## 4. Operational Runbook

### A. Health & State Check
To verify shadow compute availability from the primary VPS:
```bash
# Check SSH connectivity
ssh shadow-gpu "nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader"

# Check ComfyUI API health
ssh shadow-gpu "curl -s http://127.0.0.1:8188/system_stats"
```

### B. Job Submission Pattern (ComfyUI REST API)
1. Prepare the JSON workflow payload with node graph mappings.
2. Dispatch payload to `http://127.0.0.1:8188/prompt`.
3. Track execution state via `/history/{prompt_id}`.
4. Retrieve the resulting image/video from `/view?filename={filename}&type=output`.

### C. Resource Zen (Zero Drift)
* Checkpoints stored in `/home/ubuntu/ComfyUI/models/checkpoints/`.
* LoRAs stored in `/home/ubuntu/ComfyUI/models/loras/`.
* Output artifacts cached in `/home/ubuntu/ComfyUI/output/`.
* When idle, VRAM is released or cached efficiently without consuming primary VPS memory.

---

## 5. Failure Modes & Self-Healing

| Symptom | Cause | Resolution |
| :--- | :--- | :--- |
| **0-byte Model File** | CivitAI download without API token | Use HuggingFace mirror or append `?token=<CIVITAI_KEY>` to download URL. |
| **CUDA Out of Memory (OOM)** | High batch size or unquantized model | Switch to FP8/GGUF variant or enable `--highvram` / `--gpu-only` flags. |
| **Missing Custom Node Dependency** | Ubuntu 24.04 package deprecation | Ensure `libgl1`, `libglx-mesa0`, `libglib2.0-0` are installed in the host OS. |
| **Connection Timeout** | Dynamic port / tunnel change | Verify host entry in `/root/.ssh/config` (`Host shadow-gpu`). |

---

## 6. Audit & Receipts

Every shadow-mode dispatch records a receipt to `VAULT999`:
- `task_id`: Unique generation identifier.
- `model_used`: Checkpoint / LoRA / VAE fingerprint.
- `vram_allocated`: VRAM consumed during run.
- `duration_ms`: Total execution time.
- `status`: SUCCESS / FAILED / ROLLBACK.
