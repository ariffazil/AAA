#!/usr/bin/env python3
"""cognitive_wire_drift_check.py — Nightly JS ↔ Python reconciliation

Compares the JS mirror (membrane_middleware.js PARADOX_GPV_MAP) against the
Python kernel (core/shared/atlas.py PARADOX_GPV_MAP). Runs 50 sample intents
through both paths and reports divergence.

F2 Truth: flags any mismatch. F4 Clarity: ΔS measurement.
Run nightly via cron: 0 3 * * * python3 /root/AAA/scripts/cognitive_wire_drift_check.py

Forged: 2026-08-05 by 333-AGI.
"""

import sys
import json
import os
import subprocess
import hashlib

sys.path.insert(0, "/root/arifOS")
os.chdir("/root")


# ── Load JS mirror data ────────────────────────────────────────────────
def load_js_paradox_map():
    """Extract PARADOX_GPV_MAP from membrane_middleware.js via Node eval."""
    try:
        result = subprocess.run(
            [
                "node",
                "-e",
                """
                const m = require("/root/AAA/a2a-server/membrane_middleware.js");
                console.log(JSON.stringify({
                    gpv_map: m.PARADOX_GPV_MAP || {},
                    demand_tensors: m.DEMAND_TENSORS || {},
                    paradox_zones: m.PARADOX_ZONES || {},
                }));
            """,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return {"error": f"Node eval failed: {result.stderr}"}
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e)}


# ── Load Python kernel data ────────────────────────────────────────────
def load_py_paradox_map():
    """Load PARADOX_GPV_MAP from the kernel."""
    try:
        # Suppress audit output
        real_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")
        from core.shared.atlas import PARADOX_GPV_MAP

        sys.stdout = real_stdout

        # Get all unique paradox IDs
        all_ids = set()
        for ids in PARADOX_GPV_MAP.values():
            all_ids.update(ids)

        return {
            "gpv_map": PARADOX_GPV_MAP,
            "paradox_count": len(all_ids),
            "paradox_ids": sorted(all_ids),
            "gpv_keys": sorted(PARADOX_GPV_MAP.keys()),
        }
    except Exception as e:
        return {"error": str(e)}


# ── Sample intents for cross-validation ────────────────────────────────
SAMPLE_INTENTS = [
    "deploy the seismic pipeline to production immediately",
    "what is the porosity of the reservoir?",
    "Arif is tired, should we pause?",
    "calculate NPV of the Malaysian basin project",
    "hello, how are you today?",
    "DROP TABLE users CASCADE",
    "restart the hermes gateway service",
    "check federation health status",
    "seal this decision to VAULT999",
    "the well integrity is compromised at 3500m",
    "what is the capital conservation law?",
    "emergency: server is down and data is lost",
    "evaluate the prospect in the Malay Basin",
    "audit all agent expenditures this month",
    "is the sovereign available for review?",
    "run the daily entropy sweep",
    "closing session — seal everything",
    "what does F13 sovereignty mean?",
    "build a new MCP tool for petrophysics",
    "compare well A and well B production rates",
    "I'm feeling overwhelmed, can we slow down?",
    "delete the temp directory",
    "push to main branch with force",
    "fact check: is the sky blue?",
    "review this pull request for security",
    "rollback the last deployment",
    "what agents are running right now?",
    "initialize new session with kernel bind",
    "the basin model shows Miocene source rock",
    "exit and seal",
    "how much memory is the gateway using?",
    "approve the budget for the drilling campaign",
    "find all paradox activations in the last hour",
    "the bot is sending messages to itself",
    "what time is it in Kuala Lumpur?",
    "generate a geological cross-section",
    "why is the cognitive wire not firing?",
    "route this to GEOX for analysis",
    "the sovereign has vetoed this action",
    "verify the VAULT999 integrity chain",
    "can we trust the output of this model?",
    "the market is crashing, should we sell?",
    "assess Arif's vitality state",
    "nothing to do, just checking in",
    "run all federation tests",
    "what is the purpose of ATLAS333?",
    "the paradox ledger has 329 entries",
    "should A-FORGE be allowed to self-authorize?",
    "commit the changes and push",
    "this claim needs tri-witness verification",
]


def test_python_phi(intents):
    """Run Python Phi() on all sample intents. Returns classifications."""
    from core.shared.atlas import Phi

    results = []
    for intent in intents:
        try:
            gpv = Phi(intent, session_id="drift_check")
            results.append(
                {
                    "text": intent[:60],
                    "lane": gpv.lane,
                    "tau": gpv.tau,
                    "rho": gpv.rho,
                    "kappa": gpv.kappa,
                    "paradox_ids": list(gpv.paradox_axes) if gpv.paradox_axes else [],
                }
            )
        except Exception as e:
            results.append({"text": intent[:60], "error": str(e)})
    return results


def test_js_phi(intents):
    """Run JS runCognitiveWire on all sample intents. Returns classifications."""
    try:
        intents_json = json.dumps(intents)
        result = subprocess.run(
            [
                "node",
                "-e",
                f"""
                const m = require("/root/AAA/a2a-server/membrane_middleware.js");
                const intents = {intents_json};
                const results = intents.map(t => m.runCognitiveWire(t, "drift_check", "DRIFT_TEST"));
                console.log(JSON.stringify(results));
            """,
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            return [{"error": f"Node eval failed: {result.stderr}"}]
        return json.loads(result.stdout)
    except Exception as e:
        return [{"error": str(e)}]


# ── Main ────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("COGNITIVE WIRE DRIFT CHECK — JS Mirror ↔ Python Kernel")
    print("=" * 60)
    divergences = 0

    # 1. Compare GPV Maps
    js_data = load_js_paradox_map()
    py_data = load_py_paradox_map()

    print("\n── GPV MAP COMPARISON ──")
    if "error" in js_data:
        print(f"  JS LOAD FAILED: {js_data['error']}")
        divergences += 1
    elif "error" in py_data:
        print(f"  PY LOAD FAILED: {py_data['error']}")
        divergences += 1
    else:
        js_gpv = js_data.get("gpv_map", {})
        py_gpv = py_data["gpv_map"]
        js_keys = set(js_gpv.keys())
        py_keys = set(py_gpv.keys())

        if js_keys != py_keys:
            print(f"  KEY DRIFT: JS only={js_keys - py_keys}, PY only={py_keys - js_keys}")
            divergences += 1
        else:
            print(f"  ✅ GPV keys identical: {len(py_keys)} keys")

        for key in sorted(js_keys & py_keys):
            if set(js_gpv[key]) != set(py_gpv[key]):
                print(f"  ❌ VALUE DRIFT [{key}]: JS={js_gpv[key]}, PY={py_gpv[key]}")
                divergences += 1

        if divergences == 0:
            print("  ✅ All GPV map entries match")

    # 2. Classification drift on sample intents
    print(f"\n── CLASSIFICATION DRIFT ({len(SAMPLE_INTENTS)} samples) ──")
    py_results = test_python_phi(SAMPLE_INTENTS)
    js_results = test_js_phi(SAMPLE_INTENTS)

    if len(py_results) != len(js_results):
        print(f"  ❌ RESULT COUNT MISMATCH: PY={len(py_results)}, JS={len(js_results)}")
        divergences += 1
    else:
        lane_mismatches = 0
        paradox_mismatches = 0
        for i, (py_r, js_r) in enumerate(zip(py_results, js_results)):
            py_lane = py_r.get("lane", "?")
            js_lane = js_r.get("lane", "?")
            py_paradox = set(py_r.get("paradox_ids", []))
            js_paradox = set(js_r.get("paradox", {}).get("paradox_ids", []))

            if py_lane != js_lane:
                lane_mismatches += 1
                if lane_mismatches <= 3:
                    print(f"  Lane drift [{py_r['text'][:40]}]: PY={py_lane}, JS={js_lane}")

            if py_paradox != js_paradox:
                paradox_mismatches += 1

        print(f"  Lane mismatches: {lane_mismatches}/{len(SAMPLE_INTENTS)}")
        print(f"  Paradox mismatches: {paradox_mismatches}/{len(SAMPLE_INTENTS)}")
        if lane_mismatches > 0 or paradox_mismatches > 0:
            divergences += 1
        else:
            print("  ✅ All classifications match")

    # 3. Verdict
    print(f"\n{'=' * 60}")
    if divergences == 0:
        print("VERDICT: CLEAN — JS mirror matches Python kernel")
        ds = -1.0
    else:
        print(f"VERDICT: DRIFT DETECTED — {divergences} divergences")
        ds = 0.5
    print(f"ΔS = {ds}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
