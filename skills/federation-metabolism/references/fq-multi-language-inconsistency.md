# FQ Multi-Language Inconsistency Audit (2026-08-14)

## Source files and line numbers

### Rust SOURCE OF TRUTH
- `receipt.rs:307` — `FlowQuotient::compute()` — canonical formula
- `receipt.rs:39-82` — `StepType` enum (Execute, Verify, Cool, Seal, Barrier, Merge, Route)
- `receipt.rs:231-264` — `FlowVerdict` enum (9 variants, 3 dead)
- `invariants.rs:220-310` — `ActorFlowState` (per-actor FQ)
- `invariants.rs:340-345` — `FqThresholds` default config
- `invariants.rs:623-640` — `restricted_actors()` (uses deprecated fq field)
- `kabarkan_fq.rs` — alert enum references dead FlowVerdict values
- `main.rs:382-445` — `/health` endpoint (global scalar only, no per-actor)

### Python CONSUMERS
- `rest_routes.py:1028-1049` — φFQ computation (F1 AMANAH floor)
- `calhoun_anti_sink_gate.py:56-57` — FQ_OVERHEAT_THRESHOLD=3.0
- `resources.py:191-200` — flow-state MCP resource

### TypeScript MIRROR
- `arifflow/state/fq.ts` — `computeFQ()` — diverges from Rust

## The five versions compared

### 1. Rust compute() — verdict bands
```
verify_count == 0          → Unmeasured (quotient = None)
verify_count < 2           → Caution (quotient = None)
execute_count == 0         → Flowing (observe-only window)
q >= 1.0                   → Optimal
q >= 0.5                   → Flowing
q >= 0.1                   → Stuck
q < 0.1                    → Burning
```
NO high-FQ band. FQ=47 and FQ=1.5 are both "Optimal".

### 2. Python φFQ — different thresholds
```
FQ ∈ [1, 3]     → φFQ = 1.0
FQ ∈ [0.5, 1)   → φFQ = FQ/3.0
FQ < 0.5        → φFQ = 0.0
FQ > 3.0        → φFQ = min(1, 3.0/FQ)    ← Rust has no equivalent
```

### 3. TS fq.ts — divergent states
```
Has both UNMEASURED (both zero) AND UNKNOWN (verify zero)
Rust only has Unmeasured for both cases
Uses cost_ns > 0 as proxy for count, not StepType enum
```

### 4. Calhoun — hardcoded thresholds
```python
FQ_OVERHEAT_THRESHOLD = 3.0
FQ_WINDOW = 3
# Not inherited from Rust constants
```

### 5. Kabarkan — references dead enum
```rust
// kabarkan_fq.rs references FlowVerdict::Watching
// but compute() never assigns Watching
// FlowVerdict::Overheat and ::Balanced also never assigned
```

## Live FQ=47 case study

```
Live: quotient=47.0, verdict=OPTIMAL, verify=94, execute=2

Rust compute():  OPTIMAL (q≥1.0) — no overheat concept
Python φFQ:     0.064 (3/47) — nearly dead
Calhoun:        FQ>3.0 for 3+ cycles → grooming detected
Kabarkan:       should fire WARNING (FQ<1.0) but Watching enum never assigned
```

Three different opinions on the same number. Global FQ=47.0 also hides:
- 333-AGI: FQ=0.00 → HELD (stuck)
- Other actors with diverse per-actor FQ states

## Bug inventory

1. **Dead enum values** — FlowVerdict::Watching, ::Overheat, ::Balanced defined but never produced by compute()
2. **restricted_actors() uses deprecated fq** — comment says "Do NOT read self.fq" but restricted_actors() does exactly that
3. **No high-FQ verdict band** — q=47 and q=1.5 both OPTIMAL
4. **TS dual UNMEASURED states** — UNMEASURED + UNKNOWN, Rust only has Unmeasured
5. **TS uses cost_ns>0 not StepType** — proxy diverges from canonical counting
6. **Calhoun thresholds hardcoded** — not inherited from Rust constants
7. **No frame metadata** — quotient values lack window, sample_size, formula_version
8. **Per-actor vector invisible** — ActorFlowState computed but /health only exposes global + restricted

## Fix direction (unified FQ)

1. Rust compute() add high-FQ bands: q∈[1,3]=Optimal, q>3=Overheat
2. Implement or remove dead enum values
3. restricted_actors() → read state.quotient, not state.fq
4. TS sync exact with Rust (one UNMEASURED state, StepType-based counting)
5. φFQ Python bands match Rust verdict bands
6. Calhoun thresholds inherit from Rust FqThresholds
7. All FQ values carry frame metadata (window, sample_size, formula_version)
8. /health expose actors BTreeMap (per-actor FQ vector)
