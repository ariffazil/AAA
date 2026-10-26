---
name: message-delivery-triage
description: "Use when a sent message never reached the human."
---

# Message Delivery Triage

When the agent believes it sent something and the human received nothing, the work is usually done and the wire is broken. Find which gate failed. Never regenerate the content — the artifact already exists.

## Four gates, check in this order

1. **PRODUCED** — the answer or attachment exists (session output, file on disk, queue row).
2. **TARGETED** — the destination chat id is the human's, not the bot's own.
3. **DISPATCHED** — the adapter handed it to the platform without a refusal.
4. **DELIVERED** — the platform accepted it (message id returned, no exception).

Report the gate that failed. "Delivered" is only true at gate 4.

## Gate 2 first — the self-address trap

The platform rejects a bot addressing itself: `Forbidden: the bot can't send messages to the bot`.

Symptom set:
- Log line `Blocked unauthorized user <bot_id> in chat <bot_id>`, repeating every 30–60s
- A contact / channel-directory entry whose id equals the bot's own user id
- Session rows whose `chat_id` equals the bot id, session_key ending `dm:<bot_id>`

Diagnosis: the bot's own outbound messages come back through the update feed and are treated as inbound. Fix in this order:

1. The own-message / self-echo filter must run **before** the authorization gate, in **every** inbound handler — text, command, location, media. Patching only the text handler leaves the loop alive on media and location.
2. Remove the self entry from the platform contact/directory file (back it up first).
3. Restart the gateway from outside the gateway process.

An own-echo is not an unauthorized user. It is not an inbound message at all — it must never reach auth, batching, or the observed transcript.

## Gate 3 — read the queue, don't guess

Produced-but-unsent content persists with its failure reason. Query the delivery queue and read `last_error` — `state='abandoned'` plus a Forbidden self-send message is the **same** defect as gate 2, not a new one. Fix the root, then drain. Sessions for the affected chat id with `ended_at IS NULL` are still open and still accumulating.

## Gate 2b — cron delivery targets

`deliver: origin` resolves to wherever the job was created. Safe when created in the human's DM; dangerous when created elsewhere. Before blaming cron for lost output, enumerate each job's resolved `origin.chat_id` and compare to the human's id. Only jobs that actually resolve to the bot id or a dead chat are culprits — do not rewrite all of them on suspicion.

## Restarting the gateway

A session running inside the gateway cannot restart it. SIGTERM propagates to its own children, and background wrappers or scheduled timers get killed mid-flight — `systemd-run` and `nohup` both fail. Hand the single command to the human and wait. Do not retry around the guard.

## Reading state.db without guessing the schema

Session tables here have `id`, `chat_id`, `session_key`, `origin_json`, `created_source`, `last_activity_at`, `ended_at` — there is no `session_id` and no `created_at`. A `no such column` error means the query was written from memory; run `PRAGMA table_info(sessions)` first.

## Do not

- Do not re-generate the answer to "fix" delivery. Content was never the problem.
- Do not report delivered because send was attempted. Gate 4 evidence only.
- Do not quote the body of abandoned personal messages into a shared room to prove they exist. Report count and timestamps.
