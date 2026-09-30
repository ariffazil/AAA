# ATLAS333 — FEDERATED TRI-SUBSTRATE FORGE
## Falsification Report + Migration Proposal

> **Status:** PROPOSAL · STAGED · NOT RATIFIED · NO CANON MUTATED
> **Authority:** F13 MANDATE 888 (2026-09-30) — "Research first. Map second. Crosswalk third.
>   Falsify fourth. Propose migration fifth. Do not mutate, ratify, overwrite canon, or seal
>   until the resulting architecture has been independently reviewed and explicit authority
>   has been granted."
> **Executor:** HERMES (FI-017) · **Date:** 2026-09-30
> **Method:** live probe of source + runtime; no assertion without a path, a count, or a command.
> **Provenance tags:** `[OBS]` observed live · `[DER]` derived from observed · `[UNK]` not determined

---

## 0. HEADLINE

The mandate asks for ATLAS333 to be *upgraded* from "Agent Paradox Map" to
"Master Invariant Atlas" spanning HUMAN / AGENT / PHYSICAL.

**Finding: two of the three axes already exist, the third is misnamed, and the
umbrella rename would overwrite a live canonical name.**

Recommended architecture is smaller than the mandate, not larger:

```
        three-consequence-domains (F13_RATIFIED 2026-09-13)   ← ALREADY SEALED
        R0 World   ·   R1 Human   ·   R2 Machine
                │           │           │
            PHYSICS-9   HUMAN-9    ATLAS333
           (GEOX domain) (AAA floor) (arifOS paradox map)
                └───── one EDGE CONTRACT ─────┘
                            │
                  Paradox #21 Map ↔ Territory
                     (already exists — the guard)
```

No new umbrella. No `H://` `A://` `P://` namespace. One crosswalk + one probe.

---

## A. RESEARCH — WHAT ALREADY EXISTS `[OBS]`

### A.1 ATLAS333 is a live, sealed, narrow canonical artifact

| Evidence | Value |
|---|---|
| `arifOS/core/shared/atlas.py` | 33,155 B |
| `ATLAS333_BRIDGE.md` | 18,885 B · theory→runtime zone map |
| `ATLAS333_COGNITIVE_GEOMETRY.md` | 27,897 B |
| `ATLAS333_EVERGREEN.md` | 33,397 B · mtime 2026-09-25 (active) |
| `ATLAS333_HUMAN_ATLAS.md` | 6,915 B · mtime 2026-09-05 |
| `ATLAS333_AGENT.md` | 5,571 B · maintenance protocol |
| `okf/atlas333/` | 53 files — 40 `paradox/` + 5 `apex/` + 5 `clusters/` + index/log/router |
| `333_MIND_ATLAS.md` | v53.2.1-PERMANENT · `ARIF-AGI::CANON::ATLAS-333::2025-10-03` · status CANON |

**Live MCP resources `[OBS]`** (`arifosmcp/resources/__init__.py:47-50`):
```
arifos://atlas333/index         ATLAS333 root index (cognitive geometry)
arifos://atlas333/paradox/list  Canonical paradox catalog — "36 rows, 35 IDs"
arifos://atlas333/geometry      Full cognitive geometry map
arifos://atlas333/flow          10-stage ATLAS333 pipeline
(+ arifos://atlas333/metrics in CANONICAL_RESOURCES)
```
`[DER]` **Four to five live URIs carry the name ATLAS333. Any change to its meaning is a
breaking change to a shipped resource family.**

### A.2 ATLAS333's own scope statement `[OBS]`
`333_MIND_ATLAS.md`: *"ATLAS-333 is the sole governing map for **paradox resolution** within
arifOS."* 33 axes = 25 Kernel + 5 Shadow + 3 Dark-Matter. Law: *"No new law names. All changes
are Axis Patches."*

`[DER]` ATLAS333 is **constitutionally scoped to paradox resolution.** It is not a substrate atlas.

### A.3 The AGENT axis is already built and deeper than the mandate assumes `[OBS]`

`ATLAS333_BRIDGE.md §2` — a 7-zone theory→runtime map, each row carrying
{paradox · runtime quote · GPV lane · primary floor · cognitive territory}:

| Zone | Theme | Territory |
|---|---|---|
| I | TRUTH (epistemology, evidence, certainty) | REASON |
| II | GOVERNANCE (law, power, sovereignty) | GOVERN / ACT |
| III | AGENT (identity, memory, self) | ORIENT |
| IV | GROWTH (learning, scars, improvement) | GROW |
| V | CONNECTION (maps, paths, relationships) | MAP / VERIFY |
| VI | SYSTEM (structure, flow, boundaries) | — |
| VII | WITNESS (verification, truth, proof) | — |

GPV lanes: `FACTUAL(τ)` · `CRISIS(ρ)` · `CARE(κ)` · `SOCIAL` · `EXPLORATORY`.
TEARFRAME thresholds (§5): TRM ≥ 0.94 · Echo ≥ 0.87 · RASA ≥ 0.85 · Amanah locked.

`okf/atlas333.md` clusters: **Memory (P1–P11) · Mind (P12–P22) · Judge (P23–P33) · Contour (P34–P35)**.
APEX dials: `C-dark-darkness · G-capability · H-humility · PHI-falsification · W3-tri-witness`.

`[DER]` The mandate's "AGENT AXIS — keep the original paradox axes, TEARFRAME, 10-stage geometry"
is **already complete**. Zero work required beyond a crosswalk pointer.

### A.4 HUMAN-9 is already the human-substrate floor `[OBS]`
`AAA/instructions/human-substrate.yaml` — `F13_RATIFIED`, 2026-09-29, `invariant_count: 9`,
`valence_required: true`, `law_zero` HARD, `final_prohibition` HARD.
H1 embodiment · H2 finitude (`AttentionEfficiency = ValueCreated / (AttentionConsumed +
ContextSwitchCost)`) · H3 valence · H4 regulation · H5 historicity · H6 relationality ·
H7 meaning-making · H8 reflexive constrained agency · H9 irreducibility (`M(H) != H`, `ε_model > 0`).
Plus `master_paradoxes` (P1 self-other, P2 agency-reality…). 301 lines.

### A.5 PHYSICS-9 is a GEOX rock-physics model, not a theory of physical reality `[OBS]`
`GEOX/src/geox_core/core/physics9.py` — header: *"BACKWARD COMPATIBILITY SHIM. All canonical
Physics-9 logic has migrated to `geox_core.physics`. DO NOT ADD NEW CODE HERE."*
Exports: `forward_physics9 · inverse_physics9 · bulk_modulus · shear_modulus · young_modulus ·
poisson_ratio · acoustic_impedance · vp_vs_ratio · thermal_diffusivity · fatigue_proxy ·
build_lithology_model · anomaly_contrast_theory · metabolic_loop` + `Physics13State` +
`EARTH_MATERIAL_CATALOG` (SANDSTONE/LIMESTONE/DOLOMITE/SHALE/ANHYDRITE/SALT/COAL/BASEMENT).
Spec: `GEOX/docs/PHYSICS_9_SPEC.md`. Owner: GEOX.

`[DER]` PHYSICS-9 is a **validated-scope domain model over earth materials.** Note also the
`Physics13State` symbol — the numbering is not even internally settled at 9.

### A.6 The partition the mandate wants ALREADY EXISTS — three times, in sealed canon `[OBS]`

**(1) `three-consequence-domains.md`** — F13_RATIFIED_CHAT 2026-09-13, kanon
`APEX_REALITY_GRAPH_MEMORY_MIGRATION_v1.md`:
```
R0 = World Reality   (External Constraints: Markets, Industry, Regulation)
R1 = Human Reality   (What Matters: Commitments, Energy, Attention, Stakeholders)
R2 = Machine Reality (What Can Act: Services, Repos, Containers, Ports)
R3 = Witness · R4 = Consequence · R5 = Governance
```
*"Memory that is not mapped to these consequence domains is ENTROPY."* + 5 Golden Questions.

**(2) `agent-compartment.md`** — F13 2026-09-13: the **A2H / A2A / A2M universal triangle**
(Human ↔ Agent ↔ Machine), with the Capability Graph → APEX → SEAL → ACT → WITNESS → SCAR chain.

**(3) `four-layer-separation.md`** — F13 2026-09-13 + F6 FRAME cycle rule 2026-09-29:
`AAA explains why · Kernel decides if · A-FORGE decides how · VAULT999 proves it happened`,
plus *"No organ may both observe AND mutate the same object in one cycle."*

`[DER]` **The mandate's triad is a FOURTH restatement of an already-sealed partition, under a
different vocabulary** (`Human/Agent/Physical` vs the sealed `Human/Machine/World`).

### A.7 The "map ≠ territory" guard is already a canonical paradox `[OBS]`
`ATLAS333_BRIDGE.md` ZONE V, paradox **#21 "Map ↔ Territory"** — *"no direct quote — meta-paradox"*,
GPV lane FACTUAL, floor **F4 (CLARITY)**, territory **MAP**.

`[DER]` The mandate's stated design anchor *("ATLAS333 protects the map, not becomes the
territory")* is **not a new design choice — it is ATLAS333 paradox #21, already sealed.**

### A.8 Capability ≠ Authority is already implemented `[OBS]`
`authority-envelope.md`: `CanMutate = AuthorityGranted ∧ ScopeMatches ∧ TargetPermitted ∧ BoundaryActive`
`apex-zen-alignment.md`: CAPABILITY ≠ AUTHORITY (F13_RATIFIED 2026-09-16)
`agent-compartment.md`: Capability Graph (Possibility Space) → APEX (Constraint Selector)

---

## B. FALSIFICATION REPORT `[OBS]+[DER]`

Mandate §18 instructed: *"Attempt to falsify it… Report negative findings."* Seven findings.

### F-1 · `REJECT` — The umbrella rename breaks a live canonical name
**Claim under test:** ATLAS333 should become the top-level "Master Invariant Atlas".
**Evidence:** 333_MIND_ATLAS.md declares ATLAS-333 *"the sole governing map for paradox
resolution"*, status CANON, continuity id `…ATLAS-333::2025-10-03`, law *"No new law names."*
4–5 live resources carry the URI. `ATLAS333_EVERGREEN.md` defines an **Evergreen Update
Protocol** (contour, don't excavate; never finish).
**Verdict:** widening ATLAS333 to mean "map of all reality" **contradicts its own sealed scope
statement and silently redefines 5 live resources.** This is exactly the class of failure the
mandate's §15 warned about. → **ATLAS333 stays narrow; it is the AGENT axis, not the umbrella.**
The mandate's own §15 option-2 ("ATLAS → {HUMAN-9, existing ATLAS333, PHYSICS-9}") is the
evidence-supported branch — with the correction that **even a new "ATLAS" umbrella is
unnecessary**, because the partition already exists (F-3).

### F-2 · `REJECT` — A HUMAN axis inside ATLAS333 was already attempted and hostile-rejected
**Claim under test:** Integrate HUMAN-9 into ATLAS333 as the HUMAN AXIS.
**Evidence:** `ATLAS333_HUMAN_ATLAS.md` (v0.1, 2026-09-05) — "ATLAS333-HUMAN: Paradox-Coordinate
Theory". It contains §3 *"CANDIDATE DIMENSIONS (**Not Universal Axes**)"*, §7
**HOSTILE REVIEW VERDICT**:
```
RETAIN CORE: Human = dynamic system managing trade-offs.
REJECT: Universal 9-axis ontology, "Energy" as literal physics, Health = Flexibility.
REFINE: Shadow = operational avoidance. Orbit/Navigator = continuous dimensions.
```
**Verdict:** the previous attempt to place a human axis inside ATLAS333's coordinate system was
**rejected by its own hostile review for making a universal axis ontology out of a person.**
That is precisely the failure mode the current mandate's §2 forbids.
`[DER]` HUMAN-9 and ATLAS333-HUMAN are **structurally incompatible**: ATLAS333's primitive is an
*axis coordinate* (35 paradoxes, GPV lanes, quantised thresholds); HUMAN-9's H9 says
`M(H) != H — ε_model > 0`, and `law_zero` says *"a person is always larger than the evidence
about them."* **A person cannot be a coordinate and remain irreducible.**
→ **Do not fold HUMAN-9 into ATLAS333. Link it, never embed it.**

### F-3 · `REJECT` — Tri-substrate separation is a duplicate of sealed canon (LAW 8 risk)
**Evidence:** A.6 above — three independent sealed documents already partition
human / machine / world, and `three-consequence-domains.md` states the partition *and* the
entropy rule *and* the pre-flight gate.
**Verdict:** minting an "ATLAS333 Triad" layer creates **a second owner for one problem**
(ARIFOS::ANTI_BANGANG_ENGINEERING LAWS 1, 3, 8). Cost: two vocabularies for one partition
(F4 CLARITY loss), plus a fourth coordinate system requiring its own SOT under FATWA K1.
→ **Reuse `R0/R1/R2`. Do not mint `H://` `A://` `P://`.**

### F-4 · `PARTIAL REJECT` — PHYSICS-9 is not the "PHYSICAL substrate"
**Evidence:** A.5. PHYSICS-9 is a GEOX earth-material rock-physics kernel (bulk/shear/Young/
Poisson/impedance/Vp-Vs/thermal/fatigue + material catalog), superseded by `geox_core.physics`
with `physics9.py` a shim, and carrying a `Physics13State` symbol.
**Verdict:** naming it "the PHYSICAL AXIS of reality" **contradicts the mandate's own §4**
(*"Do not generalize domain equations beyond their validated scope"* — *"Do not assume that
PHYSICS-9 is a universal theory of physics if the implementation is specifically rock/material
physics"*).
→ Correct label: **"GEOX physical model — validated scope: earth materials, elastic + thermal
+ fatigue proxies."** Anything wider is metaphysically false and operationally dangerous.

### F-5 · `ALREADY EXISTS` — 8 of the 20 substantive sections are already live doctrine
| Mandate § | Already exists as | Status |
|---|---|---|
| §7 F-CONTAM intervention | — | `[UNK]` see C-1 |
| §8 UNKNOWN ≠ UNCREATED | Void Guard / *"no data ≠ all clear"*; evidence taxonomy `MODEL_INFERENCE`/`UNKNOWN` | `[OBS]` exists |
| §9 Floor before score | APEX floor gates · F-series · 888_HOLD | `[OBS]` exists |
| §10 Capability vs Authority | `authority-envelope.md` · `apex-zen-alignment.md` | `[OBS]` exists |
| §11 Attention | `human-attention-membrane.md` · `sovereign-attention-preservation.md` · H2 `AttentionEfficiency` | `[OBS]` exists |
| §12 Memory | `state-transition-discipline.md` (Stored≠Retrieved≠Relevant≠Current) · `recovery-reality-cache.md` · `human-memory-compartmentalization.md` (STORY/MAP/POLICY) | `[OBS]` exists |
| §13 Relationships | `relationship-intelligence.md` · HERMES_RELATIONSHIP_KERNEL H1–H7 · perspective sovereignty | `[OBS]` exists |
| §6 edge contract | Capability Graph → APEX → SEAL → ACT → WITNESS → SCAR | `[DER]` partial — the YAML edge contract IS additive |

`[DER]` **Roughly 60% of the mandate is re-derivation of ratified doctrine.** That is not a
criticism of the mandate's intent — it is the argument for *linking* rather than *building*.

### F-6 · `RISK` — Attention and consequence: the mandate adds 14 deliverables and 0 new owners
§16 requires A–N (14 artifacts + schemas + migration). Under LAW 1 (*"kalau benda tu tambah
kerja manusia, ia bukan improvement"*) and LAW 6 (Arif Test: if Arif must read 1,000 words to
make one decision, it failed), a 14-part artifact set is a governance-debt generator unless a
**named human decision** hangs off each artifact. → Produce **one** doc (this), not fourteen.

### F-7 · `CONFIRMED GOOD` — three parts of the mandate are genuinely valuable
These survive falsification and I recommend them:
1. **§7 Model-Intervention Contamination** — `[UNK]` genuinely absent (see C-1). The single best idea here.
2. **§6 cross-substrate edge contract** — additive, cheap, and it is the *only* way to make the
   existing R0/R1/R2 partition machine-legible across substrates.
3. **§21 second question** (*"what must ATLAS333 refuse to know/decide/optimize/control?"*) —
   a genuine constitutional addition. Answer in §J.

---

## C. WHAT IS GENUINELY MISSING

### C-1 · `PARTIAL EXIST` — Model-intervention contamination (mandate §7): **fragmented, not absent**
**Probed** (`grep -rli` over `AAA/instructions`, `AAA/canon`, `arifOS/arifosmcp`, `arifOS/core`):
```
intervention_ledger | InterventionLedger   → 0 hits        (no unified primitive)
observer_effect                            → arifosmcp/models/verdicts.py
                                             arifosmcp/runtime/qqq_validator.py
contamination                              → AAA/instructions/hermes-rasa.md
                                             AAA/instructions/human-substrate.yaml
                                             AAA/instructions/triad-perspective-consequence-persistence.md
counterfactual                             → AAA/instructions/constitution.md
                                             AAA/canon/META-WISDOM-CANON-2026-09-21.md
                                             AAA/canon/APEX-MATH-CANON-2026-09-23.md
```
**Verdict (revised from `[UNK]`):** the concept is **already present in three independent homes**
— kernel verdicts (`observer_effect`), human doctrine (`contamination`), and mathematical canon
(`counterfactual`) — but there is **no single owner and no ledger**.
`[OBS]` Also confirmed: the evidence taxonomy already ranks `MODEL_INFERENCE` as class 6
(*"LLM-generated content, may hallucinate"*).

→ **Do NOT build a new intervention ledger.** Under LAW 8 (*satu masalah, satu owner, satu
jalan*) the correct action is to **name the one owner and point the three existing mentions at
it** — the same mistake the mandate would otherwise repeat at a larger scale.
`[DER]` This finding is itself the strongest argument against the mandate's §16 shape: the
federation's real disease is **fragmentation of existing primitives**, not absence of new ones.

### C-2 · `[DER]` Cross-substrate edge contract (adoption, not invention)
No existing doc expresses an edge that *declares its substrate pair*. Adding the field is
additive and does not rename anything.

### C-3 · `[OBS]` Deploy-boundary honesty (side-finding, unrelated to the mandate)
While executing the tree777 order I measured: `mcp.arif-fazil.com/llms.txt` is served from
`/opt/arifos/current/venv/lib/python3.13/site-packages/arifosmcp/static/llms.txt` — **the
installed package, not the repo.** `/root/arifOS` (source) and `/opt/arifos` (deployed) are
**different lineages**: source HEAD `91a1281fd`, origin/main `53eb7e437` (+13 unpushed),
deployed checkout `0e8e66a48`, deploy stamp `9eca4764e1fc`. **Stamp ≠ checkout.** The
event-driven reconciler holds by design when local is not contained in origin/main.

---

## D. PROPOSED ARCHITECTURE (smallest sufficient)

```
REALITY
   │
   ├─ R1 HUMAN      owner: AAA/human-substrate.*   floor: HUMAN-9 (H1..H9)   law_zero
   ├─ R2 MACHINE    owner: arifOS/ATLAS333         map: 35 paradoxes · 7 zones · TEARFRAME
   └─ R0 WORLD      owner: GEOX/physics9           scope: earth materials, VALIDATED ONLY
        │
        └── EDGE CONTRACT (only new artifact) ── declares substrate pair + provenance
                     │
        GUARD: Paradox #21 Map ↔ Territory  (F4) — already sealed, invoked as the check
```

**Constitutional relation (corrected from the mandate):**
```
HUMAN ≠ MACHINE ≠ WORLD          (three namespaces, no collapse)
HUMAN ↔ MACHINE ↔ WORLD          (edges explicit, each declaring its substrate)
R0/R1/R2 are the sealed names. Do NOT introduce H:// A:// P://.
```

**What ATLAS333 becomes under this proposal: nothing.** It keeps its scope, its 35 paradoxes,
its 5 URIs, its Evergreen protocol. It gains **one crosswalk pointer** and **one crossed edge
into R0 and R1**. The "Federation Atlas" is the existing R0/R1/R2 partition + the edge contract.

**Why this and not the mandate's structure:** the mandate's structure requires renaming a sealed
artifact (F-1), attempting an already-rejected human ontology (F-2), minting a fourth coordinate
system (F-3), and mislabelling a GEOX domain model as physical reality (F-4).

---

## E. CROSSWALK — the actual deliverable

| Substrate | Owner (single) | Normative artifact | Runtime surface | Bounded by |
|---|---|---|---|---|
| **R1 HUMAN** | AAA | `human-substrate.yaml` (H1–H9, law_zero) | `floor_gate.py` (VALENCE layer, telemetry-only) | `ε_human > 0` — H9 |
| **R2 MACHINE** | arifOS | `333_MIND_ATLAS.md` + `atlas.py` | `arifos://atlas333/{index,paradox/list,geometry,flow,metrics}` | F4 #21 Map↔Territory |
| **R0 WORLD** | GEOX | `PHYSICS_9_SPEC.md` + `geox_core.physics` | GEOX MCP (`geox_*`) | validated scope only |

**Edge set (6 directions, each must declare substrate pair):**

| Edge | Provides | Forbids |
|---|---|---|
| R1 → R2 | intent, authority, consent, meaning, correction, contest | agent becoming sovereign substitute |
| R2 → R1 | attention support, analysis, recommendation, memory | `Representation(Person) == Person` |
| R0 → R2 | measurement, constraint, causal consequence | `Model(P) == P` |
| R2 → R0 | model, simulate, plan, authorised actuation | `Simulation == Measurement` |
| R0 → R1 | body, time, energy, geography, mortality | `PhysicalConstraint == HumanMeaning` |
| R1 → R0 | action, craft, measurement, intervention | human standing outside reality |

---

## F. CAPABILITY GRAPH vs AUTHORITY GRAPH

Already canonical — **do not rebuild** (F-5). Anchors to cite instead:

```
Execution(X) = Capability(X) ∧ Authority(X) ∧ ConstitutionalFloor(X) ∧ ContextValidity(X)
               ↑ authority-envelope.md   ↑ apex-zen-alignment.md   ↑ F1–F13
```
Capability owners `[OBS]` (agent-compartment + organ map): AAA=attention · HERMES=meaning ·
APEX=judgment · arifOS=authority · A-FORGE=execution · FRAME=independent witness ·
CHRON=temporal/calibration · WELL/GEOX/WEALTH=domain intelligence.
**The missing edge is not capability vs authority — it is *substrate declaration* on every edge.**

---

## G. MIGRATION PLAN (mandate §16-N classification)

| # | Proposed change | Class | Reason |
|---|---|---|---|
| 1 | Rename/expand ATLAS333 → Master Invariant Atlas | **HOLD → REJECT** | breaks sealed name + 5 live URIs (F-1) |
| 2 | New umbrella artifact "ATLAS" | **HOLD** | partition already sealed (F-3); owner exists |
| 3 | Mint `H://` `A://` `P://` namespaces | **REJECT** | FATWA K1: fourth coordinate system, no SOT; duplicates R0/R1/R2 |
| 4 | Embed HUMAN-9 as an ATLAS333 axis | **REJECT** | H9 + law_zero; prior attempt hostile-rejected (F-2) |
| 5 | Relabel PHYSICS-9 as "physical substrate" | **REJECT** | violates mandate §4 itself (F-4) |
| 6 | Cross-substrate **edge contract** (YAML) | **LINK** | additive; only genuinely new artifact |
| 7 | Crosswalk table (this doc §E) | **LINK** | makes R0/R1/R2 machine-legible across owners |
| 8 | Intervention-contamination primitive (§7) | **CONSOLIDATE** | not absent — 3 scattered homes, 0 owner (C-1). Name one owner, delete the duplicates |
| 9 | Re-use R0/R1/R2 as the federation substrate names | **KEEP** | F13_RATIFIED 2026-09-13 |
| 10 | ATLAS333 paradox map, TEARFRAME, 10-stage flow | **KEEP** | already complete |
| 11 | Capability/Authority separation | **KEEP** | already enforced |
| 12 | HUMAN-9 · PHYSICS-9 · human-substrate · physics9.py in place | **KEEP** | mandate §3 RULE OF NON-DESTRUCTION honoured — nothing moved |
| 13 | This report | **STAGE** | not canon; awaiting independent review |

**Nothing in this proposal mutates, ratifies, overwrites, or seals any canonical artifact.**

---

## H. SCHEMA SKETCH (machine-readable, proposal only)

```yaml
cross_substrate_edge:
  source:            # object id
  target:
  source_substrate:  R0 | R1 | R2          # reuse sealed names — NOT H/A/P
  target_substrate:  R0 | R1 | R2
  relation:          provides | constrains | models | measures | contests
  observation:                      # OBS
  interpretation:                   # DER — must be marked
  inference:                        # INT — must be marked
  provenance:        # path | command | receipt id
  timestamp:
  confidence:
  authority:         # who authorised  (F13 for protected mutation)
  consent:           # required when source_substrate == R1
  intervention:      # PRE  | POST   <-- C-1: was evidence produced before or after the model acted?
  reversibility:     reversible | bounded | irreversible
  consequence_owner:                 # R4 — who pays if wrong
  witness:           # independent attestation
  unknowns:          []              # UNKNOWN ≠ UNCREATED
  remainder:         { acknowledged: true }   # ε > 0 always
```

---

## I. FAILURE MODES — net-new only (mandate §17; the rest are already floored)

| Failure | Detection | Gate | Recovery |
|---|---|---|---|
| **Cross-substrate category error** (`Simulation == Measurement`, `Model(Person) == Person`) | edge lacks `source_substrate`/`target_substrate` | refuse edge | mark UNKNOWN, re-issue edge |
| **Model-intervention contamination** (§7) | `intervention` field absent or POST-without-flag | fail-closed on evidence discount | counterfactual record |
| **Axis-ontology capture of a person** | a human appears as a coordinate/score | H9 + law_zero HARD | delete the model, not the human |
| **Domain-equation inflation** (GEOX physics generalised) | claim exceeds `PHYSICS_9_SPEC.md` scope | cite spec scope or HOLD | retract claim |
| **Vocabulary duplication of R0/R1/R2** | a new name for the same partition appears | FATWA K1 | point to the sealed name |

Already-covered (cite, do not rebuild): profile collapse · motive invention · identity freezing ·
prediction laundering · authority laundering · care coercion · engagement maximisation ·
false certainty · unknown→false collapse · capability→authority collapse.

---

## J. MANDATE §21 — THE TWO QUESTIONS

**Q1 — smallest architecture that federates human + agent + physical without any one model
claiming sovereignty over the others?**
> The one already sealed on 2026-09-13: **three consequence domains (R0 World · R1 Human ·
> R2 Machine)** + **one cross-substrate edge contract** + **ATLAS333 paradox #21 (Map ↔
> Territory, F4)** as the standing guard. Three names, one edge schema, one existing paradox.
> No new layer, no new name, no new coordinate system.

**Q2 — what must ATLAS333 deliberately refuse to know, decide, optimise or control?**
> **Refuse to decide:** authority (F13 alone) · verdicts (kernel) · who a person is (H9).
> **Refuse to know:** the interior of a person (qualia) · the future as fact ·
> anything outside R0's validated scope.
> **Refuse to optimise:** attention, engagement, session length, agent dependency,
> human compliance.
> **Refuse to control:** human choice · evidence about itself (no self-certifying, no
> model-induced confirmation counted as independent) · the meaning of names already sealed.
> **Refuse to be:** the territory. It is the map — and map↔territory is already paradox #21.

---

## K. WHAT I COULD NOT DETERMINE `[UNK]`

1. Whether a model-intervention ledger / counterfactual record already exists (C-1).
2. Whether `ATLAS333_HUMAN_ATLAS.md` (which contains named human case studies) is classified
   F5-private; it sits in `arifOS/core/shared/` — a **sensitivity finding worth a ruling**.
3. Whether `/opt/arifos` and `/root/arifOS` lineages were meant to converge (C-3).
4. Whether `arifos://atlas333/metrics` has live subscribers.

## L. AUTHORITY STATUS

```
RESEARCH      ✓  (live probes, 2026-09-30)
MAP           ✓  (§A)
CROSSWALK     ✓  (§E)
FALSIFY       ✓  (§B — 7 findings, 4 rejections)
PROPOSE       ✓  (§D, §G)
MUTATE        ✗  nothing mutated
RATIFY        ✗  awaiting independent review + F13 authority
SEAL          ✗  not sealed
```

**REALITY > EVERYTHING.**
