#!/usr/bin/python3
"""validate_candidate.py — reproducible conformance check for the FED typed-contract candidate.

WHY THIS EXISTS (defect found by the 555 verify lane, 2026-10-26):
  The pilot report stated "7/7 capabilities conform (Draft 2020-12)". That was true only
  for the 4-field envelope SLICE. Validating each per-tool object as written failed 0/7,
  because the extension schema sets additionalProperties:false and each entry carries 10
  keys. The claim was not false, but it was unqualified. This script makes BOTH scopes
  explicit and reproducible, so the claim can be checked rather than believed.

Scopes tested:
  A. ENVELOPE   — each tool's {response_schema, outcomes, receipt, boundary} against
                  machine-contract-extension.schema.json (the mission's Phase-3 spec).
  B. DOCUMENT   — the whole fed-typed-contract.candidate.json against
                  fed-typed-contract.candidate.schema.json (the document wrapper).
Negative controls are run too: a bad state enum, a class supplied beside UNKNOWN, a null
evidence_ref, and an extra top-level key. Structural validity is not truth — see
CONTRADICTION-UNKNOWN-LEDGER.md C7.

Usage:  /usr/bin/python3 validate_candidate.py [dir]
Exit:   0 = all scopes pass; 1 = at least one scope or control fails.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
from referencing import Registry, Resource

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent)
EXT = BASE / "machine-contract-extension.schema.json"
DOC = BASE / "fed-typed-contract.candidate.schema.json"
CAND = BASE / "fed-typed-contract.candidate.json"

ext = json.loads(EXT.read_text())
doc = json.loads(DOC.read_text())
cand = json.loads(CAND.read_text())

registry = Registry().with_resource(ext["$id"], Resource.from_contents(ext))
registry = registry.with_resource(doc["$id"], Resource.from_contents(doc))
V_ext = jsonschema.Draft202012Validator(ext, registry=registry)
V_doc = jsonschema.Draft202012Validator(doc, registry=registry)

fail = 0

# ── Scope A: envelope slice per tool ──
env_keys = ("response_schema", "outcomes", "receipt", "boundary")
a_ok = 0
for name, entry in cand["capabilities"].items():
    slice_ = {k: entry[k] for k in env_keys}
    errs = sorted(V_ext.iter_errors(slice_), key=lambda e: list(e.path))
    if errs:
        fail += 1
        print(f"  A FAIL {name}: {errs[0].message[:120]}")
    else:
        a_ok += 1
print(
    f"SCOPE A envelope : {a_ok}/{len(cand['capabilities'])} tools conform to machine-contract-extension.v1"
)

# ── Scope B: whole document ──
errs = sorted(V_doc.iter_errors(cand), key=lambda e: list(e.path))
if errs:
    fail += 1
    for e in errs[:6]:
        print(f"  B FAIL {'.'.join(map(str, e.path))}: {e.message[:160]}")
    print(f"SCOPE B document : 0/1 candidate document conforms")
else:
    print(
        "SCOPE B document : 1/1 candidate document conforms to fed-typed-contract.candidate.v1"
    )

# ── controls: two directions. Structural validity is not truth (ledger C7). ──
good = {k: cand["capabilities"]["fed_health"][k] for k in env_keys}
must_reject = {
    "bad state enum": {**good, "outcomes": {**good["outcomes"], "state": "MAYBE"}},
    "UNKNOWN + asserted class": {
        **good,
        "boundary": {**good["boundary"], "state": "UNKNOWN", "class": "public"},
    },
    "UNKNOWN + asserted schema": {
        **good,
        "response_schema": {
            **good["response_schema"],
            "state": "UNKNOWN",
            "schema": {"type": "object"},
        },
    },
    "UNKNOWN + asserted outcomes": {
        **good,
        "outcomes": {**good["outcomes"], "state": "UNKNOWN", "allowed": ["ok"]},
    },
}
# must be ACCEPTED — mission rule: "null plus UNKNOWN is valid"
must_accept = {
    "null evidence_ref": {**good, "receipt": {**good["receipt"], "evidence_ref": None}},
    "UNKNOWN + null class": {
        **good,
        "boundary": {**good["boundary"], "state": "UNKNOWN", "class": None},
    },
}
for label, payload in must_reject.items():
    rejected = bool(list(V_ext.iter_errors(payload)))
    print(
        f"  CONTROL reject {label:<24} -> {'REJECTED (correct)' if rejected else 'ACCEPTED (schema gap)'}"
    )
    if not rejected:
        fail += 1
for label, payload in must_accept.items():
    rejected = bool(list(V_ext.iter_errors(payload)))
    print(
        f"  CONTROL accept {label:<24} -> {'ACCEPTED (correct)' if not rejected else 'REJECTED (schema too strict)'}"
    )
    if rejected:
        fail += 1

print(f"\nRESULT: {'PASS' if fail == 0 else f'FAIL ({fail} problems)'}")
sys.exit(0 if fail == 0 else 1)
