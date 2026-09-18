#!/usr/bin/env python3
"""capability_truth.py — capability-truth baseline (APEX-777 §21 P0 / STEP 1) · 333-AGI 2026-09-18

For each surface: ADVERTISED (tools/list) vs REGISTERED (dispatch table) vs
CALLABLE (safe dispatch-level probes only).

Constitutional:
  - READ-ONLY. No seal. No restart. No mutation paths executed.
  - Mutating verbs are NOT probed — reported as NOT_PROBED_MUTATING (an honest
    third state, never collapsed to a boolean).
  - Failures are data, not errors. "No data" = "cannot witness".
  - F1 AMANAH / F2 TRUTH / F7 HUMILITY.

Usage (use the live kernel venv — it has the mcp client + arifosmcp importable):
  /opt/arifos/current/venv/bin/python /root/AAA/scripts/capability_truth.py
  ... --surface arifos-local
Output: JSON -> /root/AAA/reports/capability-truth/baseline-<UTC>.json
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as _dt
import json
import sys
from pathlib import Path

# ── Surface table ────────────────────────────────────────────────────────────
SURFACES: dict[str, dict] = {
    "arifos-local": {
        "urls": ["http://127.0.0.1:8088/mcp"],
        "role": "canonical kernel (truth node)",
    },
    "hermes-local": {
        "urls": ["http://127.0.0.1:18087/mcp", "http://127.0.0.1:18087/"],
        "role": "HERMES meaning-integrity organ",
    },
    "arifos-public": {
        "urls": ["https://mcp.arif-fazil.com/mcp"],
        "role": "public route (must mirror canonical)",
    },
    "hermes-public": {
        "urls": ["https://mcp.arif-fazil.com/hermes/mcp"],
        "role": "public route (must mirror canonical)",
    },
}

# Safe probes for arifOS local (read-only verbs only; {} = cheapest dispatch proof)
ARIFOS_SAFE_PROBES: dict[str, dict] = {
    "arif_observe": {"mode": "vitals"},
    "arif_think": {"mode": "axioms"},
    "arif_route": {"intent": "__capability_truth_probe__"},
    "arif_memory": {"mode": "recall", "query": "__capability_truth_probe__"},
}
ARIFOS_NOT_PROBED_MUTATING = ["arif_init", "arif_forge", "arif_seal", "arif_judge"]

# Legacy/ghost alias names advertised by old clients & public llms.txt (SESAT set).
LEGACY_ALIASES = [
    "arif_kernel_route",
    "arif_memory_recall",
    "arif_mind_reason",
    "arif_sense_observe",
    "arif_evidence_fetch",
    "arif_reply_compose",
    "arif_heart_critique",
    "arif_judge_deliberate",
    "arif_ops_measure",
    "arif_stack_health_probe",
    "arif_bridge",
    "arif_bridge_connect",
]
LEGACY_SKIP_MUTATING = ["arif_forge_execute", "arif_vault_seal"]


def _client():
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client

    return ClientSession, streamable_http_client


def _text_of(res) -> str:
    out = ""
    for c in res.content or []:
        out += getattr(c, "text", "") or ""
    return out


async def _probe_call(session, name: str, args: dict, timeout: int = 25) -> str:
    """Returns one of: RESOLVES | UNKNOWN_TOOL | TIMEOUT | ERROR:<type>."""
    try:
        res = await asyncio.wait_for(session.call_tool(name, args), timeout=timeout)
        txt = _text_of(res).lower()
        return "UNKNOWN_TOOL" if "unknown tool" in txt else "RESOLVES"
    except asyncio.TimeoutError:
        return "TIMEOUT"
    except Exception as exc:  # noqa: BLE001
        msg = str(exc).lower()
        if "unknown tool" in msg:
            return "UNKNOWN_TOOL"
        return f"ERROR:{type(exc).__name__}"


async def measure_surface(key: str, cfg: dict, do_calls: bool, do_legacy: bool) -> dict:
    ClientSession, streamable_http_client = _client()
    result: dict = {
        "endpoint": cfg["urls"][0],
        "role": cfg["role"],
        "reachable": False,
        "advertised": [],
        "advertised_count": None,
        "callable": {},
        "phantom_tools": [],
        "legacy_aliases": {},
        "notes": [],
    }
    last_err = None
    for url in cfg["urls"]:
        try:
            async with streamable_http_client(url) as streams:
                async with ClientSession(streams[0], streams[1]) as session:
                    await asyncio.wait_for(session.initialize(), timeout=20)
                    tools = await asyncio.wait_for(session.list_tools(), timeout=30)
                    names = sorted(t.name for t in tools.tools)
                    result["reachable"] = True
                    result["endpoint_used"] = url
                    result["advertised"] = names
                    result["advertised_count"] = len(names)
                    # v0.2 — capture advertised mode enums from live schemas
                    _enum_snapshot: dict[str, list] = {}
                    for _t in tools.tools:
                        _schema = getattr(_t, "inputSchema", None) or getattr(_t, "input_schema", None) or {}
                        _props = (_schema.get("properties") or {}) if isinstance(_schema, dict) else {}
                        _mode = _props.get("mode") or {}
                        _enum = _mode.get("enum") or []
                        if _enum:
                            _enum_snapshot[_t.name] = list(_enum)
                    result["enum_snapshot"] = _enum_snapshot

                    if do_calls:
                        for tool, args in ARIFOS_SAFE_PROBES.items():
                            if tool in names:
                                result["callable"][tool] = await _probe_call(session, tool, args)
                        result["not_probed_mutating"] = [t for t in ARIFOS_NOT_PROBED_MUTATING if t in names]
                    if do_legacy:
                        legacy = {}
                        for ghost in LEGACY_ALIASES:
                            legacy[ghost] = await _probe_call(session, ghost, {})
                        result["legacy_aliases"] = {
                            "probed": legacy,
                            "skipped_mutating": LEGACY_SKIP_MUTATING,
                        }
                    break
        except Exception as exc:  # noqa: BLE001
            last_err = f"{type(exc).__name__}: {str(exc)[:160]}"
            continue
    if not result["reachable"]:
        result["notes"].append(f"UNREACHABLE — last error: {last_err}")
    return result


def _enum_truth(surface_result: dict) -> dict:
    """v0.2 — enum-level truth: advertised mode enum vs handler-declared universe.

    Read-only. Compares live tools/list schema enums against each handler's
    __dispatch_modes__ (declared capability universe). Undeclared handlers are
    reported explicitly — never assumed clean.
    """
    out: dict = {"checked": {}, "mismatches": {}, "undeclared": [], "note": ""}
    try:
        from arifosmcp.runtime.tools import CANONICAL_TOOL_HANDLERS as _CTH
    except Exception as exc:  # noqa: BLE001
        out["note"] = f"handler table unavailable: {type(exc).__name__}: {exc}"
        return out
    for tool_name, enum in (surface_result.get("enum_snapshot") or {}).items():
        handler = _CTH.get(tool_name)
        universe = getattr(handler, "__dispatch_modes__", None) if handler else None
        if universe is None:
            out["undeclared"].append({"tool": tool_name, "advertised_modes": len(enum)})
            continue
        bad = sorted(m for m in enum if m not in universe)
        out["checked"][tool_name] = {"advertised": len(enum), "universe": len(universe)}
        if bad:
            out["mismatches"][tool_name] = bad
    if not out["checked"] and not out["mismatches"]:
        out["note"] = "no declared universes on this surface — enum check dormant"
    return out


def arifos_registered_side() -> dict:
    """Registered/dispatch side, measured in-process (live venv only)."""
    try:
        from arifosmcp.runtime.tools import CANONICAL_TOOL_HANDLERS

        info = {"handler_count": len(CANONICAL_TOOL_HANDLERS)}
        try:
            from arifosmcp.runtime import public_surface as ps

            abi = set(getattr(ps, "KERNEL_ABI_8", []) or [])
            info["kernel_abi_8"] = sorted(abi)
            info["public_for_mode"] = sorted(ps.public_tool_names_for_mode())
        except Exception as exc:  # noqa: BLE001
            info["public_surface_error"] = f"{type(exc).__name__}: {exc}"
        return info
    except Exception as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", default=None)
    ap.add_argument("--no-calls", action="store_true", help="tools/list only")
    ap.add_argument("--no-legacy", action="store_true", help="skip legacy alias probes")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    keys = [args.surface] if args.surface else list(SURFACES)
    report: dict = {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "generator": "capability_truth.py v0.1 (333-AGI · APEX-777 phase 3 step 1)",
        "surfaces": {},
        "kpis": {},
    }

    for key in keys:
        cfg = SURFACES[key]
        do_calls = (not args.no_calls) and key == "arifos-local"
        do_legacy = (not args.no_legacy) and key == "arifos-local"
        print(f"▸ probing {key} …", file=sys.stderr)
        report["surfaces"][key] = await measure_surface(key, cfg, do_calls, do_legacy)

    # registered side (in-process) + KPI rollup for the local kernel
    reg = arifos_registered_side()
    report["arifos_registered_side"] = reg
    s_local = report["surfaces"].get("arifos-local", {})
    if s_local.get("reachable"):
        advertised = set(s_local["advertised"])
        abi = set(reg.get("kernel_abi_8", []))
        missing = sorted(abi - advertised) if abi else "UNMEASURED"
        callable_map = s_local.get("callable", {})
        probed = [v for v in callable_map.values()]
        ctr = round(sum(1 for v in probed if v == "RESOLVES") / len(probed), 4) if probed else None
        legacy = s_local.get("legacy_aliases", {}).get("probed", {})
        legacy_failed = sorted(k for k, v in legacy.items() if v == "UNKNOWN_TOOL")
        _enum = _enum_truth(s_local)
        report["enum_truth"] = _enum
        report["kpis"] = {
            "phantom_tools": [k for k, v in callable_map.items() if v == "UNKNOWN_TOOL"],
            "phantom_tools_note": "mutating verbs not probed — see not_probed_mutating",
            "missing_tools": missing,
            "capability_truth_rate_probed": ctr,
            "advertised_count": len(advertised),
            "handler_count": reg.get("handler_count"),
            "legacy_aliases_failed": legacy_failed,
            "schema_mismatch": _enum.get("mismatches") or {},
            "enum_checked": _enum.get("checked") or {},
            "enum_undeclared_tools": _enum.get("undeclared") or [],
            "enum_note": _enum.get("note") or "",
            "alias_conflicts": "NOT_MEASURED_V01",
        }

    out = Path(args.out) if args.out else None
    if out is None:
        d = Path("/root/AAA/reports/capability-truth")
        d.mkdir(parents=True, exist_ok=True)
        stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out = d / f"baseline-{stamp}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report["kpis"], indent=2, ensure_ascii=False))
    print(f"→ saved {out}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
