---
name: first-party-corpus-audit
description: "Use when auditing archives for what they actually evidence."
version: 1.0.0
tags: [audit, evidence, corpus, forensics, epistemic]
metadata:
  hermes:
    category: governance
    tags: [audit, evidence, corpus, epistemic]
    related: [text-forensics, claim-level-verification, governed-uncertainty, relationship-memory-isolation]
triggers:
  - user asks for an evidence-grounded reconstruction of a relationship or a period
  - user hands over a chat export / transcript / dump and asks what it evidences
  - user asks you to test an existing narrative, persona, or another AI's account against records
  - an earlier session produced a confident story and it now needs auditing
---

# First-Party Corpus Audit

When the ask is *"tell me what actually happened, based only on records you possess"* or *"audit what
we know about X"*, the deliverable is not a story. It is a graded map of what the archive
**establishes**, **suggests**, **cannot see**, and **may never resolve** — with every claim carrying
its provenance.

**Prime law:** the archive is not the relationship; it is a sensor. It has coverage, blind spots,
distortion, missing channels and temporal gaps. Therefore observed ≠ total, and **missing evidence is
bidirectional** — it can raise, lower, or leave any hypothesis unchanged. Never use absence to rescue a
preferred story.

## When to load

- Evidence-grounded reconstruction of a relationship, a person, or a past period.
- Testing an existing narrative (including one an earlier agent or another AI wrote) against records.
- Any request containing "audit", "what does the record actually show", "is this supported", "separate
  what is real from what is inferred".
- Also load `text-forensics` for the parse/extraction mechanics on chat exports.

## Procedure

### 1. Inventory the sensor BEFORE reading it
Write down, up front: corpus name, span, volume, sender split, storage location, and — critically —
what each corpus **cannot** see. A text export cannot carry tone, touch, gaze, or in-person contact.
State the blind spots in the deliverable before any finding; a reader who sees the limitation first
will not over-read the result.

### 2. Verify parse integrity before deriving any statistic
See `text-forensics` for the export format traps. The non-negotiables here:
- Validate **coverage**: parsed count vs raw line count, and a printed sample of the lines your
  pattern rejected. A date-validating parser silently drops every line it mis-parses.
- Probe the date format on the first few lines rather than assuming a locale.
- Cross-check a parsed sender census against a raw text search for the sender names.
- If the format was wrong, **re-derive everything** and publish the corrected table with the
  superseded numbers marked. Never patch the single figure you happened to notice.
- Copy the corpus to a durable private location (`700` dir / `600` files) as step one. Working copies
  in transient storage get cleaned and take the audit's re-derivability with them.

### 3. Attribute by marker, never by content
Read sender identity from the explicit marker in the record (trailing `[Name|uid]`, an origin JSON, a
speaker label). Media entries carry a machine description of the **subject** before the marker, so
attributing a photo from what it depicts inverts who posted it. When two people are plausibly in
frame, record attribution as UNKNOWN instead of picking the likely one. Keep a sender + evidence-class
column in any media inventory.

### 4. Separate the four layers — and keep them separate all the way to the output
- **OBSERVED** — directly present in the record (a message, a timestamp, a stated action).
- **REPORTED** — someone's own account of their state or of another's. Self-report is one witness.
- **INFERRED** — a reasonable bridge between observations. Always state the causal bridge and at
  least one alternative explanation.
- **UNKNOWN** — the evidence does not establish it. Use aggressively. UNKNOWN is a successful audit
  result, not a gap to fill with narrative.

### 5. Build both directions independently before any global verdict
Do not describe the relationship globally first. Map A→B and B→A as separate inventories, then
compare. A single global verdict across an asymmetric exchange hides the asymmetry that matters most.

### 6. Run the ladder tests
For any behavioural claim, report the **highest level actually evidenced**, never the level implied by
co-occurrence. Definitions, the counterfactual test, and the natural-variation test:
`references/evidence-ladders-and-counterfactuals.md`.

**The strongest test in this class is the counterfactual**: find a period where one party's behaviour
naturally stopped (without any announced test) and read what the other party did. Mark a finding
`NO NATURAL COUNTERFACTUAL AVAILABLE` when there is none — do not manufacture one, and do not
instrument anyone to create one.

### 7. Frequency is not meaning
Audit every numeric signal you extract. High contact frequency is not attachment; low affection
vocabulary is not low care; initiation volume is not dependence; silence is not rejection; body talk
is not sexual interest. **Count first, interpret second, challenge the interpretation third.** State
which conversions you refused.

### 8. Run the contamination audit
Any prior narrative — an archetype, a persona bible, a synthesis document, an imported literature
review — must be graded against the same evidence as everything else. Full procedure and the
cross-corpus reconciliation rule: `references/contamination-and-cross-corpus.md`.

### 9. Map the void explicitly
The void is a deliverable section, not an apology. Enumerate each missing channel (visual, vocal,
physical, temporal, internal-state, comparison-group) and state for each hypothesis whether the
missing channel could raise it, lower it, or leave it unchanged. Symmetry is mandatory — a channel
that could reveal more affection could equally reveal less.

### 10. Close with a minimum and a maximum model
Give the smallest model that explains the evidence, then the richest model still justified, each
extension carrying a confidence. The distance between them is the **interpretive freedom** — say how
wide it is. A narrow distance is a strong result: it means every reading of the record describes the
same relationship, and a reading outside the band is not at the edge of the evidence but beyond it.

## Output shape

Lead with the finding, not the method. Then: corrected-baseline table · chronology of first-party
events · two-way behavioural inventory · ladder verdicts with confidence · counterfactual result ·
power/asymmetry matrix (per domain — power reverses by domain, so never one global axis) · negative
evidence · UNKNOWN register · minimum and maximum model.

**Negative evidence is mandatory.** State plainly what the records fail to show, and flag where
absence is weak because the archive itself is incomplete.

## Register and privacy rules

- Audit artifacts about a real third party are **private-lane** material (e.g. a per-person lane dir),
  `chmod 600`, and never written into shared canon, memory, or session preamble.
- Every affected file that carries a corrected claim gets amended **in place, append-only** — add a
  dated amendment; never silently rewrite a published figure. When a correction invalidates a sentence,
  withdraw the sentence explicitly in the amendment.
- Do not publish a third party's private detail onto any shared surface, and do not name a synthetic
  artifact after a real person.
- **Never build monitoring.** If a test would require tracking, instrumenting, or surveilling a real
  person, do not build it. Describe the reading lens for evidence that arises naturally, and leave it
  at that.
- **Flag consent gaps, do not silently fix them.** If the audit uncovers a real person's data
  (biometrics, recordings, identity material) held without a recorded consent artifact, report it as a
  finding for the owner to decide on, and delete nothing.
- When the audit covers an emotionally loaded relationship, the discipline is to preserve ambiguity,
  not to resolve it: *"the record does not settle this"* is the answer, and it stays the answer.

## Pitfalls

- **Do not let a synthesis document be used as evidence for the thing it synthesised.** Files an agent
  wrote from a corpus are objects of the audit, not sources for it. Say so in the corpus inventory.
- **Do not import population research onto an individual.** Population findings describe populations;
  they cannot speak to one person without a causal clause. Literature is for framing, never for
  diagnosis, and never as proof about a named human.
- **Do not raise confidence because a story is coherent.** Coherence is what a good narrative does.
  Confidence tracks the evidence, and the most coherent reading is frequently the least supported.
- **Do not collapse distinct claims into one rung.** "Tolerated" ≠ "engaged" ≠ "sought" ≠ "restored".
  A ladder is climbed one rung at a time, and a report that jumps rungs is a fabricated verdict.
- **Do not ask the subject.** The UNKNOWN register exists so the answer can be *"only that person
  could say"* — identify those questions and stop. Do not route them to the person, and do not treat
  their absence as an invitation to guess.
- **Own your own errors in the deliverable.** A parse defect, a misattribution or a wrong pick is
  amended on the record with the mechanism named. An audit that hides its own corrections cannot be
  trusted on anything else.

## References

- `references/evidence-ladders-and-counterfactuals.md` — ladder definitions, the counterfactual test,
  the natural-variation test, and how to report a ceiling rather than a probability.
- `references/contamination-and-cross-corpus.md` — contamination graph, grading prior narratives, and
  the cross-corpus counting rule.
