"""surface_diff.py — cross-surface conformance probe for a live MCP service.

Enumerates every read surface of ONE service, then diffs the same entity across them.
Answers: "do all surfaces say the same thing?" — not "is X there?"

Usage:
    python3 surface_diff.py http://127.0.0.1:8088/mcp
    python3 surface_diff.py http://127.0.0.1:8088/mcp --http-base http://127.0.0.1:8088

Exit codes:
    0 = all reached surfaces agree
    1 = divergence found (grid printed)
    2 = could not reach the primary surface

Read-only. Never mutates, never calls anything but list/get methods.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

PROTOCOL_VERSION = "2025-06-18"


class SurfaceProbe:
    """One MCP JSON-RPC surface, with the session id reused across calls
    so every reading comes from the same server instance."""

    def __init__(self, url: str, timeout: float = 20.0) -> None:
        self.url = url
        self.timeout = timeout
        self.session_id: str | None = None
        self._req_id = 0

    def _post(self, payload: dict) -> tuple[dict | None, str | None]:
        self._req_id += 1
        payload.setdefault("jsonrpc", "2.0")
        payload.setdefault("id", self._req_id)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["mcp-session-id"] = self.session_id
        req = urllib.request.Request(
            self.url, data=json.dumps(payload).encode(), headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                sid = resp.headers.get("mcp-session-id")
                if sid:
                    self.session_id = sid
                body = resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return None, f"{type(exc).__name__}: {exc}"
        # Streamable-HTTP servers may answer as SSE; take the last data: line.
        if body.lstrip().startswith("event:") or "\ndata:" in body:
            lines = [ln[5:].strip() for ln in body.splitlines() if ln.startswith("data:")]
            body = lines[-1] if lines else body
        try:
            return json.loads(body), None
        except json.JSONDecodeError as exc:
            return None, f"non-JSON response: {exc}"

    def initialize(self) -> str | None:
        _, err = self._post(
            {
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": {"name": "surface-diff", "version": "1.0"},
                },
            }
        )
        return err

    def list_method(self, method: str) -> tuple[list[dict], str | None]:
        """Return (items, error). Items are the raw dicts from result.<key>."""
        key = {
            "tools/list": "tools",
            "prompts/list": "prompts",
            "resources/list": "resources",
        }[method]
        data, err = self._post({"method": method, "params": {}})
        if err:
            return [], err
        if not isinstance(data, dict):
            return [], "non-object response"
        if "error" in data:
            return [], f"jsonrpc error: {str(data['error'])[:120]}"
        result = data.get("result") or {}
        items = result.get(key) or []
        return (items if isinstance(items, list) else []), None


def http_tools(base: str) -> tuple[list[dict], str | None]:
    """Convenience projection: <base>/tools."""
    url = base.rstrip("/") + "/tools"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as exc:  # noqa: BLE001 - report, never raise
        return [], f"{type(exc).__name__}: {exc}"
    items = data.get("tools") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return [], "no 'tools' array in response"
    return items, None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mcp_url", help="MCP endpoint, e.g. http://127.0.0.1:8088/mcp")
    ap.add_argument("--http-base", default=None, help="Base for HTTP projections, e.g. http://127.0.0.1:8088")
    args = ap.parse_args()

    probe = SurfaceProbe(args.mcp_url)
    err = probe.initialize()
    if err:
        print(f"UNREACHABLE primary surface {args.mcp_url}: {err}", file=sys.stderr)
        return 2

    surfaces: dict[str, list[dict]] = {}
    unreached: dict[str, str] = {}

    for method in ("tools/list", "prompts/list", "resources/list"):
        items, e = probe.list_method(method)
        if e:
            unreached[method] = e
        surfaces[method] = items

    if args.http_base:
        items, e = http_tools(args.http_base)
        if e:
            unreached["/tools (http)"] = e
        surfaces["/tools (http)"] = items

    # ---- build entity -> {surface: record} ----
    entities: dict[str, dict[str, dict]] = {}
    for surface, items in surfaces.items():
        for it in items:
            if not isinstance(it, dict):
                continue
            name = it.get("name") or it.get("uri") or it.get("title")
            if not name:
                continue
            entities.setdefault(str(name), {})[surface] = it

    print(f"# Cross-surface conformance — {args.mcp_url}")
    print(f"# surfaces reached: {len(surfaces) - len(unreached)}  unreached: {len(unreached)}")
    for name, why in unreached.items():
        print(f"#   UNREACHED  {name}: {why}")
    print()

    # ---- diff the shared descriptive fields per entity ----
    FIELDS = ("description", "stage", "stage_code", "access", "kind", "title")
    divergent = 0
    for name in sorted(entities):
        per_surface = entities[name]
        if len(per_surface) < 2:
            continue
        row: dict[str, str] = {}
        for field in FIELDS:
            vals = {
                s: rec.get(field)
                for s, rec in per_surface.items()
                if rec.get(field) is not None
            }
            if len(set(map(repr, vals.values()))) > 1:
                row[field] = " | ".join(f"{s}={v}" for s, v in vals.items())
        if row:
            divergent += 1
            print(f"DIVERGENT  {name}")
            for field, detail in row.items():
                print(f"    {field}: {detail}")

    print()
    print(f"# entities compared: {sum(1 for e in entities.values() if len(e) >= 2)}")
    print(f"# divergent: {divergent}")
    if not divergent:
        print("# all reached surfaces agree on every shared field")
    return 1 if divergent else 0


if __name__ == "__main__":
    raise SystemExit(main())
