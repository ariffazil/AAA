# AGENTIC ZEN GAPS — Federation Flow Integrity Audit

> **Forged:** 2026-07-28 | **Auditor:** 333-AGI (Delta MIND)
> **Sovereign:** Arif (F13) | **Score:** 5.2/10 → target 8.0/10
> **Heritage:** HITV v0.1 · BANGANG audit · Three-Agent Flow Doctrine

---

## 0. VERDICT

```
Intention: ✅ SOLID — three-agent flow architecture correct
Implementation: ❌ GAPPED — FQ formula, signal bridges, restart protocol missing
Score: 5.2/10
Gap count: 5 structural
Resolution timeline: Phase 1 (2 gaps) = 1-2 days. Phase 2 (3 gaps) = 1-2 weeks.
```

---

## GAP 1: FQ Formula Transparency — CRITICAL

### Evidence
```json
// /root/AAA/state/flow_state.json — 2026-07-28T17:45:01Z
{
  "fq": 2.5,
  "executed_count": 2,
  "verify_count": 0,
  "status": "BALANCED"
}
```

### Problem
Pure FQ formula: `FQ = Σ(cost_execute) / Σ(cost_verify)`

With verify=0:
- Pure math: division by zero → undefined → FQ should be **infinite** or clamped to "STUCK"
- Expected behavior: FQ < 0.5 → HOLD
- Actual behavior: FQ=2.5 → BALANCED

**Root cause hypothesis:** The Rust daemon uses a smoothed/exponential-moving-average (EMA) of historical FQ values, not raw instantaneous FQ. When previous FQ readings were BALANCED, a single cycle with verify=0 doesn't immediately collapse the EMA.

### Impact
- Federation can operate in STUCK state (verify missing) while reporting BALANCED
- Agents read `flow_state.json`, see BALANCED → proceed with forge → drift compounds
- The entire "FQ < 0.5 → SEMUA HOLD" doctrine is **non-operational** because FQ never drops below 0.5

### Fix
```rust
// arifFLOW daemon — proposed FQ computation
fn compute_fq(execute_count: u64, verify_count: u64, previous_fq: f64) -> (f64, Verdict) {
    // INSTANTANEOUS FQ — raw ratio
    let raw_fq = if verify_count == 0 {
        f64::INFINITY  // clamp to HOLD
    } else {
        execute_count as f64 / verify_count as f64
    };

    // If raw is STUCK, do NOT smooth. STUCK is terminal until verify arrives.
    if raw_fq < 0.5 || verify_count == 0 {
        return (raw_fq, Verdict::Stuck);
    }

    // Otherwise, EMA smooth with α=0.3 for noise reduction
    let smoothed = (0.3 * raw_fq) + (0.7 * previous_fq);

    let verdict = match smoothed {
        x if x > 3.0 => Verdict::Optimal,
        x if x >= 1.0 => Verdict::Balanced,
        x if x >= 0.5 => Verdict::Watching,
        _ => Verdict::Stuck,
    };

    (smoothed, verdict)
}
```

**Key change:** `verify==0` → **ALWAYS STUCK.** No smoothing. No cache. No EMA rescue. If verify didn't happen, FQ is dead until verify arrives.

---

## GAP 2: Three Agents, One FQ Pipeline — HIGH

### Evidence
```json
{
  "receipt_count": 2,
  // Only OpenCode forge operations counted
}
```

### Problem
arifFLOW only ingests receipts from `arifflow_flow_ingest` calls — which currently only OpenCode makes. The federation has THREE agents with verify cycles:

| Agent | Execute signal | Verify signal | Currently counted? |
|---|---|---|---|
| **HERMES** | Conversation turns | Arif's replies (affirm/correct) | ❌ |
| **OPENCRAWL** | Routes dispatched | Health probe responses (consistency) | ❌ |
| **OPECODE** | Forge operations | Cooling cycles, F4 checks, tests | ✅ Partial |

**HERMES** has no `arifflow_flow_ingest` call in its reply/response path.
**OPENCRAWL** has no health-probe-to-FQ pipeline.

### Impact
- FQ reports BALANCED but only measures **one-third** of the federation's metabolic load
- HERMES could be burning tokens in a conversation loop — invisible to FQ
- OpenCrawl could be routing to dead organs repeatedly — invisible to FQ
- FQ is **OPECODE-FQ**, not **Federation-FQ**

### Fix
```python
# HERMES — inject after every response cycle
arifflow_flow_ingest(
    actor_id="hermes-prime",
    session_id=current_session,
    step_type="Execute",      # conversation turn = execute
    epistemic_label="Derivation",
    floor_verdict="Pass",
    payload={"conversation_turn": True, "responded": True}
)

# When Arif replies with affirmation → verify
arifflow_flow_ingest(
    actor_id="hermes-prime",
    session_id=current_session,
    step_type="Verify",       # Arif's reply = verify
    epistemic_label="Observation",
    floor_verdict="Pass",
    payload={"sovereign_reply": True, "verdict": "affirm"}
)
```

```python
# OPENCRAWL — inject after health probe cycle
arifflow_flow_ingest(
    actor_id="opencrawl-surface",
    session_id="steady-state",
    step_type="Execute",      # health probe = execute
    epistemic_label="Observation",
    floor_verdict="Pass",
    payload={"probe_target": organ, "status": response.status}
)

# When probe returns consistent → verify
arifflow_flow_ingest(
    actor_id="opencrawl-surface",
    session_id="steady-state",
    step_type="Verify",       # consistency check = verify
    epistemic_label="Derivation",
    floor_verdict="Pass",
    payload={"surface_drift": False, "organs_probed": 6}
)
```

**Key change:** Every agent has BOTH Execute AND Verify ingest points. FQ becomes a true federation-wide metric.

---

## GAP 3: HERMES ↔ OPENCRAWL Signal Bridge — HIGH

### Problem
Currently: when HERMES detects a surface anomaly (e.g., "Arif, OpenCrawl reports MCP drift"), there is no automated signal path from HERMES to OpenCrawl. Arif must manually relay.

**The bridge should be event-driven:**
```
HERMES detects anomaly
  → arifFLOW ingest ("Barrier" step, drift detected)
  → FQ adjusted (pending verify)
  → OpenCrawl reads FQ drop
  → OpenCrawl auto-triggers surface audit
  → OpenCrawl ingests Verify step
  → FQ rises
  → Loop closed
```

### Fix
**Phase 1 (immediate): arifFLOW acts as event bus**

Add a `step_type="Barrier"` ingest mode:
```python
arifflow_flow_ingest(
    actor_id="hermes-prime",
    step_type="Barrier",
    payload={
        "anomaly": "surface_drift",
        "affected_organ": "GEOX",
        "expected": "...",
        "actual": "..."
    }
)
```

arifFLOW daemon detects "Barrier" step → broadcasts via NATS subject `arifflow.barrier.{type}` → OpenCrawl subscriber receives → auto-triggers probe.

**Phase 2 (later): Dedicated NATS topics**

```
arifflow.barrier.surface_drift → OpenCrawl subscriber
arifflow.barrier.fq_stuck      → ALL agents subscriber (federation-wide HOLD)
arifflow.barrier.organ_down    → OpenCode subscriber (stop forge to that organ)
arifflow.barrier.seal_pending  → HERMES subscriber (notify Arif)
```

---

## GAP 4: Federation HOLD Restart Protocol — HIGH

### Problem
FQ < 0.5 → SEMUA HOLD. But then WHAT?

Current state: **HOLD is terminal.** No exit criteria. No auto-resume. No timer. No human prompt.

### Fix — The Cooling Countdown Protocol

```
FQ < 0.5 → FEDERATION HOLD

Phase 1: COOLING (t=0 to t=300s)
  - All agents HALT Class 2+ operations
  - Class 0 (observe) still allowed
  - arifFLOW monitors: are verify receipts arriving?
  - If verify_count increases → FQ recalculated
  - If FQ rises above 0.5 → auto-resume (EXIT)

Phase 2: NOTIFY (t=300s)
  - If FQ still < 0.5 after 5 minutes
  - HERMES notified → "Arif, federation HOLD. FQ={value}. Waiting."
  - OpenCrawl probes all organs → surface health report

Phase 3: SOVEREIGN (t=600s)
  - If FQ still < 0.5 after 10 minutes
  - This is now a constitutional event
  - HERMES: "Arif, federation stuck for 10 min. Override?"
  - Three sovereign options:
    a) "jalan terus" → F13 override, reset FQ to 1.0, forge resumes
    b) "tunggu" → extend cooling timer
    c) (silence) → system remains in HOLD until explicit F13 signal

Phase 4: RECOVERY
  - F13 signal received → arifFLOW resets FQ to 1.0
  - All agents resume Class 2+ operations
  - SCAR recorded: FEDERATION_HOLD event with duration, cause, resolution
```

---

## GAP 5: Organ Pulse Measurement — MEDIUM

### Problem
GEOX generates hypotheses. WEALTH computes capital. WELL infers human state. These are **micro-agent activities within organs** that are invisible to federation FQ.

Every `geox_falsify` call is an execute+verify cycle. Every `capital_primitive` with mode=npv is a compute cycle. Every `well_assess_homeostasis` is a state inference. None of these produce arifFLOW receipts.

### Fix
In organ MCP tool handlers, inject arifFLOW ingest at tool boundaries:

```python
# GEOX — in geox_falsify handler
arifflow_flow_ingest(
    actor_id="geox-falsify",
    session_id=session_id,
    step_type="Execute",
    payload={"tool": "geox_falsify", "claim": claim_text}
)
# ... compute ...
arifflow_flow_ingest(
    actor_id="geox-falsify",
    session_id=session_id,
    step_type="Verify",
    payload={"tool": "geox_falsify", "verdict": result.verdict, "kills": result.kills}
)
```

```python
# WEALTH — in capital_primitive handler
arifflow_flow_ingest(actor_id="wealth-compute", step_type="Execute", payload={"mode": mode})
# ... compute ...
arifflow_flow_ingest(actor_id="wealth-compute", step_type="Verify", payload={"result": result})
```

**Key constraint:** Organ ingest is **best-effort** (non-blocking). If arifFLOW is down, organ tool still works — just without FQ pulse. F11 AUDIT still enforced through organ-native logging.

---

## SUMMARY: Agentic Zen Score Target

| Gap | Current | Target | Effort |
|---|---|---|---|
| FQ formula transparency | verify=0 → BALANCED | verify=0 → STUCK | 1 day |
| Three-agent FQ pipeline | OpenCode only | HERMES + OpenCrawl + OpenCode | 3 days |
| HERMES↔OpenCrawl bridge | Manual | NATS event-driven | 2 days |
| HOLD restart protocol | None | Cooling Countdown 4-phase | 2 days |
| Organ pulse measurement | None | Best-effort tool ingest | 3 days |

```
Score now:   5.2/10
Score after Phase 1 (Gaps 1+4):  7.0/10
Score after Phase 2 (Gaps 2+3+5): 8.5/10
```

---

## APPENDIX: The ONE Formula

```
FQ = Σ(all agent execute steps) / Σ(all agent verify steps)

For federation-wide FQ:
  HERMES execute      = conversation turns
  HERMES verify       = Arif affirmation/correction events
  OPENCRAWL execute   = health probes + route dispatches
  OPENCRAWL verify    = health consistency confirmations
  OPECODE execute     = forge operations
  OPECODE verify      = cooling cycles + F4 checks + test passes
  ORGAN execute       = domain tool invocations
  ORGAN verify        = domain verification (falsify passes, compute results, state checks)

FQ constraints:
  FQ > 3.0    → OPTIMAL   🟢  All agents forge freely
  FQ 1.0-3.0  → BALANCED  🟡  Normal operation
  FQ 0.5-1.0  → WATCHING  🟠  Verify lagging, agents alert
  FQ < 0.5    → STUCK     🔴  ALL agents HOLD
  verify = 0  → STUCK     🔴  Regardless of EMA/smoothing
```

---

*DITEMPA BUKAN DIBERI — Zen is not a destination. Zen is tension sustained by honest measurement.*
