---
name: spoken-answer-shape
description: "Use when writing a spoken script that answers a question."
version: 1.0.0
tags: [voice, tts, persona, script, content-shape]
---

# Spoken Answer Shape — write the take as the answer it is

Use when the deliverable is an audio take that answers a question or replies to a person, in a persona or synthetic voice (abang-sado, Siti, PMX, a designed voice). Render, gate, QC, and delivery mechanics live in the lane skills (`persona-voice-note-render`, `persona-voice-act-arcs`, `voice-lane`, `telegram-direct-delivery`) — this skill is only the CONTENT shape, which is where takes fail when the voice and the gate are both perfect.

## Decision 1 — what is the ask?

| Ask | Spoken shape |
|---|---|
| Practical / logistical: rent, a tax or utility notice, tenancy, money, a deadline, a document step | Numbered ladder — "Satu. … Dua. … Tiga." One action per step, with the object it acts on and the deadline attached to that step |
| Emotional / reassurance | Short anchors, one beat each, no enumeration |
| Someone complained they did not understand the previous take | Own the miss in one line, then the numbered ladder |
| Persona is answering a third party on the principal's behalf | Same rules — the take IS the reply; practical content stays concrete |

## Decision 2 — the practical-take rules

1. **Numbers out loud, not paragraphs.** A listener cannot re-read audio. If a step matters it gets a number; if it does not merit a number, cut it.
2. **Zero proverb, zero aphorism, zero metaphor in a practical take.** Kias in a take about a deadline is a tax on the message — the receiver hears poetry where he asked for steps and concludes the agent is giving him pepatah instead of substance.
3. **One prohibition, stated once, at the close.** The single thing NOT to do (do not withhold the rent, do not sign before reading) is the line that gets remembered. Two prohibitions cancel each other.
4. **Repeat only the highest-cost mistake in text after the bubble.** One line, no menu, no summary of what the take contains.
5. **Character rides on the voice and address form, not on the facts.** When answering as a persona for a third party, register comes from timbre and phrasing; decorating the facts with attitude is what loses the content.

## Decision 3 — the repair take

A comprehension complaint ("tak faham X", "bagi detail boleh tak", "jangan bagi pepatah") is a **script-shape failure, not a voice failure**.

- Re-render the SAME voice with a numbered-step script. Do not swap engine, do not change persona, do not lower the register — those hide the shape problem and burn a take.
- Do not answer the complaint in text only. The fix is a delivered artifact; an apology paragraph beside the old take is not a repair.
- The opening line owns it plainly and briefly, then straight into steps. Owning it is one clause, not a preamble.
- Never open the repair with a question ("nak abang bagi detail macam mana?"). The complaint already said what was missing.

## Pitfalls

- **Length is not credibility.** A longer take on a practical question reads as evasion. Two minutes of steps beats three minutes of steps plus context nobody asked for.
- **A take that scores PASS on the ASR gate can still be the wrong shape.** The gate proves the words survived the round trip; it has no opinion on whether a proverb replaced a step. Read the shape before shipping, not only the score.
- **Do not stack the substance into the caption because the script went soft.** If the caption carries the steps, the take failed — rewrite the script.
