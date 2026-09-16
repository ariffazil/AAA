---
name: telegram-conversation-history-extraction
description: Read Telegram chat history from gateway.log when no API.
---

# Telegram Conversation History Extraction

Recover historical Telegram messages from local artifacts when the live Bot API is not usable (gateway dead, bot shadow-forbidden, bot can't send messages to itself, FK serve error, subagent delegated the task, etc.). The goal: produce a **timestamp | sender | raw content** chronology for a given `chat_id` over a time window, and ground it in real files — never fabricate.

## When to use this skill

Trigger on any of:
- "What did I / user X say in group Y yesterday / last week / at 9:23 AM?"
- "Show recent messages in SADO group / chat -1003815535761"
- "Read the last 24h of group Z"
- "What did Arif / Syed / Kiki reply in the past hour?"
- Subagent task: "extract recent messages from Telegram group X for the past N hours"
- Any historical Telegram message recovery when the user is NOT asking you to operate the gateway or send a new message

Do NOT use this skill to:
- Operate the gateway itself (use `hermes-telegram-gateway-ops`)
- Add a new lane/persona (use `hermes-lane-switch-routing`)
- Send a new Telegram message (use gateway ops send-via-Bot-API path)

## Pre-flight: confirm no live API is needed

Before going to logs, ask: does the user actually need LIVE access, or are they asking for what's already on disk? If they want to send a message, route to gateway ops. If they want history, proceed below.

If you believe live API might be possible, check `gateway_state.json` first:

```bash
# Is the gateway actually online?
jq -r '.platforms.telegram.state' /root/.hermes/gateway_state.json
# Recent error?
jq -r '.platforms.telegram.error_message' /root/.hermes/gateway_state.json
```

If state is "connected" and the user wants messages from minutes ago, you may still need to go to logs — Bot API `getUpdates` only returns unread, and Telegram's Bot API does NOT support fetching historical group messages at all. **For group history, logs are usually the only local source.**

## Source 1 — `gateway.log` (PRIMARY for inbound messages)

`/root/.hermes/logs/gateway.log` is the canonical source for inbound Telegram messages. Lines follow this shape:

```
2026-08-19 01:32:57,053 INFO gateway.run: inbound message: platform=telegram user=ARIF chat=-1003815535761 msg='Isi minyak lepas ambik aku la. We go McD. I need coffee' reply_to_id=None reply_to_text=''
```

Variable fields:
- `user=<display_name>` — Telegram display name (NOT user_id). Often "No name" for users with hidden profile.
- `chat=<chat_id>` — the chat_id you want (filter on this!)
- `msg='...'` — the raw message text. Replying-to audio/images is concatenated as `[Replied-to audio 'voice.ogg'`.
- `reply_to_id=...` — message_id being replied to (None for top-level)
- `reply_to_text='...'` — quoted text (empty string for media)

Bot responses appear in DIFFERENT lines (look for `response ready: ... response=N chars` nearby, but the actual reply text is NOT logged at INFO level — only its length).

**Rotated files**: `gateway.log.1`, `gateway.log.2`, `gateway.log.3` cover earlier windows. The current `gateway.log` may STOP at the time the gateway last started — if you need messages from before the last restart, also check rotated files.

**⚠️ ALWAYS `grep -a` (or `grep --text`) on `gateway.log*`** — the files contain binary bytes (media/emoji/null runs), so plain grep prints `binary file matches` and silently stops matching, truncating your extraction. Verified 2026-08-30: a plain-grep census returned 0 messages for a window that actually had 260+ inbound messages; `grep -a` recovered them all. Every grep recipe in this skill assumes `-a`.

**Rotation order**: `gateway.log` = NEWEST, `.1` → `.3` = progressively OLDER. When combining files, process in that order — piping all four into `tail -N` shows the OLDEST file's last lines (misleading: looks like activity stopped weeks ago when it's just the oldest rotation). Grep each file separately newest-first, or sort the merged output by timestamp.

## Source 2 — `agent.log` (for bot REPLIES and per-turn context)

`/root/.hermes/logs/agent.log` contains:
- `agent.turn_context: conversation turn: session=... model=... platform=telegram history=N msg='...'`
- The `msg=` here is the FULL post (often `[Wed 2026-08-19 09:35:58 +08] [Replying to: "..."] ...`) — useful when gateway.log has parts but you want the bot's final delivered text.

**Caveat**: `agent.log` truncates session summaries; session DB (`state.db`) is the FULL trust store for assistant text, but doesn't have raw inbound Telegram messages either.

## Source 3 — `state.db` (SESSION-SCOPED, NOT a Telegram cache)

**`state.db` is NOT a raw Telegram message database.** Its `messages` table has `session_id` (a Hermes conversation session), not `chat_id`. Querying it for `chat_id = -1003815535761` returns nothing because the column doesn't exist. **Don't waste time on this trap.** It holds Hermes's own conversation history — useful for "what did I say to Hermes about X", not for "what did X say in the Telegram group".

```sql
-- This will FAIL (no chat_id column):
SELECT * FROM messages WHERE chat_id = -1003815535761;
-- ERROR: no such column: chat_id

-- This is what the table actually has:
.schema messages
-- id, session_id, role, content, tool_call_id, tool_calls, tool_name, ...
-- Indexes are on session_id, not chat_id.
```

**Positive route — the `sessions` table DOES have `chat_id`.** When you need full group-session content (image-attachment markers, `reply_to_id` anchors, assistant reply text), find the session by chat_id, then read its messages by session_id:

```sql
-- 1. Find recent sessions for the group
SELECT id, chat_id, datetime(started_at,'unixepoch','localtime') AS t, message_count
FROM sessions WHERE chat_id LIKE '%1003815535761%'
ORDER BY started_at DESC LIMIT 8;

-- 2. Read that session's transcript (inbound text is [ARIF|267378578] / [Group|1087968824] prefixed)
SELECT id, role, datetime(timestamp,'unixepoch','localtime') AS t, substr(content,1,400)
FROM messages WHERE session_id='<session_id>' ORDER BY id ASC;
```

Timestamps in `state.db` are unixepoch; convert with `'localtime'` to match MYT log lines.

## Source 4 — lane-specific memory files

For SADO group specifically, ARIF-architected lane files hold **structured conversations** with timestamps:
- `/root/.hermes/profiles/aaa-hermes/memories/MEMORY-syed.md` — Syed's lane file, contains `### 2026-08-13 06:42 UTC · chat=-1003815535761 · user=1042200555` headers with full user/assistant turn content
- `MEMORY-syed-dm.md` — same for DMs (chat_id = user_id, no `-100` prefix)
- `/root/.hermes/lanes/private/abang-sado-*.md` — analysis/synthesis files (NOT live messages)

**Caveat**: these are *snapshots*, not live. Last entry may be days/weeks old. Check for the most recent `### <date>` header to see how stale the snapshot is.

## Source 5a — Named-person pre-flight (do this BEFORE grep)

When the user names a PERSON ("Nabilah", "Syed", "Azwa") not a chat_id, run a quick existence probe across all sources BEFORE searching logs. This catches the common case: user asks for a "group" that doesn't exist on Telegram at all, but the person has files in `/root/.hermes/lanes/private/`.

```bash
# 1. Any Telegram group/chat whose name contains the person?
PERSON="Nabilah"
jq -r --arg p "$PERSON" '.platforms.telegram[]? | select(.name|ascii_downcase|contains($p|ascii_downcase)) | "\(.id) | \(.name)"' /root/.hermes/channel_directory.json

# 2. Any inbound messages FROM that name across ALL gateway logs?
for f in /root/.hermes/logs/gateway.log{,.1,.2,.3}; do
  grep -i "$PERSON" "$f" 2>/dev/null | grep "inbound message" | wc -l
done

# 3. Any private lane files for that person?
ls -la /root/.hermes/lanes/private/ 2>/dev/null | grep -i "$PERSON"
ls -la /root/.hermes/lanes/private/"$PERSON"/ 2>/dev/null
```

If (1) returns empty AND (2) returns zero hits, the person has no Telegram presence. **Report the gap clearly** ("no Telegram group/DM exists for Nabilah in any channel directory or gateway log; here is what I do have") rather than fabricating a chat_id or substituting unrelated sources. Then list what (3) surfaced and ask the user to forward the actual group (WhatsApp screenshots, exports) if they meant a non-Telegram platform.

## Source 5 — `channel_directory.json` (IDENTITY RESOLVER)

`/root/.hermes/channel_directory.json` maps `chat_id → display_name` and `user_id → display_name`. **This is the canonical resolver for "who is user 1042200555?"** — naive parent callers often guess wrong.

```json
{
  "id": "1042200555",
  "name": "No name",   // Syed with hidden profile
  "type": "dm"
}
```

Critical lesson learned: **In the arifOS federation, user_id 1042200555 = Syed (@rico_ricaldo_33), NOT Arif.** Arif's Telegram user_id is 267378578. Always cross-check against `USER-<person>.md` and `lane-<person>.json` in the active profile's `memories/` directory before reporting a user's Telegram activity.

## Standard extraction recipe

```bash
# 1. Define window (use session/MYT timezone; log timestamps are likely local but verify)
WINDOW_START="2026-08-19 09:00"
WINDOW_END="2026-08-19 09:30"

# 2. Filter gateway.log by chat_id and time window
grep -E "inbound message.*chat=-1003815535761" /root/.hermes/logs/gateway.log \
  | awk -F'[, ]' '$1" "$2 >= "'"$WINDOW_START"'" && $1" "$2 <= "'"$WINDOW_END"'"'

# 3. Cross-check rotated files
for f in /root/.hermes/logs/gateway.log /root/.hermes/logs/gateway.log.1; do
  grep -E "inbound message.*chat=-1003815535761" "$f" 2>/dev/null \
    | awk -F'[, ]' '$1" "$2 >= "'"$WINDOW_START"'" && $1" "$2 <= "'"$WINDOW_END"'"'
done

# 4. Resolve user identities
jq -r '.platforms.telegram[] | select(.id=="1042200555") | .name' /root/.hermes/channel_directory.json
# Also cross-check
jq -r '.platforms.telegram[] | select(.id=="267378578") | .name' /root/.hermes/channel_directory.json
```

## Output format

When reporting, ALWAYS use:

```
timestamp | sender (user_id@username or role) | exact content
```

Never paraphrase. Never infer content from context. If a line is truncated in the log, say so.

## Pitfalls

- **state.db is NOT a Telegram history cache.** Its `messages` table has no `chat_id`. Don't query it for chat_id filters.
- **User_id identity is easy to get wrong.** `1042200555` is Syed, not Arif. Always verify via `channel_directory.json` + `USER-<person>.md` + `lane-<person>.json` before reporting.
- **gateway.log may stop while gateway still runs.** A running gateway DOES NOT guarantee the log is actively being written. Check the timestamp of the last log line vs. `gateway_state.json.updated_at`.
- **Bot replies are NOT in gateway.log at INFO level.** Only message length is logged. To get the actual bot reply text, use `agent.log` and grep for the `agent.turn_context` line with the matching session id.
- **Replied-to media is concatenated weirdly.** `[Replied-to audio 'voice.ogg'` is a partial marker — the full audio transcription may not be in the log.
- **"No name" in user= field means a private profile**, not a missing user. Resolve via channel_directory.json + lane-*.json.
- **The log may be silent during the requested window** — that's a VALID finding, not a failure. Say "no entries in local logs for that window" rather than inventing content.
- **grep without `-a` on gateway.log silently returns nothing.** The log contains binary bytes; plain grep exits with `binary file matches` and stops. A "0 messages" census can be a grep artifact, not real silence — always re-run with `grep -a` before concluding absence (verified 2026-08-30: 260 messages hidden from plain grep).
- **Don't claim "no messages" without checking ALL rotated files** (`gateway.log`, `gateway.log.1`, `gateway.log.2`, `gateway.log.3`).
- **Don't trust the parent caller's user_id naming.** Even if the task says "Arif user_id 1042200555", verify from data. F9 Anti-hantu: ground in evidence, not in the asker's description.
- **Same inbound DM can log under TWO chat ids** (primary DM plus a mirrored id that also emits `Blocked unauthorized user` warnings while still being processed). Dedupe on text + timestamp before counting messages or concluding traffic volume.
- **Before re-OCRing a scanned PDF from a lane, run `session_search` first.** A sibling session (or a parallel curator pass) may have already run pdftoppm + vision on the exact same file minutes earlier — reuse its transcription instead of paying for OCR again.
- **When the user names a person ("digest everything in group dear NABILAH") but no Telegram group/DM exists for them, do NOT pivot to an unrelated source.** Name the gap explicitly, list what you DO have in `/root/.hermes/lanes/private/<name>/`, summarise the most context-relevant file (court doc → parties/dates/status), and ask the user to forward the actual group if they meant WhatsApp or another platform. Silent substitution = fabrication.
- **Narrative overreach — never bridge log fragments with MEMORY to invent a destination/event.** Log extraction is log-only. The sequence `otw` → `da smpai` → `ada org keluar` → `nak pinjam jumper` does NOT license asserting "trip to JB", "hantar roommate balik kampung", or any destination — even when MEMORY carries context about that destination from a DIFFERENT conversation (the bridge feels natural: "he went JB before + he's otw = JB again" — that is fabrication, verified 2026-08-27, user pushback: "Apa benda JB hang mengarut"). MEMORY may colour INTERPRETATION only when explicitly flagged as interpretation; it may NEVER fill a gap in the CHRONOLOGY. If called out: retract fully, re-extract log-only, acknowledge. Same failure family as the "baru sampai ≠ sampai destinasi" spatial scar — fragments are position data, not narrative.
- **Contact display names in user-supplied screenshots are real handles, not labels.** When the user attaches screenshots of a chat with someone, the name at the top ("Fallout 1", a nickname, anything) is usually the subject's actual IG/handle — NOT a symbolic label the user assigned. Do not build interpretation on it (2026-08-27 scar: read "Fallout 1" as the user's judgment of the subject — it was the subject's IG handle; user: "Tu memang nama ig dia la". Same reply also inverted who drove — verify direction/attributions before assigning roles.)
- **Anonymous-admin sender mask — `[Group|1087968824]` is NOT a person id.** In groups, admin messages posted anonymously arrive in gateway.log as `user=unknown` with `msg='[Group|1087968824] ...'` — 1087968824 is Telegram's generic anonymous-admin placeholder, NOT Syed's (1042200555) or anyone's real user_id. Grepping by the real user_id therefore returns ZERO hits for that person's group messages, and answering "did X message last night?" with "no" is WRONG if X posts as anonymous admin. Verified 2026-09-03: Arif asked "did abang sado Syed ask anything last night?" — DM grep said nothing since 08-26, but Syed had been active in the SADO group that morning as anonymous admin (`[Group|1087968824] @ariffazil uik masuk meeting x`). Recovery: when a named person is a group admin, grep the chat_id for `[Group|` lines in the window too, and read `reply_to_text` anchors (the quoted text of a message being replied to appears even when the original sender is masked). Attribution of a `[Group|...]` line to a specific person is inference — verify by content cues (who would tag Arif about his meeting / breakfast / mak's hospital trip) and only report as inference, not fact.

## Pattern — relationship-ledger forensics (chronology that becomes relational)

Chronology requests can evolve into relational verdict questions ("am I too much for them", "are they extracting from me", "did they stalk me before we met"). Stay evidence-capped:

1. **Per-day sender census** — count inbound per sender per day across ALL rotated logs (`awk '{print $1}' | cut -d- -f1 | sort | uniq -c`); asymmetry and silence windows become visible instantly.
2. **Pull the subject's DM-to-bot lane for the same window.** The group shows the public persona; private DMs to the bot show what they hide (searches, forwarded notices, private investigations of third parties). Never judge someone's state from group logs alone.
3. **Build BOTH sides of the ledger before any verdict.** A one-sided read that amplifies the user's feeling WILL get falsified by their pushback; the second pass is where trust is won or lost. Give honest probabilities (conscious exploitation vs unconscious asymmetry), not vibes.
4. **Origin questions need contact provenance, not just first messages.** "How did you get their number/handle?" can invert the read of identical screenshots (subject already circulating in a client circuit ≠ cold first contact).
5. **Offer at most ONE falsifiable test** (e.g. stop initiating, measure what remains) — the user may have already run it; ask. The verdict belongs to the human.
6. **Pre-bot questions have no log answer.** Say so plainly and ask for the origin story instead of inferring from personality patterns.

Worked example (census table, silence-window lane-shift, scam-vs-real MdI bankruptcy-notice forensics, origin-screenshot provenance flip): `references/syed-relationship-ledger-2026-08-27.md`

## Source 6 — `/root/.hermes/lanes/private/<person>/` (per-person case files)

Private lane directories hold artifacts about a person that are NOT messages — scanned court documents, biographical notes, family maps. Examples seen this session:

- `/root/.hermes/lanes/private/nabilah/kes-nafkah-anak-2026-08-17.pdf` — scanned Malaysian Syariah nafkah anak case (Nabilah binti Fazil v. Fahim bin Ahmad Shukri)
- `/root/.hermes/lanes/private/family-fazil-faridah.md` — biographical map
- `/root/.hermes/lanes/private/arif-sibling-constellation.md` — relationship map

**These are not Telegram content.** They are useful CONTEXT for digesting a person's situation when the named-person pre-flight returns no Telegram traffic. When user asks for "everything in group dear NABILAH" and pre-flight shows zero Telegram presence, the honest move is: (a) name the gap, (b) list the lane files you DO have, (c) summarise the most recent context-bearing one (e.g. court doc → parties, dates, status), (d) ask if they meant a WhatsApp group and ask for screenshot/forward.

To list: `ls /root/.hermes/lanes/private/` then `ls /root/.hermes/lanes/private/<name>/`.

## Source 7 — WhatsApp export zips in `cache/documents` (PRIMARY for family/person history)

When a named person has no Telegram presence but the user wants their full history, the richest local source is usually `/root/.hermes/cache/documents/doc_<hash>_WhatsApp Chat with <Name>` — full WhatsApp chat exports the user sent as documents at some earlier time. They are ZIP archives (`unzip` → `<Name>.txt` + `.vcf` contact cards) even when `file` reports generic octet-stream.

```bash
# Discover what exports exist
ls /root/.hermes/cache/documents/ | grep -i "WhatsApp Chat"

# Extract and mine
cd /tmp && mkdir -p person_chat && cd person_chat
unzip -o -q "/root/.hermes/cache/documents/doc_<hash>_WhatsApp Chat with <Name>"
grep -n -i "keyword" "WhatsApp Chat with <Name>.txt"   # hits with line numbers
sed -n '38380,38430p' "WhatsApp Chat with <Name>.txt"  # context around a hit
awk '/^7\/7\/26/,/^7\/9\/26/' file.txt                 # date-range slice
```

Format notes:
- Timestamps: `M/D/YY, H:MM AM/PM` — normalize when merging with gateway.log ISO timestamps.
- `<Media omitted>` = image/voice/document placeholder. Sometimes content follows as plain text (e.g. an agent-pasted CTOS brief appears as a multi-line plain-text block right after).
- Attribution: shared/merged display handles exist ("Fahim Nabilah" posting is Fahim, not Nabilah). Read surrounding lines before quoting.
- Cross-chat timeline joins are powerful: one keyword (concert date, "lawyer", a payment) across 4-5 exports reconstructs a family-wide event window.

**Durability:** cache/ is evictable. The moment an export matters to a case, archive it: `cp` to `/root/.hermes/lanes/private/<person>/` + `chmod 600`.

## Source 8 — `errors.log` (model/provider failure attribution)

When the question is not "what was said" but "why did the bot go silent or reply garbage", `/root/.hermes/logs/errors.log` (+ `.1`, `.2`) is the one source the others cannot replace. It logs the full API failure chain per turn: provider, base_url, model, error code (429 quota, 400 param, timeout), and the fallback walk order. Correlate timestamps against gateway.log `response ready` lines.

## Failure mode — canned replies (model-layer outage, gateway looks alive)

Distinct from gateway error mode below: inbound logging works, outbound "succeeds", but every reply is a canned error string. Signature:

- `gateway.log`: `response ready: ... response=47 chars` — the SAME short length on every distinct user message in a window, then `Sending response (143 chars)` — the length mismatch is the gateway wrapping a canned agent error notice.
- `state.db`: assistant rows for those turns have content length 0 or repeated compaction blobs — do NOT conclude "the bot never replied"; the delivered text was a gateway-level fallback that never entered the session store.
- Attribution: grep `errors.log` for the same window. Classic cascade: primary lane 429 quota exhausted → every fallback lane 429/2056 insufficient_quota → last-resort lane 400s on a payload bug (seen: Groq `messages[N].content must be a string` when history contains empty/non-string content blocks, e.g. post-compaction) → every lane dead → canned reply.
- Human-impact trap: cron `no_agent` jobs keep delivering normally during a model outage (`cron.scheduler: ... delivered to telegram:<id>`). From the human side, the bot "spams reminders but ignores my questions". Always check cron delivery lines in the window before attributing anger to something the agent said.

### Triage recipe — "why is person X angry at the agent"

0. **"Hari ni / today" is a claim, not a fact.** Run `now`/`date` first and check whether X messaged today AT ALL. The anger may be yesterday's failures arriving in today's mood; if there is zero same-day inbound from X, say so plainly instead of narrating a same-day incident.
1. Extract X's inbound messages across ALL rotated gateway logs (Source 1); note silence gaps and tone shifts.
2. For each inbound, pull the matching `response ready` line; flag identical short response lengths (canned signature). Identical `Sending response (N chars)` counts across DIFFERENT inbound turns = template, never a real answer.
3. **Decode the exact canned string** from `_gateway_provider_error_reply()` in the gateway source (`/usr/local/lib/hermes-agent/gateway/run.py`) — rate-limit / auth / policy / generic English ⚠️/⏱️ templates, each a fixed length. Report what the human actually saw, not "the bot replied".
4. Grep `errors.log` (and/or `agent.log` — it also carries `Fallback activated: A → B` chains + 429/quota lines) for the window; identify which lanes died and the root error.
5. Grep `gateway.log` for `cron.scheduler: delivered` in the window; note reminders that kept flowing while interactive replies were canned.
6. Check for OVERLAPPING causes: `Skipping transcript persistence for context-overflow failure in session <id>` = oversized session that fails even with live providers (reset candidate — ask F13 before resetting). In `state.db`, assistant rows with EMPTY content are tool-call-only turns, not lost replies.
7. Live-probe the model chain (FED `/v1/chat/completions`) before promising recovery; name the seat that actually answered.
8. Only then narrate. Anger at the agent is frequently a service failure the human cannot see — not something the agent said.

## When the gateway is in error mode

If `gateway.log` shows errors like:
- `Forbidden: the bot can't send messages to the bot` — gateway is trying to send to itself
- `Reply target deleted, retrying without reply_to: Message to be replied not found` — anchor message was deleted
- `[Telegram] Blocked unauthorized user <id> in chat <id>` — prefilter allowlist stale

The gateway is still RECEIVING messages (logs store inbound), but outbound is broken. Inbound history extraction still works. For outbound, escalate to `hermes-telegram-gateway-ops` `Outbound reply` section — direct `sendMessage` via Bot API with the token from the gateway env beats the gateway log errors.

## Reference / example

- `references/sado-9am-extraction-2026-08-19.md` — concrete worked example: extracting 9:00-10:00 AM Aug 19 2026 messages from SADO group, including the user_id-confusion trap (1042200555 = Syed, not Arif).
- `references/nabilah-digest-negative-check-2026-08-20.md` — the negative case: "digest group dear NABILAH" where no such Telegram group exists locally. Four-step definitive check (directory scan → keyword grep across ALL rotated logs → sender census → lane filesystem sweep), the mirrored-DM-id dedupe trap, and the pivot to the lane PDF (nafkah anak filing) that held the real subject matter.
- `references/whatsapp-export-mining-2026-08-20.md` — the positive case that completed the arc: user later confirms story via voice note; mining 6 WhatsApp export zips (Nabilah/Faridah/Azwa/Naazira/siblings/family) to verify claims (CTOS brief, "duit lawyer" = pusaka lawyer Munirah, event windows via cross-chat timeline joins with external web dates). Includes the curl-DuckDuckGo-HTML fallback for when every search backend is down.
- `references/claim-audit-against-exports-2026-08-20.md` — the anger-phase audit pattern: when the user asserts a relational claim ("she said she hates me N times"), grep the export and report the ACTUAL count with quotes before co-signing. Zero-count answers delivered with evidence preserve the feeling while correcting the fact.
- `references/syed-anger-triage-2026-08-23.md` — the canned-reply outage case: "why is X angry at the agent" answered via errors.log failure-chain attribution (all model lanes quota-dead + Groq last-resort killed by a payload format bug) while cron reminders kept delivering. Includes the diagnostic signatures and the "human as failure alarm" trap.
- `references/syed-anger-forensics-2026-08-23.md` — companion deep-dive: full timeline of the same outage (context-overflow DM session failing since 08-21, four canned replies on 08-22, group lane healthy while DM dead), the exact `_gateway_provider_error_reply()` canned strings, and the generalized 8-step outbound-forensics recipe.
- `references/syed-relationship-ledger-2026-08-27.md` — relationship-ledger forensics walkthrough (per-day census, silence-window lane shift, scam-vs-real MdI bankruptcy-notice analysis, origin-screenshot provenance flip).
