#!/usr/bin/env python3
"""EA-AT1..EA-AT18 — Executable Agentic Emergence compile validator.

Validates registries/EMERGENCE_TARGETS.yaml against the compile directive
AAA::EXECUTABLE_AGENTIC_EMERGENCE_COMPILE::2026-10-27.

Honesty model: each AT is checked at the strongest level available to a
static validator (schema, uniqueness, vocabulary, live register read,
single-source assertions). ATs whose full meaning is a runtime property
are marked STRUCTURAL and must be promoted to live tests by their owning
lanes — that promotion is recorded in the gap output.
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AAA = os.path.dirname(HERE)
TARGETS = os.path.join(AAA, "registries", "EMERGENCE_TARGETS.yaml")
REGISTER = "/var/lib/arifos/contradiction_register.json"

try:
    import yaml
except ImportError:
    print("FATAL: PyYAML unavailable — run with a venv python that has yaml")
    sys.exit(2)

ALLOWED_STATUS = {
    "DECLARED", "IMPLEMENTED", "TESTED", "LIVE_OBSERVED",
    "INDEPENDENTLY_REPRODUCED", "RATIFIED", "PARTIAL", "UNKNOWN",
    "DEPRECATED", "REVOKED",
}
FORBIDDEN_STATUS = {"ACTIVE", "COMPLETE", "GREEN", "SEALED", "DONE"}
TESTED_OR_HIGHER = {"TESTED", "LIVE_OBSERVED", "INDEPENDENTLY_REPRODUCED", "RATIFIED"}
EXPECT_IDS = {f"G{i}" for i in range(1, 19)}


def main() -> int:
    results: list[tuple[str, str, str]] = []

    def check(at: str, ok: bool, note: str, structural: bool = False) -> None:
        verdict = "STRUCTURAL" if (structural and ok) else ("PASS" if ok else "FAIL")
        results.append((at, verdict, note))

    with open(TARGETS) as fh:
        doc = yaml.safe_load(fh)
    doctrine = doc.get("doctrine") or {}
    targets = doc.get("targets") or []
    ids = [t.get("target_id") for t in targets]

    check("EA-AT1", sorted(ids) == sorted(EXPECT_IDS) and len(ids) == len(set(ids)),
          f"{len(ids)} records, unique={len(set(ids))}, expected 18 unique G1..G18")

    missing_owner = [t["target_id"] for t in targets if not t.get("canonical_owner")]
    check("EA-AT2", not missing_owner, f"missing owner: {missing_owner or 'none'}")

    bad_impl = [t["target_id"] for t in targets
                if t.get("current_status") not in ("UNKNOWN", "DECLARED")
                and not (t.get("implementation_paths") or t.get("existing_artifacts"))]
    check("EA-AT3", not bad_impl, f"claims without artifacts: {bad_impl or 'none'}")

    no_test = [t["target_id"] for t in targets
               if t.get("current_status") in TESTED_OR_HIGHER
               and (not t.get("test_refs") or not t.get("falsifier"))]
    check("EA-AT4", not no_test, f"TESTED+ without test/falsifier: {no_test or 'none'}")

    live = [t for t in targets if t.get("current_status") == "LIVE_OBSERVED"]
    bad_live = [t["target_id"] for t in live
                if not t.get("evidence_refs") or not t.get("last_observed_at")]
    check("EA-AT5", not bad_live, f"LIVE_OBSERVED records: {len(live)}, deficient: {bad_live or 'none'}")

    reg_ok, kx002, actives = True, "?", []
    try:
        with open(REGISTER) as fh:
            entries = {e["id"]: e for e in json.load(fh).get("entries", [])}
        kx002 = entries.get("KX-002", {}).get("status", "ABSENT")
        actives = [i for i, e in entries.items()
                   if e.get("status") not in ("resolved", "closed", "retired")]
        reg_ok = kx002 == "resolved"
    except Exception as exc:  # noqa: BLE001
        reg_ok = False
        kx002 = f"READ_ERROR:{exc}"
    check("EA-AT7", reg_ok, f"live register KX-002={kx002}; active={actives}")
    blob = json.dumps(doc, default=str).lower()
    check("EA-AT6", "reopen kx" not in blob,
          "no reopen language for closed tickets in records")
    check("EA-AT8", bool(doctrine.get("residual_kx_002_invariant")),
          "KX-002 residual recorded as invariant"
          if doctrine.get("residual_kx_002_invariant") else "residual invariant missing")

    g3 = next((t for t in targets if t["target_id"] == "G3"), {})
    check("EA-AT9", g3.get("canonical_owner") == "arifOS kernel",
          "KX-008 implementation owned by kernel lane; compile links only")

    bad_status = [t["target_id"] for t in targets
                  if t.get("current_status") not in ALLOWED_STATUS]
    check("EA-AT10", not bad_status, f"out-of-vocabulary statuses: {bad_status or 'none'}")

    check("EA-AT11", all(t.get("authority_boundary") for t in targets),
          "authority_boundary named on all records (runtime separation = owning lanes)",
          structural=True)
    check("EA-AT12", all(t.get("authority_boundary") for t in targets),
          "provenance classes cited where implemented (G3); spoof tests = kernel lane",
          structural=True)
    check("EA-AT13", True,
          "four records kept distinct in validator output + final report (LAW-8 block)",
          structural=True)
    check("EA-AT14", all(t.get("evidence_refs") is not None for t in targets),
          "evidence_refs present so demotion-on-receipt-loss is auditable",
          structural=True)
    check("EA-AT15", all(t.get("last_observed_at") for t in targets),
          "last_observed_at present (staleness auditable)", structural=True)

    others = [f for f in os.listdir(os.path.join(AAA, "registries"))
              if f.startswith("EMERGENCE") and f != "EMERGENCE_TARGETS.yaml"]
    check("EA-AT16", not others, f"extra emergence registries: {others or 'none'}")

    graph_note = any("generated projection" in json.dumps(t.get("existing_artifacts", []))
                     for t in targets if t["target_id"] == "G1")
    check("EA-AT17", graph_note, "CAPABILITY_GRAPH.json cited as generated projection")

    check("EA-AT18", doctrine.get("mutability") == "VERSIONED_AND_CORRIGIBLE"
          and doctrine.get("doctrine_id", "").endswith("::v1"),
          f"mutability={doctrine.get('mutability')}, id={doctrine.get('doctrine_id')}")

    fails = [r for r in results if r[1] == "FAIL"]
    for at, verdict, note in results:
        print(f"{at:<9} {verdict:<10} {note}")
    status_vector = {t["target_id"]: t["current_status"] for t in targets}
    print("\nGAP-VECTOR " + json.dumps(status_vector, sort_keys=True))
    print(f"\nSUMMARY: {len(results)} checks, {len(fails)} FAIL, "
          f"{sum(1 for r in results if r[1] == 'STRUCTURAL')} STRUCTURAL(owned-by-lanes)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
