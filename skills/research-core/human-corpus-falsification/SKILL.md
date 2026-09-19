---
name: human-corpus-falsification
description: "Use when building a person-map from message history."
version: 1.0.0
triggers:
  - "map his shadow"
  - "deep shadow analysis"
  - "what is he really like"
  - "tell me everything about him"
  - "map the paradox of language and human"
  - "relationship audit"
  - "update the person card"
  - "a chat export or group log arrives for a person already mapped"
tags: [human-reality, forensics, falsification, epistemics, shadow, corpus]
---

# Human-corpus falsification — counts before narrative

Companion to the person-mapping skills (`text-forensics`, `whatsapp-group-intelligence`,
`shadow-mapping`, `hermes-rasa`, `hermes-shadow`). Those hold the pipeline; this holds the **ladder
that has to be climbed before any interpretive sentence is written**, and the place the result is
recorded.

> **The rule that pays for itself:** before writing one line about a person, print the counts. Prose
> reframes; counts falsify. Every person-map failure in this federation has the same shape — an
> elegant reading built from salient moments while the corpus that could have refuted it sat unread.

## The six laws

1. **Lexical attribution.** For every organising term the claim uses (worship, anger, loyalty,
   ambition, armour, denial), count it in the SUBJECT's own lines against the PRINCIPAL's own lines
   of the same corpus. If the term lives in the principal's lines and is near-absent in the subject's,
   the map is a portrait of the principal's vocabulary wearing the subject's name — and every
   individual sentence still looks sourced. Print both counts in the deliverable.
2. **Base rate before signal.** Any behaviour about to be called meaningful needs its rate over the
   whole corpus *and* the other party's rate. A motif the principal uses as often as the subject
   cannot carry an interpretation about the subject. No base rate measured → label `ASSOCIATION_ONLY`
   and print the counts instead of the reading.
3. **Recap ≠ news.** Material a person re-tells may belong to an earlier period. Before dating an
   event to today, check whether the corpus mentioned it in the year it happened; if it never
   appeared then, it is being recalled, not reported. Ask before building a today-frame on it — a
   correction here collapses every reading stacked above it.
4. **Report the rung, not the capacity.** Zero occurrences of an affection word in the subject's own
   lines supports `receives`. It does not support "cannot receive tenderness" — that is a claim about
   an interior and stays `UNKNOWN-HUMAN-PRIVATE`.
5. **Two instances is a shape, not a trait.** Name the shape, publish the falsification test, and
   label the reading `ASSOCIATION_ONLY` until the test is actually run. A test that is merely stated
   is decoration.
6. **A green verdict is not evidence.** When a gate, organ, or validator returns a pass, read the
   field that was supposed to carry the evidence. A pass on an empty payload is a defect in the
   instrument; reporting it as support repeats the defect. Report it as an instrument defect in the
   same turn.

## Procedure

1. **Inventory prior maps first.** Search the private lane, the person's card, and memory for anything
   already written about this subject. A prior map is not context — it is the thing to falsify.
2. **Parse, then print totals.** Per-speaker counts, median message length, and date range before any
   reading. A parse that silently drops wrapped lines turns every later rate into fiction.
3. **Run the probe set** (speaker counts · lexical attribution · base rate · hour histogram · distress
   vocabulary frequency · service/logistics counts · help-ask vs help-offer asymmetry). Recipes and
   the gateway-log mining pattern: `references/corpus-probes-and-ledger.md`.
4. **Write the ledger before writing the answer.** Dated file in the private lane, beside the maps it
   corrects: evidence table with paths and counts, one heading per finding, a correction log, and
   `UNSUBSTANTIATED` / `SOVEREIGN-TESTIMONY-ONLY` / `ASSOCIATION_ONLY` tiers on every old claim the
   corpus did not support. Relabel the superseded maps in the same turn — a later session that finds
   only the old map will reproduce the old error.
5. **Answer with counts first, quotes second, meaning last.** State the tier of every interpretive
   sentence. Lead with what the corpus refused to support: that is the finding the principal cannot
   get anywhere else.
6. **Own the correction plainly when he corrects a premise** — update the ledger, patch every surface
   carrying the old reading, no defence, no second cleverer reading afterwards.

## Invoking the RASA organs (when he asks for shadow / paradox analysis)

Doctrine is not the deliverable — call the `hermes_rasa` MCP organs and report what they returned.

| Tool | Use | Correct return looks like |
|---|---|---|
| `hermes_shadow_map` | tensions across self-model / self-report / behaviour | class `I`, `PRIVATE_QUALIA`, and **often `shadow_candidates: []`** — an empty list is the organ working, not a failure to retry |
| `hermes_paradox_map` | two co-active states | `coexistence_possible: true`, `resolution_required: false` |
| `hermes_contradiction` | one event, two accounts | `DUAL_PERSPECTIVES_PRESERVED`, `shared_meaning: UNKNOWN_UNCREATED` |
| `hermes_projection_guard` | speaker's feeling vs claimed target feeling | `PERSPECTIVE_TRANSFER_RISK` — speaker established, target unestablished |
| `hermes_counterstory` | break narrative gravity | candidate + supporting + against + ≥2 alternatives + a falsification test |
| `hermes_cross_layer_check` | may layer A support a claim in layer B | see the defect below |

**Defect — `cross_layer_check` returns `ALLOW_CROSS_LAYER_BRIDGE` for ANY non-empty
`bridge_evidence` string.** Passing the literal text `"NONE OFFERED"` yields a green ALLOW. So an
ALLOW is not validation: read the `bridge_evidence` field, and when it carries no real source, report
it as a witness defect rather than as support. Never quote a green ALLOW to the principal as
confirmation.

**Layer names are a closed vocabulary** — `BIOLOGICAL · BRIDGE_CLAIM · CHEMICAL · CULTURAL ·
ECONOMIC · NEURAL · NORMATIVE · PERSONALITY · PHENOMENOLOGICAL · PHYSICAL · PSYCHOLOGICAL ·
RELATIONAL · SEXUALITY · SOCIAL`. Free-text layer names are rejected on the first call.

These are local tools: one invocation per `tool_call`, never batched with connector tools.

## Delivery notes

- Lead with the correction if you got something wrong, before the new analysis. One line, no
  self-flagellation, then the substance.
- The most valuable sentence in the reply is usually the one the principal did not want to hear —
  e.g. that the map he has been building is a description of himself. Say it once, plainly, with the
  counts, and do not soften it afterwards.
- Never hand over a "full shadow". Give what the corpus supports, the tier it sits at, and the one
  question that would move it. `RETURN AUTHORITY TO THE HUMANS` when the remainder is interior.
- The subject of a map does not consent to being measured unless he was told. Infrastructure
  ownership is access, not a right — record the enacted and declared layers only, and keep the
  ledger in the private lane.

DITEMPA BUKAN DIBERI
