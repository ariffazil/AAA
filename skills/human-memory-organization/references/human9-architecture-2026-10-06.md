---
name: human9-identity-architecture
description: HUMAN9 — universal human substrate (9 invariants) + orthogonal identity-coordinate model + 16 paradoxes + salience + source-typed fields. How arifOS models a person without collapsing them into labels. Companion to human-memory-organization.
date: 2026-10-06
status: PROPOSAL · NON-CANONICAL · AWAITING F13
related: [human-memory-organization, human-meaning-membrane, agentic-state, sovereign-identity-architecture]
---

# HUMAN9 — Identity Architecture (2026-10-06)

> **Purpose.** Treat humans as **universal substrate + many variable dimensions + time + context + self-definition + relationships + irreducible remainder**. Never as `Malay → male → gay → 40s → therefore X`.

This document does **not** mutate the existing H1–H6 doctrine, ZKPC encoding, ACTG framework, or VVV combustion. It adds the **identity-coordinate layer** that already sits inside those doctrines implicitly.

---

## 1. The axiom (the math)

$$
\boxed{
HUMAN(P) \;=\; H \;+\; B \;+\; I \;+\; S \;+\; L \;+\; R \;+\; T \;+\; C \;+\; \varepsilon
}
$$

| Symbol | Meaning | Doctrine home |
|---|---|---|
| H | Universal HUMAN9 substrate (9 invariants every human shares) | §2 |
| B | Body / biological dimensions | §3, §4 |
| I | Self-identity (sovereign self-model) | H4 identity |
| S | Social / institutional position | §7, §8 |
| L | Language / meaning systems | §9 |
| R | Relationships | P-axis |
| T | History / time | H2, H6 |
| C | Current context (the salience function) | §16 |
| ε | Irreducible remainder (the VVV ash, the qualia gap) | VVV, RASA |

Therefore `P ≠ {labels}`. Labels are coordinates. Not the human.

---

## 2. The 9 universal invariants (HUMAN9)

Every human — across cultures, languages, religions, generations — shares these. They are **not identity categories**.

1. **embodiment** — has a body, lives through it
2. **finitude** — will die, knowledge is incomplete
3. **valence** — things feel good or bad
4. **regulation** — can modulate own state
5. **historicity** — carries a past that did not begin with them
6. **relationality** — exists only in relation to others
7. **meaning-making** — generates interpretations, not just reactions
8. **constrained agency** — chooses within limits, never from nothing
9. **irreducibility** — cannot be fully captured by any description of them

> Agent rule. Any agent claim that violates #9 is false by construction. If you believe you have described a person completely, you have not understood them.

This 9-set extends — not replaces — the `human-meaning-membrane` 13-substrate list (which was mostly epistemological). HUMAN9 adds embodiment, finitude, relationality, constrained agency explicitly as substrate (not just interpretive layer).

---

## 3. Identity coordinates (not categories)

Coordinates come in **nine orthogonal families**. Within-family dimensions can correlate; cross-family dimensions are **independent**.

| Family | Dimensions inside | Cardinal rule |
|---|---|---|
| A. Embodied/Biological | age, sex-characteristics, reproductive state, body morphology, ancestry, genetic variation, disability/functional state | biology ≠ destiny |
| B. Gender/Sexuality | gender identity, gender expression, sexual orientation, attraction, behaviour, identity labels | keep dimensions separate |
| C. Descent/Peoplehood | ethnicity, race/racialization, indigenous identity, clan/tribe/caste where relevant | race ≠ genetic ancestry |
| D. Political/Legal Belonging | nationality, citizenship, residency, migration status, statelessness, birthplace | legal bond ≠ culture |
| E. Language | first language, languages used, proficiency, dialect, register, literacy, code-switching | language ≠ thought |
| F. Meaning/Worldview | religion, spirituality, philosophy, ideology, moral commitments | declared belief ≠ full lived practice |
| G. Social Position | class, wealth, education, occupation, prestige, institutional role | role ≠ person |
| H. Relational Identity | child, parent, sibling, spouse, friend, mentor, lover, colleague, community member | identity changes by relationship |
| I. Chosen/Contextual | hobbies, fandoms, profession, scene membership, political affiliation, lifestyle groups | salience is contextual |

Rule: `P = Σ f_i(Family_i, t, c)`, not `P = Family_i → label → destiny`.

---

## 4. Composite fields must not be flattened

**Sex characteristics** is not `male|female`. It is:

```yaml
sex_characteristics:
  assigned_at_birth:
  reproductive_anatomy:
  hormonal_state:
  chromosomal_information:
  self_description:
  clinically_relevant_traits:
```

Most sub-fields default `UNKNOWN` unless attested by the subject or a clinical source. WHO distinction (sex ≠ gender; variations in sex characteristics are normal) is canonical.

**Sexual orientation** is at least four coordinates (attraction, behaviour, identity, relationship) per APA + WHO. The label "gay" lives under `identity` only.

**Race / ethnicity / ancestry** must NOT collapse into `bangsa`. Six separate fields: self-identified ethnicity, community membership, genealogical ancestry, genetic ancestry, racialised category, indigenous status, clan/tribe.

**State belonging** must NOT collapse into `country: Malaysia`. Seven fields: nationality, citizenship, country-of-birth, country-of-residence, habitual residence, migration history, legal status, cultural belonging.

**Age** is at minimum: chronological, biological, developmental, legal, social-generation, subjective, historical-cohort. A 40-year-old in KL 2026 ≠ a 40-year-old in rural Malaya 1950.

---

## 5. Source-typed fields (every descriptor carries a witness)

Every coordinate carries:

```yaml
value:        <scalar | string | ref | null>
source:       SELF_REPORT | DOCUMENTED | INSTITUTIONAL_RECORD | INFERRED | UNKNOWN
who_claims:   <person or system>
valid_at:     <ISO timestamp | range>
context:      <where the claim is licensed>
confidence:   [low_bound, high_bound]    # never > 0.9 (membrane rule)
privacy:      PUBLIC | PRIVATE | SOVEREIGN_ONLY | F5_HIGH
salience:     { current_context: low | medium | high }
unknowns:     [...]
```

This aligns with the existing `human-meaning-membrane` **Inference Protocol** (`observation / context / candidate_interpretations / unknowns / projection_risk / verification_path / consent_status / action_authority / confidence_band`). HUMAN9 carries the field-typed envelope; the membrane carries the inference gates.

---

## 6. The 16 paradoxes (boundary conditions, not bugs)

These are part of HUMAN — not defects to solve.

| # | Paradox | Pole A | Pole B |
|---|---|---|---|
| P1 | Universal–Particular | all humans share substrate | every person is unique |
| P2 | Continuous–Discrete | variation is continuous | institutions require categories |
| P3 | Self–Assigned | "I am X" | society/state may classify X differently |
| P4 | Biology–Meaning | bodies materially constrain life | biological traits acquire cultural meaning |
| P5 | Stable–Changing | identity provides continuity | identity develops over time |
| P6 | Individual–Group | groups have statistical patterns | individual cannot be derived from group mean |
| P7 | Belonging–Boundary | identity creates community | identity also distinguishes insiders/outsiders |
| P8 | Visible–Invisible | some traits are observable | many identities are private/interior |
| P9 | Single–Intersectional | categories can be analysed separately | lived experience arises from intersections |
| P10 | Language–Reality | language lets us represent reality | language can never contain it |
| P11 | Chosen–Inherited | some identities are chosen | others are assigned/inherited/constrained |
| P12 | Private–Political | identity may be deeply personal | institutions attach rights/resources to it |
| P13 | Similarity–Variation | members share category | within-group variance can be enormous |
| P14 | Identity–Behaviour | a person names themselves X | behaviour may not neatly correspond |
| P15 | Memory–Identity | past gives continuity | memory itself is reconstructive |
| P16 | Relationship–Self | identity belongs to person | who we are changes across relationships |

> **Agent rule.** `A ∧ B` is the default state. "Contradiction detected; choose one" is the wrong response. Same axis (coherence conflict) is genuine; cross-axis (different layers) is not contradiction at all.

This extends `human-meaning-membrane` **§12 Paradox Encoding** (kept all three live: error / deception / multidimensionality) by naming the 16 known patterns explicitly.

---

## 7. Intersectionality ≠ sum-of-coefficients

Bad model:

```
Woman + Malay + Gay + Poor = sum of four coefficients
```

Correct model:

```
Experience = f(Sex, Gender, Age, Class, Ethnicity, Language, Place,
               Institutions, Relationships, History, Context)
         + interactions X_i * X_j
```

(PubMed scoping review on intersecting identities; National Academies on typological thinking.)

---

## 8. Self is relational, not static

```
Self(P) ≠ single static state
Self(P, t, r, c) where r = relationship, c = context
```

Examples: `Arif-as-son`, `Arif-as-brother`, `Arif-as-geologist`, `Arif-as-friend-to-Syed`, `Arif-as-architect`, `Arif-as-citizen`, `Arif-alone` — all real, all non-mask. This is already implicit in ACTG (A/C/T/G) and P-axis family structure; HUMAN9 makes the **function signature** explicit.

---

## 9. Population priors are NOT individual destiny

```
P(X | G) = 0.63       # group prior
P(X | p) ≠ 0.63       # until individual evidence arrives
```

**Runtime law:** `population prior → individual evidence → person-specific posterior`. Never `category → stereotype → person claim`. Cements the membrane rule `Group variables audit distributions; individual evidence decides persons.`

---

## 10. Salience — the context function

Each coordinate carries `salience: { current_context: low | medium | high }`. Examples:

- **At immigration:** `nationality → HIGH`, `sexual orientation → IRRELEVANT`
- **At medical consult:** `biological traits → maybe HIGH`, `nationality → usually LOW`
- **At Syed relationship analysis:** `behaviour + self-described identity + relationship history → HIGH`, `ethnicity → LOW`

This prevents the agent from dragging sensitive coordinates into contexts where they add no explanatory value — the primary operational risk of category-over-fitting.

---

## 11. Language Compression Law (P10 made operational)

```
private experience → language → shared approximation
                    ≠
shared words = private experience
```

**L_CLaw:** *Every statement about a human is a compression of a reality larger than the statement.*

This is ε_qualia > 0 from `human-meaning-membrane`. Operational consequence: `man / woman / gay / straight / Malay / Malaysian / Muslim / rich / poor / friend / lover / geologist / bodybuilder` — every term gives information AND deletes information. The agent's job is not to abolish categories but to **remember they are lossy projections**.

---

## 12. Operational integration with existing doctrine

| Existing doctrine | HUMAN9 touch-point |
|---|---|
| H1–H6 (survival-value layers) | H4 identity = `I` self-model coordinates; H5 scars = P5, P6, P15 paradox witness; H6 constitutional = the invariants H through C that hold across all humans |
| P-axis / `people/` | Coordinate families A–I are the **field schema** inside person-card.md; each coordinate carries the source envelope |
| ZKPC shadow encoding | Coordinate shadows are encoded `SHADOW_XX:TYPE:ATTESTED + prohibited access list` per existing rule. Same law, applied to coordinate-shaped data. |
| ACTG four-model | `A = sovereign self-model` = the `I` slice of HUMAN; `C = sovereign model of subject` = the P-axis person card; `T/G = UNKNOWN/INFERRED` = the relationship dimensions of HUMAN (R) |
| VVV combustion | ε (the irreducible remainder) burns into VVV as **ownerless pattern** — same law, applied above ZKPC |
| Inference Protocol (membrane) | Source-typed fields (§5) + salience (§10) implement the protocol's `projection_risk` and `consent_status` at the field level |
| 16 paradoxes | Extends Paradox Encoding — names the 16 specific patterns the agent should expect, not just generic "keep three live" |
| Registry Gate / F2 receipts | Coordinate fields are F2-receiptable only when the source is documented AND attested — never from inference. |

---

## 13. Update procedure (T1, reversible)

To migrate an existing person-card to HUMAN9:

1. **Probe** — read the current `person-card.md`. List every existing scalar field. Mark each one as which Family (A–I) it actually belongs to.
2. **Split composites** — any field that combines >1 dimension (e.g. `sex: male` → split into sex-characteristics + gender-identity + gender-expression). Default unknown sub-fields to UNKNOWN, do not invent.
3. **Add source envelope** — every field gains `source, who_claims, valid_at, context, confidence [≤0.9], privacy, salience, unknowns`.
4. **Add ε block** — `irreducibility: { remainder_present: true, model_complete: false }`.
5. **ZKPC audit** — for any coordinate with `privacy ≥ PRIVATE` or that maps to a known ZKPC shadow family, re-encode per existing ZKPC rules. Do not paste content into the card.
7. **Verify** — `grep -ri 'SHADOW\|parang\|tumbuk\|diaper\|Cialis\|insurance agent' <card>` returns zero ZKPC fields with content leakage. Existing leak-check patterns apply.
8. **Do NOT touch H5-scars/ or registry**. HUMAN9 is an *envelope* layer over the existing scar ledger, not a replacement.

---

## 14. Non-negotiable blocks (additive, not replacing the membrane)

1. No coordinate treated as destiny — coordinate is observation under process.
2. No `P(X|p)` from `P(X|G)` without individual evidence.
3. No coordinate with `confidence.high > 0.9`.
4. No coordinate pulled into a context where its `salience.current_context = low` unless explicitly attested by the subject.
6. No coordinate flattened into a single label where the source envelope disagrees (`source: SELF_REPORT` ≠ `INSTITUTIONAL_RECORD` → keep both, label the disagreement).
7. Family / F5 coordinates never leave the `/root/memory/people/FAMILY/` envelope. Public surface only emits coordinates the subject has authorised for public release.

---

## 15. Open questions (recorded, not auto-resolved)

- Salience function — who sets it? Default proposal: agent sets a prior from context-class, subject may override.
- Coordinate versioning — when `valid_at` expires, does the coordinate stay with `confidence = 0` or get pruned? Architectural answer pending.
- ε block — does the agent ever surface what it cannot model? Default proposal: yes, with a one-line witness; never as a long elaboration.
- Cross-harness sync of coordinate fields — same sovereignty rule as P-axis (agent reads H-axis; never owns it).
- Public surface vs private surface — the existing F5 + P-012 rules remain binding.

---

## 16. Status & F13 queue

- **Status:** PROPOSAL · NON-CANONICAL · AWAITING F13.
- **Mutations made today:** zero. All new content under `references/`.
- **Next F13 binary (one choice, not a menu):**
  A. Seal the 9 invariants + 16 paradoxes as canonical substrate doctrine.
  B. Seal only the 16 paradoxes + source envelope (§5).
  C. HOLD — keep as reference for selective adoption.
- **Why one binary, not a menu:** the membrane prohibits menus. F13 chooses which, the rest falls out.

References: `/root/AAA/skills/human-meaning-membrane/SKILL.md` (paradox encoding, register gate, no-derivation-from-labels); `/root/AAA/skills/human-memory-organization/SKILL.md` (H1–H6, ZKPC, ACTG, VVV); WHO gender / sexuality framework; APA sexual orientation; UNHCR statelessness; National Academies population descriptors; PubMed scoping review on intersecting identities.