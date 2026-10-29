#!/usr/bin/python3
"""compile_machine_contract.py — Layer B: runtime-generated machine contract for the arifOS federation.

WHY (named failure class, not decoration):
  An agent crawling the public portal today receives an official-looking capability
  contract that is measurably incomplete: 40 published capabilities against a live
  governed tool surface an order of magnitude larger, with A-FORGE — the executor —
  published as ZERO. Hand-written tables drift. This is compiled from the runtime.

WHAT IT DOES (read-only; a mutating verb is enumerated, never executed):
  1. PROBE   every organs.yaml component that declares a port, with a real MCP
             `initialize` handshake before tools/list. No handshake => false "0 tools"
             => a fabricated death claim. Probing ALL ports (not just declared MCP ones)
             is what lets the sweep catch organs whose MCP is live but undeclared.
  2. JOIN    organs.yaml (authority_ceiling, owned/forbidden domains, public URL),
             organ tools_sot.yaml (mutation class where one is generated),
             published capabilities.json (to verify each public claim under its own protocol).
  3. EMIT    machine-contract.json  — one governed-capability entry per LIVE tool
             contract-coverage.json — the measured gap + per-claim verification + SOT defects

HONESTY RULES (F2 TRUTH / F7 HUMILITY — these ARE the deliverable):
  * request_schema is the live inputSchema. It cannot drift, because it is the runtime.
  * Anything MCP does not machine-declare (response_schema, per-tool outcomes, receipt URI,
    boundary class) is emitted as {"state": "undeclared", "reason": ...}. NEVER invented.
    The undeclared count is the real work list for Layer B.
  * States are separated, never collapsed to a boolean:
      organ liveness  : live | no_mcp_surface | not_http | unreachable | rejected
      published claim : confirmed_live | confirmed_reachable | protocol_mislabel_http_ok
                        | advertised_but_not_reachable | http_* | undeclared_no_path
    A protocol mislabel is NOT a dead capability. This compiler refuses to publish
    either error, in either direction.
  * Verification is GET-only. A published path may be a mutating endpoint.

Usage:  /usr/bin/python3 compile_machine_contract.py [--out-dir DIR] [--no-probe]
        (shebang is /usr/bin/python3 on purpose: the `env python3` on PATH is a
         bundled 3.14 without PyYAML — that combination fails silently.)

DITEMPA BUKAN DIBERI · 333-AGI · 2026-10-26
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import yaml

CONTRACT_VERSION = "1.0"
# Placeholder only. main() REPLACES this with the evidence timestamp before any artifact is
# written: wall-clock time here would make repeated compilation from unchanged inputs
# byte-different, which would fake change where none happened (regression gate 10).
NOW = "UNSET_EVIDENCE_TS"

ORGANS_YAML = Path("/root/AAA/federation/organs.yaml")
PUBLISHED = Path("/var/www/html/.well-known/capabilities.json")
VERDICT_VOCAB = ["SEAL", "HOLD", "SABAR", "VOID"]

# organs.yaml declares no MCP surface for FED, yet one answers live. Listed explicitly so the
# sweep is not silently narrower than reality; every entry is still probe-verified below.
EXTRA_MCP = {"fed": 7074}
PROBE_TIMEOUT = (
    6  # short: non-HTTP ports (postgres/redis/nats/...) accept TCP then say nothing
)

HDRS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {
            "name": "333-AGI-contract-compiler",
            "version": CONTRACT_VERSION,
        },
    },
}
NOTIF = {"jsonrpc": "2.0", "method": "notifications/initialized"}
LIST = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}


def _post(
    url: str, payload: dict, sid: str | None = None, timeout: int = PROBE_TIMEOUT
):
    h = dict(HDRS)
    if sid:
        h["mcp-session-id"] = sid
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.headers.get("mcp-session-id"), resp.read().decode()


def _envelope(body: str) -> dict:
    """Parse JSON-RPC from a bare body or an SSE `data:` stream."""
    for line in reversed(body.strip().split("\n")):
        line = line[5:].strip() if line.startswith("data:") else line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return {}


def probe_mcp(port: int) -> dict[str, Any]:
    """One local MCP surface. Failure mode is named, not flattened."""
    url = f"http://127.0.0.1:{port}/mcp"
    try:
        sid, body = _post(url, INIT)
        env = _envelope(body)
        if sid is None and "error" in env:
            return {
                "url": url,
                "port": port,
                "state": "rejected",
                "detail": str(env["error"])[:160],
                "tools": [],
            }
        info = env.get("result", {}).get("serverInfo", {}) or {}
        try:
            _post(url, NOTIF, sid)
        except Exception:  # noqa: BLE001 — notification is best-effort by spec
            pass
        _, body2 = _post(url, LIST, sid)
        tools = _envelope(body2).get("result", {}).get("tools", []) or []
        return {
            "url": url,
            "port": port,
            "state": "live",
            "tools": tools,
            "server_name": info.get("name"),
            "server_version": info.get("version"),
            "schema_valid": sum(
                1 for t in tools if isinstance(t.get("inputSchema"), dict)
            ),
        }
    except urllib.error.HTTPError as e:
        # 404/405 on /mcp = "no MCP surface here", NOT "organ dead". Different failure class.
        st = "no_mcp_surface" if e.code in (404, 405) else "unreachable"
        return {
            "url": url,
            "port": port,
            "state": st,
            "detail": f"HTTP {e.code}",
            "tools": [],
        }
    except (TimeoutError, OSError) as e:
        # Raw TCP service (postgres/redis/nats/minio/falkordb) or nothing listening.
        st = (
            "not_http"
            if isinstance(e, TimeoutError) or "timed out" in str(e).lower()
            else "unreachable"
        )
        return {
            "url": url,
            "port": port,
            "state": st,
            "detail": f"{type(e).__name__}: {e}"[:120],
            "tools": [],
        }
    except Exception as e:  # noqa: BLE001
        return {
            "url": url,
            "port": port,
            "state": "unreachable",
            "detail": f"{type(e).__name__}: {e}"[:120],
            "tools": [],
        }


def http_probe(url: str, timeout: int = 12) -> tuple[str, int | None]:
    """GET-only reachability. Never POST: a published path may be a mutating endpoint."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "333-AGI-contract-compiler/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return "reachable", resp.status
    except urllib.error.HTTPError as e:
        return ("reachable" if e.code < 500 else "server_error"), e.code
    except Exception as e:  # noqa: BLE001
        return f"unreachable:{type(e).__name__}", None




def response_schema_decl(t: dict) -> dict[str, Any]:
    """response_schema from the LIVE outputSchema. Corrects compiler v1.0, which
    hard-coded 'tools/list exposes no outputSchema' without reading the field:
    138/258 tools actually declare one (32 field-level, 106 bare {type:object})."""
    osch = t.get("outputSchema")
    if not isinstance(osch, dict):
        return {
            "state": "undeclared",
            "reason": "no outputSchema present in live tools/list for this tool",
        }
    rich = bool(osch.get("properties"))
    return {
        "state": "declared",
        "schema": osch,
        "richness": "field_level" if rich else "bare_object",
        "source": "live tools/list outputSchema (runtime-generated)",
        "does_not_imply": (
            "declared field set; it does not prove observed responses conform"
            if rich
            else "carries no field-level contract — a bare {type:object} schema "
            "constrains only that the result is an object"
        ),
    }


_MUT = re.compile(r"\b(OBSERVE|MUTATE|DEPLOY|EXECUTE|READ_ONLY|COMPUTE_ONLY)\b")


def mutation_class(desc: str, sot_entry: dict | None) -> dict[str, Any]:
    """Derive mutation class; return an honest 'undeclared' when nothing declares it."""
    sot_entry = sot_entry or {}
    tok = sot_entry.get("mutation") or sot_entry.get("tier") or sot_entry.get("class")
    if tok:
        return {
            "class": str(tok).upper(),
            "state": "declared",
            "source": f"tools_sot.yaml typed field; access={sot_entry.get('access')!r}",
        }
    src = (
        f"tools_sot.yaml description (access={sot_entry.get('access')!r})"
        if sot_entry
        else "tool description"
    )
    hay = " ".join(filter(None, [desc, sot_entry.get("description", "")])).upper()
    m = _MUT.search(hay)
    if m:
        return {
            "class": m.group(1),
            "state": "declared_in_prose",
            "source": src,
            "note": "class token lives in prose, not a typed field — runtime should declare it",
        }
    return {
        "class": "undeclared",
        "state": "undeclared",
        "reason": "no typed mutation class in tools/list, none parseable from SOT/description",
    }


def load_organs() -> dict[str, dict]:
    d = yaml.safe_load(ORGANS_YAML.read_text()) or {}
    return {
        c["id"]: c for c in d.get("components", []) if isinstance(c, dict) and "id" in c
    }


def load_sot(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    try:
        d = yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError:
        return {}
    return {
        t["name"]: t for t in d.get("tools", []) if isinstance(t, dict) and "name" in t
    }


def published_index(
    published_path: Path = PUBLISHED,
) -> tuple[dict[str, list[dict]], dict]:
    """surface host -> published capability entries (full objects: protocol matters)."""
    if not published_path.exists():
        return {}, {}
    try:
        d = json.loads(published_path.read_text())
    except json.JSONDecodeError:
        return {}, {}
    return (
        {
            s: [
                c
                for c in (b or {}).get("capabilities") or []
                if isinstance(c, dict) and c.get("name")
            ]
            for s, b in (d.get("surfaces") or {}).items()
        },
        d,
    )


def surface_to_organ(organs: dict[str, dict]) -> dict[str, str]:
    """Derive the surface-host -> organ map FROM organs.yaml public URLs. Not hardcoded:
    a hardcoded map is how geox/wealth/well got silently dropped in the first cut."""
    out = {}
    for oid, c in organs.items():
        for field in ("public_mcp", "mcp_endpoint", "public_url", "url"):
            v = c.get(field)
            if isinstance(v, str) and "://" in v:
                host = urllib.parse.urlparse(v).netloc.lower()
                if host:
                    out.setdefault(host, oid)
    return out


def verify_published(
    entries: list[dict], surface: str, live_mcp_names: set[str]
) -> list[dict]:
    """Verify each published claim UNDER ITS OWN declared protocol.

    capabilities.json mixes mcp | http | webmcp in one flat list. A name-only diff against
    the live MCP tool set therefore fabricates deaths (a real HTTP route labelled
    protocol=mcp looks "dead"). Every entry is verified under the protocol it declares.
    """
    base = f"https://{surface}"
    rows = []
    for e in entries:
        proto = (e.get("protocol") or "undeclared").lower()
        path = e.get("path") or e.get("endpoint") or ""
        url = (
            path
            if path.startswith("http")
            else f"{base}{'' if path.startswith('/') or not path else '/'}{path}"
        )
        row = {
            "name": e["name"],
            "declared_protocol": proto,
            "url_probed": url if path else None,
        }
        if proto == "mcp":
            if e["name"] in live_mcp_names:
                row.update(
                    verdict="confirmed_live", method="present in live tools/list"
                )
            else:
                st, code = http_probe(url) if path else ("no_path", None)
                row.update(
                    http_status=code,
                    verdict=(
                        "protocol_mislabel_http_ok"
                        if st == "reachable"
                        else "advertised_but_not_reachable"
                    ),
                    method="absent from live tools/list; GET probed under its own path",
                )
        elif proto in ("http", "webmcp"):
            if not path:
                row.update(
                    verdict="undeclared_no_path", method="no path published to verify"
                )
            else:
                st, code = http_probe(url)
                row.update(
                    http_status=code,
                    verdict="confirmed_reachable"
                    if st == "reachable"
                    else f"http_{st}",
                    method="GET only (webmcp tool invocation not executed)",
                )
        else:
            row.update(
                verdict="unknown_protocol",
                method=f"protocol {proto!r} has no verification rule",
            )
        rows.append(row)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="/root/AAA/ops/capabilities")
    ap.add_argument(
        "--no-probe", action="store_true", help="reuse cached probe (offline)"
    )
    ap.add_argument("--cache", default="/tmp/opencode/live_probe_full.json")
    ap.add_argument(
        "--published",
        default=str(PUBLISHED),
        help="capabilities.json to verify against (default: live public surface; "
        "override to regression-test a repaired-but-not-deployed copy)",
    )
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    organs = load_organs()
    pub_idx, pub_raw = published_index(Path(args.published))
    surf2organ = surface_to_organ(organs)
    sot_by_organ = {
        oid: load_sot(p)
        for oid, p in {
            "a-forge": Path("/root/A-FORGE/tools_sot.yaml"),
            "wealth": Path("/root/WEALTH/tools_sot.yaml"),
        }.items()
    }

    # Probe every component that declares ANY port — the sweep must not be narrower than reality.
    ports: dict[str, int] = {}
    for oid, c in organs.items():
        p = c.get("mcp_port") or c.get("port")
        if isinstance(p, int):
            ports[oid] = p
    for oid, p in EXTRA_MCP.items():
        ports.setdefault(oid, p)

    cache = Path(args.cache)
    global NOW
    if args.no_probe and cache.exists():
        results = json.loads(cache.read_text())
        # Reused evidence: stamp artifacts with the cache's capture time, not "now".
        NOW = (
            dt.datetime.fromtimestamp(cache.stat().st_mtime, dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )
    else:
        results = {oid: probe_mcp(p) for oid, p in ports.items()}
        NOW = (
            dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(results, indent=1))

    capabilities: list[dict] = []
    organ_rows: list[dict] = []
    sot_defects: list[dict] = []
    for oid, r in results.items():
        meta = organs.get(oid, {})
        sot = sot_by_organ.get(oid, {})
        live_names = {t["name"] for t in r.get("tools", [])}

        # organs.yaml completeness: MCP answers live but the SOT declares no MCP surface.
        declares_mcp = bool(
            meta.get("mcp_port")
            or meta.get("public_mcp")
            or meta.get("mcp_endpoint")
            or (meta.get("interfaces") or {}).get("mcp")
        )
        if r["state"] == "live" and not declares_mcp:
            sot_defects.append(
                {
                    "organ": oid,
                    "port": r["port"],
                    "live_tools": len(live_names),
                    "defect": "mcp_live_but_undeclared_in_organs_yaml",
                    "consequence": "any consumer selecting MCP targets from organs.yaml silently "
                    "omits this organ — this is how 3 of 5 published surfaces were "
                    "dropped by the first cut of this compiler",
                }
            )

        for t in r.get("tools", []):
            name = t["name"]
            desc = (t.get("description") or "").strip()
            capabilities.append(
                {
                    "capability_id": f"{oid}.{name}",
                    "contract_version": CONTRACT_VERSION,
                    "organ": oid,
                    "title": name,
                    "purpose": {
                        "description": desc[:600] or "undeclared",
                        "state": "declared" if desc else "undeclared",
                        "source": f"live tools/list ({oid})"
                        + (" + tools_sot.yaml" if name in sot else ""),
                    },
                    "transport": {
                        "protocol": "mcp",
                        "endpoint_local": r["url"],
                        "endpoint_public": meta.get("public_mcp")
                        or meta.get("mcp_endpoint")
                        or "undeclared",
                        "handshake_required": True,
                        "server_name": r.get("server_name"),
                        "server_version": r.get("server_version"),
                    },
                    "request_schema": t.get("inputSchema") or {"state": "undeclared"},
                    "response_schema": response_schema_decl(t),
                    "authority": {
                        "organ_ceiling": meta.get("authority_ceiling") or "undeclared",
                        "owned_domains": meta.get("owned_domains") or [],
                        "forbidden_domains": meta.get("forbidden_domains") or [],
                        "human_veto": "ARIF (F13 SOVEREIGN)",
                        "verdict_vocabulary": VERDICT_VOCAB,
                        "verdict_scope": "organ-level, not per-tool: the runtime declares no per-capability outcomes",
                    },
                    "mutation": mutation_class(desc, sot.get(name)),
                    "outcomes": {
                        "state": "undeclared",
                        "reason": "no per-tool outcome enum is machine-declared by any organ",
                    },
                    "receipt": {
                        "state": "undeclared",
                        "reason": "no per-tool verification_uri is machine-declared; VAULT999 receipts are "
                        "emitted at call time by arifOS/A-FORGE, not advertised in the contract",
                    },
                    "status": {
                        "liveness": r["state"],
                        "schema_valid": isinstance(t.get("inputSchema"), dict),
                    },
                    "evidence": {
                        "source": "runtime-generated",
                        "method": "mcp initialize handshake + notifications/initialized + tools/list",
                        "probed_at": NOW,
                        "does_not_imply": "enumerated != callable != authorized. Mutating verbs were NOT executed.",
                    },
                }
            )

        organ_rows.append(
            {
                "organ": oid,
                "port": r["port"],
                "liveness": r["state"],
                "detail": r.get("detail"),
                "live_tools": len(live_names),
                "schema_valid": r.get("schema_valid", 0),
                "declares_mcp_in_organs_yaml": declares_mcp,
                "authority_ceiling": meta.get("authority_ceiling") or "undeclared",
                "server_name": r.get("server_name"),
                "server_version": r.get("server_version"),
            }
        )

    # Verify EVERY published surface, mapped to an organ by data — unmapped surfaces are
    # verified too (live_mcp_names empty), so no public claim escapes inspection.
    pub_rows = []
    for surf, entries in pub_idx.items():
        oid = surf2organ.get(surf.lower())
        live_names = (
            {t["name"] for t in results[oid].get("tools", [])}
            if oid in results
            else set()
        )
        v = verify_published(entries, surf, live_names)
        defects: dict[str, list[str]] = {}
        for row in v:
            if not row["verdict"].startswith("confirmed"):
                defects.setdefault(row["verdict"], []).append(row["name"])
        pub_rows.append(
            {
                "surface": surf,
                "mapped_organ": oid or "UNMAPPED (no organs.yaml public URL)",
                "published": len(entries),
                "verification": v,
                "defects": defects,
            }
        )

    live_total = sum(o["live_tools"] for o in organ_rows if o["liveness"] == "live")
    schema_total = sum(o["schema_valid"] for o in organ_rows)
    pub_total = sum(p["published"] for p in pub_rows)
    pub_confirmed = sum(
        1
        for p in pub_rows
        for r in p["verification"]
        if r["verdict"].startswith("confirmed")
    )
    declared_mut = sum(
        1 for c in capabilities if c["mutation"]["state"] != "undeclared"
    )
    resp_declared = sum(
        1 for c in capabilities if c["response_schema"]["state"] == "declared"
    )
    resp_rich = sum(
        1 for c in capabilities if c["response_schema"].get("richness") == "field_level"
    )
    n = len(capabilities) or 1

    coverage = {
        "contract_version": CONTRACT_VERSION,
        "generated_at": NOW,
        "generator": "AAA ops/capabilities/compile_machine_contract.py (read-only; live MCP + HTTP probe)",
        "headline": {
            "live_governed_tools": live_total,
            "live_input_schema_valid": schema_total,
            "organs_live": sum(1 for o in organ_rows if o["liveness"] == "live"),
            "organs_probed": len(organ_rows),
            "published_claims_total": pub_total,
            "published_claims_confirmed": pub_confirmed,
            "published_claims_defective": pub_total - pub_confirmed,
            "published_generated_at": pub_raw.get("generated_at"),
            "published_source": str(Path(args.published).resolve()),
            "published_source_deployed": Path(args.published).resolve()
            == PUBLISHED.resolve(),
            "coverage_pct": round(100 * pub_total / live_total, 1)
            if live_total
            else None,
        },
        "layer_b_field_readiness": {
            "note": "What the runtime already gives for free vs what still needs a new runtime "
            "declaration. The second block IS the Layer B work list.",
            "free_from_runtime": {
                "capability_id": f"{len(capabilities)}/{len(capabilities)}",
                "transport": f"{len(capabilities)}/{len(capabilities)}",
                "request_schema": f"{schema_total}/{len(capabilities)} (live inputSchema)",
                "authority.organ_ceiling": f"{sum(1 for c in capabilities if c['authority']['organ_ceiling'] != 'undeclared')}/{len(capabilities)}",
                "mutation.class": f"{declared_mut}/{len(capabilities)} ({round(100 * declared_mut / n)}%)",
                "status.liveness": f"{len(capabilities)}/{len(capabilities)}",
                "response_schema": f"{resp_declared}/{len(capabilities)} declared via live outputSchema "
                f"({resp_rich} field-level, {resp_declared - resp_rich} bare {{type:object}})",
            },
            "requires_new_runtime_declaration": {
                "outcomes_per_tool_verdict_enum": f"0/{len(capabilities)}",
                "receipt_verification_uri": f"0/{len(capabilities)}",
                "boundary_public_internal_governed": f"0/{len(capabilities)}",
                "mutation_class_typed_field": f"0/{len(capabilities)} (all {declared_mut} are prose-derived)",
            },
        },
        "published_verification": pub_rows,
        "organs": organ_rows,
        "organs_yaml_defects": sot_defects,
        "defect_vocabulary": {
            "protocol_mislabel_http_ok": "declared protocol=mcp but absent from live tools/list; its path "
            "answers HTTP 200 — a labelling defect, NOT a dead capability",
            "advertised_but_not_reachable": "declared, and neither a live MCP tool nor a reachable path",
            "http_unreachable:*": "published path failed to resolve",
            "http_server_error": "published path returned 5xx",
            "undeclared_no_path": "no path published, nothing to verify against",
            "unknown_protocol": "protocol has no verification rule in this compiler",
            "mcp_live_but_undeclared_in_organs_yaml": "topology SOT is narrower than the running system",
        },
        "surface_entropy": {
            "well_known_json_files": sorted(
                p.name for p in Path("/var/www/html/.well-known").glob("*.json")
            )
            if Path("/var/www/html/.well-known").exists()
            else [],
            "note": "Several capability vocabularies are published at once and disagree. Retirement is an "
            "F13 blast-radius call (external consumers unknown), not a compiler action.",
        },
    }

    (out / "machine-contract.json").write_text(
        json.dumps(
            {
                "$schema": "https://arif-fazil.com/.well-known/schemas/machine-contract.v1.json",
                "contract_version": CONTRACT_VERSION,
                "generated_at": NOW,
                "generator": coverage["generator"],
                "sovereign": "Muhammad Arif bin Fazil — F13",
                "motto": "DITEMPA BUKAN DIBERI",
                "authority_note": "Reading this contract grants no authority. Capability = Declared ∩ Callable ∩ "
                "Authorized ∩ Competent. Enumerated here = Declared only.",
                "capabilities": capabilities,
            },
            indent=1,
        )
    )
    (out / "contract-coverage.json").write_text(json.dumps(coverage, indent=1))

    h = coverage["headline"]
    print(f"organs probed     : {h['organs_probed']} (live {h['organs_live']})")
    print(
        f"live tools        : {h['live_governed_tools']}   inputSchema valid: {h['live_input_schema_valid']}"
    )
    print(
        f"published claims  : {h['published_claims_total']} -> confirmed {h['published_claims_confirmed']}, "
        f"defective {h['published_claims_defective']} (gen {h['published_generated_at']})"
    )
    print(f"coverage          : {h['coverage_pct']}% of the live surface is published")
    print(
        f"mutation declared : {declared_mut}/{len(capabilities)} ({round(100 * declared_mut / n)}%)"
    )
    for d in sot_defects:
        print(
            f"SOT DEFECT: {d['organ']} :{d['port']} — {d['defect']} ({d['live_tools']} live tools)"
        )
    for p in pub_rows:
        for verdict, names in p["defects"].items():
            print(f"PUB DEFECT: {p['surface']:<26} {verdict:<30} {names}")
    print(f"wrote: {out / 'machine-contract.json'} ({len(capabilities)} capabilities)")
    print(f"wrote: {out / 'contract-coverage.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
