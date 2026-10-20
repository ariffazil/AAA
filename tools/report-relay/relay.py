#!/usr/bin/env python3
"""
relay — the spine that keeps the human out of the agents' loop.
================================================================

Three surfaces, one door. The whole design goal: agents talk to agents by
default, the human is interrupted only when interruption is warranted, and no
agent ever needs the human as a wire.

  AGENT LANE   POST /handoff    agent -> agent. Never touches the human.
                               Filed into inbox/<to>.jsonl.
  AGENT LANE   GET  /inbox      an agent reads what was addressed to it.
  AGENT LANE   GET  /handoffs   the full agent-lane witness trail.

  HUMAN LANE   POST /report     escalation. P0/P1 held by key -> DM now.
                               P2/P3 -> digest queue, never an instant ping.
  HUMAN LANE   GET  /ledger     what was escalated, and whether it landed.
  HUMAN LANE   GET  /pending    what is waiting in the digest queue.

  MCP SURFACE  POST /mcp        a real MCP server exposing ONE tool:
                               report_to_arif. This is how chat-surface agents
                               (ChatGPT, Claude web, Grok, Perplexity) that
                               cannot make raw HTTP calls reach the relay.
                               The kernel keeps its canonical 8 verbs; the
                               relay owns transport, not governance.

Authority rule that makes the triage honest:
  - carrying the relay key  -> may declare P0/P1 and interrupt the human now
  - no key                  -> accepted, but severity is capped at P2, so an
                               unverified caller can never ring the sovereign's
                               phone; it lands in the digest with everything else

Design constraints:
  - stdlib only (no venv drift, no dependency rot)
  - fail loud: a rejected message returns why, never a silent 200
  - per-source, per-lane rate limits
  - every accepted message is appended to a jsonl witness trail
  - the human lane only ever sends to the sovereign DM

Run: python3 relay.py  (systemd: report-relay.service)
Digest flush: digest.py  (systemd timer: report-digest.timer)
"""

from __future__ import annotations

import json
import os
import re
import secrets
import threading
import time
import urllib.parse
import urllib.request
from collections import defaultdict, deque
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ── Config ────────────────────────────────────────────────────────────────────
HOST = os.environ.get("RELAY_HOST", "127.0.0.1")
PORT = int(os.environ.get("RELAY_PORT", "18101"))
KEY = os.environ.get("REPORT_RELAY_KEY", "")
TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("RELAY_CHAT_ID", "267378578")

BASE = os.environ.get("RELAY_BASE", "/var/log/report-relay")
REPORTS = os.environ.get("RELAY_LEDGER", os.path.join(BASE, "reports.jsonl"))
HANDOFFS = os.path.join(BASE, "handoffs.jsonl")
PENDING = os.path.join(BASE, "pending.jsonl")
INBOX_DIR = os.path.join(BASE, "inbox")

MAX_BODY = 12000
MAX_HANDOFF = 60000
RATE_REPORT = 20          # human-lane per source per window
RATE_HANDOFF = 200        # agent-lane per source per window
RATE_ANON = 10            # keyless MCP callers, per address per window
RATE_WINDOW = 3600
TG_LIMIT = 3900

INTERRUPT = ("P0", "P1")   # severities allowed to reach the DM immediately

_seen: dict[str, deque] = defaultdict(deque)
_lock = threading.RLock()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_name(s: str) -> str:
    s = re.sub(r"[^a-z0-9._-]", "-", s.lower().strip())
    return s[:48] or "unknown"


# ── Telegram (human lane only) ────────────────────────────────────────────────
def tg_send(text: str) -> tuple[bool, str]:
    if not TG_TOKEN:
        return False, "TELEGRAM_BOT_TOKEN not configured"
    if len(text) > TG_LIMIT:
        text = text[:TG_LIMIT] + "\n\n… [truncated by relay]"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true",
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            payload = json.loads(r.read().decode())
    except Exception as e:  # noqa: BLE001 - transport boundary
        return False, f"transport: {e.__class__.__name__}: {e}"
    if not payload.get("ok"):
        return False, f"telegram: {payload.get('description', 'unknown')}"
    return True, str(payload.get("result", {}).get("message_id", ""))


# ── Formatting ────────────────────────────────────────────────────────────────
_ESC = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}


def esc(s: str) -> str:
    for k, v in _ESC.items():
        s = s.replace(k, v)
    return s


def render(title: str, body: str, source: str, severity: str) -> str:
    sev = {"P0": "🔴 P0", "P1": "🟠 P1", "P2": "🟡 P2", "P3": "🟢 P3"}.get(severity, "⚪ P?")
    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    return f"<b>{esc(title)}</b>\n<code>{esc(source)}</code> · {sev} · {esc(stamp)}\n\n{esc(body)}"


# ── Storage ───────────────────────────────────────────────────────────────────
def append_jsonl(path: str, row: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with _lock:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: str, limit: int) -> list[dict]:
    if not os.path.exists(path):
        return []
    with _lock:
        with open(path, encoding="utf-8") as f:
            rows = [json.loads(x) for x in f if x.strip()]
    return rows[-limit:]


def rate_ok(bucket: str, source: str, limit: int) -> bool:
    now = time.time()
    with _lock:
        q = _seen[f"{bucket}:{source}"]
        while q and now - q[0] > RATE_WINDOW:
            q.popleft()
        if len(q) >= limit:
            return False
        q.append(now)
        return True


# ── Delivery with triage ──────────────────────────────────────────────────────
def deliver(title: str, body: str, source: str, severity: str, urgent_authority: bool) -> dict:
    """
    Route one human-lane message.

    urgent_authority=True  -> the caller proved it holds the key.
    urgent_authority=False -> keyless (e.g. a chat-surface agent). Cannot ring.
    """
    if severity in INTERRUPT and urgent_authority:
        ok, detail = tg_send(render(title, body, source, severity))
        return {"delivered": "telegram" if ok else "failed", "message_id": detail if ok else None,
                "error": None if ok else detail, "queued": False}

    row = {
        "ts": now_iso(), "id": secrets.token_hex(8),
        "source": source, "severity": severity, "title": title,
        "body": body, "chars": len(body),
    }
    append_jsonl(PENDING, row)
    return {"delivered": "digest", "message_id": None, "error": None, "queued": True, "id": row["id"]}


# ── MCP surface (one tool) ────────────────────────────────────────────────────
MCP_TOOL = {
    "name": "report_to_arif",
    "description": (
        "Send a finding to Arif, the human principal of this system. "
        "Use this to hand off a concluded piece of work, not to chat. "
        "P0/P1 are reserved for immediate harm, data loss, a live security hole, "
        "or a decision only a human may make; anything else is queued into a digest "
        "so his attention is not spent on status updates. "
        "Returns a receipt with the delivery channel."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "One-line headline, max ~80 chars."},
            "body": {"type": "string", "description": "The finding. Verdict first, evidence second, caveats last. Max 12000 chars."},
            "severity": {
                "type": "string",
                "enum": ["P0", "P1", "P2", "P3"],
                "description": "P0 immediate harm/data loss/live security hole; P1 needs him today; P2 normal finding; P3 FYI.",
            },
            "source": {"type": "string", "description": "Who you are, e.g. chatgpt / claude-web / geox."},
        },
        "required": ["title", "body"],
    },
    "annotations": {"readOnlyHint": False, "destructiveHint": False, "openWorldHint": True},
}


def mcp_response(req_id, result: dict | None = None, error: dict | None = None) -> dict:
    out = {"jsonrpc": "2.0", "id": req_id}
    if error:
        out["error"] = error
    else:
        out["result"] = result or {}
    return out


# ── HTTP ──────────────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    server_version = "relay/3.0"

    def log_message(self, format, *args):  # noqa: A002 - stdlib signature
        print(f"{self.address_string()} {format % args}", flush=True)

    def _json(self, code: int, obj: dict) -> None:
        raw = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _has_key(self) -> bool:
        return bool(KEY) and secrets.compare_digest(
            self.headers.get("X-Report-Key", ""), KEY
        )

    def _auth(self) -> bool:
        if not KEY:
            self._json(503, {"ok": False, "error": "relay key not configured"})
            return False
        if not self._has_key():
            self._json(401, {"ok": False, "error": "bad or missing X-Report-Key"})
            return False
        return True

    def _read_body(self, cap: int) -> dict | None:
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length <= 0:
            self._json(400, {"ok": False, "error": "empty body"})
            return None
        if length > cap * 4:
            self._json(413, {"ok": False, "error": f"body too large (>{cap * 4} bytes)"})
            return None
        try:
            obj = json.loads(self.rfile.read(length).decode("utf-8", "replace"))
        except Exception as e:  # noqa: BLE001
            self._json(400, {"ok": False, "error": f"invalid json: {e}"})
            return None
        if not isinstance(obj, dict):
            self._json(400, {"ok": False, "error": "body must be a JSON object"})
            return None
        return obj

    def _route(self) -> str:
        p = self.path.split("?")[0]
        return p[len("/report"):] if p.startswith("/report/") else p

    def _qs(self) -> dict:
        return urllib.parse.parse_qs(self.path.split("?", 1)[1]) if "?" in self.path else {}

    def _limit(self, default: int = 20) -> int:
        try:
            return max(1, min(int(self._qs().get("n", [str(default)])[0]), 200))
        except ValueError:
            return default

    # ---- GET -----------------------------------------------------------
    def do_GET(self) -> None:  # noqa: N802
        path = self._route()

        if path in ("/health", ""):
            self._json(200, {
                "ok": True,
                "service": "relay",
                "surfaces": {
                    "agent": ["/handoff", "/inbox", "/handoffs"],
                    "human": ["/report", "/ledger", "/pending"],
                    "mcp": ["/mcp"],
                },
            })
            return

        if not self._auth():
            return

        n = self._limit()

        if path == "/ledger":
            rows = read_jsonl(REPORTS, n)
            self._json(200, {"ok": True, "lane": "human", "count": len(rows), "reports": rows})
            return

        if path == "/pending":
            rows = read_jsonl(PENDING, n)
            self._json(200, {"ok": True, "lane": "digest", "count": len(rows), "pending": rows})
            return

        if path == "/inbox":
            agent = safe_name(self._qs().get("agent", [""])[0])
            if agent == "unknown":
                self._json(400, {"ok": False, "error": "?agent=<your id> required"})
                return
            rows = read_jsonl(os.path.join(INBOX_DIR, f"{agent}.jsonl"), n)
            self._json(200, {"ok": True, "lane": "agent", "agent": agent,
                             "count": len(rows), "messages": rows})
            return

        if path == "/handoffs":
            rows = read_jsonl(HANDOFFS, n)
            self._json(200, {"ok": True, "lane": "agent", "count": len(rows), "handoffs": rows})
            return

        self._json(404, {"ok": False, "error": "not found"})

    # ---- POST ----------------------------------------------------------
    def do_POST(self) -> None:  # noqa: N802
        path = self._route()

        if path == "/mcp":
            self._mcp()
            return

        if path not in ("/report", "/handoff"):
            self._json(404, {"ok": False, "error": "not found"})
            return
        if not self._auth():
            return
        if path == "/handoff":
            self._handoff()
        else:
            self._report()

    # ---- human lane ----------------------------------------------------
    def _report(self) -> None:
        payload = self._read_body(MAX_BODY)
        if payload is None:
            return
        title = str(payload.get("title") or "").strip()
        body = str(payload.get("body") or payload.get("text") or "").strip()
        source = re.sub(r"[^\w .:/@-]", "", str(payload.get("source") or "unknown"))[:60] or "unknown"
        severity = str(payload.get("severity") or "P2").upper()
        if severity not in ("P0", "P1", "P2", "P3"):
            severity = "P2"

        missing = [k for k, v in (("title", title), ("body", body)) if not v]
        if missing:
            self._json(400, {"ok": False, "error": "missing required", "fields": missing})
            return
        if len(body) > MAX_BODY:
            self._json(413, {"ok": False, "error": f"body exceeds {MAX_BODY} chars", "got": len(body)})
            return
        if not rate_ok("report", source, RATE_REPORT):
            append_jsonl(REPORTS, {"ts": now_iso(), "source": source, "severity": severity,
                                   "title": title, "accepted": False, "reason": "rate_limited"})
            self._json(429, {"ok": False, "error": f"rate limit: {RATE_REPORT}/{RATE_WINDOW}s per source"})
            return

        out = deliver(title, body, source, severity, urgent_authority=True)
        append_jsonl(REPORTS, {
            "ts": now_iso(), "source": source, "severity": severity, "title": title,
            "chars": len(body), "accepted": out["error"] is None,
            "delivered": out["delivered"], "message_id": out["message_id"], "error": out["error"],
        })
        if out["error"]:
            self._json(502, {"ok": False, "error": out["error"]})
            return
        self._json(200, {"ok": True, "lane": "human", **out})

    # ---- agent lane ----------------------------------------------------
    def _handoff(self) -> None:
        payload = self._read_body(MAX_HANDOFF)
        if payload is None:
            return
        to = safe_name(str(payload.get("to") or ""))
        frm = safe_name(str(payload.get("from") or "unknown"))
        subject = str(payload.get("subject") or "").strip()
        body = str(payload.get("body") or payload.get("text") or "").strip()
        ref = str(payload.get("ref") or "").strip()[:200]
        wants_human = bool(payload.get("escalate_human", False))

        if to == "unknown":
            self._json(400, {"ok": False, "error": "missing required", "fields": ["to"]})
            return
        if not body:
            self._json(400, {"ok": False, "error": "missing required", "fields": ["body"]})
            return
        if len(body) > MAX_HANDOFF:
            self._json(413, {"ok": False, "error": f"body exceeds {MAX_HANDOFF} chars", "got": len(body)})
            return
        if not rate_ok("handoff", frm, RATE_HANDOFF):
            self._json(429, {"ok": False, "error": f"rate limit: {RATE_HANDOFF}/{RATE_WINDOW}s per source"})
            return

        row = {
            "ts": now_iso(), "id": secrets.token_hex(8),
            "to": to, "from": frm, "subject": subject or "(no subject)",
            "body": body, "ref": ref, "chars": len(body),
        }
        append_jsonl(os.path.join(INBOX_DIR, f"{to}.jsonl"), row)
        append_jsonl(HANDOFFS, {k: row[k] for k in ("ts", "id", "to", "from", "subject", "ref", "chars")})

        escalated = False
        if wants_human:
            out = deliver(
                f"[{frm} → {to}] {row['subject']}",
                f"{body}\n\n— handoff {row['id']}" + (f"\nref: {ref}" if ref else ""),
                frm, "P2", urgent_authority=True,
            )
            escalated = out["delivered"] == "telegram"

        self._json(200, {
            "ok": True, "lane": "agent", "id": row["id"], "to": to,
            "escalated_to_human": escalated,
        })

    # ---- MCP -----------------------------------------------------------
    def _mcp(self) -> None:
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        raw = self.rfile.read(length) if length > 0 else b""
        try:
            msg = json.loads(raw.decode("utf-8", "replace")) if raw else {}
        except Exception:  # noqa: BLE001
            self._json(200, mcp_response(None, error={"code": -32700, "message": "parse error"}))
            return

        method = msg.get("method", "")
        req_id = msg.get("id")

        # notifications carry no id and expect no reply
        if req_id is None and method.startswith("notifications/"):
            self.send_response(202)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        if method == "initialize":
            result = {
                "protocolVersion": "2025-06-18",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "arifOS relay", "version": "relay-3.0"},
                "instructions": (
                    "One tool: report_to_arif. Send a concluded finding to the human "
                    "principal. P0/P1 are for genuine interruption only; everything "
                    "else is digested. This surface carries no governance authority — "
                    "for verdicts, use the arifOS kernel MCP server."
                ),
            }
        elif method == "tools/list":
            result = {"tools": [MCP_TOOL]}
        elif method == "ping":
            result = {}
        elif method in ("resources/list", "prompts/list"):
            result = {"resources": [], "prompts": []} if method.startswith("resources") else {"prompts": []}
        elif method == "tools/call":
            params = msg.get("params") or {}
            if params.get("name") != "report_to_arif":
                self._json(200, mcp_response(req_id, error={
                    "code": -32602, "message": f"unknown tool: {params.get('name')}"}))
                return
            args = params.get("arguments") or {}
            title = str(args.get("title") or "").strip()
            body = str(args.get("body") or "").strip()
            severity = str(args.get("severity") or "P2").upper()
            source = re.sub(r"[^\w .:/@-]", "", str(args.get("source") or "mcp-client"))[:60] or "mcp-client"
            if severity not in ("P0", "P1", "P2", "P3"):
                severity = "P2"

            if not title or not body:
                self._json(200, mcp_response(req_id, {
                    "content": [{"type": "text", "text": "rejected: title and body are required"}],
                    "isError": True,
                }))
                return
            if len(body) > MAX_BODY:
                self._json(200, mcp_response(req_id, {
                    "content": [{"type": "text",
                                 "text": f"rejected: body exceeds {MAX_BODY} chars (got {len(body)})"}],
                    "isError": True,
                }))
                return

            verified = self._has_key()
            addr = self.client_address[0]
            if not verified:
                # keyless callers cannot interrupt the human, and cannot spam
                if severity in INTERRUPT:
                    severity = "P2"
                source = f"ext:{source}"
                if not rate_ok("anon", addr, RATE_ANON):
                    self._json(200, mcp_response(req_id, {
                        "content": [{"type": "text", "text": "rate limited: 10/hour per address"}],
                        "isError": True,
                    }))
                    return
            elif not rate_ok("report", source, RATE_REPORT):
                self._json(200, mcp_response(req_id, {
                    "content": [{"type": "text", "text": f"rate limited: {RATE_REPORT}/hour"}],
                    "isError": True,
                }))
                return

            out = deliver(title, body, source, severity, urgent_authority=verified)
            append_jsonl(REPORTS, {
                "ts": now_iso(), "source": source, "severity": severity, "title": title,
                "chars": len(body), "accepted": out["error"] is None,
                "delivered": out["delivered"], "message_id": out["message_id"],
                "channel": "mcp", "verified": verified, "error": out["error"],
            })
            receipt = {
                "ok": out["error"] is None,
                "channel": out["delivered"],
                "severity_used": severity,
                "verified_caller": verified,
                "queued": out["queued"],
                "message_id": out["message_id"],
                "note": ("delivered to the human now" if out["delivered"] == "telegram"
                         else "queued for the next digest — the human is not interrupted for this"),
            }
            if out["error"]:
                receipt["error"] = out["error"]
            self._json(200, mcp_response(req_id, {
                "content": [{"type": "text", "text": json.dumps(receipt, ensure_ascii=False)}],
                "structuredContent": receipt,
                "isError": out["error"] is not None,
            }))
            return
        else:
            self._json(200, mcp_response(req_id, error={
                "code": -32601, "message": f"method not found: {method}"}))
            return

        self._json(200, mcp_response(req_id, result))


def main() -> None:
    if not KEY:
        raise SystemExit("REPORT_RELAY_KEY is required")
    if not TG_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN is required")
    os.makedirs(INBOX_DIR, exist_ok=True)
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"relay http://{HOST}:{PORT} | human->telegram {CHAT_ID} | agent->{INBOX_DIR} | mcp /mcp", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
