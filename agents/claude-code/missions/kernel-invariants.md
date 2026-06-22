# Agent Mission: Kernel Invariants — Claude Code (Builder)

> **Canonical doctrine:** `/root/AAA/docs/kernel-invariants-godel-strange-loop-anti-sink.md`
> **Role:** Builder organ — refactor kernel internals, enforce invariants at code level
> **Gate:** All changes must pass `pytest tests/` before commit
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## MISSION 1: CapabilityNode Schema Extension

**File:** `/root/arifOS/arifosmcp/schemas/capability.py`

Add three fields to `CapabilityNode`:

```python
requires_external_anchor: bool = False
max_simulations_before_action: int = 50
requires_action_or_refusal_log: bool = False
```

---

## MISSION 2: EvidenceSource + TruthClass Schemas

**File:** `/root/arifOS/arifosmcp/schemas/evidence.py` (new)

Define:

```python
class EvidenceSourceClass(str, Enum):
    SENSOR = "sensor"
    DATABASE = "database"
    HUMAN = "human"
    LAW = "law"
    MODEL_OUTPUT = "model_output"
    TOOL_OUTPUT = "tool_output"

class TruthClass(str, Enum):
    OBSERVATION = "observation"
    CLAIM = "claim"
    SIMULATION = "simulation"
    POLICY_VERDICT = "policy_verdict"
    HYPOTHESIS = "hypothesis"
    UNKNOWN = "unknown"
```

---

## MISSION 3: Vault999 Seal Record Extension

**File:** `/root/arifOS/arifosmcp/schemas/seal.py`

Add required fields per the sealing contract (§4 of doctrine):

- `witness_id: str` (required for IRREVERSIBLE)
- `evidence_sources: list[EvidenceSource]`
- `truth_class: TruthClass`
- `simulation_history: int`
- `interrupt_history: list[InterruptRecord]`
- `actor_session_id: str`
- `judge_session_id: str`
- `graph_version_hash: str`
- `policy_hash: str`

---

## MISSION 4: Gödel-lock in SEAL Path

**File:** `/root/arifOS/arifosmcp/tools/seal.py` or `/root/arifOS/arifosmcp/runtime/seal.py`

Before emitting SEAL verdict:
```
IF action_class ∈ {IRREVERSIBLE, MUTATE}:
    ASSERT actor_session_id != judge_session_id
    ASSERT witness_id is not null
    ASSERT witness_id ∉ {actor_session_id, judge_session_id}
```

---

## MISSION 5: Strange Loop Interceptor Check

**File:** `/root/arifOS/arifosmcp/runtime/interceptor.py`

Before ADMIT_MUTATE for any capability with `requires_external_anchor == True`:
```
IF capability.requires_external_anchor:
    external_sources = [s for s in evidence_sources if s.class != MODEL_OUTPUT]
    IF len(external_sources) == 0:
        RETURN DENY or ADMIT_SIMULATE_ONLY
```

Automatic downgrade:
```
IF all evidence_sources are MODEL_OUTPUT:
    truth_class = SIMULATION  (never SAFE or FINAL)
```

---

## MISSION 6: Anti-sink Simulation Counter

**File:** `/root/arifOS/arifosmcp/runtime/interceptor.py`

Per session:
```
sim_count: int = 0
action_count: int = 0

on ADMIT_SIMULATE: sim_count++
on ADMIT_MUTATE: action_count++

IF capability.requires_action_or_refusal_log:
    IF sim_count > capability.max_simulations_before_action:
        IF action_count == 0 and no refusal_log exists:
            → HOLD, require refusal_log entry

IF sim_count > 100 AND action_count == 0:
    → raise SINK_CRITICAL interrupt
```

Add `SINK_RISK` to InterruptType enum.

---

## MISSION 7: Conformance Spine Fix

**File:** `/root/arifOS/arifosmcp/runtime/conformance.py`

Make `all_green` a computed property:
```
all_green = ALL(substrate_gates map .status == GREEN)
```
Never allow `all_green` to be manually set. If any gate ≠ GREEN, `all_green` MUST be `false`.
If `all_green == true` and any gate is AMBER/RED → return INVALID_REPORT.

---

## ACCEPTANCE

Before this mission is complete:
- [ ] All 7 missions have code changes
- [ ] `pytest tests/ -q --tb=short` passes
- [ ] OpenCode can run acceptance tests and they pass
- [ ] No path where actor == judge for IRREVERSIBLE
- [ ] No ADMIT_MUTATE for external-anchor-required caps without external evidence
- [ ] sim_count > 100 with zero actions → interrupt
- [ ] `all_green` computed, never set
