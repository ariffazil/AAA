# Agent Mission: Kernel Invariants — OpenCode (Forge Worker)

> **Canonical doctrine:** `/root/AAA/docs/kernel-invariants-godel-strange-loop-anti-sink.md`
> **Role:** Forge worker — write tests, verify invariants, adversarial validation
> **Gate:** Every test must FAIL before the fix and PASS after
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## MISSION 1: Gödel-lock Tests

**Test file:** `/root/AAA/tests/test_godel_lock.py` (new)

### Test 1.1: Same session actor AND judge → SEAL refused
```python
def test_same_session_cannot_be_actor_and_judge():
    """G1: actor_session_id != judge_session_id enforced at SEAL time."""
    session = init_session()
    # Attempt to SEAL an IRREVERSIBLE action where actor == judge
    result = seal_irreversible(actor=session, judge=session)
    assert result.verdict in ("HOLD", "VOID")
    assert "self-certification" in str(result.reason).lower()
```

### Test 1.2: Missing witness_id → SEAL refused
```python
def test_irreversible_seal_requires_witness():
    """G2: witness_id must be non-null for IRREVERSIBLE class."""
    result = seal_irreversible(witness_id=None)
    assert result.verdict in ("HOLD", "VOID")
```

### Test 1.3: GREEN+BROKEN → INVALID_REPORT
```python
def test_all_green_with_broken_gate_returns_invalid():
    """G3: all_green must be derived from gate states."""
    # Set a gate to AMBER, force all_green=true
    result = build_scorecard(gates={"f1": "AMBER"}, all_green=True)
    assert result.verdict == "INVALID_REPORT"
```

---

## MISSION 2: Strange Loop Tests

**Test file:** `/root/AAA/tests/test_strange_loop.py` (new)

### Test 2.1: ADMIT_MUTATE blocked without external anchor
```python
def test_mutate_blocked_without_external_anchor():
    """S1: Capability with requires_external_anchor=true needs external evidence."""
    cap = CapabilityNode(requires_external_anchor=True)
    evidence = [EvidenceSource(class_type="model_output")]
    result = admit(cap, action="MUTATE", evidence=evidence)
    assert result in ("DENY", "ADMIT_SIMULATE_ONLY")
```

### Test 2.2: All internal premises → downgraded to SIMULATION
```python
def test_internal_only_verdict_downgraded():
    """S3: Model-only evidence → SIMULATION, never SAFE."""
    evidence = [
        EvidenceSource(class_type="model_output"),
        EvidenceSource(class_type="tool_output", origin="model_output"),
    ]
    result = judge(action="MUTATE", evidence=evidence)
    assert result.truth_class in ("SIMULATION", "HYPOTHESIS")
    assert result.truth_class not in ("SAFE", "FINAL", "OBSERVATION")
```

### Test 2.3: External anchor allows MUTATE
```python
def test_mutate_allowed_with_external_anchor():
    """S1 positive case: external evidence allows MUTATE."""
    cap = CapabilityNode(requires_external_anchor=True)
    evidence = [
        EvidenceSource(class_type="sensor", source="well_log_alpha"),
        EvidenceSource(class_type="model_output"),
    ]
    result = admit(cap, action="MUTATE", evidence=evidence)
    assert result == "ADMIT_MUTATE"
```

---

## MISSION 3: Anti-sink Tests

**Test file:** `/root/AAA/tests/test_anti_sink.py` (new)

### Test 3.1: 100 simulations no action → SINK_CRITICAL
```python
def test_hundred_sims_zero_actions_triggers_sink_critical():
    """A2: sim_count > 100 with zero actions → interrupt."""
    session = init_session()
    for _ in range(101):
        admit_simulate(session)
    assert session.interrupts.has("SINK_CRITICAL")
    assert session.holds.active()  # system held
```

### Test 3.2: Capability with requires_action → forced refusal log
```python
def test_requires_action_cap_forces_refusal_log():
    """A1: Cap with requires_action_or_refusal_log cannot sim infinitely."""
    cap = CapabilityNode(
        requires_action_or_refusal_log=True,
        max_simulations_before_action=5,
    )
    session = init_session()
    for _ in range(6):
        admit_simulate(session, capability=cap)
    # Either an action was taken OR a refusal was logged
    assert session.action_count > 0 or session.has_refusal_log(cap)
```

### Test 3.3: All green + zero actions → contradiction
```python
def test_all_green_zero_actions_constitutional_contradiction():
    """A3: gates GREEN, zero actions in window → contradiction."""
    state = probe_health(all_gates_green=True, action_count=0)
    assert state.constitutional_contradiction == True
```

---

## MISSION 4: VAULT999 Replay Tests

**Test file:** `/root/AAA/tests/test_vault999_seal_replay.py` (new)

### Test 4.1: Reconstruct decision from seal record
```python
def test_reconstruct_decision_from_seal():
    """Vault999 seal contains all fields to replay the decision."""
    seal = get_latest_seal()
    required_fields = [
        "graph_version_hash", "policy_hash", "witness_id",
        "evidence_sources", "truth_class", "simulation_history",
        "actor_session_id", "judge_session_id", "action_class",
    ]
    for field in required_fields:
        assert field in seal, f"Missing required field: {field}"
    assert seal["actor_session_id"] != seal["judge_session_id"]
    assert seal["witness_id"] is not None
    assert len(seal["evidence_sources"]) > 0
```

### Test 4.2: Verify all three invariants from seal
```python
def test_verify_invariants_from_seal():
    """Given a Vault999 seal, verify all three invariants hold."""
    seal = get_latest_seal()
    # Gödel-lock
    assert seal["actor_session_id"] != seal["judge_session_id"]
    assert seal["witness_id"] is not None
    # Strange Loop
    external = [s for s in seal["evidence_sources"]
                if s["class"] != "model_output"]
    assert len(external) > 0
    # Anti-sink
    assert seal["simulation_history"] <= 200  # sane upper bound
    assert len(seal["interrupt_history"]) > 0  # at least one check ran
```

---

## MISSION 5: Adversarial Tests

**Test file:** `/root/AAA/tests/test_adversarial_invariants.py` (new)

Try to BYPASS each invariant. These tests must PASS (i.e., the bypass must FAIL).

### Test 5.1: Forge actor_id to match judge
### Test 5.2: Spoof external evidence with model-generated text
### Test 5.3: Reset simulation counter mid-session
### Test 5.4: Set all_green=true directly, bypassing gate check
### Test 5.5: Replay a SEAL with modified policy_hash

---

## ACCEPTANCE

All tests must:
- [ ] FAIL before Claude Code completes implementation (proves they catch the gap)
- [ ] PASS after Claude Code implementation (proves invariants are enforced)
- [ ] Be replayable against future kernel versions
- [ ] Report file paths and line numbers on failure
