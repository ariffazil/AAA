# Epistemic Repair Dossier — 2026-09-20

> Source: FI-007 (Grok) deep probe session. Verified against disk by FI-003 (Qwen Code).

## Three Root Causes

### Issue 1: Substrate ≠ Authority conflation

**File:** `arifosmcp/runtime/tools.py:3255-3350` (`_compute_scoped_verdicts`)

**Bug:** When `actor_cryptographically_verified=false`, session auth failure can cascade into `substrate.state=DEGRADED`. The derivation checks `_sub_out.get("state") == "DEGRADED"` without distinguishing WHY it's degraded.

**Impact:** `arif_init` returns `substrate=HEALTHY` while `arif_observe` returns `substrate=DEGRADED` — same actor, same session. Two code paths, two truths.

**Note (FI-003 verification):** The substrate derivation at lines 3296-3330 uses `issuer="arifos_conformance"` (not `session_capability_token`). The cascade happens through `_sub_out.get("state")` picking up session-related degradation from the `substrate` dict, not through issuer filtering.

### Issue 2: Memory audit dual path

**File:** `runtime/memory_handlers_v5.py:1450-1466`

**Bug:** Two audit code paths exist:
1. `tools/memory.py:1649` → calls `audit_governance()` directly (no `action.description` needed)
2. `memory_handlers_v5.py:1450` → requires `action.description` (hidden required field)

MCP schema routes through path 1, but some internal calls route through path 2.

### Issue 3: Think verify = threat classification, not evidence verification

**File:** `runtime/tools.py:15089-15101`

**Bug:** `arif_think(mode="verify")` runs `threat_engine.classify()` and returns VOID/SEAL based on threat tier. Does NOT consume evidence, populate `evidence_used`, or verify claims against evidence.

## Proposed Path: B → (D+C) → A

### M1 — REPAIR THE SPINE
Goal: one legitimate SEAL lands in VAULT999.
1. Reconcile source/built/deployed until `drift=false` ✅ DONE
2. Fix 14 ExecStart lines pointing at non-existent `/opt/arifos/venv`
3. Ed25519 bind → `actor_cryptographically_verified=true`
4. T3 boot-attestation seed + T6 verdict floor-guard

### M2 — CLOSE THE LOOP
- One emitter: every `forge_*` receipt carrying `expected_output` auto-writes WM trajectory + proxy observation
- Switch on CHRON verification cadence. Target: calibration non-null, ≥10 verified, inside 14 days
- Second independent witness so W3 stops being null
- Probe disagreement = logged CONTRADICTION

Exit test: ≥5 of 14 proxy pairs observed · trajectories ≥60 · calibration non-null · W3 computed at least once.

### M3 — THEN the ontology
VOID should be generated, not authored. After M2 the system can compute V = R − M from real unmeasured-scalar lists.

## Session State (at time of analysis)

| Surface | State |
|---------|-------|
| All services | ACTIVE (6/6) |
| Swap | RECOVERED (8GB free) |
| Frame drift | STABLE (0 drifts) |
| WEALTH registry | PASS (14/14 tools) |
| WEALTH tests | 788 passed, 26 failed (was 35) |
| G | 0.4631 |
| C_dark | 0.219 |
| W3 | null (never computed) |
| CHRON | 19 predictions, 1 verified, 0 lessons |
| Proxy-reality | 14 pairs registered, 0 observations |
| World model | 22/100 trajectories, 3 tools, avg surprise 0.77 |
| FQ | 2.50 (floor 0.5) |
| Governance receipts | 16,927 in 7 days |

## Key Insight

> You built a world-class measuring instrument and are feeding it almost nothing. The system is running hot and learning close to zero.
