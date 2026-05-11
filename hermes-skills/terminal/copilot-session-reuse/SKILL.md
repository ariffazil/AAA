---
name: copilot-session-reuse
description: Reuse Copilot CLI session context across terminal agent calls — avoids losing context built in previous terminal agent calls. Use when Arif asks to "use the same session" or wants to continue from where the last terminal agent left off.
trigger: "Use when: (1) Arif says 'same session', 'reuse session', 'continue from where we left off'; (2) terminal agent needs to build on context from previous terminal agent call; (3) `-p` prompt references something the previous terminal agent did."
author: Hermes
valid_from: 2026-05-09
tags: [copilot, terminal, session, context]
---

# Copilot CLI Session Reuse — Terminal Agent Context Continuity

## The Problem

`delegate_task` with terminal tools spawns a **fresh Copilot session** every time. The new session has no memory of what the previous terminal agent built or found. Context is lost → Bazir builds same things repeatedly.

## The Fix

Use Copilot's native session flags to chain context:

### Pattern 1: Resume Most Recent Session (`--continue`)
```bash
copilot --continue -p "Continue from where we left off — build on the arifOS tool audit findings"
```

### Pattern 2: Resume Specific Session (`--resume`)
```bash
# Find session IDs from the session-state directory
ls -lt ~/.copilot/session-state/ | head -10

# Resume by full UUID
copilot --resume=0cb916db-26aa-40f2-86b5-1ba81b225fd2 -p "Continue the arifOS deploy..."

# Resume by name prefix (7+ hex chars enough)
copilot --resume=0cb916d -p "Continue..."
```

### Pattern 3: Name Sessions for Easy Resume
```bash
# First call — name the session
copilot --name="arifos-deploy" -p "Deploy arifOS to VPS..." --allow-all-tools

# Subsequent calls — resume by name
copilot --resume="arifos-deploy" -p "Continue from the deploy step..." --allow-all-tools
```

## Session State Location
```
~/.copilot/session-state/<uuid>/
  conversation.jsonl      # Full transcript
  session.json            # Metadata (id, name, created_at)
```

## Session Listing
```bash
# List recent sessions (most recent first)
ls -lt ~/.copilot/session-state/ | head -20

# Resume most recent
copilot --continue -p "..."

# Resume specific by name
copilot --resume="arifOS-deploy" -p "..."
```

## Key Flags for Terminal Agents

| Flag | Purpose |
|------|---------|
| `--continue` | Resume the most recent session — USE THIS for "same session" requests |
| `--resume[=<id>]` | Resume by UUID, name, or 7+ char prefix |
| `--name <name>` | Name a session for future resume |
| `--allow-all-tools` | Skip tool permission prompts (required for non-interactive) |
| `--no-ask-user` | Agent works autonomously without asking |
| `-s, --silent` | Silent output (no stats), cleaner for scripting |

## Important Rules

1. **Name sessions** for multi-step tasks so they can be resumed deterministically
2. **`--continue` works for the most recent session** — if Arif wants "the session we just built", use `--continue`
3. **Session state persists** across calls — context from prior turns IS available
4. **Use `--allow-all-tools`** in all non-interactive terminal agent calls to avoid hanging on permission prompts

## Example: arifOS Deploy Chained Session

```bash
# Step 1 — start and name session
copilot --name="arifos-deploy" \
  -p "Run arifOS health check: curl -s http://127.0.0.1:8080/health" \
  --allow-all-tools -s

# Step 2 — continue same session
copilot --resume="arifos-deploy" \
  -p "Deploy the updated arifOS container using docker compose" \
  --allow-all-tools --no-ask-user -s

# Step 3 — continue again
copilot --resume="arifos-deploy" \
  -p "Verify the deploy: curl the /tools endpoint and confirm all 13 tools present" \
  --allow-all-tools -s
```

## When Session Reuse Fails

If `--resume` fails with "session not found":
- The session may have expired or been garbage collected
- Use `ls -lt ~/.copilot/session-state/` to find valid session IDs
- Default retention: ~30 days or until GC'd

---

*Seal: 999 | Ditempa Bukan Diberi*