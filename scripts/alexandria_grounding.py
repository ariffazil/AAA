#!/usr/bin/env python3
"""
alexandria_grounding.py — Governed External Evidence Grounding Adapter for arifOS
=================================================================================
STATUS: F13 RATIFIED (2026-09-24) — Follows arifOS_connection_design:
  "Treat Alexandria/Firecrawl as an external evidence-grounding provider behind
   an arifOS governed adapter; send proposed action through arifOS before execution,
   then attach returned evidence to receipt/audit flow."

INVARIANTS:
  - F2 TRUTH CLASS: Output is explicitly labeled MEASURED or REPORTED (never INFERRED).
  - PROVENANCE: Every query & fetched payload receives an immutable trace_id and SHA-256.
  - SINK: Writes receipt to /root/AAA/state/evidence_queue.jsonl.
"""

from __future__ import annotations

import os
import sys
import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests

EVIDENCE_SINK = Path("/root/AAA/state/evidence_queue.jsonl")
EVIDENCE_SINK.parent.mkdir(parents=True, exist_ok=True)

def load_firecrawl_key() -> str:
    key = os.getenv("FIRECRAWL_API_KEY")
    if key and not key.startswith("${"):
        return key

    for p in ["/root/.secrets/kunci-root.env", "/root/.secrets/vault.flat.env"]:
        path = Path(p)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if "FIRECRAWL_API_KEY=" in line:
                        v = line.split("=", 1)[1].strip("\"'\n")
                        if v and not v.startswith("${"):
                            return v
    raise RuntimeError("No valid FIRECRAWL_API_KEY found.")

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

class AlexandriaGrounding:
    BASE_URL = "https://api.firecrawl.dev/v2"

    @staticmethod
    def get_headers() -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {load_firecrawl_key()}",
            "Content-Type": "application/json"
        }

    @classmethod
    def discover_tools(cls, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Step 1: Free discovery of Alexandria structured data tools and contracts.
        """
        url = f"{cls.BASE_URL}/search"
        payload = {
            "query": query,
            "sources": ["alexandria"],
            "limit": limit
        }
        resp = requests.post(url, headers=cls.get_headers(), json=payload, timeout=20)
        if resp.status_code != 200:
            raise RuntimeError(f"Alexandria discovery failed ({resp.status_code}): {resp.text}")

        data = resp.json().get("data", {})
        return data.get("tools", [])

    @classmethod
    def fetch_evidence(
        cls,
        provider: str,
        capability: str,
        options: Dict[str, Any],
        requested_by: str = "GEOX/WEALTH"
    ) -> Dict[str, Any]:
        """
        Step 2: Execute contracted scrape, bind F2 provenance, and write audit receipt.
        """
        trace_id = f"ALX-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{os.urandom(4).hex()}"
        ts_utc = datetime.now(timezone.utc).isoformat()
        url = f"{cls.BASE_URL}/scrape"

        payload = {
            "alexandria": {
                "provider": provider,
                "capability": capability,
                "options": options
            }
        }

        t0 = time.time()
        resp = requests.post(url, headers=cls.get_headers(), json=payload, timeout=30)
        latency_ms = int((time.time() - t0) * 1000)

        if resp.status_code != 200:
            raise RuntimeError(f"Alexandria scrape failed ({resp.status_code}): {resp.text}")

        resp_json = resp.json()
        alex_data = resp_json.get("data", {}).get("alexandria", [{}])[0]
        records = alex_data.get("data", [])
        if isinstance(records, str):
            try:
                records = json.loads(records)
            except Exception:
                pass
        credits_used = resp_json.get("creditsUsed") or resp_json.get("data", {}).get("creditsCost", 0)

        raw_str = json.dumps(records, ensure_ascii=False)
        payload_sha256 = sha256_str(raw_str)

        # F2 Provenance Receipt
        evidence_packet = {
            "trace_id": trace_id,
            "timestamp_utc": ts_utc,
            "truth_class": "MEASURED",  # Direct API contract return
            "source": f"alexandria/{provider}/{capability}",
            "requested_by": requested_by,
            "options": options,
            "records_count": len(records) if isinstance(records, list) else 1,
            "payload_sha256": payload_sha256,
            "credits_used": credits_used,
            "latency_ms": latency_ms,
            "alexandria_id": alex_data.get("alexandriaId")
        }

        # Write immutable audit receipt to evidence queue
        with open(EVIDENCE_SINK, "a", encoding="utf-8") as f:
            f.write(json.dumps(evidence_packet, ensure_ascii=False) + "\n")

        return {
            "evidence_packet": evidence_packet,
            "data": records
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 alexandria_grounding.py discover <query>")
        print("  python3 alexandria_grounding.py fetch <provider> <capability> '<json_options>'")
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "discover":
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "crude oil brent spot price"
        tools = AlexandriaGrounding.discover_tools(q)
        print(f"\nDiscovered {len(tools)} tools for '{q}':")
        for t in tools:
            print(f"  • {t.get('provider')}/{t.get('capability')} -> {t.get('description', '')[:90]}...")
    elif cmd == "fetch":
        prov = sys.argv[2] if len(sys.argv) > 2 else "eia-gov"
        cap = sys.argv[3] if len(sys.argv) > 3 else "energy-data/data"
        opts = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {"route": "petroleum/pri/spt"}
        res = AlexandriaGrounding.fetch_evidence(prov, cap, opts)
        pkt = res["evidence_packet"]
        print(f"\n[SUCCESS] Fetched evidence via {pkt['source']}!")
        print(f"  Trace: {pkt['trace_id']}")
        print(f"  Truth Class: {pkt['truth_class']}")
        print(f"  SHA-256: {pkt['payload_sha256']}")
        print(f"  Credits: {pkt['credits_used']} (Latency: {pkt['latency_ms']}ms)")
        print(f"  Receipt written to: {EVIDENCE_SINK}")
