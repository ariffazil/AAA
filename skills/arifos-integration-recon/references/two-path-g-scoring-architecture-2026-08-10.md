# Two-Path G Scoring Architecture (2026-08-10)

## The Discovery

arifOS has **two completely independent G score computations** that measure different things with different formulas. Confusing them causes false drift alarms.

### Path 1: `compute_apex.py` — Judgment Path (Constitutional)

**File:** `/root/arifOS/governance/_t000_evaluator/compute_apex.py`
**Called by:** `arif_judge` (the constitutional judgment tool)
**Input:** 13 floor scores (F1–F9, L10–L13) from the governance pipeline
**Output:** G, verdict (SEAL/SABAR/HOLD/VOID)

**Formula:**
```
A = geometric_mean([F2, F7, F10])        ← AKAL
P = geometric_mean([F1, F5, F11, F13])    ← PRESENT
E = geometric_mean([F4, F12, energy])      ← ENERGY
X = geometric_mean([F3, F6, F8, F9, risk]) ← EXPLORATION
G = geometric_mean([A, P, E, X])
```

**Hard floor overrides (lines 76-111):**
- F13 < 1.0 → VOID
- F9 < 1.0 → VOID ← **BUG: see below**
- F10 < 1.0 → VOID
- F12 < 1.0 → VOID

### Path 2: `apex_primitives.py` — Health Endpoint (Operational)

**File:** `/root/arifOS/arifosmcp/runtime/apex_primitives.py`
**Called by:** `rest_routes.py` line 1157 (`compute_apex_from_metrics()`)
**Input:** SQLite tool call metrics from `apex_metrics.db` (7-day window)
**Output:** G, C_dark, h, W3 (displayed in `/health` apex_scalars)

**Formula:**
```
A = lease_compliance (within_lease / n)
P = evidence_compliance (with_evidence / n)
E = success_rate (successes / n)
X = reversibility_rate (dry_run_first / n)
G = (A·P·E·X)^(1/4) with 0.01 floor per factor
C_dark = A × (1 - P) × (1 - X)
h = 1 - P
```

### Why They Differ

| Aspect | Judgment Path | Health Endpoint |
|---|---|---|
| **Input source** | 13 floor scores | Tool call SQLite metrics |
| **What it measures** | Constitutional compliance | Operational tool quality |
| **F7/F9 role** | Direct floor values in geometric mean | NOT USED (different inputs entirely) |
| **Typical G** | Varies (0.84 after fix) | 0.37 (from tool metrics) |
| **Fix domain** | Formula compliance inversion | Improve tool call practices |

### The Inverse Metric Bug (Fixed 2026-08-10)

**F7 (Ω₀ humility):** Low value = HIGH humility = GOOD
- F7=0.04 means "perfectly humble" (center of [0.03, 0.05] band)
- But `compute_apex.py` line 121 uses F7 RAW: `geometric_mean([F2, F7, F10])`
- With F7=0.04: A = geometric_mean([1.0, 0.04, 1.0]) = 0.3420 (dragged down)
- **Fix:** `A = geometric_mean([F2, 1-F7, F10])` → A = 0.9865

**F9 (C_dark shadow):** Low value = LOW deception = GOOD
- F9=0.00 means "zero deception" (maximally clean)
- But `compute_apex.py` line 130 uses F9 RAW: `geometric_mean([F3, F6, F8, F9, risk])`
- With F9=0.00: geometric_mean returns 0.0 (any factor ≤ 0 → 0)
- Hard floor check (line 89): `F9 < 1.0 → VOID` — ALWAYS triggers for clean systems
- **Fix:** `X = geometric_mean([F3, F6, F8, 1-F9, risk])` AND change hard floor to `F9 >= 0.30 → VOID`

**After fix simulation:**
```
A=0.9865  P=0.8409  E=0.6739  X=0.9229
G=0.8475 → SEAL ✅
```

### Practical Rule

When reading `/health` apex_scalars.G:
- **Low G (0.3-0.5)** from health endpoint → tool call quality issue (evidence, dry-runs)
- **Low G (0.0-0.3)** from judgment path → floor compliance issue (inverse metrics or hard floor)

Never compare apex_scalars.G with runtime_floors.F8 — they measure different things.

### Related Pitfalls

- `apex_primitives.py` is marked `MEMBRANE_BRIDGE` — temporary placement in arifOS until A-FORGE TypeScript implementation is ready
- W3 in apex_primitives is `None` (honest) — computed separately in rest_routes from `resolved_witness`
- QDF = G × (1 - C_dark) — derived scalar, not an independent measurement
