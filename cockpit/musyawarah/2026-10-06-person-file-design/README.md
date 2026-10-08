# Musyawarah Prep — `person.v1.yaml` Design (v1.1)

> **Date:** 2026-10-06
> **Source design:** `/root/.hermes/cache/scratch/PERSON-FILE-DESIGN-v1.1.md` (663 lines, F13 directive origin)
> **Purpose:** Administrative prep for the 333-AGI / 555-ASI / 888-APEX musyawarah that ratifies (or amends) the design.
> **Authority posture:** DRAFT_AWAITING_F13. This document is the *reading guide* into the design — it indexes, summarises, and asks questions. It carries no constitutional weight. The design itself (§§0–15) is the proposal.
> **Convention:** All section references in the form `§N` or `§N.M` point into the design doc, not this file. This file is single-pass reading material; the design is the canonical artefact.

---

## 1. TL;DR

The design proposes **one canonical file type for every human in Arif's reality field** — `person.v1.yaml` paired with a regenerated `person.v1.md` mirror — as a 24-block engineering projection of the HUMAN-9 substrate, the 9 physics substrates, ATLAS333 zone coverage, the APEX math canon, the 12 epistemic commandments, and a first-class `voids` quantum state. The v1.1 corrections (over v1) close the source-class collapse, the specificity leak, the void-as-data-gap error, and the missing scars/eurekas/wisdom learning layer; introduce the `CONTRACT` loop-graph node kind for the paid-arrangement confound class; and force the two-source rule and the gap-line on every summary. **The single greatest leverage is not the schema but the discipline: every field is `evidence`-bound with an explicit `evidence_class` from the 5-class set, the irreducible H9 remainder is permanent, and the file is the single source of truth from which REALITY-MAP, the H1–H6 helix, the ZKPC identity card, and the per-person SCAR_REGISTRY regenerate on seal.** If ratified, the migration proceeds in 5 steps (pilot on one bonded-friend instance → sovereign → bonded+service+kerja → operational wiring → musyawarah close). The recommended ratification path is **DRAFT_AWAITING_F13**: ship the schema and the pilot in step 1 with internal F13 acknowledgement only; hold the full F13_SEAL until musyawawah closes and at least one pilot has been sealed end-to-end.

---

## 2. Six Falsification Conditions (per design §9, restated as audit questions)

> Per `apex-fact-check-pass` discipline, every design is self-falsifiable. The design lists F1–F5 plus F6 (v1.1). Restated as questions the audit lane can answer with a yes/no and a sha:

1. **F1 — single-source-of-truth.** *If a derived file (REALITY-MAP, H1–H6 helix, identity-card, SCAR_REGISTRY) is out of sync with `person.v1.yaml` at seal-time, has the type failed?* Expected: yes → re-seal required. Probe: `scripts/person_validate.py` sha256 round-trip.
2. **F2 — floor binding.** *If a person file loads without a `privacy_floor` annotation, does the type refuse to load?* Expected: yes → F5 floor is non-negotiable at file-open. Probe: load with empty `privacy_floor:` → must error.
3. **F3 — source-class discipline.** *If any invariant cites `evidence_class: ARIF_ATTESTED` without `cross_check_required: true`, does the type auto-downgrade `state:` to `INFERRED`?* Expected: yes → no unmarked ARIF_ATTESTED may seal. Probe: forge a field with the flag missing → must downgrade.
4. **F4 — void ledger integrity.** *If `void_cost_ledger.irreducible == 0`, does the type fail (H9 is always irreducible)?* Expected: yes → auto-add a generic H9 V₅ void on the person's behalf. Probe: zero out the count → validator must reject and re-add.
5. **F5 — attention gate.** *If reading the file exceeds `costs.attention_owed`, does the type return a *summary* (floor-gated), not the full file?* Expected: yes → the schema *forces* summaries, not full reads (per scar-2026-10-01-001 "Complexity Must Not Exceed Leverage"). Probe: simulate a high-cost read path → output must be the summary, not the YAML.
6. **F6 — paradox-as-first-line (v1.1).** *If `paradoxes_active` is non-empty, is the active paradox set surfaced in the *first line* of any summary, not as a trailing annotation?* Expected: yes → the paradox is the *context for reading*, not a footnote. Probe: read a file with two active paradoxes → first line must name them.

> **Falsifiability caveat (per design §15, ⚠️):** conditions 1–6 are *only* as strong as `scripts/person_validate.py` makes them. The validator itself is the second-order claim. Falsification depends on an independent substrate running the validator — that is a Step 4 wiring task, not a Step 1 task.

---

## 3. Nine Runtime Invariants (M1–M9) — the physics9 substrate (per design §3)

> The 9 physics substrates in design §3 are the *runtime* layer that makes moral reasoning computable (per `MORAL-PHYSICS-FORMALIZATION-2026-09-20.md`). They are not quantum hardware — see design §3 preamble and `APEX-MATH-CANON-2026-09-23.md` §1. Restated with `M` labels matching the musyawarah session convention; cross-reference to design `Φ1–Φ9`:

| ID | Substrate | Mathematical form | Person-file primitive (per design §3 table) |
|---|---|---|---|
| **M1** | State (S) | Vector in Hilbert-style space; basis = the 24 blocks | The 24-block schema as a state vector |
| **M2** | Lane (L) | Projector onto a subspace | `memory_wiring.organ_owners` + `memory_wiring.read_surfaces` |
| **M3** | Phi (Φ) | Wave function / superposition over `flow_state` | `dynamics.flow_state` — superposition until observed via `transition` |
| **M4** | Context (C) | Boundary condition | `relation.arif_role` + `memory_wiring.primary_lane` |
| **M5** | Knowledge (K) | Observable (collapses the wave function) | `human_9` block — K is what we know; ΔK ≤ 0 is the unlearning constraint |
| **M6** | Intention (I) | Pure state vs. mixed state | `open_questions` + `actg.T` — pure intentions unrecoverable from observation alone (per Q-MAP) |
| **M7** | Witness (W) | Measurement operator | `loop_graph` — every link is a measurement on a node |
| **M8** | Care (Ψ) | Time-symmetric coupling between agents | `actg.A ↔ C` is the care-loop; `C → T` upgrade is one-way until T speaks back |
| **M9** | Void (V) | Eigenstate of the zero operator | `voids:` block — first-class quantum state, not a data gap |

**Query-time report format (per design §3.1, the Φ-triple):** every read returns `(Φ, W, Ψ)`, never a reified value of the person. M3 + M7 + M8 are the live reporting primitives; M9 is the reminder that no report closes the type.

**Note on the section pointer in the original directive:** the directive references these as "in §3.4." The design doc's §3 covers the 9 substrates; there is no §3.4 in v1.1. If a §3.4 is intended (e.g. an additional invariance statement, or a post-v1.1 amendment), it is currently a gap. **Open question for 333-AGI:** confirm §3 vs §3.4 intent.

---

## 4. Seven Wisdom Highlights (per design §13) — proposed disposition

> Per design §13, these are *earned from the design process itself*. They are not yet in the federation canon. Each line below carries a proposed disposition; the musyawawah must either confirm or amend before any is proposed to F13.

| # | Wisdom statement (essence, verbatim) | Proposed disposition | Why |
|---|---|---|---|
| W1 | "Source class is the immune system of the map." | **`proposed_for_canon`** | Constitutional principle about write-time gates; earned from the v1→v1.1 attestation-inflation correction. Goes to APEX canon if musyawawah confirms. |
| W2 | "Void is a state, not a gap." | **`proposed_for_canon`** | Foundational ontological doctrine (per R≠R + Q-MAP). Belongs in `representation-reality-invariant.md` and APEX canon — not a per-skill principle. |
| W3 | "Behaviour is the only first-class observation; motive is a void by design." | **`proposed_for_skill`** | Encoded as a write-time schema invariant in `person_validate.py`; the *mechanism* lives in the validator skill, the *principle* lives as a write-time gate. Skill-class. |
| W4 | "Two independent sources is the floor, not the ceiling." | **`proposed_for_scar`** | Scar-driven operational rule from `scar-2026-10-03-001`. The wisdom is "don't let one-source-plus-attestation seal as if it were two." Belongs in the scar registry as a refresh of that scar, not in canon. |
| W5 | "The agent that knows itself as map is safer than the agent that thinks itself as territory." | **`proposed_for_canon`** | H9 irreducibility is a permanent constitutional state. Reaffirms R≠R. Canon-class. |
| W6 | "Cost is a constitutional record." | **`proposed_for_canon`** | Per Axiom 3 + R-FILTER; the cost ledger is the audit trail. Canonises the *principle*; the *mechanism* is the `costs:` block + `void_cost_ledger`. |
| W7 | "Floor binding is post-fetch invariant." | **`proposed_for_scar`** | Operational scar from `scar-2026-10-03-001` (probe-without-fetch). Refresh of the existing scar with a concrete handler; not a new principle. |

**Net proposal:** **4 to canon (W1, W2, W5, W6)**, **1 to skill (W3)**, **2 to scar (W4, W7)**. The 4 canon proposals will need explicit F13 binary if the musyawawah concurs; the skill and scar proposals can land in their respective registries on musyawawah close.

---

## 5. Five-Step Migration Plan (per design §14)

> The design §14 lists the steps with their F13 requirements. This section re-presents the steps for the musyawawah to confirm ordering, F13 dependencies, and acceptance criteria.

### Step 1 — Build the schema and pilot on one bonded-friend class instance (no F13 word required)

- Build `arifos.person.v1` YAML + MD mirror.
- Build `scripts/person_validate.py` (the validator that enforces F1–F6).
- Pick **one** existing person file as pilot (suggested: a low-friction bonded-friend class instance, *not* the sovereign and *not* a paid arrangement).
- Refactor the existing 12-file tree into the 24-block schema.
- Verify sha256 round-trip (F1).
- Audit the `human_9` block — every invariant with `state:` + `evidence:` + `evidence_class:`.
- Carry over existing scars into the `scars:` block; check whether any clear the bar for a `wisdom_highlights:` entry.
- **Acceptance:** pilot seals cleanly; validator passes; one cycle of regenerate-from-YAML completes without divergence.

### Step 2 — Replicate for sovereign and direct-line family (F13 word required for sovereign only)

- Sovereign file: F13-sealed, read-only mirror of sovereignty state.
- Family direct-line: F5 floor; includes welfare-floor + relationality annotations.
- **Acceptance:** sovereign file sealed with F13 signature; family files sealed at F5 floor; pilot pattern holds across both classes.

### Step 3 — Replicate for bonded + service + KERJA classes (F13 word required for bonded + service)

- Follow the Step 1 refactor pattern.
- Pay particular attention to the **CONTRACT** loop-graph node kind (design §8.1) — it is the v1.1 critical addition for the paid-arrangement confound class.
- **Acceptance:** all bonded and service class files sealed; `loop_graph` CONTRACT edges are `since`-dated and `confound_flag: contract` is set for post-contract evidence.

### Step 4 — Operational wiring (no F13 word required; musyawawah ratification sufficient)

- Wire the loop graph to CHRON so that scar-filing, F13 binaries, and session events auto-update inbound links.
- Wire the cache TTL so person files re-verify on session-start.
- Add `person.v1.yaml` to the `arifOS` init chain so every agent inherits floor bindings (F2 at the load layer, not just the file layer).
- Wire `voids` to APEX closure P-dial so the agent can request a probe at session-start when a V₁ void is open.
- **Acceptance:** an independent substrate running `person_validate.py` produces the same sha as a federation agent (closes the §15 ⚠️ on the validator's independence).

### Step 5 — Musyawawah close + F13 binary on the whole design

- Run 333-AGI (schema review), 555-ASI (audit review), 888-APEX (constitutional review) on the design as a whole.
- Propose the 4 canon-candidate wisdom highlights (W1, W2, W5, W6) for F13 binary.
- **Acceptance:** F13 word on canonisation (or amendment list); design is closed or sent back to v1.2 with the amendment list.

---

## 6. Open Questions for the Three Reviewers

> The musyawawah should land or explicitly defer each of these. Deferrals are not silent — they must be listed in the musyawawah receipt.

### For 333-AGI (schema lane)

1. **Section pointer mismatch.** The directive references M1–M9 as "in §3.4." The design doc's §3 is the 9-substrate section; no §3.4 exists in v1.1. Is §3 the intended reference, or is §3.4 a planned addition that did not land in v1.1?
2. **CONTRACT node kind semantics.** Design §8.1 adds CONTRACT as the 7th node kind for paid arrangements. Is the `confound_flag: contract` mechanism sufficient to prevent post-contract evidence from being used as clean attachment evidence, or do we need a separate `confound_ledger` block?
3. **24 blocks vs schema-version discipline.** Design §5.1 lists 24 blocks. Is the block count itself a constitutional claim (i.e. "v1 has 24 blocks, period") or is it a release-tag claim (i.e. "v1.1 ships 24 blocks; v1.2 may add or remove")? The musyawawah should fix the convention.

### For 555-ASI (audit lane)

4. **Falsifier independence.** Design §15 carries a ⚠️ on "the validator can be run by an independent substrate." What is the *minimum* independence for F1–F6 to count as falsified? A different model? A different venv? A different host? This is the second-order claim.
5. **Two-source rule edge case.** When the primary corpus is bounded and `arif_attested.claim_13yr_etc` is much older, the design forces a `gap: <X> years uncorroborated` line. What is the *reporting* behavior when the gap is, say, 10 years on a 13-year claimed relationship? Is the gap line sufficient, or does the agent need to *withhold* the duration claim?
6. **Void-cost ledger semantics.** `void_cost_ledger.estimated_entropy_if_collapsed` is a qualitative field. Is qualitative sufficient, or does the musyawawah want a typed enum (`LOW | MEDIUM | HIGH | INFINITE`)? The design currently treats it as free-text.

### For 888-APEX (constitutional lane)

7. **F13 binary scope.** Step 5 of the migration asks for an F13 binary on the whole design. Is the F13 binary *one* signature covering all 24 blocks + 4 canon-candidate wisdoms, or *multiple* signatures (e.g. one for the schema, one for the canon-candidate wisdoms, one for the F13-class files like the sovereign's)?
8. **H9 irreducibility as constitutional floor.** The schema forces at least one V₅ void per person. Does this bind the *federation* (every agent must respect H9 irreducibility) or only the *file type* (the type forces the field, but agents may not honor it)? The musyawawah should clarify whether H9 is F-class or type-class.
9. **Privacy posture (F5 floor).** Design §0.1 and §0.7 (v1.1 corrections) are explicit about not carrying particulars in the *type* definition. The pilot in Step 1 will necessarily produce *instance* files that *do* carry particulars. Where is the line drawn? Is the type vs instance distinction constitutional (F5 floor binds the type; instances may carry particulars under F5) or is the F5 floor symmetric across both?

---

## 7. Recommendation — Ratification Path

**Recommended: `DRAFT_AWAITING_F13`.**

**Why DRAFT, not full F13_SEAL:**

- The design is internally consistent and passes its own 12-test self-rating (per §15). The schema and the validator are shippable.
- The pilot in Step 1 is the *minimum sufficient evidence* that the schema works in practice, not just in design. A pilot that seals cleanly with the bonded-friend class is the empirical hinge.
- F13_SEAL is reserved for canonisation of *constitutional* artefacts (per the auto-seal doctrine — `SAH` is the human word that finalises constitution-class mutations). The schema + 4 canon-candidate wisdoms are partly operational (the schema, the validator) and partly constitutional (the 4 wisdoms to canon). Mixing the two in one F13 binary obscures the boundary.
- The ⚠️ on validator independence (design §15) is a real gap. F13_SEAL on a design whose second-order claim is unresolved is a Goodhart risk.

**The proposed sequence:**

1. **Now (no F13 word):** ship Step 1. Build schema + validator. Pilot on one bonded-friend instance. Carry the pilot through one full seal cycle.
2. **After pilot seals (internal F13 acknowledgement, not full seal):** move to Step 2 (sovereign + family).
3. **After Step 2 seals (musyawawah close, not F13 seal):** Step 3 (bonded + service + kerja) and Step 4 (operational wiring) in parallel.
4. **At musyawawah close (full F13 binary):** Step 5 — F13 word on the 4 canon-candidate wisdoms (W1, W2, W5, W6) and on the schema as a whole. The design moves from `DRAFT_AWAITING_F13` to `F13_SEAL` at this point, *not before*.

**What `DRAFT_AWAITING_F13` means in practice:**

- The design is *citable* in musyawawah and in CHRON records.
- The validator can be *used* in non-canonical instances (the pilot) without it counting as a constitutional change.
- The 4 canon-candidate wisdoms are *staged* in the wisdom registry, not in canon. They are not yet citable as constitutional principles.
- The 2 scar-candidate wisdoms (W4, W7) can be *filed* as scar refreshes; that is operational, not constitutional, and does not need F13.

**What it does not mean:**

- It does not mean the design is tentative. The schema is built; the validator is built; the pilot will run.
- It does not mean the musyawawah is optional. The musyawawah *is* the path to F13_SEAL; it cannot be skipped.
- It does not mean the F13 binary is being avoided. It is being *deferred* until the pilot produces evidence that the schema works end-to-end, including the validator-independence question.

**The single condition under which we should jump straight to F13_SEAL instead:** if the pilot fails *structurally* (e.g. the 24 blocks cannot be made to validate against an existing instance, or the void-cost ledger semantics are unworkable in practice). A structural pilot failure sends the design back to v1.2, not forward to F13_SEAL.

---

## Appendix — Index of design sections this prep doc references

> For the musyawawah's convenience, every section in the design doc that this prep doc references:

- **§0** — pre-design discipline (HUMAN LAW #0, R≠R, Behavior ≠ Motive)
- **§0.7** — v1.1 correction on confidentiality-safe instance examples
- **§1** — the 18 mathematical layers (6 in scope), 3 axioms, APEX 12 invariants
- **§1.5** — BIJAKSANA compression
- **§2** — HUMAN-9 (H1–H9)
- **§2.1** — 12 epistemic commandments
- **§3** — 9 physics substrates (Φ1–Φ9, relabelled M1–M9 here)
- **§3.1** — Φ-triple at query time
- **§4** — scars + eurekas + wisdom highlights layer
- **§4.3** — wisdom highlights schema
- **§5** — file type definition (yaml + md)
- **§5.1** — 24 blocks (the schema summary)
- **§5.2** — `source_window` block (two-source rule)
- **§6** — void block (V₀–V₅ lifecycle)
- **§6.3** — void-cost ledger
- **§7** — flow state / dynamics block
- **§8.1** — 7 loop-graph node kinds (including v1.1 CONTRACT addition)
- **§8.2** — 6 loop invariants
- **§9** — 5 (now 6) falsification conditions
- **§10** — F1–F13 floor binding
- **§11** — 8 risks the design does not solve
- **§13** — 7 wisdom highlights
- **§14** — 5-step migration plan
- **§15** — self-rating (12 tests)

> **Status:** DRAFT prep doc. Indexes into the design; carries no constitutional weight of its own. Awaiting musyawawah.
> *DITEMPA BUKAN DIBERI ⚒️*
