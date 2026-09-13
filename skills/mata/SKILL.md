---
name: mata
description: Unified visual intelligence truth-pane for arifOS — before ANY claim about image/video generation or understanding capability (or its absence), run mata. Kills stale-prose lies ("no API key", "quota habis", "404") with live canaries. Covers gemini, minimax (Hailuo video), mimo, kimi, dashscope VL, bailian wan2.7, qwen token-plans, ComfyUI, FED, pollinations. Trigger phrases - "generate image", "generate video", "no vision model", "quota habis", "no api key", "can we make video", "which vision model", anything visual-capability-related.
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# MATA — Sebelum cakap takde, tengok dulu (look before claiming absence)

MATA is the federation's single truth surface for visual capability (image gen, video gen, image/video understanding). Canonical map: `/root/AAA/knowledge-graph/MATA.md`.

## The law this skill enforces

Human Zero-Visibility Invariant HARAM-3: never claim a visual lane (or its absence) without a live probe within 24h. Models-list 200 ≠ generation quota. "Not probed" ≠ "exhausted".

## Usage

```bash
set -a; source /root/.secrets/kunci-root.env; set +a
/root/scripts/mata.sh          # pane — one line per lane, verdict + latency
/root/scripts/mata.sh --json   # machine snapshot → ~/.local/share/arifos/mata_last.json
/root/scripts/mata.sh --gen    # adds REAL generation canaries (spends quota — ask first for paid lanes)
```

Agents without shell: read `~/.local/share/arifos/mata_last.json` (check `probed_at` < 24h; if stale, ask a shell-capable agent to re-run).

## Routing quick-table (verify with pane first)

- **Image gen:** bailian wan2.7-image(-pro) → pollinations fallback → ComfyUI local (start if down) → qwen-indiv (check reset)
- **Video gen:** MiniMax-Hailuo-2.3 (3/day, 6s|10s; POST /v1/video_generation → poll query → files/retrieve) → happyhorse-1.1 t2v/i2v/r2v on qwen-indiv → Veo (needs gemini prepay top-up = F13 decision)
- **Understanding (img/video in):** mimo-v2.5 omni → zai-vision (GLM-5.3-Flash / @z_ai/mcp-server) → MiniMax-M3 → k3 (resolve 401 first) → gemini family (video-native, canary-verified)
- **OCR:** zai-vision (extract_text_from_screenshot / GLM-5.3-Flash) / M3 / mimo-v2.5 (dashscope VL fleet = 403 dead until payment-info wall resolved)

## Scars baked in (read MATA.md §Scars before extending)

1. Models-list trap (gemini: auth 200, gen 429)
2. Console-redaction stub keys (13-char `sk-cp-…` ≠ key — sweep sibling env vars)
3. Wrong-path 404s (probe endpoint variants with empty-body POST: 400/200 = EXISTS)
4. SOT staleness (anything `last_verified` > 7d = STALE)
