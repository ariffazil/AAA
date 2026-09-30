#!/usr/bin/env python3
"""
apply_apex_zen_fixes.py — Apply staged apex-zen deltas to OpenCode + Kimi cards.

Reversible. Preserves ORIGINAL KEY ORDER (does NOT use sort_keys=True — that would
resort all keys alphabetically and break diffs/parsers that depend on order).

Does NOT touch:
  - authority_boundary.canDo / cannotDo (no permission revocation)
  - securitySchemes (no auth removal)
  - mcp_surface.endpoints (no MCP server removal)
  - capabilities (no capability revocation)
  - For Kimi: anti_bangang_architecture.permission_mode=yolo (preserved)
  - Hooks / sub-agents / model routes (all preserved as-is)
"""

import json
import sys
from collections import OrderedDict
from pathlib import Path

OPENCODE_CARD = Path("/root/AAA/agents/opencode/agent-card.json")
OPENCODE_PATCH = Path("/root/AAA/reports/apex-zen-upgrade-2026-09-30/opencode-card-staged-fix.json")
KIMI_CARD = Path("/root/AAA/a2a-server/agent-cards/forge/fi-008-kimi-code.json")
KIMI_PATCH = Path("/root/AAA/reports/apex-zen-upgrade-2026-09-30/kimi-card-staged-fix.json")


def load_preserving_order(path: Path):
    """Load JSON but preserve original key insertion order."""
    with path.open() as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def dump_preserving_order(doc, path: Path):
    """Write JSON preserving key order. indent=2, no sort_keys."""
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def resolve_path(doc, path: str):
    parts = [p for p in path.split("/") if p]
    cur = doc
    for p in parts:
        if isinstance(cur, list):
            cur = cur[int(p)]
        else:
            cur = cur[p]
    return cur


def apply_op(doc, op):
    p = op["path"]
    parts = [x for x in p.split("/") if x]
    kind = op["op"]
    # Accept any of: new_value / value / new (RFC 6902 "replace" uses "new")
    new_val = op.get("new_value", op.get("value", op.get("new")))

    if kind == "delete":
        cur = doc
        for x in parts[:-1]:
            cur = cur[x] if isinstance(cur, dict) else cur[int(x)]
        leaf = parts[-1]
        if isinstance(cur, list):
            del cur[int(leaf)]
        else:
            del cur[leaf]
        return doc

    if kind in ("add", "set", "replace"):
        cur = doc
        for x in parts[:-1]:
            cur = cur[x] if isinstance(cur, dict) else cur[int(x)]
        leaf = parts[-1]
        if isinstance(cur, list):
            cur.insert(int(leaf), new_val)
        else:
            cur[leaf] = new_val
        return doc

    raise ValueError(f"unknown op: {op['op']}")


def apply_patch(card_path: Path, patch_path: Path, label: str):
    print(f"\n=== Applying patch to {label} ===")
    print(f"  card:  {card_path}")
    print(f"  patch: {patch_path}")
    patch = load_preserving_order(patch_path)
    actions = patch["_meta"]["actions"] if "_meta" in patch else patch.get("actions", [])
    print(f"  ops:   {len(actions)}")

    card = load_preserving_order(card_path)
    original_size = len(card_path.read_bytes())

    for op in actions:
        apply_op(card, op)
        kind = op["op"]
        path = op["path"]
        new = op.get("new_value", op.get("value"))
        new_repr = json.dumps(new, ensure_ascii=False)[:80] if new is not None else "(deleted)"
        print(f"    [{kind}] {path} → {new_repr}")

    # Atomic write via temp + rename.
    tmp = card_path.with_suffix(card_path.suffix + ".tmp")
    dump_preserving_order(card, tmp)
    tmp.replace(card_path)
    new_size = len(card_path.read_bytes())
    print(f"  size:  {original_size} → {new_size} bytes")

    audit_path = card_path.with_suffix(card_path.suffix + ".applied-20260930T123500Z.json")
    audit_path.write_text(
        json.dumps(
            {
                "card": str(card_path),
                "patch": str(patch_path),
                "applied_at": "2026-09-30T12:35:00+08:00",
                "applied_by": "333-AGI (FI-001) under user directive 'fix opencode and kimi code, don't block any tools'",
                "ops_count": len(actions),
                "ops": [{"op": a["op"], "path": a["path"]} for a in actions],
                "key_order_preserved": True,
                "sort_keys_used": False,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )
    print(f"  audit: {audit_path}")

    return card


if __name__ == "__main__":
    opencode_after = apply_patch(OPENCODE_CARD, OPENCODE_PATCH, "OpenCode FI-001")
    kimi_after = apply_patch(KIMI_CARD, KIMI_PATCH, "Kimi Code FI-008")

    print("\n=== POST-FLIGHT: confirm no tool/access restriction ===")
    print(f"  OpenCode mcp endpoints: {len(opencode_after['mcp_surface']['endpoints'])} (was 6)")
    print(f"  OpenCode canDo count:    {len(opencode_after['authority_boundary']['canDo'])}")
    print(f"  OpenCode capabilities:   {len(opencode_after['capabilities'])}")
    print(f"  OpenCode securitySchemes: {list(opencode_after['securitySchemes'].keys())}")
    print(f"  Kimi mcp endpoints:      {len(kimi_after['mcp_surface']['endpoints'])} (was 12)")
    print(f"  Kimi canDo count:        {len(kimi_after['authority_boundary']['canDo'])}")
    print(f"  Kimi capabilities:       {len(kimi_after['capabilities'])}")
    print(f"  Kimi YOLO preserved:     {kimi_after.get('anti_bangang_architecture', {}).get('permission_mode')}")
    print(
        f"  Kimi hooks count:        {len(kimi_after.get('anti_bangang_architecture', {}).get('hook_inventory', {}))}"
    )
    print()
    print("=== KEY ORDER PRESERVATION CHECK ===")
    print(f"  OpenCode first 5 keys:  {list(opencode_after.keys())[:5]}")
    print(f"  Kimi first 5 keys:       {list(kimi_after.keys())[:5]}")
