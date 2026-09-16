# Shadow GPU + ComfyUI Remote Generation — When Free Lanes Suck

**Authored 2026-08-26 after user correction: "Ok why bother have GPU if the image sucks"**

When Arif has an A100 80GB (or similar high-VRAM GPU) reachable via SSH on a remote box (e.g. Hostinger `shadow-gpu` at `117.18.102.47:31624` with `~/.ssh/hostinger_ed25519`, alias `shadow-gpu`), and ComfyUI is running locally there on `:8188`, **prefer that path over MiniMax / Pollinations / MuleRouter free tiers** for quality-sensitive work. Verified: Juggernaut XL v9 on A100 delivers proper fitness-grade realism (sharp Malay phenotype, defined muscle, dramatic lighting) — free lanes deliver generic stock-photo stock.

## When to fire this path

- **Quality matters** — fitness/physique, photorealistic people, lighting-critical scenes
- **GPU is reachable** — `ssh shadow-gpu curl -s http://127.0.0.1:8188/system_stats` returns JSON
- **VRAM free ≥ 8 GB** for SDXL, ≥ 12 GB for Flux

## When NOT to fire this path

- Quick drafts / placeholders / throwaway visuals — free lanes fine
- GPU unreachable or ComfyUI down — fall back to MiniMax Media MCP (always alive)
- Sensitive content (F1 holds regardless of engine — see escalation-trajectory-hold)

## Hand-Rolled Remote Workflow (verified 2026-08-26)

If you can't use `comfyui/scripts/run_workflow.py` over SSH (e.g. because the script isn't installed on the remote box), use this pattern. Three gotchas to know:

### Gotcha 1: Output dir is configurable, not default

The launch flag `--output-directory /home/ubuntu/comfyui-output` overrides the default. Outputs land there, NOT `/home/ubuntu/ComfyUI/output/`. Check the actual `python main.py` launch line in `pgrep -af 'python.*main.py'` to confirm.

### Gotcha 2: `curl --data @file` inside `ssh` reads REMOTE path

If you run `ssh remote curl --data @/tmp/foo.json`, curl reads `/tmp/foo.json` ON THE REMOTE, not your local box. For local-file workflows:
```bash
scp -q local_file.json shadow-gpu:/tmp/remote_file.json
ssh shadow-gpu "curl -X POST http://127.0.0.1:8188/prompt -H 'Content-Type: application/json' --data @/tmp/remote_file.json"
```

### Gotcha 3: Workflow JSON must wrap nodes in `{"prompt": {...}}` envelope

The `/prompt` endpoint expects `{"prompt": {<node_id>: {class_type, inputs}, ...}, "client_id": "<uuid>"}`. Bare node dicts return `{"error": {"type": "no_prompt"}}`. Don't forget the envelope.

## Verified Recipe (Juggernaut XL v9 SDXL, 30 steps)

```bash
# 1. Verify GPU + ComfyUI live
ssh shadow-gpu "curl -s http://127.0.0.1:8188/system_stats" | python3 -c "import json,sys;d=json.load(sys.stdin);print('GPU:',d['devices'][0]['name'],'VRAM free:',round(d['devices'][0]['vram_free']/1e9,1),'GB')"

# 2. Confirm models
ssh shadow-gpu "ls /home/ubuntu/ComfyUI/models/checkpoints/"

# 3. Build API-format workflow JSON locally
# Each node: {"inputs": {...}, "class_type": "..."}
# Required nodes: CheckpointLoaderSimple, CLIPTextEncode (x2: positive + negative),
# EmptyLatentImage, KSampler, VAELoader, VAEDecode, SaveImage

# 4. Wrap in {"prompt": {...}} envelope and scp to remote
scp -q workflow.json shadow-gpu:/tmp/wf.json

# 5. Submit and capture prompt_id
PROMPT_ID=$(ssh shadow-gpu "curl -s -X POST http://127.0.0.1:8188/prompt -H 'Content-Type: application/json' --data @/tmp/wf.json" | python3 -c "import json,sys;print(json.load(sys.stdin)['prompt_id'])")

# 6. Poll /history/<id> until complete (or sleep 20s for 30-step SDXL on A100)
sleep 20
ssh shadow-gpu "ls -la /home/ubuntu/comfyui-output/ | grep <prefix>"

# 7. scp the output back
scp -q shadow-gpu:/home/ubuntu/comfyui-output/<prefix>_00001_.png /tmp/output.png
```

## Performance Baselines (A100 80GB PCIe, SageAttention on)

| Workflow | Steps | Wall time | VRAM |
|---|---|---|---|
| SDXL Juggernaut v9, 1024×1024 | 30 | ~15-20s | ~6 GB |
| SDXL Juggernaut v9 + ControlNet | 30 | ~30s | ~10 GB |
| Flux Dev fp8 | 20 | ~25-30s | ~18 GB |

SageAttention (verify via `pgrep -af 'python.*main.py'` showing `--use-sage-attention`) saves 30-80% vs default on SDXL/Flux. If you don't see that flag, it's not installed — fall back to xformers or default attention.

## User Preference Embedded (2026-08-26)

Arif's correction: "Ok why bother have GPU if the image sucks" → when GPU is reachable and ComfyUI is loaded, USE IT for tasteful fitness/portrait/photoreal work. Free lanes are fine for throwaway drafts but not for deliverable visuals.

## Reference

- ComfyUI workflow JSON API format: see `comfyui/references/workflow-format.md`
- SageAttention installation: see Hermes federation skill `comfyui` (bundled, read-only)
- Remote GPU SSH setup: see `termux-arif-tailscale-ssh` skill
