# Worked example — "why is person X angry at the agent" outbound forensics (2026-08-23)

Trigger: Arif asked "Kenapa abang Syed marah dengan agent hari ni". There were NO messages from Syed today — the failures were yesterday. Diagnosis required recovering what the BOT SENT, not what was received.

## Subject resolution
- Syed = Telegram user_id 1042200555 (hidden profile → logs as `user=No name`), DM chat=1042200555, SADO group chat=-1003815535761.

## Timeline recovered from gateway.log (inbound + outbound)
- Fri 2026-08-21 23:34 DM "Cari kan aku supplemnt utk gerd yg review bagus" → real answer delivered.
- Fri 23:38 "Bagi gmbr" → 132.3s, `response=47 chars`, `Skipping transcript persistence for context-overflow failure in session 20260816_154725_68f631b8`, then `Sending response (138 chars)` = canned error. Image never delivered.
- Sat 2026-08-22 07:39 two scam-bankruptcy scam-spam forwards, 13:52 "Mastton prop tahN bapr lama dalam badan?", 15:49 "N heloo" → every turn `response=47 chars` + `Sending response (143 chars) to 1042200555` = the SAME canned rate-limit template, four times.
- Sat 14:45 SADO group "Server terbakar ni" → normal 641-char streamed answer (group lane healthy; only the DM was dead).
- Sat 22:30 cron job 8fef34d562a0 still DELIVERED to telegram:1042200555 → bot pinged him on schedule while his real questions got error templates.
- Sun 2026-08-23: zero inbound from Syed all day → reported honestly that same-day Telegram evidence does not exist.

## The 429 dead-chain (agent.log 2026-08-22 07:40:09–13, ~4 seconds)
i-arif 429 token-plan exhausted → Fallback mimo-v2.5-pro: HTTP 400 "Param Incorrect — `text` is not set" (MiMo chat/completions is NOT a usable chat fallback seat — it burns a hop in every cascade; provider quirk, durable) → qwen3.8-max qwen-token-plan-team insufficient_quota → qwen-token-plan-arifos insufficient_quota → qwen-token-plan-ariffazil insufficient_quota → MiniMax-M3 429 "Token Plan usage limit reached (2056)" (credential pool marked MINIMAX_API_KEY exhausted, rotating) → groq gpt-oss-120b HTTP 400 "messages[31].content must be a string". Chain dead → canned template sent.

Two OVERLAPPING failure modes: (a) every provider seat exhausted simultaneously, (b) DM session 20260816_154725_68f631b8 oversized since 08-16 (context-overflow on 08-21) — fails even with live providers.

## Decoding canned replies
Gateway source `/usr/local/lib/hermes-agent/gateway/run.py` → `_gateway_provider_error_reply()`. Rate-limit variant: "⏱️ The model provider is rate-limiting requests. Please wait a moment and try again." (~143 chars with platform wrapper). Identical `Sending response (N chars)` lengths across DIFFERENT inbound turns = template, never a real answer. All templates are English ⚠️/⏱️ strings — instantly recognizable to a BM-speaking user as an error, which is exactly why the human got angrier with each reply.

## Recipe (generalized)
1. `now`/`date` FIRST — "hari ni" is a claim. Check whether the person messaged today at all.
2. Resolve person → user_id + chat_ids (channel_directory.json + lane files; hidden profiles log as "No name").
3. Grep gateway.log for their chat_ids over a 48h window: inbound lines AND `Sending response` lines.
4. Identical outbound char counts → pull `_gateway_provider_error_reply()` from the gateway source; report what the human actually saw.
5. agent.log same window: `Fallback activated` chain + `429|quota` = dead-chain window; `Skipping transcript persistence for context-overflow failure in session <id>` = oversized session (reset candidate).
6. state.db assistant rows for the session: empty content = tool-call-only turns, not lost replies.
7. Check cron deliveries to that user_id — scheduled pings landing while interactive replies fail is the insult pattern; surface it explicitly in the answer.
8. Live-probe the model chain (FED /v1/chat/completions with master key) before promising recovery; name the seat that actually answered (here: i-arif routing through glm-5.3, FED green).

## Outcome delivered
Full cause chain reported to Arif with timestamps; DM session reset offered as the one-minute fix, held for F13 go-ahead.
