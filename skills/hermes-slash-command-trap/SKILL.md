---
name: hermes-slash-command-trap
description: "Hermes custom slash command registration — the plugin vs built-in COMMAND_REGISTRY conflict. When /seal, /init, or any custom command fails silently in Telegram, this is the first thing to check. One-shot diagnostic + fix pattern."
tags: [hermes, plugin, commands, troubleshooting, gateway, telegram]
related_skills: [hermes-agent, hermes-telegram-gateway-ops]
---

# Hermes Slash Command Registration Trap

Custom slash commands (/seal, /init, etc.) fail silently when accidentally registered as built-in `CommandDef` entries instead of using the plugin system.

## Trigger

- Telegram slash command appears in the command menu but does nothing when typed
- Gateway log shows: `Plugin '<name>' tried to register command '/<cmd>' which conflicts with a built-in command. Skipping.`
- User reports "/seal fails" or "/init fails" after a recent Hermes modification

## Root Cause

`hermes_cli/plugins.py` line ~562 — `register_command()` checks `resolve_command(name)` and rejects the plugin if a `CommandDef` with the same name exists in `COMMAND_REGISTRY`. The gateway then sees the command as "known" but has no handler → falls through to agent text processing → silent failure.

## The Two Paths

| Command type | Where it belongs | Why |
|---|---|---|
| Upstream Hermes core (`/new`, `/model`, `/help`, `/stop`) | `COMMAND_REGISTRY` in `commands.py` | Core gateway dispatch, cross-platform |
| Profile-specific / federation custom (`/seal`, `/init`) | Plugin in `~/.hermes/plugins/<name>/` | Isolated, no core conflicts, same lifecycle |

## Gateway Dispatch Flow (for reference)

```
Telegram /cmd → Gateway
  1. resolve_command(cmd) → built-in CommandDef? 
     → YES: check _DEDICATED_HANDLERS → specific handlers → catch-all
     → NO: continue
  2. Quick commands (config alias) → redirect
  3. Plugin handler (get_plugin_command_handler) → call it → return
  4. Skill command → load skill → inject into agent
  5. Fall through to agent text processing
```

Step 3 only fires if the plugin successfully registered. If step 1 found a built-in `CommandDef` for the same name, the plugin was never registered → step 3 returns None → fall through.

## Fix

1. Remove the `CommandDef("name", ...)` entry from `COMMAND_REGISTRY` in `hermes_cli/commands.py`
2. Ensure the plugin exists in `~/.hermes/plugins/<name>/` with `__init__.py`, `plugin.yaml`, `manifest.json`
3. Restart gateway: `sudo systemctl restart hermes-gateway`
4. Verify: `journalctl -u hermes-gateway --since "5 min ago" | grep "registered"`

## Plugin Template

```python
# ~/.hermes/plugins/my-command/__init__.py
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def _handle_slash(raw_args: str) -> Optional[str]:
    """Handle /my-command."""
    return "✅ Done"

def register(ctx) -> None:
    ctx.register_command(
        "my-command",
        handler=_handle_slash,
        description="What this command does",
        args_hint="[optional arg]",
    )
    logger.info("my-command plugin registered /my-command")
```

## Verification

```bash
# Check if plugin registered successfully
journalctl -u hermes-gateway --since "5 min ago" | grep -E "registered|plugin.*command"

# Check if conflict still exists  
grep -n "CommandDef.*seal\|CommandDef.*init" /usr/local/lib/hermes-agent/hermes_cli/commands.py
# Should return nothing (removed)
```

## Related

- `hermes-telegram-gateway-ops` — broader Telegram gateway diagnostics
- `hermes-agent` — upstream Hermes documentation (protected, cannot patch)
