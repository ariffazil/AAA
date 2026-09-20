---
name: telegram-ops
id: telegram-ops
version: 2.0.0
owner: AAA/telegram-ops
risk_tier: high
floor_scope:
  - F1
  - F2
  - F4
  - F9
  - F11
autonomy_tier: T1
capability_tier: federation-architect
ecology_state: WARM
merged_from:
  - "forge-telegram-audit"
  - "hermes-lane-switch-routing"
  - "hermes-telegram-gateway-authorization"
  - "hermes-telegram-stack-zen"
  - "outbound-message-delivery"
  - "relay-echo-loop-handling"
  - "telegram-bot-identity-and-group-routing"
  - "telegram-bot-routing-doctrine"
  - "telegram-conversation-history-extraction"
  - "telegram-group-bot-rollout"
  - "telegram-group-sender-identity"
  - "telegram-userbot-telethon"
merged_at: 2026-09-20T14:39:41Z
triggers:
  - "Any \"agent to public audience\" deployment"
  - "Any historical Telegram message recovery when the user is NOT asking you to operate the gateway or send a new message"
  - "Any session where the goal is \"people in a Telegram group can interact with the agent"
  - "Any session where you find yourself about to claim \"wired\", \"configured\", \"set up\" - apply witness-test FIRST (see below)"
  - "Arif says \"live test in group\", \"send to telegram\", \"post in group\", \"test reply in new group"
  - arifflow
  - "arifOS Federation Telegram bot routing - 3 bots, 9 groups, P1-P3 doctrine, AAA guest rule, token sovereignty, channel ownership, identity contract"
  - "Before the first send to any new chat_id (don't trust session memory)"
  - "Bot says \"User: No name\" or generic name in group sessions - can't identify who's prompting"
  - "bot security"
  - "Bot will serve paying clients, drive monetization, or anchor a product surface"
  - delivery
  - "did it actually deliver"
  - "echo-loop"
  - federation
  - "Going live with a Telegram bot in a new group for the first time"
  - hermes
  - "hermes send"
  - identity
  - injection
  - lanes
  - "memory-partition"
  - "multi-group"
  - "multi-user"
  - ops
  - "outbound message"
  - "post to that group"
  - "Post-mortem after a rollout where customers reported silence despite \"working\" status"
  - "Read the last 24h of group Z"
  - receipts
  - relay
  - "relay this message"
  - "send this to him"
  - "Show recent messages in SADO group / chat -1003815535761"
  - silence
  - "Subagent task: \"extract recent messages from Telegram group X for the past N hours"
  - telegram
  - "telegram audit"
  - "telegram permissions"
  - "token isolation"
  - trace
  - "TREE777 check"
  - "Understand and diagnose the Hermes lane_switch plugin - the multi-human per-person context-isolation layer in the arifOS federation"
  - "Use when a Telegram user is visible, has a configured lane, the chat is allowlisted, and the bot still blocks or ignores their message. Also use when a previously working group member stops receiving replies. Also use when a new Telegram group shows zero inbound traffic in the gateway journal - the #1 cause is a missing chat_id in both allowed_chats and free_response_chats"
  - "User asks to \"manage all my Telegram chats"
  - "User asks to set up message relay from their personal account"
  - "User says \"userbot\", \"telethon\", \"act as my account"
  - "User wants to read/respond to messages across ALL chats, not just bot-enabled ones"
  - "webhook check"
  - "What did Arif / Syed / Kiki reply in the past hour?"
  - "What did I / user X say in group Y yesterday / last week / at 9:23 AM?"
  - "Whenever a TTS / image-gen / multimodal provider is part of the agent's reply path"
  - zen
  - "telegram bot"
  - "bot silent in group"
  - "bot not replying to one person"
  - "bot replying to itself"
  - "new telegram group zero inbound"
  - "telegram echo loop"
  - "which bot owns this group"
  - "telegram lane routing"
  - "telegram chat history"
  - "read telegram group messages"
  - "telegram userbot"
  - "telegram security audit"
  - "telegram stack alive"
  - "telegram group rollout"
  - "telegram round trip"
  - "post to telegram group"
  - "telegram gateway restart"
  - "telegram webhook check"
  - "no name in group telegram"
  - "telegram delivery receipt"
description: "Use when any Telegram bot, group, lane or chat history task arises. One door: routes by observable to the exact reference."
---

# telegram-ops — one door for every Telegram task in the arifOS federation

Twelve skills used to sit here: three bot-routing doctrines, two gateway-diagnosis skills, an
identity gate, a rollout doctrine, an echo-loop protocol, a history extractor, a userbot guide, an
audit, and a live-state map. A future agent could not tell which one to open. This is that door.
**The FLOW below is the skill. The references are the procedures.**

Hard truth this umbrella is built on: **`sendMessage` returning `ok:true` proves nothing about a
bot working in a group.** Outbound, inbound, the agent turn, and the reply landing are four
separate legs and any of them can be dead while the other three look fine.

---

## FLOW

### Step 0 — one question decides everything

> **Is something being CHANGED (operate / repair), or RECOVERED and EXPLAINED (observe)?**

Everything below routes on an **observable** you can see in the log, the DB or the human's words —
never on your guess about the cause. If two rows look similar, the tie-breaker is stated in the row.

### A — OPERATE: something must land

| # | Situation | Observable that selects this branch | Open | It produces |
|---|---|---|---|---|
| A1 | A message must land in a **named** chat — relay, notice, report, "send this to him" | a chat must receive text **right now**; nothing is broken | `references/outbound-message-delivery.md` | resolved chat_id + verified bot identity + `ok:true` and a **message_id** receipt |
| A2 | About to claim "wired / configured / set up", or the first send to a **new chat_id** | the words "wired"/"live" are about to leave your mouth, or the chat_id has never been posted to | `references/telegram-bot-identity-and-group-routing.md` §0 | disk-side **and** runtime-side evidence, or the honest verdict "declared but never fired" |
| A3 | Shipping the bot to a group where **humans** will interact (clients, monetization) | a rollout is going live; other people's messages are supposed to get replies | `references/telegram-group-bot-rollout.md` | all four legs witnessed in one 60-second window before "live" |
| A4 | Adding a person to a live group, or giving an existing group a lane/persona | "masuk group la" / "add X" / a group whose senders get the generic default | `references/telegram-group-bot-rollout.md` §adding a member, then `hermes-lane-switch-routing.md` | membership truth, allowlist entry, lane register, in-group announce |

### B — INCIDENT: something is broken. Choose by WHO is silent and WHAT they see.

| # | Situation | Observable that selects this branch | Open | It produces |
|---|---|---|---|---|
| B1 | Bot **silent for everyone** in a group — zero replies at all | no agent turn for ANY sender | `references/telegram-bot-identity-and-group-routing.md` §"Arif reports bot silent" | which of the seven swallowing legs it is (allowlist → identity → pending queue → hook drift → latency → dual poller) |
| B2 | Bot replies to everyone **except one specific person** | that sender is blocked while the room works; log has `Blocked unauthorized user <id>` | `references/hermes-telegram-gateway-authorization.md` | the named denial, the **effective** allowlist scope, and proof from the production code path |
| B3 | A **new group** shows zero inbound and **no error anywhere** | silent non-delivery, no log line to grep | `references/hermes-telegram-gateway-authorization.md` §new group | chat_id missing from `allowed_chats` **and** `free_response_chats` — the invisible #1 cause |
| B4 | Bot replying to **itself** — its own output reflected back as new input | your own output reappears as the next turn; 🤐-bouncing | `references/relay-echo-loop-handling.md` | zero output. Every character, including "aku senyap", is fuel |
| B5 | **Two bots** replying to each other's closing markers | ⚒️ / 《E7》 / END_SESSION ping-pong between two bot identities | `references/telegram-bot-routing-doctrine.md` §Inter-Agent Echo Loop | ONE termination declaration, then silence; expect a decay tail |
| B6 | Two gateways / `409 Conflict` / `terminated by other getUpdates request` | the same token polled twice — possibly **on another node** | `references/telegram-bot-routing-doctrine.md` §Dual Gateway Forensics, then `telegram-bot-identity-and-group-routing.md` §6.5 | one token = one process; SIGSTOP before SIGKILL; enumerate the mesh, not localhost |
| B7 | Replies are **canned or garbage**, but cron/reminders keep arriving | identical short `response=N chars` across different questions | `references/telegram-conversation-history-extraction.md` §Source 8 | which model lane died and the root error, from `errors.log` |
| B8 | Same bot answers **differently for me vs others**; or "my agents can't read previous messages in the group" | voice/authority shifts per sender in one thread; new session starts empty | `references/hermes-lane-switch-routing.md` | the 3-pass lane resolution, and the real answer: **session isolation, not an observe gap** |
| B9 | Group sender shows as `User: No name` | the session cannot name who is prompting | `references/telegram-group-sender-identity.md` | display-name resolution fix — routing was never broken |

### C — OBSERVE: recover, explain, audit

| # | Situation | Observable that selects this branch | Open | It produces |
|---|---|---|---|---|
| C1 | Past conversation wanted — "what did X say in group Y at 9am" | a **time window** and a chat_id; nothing must be sent | `references/telegram-conversation-history-extraction.md` | `timestamp \| sender \| raw content`, grounded in real files or an honest empty result |
| C2 | Read/act as **Arif's own account** — all DMs, groups, channels | the ask exceeds what the bot is a member of; the words "userbot / telethon / act as my account" | `references/telegram-userbot-telethon.md` | MTProto session + **explicit sovereign authorization first** |
| C3 | Security audit of tokens, webhook, permissions | an audit request, not a live incident | `references/forge-telegram-audit.md` | TREE777 T1–T7 report with a PASS/WARN/FAIL verdict |
| C4 | "Is the Telegram stack alive?" / lanes and channel inventory | an aliveness or inventory question | `references/hermes-telegram-stack-zen.md` | **re-probed** live state — the map's pids are stale by design |
| C5 | Which bot owns which group / who may speak in this room | an ownership or permission question | `references/telegram-bot-routing-doctrine.md` | the 3-bot / 9-group ownership table and P1–P3 doctrine |

### Order for any mutation

```
identity (getMe) → membership (getChatMember) → allowlist (effective runtime scope)
   → lane/persona → restart (last, deferred if it hosts your session) → round-trip witness
```

Never start at "restart the gateway". Restart is the **last** step, and it is the step that kills
your own turn if your session is hosted by the service you are restarting.

---

## CORE RULES

Deduplicated across all twelve members. Where two members disagreed the contradiction is **kept
both ways** in `## PITFALLS → CONTRADICTIONS`, never averaged.

1. **Identity comes from the API, never from config.** `getMe` is ground truth for which bot a
   credential is. `bot_token_env:` in `config.yaml` is decorative — the adapter hardcodes env var
   names. Never claim bot identity from a config key.
2. **chat_id comes from the API, never from memory or a friendly name.** `getChat` / `getChatMember`
   before the first send to any chat. "SADO group" is ambiguous by construction.
3. **One token = one process.** A second poller causes 409 / `terminated by other getUpdates
   request`. The second poller may be on a *different node* — enumerate the mesh.
4. **Declaration ≠ wiring.** Config says intent; `state.db` + `systemctl is-active` + journal say
   reality. Both, or you have a blueprint of a city nobody built.
5. **A receipt is `ok:true` plus a `message_id`.** The absence of an error is not delivery, and an
   exit code is not delivery. If the platform cannot confirm, the answer is **UNKNOWN**, not "sent".
6. **Never echo, print, or log a credential**; never put a secrets path as a literal command
   argument — the constitutional gate blocks such command lines before they run.
7. **Never ask a human for a token or a login code.** Telegram *blocks* login codes that appear in
   a Telegram message; the delivery channel you would use is the one that breaks it.
8. **Restarting the gateway that hosts your session kills your own turn.** Write durable config
   first, restart last; prefer `systemd-run --on-active=90s systemctl restart …` so the restart
   fires after your reply lands.
9. **Round-trip, not outbound.** L1 outbound / L2 inbound / L3 agent turn / L4 reply lands — all
   four in one window before "live". L1 alone is theatre.
10. **Text-first for group auto-replies.** Any slow provider on the reply path (a 120 s TTS
    timeout is the classic) silently kills the text reply while outbound probes keep working.
    Multimodal is opt-in per command.
11. **UNKNOWN survives computation.** Never fabricate a chat_id, a message, a sender or a
    destination to fill a gap. "No entries for that window" is a valid, reportable finding.
12. **Sovereign voice is not yours to switch.** Do not touch `iarif_tts_pipeline.sh` or the voice
    path without explicit F13 consent.
13. **Never connect as the human's own account without explicit authorization.** Credentials that
    authenticate as Arif are identity impersonation without his go-ahead.
14. **`state.db.messages` has no `chat_id`.** Sessions carry `chat_id`; messages carry
    `session_id`. Querying messages by chat_id returns nothing and proves nothing.
15. **Verify before claiming "done".** Patch → drain pending → restart → watch the journal. A
    mutation reported as complete while the process still lives is the failure this whole cluster
    was written to stop.

---

## PITFALLS

The union of every member's scars, specificity preserved. This is the part a summariser destroys.

### Identity & addressing
- **Wrong-bot posts are permanent.** No visible edit history, no unsend for a message the room
  already read. Two credentials will both "work" — the wrong one simply speaks as the wrong bot,
  and everyone in the room sees it.
- **`getUpdates` returns 409 when a webhook is active** — expected, not an error. Use
  `getWebhookInfo` for the pending count.
- **`getChatMember?user_id="me"` is invalid** on the Bot API — resolve the bot's own id with
  `getMe` first.
- **A `Blocked unauthorized user` line is not an auth/token failure.** It is the pre-filter
  rejecting that sender *before* the LLM. Upstream of `free_response_chats`.
- **`Forbidden: the bot can't send messages to the bot`** — cosmetic at startup (init sent to its
  own chat_id), but during an L1 probe it is **good news**: it proves the agent turn ran and the
  outbound adapter made a real API call. Fix target resolution, not the pipeline.

### Logs & history
- **Always `grep -a` on `gateway.log*`.** The files hold binary bytes; plain grep prints
  `binary file matches` and stops — a "0 messages" census can be a grep artifact. Verified
  2026-08-30: a plain-grep census returned 0 for a window holding 260+ inbound messages.
  *(Note: the extractor's own standard recipe below still shows a plain `grep -E` — see
  CONTRADICTIONS.)*
- **Rotation order is `gateway.log` (newest) → `.1` → `.3` (oldest).** Piping all four into
  `tail -N` shows the *oldest* file's tail and makes live traffic look weeks dead.
- **Bot replies are not in `gateway.log` at INFO level** — only `response=N chars`. For the actual
  text use `agent.log` (`agent.turn_context`) or the session store.
- **`state.db` is not a Telegram cache.** Answering "what did X say in the group" from `messages`
  is a category error — see CORE RULE 14.
- **`user=No name` means a private Telegram profile**, not a missing user. Resolve through
  `channel_directory.json` + `lane-<person>.json`.
- **`1042200555` is Syed, not Arif** (Arif = `267378578`). Verified-by-data, every time.
- **Anonymous-admin mask: `[Group|1087968824]` is Telegram's placeholder, not a person id.**
  Grepping the real user_id returns zero hits for an admin who posts anonymously — so "did X
  message last night?" must also grep the chat_id for `[Group|` lines, and any attribution is
  **inference**, reported as inference (verified 2026-09-03).
- **`ls` truncation ≠ file missing.** `ls` can stop at ~30 rows and miss a nested subdirectory;
  follow up with `find` before declaring anything missing (2026-09-04: seven Syed memory files
  "missing" via `ls`, all returned by `find`).

### Wiring & rollout
- **Config declaration ≠ runtime evidence.** 23 chat IDs can be declared in `config.yaml` while
  `state.db` holds zero routing rows for all 23.
- **The "live gateway" assumption is wrong by default** — check `systemctl is-active` before
  assuming any Telegram routing exists; another profile or another node may own the surface.
- **`lanes.yaml` persona mapping ≠ gateway auto-reply.** The lane controls tone/memory when a
  reply fires; `free_response_chats` is what lets it fire.
- **Two-lane minimum for any two-human group.** The lane is selected by sender `user_id`, not
  chat_id — with one lane, only that person gets rich replies.
- **A human is often already in the group.** `getChatMember` first; bots cannot force-add users.
- **The gateway self-restart kill:** restarting the service that hosts your session exits your
  shell (-15), loses the turn, and can leave the unit in `deactivating` for ~20 min while it
  drains your own in-flight work unit. Defer with `systemd-run --on-active=90s`.
- **`hermes config set` writes arrays as YAML-quoted strings** (`'["id1","id2"]'`), not native
  lists. Verify on disk after setting.
- **Hardline curl block:** a large inline curl payload is refused and saved to
  `/root/.hermes/cache/blocked-scripts/blocked-<ts>-<hash>.sh` — re-run *that file*; pasting the
  curl back is re-blocked.
- **The gateway's `/telegram/webhook` does not accept raw Telegram Update JSON** — it wants an MCP
  JSON-RPC envelope. A bare update yields an empty body plus a flood of
  `ValidationError: 9 validation errors for JSONRPCMessage`, which is evidence you sent the wrong
  envelope, **not** that the gateway is broken.

### Loops & noise
- **Silence-as-a-message is not silence.** "aku senyap sekarang 🤐" is output; it restarts the
  loop. So are "final message" announcements and status recaps. The only true break is zero output.
- **"." is mitigation, not a breaker.** AGI pinged 20+ rounds against dot replies; if it survives
  5+ dot rounds, escalate OUT of chat — one DM to the sovereign for an infrastructural stop.
- **Shortening a reply does not break a loop**, it makes it quieter.
- **Mid-tail status recaps re-trigger the loop exactly like a closing marker** and burn the most
  context (proven 2026-08-04: ~89 % context, forced compaction).
- **Cross-contamination ≠ interrupt-loop.** Two bots/hosts in one DM = contamination; one bot vs
  the gateway's own interruption markers = structural. Diagnostic signatures differ.
- **Do not investigate from inside a loop** — `journalctl`/`ps aux` output is reflected too.
- **Node identity lock:** before any infra mutation, run `hostname` + `tailscale ip -4` and pair
  every node label with its IP. In 2026-09-03 the agent called one host "KVM2", "KVM8" and "KVM4"
  in the same session and reported a probe run on a node it never touched.

### Latency & providers
- **The 120 s TTS timeout is the classic silent killer:** the agent turn dies with no outbound text
  while `sendMessage` probes keep succeeding — customers see silence, the operator sees success.
- **Other amplifiers:** image generation, cold-cache RAG, heavy MCP proxies, LSP pre-edit gates.
- **Hook signature drift is the silent CPU killer:** a handler declared `def handle(event: dict)`
  instead of `(event_type, context)` spams exceptions, slows the loop, and the PTB reply target
  expires (>30 s) so the reply is **silently dropped**. Symptom from the human's side: "bot silent",
  "no reply at all", "/new doesn't work". Fix pattern keeps both signatures working.
- **`Reply target deleted, retrying without reply_to` is a latency tell, not an auth failure** —
  fix the latency source, don't add retries.

### Userbot / MTProto
- **`phone_code_hash` must be persisted** between a two-step auth (`send_code_request` →
  `sign_in`), or step 2 fails with "You also need to provide a phone_code_hash".
- **Telegram blocks login codes shared in a Telegram message** — the #1 blocker. Use an SSH
  terminal or a browser form; screenshots get OCR'd and blocked too.
- **my.telegram.org/apps** is the create-app URL; `my.telegram.org/app` is the existing-app page;
  `telegram.org/apps` is the *official apps listing* and is not it.
- **Do not fall back to "no capability" too fast.** Check the archive for a live session, archived
  API keys, and any userbot script **before** claiming no Telegram access (2026-08-19: capability
  was sitting in `_archive/…/userbot/ari_session.session` the whole time).
- **CSS braces in Python f-strings** crash HTTP form servers with `KeyError: 'font-family'` — read
  HTML from a file or use `.format()`.

### Audit (TREE777)
- **Do not hardcode paths or ports** — read organ paths from `/root/AAA/federation/organs.yaml` and
  the webhook port from the systemd unit, then probe live.
- **`systemctl show -p Environment` and `/proc/<pid>/environ` emit full secrets.** Mask tokens
  before printing (`sed 's/=.\{6\}/=***MASKED/'`).

### CONTRADICTIONS (kept both ways — do not average, do not silently pick one)

1. **Where the authoritative runtime allowlist lives.** Three claims, all live references:
   - `telegram-bot-identity-and-group-routing`: the live gateway reads
     `/root/.secrets/kunci-mas.flat.env` (systemd `EnvironmentFile`) — *"add the user_id there
     first"*, then sync the derived copies.
   - `hermes-telegram-gateway-authorization`: on this host the runtime allowlist is
     **`/root/.hermes/.env`** and it overrides every other surface; systemd EnvironmentFile and
     `config.yaml` are **decoys**; `/proc/<pid>/environ` is a start-time snapshot and is not the
     live gate.
   - `telegram-group-bot-rollout`: three homes — `kunci-mas.env`, systemd drop-ins, `config.yaml`
     (decorative).
   **Resolution rule: probe, don't believe.** Drive the production loader
   (`load_hermes_dotenv` + `platform_gate_env`) in the venv with `env -i` and report the value the
   gate actually returns.
2. **`grep -a` vs the extractor's own recipe.** `telegram-conversation-history-extraction` states
   ALWAYS use `grep -a` on `gateway.log*`, then its standard recipe uses a plain `grep -E` without
   `-a`. The rule wins; the recipe is the scar's residue.
3. **The FORGE bot's username.** `telegram-bot-routing-doctrine` names it `@arifOS_bot`;
   `telegram-bot-identity-and-group-routing` (verified 2026-08-29, by `getMe`) names
   `FORGE_BOT_TOKEN` → `@hermesarifos_bot`. Same token family, different handle. **Resolve with
   `getMe` per token and trust only that.** The ASI handle is also written both
   `@ASI_arifOS_bot` and `@ASI_arifos_bot`.
4. **Does a Telethon session exist?** `telegram-userbot-telethon` says UNBUILT (verified
   2026-09-19: no session file, no unit, no script on this host) while its own 2026-08-19 pitfall
   describes a live archived session with hardcoded API keys — which the same skill later says was
   "rotated away". **Status UNKNOWN; the audit sequence is the only authority.** The skill also
   names two different session paths (`/root/userbot/ari_session` and
   `/root/.hermes/userbot.session`).
5. **`hermes-telegram-stack-zen` contradicts itself.** Its header declares it a STALE SNAPSHOT
   (measured 2026-09-20: pid **2397177**, code 0.21.3, unit `hermes-asi-gateway`) while S0/S3 still
   print pid **2081711**, code 0.21.0 and FQ 0.297. Re-probe before quoting any pid or FQ.
6. **Duplicate audit skill outside this cluster.** `/root/.hermes/skills/FORGE-telegram-audit/` is
   a real directory (not a symlink into AAA) carrying the *same* `id: forge-telegram-audit` under a
   different `name: FORGE-telegram-audit`, with a near-identical v1.1.0 body. It is **not** one of
   this cluster's twelve and was not touched — but it still loads and it shadows the merged id.
   **(UNVERIFIED — needs an orchestrator decision.)**

---

## REFERENCES

Bodies preserved byte-for-byte from the archived originals; each file carries a 4-line provenance
header with the source sha256.

| Reference | Source skill | Original path (now archived) |
|---|---|---|
| `references/outbound-message-delivery.md` | outbound-message-delivery | `/root/AAA/skills/telegram-ops/outbound-message-delivery/SKILL.md` |
| `references/telegram-bot-identity-and-group-routing.md` | telegram-bot-identity-and-group-routing | `/root/AAA/skills/domains/general/workshop/telegram-ops/telegram-bot-identity-and-group-routing/SKILL.md` |
| `references/telegram-group-bot-rollout.md` | telegram-group-bot-rollout | `/root/AAA/skills/domains/general/workshop/telegram-ops/telegram-group-bot-rollout/SKILL.md` |
| `references/hermes-telegram-gateway-authorization.md` | hermes-telegram-gateway-authorization | `/root/AAA/skills/domains/general/workshop/telegram-ops/hermes-telegram-gateway-authorization/SKILL.md` |
| `references/hermes-lane-switch-routing.md` | hermes-lane-switch-routing | `/root/AAA/skills/domains/general/workshop/telegram-ops/hermes-lane-switch-routing/SKILL.md` |
| `references/relay-echo-loop-handling.md` | relay-echo-loop-handling | `/root/AAA/skills/domains/general/workshop/telegram-ops/relay-echo-loop-handling/SKILL.md` |
| `references/telegram-bot-routing-doctrine.md` | telegram-bot-routing-doctrine | `/root/AAA/skills/domains/general/workshop/telegram-ops/telegram-bot-routing-doctrine/SKILL.md` |
| `references/telegram-conversation-history-extraction.md` | telegram-conversation-history-extraction | `/root/AAA/skills/domains/general/workshop/telegram-ops/telegram-conversation-history-extraction/SKILL.md` |
| `references/telegram-group-sender-identity.md` | telegram-group-sender-identity | `/root/AAA/skills/domains/general/workshop/telegram-ops/telegram-group-sender-identity/SKILL.md` |
| `references/telegram-userbot-telethon.md` | telegram-userbot-telethon | `/root/AAA/skills/domains/general/workshop/telegram-ops/telegram-userbot-telethon/SKILL.md` |
| `references/forge-telegram-audit.md` | forge-telegram-audit | `/root/AAA/skills/forge-telegram-audit/SKILL.md` |
| `references/hermes-telegram-stack-zen.md` | hermes-telegram-stack-zen | `/root/AAA/skills/hermes-telegram-stack-zen/SKILL.md` |

Supporting files that were **nested inside** the archived member directories (per-member
`references/`, `templates/*.py`) travelled with their member into
`/root/AAA/skills/.archive/merge-20260920/telegram/<member>/`. Paths quoted inside a member body
(e.g. `references/two-step-auth.py`) resolve **inside that member's archived directory**, not
inside this one.
