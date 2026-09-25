---
name: arif-digest-group-chat
description: "Use when Arif asks to read or summarise a Telegram group."
version: 1.0.0
risk_tier: low
autonomy_tier: T1
triggers:
  - "baca chat X"
  - "apa cerita dalam group"
  - "aku malas nak copy paste"
  - "show recent SADO/group messages"
  - "what did Arif/Syed/Kiki say recently"
  - "explain latest conversation in group"
  - "ringkaskan apa jadi dalam group"
  - "summarise the last 24h"
  - "extract recent messages from Telegram group"
---

# arif-digest-group-chat — full pipeline for "tolong baca chat group ni"

Arif triggers this with phrasing like *"aku malas nak copy paste"*, *"baca chat SADO"*, *"apa hang tau pasal perbualan kami"*. The class of task: **pull recent N hours/days of a Telegram group from local gateway logs**, resolve senders from `[Tag|user_id]` prefixes, surface the human-voice analysis — without him forwarding anything.

Two protected skills already own the legs of this work:
- `telegram-conversation-history-extraction` (AAA/telegram-ops) — the extraction procedure
- `bridge-protocol` (F13) — the human-voice output contract

This skill composes them. Do not re-document extraction or voice contract here — link and reuse.

## Inputs (resolve in this order)

1. **chat_id** — from `/root/.hermes/channel_directory.json`. Group names like "SADO" are ambiguous; if a name maps to multiple chat_ids, ask. If a name maps to none, run the named-person pre-flight (Source 5a in the extraction reference) before fabricating a chat_id.
2. **window** — default last 72 hours. Override if Arif says "hari ni / semalam / minggu ni". "Hari ni" is a claim, not a fact — verify against `now` and the gateway log's actual last-entry timestamp.
3. **person of interest** (optional) — if Arif names a person ("Syed cakap apa"), add a sender filter post-parse.

## Procedure

```
1. PROBE gateway state
   jq -r '.platforms.telegram.state' /root/.hermes/gateway_state.json
   jq -r '.platforms.telegram.error_message' /root/.hermes/gateway_state.json
   If state != "connected", route to telegram-ops §B-incident branch.

2. EXTRACT from gateway.log across all rotated files
   for f in /root/.hermes/logs/gateway.log{,.1,.2,.3}; do
     grep -a -E "inbound message.*chat=<CHAT_ID>" "$f" 2>/dev/null
   done
   - `-a` is mandatory. Plain grep silently returns 0 on binary bytes.
   - rotated file order = newest (gateway.log) → oldest (gateway.log.3).

3. PARSE with the canonical line shape (no third-party parser needed)
   pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+\s+\S+\s+\S+\s*:\s*inbound message:\s+platform=\S+\s+user=(\S+)\s+chat=(\S+)\s+msg=(.*?)\s+reply_to_id=(\S+)\s+reply_to_text=(.*)$'
   - The user= field for group messages is almost always `unknown`. Real sender identity lives in the `msg=` prefix as `[Tag|user_id]`. Extract it from inside the message.
   - Strip outer quotes if msg starts/ends with matching single or double quotes.
   - Strip `[Replied-to image 'file_X.jpg' saved at: ...]` suffix when summarising, but keep the message-id anchor when the reply target matters.

4. RESOLVE senders against channel_directory.json
   - tag_to_uid: map [ARIF|267378578] → "ARIF", [No name|1042200555] → "SYED", etc.
   - The arifOS identity table is in MEMORY.md and lane-<person>.json files. The channel_directory.json is the canonical resolver for Telegram user_ids.

5. FILTER by window and (optional) person of interest
   - Sort ts desc. Top of the list = most recent.
   - Apply person filter on the tag (NOT on user= field).

6. ANALYSE — the human-voice layer (this is where bridge-protocol binds)
   - Lead with the **one thread that runs through the window**, not a per-message enumeration.
   - Per-message enumeration is acceptable as a supporting table but never as the lead.
   - When sender patterns reveal something real (asymmetry, silence windows, repeated themes, role-shifts in the room), name it — but bind it to evidence: per-day census, named sender counts, quoted messages.
   - When the human asks about a specific person, grep DM lanes too — group shows the public persona, DM shows what they hide. Never judge a person from group logs alone (reference: relationship-ledger forensics).

7. OUTPUT contract (bridge-protocol stage 3)
   - Lead paragraph: 2-4 sentences, BM Penang, what actually happened in the window.
   - One short sender census with counts (the asymmetry IS the story).
   - Quoted messages only when the exact wording carries the finding. Paraphrase otherwise.
   - Close with the one thing that the human should look at next — a question or a single fact, not a menu.
   - NEVER print labels ([OBS], [DER], [INT]), receipts, raw field names, or skill paths to the human.
   - NEVER print a date or time from cache/memory. Compute at render.
```

## Pitfalls

- **`-a` is not optional.** A plain `grep -E` on gateway.log returns `binary file matches` and exits 0 — the human will see "no messages found" when there were 260+. This is the most common single-source-of-truth failure in this pipeline.
- **Rotated file order is newest→oldest, NOT the order `ls` shows.** `ls gateway.log*` lists `.1 .2 .3 gateway.log` alphabetically, which puts the oldest file first. Process in reverse order: `gateway.log` first, `.1` second, `.2`, `.3` last.
- **`user=unknown` is the default for ALL group inbound.** Real sender identity is in the `msg=` prefix. Build the parser to extract sender from the prefix, not from the user= field.
- **Display names lie.** `No name` means a hidden Telegram profile, not a missing user. The federation's Syed (1042200555) shows as `No name`. Resolve via channel_directory.json before reporting "User No name sent X".
- **An image transcript that mentions a file path is a vision-call instruction, not a refusal.** When a user-supplied image transcript includes `vision_analyze with image_url: /root/.hermes/cache/images/img_XXX.jpg ~`, call vision_analyze with that path before refusing or summarising the transcript alone. The transcript is the discoverer; the vision call is the actual read.
- **Don't collapse to "the bot said" framing.** The bot does not speak in the source. The humans in the group spoke. Quote them by name + user_id + exact text when the wording is the evidence.
- **Person-of-interest filter must run on the `[Tag|user_id]` prefix, not on the user= field.** Two reasons: (1) user= is almost always `unknown` for group messages, (2) the prefix is the only stable identity across displays-name changes.

## When NOT to use this skill

- Arif asks to OPERATE the gateway (send a message, add a person to the group, restart a service) → route to telegram-ops §A-operate branches.
- Arif asks for a SECURITY audit of the Telegram stack → route to telegram-ops §C3 (forge-telegram-audit reference).
- Arif names a person who has no Telegram presence at all → run the named-person pre-flight from the extraction reference and report the gap; do not pivot to unrelated sources.
- The query is about live minutes-old traffic and the gateway is connected → use Bot API `getUpdates` only if the message is unread AND the human accepts that Bot API cannot fetch historical group messages.

## Reference (one file, named for the topic — never per-session)

`references/parse-gateway-log-line.md` — the exact `re.compile` pattern with edge cases (empty msg, [Replied-to ...] suffix, quote-mismatched wrappers, embedded binary), and the channel_directory.json resolution map.
