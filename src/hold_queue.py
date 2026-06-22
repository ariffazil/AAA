#!/usr/bin/env python3
"""
AAA Cockpit — HOLD Queue and Veto Surface
==========================================
Provides the human control plane for reviewing and resolving HOLD items.

A HOLD item is any action that arifOS gated at F1, F5, F11, F13, or
any floor requiring human review. The queue surfaces these to Arif
for explicit resolution: APPROVE, DENY, or DEFER.

This is AAA as glass — exposing held actions for human judgment,
never issuing verdicts itself.

Usage:
    python3 src/hold_queue.py           # Show queue
    python3 src/hold_queue.py --serve   # Start HTTP API
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import httpx

KERNEL_URL = os.environ.get("ARIFOS_KERNEL_URL", "http://localhost:8088")
QUEUE_FILE = Path(__file__).resolve().parent.parent / "data" / "hold_queue.jsonl"
QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)


# ── HOLD Item Schema ────────────────────────────────────────────────────────

class HoldItem:
    """A single HOLD item awaiting human review."""

    def __init__(
        self,
        intent: str,
        action_class: str,
        proposed_by: str,
        blocked_at: str,
        reasons: list,
        violated_floors: list,
        trace_id: str = "",
        evidence: Optional[dict] = None,
    ):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.intent = intent
        self.action_class = action_class
        self.proposed_by = proposed_by
        self.blocked_at = blocked_at
        self.reasons = reasons
        self.violated_floors = violated_floors
        self.trace_id = trace_id
        self.evidence = evidence or {}
        self.status = "PENDING"  # PENDING | APPROVED | DENIED | DEFERRED
        self.resolved_by = ""
        self.resolved_at = ""
        self.resolution_note = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "intent": self.intent,
            "action_class": self.action_class,
            "proposed_by": self.proposed_by,
            "blocked_at": self.blocked_at,
            "reasons": self.reasons,
            "violated_floors": self.violated_floors,
            "trace_id": self.trace_id,
            "evidence": self.evidence,
            "status": self.status,
            "resolved_by": self.resolved_by,
            "resolved_at": self.resolved_at,
            "resolution_note": self.resolution_note,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "HoldItem":
        item = cls(
            intent=d.get("intent", ""),
            action_class=d.get("action_class", ""),
            proposed_by=d.get("proposed_by", ""),
            blocked_at=d.get("blocked_at", ""),
            reasons=d.get("reasons", []),
            violated_floors=d.get("violated_floors", []),
            trace_id=d.get("trace_id", ""),
            evidence=d.get("evidence", {}),
        )
        item.id = d.get("id", item.id)
        item.created_at = d.get("created_at", item.created_at)
        item.status = d.get("status", "PENDING")
        item.resolved_by = d.get("resolved_by", "")
        item.resolved_at = d.get("resolved_at", "")
        item.resolution_note = d.get("resolution_note", "")
        return item


# ── HOLD Queue ──────────────────────────────────────────────────────────────

class HoldQueue:
    """
    Persistent HOLD queue backed by JSONL.

    Items are written to data/hold_queue.jsonl.
    The queue surfaces pending holds for human review via the AAA cockpit.
    """

    def __init__(self, queue_file: Path = QUEUE_FILE):
        self.queue_file = queue_file

    def add(self, item: HoldItem) -> str:
        """Add a HOLD item to the queue. Returns the item ID."""
        with open(self.queue_file, "a") as f:
            f.write(json.dumps(item.to_dict()) + "\n")
        return item.id

    def add_from_verdict(
        self,
        intent: str,
        action_class: str,
        proposed_by: str,
        verdict_response: dict,
    ) -> str:
        """Create a HOLD item from an arifOS judge response."""
        item = HoldItem(
            intent=intent,
            action_class=action_class,
            proposed_by=proposed_by,
            blocked_at=verdict_response.get("blocked_at", "unknown"),
            reasons=verdict_response.get("reasons", ["No reason provided"]),
            violated_floors=verdict_response.get("violated_laws", []),
            trace_id=str(uuid.uuid4()),
            evidence={"raw_verdict": verdict_response},
        )
        return self.add(item)

    def list_pending(self) -> list[dict]:
        """List all PENDING HOLD items, newest first."""
        items = self._load_all()
        pending = [i.to_dict() for i in items if i.status == "PENDING"]
        pending.sort(key=lambda x: x["created_at"], reverse=True)
        return pending

    def list_all(self, limit: int = 50) -> list[dict]:
        """List all HOLD items, newest first."""
        items = self._load_all()
        items.sort(key=lambda x: x.created_at, reverse=True)
        return [i.to_dict() for i in items[:limit]]

    def get(self, item_id: str) -> Optional[dict]:
        """Get a specific HOLD item by ID."""
        items = self._load_all()
        for item in items:
            if item.id == item_id:
                return item.to_dict()
        return None

    def resolve(
        self,
        item_id: str,
        resolution: str,
        resolved_by: str = "arif",
        note: str = "",
    ) -> bool:
        """
        Resolve a HOLD item.

        Args:
            item_id: ID of the HOLD item.
            resolution: APPROVED | DENIED | DEFERRED.
            resolved_by: Who resolved it (default: "arif").
            note: Optional resolution note.

        Returns:
            True if item was found and resolved.
        """
        if resolution not in ("APPROVED", "DENIED", "DEFERRED"):
            raise ValueError(f"Invalid resolution: {resolution}")

        items = self._load_all()
        found = False
        for i, item in enumerate(items):
            if item.id == item_id:
                item.status = resolution
                item.resolved_by = resolved_by
                item.resolved_at = datetime.now(timezone.utc).isoformat()
                item.resolution_note = note
                found = True
                break

        if not found:
            return False

        # Rewrite entire file
        with open(self.queue_file, "w") as f:
            for item in items:
                f.write(json.dumps(item.to_dict()) + "\n")
        return True

    def count_pending(self) -> int:
        """Count pending HOLD items."""
        return len(self.list_pending())

    def _load_all(self) -> list[HoldItem]:
        """Load all HOLD items from the JSONL file."""
        if not self.queue_file.exists():
            return []
        items = []
        with open(self.queue_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append(HoldItem.from_dict(json.loads(line)))
                except (json.JSONDecodeError, KeyError):
                    continue
        return items


# ── Veto Surface ────────────────────────────────────────────────────────────

class VetoSurface:
    """
    F13 veto surface — the human sovereignty interface.

    This is AAA as glass: it displays what's pending, logs veto decisions,
    and surfaces them to arifOS. It does NOT issue verdicts itself.
    """

    def __init__(self):
        self.queue = HoldQueue()

    def display_veto_board(self) -> dict:
        """
        Return the full veto board for the AAA cockpit.

        Returns:
            dict with:
            - total_pending: count
            - items: list of pending items
            - floors_summary: which floors are most violated
            - oldest_pending: age in hours
        """
        pending = self.queue.list_pending()

        # Aggregate violated floors
        floor_counts = {}
        for item in pending:
            for floor in item.get("violated_floors", []):
                floor_counts[floor] = floor_counts.get(floor, 0) + 1
        floors_summary = dict(sorted(floor_counts.items(), key=lambda x: -x[1]))

        # Calculate oldest pending
        oldest = None
        if pending:
            oldest_created = min(item["created_at"] for item in pending)
            oldest_dt = datetime.fromisoformat(oldest_created)
            oldest_hours = (datetime.now(timezone.utc) - oldest_dt).total_seconds() / 3600
            oldest = round(oldest_hours, 1)

        return {
            "total_pending": len(pending),
            "items": pending[:20],  # Top 20
            "floors_summary": floors_summary,
            "oldest_pending_hours": oldest,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def apply_veto(
        self,
        item_id: str,
        decision: str,
        veto_by: str = "arif",
        note: str = "",
    ) -> dict:
        """
        Apply a sovereign veto (F13) to a HOLD item.

        This is THE F13 surface. It does not judge — it reports the
        human's decision.

        Args:
            item_id: HOLD item ID.
            decision: APPROVED | DENIED | DEFERRED.
            veto_by: Who applied the veto.
            note: Why.

        Returns:
            dict with result, item details, and next steps.
        """
        if decision not in ("APPROVED", "DENIED", "DEFERRED"):
            return {"status": "ERROR", "error": f"Invalid decision: {decision}"}

        success = self.queue.resolve(item_id, decision, veto_by, note)
        if not success:
            return {"status": "ERROR", "error": f"Item {item_id} not found"}

        item = self.queue.get(item_id)
        return {
            "status": "OK",
            "decision": decision,
            "veto_by": veto_by,
            "item": item,
            "note": note,
            "resolved_at": datetime.now(timezone.utc).isoformat(),
            "next_action": "Action may proceed" if decision == "APPROVED" else "Action blocked",
        }


# ── MCP Integration (pull HOLD items from arifOS) ──────────────────────────

def pull_holds_from_arifos() -> list[dict]:
    """
    Query arifOS kernel for recent HOLD events.
    Pulls from arif_judge_deliberate history if available.
    """
    try:
        with httpx.Client(base_url=KERNEL_URL, timeout=10) as c:
            resp = c.post("/mcp", headers={"Accept": "application/json"}, json={
                "jsonrpc": "2.0", "id": "aaa-hold-pull",
                "method": "tools/call",
                "params": {
                    "name": "arif_judge_deliberate",
                    "arguments": {"mode": "history", "limit": 20},
                },
            })
            if resp.status_code != 200:
                return []
            body = resp.json()
            if "error" in body:
                return []
            result = body.get("result", {})
            for c in result.get("content", []):
                if c.get("type") == "text":
                    try:
                        return json.loads(c["text"]).get("results", [])
                    except (json.JSONDecodeError, KeyError):
                        continue
            return []
    except Exception:
        return []


# ── HTTP API (for AAA React cockpit to call) ───────────────────────────────

def serve_api(host: str = "127.0.0.1", port: int = 18999):
    """
    Start a simple HTTP API for the AAA React cockpit.

    Endpoints:
        GET  /hold/pending    — list pending HOLD items
        GET  /hold/all        — list all HOLD items
        GET  /hold/{id}       — get specific item
        POST /hold/{id}/resolve — resolve an item
        GET  /veto/board      — display veto board
    """
    import urllib.parse
    from http.server import BaseHTTPRequestHandler, HTTPServer

    queue = HoldQueue()
    veto = VetoSurface()

    class Handler(BaseHTTPRequestHandler):
        def _json(self, data, status=200):
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data, indent=2).encode())

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path.rstrip("/")

            if path == "/hold/pending":
                self._json({"status": "OK", "items": queue.list_pending()})
            elif path == "/hold/all":
                self._json({"status": "OK", "items": queue.list_all()})
            elif path.startswith("/hold/") and len(path) > 6:
                item_id = path.split("/")[-1]
                item = queue.get(item_id)
                if item:
                    self._json({"status": "OK", "item": item})
                else:
                    self._json({"status": "ERROR", "error": "Not found"}, 404)
            elif path == "/veto/board":
                self._json(veto.display_veto_board())
            else:
                self._json({"status": "ERROR", "error": "Unknown endpoint"}, 404)

        def do_POST(self):
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path.rstrip("/")

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                data = {}

            if path.startswith("/hold/") and path.endswith("/resolve"):
                item_id = path.split("/")[-2]
                decision = data.get("decision", "")
                veto_by = data.get("veto_by", "arif")
                note = data.get("note", "")
                result = veto.apply_veto(item_id, decision, veto_by, note)
                self._json(result)
            else:
                self._json({"status": "ERROR", "error": "Unknown endpoint"}, 404)

        def log_message(self, format, *args):
            if VERBOSE:
                print(f"  [API] {args[0]} {args[1]}")

    print(f"  AAA HOLD API server at http://{host}:{port}")
    print("  Endpoints:")
    print("    GET  /hold/pending")
    print("    GET  /hold/all")
    print("    GET  /hold/<id>")
    print("    POST /hold/<id>/resolve  (body: decision, note)")
    print("    GET  /veto/board")

    server = HTTPServer((host, port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")


# ── Main ────────────────────────────────────────────────────────────────────

def demo():
    """Demonstrate HOLD queue and veto surface."""
    print("═══ AAA Cockpit — HOLD Queue + Veto Surface ═══")
    print()

    queue = HoldQueue()
    veto = VetoSurface()

    # Add some demo HOLD items
    print("Adding demo HOLD items...")

    items_data = [
        ("Delete production database", "ATOMIC", "agent-01", "GATE_1_IDENTITY",
         ["Anonymous actor cannot execute ATOMIC"], ["F1", "F11"]),
        ("Deploy without rollback", "MUTATE", "agent-02", "GATE_5_PEACE",
         ["Action has irreversible side effects without rollback"], ["F1", "F5"]),
        ("Exfiltrate customer data", "ATOMIC", "agent-03", "GATE_9_ANTHANTU",
         ["Action attempts unauthorized data transfer"], ["F5", "F9", "F12"]),
        ("Leverage 10x on single position", "ALLOCATE", "agent-04", "GATE_5_PEACE",
         ["Capital risk exceeds threshold without WEALTH witness"], ["F5", "F11"]),
    ]

    for intent, ac, agent, gate, reasons, floors in items_data:
        item = HoldItem(
            intent=intent,
            action_class=ac,
            proposed_by=agent,
            blocked_at=gate,
            reasons=reasons,
            violated_floors=floors,
        )
        queue.add(item)
        print(f"  📋 {item.id[:8]}... | {intent[:40]:40s} | PENDING")

    print()

    # Display veto board
    print("Veto board:")
    board = veto.display_veto_board()
    print(f"  Total pending: {board['total_pending']}")
    print(f"  Floors summary: {board['floors_summary']}")
    print(f"  Oldest pending: {board['oldest_pending_hours']} hours")
    print()

    # Resolve one
    pending = queue.list_pending()
    if pending:
        first = pending[0]
        print(f"Resolving: {first['intent']}")
        result = veto.apply_veto(first["id"], "DENIED", "arif", "Not authorized at this time")
        print(f"  Decision: {result['decision']}")
        print(f"  Next action: {result['next_action']}")

    print()
    print(f"Remaining pending: {queue.count_pending()}")
    print()
    print("✅ HOLD Queue + Veto Surface operational")
    print()
    print("To serve API:  python3 src/hold_queue.py --serve")


VERBOSE = "-v" in os.environ.get("ARIFOS_VERBOSE", "")


if __name__ == "__main__":
    import sys

    if "--serve" in sys.argv:
        serve_api()
    else:
        demo()
