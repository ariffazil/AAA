# 2026-08-29 Session — SADO Group Live Test: Bot Identity Framing + Direct Bot API Outbound Pattern

Captured during the SADO Telegram group (`-1003815535761`) live-test deployment session. Two new class-level lessons emerged that fit the SKILL.md body but are tied to a specific workflow — captured here as reference, not as inline fragment.

---

## Lesson 1 — F9 Anti-Hantu: Bot Identity Framing for Multi-Stakeholder Group Posts

**Trap:** Agent is asked to send a "live test" or any outbound message into a Telegram group that contains a non-owner stakeholder (e.g., SADO group with Arif + Syed + @ASI_arifOS_bot). Agent posts directly without surfacing the bot identity + ownership context in the bridge output. The non-owner stakeholder (Syed) sees "Hermes replied" and assumes the bot is *their* coaching assistant (or their org's channel). F9 fabrication-by-omission breach — they build expectations on a phantom.

**Why this is class-level, not SADO-specific:** Any group with 2+ named stakeholders from different "ownership domains" carries this risk. SADO today, but applies to any group with mixed client/prospect/sovereign/sidekick participants.

**Detection signals (apply BEFORE any outbound post into a multi-stakeholder group):**
- Group has 2+ named humans who don't share the bot owner's context
- The group has been discussed as someone-else's customer/client/prospect space
- The bot reply could plausibly be mistaken for an org-channel reply ("coach reply", "admin reply", "their AI")
- The bot is owned by Arif (or any single person) but lives in a group where others might assume shared ownership

**Fix pattern — surface bot identity before the post lands:**
- ✅ One line in the bridge output BEFORE posting: "Bot identity: @ASI_arifOS_bot (Arif punya agentic infra, bukan [other stakeholder] punya [X])"
- ✅ State what scope the bot operates in (training/nutrition/etc., not "everything")
- ✅ Post the message
- ✅ Confirm with `message_id` + `chat.username` from the API `ok:true` response — NOT self-report
- ❌ Don't post silently and let stakeholders infer ownership from the username alone — many won't read past the message body
- ❌ Don't assume the username alone makes ownership obvious — "@ASI_arifOS_bot" reads as "Arif's bot" to Arif but as "an AI assistant" to Syed

**Verified 2026-08-29:** SADO group live test posted as @ASI_arifOS_bot with explicit identity framing in the bridge. Post: "Bot identity: @ASI_arifOS_bot (Arif punya agentic infra, bukan Syed punya coaching bot)." Syed sees post framed as Arif's bot assistant, not his coaching bot. F9 surface preserved. message_id 13954, `ok:true`.

**Output shape:**
```
[1 line: bot identity + whose infra + who stakeholder might mistake it for]
[1 line: scope of operation]
[Post the message — curl with -d chat_id + -d text + -d parse_mode]
[1 line: confirm with message_id + chat.username from API JSON]
```

**Distinction from existing pitfalls:**
- "Sovereign Testimony Is Fact, Not Evidence" = user declares identity, agent accepts. This = agent declares ownership before posting into a group where ownership could be misread.
- "Moral Reactions — Witness, Don't Analyze" = user has emotional load. This = no emotional load, just ownership framing.
- "Quotient Receipt Ingestion" = user seals state. This = agent delivers state to multiple viewers, all need to read it correctly.

**The rule:** When the bot posts into a group with multiple stakeholders, the FIRST thing any non-owner sees is the bot identity + scope. If that line is missing, they will read the rest of the post through whatever assumption they hold. Once assumption locks in, it's hard to walk back without re-posts and clarification noise.

---

## Lesson 2 — Direct Bot API Curl for Outbound Smoke Tests (Skip Gateway Routing)

**Trap:** Agent wants to verify a Telegram bot can post into a group. Routes the test through the running gateway (`hermes gateway run --replace`). Gateway is busy with other sessions, queues the test, or surfaces `Flood control exceeded` warnings that look like failures but are actually auto-retry on success. Agent misreads the warnings, declares the test failed, escalates unnecessarily.

**Why this is class-level, not session-specific:** Every "live test" / outbound smoke test / can-this-bot-post-here scenario should default to direct Bot API curl. The gateway is for production auto-reply flow, not for one-shot verification.

**Detection signals (apply BEFORE running any outbound Telegram test):**
- Task is "verify bot can post" / "live test" / "send one message to confirm X works"
- The test is single-shot, not a flow that needs lane routing or memory persistence
- Gateway log will show `Flood control` warnings on outbound retries (visible noise, not failures)
- Direct Bot API curl returns deterministic `{ok:true, message_id, chat}` JSON

**Fix pattern — Direct Bot API curl as default for one-shot outbound tests:**
```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendMessage" \
  -d chat_id="-1003815535761" \
  -d parse_mode="Markdown" \
  -d text="..." | jq -c '{ok, message_id: .result.message_id, chat: .result.chat.username}'
```

**`ok:true` + `message_id` = delivered (API response, not self-report).** Use this for verification, not the gateway log.

**Disambiguating gateway `Flood control` warnings (from journalctl or gateway.log):**
- `WARNING hermes_plugins.telegram_platform.adapter: Telegram flood control, waiting Ns` = gateway auto-retrying outbound. NOT a failure. The next log line will confirm send success.
- `ERROR ... sendMessage ... code: 429` = persistent flood. Wait 30-60s, retry once, then HOLD.
- `ERROR ... code: 401` = token rejected. Token drift — check vault/drop-in, not flood.
- `pending_update_count > 0` on webhook = delivery stuck on inbound side, not outbound.

**Verified 2026-08-29:** Gateway log showed 4+ `Flood control, waiting 36s` warnings during the outbound SADO post. The actual direct-curl `sendMessage` returned `ok:true, message_id: 13954` immediately. The warnings were gateway auto-retry for OTHER sessions (the agent was busy with prior turns, residual traffic, etc), NOT for the test post.

**Caveats / when to NOT use direct curl:**
- Direct curl bypasses lane routing — no `arif-sado` vs `syed` lane distinction. Fine for one-shot smoke test, NOT for production auto-reply flow.
- For auto-reply round-trip tests (user posts in group → bot auto-receives via webhook → bot auto-replies), the gateway IS the path. Direct curl only for outbound verification.
- If the task requires lane-specific memory, persona config, or skill routing — the gateway is mandatory. Don't bypass for "faster" testing.

**Two-step round-trip test (the proper verification):**
1. **Outbound smoke (Bot API curl):** confirm bot can post. Captures `message_id`.
2. **Inbound round-trip:** Arif or stakeholder replies in group → bot auto-receives via webhook → bot auto-replies. Captures `message_id` of bot's auto-reply.

If step 1 works but step 2 doesn't, the failure is almost always:
- `require_mention=true` and reply didn't @-mention the bot
- Lane routing mismatch (lane configured for user X, message from user Y → silence)
- `free_response_chats` missing the group ID (gateway prefilter rejects)
- Webhook `pending_update_count > 0` (delivery stuck — see existing Webhook Troubleshooting)

Verify each before declaring the test failed.

**Distinction from existing patterns:**
- "Verification-as-terminal-state" = agent verifies work before claiming done. This = agent uses the right tool (curl vs gateway) for the verification.
- "BANYAK TANYA" = over-asking. This = under-asking by relying on a heavier tool (gateway) when direct curl answers the question.

**The rule:** For one-shot outbound verification, curl direct. For multi-turn production auto-reply, route through the gateway. Match the tool to the verification scope. Don't read gateway `Flood control` warnings as failures — they're auto-retry, not signal.

---

## Why these two lessons belong together

Both emerged from the same task: "live test sent to that telegram group." Lesson 1 is about the bridge output (what to say before posting). Lesson 2 is about the execution path (which tool to use). Different layers, same workflow.

If you ever see "live test" + a Telegram group with multiple humans → load both. Lesson 1 fails first (omission of identity framing) — that's the visible scar. Lesson 2 fails second (agent misreads gateway warnings and escalates) — that's the noise that compounds the visible scar.
