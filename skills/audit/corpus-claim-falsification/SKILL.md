---
name: corpus-claim-falsification
description: "Use when writing claims about a person from a chat corpus."
version: 1.0.0
owner: curator
risk_tier: high
floor_scope: [F1, F2, F5, F6, F9]
triggers:
  - "map this person's shadow"
  - "what does he really feel"
  - "analyse this chat export"
  - "read the group and tell me what he is like"
  - "is this person X"
  - "build a person card"
  - "deep shadow analysis"
  - "what is behind his behaviour"
  - "he must be hiding something"
  - "who is he really"
tags: [audit, corpus, evidence, claims, privacy, person]
---

# Corpus Claim Falsification

Before a sentence about a person is written — into a card, a map, a letter, a reply — it has to survive
four tests against the corpus. Each one has killed a claim that read as obvious.

**Why this exists.** A person-map built from testimony plus a handful of vivid moments produces
sentences that each *look* sourced and are collectively wrong. The prose is not the failure; the
usual cause is quieter — **the map's vocabulary belongs to the person who commissioned it**.

A claim that cannot be falsified by the person it describes is not a finding. It is a story with
citations attached.

Also load: `governed-uncertainty`, `hermes-rasa`, `hermes-shadow` for the claim-object and ladder
rules this skill assumes. This skill owns the **corpus measurement** that backs them.

---

## The four tests (run before writing, not after)

### 1. Lexical attribution — whose words are these?

Count the claim's **organising vocabulary** in the SUBJECT's own lines versus the PRINCIPAL's lines.

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

### 2. Bidirectionality — is this a trait, or a routine?

Before calling a behaviour a property of the subject, count the **principal's own lines for the same
behaviour**. If the principal does it as often, it is a **dyadic routine**, not an individual trait,
and writing it as a trait misassigns the property to one party.

Measured: a partner-reference vocabulary over three years came out principal 18 / subject 13 — so the
subject's mention of it was not a subject-specific signal at all. Half the observations in a
"his armour" reading applied equally to the person describing him.

### 3. Ordering — sort the timeline before reading any single message

Build the message store from **logs first** (`gateway.log` timestamps are ground truth) and sort it,
THEN read meaning out of any one line. A message read out of order produces the wrong shape — an exit
read as a reaction to the subject's disclosure, when the other party's long message had already
landed five minutes earlier, reverses the causality. The person who was there will correct it.

**Screenshots are a different evidence tier from the corpus.** OCR is not the record. When two vision
passes on one image return different words for a material token, keep **both** readings open and say
which one you cannot resolve. Never collapse to the more narratively convenient reading.

### 4. Tier every claim, in the artifact

Each surviving sentence carries its evidence class beside it:

| Tier | Meaning |
|---|---|
| `OBSERVED` | a direct event in the record |
| `MEASURED` | a count you ran |
| `REPORTED` | the principal says so; not cross-checked |
| `SOVEREIGN-TESTIMONY-ONLY` | asserted by the principal, zero corpus support |
| `ASSOCIATION_ONLY` | two points co-occur; base rate not compared |
| `UNKNOWN-HUMAN-PRIVATE` | needs an interior no channel reaches |

A map with per-claim tiers is a map. A map without them is a narrative.

---

## Measure expression; never infer capacity

Zero occurrences of an affection word in the subject's lines supports the **`receives`** rung on the
relational ladder — nothing higher. It does **not** support "cannot receive tenderness": that is a
claim about an interior the record has no channel to.

Report the rung reached. Leave the capacity `UNKNOWN-HUMAN-PRIVATE`. Same rule for any claim shaped
like "is unable to …", "never allows himself to …", "secretly wants …".

---

## Base-rate before shape

Two instances are enough to *name a shape* and not enough to *name a trait*. Say the shape, flag
`ASSOCIATION_ONLY`, and write down the falsification test that would settle it — including the
comparison group and the baseline it must beat. "He does X after Y" is not a finding until the rate
of X-after-Y exceeds his own base rate of X.

---

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

---

## Reporting to the principal

- **Lead with what the corpus says, then what the map claimed, then the gap.** The gap is the finding.
- **Report reads as reads and writes as pending.** Never say a card was written before the write
  returns verified. If a claimed-but-unwritten artifact is caught, own it in the same turn.
- **When corrected, update and do not defend.** The principal has lived data; you have a file. Say
  plainly which earlier reading is withdrawn.
- **Do not compute a score for a person.** No affection metric, no compatibility number, no
  scalar for "who cares more". Currencies stay unpriced.

---

## Pitfalls

- **The amplification trap has a second form that hides better than dramatic prose**: misattributed
  lexicon. Every individual sentence looks sourced, so no reader catches it. That is why test 1 runs
  before the writing, not after.
- **Do not equate volume of writing with depth of finding.** A long artifact that survives the four
  tests is fine; a long artifact that skips them produces confident wrong sentences that later
  corrections cannot fully unwind.
- **A quotation is not a self-report.** One instance of the subject using the principal's word is
  him repeating the principal, not him owning the word. Read the enclosing line.
- **A message that recaps an old event is not news.** When the principal tells you the story is
  historical, re-read the row as retrospective disclosure — which is itself information — rather than
  a crisis report, and withdraw any "why did nobody respond" reading built on the wrong tense.
- **Keep both readings when the token is ambiguous.** "hal umah" vs "hal umrah" is a material
difference; a re-render of the same image is not independent evidence.

DITEMPA BUKAN DIBERI ⚒️
