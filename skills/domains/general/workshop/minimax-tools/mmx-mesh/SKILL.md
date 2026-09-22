---
name: mmx-mesh
description: "MiniMax AGI/ASI Meta-Mesa orchestrator."
version: 1.0.0
author: hermes-curator
license: MIT
metadata:
  hermes:
    category: AGI
    tags: [minimax, mmx, meta-mesa, agi, asi, text, image, video, speech, music, vision, search, hailuo]
    related_skills: [mmx-cli, minimax-media, minimax-image-gen, minimax-voice-design-prompts, AGI-skill-unification]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# MiniMax AGI/ASI Meta-Mesa Skill

Unified entry point for ALL MiniMax capabilities via `mmx` CLI. Routes intent to the right command, integrates with the Hermes skill mesh.

## Architecture

```
User intent
    ↓
mmx-mesh (this skill) ← classifies intent
    ↓
┌────────────────────────────────────────────────────────────┐
│  TEXT / CHAT / CODE     → mmx text chat                    │
│  IMAGE GENERATION       → mmx image generate               │
│  VIDEO GENERATION       → mmx video generate               │
│  SPEECH / TTS           → mmx speech synthesize            │
│  MUSIC                  → mmx music generate               │
│  VISION / OCR           → mmx vision describe              │
│  WEB SEARCH             → mmx search query                 │
│  QUOTA / BILLING        → mmx quota show                   │
│  AUTH / CONFIG          → mmx auth / mmx config            │
└────────────────────────────────────────────────────────────┘
    ↓
mmx CLI uses $MINIMAX_API_KEY (from kunci-root.env or ~/.mmx/config.json)
```

## Prerequisites

```bash
# CLI installed (v1.0.19 as of 2026-08-26)
mmx --version

# Auth status
mmx auth status

# If not authenticated:
mmx auth login --api-key sk-xxxxx
```

## Auth Status (Current)

- **CLI:** v1.0.19 installed globally
- **Key:** `sk-cp-...` (Coding Plan key in `~/.mmx/config.json`)
- **Region:** global (`api.minimax.io`)
- **Status:** Coding Plan keys do NOT support direct API calls (same pattern as QwenCloud `sk-sp-` keys)
- **Action needed:** Token Plan key required for API calls. Get from https://platform.minimax.io/subscribe/token-plan

## Intent Classification & Routing

### TEXT ROUTE — mmx text chat
**When:** User asks to chat, generate text, write code, reason.
```bash
mmx text chat --message "user:Your prompt here" --output json --quiet
```
**Default model:** MiniMax-M3
**Flags:** `--system`, `--model`, `--max-tokens`, `--temperature`, `--stream`, `--tool`

### IMAGE ROUTE — mmx image generate
**When:** User asks to generate images, posters, designs.
```bash
mmx image generate --prompt "description" --output json --quiet
```
**Default model:** image-01
**Flags:** `--aspect-ratio`, `--n`, `--seed`, `--width`, `--height`, `--prompt-optimizer`, `--out-dir`

### VIDEO ROUTE — mmx video generate
**When:** User asks to generate video from text or image.
```bash
# Blocking (wait for completion)
mmx video generate --prompt "description" --download output.mp4 --quiet

# Non-blocking (get task ID)
mmx video generate --prompt "description" --async --quiet
```
**Default model:** MiniMax-Hailuo-2.3
**Flags:** `--image`, `--last-frame`, `--async`, `--download`, `--poll-interval`
**For MiniMax-H3 (advanced):** Load `h3-video/SKILL.md` from the mmx-cli skill directory.

### SPEECH ROUTE — mmx speech synthesize
**When:** User asks to convert text to speech, create voiceovers.
```bash
mmx speech synthesize --text "speech content" --out output.mp3 --quiet
```
**Default model:** speech-2.8-hd
**Flags:** `--voice`, `--speed`, `--volume`, `--pitch`, `--format`, `--language`, `--subtitles`, `--stream`
**Max:** 10,000 characters per call

### MUSIC ROUTE — mmx music generate
**When:** User asks to generate music, songs, instrumentals.
```bash
mmx music generate --prompt "description" --out output.mp3 --quiet
```

### VISION ROUTE — mmx vision describe
**When:** User asks to understand/analyze images.
```bash
mmx vision describe --image path_or_url --prompt "What is this?" --output json
```

### SEARCH ROUTE — mmx search query
**When:** User asks to search the web via MiniMax.
```bash
mmx search query --q "search terms" --output json --quiet
```

### QUOTA ROUTE — mmx quota show
**When:** User asks about MiniMax usage, billing, remaining quota.
```bash
mmx quota show --output json
```
**Note:** Returns 404 for Coding Plan keys. Requires Token Plan key.

## Agent Flags (Always Use)

| Flag | Purpose |
|---|---|
| `--non-interactive` | Fail fast on missing args |
| `--quiet` | Suppress spinners; stdout is pure data |
| `--output json` | Machine-readable JSON |
| `--async` | Return task ID immediately (video) |
| `--yes` | Skip confirmation prompts |

## Key Compatibility

**Two credential systems — NEVER confuse:**

| System | Format | Purpose | Endpoint |
|---|---|---|---|
| Token Plan API Key | `sk-...` | Direct API calls via mmx CLI | api.minimax.io |
| Coding Plan Key | `sk-cp-...` | Interactive coding tools only (Cursor, Claude Code) | N/A for CLI |

Current key in `kunci-root.env`: `MINIMAX_API_KEY=sk-cp-...` (Coding Plan — does NOT work for mmx CLI API calls).

**To fix:** Get a Token Plan key from https://platform.minimax.io/subscribe/token-plan and update `MINIMAX_API_KEY` in `/root/.secrets/kunci-root.env`.

## Configuration

```bash
# View config
mmx config show

# Set region (auto-detected usually)
mmx config set --key region --value global

# Set default models
mmx config set --key default-text-model --value MiniMax-M3
mmx config set --key default-speech-model --value speech-2.8-hd
mmx config set --key default-video-model --value MiniMax-Hailuo-2.3
```

## Pitfalls

1. **DO NOT** use Coding Plan keys (`sk-cp-`) for mmx CLI — they return 404/401.
2. **DO NOT** confuse MiniMax regions: `global` (api.minimax.io) vs `cn` (api.minimaxi.com).
3. **DO** use `--quiet --output json` for all agent-context calls.
4. **DO** use `--async` for video generation in agent context (avoid blocking).
5. **DO** check `mmx auth status` before any API call.
6. **DO NOT** output API keys in plaintext.

## Relationship to Other Skills

| Skill | Relationship |
|---|---|
| `mmx-cli` | Source SKILL.md from `~/.agents/skills/mmx-cli/`. Full command reference. |
| `minimax-media` | MCP-based MiniMax media generation (alternative to CLI). |
| `minimax-image-gen` | MCP-based MiniMax image generation. |
| `minimax-voice-design-prompts` | Voice design prompts for MiniMax TTS. |
| `qwencloud-mesh` | Parallel mesh for QwenCloud capabilities. |

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | General error |
| 2 | Usage error |
| 3 | Authentication error |
| 4 | Quota exceeded |
| 5 | Timeout |
| 10 | Content filter |

DITEMPA BUKAN DIBERI.
