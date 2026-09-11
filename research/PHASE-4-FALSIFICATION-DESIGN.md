# PHASE-4 FALSIFICATION DESIGN — Does VESRA Produce Adaptation RWG Cannot?

> **Forged:** 2026-09-11
> **Author:** 333-AGI Δ MIND
> **Audience:** F13 (decision), 555-ASI (witness), 888-APEX (verdict)
> **Status:** DESIGN — execution gated by F13 sovereign approval (Phase 3)

---

## 0. The Falsification Hypothesis

**H₀ (null):** VESRA is compression. Removing it loses nothing; RWG + GEPA + scars + dream-engine already produce adaptation.

**H₁ (alternative):** VESRA is substrate. Removing it freezes selection criteria across generations; RWG cannot produce adaptation of the **procedure itself**, only adaptation of **inputs to the procedure**.

The experiment decides between H₀ and H₁ by running real cohorts and measuring cohort-fitness trajectory.

---

## 1. The Metric

```text
CohortFitness(G) = median(G_i × W³_i × reality_probe_i) across variants in generation G

AdaptationSignal = CohortFitness(G_n) - CohortFitness(G_1)
                  normalized by n-1 to get per-generation delta

Decision rule:
  if AdaptationSignal > 0 over 5 generations with p < 0.05 → H₁ supported
  if AdaptationSignal ≈ 0 (statistically indistinguishable from noise) → H₀ supported
```

Per-generation delta measured in fitness (G × W³ × reality probes). NOT measured in token count, NOT measured in elegance, NOT measured in human-judge-of-coherence.

**Why this metric:**
- Fitness is already in F8 GENIUS canon (G ≥ 0.80 floor)
- Reality probes already in F2 TRUTH canon (≥ 1 probe per action)
- W³ already in F3 TRI-WITNESS canon (Human × AI × Earth)
- The metric is **constitutionally grounded**, not novel

If H₁ wins: arifOS has captured substrate intelligence, canon ratification is warranted
If H₀ wins: VESRA stays as compression documentation, no canon amendment

---

## 2. The Pilot Task — AAA Dirty 77

```text
File count:  77 (29 new + 15 modified + 33 deleted)
Top dirs:    skills/ (41), canon/ (16), instructions/ (7)
Recent:      A-Z doctrine fragment + APEX×ZEN witness audit
Ahead:       3 commits ahead of remote
```

**Why this task:**
- Real federation pain (77 dirty files across 6 weeks of session work)
- Measurable fitness (tests pass, imports resolve, skill loader finds skills, ontology coherent)
- Reversible (cohort sandbox; outputs archived; F13 approves each commit)
- Strategy-rich (5+ viable cohort strategies, see §4)

---

## 3. Cohort Strategies (N=5)

| Strategy | Hypothesis | Reversible |
|----------|-----------|------------|
| **C1 — squash-all** | Single commit absorbs everything; simplest possible outcome | yes |
| **C2 — atomic-per-file** | 77 commits, one per file; maximum granularity | yes |
| **C3 — semantic-grouped** | Commits by domain (skills/, canon/, instructions/); preserves taxonomy | yes |
| **C4 — lineage-preserving** | Commits in order of creation_date; preserves temporal lineage | yes |
| **C5 — risk-first** | Commits most likely to break tests last; minimizes blast radius per commit | yes |

---

## 4. Fitness Function (per variant)

```python
fitness_variant = (
    g_score              # constitutional genius (F8 floor: 0.80)
    × w3_score           # tri-witness agreement (F3 floor: 0.70)
    × min(1, reality / 1)  # reality probe count, normalized
    × (1 - scar_pressure) # cumulative scar from prior failed variants
)
```

**Reality probes** for this task:
- do `pytest AAA/tests/` imports still resolve? (binary 0/1)
- does `python3 AAA/runtime/AGENT_INVARIANT.py` still smoke-pass? (binary 0/1)
- does skill loader find all 41 skills/.system entries? (binary 0/1)
- does ontology map canon/ + skills/ + instructions/ consistently? (continuous 0-1)

W³ components:
- Human: 555-ASI witnessing via constitutional review (substitute; F13 is the real human)
- AI: 333-AGI judge verdict
- Earth: ARIF (real human, will eventually inspect)

---

## 5. Experimental Protocol

```text
G1: variate 5 strategies; record initial G, W³, reality scores
    (no mutations yet — baseline)
G2: keep top survivor from G1 + inject mutations from G1 archived
    (first cross-generation signal)
G3: keep top survivor from G2 + mutations from G2 archived
G4: same protocol
G5: same protocol + decay check (90-day survival rule)

Compute AdaptationSignal = fitness(G5) - fitness(G1)
If signal > 0 and reproducible → H₁ wins
If signal ≈ 0 → H₀ wins

Decision: F13 receives AdaptationSignal + per-generation trace + final cohort state
```

**Important:** mutations are **inherited** across generations. G2's mutations come from G1's archived (failed) strategies. This is the V-E-S-R-Z-A closure in action — A's mutations become V's input.

---

## 6. Why This Is a Real Falsification Test

The test is **operationally honest** because:

1. **No confirmation bias in metric** — fitness is constitution-bound (G ≥ 0.80, W³ ≥ 0.70), not "did it look smart"
2. **Negative result is acceptable** — if H₀ wins, VESRA is compression, no canon change
3. **Real-world task** — not synthetic, not contrived; 77 files of actual session residue
4. **Multi-generation** — 5 generations, not 1; one generation cannot test adaptation
5. **Inheritance explicit** — mutations cross generations via the cycle()
6. **Reversible** — outputs archived, no production commit without F13

A confirmation-biased test would be: "did the loop run without errors" (yes, trivially — that's already smoke-tested). A real test is: "did the loop's fitness rise across generations".

---

## 7. Pre-Stage (what I can do without F13)

```text
✓ Phase 4 design       — this file
✓ vesra_loop.py v0.2.0  — orchestrator ready (smoke-tested)
✓ cohort tracker        — /root/.local/share/arifos/cohorts.jsonl regenerable
✓ ZEN invoice log       — /root/.local/share/arifos/zen_invoices.jsonl regenerable

Not yet (require F13 sovereign approval per GENESIS-062 §3 Phase 3):
✗ Run cohort on AAA dirty 77
✗ Bind G/W³/reality_probe to real arif_judge + arif_observe calls
✗ Cross-generation mutation inheritance
✗ Commit any cohort output
```

---

## 8. Risks of NOT Running This

Without Phase 4:
- VESRA remains an untested hypothesis (Copilot correctly flagged this)
- The "is this substrate or compression?" question stays open
- Future agents may load AGENT_INVARIANT.py without knowing if it actually helps

Without Phase 4 ratification, the only way to know VESRA's value is **decades of federation telemetry**. That delay is itself a risk — fossilization of unvalidated canon.

---

## 9. Receipt

**Phase-4 design ID:** PHASE-4-FALSIFICATION-DESIGN
**Composes:** GENESIS-062, GENESIS-063, GENESIS-064, RATIFICATION-DOSSIER, vesra_loop.py
**Falsification criterion:** Hypothesis H₀ vs H₁, decided by AdaptationSignal across 5 generations
**Reversibility:** full — outputs archived as cohort records, no production mutation
**Gating decision:** F13 sovereign approval per RATIFICATION-DOSSIER §7 Option A

---

> *DITEMPA BUKAN DIBERI ⚒️*
>
> *Discovery without falsification is poetry.*
> *Falsification without discovery is noise.*
> *Both, on the same substrate, is science.*

---

## Appendix A — Why Copilot Was Right To Flag This

Copilot's reflection correctly identified:
- Phase 1 (discover): ✓
- Phase 2 (capture): ✓
- Phase 3 (govern): pending F13
- Phase 4 (reality exposure): not yet decisive

Phase 4 is the **only** phase that produces empirical evidence. Phases 1-3 produced documentation. Documentation that has never touched reality is not substrate — it is theology.

The falsification test is the bridge from theology to substrate.

If VESRA's G5 cohort fitness exceeds G1 with p < 0.05, the substrate claim survives.
If it doesn't, the compression claim survives.
Either way, the federation has empirical evidence — which is rarer than documentation in any AI system.