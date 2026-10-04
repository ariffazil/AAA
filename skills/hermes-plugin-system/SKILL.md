---
name: hermes-plugin-system
description: "Operate the Hermes Agent plugin system — plugin discovery, enablement, command registration, gateway dispatch, and the VAULT999 auth wall for governance commands. Use when: creating a new slash command plugin, debugging why a plugin isn't loading, understanding plugin→gateway command dispatch, or building governance commands (/seal, /init) that interact with arifOS kernel."
tags: [hermes, plugins, gateway, slash-commands, governance]
---

# Hermes Plugin System

Operating the Hermes Agent plugin system — how plugins are discovered, enabled, register slash commands, and get dispatched by the gateway.

## Plugin Discovery Paths

Plugins are scanned from TWO locations (profile-aware):

| Path | Scope | Notes |
|---|---|---|
| `~/.hermes/plugins/` | Global (default profile) | Only if `HERMES_HOME` is unset |
| `$HERMES_HOME/profiles/<name>/plugins/` | Profile-specific | **Active path for profiled installs** |

The gateway logs which path it scans: `Scanning user plugins: <path>`. A plugin placed in the wrong path is silently invisible.

## The `plugins.enabled` Gate

**Plugins NOT in `plugins.enabled` config are silently skipped.** Even with valid `plugin.yaml` + `__init__.py` + `register(ctx)`, the plugin will NOT load. The gateway log shows: `Skipping '<name>' (not in plugins.enabled)`.

```bash
# Check current enabled list
python3 -c "from hermes_cli.config import load_config; print(load_config().get('plugins',{}).get('enabled',[]))"

# Enable a plugin
python3 -c "
from hermes_cli.config import load_config, save_config
cfg = load_config()
enabled = cfg.setdefault('plugins', {}).setdefault('enabled', [])
for p in ['my-plugin']:
    if p not in enabled: enabled.append(p)
save_config(cfg)
"
```

## Plugin Directory Structure

```
$HERMES_HOME/profiles/<name>/plugins/<plugin-name>/
  plugin.yaml          # REQUIRED: name, version, description, hooks
  __init__.py          # REQUIRED: register(ctx) function
```

### plugin.yaml

```yaml
name: my-plugin
version: "1.0.0"
description: "What it does"
author: "who"
hooks: []              # Lifecycle hooks (empty = command-only plugin)
```

### register(ctx) — Slash Command Registration

```python
def register(ctx) -> None:
    """Register slash command."""
    ctx.register_command(
        "my-command",                    # without leading slash
        handler=_handle_slash,           # fn(raw_args: str) -> str | None (sync or async)
        description="What it does",
        args_hint="[optional args]",    # shows in Discord native picker
    )
```

Handler signature: `fn(raw_args: str) -> str | None`. Async handlers are supported — the gateway awaits them.

## Command Registration Conflict

If a command name already exists in `COMMAND_REGISTRY` (hermes_cli/commands.py), `ctx.register_command()` **rejects it as a conflict** — silently, with a warning log:

```
Plugin 'my-plugin' tried to register command '/seal' which conflicts with a built-in command. Skipping.
```

**Fix:** Remove the `CommandDef` from `COMMAND_REGISTRY` so the plugin can claim the name. The gateway's `is_gateway_known_command()` checks both built-in AND plugin commands, so plugin-registered commands still get hooks and access control.

## Gateway Command Dispatch Order

```
1. Built-in handlers (if canonical == "new":, "help":, etc.)
2. Quick commands (config.yaml → quick_commands)
3. Plugin commands (get_plugin_command_handler())     ← plugins land here
4. Skill slash commands (/skill-name loads skill)
5. Fall-through to agent (plain text to LLM)
```

Plugin commands fire AFTER all built-ins. If a built-in handler matches the same name, the plugin never runs.

## Gateway Restart from Inside = Blocked

The gateway blocks self-restart (SIGTERM propagation kills the executing command). Use `systemctl restart` from outside. Do NOT try to bypass the guard.

## VAULT999 Seal Authentication Wall

Both Lane A (`arif_seal` at :8088) and Lane B (`forge_vault` at :7072) require sovereign authentication (ACT/sct_v1.*) for irreversible VAULT999 writes. A Telegram `/seal` command **cannot** autonomously seal.

| Lane | Endpoint | Auth Required | Error Without Auth |
|---|---|---|---|
| A (constitutional) | `arif_seal` :8088 | DID + session token | `888_HOLD: IRREVERSIBLE requires non-anonymous actor_id` |
| B (session receipt) | `forge_vault` :7072 | ACT / sct_v1.* | `-32042 URLElicitationRequiredError` |

The correct `/seal` plugin pattern: build receipt → save locally → report to sovereign for authorization. This is F13 governance working correctly, not a bug.

## Debugging Checklist

```bash
# 1. Are plugins enabled?
python3 -c "from hermes_cli.config import load_config; print(load_config().get('plugins',{}).get('enabled',[]))"

# 2. What did the gateway actually load?
python3 -c "
import logging; logging.basicConfig(level=logging.DEBUG)
from hermes_cli.plugins import discover_plugins, get_plugin_commands
discover_plugins()
print('Commands:', list(get_plugin_commands().keys()))
" 2>&1 | grep -E 'Skipping|Registered|Scanning'

# 3. Check gateway logs for plugin loading
grep -i 'plugin\|skip' ~/.hermes/logs/gateway.log | tail -10

# 4. Test a plugin handler directly
python3 -c "
from hermes_cli.plugins import discover_plugins, get_plugin_command_handler
discover_plugins()
h = get_plugin_command_handler('my-command')
if h: print(h('test args'))
else: print('NOT FOUND')
"
```

## Common Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| Plugin not loading | Not in `plugins.enabled` | Add to config |
| `register_command` rejected | Name conflicts with COMMAND_REGISTRY | Remove CommandDef from commands.py |
| Handler never called | Built-in handler matches same name | Check dispatch order |
| `Skipping '<name>' (not in plugins.enabled)` in logs | Config gate | Enable in config |
| Plugin at wrong path | Profile vs global mismatch | Move to `$HERMES_HOME/profiles/<name>/plugins/` |

## Pitfalls

- `plugins.enabled` is the ONLY way to activate a plugin. No auto-discovery.
- Plugin names with underscores are normalized to hyphens for Telegram: `register_command("my_cmd")` matches `/my-cmd` in Telegram.
- The `hooks: []` in plugin.yaml is for lifecycle hooks (pre_tool_call, etc.), NOT slash commands. Slash commands are registered via `ctx.register_command()` in `register()`.
- A plugin's `register()` runs at import time during `discover_plugins()`. If it raises, the plugin is silently skipped.
