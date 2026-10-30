#!/usr/bin/env python3
"""test_fixtures.py — RSR v0 Phase 1 seven mandatory fixtures + acceptance tests.

Runs against shadow_capture.py only. No production gate touched, no CHRON write,
no organ call. Executes the replay the review directive required BEFORE soak.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shadow_capture import ShadowCapture  # noqa: E402

RESULTS = []


def check(name: str, cond: bool, detail: str = ""):
    RESULTS.append((name, cond, detail))
    print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def fresh_store():
    d = tempfile.mkdtemp(prefix="rsr-shadow-")
    return ShadowCapture(d), d


def ev(**kw):
    base = {
        "source": {"service": "test-organ", "operation": "probe",
                   "source_version": "v1", "deployed_version": "v1"},
        "state": {"transport_status": "returned",
                  "verification_status": "not_assessed"},
        "claim": "test claim",
        "occurred_at": "2026-10-30T00:00:00+00:00",
    }
    base.update(kw)
    return base


# ── Fixture 1: transport ok + kernel HOLD → both preserved, not flattened ──
cap, d1 = fresh_store()
r = cap.ingest(ev(state={"transport_status": "returned",
                         "kernel_verdict": "HOLD",
                         "workflow_status": "blocked",
                         "verification_status": "not_assessed"}))
rec = cap.get(r["lineage_id"])
check("F1 hold-dominates",
      r["status"] == "recorded"
      and rec["state"]["kernel_verdict"] == "HOLD"
      and rec["state"]["transport_status"] == "returned"
      and cap.project()["verdict_mismatches"] == 1,
      "mismatch surfaced in projection")
shutil.rmtree(d1)

# ── Fixture 2: same observation twice → 1 lineage, second is duplicate ──
cap, d2 = fresh_store()
r1 = cap.ingest(ev(claim="corrections persist after restart"))
r2 = cap.ingest(ev(claim="corrections persist after restart"))
check("F2 lineage-dedup",
      r1["status"] == "recorded" and r2["status"] == "duplicate"
      and r1["lineage_id"] == r2["lineage_id"])
shutil.rmtree(d2)

# ── Fixture 3: evidence superseded mid-review → only that lineage stales ──
cap, d3 = fresh_store()
ra = cap.ingest(ev(claim="baseline claim A"))
rb = cap.ingest(ev(claim="unrelated claim B"))
affected = cap.supersede(ra["lineage_id"], "contradicted by EVID-27")
a_rec, b_rec = cap.get(ra["lineage_id"]), cap.get(rb["lineage_id"])
check("F3 dependency-scoped-invalidation",
      affected == [ra["event_id"]] and a_rec.get("freshness") == "stale"
      and b_rec.get("freshness") != "stale")
shutil.rmtree(d3)

# ── Fixture 4: future-dated timestamp → quarantined, not silently accepted ──
cap, d4 = fresh_store()
r = cap.ingest(ev(occurred_at="2027-01-01T00:00:00+00:00"))
check("F4 future-quarantine", r["status"] == "quarantined" and "future_dated" in r["reason"])
shutil.rmtree(d4)

# ── Fixture 5: malformed / missing required state → quarantined, no defaults ──
cap, d5 = fresh_store()
r = cap.ingest({"source": None})
check("F5 quarantine-no-fabrication", r["status"] == "quarantined")
shutil.rmtree(d5)

# ── Fixture 6: capture dies and revives → no silent loss, no duplicate ──
cap, d6 = fresh_store()
r1 = cap.ingest(ev(claim="pre-crash event"))
cap2 = ShadowCapture(d6)                      # simulate restart, same store dir
r2 = cap2.ingest(ev(claim="pre-crash event"))  # replay after crash
proj = cap2.project()
check("F6 crash-recovery",
      r2["status"] == "duplicate" and proj["total_records"] == 1,
      "replayed ingest deduped against persisted ledger")
# partial-write resilience: corrupt trailing line → quarantined, clean still readable
with open(os.path.join(d6, "shadow_ledger.jsonl"), "a") as f:
    f.write('\n{"event_id": "trunc')
cap3 = ShadowCapture(d6)
proj = cap3.project()
check("F6b corrupt-tail-quarantined",
      proj["quarantined"] == 1 and proj["total_records"] == 1,
      "clean record preserved, corrupt line surfaced in quarantine")
shutil.rmtree(d6)

# ── Fixture 7: execution recorded without verification → stays pending ──
cap, d7 = fresh_store()
r = cap.ingest(ev(event_type="action_attempted",
                  state={"transport_status": "returned",
                         "execution_status": "attempted",
                         "verification_status": "unknown"}))
rec = cap.get(r["lineage_id"])
check("F7 verification-stays-pending",
      rec["state"]["verification_status"] == "unknown"
      and cap.project()["verification_pending"] == 1)
shutil.rmtree(d7)

# ── Acceptance tests from the directive ──
cap, d8 = fresh_store()
# A2: update produces new version, original preserved
r0 = cap.ingest(ev(claim="forecast basis v1"))
affected = cap.supersede(r0["lineage_id"], "new evidence")
r1 = cap.ingest(ev(claim="forecast basis v1", occurred_at="2026-10-30T01:00:00+00:00"))
hist = list(cap._iter(os.path.join(d8, "shadow_ledger.jsonl")))
check("A2 update-new-version-original-kept",
      len(hist) == 2 and hist[0]["freshness"] == "stale" and r1["status"] == "recorded")
# A9: prospective vs retrospective separated by field (mode recorded at lock)
rm = cap.ingest(ev(claim="trial", event_type="forecast_lock"))
rec_m = cap.get(rm["lineage_id"])
check("A9 mode-field", rec_m["event_type"] == "forecast_lock")
# A10: no evaluation object grants execution authority — projection exposes no such field
proj = cap.project()
check("A10 projection-no-authority", all("authoriz" not in k for k in proj))
shutil.rmtree(d8)

# ── Summary ──
fails = [n for n, ok, _ in RESULTS if not ok]
print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} passed. Failures: {fails or 'none'}")
sys.exit(1 if fails else 0)
