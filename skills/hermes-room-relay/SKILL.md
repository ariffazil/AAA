---
name: hermes-room-relay
description: "Relay a chat room to an external agent runtime."
tags: [hermes, gateway, plugin, relay, telegram, opencode, hooks]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Hermes Room Relay

Class of task: a chat room (DM, group, forum topic) must hand a message to a runtime that Hermes does NOT own — OpenCode's server, a CLI coding agent's session, any local service — and post that runtime's answer back into the exact room the message came from.

Hermes owns the transport; the other runtime owns the session. Neither can reach the other. The seam is a `pre_gateway_dispatch` plugin. Do not build a second Telegram bot for this, and do not make the human relay by copy-paste.

## Hook semantics (memorise these three)

`pre_gateway_dispatch` runs BEFORE auth, before mention checks, before session setup. Return values:

| Return | Effect |
|---|---|
| `{"action": "skip", "reason": ...}` | Message is DROPPED. Hermes never answers it. Use after a successful hand-off so there is no double reply. |
| `{"action": "rewrite", "text": ...}` | Replaces `event.text`, normal dispatch continues. |
| `{"action": "allow"}` or `None` | Normal dispatch. Every error path must land here. |

Because it fires before auth, you MUST do your own room gate — an id allowlist on `(chat_id, user_id)` pairs, not "is it a group". A platform-level allowlist does not protect a relay that spends money or drives a coding session.

## Contract that makes a relay safe

1. **Trigger prefix, not every message.** `oc:`-style prefix, plus an `oc@<session> <text>` one-shot override, so the room stays usable for normal conversation.
2. **Explicit target only.** Reply goes to `telegram:<chat_id>:<thread_id>` taken from the event that triggered it. Never infer, never "home channel". `hermes send` enforces the same rule and refuses a targetless send with a TRANSPORT LOCK error — that refusal is correct, do not work around it.
3. **Thread the long call.** The hook must return in milliseconds. Spawn a `daemon=True` thread for the subprocess; a multi-minute job must not stall the gateway loop.
4. **Ack then answer.** Post a short `⏳ <runtime> <session>` line first, then the real output. Otherwise the room looks dead for minutes.
5. **Fail-open always.** Missing config, bad JSON, dead binary, send failure — every path returns `None`. A relay fault must never silence the room.
6. **Fence the answer.** Wrap multi-line output in one code fence so markdown/code survives Telegram intact; truncate at a character cap with an explicit `…(dipotong)` marker.

Calling a CLI agent headlessly: prefer the runtime's JSON output mode and parse the NDJSON text parts, falling back to raw stdout. Never scrape a TUI.

## Enable + reload without restarting the gateway

Discovery alone does nothing. A freshly dropped plugin loads as `enabled: False, error: "not enabled in config (run hermes plugins enable <name>)"` — visible in the plugin list, and it never fires.

```bash
hermes plugins enable <plugin-name>      # also nudges a live gateway reload
```

To force re-discovery yourself, use the gateway control socket instead of restarting the gateway (no downtime, no dropped sessions):

```python
import sys; sys.path.insert(0, "/usr/local/lib/hermes-agent")
from pathlib import Path
from gateway.control_socket import reload_gateway_plugins
r = reload_gateway_plugins(Path("/root/.hermes").resolve())
print(r["reloaded"], r["adapters_rewired"])
```

**Verify activation, do not assume it.** The reload response carries `activations[]`; find your plugin and read `activated_now`:

```
{"name":"my_relay","activated_now":{"gateway_transforms":["pre_gateway_dispatch"]},"deferred":{}}
```

An entry present in `plugins[]` but absent from `activations`, or with empty `activated_now`, is loaded-and-inert.

## Test before the human finds out

Call the hook directly with a synthetic event — no network, no real chat:

```python
hook = m._on_pre_gateway_dispatch(event=Event(text="oc: ping", source=Source(chat_id=..., user_id=...)))
assert hook and hook["action"] == "skip"                                            # trigger path
assert m._on_pre_gateway_dispatch(event=Event(text="hello", source=...)) is None     # normal path
assert m._room_allowed(Source(chat_id="-100...", user_id="999"), cfg) is False        # gate holds
```

Test the OUTBOUND leg separately (`_send(chat_id, thread, "test")`) so a transport fault is diagnosed before a real answer is lost.

**Warn the human when a synthetic test escapes into a real room.** A unit test calling `_send` with a real chat id posts a real message. Say so unprompted; a stray "TEST OK" in a live room with no explanation reads as a malfunction.

## Known limits to state up front

- Two triggers arriving together run two subprocesses against one session and can interleave answers. Say it, and offer a single-flight lock.
- A daemon thread dies with the gateway; anything not yet sent is lost silently across a restart. Durable relay work belongs in a job queue, not a thread.
- `hermes send` writes to the room as the bot. In a forum, the thread id must be inside the target string or the answer lands in the wrong topic.

## Pitfalls

- **Returning `None` after a successful hand-off** produces two answers (runtime + Hermes). Return `{"action": "skip"}`.
- **Gating on group-ness instead of identity** lets any member of a large group spend the principal's budget. Gate on `(chat_id, user_id)` pairs from a config file.
- **Reading config on every hook call** is fine (cheap, hot-editable) but means a malformed JSON file silently disables the relay. Log at debug, never raise.
- **Hardcoding chat ids in the plugin** makes it per-room and unshareable. Config file beside the plugin.
- **Assuming `hermes send` will infer the room** — it will not; the refusal is governance. Pass the full `telegram:<chat>:<thread>`.
- **Restarting the gateway to pick up a plugin** drops live sessions for a change a control-socket reload handles in place.
