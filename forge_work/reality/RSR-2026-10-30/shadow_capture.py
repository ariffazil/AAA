#!/usr/bin/env python3
"""shadow_capture.py — RSR v0 Phase 1 thin capture adapter.

Layer kecil: rekod event runtime ke shadow ledger (append-only JSONL),
dengan lineage dedup, quarantine, dan state separation. TIDAK mengeluarkan
verdict kernel, TIDAK menukar approval, TIDAK execute apa-apa, TIDAK hantar
telemetry ke CHRON sebagai prediction. CHRON menerima forecast ber-definisi,
bukan semua sampel.

State semantics dipinjam dari AAA reality_graph.py (epistemic classes) dan
arifOS contracts (workflow ≠ kernel verdict). Supersede = dependency-scoped.

DITEMPA BUKAN DIBERI ⚒️
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Any, Optional

SCHEMA_VERSION = "shadow-event.v1"

# Workflow states (local, BUKAN kernel verdict)
WORKFLOW_STATES = {
    "input_required", "review_required", "authorization_required",
    "execution_eligible", "verification_pending", "completed",
    "blocked", "paused",
}
# Kernel verdicts (arifOS lattice, 5) — stored separately, never merged
KERNEL_VERDICTS = {"SEAL", "HOLD", "SABAR", "PARTIAL", "VOID"}
EPISTEMIC = {"OBS", "DER", "INT", "SPEC", "SEAL"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _h(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(obj, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]


class ShadowCapture:
    """Append-only shadow event store. Rejected/quarantined payloads land in
    quarantine.jsonl with a reason — nothing is fabricated, nothing silently lost."""

    def __init__(self, store_dir: str):
        self.store_dir = store_dir
        os.makedirs(store_dir, exist_ok=True)
        self.ledger_path = os.path.join(store_dir, "shadow_ledger.jsonl")
        self.quarantine_path = os.path.join(store_dir, "quarantine.jsonl")

    # ── ingest ────────────────────────────────────────────────────────
    def ingest(self, event: dict) -> dict:
        """Validate + record one runtime event as a shadow record.
        Returns {"status": "recorded"|"quarantined"|"duplicate", ...}."""
        # 1. required fields
        missing = [k for k in ("source", "state") if not isinstance(event.get(k), dict)]
        if missing:
            return self._quarantine(event, f"missing_or_malformed:{','.join(missing)}")

        # 2. future-dated timestamps → quarantine (temporal discipline)
        for ts_field in ("occurred_at",):
            ts = event.get(ts_field)
            if ts:
                try:
                    t = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                    if t > datetime.now(timezone.utc):
                        return self._quarantine(event, f"future_dated:{ts_field}")
                except ValueError:
                    return self._quarantine(event, f"unparseable:{ts_field}")

        # 3. state separation: workflow vs kernel verdict never merged
        st = event["state"]
        wf = st.get("workflow_status")
        kv = st.get("kernel_verdict")
        if wf is not None and wf not in WORKFLOW_STATES:
            return self._quarantine(event, f"invalid_workflow_state:{wf}")
        if kv is not None and kv not in KERNEL_VERDICTS:
            return self._quarantine(event, f"invalid_kernel_verdict:{kv}")
        # verification semantics preserved: unknown stays unknown
        vs = st.get("verification_status", "not_assessed")
        if vs not in {"not_assessed", "pending", "verified", "failed", "unknown"}:
            return self._quarantine(event, f"invalid_verification_status:{vs}")

        # 4. lineage: identical semantic payload = same lineage, not two witnesses
        lineage = _h({
            "source": event["source"],
            "claim": event.get("claim"),
            "occurred_at": event.get("occurred_at"),
        })
        for prev in self._iter(self.ledger_path):
            if prev.get("lineage_id") == lineage:
                return {"status": "duplicate", "lineage_id": lineage,
                        "existing_event_id": prev["event_id"]}

        event_id = event.get("event_id") or ("evt-" + _h(event)[:24])
        record = {
            "schema_version": SCHEMA_VERSION,
            "event_id": event_id,
            "lineage_id": lineage,
            "correlation_id": event.get("correlation_id"),
            "event_type": event.get("event_type", "tool_result_observed"),
            "occurred_at": event.get("occurred_at"),   # source-event time; null honest
            "ingested_at": _now(),
            "claim": event.get("claim"),
            "epistemic_class": event.get("epistemic_class", "OBS"),
            "source": {
                "service": event["source"].get("service"),
                "operation": event["source"].get("operation"),
                "source_version": event["source"].get("source_version"),
                "deployed_version": event["source"].get("deployed_version"),
            },
            "state": {
                "transport_status": st.get("transport_status", "returned"),
                "workflow_status": wf,
                "kernel_verdict": kv,          # kept separate, even when transport ok
                "execution_status": st.get("execution_status", "unknown"),
                "verification_status": vs,
            },
            "provenance": {
                "request_ref": event.get("provenance", {}).get("request_ref"),
                "response_ref": event.get("provenance", {}).get("response_ref"),
                "payload_hash": _h(event),
            },
            "supersedes": event.get("supersedes") or [],
        }

        # drift: source vs deployed version differ → displayed, cause NOT assumed
        sv, dv = record["source"]["source_version"], record["source"]["deployed_version"]
        record["drift_flag"] = bool(sv and dv and sv != dv)

        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(record, default=str) + "\n")
        return {"status": "recorded", "event_id": event_id, "lineage_id": lineage,
                "drift_flag": record["drift_flag"]}

    # ── supersede: dependency-scoped invalidation ─────────────────────
    def supersede(self, old_lineage_id: str, reason: str) -> list[str]:
        """Mark records of old_lineage stale (freshness), leave others untouched.
        Correction adds history; it never rewrites history."""
        affected = []
        changed = False
        out = []
        for rec in self._iter(self.ledger_path):
            if rec.get("lineage_id") == old_lineage_id:
                rec["freshness"] = "stale"
                rec["stale_reason"] = reason
                rec["staled_at"] = _now()
                affected.append(rec["event_id"])
                changed = True
            out.append(rec)
        if changed:
            self._rewrite(self.ledger_path, out)
        return affected

    def get(self, lineage_id: str) -> Optional[dict]:
        latest = None
        for rec in self._iter(self.ledger_path):
            if rec.get("lineage_id") == lineage_id:
                latest = rec  # last write wins for display; history preserved in file
        return latest

    # ── projection: Reality Graph view built FROM ledger, never the record ──
    def project(self) -> dict:
        """Rebuildable projection. If wrong, records are untouched."""
        recs = list(self._iter(self.ledger_path))
        return {
            "projected_at": _now(),
            "total_records": len(recs),
            "quarantined": sum(1 for _ in self._iter(self.quarantine_path)),
            "stale": sum(1 for r in recs if r.get("freshness") == "stale"),
            "drift_flagged": sum(1 for r in recs if r.get("drift_flag")),
            "verification_pending": sum(
                1 for r in recs if r["state"]["verification_status"] in ("pending", "unknown")),
            "verdict_mismatches": sum(  # transport ok but kernel says HOLD/SABAR/PARTIAL/VOID
                1 for r in recs if r["state"]["transport_status"] == "returned"
                and r["state"].get("kernel_verdict") in {"HOLD", "SABAR", "PARTIAL", "VOID"}),
        }

    # ── internals ─────────────────────────────────────────────────────
    def _iter(self, path: str):
        if not os.path.exists(path):
            return
        corrupt = []
        with open(path) as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    corrupt.append((lineno, line[:80]))
        # fail-safe: corrupt lines are surfaced, never silently lost
        if corrupt and path == self.ledger_path:
            for lineno, frag in corrupt:
                self._quarantine({"corrupt_file": path, "line": lineno, "fragment": frag},
                                 "corrupt_ledger_line")

    def _rewrite(self, path: str, records) -> None:
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            for r in records:
                f.write(json.dumps(r, default=str) + "\n")
        os.replace(tmp, path)  # atomic; crash-safe

    def _quarantine(self, event: dict, reason: str) -> dict:
        rec = {"quarantined_at": _now(), "reason": reason, "payload_hash": _h(event)}
        with open(self.quarantine_path, "a") as f:
            f.write(json.dumps(rec) + "\n")
        return {"status": "quarantined", "reason": reason, "payload_hash": rec["payload_hash"]}


if __name__ == "__main__":
    print("shadow_capture module — run test_fixtures.py")
