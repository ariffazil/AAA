# RunPod Agent Setup — Verified Transcript (2026-08-10)

## Source
`https://docs.runpod.io/agent-setup.md` — official RunPod documentation.

## Steps Executed

### 1. Skills install (partially succeeded)
```bash
npx -y skills add runpod/runpod-plugins-official --skill '*' --yes --global
```
- **Result:** 4 of 6 skills copied to `~/.agents/skills/` (runpod, runpod-mcp, runpodctl, runpod-usage)
- **Failure:** `flash` and `companion-clis` failed: "PromptScript does not support global skill installation"
- **Fix:** Clone repo and copy manually:
  ```bash
  cd /tmp && git clone --depth 1 https://github.com/runpod/runpod-plugins-official.git
  cp -r /tmp/runpod-plugins-official/plugins/runpod/skills/flash ~/.agents/skills/
  cp -r /tmp/runpod-plugins-official/plugins/runpod/skills/companion-clis ~/.agents/skills/
  ```

### 2. Symlink into Hermes skill mesh
```bash
cd /usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/
for skill in runpod runpod-mcp runpod-usage runpodctl flash companion-clis; do
  ln -sfn ~/.agents/skills/$skill ./$skill
done
```
- **Result:** All 6 skills in Hermes mesh ✓

### 3. MCP server (OAuth required — user step)
```bash
hermes mcp add runpod --url https://mcp.getrunpod.io/ --auth oauth
```
- **Result:** 401 Unauthorized (expected — OAuth is browser sign-in)
- **Action needed:** User runs `hermes mcp login runpod` and completes OAuth in browser

### 4. runpodctl CLI — deferred (on-demand per RunPod docs)
The docs say: "Skills install the Runpod CLI and Flash SDK later, on demand, the first time a task needs them — do not install those now."
CLI installs automatically via the `runpodctl` skill when first used.

## Pod Economics (verified 2026-08-10)

| GPU | Cost/hr | VRAM | Best for |
|---|---|---|---|
| **H200 SXM** | $4.60/hr (per-ms) | 141GB | Video models ≥30GB, 70B+ LLM, multi-model batch |
| **A100 80GB** community | $1.19/hr | 80GB | Image gen, Flux, medium LLM — BEST VALUE |
| **A100 80GB** secure | $1.64/hr | 80GB | Same + security isolation |
| **L40S** | ~$0.50/hr | 48GB | SD1.5/SDXL image gen — CHEAPEST viable |
| **T4** | ~$0.12/hr | 16GB | SD1.5 only, light work |

Storage: network volume $0.005/hr ($3.6/mo) — always-on persistent model store.
Container disk: $0.004/hr (~$2.9/mo) for 80GB.
Billed per millisecond — stop when idle = ~$0 GPU cost.

## Pending User Steps (as of 2026-08-10)
1. **OAuth sign-in** → browser flow for hosted MCP at `mcp.getrunpod.io`
2. **API key** → RunPod dashboard → Settings → API Keys → provide key (add to `kunci-mas.env` as `RUNPOD_API_KEY`)
3. **Pod deployment** → choose GPU tier; deploy; report endpoint/IP
4. **Pod lifecycle** → RUN only when generating; STOP when idle; never run 24/7 unless actively generating

## Pod Config — Arif's Selection (2026-08-10)
- RunPod PyTorch 2.8.0, 1x H200 SXM, 141GB VRAM, 188GB RAM, 12 vCPU
- CUDA 12.8/13.0, 80GB disk, network volume attached
- $4.60/hr total (billed per ms)

**Judgment:** H200 overkill for image-only work (use A100 at 1/4 price). Justified ONLY if running Wan 2.2 (30GB) video model, Hunyuan, or 70B+ LLM. For worship visuals = A100 sufficient.
