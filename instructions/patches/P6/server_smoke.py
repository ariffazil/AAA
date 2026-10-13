"""
P6 smoke test against the patched server module — invokes the inlined
_p6_scan via import (no MCP, no network, no service restart).

This is what we run BEFORE restarting the live daemon: prove the inlined code
is correct. After this passes, the activation step restarts PID 1194 cleanly.
"""

import importlib.util
import json
import sys

spec = importlib.util.spec_from_file_location(
    "hermes_rasa_patched",
    "/root/HERMES/mcp/hermes-rasa/server.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# Hand-built fixture (identical to detector.fixture_eight_claims()).
CLAIMS = [
    {"id": "C1", "text": "Federal spending 2027 totals RM510 billion including statutory and PPP investment",
     "source": "mof.gov.my/belanjawan2027", "principal": "federal_budget_total",
     "geography": "MY", "kind": "REPORTED", "time": "2026-10-09"},
    {"id": "C2", "text": "Federal operating spending 2027 totals RM459.8 billion",
     "source": "Reuters world/asia-pacific 2026-10-09", "principal": "federal_budget_total",
     "geography": "MY", "kind": "REPORTED", "time": "2026-10-09"},
    {"id": "C3", "text": "PETRONAS dividend to federal government 2027 will be RM32 billion",
     "source": "mof fiscal outlook 2027", "principal": "petronas_dividend",
     "geography": "MY", "kind": "FORECAST", "time": "2026-10-09"},
    {"id": "C4", "text": "Petronas dividend to federal government 2027 estimated around RM25 billion",
     "source": "CIMB research The Edge 2026-10-07", "principal": "petronas_dividend",
     "geography": "MY", "kind": "FORECAST", "time": "2026-10-07"},
    {"id": "C5", "text": "2027 deficit target is 3.3 percent of GDP",
     "source": "mof budget speech 2027", "principal": "deficit_pct_gdp",
     "geography": "MY", "kind": "FORECAST", "time": "2026-10-09"},
    {"id": "C6", "text": "Deficit could remain at 3.6 percent of GDP in 2027",
     "source": "OCBC research Business Today 2026-09-25", "principal": "deficit_pct_gdp",
     "geography": "MY", "kind": "FORECAST", "time": "2026-09-25"},
    {"id": "C7", "text": "Government subsidies, aid and incentives for 2027 exceed RM80 billion including fuel subsidy about RM40 billion",
     "source": "mof budget speech 2027", "principal": "subsidy_total",
     "geography": "MY", "kind": "REPORTED", "time": "2026-10-09"},
    {"id": "C8", "text": "Subsidy spend falls marginally to RM72.7 billion in 2027",
     "source": "Reuters world/asia-pacific 2026-10-09", "principal": "subsidy_total",
     "geography": "MY", "kind": "REPORTED", "time": "2026-10-09"},
    {"id": "C9", "text": "Brent crude traded at about USD85 per barrel as the 2026 average assumption",
     "source": "mof fiscal outlook 2027", "principal": "oil_assumption",
     "geography": "MY", "kind": "FORECAST", "time": "2026-10-09"},
    {"id": "C10", "text": "Brent crude spot price USD101 per barrel reported on 11 September",
     "source": "The Star 2026-09-11", "principal": "oil_spot_observation",
     "geography": "MY", "kind": "REPORTED", "time": "2026-09-11"},
    {"id": "C11", "text": "Federal deficit 1H 2026 about 4.2 percent and well below targeted 3.5 percent",
     "source": "The Star column via Webull 2026-09-27", "principal": "deficit_pct_gdp",
     "geography": "MY", "kind": "REPORTED", "time": "2026-09-27"},
]

out = m.hermes_contradiction_scan(CLAIMS)
print("ok:", out["ok"])
print("count:", len(out["contradictions"]))
classes = {}
for r in out["contradictions"]:
    classes[r["class"]] = classes.get(r["class"], 0) + 1
print("classes:", json.dumps(classes))
subjects = {}
for r in out["contradictions"]:
    subjects[r["subject"]] = subjects.get(r["subject"], 0) + 1
print("subjects:", json.dumps(subjects))
print("first row id:", out["contradictions"][0]["contradiction_id"] if out["contradictions"] else "NONE")

# Negative controls.
assert out["ok"] is True
assert len(out["contradictions"]) >= 4, f"need >=4 contradictions, got {len(out['contradictions'])}"
classes_set = set(classes.keys())
must_have = {"SCOPE"}
missing = must_have - classes_set
assert not missing, f"missing class rows: {missing}"

# Cross-organ passage: limit clauses.
for r in out["contradictions"]:
    assert r["status"] in m._P6_STATUSES, f"illegal status: {r['status']}"
    assert r["class"] in m._P6_CLASSES, f"illegal class: {r['class']}"
    assert r.get("limitations") and isinstance(r["limitations"], list)

# No governance labels anywhere.
import json as _j
text = _j.dumps(out)
for forbid in ["SEAL\":","HOLD\":","ALLOW\":","VOID\":","DENY\":"]:
    assert forbid not in text, f"forbidden governance label leaked: {forbid}"
print("SMOKE-PASS")
