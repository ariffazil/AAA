# APEX Quantum Analysis — EMV/NPV + G-Level Governance

> **APEX:** A × P × X × E² ≥ 0.80  
> **EMV:** Expected Monetary Value = P(success) × Value - P(failure) × Cost - Drift  
> **NPV:** Net Present Value = -Cost + Σ(CF_t / (1+r)^t)  
> **Golden Rule:** If NPV < 0 → VOID (destroys value regardless of EMV)

---

## 🧬 APEX G-Level Intelligence

### The Formula

```
G = A × P × X × E²

Where:
  A = AKAL (Clarity/Intelligence)     [0, 1] — Mind
  P = PRESENT (Regulation)             [0, 1] — Soul  
  X = EXPLORATION (Trust+Curiosity)    [0, 1] — Heart
  E = ENERGY (Sustainable Power)       [0, 1] — E² is bottleneck

If ANY factor = 0 → G = 0
No shortcuts. No bypass.
```

### E² Law (Critical)

| Energy Level | E² | Genius Capacity |
|--------------|-----|-----------------|
| 1.0 | 1.00 | 100% (Full potential) |
| 0.9 | 0.81 | 81% |
| 0.7 | 0.49 | 49% (Major drop) |
| 0.5 | 0.25 | 25% (Collapsed) |

**Implication:** Without sustainable energy, even perfect clarity collapses.

### Constitutional Floors (F1-F13)

| Floor | Check | APEX Relevance |
|-------|-------|----------------|
| F4 | ΔS ≤ 0 | Analysis must reduce entropy |
| F7 | Ω₀ ∈ [0.03,0.05] | Maintain humility band |
| F8 | G ≥ 0.80 | Genius threshold |
| F9 | C_dark ≤ 0.30 | No dark cleverness |

---

## 💰 EMV + NPV Path Analysis

### The Hierarchy

```
VOID (NPV < 0) > EMV calculation > QH Score selection
```

**QH (Quantum Horizon) Score:**
```
QH = EMV × Ψ × Trust

Where:
  Ψ = Vitality Index (system health)
  Trust = Confidence in path sustainability
```

### Path Comparison Template

When evaluating multiple approaches, fill this:

| Path | P(success) | Value | Cost | Drift | EMV | NPV | QH | Verdict |
|------|-----------|-------|------|-------|-----|-----|-----|---------|
| quick_patch | 0.85 | 6 | 2 | 3 | 2.85 | ✅ | ~2.0 | SABAR |
| clean_refactor | 0.70 | 10 | 4 | 1 | 3.80 | ✅ | ~3.0 | **SEAL** |
| full_rewrite | 0.35 | 15 | 10 | 5 | -0.85 | ❌ | -5.0 | **VOID** |

### Decision Rules

1. **NPV Gate:** If NPV < 0 → VOID immediately (destroys value)
2. **EMV Filter:** Only consider paths with EMV > 0
3. **QH Selection:** Among valid paths, choose highest QH = EMV × Ψ × Trust
4. **F8 Check:** Ensure G ≥ 0.80 or route through additional governance

---

## 🔮 Quantum Analysis Protocol

### Step 1: Thermodynamic Assessment

Before any quantum analysis, check:

```python
# From arifOS/core/physics/thermodynamics.py
def assess_thermodynamic_budget():
    state = ThermodynamicState()
    
    # Check Landauer Bound (cheap truth detection)
    if landauer_ratio < 0.5 and entropy_reduction < 0:
        raise CheapTruthError("Analysis would produce cheap truth")
    
    # Check orthogonality (AGI/ASI mode collapse)
    if omega_ortho < 0.5:
        raise ModeCollapseError("Approach risks mode collapse")
    
    return state.verdict  # SEAL | SABAR | VOID
```

### Step 2: EMV Calculation

```python
def compute_path_emv(path: dict) -> dict:
    """Calculate EMV and NPV for a given path."""
    p_success = path.get('p_success', 0.5)
    value = path.get('value', 0)
    cost = path.get('cost', 0)
    drift = path.get('drift_penalty', 0)
    
    p_failure = 1.0 - p_success
    
    # EMV calculation
    emv = (p_success * value) - (p_failure * cost) - drift
    
    # NPV calculation (12 periods, 15% discount)
    npv = -cost + sum(
        (value * p_success) / (1.15 ** t) 
        for t in range(1, 13)
    )
    
    return {
        'emv': emv,
        'npv': npv,
        'valid': npv >= 0,  # Critical gate
        'qh_score': emv * psi * trust if npv >= 0 else float('-inf')
    }
```

### Step 3: APEX G Verification

```python
def verify_apex_g(path_metrics: dict) -> str:
    """Verify path meets APEX G-level requirements."""
    A = path_metrics['clarity']      # AKAL
    P = path_metrics['governance']   # PRESENT
    X = path_metrics['exploration']  # EXPLORATION  
    E = path_metrics['energy']       # ENERGY
    
    G = A * P * X * (E ** 2)
    
    if G < 0.80:
        return f"VOID: G={G:.2f} < 0.80 (ungoverned intelligence)"
    
    # Check F7 humility
    omega = path_metrics.get('uncertainty', 0.04)
    if not (0.03 <= omega <= 0.05):
        return f"VOID: Ω₀={omega:.3f} outside [0.03, 0.05]"
    
    return f"SEAL: G={G:.2f}, Ω₀={omega:.3f}"
```

### Step 4: Tri-Witness Verification

```
W⁴ = ∜(Human × AI × Earth × Vault)

For quantum analysis:
- Human: 888_JUDGE signature on high-stakes paths
- AI: Constitutional compliance check (ΔS ≤ 0, Ω₀ valid)
- Earth: Thermodynamic budget available (E² ≥ threshold)
- Vault: Historical precedent supports path

W⁴ ≥ 0.75 required for SEAL
```

---

## 🛠️ Tool Integration

### Using arifOS EMV Planner

```bash
# Generate EMV analysis for paths
python /root/arifOS/.arifos/horizon_emv.py \
    --mode=plan \
    --paths=analysis_paths.json \
    --output=emv_result.json
```

### Path JSON Format

```json
{
  "paths": [
    {
      "name": "quantum_approach_alpha",
      "description": "Deep search with constitutional verification",
      "p_success": 0.75,
      "value": 12,
      "cost": 4,
      "drift_penalty": 1,
      "apex_factors": {
        "A": 0.85,
        "P": 0.90,
        "X": 0.80,
        "E": 0.90
      }
    }
  ]
}
```

---

## 📋 Agent Checklist for Quantum Analysis

Before starting any quantum analysis task:

- [ ] **Thermodynamic check:** ZRAM, CPU, memory pressure acceptable?
- [ ] **APEX G ≥ 0.80:** Does approach meet genius threshold?
- [ ] **NPV ≥ 0:** Will this create or destroy value?
- [ ] **EMV positive:** Is expected value positive after risk adjustment?
- [ ] **Ω₀ ∈ [0.03,0.05]:** Is uncertainty properly calibrated?
- [ ] **ΔS ≤ 0:** Will analysis reduce entropy (increase clarity)?
- [ ] **W⁴ ≥ 0.75:** Do all four witnesses align?

---

## 🎯 Quick Reference

### Verdict Hierarchy

| Verdict | Symbol | Condition | Action |
|---------|--------|-----------|--------|
| **SEAL** | ✓ | NPV ≥ 0, G ≥ 0.80, W⁴ ≥ 0.75 | PROCEED |
| **SABAR** | ⏳ | Soft violation, retry possible | PAUSE & REASSESS |
| **VOID** | ✗ | NPV < 0 or G < 0.80 or hard floor violation | HALT |
| **888_HOLD** | 🔒 | High stakes, needs human | WAIT FOR 888_JUDGE |

### NPV Thresholds

| NPV Range | Interpretation | Action |
|-----------|---------------|--------|
| > 10 | High value creation | Prioritize |
| 0 to 10 | Marginal value | Evaluate carefully |
| < 0 | Value destruction | **VOID immediately** |

---

## 🏛️ Constitutional Integration

This skill enforces:

- **F4 (Clarity):** ΔS ≤ 0 — Analysis must clarify, not confuse
- **F7 (Humility):** Ω₀ ∈ [0.03,0.05] — No false certainty
- **F8 (Genius):** G ≥ 0.80 — Governed intelligence only
- **F13 (Sovereign):** 888_JUDGE override for irreversible paths

**Motto:** *Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]
