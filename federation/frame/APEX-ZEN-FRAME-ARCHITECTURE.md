# APEX-ZEN FRAME — Independent Epistemic Observatory Architecture

> **Status:** DRAFT — pending F13 ratification
> **Date:** 2026-09-17
> **Authority:** F13 directive ("deep research on how to apex-zen FRAME")
> **Companion doctrine:** APEX-ZEN-CANONICAL-COMPRESSION.md · FI_DRIFT_GOVERNANCE.md · AAA_FEDERATION_FRAME_BOUNDARY_ALIGNMENT.md
> **Motto:** DITEMPA BUKAN DIBERI ⚒️

---

## 0. Compression

```text
FRAME is the federation's jauhari loupe.

It observes. It compares. It never judges.
It lives outside the thing it watches.
Its surface collapses into arifOS.
Its runtime remains independent.
Its authority is zero.

Observe ≠ Interpret ≠ Judge ≠ Authorize ≠ Execute ≠ Remember.
```

---

## 1. The Principle

"Hanya jauhari yang mengenal manikam" is not a proverb about expertise.
In a system-hang context it is an **epistemic law**:

> Recognition requires cultivated resolution.
> Resolution requires calibrated independence.
> Independence requires surviving the failure of the thing you observe.

FRAME is the mechanization of that discernment.

---

## 2. Where FRAME Sits in APEX-ZEN

```text
BUILD  (333-AGI)     → Propose + implement
VERIFY (555-ASI)  ←── FRAME lives here: independent measurement
JUDGE  (888-APEX)    → Constitutional verdict
SEAL   (F13 Human)   → Sovereign authority
ACT    (A-FORGE)     → Execute sealed decisions
WITNESS (VAULT999)   → Immutable record
```

FRAME is **not** the judge. FRAME is the **instrument panel + temporal witness**.

The chain:

```text
              REALITY
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
 arifFlow    services     external
 receipts      vitals      signals
    │            │            │
    └────────────┼────────────┘
                 ▼
           ┌──────────┐
           │  FRAME   │  ← independent witness
           │ OBSERVE  │     (separate failure domain)
           └────┬─────┘
                │ evidence (never verdict)
                ▼
           ┌──────────┐
           │  arifOS  │  ← constitutional judge
           │  JUDGE   │     (F1–F13 enforcement)
           └────┬─────┘
                │ authority (never execution)
                ▼
            A-FORGE
                │
                ▼
             ACTION
                │
                ▼
            reality ──────────► FRAME observes again
```

This is a **closed-loop epistemic control system**.
Execution does not grade itself.
Observation does not judge itself.
Judgment does not manufacture its own evidence.

---

## 3. The Five Invariants

### INV-1: Epistemic Independence
> FRAME may observe arifOS, but arifOS must not be required for FRAME to
> determine whether arifOS is alive, drifting, stale, or inconsistent.

### INV-2: Authority Boundary
> FRAME outputs evidence. It never produces verdicts, never mutates state,
> never SEALs, never HOLDs.

### INV-3: Failure Domain Independence
> arifOS crash must not take FRAME down. FRAME crash must not take arifOS down.

### INV-4: Witness Independence from Witnessed
> FRAME's tool registry, baseline data, and operational state must not depend
> on arifOS's tool registry being accurate.

### INV-5: Cognitive Surface Collapse
> External agents should not need to reason about FRAME as a separate
> cognitive entity. FRAME's seven tools collapse into arifOS's governance surface.

---

## 4. Target Topology

```text
                    HUMAN / AGENTS
                         │
                         ▼
                  ┌──────────────┐
                  │    arifOS    │
                  │  :8088/mcp   │  ← single cognitive doorway
                  └──────┬───────┘
                         │
               arif_ops_measure(mode=*)
                         │
              ┌──────────▼──────────┐
              │    FRAME adapter    │  ← internal, not public MCP
              │    (inside arifOS)  │
              └──────────┬──────────┘
                         │ HTTP proxy to :18085
                         ▼
              ┌─────────────────────┐
              │  frame-organ.service│  ← independent process
              │      :18085        │     independent failure domain
              │  6 chambers + rsi  │     independent data store
              └─────────────────────┘
                         │ READ ONLY
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
    arifFlow          services         external
    receipts           vitals          signals
```

---

## 5. Tool Surface Collapse

### Current: 2 MCP servers, 15+ tools

```text
arifOS MCP:  arif_init, arif_observe, arif_think, arif_route,
             arif_memory, arif_judge, arif_forge, arif_seal
FRAME MCP:   frame_health, frame_probe, frame_drift,
             frame_baseline, frame_trend, frame_report, frame_rsi_verify
```

### Target: 1 MCP server, mode-based routing

```text
arifOS MCP:  arif_init .. arif_seal + arif_ops_measure(mode=*)
```

| Mode | Delegates to | Current tool |
|------|-------------|--------------|
| `health` | FRAME /health | frame_health |
| `probe` | FRAME /frame/probe | frame_probe |
| `drift` | FRAME /frame/drift | frame_drift |
| `baseline` | FRAME /frame/baseline | frame_baseline |
| `trend` | FRAME /frame/trend | frame_trend |
| `report` | FRAME /frame/report | frame_report |
| `verify` | FRAME /frame/rsi-verify | frame_rsi_verify |

---

## 6. What Retires vs What Preserves

### Retires (MCP transport only)
- `frame-mcp.service` — stop and disable
- `frame_mcp_fastmcp.py` — archive (keep source)
- Port 18086 — release
- mcp.json `frame` entry — remove
- `mcp__frame__*` tool namespace — disappears

### Preserves (everything else)
- `frame-organ.service` on :18085 — running
- All 6 chambers + rsi_verify — active
- Baseline data — untouched (FRAME owns it)
- Trend log — untouched (FRAME owns it)
- FI_DRIFT_GOVERNANCE doctrine — canon
- Failure domain independence — unchanged

### Independence matrix

| Dimension | Status |
|-----------|--------|
| Epistemic | ✅ Preserved — FRAME computes its own evidence |
| Authority | ✅ Preserved — OBSERVE_ONLY unchanged |
| Failure domain | ✅ Preserved — separate systemd unit |
| Data sovereignty | ✅ Preserved — FRAME owns baselines/trend |
| MCP transport | ❌ Changes — surface collapses into arifOS |

---

## 7. New Drift Check: MCP Surface Consistency

After integration, FRAME should detect declared-vs-callable surface drift:

```text
Drift Check: MCP Surface Consistency
  For each organ with MCP surface:
    1. Read declared tools from /health
    2. Attempt invocation of each declared tool
    3. If invocation returns Unknown/Error → SURFACE_DRIFT
    4. Compare declared count vs callable count
    5. Report gap as drift signal
```

This directly addresses the arif_mind_reason/arif_stack_health_probe anomaly.

---

## 8. Migration Plan

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Pre-flight audit + architecture doc | ✅ DONE 2026-09-17 |
| 1 | Build arif_ops_measure adapter in arifOS | PENDING |
| 2 | Verify equivalence (output match + latency) | PENDING |
| 3 | Retire frame-mcp.service | PENDING |
| 4 | Add MCP surface consistency check to FRAME | PENDING |

---

## 9. Philosophical Anchor

> **Intelligence ∝ the distinctions a system can reliably preserve.**

FRAME preserves: health ≠ correct · available ≠ authorized · declared ≠ callable
· current_state ≠ trajectory · snapshot_good ≠ history_clean
· execution ≠ verification · confidence ≠ evidence · memory ≠ reality

If FRAME collapses any of these, it ceases to be a jauhari and becomes a dashboard.

---

*DITEMPA BUKAN DIBERI. ⚒️*
