#!/usr/bin/env python3
"""
Reproduce known arifOS envelope contradiction classes against live :8088.

Run:  python3 scripts/probe_kernel_contradictions.py

Checks (see frontier-model-audit-verification SKILL.md §3 for the full class table):
  1. Actor identity fork: arif-fazil → arif in standing.claimed_id
  2. Confidence 0.65 fallback on unknown actor
  3. entropy_dS mode: does delta_S appear in payload?
  4. arif_judge on empty evidence: 0.65 or HOLD?
  5. constitutional_check vs outer verdict dual-truth
  6. Weight table serialization in payload
"""

import json, sys, urllib.request

BASE = "http://127.0.0.1:8088/mcp"
SESSION = "contradiction_probe"
RESULTS: dict[str, dict] = {}


def call(tool: str, args: dict, rid: int = 1) -> dict:
    body = {
        "jsonrpc": "2.0",
        "id": rid,
        "method": "tools/call",
        "params": {"name": tool, "arguments": args},
    }
    req = urllib.request.Request(
        BASE,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode()
    # MCP streamable may be SSE or direct JSON
    lines = [l for l in raw.splitlines() if l.startswith("data:")]
    text = lines[-1][5:].strip() if lines else raw
    outer = json.loads(text)
    txt = outer.get("result", {}).get("content", [{}])[0].get("text", "")
    return json.loads(txt) if txt else outer.get("result", {})


def check(name: str, passed: bool, detail: str):
    status = "✅ PASS" if passed else "❌ FAIL"
    RESULTS[name] = {"passed": passed, "detail": detail}
    print(f"  {status}  {name}")
    if not passed:
        print(f"    → {detail}")


print("=" * 60)
print("arifOS Envelope Contradiction Probe")
print("=" * 60)

# --- Test 1: Actor identity fork ---
print("\n[1] Actor identity fork (arif-fazil vs standing.claimed_id)")
r = call("arif_init", {"mode": "init", "actor_id": "arif-fazil"})
top_actor = r.get("actor_id")
standing_actor = (r.get("standing") or {}).get("actor", {})
claimed = standing_actor.get("claimed_id")
check(
    "actor_fork",
    top_actor == claimed,
    f"top.actor_id={top_actor!r} ≠ standing.actor.claimed_id={claimed!r}",
)

# --- Test 2: Confidence fallback ---
print("\n[2] Confidence fallback (should be None/UNMEASURED, not 0.65)")
r2 = call("arif_observe", {
    "subject": "confidence_test",
    "frame": "no real evidence provided",
    "session_id": SESSION,
})
conf = r2.get("confidence")
cc = r2.get("constitutional_check", {})
band = (r2.get("metacognition") or {}).get("confidence_band", "")
check(
    "confidence_not_fake",
    conf is None or band == "UNMEASURED",
    f"confidence={conf!r}, band={band!r} (expected None + UNMEASURED)",
)

# --- Test 3: entropy_dS missing delta_S ---
print("\n[3] entropy_dS mode emits delta_S")
r3 = call("arif_observe", {
    "subject": "entropy_test",
    "frame": "deliberately contradictory: both verified and unverified; vault both empty and full",
    "mode": "entropy_dS",
    "session_id": SESSION,
})
has_delta_s = "delta_S" in r3
check(
    "entropy_delta_s_present",
    has_delta_s,
    f"delta_S field {'present' if has_delta_s else 'ABSENT from payload'}",
)

# --- Test 4: judge empty evidence ---
print("\n[4] arif_judge on empty evidence (should HOLD, not 0.65)")
r4 = call("arif_judge", {
    "claim": "this is a test claim with no evidence",
    "evidence": {},
    "session_id": SESSION,
})
conf4 = r4.get("confidence")
rr4 = r4.get("raw_response")
check(
    "judge_empty_evidence_holds",
    rr4 is not None and rr4 != "None",
    f"raw_response={rr4!r}, confidence={conf4!r} (expected rejection, not 0.65)",
)

# --- Test 5: dual-truth check ---
print("\n[5] constitutional_check vs outer verdict consistency")
r5 = call("arif_observe", {
    "subject": "dual_truth_test",
    "frame": "test payload for dual truth",
    "session_id": SESSION,
})
outer_verdict = r5.get("verdict")
cc_floor = (r5.get("constitutional_check") or {}).get("floor_passed")
cc_hold = (r5.get("constitutional_check") or {}).get("hold_required")
derivation = (r5.get("constitutional_check") or {}).get("_derivation")
check(
    "dual_truth_consistent",
    (outer_verdict in ("SEAL", "PROCEED") and cc_floor is True and cc_hold is False)
    or (outer_verdict == "HOLD" and cc_hold is True),
    f"verdict={outer_verdict!r}, cc.floor_passed={cc_floor!r}, "
    f"cc.hold_required={cc_hold!r}, derivation={derivation!r}",
)

# --- Test 6: Weight tables ---
print("\n[6] Weight table serialization (SUBSTRATE_WEIGHT in payload)")
has_weights = "SUBSTRATE_WEIGHT" in r5
check(
    "no_weight_tables",
    not has_weights,
    f"SUBSTRATE_WEIGHT {'present in payload (token rent!)' if has_weights else 'not present (clean)'}",
)

# --- Summary ---
print("\n" + "=" * 60)
fails = [k for k, v in RESULTS.items() if not v["passed"]]
if fails:
    print(f"RESULT: {len(fails)} FAILURES")
    for f in fails:
        print(f"  ❌ {f}: {RESULTS[f]['detail']}")
    sys.exit(1)
else:
    print("RESULT: ALL PASS")
    sys.exit(0)