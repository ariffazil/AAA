# MiniMax Media MCP Route — Technical Reference

**Added:** 2026-08-19 | **Source:** Session debugging + integration

## Server Details

- **Process:** `/opt/minimax-mcp-media/run_v2.py` (PID managed by systemd or manual start)
- **Port:** 18100 (loopback only)
- **Transport:** streamable-http with SSE responses
- **URL:** `http://127.0.0.1:18100/mcp`
- **MCP server name:** `Minimax` v1.27.2

## Available Tools

| Tool | Description | Cost |
|------|-------------|------|
| `text_to_image` | Generate image from prompt | MiniMax API quota |
| `generate_video` | Generate video from prompt | MiniMax API quota |
| `music_generation` | Generate music from prompt | MiniMax API quota |
| `text_to_audio` | TTS with voice selection | MiniMax API quota |
| `voice_clone` | Clone voice from audio files | MiniMax API quota |
| `voice_design` | Generate voice from description | MiniMax API quota |
| `list_voices` | List available voices | Free |
| `play_audio` | Play audio file locally | Free |

## CLI Wrapper: `agy-image`

**Location:** `/usr/local/bin/agy-image`
**Usage:**
```bash
agy-image "prompt text"                           # basic generation
agy-image "prompt" --out /tmp/custom.jpg          # custom output path
agy-image "prompt" --aspect 16:9                  # landscape
agy-image "prompt" --model image-01               # specify model
agy-image "prompt" --telegram                     # auto-send to Telegram
agy-image "prompt" --json                         # machine-readable output
agy-image "prompt" --telegram --json              # both
agy-image "prompt" --no-optimize                  # skip prompt optimization
```

**Output (stdout):** file path (or JSON with `--json`)
**Logs (stderr):** progress, URL, file size, Telegram status

**Dependencies:** Python 3.10+, `mcp` package (installed at `/usr/local/lib/python3.13/dist-packages/mcp/`)

## MCP Transport Gotchas

1. **Session required:** Raw HTTP POST without MCP session init returns `{"error": "Missing session ID"}`. The Python MCP client handles this automatically.
2. **Headers:** Server expects `Accept: application/json, text/event-stream`. Standard `requests` library without this header gets HTTP 406.
3. **SSE responses:** Server sends Server-Sent Events format (`event: message\ndata: {...}`), not plain JSON.
4. **Session init flow:** `initialize` → `initialized` notification → `tools/call`. The MCP client abstracts this.

## Config Registration

Added to `/root/.hermes/config.yaml` under `mcp_servers`:
```yaml
minimax-media:
  description: MiniMax Media MCP — image gen, video, music, TTS, voice clone
  enabled: true
  transport: streamable-http
  url: http://127.0.0.1:18100/mcp
```

Hermes detects this as a new MCP server and exposes the tools. Requires Hermes restart for live sessions.

## Telegram Delivery

The `agy-image --telegram` flag uses the Telegram Bot API directly:
- Reads `HERMES_TELEGRAM_BOT_TOKEN` from environment (sourced from `kunci-root.env`)
- Falls back to `bash -c 'source ... && echo $HERMES_TELEGRAM_BOT_TOKEN'` for shell expansion
- Sends via `curl -F photo=@file -F chat_id=267378578` (Arif DM)
- Bot token is `ASI_BOT_TOKEN` aliased as `HERMES_TELEGRAM_BOT_TOKEN` (see `kunci-root.env`)

## Known Broken Routes (2026-08-19)

| Route | Status | Issue |
|-------|--------|-------|
| FAL.ai (Hermes built-in `image_gen`) | DEAD | `FAL_KEY` not set in environment |
| Modal/Mage-Flow (`/root/AAA/tools/generate_image.py`) | DEGRADED | Returns static placeholder images (~5KB), real GPU inference broken |
| `agy` binary | N/A | Coding agent (Claude Code clone), NOT image generation |

## Config Editing Pitfall

**NEVER use `yaml.dump()` on `config.yaml`** — strips all comments, reorders keys, destroys documentation context. Use line-by-line Python insertion or `sed` for surgical edits. Always back up first.
