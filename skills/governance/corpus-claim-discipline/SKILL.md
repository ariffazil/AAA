---
name: corpus-claim-discipline
id: corpus-claim-discipline
version: 2.0.0
owner: AAA
risk_tier: high
floor_scope: [F1, F2, F5, F6, F9, F11]
autonomy_tier: T1
description: "Use when quantifying a message corpus or claiming from it. Covers counts, person maps, shadow reads, and any tiered claim about a person drawn from a chat store."
tags: [corpus, claims, quantification, provenance, chat-logs, epistemic, person, privacy, audit, falsification]
triggers:
  - "how often does he ..."
  - "he always / he never"
  - "how many times did this happen in the chat"
  - "quantify this chat export"
  - "map this person's shadow"
  - "what does he really feel"
  - "analyse this chat export"
  - "read the group and tell me what he is like"
  - "is this person X"
  - "build a person card"
  - "deep shadow analysis"
  - "what is behind his behaviour"
  - "who is he really"
  - "nothing in our logs / there is no record of X"
  - "quote a pattern about a person"
merged_from:
  - name: corpus-claim-falsification
    sha256: aaf85c7062ffaec0
    frozen: /root/AAA/skills-retired/2026-09-20-governance-wave1/corpus-claim-falsification/
support_files:
  - references/corpus-counting.md
  - references/human-state-mcp.md
  - scripts/corpus_probe.py
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

**Why the person-claim half of this skill exists.** A person-map built from testimony plus a handful
of vivid moments produces sentences that each *look* sourced and are collectively wrong. The prose is
not the failure; the usual cause is quieter — **the map's vocabulary belongs to the person who
commissioned it**. A claim that cannot be falsified by the person it describes is not a finding. It is
a story with citations attached.

**Also load:** `governed-uncertainty`, `hermes-rasa`, `hermes-shadow` for the claim-object and ladder
rules this skill assumes. This skill owns the **corpus measurement** that backs them.

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

**Whose words are these?** Count the claim's **organising vocabulary** in the SUBJECT's own lines
versus the PRINCIPAL's lines before anything is filed as the subject's property.

```bash
f="WhatsApp Chat with <Name>.txt"
grep -c " - <Subject>: .*worship"   "$f"
grep -c " - <Principal>: .*worship" "$f"
```

If the map's key words appear overwhelmingly in the principal's messages and near-zero in the
subject's, the map is **a portrait of the principal's vocabulary wearing the subject's name**.
One measured case: a 4,300-message export where `worship` = principal 19 / subject 1 — and the
subject's single hit was him quoting the principal back.

**A name with zero occurrences cannot carry anything.** `grep -c "<proper-noun>"` returning 0 across
the whole corpus means every claim resting on that name is `SOVEREIGN-TESTIMONY-ONLY`, never evidence.
Mark it so, in the artifact.

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


Measured: a partner-reference vocabulary over three years came out principal 18 / subject 13 — so the
subject's mention of it was not a subject-specific signal at all. Half the observations in a
"his armour" reading applied equally to the person describing him.
### 5. Era-check every pattern before calling it architecture

**Order before meaning.** Build the message store from **logs first** (`gateway.log` timestamps are
ground truth), sort it, THEN read meaning out of any one line. A message read out of order produces
the wrong shape — an exit read as a reaction to the subject's disclosure, when the other party's long
message had already landed five minutes earlier, reverses the causality. The person who was there
will correct it.

**Screenshots are a different evidence tier from the corpus.** OCR is not the record. When two vision
passes on one image return different words for a material token, keep **both** readings open and say
which one you cannot resolve. Never collapse to the more narratively convenient reading.

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


## Tier every claim, in the artifact

Each surviving sentence carries its evidence class beside it. A map with per-claim tiers is a map;
a map without them is a narrative.

| Tier | Meaning |
|---|---|
| `OBSERVED` | a direct event in the record |
| `MEASURED` | a count you ran |
| `REPORTED` | the principal says so; not cross-checked |
| `SOVEREIGN-TESTIMONY-ONLY` | asserted by the principal, zero corpus support |
| `ASSOCIATION_ONLY` | two points co-occur; base rate not compared |
| `UNKNOWN-HUMAN-PRIVATE` | needs an interior no channel reaches |

## Measure expression; never infer capacity

Zero occurrences of an affection word in the subject's lines supports the **`receives`** rung on the
relational ladder — nothing higher. It does **not** support "cannot receive tenderness": that is a
claim about an interior the record has no channel to.

Report the rung reached. Leave the capacity `UNKNOWN-HUMAN-PRIVATE`. Same rule for any claim shaped
like "is unable to …", "never allows himself to …", "secretly wants …".

## Base-rate before shape

Two instances are enough to *name a shape* and not enough to *name a trait*. Say the shape, flag
`ASSOCIATION_ONLY`, and write down the falsification test that would settle it — including the
comparison group and the baseline it must beat. "He does X after Y" is not a finding until the rate
of X-after-Y exceeds his own base rate of X.

## Storage — F5 artifacts must not land in a tracked tree

A document lane that looks private can be version-controlled. Most `forge_work/` PDF lanes ARE
tracked (`git ls-files forge_work` returns them), so writing an F5/F5-private artifact there puts a
person's private material into the repo history.

```bash
git -C <repo> check-ignore -v <path>     # non-zero exit = NOT ignored = do not write here
git -C <repo> status -s                  # confirm empty after the move
```

Write F5 artifacts under a lane whose `.gitignore` covers it (e.g. `lanes/private/`, ignored as
`lanes/`), `chmod 600`, and delete the tracked copy in the same step. Build files may stay in the
tracked tree; the artifact may not.

## Reporting to the principal

- **Lead with what the corpus says, then what the map claimed, then the gap.** The gap is the finding.
- **Report reads as reads and writes as pending.** Never say a card was written before the write
  returns verified. If a claimed-but-unwritten artifact is caught, own it in the same turn.
- **When corrected, update and do not defend.** The principal has lived data; you have a file. Say
  plainly which earlier reading is withdrawn.
- **Do not compute a score for a person.** No affection metric, no compatibility number, no scalar
  for "who cares more". Currencies stay unpriced.

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
| Misattributed lexicon (the quiet amplification trap) | Every sentence looks sourced, so no reader catches it — run the lexical-attribution count BEFORE writing |
| A quotation read as a self-report | One instance of the subject using the principal's word is him repeating the principal; read the enclosing line |
| A recap read as news | When the principal says the story is historical, re-read the row as retrospective disclosure and withdraw any "why did nobody respond" reading built on the wrong tense |
| Volume of writing equated with depth of finding | A long artifact that survives the tests is fine; one that skips them produces confident wrong sentences later corrections cannot unwind |
| An ambiguous token collapsed to one reading | "hal umah" vs "hal umrah" is a material difference; a re-render of the same image is not independent evidence |

---

## Provenance

`v2.0.0` (2026-09-20, governance/verification wave-1 merge) absorbed **`corpus-claim-falsification`**
(sha256 `aaf85c7062ffaec0…`), which had grown as the person-claims half of this same procedure — its
four tests duplicated steps 2, 4 and 5 above and have been fused into them; its tiers, expression-vs-
capacity rule, base-rate rule, F5 storage rule and principal-reporting contract are kept verbatim in
the sections above. Full original body frozen at
`/root/AAA/skills-retired/2026-09-20-governance-wave1/corpus-claim-falsification/`. The name
`corpus-claim-falsification` is now an alias resolving here.

DITEMPA BUKAN DIBERI ⚒️
