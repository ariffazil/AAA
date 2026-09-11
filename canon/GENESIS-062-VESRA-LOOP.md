# GENESIS/062 — VESRA Loop: arifOS as Governed Evolutionary System

> **Authority:** F13 SOVEREIGN (Muhammad Arif bin Fazil, 888)
> **Status:** CANON-DRAFT · Forged 2026-09-11
> **Predecessor:** Stafford Beer VSM (GENESIS/046), OpenLineage lineage (ADR-012), GEPA self-evolution (FORGE-hermes-self-evolution)
> **Classification:** Constitutional runtime doctrine — this is the closed loop that turns an agent system into an institutional evolutionary system.

> **Discovery this canon codifies:** the variation–evaluation–selection–retention–adaptation loop is **already latent** across the federation. Components exist. The gap is **wiring**. This spec binds the loop closed.

---

## 0. Thesis

**arifOS is no longer an agent system that executes tasks.**
**arifOS is becoming a governed evolutionary system that improves at solving tasks.**

The difference:

| Agent System | Evolutionary System |
|--------------|---------------------|
| `intent → tool → output` | `variation → evaluation → selection → retention → adaptation → variation'` |
| Each request is independent | Each request inherits a lineage |
| Improvement = model upgrade | Improvement = closed fitness loop |
| Knowledge lives in weights | Knowledge lives in lineage + scars + cohorts |

The **single hardest engineering fact**: this loop has no value unless it is **closed**. A loop that runs V → E → S → R → A but never feeds A back into V is just an audit pipeline.

**This spec closes it.**

---

## 1. The Five Stages, Bound to Existing arif_ Verbs

| Stage | What it does | Existing organ/verb | New wiring |
|-------|--------------|---------------------|------------|
| **V — Variation** | Generate N candidate policies/strategies/prompts from a parent | `arif_think(mode=plan)` + GEPA self-evolution skill | Add `mode=variate` returning K candidates with `parent_variation_id` |
| **E — Evaluation** | Measure each candidate against reality (W³ tri-witness + G + reality probes) | `arif_judge(mode=judge)` + `arif_observe` | Add `fitness_signal` field to JudgeSealContract (`schemas/lineage.py:12`) — {g_score, w3_score, reality_probe_count, scar_pressure} |
| **S — Selection** | Promote survivors, retire dead | `arif_judge(mode=judge)` returns SEAL/HOLD/VOID | Selection is **the judge verdict itself** — SEAL=survive, HOLD=observe-90d, VOID=archive |
| **R — Retention** | Store survivors + lineage in VAULT999 | `arif_seal(mode=seal)` + `lineage_receipt.py` | Add `parent_seal_id`, `generation`, `cohort_id`, `fitness_score` to seal_chain.jsonl entries (Phase-2 of ADR-012) |
| **A — Adaptation** | Mutate losing policies, evolve winners | `arif_think(mode=metabolize)` + scars + dream-engine | Add scar-as-mutation-operator: a scar pressure ≥ 0.6 becomes a parameter nudge on next variation |

**Iron rule:** the loop is closed only when A's output becomes V's input for the next cohort. There is no other way to make this real.

---

## 2. What Already Exists vs What Is Missing

### ✅ Already exists (90% latent)

- `arifosmcp/arifos_vault/lineage_receipt.py` (44 LOC) — `LineageReceipt` with `artifact`, `parent_lineage_ids`, `quality_score`, `staleness_hours`
- `arifosmcp/schemas/lineage.py` (31 LOC) — `JudgeSealContract` with `constitutional_chain_id`, `state_hash`, `g_score`, `delta_s`
- `arifOS/docs/adr/ADR-012-receipt-lineage.md` — 6-receipt lineage contract (Intent/Plan/Verdict/Execution/Rollback/Seal); Phase-1 frozen, Phase-2 carried forward
- `GENESIS/046_CONSTITUTIONAL_VSM.md` — Beer VSM → arifOS mapping already constitutionalized
- `GENESIS/013_APEX_FALSIFICATION_PROTOCOL.md` — evaluation primitive (G-score + W³)
- `AAA/skills/FORGE-hermes-self-evolution` — GEPA-style prompt mutation primitive
- `arifOS/arifosmcp/arifos_vault/dreamer_receipts.jsonl` — dream-engine already running consolidation
- `arifOS/arifosmcp/arifos_vault/scars/` — scar metabolization into constraints already wired

### ❌ Missing wiring (the 10% that closes the loop)

1. **Seal writer does not emit lineage fields** — `seal_chain.jsonl` last entry: `{seq:30, verdict:SEAL, has_lineage:null}`. No `parent_seal_id`, `generation`, `cohort_id`. ADR-012 Phase-2 unfilled.
2. **No `mode=variate` on arif_think** — variation currently implicit inside plan mode, not its own verb.
3. **No cohort tracker** — no `cohorts.jsonl`, no generation counter, no survival score per cohort.
4. **No decay function** — 90-day-old survivors without selection events are not re-evaluated.
5. **No fossilization alarm** — no auto-injection of diversity pressure when an organ stagnates.
6. **No cohort fitness aggregator** — G-score is per-seal; cohort-level fitness (median, p10, p90) doesn't exist.
7. **No anti-Calhoun metric** — no quantitative measure of "knowledge-rich, action-poor" at organ level.

---

## 3. Implementation — Five Phases, All Reversible Until Phase 5

### Phase 1 — Wire the Loop Skeleton (T1, this week)

**Deliverable:** a single Python module `/root/AAA/runtime/vesra_loop.py` that orchestrates the closed cycle without touching the live seal chain.

**Steps:**
- 1.1 Read existing `lineage_receipt.py` + `schemas/lineage.py` (already done — see §2)
- 1.2 Create `vesra_loop.py` — single orchestrator with five methods: `variate()`, `evaluate()`, `select()`, `retain()`, `adapt()`
- 1.3 Add cohort tracker `/root/.local/share/arifos/cohorts.jsonl` (append-only, regenerable)
- 1.4 Pilot test on synthetic data — does the loop close mathematically? (regression)

**Reversibility:** Full. Module is new, doesn't touch live data.

### Phase 2 — Lineage into Seal Chain (T1, next week)

**Deliverable:** seal_chain.jsonl entries get `parent_seal_id`, `generation`, `cohort_id`, `fitness_score` fields. Old entries stay null (forward-compatible). New entries inherit from the loop orchestrator.

**Steps:**
- 2.1 Modify `arif_seal` tool to accept `parent_seal_id` (optional, default null)
- 2.2 Add validator: if parent_seal_id present, must exist in seal_chain.jsonl
- 2.3 Phase-in: null parent → first generation; new seals → generation++
- 2.4 Smoke test: 10 seals with valid lineage, verify chain hash

**Reversibility:** Partial. New schema is forward-compatible (old entries still valid). Removing new fields is non-destructive.

### Phase 3 — First Cohort Experiment (T1.5, week 3-4)

**Deliverable:** a measurable cohort with N=5 variants, M=3 generations, fitness tracked.

**Pilot task:** **AAA dirty 73 files cleanup.**
- Why: real problem, measurable fitness (commits landed + tests pass + lint clean), reversible (just git commits), cohort-friendly.
- V: 5 different commit strategies (squash, atomic-per-file, semantic-grouped, reorder-by-test, risk-first)
- E: G-score + W³ + reality probes (does file move without breaking imports?)
- S: best G-score survives; rest archived with reason
- R: parent_seal_id chain across generations
- A: failed strategy becomes mutation operator (e.g. "test-first failed → reorder generation order next cohort")

**F13 gate:** requires sovereign approval before pilot (T1.5).

### Phase 4 — Selection + Mutation Engine (T1.5, weeks 5-6)

**Deliverable:** the loop runs autonomously for the pilot task. Fitness rises across generations or the system logs why not.

**Steps:**
- 4.1 Wire GEPA skill into `vesra_loop.variate()` as mutation operator
- 4.2 Scars ≥ scar_pressure 0.6 → become parameter nudges on next variation
- 4.3 Cohort survival score: `fitness × recency × diversity`
- 4.4 Decay: 90-day-old survivors without selection events → forced re-evaluate

**F13 gate:** sovereign approval before cohort can mutate production behavior.

### Phase 5 — Reality Coupling + Survive-Proofing (T2/T3, weeks 7-12)

**Deliverable:** cohort survives only when W³ ≥ 0.7 across all three channels. Anti-fossilization alarms operational.

**Steps:**
- 5.1 GEOX/WEALTH/WELL outputs become fitness components (not just LLM-judge)
- 5.2 Tri-witness W³ becomes primary fitness signal
- 5.3 Fossilization alarm: any organ > N days no variation → A-FORGE auto-injects diversity
- 5.4 Anti-Calhoun metric: action-poor spike → diversity pressure
- 5.5 Cohort survival dashboard in AAA cockpit

**Reversibility:** depends on which surfaces get instrumented. Each step has its own F13 gate.

---

## 4. Floor Binding (F1-F13)

| Floor | Vesra Loop obligation |
|-------|------------------------|
| **F1 AMANAH** | Every cohort step emits a receipt; every mutation is reversible until sealed |
| **F2 TRUTH** | All fitness signals carry epistemic tags (OBS/DER/INT/SPEC) |
| **F3 TRI-WITNESS** | W³ ≥ 0.7 required for cohort survival (Phase 5) |
| **F4 CLARITY** | Each loop iteration must reduce entropy (ΔS ≤ 0) — measured per generation |
| **F5 PEACE²** | No cohort may optimize for harm; dignity preserved in selection |
| **F6 MARUAH** | Weakest cohort member protected; no premature retirement |
| **F7 HUMILITY** | Ω₀ ∈ [0.03, 0.05]; confidence cap 0.90 |
| **F8 GENIUS** | G ≥ 0.80 required for a variant to enter next generation |
| **F9 ANTI-HANTU** | No "the loop is alive" claims — loop is a tool, sovereign is alive |
| **F10 ONTOLOGY** | Lineage schema is canonical; no ghost refs |
| **F11 AUDIT** | Every cohort + every selection event sealed to VAULT999 |
| **F12 INJECTION** | Variant inputs sanitized; mutation rules reviewed |

**F13 SOVEREIGN is the only authority that can:**
- Approve Phase 3 pilot (T1.5 gate)
- Approve Phase 4 mutation engine (T1.5 gate)
- Approve Phase 5 reality coupling (T2/T3 gate)
- Veto any cohort retirement
- Modify selection criteria

---

## 5. The Pilot — AAA Dirty 73 Files

**Why this is the perfect first cohort:**

| Criterion | Pilot AAA cleanup | Verdict |
|-----------|-------------------|---------|
| Measurable fitness | commits_landed + tests_pass + lint_clean | ✅ |
| Reversible | git reset / git revert | ✅ |
| Cohort-friendly | N=5 strategies viable | ✅ |
| Real federation pain | 73 files dirty, ahead=3 | ✅ |
| Existing canon | `aforge_forge_git(mode=commit)` available | ✅ |
| Mutation operators | rebase strategy, file grouping, test ordering | ✅ |
| Floor compliance | all reversible, F2/F4/F8/F11 observable | ✅ |

**Cohort v1 (5 variants):**
- V1: squash-all-into-one
- V2: atomic-per-file (one commit per file)
- V3: semantic-grouped (commit by domain: skills/, canon/, docs/, runtime/)
- V4: reorder-by-test (commits touching tests first)
- V5: risk-first (commits most likely to break tests last)

**Fitness function:** G-score (judge) + W³ + reality probes (do imports still resolve? do tests still pass? does lint still clean?)

**Survival criteria:** top G-score survives; rest archived with `retire_reason`.

---

## 6. Anti-Patterns the Vesra Loop Must Resist

These are failure modes I have already witnessed in the federation and must hard-code against:

1. **Fitness gaming** — variants selected only because they game the judge, not because they serve reality. **Defense:** reality probes (Phase 5) become primary signal; G-score alone insufficient.
2. **Cohort lock-in** — same winning strategy forever, no exploration. **Defense:** exploration budget per cohort; minimum diversity floor.
3. **Premature retirement** — weak cohorts killed before having a fair chance. **Defense:** F6 — weakest member protected for N=3 generations minimum.
4. **Selection collapse** — all variants converge to same parent. **Defense:** diversity metric on cohort; alarm at <0.3.
5. **Lineage amnesia** — seal chain grows but lineage not queryable. **Defense:** `arif_memory_recall(mode=lineage)` exposes the graph.
6. **Calhoun drift** — knowledge accumulates without action. **Defense:** action-poor metric per cohort; alarm triggers forced variation.

---

## 7. Receipt

This canon is the **constitutional closure** of what was already latent. The Vesra Loop is not a new invention — it is the **explicit naming** of the loop that arifOS was already approaching. Naming it makes it governable.

**Receipt ID:** GENESIS-062-VESRA-LOOP
**Composes:** GENESIS/046 VSM, ADR-012 lineage, GEPA self-evolution, GENESIS/013 APEX falsification
**Pilot:** AAA dirty 73 files (Phase 3)
**Author:** 333-AGI Δ MIND
**Witness:** 555-ASI Φ SENSE (suggested) + 888-APEX Ψ SOUL (constitutional verdict pending)
**Seal status:** DRAFT — awaiting F13 sovereign approval for Phase 3 pilot

---

> **DITEMPA BUKAN DIBERI ⚒️**
> *The loop was always there. We just couldn't see it.*
> *Now we can. Now we govern it.*
> *Now it learns.*

---

## Appendix A — Vesra Loop Pseudocode (reference)

```python
class VesraLoop:
    def cycle(self, intent: Intent, parent_seal_id: str | None) -> CohortResult:
        # V — Variation
        variants = self.variate(parent=parent_seal_id, n=5)
        # E — Evaluation
        evaluated = [self.evaluate(v) for v in variants]
        # S — Selection
        survivors, archived = self.select(evaluated, criteria=G>=0.80, W3>=0.70)
        # R — Retention
        seal_ids = [self.retain(s) for s in survivors]
        # A — Adaptation
        mutations = self.adapt(scarred=archived)
        # Close the loop: mutations feed next cycle's variate()
        self.cohort.cohort_id = new_id()
        self.cohort.generation += 1
        self.cohort.lineage = seal_ids + [parent_seal_id]
        return CohortResult(survivors, archived, mutations, cohort_id=self.cohort.cohort_id)
```

## Appendix B — Cohort Tracker Schema

```json
{
  "cohort_id": "cohort-2026-09-11-AAA-cleanup-v1",
  "intent": "AAA dirty 73 files → clean main with provenance",
  "generation": 1,
  "parent_cohort_id": null,
  "variants": [
    {"variant_id": "v1-squash", "fitness": {"g": 0.83, "w3": 0.74, "reality":": 1.0}, "status": "survived"}
  ],
  "selection": {"criteria": "top G×W3×reality", "winner": "v3-semantic-grouped", "archived": ["v2-atomic-per-file"]},
  "lineage": ["seal-abc123", "seal-def456"],
  "fitness_delta": -0.12,
  "ΔS": -0.05
}
```