#!/usr/bin/env python3
"""
mcp_audit.py — Phase 3: MCP security audit via code graph walk.

For every MCP tool exposed by the federation, walk the code graph from
its definition point and check whether the blast radius reaches any
sensitive path. Produces a tiered risk table.

Sensitive paths (configurable):
  /root/.secrets/         — bearer tokens, API keys, ROOT_ENVELOPE
  /root/.ssh/             — SSH keys
  /opt/*/app/.env         — runtime env (proxies, secrets)
  /root/VAULT999/sealed/  — sealed audit chain
  /root/.arifos/agents/*/state.db  — agent session state

Risk tier:
  GREEN  — no sensitive path reachable
  YELLOW — sensitive path reachable via imports only (transitive risk)
  RED    — entry file directly imports / reads / writes a sensitive path
"""
from __future__ import annotations
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

GRAPH_DB = Path("/root/AAA/graph/codegraph.db")

# Sensitive path patterns — substring match on abs path
SENSITIVE_PATTERNS = [
    "/.secrets/",
    "/.ssh/",
    "/opt/arifos/app/.env",
    "/opt/aforge/app/.env",
    "/opt/wealth/app/.env",
    "/opt/well/app/.env",
    "/opt/geox/app/.env",
    "/root/VAULT999/sealed/",
    "/.arifos/agents/",  # agent session state
]

# ─── tool discovery ────────────────────────────────────────────────────────


def discover_a_forge_tools() -> dict[str, tuple[str, str]]:
    """Map A-FORGE forge_* tool name → (repo, rel_path).

    Patterns handled:
      server.registerTool("name", ...)
      server.tool("name", ...)
      mcp.tool("name", ...)
      mcp.add_tool(TOOL_OBJECT)  → resolved via import lookup
    """
    repo_root = Path("/root/A-FORGE/src")
    tools = {}
    for fp in repo_root.rglob("*.ts"):
        text = fp.read_text(errors="ignore")
        rel = str(fp.relative_to(Path("/root/A-FORGE")))
        # All three patterns
        for m in re.finditer(r'(?:server|mcp|app)\.(?:registerTool|tool|add_tool)\(\s*["\']([a-zA-Z_][\w_]+)["\']', text):
            tools[m.group(1)] = ("A-FORGE", rel)
    return tools


def discover_arifos_tools() -> dict[str, tuple[str, str]]:
    """Map arifOS tool name → (repo, rel_path).

    Patterns:
      @mcp.tool(annotations=...)  followed by `def name(...)`
      mcp.add_tool(TOOL)          followed by `TOOL = Tool(...)` definitions
      app.tool()                  FastMCP style
    """
    repo_root = Path("/root/arifOS/arifosmcp")
    tools = {}
    for fp in repo_root.rglob("*.py"):
        text = fp.read_text(errors="ignore")
        rel = str(fp.relative_to(Path("/root/arifOS")))
        # @mcp.tool() / @server.tool() decorators → def name
        for m in re.finditer(r'@(?:mcp|server|app)\.tool(?:\([^)]*\))?\s*\n?\s*(?:async\s+)?def\s+([a-zA-Z_]\w*)', text):
            tools[m.group(1)] = ("arifOS", rel)
        # mcp.add_tool(ARIF_CLAIM_GATE_TOOLS) → look for the constant
        for m in re.finditer(r'mcp\.add_tool\(\s*([A-Z_][A-Z0-9_]+)\s*\)', text):
            constant_name = m.group(1)
            # Find the constant definition in same file
            const_match = re.search(
                rf'^{constant_name}\s*=\s*\[([^\]]+)\]',
                text, re.MULTILINE
            )
            if const_match:
                for name_match in re.finditer(r'["\']([a-zA-Z_]\w+)["\']', const_match.group(1)):
                    tools[name_match.group(1)] = ("arifOS", rel)
        # mcp.tool() / app.tool() with literal name
        for m in re.finditer(r'(?:server|mcp|app)\.(?:registerTool|tool|add_tool)\(\s*["\']([a-zA-Z_][\w_]+)["\']', text):
            tools[m.group(1)] = ("arifOS", rel)
    return tools


def discover_aaa_tools() -> dict[str, tuple[str, str]]:
    """Map AAA tools if any."""
    repo_root = Path("/root/AAA")
    tools = {}
    for fp in repo_root.rglob("*.py"):
        if "graph" in str(fp):  # skip the code graph itself
            continue
        text = fp.read_text(errors="ignore")
        rel = str(fp.relative_to(Path("/root/AAA")))
        for m in re.finditer(r'@(?:mcp|server|app)\.tool(?:\([^)]*\))?\s*\n?\s*(?:async\s+)?def\s+([a-zA-Z_]\w*)', text):
            tools[m.group(1)] = ("AAA", rel)
    return tools


# ─── graph queries ────────────────────────────────────────────────────────


def get_file_id(repo: str, rel_path: str) -> int | None:
    conn = sqlite3.connect(str(GRAPH_DB))
    try:
        r = conn.execute(
            "SELECT f.id FROM files f JOIN repos r ON f.repo_id=r.id"
            " WHERE r.name=? AND f.rel_path=?",
            (repo, rel_path),
        ).fetchone()
        return r[0] if r else None
    finally:
        conn.close()


def get_symbol_id(repo: str, rel_path: str, qualified_name: str) -> int | None:
    conn = sqlite3.connect(str(GRAPH_DB))
    try:
        r = conn.execute(
            "SELECT s.id FROM symbols s JOIN files f ON s.file_id=f.id"
            " JOIN repos r ON f.repo_id=r.id"
            " WHERE r.name=? AND f.rel_path=? AND s.qualified_name=?",
            (repo, rel_path, qualified_name),
        ).fetchone()
        return r[0] if r else None
    finally:
        conn.close()


def blast_radius_for(repo: str, rel_path: str, qualified_name: str | None) -> dict:
    """Compute blast radius: set of (repo, rel_path) reachable in 2 hops.

    Strategy (depth-2 BFS):
      hop 0: this file + its defined symbols
      hop 1: every file that imports this file's module + every file
             whose edges reference this file's symbols by name
      hop 2: same expansion on hop-1 frontier
    """
    conn = sqlite3.connect(str(GRAPH_DB))
    seen = set()  # set of (repo, rel_path)
    frontier_files = set()
    layers = []

    # Hop 0: starting set
    start = (repo, rel_path)
    seen.add(start)
    frontier_files.add(start)

    for hop in range(2):
        new_files = set()
        for (r, p) in frontier_files:
            fid = get_file_id(r, p)
            if not fid:
                continue
            # 1) Files that import this file's module (inbound imports)
            module_stem = p.replace("/", ".").removesuffix(".py")
            if module_stem.endswith(".__init__"):
                module_stem = module_stem[:-9]
            parent_pkgs = [module_stem[:i] for i in range(1, len(module_stem.split(".")))]
            placeholders = ",".join("?" * (len(parent_pkgs) + 1))
            params = (module_stem, *parent_pkgs)
            rows = conn.execute(
                f"SELECT DISTINCT r.name, f.rel_path"
                f" FROM imports i"
                f" JOIN files f ON i.file_id=f.id"
                f" JOIN repos r ON f.repo_id=r.id"
                f" WHERE i.src_module IN ({placeholders})",
                params,
            ).fetchall()
            for rr in rows:
                new_files.add((rr[0], rr[1]))

            # 2) Files whose edges reference symbols in this file
            #    (we use qualified_name match against the file's symbols)
            sym_rows = conn.execute(
                "SELECT s.qualified_name FROM symbols s WHERE s.file_id=?",
                (fid,),
            ).fetchall()
            sym_names = [sr[0] for sr in sym_rows]
            if sym_names:
                placeholders = ",".join("?" * len(sym_names))
                rows2 = conn.execute(
                    f"SELECT DISTINCT r.name, f.rel_path"
                    f" FROM edges e"
                    f" JOIN files f ON e.src_file_id=f.id"
                    f" JOIN repos r ON f.repo_id=r.id"
                    f" WHERE e.dst_qualified_name IN ({placeholders})",
                    sym_names,
                ).fetchall()
                for rr in rows2:
                    new_files.add((rr[0], rr[1]))

        new_files -= seen
        if not new_files:
            break
        layers.append({"hop": hop + 1, "files": sorted(f"{r}/{p}" for (r, p) in new_files)})
        seen |= new_files
        frontier_files = new_files

    conn.close()
    return {"layers": layers, "total_reachable": len(seen) - 1}  # minus self


def get_repo_for_file(file_id: int) -> str:
    conn = sqlite3.connect(str(GRAPH_DB))
    try:
        r = conn.execute(
            "SELECT r.name FROM files f JOIN repos r ON f.repo_id=r.id WHERE f.id=?",
            (file_id,),
        ).fetchone()
        return r[0] if r else "?"
    finally:
        conn.close()


def file_imports_paths(repo: str, rel_path: str) -> list[str]:
    """Get actual import module strings in this file — for sensitive path cross-check."""
    conn = sqlite3.connect(str(GRAPH_DB))
    try:
        rows = conn.execute(
            "SELECT i.src_module FROM imports i"
            " JOIN files f ON i.file_id=f.id"
            " JOIN repos r ON f.repo_id=r.id"
            " WHERE r.name=? AND f.rel_path=?",
            (repo, rel_path),
        ).fetchall()
        return [r[0] for r in rows]
    finally:
        conn.close()


# ─── audit ──────────────────────────────────────────────────────────────


def audit() -> dict:
    tools: dict[str, tuple[str, str]] = {}
    tools.update(discover_a_forge_tools())
    tools.update(discover_arifos_tools())
    tools.update(discover_aaa_tools())

    by_tier: dict[str, list] = {"RED": [], "YELLOW": [], "GREEN": []}
    detail = []

    for tool_name, (repo, entry_path) in sorted(tools.items()):
        # Direct sensitive check on entry file imports
        direct_sensitive = []
        imports = file_imports_paths(repo, entry_path)
        for imp in imports:
            for pat in SENSITIVE_PATTERNS:
                if pat in imp:
                    direct_sensitive.append(imp)
        # Content-based check: read entry file for sensitive literals
        content_sensitive = []
        try:
            entry_abs = Path("/root") / repo / entry_path
            if entry_abs.exists():
                text = entry_abs.read_text(errors="ignore")
                content_hits = []
                # .secrets/ paths
                for m in re.finditer(r'["\']([^"\']*\.secrets/[^"\']+)["\']', text):
                    content_hits.append(m.group(1))
                for m in re.finditer(r'["\']([^"\']*kunci-root\.env[^"\']*)["\']', text):
                    content_hits.append(m.group(1))
                for m in re.finditer(r'["\']([^"\']*\.ssh/[^"\']*)["\']', text):
                    content_hits.append(m.group(1))
                for m in re.finditer(r'["\'](/opt/[a-z-]+/app/\.env)["\']', text):
                    content_hits.append(m.group(1))
                # Drop duplicates, keep first 5
                seen = set()
                for h in content_hits:
                    if h not in seen:
                        seen.add(h)
                        content_sensitive.append(h)
                        if len(content_sensitive) >= 5:
                            break
        except Exception:
            pass
        # Blast radius (file-level)
        blast = {"layers": [], "total_reachable": 0}
        try:
            blast = blast_radius_for(repo, entry_path, None)
            reachable = set()
            for layer in blast["layers"]:
                for f in layer["files"]:
                    reachable.add(f)
        except Exception:
            reachable = set()
        # Sensitive paths in reachable files — check both:
        # 1. the path string against patterns (catches /root/.secrets/* etc)
        # 2. the file's CONTENT for sensitive literals (catches utility modules
        #    that read secrets but don't live in /root/.secrets/)
        reachable_sensitive = []
        for r_path in reachable:
            # r_path is "repo/rel_path" form
            for pat in SENSITIVE_PATTERNS:
                if pat in r_path:
                    reachable_sensitive.append(r_path)
                    break
            else:
                # check file content (only for first 50 reachable to bound cost)
                if len(reachable_sensitive) < 5 and len(reachable) < 200:
                    try:
                        sep = r_path.find("/")
                        rr, pp = r_path[:sep], r_path[sep+1:]
                        if rr == repo and pp == entry_path:
                            continue
                        abs_path = Path("/root") / rr / pp
                        if abs_path.exists() and abs_path.stat().st_size < 500_000:
                            text = abs_path.read_text(errors="ignore")
                            for pat in [".secrets/", "kunci-root.env", ".ssh/"]:
                                if pat in text:
                                    reachable_sensitive.append(f"{r_path} (content: {pat})")
                                    break
                    except Exception:
                        pass

        # Tier:
        # RED: entry file content directly references a sensitive path literal
        # YELLOW: blast_radius reaches a file with sensitive path OR sensitive
        #         content OR imports touch sensitive path
        # GREEN: nothing
        if content_sensitive:
            tier = "RED"
        elif direct_sensitive or reachable_sensitive:
            tier = "YELLOW"
        else:
            tier = "GREEN"

        entry = {
            "tool": tool_name,
            "repo": repo,
            "entry_path": entry_path,
            "tier": tier,
            "direct_sensitive_imports": direct_sensitive[:5],
            "content_sensitive_refs": content_sensitive,
            "blast_reachable_count": blast.get("total_reachable", 0),
            "blast_reachable_sensitive": reachable_sensitive[:5],
        }
        by_tier[tier].append(entry)
        detail.append(entry)

    return {
        "summary": {
            "total_tools": len(tools),
            "RED": len(by_tier["RED"]),
            "YELLOW": len(by_tier["YELLOW"]),
            "GREEN": len(by_tier["GREEN"]),
            "sensitive_patterns": SENSITIVE_PATTERNS,
        },
        "by_tier": by_tier,
        "detail": detail,
    }


if __name__ == "__main__":
    r = audit()
    print(json.dumps(r, indent=2, default=str))