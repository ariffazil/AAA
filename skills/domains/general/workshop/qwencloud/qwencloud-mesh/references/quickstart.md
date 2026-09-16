# QwenCloud Quickstart — Hermes Commands

Copy-paste ready commands for the most common QwenCloud tasks.

## Pre-Flight (ALWAYS RUN FIRST)

```bash
source /root/.secrets/kunci-root.env && \
echo "API_KEY: $([ -n "$DASHSCOPE_API_KEY" ] && echo SET || echo MISSING)" && \
qwencloud auth status --format json 2>&1 | jq -r '.authenticated'
```

## Text Generation (Default: qwen3.6-plus)

```bash
source /root/.secrets/kunci-root.env && \
python3 /root/.agents/skills/qwencloud-text/scripts/text.py \
  --prompt "Explain quantum entanglement in BM Penang"
```

## Image Generation (Default: wan2.6-t2i)

```bash
source /root/.secrets/kunci-root.env && \
python3 /root/.agents/skills/qwencloud-image-generation/scripts/image.py \
  --mode t2i \
  --prompt "A futuristic Penang island skyline at sunset, cyberpunk style" \
  --save /tmp/penang.png
```

## Vision Analysis (Default: qwen-vl-plus)

```bash
source /root/.secrets/kunci-root.env && \
python3 /root/.agents/skills/qwencloud-vision/scripts/analyze.py \
  --image /path/to/image.jpg \
  --prompt "What is in this image?"
```

## TTS (Default: qwen3-tts-flash, voice Cherry)

```bash
source /root/.secrets/kunci-root.env && \
python3 /root/.agents/skills/qwencloud-audio-tts/scripts/tts.py \
  --text "Selamat datang ke sistem i-ARIF" \
  --voice Cherry \
  --save /tmp/welcome.wav
```

## Check Quota (Free Tier)

```bash
source /root/.secrets/kunci-root.env && \
qwencloud usage free-tier --format json | \
  jq '.free_tier[] | select(.quota.remaining > 0 and .model_id | startswith("wan2.6"))'
```

## List Available Models

```bash
source /root/.secrets/kunci-root.env && \
qwencloud models list --format json | jq '.models[].id' | head -30
```

## Billing Summary

```bash
source /root/.secrets/kunci-root.env && \
qwencloud billing summary --from 2026-08-01 --to 2026-08-26
```

## Token Plan Status

```bash
source /root/.secrets/kunci-root.env && \
qwencloud subscription status --format json
```

## CLI Auth (If Expired)

```bash
# Step 1: get URL
qwencloud auth login --init-only --format json

# Step 2: open URL in browser, authorize

# Step 3: complete
qwencloud auth login --complete --format json
```

## See Also

- `/root/.hermes/skills/qwencloud-mesh/SKILL.md` — Full meta-mesa skill
- `/root/.hermes/skills/qwencloud-mesh/references/quota-snapshot.md` — Quota state
- `/root/.hermes/skills/qwencloud-cli/SKILL.md` — CLI ops reference