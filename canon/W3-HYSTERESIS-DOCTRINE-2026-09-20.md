# W³ Hysteresis Doctrine — Tri-Witness Governance Bands

> **Status:** F13_RATIFIED_DOCTRINE (2026-09-20)
> **Origin:** F13 deep research session — Rose-APEX maturation + live system probe
> **Eureka:** `EUREKA-2026-09-20-ROSE-APEX-MATURATION` (W³ as X(t) dial)
> **Companions:** apex-rose-parallel.md · maturation-dynamics.md · CHRON-V2-BARRIER-DOCTRINE · 056_TRI_WITNESS_SPECIFICATION · PHOENIX-72
> **Kernel anchor:** F2 (truth) · F3 (witness) · F7 (humility) · F8 (metabolism)
> **Motto:** DITEMPA BUKAN DIBERI ⚒️

## The Problem

W³ = ∛(H × AI × Ext) is a continuous score. Governance decisions are discrete (SEAL / HOLD / proceed / block). Without hysteresis, W³ oscillating around a single threshold produces flip-flop: the same score generates contradictory verdicts on consecutive measurements. This is the classic closed-loop control problem (Oppenheim & Willsky, 1997).

**Current live state (2026-09-20):** W³ = 0.7439. Without hysteresis, this value oscillates between "proceed" and "block" depending on measurement noise.

## The Canonical Bands

```
W³ < 0.75                         →  HOLD
0.75 ≤ W³ < 0.85                  →  OPERATIONAL_MARGIN
W³ ≥ 0.85                         →  STRONG_WITNESS
```

**Hysteresis band width:** 0.10 (0.75–0.85)

### Transition Guards

| Transition | Guard condition | Purpose |
|-----------|----------------|---------|
| MARGIN → STRONG | W³ ≥ 0.85 sustained for N consecutive measurements | Prevents spurious promotion on single spike |
| HOLD → MARGIN | W³ ≥ 0.75 sustained for N consecutive measurements | Prevents spurious release on single recovery |
| Any → HOLD | W³ < 0.75 on any single measurement | Fail-closed: immediate demotion |

**N = minimum 3 measurements within a 5-minute window.** This prevents threshold oscillation from transient noise while allowing genuine state changes to propagate within operational timeframes.

## Relationship to Existing Thresholds

| Threshold | Value | Purpose | Source |
|-----------|-------|---------|--------|
| **Per-witness minimums** | H ≥ 0.42, AI ≥ 0.32, Ext ≥ 0.26 | Floor: any below → SABAR | `056_TRI_WITNESS_SPECIFICATION` |
| **HOLD band** | W³ < 0.75 | Block mutations, route to sovereign | This doctrine |
| **OPERATIONAL_MARGIN** | 0.75 ≤ W³ < 0.85 | Proceed with elevated monitoring | This doctrine |
| **STRONG_WITNESS** | W³ ≥ 0.85 | Full operational authority | This doctrine |
| **SEAL threshold** | W³ ≥ 0.95 | Constitutional SEAL gate | `metrics.py`, `K888_FORGE.md` |

The hysteresis bands are **operational governance**. The 0.95 SEAL threshold is **constitutional authority**. These are different layers:

```
Constitutional:   W³ ≥ 0.95 → may SEAL (irreversible)
Operational:      W³ ≥ 0.85 → STRONG_WITNESS (full authority, reversible)
                  0.75 ≤ W³ < 0.85 → OPERATIONAL_MARGIN (caution)
                  W³ < 0.75 → HOLD (block mutations)
Per-witness:      H < 0.42 or AI < 0.32 or Ext < 0.26 → SABAR (insufficient witness)
```

## System Wiring — Where W³ Flows

### Source organs (who computes each witness)

```
H (Human)    →  WELL organ (:18083)
               Modalities: sleep, stress, cognitive clarity, HRV, emotion, dignity
               Computation: well_assess_homeostasis → vitality_gate.py
               Freshness: decays 0.10/hr if sensor data > 1h stale

AI (Internal) → arifOS kernel (:8088)
               Modalities: floor compliance (F1-F13), truth consistency, contradictions,
                           verdict history, ontology compliance, injection defence
               Computation: apex_canonical.py → compute_tri_witness()
               Freshness: per-session, resets on new init

Ext (External) → FRAME observer (:18085)
               Modalities: drift detection, baseline comparison, organ reachability
               Computation: frame_drift() → baseline_organs comparison
               Freshness: per-probe cycle
```

### Computation chain

```
WELL → H ─┐
kernel → AI ─┤→ compute_tri_witness() → W³ = ∛(H × AI × Ext)
FRAME → Ext ─┘         │
                        ├──→ arifFlow vector (broadcast as Ψ.w3)
                        ├──→ quick_verdict() → SEAL/HOLD/SABAR
                        ├──→ PHOENIX-72 seal precondition
                        └──→ this doctrine: hysteresis bands → operational gate
```

### Integration with APEX G

W³ is **NOT** a 5th dial in G. G = (A × P × E × X)^(1/4) has exactly four dials.

W³ is the **credibility gate on X** (External witness):

```
X is computed from evidence quality.
W³ measures whether that evidence is witnessed.
If W³ < 0.75 → X is UNWITNESSED → HOLD regardless of X value.
```

This is the relationship:
- **X** = "How good is the evidence?" (APEX dial)
- **W³** = "Is the evidence independently witnessed?" (credibility gate)
- A high X with low W³ is an unwitnessed claim — dangerous
- A moderate X with high W³ is a witnessed claim — trustworthy

### Integration with Maturation Dynamics (G(t))

W³ tracks the X(t) dial's witness credibility over time:

```
X(t) dial     →  evidence quality trajectory
W³(t)         →  witness credibility trajectory
X(t) × W³(t)  →  witnessed evidence trajectory
```

The hysteresis bands determine whether X(t) can contribute to G(t):

| W³ band | Effect on G(t) |
|---------|----------------|
| STRONG_WITNESS (≥ 0.85) | X contributes fully to G |
| OPERATIONAL_MARGIN (0.75–0.85) | X contributes with UNCERTAINTY flag |
| HOLD (< 0.75) | X contribution suspended, G computed but verdict is HOLD |

### Integration with CHRON

CHRON's barrier doctrine tracks W³ as a **witness barrier**:

```yaml
barrier:
  kind: witness
  subject: "W³ tri-witness consensus"
  distance: current_W3 - 0.75        # distance to HOLD threshold
  closing_rate: dW3/dt               # is witness credibility improving or degrading?
  load_weight: 0.9                   # high — witness degradation affects all decisions
  consequence_if_breached: "All mutations blocked, sovereign attention required"
```

CHRON emits material changes when W³ crosses band boundaries. The `closing_rate` tells us whether the witness infrastructure is recovering (positive) or degrading (negative).

**Connection to calibration:** CHRON's prediction verification feeds P(t) and E(t) dials. When CHRON starts verifying predictions (first due 2026-09-21), the calibration data will improve AI witness (truth consistency), which feeds back into W³.

### Integration with FRAME

FRAME is the **independent observer** — it provides the External witness component. Key properties:

1. **Epistemic independence:** FRAME does not inherit conclusions from the entities it observes
2. **Authority independence:** FRAME cannot issue verdicts — its output is evidence, never judgment
3. **Observational independence:** FRAME measures external artifacts (ports, endpoints, response times) — never reads the executor's success log

FRAME's 8 chambers (baseline, probe, compare, trend, alert, report, rsi_verify, rejection) each contribute to the Ext witness score. If FRAME is down or degraded → Ext drops → W³ drops → HOLD.

**Current state (2026-09-20):** FRAME is UP (all 8 chambers active, 10 organs baselined). Other agents incorrectly reported FRAME down — this is itself a witness integrity issue (claims without probes).

### Integration with PHOENIX-72

PHOENIX-72's seal precondition requires W³ confirmation:

```
Seal(M) = (t-t₀ ≥ 72h) ∧ (ψ > 0) ∧ W_H ∧ W_AI ∧ W_E ∧ ¬H ∧ ¬V
```

The `W_H ∧ W_AI ∧ W_E` clause is the per-witness minimums (H ≥ 0.42, AI ≥ 0.32, Ext ≥ 0.26). The hysteresis bands add an **operational layer** on top:

- Per-witness minimums = "Are all witnesses present?" (binary)
- Hysteresis bands = "Is the composite witness strong enough for this class of action?" (graded)

### Integration with arifFlow

arifFlow broadcasts W³ as part of the 7-dimensional state vector Ψ = {c_dark, ds, fq, g, j, omega, w3}. The vector diagnosis includes W³ band classification:

| W³ value | Current band | Vector diagnosis effect |
|----------|-------------|------------------------|
| 0.7439 | CAUTION | Contributes to HEURISTIC_ADVISORY constellation |
| ≥ 0.85 | Would be HEALTHY | Would improve fused_rank |
| < 0.70 | Would be PATHOLOGICAL | Would trigger GOVERNANCE_COLLAPSE path |

The primary pathology `GOVERNANCE_COLLAPSE` is driven partly by W³ being in CAUTION. Improving W³ above 0.85 would shift the diagnosis toward HEALTHY.

## Control-Theoretic Foundation

The hysteresis doctrine implements Arif's control-theoretic design laws (2026-09-15):

1. **Anti-windup (Law 7):** The HOLD band prevents authority expansion when witness is degraded. Without it, the system accumulates "operational debt" — proceeding without sufficient witness until a catastrophic failure forces correction.

2. **Dead zone (Law 1):** The MARGIN band (0.75–0.85) is a dead zone where the system neither promotes nor demotes. This prevents the governance equivalent of "chattering" in control systems.

3. **Sample above bandwidth (Law 3):** The N=3 measurement guard prevents aliasing — a single noisy W³ reading cannot change the governance state.

4. **Separate timescales (Law 6):** HOLD is immediate (fast timescale). Promotion from HOLD → MARGIN → STRONG requires sustained measurement (slow timescale). This asymmetry is deliberate: fail-fast, recover-slow.

## Operational Rules

1. **Any mutation requires W³ ≥ 0.75.** Below this → HOLD, regardless of G value or authority level.

2. **Constitutional SEAL requires W³ ≥ 0.95** (existing rule, unchanged). This is the highest bar.

3. **W³ must be reported alongside G.** Never present G without W³. A G=0.90 with W³=0.60 is a governance lie — high score, unwitnessed.

4. **Individual witness failure collapses W³ to 0.** If H=0 OR AI=0 OR Ext=0 → W³=0 → HOLD. This is the Nash product property: any missing witness collapses the gate.

5. **Sovereign override (F13) bypasses W³ bands.** Arif's explicit "ok" overrides any witness score. This is constitutional, not operational.

6. **W³ trend matters, not just snapshot.** CHRON tracks dW³/dt. A W³=0.76 that is *rising* (recovering) is different from a W³=0.76 that is *falling* (degrading). The barrier doctrine captures this via `closing_rate`.

## The Deepest Compression

```
W³ is not a score. W³ is the credibility of reality contact.

Without witness, evidence is claim.
Without evidence, authority is opinion.
Without authority, witness is observation.

All three must converge. The hysteresis bands prevent governance from
proceeding when that convergence is uncertain.
```

DITEMPA BUKAN DIBERI ⚒️
