# FQ (Flow Quotient) — Five-Version Divergence Audit

> **Session:** 2026-08-14, Arif DM. Full audit of FQ computation across arifOS/ arifFlow.
> **Status:** [OBS] — all findings are from live code reading and live service probing.

## The Five Versions

FQ is computed in **three languages** with **five distinct implementations** that disagree.

### Version 1: arifFlow Rust (SOURCE OF TRUTH)

**File:** `/root/arifFlow/src/receipt.rs` — `FlowQuotient::compute()` (line 307)

```rust
// v2.1: count-based quotient = verify / execute (inverted from v2.0)
let raw_quotient = if verify_count == 0 {
    None  // undefined, not 0, not ∞
} else if execute_count == 0 {
    None  // observe-only window
} else {
    Some(verify_count as f64 / execute_count as f64)
};

// Six-state band
let verdict = if verify_count == 0 { Unmeasured }
    else if verify_count < 2 { Caution }
    else if execute_count == 0 { Flowing }  // observe-only neutral
    else {
        let q = raw_quotient.unwrap_or(0.0);
        if q >= 1.0 { Optimal }
        else if q >= 0.5 { Flowing }
        else if q >= 0.1 { Stuck }
        else { Burning }
    };
```

**Verdicts actually produced:** Unmeasured, Caution, Optimal, Flowing, Stuck, Burning
**Verdicts declared but NEVER produced:** Watching, Overheat, Balanced (dead enum variants)

### Version 2: arifFlow TypeScript (MIRROR)

**File:** `/root/arifFlow/src/ts/arifflow/state/fq.ts`

```typescript
// DIFFERENCE from Rust: uses cost_ns > 0 as proxy for count
// DIFFERENCE: two "unknown" states (UNMEASURED + UNKNOWN) vs Rust's one (Unmeasured)
const verdict = (() => {
    if (execute_count === 0 && verify_count === 0) return 'UNMEASURED';
    if (verify_count === 0) return 'UNKNOWN';       // ← not in Rust
    if (verify_count < 2) return 'CAUTION';
    // ... same bands as Rust from here
})();
```

**Divergence:** TS has UNMEASURED + UNKNOWN; Rust only has Unmeasured. TS counts via `cost_ns > 0` not `StepType` enum.

### Version 3: arifOS Python φFQ (CONSUMER — F1 floor)

**File:** `/root/arifOS/arifosmcp/runtime/rest_routes/rest_routes.py` (line 1028)

```python
# phiFQ mapping — maps FQ quotient to [0,1] for floor F1
if 1.0 <= _fq_quotient <= 3.0:
    _phi_fq = 1.0          # fully healthy
elif 0.5 <= _fq_quotient < 1.0:
    _phi_fq = _fq_quotient / 3.0  # degraded
elif _fq_quotient < 0.5:
    _phi_fq = 0.0          # dead
else:  # quotient > 3.0
    _phi_fq = min(1.0, 3.0 / _fq_quotient)  # damp (overheat)
```

**Divergence from Rust:** φFQ penalizes FQ>3 (overheat), but Rust verdict treats FQ=47 same as FQ=1.5 (both OPTIMAL). φFQ=0.064 when FQ=47 — "almost dead" — while Rust says "OPTIMAL."

### Version 4: Calhoun Anti-Sink Gate

**File:** `/root/arifOS/arifosmcp/runtime/calhoun_anti_sink_gate.py` (line 56)

```python
FQ_OVERHEAT_THRESHOLD = 3.0   # FQ > 3.0 for 3+ cycles = grooming
FQ_WINDOW = 3                 # last 3 samples
```

**Divergence:** Has overheat detection (FQ>3.0 sustained) that Rust compute() never triggers.

### Version 5: Kabarkan FQ Alerts

**File:** `/root/arifFlow/src/governance/kabarkan_fq.rs`

```rust
// FQ < 1.0 → WARNING ("Watching")
// FQ < 0.5 → CRITICAL ("Stuck")
// recovered → RECOVERED
```

**Divergence:** References `FlowVerdict::Watching` and `FqAlertSeverity::Critical`, but `compute()` never produces Watching. Kabarkan's thresholds assume Watching exists — it doesn't.

## Live Evidence (2026-08-14 14:00 MYT)

```json
{
  "fq": {
    "execute_count": 2,
    "quotient": 47.0,
    "verdict": "OPTIMAL",
    "verify_count": 94
  }
}
```

| Component | Verdict on FQ=47 |
|---|---|
| Rust compute() | OPTIMAL (q ≥ 1.0) |
| Python φFQ | 0.064 — nearly dead |
| Calhoun gate | OVERHEAT (q > 3.0 for 3+ cycles) |
| Kabarkan | Should fire WARNING but enum never assigned |

**Four systems, four verdicts on the same number.**

## Specific Inconsistencies

| # | Issue | Location |
|---|---|---|
| 1 | Dead enum variants: Watching, Overheat, Balanced never produced | Rust `receipt.rs` FlowVerdict |
| 2 | FQ=47 = OPTIMAL in Rust but φFQ=0.064 in Python | Rust vs Python |
| 3 | TS has UNMEASURED+UNKNOWN; Rust has only Unmeasured | TS `fq.ts` vs Rust `receipt.rs` |
| 4 | Kabarkan references Watching which compute() never assigns | `kabarkan_fq.rs` vs `receipt.rs` |
| 5 | High-FQ penalty (overheat) exists in φFQ + Calhoun but not in compute() | Rust compute() |
| 6 | STUCK vs BURNING naming inverted (q<0.1 = "burning" = execute-dominated) | Rust verdict bands |

## Recommendation

1. **Rust compute()** needs high-FQ bands: q>3.0 → OVERHEAT
2. **Dead enum variants** (Watching/Overheat/Balanced) — implement or remove
3. **TS sync** — align state machine with Rust (remove UNKNOWN, use cost_ns consistently)
4. **φFQ bands** — must match Rust verdicts, not ad-hoc thresholds
5. **Calhoun thresholds** — inherit from Rust constants, not hardcoded
6. **FQ frame metadata** — every quotient needs window + sample_size + formula_version
