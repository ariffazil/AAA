#!/usr/bin/env python3
"""arifOS Federation Conformance Suite v2 — registry-driven."""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = ROOT / "mcp-surface-registry.yaml"


def _load_registry() -> dict[str, dict[str, object]]:
    if not REGISTRY_PATH.exists():
        raise SystemExit(f"missing registry: {REGISTRY_PATH}")

    with REGISTRY_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    organs = data.get("organs", {})
    canonical: dict[str, dict[str, object]] = {}
    for organ, spec in organs.items():
        tools = list(spec.get("canonical_tools") or spec.get("tools") or [])
        canonical[organ] = {
            "port": int(spec["port"]),
            "role": str(spec.get("role", "")),
            "transport": str(spec.get("transport", "")),
            "internal_tools": int(spec.get("internal_tools", 0) or 0),
            "tools": tools,
        }
    return canonical


CANONICAL = _load_registry()


def fetch_tools(port: int) -> list[str] | None:
    """Fetch tools/list with proper MCP handshake (stateless-aware)."""
    try:
        body = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "conformance-v2", "version": "1.0"},
                },
            }
        ).encode()
        req = urllib.request.Request(
            f"http://localhost:{port}/mcp",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        sid = resp.headers.get("Mcp-Session-Id") or resp.headers.get("mcp-session-id")
        resp.read()

        if sid:
            try:
                n = urllib.request.Request(
                    f"http://localhost:{port}/mcp",
                    data=json.dumps(
                        {"jsonrpc": "2.0", "method": "notifications/initialized"}
                    ).encode(),
                    headers={
                        "Content-Type": "application/json",
                        "Mcp-Session-Id": sid,
                    },
                    method="POST",
                )
                urllib.request.urlopen(n, timeout=5).read()
            except Exception:
                pass

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if sid:
            headers["Mcp-Session-Id"] = sid
        request = urllib.request.Request(
            f"http://localhost:{port}/mcp",
            data=json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}).encode(),
            headers=headers,
            method="POST",
        )
        response = urllib.request.urlopen(request, timeout=10)
        payload = json.loads(response.read())
        return [t["name"] for t in payload.get("result", {}).get("tools", [])]
    except Exception:
        return None


results = []
for organ, spec in CANONICAL.items():
    port = int(spec["port"])
    expected = set(spec["tools"])
    if spec.get("transport") == "N/A" or not expected:
        results.append(("CT-01", "tool_count", "SKIP", organ, "A2A-only surface; no MCP tools/list contract"))
        results.append(("CT-02", "name_equality", "SKIP", organ, "A2A-only surface; no MCP tools/list contract"))
        continue
    actual = fetch_tools(port)

    if actual is None:
        results.append(("CT-01", "connect", "ERROR", organ, "Cannot reach MCP"))
        continue

    actual_set = set(actual)
    results.append(("CT-01", f"tool_count ({len(actual)})", "PASS" if actual else "FAIL", organ, ""))

    missing = expected - actual_set
    extra = actual_set - expected
    if not missing:
        results.append(("CT-02", "name_equality", "PASS", organ, f"All {len(expected)} match"))
    else:
        parts = []
        if missing:
            parts.append(f"missing:{sorted(missing)[:5]}")
        if extra:
            parts.append(f"extra:{sorted(extra)[:5]}")
        results.append(("CT-02", "name_equality", "FAIL", organ, "; ".join(parts)))
    if extra and not missing:
        results.append(("CT-02", "extra_tools", "PASS", organ, f"Allowed internal extras: {len(extra)}"))

# CT-06: Evidence envelope (WEALTH safe call)
try:
    body = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "capital_primitive",
                "arguments": {"mode": "kelly", "win_prob": 0.55, "odds": 2.0},
            },
        }
    ).encode()
    req = urllib.request.Request(
        "http://localhost:18082/mcp",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        method="POST",
    )
    resp = urllib.request.urlopen(req, timeout=15)
    d = json.loads(resp.read())
    content = d.get("result", {}).get("content", [])
    if content:
        inner = json.loads(content[0].get("text", "{}"))
        if "tool_name" in inner:
            results.append(("CT-06", "envelope", "PASS", "wealth", f"tool_name={inner['tool_name']}"))
        else:
            results.append(("CT-06", "envelope", "FAIL", "wealth", f"keys={list(inner.keys())[:5]}"))
except Exception as e:
    results.append(("CT-06", "envelope", "ERROR", "wealth", str(e)[:80]))

# CT-10: Phantom detection
actual_well = fetch_tools(int(CANONICAL["well"]["port"]))
if actual_well:
    phantoms = [t for t in actual_well if t not in set(CANONICAL["well"]["tools"])]
    if phantoms:
        results.append(("CT-10", "phantom_check", "FAIL", "well", f"{len(phantoms)} phantoms: {phantoms[:3]}"))
    else:
        results.append(("CT-10", "phantom_check", "PASS", "well", "0 phantoms"))

# Report
print("=" * 60)
print("CONFORMANCE SUITE v2")
print("=" * 60)
icons = {"PASS": "✅", "FAIL": "❌", "ERROR": "💥"}
icons["SKIP"] = "➖"
for tid, name, status, organ, detail in results:
    print(f"  {icons.get(status, '?')} {tid} {name} [{organ}]: {status}")
    if detail:
        print(f"     {detail}")

p = sum(1 for r in results if r[2] == "PASS")
f = sum(1 for r in results if r[2] == "FAIL")
e = sum(1 for r in results if r[2] == "ERROR")
print(f"\n  PASS:{p} FAIL:{f} ERROR:{e} TOTAL:{len(results)}")
print(f"  VERDICT: {'PASS' if f == 0 and e == 0 else 'FAIL'}")
print("=" * 60)
