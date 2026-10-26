---
name: hermes-delivery-target-guard
description: "Use when output is produced but never reaches the chat."
version: 1.0.0
floors: [F2, F9]
triggers:
  - "DELIVERY_TARGET_BLOCKED"
  - "bot can't send messages to the bot"
  - "message produced but not delivered"
  - "gateway alive but no message"
  - "delivery obligations abandoned"
  - "cron ran but nothing arrived"
  - "which channel_directory"
  - "delivery guard"
capability_tier: fed-long-context
ecology_state: WARM
---

# Hermes Delivery Target Guard

Producing a message and delivering it are separate states. The gateway can be `active`,
`NRestarts=0`, and answering on Telegram while every outbound send to a given chat is
refused before the network call. This skill is the probe order for that gap.

## The defect class: writer and reader are different files

The guard does not read the directory the running gateway maintains.

```
reader   gateway/delivery_guard.py::target_allowed()
         PROFILE_ROOT = /usr/local/lib/hermes-agent/profiles
         name = active_profile file → $HERMES_PROFILE → 'aaa-hermes'
         file = PROFILE_ROOT/name/channel_directory.json

writer   gateway/channel_directory.py::build_channel_directory()
         rebuilt at boot from connected adapters + session origins
         persisted under the gateway's WorkingDirectory (= /root/.hermes)
```

Two files, one name. The live one is large and freshly stamped; the guarded one is small
and can carry an `updated_at` from months ago. **Adding a chat id to the live file changes
nothing** — the reader never opens it. Every downstream symptom (group added, still blocked;
new lane silent) follows from this one split.

Treat it as a single-writer violation and look for it *before* debugging IDs.

## Probe order

### 1. Ask the guard, not the log

```bash
cd /usr/local/lib/hermes-agent && python3 - <<'EOF'
import sys; sys.path.insert(0,'/usr/local/lib/hermes-agent')
from gateway.delivery_guard import target_allowed, _active_profile_dir
print('active profile dir:', _active_profile_dir())
for cid in ['<chat_id_1>', '<chat_id_2>', '<bot_id>']:
    print(cid, target_allowed('telegram', str(cid)))
EOF
```

This returns `(allowed, reason)` per id and is the only call that reflects what the guard
will decide. A file listing is not the same answer.

### 2. Compare the two files explicitly

```bash
stat -c '%y %s %n' /usr/local/lib/hermes-agent/profiles/*/channel_directory.json \
                    /root/.hermes/channel_directory.json
python3 - <<'EOF'
import json
for p in ('/usr/local/lib/hermes-agent/profiles/aaa-hermes/channel_directory.json',
          '/root/.hermes/channel_directory.json'):
    d=json.load(open(p)); tg=d['platforms']['telegram']
    print(p, '| updated_at:', d.get('updated_at'), '| entries:', len(tg))
EOF
```

Report both stamps and both counts side by side. The gap is the finding; "id present" is not.

### 3. Read the reason taxonomy before counting anything as fixed

Grepping a pretty log truncates the reason and makes every block look identical. Pull the
full line, then classify:

| Reason substring | Meaning | Verdict |
|---|---|---|
| `is not a known human/group in channel_directory.json` | the guarded copy lacks the id | real gap — fix the reader |
| `is a bot id in IDENTITY_LOCK.json` | Telegram refuses bot-to-bot | **correct refusal**, not a defect |
| `identity lock unreadable` / `channel directory unreadable` | fail-closed on unreadable state | correct, investigate the path |
| `delivery guard unavailable: …` | import/exception path | fail-closed, fix the loader |

Never count the bot-id shape among "ids recovered" — that inflates a fix with a designed
refusal, and the same id will keep appearing at a steady rate with no harm done.

### 4. Blocked ≠ recovered: check the obligation store

The log stops shouting as soon as the guard is fixed. The queue does not drain itself.

```bash
sqlite3 'file:/root/.hermes/state.db?mode=ro' \
  "select chat_id, state, attempts, substr(last_error,1,45) from delivery_obligations
   where state!='delivered' order by updated_at desc limit 20;"
```

Rows carrying `last_error LIKE 'delivery_target_blocked%'` remain `abandoned` after the
fix; they need a re-queue. `state='delivered'` count N never implies the abandoned rows
went out — the two states are disjoint by construction.

### 5. A refresh can carry the right id with the wrong name

Diff each entry's `name` against the canonical file. A chat arriving under a config-shaped
label instead of its real name is a routing hint nobody will recognise in tomorrow's log,
and it will be read as a different chat.

## Post-restart: prove silence, do not assume it

Restarting from inside the gateway kills the command before it finishes (SIGTERM
propagates to children); `systemd-run --on-active` is refused for the same reason. Use a
separate shell.

After the restart, bound the check by the start timestamp, never by "now":

```bash
systemctl show hermes-asi-gateway -p ActiveEnterTimestamp -p ActiveState -p MainPID --value
grep DELIVERY_TARGET_BLOCKED ~/.hermes/logs/gateway.log \
  | awk '$2>="<HH:MM:SS of restart>"' | grep -oE 'target=[-0-9]+' | sort | uniq -c
```

An empty result over a **bounded** window is a real finding. An empty result over an
unstated window is not — see the log-window rule below.

## The log-window rule that causes false claims in both directions

A short window answers "is it happening right now", never "did it happen". Before
reporting either silence or an active fire, print the timestamp distribution over the
widest window available:

```bash
docker logs --timestamps --since 6h <container> 2>&1 | grep -i <signature> \
  | awk '{print $1}' | cut -c1-13 | sort | uniq -c
```

A ten-minute burst four hours back and genuine silence are indistinguishable at `--since 1h`.
Both wrong answers have been produced from this: "still burning" (the burst had already
ended) and "no activity" (the burst was outside the window). Re-derive your own earlier
claim before defending it.

## Pitfalls

- **`NRestarts=0` is not "never restarted".** It counts systemd auto-revivals of failed
  units only. An operator restart or an exit-1 signal shutdown increments nothing; a PID
  change between two reports is the real tell.
- **`N delivered` is not a health metric.** Split by destination and by state first — one
  blocked bot id can hold every failure while human delivery is 100%.
- **Fixing the reader is a T2 mutation.** Stage it, name the file, and say which copy
  becomes canonical; do not silently union two directories, which creates a third writer.
- **Do not test delivery by sending to a group you cannot read.** Verify with
  `target_allowed()` plus an obligation row; a successful API call to the wrong chat looks
  identical to success.
- **Never edit `config.yaml` or the install tree to change routing.** Config changes go
  through `hermes config set`; the guard's file is resolved from `active_profile`, so point
  that at the intended directory rather than patching paths inline.

## Report shape

Lead with the one-line state (`guard blocked / guard allows / unverifiable`), then the two
file stamps and counts, then the blocked-id classification table, then the number of
obligations still `abandoned`. Anything not re-derived in this pass is marked UNVERIFIED
rather than guessed.
