---
name: provenance-typed-analysis
description: "Use when the principal asks where an analysis came from."
version: 1.0.0
owner: curator
risk_tier: medium
floor_scope: [F2, F4, F9, F13]
triggers:
  - "where did you get this"
  - "mana hang dapat ni"
  - "is this true or not"
  - "prove it"
  - "which of this is yours"
  - "deep analysis"
  - "relate this to ai agents"
tags: [provenance, analysis, epistemic, delivery, claims, retraction]
related_skills: [synthesis-verification-gate, claim-receipt-discipline, auditable-numeric-artifacts, governed-uncertainty]
---

# Provenance-Typed Analysis

A multi-claim analysis delivered as smooth prose cannot answer *where did this come from*. This skill
governs how to compose such an analysis so that provenance is a property of the work rather than a
reconstruction performed after being challenged.

**Load before** writing any answer that mixes cited findings with your own reasoning: mechanism
explanations, "why do humans / why do systems" answers, cross-domain syntheses, and anything the
principal will use to make a decision or form a belief about people.

## The rule

**Tag every claim at composition time, then expose the tags on demand.** Rebuilding the ledger after
the question is reconstruction, not memory, and it is where false confidence enters.

| Tag | Meaning | How it must be worded |
|---|---|---|
| `SOURCED` | Named paper, instrument, dictionary, primary document | Cite author · venue · year, or the artefact by path |
| `MEASURED` | Probed live in this session | State the probe and when |
| `OWN_ARGUMENT` | Your reasoning, inference, taxonomy, compression | Allowed to stand — but labelled as yours |
| `RETRACTED` | Delivered earlier and now wrong | Name the sentence, the reason, the corrected position |

Add two habits that make the ledger honest:

- **Name the weakest claim yourself**, before the principal finds it.
- **Do not let a sourced mechanism lend authority to an unsourced interpretation.** Naming a paper for
a mechanism is legitimate; presenting your reading of that mechanism in the same register is the
defect.

## On demand: the shape of the answer

When asked where the material came from, answer as a **per-claim list**, closed by a count, e.g.
`sourced 5 · dictionary 2 · own argument 4 · retracted 1`. State plainly which parts are yours and
which were wrong. A hedge ("some might argue") is not a retraction, and a silent edit leaves the
earlier version standing in the principal's head.

## Standing rules

- **Own arguments are permitted content.** The failure is not having them; the failure is presenting
them at the same confidence as a finding. A taxonomy you invented is useful and must be introduced
as invented.
- **A gauge that was never measured must be named as fabricated.** Where a number reported as
measured
resolves to a constant or a hardcoded product, the finding is the fabrication, not the value, and it
must be reported that way even when it embarrasses the system that produced it.
- **Answer the question that was asked, not the philosophical upgrade of it.** When the principal asks
for a concrete reading ("is this true or not"), give the per-claim verdict; do not reframe the
question as an essay about epistemology.
- **Land on consequence.** Close with what the finding changes for a decision he is actually facing —
the principal treats a synthesis with no consequence as noise and will say so.
- **When asked to map an analysis onto agents or onto yourself, give the contrast, not the mirror.**
Walk each term, state the agent-side equivalent, then state which direction it inverts. A mirrored
list reads as insight and teaches nothing; the inverted term is the finding. Where the subject is
the agent's own limits, name the asymmetry plainly — including the case where the agent articulates a
concept best precisely because it cannot have the experience.

## Pitfalls

- **Sourcing nothing and sounding certain.** Every mechanism claim should be attachable to a named
origin at the moment of writing, not at the moment of challenge.
- **Over-retracting.** Withdraw the specific wrong sentence and its consequences; do not disown the
whole piece, which destroys the parts that were sound and leaves the principal with nothing usable.
- **Re-citing the same origin many times as if it were corroboration.** One instrument, one wire
item, one release is one origin however many outlets carry it.
- **Letting a stale figure survive a correction.** When a number changes, the old one becomes
superseded; do not let both stand in the same answer.

## Related skills

- `synthesis-verification-gate` — the earlier gate for enumerating and classifying claims before
  output (source taxonomy: PROBED / CITED / HEARSAY / MEMORY / INFERRED / CONTESTED / UNKNOWN).
  Overlaps this skill on classification; this one adds composition-time tagging, the on-demand
  breakdown, retraction discipline, and the agent-self contrast rule.
- `claim-receipt-discipline`, `auditable-numeric-artifacts` — receipts and sourced figures.
- `governed-uncertainty` — when the analysis is about a human being rather than a system.
