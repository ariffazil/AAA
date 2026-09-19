---
name: corpus-claim-discipline
description: "Use when quantifying a message corpus or claiming from it."
version: 1.0.0
risk_tier: high
floor_scope: [F2, F9, F11]
tags: [corpus, claims, quantification, provenance, chat-logs, epistemic]
---

# Corpus Claim Discipline

Counting a corpus of human messages is a claim about a denominator, and the denominator is normally
wrong before you fix it. This skill is the ordered procedure that makes a corpus claim honest, plus
the emission rules for claims about a person drawn from one.

**Trigger:** any "how often does he…", "he always…", "he never…" question answered from chat logs;
any frequency, share or "N occurrences" figure quoted from a message store; building or updating an
explanatory map of a person from their messages; any **negative** about delivery, receipt or presence
drawn from a log you own; any durable artifact stating a pattern about a person.

**The one sentence:** *a clean number implies a reach it does not have.* Report the rung the count
evidence, and leave the remainder unknown.

Support files:
- `references/corpus-counting.md` — probe recipes: dedupe funnel, attribution, frequency vs function,
  the two-sided test, era-check.
- `references/human-state-mcp.md` — calling the human-state enforcement MCP, its exact refusals, and
  how to report a rejection to the principal as evidence rather than as an obstacle.
- `scripts/corpus_probe.py` — re-runnable probe (dedupe funnel + per-speaker + hour histogram for one
  lane) with a schema guard that exits loudly rather than guessing.

---

## Procedure, in order

### 1. Dedupe replays before counting anything

Live message stores re-quote earlier messages inside later turns and quote-blocks nest, so a single
line can appear five or more times. **A raw substring count over such a store is inflated and will
manufacture patterns that do not exist.**

Collapse identical bodies within the same minute, then collapse near-adjacent duplicate ids. Print
the funnel (`raw 240 → 155 deduped`) with every figure you report. A count without a funnel cannot be
audited and is not yet a count.

### 2. Attribute before aggregating

A group corpus is not one speaker. In Telegram-derived stores the sender lives **inside the message
content** as a `[Name|uid]` prefix, not in a column; an unset display name reads as `No name`, so
resolve the `uid` against the channel registry rather than trusting the label. One lane spans many
session ids across resets — sweep the lane, never a single session id.

### 3. Count the word's function, not just its frequency

A high-frequency word may be carrying a **permission** rather than a **referent**. Sample every line
containing it and ask: do they cluster around access, availability and absence? A word that
alternates between *"you may come"* and *"not now"* is a control token in the shared vocabulary.
Counting it as a topic yields a wrong map of the relationship.

### 4. Two-sided test before attributing a frame to one person

Count the same token in the other party's lines, and in the principal's own lines, before filing it
as the subject's tell. A frame both people use, ask about and reciprocate is **co-authored**, and may
not be filed as one party's concealment, armour or defence. Reciprocated vocabulary is the most
common false attribution in a two-person corpus — it looks like the subject's private device and is
actually the room's language.

### 5. Era-check every pattern before calling it architecture

A pattern in the transcript may belong to a life phase the person has already left. Attach a date
before the pattern becomes a claim about the present. When the principal says *"that was during a
past chapter, it is different now,"* pull the dated lines on both sides rather than accepting either
version; if a dated line appears to contradict the framing, place the **date** on the table, not an
accusation. A prior-era line is a fact about the prior era plus an open question about the present.

### 6. Scope every negative to the lane you searched

The easiest thing to read is your own delivery/log lane, and its silence feels like a verdict. It is
only a measurement of your lane. When you must report a negative, name the lane searched and the
strength that search supports:

```
WRONG:  "It never reached him."
RIGHT:  "Nothing in our outbound lane — I searched X only; delivery outside it is invisible to me."
```

Ask: *could this event have happened through a channel I do not instrument?* If yes, the negative is
lane-scoped. This is the mirror of ghost capability — **phantom absence and ghost capability are the
same defect with the sign flipped.** Once you own the over-reach and the event is shown to have
occurred, retract the negative in the same turn; a stale negative propagates exactly like a stale
positive.

### 7. Run the claim through the enforcement layer before emitting

Where the environment provides a human-state enforcement MCP, call it *before* the claim reaches the
human: literal events first, then the typed claim, then the paradox / projection / cross-layer
checks. Expect refusals — they are the point, and a rejection is evidence to report plainly, not an
obstacle to route around. Patterns, exact refusal triggers and batching rules:
`references/human-state-mcp.md`.

---

## Emission rules

- Lead with what the count evidences; name the rung reached; state the remainder as unknown.
- Never let a number reach further than the corpus does: counting reaches enacted behaviour,
  self-report, vocabulary, timing, volume and silence gaps — not attachment, motive, interior or
  shared meaning.
- Separate the media: a group room and a private channel are different stages. A line present in one
  and absent in the other is a fact about the medium, not about truth.
- Report reads as reads and writes as writes. A claimed-but-unwritten artifact is a false receipt;
  own it in the same turn, produce it, restate true status.
- A single instance is a **shape**, not a pattern. Say "one instance" and give the repeat count that
  would make it a pattern — do not let a lone datum borrow the authority of a trend.

---

## Pitfalls

| Pitfall | Rule |
|---|---|
| Raw `LIKE '%x%'` count over live logs | Dedupe replays first; print the funnel |
| "There is no record of X" | State the lane searched and what it cannot prove |
| Reading a control token as a topic | Sample its lines; test for access/absence clustering |
| Attributing a shared frame to one party | Two-sided test first; co-authored frame is not a private device |
| Treating an old-era pattern as current | Attach a date; re-pull both sides on correction |
| Numbers implying interior knowledge | Report the rung; leave the remainder unknown |
| One instance presented as a trend | Say "one instance" + the repeat threshold |
| Counting before attributing in a group room | Resolve the uid; sweep the lane, not the session id |

---

DITEMPA BUKAN DIBERI ⚒️
