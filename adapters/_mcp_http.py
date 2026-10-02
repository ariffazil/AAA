"""Shared streamable-HTTP MCP transport for AAA organ adapters (PR-3 ONE-DOOR).

One owner for the door plumbing. Every adapter speaks to an organ the same
way: HTTP initialize → notifications/initialized → tools/call, tolerant of
both plain-JSON and SSE (``data:``) response bodies. Stdlib only.

Read-only calls only — adapters never mutate organ state.

PR-3 ONE-DOOR (2026-10-02): AAA consumes organ *capabilities* over HTTP.
No organ filesystem paths, no sys.path insertion into organ repos, no
imports of organ python modules. Unreachable organ ⇒ typed failure, never
a guessed answer (F1 AMANAH).
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

MCP_PROTOCOL_VERSION = "2025-06-18"

_CLIENT_INFO = {"name": "aaa-adapter", "version": "1.0"}


class McpTransportError(Exception):
    """The door itself is unusable — connect failure or protocol error."""


def http_json(
    url: str,
    *,
    method: str = "GET",
    payload: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 5.0,
) -> tuple[int, dict[str, str], str]:
    """One HTTP round trip. Returns (status, response-headers, body-text).

    HTTPError (non-2xx) is returned as a status, not raised — the body may
    still carry a diagnostic. Connection-level failures raise
    McpTransportError.
    """
    req = urllib.request.Request(url, data=payload, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return (
                resp.status,
                {k.lower(): v for k, v in resp.headers.items()},
                resp.read().decode(errors="replace"),
            )
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode(errors="replace")
        except Exception:
            body = ""
        return exc.code, {k.lower(): v for k, v in exc.headers.items()}, body
    except (urllib.error.URLError, OSError) as exc:
        raise McpTransportError(f"{type(exc).__name__}: {exc}") from exc


def parse_jsonrpc_body(raw: str) -> dict[str, Any]:
    """Parse a plain-JSON or SSE (``data:`` line) JSON-RPC response body."""
    raw = (raw or "").strip()
    if not raw:
        raise McpTransportError("empty response body")
    if raw.startswith("{") or raw.startswith("["):
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise McpTransportError(f"unparseable JSON body: {exc}") from exc
    for line in raw.splitlines():
        if line.startswith("data:"):
            chunk = line[len("data:"):].strip()
            if chunk:
                try:
                    return json.loads(chunk)
                except json.JSONDecodeError as exc:
                    raise McpTransportError(f"unparseable SSE payload: {exc}") from exc
    raise McpTransportError("no JSON-RPC payload found in response")


class McpHttpSession:
    """One streamable-HTTP MCP session against an organ's ``/mcp`` endpoint."""

    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session_id: str | None = None

    def __enter__(self) -> "McpHttpSession":
        self.open()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def open(self) -> dict[str, Any]:
        """MCP initialize handshake + initialized notification."""
        status, headers, body = self._rpc(
            id_=1,
            method="initialize",
            params={
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": _CLIENT_INFO,
            },
        )
        if status not in (200, 201, 202):
            raise McpTransportError(f"initialize failed: HTTP {status} {body[:200]}")
        self.session_id = headers.get("mcp-session-id")
        if not self.session_id:
            raise McpTransportError("server issued no mcp-session-id")
        # notifications/initialized — no id, no response body expected
        self._post(
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
        )
        try:
            return parse_jsonrpc_body(body).get("result", {})
        except McpTransportError:
            return {}  # initialize result is informative, not required downstream

    def close(self) -> None:
        """Best-effort session teardown — never raises."""
        if not self.session_id:
            return
        try:
            self._post({}, extra_headers={}, delete=True)
        except Exception:
            pass
        self.session_id = None

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        """tools/call → parsed JSON payload from the first text content block.

        Returns {"_raw": text} when the organ answers with non-JSON text.
        """
        self._next_id = getattr(self, "_next_id", 1) + 1
        status, _headers, body = self._rpc(
            id_=self._next_id,
            method="tools/call",
            params={"name": name, "arguments": arguments or {}},
        )
        if status != 200:
            raise McpTransportError(f"tools/call {name}: HTTP {status}")
        envelope = parse_jsonrpc_body(body)
        if envelope.get("error"):
            raise McpTransportError(f"tools/call {name}: {envelope['error']}")
        result = envelope.get("result") or {}
        if result.get("isError"):
            raise McpTransportError(f"tool {name} reported error: {result}")
        content = result.get("content") or []
        text = ""
        for block in content:
            if isinstance(block, dict) and block.get("text"):
                text = block["text"]
                break
        if not text:
            return {}
        try:
            parsed = json.loads(text)
            return parsed if isinstance(parsed, dict) else {"_value": parsed}
        except json.JSONDecodeError:
            return {"_raw": text}

    # ── internals ───────────────────────────────────────────────────

    def _next_rpc_id(self) -> int:
        self._rpc_id = getattr(self, "_rpc_id", 1) + 1
        return self._rpc_id

    def _headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        return headers

    def _post(self, body: dict[str, Any], extra_headers: dict[str, str] | None = None,
              delete: bool = False) -> tuple[int, dict[str, str], str]:
        return http_json(
            f"{self.base_url}/mcp",
            method="DELETE" if delete else "POST",
            payload=json.dumps(body).encode(),
            headers={**self._headers(), **(extra_headers or {})},
            timeout=self.timeout,
        )

    def _rpc(self, *, id_: int, method: str, params: dict[str, Any]) -> tuple[int, dict[str, str], str]:
        status, headers, body = self._post(
            {"jsonrpc": "2.0", "id": id_, "method": method, "params": params}
        )
        if status in (200, 201, 202) and not self.session_id:
            self.session_id = headers.get("mcp-session-id")
        return status, headers, body
