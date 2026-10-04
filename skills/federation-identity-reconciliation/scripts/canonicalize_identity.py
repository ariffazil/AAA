#!/usr/bin/env python3
"""Canonicalize CANONICAL_ACTORS identity.py to align three source trees.

Reads the canonical /opt/arifos/app/contracts/identity.py, extracts
CANONICAL_ACTORS dict, then patches:
  1. /opt/arifos/identity/agent_identities.json  (registry)
  2. /root/A-FORGE/data/agent_identities.json   (mirror)
  3. /root/arifOS/contracts/identity.py          (source)
  4. /root/arifOS/arifosmcp/contracts/identity.py (source)
  5. /opt/arifos/app/contracts/identity.py       (deploy)

Adds missing canonical actors (QWEN, KIMI, CODEX, etc.) to registries
and ensures identity.py is identical across all three source trees.

Usage:
  python3 canonicalize_identity.py [--dry-run]

Authoritative source: /opt/arifos/app/contracts/identity.py
Created: 2026-08-12, federation-identity-reconciliation skill reference.
"""
import json
import os
import sys
import shutil
from pathlib import Path
from typing import Any

DRY_RUN = "--dry-run" in sys.argv

CANONICAL_ACTORS_PY = "/opt/arifos/app/contracts/identity.py"
REGISTRY_PRIMARY = "/opt/arifos/identity/agent_identities.json"
REGISTRY_MIRROR = "/root/A-FORGE/data/agent_identities.json"

SOURCE_TREES = [
    "/root/arifOS/contracts/identity.py",
    "/root/arifOS/arifosmcp/contracts/identity.py",
]

# Canonical actor entries to ensure exist in registries
# Format: key → {sovereign_id, default_tier, aliases}
CANONICAL_REGISTRY_ENTRIES = {
    "FORGE": {"sovereign_id": "ARIF_FAZIL", "default_tier": "AGENT", "aliases": ["forge", "a-forge"]},
    "hermes": {"sovereign_id": "ARIF_FAZIL", "default_tier": "AGENT", "aliases": ["hermes", "hermes-asi"]},
    "openclaw": {"sovereign_id": "ARIF_FAZIL", "default_tier": "OPERATOR", "aliases": ["openclaw", "OpenClaw"]},
    "opencode": {"sovereign_id": "ARIF_FAZIL", "default_tier": "AGENT", "aliases": ["opencode", "OpenCode"]},
    "qwen-code": {"sovereign_id": "ARIF_FAZIL", "default_tier": "AGENT", "aliases": ["qwen-code", "QWEN"]},
    "kimi-code": {"sovereign_id": "ARIF_FAZIL", "default_tier": "AGENT", "aliases": ["kimi-code", "KIMI"]},
    "codex": {"sovereign_id": "ARIF_FAZIL", "default_tier": "AGENT", "aliases": ["codex", "codex-cli"]},
}


def sync_registry(primary: Path, mirror: Path) -> dict[str, list[str]]:
    """Sync primary registry to mirror, report differences."""
    with open(primary) as f:
        p_data = json.load(f)
    with open(mirror) as f:
        m_data = json.load(f)

    p_keys = set(p_data.keys())
    m_keys = set(m_data.keys())

    added_to_mirror = p_keys - m_keys
    added_to_primary = m_keys - p_keys

    # Add missing to mirror
    for k in added_to_mirror:
        m_data[k] = p_data[k]

    # Add missing to primary from canonical entries
    for k, v in CANONICAL_REGISTRY_ENTRIES.items():
        if k not in p_data:
            p_data[k] = v
            added_to_primary.add(k)

    if not DRY_RUN:
        with open(primary, "w") as f:
            json.dump(p_data, f, indent=2, ensure_ascii=False)
        with open(mirror, "w") as f:
            json.dump(m_data, f, indent=2, ensure_ascii=False)

    return {
        "added_to_mirror": sorted(added_to_mirror),
        "added_to_primary": sorted(added_to_primary - added_to_mirror),
        "mirror_has_extras": sorted(m_keys - p_keys),
        "total_p": len(p_data),
        "total_m": len(m_data),
        "match": set(p_data.keys()) == set(m_data.keys()),
    }


def sync_source_trees() -> list[dict[str, Any]]:
    """Ensure identity.py is identical across deployed + source trees."""
    results = []
    deployed = Path(CANONICAL_ACTORS_PY)

    for src in SOURCE_TREES:
        src_path = Path(src)
        if not src_path.exists():
            results.append({"path": src, "status": "MISSING"})
            continue

        if deployed.read_text() == src_path.read_text():
            results.append({"path": src, "status": "identical"})
        else:
            if not DRY_RUN:
                shutil.copy2(deployed, src_path)
            results.append({"path": src, "status": "synced_from_deployed" if not DRY_RUN else "DRIFT"})

    return results


def verify_normalization() -> list[dict[str, str]]:
    """Test that key actors normalize correctly."""
    sys.path.insert(0, "/root/arifOS")
    from arifosmcp.contracts.identity import normalize_actor_identity

    test_cases = [
        ("qwen-code", "QWEN"),
        ("qwen-code/FI-003", "QWEN"),  # slash form should also resolve via aliases
        ("kimi-code", "FI-008"),
        ("codex", "codex"),
        ("claude-code", "CLAUDE"),
        ("opencode", "OPENCODE"),
        ("hermes", "HERMES"),
    ]

    results = []
    for actor_id, expected in test_cases:
        r = normalize_actor_identity(actor_id)
        normalized = r.get("normalized", "NONE") if isinstance(r, dict) else "ERROR"
        ok = normalized == expected
        results.append({
            "input": actor_id,
            "expected": expected,
            "got": normalized,
            "ok": ok,
        })
    return results


def main():
    print("=" * 60)
    print("CANONICAL IDENTITY SWEEP")
    print(f"Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")
    print("=" * 60)

    # 1. Registry sync
    print("\n── Registry Sync ──")
    r = sync_registry(Path(REGISTRY_PRIMARY), Path(REGISTRY_MIRROR))
    print(f"  Primary keys: {r['total_p']}")
    print(f"  Mirror keys:  {r['total_m']}")
    print(f"  Match: {r['match']}")
    if r["added_to_mirror"]:
        print(f"  Added to mirror: {r['added_to_mirror']}")
    if r["added_to_primary"]:
        print(f"  Added to primary: {r['added_to_primary']}")
    if r["mirror_has_extras"]:
        print(f"  ⚠️ Mirror extras (not in primary): {r['mirror_has_extras']}")

    # 2. Source tree sync
    print("\n── Source Tree Sync ──")
    for result in sync_source_trees():
        status = result["status"]
        icon = "✅" if status == "identical" else "🔧" if status == "synced_from_deployed" else "❌"
        print(f"  {icon} {result['path']}: {status}")

    # 3. Normalization verification
    print("\n── Normalization Verification ──")
    all_ok = True
    for r in verify_normalization():
        icon = "✅" if r["ok"] else "❌"
        print(f"  {icon} {r['input']:25s} → {r['got']:15s} (expected {r['expected']})")
        if not r["ok"]:
            all_ok = False

    print("\n" + "=" * 60)
    if all_ok:
        print("✅ All identity normalization tests pass")
    else:
        print("❌ Some normalization tests failed — check CANONICAL_ACTORS aliases")
    print("=" * 60)


if __name__ == "__main__":
    main()
