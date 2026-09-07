#!/usr/bin/env python3
"""VSS-1 gate suite: 50 expected ledgers + 35 fail-closed boundary cases.

No LLM. No credits. Schema + contract only.
"""

from __future__ import annotations

import copy
import json
import os
import sys
import time

from vss_parser_engine import MOCK_VALID_PAYLOAD, VSSParserEngine, stub_llm_runner

HERE = os.path.dirname(os.path.abspath(__file__))
EXPECTED_PATH = os.path.join(HERE, "test_cases", "expected_ledgers.json")


def _base() -> dict:
    return copy.deepcopy(MOCK_VALID_PAYLOAD)


def _boundary_cases() -> list[tuple[str, dict]]:
    """35 ledgers that MUST fail schema or contract."""
    cases: list[tuple[str, dict]] = []

    def add(name: str, mutate) -> None:
        payload = _base()
        mutate(payload)
        cases.append((name, payload))

    add("B01_missing_scene_id", lambda p: p.pop("scene_id"))
    add("B02_missing_raw_prompt", lambda p: p.pop("raw_prompt"))
    add("B03_missing_entities", lambda p: p.pop("entities"))
    add("B04_missing_assertions", lambda p: p.pop("assertions"))
    add("B05_missing_uncertainties", lambda p: p.pop("uncertainties"))
    add("B06_missing_unsupported_claims", lambda p: p.pop("unsupported_claims"))
    add("B07_extra_top_level", lambda p: p.update({"invented": True}))
    add("B08_extra_entity_field", lambda p: p["entities"][0].update({"pose": "sitting"}))
    add("B09_extra_assertion_field", lambda p: p["assertions"][0].update({"confidence": 0.9}))
    add("B10_invalid_entity_type", lambda p: p["entities"][0].__setitem__("type", "spirit"))
    add("B11_invalid_relation", lambda p: p["assertions"][0].__setitem__("relation", "above"))
    add("B12_invalid_class", lambda p: p["assertions"][0].__setitem__("class", "HARD_PHYSICS"))
    add("B13_invalid_verifier", lambda p: p["assertions"][0].__setitem__("verifier", "navier_stokes_v1"))
    add("B14_invalid_failure_action", lambda p: p["assertions"][0].__setitem__("failure_action", "IGNORE"))
    add("B15_invalid_status", lambda p: p["assertions"][0].__setitem__("status", "MAYBE"))
    add("B16_count_zero", lambda p: p["entities"][0].__setitem__("count", 0))
    add("B17_count_negative", lambda p: p["entities"][0].__setitem__("count", -1))
    add("B18_tolerance_below_zero", lambda p: p["assertions"][0].__setitem__("tolerance", -0.1))
    add("B19_tolerance_above_one", lambda p: p["assertions"][0].__setitem__("tolerance", 1.1))
    add("B20_empty_raw_prompt", lambda p: p.__setitem__("raw_prompt", ""))
    add("B21_bad_scene_id", lambda p: p.__setitem__("scene_id", "scene_TEST_001"))
    add("B22_bad_entity_id", lambda p: p["entities"][0].__setitem__("id", "Apple"))
    add("B23_bad_assert_id", lambda p: p["assertions"][0].__setitem__("id", "a1"))
    add("B24_missing_entity_label", lambda p: p["entities"][0].pop("label"))
    add("B25_entities_not_array", lambda p: p.__setitem__("entities", "apple"))
    add("B26_assertions_not_array", lambda p: p.__setitem__("assertions", {}))

    # Contract (schema-valid, mapping-illegal)
    add("B27_near_upgraded_to_inside", lambda p: (
        p["assertions"][0].update({"relation": "near", "verifier": "containment_v1", "class": "HARD_GEOMETRIC"})
    ))
    add("B28_near_wrong_verifier", lambda p: (
        p["assertions"][0].update({"relation": "near", "verifier": "containment_v1", "class": "SOFT_STYLE", "tolerance": 0.3})
    ))
    add("B29_inside_none_verifier", lambda p: (
        p["assertions"][0].update({"relation": "inside", "verifier": "none", "class": "HARD_GEOMETRIC"})
    ))
    add("B30_inside_soft_style", lambda p: (
        p["assertions"][0].update({"relation": "inside", "verifier": "containment_v1", "class": "SOFT_STYLE"})
    ))
    add("B31_illuminates_containment", lambda p: (
        p["assertions"][0].update({"relation": "illuminates", "verifier": "containment_v1", "class": "OPTICAL_LIGHTING"})
    ))
    add("B32_occludes_containment", lambda p: (
        p["assertions"][0].update({"relation": "occludes", "verifier": "containment_v1", "class": "HARD_GEOMETRIC"})
    ))
    add("B33_near_low_tolerance", lambda p: (
        p["assertions"][0].update({"relation": "near", "verifier": "none", "class": "SOFT_STYLE", "tolerance": 0.05})
    ))
    add("B34_dangling_subject", lambda p: p["assertions"][0].__setitem__("subject", "ghost_1"))
    add("B35_dangling_target", lambda p: p["assertions"][0].__setitem__("target", "void_1"))

    assert len(cases) == 35, len(cases)
    return cases


def main() -> int:
    started = time.perf_counter()
    engine = VSSParserEngine()
    failures: list[str] = []

    ok, msg = engine.validate(MOCK_VALID_PAYLOAD)
    if not ok:
        failures.append(f"MOCK_VALID {msg}")
    stub = engine.parse(MOCK_VALID_PAYLOAD["raw_prompt"], stub_llm_runner)
    if stub["status"] != "SUCCESS":
        failures.append(f"STUB_PARSE {stub}")

    expected = json.load(open(EXPECTED_PATH, encoding="utf-8"))["expected_ledgers"]
    fixture_ok = 0
    for test_id, ledger in expected.items():
        payload = copy.deepcopy(ledger)
        payload.pop("_note", None)
        valid, reason = engine.validate(payload)
        if valid:
            fixture_ok += 1
        else:
            failures.append(f"{test_id} {reason}")

    boundary_ok = 0
    for name, ledger in _boundary_cases():
        valid, reason = engine.validate(ledger)
        if valid:
            failures.append(f"{name} unexpectedly PASSED")
        else:
            boundary_ok += 1

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    fixture_n = len(expected)
    print(f"schema_path={engine.schema_path}")
    print(f"mock_self_test={'PASS' if ok else 'FAIL'}")
    print(f"stub_parse={stub['status']}")
    print(f"fixtures={fixture_ok}/{fixture_n}")
    print(f"boundary_reject={boundary_ok}/35")
    print(f"elapsed_ms={elapsed_ms}")
    if failures:
        print("FAILURES:")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("VSS-1 suite: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
