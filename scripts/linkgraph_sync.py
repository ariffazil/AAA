#!/usr/bin/env python3
"""linkgraph_sync — pump CHRON + reality signals into the Graphiti link graph.

Why this exists:
  The lg: namespace (per /root/AAA/instructions/linkgraph-namespace.md) is the
  canonical graph for the federation. The actual storage is Graphiti v1.29.1
  (FalkorDB backend) at 127.0.0.1:18412, with 7 group_ids: arif_l5_knowledge,
  sado_knowledge, atlas333_graph, af_forge, arifos, arifos_federation,
  searah_2026q3.

  This script:
    1. Reads CHRON data (predictions, lessons, calibrations) + reality signals
    2. Wraps them as Graphiti episodes (one per fact)
    3. POSTs to the Graphiti MCP endpoint via the JSON-RPC SSE transport
    4. Logs sync receipts to /root/chron/data/linkgraph_sync.jsonl

  Bitemporal: each episode carries a reference_time so facts can be
  superseded without losing history.

Usage:
  python3 /root/AAA/scripts/linkgraph_sync.py [--dry-run] [--group-id X]

Group routing:
  arif_l5_knowledge  - sovereign decisions, personal state, MSS/OD1
  sado_knowledge     - abang sado, gym, market, gold
  atlas333_graph     - doctrine, scar, paradox, geometric cognition
  af_forge           - forge work, build artifacts
  arifos             - kernel state, decisions, federated layer
  arifos_federation  - cross-organ, agent registry
  searah_2026q3      - quarterly review, retros
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

GRAPHITI_URL = "http://127.0.0.1:18412/mcp/"
NOW = datetime.now(timezone(timedelta(hours=8)))
TODAY = NOW.date().isoformat()
NOW_ISO = NOW.isoformat()

# ---- Group routing rules ----
def route_to_group(fact: dict) -> str:
    """Pick the right group_id for a fact based on content + audience."""
    audience = (fact.get("audience") or "").lower()
    title = (fact.get("title") or fact.get("claim") or fact.get("text") or "").lower()
    ftype = (fact.get("type") or fact.get("kind") or "").lower()

    # Personal sovereign
    if audience == "arif" or "arif" in title or "mss" in title or "od1" in title:
        return "arif_l5_knowledge"
    # Syed lane
    if audience == "syed" or "syed" in title or "abang sado" in title or "gym" in title or "xau" in title or "gold" in title:
        return "sado_knowledge"
    # Doctrine / scar / paradox
    if ftype in ("scar", "paradox", "doctrine") or "scar" in title or "paradox" in title or "doctrine" in title:
        return "atlas333_graph"
    # Forge work
    if ftype in ("build", "deploy", "artifact") or "forge" in title or "build" in title or "deploy" in title:
        return "af_forge"
    # Kernel / decisions
    if ftype in ("kernel", "decision", "seal") or "kernel" in title or "seal" in title:
        return "arifos"
    # Federation / agent registry
    if "agent" in title or "federation" in title or "registry" in title:
        return "arifos_federation"
    # Default
    return "searah_2026q3"


# ---- Graphiti MCP client (SSE) ----
class GraphitiClient:
    def __init__(self, url: str = GRAPHITI_URL):
        self.url = url
        self.session_id: str | None = None
        self._req_id = 0

    def _next_id(self) -> int:
        self._req_id += 1
        return self._req_id

    def _post(self, payload: dict) -> dict:
        body = json.dumps(payload)
        # Use curl -i to capture response headers (mcp-session-id).
        cmd = [
            "curl", "-sL", "-i", "--max-time", "20",
            "-X", "POST", self.url,
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json, text/event-stream",
        ]
        if self.session_id:
            cmd += ["-H", f"mcp-session-id: {self.session_id}"]
        cmd += ["-d", body]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        except subprocess.TimeoutExpired:
            return {"error": "timeout"}
        except Exception as e:
            return {"error": str(e)[:200]}

        # split headers from body
        raw = r.stdout
        body_start = 0
        session_id_captured = None
        for i, line in enumerate(raw.splitlines()):
            if line.strip() == "":
                body_start = i + 1
                break
            if line.lower().startswith("mcp-session-id:"):
                session_id_captured = line.split(":", 1)[1].strip()
        if session_id_captured:
            self.session_id = session_id_captured

        body = "\n".join(raw.splitlines()[body_start:])

        if not body:
            return {"error": f"empty body, stderr={r.stderr.strip()[:200]}"}

        # parse SSE: look for "data: {json}"
        for line in body.splitlines():
            if line.startswith("data: "):
                try:
                    parsed = json.loads(line[6:])
                except json.JSONDecodeError:
                    continue
                # check for json-rpc error wrapper
                if isinstance(parsed, dict) and parsed.get("error"):
                    return parsed
                # check tool-call result for isError flag
                if isinstance(parsed, dict):
                    result = parsed.get("result", {})
                    if isinstance(result, dict) and result.get("isError"):
                        return {"error": f"tool isError: {result.get('content', '')[:300]}"}
                    # also unwrap structuredContent if present
                    if isinstance(result, dict) and "structuredContent" in result:
                        sc = result["structuredContent"]
                        if isinstance(sc, dict) and sc.get("status") not in (None, "ok"):
                            return {"error": f"tool returned non-ok: {json.dumps(sc)[:300]}"}
                return parsed
        # if no SSE prefix, return raw
        try:
            parsed = json.loads(body)
            if isinstance(parsed, dict) and parsed.get("error"):
                return parsed
            return parsed
        except json.JSONDecodeError:
            return {"raw": body[:500]}

    def initialize(self) -> dict:
        return self._post({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "linkgraph_sync", "version": "0.1"},
            },
        })

    def initialized(self) -> dict:
        return self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def add_memory(self, name: str, content: str, group_id: str, reference_time: str | None = None) -> dict:
        args = {"name": name, "episode_body": content, "group_id": group_id, "source": "text"}
        if reference_time:
            args["reference_time"] = reference_time
        return self._post({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {"name": "add_memory", "arguments": args},
        })

    def search_nodes(self, query: str, group_ids: list[str] | None = None, limit: int = 5) -> dict:
        args = {"query": query, "limit": limit}
        if group_ids:
            args["group_ids"] = group_ids
        return self._post({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {"name": "search_nodes", "arguments": args},
        })

    def get_status(self) -> dict:
        return self._post({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {"name": "get_status", "arguments": {}},
        })


# ---- Source collectors ----
def collect_chron_signals() -> list[dict]:
    """Pull recent CHRON signals from /root/chron/data/"""
    signals: list[dict] = []
    base = Path("/root/chron/data")

    # 1) Predictions (newest 30)
    p_path = base / "predictions.jsonl"
    if p_path.exists():
        preds = [json.loads(l) for l in p_path.read_text().splitlines() if l.strip()]
        # sort by created_at desc, take 30
        preds.sort(key=lambda p: p.get("created_at", ""), reverse=True)
        for p in preds[:30]:
            signals.append({
                "type": "prediction",
                "id": p.get("prediction_id"),
                "claim": p.get("claim", ""),
                "audience": p.get("audience"),
                "confidence": p.get("confidence"),
                "status": p.get("status"),
                "verify_at": p.get("verify_at"),
                "created_at": p.get("created_at"),
            })

    # 2) Lessons (all)
    l_path = base / "lessons.jsonl"
    if l_path.exists():
        for ln in l_path.read_text().splitlines():
            if not ln.strip():
                continue
            d = json.loads(ln)
            signals.append({
                "type": "lesson",
                "id": d.get("lesson_id"),
                "text": d.get("lesson", ""),
                "error_type": d.get("error_type"),
                "audience": d.get("audience"),
                "source_prediction_id": d.get("source_prediction_id"),
                "created_at": d.get("created_at"),
            })

    # 3) Chron events (top 20 ranked)
    ev_path = Path("/root/AAA/scripts/chron_events.json")
    if ev_path.exists():
        events = json.loads(ev_path.read_text()).get("events", [])
        from datetime import date
        future = [e for e in events if e.get("target_date", "") >= TODAY]
        future.sort(key=lambda e: e.get("target_date", ""))
        for e in future[:20]:
            signals.append({
                "type": "event",
                "id": e.get("id"),
                "title": e.get("title"),
                "target_date": e.get("target_date"),
                "audience": e.get("audience"),
                "kind": e.get("kind"),
                "consequence": e.get("consequence"),
            })

    return signals


def collect_reality_signals() -> list[dict]:
    """Pull live reality signals from federated caches."""
    signals: list[dict] = []

    # Market cache
    cache = Path("/root/AAA/scripts/.chron_market_cache.json")
    if cache.exists():
        d = json.loads(cache.read_text())
        signals.append({
            "type": "market",
            "text": f"Market snapshot @ {d.get('captured_at')}: Brent={d.get('brent')}, USD/MYR={d.get('usdmyr')}, VIX={d.get('vix')}, DXY={d.get('dxy')}, US10Y={d.get('us10y')}, silver={d.get('silver')}",
            "source": "WEALTH MCP via :4000",
            "captured_at": d.get("captured_at"),
            "audience": "both",
        })

    # Verification log (last 20)
    v_path = Path("/root/chron/data/verification_log.jsonl")
    if v_path.exists():
        lines = v_path.read_text().splitlines()
        for ln in lines[-20:]:
            if not ln.strip():
                continue
            d = json.loads(ln)
            signals.append({
                "type": "verification",
                "id": d.get("prediction_id"),
                "outcome": d.get("outcome"),
                "brier": d.get("brier"),
                "evidence": d.get("evidence", "")[:200],
                "audience": "arif",
            })

    return signals


def collect_scar_telemetry() -> list[dict]:
    """Pull the latest scar / scar-pattern signals from memory."""
    signals: list[dict] = []
    # From recent_lessons in carry_forward
    cf = Path("/root/.local/share/arifos/carry_forward.json")
    if cf.exists():
        d = json.loads(cf.read_text())
        for l in d.get("chron_briefing", {}).get("recent_lessons", [])[:10]:
            signals.append({
                "type": "scar_candidate",
                "text": l.get("lesson", ""),
                "source_prediction": l.get("source_prediction"),
                "audience": "arif",
            })
    return signals


# ---- Main ----
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--group-id", default=None, help="force a single group_id (override routing)")
    ap.add_argument("--limit", type=int, default=50, help="max episodes to push")
    args = ap.parse_args()

    print(f"linkgraph_sync @ {NOW_ISO}")
    print(f"  graphiti: {GRAPHITI_URL}")
    if args.dry_run:
        print("  DRY-RUN — no graph mutations")
    print()

    # 1) Collect signals
    chron = collect_chron_signals()
    reality = collect_reality_signals()
    scars = collect_scar_telemetry()
    all_signals = chron + reality + scars
    print(f"  collected: {len(chron)} chron + {len(reality)} reality + {len(scars)} scar = {len(all_signals)} total")

    if not all_signals:
        print("  no signals to push")
        return 0

    if args.dry_run:
        # show first 5 with their group routing
        for s in all_signals[:5]:
            gid = args.group_id or route_to_group(s)
            text = s.get("text") or s.get("claim") or s.get("title") or s.get("evidence") or ""
            print(f"  {gid:25}  {s['type']:14}  {text[:80]}")
        print(f"  ... and {len(all_signals) - 5} more")
        return 0

    # 2) Init Graphiti session
    client = GraphitiClient()
    init = client.initialize()
    if "error" in init:
        print(f"  init failed: {init['error']}")
        return 1
    print(f"  session: {client.session_id or '(no session id)'}")
    client.initialized()

    # 3) Push each as an episode
    receipts: list[dict] = []
    pushed = 0
    errors = 0
    for s in all_signals[: args.limit]:
        gid = args.group_id or route_to_group(s)
        name = f"{s['type']}:{(s.get('id') or s.get('title') or s.get('claim') or 'unnamed')[:80]}"
        text = s.get("text") or s.get("claim") or s.get("title") or s.get("evidence") or json.dumps(s)[:200]
        ref_time = s.get("captured_at") or s.get("created_at") or s.get("verify_at") or s.get("target_date") or NOW_ISO

        try:
            r = client.add_memory(name=name, content=text, group_id=gid, reference_time=ref_time)
            if "error" in r:
                errors += 1
                receipts.append({"name": name, "group_id": gid, "error": r["error"][:200]})
            else:
                pushed += 1
                receipts.append({"name": name, "group_id": gid, "ok": True})
        except Exception as e:
            errors += 1
            receipts.append({"name": name, "group_id": gid, "error": str(e)[:200]})

    print(f"  pushed: {pushed}  errors: {errors}")

    # 4) Log receipts
    log = Path("/root/chron/data/linkgraph_sync.jsonl")
    with log.open("a") as f:
        for r in receipts:
            f.write(json.dumps({"ts": NOW_ISO, **r}, ensure_ascii=False) + "\n")
    print(f"  receipts: {log}  (+{len(receipts)} entries)")

    # 5) Sample search to prove linkgraph is queryable
    if pushed > 0:
        print()
        print("  === search probe: 'Brent' ===")
        s = client.search_nodes("Brent crude", group_ids=["searah_2026q3", "arif_l5_knowledge"], limit=3)
        if "result" in s:
            content = s["result"].get("content", [{}])[0].get("text", "")[:300] if isinstance(s["result"].get("content"), list) else str(s["result"])[:300]
            print(f"  result: {content}")
        elif "error" in s:
            print(f"  search error: {s['error'][:200]}")
        else:
            print(f"  raw: {str(s)[:200]}")
    return 0 if errors == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
