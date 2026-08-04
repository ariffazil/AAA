# FQ Scale Standard — Flow Quotient

> **Status:** OPERATIONAL ZEN (2026-08-04)  
> **Canon code:** `/root/arifFlow/src/receipt.rs` (`FlowQuotient`, `FlowVerdict`)  
> **SOT live:** `curl -sf http://127.0.0.1:7073/health` → `.fq`  
> **Cache:** `AAA/state/flow_state.json` (TTL 5 min, mirror only)  
> **DITEMPA BUKAN DIBERI**

---

## 1. Definition (one formula — never recompute offline)

```
FQ = Σ(cost_execute_ns) / Σ(cost_verify_ns [+ preceding_verify_ns])
```

Over a **sliding window of receipts** (daemon-owned; default N≈100 or store window).

| Symbol | Meaning |
|--------|---------|
| Numerator | Cost of **doing** (Execute, Seal, Merge) |
| Denominator | Cost of **checking** (Verify + preceding verify) |
| FQ = 1.0 | Equal cost of action and verification — equilibrium |
| FQ → 0⁺ | All verify, no execute — paralysis |
| FQ → +∞ | All execute, no verify — pure thrust (reported as large number or `f64::MAX`) |

**Fallback (code):** if verify `cost_ns` are placeholder defaults, use **count ratio**  
`execute_count / verify_count` so cost noise does not fake OVERHEAT.

---

## 2. Scale type — answer: NO negatives

| Property | Value |
|----------|--------|
| Scale class | **Ratio scale** (true zero, meaningful ratios) |
| Domain | **(0, +∞)** — never negative by construction |
| Unit | Dimensionless (cost / cost) or count / count |
| Zero | FQ = 0 only if no execute and no (or zero-cost) work — empty / pure freeze edge |
| Negative | **FORBIDDEN** — would not mean “reverse flow”; inventing −FQ breaks the formula |

**Why not negative?**  
Negative would require signed “anti-execution” or subtractive verify. That confuses FQ with **ΔS**, **G**, or **error budgets**. Separate signals stay separate:

| Signal | Domain | Job |
|--------|--------|-----|
| **FQ** | (0, ∞) | Action vs check *rhythm* |
| **G** | [0, 1] | Constitutional fitness |
| **ΔS** | signed OK | Entropy change of *output* |
| **FQ_gap** | ≥ 0 | \|live − cache\| or dual-register mismatch |

Use **log₁₀(FQ)** for charts if you want a symmetric-looking plot; store and seal **raw FQ ≥ 0** only.

---

## 3. Verdict bands (canonical — match Rust)

Source of truth: `receipt.rs` thresholds (not prose memory).

| Raw FQ | Verdict | Plain meaning | Agent posture |
|--------|---------|---------------|---------------|
| **> 10** | **OVERHEAT** | Execute ≫ verify — under-verification risk | Throttle execute, force verify, ANNOUNCE |
| **(3, 10]** | **OPTIMAL** | In flow; governance in architecture | Proceed; log trend |
| **(1, 3]** | **BALANCED** | Healthy support of action by check | Normal ops |
| **(0.5, 1]** | **WATCHING** | Checking competes with doing | Prefer cheap routes; watch trend |
| **≤ 0.5** | **STUCK** | Self-monitoring *is* the task | HOLD non-critical MUTATE; cool; FLAME/reroute |

**Special:** no verifies at all → code may emit **OPTIMAL** with quotient `∞`/`MAX` (suspicious pure execution — still not a negative).

### Mental anchors (memorize these three)

```
1.0  = equilibrium (do ≈ check cost)
3.0  = start of "in flow"
10.0 = start of "too hot — verify lagging"
```

Everything else is interpolation.

---

## 4. What the number means (and does not)

### Means

- **Proprioception of metabolism** — how hard the federation is *pushing* vs *checking*
- Windowed — **changes with time** (15 vs 45 both can be OVERHEAT)
- **Verdict class** often more actionable than raw float for gates

### Does NOT mean

- Quality / correctness (that is evidence + G + floors)
- Safety / risk (F1/F12/G)
- Human feeling / RASA / qualia
- Constitutional genius (G ≥ 0.80)

**Iron:** FQ ≠ G ≠ RASA ≠ J.

---

## 5. Presentation standard (zen for agents & cockpit)

Always emit a **bundle**, not a naked float:

```json
{
  "fq": 15.46,
  "verdict": "OVERHEAT",
  "band": ">10",
  "execute_count": 23,
  "verify_count": 19,
  "window": "daemon",
  "sot": "arifFlow:7073/health",
  "scale": "ratio_execute_over_verify",
  "domain": "(0, +inf)",
  "negative_allowed": false
}
```

### Optional display transforms (never replace SOT)

| Name | Formula | Use |
|------|---------|-----|
| **FQ** | raw | SEAL, gates, mirror |
| **FQ_db** | `10·log₁₀(FQ)` (only if FQ>0) | Charts; 0 dB @ FQ=1 |
| **FQ★** | clip/normalize for UI bars only | e.g. map log to 0–100 gauge — **label as display** |

Recommended **FQ_db** anchors:

| FQ | FQ_db ≈ | Band |
|----|---------|------|
| 0.5 | −3.0 | STUCK edge |
| 1.0 | 0.0 | equilibrium |
| 3.0 | +4.8 | OPTIMAL edge |
| 10.0 | +10.0 | OVERHEAT edge |
| 15.46 | +11.9 | current hot |

Still **no negatives on raw FQ**; FQ_db can be negative when FQ < 1 (that is fine for plots).

---

## 6. Dual-register (do not collapse)

| Register | Source | Role |
|----------|--------|------|
| **FQ_live** | `:7073/health` | Authoritative |
| **FQ_cache** | `flow_state.json` | Convenience, TTL 5 min |
| **FQ_gap** | \|live − cache\| | Staleness / Goodhart detector; ≥ 0 |

If `FQ_gap > 0.3` → `FQ_SIGNAL_DRIFT` → use live only.

Do **not** invent a second formula for “governance FQ.” Old 1.58 BALANCED was a **stale cache**, not a second physics.

---

## 7. Gates (standardized agent response)

| Condition | Action |
|-----------|--------|
| FQ unavailable | HOLD high-stakes MUTATE or use cache only if age < TTL |
| STUCK (≤ 0.5) | HOLD non-critical execute; cool |
| WATCHING | Prefer verify / FLAME; no panic |
| BALANCED / OPTIMAL | Proceed under floors |
| OVERHEAT (> 10) | ANNOUNCE; reduce execute; increase verify; no “all green” claims |

---

## 8. Zen one-liner

> **FQ is how many units of *doing* you buy per unit of *checking* in the recent window.**  
> **1 = even. 3–10 = flow. >10 = hot. <0.5 = stuck. Never negative. Never fold into G.**

---

*Aligned to arifFlow `receipt.rs` + FLOW_QUOTIENT_SPEC_v1. Standardized 2026-08-04 for federation agents.*
