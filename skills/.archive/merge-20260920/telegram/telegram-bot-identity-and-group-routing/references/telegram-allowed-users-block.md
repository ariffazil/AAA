# Telegram Authorization Allowlist Block — "Blocked unauthorized user"

Worked incident: Nabilah Fazil (user_id `337052422`) in "Dear NABILAH" group (`-1003792478194`), 2026-08-31. Auto-reply was set up (group in `free_response_chats`, `require_mention: false`) but her messages never reached the agent.

## Symptom
- Bot replies to Arif in the same group, but NOT to a specific member.
- Their messages appear to vanish (no reply ever generated).
- Group is correctly in `allowed_chats` + `free_response_chats`.

## The tell (gateway log)
```bash
grep -a "Blocked unauthorized user" /root/HERMES/logs/gateway.log | tail
# WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Blocked unauthorized user 337052422 in chat -1003792478194
```
`grep -a` on the live gateway.log can swallow matches because the file has raw bytes; add `-a` for text mode.

## Root cause
`_is_user_authorized_from_message` (in `plugins/platforms/telegram/adapter.py`) rejects the sender before the message is batched/evented. It checks, in order:
1. `group_allow_from` / `allow_from` (config `telegram.extra`) — not set here
2. `TELEGRAM_ALLOWED_USERS` env — **this is where it blocked** (Nabilah's id missing)
3. runner `_is_user_authorized`

`free_response_chats` is downstream of this. A group being whitelisted does NOT whitelist its members.

## Verify the user is a member
```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChatMember?chat_id=-1003792478194&user_id=337052422" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; u=r['user']; print(r['status'], u.get('first_name'), u.get('last_name'), u.get('username'))"
# member Nabilah Fazil None
```

## Where the live gateway reads the env
```bash
systemctl cat hermes-asi-gateway.service | grep EnvironmentFile
# EnvironmentFile=/root/.secrets/kunci-mas.flat.env
```
Confirme the running process actually carries it (so you edit the right copy):
```bash
cat /proc/$(pgrep -f "hermes.*gateway --replace" | head -1)/environ | tr '\0' '\n' | grep ^TELEGRAM_ALLOWED_USERS=
```

## The four env files that must stay in sync
- `/root/.secrets/kunci-mas.flat.env` — the live gateway source (edit FIRST)
- `/root/.secrets/kunci-mas.env` (export variant)
- `/root/.secrets/kunci-root.env` (export variant)
- `/root/.secrets/kunci-root.flat.env`

Back up, then append the id to the CSV tail. The original tail here was `...6041855106`:
```bash
cd /root/.secrets
TS=$(date +%Y%m%dT%H%M%S)
for f in kunci-mas.flat.env kunci-mas.env kunci-root.env kunci-root.flat.env; do
  cp "$f" "$f.bak-nabilah-$TS"
done
# flat variant (no quotes)
sed -i 's/^TELEGRAM_ALLOWED_USERS=...6041855106$/TELEGRAM_ALLOWED_USERS=...6041855106,337052422/' kunci-mas.flat.env kunci-root.flat.env
# export variant (quoted)
sed -i 's/^export TELEGRAM_ALLOWED_USERS="...6041855106"$/export TELEGRAM_ALLOWED_USERS="...6041855106,337052422"/' kunci-mas.env kunci-root.env
```
Verify all four contain the id: `grep -c "337052422" <file>`.

## Restart — self-kill trap
`systemctl restart hermes-asi-gateway.service` issued from INSIDE a session the gateway hosts kills your own session:
- Log shows `Shutdown context: signal=SIGTERM under_systemd=yes` then the session goes exit -15.
- `systemctl status` shows `deactivating (stop-sigterm)` for a while (TimeoutStopUSec=3min).
- Do env + lane edits FIRST (durable to disk), restart LAST, expect to reconnect after it returns.
- After return, verify new env: `cat /proc/<newpid>/environ | grep TELEGRAM_ALLOWED_USERS` → contains `337052422`.

## Then wire the lane
If the person has no lane they'd fall to `guest` (minimal, no personal data). Create a wall gate in `/root/HERMES/lanes/lanes.yaml`:
```yaml
  nabilah:
    display_name: <Name> — <Role>
    authority_level: WARGA
    triggers:
      telegram_user_ids:
      - '337052422'
    memory_files:
    - /root/HERMES/memories/MEMORY.md
    - /root/HERMES/lanes/private/nabilah/nabilah-fazil-map.md
    voice:
      register: '<register>'
      tts_voice: ms-MY-YasminNeural
      tone: '<tone>'
    doctrines:
      never_claim_real_person: true
      family_privacy_f5: true
      no_federation_memory: true
      unknown_beats_invented: true
      fabrication_hard_block: true
      answer_or_unknown: true
```
Note: `register:`/`tone:` strings with commas/colons MUST be single-quoted or YAML parse fails ("mapping values are not allowed here"). Validate before restart:
```python
import yaml; d=yaml.safe_load(open('/root/HERMES/lanes/lanes.yaml')); print('nabilah' in d['lanes'])
```
And confirm `detect_lane` returns `nabilah` for the user (match on `telegram_user_ids`).
