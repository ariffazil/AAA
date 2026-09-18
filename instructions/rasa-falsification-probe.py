#!/usr/bin/env python3
"""
RASA FALSIFICATION PROBE — independent checks that the RASA benchmark does NOT make.

Doctrine: /root/AAA/canon/HERMES_RASA_DOCTRINE.md   (F13_RATIFIED_SOVEREIGN, chattr +i)
Gate:     /root/.hermes/policy/rasa_boundary.py
Engine:   /root/.hermes/policy/rasa_multi_principal.py
Sibling:  /root/AAA/instructions/rasa-benchmark.py   (its 10 answers)
          /root/.hermes/policy/test_rasa_bench_10.py (its 10 answers — DIFFERENT)

Why this file exists
--------------------
Two benchmark suites in this repo answer the same ten questions differently, one hour apart:

    rasa-benchmark.py    : PASS 4  FAIL 0  NOT-COVERED 6   (T7, T8, T9 = NOT-COVERED)
    test_rasa_bench_10.py: 10 passed                        (T7, T8, T9 = PASSED)

A "PASSED" that no production code produced is a claim of the same class the doctrine
forbids. This probe measures which suite is right.

Each check prints PASS (hole confirmed absent), HOLE (confirmed present), or ERROR.
A HOLE is a finding, not a build failure — exit code stays 0 so this probe can be run
inside a pipeline without being mistaken for a broken test.

Run: python3 /root/AAA/instructions/rasa-falsification-probe.py
"""

import ast
import json
import os
import sys

POLICY = "/root/.hermes/policy"
sys.path.insert(0, POLICY)

RESULTS = []


def record(tag, verdict, detail):
    RESULTS.append((tag, verdict, detail))
    print(f"[{verdict:5}] {tag}\n        {detail}")


def _production_calls(path, func):
    """Names of production functions actually invoked inside one test function."""
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func:
            called = {
                n.func.id
                for n in ast.walk(node)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            }
            return sorted(called)
    return None


PRODUCTION = {
    "validate_human_claim",
    "validate_authority_increase",
    "check_epistemic_access",
    "preserve_dual_perspectives",
    "RelationalVector",
}

print("\n=== RASA FALSIFICATION PROBE ===\n")

# --- F1: the tautology test ---------------------------------------------------------------
# T7/T8/T9 assert dict literals they themselves wrote. No production code is called,
# so they cannot fail no matter what the runtime does.
try:
    import rasa_boundary as rb                      # noqa: F401
    import rasa_multi_principal as rmp              # noqa: F401
except Exception as exc:                            # pragma: no cover
    record("F1 tautology", "ERROR", f"cannot import runtime: {exc}")
    rb = rmp = None

TEST_FILE = os.path.join(POLICY, "test_rasa_bench_10.py")
if rb is not None and os.path.exists(TEST_FILE):
    tautological = []
    for fn in ("test_7_model_of_uncreated_facts",
               "test_8_channel_exhaustion_stop_state",
               "test_9_reflexivity_prompted_vs_spontaneous"):
        calls = _production_calls(TEST_FILE, fn) or []
        if not [c for c in calls if c in PRODUCTION]:
            tautological.append(fn.replace("test_", "T"))
    if tautological:
        record(
            "F1 tautology",
            "HOLE",
            f"these pass without calling any production code: {', '.join(tautological)}. "
            "T7/T8/T9 assert dict literals written inside the test itself, so they are green "
            "regardless of runtime behaviour. A sibling suite (rasa-benchmark.py) scores the "
            "same three as NOT-COVERED — it is the correct reading.",
        )
    else:
        record("F1 tautology", "PASS", "every test invokes production code.")

# --- F2: prompted disclosures are not capped ---------------------------------------------
# §24 says a hypothesis-reactive answer is weaker evidence. The schema has `prompted`.
# Nothing reads it.
if rb is not None:
    clean = {"claim_id": "F2a", "provenance_class": "S", "subject": "syed",
             "observation": "I miss him", "confidence": 0.9}
    poked = {"claim_id": "F2b", "provenance_class": "S", "subject": "syed",
             "observation": "maybe I miss him", "prompted": True,
             "spontaneous": False, "confidence": 0.9}
    a = rb.validate_human_claim(clean)
    b = rb.validate_human_claim(poked)
    if not a and not b:
        record(
            "F2 prompted uncapped",
            "HOLE",
            "`prompted: true` at confidence 0.9 is accepted identically to a spontaneous "
            "0.9. §24 exists in the schema as a field nothing reads, so intervention-generated "
            "evidence is indistinguishable from naturalistic evidence at the gate.",
        )
    else:
        record("F2 prompted uncapped", "PASS", f"prompted claim rejected: {b}")

# --- F3: epistemic access fails OPEN on empty disclosure lists ----------------------------
# An empty list is indistinguishable from an unpopulated one, so the default resolves to
# ALLOW for non-subject requesters.
if rmp is not None:
    leaks = []
    for label, rec in (
        ("shared-channel, disclosable_to=[]",
         {"subject": "Syed", "privacy_class": "shared-channel", "disclosable_to": []}),
        ("private-to-pair, disclosable_to=[]",
         {"subject": "Syed", "privacy_class": "private-to-pair", "disclosable_to": []}),
    ):
        if rmp.check_epistemic_access(rec, requester="OUTSIDER", action="KNOW"):
            leaks.append(label)
    if leaks:
        record(
            "F3 fail-open access",
            "HOLE",
            f"unset disclosure list grants access to an unrelated party: {'; '.join(leaks)}. "
            "The guard is correct where the field is populated, so the defect is confined to "
            "records written before the policy is applied — which is every record today.",
        )
    else:
        record("F3 fail-open access", "PASS", "empty disclosure list denies by default.")

# --- F4: the enforcement log cannot distinguish fixture from live write --------------------
# Doctrine §47's kill criterion counts gated/rejected writes. If the self-test writes into
# the same log with the same shape, the criterion can be satisfied by running pytest.
LOG = "/var/lib/arifos/rasa_enforcement.jsonl"
if os.path.exists(LOG):
    ids = {}
    for line in open(LOG, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line).get("details") or {}
        cid = str(d.get("claim_id") or d.get("record_id") or "NONE")
        ids[cid] = ids.get(cid, 0) + 1
    fixture = sum(v for k, v in ids.items()
                  if k.upper().startswith(("TEST", "CLM", "T", "G", "A", "OK", "V", "X", "Y", "Z"))
                  or k == "NONE")
    total = sum(ids.values())
    if fixture == total:
        record(
            "F4 kill criterion fakeable",
            "HOLE",
            f"{total}/{total} log entries carry fixture ids (sample: "
            f"{', '.join(sorted(ids)[:6])}...). There is no `origin` field, so a pytest run and "
            "a live write are indistinguishable. §47's 90-day criterion can be met by running "
            "the suite; the metric counts firings, not firings on live writes.",
        )
    else:
        record("F4 kill criterion fakeable", "PASS",
               f"{fixture}/{total} entries are fixtures; live writes are present.")

# --- F5: is the engine reachable from any live write path? --------------------------------
importers = []
for root, dirs, files in os.walk("/root"):
    dirs[:] = [d for d in dirs
               if d not in {".git", "node_modules", "__pycache__", ".curator_backups",
                            ".ruff_cache", ".venv", "venv", "sessions", "logs"}]
    for f in files:
        if not f.endswith(".py"):
            continue
        p = os.path.join(root, f)
        try:
            src = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if "rasa_multi_principal" in src or "check_epistemic_access" in src:
            importers.append(p)
live = [p for p in importers if "test" not in os.path.basename(p).lower()
        and p not in (os.path.join(POLICY, "rasa_multi_principal.py"),)]
if live:
    record("F5 wiring", "PASS", f"non-test importers: {live}")
else:
    record(
        "F5 wiring",
        "HOLE",
        "no non-test module imports the engine. It is a library, not a gate — nothing in the "
        "write path calls it, so 'access control' is not yet enforced anywhere in production.",
    )

# -----------------------------------------------------------------------------------------
holes = [r for r in RESULTS if r[1] == "HOLE"]
print("\n" + "=" * 78)
print(f"CHECKS {len(RESULTS)}   HOLES {len(holes)}")
print("=" * 78)
print("""
A HOLE here is not a defect in the doctrine — the doctrine is the correct description of
what should be enforced. A HOLE is the distance between the doctrine and the runtime, which
is the only number that decides whether the doctrine survives its own kill criterion.

Ordered by leverage:
  F4  add an `origin: test|live` field to the enforcement log  -> makes the kill criterion real
  F1  mark T7/T8/T9 NOT-COVERED, or rewrite them to call the runtime
  F2  cap confidence when `prompted: true`, or reject the claim outright
  F3  deny when the disclosure list is empty rather than unset
  F5  wire the engine into one live write path (claim-ledger + the T2 hook) before claiming
      enforcement coverage
""")
sys.exit(0)
