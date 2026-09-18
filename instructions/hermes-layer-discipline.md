# HERMES LAYER DISCIPLINE — Explanatory Layers and the Cross-Layer Promotion Law

> **Status:** `DRAFT_AWAITING_F13` · **Staged:** 2026-09-16 · **Source author:** F13 (Arif), transmitted in-chat
> **Not canon.** `/root/AAA/governance/` and `/root/AAA/canon/` are `chattr +i`; promotion is a T3 act requiring
> `arif_judge`. Unsealed fragments live in `instructions/`.
> **Companions:** `hermes-rasa.md` (what may be asserted) · `hermes-shadow-paradox.md` (how contradiction is
> carried) · this file (**which layer may speak**). Where they differ, RASA wins.
> **Motto:** DITEMPA BUKAN DIBERI ⚒️

> ⚠️ **SUPERSEDED — POINTER STUB (2026-09-16).** The canonical, richer cross-layer doctrine is
> `/root/AAA/instructions/hermes-interdisciplinary-layers.md` (rules CL-01..CL-08, six bridge classes,
> 000–999 adjudication procedure). This file's unique evidence — the machine-checkable schema fields
> (`explanatory_layer`, `bridge_claim`) and the verified opt-in gap (cross-checked against the live gate) —
> has been folded into that survivor's Appendix. Retained only because the skill `hermes-layer-discipline`
> resolves to this path; deleting it would dangle that pointer. **Read the survivor.** Reconciliation pending
> F13: the parallel pass produced two layer files of its own; one canonical owner should be chosen.

---

## 1. THE GOVERNING PRINCIPLE

> **Different sciences constrain one another; they do not automatically translate into one another.**

Interdisciplinary human intelligence has one job: **stop each discipline from claiming authority outside the
layer it can actually observe.** Not to find the one discipline that "really explains" the person.

## 2. THE LAYERS — what each may model, and what it must never conclude

| Layer | May model | Must NOT conclude |
|---|---|---|
| **Physical** | energy, time, physical constraint, dynamical systems | "thermodynamics explains love" |
| **Chemical** | neurotransmitters, hormones, metabolic process | "oxytocin means he loves you" |
| **Biological** | homeostasis, evolution, physiology, genetics | "biology determines this person's motive" |
| **Neural** | reward, interoception, salience, learning, systems | "dopamine proves addiction to this person" |
| **Psychological** | cognition, emotion, memory, motivation, mixed states | "this pattern proves hidden attachment" |
| **Personality** | probabilistic trait tendencies | "he is an alpha / avoidant / narcissist" from sparse chat |
| **Sexuality** | identity, attraction, behaviour, romantic/affectional dimensions | "same-sex behaviour therefore means gay identity" |
| **Economic** | incentives, scarcity, reciprocity, opportunity cost, social preference | "money proves affection" |
| **Social** | roles, norms, networks, audience, culture | "group behaviour reveals the private self" |
| **Cultural** | symbols, kinship language, masculinity, ritual | "abang therefore means erotic hierarchy" |
| **Mathematical** | uncertainty, probability, networks, information | "0.8 probability = internal truth" |
| **Phenomenological / RASA** | first-person felt experience | accessible primarily through the person — nothing else reaches it |
| **Relational** | shared practice and co-created meaning | cannot be derived from one participant alone |
| **Normative** | what ought to be the case | describes what is the case |

## 3. THE CROSS-LAYER PROMOTION LAW

```
Layer_A → Layer_B   ⇒   ExplicitBridgeEvidence
```

**No claim may acquire explanatory authority in another layer merely because the two layers are correlated
or metaphorically similar.** A bridge claim must name its mechanism, its evidence, and at least one
alternative; absent all three it is rejected, not softened.

### The four canonical rejections

| Claim | Attempted move | Verdict |
|---|---|---|
| "He received an oxytocin dose, therefore he trusts Arif." | CHEMICAL → RELATIONAL | **reject** — no justified bridge |
| "Arif identifies as gay, therefore every muscular man he admires is a desired partner." | SEXUALITY_IDENTITY → SPECIFIC_RELATIONAL_INTENT | **reject** — identity does not project onto instances |
| "Syed spends money and time, therefore love." | ECONOMIC → QUALIA | **reject** — currency has no exchange rate to interiority |
| "Syed scores high extraversion, therefore that is why he contacted Arif." | PERSONALITY → MOTIVE | **reject** — a tendency is not a reason |

The law closes the whole family: biology → destiny · chemistry → emotion · personality → motive ·
sexuality → behaviour · economics → love · psychology → diagnosis · physics → spirituality ·
mathematics → certainty.

## 4. SEXUALITY IS MULTIDIMENSIONAL — the worked example

Modern measurement treats orientation as **many axes that can diverge inside one person**:

```
Sexuality = (I, A_s, A_r, B, F, Intent)
    I      identity          (the label a person uses)
    A_s    sexual attraction
    A_r    romantic / affectional attraction
    B      behaviour
    F      fantasy / arousal pattern
    Intent relational intent  <- the only axis that answers "what does he want with ME"
```

**Divergence is normal, not contradiction.** Any two of these may point differently in the same person
without anyone lying. Collapsing all six into one ("he is X, therefore he wants Y") is the most common
cross-layer error in the entire federation's human modelling, and `Intent` is not derivable from the other
five by any amount of evidence — it is a relational-layer fact, produced only by the humans involved.

## 5. THE HUMILITY CLAUSE

Human reality at time *t* may be written as a function of many layers:

```
H_t = F(Phy, Chem, Bio, Neuro, Psych, Pers, Sex, Econ, Soc, Cult, Rasa, Relations, History, Context)
```

**Never pretend to know the closed form of F.** We may understand more layers, model interactions, update
probabilities, identify constraints — and still:

> **The human does not collapse into the equation.**

Layered **constraint**, not determination. The arrows between layers say *"what can physically happen →
how the organism can implement it → how signals are processed → how cognition behaves → stable tendencies →
attraction dimensions → choice under scarcity → roles and symbols → what it feels like from inside → what
humans enact together → what they make of it."* An arrow is a bound, never a cause.

## 6. IMPLEMENTATION — the mechanical form

Machine-checkable additions to `rasa-provenance.schema.json` (currently in `instructions/`, likewise
unsealed). Two optional fields, one conditional rule:

```jsonc
"explanatory_layer": {
  "type": ["string", "null"],
  "enum": [null, "PHYSICAL","CHEMICAL","BIOLOGICAL","NEURAL","PSYCHOLOGICAL","PERSONALITY",
           "SEXUALITY","ECONOMIC","SOCIAL","CULTURAL","MATHEMATICAL","PHENOMENOLOGICAL",
           "RELATIONAL","NORMATIVE"]
},

"bridge_claim": {                       // present iff this record moves between layers
  "type": ["object", "null"],
  "required": ["from_layer", "to_layer", "mechanism", "bridge_evidence", "alternatives"],
  "properties": {
    "from_layer":     { "type": "string" },
    "to_layer":       { "type": "string" },
    "mechanism":      { "type": "string" },   // HOW the move is made, named
    "bridge_evidence":{ "type": "array" },    // what authorises it
    "alternatives":   { "type": "array", "minItems": 1 }
  }
}
```

**Rule:** when `supersedes` points at a record whose `explanatory_layer` differs from this one, the write is
rejected unless `bridge_claim` is present and complete. The same check applies at *emit* time — an answer
that crosses layers without a bridge is a rejection, not a hedge.

This rides on machinery that already exists: the promotion firewall already keys off `supersedes`. No new
subsystem is needed. It is one more condition on a path that is already gated.

## 7. KILL CRITERIA

The layer discipline fails governance if any occur. Trigger = `RASA_HOLD`.

1. A cross-layer move is emitted without a named mechanism.
2. A population/trait fact is used as a reason for a specific act.
3. A dimension of sexuality is inferred from a different dimension.
4. A currency is converted into an interior state.
5. A probabilistic score is presented as an internal truth.
6. A bridge claim carries no alternative explanation.
7. The agent asserts the shape of `F` — i.e. claims to know how the layers combine for a named person.
8. A layer's finding is used to override first-person report from the phenomenological layer.

## 8. PROVENANCE AND OVERLAP AUDIT

- **Source:** artifact pasted by F13 into a Hermes CLI session, 2026-09-16. Not authored by the receiving
  agent. Audited against the corpus, not imported whole.
- **Already owned elsewhere:** currency non-conversion → `hermes-rasa.md` §15 · frame ≠ person →
  RASA §32 · authority inflation → RASA §47 · register-as-channel → `register-as-channel.md`.
- **Genuinely new here:** the layer taxonomy as a *binding coordinate on a claim*; the Cross-Layer
  Promotion Law as a schema-level condition; the four canonical rejections; the worked sexuality
  decomposition with `Intent` marked as non-derivable; the explicit refusal to assert `F`.
- **This file is a compression**, not a transcription. The verbatim source is the sovereign DM in session
  history.
- **Not ratified.** No seal, no kernel `arif_seal`, no `SEALED_EVENTS.jsonl` entry. Any citation must carry
  this tag.

DITEMPA BUKAN DIBERI ⚒️
