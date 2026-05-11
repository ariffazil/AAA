---
name: openclaw-reasoning-leak-fix
description: Fix MiniMax reasoning_content leaking as visible text in OpenClaw Telegram output
triggers:
  - reasoning_content appears in Telegram
  - thinking blocks visible in group chat
  - openclaw streaming transport bug
---

# OpenClaw Reasoning Content Leak Fix

## Trigger
MiniMax `reasoning_content` / `<thinking>` blocks appearing as visible text in Telegram output from OpenClaw gateway. Affects A2A AAA group chat clarity.

## Root Cause
In OpenClaw's streaming transport (`openai-transport-stream-*.js`), line ~536 has a fallback for reasoning blocks:

```javascript
// BROKEN — leaks thinking as visible text when model IDs don't match
content.push(isSameModel ? block : { type: "text", text: block.thinking });
```

When MiniMax M2.7 returns `reasoning_content` with a model identifier that doesn't exactly match the request model, this fallback converts the thinking block to a user-visible `text` content block. The `thinking: { type: "disabled" }` wrapper is ignored by MiniMax M2.7.

## Fix

**File:** `/root/.openclaw/plugin-runtime-deps/openclaw-2026.4.29-4eca5026e977/dist/openai-transport-stream-aPa0aR5w.js`
**Line:** ~536

```javascript
// FIXED — silently drop thinking for non-same-model
if (isSameModel) content.push(block);
// Non-same-model: thinking content dropped silently
```

**Hermes Agent** (`/root/.hermes/venv/lib/python3.13/site-packages/run_agent.py`): Already clean — `_strip_think_blocks()` at line 2700 strips `` from `final_response`; `reasoning_content` stored in separate `msg["reasoning_content"]` field not displayed by downstream consumers. No patch needed.

## Verification
```bash
# Gateway health
curl -s http://127.0.0.1:18789/health

# Channel probe
openclaw channels status --probe
# Expected: Telegram connected, mode:polling, running

# Restart after patch
systemctl --user restart openclaw-gateway
```

## Gotchas
- `thinking: { type: "disabled" }` in the request payload does NOT work for MiniMax M2.7 — the `reasoning_content` still streams regardless
- The fix preserves thinking blocks for same-model responses (internal processing), only drops cross-model leaked thinking
- OpenClaw streaming patch covers both standalone and embedded (Hermes-inside-OpenClaw) paths
- If `/tmp/openclaw/openclaw-*.log` is empty, check `journalctl --user -u openclaw-gateway -n 50` for crash details

## Related
- Exit 78 on restart = orphan process holding port 18789 — kill it first with `kill <PID>`
- Telegram "audit failed" = expected (non-HTTPS), not a functional blocker
