---
name: cross-harness-relay-wiring
description: "Wire a chat room to a coding-agent session."
version: 1.0.0
tags: [hermes, opencode, telegram, relay, plugin, hook]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Cross-harness relay wiring

Use when one harness must drive another across a chat room — a Telegram group
message spawning work in an OpenCode (or sibling CLI) session, and that session's
answer returning to the same room lane.

Three surfaces fail independently and look identical when they do: **inbound hook**,
**harness invocation**, **outbound send**. Wire and verify each one on its own before
blaming the other two.

## 1. Inbound — the plugin

Create `~/.hermes/plugins/<name>/`:

- `plugin.yaml` — `name`, `version`, `description`, and `hooks: [pre_gateway_dispatch]`.
- `__init__.py` — a `register(ctx)` that calls `ctx.register_hook("pre_gateway_dispatch", fn)`,
  guarded by a module-level `_REGISTERED` flag so repeat discovery does not double-register.

## 2. Activate — a directory is not an install

Discovery loads the plugin **disabled**: `enabled: False`, error `not enabled in config`.
Nothing runs. Run:

```
hermes plugins enable <name>
```

The CLI nudges the running gateway itself. Then prove activation, not existence, over the
control socket:

```python
import sys; sys.path.insert(0, "/usr/local/lib/hermes-agent")
from pathlib import Path
from gateway.control_socket import reload_gateway_plugins
r = reload_gateway_plugins(Path("/root/.hermes").resolve())
# require: an entry in r["activations"] whose activated_now.gateway_transforms
# contains the hook. A name in r["plugins"] proves only that it was discovered.
```

## 3. Hook contract

`pre_gateway_dispatch` runs BEFORE auth and before mention checks — the plugin is the only
gate, so allowlist explicit `(chat_id, sender_id)` pairs in a JSON config and return `None`
for everything else.

| return | effect |
|---|---|
| `{"action": "skip"}` | drop the message — use after a successful handoff so the host does not answer too |
| `{"action": "rewrite", "text": ...}` | replace the inbound text |
| `None` / `{"action": "allow"}` | normal dispatch |

Never raise. A hook exception must fall through to normal dispatch, or one bug silences
an entire room. Do the slow work in `threading.Thread(daemon=True)` — a hook that blocks on
a multi-minute subprocess stalls the gateway loop.

## 4. Drive the other harness through its CLI

```
opencode run --session <id> --format json -- "<message>"
```

Emits NDJSON; take lines where `type == "text"` and concatenate `part.text`. Confirm the
session id with `opencode session list` before wiring it into config.

The `opencode serve` port answers `/` with HTML and exposes no REST control surface at
`/session` or `/openapi.json` — probing it returns markup, not state. Do not build on it.

## 5. Reply with a declared destination

```
hermes send --to telegram:<chat_id>:<thread_id> <text>
```

The thread id is mandatory for forum topics; without it the reply lands in a different
lane. The transport lock refuses an inferred target by design — declare it, never work
around it.

## Pitfalls

- **Two triggers, one session id** → two harness processes interleave their output. Serialize
  per session before adding a second caller.
- **Daemon thread dies with the gateway** → replies not yet sent vanish on restart. For
  durability persist the job and send from a queue, not from the thread.
- **Unit-testing the hook proves parsing only.** Verify end to end with a unique token in
  and the same token out.
- **Synthetic hook tests reach the real send path** and post into the live room. Point them at
  a scratch chat, or stub the send during tests.
- **Check what the plan/key allows before trusting the lane.** A subscription key can serve a
  model on one protocol and be throttled on another; probe the exact endpoint the harness will
  use, not the vendor's headline one.
