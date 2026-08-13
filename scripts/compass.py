#!/usr/bin/env python3
"""
COMPASS LAYER — Orthogonal Router (fail-closed tool gate)
==========================================================
Reads SKILL.md frontmatter (required_tools + tool_gate) and emits a
per-skill tool allowlist. F1 FAIL-CLOSED: no metadata → strict OBSERVE_ONLY
minimum, never leak all 62 tools.

Contract:  SCHEMA_STANDARD_required_tools_tool_gate_v1.md
Registry:  TOOL_INVENTORY.jsonl (exact names) + known native/MCP tools.
Deterministic, no LLM in gate.
Usage:
  python3 compass.py --skill <name>                # allowlist for one
  python3 compass.py --skill ocr --show            # with denied/reason
  python3 compass.py --audit                       # all skills, summary
F1 floors: fail-closed, exact-match only, never mutates skill files.
DITEMPA BUKAN DIBERI.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

AAA = Path("/root/AAA/skills")
INVENTORY = Path("/root/forge_work/2026-08-10-browser-zen/TOOL_INVENTORY.jsonl")
INDEX = Path("/root/AAA/skills_index.json")

# Native Hermes/MCP tools that are valid even if not in A-FORGE TOOL_INVENTORY.jsonl
# (inventory is A-FORGE-centric category A-G; these are harness-native / organ MCP).
NATIVE_TOOLS = {
    "vision_analyze", "image_generate", "image_edit", "terminal", "read_file",
    "write_file", "patch", "search_files", "web_search", "web_extract",
    "arif_observe", "arif_think", "arif_memory", "arif_init", "arif_route",
    "arif_judge", "arif_seal", "delegate_task", "cronjob", "memory",
    "browser_exec", "browser_navigate", "forge_fetch", "forge_search",
    "forge_health_check", "forge_probe", "forge_scan", "forge_seal", "forge_vault",
    "forge_well", "forge_wealth", "forge_docker", "forge_git", "forge_postgres",
    "skill_view", "skills_list", "skill_manage", "computer_use", "vision",
}

def load_inventory_names() -> set[str]:
    names = set()
    try:
        for line in INVENTORY.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                names.add(json.loads(line).get("tool"))
            except json.JSONDecodeError:
                n = re.search(r'"tool"\s*:\s*"([^"]+)"', line)
                if n:
                    names.add(n.group(1))
    except FileNotFoundError:
        pass
    return names

def parse_fm(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    try:
        import yaml
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        # fallback: line parse
        d = {}
        for line in m.group(1).splitlines():
            if ":" in line and not line.lstrip().startswith("-"):
                k, _, v = line.partition(":")
                d[k.strip()] = v.strip()
        return d

def find_skill(name: str) -> Path | None:
    idx = None
    if INDEX.exists():
        try:
            idx = json.loads(INDEX.read_text())
        except Exception:
            idx = None
    if idx:
        for s in idx["skills"]:
            if s["name"] == name:
                return Path(s["path"])
    # fallback walk
    for p in AAA.rglob("SKILL.md"):
        if p.parent.name == name:
            return p
    return None

def extract_tools_from_fm(fm: dict) -> tuple[str, list[str]]:
    """Return (gate, tools). FAIL-CLOSED defaults."""
    seen = {"strict", "permissive"}
    raw_gate = str(fm.get("tool_gate", "")).strip().lower()
    gate = raw_gate if raw_gate in seen else "strict"  # fail-closed
    rt = fm.get("required_tools")
    if isinstance(rt, str):
        import ast
        try:
            rt = ast.literal_eval(rt)
        except Exception:
            rt = [x.strip() for x in rt.replace("[","").replace("]","").split(",") if x.strip()]
    if not isinstance(rt, list):
        rt = []
    return gate, [str(t).strip() for t in rt if str(t).strip()]

VALID = load_inventory_names() | NATIVE_TOOLS
# core observation tools always allowed under strict (fail-safe OBSERVE floor)
OBSERVE_FLOOR = {"arif_observe", "forge_fetch"}

def reward_for(skill_path: Path | None, request: str) -> dict:
    if not skill_path or not skill_path.exists():
        return {"skill": request, "found": False, "gate": "strict",
                "tools": sorted(OBSERVE_FLOOR), "denied": [],
                "reason": "skill_not_found→fail_closed OBSERVE_ONLY floor"}
    fm = parse_fm(skill_path.read_text())
    gate, declared = extract_tools_from_fm(fm)
    risk = str(fm.get("risk_tier", "low")).lower()
    # F1 override: high risk + not strict → force strict
    if risk in ("high", "critical") and gate != "strict":
        gate = "strict"
    valid = [t for t in declared if t in VALID]
    invalid = [t for t in declared if t not in VALID]
    all_tools = list(valid) if gate == "strict" else list(set(valid) | OBSERVE_FLOOR)
    if not all_tools:
        all_tools = sorted(OBSERVE_FLOOR)
    return {"skill": skill_path.parent.name, "found": True, "gate": gate,
            "tools": sorted(set(all_tools)), "denied": sorted(set(invalid)),
            "risk_override": risk in ("high", "critical"),
            "declared": declared}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", help="skill name to resolve allowlist")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--audit", action="store_true")
    a = ap.parse_args()
    if a.skill:
        r = reward_for(find_skill(a.skill), a.skill)
        print(json.dumps(r, indent=2))
        return 0
    if a.audit:
        import os
        total = found = fail_closed = 0
        for sk in AAA.rglob("SKILL.md"):
            total += 1
            r = reward_for(sk, sk.parent.name)
            if r["found"]:
                found += 1
                if len(r["tools"]) == len(OBSERVE_FLOOR) and r["gate"] == "strict":
                    fail_closed += 1
        print(f"audit: total={total} found={found} fail_closed_default={fail_closed} "
              f"({100*fail_closed/max(total,1):.0f}%)")
        print(f"registry: {len(VALID)} valid tool names (inventory+native)")
        return 0
    print("usage: compass.py --skill <name> [--show] | --audit")
    return 1

if __name__ == "__main__":
    sys.exit(main())