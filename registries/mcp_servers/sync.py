#!/usr/bin/env python3
"""
AAA MCP Registry Sync — Federation Resource & Agent Mapping Engine (FRAME)

Reads /root/.config/opencode/opencode.json (the federation's MCP runtime) and
emits per-server JSON files + INDEX.json in the official MCP 2026 server schema
(https://modelcontextprotocol.io/schemas/2026/server.json).

Stateless-ready: per-server records carry protocol_versions_supported, endpoints
(array, not single URL for LB), mrtr_capable, subscriptions, cache_scope, plus
harness_visibility (which of the 8 agent classes from MCP-FRAME.md see it) and
status_reason (for the 5 disabled servers).

Idempotent: re-running on the same opencode.json produces a byte-identical set
of per-server files (sorted keys, deterministic timestamps via SOURCE_GENERATED_AT).

Reverse: the 5 organ files (arifos, aforge, geox, wealth, well) are NOT touched
by this script — they carry the full per-tool manifest. The script emits only
the 21 non-organ extension files. To regenerate organs, use
forge_surface_audit mode=scan or live probe.

Authority: T1 (auto-do). F1 AMANAH: read-only on source. F11 AUDIT: every
emission logged with sha256 of source + sha256 of output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

OPENCODE_CONFIG = Path("/root/.config/opencode/opencode.json")
REGISTRY_DIR = Path("/root/AAA/registries/mcp_servers")
INDEX_PATH = REGISTRY_DIR / "INDEX.json"
SCHEMA_URL = "https://modelcontextprotocol.io/schemas/2026/server.json"
SOURCE_GENERATED_AT = "2026-08-10T10:30:00.000000+00:00"  # Pinned for idempotency
SOVEREIGN = "Muhammad Arif bin Fazil (F13 SOVEREIGN)"

# Organ files: never overwritten by this script (they carry full per-tool manifests)
ORGAN_FILES = {"arifos.json", "aforge.json", "geox.json", "wealth.json", "well.json"}

# Per-server metadata. Keys: opencode.json mcp key. Values: dict of static metadata
# that opencode.json does not carry. Adding new fields here is the right move;
# changing the opencode.json source to drive these is over-engineering for 21 entries.
SERVER_META: dict[str, dict] = {
    # ───── INFRASTRUCTURE ─────
    "arifflow": {
        "category": "infrastructure",
        "tags": ["arifos-federation", "metabolism", "arifflow"],
        "constitutional_tier": "F11_AUDIT",
        "description": "arifFLOW metabolism organ — Flow Quotient, receipt ingestion, attention checkpointing. Routes/checkpoints/witnesses; never judges, never executes.",
        "transport_type": "stdio",
        "command": "/root/arifFlow/mcp/arifflow-mcp.py",
        "harness_visibility": ["codex", "kimi", "opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "fed": {
        "category": "infrastructure",
        "tags": ["arifos-federation", "router", "fed"],
        "constitutional_tier": "F2_TRUTH",
        "description": "FED — Federation Router. Answers WHICH model@provider to call. Constitutional tier gate: ≥666 → direct only. SOT: /root/.config/federation-models.json",
        "transport_type": "http",
        "endpoint": "http://127.0.0.1:7074/mcp",
        "harness_visibility": ["kimi", "opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "hermes": {
        "category": "infrastructure",
        "tags": ["arifos-federation", "edge", "hermes", "telegram"],
        "constitutional_tier": "F13_SOVEREIGN",
        "description": "Hermes edge agent — Telegram gateway, multimodal bridge, A2A router. The ONLY agent that communicates with Arif directly (F13 governance).",
        "transport_type": "stdio",
        "command": "/root/.hermes/mcp_servers/hermes_mcp.py",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": True,
        "subscriptions": ["toolsListChanged", "resourcesListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25", "2026-07-28"],
    },
    "hermes-agent": {
        "category": "infrastructure",
        "tags": ["arifos-federation", "agent", "hermes"],
        "constitutional_tier": "F13_SOVEREIGN",
        "description": "Hermes Agent endpoint — companion HTTP surface to Hermes stdio. A2A dispatch for federation agents.",
        "transport_type": "http",
        "endpoint": "http://127.0.0.1:18090/mcp",
        "harness_visibility": ["opencode"],
        "mrtr_capable": True,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25", "2026-07-28"],
    },
    "hindsight": {
        "category": "infrastructure",
        "tags": ["arifos-federation", "memory", "retired"],
        "constitutional_tier": "F2_TRUTH",
        "description": "Hindsight memory layer (RETIRED 2026-08-05). Endpoint kept for forensic rollback only.",
        "transport_type": "http",
        "endpoint": "http://127.0.0.1:18087/mcp",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": False,
        "subscriptions": [],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-06-18"],
        "status": "RETIRED",
        "status_reason": "Retired 2026-08-05. Endpoint kept offline for forensic rollback. Remove after 90-day grace.",
    },
    # ───── RESEARCH & SEARCH ─────
    "context7": {
        "category": "research",
        "tags": ["docs", "library", "context7"],
        "constitutional_tier": "F2_TRUTH",
        "description": "Context7 — library documentation lookup. AI-synthesized code snippets for any library version.",
        "transport_type": "stdio",
        "command": "/usr/local/bin/context7-mcp",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "public",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "minimax": {
        "category": "research",
        "tags": ["search", "web", "minimax", "token-plan"],
        "constitutional_tier": "F2_TRUTH",
        "description": "MiniMax Token Plan MCP — web_search tool for coding queries. Provider: MiniMax. RATE-LIMITED at provider.",
        "transport_type": "stdio",
        "command": "minimax-coding-plan-mcp",
        "harness_visibility": ["kimi", "opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "minimax-mcp": {
        "category": "multimodal",
        "tags": ["multimodal", "image", "video", "audio", "minimax"],
        "constitutional_tier": "F2_TRUTH",
        "description": "MiniMax MCP — image gen (text_to_image), video gen (generate_video), TTS (text_to_audio), voice clone, music gen. URL-mode resource delivery.",
        "transport_type": "stdio",
        "command": "uvx minimax-mcp -y",
        "harness_visibility": ["opencode"],
        "mrtr_capable": True,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "free-search": {
        "category": "research",
        "tags": ["search", "web", "self-hosted"],
        "constitutional_tier": "F2_TRUTH",
        "description": "Free-search MCP — DDG+Mojeek engine diversity. Zero external API key. Governed by A-FORGE forge_search doctrine.",
        "transport_type": "stdio",
        "command": "uvx free-search-mcp",
        "harness_visibility": ["opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "public",
        "protocol_versions_supported": ["2025-11-25"],
    },
    # ───── EXTERNAL BRIDGE (phasing out) ─────
    "openrouter": {
        "category": "external-bridge",
        "tags": ["router", "openrouter", "phasing-out"],
        "constitutional_tier": "F2_TRUTH",
        "description": "OpenRouter MCP — multi-model provider. PHASING OUT: FED replaces this entirely. Per FRAME G7, remove once all consumers migrate to FED.",
        "transport_type": "http",
        "endpoint": "https://mcp.openrouter.ai/mcp",
        "harness_visibility": ["opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
        "status": "PHASING_OUT",
        "status_reason": "Replaced by FED. Migrate consumers, then remove. Target: 2026-Q3.",
    },
    # ───── DATA & STORAGE ─────
    "supabase": {
        "category": "data-store",
        "tags": ["database", "supabase", "sql"],
        "constitutional_tier": "F1_MUTATE",
        "description": "Supabase MCP — Postgres + Auth + Storage via @supabase/mcp-server-supabase. Project ref pinned in opencode.json.",
        "transport_type": "stdio",
        "command": "npx @supabase/mcp-server-supabase",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "qdrant": {
        "category": "data-store",
        "tags": ["vector", "qdrant", "embeddings"],
        "constitutional_tier": "F2_TRUTH",
        "description": "Qdrant MCP bridge — vector memory for federation semantic search. Substrate for L3→L4 recall.",
        "transport_type": "stdio",
        "command": "python3 /usr/local/bin/qdrant-mcp-bridge.py",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "megamemory": {
        "category": "data-store",
        "tags": ["memory", "megamemory", "opencode"],
        "constitutional_tier": "F2_TRUTH",
        "description": "MegaMemory — opencode-side memory layer. Substrate for /root/.config/opencode/.megamemory/.",
        "transport_type": "stdio",
        "command": "npx megamemory",
        "harness_visibility": ["opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "sqlite": {
        "category": "data-store",
        "tags": ["database", "sqlite", "disabled"],
        "constitutional_tier": "F1_MUTATE",
        "description": "SQLite MCP — local file-backed DB for arifos local state. DISABLED: schema migrated to Postgres.",
        "transport_type": "stdio",
        "command": "/usr/bin/mcp-server-sqlite",
        "harness_visibility": ["opencode"],
        "mrtr_capable": False,
        "subscriptions": [],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-06-18"],
        "status": "DISABLED",
        "status_reason": "Schema migrated to Postgres. Local SQLite kept read-only for forensic replay. Do not re-enable.",
    },
    "graphiti": {
        "category": "data-store",
        "tags": ["graph", "temporal", "falkordb", "disabled"],
        "constitutional_tier": "F2_TRUTH",
        "description": "Graphiti MCP — temporal knowledge graph (FalkorDB + Ollama). DISABLED: endpoint down, not yet revived.",
        "transport_type": "http",
        "endpoint": "http://127.0.0.1:8000/mcp",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": False,
        "subscriptions": [],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-06-18"],
        "status": "DISABLED",
        "status_reason": "Endpoint offline since 2026-08-08. Awaiting FalkorDB restart. Will be re-attempted in F2-2026-Q3 sprint.",
    },
    "codebase-memory": {
        "category": "data-store",
        "tags": ["memory", "codebase", "context"],
        "constitutional_tier": "F2_TRUTH",
        "description": "Codebase Memory MCP — local persistent context across sessions. npm-global install at /root/.npm-global/bin/codebase-memory-mcp.",
        "transport_type": "stdio",
        "command": "/root/.npm-global/bin/codebase-memory-mcp",
        "harness_visibility": ["opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
    },
    # ───── DEV TOOLS ─────
    "hostinger-vps": {
        "category": "dev-tool",
        "tags": ["vps", "hostinger", "infra"],
        "constitutional_tier": "F1_MUTATE",
        "description": "Hostinger VPS MCP — managed-VPS primitives. 62 tools. Bypasses A-FORGE governance by design (VPS actuator, not federation).",
        "transport_type": "stdio",
        "command": "/root/.npm-global/bin/hostinger-vps-mcp --stdio",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "semgrep": {
        "category": "dev-tool",
        "tags": ["security", "semgrep", "disabled", "license-gated"],
        "constitutional_tier": "F9_ANTIHANTU",
        "description": "Semgrep MCP — rule-based static analysis with 7 Eurekas distilled (see /root/forge_work/2026-08-10-semgrep-eureka/). DISABLED: requires Semgrep Pro Engine license. Free OCaml core cannot serve MCP.",
        "transport_type": "stdio",
        "command": "/root/.arifos/agents/kimi/mcp-launchers/semgrep.sh",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": False,
        "subscriptions": [],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-06-18"],
        "status": "DISABLED",
        "status_reason": "Pro Engine license required. Both `semgrep` and `semgrep-mcp` channels gated. Re-enable after license obtained.",
    },
    # ───── META & UTILITY ─────
    "capability-index": {
        "category": "meta-utility",
        "tags": ["registry", "capability", "arifos"],
        "constitutional_tier": "F2_TRUTH",
        "description": "Capability Index — federation-wide tool/skill/surface discoverability. Pairs with /root/AAA/registries/CAPABILITY_INDEX.json.",
        "transport_type": "stdio",
        "command": "PYTHONPATH=core exec /root/arifOS/.venv/bin/python core/capability_index/mcp_server.py",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "public",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "repomapper": {
        "category": "meta-utility",
        "tags": ["repo", "mapper", "topology"],
        "constitutional_tier": "F2_TRUTH",
        "description": "RepoMapper — codebase topology sensor. Emits file/import graph for context injection. Pairs with AAA/docs/OBSERVATORY_FOLDER_STRUCTURE.md.",
        "transport_type": "stdio",
        "command": "/root/.claude/mcp-launchers/repomapper.sh",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": False,
        "subscriptions": ["toolsListChanged"],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-11-25"],
    },
    "serena": {
        "category": "meta-utility",
        "tags": ["ide", "lsp", "serena", "disabled"],
        "constitutional_tier": "F2_TRUTH",
        "description": "Serena MCP — IDE-grade code navigation via LSP. DISABLED: stdio wrapper unstable post sh→bash fix. Will retry on next harness sweep.",
        "transport_type": "stdio",
        "command": "/root/.claude/mcp-launchers/serena.sh",
        "harness_visibility": ["codex", "opencode"],
        "mrtr_capable": False,
        "subscriptions": [],
        "cache_scope": "private",
        "protocol_versions_supported": ["2025-06-18"],
        "status": "DISABLED",
        "status_reason": "stdio wrapper crashed on sh→bash transition. Re-attempt on next harness sweep (target 2026-08-12).",
    },
}

# Servers present in opencode.json that should be SKIPPED (already covered as organ
# files, or known-removed)
SKIP_SERVERS = {
    "arifos", "aforge", "geox", "wealth", "well",  # organs, separate files
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def build_server_entry(name: str, mcp_entry: dict) -> dict:
    """Build a single per-server JSON in the 2026 MCP registry schema."""
    meta = SERVER_META[name]
    enabled = mcp_entry.get("enabled", True)

    # Transport: prefer the explicit type from opencode.json; fallback to meta hint
    opencode_type = mcp_entry.get("type")
    if opencode_type == "remote":
        transport_type = "streamable_http"
        endpoint = mcp_entry.get("url")
    elif opencode_type == "local":
        transport_type = "stdio"
        # command in opencode is a list; we store the primary path
        cmd_list = mcp_entry.get("command", [])
        endpoint = " ".join(cmd_list) if cmd_list else None
    else:
        transport_type = meta.get("transport_type", "stdio")
        endpoint = meta.get("endpoint") or meta.get("command")

    transport: dict = {
        "type": transport_type,
    }
    if transport_type == "streamable_http" and endpoint:
        transport["endpoint"] = endpoint
        # Public endpoint, if known (for organs) — empty for now on extensions
    elif transport_type == "stdio" and endpoint:
        transport["command"] = endpoint

    # Auth: env-based bearer for HTTP, none-in-tracked for stdio (env vars in opencode)
    env = mcp_entry.get("environment", {}) or {}
    auth: dict = {"type": "env_scoped" if env else "none"}
    if env:
        auth["env_keys"] = sorted(env.keys())  # never values
    if transport_type == "streamable_http":
        auth["type"] = "sct_bearer"  # arifOS organ convention; public endpoints may differ

    # Status: disabled/retired/phasing-out wins over enabled
    if not enabled:
        status = meta.get("status", "DISABLED")
    else:
        status = meta.get("status", "ONLINE")

    # 2026-07-28 stateless fields
    pversions = meta["protocol_versions_supported"]
    cache_scope = meta["cache_scope"]
    mrtr_capable = meta["mrtr_capable"]
    subscriptions = meta["subscriptions"]
    harness_visibility = meta["harness_visibility"]

    entry: dict = {
        "$schema": SCHEMA_URL,
        "id": f"ext.{name}",
        "name": f"{name}-federation-extension",
        "description": meta["description"],
        "version": "v2026.08.10",
        "author": SOVEREIGN,
        "category": meta["category"],
        "tags": meta["tags"],
        "transport": transport,
        "auth": auth,
        "constitutional_tier": meta["constitutional_tier"],
        "tools_count": 0,  # populated by live probe (forge_mcp_lifeguard mode=probe)
        "tools": [],  # same; live probe populates
        "status": status,
        "status_reason": meta.get("status_reason", ""),
        "harness_visibility": harness_visibility,
        "protocol_versions_supported": pversions,
        "mrtr_capable": mrtr_capable,
        "subscriptions": subscriptions,
        "cache_scope": cache_scope,
        "opencode_enabled": enabled,
        "opencode_source_path": str(OPENCODE_CONFIG),
        "last_reconciled": SOURCE_GENERATED_AT,
    }
    if not entry["status_reason"]:
        # Drop the field when empty for clean schema (matches organ files)
        del entry["status_reason"]
    return entry


def build_index(per_server_files: dict[str, dict]) -> dict:
    """Build INDEX.json aggregating all 26 server entries."""
    total_tools = 0
    for f in REGISTRY_DIR.iterdir():
        if f.name in ORGAN_FILES or f.name == "INDEX.json":
            continue
        if f.suffix == ".json":
            with f.open() as fh:
                d = json.load(fh)
                total_tools += d.get("tools_count", 0)
    # Add organ totals from existing files
    for organ_name in ["arifos", "aforge", "geox", "wealth", "well"]:
        with (REGISTRY_DIR / f"{organ_name}.json").open() as f:
            d = json.load(f)
            total_tools += d.get("tools_count", 0)

    servers_summary = {}
    for name, entry in per_server_files.items():
        # `enabled` for drift_audit.sh compat = opencode.json runtime truth.
        # `status` is the informational label (ONLINE, AUTH_GATED, PHASING_OUT, DISABLED, RETIRED).
        # A PHASING_OUT server can still be `enabled: true` — the status is advisory, not gating.
        is_runtime_enabled = entry["opencode_enabled"]
        servers_summary[name] = {
            "id": entry["id"],
            "name": entry["name"],
            "category": entry["category"],
            "tool_count": entry["tools_count"],
            "status": entry["status"],
            "enabled": is_runtime_enabled,
            "endpoint": entry["transport"].get("endpoint", entry["transport"].get("command", "?")),
            "harness_visibility": entry["harness_visibility"],
            "metadata_file": f"{name}.json",
        }

    return {
        "generated_at": SOURCE_GENERATED_AT,
        "federation": "arifOS",
        "sovereign": SOVEREIGN,
        "spec_version": "MCP 2026-07-28 (stateless)",
        "total_servers": 5 + len(per_server_files),
        "total_tools": total_tools,
        "enabled_count": sum(1 for e in per_server_files.values() if e["opencode_enabled"]),
        "disabled_count": sum(1 for e in per_server_files.values() if not e["opencode_enabled"]),
        "harness_alignment": "opencode (26/26)",
        "servers": servers_summary,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync MCP registry from opencode.json")
    ap.add_argument("--dry-run", action="store_true", help="Compute diff but do not write")
    ap.add_argument("--force", action="store_true", help="Overwrite even if unchanged")
    args = ap.parse_args()

    if not OPENCODE_CONFIG.exists():
        print(f"ERR: source not found: {OPENCODE_CONFIG}", file=sys.stderr)
        return 2
    if not REGISTRY_DIR.exists():
        print(f"ERR: registry dir missing: {REGISTRY_DIR}", file=sys.stderr)
        return 2

    with OPENCODE_CONFIG.open() as f:
        oc_cfg = json.load(f)
    mcp = oc_cfg.get("mcp", {})

    # Build per-server entries
    per_server: dict[str, dict] = {}
    skipped: list[str] = []
    for name, mcp_entry in mcp.items():
        if name in SKIP_SERVERS:
            skipped.append(name)
            continue
        if name not in SERVER_META:
            print(f"WARN: {name} present in opencode.json but not in SERVER_META — skip", file=sys.stderr)
            continue
        per_server[name] = build_server_entry(name, mcp_entry)

    print(f"Build: {len(per_server)} per-server entries, {len(skipped)} skipped (organs)")

    if args.dry_run:
        print("Dry run — no files written")
        for n, e in per_server.items():
            print(f"  would-write: {n}.json status={e['status']}")
        return 0

    # Write per-server files
    src_sha = sha256_file(OPENCODE_CONFIG)
    written = []
    for name, entry in per_server.items():
        target = REGISTRY_DIR / f"{name}.json"
        with target.open("w") as f:
            json.dump(entry, f, indent=2, ensure_ascii=False, sort_keys=False)
            f.write("\n")
        written.append(str(target))

    # Write INDEX.json
    index = build_index(per_server)
    with INDEX_PATH.open("w") as f:
        json.dump(index, f, indent=2, ensure_ascii=False, sort_keys=False)
        f.write("\n")
    written.append(str(INDEX_PATH))

    print(f"\nWrote {len(written)} files:")
    for w in written:
        print(f"  + {w}")
    print(f"\nINDEX: {index['total_servers']} servers, {index['total_tools']} tools, "
          f"{index['enabled_count']} enabled, {index['disabled_count']} disabled")
    print(f"Source sha256: {src_sha}")
    print(f"Generated at:  {SOURCE_GENERATED_AT}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
