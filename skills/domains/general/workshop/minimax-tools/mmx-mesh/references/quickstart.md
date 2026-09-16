# MiniMax Quickstart — Hermes Commands

Copy-paste ready commands for the most common MiniMax tasks.

## Pre-Flight (ALWAYS RUN FIRST)

```bash
# Check CLI
mmx --version

# Check auth
mmx auth status

# If not authenticated:
source /root/.secrets/kunci-root.env && mmx auth login --api-key "$MINIMAX_API_KEY"
```

## Text Generation (Default: MiniMax-M3)

```bash
mmx text chat --message "user:Write a 4-line poem about AI" --output json --quiet
```

## Image Generation (Default: image-01)

```bash
mmx image generate --prompt "Cyberpunk city night scene, 16:9" --output json --quiet
```

## Video Generation (Default: MiniMax-Hailuo-2.3)

```bash
# Blocking (waits for completion)
mmx video generate --prompt "Ocean waves at sunset" --download /tmp/waves.mp4 --quiet

# Non-blocking (returns task ID)
mmx video generate --prompt "Ocean waves at sunset" --async --quiet
```

## Speech / TTS (Default: speech-2.8-hd)

```bash
mmx speech synthesize --text "Welcome to i-ARIF" --out /tmp/welcome.mp3 --quiet
```

## Music Generation

```bash
mmx music generate --prompt "Upbeat jazz song about summer" --out /tmp/jazz.mp3 --quiet
```

## Vision / Image Understanding

```bash
mmx vision describe --image /path/to/photo.jpg --prompt "What is this?" --output json
```

## Web Search

```bash
mmx search query --q "latest AI news" --output json --quiet
```

## Quota Check

```bash
mmx quota show --output json
# Note: returns 404 for Coding Plan keys
```

## See Also

- `/root/.hermes/skills/mmx-mesh/SKILL.md` — Full meta-mesa skill
- `/root/.agents/skills/mmx-cli/SKILL.md` — Full command reference
- `/root/.npm-global/lib/node_modules/mmx-cli/` — CLI source
