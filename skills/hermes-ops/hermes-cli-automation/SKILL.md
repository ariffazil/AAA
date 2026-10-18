---
name: hermes-cli-automation
description: "Use when scripting Hermes CLI ops non-interactively."
version: 1.0.0
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Hermes CLI Automation — non-interactive scripting

## The one rule

Interactive `hermes` subcommands that read prompts via `input()` / `getpass` **cannot be piped from
stdin** — a `printf '...\n...\n' | hermes <subcommand>` hits `EOFError` at the first unfed prompt and
drops the rest. Password-type fields never accept stdin at all (by design: the secret must not reach
shell history or the process list).

**To script such a subcommand, call the underlying Python module directly under the harness's own venv:**

```bash
/usr/local/lib/hermes-agent/.venv/bin/python3
```

and import the module the CLI wraps (e.g. `from agent.vault_store import get_vault_store`). Prompt
secrets with `getpass.getpass()` inside the script so they stay hidden. The wrapped module's functions
are the real API; the CLI is a thin interactive wrapper over them.

## Worked example — vault add

`hermes vault add --kind login` is a tty wizard (label → origin → identifier_type → identifier →
password → otp). It cannot be piped. The non-interactive path:

```python
from agent.vault_store import get_vault_store
meta = get_vault_store().add_item(
    kind="login",
    label="...",
    secret={"identifier_type": "email", "identifier": "...", "password": "..."},
    origin="https://accounts.google.com",
)
# meta.id = the handle returned by hermes vault list
```

Live scripts on box (copy/modify, don't reinvent):
- `/root/scripts/vault-add-login.sh` — argv-driven: label, origin, identifier as args; password prompted.
- `/root/scripts/vault-add-google.sh` — auto-fetches the email from the OAuth token, prompts password only.

## Pitfalls

- **Don't put prose inside the thing-to-paste.** A code block meant for one-tap copy must contain ONLY
  the command; explanation goes outside the block (pasting prose runs `sebab: command not found`).
- **`getpass`, not `input`, for any secret field** in a scripted helper — otherwise the value lands in
  shell history / the process list, which is exactly what the interactive wizard's design avoids.
- **Use the harness's own venv python** (`/usr/local/lib/hermes-agent/.venv/bin/python3`), not the
  system python — the `agent.*` modules are only installed there.
