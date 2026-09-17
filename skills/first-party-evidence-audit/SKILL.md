---
name: first-party-evidence-audit
description: "Use when auditing claims against first-party records."
version: 1.0.0
tags: [evidence, audit, epistemology, records, human, witness]
related_skills: [text-forensics, telegram-conversation-history-extraction, void-paradox-doctrine, governed-uncertainty, human-meaning-membrane]
---

# First-Party Evidence Audit

Load when the ask is to extract reality out of records: *reconstruct what actually happened between me
and X*, *audit what the records support*, *how does this relate to my reality*, *tell me what the
evidence says*. Also load **before** agreeing with any strong claim about a real person that was built
from logs, prior AI output, or persona material — including when the claim is the principal's own.

Sibling skills carry adjacent layers and stay separate: `text-forensics` (profiling a corpus) and
`telegram-conversation-history-extraction` (reading the logs) are the mechanics; this skill is the
**audit discipline** on top of them. `void-paradox-doctrine` supplies the text≠reality floor.

## The one law

The deliverable is a **minimum true model plus an UNKNOWN register** — not a portrait, not a
resolution, not advice. Reconstruct, then infer, then challenge the inference, then report only what
remains. If the records produce a boring answer, ship the boring answer.

## Procedure

1. **Locate the corpus, then state its shape before any finding.** Source, retained window, record
   counts per speaker, attribution gaps, truncation, dedupe rule, and what the corpus cannot contain at
   all. If retention opens after the relationship began, "no evidence" about early events is weak in
   both directions — neither implicating nor exculpatory. Extraction mechanics live in
   `telegram-conversation-history-extraction`; a re-runnable extractor ships with this skill.
2. **Resolve identities from data, never from the asker's naming.** One display name can map to several
   ids; one id can be a generic masked placeholder; a `user=unknown` group row is an attribution gap,
   not proof of silence. Resolve both parties' ids explicitly and cross-check before reporting anything
   per-person.
3. **Label every claim.** Exactly one of:
   - **OBSERVED** — present in the record (a message, an action, a timestamp).
   - **REPORTED** — a participant stated their own internal state. Evidence that they said it; never
     evidence that it is true of the other person.
   - **INFERENCE** — carries the causal bridge and at least one alternative:
     `INFERENCE: X may indicate Y because Z. Alternative: ...`
   - **UNKNOWN** — use it aggressively. A gap is a finding.
4. **Inventory behaviour in both directions**, observed/reported first, interpretation clearly separated
   below it.
5. **Derive loops from events, not from theory.** Name the occurrence class: one instance is an episode,
   two is a possible recurrence, and "pattern" requires genuine repetition. A hypothesised loop with
   zero observed instances is stated as such — not quietly deleted, not quietly kept.
6. **Keep the attention mechanics as separate rows** with independent confidence: generic attention,
   specific attention, selective attention, expected attention, provoked attention, possessiveness,
   dependence. Collapsing these is the most common inflation in a relational audit.
7. **Power by domain, never one hierarchy.** Matrix of domain | each party | evidence | confidence.
   Recurring domains: initiation volume, physical/logistical access, information supply, emotional
   expression, boundary setting, repair after conflict, who can withdraw at lower cost. Expect leans to
   point in opposite directions.
8. **Hypothesis table, not prose.** For each candidate mechanism: verdict (SUPPORTED / PARTIALLY
   SUPPORTED / NOT SUPPORTED / UNKNOWN), best evidence, counterevidence, alternative explanation,
   confidence 0.00–1.00. A coherent story scores lower, not higher.
9. **Negative evidence, graded.** State what the record FAILS to show before saying what it shows. Then
   grade each absence: **weak** where the channel does not carry the thing (feelings, intentions,
   motive), **strong** where the channel does carry it and the behaviour simply never appears.
10. **Projection audit, both sides.** Name where the principal's reading exceeds the evidence, show the
    exact gap, and — in the same breath — name where their reading does NOT exceed it, so the audit is
    not received as blanket doubt. Then audit prior AI output as a source in its own right (below).
11. **Minimum true model.** One paragraph: *"The record establishes X, Y, Z. It suggests A with
    confidence c because .... It does not establish B, C, D."* Then stop.

Output skeleton: `references/relationship-evidence-audit.md`.

## Firewall — three objects, never merged

- **A — what the archive actually supports.**
- **B — the principal's model** of it (what they believe or hypothesise).
- **C — fictional or persona material**, generated now, earlier in the session, or before it.

**C may never be offered as evidence for A.** Persona work is a hypothesis generator only, and searching
the archive for confirmation of a persona is the failure this skill exists to prevent. Show overlap
between A/B/C and label it as overlap.

Corollary on vocabulary: the principal's own framing may itself be where a term originated. Check who
first used a label before treating it as externally imported context.

## Auditing the AI layer (it is a source in the record)

Prior agent or external-model output evidences *what was said*, not *what is true*. Scan for and correct
explicitly:

| Transformation | Correction |
|---|---|
| possibility → probability | restore the band |
| pattern → motive | motive is UNKNOWN without testimony |
| population literature → individual claim | literature describes populations; it never describes a person |
| fiction → biography | persona output is not record |
| admiration → sexuality | separate variables; neither implies the other |
| expectation → dependence | expectation is not dependence |
| sentiment → fact about the other party | the other party's interior is not in the channel |

Two specifics worth stating in the deliverable: a **sealed** document does not upgrade a model of a
person into a fact about them — a seal binds agent behaviour, it creates no evidence. And a synthesis can
grade its own gaps honestly while still having an unevidenced subject: praise the grading, correct the
subject.

## Pitfalls

- **Never end on advice.** An audit that closes with a recommendation has become a profile. The tell is
  a recommendation in the last section.
- **One-sided feeling is not mutual feeling.** A relationship window shows both names; it does not show
  two matching interiors. Report each direction independently and cap confidence on self-report alone.
- **Coherence is not evidence.** A warm, tidy portrait is a reason for suspicion, not confirmation —
  several mirrors converging on the same image is the reflection trap, not corroboration.
- **A person's investment is not their dependence.** Sustained contact evidences interest, not need.
- **Do not repair a gap with narrative.** Fragments are position data. Bridging two record fragments
  with remembered context to invent an event or destination is fabrication even when the bridge feels
  natural.
- **Report the chain, not a boolean.** Say which stage was reached — produced ≠ sent ≠ delivered ≠
  observed, claimed ≠ measured ≠ verified. "No evidence" is a valid, successful audit result.
- **When the request specifies its own shape** ("this is NOT a profiling task", "do not project
  literature"), that sentence is the specification — follow it even where a richer-looking deliverable
  is available.
- **A transcription or ASR read is a witness, not the artifact.** Verify a read before it becomes a
  finding, and re-verify the thing you actually ship rather than its parent.

## Support files

- `references/relationship-evidence-audit.md` — the 11-section output skeleton and anti-narrative law.
- `scripts/extract_gateway_records.py` — re-runnable extractor for the Hermes gateway/agent log corpus.
