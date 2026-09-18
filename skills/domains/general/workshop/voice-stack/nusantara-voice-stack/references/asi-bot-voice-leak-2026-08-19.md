# ASI Bot Sado Voice Leak — 2026-08-19

## What Happened

Syed posted "smlm aki xleh tido" in the SADO Telegram group at ~07:47 MYT.
The **ASI bot** (the main Hermes bot, NOT the Sado-locked persona) replied with:

1. A long message about demam, MC, thermometer, gejala fizikal
2. **A female voice note** — violating Sado group policy (F10: male voices only)
3. **Leaked internal processing tags** visible in the output:
   `][]>minimax[|></message></mm:think>`

## Root Cause

The Sado voice lock (`ttv-voice-2026081808404926-BdoQh6ec`, 0.83x, neutral) is wired into the
**Hermes ASI persona** and the `nusantara-voice-stack` skill, but the lock is at the
**agent personality level**, not at the **Telegram routing/hook level**.

When the ASI bot (not the Hermes ASI sub-agent) responded in the SADO group, it used
its default voice pipeline — which for that turn was female (YasminNeural) — because
the routing did NOT enforce the Sado-locked-voice hook for SADO group messages.

## Leaked Tags

The internal model processing tokens leaked into Telegram output:
`][]>minimax[|></message></mm:think>`

These are model-internal XML tags that should be stripped before Telegram delivery.
The gateway text sanitizer did NOT catch them. This is a separate rendering/config
issue but surfaced in the same event.

## Impact

- Syed saw a female voice note from "Arif's agent" in his own group
- Syed saw internal processing tags that suggest machine-generated content
- The policy violation undermines the trust architecture of the Sado lane
- Arif had to wake up to this leak

## Remediation Direction (T2 — requires Arif review)

The fix is NOT in the skill — it's in the Telegram gateway routing:

1. **Group-level agent routing:** When the SADO group (-1003815535761) receives a message,
   route it to the Hermes ASI (Sado-locked) agent profile, NOT the default bot.
2. **Voice hook at gateway level:** Before TTS generation, check: is this output going
   to SADO group? If yes → enforce male voice only, no persona tags.
3. **Tag sanitizer:** Strip model-internal think tokens before Telegram delivery.

Until fix, manual monitoring: Arif must check bot replies in SADO group for gender
violations.

## Evidence

Screenshots (2026-08-19 ~09:19 MYT):
- `/root/.hermes/cache/images/img_3e712e224cdb.jpg` — ASI reply with female voice note
- `/root/.hermes/cache/images/img_31b1f598877a.jpg` — Syed's "xleh tido" + ASI demam reply

## Related

- `references/syed-persona-lock.md` — the policy this event violated
- `nusantara-voice-stack` §13 — Voice Policy dual-lane
- SADO group ID: -1003815535761
