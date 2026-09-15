#!/usr/bin/env python3
"""compile_descriptions.py — OPEN ITEM #3, wire (b): ledger/registry → description compilation.

WHY (F5 finding, 333-AGI deep research 2026-09-15):
  OpenCode's runtime reads EXACTLY two frontmatter fields (name + description).
  Governance fields (capability_tier, floor_scope, risk_tier, autonomy_tier …
  304/240/233/220 present locally) are parsed by YAML then DISCARDED.
  The description is the ONLY routing surface. Until governance is compiled
  into descriptions, no learning above L1 is visible to any model.

WHAT IT DOES:
  For every SKILL.md under /root/AAA/skills with governance frontmatter,
  compile a compact machine-legible tag INTO the description:
      [fed: tier=<capability_tier> floors=<floor_scope> auto=<autonomy_tier> risk=<risk_tier>]
  • Idempotent: replaces an existing [fed: …] tag instead of appending twice.
  • Respects the 1024-char description cap; skips compile if it would overflow.
  • v1 (staged, not in this script): append promoted-capability links from
    /root/AAA/rsi/state/baselines.json once capability→skill mapping exists.

MODES:
  --dry-run   (default) print per-file planned tag + aggregate stats. No writes.
  --execute   write files. Backup first: <file>.bak-precompile (F1 AMANAH).

Return shape: JSON receipt to stdout. ΔS<0: descriptions gain information.
"""

import os, re, sys, json, glob, shutil

STORE = "/root/AAA/skills"
FIELDS = ["capability_tier", "floor_scope", "autonomy_tier", "risk_tier"]
MARKER_RE = re.compile(r"\s*\[fed:[^\]]*\]")


def parse_fm(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else None


def field(fm, name):
    mm = re.search(rf"^{name}:\s*[\"']?([^\"'\n]+)", fm, re.M)
    if mm:
        v = mm.group(1).strip()
        return None if v.startswith("-") else v
    # YAML list form:  field:\n  - a\n  - b
    ml = re.search(rf"^{name}:\s*\n((?:[ \t]+-[^\n]+\n?)+)", fm, re.M)
    if ml:
        items = re.findall(r"-\s*([^\n]+)", ml.group(1))
        return ",".join(i.strip().strip("\"'") for i in items)
    return None


def compile_tag(fm):
    parts = [f"{f.split('_')[0] if False else f}={field(fm, f)}" for f in FIELDS]
    parts = [p for p in parts if not p.endswith("=None") and "=None" not in p]
    # short keys: capability_tier→tier, floor_scope→floors, autonomy_tier→auto, risk_tier→risk
    out = []
    for f in FIELDS:
        v = field(fm, f)
        if v:
            key = {"capability_tier": "tier", "floor_scope": "floors", "autonomy_tier": "auto", "risk_tier": "risk"}[f]
            out.append(f"{key}={v}")
    return "[fed: " + ", ".join(out) + "]" if out else None


def process(path, execute):
    text = open(path, errors="ignore").read()
    fm = parse_fm(text)
    if not fm:
        return None
    desc = re.search(r"^(description:\s*[\"']?)(.*?)([\"']?)$", fm, re.M)
    if not desc:
        return None
    tag = compile_tag(fm)
    if not tag:
        return None
    body = MARKER_RE.sub("", desc.group(2)).strip()
    new_desc = body + (" " if body else "") + tag
    if len(new_desc) > 1024:
        return {"file": path, "skipped": "desc_overflow", "len": len(new_desc)}
    if new_desc == desc.group(2).strip():
        return {"file": path, "unchanged": True}
    if not execute:
        return {
            "file": path.replace(STORE + "/", ""),
            "planned_tag": tag,
            "was_compiled": bool(MARKER_RE.search(desc.group(2))),
        }
    # F1: backup then write
    shutil.copy2(path, path + ".bak-precompile")
    new_fm = fm.replace(desc.group(0), desc.group(1) + new_desc + desc.group(3), 1)
    open(path, "w").write(text.replace("---\n" + fm + "\n---", "---\n" + new_fm + "\n---", 1))
    return {"file": path.replace(STORE + "/", ""), "written": True, "tag": tag}


def main():
    execute = "--execute" in sys.argv
    results = [r for f in sorted(glob.glob(STORE + "/**/SKILL.md", recursive=True)) if (r := process(f, execute))]
    planned = [r for r in results if r and "planned_tag" in r]
    written = [r for r in results if r and r.get("written")]
    print(
        json.dumps(
            {
                "mode": "execute" if execute else "dry-run",
                "scanned": len(results),
                "planned_changes": len(planned),
                "written": len(written),
                "already_compiled": len([r for r in results if r.get("was_compiled")]),
                "skipped_overflow": len([r for r in results if r.get("skipped")]),
                "samples": planned[:3],
            },
            indent=1,
        )
    )


if __name__ == "__main__":
    main()
