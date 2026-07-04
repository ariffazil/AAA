# Agent Mission: Kernel Invariants — Claude Code (Builder)

> **Canonical doctrine:** `/root/AAA/docs/KERNEL_INVARIANTS.md`
> **Audit reference:** 2026-06-22 kernel audit — 16 gaps confirmed across 8 files
> **Role:** Builder organ — refactor kernel internals, enforce invariants at code level
> **Gate:** All changes must pass `pytest tests/ -q --tb=short` before commit
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## MISSION 1: CapabilityNode Schema Extension

**File:** `/root/arifOS/arifosmcp/kernel/models.py` (lines 115-186, `CapabilityNode` class)

Add three fields:

```python
requires_external_anchor: bool = False       # S1 — must have external evidence before MUTATE
max_simulations_before_action: int = 50      # A1 — anti-sink budget
requires_action_or_refusal_log: bool = False # A1 — force action or refusal
```

---

## MISSION 2: EvidenceSource + TruthClass + SinkThreshold Schemas

**File:** `/root/arifOS/arifosmcp/schemas/evidence.py` (NEW)

```python
class EvidenceSourceClass(str, Enum):
    SENSOR = "sensor"           # external: seismic, well log, DST
    DATABASE = "database"       # external: Supabase, Redis, Qdrant
    HUMAN = "human"             # external: Arif's input
    LAW = "law"                 # external: constitutional text, VAULT999 record
    MODEL_OUTPUT = "model_output"   # internal: LLM-generated
    TOOL_OUTPUT = "tool_output"     # depends: trace to origin

class TruthClass(str, Enum):
    OBSERVATION = "observation"
    CLAIM = "claim"
    SIMULATION = "simulation"
    POLICY_VERDICT = "policy_verdict"
    HYPOTHESIS = "hypothesis"
    UNKNOWN = "unknown"
```

**File:** `/root/arifOS/arifosmcp/kernel/models.py` (add after `GateVerdict` enum)

```python
class SinkThreshold(float, Enum):
    NORMAL = 0.1        # <10:1 sim/action
    ELEVATED = 0.02     # 10:1 to 50:1
    SINK_RISK = 0.01    # 50:1 to 100:1
    SINK_CRITICAL = 0.0 # >100:1 — HOLD

class InterruptType(str, Enum):
    # ... existing types ...
    SINK_RISK = "SINK_RISK"
    EXTERNAL_ANCHOR_MISSING = "EXTERNAL_ANCHOR_MISSING"
    SELF_CERTIFICATION = "SELF_CERTIFICATION"
```

---

## MISSION 3: Vault999 Seal Record Extension

**File:** `/root/arifOS/arifosmcp/schemas/verdict.py` (lines 892-1027, `SealOutput`)

Add to `SealOutput`:
- `witness_id: str | None = None` (required for IRREVERSIBLE, ~line 955)
- `evidence_sources: list[dict] = field(default_factory=list)` (~line 960)
- `truth_class: str = "UNKNOWN"` (~line 965)
- `simulation_history: int = 0` (~line 970)
- `interrupt_history: list[dict] = field(default_factory=list)` (~line 975)
- `actor_session_id: str = ""` (~line 980)
- `judge_session_id: str = ""` (~line 985)
- `graph_version_hash: str = ""` (~line 990)
- `policy_hash: str = ""` (~line 995)

**File:** `/root/arifOS/arifosmcp/schemas/lineage.py` (lines 12-29, `JudgeSealContract`)

Add `witness_id: str | None = None` to `JudgeSealContract`.

---

## MISSION 4: Gödel-lock — SEAL Path Enforcement

**File:** `/root/arifOS/arifosmcp/tools/judge.py` (line ~1149, inside the `vault_entry_id and is_seal` block)

Insert the Gödel-lock check BEFORE seal emission:

```python
# GÖDEL-LOCK (G1): No self-certification
if result.get("action_class") in ("IRREVERSIBLE", "MUTATE"):
    actor_sid = body.get("actor_id") or session_id
    judge_sid = session_id  # the current session is judging
    if actor_sid == judge_sid:
        return _hold(f"GÖDEL-LOCK: actor {actor_sid} cannot certify its own IRREVERSIBLE action. "
                      "Requires separate judge session.", "SELF_CERTIFICATION")

    # G2: witness required for IRREVERSIBLE
    witness_id = body.get("witness_id") or result.get("witness_id")
    if not witness_id:
        return _hold("GÖDEL-LOCK: IRREVERSIBLE seal requires non-null witness_id.",
                      "MISSING_WITNESS")
    if witness_id in (actor_sid, judge_sid):
        return _hold("GÖDEL-LOCK: witness cannot be actor or judge.",
                      "INVALID_WITNESS")
```

**File:** `/root/arifOS/arifosmcp/tools/forge.py` (line ~43, `arif_forge()` entry)

Verify `actor_id` ≠ judge identity at forge time.

---

## MISSION 5: Strange Loop — Interceptor External Anchor Check

**File:** `/root/arifOS/arifosmcp/kernel/interceptor.py` (lines 106-267, floor checks)

Add new floor check after F8:

```python
# FLOOR 9: EXTERNAL ANCHOR (Strange Loop — S1)
if capability.requires_external_anchor:
    evidence_sources = context.get("evidence_sources", [])
    external = [s for s in evidence_sources
                if s.get("class") not in ("model_output",)]
    if not external:
        context["_strange_loop_violation"] = True
        context["_downgraded_to"] = "SIMULATION"
        return InterceptorDecision(
            verdict=GateVerdict.ADMIT_SIMULATE,
            reason="STRANGE_LOOP: capability requires external anchor, none provided.",
            context=context,
        )
```

**File:** `/root/arifOS/arifosmcp/tools/judge.py` (line ~1046, the simulative detection gate)

Add automatic downgrade for internal-only evidence:

```python
# STRANGE LOOP (S3): Downgrade internal-only verdicts
evidence_sources = body.get("evidence_sources", [])
external = [s for s in evidence_sources
            if s.get("class") not in ("model_output",)]
if not external and result.get("truth_class") not in ("SIMULATION", "HYPOTHESIS"):
    result["truth_class"] = "SIMULATION"
    result["_downgraded"] = True
    result["_downgrade_reason"] = "STRANGE_LOOP: all evidence internal — verdict downgraded to SIMULATION"
```

---

## MISSION 6: Anti-sink — Session Simulation Counter

**File:** `/root/arifOS/arifosmcp/runtime/ingress_middleware.py` (line ~1021, before proceed path)

```python
# ANTI-SINK: Per-session simulation vs action tracking
_sink_counters: dict[str, dict] = {}  # module-level, keyed by session_id

def _track_action_class(session_id: str, verdict: GateVerdict, capability):
    """Track sim/action ratio per session for anti-sink enforcement."""
    if session_id not in _sink_counters:
        _sink_counters[session_id] = {"sim": 0, "action": 0, "refusals": []}

    c = _sink_counters[session_id]
    if verdict == GateVerdict.ADMIT_SIMULATE:
        c["sim"] += 1
    elif verdict in (GateVerdict.ADMIT_MUTATE, GateVerdict.ADMIT_EXECUTE):
        c["action"] += 1

    # A1: Capability budget exceeded
    if (capability.requires_action_or_refusal_log and
        c["sim"] > capability.max_simulations_before_action and
        c["action"] == 0 and
        len(c["refusals"]) == 0):
        return _hold(f"ANTI-SINK: {c['sim']} simulations with no action. "
                      "Capability requires action or refusal log.",
                      "SINK_RISK")

    # A2: SINK_CRITICAL threshold
    if c["sim"] > 100 and c["action"] == 0:
        return _hold(f"ANTI-SINK: SINK_CRITICAL — {c['sim']} sims, 0 actions. "
                      "System held until action or refusal log.",
                      "SINK_CRITICAL")

    return None  # proceed
```

---

## MISSION 7: Conformance Spine — all_green as Blocking Gate

**File:** `/root/arifOS/arifosmcp/transport/conformance_spine.py` (line ~742, after `all_green` computation)

```python
# G3: all_green MUST be derived from substrate gates
all_green = all(g.status == "GREEN" for g in substrate_gates)
# NEVER allow manual override. This is a computed property.

# G3 enforcement: block if all_green is true but any gate isn't GREEN
if all_green and any(g.status != "GREEN" for g in substrate_gates):
    return {"verdict": "INVALID_REPORT",
            "reason": "GÖDEL-LOCK: all_green contradicts gate statuses",
            "gates": {g.name: g.status for g in substrate_gates}}

# A3: all_green + zero actions = constitutional contradiction
if all_green and session_action_count == 0:
    return {"verdict": "CONSTITUTIONAL_CONTRADICTION",
            "reason": "ANTI-SINK: all gates GREEN but zero actions — sterile system",
            "gates": {g.name: g.status for g in substrate_gates}}
```

---

## ACCEPTANCE

Before this mission is complete:
- [ ] All 7 missions have code changes at the exact file paths above
- [ ] `pytest tests/ -q --tb=short` passes (in `/root/arifOS/`)
- [ ] OpenCode's acceptance tests pass against the modified kernel
- [ ] No path where `actor_session_id == judge_session_id` for IRREVERSIBLE
- [ ] No ADMIT_MUTATE for `requires_external_anchor` caps without external evidence
- [ ] `sim_count > 100` with zero actions → SINK_CRITICAL interrupt
- [ ] `all_green == true` when any gate ≠ GREEN → INVALID_REPORT
- [ ] `all_green == true` with zero actions → CONSTITUTIONAL_CONTRADICTION

---

*Updated 2026-06-22 — file paths corrected against kernel audit (16 gaps, 8 files).*
*DITEMPA BUKAN DIBERI — Forged, Not Given.*
