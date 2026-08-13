#!/usr/bin/env python3
"""
SCHEMA INJECTOR — add required_tools + tool_gate to SKILL.md frontmatter.
Pilot (10) pertama. F1: backup *.bak sebelum write, patch atomik, idempotent
(tidak buang field sedia ada, sertai list required_tools).
Contract: SCHEMA_STANDARD_required_tools_tool_gate_v1.md
"""
from __future__ import annotations
import shutil, sys, re
from pathlib import Path

# name -> (path, tool_gate, required_tools)
PILOT = {
    "AAA-OCR-optical-compression": (None, "strict", ["vision_analyze", "arif_observe"]),
    "image-text-editing": ("creative", "strict", ["image_generate", "vision_analyze"]),
    "aaa-image-editing": ("media", "strict", ["image_generate", "vision_analyze"]),
    "AGI-agentic-web": (None, "permissive", ["forge_fetch", "forge_search"]),
    "AGI-plan-dag": (None, "strict", ["terminal"]),
    "FORGE-mcp-lifeguard": (None, "strict", ["forge_health_check"]),
    "ASI-drift-watch": (None, "permissive", ["arif_observe", "forge_fetch"]),
    "observe-ground": ("substrate", "strict", ["arif_observe", "arif_think"]),
    "memory-manage": ("substrate", "strict", ["arif_memory"]),
}

root = Path("/root/AAA/skills")
def find_sk(name, sub):
    p = root / sub / name / "SKILL.md" if sub else root / name / "SKILL.md"
    return p if p.exists() else None

def inject(p: Path, gate: str, tools: list[str]) -> tuple[str, str]:
    text = p.read_text(encoding="utf-8")
    # frontmatter: between first --- and second ---
    m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n)", text, re.DOTALL)
    if not m:
        return "NOfront", p.name
    open_fm, body, close_fm = m.groups()
    lines = body.splitlines()
    # filter existing required_tools/tool_gate raw lines
    newlines = [l for l in lines if not re.match(r"^(required_tools|tool_gate)\s*:", l)]
    # append at end (before closing ---), after any tools: list style handled
    newlines.append(f"required_tools: {tools}")
    newlines.append(f"tool_gate: {gate}")
    body2 = "\n".join(newlines)
    p.write_text(f"{open_fm}{body2}\n{close_fm}{text[m.end():]}", encoding="utf-8")
    return "OK", p.name

def main():
    changed = 0
    for name, (sub, gate, tools) in PILOT.items():
        p = find_sk(name, sub)
        if not p:
            for cand in root.rglob("SKILL.md"):
                if cand.parent.name == name:
                    p = cand; break
            if not p:
                print(f"  SKIP (missing): {name}")
                continue
        # backup
        bak = p.with_suffix(".md.bak")
        if not bak.exists():
            shutil.copy2(p, bak)
        st, who = inject(p, gate, tools)
        if st == "OK":
            changed += 1
            print(f"  [INJECT] {p.relative_to(root)}  gate={gate} tools={tools}")
        else:
            print(f"  [WARN] {who} — {st}")
    print(f"\n  changed/skipped: {changed}")

if __name__ == "__main__":
    main()