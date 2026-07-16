#!/usr/bin/env python3
"""
Truth Kernel Acceptance Test — Card vs Registry Diff

Compares agent-card-declared tools against live MCP surface.
Exit 0 = all organs PASS. Exit 1 = drift detected.

Usage:
  python3 acceptance_test.py         # full test
  python3 acceptance_test.py --json  # JSON output

DITEMPA BUKAN DIBERI
"""

import json
import subprocess
import sys
from pathlib import Path

ORGANS = {
    "arifos": {"port": 8088, "card": "/root/AAA/agent-cards/organs/arifos/agent-card.json"},
    "aforge": {"port": 7072, "card": "/root/AAA/agent-cards/organs/aforge/agent-card.json"},
    "geox": {"port": 8081, "card": "/root/AAA/agent-cards/organs/geox/agent-card.json"},
    "wealth": {"port": 18082, "card": "/root/AAA/agent-cards/organs/wealth/agent-card.json"},
    "well": {"port": 18083, "card": "/root/AAA/agent-cards/organs/well/agent-card.json"},
}

WARGA_CARDS = {
    "333-AGI": "/root/AAA/agent-cards/identity/333-AGI/agent-card.json",
    "555-ASI": "/root/AAA/agent-cards/identity/555-ASI/agent-card.json",
    "888-APEX": "/root/AAA/agent-cards/identity/888-APEX/agent-card.json",
}


def probe_tools(port):
    try:
        r = subprocess.run(
            [
                "curl",
                "-sf",
                f"http://127.0.0.1:{port}/mcp",
                "-X",
                "POST",
                "-H",
                "Content-Type: application/json",
                "-d",
                '{"jsonrpc":"2.0","id":1,"method":"tools/list"}',
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        d = json.loads(r.stdout)
        return set(t["name"] for t in d.get("result", {}).get("tools", []))
    except Exception:
        return None  # probe failed


def load_card_tools(card_path):
    try:
        card = json.load(open(card_path))
    except Exception:
        return None, None

    tools = set()
    for ep in card.get("mcp_surface", {}).get("endpoints", []):
        ep_tools = ep.get("tools", [])
        for t in ep_tools:
            if isinstance(t, str):
                tools.add(t)
            elif isinstance(t, dict) and "name" in t:
                tools.add(t["name"])

    receipt_hash = card.get("registry_receipt_hash", "MISSING")
    admissible = card.get("admissible", None)

    return tools, {"hash": receipt_hash, "admissible": admissible}


def main():
    results = {}
    all_pass = True

    print("=" * 60)
    print("  TRUTH KERNEL ACCEPTANCE TEST")
    print("  Card-declared vs Registry-declared")
    print("=" * 60)

    for name, org in ORGANS.items():
        print(f"\n--- {name.upper()} :{org['port']} ---")

        live_tools = probe_tools(org["port"])
        card_tools, card_meta = load_card_tools(org["card"])

        if live_tools is None:
            print(f"  ⚠️  MCP probe FAILED — skipping organ")
            results[name] = {"status": "PROBE_FAILED", "live": 0, "card": len(card_tools) if card_tools else 0}
            continue

        if card_tools is None:
            print(f"  ❌ Card load FAILED")
            results[name] = {"status": "CARD_FAILED", "live": len(live_tools), "card": 0}
            all_pass = False
            continue

        # Diff
        in_card_not_live = card_tools - live_tools
        in_live_not_card = live_tools - card_tools
        overlap = card_tools & live_tools

        has_hash = card_meta["hash"] != "MISSING"
        is_admissible = card_meta["admissible"]

        # Verdict
        dead_names = in_card_not_live
        missing_names = in_live_not_card
        drift_pct = round(100 * len(overlap) / len(card_tools), 1) if card_tools else 100.0

        status = "PASS"
        if dead_names:
            status = "DRIFT"
            all_pass = False
        if not has_hash:
            status = "NO_HASH"
            all_pass = False
        if is_admissible is False:
            status = "INADMISSIBLE"
            all_pass = False

        print(f"  Live: {len(live_tools)} tools")
        print(f"  Card: {len(card_tools)} tools")
        print(f"  Overlap: {len(overlap)} ({drift_pct}%)")
        print(f"  Dead names (in card, not live): {len(dead_names)}")
        if dead_names:
            for t in sorted(dead_names)[:5]:
                print(f"    💀 {t}")
            if len(dead_names) > 5:
                print(f"    ... +{len(dead_names) - 5} more")
        print(f"  Missing (in live, not card): {len(missing_names)}")
        if missing_names:
            for t in sorted(missing_names)[:5]:
                print(f"    ⚠️  {t}")
        print(f"  Registry hash: {card_meta['hash']}")
        print(f"  Admissible: {is_admissible}")
        print(f"  VERDICT: {status}")

        results[name] = {
            "status": status,
            "live": len(live_tools),
            "card": len(card_tools),
            "overlap": len(overlap),
            "drift_pct": drift_pct,
            "dead_names": sorted(dead_names),
            "missing_names": sorted(missing_names),
            "hash": card_meta["hash"],
            "admissible": is_admissible,
        }

    # Warga cards check
    print(f"\n{'=' * 60}")
    print(f"  WARGA CARD INTEGRITY")
    print(f"{'=' * 60}")

    for warga_name, card_path in WARGA_CARDS.items():
        card_tools, card_meta = load_card_tools(card_path)
        if card_tools is None:
            print(f"  ❌ {warga_name}: card load FAILED")
            all_pass = False
            continue
        has_hash = card_meta["hash"] != "MISSING"
        print(f"  {'✅' if has_hash else '⚠️'}  {warga_name}: {len(card_tools)} tools, hash={card_meta['hash']}")
        results[f"warga_{warga_name}"] = {"status": "PASS" if has_hash else "NO_HASH", "tools": len(card_tools)}

    # Summary
    print(f"\n{'=' * 60}")
    print(f"  ACCEPTANCE VERDICT")
    print(f"{'=' * 60}")

    organ_statuses = [r["status"] for k, r in results.items() if not k.startswith("warga_")]
    passed = sum(1 for s in organ_statuses if s == "PASS")
    total = len(organ_statuses)

    print(f"  Organs: {passed}/{total} PASS")
    print(f"  Overall: {'✅ PASS' if all_pass else '❌ DRIFT DETECTED'}")

    if not all_pass:
        print(f"\n  FAILED ORGANS:")
        for k, r in results.items():
            if r.get("status") not in ("PASS",):
                print(f"    {k}: {r['status']}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
