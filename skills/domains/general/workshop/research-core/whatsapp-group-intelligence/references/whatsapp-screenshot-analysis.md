# WhatsApp Screenshot Analysis — Multimodal Reading Protocol

Forged 2026-08-21 from a live session where the agent misread the same WhatsApp screenshot THREE times, with two explicit user corrections ("This is beyond OCR. Reread again" and "No need to come exact time tu aku yang kata la. Aku color hijau"). Every failure mode below was caught live. This is the protocol that replaces them.

## When this applies

- User shares a **screenshot** of a WhatsApp chat (not an export) and asks for interpretation — especially family/personal conversations where getting the attribution wrong damages the analysis
- Any task where you must say "who said what" from a chat image

## The three failure modes (all observed in one session)

### Failure 1: Narrating from relayed text instead of looking at the image
The user quoted a fragment of the chat in their message. The agent analyzed THE FRAGMENT as if it were the whole picture, building a story ("she's juggling schedules, worried about you") from partial data. The screenshot contained more context that inverted the reading.
**Rule:** When a screenshot exists, the image is the source of truth, not the user's relay of it. Load the image FIRST (find it in the gateway cache — e.g. `/root/HERMES/cache/images/` for Telegram-received images), analyze it fully, THEN compare against what the user said.

### Failure 2: Treating quote-bars as separate messages
WhatsApp reply-quote bars (the compressed gray block above a new message showing "You: <old text>" or "Name: <old text>") were read as fresh standalone messages. This fabricated a narrative: an old message re-quoted in a reply bar was narrated as a present-tense event ("he is on the train now") when it was an echo of something said earlier.
**Rule:** Every visual block must be classified as either (a) NEW message text or (b) QUOTED OLD text inside a reply bar. The quote bar shows the sender name + truncated original. The new content is what appears BELOW the bar. Never build chronology from quote-bar content — it is history, not present.

### Failure 3: Wrong speaker attribution from not checking bubble side
In WhatsApp, the phone owner's messages are on the RIGHT (green), the other party's on the LEFT (white/gray). The agent attributed a message to the wrong party ("she gave you the exit — 'No need to come exact time'") when in fact the phone owner had said it. The user corrected: "tu aku yang kata la. Aku color hijau."
**Rule:** For EVERY message block, explicitly record side (left/right) before attributing. In WhatsApp: RIGHT = phone owner (the person who took the screenshot), LEFT = the other party. In Telegram the convention differs — check the platform first. When the user is the phone owner, right-side messages are THE USER's own words.

## Mandatory extraction protocol

For each screenshot, produce a structured block-by-block ledger BEFORE any interpretation:

```
[timestamp] [SIDE: left/right] [QUOTE-BAR: sender + old text, or none] → [NEW TEXT] [ticks: ✓/✓✓/✓✓blue]
```

Only after the ledger is complete do you interpret. Ticks matter: ✓✓ (delivered, not read) vs ✓✓blue (read) vs ✓ (sent) change the meaning of silence after a message.

## What lives beyond OCR (the multimodal layer)

- **Bubble direction** = speaker identity (the whole point)
- **Quote bars** = reply-threading; an echo, not a new statement
- **Standalone emoji bubbles** = emotional register shifts (a solo 😂 after 11 years of silence is a data point, not decoration)
- **Tick states** = whether the other party has SEEN the latest message
- **Punctuation/register** ("Okiee", "keee", "Alright2") = warmth level, casualness
- **Who asks questions vs who gives cushions** = the care direction in the exchange

## Verification rule

If the user corrects your attribution once, re-read the ENTIRE image block by block with the ledger protocol — do not patch the single error and move on. Attribution errors cluster: if one speaker was wrong, other attributions were likely built on the same wrong assumption.

## Cross-references

- `1on1-tenure-analysis.md` — 1:1 export protocol (for full exports, not screenshots)
- `event-anchored-retrieval.md` — temporal anchoring when the screenshot references external events
- SKILL.md §Cross-Medium Verification — screenshots vs exports vs live gateway logs are different mediums; never merge narratives across them without noting it
