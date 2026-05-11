#!/usr/bin/env python3
"""
README SOT Audit — arifOS ecosystem
Scans repo architecture, compares against README claims, reports DELTAs.
DITEMPA BUKAN DIBERI — Intelligence is forged, not given.
"""
import json
import sys
import os
import re
from pathlib import Path
from typing import Optional

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def scan_tool_registry(repo_root: Path) -> dict:
    """Extract facts from arifOS tool_registry.json"""
    registry_path = repo_root / "arifosmcp" / "tool_registry.json"
    if not registry_path.exists():
        return {"found": False}

    with open(registry_path) as f:
        d = json.load(f)

    tools_data = d.get("tools", [])
    # Handle both list format (MCP) and dict format (CANONICAL_TOOLS)
    if isinstance(tools_data, dict):
        tool_names = sorted(tools_data.keys())
        tool_count = len(tools_data)
    elif isinstance(tools_data, list):
        tool_names = sorted([
            t.get("function", {}).get("name", "?") if isinstance(t, dict) else str(t)
            for t in tools_data
        ])
        tool_count = len(tools_data)
    else:
        tool_names = []
        tool_count = 0

    return {
        "found": True,
        "registry_version": d.get("registry_version"),
        "build_epoch": d.get("build_epoch"),
        "build_timestamp": d.get("build_timestamp"),
        "system": d.get("system"),
        "description": d.get("description"),
        "tool_count": tool_count,
        "tool_names": tool_names,
        "floor_count": d.get("governance", {}).get("floor_count"),
    }


def scan_constitutional_map(repo_root: Path) -> dict:
    """Extract CANONICAL_TOOLS from constitutional_map.py"""
    cmap_path = repo_root / "arifosmcp" / "constitutional_map.py"
    if not cmap_path.exists():
        return {"found": False}

    content = cmap_path.read_text()

    # Count arif_ tool definitions
    tool_defs = re.findall(r'"(arif_\w+)":', content)
    stage_map = re.findall(r'ToolStage\.(\w+)', content)
    stages = re.findall(r'"stage":\s*ToolStage\.(\w+)', content)

    return {
        "found": True,
        "canonical_tool_count": len(tool_defs),
        "tool_defs": sorted(tool_defs),
        "stages": stages,
    }


def scan_megatools(repo_root: Path) -> list[str]:
    """List megaTools/*.py files"""
    mega_path = repo_root / "arifosmcp" / "megaTools"
    if not mega_path.exists():
        return []
    return sorted([
        f.name for f in mega_path.glob("tool_*.py")
    ])


def scan_tools_dir(repo_root: Path) -> list[str]:
    """List arifosmcp/tools/*.py (excluding __init__, base.py, manifests)"""
    tools_path = repo_root / "arifosmcp" / "tools"
    if not tools_path.exists():
        return []
    return sorted([
        f.name for f in tools_path.glob("*.py")
        if f.name not in ("__init__.py", "base.py", "registry.py")
        and not str(f).endswith("__pycache__")
    ])


def scan_runtime_dirs(repo_root: Path) -> dict[str, int]:
    """Count files in key runtime directories"""
    counts = {}
    for subdir in ["runtime", "core", "providers", "apps"]:
        path = repo_root / "arifosmcp" / subdir
        if path.exists():
            py_files = list(path.rglob("*.py"))
            py_files = [f for f in py_files if "__pycache__" not in str(f)]
            counts[subdir] = len(py_files)
    return counts


def scan_readme_claims(repo_root: Path) -> dict:
    """Extract what README claims about tools, version, endpoints"""
    readme_path = repo_root / "README.md"
    if not readme_path.exists():
        return {"found": False}

    content = readme_path.read_text()

    # Version claim
    version_match = re.search(r"VERSION:\s*(.+)", content)
    version_claim = version_match.group(1).strip() if version_match else None

    # Build epoch
    epoch_match = re.search(r"BUILD_EPOCH[:\s]*(\d{4}\.\d{2}\.\d{2})", content)
    build_epoch_claim = epoch_match.group(1) if epoch_match else None

    # Tool count claim
    tool_count_match = re.search(r"(\d+)\s+tools?", content)
    tool_count_claim = int(tool_count_match.group(1)) if tool_count_match else None

    # Tool names claimed
    tool_rows = re.findall(r'`(arifos_\w+)`', content)

    # Endpoints claimed
    endpoint_rows = re.findall(r'`(/[\w-]+)`', content)

    # Floors claimed
    floor_match = re.search(r"F\d+.*?F13", content)
    floors_claim = floor_match.group(0)[:30] if floor_match else None

    return {
        "found": True,
        "version": version_claim,
        "build_epoch": build_epoch_claim,
        "tool_count": tool_count_claim,
        "tool_names": tool_rows,
        "endpoints": endpoint_rows,
        "floors_claim": floors_claim,
    }


def extract_sot_sections(readme_path: Path) -> dict[str, str]:
    """Extract content between SOT markers"""
    content = readme_path.read_text()
    pattern = r'<!-- SOT:(\w+) -->(.*?)<!-- /SOT:\1 -->'
    matches = re.findall(pattern, content, re.DOTALL)
    return {name: body.strip() for name, body in matches}


def audit_repo(repo_path: str, repo_name: str) -> dict:
    """Full audit of one repo"""
    repo_root = Path(repo_path)
    results = {
        "repo": repo_name,
        "deltas": [],
        "oks": [],
        "errors": [],
    }

    # --- Tool registry facts ---
    reg = scan_tool_registry(repo_root)
    cmap = scan_constitutional_map(repo_root)
    megatools = scan_megatools(repo_root)
    tools_dir = scan_tools_dir(repo_root)
    runtime_counts = scan_runtime_dirs(repo_root)
    claims = scan_readme_claims(repo_root)
    sot_sections = extract_sot_sections(repo_root / "README.md")

    # --- DELTA: Tool count ---
    if reg["found"]:
        if claims["tool_count"]:
            if claims["tool_count"] != reg["tool_count"]:
                results["deltas"].append(
                    f"tool_count: README claims {claims['tool_count']}, "
                    f"registry has {reg['tool_count']}"
                )
            else:
                results["oks"].append(f"tool_count: {reg['tool_count']} (ok)")

    # --- DELTA: Version/build_epoch ---
    if reg["found"] and claims["found"]:
        if claims["version"]:
            if claims["version"] != reg["build_epoch"]:
                results["deltas"].append(
                    f"version: README '{claims['version']}', "
                    f"registry build_epoch '{reg['build_epoch']}'"
                )
        if claims["build_epoch"] and claims["build_epoch"] != reg["build_epoch"]:
            results["deltas"].append(
                f"build_epoch: README '{claims['build_epoch']}', "
                f"registry '{reg['build_epoch']}'"
            )

    # --- DELTA: Tool names ---
    if reg["found"] and claims["tool_names"]:
        reg_names = set(reg["tool_names"])
        claimed_names = set(claims["tool_names"])
        missing_in_registry = claimed_names - reg_names
        if missing_in_registry:
            results["deltas"].append(
                f"tool_names in README but NOT in registry: {sorted(missing_in_registry)}"
            )

    # --- INFO: Canonical map tools ---
    if cmap["found"]:
        results["info"] = results.get("info", {})
        results["info"]["canonical_tools_in_constitutional_map"] = cmap["canonical_tool_count"]
        results["info"]["megatools_files"] = len(megatools)
        results["info"]["tools_dir_files"] = len(tools_dir)
        results["info"]["runtime_dirs"] = runtime_counts

    # --- INFO: SOT sections ---
    if sot_sections:
        results["info"] = results.get("info", {})
        results["info"]["sot_sections_found"] = list(sot_sections.keys())

    # --- OK: Endpoints ---
    server_path = repo_root / "arifosmcp" / "server.py"
    if server_path.exists() and claims["found"]:
        server_content = server_path.read_text()
        found_endpoints = re.findall(r'["\'](/[\w.-]+)["\']', server_content)
        found_endpoints = sorted(set(found_endpoints))
        if claims["endpoints"]:
            claimed_eps = set(e.strip() for e in claims["endpoints"])
            found_eps = set(found_endpoints)
            missing = claimed_eps - found_eps
            if missing:
                results["deltas"].append(f"endpoints claimed but not in server.py: {missing}")
            else:
                results["oks"].append(f"endpoints: all {len(claimed_eps)} found (ok)")
        results["info"] = results.get("info", {})
        results["info"]["endpoints_in_server"] = found_endpoints

    return results


def print_audit(results: dict):
    repo = results["repo"]
    print(f"\n{BOLD}{'='*60}")
    print(f"README SOT AUDIT: {repo}")
    print(f"{'='*60}{RESET}")

    if results["errors"]:
        print(f"\n{RED}[ERROR]{RESET}")
        for e in results["errors"]:
            print(f"  {RED}✗{RESET} {e}")

    if results["deltas"]:
        print(f"\n{RED}[DELTA] — Drift detected{RESET}")
        for d in results["deltas"]:
            print(f"  {RED}Δ{RESET} {d}")
    else:
        print(f"\n{GREEN}[OK]{RESET} No drift detected")

    if results["oks"]:
        print(f"\n{GREEN}[OK]{RESET}")
        for ok in results["oks"]:
            print(f"  {GREEN}✓{RESET} {ok}")

    if results.get("info"):
        print(f"\n{YELLOW}[INFO]{RESET}")
        for k, v in results["info"].items():
            print(f"  {YELLOW}ℹ{RESET} {k}: {v}")

    total = len(results["deltas"])
    seal = "SEAL" if total == 0 else f"{total} DELTA{'S' if total > 1 else ''}"
    print(f"\n{BOLD}Result: {seal}{RESET}")
    return total


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: audit.py <repo_path> [repo_name]")
        sys.exit(1)

    repo_path = sys.argv[1]
    repo_name = sys.argv[2] if len(sys.argv) > 2 else Path(repo_path).name

    results = audit_repo(repo_path, repo_name)
    total_deltas = print_audit(results)
    sys.exit(0 if total_deltas == 0 else 1)
