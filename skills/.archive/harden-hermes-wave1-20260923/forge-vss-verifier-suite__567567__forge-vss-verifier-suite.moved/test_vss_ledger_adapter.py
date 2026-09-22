#!/usr/bin/env python3
"""VSS-2 reads VSS-1 ledgers. No VLM. No credits."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARSER = Path("/root/AAA/skills/forge-vss-parser")
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(PARSER))

from vss_ledger_adapter import project_ledger  # noqa: E402
from vss_parser_engine import MOCK_VALID_PAYLOAD  # noqa: E402

EXPECTED = json.loads((PARSER / "test_cases" / "expected_ledgers.json").read_text())


def main() -> int:
    failures: list[str] = []
    ledgers = EXPECTED["expected_ledgers"]

    ok_n = 0
    for test_id, ledger in ledgers.items():
        payload = copy.deepcopy(ledger)
        payload.pop("_note", None)
        result = project_ledger(payload)
        if not result.get("ok"):
            failures.append(f"{test_id} {result}")
            continue
        work = result["work_order"]
        if "raw_prompt" in json.dumps(work):
            failures.append(f"{test_id} prompt leaked into work_order")
            continue
        if work.get("f9_prompt_stripped") is not True:
            failures.append(f"{test_id} missing F9 strip flag")
            continue
        ok_n += 1

    # Specific projections
    cat = project_ledger(ledgers["test_002"])
    contain = cat["work_order"]["containments"]
    if not any(c["relation"] == "inside" and c["subject"] == "cat" for c in contain):
        failures.append(f"test_002 missing cat-inside-box: {contain}")

    birds = project_ledger(ledgers["test_005"])
    if birds["work_order"]["counts"].get("birds") != 3:
        failures.append(f"test_005 counts={birds['work_order']['counts']}")

    near = project_ledger(ledgers["test_011"])
    if near["work_order"]["routed"]["count_containment"]:
        failures.append("test_011 near must not route to containment")
    if not near["work_order"]["unrouted"]:
        failures.append("test_011 near must stay unrouted (verifier=none)")

    lamp = project_ledger(ledgers["test_029"])
    if not lamp["work_order"]["routed"]["shadow_light"]:
        failures.append("test_029 candle illuminates must route to shadow_light")
    if lamp["work_order"]["light_source_count"] < 1:
        failures.append("test_029 missing light_source_count")

    # Invalid ledger rejected
    bad = project_ledger({"scene_id": "nope"})
    if bad.get("ok"):
        failures.append("invalid ledger unexpectedly accepted")

    mock = project_ledger(MOCK_VALID_PAYLOAD)
    if not mock.get("ok"):
        failures.append(f"mock ledger rejected: {mock}")
    elif "raw_prompt" in json.dumps(mock["work_order"]):
        failures.append("mock work_order leaked raw_prompt")

    from forge_vss_verifier_suite import run_verifier_suite

    rejected = run_verifier_suite("/nonexistent.png", assertions={"scene_id": "nope"})
    if rejected.get("overall_verdict") != "ERROR":
        failures.append(f"suite did not fail-closed on bad ledger: {rejected.get('overall_verdict')}")
    if rejected.get("error_code") not in {"E_SCHEMA_INVALID", "E_CONTRACT_INVALID", "E_LEDGER_NOT_OBJECT"}:
        failures.append(f"suite missing ingest error_code: {rejected}")

    print(f"ledgers_projected={ok_n}/{len(ledgers)}")
    if failures:
        print("FAILURES:")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("VSS-2 ledger-read: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
