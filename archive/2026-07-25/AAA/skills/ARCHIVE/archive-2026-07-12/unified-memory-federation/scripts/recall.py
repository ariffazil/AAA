#!/usr/bin/env python3
"""
Unified memory recall across L1-L2 federation surfaces.
L3+ requires MCP tools (arif_memory, knowledge-graph-query, arif_seal).
"""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

FORGE_WORK = Path("/root/A-FORGE/forge_work")
MEMORY_DIR = Path("/root/memory")
CARRY_FORWARD = Path("/root/.local/share/arifos/carry_forward.json")
SELF_HEAL = Path("/root/.local/share/arifos/self-heal-RECEIPT.md")
KG_QUERY = Path("/root/.agents/skills/knowledge-graph-query/scripts/query.py")


def grep_dir(directory: Path, pattern: str, max_hits: int = 10):
    hits = []
    if not directory.exists():
        return hits
    regex = re.compile(re.escape(pattern), re.IGNORECASE)
    for root, _dirs, files in os.walk(directory):
        for fname in files:
            if fname.endswith((".pyc", ".pyo", ".png", ".jpg", ".jpeg", ".gif")):
                continue
            fpath = Path(root) / fname
            try:
                with fpath.open("r", encoding="utf-8", errors="ignore") as f:
                    for lineno, line in enumerate(f, 1):
                        if regex.search(line):
                            hits.append({
                                "path": str(fpath),
                                "line": lineno,
                                "snippet": line.strip()[:200],
                            })
                            if len(hits) >= max_hits:
                                return hits
            except Exception:
                continue
    return hits


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}


def read_head(path: Path, lines: int = 20):
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            return "".join(f.readlines()[:lines])
    except Exception as e:
        return str(e)


def query_kg(name: str):
    if not KG_QUERY.exists():
        return {"error": "knowledge-graph-query script not found"}
    try:
        result = subprocess.run(
            ["python3", str(KG_QUERY), "--name", name, "--max-results", "5"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return json.loads(result.stdout) if result.returncode == 0 else {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Unified memory recall (L1-L2 + L4 convenience).")
    parser.add_argument("query", help="Keyword or phrase to recall")
    parser.add_argument("--tiers", default="L1,L2,L4", help="Comma-separated tiers to search")
    parser.add_argument("--max-hits", type=int, default=10)
    args = parser.parse_args()

    tiers = [t.strip().upper() for t in args.tiers.split(",")]
    result = {
        "query": args.query,
        "tiers_requested": tiers,
        "results": {},
        "routing": {
            "L0": "inspect current session context manually",
            "L3": "use arif_memory(mode=recall)",
            "L5": "use arif_seal(mode=list)",
        },
    }

    if "L1" in tiers:
        result["results"]["L1_working"] = grep_dir(FORGE_WORK, args.query, args.max_hits)
    if "L2" in tiers:
        result["results"]["L2_daily"] = grep_dir(MEMORY_DIR, args.query, args.max_hits)
        result["results"]["L2_carry_forward"] = read_json(CARRY_FORWARD)
        result["results"]["L2_self_heal"] = read_head(SELF_HEAL, 10)
    if "L4" in tiers:
        result["results"]["L4_knowledge_graph"] = query_kg(args.query)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
