#!/usr/bin/env python3
"""
Session-end memory consolidation pipeline.
Aggregates L1 (forge_work) and L2 (/root/memory) surfaces into a structured
report, extracts action items, and prepares durable-memory promotion.
L3+ promotion is delegated to arif_memory / asi-knowledge-writeback.
"""
import argparse
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

CARRY_FORWARD = Path("/root/.local/share/arifos/carry_forward.json")
MEMORY_DIR = Path("/root/memory")
FORGE_WORK = Path("/root/A-FORGE/forge_work")
OUTPUT_DIR = Path("/root/A-FORGE/forge_work/consolidation")


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}


def find_memory_files(date_str: str):
    files = []
    if MEMORY_DIR.exists():
        for f in MEMORY_DIR.iterdir():
            if f.is_file() and date_str in f.name:
                files.append(f)
    return sorted(files)


def find_recent_forge_work(hours: int = 24):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    files = []
    if FORGE_WORK.exists():
        for root, _dirs, fnames in os.walk(FORGE_WORK):
            for fname in fnames:
                fpath = Path(root) / fname
                try:
                    mtime = datetime.fromtimestamp(fpath.stat().st_mtime, tz=timezone.utc)
                    if mtime >= cutoff:
                        files.append(str(fpath))
                except Exception:
                    pass
    return sorted(files)


def extract_action_items(text: str):
    actions = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.search(r"^\s*[-*]\s+\[\s*\]", stripped):
            actions.append(stripped)
        elif re.search(r"\b(TODO|FIXME|ACTION|HOLD|888_HOLD)\b", stripped, re.IGNORECASE):
            actions.append(stripped)
    return actions


def extract_remember_lines(text: str):
    return [line.strip() for line in text.splitlines() if "#remember" in line.lower()]


def consolidate(date_str: str):
    carry = read_json(CARRY_FORWARD)
    memory_files = find_memory_files(date_str)
    recent_forge = find_recent_forge_work()

    memory_snippets = []
    action_items = []
    remember_lines = []

    for mf in memory_files:
        try:
            content = mf.read_text(encoding="utf-8", errors="ignore")
            memory_snippets.append({"file": str(mf), "chars": len(content)})
            action_items.extend(extract_action_items(content))
            remember_lines.extend(extract_remember_lines(content))
        except Exception as e:
            memory_snippets.append({"file": str(mf), "error": str(e)})

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": date_str,
        "carry_forward": carry,
        "memory_files": memory_snippets,
        "recent_forge_work": recent_forge,
        "action_items": action_items,
        "remember_candidates": remember_lines,
        "next_steps": [
            "Review action_items and resolve or promote to L3 via arif_memory(remember).",
            "Review remember_candidates and write to knowledge graph via asi-knowledge-writeback if SEALED.",
            "Run identity-drift-watchdog.sh to refresh carry_forward.json.",
        ],
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{date_str}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(json.dumps(report, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Consolidate session memory surfaces.")
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"), help="Date string to match memory files")
    args = parser.parse_args()
    consolidate(args.date)


if __name__ == "__main__":
    main()
