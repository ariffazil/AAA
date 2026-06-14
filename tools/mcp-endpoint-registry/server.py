#!/root/arifOS/.venv/bin/python
"""
MCP Endpoint Registry Wrapper — thin read-only query surface over the canonical
mcp-endpoint-registry.md source of truth.

Tools:
  mcp_endpoint_list     — parse registry, return structured endpoint records
  mcp_endpoint_health   — curl each endpoint's health URL, cache result
  mcp_endpoint_validate — deeper check: MCP initialize + tools/list handshake

Health snapshots write to .cache/endpoint-health.json (computed, disposable).
NEVER touches the canonical markdown file.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

# ── paths ──────────────────────────────────────────────────────────────
REGISTRY_MD = Path("/root/AAA/docs/mcp-endpoint-registry.md")
CACHE_DIR = Path(__file__).resolve().parent / ".cache"
CACHE_FILE = CACHE_DIR / "endpoint-health.json"

# ── server ─────────────────────────────────────────────────────────────
mcp = FastMCP("mcp-endpoint-registry")

# ═══════════════════════════════════════════════════════════════════════
# Markdown Parser
# ═══════════════════════════════════════════════════════════════════════

def _parse_registry() -> list[dict[str, str]]:
    """Parse the canonical markdown registry into a list of endpoint records."""
    if not REGISTRY_MD.exists():
        return []

    text = REGISTRY_MD.read_text()
    endpoints: list[dict[str, str]] = []
    current: dict[str, str] = {}
    in_table = False

    for line in text.splitlines():
        # New endpoint section: ### Name
        if line.startswith("### ") and not line.startswith("#### "):
            if current and "name" in current:
                endpoints.append(_clean_record(current))
            current = {"category": line[4:].strip()}
            in_table = False
            continue

        # Table header row
        if line.strip().startswith("| Property") and "Value" in line:
            in_table = True
            continue
        # Separator row
        if line.strip().startswith("|---") or line.strip().startswith("|--"):
            continue

        # Table data row
        if in_table and line.strip().startswith("|"):
            parts = [p.strip() for p in line.strip().split("|")]
            if len(parts) >= 3:
                key = parts[1].strip()
                val = parts[2].strip()
                # Strip backtick formatting
                val = val.strip("`")
                # Map property names to canonical keys
                _map_property(current, key, val)

        # End of table
        if in_table and not line.strip().startswith("|"):
            in_table = False

    # Don't miss the last one
    if current and "name" in current:
        endpoints.append(_clean_record(current))

    return endpoints


def _map_property(record: dict, key: str, val: str) -> None:
    """Map a markdown table property to a canonical record key."""
    key_lower = key.lower().replace(" ", "_")
    mapping = {
        "name": "name",
        "public_url": "url",
        "transport": "transport",
        "internal": "internal_url",
        "container_port": "port",
        "caddy_route": "caddy_route",
        "tools": "tools",
        "auth": "auth",
        "status": "declared_status",
        "note": "note",
    }
    canonical = mapping.get(key_lower, key_lower)
    record[canonical] = val


def _clean_record(record: dict) -> dict[str, str]:
    """Normalize keys; ensure 'name' and 'url' are present."""
    if "name" not in record:
        # Derive name from category
        record["name"] = record.get("category", "unknown").split("(")[0].strip()
    if "url" not in record:
        record["url"] = ""
    record.setdefault("transport", "unknown")
    record.setdefault("port", "")
    record.setdefault("declared_status", "UNKNOWN")
    return record


# ═══════════════════════════════════════════════════════════════════════
# Health Cache
# ═══════════════════════════════════════════════════════════════════════

def _load_cache() -> dict:
    """Load health cache from disk (computed state, not canonical truth)."""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_cache(data: dict) -> None:
    """Write health cache to disk."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(data, indent=2, default=str))


def _derive_health_url(record: dict) -> str | None:
    """Derive a /health endpoint URL from the public or internal URL."""
    url = record.get("url", "") or record.get("internal_url", "")
    if not url:
        return None
    # If URL ends with /mcp, replace with /health
    if "/mcp" in url:
        return url.rsplit("/mcp", 1)[0] + "/health"
    # Otherwise append /health
    base = url.rstrip("/")
    return f"{base}/health"


def _curl_health(url: str, timeout: int = 5) -> dict:
    """Run a non-mutating health check via curl. Returns {status, code, latency_ms, error}."""
    start = time.monotonic()
    try:
        result = subprocess.run(
            ["curl", "-sf", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", str(timeout), url],
            capture_output=True, text=True, timeout=timeout + 2,
        )
        latency_ms = round((time.monotonic() - start) * 1000)
        code = result.stdout.strip()
        return {
            "status": "UP" if code and code[0] == "2" else "DEGRADED",
            "http_code": int(code) if code.isdigit() else 0,
            "latency_ms": latency_ms,
            "error": None,
        }
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError) as exc:
        latency_ms = round((time.monotonic() - start) * 1000)
        return {
            "status": "DOWN",
            "http_code": 0,
            "latency_ms": latency_ms,
            "error": str(exc)[:200],
        }


def _mcp_handshake(url: str, timeout: int = 5) -> dict:
    """Attempt an MCP initialize → tools/list handshake. Returns {mcp_alive, tools_count, error}."""
    try:
        # Initialize
        init_payload = json.dumps({
            "jsonrpc": "2.0", "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "mcp-endpoint-registry", "version": "1.0.0"}
            },
            "id": 1
        })
        result = subprocess.run(
            ["curl", "-sf", "-X", "POST", url,
             "-H", "Content-Type: application/json",
             "-H", "Accept: application/json, text/event-stream",
             "-d", init_payload,
             "--max-time", str(timeout)],
            capture_output=True, text=True, timeout=timeout + 2,
        )
        if result.returncode != 0:
            return {"mcp_alive": False, "tools_count": 0, "error": f"curl failed: {result.stderr[:200]}"}

        # Try to extract server info from the response
        body = result.stdout.strip()
        # SSE responses may have "data:" prefix
        if "data:" in body:
            # Extract JSON from SSE
            json_match = re.search(r'\{.*\}', body, re.DOTALL)
            if json_match:
                body = json_match.group(0)

        try:
            init_data = json.loads(body)
        except json.JSONDecodeError:
            return {"mcp_alive": False, "tools_count": 0, "error": f"bad JSON response: {body[:200]}"}

        server_info = init_data.get("result", {}).get("serverInfo", {})
        protocol = init_data.get("result", {}).get("protocolVersion", "unknown")

        # Now send a tools/list
        list_payload = json.dumps({
            "jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 2
        })
        result2 = subprocess.run(
            ["curl", "-sf", "-X", "POST", url,
             "-H", "Content-Type: application/json",
             "-d", list_payload,
             "--max-time", str(timeout)],
            capture_output=True, text=True, timeout=timeout + 2,
        )
        tools_count = 0
        if result2.returncode == 0:
            try:
                body2 = result2.stdout.strip()
                if "data:" in body2:
                    json_match = re.search(r'\{.*\}', body2, re.DOTALL)
                    if json_match:
                        body2 = json_match.group(0)
                tools_data = json.loads(body2)
                tools_count = len(tools_data.get("result", {}).get("tools", []))
            except (json.JSONDecodeError, KeyError):
                pass

        return {
            "mcp_alive": True,
            "tools_count": tools_count,
            "protocol_version": protocol,
            "server_name": server_info.get("name", "unknown"),
            "server_version": server_info.get("version", "unknown"),
            "error": None,
        }

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError) as exc:
        return {"mcp_alive": False, "tools_count": 0, "error": str(exc)[:200]}


# ═══════════════════════════════════════════════════════════════════════
# Tools
# ═══════════════════════════════════════════════════════════════════════

@mcp.tool()
def mcp_endpoint_list(category: str = "") -> str:
    """List all MCP endpoints from the canonical registry.

    Returns structured JSON with name, url, transport, port, declared_status,
    auth, and tools for every registered endpoint.

    Args:
        category: Optional filter — only return endpoints whose name or category
                  contains this string (case-insensitive).
    """
    endpoints = _parse_registry()
    if category:
        q = category.lower()
        endpoints = [
            e for e in endpoints
            if q in e.get("name", "").lower() or q in e.get("category", "").lower()
        ]

    summary = {
        "total": len(endpoints),
        "filter": category or None,
        "endpoints": endpoints,
    }
    return json.dumps(summary, indent=2)


@mcp.tool()
def mcp_endpoint_health(name: str = "") -> str:
    """Check health of registered MCP endpoints via HTTP GET /health.

    Results are written to the health cache (.cache/endpoint-health.json).
    Never modifies the canonical markdown registry.

    Args:
        name: Optional endpoint name filter (case-insensitive substring match).
              Omit to check all endpoints.
    """
    endpoints = _parse_registry()
    if name:
        q = name.lower()
        endpoints = [e for e in endpoints if q in e.get("name", "").lower()]

    cache = _load_cache()
    results = []
    for ep in endpoints:
        health_url = _derive_health_url(ep)
        if not health_url:
            r = {"name": ep["name"], "status": "NO_HEALTH_URL", "http_code": 0, "latency_ms": 0, "error": "No URL to derive health endpoint from"}
        else:
            r = _curl_health(health_url)
            r["health_url"] = health_url
        r["name"] = ep["name"]
        r["checked_at"] = datetime.now(timezone.utc).isoformat()

        # Update cache keyed by endpoint name
        cache[ep["name"]] = {
            "name": ep["name"],
            "url": ep.get("url", ""),
            "status": r["status"],
            "http_code": r.get("http_code", 0),
            "latency_ms": r.get("latency_ms", 0),
            "last_checked": r["checked_at"],
            "error": r.get("error"),
        }
        results.append(r)

    _save_cache(cache)

    summary = {
        "checked": len(results),
        "up": sum(1 for r in results if r["status"] == "UP"),
        "degraded": sum(1 for r in results if r["status"] == "DEGRADED"),
        "down": sum(1 for r in results if r["status"] in ("DOWN", "NO_HEALTH_URL")),
        "results": results,
    }
    return json.dumps(summary, indent=2)


@mcp.tool()
def mcp_endpoint_validate(name: str = "") -> str:
    """Validate MCP endpoints by performing an initialize + tools/list handshake.

    Goes deeper than health check: verifies the endpoint actually speaks MCP
    and returns a tool count. Results are NOT cached — this is an active probe.

    Args:
        name: Endpoint name filter (case-insensitive substring match).
              Omit to validate all endpoints.
    """
    endpoints = _parse_registry()
    if name:
        q = name.lower()
        endpoints = [e for e in endpoints if q in e.get("name", "").lower()]

    results = []
    for ep in endpoints:
        url = ep.get("url") or ep.get("internal_url", "")
        if not url:
            results.append({
                "name": ep["name"],
                "mcp_alive": False,
                "tools_count": 0,
                "error": "No URL found in registry",
            })
            continue

        r = _mcp_handshake(url)
        r["name"] = ep["name"]
        r["url"] = url
        r["validated_at"] = datetime.now(timezone.utc).isoformat()
        results.append(r)

    summary = {
        "validated": len(results),
        "mcp_alive": sum(1 for r in results if r.get("mcp_alive")),
        "mcp_dead": sum(1 for r in results if not r.get("mcp_alive")),
        "results": results,
    }
    return json.dumps(summary, indent=2)


# ═══════════════════════════════════════════════════════════════════════
# Entry
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    mcp.run()
