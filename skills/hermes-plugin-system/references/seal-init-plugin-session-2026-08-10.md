# /seal and /init Plugin Implementation — Session Transcript

## Date: 2026-08-10

## Problem

`/seal` and `/init` commands were registered in BotFather + `COMMAND_REGISTRY` but failed when tried from Telegram. The commands fell through to the agent as plain text.

## Root Cause (two layers)

### Layer 1: Plugins disabled in config

The `seal-command` and `init-command` plugins existed at the profile plugins path (`/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/`) but were NOT in `plugins.enabled`:

```python
# Before fix
plugins:
  enabled:
    - lane_switch       # ← only this was enabled

# After fix
plugins:
  enabled:
    - lane_switch
    - seal-command       # ← added
    - init-command       # ← added
```

Gateway log showed: `Skipping 'seal-command' (not in plugins.enabled)`

### Layer 2: Command registration conflict (already resolved before this session)

The `CommandDef("seal")` and `CommandDef("init")` in `COMMAND_REGISTRY` blocked plugin registration via the conflict check in `ctx.register_command()`:

```python
# hermes_cli/plugins.py line 564
from hermes_cli.commands import resolve_command
if resolve_command(clean) is not None:
    logger.warning("Plugin '%s' tried to register command '/%s' which conflicts...")
    return  # ← registration rejected
```

The CommandDefs had already been removed before this session, so the plugins could register — they just weren't enabled.

## Seal Plugin Architecture

### What was wrong (original)

The original seal plugin called `forge_vault` at A-FORGE :7072. This returns `-32042 URLElicitationRequiredError` without sovereign ACT/sct.

### What was fixed

Rewrote to:
1. Build receipt from `carry_forward.json` state
2. Save locally (always succeeds)
3. Report honestly that VAULT999 seal requires sovereign authorization
4. No fake vault calls

### VAULT999 auth wall (confirmed)

Both lanes require sovereign authentication:

```
Lane A: arif_seal :8088 → 888_HOLD: IRREVERSIBLE requires non-anonymous actor_id
Lane B: forge_vault :7072 → -32042 URLElicitationRequiredError
```

DID registry has `did:arif:hermes` but the plugin uses `actor_id: "hermes-AAA-warga"` which doesn't match → treated as anonymous.

## Init Plugin

Simple probe plugin — calls health endpoints via curl:
- arifOS :8088/health
- A-FORGE :7072/health  
- arifFlow :7073/health

Loads `carry_forward.json` for FQ state. No auth required (read-only probes).

## Key Files

| File | Purpose |
|---|---|
| `/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/seal-command/__init__.py` | Seal plugin (rewritten) |
| `/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/init-command/__init__.py` | Init plugin (existing) |
| `/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/seal-command/plugin.yaml` | Seal manifest |
| `/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/init-command/plugin.yaml` | Init manifest |
| `/usr/local/lib/hermes-agent/hermes_cli/commands.py` | COMMAND_REGISTRY (seal/init removed) |
| `config.yaml → plugins.enabled` | Plugin activation gate |

## Verification

```bash
# Confirm plugins register
python3 -c "
from hermes_cli.plugins import discover_plugins, get_plugin_commands
discover_plugins()
print(list(get_plugin_commands().keys()))
# → ['init', 'seal']
"

# Test init handler
python3 -c "
from hermes_cli.plugins import discover_plugins, get_plugin_command_handler
discover_plugins()
print(get_plugin_command_handler('init')(''))
# → ✅ arifOS | ✅ A-FORGE | ✅ arifFlow
# → FQ: unknown
# → Session initialized.
"

# Test seal handler  
python3 -c "
from hermes_cli.plugins import discover_plugins, get_plugin_command_handler
discover_plugins()
print(get_plugin_command_handler('seal')('test note'))
# → 📋 RECEIPT PREPARED — ...
# → Status: Receipt saved locally.
# → VAULT999 seal requires sovereign authorization (F13 ACT).
"
```
