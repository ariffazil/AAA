#!/usr/bin/env python3
"""
trust_ledger_emitter.py — v0 PROVISIONAL: feed trust_trajectory from REAL ledgers.
===================================================================================
Gap closed (audit 2026-08-14): the detector guarded a ledger nobody wrote.
This adapter derives trust-trajectory events from ledgers the federation
ALREADY produces. Stdlib only. Evidence-producer only — no verdicts.

Sources (auto-detected; missing → skipped with count, never fatal):
  session-receipts.jsonl   → per-agent completed sealed work  → helpful_act
  agent_commission.jsonl   → agent commissioned w/ authority  → authority_request
  vault999/seal_chain.jsonl→ actor exercised stage-999 power → authority_request

Mapping honesty (v0 PROVISIONAL):
  - commissioning ≈ authority grant-event; refine when ACT/lease logs expose
    request-vs-grant distinction (v1).
  - timestamps fall back to file mtime when the record carries none
    (context.ts_source marks it) — mtime is weak evidence, flagged as such.

Idempotent: appends only lines whose source-sha256 is not already banked.
Output: TRUST_LEDGER env (default /root/.arifos/registries/trust-ledger.jsonl)
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

BASE = "/root/.local/share/arifos"
SOURCES = {
    "session_receipts": (f"{BASE}/session-receipts.jsonl", "helpful_act"),
    "agent_commission": (f"{BASE}/agent_commission.jsonl", "authority_request"),
    "seal_chain": (f"{BASE}/vault999/seal_chain.jsonl", "authority_request"),
}
DEFAULT_LEDGER = "/root/.arifos/registries/trust-ledger.jsonl"


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ts_of(rec, path):
    for k in ("timestamp", "ts", "timestamp_utc", "sealed_at"):
        v = rec.get(k)
        if isinstance(v, str) and len(v) >= 10:
            return v.replace(" ", "T")[:19] + ("Z" if not ("+" in v or v.endswith("Z")) else ""), "record"
    return datetime.fromtimestamp(os.stat(path).st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "file_mtime"


def _agent_of(rec):
    for k in ("agent", "agent_id", "actor_id", "actor"):
        v = rec.get(k)
        if isinstance(v, str) and v:
            return v
    return None


def main():
    ledger_path = os.environ.get("TRUST_LEDGER", DEFAULT_LEDGER)
    banked = set()
    if os.path.exists(ledger_path):
        with open(ledger_path) as f:
            for line in f:
                try:
                    banked.add(json.loads(line).get("context", {}).get("source_sha256"))
                except Exception:
                    pass

    emitted = []
    skipped = {}
    skipped["no_agent"] = 0
    for name, (path, event) in SOURCES.items():
        if not os.path.exists(path):
            skipped[name] = "source_missing"
            continue
        n = 0
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                sha = hashlib.sha256(line.encode()).hexdigest()
                if sha in banked:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if not isinstance(rec, dict):
                    continue
                agent = _agent_of(rec)
                if not agent or agent.upper() in ("ARIF", "F13", "SOVEREIGN"):
                    skipped["no_agent"] += 1
                    continue
                ts, ts_src = _ts_of(rec, path)
                emitted.append(
                    {
                        "ts": ts,
                        "agent": agent,
                        "event": event,
                        "context": {"source": name, "source_sha256": sha, "ts_source": ts_src},
                    }
                )
                banked.add(sha)
                n += 1
        skipped[name] = n

    if emitted:
        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
        with open(ledger_path, "a") as f:
            for e in emitted:
                f.write(json.dumps(e) + "\n")

    print(f"trust_ledger_emitter v0 — emitted {len(emitted)} events → {ledger_path}")
    for k, v in skipped.items():
        print(f"  {k}: {v}")
    print("role: EVIDENCE_PRODUCER — run trust_trajectory.py on the ledger; verdicts belong to arif_judge")
    return 0


if __name__ == "__main__":
    sys.exit(main())
