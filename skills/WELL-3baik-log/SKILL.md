---
name: WELL-3baik-log
description: "Capture 3baik Telegram replies into the wellbeing joy log."
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# 3 Baik Hari Ini — reply capture

When a DM from Arif starts with `3baik:` (case-insensitive):

1. Parse the text after the colon. Items are separated by `;` or `,` or newlines. Take up to 3 items, verbatim, no paraphrasing.
2. **Recording is automatic — do NOT append to the log yourself.** `state-intake-hook` on the gateway writes the JSONL line deterministically at message receipt, same contract: `{"timestamp_utc", "items", "raw"}` — items + timestamp only, no interpretation, no mood inference (data minimization directive). You writing it too creates duplicate streak rows (LAW 8 — one owner). Briefly check the tail of `/root/WELL/state/3baik_log.jsonl` to confirm the row landed.
3. Reply with ONE short line — "Direkod ✨" or "Sah — tak ada pun dikira." Nothing else. No follow-up question.

## Rules (witness-ratified contract, 2026-09-16; capture-owner amendment 2026-09-29)

- `tak ada`, `skip`, `bad day`, empty, or fewer than three items — ALL valid replies. Store what was given (`items` may be `["tak ada"]`). Never prompt again, never cheer up uninvited.
- Never diagnose. Never suggest medical action from this data. This is joy accounting, not surveillance.
- Do not turn gratitude into compulsory positivity — an honest "bad day" entry is a SUCCESS of the ritual, not a failure.
- If the row has NOT landed within a minute, or the log is unwritable, say so honestly in one line. Never claim success falsely.
- This log feeds one thing only: the streak counter in the 22:00 digest ("Streak 3 baik: N hari").
- The JSONL entry itself (timestamp + items) is the durable inbound receipt — record nothing beyond it, forward nothing to general memory.
