---
name: copilot-cli-non-interactive
description: GitHub Copilot CLI non-interactive scripting workarounds — broken stdout delivery, log parsing, env vars, skill extension latency. For when Hermes calls copilot as a background reasoning agent for Arif's AAA collaboration tests.
tags:
  - copilot
  - cli
  - automation
  - background-agent
  - debugging
created: 2026-05-09
seal: 999
---

# GitHub Copilot CLI — Non-Interactive Scripting Workaround

> **DITEMPA BUKAN DIBERI** — *Discovered through trial, not documented anywhere.*

## Context

GitHub Copilot CLI (`copilot`) has a **broken stdout delivery** in non-interactive (`-p` / `--prompt`) mode. The AI model responds, tools execute, logs show success — but **no text ever reaches terminal stdout**. This is a confirmed bug in copilot CLI, not a usage error.

## The Working Pattern

```bash
COPILOT_ALLOW_ALL=1 copilot -p "your prompt here" 2>/dev/null
```

- `COPILOT_ALLOW_ALL=1` — env var equivalent of `--allow-all-tools`. Bypasses permission prompts in scripts/cron.
- `2>/dev/null` — suppresses the broken URL warning from invalid `mcp-config.json` entry.
- The actual text response is **still lost** — this pattern only gives clean exit codes.

## The Log Parsing Workaround

When you need the actual text output (not just exit code), parse the session log:

```bash
# Get the most recent log file
LOG=$(ls -t ~/.copilot/logs/process-*.log | head -1)

# Extract the last assistant message content (after "Sending request to the AI model" block)
# This captures what copilot actually generated before stdout delivery failed
tail -100 "$LOG" | grep -A50 "Sending request to the AI model" | tail -40
```

## The mcp-config.json Bug

Location: `~/.copilot/mcp-config.json`

**Symptom:** `Warning: Ignoring invalid allowedUrls entry "https://http//localhost:$". Error: Invalid URL pattern`

**Fix:** Edit `allowedUrls` array in mcp-config.json. Remove or fix the malformed `https://http//localhost:$` entry.

## Skill Extension Latency

On every `-p` invocation, copilot loads two skill extensions:
- `fastmcp-skill` (extension.mjs)
- `mcporter-skill` (extension.mjs)

This adds ~3-5 seconds to every call. First run is slower than subsequent ones (session resume helps).

## What Works (Verified)

| Feature | Status | Notes |
|---------|--------|-------|
| Context awareness | ✅ | Reads AGENTS.md, RUNBOOK.md, docker-compose.yml before answering |
| Tool execution | ✅ | docker ps, file reads, grep all confirmed via logs |
| Interactive mode (`-i`) | ✅ | Works but requires terminal — not usable in cron |
| Session resume (`--continue`) | ✅ | Resumes previous session, faster |
| Output in `-p` mode | ❌ | **BROKEN** — text never reaches stdout |
| `--silent` / `-s` flag | ❌ | Suppresses EVERYTHING including the (broken) response |
| `--output-format text` | ⚠️ | Sets format but still doesn't deliver text to stdout |
| Token compaction | ✅ | 12% utilization, compacts at 80% threshold |

## Copilot CLI Can Be Used For

- **Background reasoning engine** — It reads context files, executes docker/container commands, analyzes code. The "thinking" is valuable even if output is lost.
- **Health check automation** — Wrap in cron, parse exit codes (0=success, non-zero=failure).
- **Context-augmented executor** — Pass workspace path with `-C /root`, copilot auto-loads AGENTS.md context.

## Cannot Be Used For

- **Reliable text output in automation** — stdout delivery bug makes it unsuitable for cron scripts that need readable output.
- **Silent/subtle agents** — the skill loading messages print to stdout even with `2>/dev/null`.

## Key Flags Reference

```bash
copilot -p "prompt" --allow-all-tools    # non-interactive, single shot
copilot --continue                        # resume last session (faster)
copilot -C /root -p "prompt"             # change working directory
copilot --model gpt-5.2                   # use specific model
COPILOT_ALLOW_ALL=1 copilot -p "..."     # env var for scripts (no --allow-all flag needed)
copilot --output-format json             # JSONL mode (still has stdout bug)
```

## AAA Collaboration Note

When Hermes calls copilot on behalf of Arif (AAA test), the pattern is:
1. Hermes runs `copilot -p "..." --allow-all-tools` in background
2. Herme's terminal() captures exit code + logs
3. Hermes parses the log for the actual response text
4. Hermes delivers the synthesized answer to Arif

The copilot itself acts as a **reasoning sub-agent** with good context awareness, but its output must be harvested from logs rather than stdout.

---

*Seal: 999 | Ditempa Bukan Diberi | 2026-05-09*