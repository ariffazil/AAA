#!/usr/bin/env python3
"""
organ_counts.py — count-only organ projection for the public edge
═════════════════════════════════════════════════════════════════
Serves a MINIMUM NECESSARY MEANING projection of each organ's health and tool
inventory, so the public dashboards keep working while the full payloads stop
being readable by anonymous callers.

WHY THIS EXISTS (measured 2026-10-03)
    arifos.arif-fazil.com/api/organs/a-forge/health returned 24 top-level keys
    to any anonymous cross-origin caller, including:
        identity, identity_hash, authority_ceiling, final_authority,
        source_commit, deployed_commit, apex_scalars, act_mutation_gate,
        federation_geometry, owner_summary, deployment_drift
    The single consumer — /var/www/html/shared/arrow-of-time-body.js:115 — reads
    exactly ONE field: `forge.ok === true`. So ~23 keys of governance internals
    were published to serve a boolean.
    /api/organs/*/tools was worse (13,357 B of full schema on arifos., 48,273 B
    on mcp.) and had NO consumer at all: a grep of /var/www/html for
    `api/organs/*/tools` returns zero pages.

DESIGN: ALLOWLIST, NOT BLOCKLIST
    Only the fields named in HEALTH_FIELDS ever leave this process. A blocklist
    (strip identity, strip hashes, ...) leaks every field a future organ adds,
    silently, the day it is added. An allowlist fails closed instead: a new
    upstream field simply does not appear until someone decides it should.

FAIL-CLOSED
    An unreachable organ yields HTTP 502 with {"ok": false, "status":
    "UNREACHABLE"}. It never yields a cached, default, or synthesised "ok": true.
    A stale health pane that reports LIVE for a dead lane is worse than no pane.
    Every response carries generated_at and upstream_ms so freshness is visible
    rather than assumed — the frozen-instrument defect this pass exists to remove.

LIVE, NOT CACHED
    Each request hits the organ. Tool counts change on deploy; a counts file
    refreshed on a timer is a cached number wearing a timestamp, and the moment
    it drifts it is a lie with a receipt. Nothing here is stored.

Forged 2026-10-03 by FI-003 (F13 order: "fix arifos. too with the count-only
endpoint"). DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 18108
BIND = "127.0.0.1"          # edge-only: Caddy is the sole intended client
UPSTREAM_TIMEOUT_S = 5

# Organ → upstream port. Mirrors the live mapping in
# /etc/caddy/vhosts/mcp.arif-fazil.com.conf, including the alias spellings the
# estate actually uses (a-forge / aforge / forge all denote A-FORGE).
ORGAN_PORTS = {
    "arifos": 8088,
    "aforge": 7071,
    "a-forge": 7071,
    "forge": 7071,
    "geox": 8081,
    "wealth": 18082,
    "well": 18083,
}

# Allowlist. `ok` first because it is the only field with a confirmed consumer.
HEALTH_FIELDS = ("ok", "service", "status", "tool_count", "tools_loaded")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _fetch(port: int, path: str) -> tuple[dict | None, float, str | None]:
    """Live upstream read. Returns (json_or_None, elapsed_ms, error_or_None)."""
    t0 = time.monotonic()
    url = f"http://127.0.0.1:{port}{path}"
    try:
        with urllib.request.urlopen(url, timeout=UPSTREAM_TIMEOUT_S) as r:
            raw = r.read()
        ms = (time.monotonic() - t0) * 1000.0
        return json.loads(raw), ms, None
    except urllib.error.HTTPError as e:
        return None, (time.monotonic() - t0) * 1000.0, f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001 — any failure must degrade honestly
        return None, (time.monotonic() - t0) * 1000.0, f"{type(e).__name__}: {e}"


def project_health(organ: str) -> tuple[int, dict]:
    port = ORGAN_PORTS.get(organ)
    if port is None:
        return 404, {"ok": False, "organ": organ, "status": "UNKNOWN_ORGAN",
                     "generated_at": _now()}
    data, ms, err = _fetch(port, "/health")
    if data is None or not isinstance(data, dict):
        return 502, {"ok": False, "organ": organ, "status": "UNREACHABLE",
                     "error": err, "upstream_ms": round(ms, 1),
                     "generated_at": _now()}
    out = {"organ": organ, "generated_at": _now(), "upstream_ms": round(ms, 1)}
    for k in HEALTH_FIELDS:
        if k in data:
            out[k] = data[k]

    # `ok` derivation. Only A-FORGE emits an explicit `ok`; arifos/geox/well/
    # wealth answer with `status` instead. Defaulting those to ok:false (the
    # first draft did) reported healthy organs as broken — a wrong signal is not
    # the same as a fail-closed one. So: trust `ok` when present, else derive
    # from `status`, else report that neither exists. ok_source makes the
    # derivation visible instead of implicit.
    if "ok" in data:
        out["ok_source"] = "organ_field"
    else:
        st = str(data.get("status", "")).strip().lower()
        if st:
            out["ok"] = st in ("healthy", "ok", "up", "ready")
            out["ok_source"] = f"derived_from_status={data.get('status')!r}"
        else:
            out["ok"] = False
            out["ok_source"] = "unavailable_no_ok_or_status"
    out["fields_withheld"] = max(0, len(data) - len([k for k in HEALTH_FIELDS if k in data]))
    return 200, out


def project_tools(organ: str) -> tuple[int, dict]:
    port = ORGAN_PORTS.get(organ)
    if port is None:
        return 404, {"organ": organ, "status": "UNKNOWN_ORGAN",
                     "generated_at": _now()}
    data, ms, err = _fetch(port, "/tools")
    if data is None or not isinstance(data, dict):
        return 502, {"organ": organ, "status": "UNREACHABLE", "error": err,
                     "upstream_ms": round(ms, 1), "generated_at": _now()}
    tools = data.get("tools")
    n = len(tools) if isinstance(tools, list) else None
    return 200, {
        "organ": organ,
        "tool_count": n,
        "generated_at": _now(),
        "upstream_ms": round(ms, 1),
        # A count is the disclosure budget here. Names and schemas are not
        # served: the caller has no consumer that needs them, and MCP clients
        # that legitimately do can call tools/list on the governed door.
        "withheld": ["tool_names", "tool_schemas"],
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "organ-counts/1.0"

    def _send(self, code: int, body: dict) -> None:
        raw = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802 — http.server API
        parts = [p for p in self.path.split("?")[0].split("/") if p]
        if parts[:1] == ["organs"] and len(parts) == 3:
            organ, kind = parts[1].lower(), parts[2].lower()
            if kind == "health":
                code, body = project_health(organ)
                return self._send(code, body)
            if kind == "tools":
                code, body = project_tools(organ)
                return self._send(code, body)
        if parts == ["health"]:
            return self._send(200, {"status": "ok", "service": "organ-counts",
                                    "organs": sorted(set(ORGAN_PORTS)),
                                    "generated_at": _now()})
        self._send(404, {"error": "expected /organs/<organ>/(health|tools)",
                         "organs": sorted(set(ORGAN_PORTS))})

    def log_message(self, fmt, *args) -> None:  # keep the journal quiet
        pass


def main() -> None:
    srv = ThreadingHTTPServer((BIND, PORT), Handler)
    print(f"organ-counts listening on {BIND}:{PORT} — allowlist projection, "
          f"organs={sorted(set(ORGAN_PORTS))}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
