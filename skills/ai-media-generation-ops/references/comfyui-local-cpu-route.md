# Local ComfyUI CPU route — verified 2026-08-15

Session-proven facts from the 2026-08-15 test session (Arif: "aku sanggup
tunggu 10 minit kalau free").

## Install state (pre-existing, discovered not built)

- `/root/comfy/ComfyUI` — clone from 2026-08-10, venv at `.venv/`,
  torch CPU (2.12/2.13), ComfyUI 0.31.0.
- One checkpoint: `models/checkpoints/v1-5-pruned-emaonly.safetensors` (4.0GB
  vanilla SD1.5). No custom nodes.
- No comfy-cli on this box — launch the venv python directly.

## Start / stop

```bash
# Start (background, terminal background=true)
cd /root/comfy/ComfyUI && .venv/bin/python main.py --cpu --listen 127.0.0.1 --port 8188 --use-split-cross-attention

# Verify
curl -sf -m 3 http://127.0.0.1:8188/system_stats

# Stop — ALWAYS kill after use (holds ~2.5GB RAM; earlyoom will SIGKILL it
# under memory pressure mid-render otherwise)
# (kill the background session / pid owning :8188)
```

## Measured performance (8-core box, 31GB RAM, shared with 77 services)

| Metric | Value |
|---|---|
| 512×512, 20 steps, euler | **13:35** (idle-ish box) / **15:11** (box also running another job) |
| Per-step | 36–50 s/it depending on contention |
| RAM | ~2.4–2.5GB for the render process |
| CPU | 220–256% (2+ cores); load spikes 10–12 |
| Boot to listening | ~4–6 s (warm page cache) |

## The two renders

1. **SFW flex test** — "extremely muscular bodybuilder flexing double biceps,
   malay southeast asian, gym shorts, golden hour" → good quality, no
   artifacts, but face rendered East Asian (SD1.5 weakness on SEA faces).
2. **NSFW test** — explicit "full frontal nudity" prompt → **server accepted
   the prompt with zero filtering** (no refusal, no safety error), but the
   OUTPUT reframed itself: shirtless torso shot, frame squared off at the
   waist, no explicit anatomy. Vanilla SD1.5's training is the limit, not the
   server.

**NSFW routing conclusion:** local ComfyUI = uncensored *infrastructure*,
censored *model*. Explicit anatomy needs a fine-tuned checkpoint → the RunPod
Pony V6 XL route (see `comfyui-runpod-pipeline.md`) remains the explicit lane.
Local SD1.5 delivers "shirtless sado" fine, nothing more.

## Pitfalls hit in session (burned ~40 min total — read before re-running)

1. **CLIPTextEncode requires the `clip` input wired**: `"clip": ["4", 1]`
   from CheckpointLoaderSimple. Missing it → HTTP 400
   `Required input is missing: clip` + "Output will be ignored" warning.
   The full working node graph is embedded in `scripts/comfy_local_submit.py`.
2. **The HTTP thread starves during sampling.** Polling `/history/{pid}` with
   a 15s timeout returns TimeoutError while the render is perfectly healthy —
   do NOT treat poll failure as render failure. Poll `/queue` with 60–90s
   curl timeouts; pull `/history` only after the queue is empty.
3. **Port 8188 is shared state.** A second `main.py` start while one runs →
   `Port 8188 is already in use` + `comfyui.db` lock error, and the failed
   process still lingers. Always `ss -tlnp | grep 8188` first. A submit can
   land on ANOTHER session's server — status `execution_interrupted` in
   history means that server's owner cancelled/interrupted, not your error.
4. **earlyoom may SIGKILL the render** when box memory is tight (it prefers
   python victims). Symptom: connection refused mid-render, queue gone,
   nothing in /history. Check `journalctl -u earlyoom` before re-attempting.
   Don't stack a local render while other heavy jobs run.
5. **`status: error` in /history ≠ filter.** Read the `status.messages` —
   `execution_interrupted` (cancelled) vs a real node traceback are different
   failure classes.

## Decision rule

- Arif says he'll wait / wants free → this route, ONE render at a time.
- Arif wants it now, or wants quality/SEA faces → Gemini primary route.
- Arif wants explicit → RunPod Pony V6 XL, not local SD1.5.
