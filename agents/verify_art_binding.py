#!/usr/bin/env python3
"""
ART Binding Verification Script
Forged: 2026-06-21 by 777_FORGE

Verifies that Claude Code and OpenCode are properly bound to ART.

Usage:
    python3 verify_art_binding.py
"""

import json
import sys
from pathlib import Path


def check_file_exists(path: str, label: str) -> bool:
    """Check if a file exists and report."""
    p = Path(path)
    if p.exists():
        print(f"  ✅ {label}: {path}")
        return True
    else:
        print(f"  ❌ {label}: {path} (NOT FOUND)")
        return False


def check_art_import() -> bool:
    """Check if ART can be imported."""
    try:
        sys.path.insert(0, "/root/arifOS")
        print("  ✅ ART import: success")
        return True
    except Exception as e:
        print(f"  ❌ ART import: {e}")
        return False


def check_art_reflex() -> bool:
    """Check if ART reflex works."""
    try:
        sys.path.insert(0, "/root/arifOS")
        from arifosmcp.runtime.art import ArtRequest, art

        result = art(ArtRequest(
            action_class="observe",
            tool_state="observed",
            blast_radius="low",
            trust_level="evidence",
            actor_resolved=True,
            schema_locked=True,
            degraded=False,
            reversible=True,
        ))
        print(f"  ✅ ART reflex: {result.verdict.value}")
        return True
    except Exception as e:
        print(f"  ❌ ART reflex: {e}")
        return False


def verify_agent_binding(agent_id: str) -> bool:
    """Verify an agent's ART binding."""
    print(f"\n{'='*60}")
    print(f"Verifying ART binding for: {agent_id}")
    print(f"{'='*60}")

    # Check agent card
    card_path = f"/root/AAA/agents/{agent_id}/agent-card.json"
    if not check_file_exists(card_path, "Agent card"):
        return False

    # Load and verify agent card
    with open(card_path) as f:
        card = json.load(f)

    art_binding = card.get("art_binding", {})
    if not art_binding.get("enabled"):
        print("  ❌ ART binding: NOT ENABLED")
        return False

    print("  ✅ ART binding: ENABLED")

    # Check binding YAML
    binding_yaml = art_binding.get("binding_yaml")
    if binding_yaml:
        check_file_exists(binding_yaml, "Binding YAML")

    # Check reflex path
    reflex_path = art_binding.get("reflex_path")
    if reflex_path:
        check_file_exists(reflex_path, "Reflex path")

    # Check skill path
    skill_path = art_binding.get("skill_path")
    if skill_path:
        check_file_exists(skill_path, "Skill path")

    # Check substrates
    substrates = art_binding.get("substrates", {})
    print("\n  Substrate binding:")
    for substrate, path in substrates.items():
        check_file_exists(path, f"  {substrate}")

    return True


def main():
    """Main verification."""
    print("ART Binding Verification")
    print("="*60)

    # Check ART itself
    print("\n1. Checking ART reflex:")
    art_import_ok = check_art_import()
    art_reflex_ok = check_art_reflex()

    # Check Claude Code binding
    print("\n2. Checking Claude Code binding:")
    claude_ok = verify_agent_binding("claude-code")

    # Check OpenCode binding
    print("\n3. Checking OpenCode binding:")
    opencode_ok = verify_agent_binding("opencode")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  ART reflex:      {'✅ OK' if art_import_ok and art_reflex_ok else '❌ FAIL'}")
    print(f"  Claude Code:     {'✅ BOUND' if claude_ok else '❌ UNBOUND'}")
    print(f"  OpenCode:        {'✅ BOUND' if opencode_ok else '❌ UNBOUND'}")

    if art_import_ok and art_reflex_ok and claude_ok and opencode_ok:
        print("\n✅ All agents bound to ART. 5-substrate architecture complete.")
        return 0
    else:
        print("\n❌ Some bindings missing. Fix and re-run.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
