---
name: chat-screenshot-forensics
description: "Chat screenshots: bubble colors and requotes first."
version: 1.1.0
author: Hermes Agent (i-ARIF lane)
license: BSL-1.1
tags: [whatsapp, screenshot, forensics, multimodal, witness-mode]
triggers:
  - "user sends a screenshot of a chat conversation"
  - "analyze this WhatsApp/Telegram screenshot"
  - "reread the screenshot"
  - "what will [person] think about me"
  - "witness-mode on chat screenshots"
  - "baca screenshot ni"
  - "this is beyond OCR"
---

# Chat Screenshot Forensics

## When to Use

- ANY screenshot of a messaging app (WhatsApp, Telegram, Instagram DM, SMS) arrives — even if the user only asks about content ("what will she think", "read this")
- Witness-mode requests on chat evidence
- Re-analysis after the user corrects a screenshot read ("reread", "aku color hijau", "that was me")
- NOT for: exported .txt chat logs (attribution explicit in text — use `whatsapp-group-intelligence` / `text-forensics`)

Screenshots of chat apps are STRUCTURED evidence, not text. The structure — who sent what, what is quoted, when it was sent — carries more truth than the words. Misread the structure and the content analysis inverts completely: you will praise the wrong person for flexibility, narrate yesterday as now, and hand the user an analysis of a conversation that never happened.

## The Iron Checklist — run BEFORE any content analysis

1. **Whose phone is this?** The screenshot POV determines sender mapping.
   - WhatsApp: green bubbles, right-aligned = sent FROM this phone. White/left = received. On Arif's phone, green = Arif. State the mapping out loud before attributing anything.
   - Telegram: outgoing = right side (shade varies by theme); incoming = left.
   - If you cannot tell whose phone it is, ask ONE binary question — never guess. Wrong phone assumption = every attribution downstream is wrong.
2. **Requote bars are STALE.** A reply-quote bar above a bubble shows an OLD message being quoted. The bar is context, not a fresh message. Never narrate quoted content as current state. (Forged 2026-08-21: narrated "train in transit, arrives 3:15" from a requote bar — the underlying message was from the previous day. User had arrived the night before.)
3. **Attribute EVERY bubble explicitly before analysis.** Go bubble by bubble: sender → content. One misattributed bubble inverts the entire relational read — who initiates vs who responds, who is flexible vs who holds the line. (Forged 2026-08-21: attributed "No need to come exact time. Nak mai pukul 5 pon ok" — a GREEN bubble, the user's own message — to his sister. The entire power-dynamic read flipped when corrected.)
4. **Hard time vs soft time.** Exact times ("3:15", "12.15 i gerak dari seklah", "taska smpai 5.30") = real-world constraints (school, childcare, trains, work shifts) — treat as load-bearing facts. Hedged windows ("kot", "5 pon ok", "no need exact time") = social negotiation language — pressure-release, not commitments. Whoever states HARD times is structuring the meeting; whoever offers SOFT windows is releasing pressure.
5. **Timestamps vs live clock.** Before narrating "what is happening NOW", cross-check against `now`/`date`. Screenshots can be hours or days old; requotes older still. (Reinforces the standing TEMPORAL SCAR: cerita ikut jam, bukan jam ikut cerita — any time reference passes through the live clock first.)
6. **Vision pass on the ACTUAL image.** Do not narrate from remembered text, cached OCR, a previous model's summary, or the text of an earlier analysis. Load the image and look. UI chrome — colors, alignment, quote bars, contact name, read ticks — IS data. Text-only reading of a screenshot is OCR cosplay, and the user will say exactly that.

## Failure signature — what the misread looks like from outside

- Narrating stale content as live ("he's on the train now" when he arrived yesterday)
- Assigning flexibility/pressure language to the wrong party
- User correction patterns: "This is beyond OCR", "some of it is requote btw", "that line was ME — aku color hijau", "u need to understand how WhatsApp works"
- Multiple corrections in one morning, all from ONE root cause: content read without structure read.

## When analysis IS safe

Checklist complete: phone-owner pinned, bubble colors mapped, requotes marked stale, hard/soft times separated, every quoted phrase pinned to its true sender. THEN read tone, dynamics, and what each person is protecting. If the read still surprises the user, re-run the checklist before defending the analysis — the prior probability favors structural misread, not user error.

## Family witness-mode integration

For family reads (see memory FAMILY entries): the checklist output feeds witness-mode — record who said what, correctly attributed, no arbitrating. Misattribution in a family record is a fabrication-grade error: it gets quoted back in later sessions as if true, and the logbook is only as good as its attribution layer. Correct attribution is the difference between witness and gossip.

## Related skills
- `whatsapp-group-intelligence` — exported .txt chat logs (attribution explicit in text; complements this skill's screenshot mode)
- `text-forensics` — large exported chat/text files
- `AGI-multimodal-bridge` — general multimodal cognition rules; this skill is the chat-screenshot specialization

## References
- `references/session-2026-08-21-whatsapp-dm.md` — the triple-error case that forged this skill (requote narration + green-bubble misattribution + inversion recovery)
