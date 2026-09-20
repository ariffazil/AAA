<!-- PROVENANCE
     source-skill: telegram-bot-identity-and-group-routing
     original-path: /root/AAA/skills/domains/general/workshop/telegram-ops/telegram-bot-identity-and-group-routing/SKILL.md
     sha256-body: 173ae219709f85c5c28b7670cc3e661c65210d5aa67207f48920df3fe6b9fc74 -->

---
name: telegram-bot-identity-and-group-routing
description: "Verify bot + group + lane before any live Telegram test."
---

# Telegram Bot Identity & Group Routing — Pre-Live-Test Gate

Sending an outbound message to a Telegram group is easy. Sending it to the **right group, as the right bot, with the routing wired so replies actually flow** is the class of failure that wastes Arif's time and breaks monetization pilots.

## When to use

- Arif says "live test in group", "send to telegram", "post in group", "test reply in new group"
- Any "agent to public audience" deployment
- Before the first send to any new chat_id (don't trust session memory)
- Any session where you find yourself about to claim "wired", "configured", "set up" — apply witness-test FIRST (see below)

## 0. Witness-test BEFORE claiming anything is "wired"

**Lesson learned (2026-09-04):** the difference between a config declaration and a runtime behavior is the difference between a city blueprint and a city with power. Never claim wiring from config alone. Never claim wiring from disk alone. Both.

Two failure modes that this section prevents:

### Failure mode A — "files don't exist" when they do

Terminal output truncates. `ls /root/HERMES/` may stop at 30 rows and miss the `profiles/` subdirectory entirely. A second `ls /root/HERMES/profiles/` then lists the missing subdir. The file is real; you didn't see it.

**Fix:** when `ls` returns nothing or seems short, follow up with `find /root -name "<pattern>" -type f 2>/dev/null` before declaring files missing. Trust `find` over `ls` for existence claims. `ls` is a presentation; `find` is a search.

### Failure mode B — "config says wired" when runtime never fires

`/root/.hermes/config.yaml` declares 23 chat IDs in `allowed_chats` + `free_response_chats`. That means *somebody configured those*. It does NOT mean the runtime gateway ever processed any of them. The two pieces of evidence are independent.

**Verify both — disk AND runtime:**

```bash
# Disk-side: declarations exist
grep -c "^- " /root/.hermes/config.yaml | head -1
echo "---"
# Runtime-side: did the gateway actually route anything?
DB=/root/HERMES/profiles/hermes_asi/state.db  # adjust to active profile
sqlite3 "$DB" "SELECT COUNT(*) FROM sessions WHERE chat_id LIKE '%-1003815535761%';"
sqlite3 "$DB" "SELECT COUNT(*) FROM sessions WHERE user_id = '1042200555';"
sqlite3 "$DB" "SELECT COUNT(*) FROM messages WHERE session_id IN (SELECT id FROM sessions WHERE chat_id LIKE '%-1003815535761%');"
echo "---"
# Live service check
systemctl is-active hermes-asi-gateway
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getWebhookInfo" | python3 -c "import sys,json; d=json.load(sys.stdin)['result']; print(f'url: {d.get(\"url\",\"none\")}')"
```

If runtime is empty but config is full → the wiring is **declared but not executed**. Don't tell Arif "wired" — tell him "declared in config, runtime not firing, here's the gap".

### Witness-test ritual (do this before any "wired" claim)

1. **Disk:** `find /root -name "<expected-file>"` — file exists?
2. **Disk:** `grep "<expected-keyword>" /path/to/config` — declaration exists?
3. **Runtime:** `systemctl is-active <service>` — service running?
4. **Runtime:** `sqlite3 state.db "SELECT ..."` — any rows for the chat/user?
5. **Cross-surface:** if hermes_asi state.db is empty, check `hermes_apex`, `hermes_forge`, OpenClaw, and other mesh nodes — somebody else might own this surface.

If any of (3), (4), (5) come back empty, you do NOT have wiring. You have declaration. Two different things.

**Why this section exists:** in 2026-09-04, a session claimed "11 lanes / 3 bot tokens / 23 chat configs wired" from a config.yaml scan alone. Reality: 18 lanes / 1 active token / hermes_asi state.db empty for ALL 23 chats. The "wiring" was a blueprint of a city nobody had built. Witness-test prevents that.

Full protocol + worked example: `references/witness-test-protocol.md`.

## The Three Things You Must Verify BEFORE First Send

### 1. Bot identity truth (not config-truth)

Three different bots share this VPS. `config.yaml` lies; only `getMe` and the running gateway process tell the truth.

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
for v in ASI_ARIFOS_BOT_TOKEN TELEGRAM_BOT_TOKEN FORGE_BOT_TOKEN HERMES_TELEGRAM_BOT_TOKEN; do
  T=$(eval echo \$$v)
  BOT=$(curl -s "https://api.telegram.org/bot${T}/getMe" | python3 -c "import sys,json; print(json.load(sys.stdin).get('result',{}).get('username','INVALID'))")
  echo "$v -> @$BOT"
done
```

Bot map (verified 2026-08-29):
- `ASI_ARIFOS_BOT_TOKEN` → `@ASI_arifOS_bot` (Arif's sovereign agent)
- `FORGE_BOT_TOKEN` → `@hermesarifos_bot` (Gateway 4 / archive)
- `AGI_ASI_BOT_TOKEN` → OpenClaw family
- `HERMES_TELEGRAM_BOT_TOKEN` → default fallback

**F9 anti-hantu:** never claim bot identity based on `bot_token_env:` in config.yaml. The adapter hardcodes env vars, not config keys. Identity = ground truth from `getMe`.

### 2. Group identity (chat_id truth)

Arif often refers to groups by friendly name ("SADO group", "my Syed group"). Friendly name ≠ group_id. Before posting, confirm:

```bash
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChat?chat_id=-100XXXXXXXXXX" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['title'], r['type'], r.get('invite_link'))"
```

**Mandatory pre-flight checklist for "live test in group":**
- [ ] Got the exact chat_id from Arif (don't assume from prior context)
- [ ] Confirmed `getChat` returns the title Arif meant
- [ ] Confirmed `getChatMembersCount` returns ≥2 (not a dead group)
- [ ] Confirmed `getChatMember?user_id=<bot_id>` returns `"status": "administrator"`
- [ ] Checked `getWebhookInfo` → `pending_update_count == 0`, `last_error_message == null`

### 3. Lane routing (reply will actually flow)

The bot CAN post outbound via direct Bot API even if lane routing is broken. But that proves **outbound**, not **round-trip**. For Syed or clients to post → bot replies → everyone sees, the lane must be wired:

```bash
grep -B 1 -A 20 "free_response_chats:" /root/.hermes/config.yaml
grep -B 2 -A 2 "require_mention" /root/.hermes/config.yaml
```

**Pitfall — `free_response_chats` with `require_mention: true` upstream still requires mention.** Always diff require_mention at the immediate block level, not top level.

**Pitfall — `lanes.yaml` persona mapping ≠ gateway auto-reply.** A persona defined in `lanes.yaml` for chat_id X controls TONE/MEMORY when the reply fires. It does NOT enable replies. The `free_response_chats` list does.

## Class of Failure This Prevents — SADO 2026-08-29

Two groups existed —
- `-1003815535761` = "SADO" — private room (Arif + Syed + bot, emotional bromance space)
- `-1003747272167` = "Syed Sado Agent Client" — public group for clients (monetization pilot)

Live test was posted to the **private** group first. Arif corrected: "group SADO tu banyak sangat lobing2 emotional bromance dengan abang sado syed. malu klaau orang luar tahu. but abang sado need it."

**Lesson:** Private emotional-bonding groups and public monetization groups MUST be treated as separate surfaces with separate bot behavior. F9 anti-hantu applies — the bot appearing as "Arif's intimate friend" in a public group is a breach.

**Rule for any future "live test to new group":**
1. Get the explicit chat_id from Arif (not inferred from session memory)
2. `getChat` to confirm title
3. Ask Arif which **mode** the group runs in:
   - **Private bond mode** (Arif + named person only): mention-only, bot quiet, F9 strict
   - **Public client mode** (agent assists group members): free_response_chats enabled, bot active
4. Post to the **public** group by default unless Arif says private bond
5. Confirm round-trip works (member posts, bot auto-replies) before declaring success

## Routing Worksheet

For each new group Arif asks you to deploy to, record:

```yaml
- chat_id: -100XXXXXXXXXX
  title: <verified via getChat>
  mode: private_bond | public_client
  bot_username: @<from getMe>
  bot_status: administrator | member | absent
  free_response: true | false
  require_mention: true | false
  lane_persona: <from lanes.yaml>
  notes: <emotional context, F9 considerations>
```

Store this in `/root/HERMES/groups/<chat_id>.yaml` so future sessions know the group's mode without re-asking.

## Outbound Send Pattern (verified working 2026-08-29)

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s -X POST "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendMessage" \
  -d chat_id="-1003747272167" \
  -d parse_mode="Markdown" \
  --data-urlencode "text=..." \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok:', d.get('ok'), 'msg_id:', d.get('result',{}).get('message_id'))"
```

`Markdown` parse_mode works for most. Switch to `MarkdownV2` only for stricter formatting. For tables/buttons, use Telegram's native UI.

## Full Enumeration Audit — When to Run

Run a full Telegram surface audit when:
- Arif asks "map all groups" or "list all users with access"
- Adding a new group or user (verify no conflicts)
- After a bot token rotation (re-verify all getChat calls)
- Quarterly hygiene check

### Enumeration Recipe (verified 2026-08-29)

```
1. Get all allowed_chats from config.yaml (the master list)
2. Get all free_response_chats from config.yaml (auto-reply list)
3. Get all lane triggers from lanes.yaml (who has persona mapping)
4. For each chat_id in allowed_chats, call getChat API:
   - Confirms the chat still exists (API returns "chat not found" = stale)
   - Gets title, type (supergroup/channel/private), member count
5. Cross-reference: which chats are in allowed but NOT in lanes? (= orphan, guest-only)
6. Cross-reference: which chats are in lanes but NOT in allowed? (= broken, won't receive updates)
7. Report: full table with columns [chat_id, name, type, members, lane?, mode, staleness]
```

### Stale Entry Detection

Any chat_id/user_id that returns `Bad Request: chat not found` from `getChat` API is stale. Common causes:
- User blocked the bot
- User deleted their Telegram account
- Group was deleted or the bot was removed
- Typo in config (wrong digits)

**Action:** Remove from `allowed_chats` + `free_response_chats` in config.yaml. Leave in lanes.yaml until confirmed (lanes don't cause errors if the chat is gone — they just never match).

### Unmapped Chat Diagnosis

When a chat has free_response_chats access but no lane:
- Bot uses the `guest` lane (authority: TAMU, capabilities: READ_ONLY)
- Guest lane has `no_private_data: true`, `no_federation_tools: true`
- Guest replies are polite, minimal, no personal disclosure
- If richer behavior is needed: add a lane entry in lanes.yaml with triggers, memory, voice, doctrines

### Pitfalls

- **`bot_token_env:` in config.yaml is decorative** — adapter hardcodes env var names. `getMe` is the only ground truth.
- **`getUpdates` returns 409 when webhook is active** — expected, not an error. Use `getWebhookInfo` for pending count instead.
- **Direct Bot API send proves outbound only** — not round-trip. For round-trip, member posts in group, you watch journalctl for inbound webhook, watch agent turn complete, watch outbound send.
- **Don't touch the TTS pipeline** for group replies without explicit Arif consent — `iarif_tts_pipeline.sh` is sovereign voice IP. For group monetization pilots, default to text-only; voice only when user explicitly requests.
- **Don't infer chat_id from session memory** — every "live test to group" should re-verify the chat_id via `getChat`. Sessions can span days; group ids are stable but friendly names drift.
- **AGY agent running concurrently** — if you see `agy` PID burning CPU, that's another tenant on the VPS. Don't assume a CPU-hog is yours to kill.
- **Two groups with similar friendly names** — Arif's voice often says "SADO group" ambiguously. When the friendly name is generic ("SADO", "Group", "Community"), ALWAYS confirm chat_id from previous explicit message or ask.
- **`ls` truncation ≠ file missing** — `ls /root/.hermes/` can stop at the first 30 entries and miss nested subdirectories. When `ls` returns "no such file", follow up with `find /root -name "" -type f` before declaring anything missing. Proven 2026-09-04 — Syed memory files appeared "missing" via `ls` but `find` returned all 7.
- **Config declaration ≠ runtime evidence** — `config.yaml` lists 23 chat IDs and `state.db` may have zero rows for any of them. Configuration is the blueprint; runtime is the city. A blueprint without a city is not "wired". Always check `state.db` (`SELECT COUNT(*) FROM sessions WHERE chat_id = '<id>'`) and `systemctl is-active hermes-asi-gateway` before claiming "wired".
- **The "live gateway" assumption is wrong by default** — hermes_asi-gateway was inactive in 2026-09-04 while Syed/Arif/SADO group configs all declared "wired". Verify `systemctl is-active hermes-asi-gateway` BEFORE assuming any Telegram routing exists on this profile. Other profiles (hermes_apex, hermes_forge) and other surfaces (OpenClaw gateway, wawabot on azwaos) may or may not own the chat — enumerate before claiming.

## "Arif reports bot silent — no reply at all" — 2026-08-29 incident class

When Arif says "no reply", "bot silent", "why no answer", do NOT assume auth or token failure. **Most of the time the bot is fine and processing — the reply is being swallowed upstream.** Diagnostic ladder:

### 0. Authorization allowlist — "Blocked unauthorized user" (per-user block, NOT auth/token)

When the bot is silent for **ONE specific person** in a group (but replies fine to Arif / others in the same group), and the group IS in both `allowed_chats` and `free_response_chats` — this is the first thing to check. The group being whitelisted does NOT exempt individual users.

The gateway log names it outright:
```
WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Blocked unauthorized user <user_id> in chat <chat_id>
```

**Root cause:** the adapter's `_is_user_authorized_from_message` rejects the sender **before** the message reaches the LLM. This is upstream of `free_response_chats`. The allowlist is `TELEGRAM_ALLOWED_USERS` in the gateway env.

Verify (three checks):
- `getChatMember?chat_id=<group>&user_id=<id>` returns `status: member` (they ARE in the group).
- `grep "Blocked unauthorized user" gateway.log` names that user_id.
- `TELEGRAM_ALLOWED_USERS` (live gateway env) does NOT contain their user_id. Classic tell: user is a member, but their id is missing from the allowlist.

Fix:
1. Live gateway reads `/root/.secrets/kunci-mas.flat.env` — confirm via `systemctl cat hermes-asi-gateway.service | grep EnvironmentFile`. Add the user_id to `TELEGRAM_ALLOWED_USERS` **there first**.
2. Sync derived copies so they don't drift: `/root/.secrets/kunci-mas.env`, `/root/.secrets/kunci-root.env`, `/root/.secrets/kunci-root.flat.env`.
3. Back up each file first (`cp f f.bak-<name>-<ts>`), keep 0600.
4. Confirm id present in all four, then restart gateway.

⚠️ **Restart pitfall:** issuing `systemctl restart hermes-asi-gateway.service` from WITHIN a session that the gateway itself hosts kills your own session (log shows `Stopping... shutdown context: signal=SIGTERM`, exit -15 / `deactivating (stop-sigterm)`). Edit env + lane config FIRST (they're durable to disk), do the restart last, expect the session to drop, and re-establish after the gateway returns. On a slow stop (`TimeoutStopUSec=3min`) the service can sit in `deactivating` for minutes — wait, don't re-fire. Verify the new env is live afterward: `cat /proc/<newpid>/environ | grep TELEGRAM_ALLOWED_USERS`.

Then confirm the person has a lane: lane_switch (`.../profiles/aaa-hermes/plugins/lane_switch/__init__.py`) matches `telegram_user_ids` (exact user+chat) → person-level → `guest`. If no lane exists they'll get `guest` (minimal, no personal data). Create one in `/root/HERMES/lanes/lanes.yaml` keyed on their `telegram_user_ids` so they get the right persona/voice/memory instead of guest.

Full worked recipe (Nabilah 337052422, 2026-08-31): `references/telegram-allowed-users-block.md`.

### 1. Bot identity alive?
```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getMe" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['username'], r['id'])"
```
If `ok: True` with bot username → token live, skip auth hypothesis.

### 2. Pending updates piling up?
```bash
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getWebhookInfo" \
  | python3 -c "import sys,json; print('pending:', json.load(sys.stdin)['result'].get('pending_update_count'))"
```
**`pending_update_count > 5` means bot is NOT polling/responding.** Drain before diagnosing further:
```bash
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getUpdates?limit=100&timeout=0" \
  | python3 -c "
import sys, json, urllib.request, os
token = os.environ['ASI_ARIFOS_BOT_TOKEN']
updates = json.load(sys.stdin)['result']
if updates:
    max_id = max(u['update_id'] for u in updates)
    with urllib.request.urlopen(f'https://api.telegram.org/bot{token}/getUpdates?offset={max_id+1}&timeout=0', timeout=15) as r:
        d = json.load(r)
        print(f'ACK max={max_id} count={len(updates)} remaining={len(d[\"result\"])}')
"
```
Then restart gateway so polling re-establishes.

### 3. Hook signature drift — the silent killer
Gateway dispatcher (`/usr/local/lib/hermes-agent/gateway/hooks.py:195`) calls hooks as `fn(event_type, context)`. If a hook under `/root/.hermes/hooks/*/handler.py` declares `def handle(event: dict)` instead, EVERY `agent:start` and `agent:end` crashes with:
```
[hooks] Error in handler for 'agent:end': handle() takes 1 positional argument but 2 were given
```
**Symptoms from Arif's POV:** "bot silent", "no reply at all", "/new doesn't work".
**Why it's silent:** hooks are observational, don't block dispatch — but exception spam burns CPU, slows the event loop, and PTB reply_target expires (>30s) → reply silently dropped.

**Verify:**
```bash
journalctl -u hermes-asi-gateway --since "1h ago" | grep -c "handle() takes 1"
# >0 = hook signature drift present
```
**Audit all hooks at once:**
```bash
for f in /root/.hermes/hooks/*/handler.py; do
  echo "=== $f ==="
  grep -E "^def handle\(|^async def handle\(" "$f"
done
```
All four must match `(event_type, context)` form. If any shows `(event: dict)`, patch it.

**Fix pattern (compatible with both gateway + legacy single-dict tests):**
```python
def handle(event_type=None, context=None, event=None) -> dict:
    if isinstance(event_type, dict):
        # Legacy single-dict call (tests, old call sites)
        event = event_type
        event_type = event.get("event_type", event.get("type", "unknown"))
        context = event
    else:
        event_type = event_type or "unknown"
        context = context or {}
    # ... use context.get('messages', []) instead of event.get(...)
```

### 4. "Reply target deleted, retrying without reply_to" — latency symptom, not auth
This warning fires when the original message PTB tried to reply to no longer exists. **It is a latency tell**, not an auth failure. Common cause: agent loop slow (hook spam, slow MCP, cold provider) → reply arrives after Telegram moved the original out of context. After fixing hook signatures (step 3) the count drops from 7/trip to 0. Don't add retry logic — fix the latency source.

### 5. "Forbidden: the bot can't send messages to the bot" — startup noise only
Init code tried to send to its own chat_id (e.g. `8410138119` for ASI_arifOS_bot). Telegram rejects, gateway logs 3× then continues. Cosmetic — ignore if only seen during startup.

### 6.5 Cross-node dual-gateway polling conflict — "terminated by other getUpdates request"

**Symptom:** gateway log repeats `[Telegram] Telegram polling conflict (1/5) — previous session still held open on Telegram's servers. Error: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running`. Replies intermittently drop — two pollers steal updates from each other.

**Root cause class:** TWO `hermes-asi-gateway` instances on DIFFERENT mesh nodes hold the same `TELEGRAM_BOT_TOKEN`. Observed 2026-09-02: KVM8 (af-forge) + KVM4 (srv1946043, CCC worker node) both polled token 8410138119. Stopping every LOCAL Telegram process (`hermes-real-bridge` — stopped + disabled) did NOT clear the conflict, because the second poller was on another node.

**Diagnosis (both steps; always mask tokens — `/proc/environ` and `systemctl show -p Environment` emit full secrets):**
```bash
# 1. Confirm conflict locally
journalctl -u hermes-asi-gateway --since "1h ago" | grep -c "polling conflict"

# 2. Enumerate pollers across the mesh — read gateway env on every node running one
ssh root@100.64.0.5 'tr "\0" "\n" < /proc/$(systemctl show -p MainPID --value hermes-asi-gateway)/environ 2>/dev/null | grep -E "TELEGRAM.*TOKEN" | sed "s/=.\{6\}/=***MASKED/"'
```

**Resolution:** exactly ONE node may poll a given token. Stop + `systemctl disable` the redundant gateway on the non-owner node (KVM4 is a CCC coding pool — it does NOT need a Telegram gateway; KVM8 owns the bot). If the redundant gateway serves a real purpose, HOLD and ask which side keeps the token — same-token dual-polling never stabilizes on its own.

**Pitfall:** a local conflict count that persists after stopping every local Telegram process means the other poller is REMOTE. Enumerate the mesh; don't re-audit localhost.

**NOTE (2026-09-02):** if the conflict log lines stop on their own after local cleanup, verify over 15+ minutes before declaring resolution — a ghost session held open on Telegram's servers can take minutes to expire. `journalctl -u hermes-asi-gateway --since "15 min ago" | grep -c "polling conflict"` = 0 is the pass condition.

### 7. After patching — restart discipline
Always: patch → drain pending → `systemctl restart hermes-asi-gateway.service` → wait 5s → check `journalctl --since "30 sec ago"` for ERROR/hooks/Forbidden lines. Verify restart count with `systemctl show hermes-asi-gateway -p NRestarts` (anything > 5 in 5 min = circuit breaker, stop and re-diagnose).

## Verification Steps After Send

1. `journalctl -u hermes-asi-gateway --since "5 minutes ago"` — should show inbound webhook pick up your message (look for `chat_id` in adapter logs)
2. `getWebhookInfo` — `pending_update_count` should stay 0
3. `getChatMembersCount` — unchanged (your send doesn't add members)
4. If reply was supposed to be auto-generated: check for outbound `sendMessage` calls in the gateway log matching your message context

## Related skills

- `hermes-telegram-gateway-ops` (in profile-archive — identity verification + restart discipline for the gateway itself)
- `telegram-bot-routing-doctrine` (3-bot / 9-group federation routing table)

## Reference index

- `references/asi-silence-2026-08-29.md` — Full transcript of "bot silent, no reply at all" incident: hook signature drift root cause, 71-pending-queue drain, three-layer cascade. Read first when Arif says "no reply at all" or `/new`/`/restart` don't work.
- `references/telegram-allowed-users-block.md` — The per-user authorization allowlist block: "Blocked unauthorized user" in gateway.log, TELEGRAM_ALLOWED_USERS root cause, the 4-copy env sync, and the restart-self-kill trap. Read next when the bot replies to some group members but not one specific person.
- `references/witness-test-protocol.md` — Disk vs runtime witness-test recipe. Read FIRST when you're about to claim any Telegram routing is "wired" or "configured". Includes the 2026-09-04 lesson: declared-but-never-fired state where config.yaml has 23 chats and state.db has zero routing records.
