# G0-A NORMALIZATION PACKET v2 — Provenance Graphs

> Mode: READ-ONLY | Created: 2026-09-12T14:25:00+08:00
> Auditor: Hermes | Status: EVIDENCE COLLECTED (not sealed)
> Scope: Two critical traces only — W3 and GOVERNANCE_COLLAPSE

---

## TRACE 1: W3 Provenance Graph

### Finding: W3 has THREE independent computation paths with DIFFERENT inputs and semantics

No single source of truth for W3 exists. The displayed value depends on which code path is active.

#### PATH A: rest_routes.py (arifOS /health endpoint — live health surface)

```python
# /root/arifOS/arifosmcp/runtime/rest_routes/rest_routes.py:5715-5718
trinity_witness = {
    "human": 1.0 if actor_id and actor_id != "anonymous" else 0.5,
    "ai": 1.0 if model_card is not None else 0.85,
    "earth": 1.0 if any_organ_up else 0.0,
}
```

**Inputs:**
- human: 1.0 if actor identified, 0.5 if anonymous
- ai: 1.0 if model_card exists, 0.85 otherwise
- earth: 1.0 if any federation organ responds to health probe, 0.0 otherwise

**Formula:** W3 = ∛(human × ai × earth)

**Semantic meaning:** "Is the system configured to have human accountability, a model, and live organs?" — a CONFIGURATION check, not a WITNESS measurement.

**Sample outputs:**
- Full config: ∛(1.0 × 1.0 × 1.0) = 1.0
- No model card: ∛(1.0 × 0.85 × 1.0) = 0.947
- Anonymous, no model, organ up: ∛(0.5 × 0.85 × 1.0) = 0.754

#### PATH B: webmcp/governance.py (pre-flight governance evaluation)

```python
# /root/arifOS/arifosmcp/runtime/webmcp/governance.py:258-261
human_score = 0.95 if request.agent_did.human_sovereign else 0.3
ai_score = 0.9  # hardcoded — "Agent passed auth"
earth_score = 0.85 if request.evidence_urls else 0.5
tri_witness = TriWitnessScore(human=human_score, ai=ai_score, earth=earth_score)
tri_witness.W3 = tri_witness.calculate()
```

**Inputs:**
- human: 0.95 if human_sovereign flag set, 0.3 otherwise
- ai: 0.9 (HARDCODED — always 0.9 if auth passed)
- earth: 0.85 if evidence_urls present, 0.5 otherwise

**Formula:** W3 = ∛(human × ai × earth)

**Semantic meaning:** "Pre-flight estimate of witness confidence based on request metadata" — a PREDICTIVE heuristic, not a measurement.

**Sample outputs:**
- Full sovereignty + evidence: ∛(0.95 × 0.9 × 0.85) = 0.899
- Sovereignty + no evidence: ∛(0.95 × 0.9 × 0.5) = 0.753
- No sovereignty + no evidence: ∛(0.3 × 0.9 × 0.5) = 0.513

#### PATH C: phoenix_72.py (receipt-level post-hoc computation)

```python
# /root/arifOS/arifosmcp/runtime/phoenix_72.py:104-165
def compute_w3(tri_witness, position_debt=0, narrator_debt=0):
    h_raw = tri_witness.get("human", False)
    ai_raw = tri_witness.get("ai", False)
    ext_raw = tri_witness.get("earth", False)
    h = float(h_raw) if isinstance(h_raw, (int, float)) else (1.0 if h_raw else 0.0)
    ai = float(ai_raw) if isinstance(ai_raw, (int, float)) else (1.0 if ai_raw else 0.0)
    ext = float(ext_raw) if isinstance(ext_raw, (int, float)) else (1.0 if ext_raw else 0.0)
    w3 = (h * ai * ext) ** (1 / 3)
    # Positional debt degrades: penalty = min(debt * 0.15, 0.45)
    if position_debt > 0:
        penalty = min(debt * 0.15, 0.45)
        w3_effective = max(0.0, w3 - penalty)
```

**Inputs:** tri_witness dict from receipt data (boolean or float per channel), plus positional debt

**Formula:** W3 = ∛(h × ai × ext) − penalty (if positional debt > 0)

**Semantic meaning:** "Post-hoc witness quality including positional honesty" — the most sophisticated path, accounting for self-witnessing degradation.

#### PATH D: apex_primitives.py (tool-call metrics)

```python
# W3 = None (honest — "needs live witness channels")
```

**Semantic meaning:** "Tool-call metrics cannot carry witness information" — correctly returns UNKNOWN.

### W3 Provenance Assessment

| Property | Status |
|---|---|
| Canonical formula | ∛(H × AI × Ext) — geometric mean (Nash 1950) |
| Number of computation paths | 4 (rest_routes, governance, phoenix_72, apex_primitives) |
| Path agreement | NO — different inputs, different semantics |
| W3=0.74 origin | NOT TRACED to a specific path; likely a runtime state from Path A or B |
| Witness independence | NOT MEASURED — human/ai/earth scores are heuristic, not calibrated |
| Calibration dataset | NONE |
| Decision authority | Used as gate (F3 threshold ≥ 0.75) |

### W3 Provenance Verdict

**W3 is a HEURISTIC with four competing implementations, not a calibrated measurement.** The displayed value depends on which code path is active and what runtime inputs it receives. The canonical formula (∛(H × AI × Ext)) is correct, but the inputs are NOT independent witnesses — they are heuristic flags (actor identified? model card present? organ up? evidence URLs present?).

**Classification: HYPOTHESIS — the construct (tri-witness consensus) is valid, but the operational definition uses proxy flags instead of actual witness measurements.**

---

## TRACE 2: GOVERNANCE_COLLAPSE Provenance Graph

### Finding: GOVERNANCE_COLLAPSE is a deterministic classifier in arifFlow's vector diagnosis system

The classifier is located and fully traceable.

#### Classification Chain

```
1. G raw value from apex_primitives.py
   G = (A × P × E × X)^(1/4)
   (e.g., G = 0.51)

2. G injected into arifFlow VectorStore as Dimension::G reading
   value = G_raw

3. band_normalize(Dimension::G, raw_g) = raw_g.clamp(0.0, 1.0)
   (identity function for G — raw maps directly to health band)

4. health(Dimension::G) → (h_eff, freshness, is_pathology)
   h_eff = decay(h_band, tau, hl)
   (time decay reduces health if reading is stale)

5. band_of(h_eff):
   h >= 0.75 → "HEALTHY", pathological = false
   h >= 0.50 → "CAUTION", pathological = false
   h < 0.50  → "PATHOLOGICAL", pathological = true

6. constellation():
   - Check all WIRED dimensions
   - If G is the only pathological wired dim → "GOVERNANCE_COLLAPSE"
   - If multiple pathological → prefix with "PARTIAL_WIRING" + primary

7. fq_policy.yaml escalation:
   trigger: vector diagnosis GOVERNANCE_COLLAPSE (g-dimension pathological)
   action: report to arifOS :8088 for 888 review
```

#### Key Code Locations

| Step | File | Line |
|---|---|---|
| Dimension enum | vector.rs | 78: `Dimension::G => "GOVERNANCE_COLLAPSE"` |
| Band normalization | vector.rs | 104-110: `Dimension::G => raw.clamp(0.0, 1.0)` |
| Health computation | vector.rs | 312-368: `fn health()` with decay |
| Band classification | vector.rs | 600-608: `fn band_of()` — h < 0.5 = PATHOLOGICAL |
| Constellation | vector.rs | 520+: `fn constellation()` — single pathological dim = failure name |
| Policy trigger | fq_policy.yaml | 35: `GOVERNANCE_COLLAPSE (g-dimension pathological)` |

#### What triggers GOVERNANCE_COLLAPSE

```
GOVERNANCE_COLLAPSE occurs when:
  1. Dimension::G is WIRED (has an active producer)
  2. G raw value < 0.50 (after band normalization and time decay)
  3. G is the ONLY wired dimension with h < 0.50
  4. No higher-priority constellation (FEEL_UNANCHORED, REALITY_LAG) applies
```

#### Runtime conditions that produce it

If G = 0.51 (as observed) and no significant time decay has occurred:
- h_eff ≈ 0.51
- band_of(0.51) → "CAUTION" (NOT pathological)
- constellation would NOT be "GOVERNANCE_COLLAPSE"

If G = 0.51 AND the reading has decayed (stale data):
- h_eff = decay(0.51, tau, hl) could drop below 0.50
- band_of(h_eff < 0.50) → "PATHOLOGICAL"
- constellation → "GOVERNANCE_COLLAPSE"

**Therefore: GOVERNANCE_COLLAPSE requires BOTH a low G value AND staleness (or G genuinely below 0.50).**

### GOVERNANCE_COLLAPSE Provenance Verdict

**The classifier is DETERMINISTIC and TRACEABLE.** It is NOT a subjective assessment or a narrative label. It is a mathematically defined classification based on:
- G raw value from apex_primitives.py (which IS formula-correct)
- Time decay from staleness
- Band normalization (identity for G)
- Constellation logic (argmin pathological among wired dims)

**Classification: CLAIM (traceable) but with caveats:**
1. G raw value inputs (A, P, E, X) come from tool-call metrics — their freshness and completeness are unverified
2. The G=0.51 threshold for GOVERNANCE_COLLAPSE requires h_eff < 0.50, which requires either G < 0.50 or significant staleness
3. The escalation action ("report to arifOS :8088 for 888 review") is advisory — it does not auto-HOLD

---

## Updated HOLD Vector

| HOLD Label | Classification | Evidence |
|---|---|---|
| No F13 authorization | DIRECTLY_SUPPORTED | No authorization evidence found |
| WELL telemetry stale | DIRECTLY_SUPPORTED | 8-day staleness claim (verify timestamp) |
| GEOX parity mismatch | DIRECTLY_SUPPORTED | 26/27/30 count discrepancy |
| G < floor | CONSERVATIVE_HEURISTIC | G=0.51, formula correct, threshold discrepancy 0.70 vs 0.80 |
| W3 < 0.75 | METRIC_ARTIFACT_RISK | 4 computation paths, no canonical source, inputs are proxy flags |
| GOVERNANCE_COLLAPSE | DIRECTLY_SUPPORTED (if G decayed below 0.50) or CONSERVATIVE_HEURISTIC (if G=0.51 and not decayed) | Classifier traceable; depends on staleness |
| FQ fossilization | PLAUSIBLE | Formula clear, runtime state needs verification |

### Summary

| Classification | Count | Items |
|---|---|---|
| DIRECTLY_SUPPORTED | 3-4 | F13 absence, WELL stale, GEOX parity, possibly GOVERNANCE_COLLAPSE |
| CONSERVATIVE_HEURISTIC | 2 | G threshold, possibly GOVERNANCE_COLLAPSE |
| METRIC_ARTIFACT_RISK | 1 | W3 |
| PLAUSIBLE | 1 | FQ fossilization |

---

## Resolution Status

| Gap | v1 Status | v2 Status |
|---|---|---|
| W3 computation path | UNKNOWN | RESOLVED — 4 paths found, no canonical source |
| GOVERNANCE_COLLAPSE classifier | UNKNOWN | RESOLVED — deterministic classifier in vector.rs |
| F7 confidence cap | CONTRADICTION CONFIRMED | Carried from v1 |
| min_g_score | CONTRADICTION CONFIRMED | Carried from v1 |
| G formula comment | CONTRADICTION CONFIRMED | Carried from v1 |

---

## Remaining Unknowns

| ID | Description | Severity |
|---|---|---|
| U-011 | Which W3 path produced the displayed 0.74? | MEDIUM (all paths are heuristic) |
| U-012 | Is G=0.51 stale enough to trigger h_eff < 0.50? | HIGH (determines if GOVERNANCE_COLLAPSE is active) |
| U-013 | Are A, P, E, X inputs to G from fresh data? | MEDIUM |
| U-014 | W3 witness independence not measurable with current inputs | HIGH (fundamental limitation) |

---

## Recommendation

**G0-A v2 is sufficient for a constitutional verdict.** Both critical traces are resolved:

1. **W3**: Traceable but fundamentally limited — uses proxy flags, not actual witness measurements. Cannot be promoted to law. Retain as advisory signal.

2. **GOVERNANCE_COLLAPSE**: Fully traceable deterministic classifier. Active if G < 0.50 (after decay). Current state depends on staleness of G=0.51 reading.

**The HOLD is justified by:**
- Direct predicates (F13 absence, WELL stale, GEOX parity) — these alone support a HOLD
- Conservative heuristics (G, W3, FQ) — useful as signals, not as law

**No mutation is authorized. The HOLD remains in place on direct predicate grounds.**

---

DITEMPA BUKAN DIBERI — G0-A v2 COMPLETE, NOT SEALED
