#!/usr/bin/env python3
"""
README SOT Generator — inject dynamic facts into README at SOT markers.
DITEMPA BUKAN DIBERI — Intelligence is forged, not given.

Usage:
    generate.py /root/arifOS --dry-run    # show what would change
    generate.py /root/arifOS --apply       # actually write
    generate.py /root/arifOS --apply --force  # skip confirmation
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


def load_registry(repo_root: Path) -> dict:
    registry_path = repo_root / "arifosmcp" / "tool_registry.json"
    if not registry_path.exists():
        return {}
    with open(registry_path) as f:
        return json.load(f)


def load_constitutional_map(repo_root: Path) -> dict:
    cmap_path = repo_root / "arifosmcp" / "constitutional_map.py"
    if not cmap_path.exists():
        return {}
    content = cmap_path.read_text()

    # Extract tool definitions: "arif_session_init": { ... "stage": ToolStage.INIT ...
    tool_blocks = re.findall(
        r'"(arif_\w+)":\s*\{[^}]*"stage":\s*ToolStage\.(\w+)[^}]*"floors":\s*\[(.*?)\]',
        content,
        re.DOTALL
    )

    # Simpler: just get the tool names and their stage
    tools = re.findall(r'"(arif_\w+)":\s*\{[^}]?"stage":\s*ToolStage\.(\w+)', content)
    return {name: stage for name, stage in tools}


def extract_tool_table(registry: dict) -> list[dict]:
    """Extract tools from registry in format for README table.
    Handles two formats:
      - list format: [{function: {name: "arifos_000_init"}}, ...]  (MCP list)
      - dict format: {arif_session_init: {stage: "000", ...}, ...}  (CANONICAL_TOOLS dict)
    """
    tools_data = registry.get("tools", [])
    result = []

    if isinstance(tools_data, dict):
        # CANONICAL_TOOLS dict format: {name: {stage, lane, ...}}
        for fname, props in tools_data.items():
            if isinstance(props, dict):
                stage = props.get("stage", "???")
                lane = props.get("lane", "?")
            else:
                stage, lane = "???", "?"
            # Convert stage like "000" or "010" or "FORGE" for forge
            result.append({"stage": str(stage), "name": fname, "full": fname, "lane": lane})

    elif isinstance(tools_data, list):
        # MCP list format: [{function: {name: "arifos_000_init"}}, ...]
        for t in tools_data:
            if isinstance(t, dict):
                fname = t.get("function", {}).get("name", "?")
            else:
                fname = str(t)
            m = re.match(r"arifos_(\d+)_(\w+)", fname)
            if m:
                stage, name = m.groups()
            else:
                stage, name = "???", fname
            result.append({"stage": stage, "name": name, "full": fname})

    return sorted(result, key=lambda x: x["stage"])


def build_tool_surface_section(registry: dict, cmap: dict) -> str:
    """Build SOT:tool_surface content from registry."""
    tools = extract_tool_table(registry)
    build_epoch = registry.get("build_epoch", "??????")
    system = registry.get("system", "arifOS MCP")

    lines = [
        f"<!-- SOT:tool_surface -->",
        f"**Surface:** {system}",
        f"**Build Epoch:** {build_epoch}",
        f"**Total Tools:** {len(tools)}",
        "",
        "| Stage | Tool | Lane | Description |",
        "|-------|------|------|-------------|",
    ]

    # Lane mapping from stage
    lane_map = {
        "000": "AGI", "111": "AGI", "222": "AGI",
        "333": "AGI", "444": "AGI",
        "555": "AGI",
        "666": "ASI", "777": "AGI",
        "888": "ASI", "999": "APEX",
    }
    desc_map = {
        "000": "Session bootstrap + identity binding",
        "111": "Reality-grounded observation",
        "222": "Evidence-preserving witness",
        "333": "Inductive reasoning engine",
        "444": "Kernel syscall and telemetry",
        "555": "Vector memory and context retrieval",
        "666": "Thermodynamic vitality monitor",
        "777": "Operations and economic thermodynamics",
        "888": "Constitutional verdict engine",
        "999": "Immutable ledger",
        "forge": "Execution substrate dispatch",
    }

    for t in tools:
        stage = t["stage"]
        name = t["name"]
        full = t["full"]
        # lane from tool data (dict format) overrides lane_map
        lane = t.get("lane") or lane_map.get(stage, "?")
        desc = desc_map.get(stage, desc_map.get(name, "—"))
        if stage == "???" or stage == "010":
            stage = "FORGE"
            desc = "Execution substrate dispatch"
        lines.append(f"| `{stage}` | `{full}` | {lane} | {desc} |")

    lines.append("")
    lines.append(f"_Auto-generated from `tool_registry.json` — {build_epoch}_")
    lines.append("<!-- /SOT:tool_surface -->")
    return "\n".join(lines)


def build_version_section(registry: dict) -> str:
    build_epoch = registry.get("build_epoch", "??????")
    build_timestamp = registry.get("build_timestamp", "")
    constitutional_hash = registry.get("constitutional_hash", "??????")[:12]
    tool_count = len(registry.get("tools", []))

    lines = [
        "<!-- SOT:version_info -->",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| VERSION | {build_epoch}-KANON |",
        f"| BUILD_EPOCH | {build_epoch} |",
        f"| BUILD_TIMESTAMP | {build_timestamp} |",
        f"| CONSTITUTIONAL_HASH | `{constitutional_hash}...` |",
        f"| TOOL_COUNT | {tool_count} |",
        f"| FLOOR_COUNT | 13 (F1–F13) |",
        "",
        f"_Auto-generated — {build_timestamp}_",
        "<!-- /SOT:version_info -->",
    ]
    return "\n".join(lines)


def build_file_structure_section(repo_root: Path) -> str:
    """Build SOT:file_structure from actual directory tree."""
    lines = ["<!-- SOT:file_structure -->", "```"]

    key_dirs = [
        "arifosmcp/tools",
        "arifosmcp/megaTools",
        "arifosmcp/runtime",
        "arifosmcp/core",
        "arifosmcp/apps",
        "arifosmcp/providers",
        "skills",
    ]

    for d in key_dirs:
        dir_path = repo_root / d
        if dir_path.exists():
            files = sorted([
                f.name for f in dir_path.rglob("*.py")
                if "__pycache__" not in str(f)
            ])
            if files:
                lines.append(f"{d}/")
                for f in files[:20]:  # cap at 20 per dir
                    lines.append(f"  {f}")
                if len(files) > 20:
                    lines.append(f"  ... +{len(files)-20} more")
    lines.append("```")
    lines.append("<!-- /SOT:file_structure -->")
    return "\n".join(lines)


def build_endpoints_section(repo_root: Path) -> str:
    server_path = repo_root / "arifosmcp" / "server.py"
    endpoints = []
    if server_path.exists():
        content = server_path.read_text()
        found = re.findall(r'["\'](/[\w-]+)["\']', content)
        endpoints = sorted(set(found))

    lines = [
        "<!-- SOT:endpoints -->",
        "| Endpoint | Purpose |",
        "|----------|---------|",
    ]
    purpose_map = {
        "/health": "Live vitals — tools, prompts, resources count",
        "/healthz": "Deep health check with registry stats",
        "/metadata": "Gateway capabilities and tool access classification",
        "/humans.txt": "Sovereign attribution",
        "/mcp": "MCP protocol endpoint",
        "/tools": "Tool manifest",
    }
    for ep in endpoints:
        purpose = purpose_map.get(ep, "—")
        lines.append(f"| `{ep}` | {purpose} |")
    lines.append("")
    lines.append(f"_Auto-generated from `server.py` — {len(endpoints)} endpoints_")
    lines.append("<!-- /SOT:endpoints -->")
    return "\n".join(lines)


def generate_readme(repo_root: Path, dry_run: bool = False, force: bool = False) -> str:
    registry = load_registry(repo_root)
    cmap = load_constitutional_map(repo_root)

    readme_path = repo_root / "README.md"
    if not readme_path.exists():
        return "ERROR: README.md not found"

    content = readme_path.read_text()

    # Build all SOT sections
    new_sections = {}

    if registry.get("tools"):
        new_sections["tool_surface"] = build_tool_surface_section(registry, cmap)
        new_sections["version_info"] = build_version_section(registry)
        new_sections["endpoints"] = build_endpoints_section(repo_root)

    new_sections["file_structure"] = build_file_structure_section(repo_root)

    # Replace each SOT section in content
    new_content = content
    for section_name, new_body in new_sections.items():
        pattern = r'<!-- SOT:' + section_name + r' -->.*?<!-- /SOT:' + section_name + r' -->'
        if re.search(pattern, new_content, re.DOTALL):
            new_content = re.sub(pattern, new_body, new_content, flags=re.DOTALL)
        else:
            # Section marker not found — append info note
            new_content += f"\n\n> [!NOTE]\n> SOT:{section_name} marker not found in README. Dynamic section not injected.\n"

    if new_content == content:
        return "No changes needed — README matches SOT."

    if dry_run:
        # Show diff
        old_lines = content.splitlines()
        new_lines = new_content.splitlines()
        print(f"{YELLOW}--- OLD (first 30 lines){RESET}")
        for l in old_lines[:30]:
            print(l)
        print(f"\n{YELLOW}--- NEW (first 30 lines){RESET}")
        for l in new_lines[:30]:
            print(l)
        return f"\n{BOLD}Dry run complete — {len(new_lines)} lines in new version{RESET}"

    if not force:
        response = input(f"\n{RED}WARNING: This will overwrite README.md{RESET}\nType 'yes' to proceed: ")
        if response.lower() != "yes":
            return "Aborted."

    readme_path.write_text(new_content)
    return f"{GREEN}README.md updated successfully.{RESET}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate dynamic README sections")
    parser.add_argument("repo_path", help="Path to repository")
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing")
    parser.add_argument("--apply", action="store_true", help="Apply changes to README")
    parser.add_argument("--force", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    result = generate_readme(Path(args.repo_path), dry_run=args.dry_run, force=args.force)
    print(result)
