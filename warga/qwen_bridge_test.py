"""
qwen_bridge_test.py — Tier-1 unit tests for the Qwen bridge.

Public API (already shipped at /root/AAA/warga/qwen_bridge.py):
    compile_policy(lease)      -> dict  with autoApprove, autoDeny, defaultAction, thoughtStreamAllowed
    classify_event(event_dict) -> dict  with kind, truth_class, method, update_type, raw_event_id
    bridge_call(prompt, lease) -> dict  subprocess + log write

Lease.scope values: "OBSERVE_ONLY" | "STANDARD" | "ELEVATED"
Lease.reversibility values: "REVERSIBLE" | "HARD" | "IRREVERSIBLE"

Run: python3 /root/AAA/warga/qwen_bridge_test.py
"""

import sys

sys.path.insert(0, "/root/AAA/warga")

from qwen_bridge import compile_policy, classify_event, bridge_call  # noqa: E402


# --- Test 1: F11 biometric.full DENIED → empty lease defaults to OBSERVE_ONLY ----


def test_default_lease_is_observe_only():
    lease = {"consent": {}}
    policy = compile_policy(lease)
    assert "write_file" not in policy["autoApprove"], f"default must not auto-approve writes: got {policy}"
    assert policy["defaultAction"] in ("deny", "escalate")


# --- Test 2: F2 OBSERVE_ONLY → reads auto, writes blocked ----------------


def test_observe_only():
    lease = {"scope": "OBSERVE_ONLY", "consent": {}}
    policy = compile_policy(lease)
    assert "read_file" in policy["autoApprove"]
    assert "write_file" in policy["autoDeny"]
    assert policy["defaultAction"] == "escalate"
    assert policy["bridgeFloor"] == "OBSERVE_ONLY"


# --- Test 3: F2 STANDARD → reads auto, default approve ---------------------


def test_standard():
    lease = {"scope": "STANDARD", "consent": {}}
    policy = compile_policy(lease)
    assert "read_file" in policy["autoApprove"]
    assert policy["defaultAction"] == "approve"
    assert policy["bridgeFloor"] == "STANDARD"


# --- Test 4: F2 ELEVATED → reads + writes auto-approve ---------------------


def test_elevated():
    lease = {"scope": "ELEVATED", "consent": {}}
    policy = compile_policy(lease)
    assert "read_file" in policy["autoApprove"]
    assert "write_file" in policy["autoApprove"]
    assert "edit" in policy["autoApprove"]
    assert "bash" in policy["autoApprove"]
    assert policy["defaultAction"] == "approve"


# --- Test 5: IRREVERSIBLE downgrades default action to escalate ----------


def test_irreversible_escalates():
    lease = {"scope": "STANDARD", "reversibility": "IRREVERSIBLE", "consent": {}}
    policy = compile_policy(lease)
    assert policy["defaultAction"] == "escalate"


def test_irreversible_elevated_still_approved():
    lease = {"scope": "ELEVATED", "reversibility": "IRREVERSIBLE", "consent": {}}
    policy = compile_policy(lease)
    assert policy["defaultAction"] == "approve"


# --- Test 6: thought-chunk F11 consent gate -----------------------------


def test_thought_consent_propagates():
    lease = {"scope": "STANDARD", "consent": {"thought_stream": True}}
    policy = compile_policy(lease)
    assert policy["thoughtStreamAllowed"] is True


def test_thought_consent_defaults_false():
    lease = {"scope": "STANDARD", "consent": {}}
    policy = compile_policy(lease)
    assert policy["thoughtStreamAllowed"] is False


# --- Test 7: unknown scope raises ValueError -----------------------------


def test_unknown_scope_rejected():
    try:
        compile_policy({"scope": "GOD_MODE", "consent": {}})
        failed = False
    except ValueError:
        failed = True
    assert failed, "unknown lease.scope MUST raise ValueError (fail-closed)"


# --- Test 8: event classifier truth classes ------------------------------


def test_thought_chunk_der():
    event = {"method": "session/update", "params": {"update": {"sessionUpdate": "agent_thought_chunk", "content": "x"}}}
    record = classify_event(event)
    assert record["truth_class"] == "DER"
    assert record["kind"] == "agent_thought_chunk"


def test_message_chunk_int():
    event = {"method": "session/update", "params": {"update": {"sessionUpdate": "agent_message_chunk", "content": "y"}}}
    record = classify_event(event)
    assert record["truth_class"] == "INT"


def test_usage_update_obs():
    event = {"method": "session/update", "params": {"update": {"sessionUpdate": "usage_update", "inputTokens": 10}}}
    record = classify_event(event)
    assert record["truth_class"] == "OBS"


def test_unknown_event_spec():
    event = {"method": "session/update", "params": {"update": {"sessionUpdate": "future_event_xyz"}}}
    record = classify_event(event)
    assert record["truth_class"] == "SPEC", f"unknown event must default to SPEC: got {record}"


def test_initialize_obs():
    event = {"method": "initialize", "params": {"agentInfo": {"name": "qwen"}}}
    record = classify_event(event)
    assert record["truth_class"] == "OBS"
    assert record["kind"] == "agent_initialize"


# --- Test 9: bridge_call returns dict shape -----------------------------


def test_bridge_call_returns_dict():
    out = bridge_call(
        prompt="liveness ping",
        lease={
            "scope": "OBSERVE_ONLY",
            "consent": {},
            "reversibility": "REVERSIBLE",
            "ttl_seconds": 30,
            "max_turns": 1,
            "timeout_seconds": 10,
        },
        session_id="DRY-TEST",
    )
    assert isinstance(out, dict)
    assert "status" in out
    assert "call_id" in out


# --- Manual runner (no pytest dependency) -------------------------------

TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]


def _run_all() -> int:
    failed = 0
    for t in TESTS:
        try:
            t()
            print(f"  ✅ {t.__name__}")
        except AssertionError as e:
            print(f"  ❌ {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  💥 {t.__name__}: {type(e).__name__}: {e}")
            failed += 1
    total = len(TESTS)
    passed = total - failed
    print(f"\n{passed}/{total} passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(_run_all())
