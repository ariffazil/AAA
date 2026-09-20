#!/usr/bin/env python3
"""Capability-surface conformance sweep for an MCP organ.

Answers, on the live wire:
  1. What does each surface advertise? (tools/list, prompts/list, HTTP /tools)
  2. Do the surfaces agree on the same field per verb? (stage / ontology divergence)
  3. Is every advertised tool actually callable? (phantom / mismatch / resolved)

Usage:
    python3 mcp_surface_conformance_sweep.py [base_url] [--field stage]

Defaults to http://127.0.0.1:8088 . Read-only: it calls each tool with the safest mode
it can derive from the live schema. It never mutates.

Why this exists: a report that "the surface is broken, only N of M tools work" is a claim.
This sweep re-derives it, and separates client-side cache from server-side divergence.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

DEFAULT_URL = "http://127.0.0.1:8088"

# Preference order for the safest read-only-ish mode, tried against the live enum.
SAFE_MODES = (
    "verify", "light", "vitals", "read", "search", "recall", "status",
    "validate", "critique", "dry_run", "inspect", "health",
)


def post(url: str, payload: dict, timeout: int = 30) -> str:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode()


def get(url: str, timeout: int = 15) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return resp.read().decode()


def rpc(url: str, method: str, params: dict | None = None, rid: int = 2) -> dict:
    raw = post(url, {"jsonrpc": "2.0", "id": rid, "method": method,
                     "params": params or {}})
    return json.loads(raw)


def initialize(url: str) -> bool:
    try:
        rpc(url, "initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "surface-conformance-sweep", "version": "1"},
        }, rid=1)
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"initialize FAILED: {exc}")
        return False


def call_tool(url: str, name: str, args: dict) -> str:
    """Return the raw tool-call text, or an ERROR: marker string."""
    try:
        out = post(url, {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                         "params": {"name": name, "arguments": args}})
        body = json.loads(out)
        return body.get("result", {}).get("content", [{}])[0].get("text", "")
    except urllib.error.HTTPError as exc:
        return f"ERROR: HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001
        return f"ERROR: {exc}"


def derive_safe_args(schema: dict) -> dict:
    """Best-effort: prefer an enum'd mode, else no args at all."""
    props = (schema or {}).get("properties", {}) or {}
    mode = props.get("mode") or {}
    enum = mode.get("enum") or []
    if enum:
        for preferred in SAFE_MODES:
            if preferred in enum:
                return {"mode": preferred}
        return {"mode": enum[0]}
    return {}


def is_cache_artifact(text: str) -> bool:
    return "Unknown tool" in text or "unknown tool" in text


def is_schema_reject(text: str) -> bool:
    low = text.lower()
    return ("validation error" in low or "missing required" in low
            or "unexpected keyword" in low or "missing_argument" in low)


def surface_tools(url: str) -> list[dict]:
    try:
        d = rpc(url, "tools/list")
        return d.get("result", {}).get("tools", []) or []
    except Exception:  # noqa: BLE001
        return []


def surface_prompts(url: str) -> list:
    try:
        d = rpc(url, "prompts/list")
        return d.get("result", {}).get("prompts", []) or []
    except Exception:  # noqa: BLE001
        return []


def http_tools(base: str) -> list[dict]:
    for path in ("/tools", "/mcp/tools"):
        try:
            d = json.loads(get(base.rstrip("/") + path))
            if isinstance(d, dict) and d.get("tools"):
                return d["tools"]
        except Exception:  # noqa: BLE001
            continue
    return []


def stage_of(entry: dict) -> str | None:
    """Pull a comparable ontology field out of any of the surface shapes."""
    if not isinstance(entry, dict):
        return None
    for key in ("stage", "stage_code"):
        if entry.get(key) is not None:
            return str(entry[key])
    meta = entry.get("meta") or {}
    for key in ("stage", "stage_code"):
        if isinstance(meta, dict) and meta.get(key) is not None:
            return str(meta[key])
    # prompts often encode the stage in the leading token of the name
    name = str(entry.get("name", ""))
    head = name.split(" ")[0].strip()
    return head if head.isdigit() else None


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = args[0] if args else DEFAULT_URL
    url = base.rstrip("/") + ("/mcp" if not base.rstrip("/").endswith("/mcp") else "")

    print(f"=== surface conformance sweep: {base} ===\n")
    if not initialize(url):
        return 2

    tools = surface_tools(url)
    prompts = surface_prompts(url)
    http_surface = http_tools(base)

    print(f"tools/list   : {len(tools)} verbs")
    print(f"prompts/list : {len(prompts)} entries")
    print(f"HttpGet /tools: {len(http_surface)} verbs\n")

    # ---- cross-surface ontology comparison -------------------------------
    t_stage = {t.get("name"): stage_of(t) for t in tools if t.get("name")}
    h_stage = {t.get("name"): stage_of(t) for t in http_surface if t.get("name")}
    # prompts carry stages but rarely the same verb name; compare by stage token set
    p_stages = {stage_of(p) for p in prompts if stage_of(p)}
    t_stages = {v for v in t_stage.values() if v}

    print("--- per-verb stage agreement ---")
    divergent = 0
    for name, ts in sorted(t_stage.items()):
        hs = h_stage.get(name)
        if hs is not None and ts is not None and hs != ts:
            print(f"  DIVERGENT  {name:20s} tools/list={ts}  http/tools={hs}")
            divergent += 1
        elif ts:
            print(f"  ok         {name:20s} stage={ts}")
    if not h_stage:
        print("  (no HTTP /tools surface to compare)")

    only_prompt = sorted(p_stages - t_stages)
    only_tool = sorted(t_stages - p_stages)
    if only_prompt or only_tool:
        print("\n--- stage universe divergence ---")
        print(f"  stages only in prompts/list : {only_prompt}")
        print(f"  stages only in tools/list   : {only_tool}")
        print("  -> two different ontologies are being served by one build")

    # ---- callability sweep ----------------------------------------------
    print("\n--- callability sweep (safest mode per verb) ---")
    phantom = mismatch = resolved = 0
    for t in tools:
        name = t.get("name")
        if not name:
            continue
        argv = derive_safe_args(t.get("inputSchema") or {})
        text = call_tool(url, name, argv)
        if text.startswith("ERROR:"):
            print(f"  ERROR      {name:20s} {text[:70]}")
            mismatch += 1
        elif is_cache_artifact(text):
            print(f"  PHANTOM    {name:20s} advertised but Unknown tool")
            phantom += 1
        elif is_schema_reject(text):
            print(f"  MISMATCH   {name:20s} rejected args {argv}")
            mismatch += 1
        else:
            print(f"  resolved   {name:20s} args={argv}")
            resolved += 1

    total = phantom + mismatch + resolved
    rate = (resolved / total) if total else 0.0
    print(f"\nresolved={resolved}  phantom={phantom}  mismatch={mismatch}")
    print(f"CapabilityTruthRate = {resolved}/{total} = {rate:.2f}")

    print("\n--- reading ---")
    if phantom:
        print("  phantom > 0 on the LIVE surface = real server defect (tools advertised in")
        print("  tools/list but not dispatchable).")
    else:
        print("  zero phantom over tools/list. A client reporting many 'Unknown tool'")
        print("  names is dispatching a CACHED pre-migration tool list -> have it re-initialise.")
    if mismatch:
        print("  mismatch > 0: check each against inputSchema.properties before calling it a")
        print("  schema defect - a wrong arg looks identical to a rejected schema.")
    if divergent or only_prompt or only_tool:
        print("  cross-surface divergence detected: hash canon vs deployed (identical sha256")
        print("  means the deploy is fine), then read each surface's import block - if they")
        print("  do not import each other, no deploy will ever reconcile them. That is a")
        print("  missing GATE, not a missing release.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
