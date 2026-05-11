---
name: mmx
description: Full multimodal generation via MiniMax CLI (mmx). Covers text chat, image generation, video synthesis, TTS speech, music composition, vision analysis, and web search. ACTIVATES ON EVERY IMAGE ANALYSIS REQUEST from Arif. Prerequisites: mmx auth login with API key. NOT for deep research loops (use mmx-text-researcher skill instead).
metadata: {"openclaw": {"emoji": "🎨", "requires": {"bins": ["mmx"]}}}
setup_needed: true
user-invocable: true
---

## 🚨 CRITICAL: Vision Analysis — MANDATORY EXEC PATH

**When Arif sends a photo, screenshot, or asks about any image — you MUST use this pipe:**

```bash
mmx vision describe --image <file-path-or-url> --prompt "<Arif's question>"
```

**Verified working syntax (mmx 1.0.12):**
```
mmx vision describe --image /tmp/vision.jpg --prompt "What is shown?"
mmx vision describe --image https://example.com/img.jpg --prompt "What breed?"
mmx vision describe --image /tmp/geo.jpg --prompt "What formation is this?"
```

**Example flow:**
1. Arif sends photo → "what's in this image?"
2. Save the image to a temp path (e.g. /tmp/vision.jpg)
3. Call: `exec(command="mmx vision describe --image /tmp/vision.jpg --prompt 'What is shown in this image?'", timeout=30)`
4. Parse JSON stdout → return the `"content"` field as your answer

**The mmx vision CLI is pre-authenticated. Do NOT try any other path. This is the only correct vision pipe.**

**Quick test:**
```bash
exec(command="mmx vision describe --image /tmp/test.jpg --prompt 'What is this?'", timeout=30)
**The mmx vision CLI is pre-authenticated. Do NOT try any other path. This is the only correct vision pipe.**

**⚠️ FALLBACK GOTCHA — IF vision_analyze FAILS:**
If `vision_analyze` returns "no image attached" or similar error, **do NOT retry it**. Directly use terminal to call mmx:
```bash
cp /root/.hermes/cache/images/<uuid>.jpg /tmp/vision.jpg
mmx vision describe --image /tmp/vision.jpg --prompt "<question>"
```
This works when vision_analyze fails. Tested 2026-05-08: vision_analyze consistently returned "no image attached" for local VPS files, but mmx CLI via terminal succeeded every time.

**DO NOT USE these tools for local image analysis:**
- `vision_analyze` — broken pipe, does not call mmx for local files
- `image` tool with local file paths — path restrictions will cause failure

**ONLY use:** `exec(command="mmx vision describe --image <path> --prompt '<question>'", timeout=30)`

**Quick test you can run anytime:**
```bash
exec(command="mmx auth status", timeout=10)
```


# MMX — MiniMax Multimodal CLI

## ⚠️ CRITICAL: Wrong Package Trap

**`minimax-mcp` (pip) ≠ `mmx-cli` (npm)** — completely different packages:
- `minimax-mcp` on PyPI = Claude config helper, **NOT** the CLI ❌
- `mmx-cli` on npm = Actual MiniMax CLI, installs as `mmx` binary ✅
- `pip install mmx` → fails (no such package)
- `npm install @minimax/mmx` → fails (not in registry)
- **Fix:** `npm install -g mmx-cli`

For deep research workflows, use `mmx-text-researcher` skill instead.

## Auth Check (First)

```bash
mmx auth status
# If not authenticated:
mmx auth login --api-key <your-api-key>
# Check region:
mmx config show
```

## Text Chat

```bash
# Basic
mmx text chat --message "What is MiniMax?"

# Streaming
mmx text chat --model MiniMax-M2.7-highspeed --message "Hello" --stream

# With system prompt
mmx text chat --system "You are a coding assistant" --message "Fizzbuzz in Go"

# Multi-turn (conversation history)
mmx text chat --message "user:Hi" --message "assistant:Hey!" --message "How are you?"

# JSON output
mmx text chat --message "Extract key facts as JSON" --output json

# From file
cat messages.json | mmx text chat --messages-file - --output json
```

### Models
- `MiniMax-M2.7` — standard
- `MiniMax-M2.7-highspeed` — faster response
- `MiniMax-Text-01` — best for research/synthesis

## Image Generation

```bash
# Simple
mmx image "A cat in a spacesuit"

# With options
mmx image generate --prompt "A cat" --n 3 --aspect-ratio 16:9

# Output to directory
mmx image generate --prompt "Logo" --out-dir ./out/

# Available aspect ratios: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
```

## Video Generation

```bash
# Async (start and track)
mmx video generate --prompt "Ocean waves at sunset"

# Async with progress tracking
mmx video generate --prompt "A robot painting" --async

# Get task status
mmx video task get --task-id <task-id>

# Download completed video
mmx video download --file-id <file-id> --out video.mp4
mmx video generate --prompt "Ocean waves at sunset" --download sunset.mp4
```

## Speech / TTS

```bash
# Basic synthesis
mmx speech synthesize --text "Hello!" --out hello.mp3

# Streaming playback (pipe to mpv)
mmx speech synthesize --text "Stream me" --stream | mpv -

# Voice selection + speed
mmx speech synthesize --text "Hi" --voice English_magnetic_voiced_man --speed 1.2

# List available voices
mmx voices

# From stdin
echo "Breaking news" | mmx speech synthesize --text-file - --out news.mp3
```

## Music Generation

```bash
# With lyrics
mmx music generate --prompt "Upbeat pop" --lyrics "[verse] La da dee, sunny day" --out song.mp3

# Auto-generate lyrics from prompt
mmx music generate --prompt "Indie folk, melancholic, rainy night" --lyrics-optimizer --out song.mp3

# Instrumental (no vocals)
mmx music generate --prompt "Cinematic orchestral" --instrumental --out bgm.mp3

# Cover (generate cover from reference audio)
mmx music cover --prompt "Jazz, piano, warm female vocal" --audio-file original.mp3 --out cover.mp3

# Cover from URL
mmx music cover --prompt "Indie folk" --audio https://example.com/song.mp3 --out cover.mp3
```

## Vision / Image Understanding

```bash
# Local file — shorthand (uses default prompt "Describe the image.")
mmx vision photo.jpg

# Describe with custom prompt — CORRECT SYNTAX (requires 'describe' subcommand)
mmx vision describe --image photo.jpg --prompt "What breed?"
mmx vision describe --image /tmp/screenshot.png --prompt "What is shown in this screenshot?"
mmx vision describe --image https://example.com/img.jpg --prompt "What breed?"

# From file-id (pre-uploaded)
mmx vision describe --file-id file-123 --prompt "Extract all text"
```

## Web Search

```bash
# Basic
mmx search "MiniMax AI"

# Structured JSON output
mmx search query --q "latest news" --output json
```

## Utility

```bash
# Check quota
mmx quota

# Show config
mmx config show

# Set region (global or cn)
mmx config set --key region --value cn

# Set default model
mmx config set --key default-text-model --value MiniMax-M2.7-highspeed

# Export schema
mmx config export-schema | jq .

# Update CLI
mmx update
mmx update latest
```

## Common Use Cases

| Task | Command |
|---|---|
| Generate image for Arif's geology viz | `mmx image generate --prompt "<description>" --aspect-ratio 16:9 --out-dir ./output/` |
| Create video clip | `mmx video generate --prompt "<scene>" --async` |
| TTS voice message | `mmx speech synthesize --text "<message>" --voice <voice> --out voice.mp3` |
| Compose background music | `mmx music generate --prompt "<mood>" --instrumental --out bgm.mp3` |
| Analyze geology photo | `mmx vision <path-to-image>` |
| Quick fact check | `mmx search "<query>"` |
| Research synthesis | Use `mmx-text-researcher` skill instead |
