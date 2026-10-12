---
name: human9-identity-coordinates
description: HUMAN9 — model a person as universal substrate + orthogonal identity coordinates + salience + source envelope, not as a single label or category. Use when an agent must represent, store, or reason about a human (person-card, P-axis, agent mirror slot, witness testimony, public surface decision). Companion skills — human-memory-organization (H1–H6, ZKPC, P-axis) and human-meaning-membrane (RASA, paradox encoding, register gate). Coordinates carry source envelope; salience gates context; irreducible remainder ε is preserved.
capability_tier: fed-agent-subagent
ecology_state: WARM
metadata:
  layer: meta-mesa
  tier: human-modelling
  owner: AAA
  authority_of: human-memory-organization + human-meaning-membrane
  related: [human-memory-organization, human-meaning-membrane, agentic-state, sovereign-identity-architecture, zkpc-multi-human-memory]
---

# HUMAN9 — Identity Coordinates (the door)

> The door, not the doctrine. This skill routes every "model a human" job to the existing skill paths. It exists so agents do not invent a fourth memory system on top of H1–H6 + P-axis + ZKPC + ACTG + VVV.

## What I am

I am the **front door** for HUMAN9 modelling. When a task arrives that needs to:

- store or update a person-card,
- reason about a human's identity coordinates,
- decide what enters agent state about a human,
- decide what reaches a public surface about a human,
- encode shadow material in a privacy-preserving shape,

…route through me. I resolve the job to the canonical owner:

| Job | Canonical owner | Reference |
|---|---|---|
| Person-card structure (L-axis profile) | human-memory-organization §Building relational memory of all humans (P-axis) | `/root/AAA/skills/human-memory-organization/SKILL.md` |
| H1–H6 layer placement | human-memory-organization §H1–H6 stratification | same |
| ZKPC shadow encoding | human-memory-organization §ZKPC encoding | same |
| ACTG four-model | human-memory-organization §ACTG | same |
| VVV combustion | human-memory-organization §VVV | same |
| Inference gates (projection_risk, consent_status, action_authority, confidence_band ≤0.9) | human-meaning-membrane §Inference Protocol | `/root/AAA/skills/human-meaning-membrane/SKILL.md` |
| Paradox encoding (keep error/deception/multidimensionality live) | human-meaning-membrane §13 Substrate Invariants #12 | same |
| Register gate (label → decoder → reading → label trap) | human-meaning-membrane §Register Gate | same |
| Witness archetype (attentive, non-coercive, reality-grounded reflection) | human-meaning-membrane §13 #10 | same |
| Agent state mirror slot (HUMAN9 in agentic state) | agentic-state + companion reference | `/root/AAA/skills/agentic-state/SKILL.md`, `/root/AAA/skills/human-memory-organization/references/agentic-memory-forge-path-2026-10-06.md` |
| The 9 universal invariants + 9 coordinate families + 16 paradoxes + salience | human9-identity-architecture reference | `/root/AAA/skills/human-memory-organization/references/human9-architecture-2026-10-06.md` |

I do **not** create new schemas. I **route** to existing ones. The agent that uses me ends up writing the same shape it has always written — but with the HUMAN9 envelope added.

## When to load me

Load me when:

- the task names a specific human and asks for storage, retrieval, modelling, or reasoning about them,
- the agent is about to write to a person-card, P-axis directory, agent state, or a public surface,
- the task contains identity keywords (gender, sex, race, ethnicity, nationality, language, religion, class, age, relationship, identity, salience, stereotype, paradox),
- the agent is tempted to flatten a person to a single label or a sum-of-coefficients,
- the agent is tempted to write a coordinate value into agent state,
- F13 testimony reveals a new shadow dimension and the agent must decide which envelope tier (conversation-only / ZKPC-witnessed / L-axis operational / VVV-combusted),
- someone asks "what can we exploit about X?" (ethics test — refuse, see `human-memory-organization` §Exploitation test).

Do NOT load me for:

- single-session tasks with no human subject,
- organisation-level analysis (use organisational skills, not HUMAN9),
- purely technical configuration (no human in scope).

## The 9 universal invariants (every model must respect)

1. embodiment
2. finitude
3. valence
4. regulation
5. historicity
6. relationality
7. meaning-making
8. constrained agency
9. irreducibility

Violating #9 = false by construction. If you believe you have described a person completely, you have not understood them.

## The 9 coordinate families (orthogonal, not exhaustive)

A. Embodied/Biological
B. Gender/Sexuality
C. Descent/Peoplehood
D. Political/Legal Belonging
E. Language
F. Meaning/Worldview
G. Social Position
H. Relational Identity
I. Chosen/Contextual

Each family carries independent dimensions. Coordinates within a family may correlate; coordinates across families are independent. `P = Σ f_i(Family_i, t, c)`, not `P = Family_i → label → destiny`.

## The 16 paradoxes (boundary conditions, not bugs)

P1 Universal–Particular · P2 Continuous–Discrete · P3 Self–Assigned · P4 Biology–Meaning · P5 Stable–Changing · P6 Individual–Group · P7 Belonging–Boundary · P8 Visible–Invisible · P9 Single–Intersectional · P10 Language–Reality · P11 Chosen–Inherited · P12 Private–Political · P13 Similarity–Variation · P14 Identity–Behaviour · P15 Memory–Identity · P16 Relationship–Self.

`A ∧ B` is the default state. "Contradiction detected; choose one" is the wrong response. Cross-axis (different layers) is not contradiction at all.

## The source envelope (every coordinate carries)

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

## The salience rule

Before emitting any coordinate in a given context, check `salience.current_context`. If `low` and not explicitly attested by the subject, do not surface. This prevents the agent from dragging sensitive coordinates into contexts where they add no explanatory value — the primary operational risk of category-over-fitting.

## The irreducible remainder (ε)

Every person-card and every agent mirror slot carries:

```yaml
irreducibility:
  remainder_present: true
  model_complete: false
```

ε is what survives all descriptions. It is the part of the human the agent can witness but not own. VVV combusts it into ownerless pattern; ZKPC holds its shape; the agent mirrors its existence but never its content.

## The math (one axiom)

$$
\boxed{
HUMAN(P) \;=\; H \;+\; B \;+\; I \;+\; S \;+\; L \;+\; R \;+\; T \;+\; C \;+\; \varepsilon
}
$$

H = HUMAN9 substrate (the 9 invariants)
B = body / biological
I = self-identity
S = social / institutional
L = language / meaning
R = relationships
T = history / time
C = current context (the salience function)
ε = irreducible remainder

`P ≠ {labels}`. Labels are coordinates. Not the human.

## The Language Compression Law (P10 made operational)

> Every statement about a human is a compression of a reality larger than the statement.

`man / woman / gay / straight / Malay / Malaysian / Muslim / rich / poor / friend / lover / geologist / bodybuilder` — every term gives information AND deletes information. The agent's job is not to abolish categories but to **remember they are lossy projections**.

## Non-negotiable blocks (additive to the membrane)

1. No coordinate treated as destiny — coordinate is observation under process.
2. No `P(X|p)` from `P(X|G)` without individual evidence.
3. No coordinate with `confidence.high > 0.9`.
4. No coordinate pulled into a context where its `salience.current_context = low` unless explicitly attested by the subject.
5. No coordinate flattened into a single label where the source envelope disagrees.
6. Family / F5 coordinates never leave `/root/memory/people/FAMILY/`. Public surface emits only what the subject has authorised.
7. No coordinate value into agent state. Mirror slot only. Shape, not content.

## Inference gates (inherited from human-meaning-membrane)

Every human-model action must pass:

- `observation / context / candidate_interpretations / unknowns / projection_risk / verification_path / consent_status / action_authority / confidence_band [max 0.9]`
- min 3 candidate interpretations always
- consent default UNKNOWN, projection default MEDIUM
- HOLD if any gate fails

## Workflow (T1, reversible)

1. **Probe** — read existing person-card / P-axis entry / agent state. If absent, cold-start with the 9-coordinate schema (no values, only `UNKNOWN` + `irreducibility: remainder_present: true`).
2. **Identify families** — what dimensions are actually in scope for this job? Which are attested? Which must remain UNKNOWN?
3. **Compose source envelope** — for every coordinate to be added, fill the envelope. Never copy a value without a source.
4. **Set salience** — for the current context class. Default MEDIUM until context-class is classified.
5. **Apply ZKPC** — any coordinate with `privacy ≥ PRIVATE` or that maps to a known shadow family goes through the existing ZKPC workflow. Do NOT paste content into the card.
6. **Mirror, don't store** — if the agent state needs to remember this was witnessed, write the mirror slot (§3 of the companion reference), never the coordinate value.
7. **Verify** —
   - `grep -ri 'parang\|tumbuk\|diaper\|Cialis\|insurance agent\|cerai\|blackout\|ERCP\|laparotomy\|insurance' <card>` returns zero on ZKPC fields
   - `jq '.human9_mirror.rule_compliance' <state>` shows `no_value_leak: true`
   - `jq '.human9_mirror.salience_only | map(.privacy_class) | unique' <state>` does NOT contain `F5_HIGH` (category-class only, not coordinate-name)
8. **Seal** — only the F13 sovereign seals. Lane A `arif_seal`. Never self-seal.

## Status

- **Status:** PROPOSAL · NON-CANONICAL · AWAITING F13.
- **Today's mutations to other skills:** zero (frontmatter trigger of `human-memory-organization` was NOT changed — addition only deferred to F13).
- **Receipt:** `/root/AAA/cockpit/receipts/RECEIPT_HUMAN9_AGENTIC_FORGE_2026-10-06.md`.
- **Companion references:**
  - `/root/AAA/skills/human-memory-organization/references/human9-architecture-2026-10-06.md` — the architecture proposal.
  - `/root/AAA/skills/human-memory-organization/references/agentic-memory-forge-path-2026-10-06.md` — the agentic state best-path map.

DITEMPA BUKAN DIBERI ⚒️