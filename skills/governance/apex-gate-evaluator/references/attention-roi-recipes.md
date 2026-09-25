# Attention ROI — Compression Recipes

Companion to `apex-gate-evaluator` gate_type `attention_roi`. These recipes turn a
COMPRESS or HOLD verdict into a concrete rewrite. Use the smallest recipe that fits
the situation; over-application loses the decision content.

## Recipe 1 — The 6-word question (most common case)

**Trigger:** Human question ≤ 10 words; proposed answer > 100 words; topic conversational.

**Pattern:** The reply can usually be 1-3 sentences plus a closing line.

```
Before (FAIL):
  "Human attention is priceless? Or the most expensive things in agentic economy..."

  [800-token essay on attention scarcity, agentic economy, compute economics,
   three axioms, F4/F8 anchors, closing metaphor]

After (ALLOW):
  "Ya. Compute semakin murah, attention manusia tak boleh scale. Dalam
   agentic economy, judgment manusia — bukan token — yang bottleneck."
```

**Mechanism:** The shorter version carries the same decision content (attention > compute)
in 1/8th the reading cost. ROI goes from 0.04 (HOLD) to 1.2 (ALLOW).

## Recipe 2 — Drop the framework the human didn't ask for

**Trigger:** Topic is conversational or reflective; the agent reflex introduced
a numbered list, 5-axis matrix, or 7-step procedure.

```
Before (FAIL):
  "There are 5 dimensions to consider when answering that:
   1. ...
   2. ...
   3. ...
   ..."

After (ALLOW):
  "Paling berat satu je — [the actual decision content]. Yang lain tu
   secondary."
```

**Mechanism:** Frameworks carry information density only when the human asked for them.
When the human asked a question, they want the answer, not a framework for answering.

## Recipe 3 — Compress, don't truncate

**Trigger:** Reply must keep the decision content but needs to lose 50%+ length.

**Pattern:** Keep head (anchor) + first body paragraph (decision) + tail (closing line).

```
Original:  [head] [para1] [para2] [para3] [para4] [tail]
Compressed:[head] [para1 (cut at last full sentence)] [tail]
```

**Why not truncate mid-sentence:** Truncation leaves the human reading an incomplete
thought and guessing what was cut. Compression at the paragraph boundary preserves
the decision and lets the human fill in the gaps if curious.

## Recipe 4 — Move content to a reference, send the decision

**Trigger:** The reply is correct AND long AND the human needs the decision now, not
the full derivation.

```
Pattern:  Send the decision (1-2 sentences) + the verdict, with a one-line pointer
          to where the full reasoning lives.
          "Full reasoning kat <path>. Aku hantar decision dulu."
```

**Mechanism:** Telegram surfaces that can't render long replies degrade the human
twice — once for length, once for fragmentation. Decision-first + reference-after
respects both reading budget and decision urgency.

## Recipe 5 — When to ALLOW a long reply

Some replies earn their length. The gate ALLOWs if ANY of these are true:

1. The human asked for depth ("explain in detail", "macam mana exactly", "give me the full picture").
2. The reply closes a loop that's been open > 1 turn (carry_forward reference).
3. The reply contains a decision the human will act on tomorrow, where under-explaining
   costs more than reading time.
4. The reply is the principal's own words being reflected back (witness letter,
   voice memo transcript) — length is appropriate to the medium.

**Default:** When in doubt, apply Recipe 1.

## Anti-recipe — What NOT to do

- **Don't apologize for length.** "Sorry panjang sikit" wastes tokens confirming what
  the human already knows.
- **Don't add "TL;DR" at the top.** If you needed a TL;DR, the reply was already too long.
- **Don't break long replies into numbered chunks** ("1. ... 2. ... 3. ...") to dodge
  the gate. Numbered chunks are still long. Compress first; number only if the human
  explicitly asked for structure.
- **Don't quote the doctrine to justify the length.** "Per compute-attention-invariant..."
  is itself jargon leak; the gate was supposed to prevent that.

## Measurement (for after-the-fact audits)

After any reply, check:
- Token count vs the question's token count (target: ≤ 3x for technical, ≤ 1.5x for conversational)
- Did the reply change a decision or close a loop? (yes/no)
- Did the human need to re-read? (yes = ROI negative regardless of content correctness)

If three consecutive replies in a session trigger Recipe 1 compression, the agent is
in length-drift — review the prior turns and find where the framework reflex started.
