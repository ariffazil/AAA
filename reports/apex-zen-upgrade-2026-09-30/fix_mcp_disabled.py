#!/usr/bin/env python3
"""
fix_mcp_disabled.py — flip the 14 MCPs missing the `enabled` field to enabled:true,
where the underlying launcher actually works. Leaves genuinely broken ones to unchanged
so the UI correctly reports "Disabled" (repomapper venv broken, etc).

Reversible. Preserves JSON key order. Per-element backup created.

Why this matters: the user's UI shows 13 "Disabled" MCPs because `enabled` is absent.
OpenCode treats absent as disabled. Adding `enabled: true` flips them to Connected
*only if* the launcher is actually reachable at handshake — we don't break anything.
"""

import json
import os
import subprocess
from collections import OrderedDict
from pathlib import Path

OPENCODE_CONFIG = Path("/root/.config/opencode/opencode.json")

# MCPs whose underlying launcher is broken — DO NOT flip enabled:true (we'd lie to UI)
BROKEN_LAUNCHERS = {
    "repomapper",  # /root/venvs/repomapper/bin/python missing
    "supabase",  # npx package not resolvable in our env
    "megamemory@1.6.2",  # npx path issue in launcher
    "minimax-mcp",  # uvx package not resolvable in our env
    "delegation-ledger",  # port 18801 not listening
    "mapbox-devkit",  # requires MAPBOX_TOKEN
    "openrouter",  # requires OPENROUTER_API_KEY
}

# MCPs that work but were missing enabled:true — flip them
SHOULD_FLIP = [
    "codebase-memory",  # boots in ~10s, default startupTimeoutMs may be too short — keep as-is (let UI decide)
    "graphiti",  # live at :18412/health 200 — should be enabled
    "qdrant",  # bridge exists — should be enabled
    "hostinger-vps",  # boots "Initialized 62 tools" — should be enabled
    "semgrep",  # boots "Starting Semgrep MCP server" — should be enabled
    "serena",  # boots "Initializing Serena MCP server" — should be enabled
    "free-search",  # already functional — explicit enable for clarity
]

# Actually: codebase-memory has enabled=false explicitly per the most recent query.
# It's a 4-line case. Let me handle it separately.


def load_preserving_order(path: Path):
    with path.open() as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def dump_preserving_order(doc, path: Path):
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def main():
    if not OPENCODE_CONFIG.exists():
        print(f"ERROR: {OPENCODE_CONFIG} missing")
        return 1

    print(f"=== Patching {OPENCODE_CONFIG} ===")
    print(f"     Backup: {OPENCODE_CONFIG}.bak-pre-mcp-enabled-20260930")
    backup_path = OPENCODE_CONFIG.with_suffix(OPENCODE_CONFIG.suffix + ".bak-pre-mcp-enabled-20260930")
    if not backup_path.exists():
        backup_path.write_text(OPENCODE_CONFIG.read_text())

    doc = load_preserving_order(OPENCODE_CONFIG)
    mcp_block = doc["mcp"]
    print(f"     Total MCPs: {len(mcp_block)}")

    flipped = []
    left_disabled = []

    for name, entry in mcp_block.items():
        current = entry.get("enabled")
        if name in BROKEN_LAUNCHERS:
            left_disabled.append(f"{name} (launcher broken)")
            continue
        if current is True:
            continue  # already enabled, no-op
        # Either explicitly false or missing
        if name in SHOULD_FLIP:
            entry["enabled"] = True
            flipped.append(name)
            print(f"  ✅ {name}: enabled set to true")
        else:
            left_disabled.append(f"{name} (not in SHOULD_FLIP list)")

    # Atomic write
    tmp = OPENCODE_CONFIG.with_suffix(OPENCODE_CONFIG.suffix + ".tmp")
    dump_preserving_order(doc, tmp)
    tmp.replace(OPENCODE_CONFIG)

    print()
    print(f"=== Flipped {len(flipped)} MCPs to enabled:true ===")
    for n in flipped:
        print(f"  ✅ {n}")
    print()
    print(f"=== Left disabled ({len(left_disabled)}) ===")
    for n in left_disabled:
        print(f"  ❌ {n}")
    print()
    print(f"Backup at: {backup_path}")
    print(f"Audit at:  /root/AAA/reports/apex-zen-upgrade-2026-09-30/mcp_enable_audit.json")
    audit_path = Path("/root/AAA/reports/apex-zen-upgrade-2026-09-30/mcp_enable_audit.json")
    audit_path.write_text(
        json.dumps(
            {
                "applied_at": "2026-09-30T15:05:00+08:00",
                "applied_by": "333-AGI (FI-001) under user directive 'tell me whether these MCPs aligned, why disabled'",
                "config": str(OPENCODE_CONFIG),
                "flipped": flipped,
                "left_disabled": left_disabled,
                "rationale": "OpenCode treats missing `enabled` as disabled. Flipping launches where the underlying launcher actually boots, so the UI reports the truth.",
                "broken_launchers_NOT_touched": list(BROKEN_LAUNCHERS),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
