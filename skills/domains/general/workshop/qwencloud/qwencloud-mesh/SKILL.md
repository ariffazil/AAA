---
name: qwencloud-mesh
description: "QwenCloud AGI/ASI Meta-Mesa orchestrator."
version: 1.0.0
author: hermes-curator
license: MIT
metadata:
  hermes:
    category: AGI
    tags: [qwencloud, meta-mesa, agi, asi, text, vision, image, video, tts, deploy, billing, mesh]
    related_skills: [qwencloud-cli, qwen-harness-tools, qwen-token-plan-team-edition, tokenrouter-guide, AGI-skill-unification]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# QwenCloud AGI/ASI Meta-Mesa Skill

Unified entry point for ALL QwenCloud capabilities. Routes intent to the right execution skill, references canonical script paths, and integrates with the Hermes skill mesh.

## Architecture

```
User intent
    ↓
qwencloud-mesh (this skill) ← classifies intent
    ↓
┌────────────────────────────────────────────────────────────┐
│  TEXT / CHAT / CODE        → qwencloud-text/scripts/text.py │
│  VISION / OCR / ANALYZE    → qwencloud-vision/scripts/*.py │
│  IMAGE GENERATION / EDIT   → qwencloud-image-generation/scripts/image.py │
│  VIDEO GENERATION / EDIT   → qwencloud-video-generation/scripts/*.py │
│  TTS / SPEECH SYNTHESIS    → qwencloud-audio-tts/scripts/tts.py │
│  MODEL SELECTION / PRICING → qwencloud-model-selector (advisory) │
│  AUTH / BILLING / SUBS     → qwencloud CLI (qwencloud *)  │
│  DEPLOYMENT                → qwencloud-deploy (alibaba cloud) │
└────────────────────────────────────────────────────────────┘
    ↓
Python scripts use $DASHSCOPE_API_KEY (from kunci-root.env)
CLI uses OAuth device flow (separate from API key)
```

## Execution Skill Paths (Canonical)

All Python scripts live under `/root/.agents/skills/`. These are the canonical execution paths:

| Capability | Script Path | Auth Required |
|---|---|---|
| Text/chat/code/reasoning | `/root/.agents/skills/qwencloud-text/scripts/text.py` | $DASHSCOPE_API_KEY |
| Vision/OCR/analysis | `/root/.agents/skills/qwencloud-vision/scripts/analyze.py` | $DASHSCOPE_API_KEY |
| Vision OCR specific | `/root/.agents/skills/qwencloud-vision/scripts/ocr.py` | $DASHSCOPE_API_KEY |
| Vision reasoning | `/root/.agents/skills/qwencloud-vision/scripts/reason.py` | $DASHSCOPE_API_KEY |
| Image generation (t2i) | `/root/.agents/skills/qwencloud-image-generation/scripts/image.py` | $DASHSCOPE_API_KEY |
| Image editing | `/root/.agents/skills/qwencloud-image-generation/scripts/image.py` | $DASHSCOPE_API_KEY |
| TTS (Qwen) | `/root/.agents/skills/qwencloud-audio-tts/scripts/tts.py` | $DASHSCOPE_API_KEY |
| TTS (CosyVoice) | `/root/.agents/skills/qwencloud-audio-tts/scripts/tts_cosyvoice.py` | $DASHSCOPE_API_KEY |
| CLI auth/billing/models | `qwencloud` (global npm install) | OAuth device flow |

## Skill Reference Files (On Demand)

Each execution skill has reference docs. Load only when default script path fails or details needed:

| Skill | References Dir |
|---|---|
| qwencloud-text | `/root/.agents/skills/qwencloud-text/references/` |
| qwencloud-vision | `/root/.agents/skills/qwencloud-vision/references/` |
| qwencloud-image-generation | `/root/.agents/skills/qwencloud-image-generation/references/` |
| qwencloud-video-generation | `/root/.agents/skills/qwencloud-video-generation/references/` |
| qwencloud-audio-tts | `/root/.agents/skills/qwencloud-audio-tts/references/` |
| qwencloud-model-selector | `/root/.agents/skills/qwencloud-model-selector/references/` |
| qwencloud-ops-auth | `/root/.agents/skills/qwencloud-ops-auth/references/` |
| qwencloud-usage | (CLI-based, no references dir) |

## Intent Classification & Routing

### TEXT ROUTE — text.py
**When:** User asks to chat with Qwen, generate text, write code, translate, reason, use function calling.
**Command pattern:**
```bash
python3 /root/.agents/skills/qwencloud-text/scripts/text.py \
  --model <MODEL> \
  --prompt "user message" \
  [--system "system prompt"] \
  [--stream]
```
**Default model:** `qwen3.6-plus` (flagship, balanced cost/perf/speed)
**See:** `cat /root/.agents/skills/qwencloud-text/references/prompt-guide.md`

### VISION ROUTE — analyze.py / ocr.py / reason.py
**When:** User asks to understand images, OCR, chart analysis, video understanding.
**Command pattern:**
```bash
# Analysis
python3 /root/.agents/skills/qwencloud-vision/scripts/analyze.py \
  --model <MODEL> \
  --image "url_or_path" \
  --prompt "what to analyze"

# OCR
python3 /root/.agents/skills/qwencloud-vision/scripts/ocr.py \
  --model <MODEL> \
  --image "url_or_path"
```
**Default model:** `qwen-vl-plus` or `qwen3-vl-32b-thinking`
**See:** `cat /root/.agents/skills/qwencloud-vision/references/api-guide.md`

### IMAGE GENERATION ROUTE — image.py
**When:** User asks to generate images, create posters, product photos, artistic designs, edit/transform images, apply style transfer.
**Command pattern:**
```bash
# Text-to-image
python3 /root/.agents/skills/qwencloud-image-generation/scripts/image.py \
  --mode t2i \
  --model wan2.6-t2i \
  --prompt "description" \
  [--aspect_ratio "1:1"] \
  [--save path.png]

# Image editing
python3 /root/.agents/skills/qwencloud-image-generation/scripts/image.py \
  --mode image-edit \
  --model wan2.7-image-pro \
  --prompt "edit instruction" \
  --reference_images img1.png img2.png \
  [--save output.png]
```
**Default models:** `wan2.6-t2i` (t2i), `wan2.7-image-pro` (editing)
**See:** `cat /root/.agents/skills/qwencloud-image-generation/references/prompt-guide.md`

### VIDEO GENERATION ROUTE
**When:** User asks to generate video from text, animate images, edit video.
**Skill:** `/root/.agents/skills/qwencloud-video-generation/`
**Load the SKILL.md for mode/model selection — video has complex async workflow.**

### TTS ROUTE — tts.py / tts_cosyvoice.py
**When:** User asks to convert text to speech, create voiceovers, read aloud.
**Command pattern:**
```bash
# Qwen TTS (recommended)
python3 /root/.agents/skills/qwencloud-audio-tts/scripts/tts.py \
  --model qwen3-tts-flash \
  --text "speech content" \
  [--voice Cherry] \
  [--save output.wav]

# CosyVoice (higher quality, requires dashscope SDK)
python3 /root/.agents/skills/qwencloud-audio-tts/scripts/tts_cosyvoice.py \
  --model cosyvoice-v3-flash \
  --text "speech content" \
  [--voice longanyang] \
  [--save output.wav]
```
**Default:** `qwen3-tts-flash` via `tts.py`
**Available voices:** Cherry, Ethan, Serena (Qwen TTS); longanyang, longanhuan, longhuhu_v3 (CosyVoice)

### MODEL SELECTION ROUTE (Advisory)
**When:** User asks which model to use, compares pricing, needs recommendation.
**Method:** Load `/root/.agents/skills/qwencloud-model-selector/SKILL.md` and follow the diagnostic flow.
**Primary data source:** `qwencloud models list --format json` (CLI).

### AUTH / BILLING / SUBSCRIPTION ROUTE (CLI)
**When:** User asks about account, billing, usage, quota, auth status.
**Method:** Use `qwencloud` CLI. See `/root/.hermes/skills/qwencloud-cli/SKILL.md`.
**Key commands:**
```bash
qwencloud auth status                    # Check auth
qwencloud usage summary                  # Usage overview
qwencloud usage free-tier                # Free tier quota
qwencloud subscription status            # Token Plan status
qwencloud billing summary                # Billing totals
qwencloud billing breakdown              # Per-model costs
qwencloud models list --format json      # All models + quota
```

### DEPLOYMENT ROUTE (Alibaba Cloud International)
**When:** User asks to deploy to cloud.
**Method:** Requires `qwencloud-deploy` skill (install separately: `npx skills add QwenCloud/qwencloud-deploy`).
**Status:** NOT YET INSTALLED. If user requests, guide through install.

## Pre-Execution Checklist (MANDATORY)

Before executing ANY API call:

1. **Auth check:** `source /root/.secrets/kunci-root.env && echo $DASHSCOPE_API_KEY | head -c 10`
   - If not set → STOP. Guide user to get key from https://home.qwencloud.com/api-keys
   - NEVER output the full key. Report only: SET / NOT SET.

2. **Free tier check (quota-aware execution):**
   ```bash
   source /root/.secrets/kunci-root.env && qwencloud usage free-tier --format json
   ```
   - Check if the target model has remaining quota
   - If exhausted → use fallback model or inform user

3. **Token Plan check (for token-plan models):**
   ```bash
   source /root/.secrets/kunci-root.env && qwencloud subscription status --format json
   ```
   - If remainingCredits = 0 → only free-tier models available
   - Inform user before executing

4. **CLI auth check (if using CLI):**
   ```bash
   qwencloud auth status --format json
   ```
   - If not authenticated → run device flow

## Key Compatibility Warning

**Two credential systems — NEVER confuse:**

| System | What it does | Format | Endpoint |
|---|---|---|---|
| API Key (`$DASHSCOPE_API_KEY`) | Call model APIs via Python scripts | `sk-...` | dashscope-intl.aliyuncs.com |
| CLI OAuth session | `qwencloud` CLI commands (billing, models, auth) | Browser device flow | cli.qwencloud.com |

- Coding Plan keys (`sk-sp-...`) **DO NOT WORK** for Python scripts. Standard key only.
- `QWEN_API_KEY` / `BAILIAN_TOKEN_PLAN_API_KEY` from `kunci-root.env` = standard API key.
- `qwencloud` CLI OAuth = separate. Both must be configured independently.

## Quota-Aware Routing (Fallback Chain)

When a preferred model is exhausted, use this fallback:

| Category | Preferred | Fallback 1 | Fallback 2 |
|---|---|---|---|
| Text (flagship) | qwen3.6-plus | qwen3.5-plus | qwen-plus-latest |
| Text (fast/cheap) | qwen3.5-flash | qwen3.6-flash-2026-04-16 | qwen-flash-2025-07-28 |
| Text (reasoning) | qwq-plus | qwen3-vl-235b-a22b-thinking | (ask user) |
| Vision | qwen-vl-plus | qwen3-vl-32b-thinking | qwen3-vl-235b-a22b-thinking |
| Image (t2i) | wan2.6-t2i | wan2.1-t2i-turbo | wan2.2-t2i-flash |
| Image (edit) | wan2.7-image-pro | wan2.7-image | qwen-image-2.0-pro |
| TTS | qwen3-tts-flash | cosyvoice-v3-flash | qwen-audio-3.0-tts-flash |
| Video | wan2.6-t2v | wan2.5-t2v-preview | wan2.1-t2v-plus |
| Embedding | text-embedding-v4 | text-embedding-v3 | (same pool) |
| ASR | qwen3-asr-flash | fun-asr | qwen-audio-3.0-asr-flash |

## Pitfalls

1. **DO NOT** call `qwencloud` CLI for API calls — it's for billing/auth/model-query only.
2. **DO NOT** use `$QWEN_API_KEY` with `qwencloud` CLI commands — CLI uses OAuth, not API key.
3. **DO NOT** output API keys in plaintext — always report SET/NOT SET status only.
4. **DO NOT** run Python scripts without `source /root/.secrets/kunci-root.env` first.
5. **DO NOT** assume model availability — always check free-tier quota before executing.
6. **DO** check quota BEFORE executing expensive operations (image gen, video, TTS).
7. **DO** use `--format json` on CLI commands when parsing output programmatically.
8. **DO** load the specific sub-skill SKILL.md when the default script path fails.

## Relationship to Other Skills

| Skill | Relationship |
|---|---|
| `qwencloud-cli` | Covers `qwencloud` CLI commands (auth, billing, models). This mesh covers the execution scripts. |
| `qwen-harness-tools` | Covers Qwen Token Plan Harness tools (web search, code interpreter). Model capability, not API calls. |
| `qwen-token-plan-team-edition` | Covers the 4 Token Plan seats, IAM grants, OSS signed URLs. Different auth, different tool. |
| `tokenrouter-guide` | Covers model routing in Hermes/OpenCode. Complementary. |
| `AAA-voice-cloning-qwen-cloud` | Covers Qwen voice cloning pipeline. Complementary. |

DITEMPA BUKAN DIBERI.
