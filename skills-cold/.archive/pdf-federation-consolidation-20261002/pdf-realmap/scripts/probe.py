"""
probe.py — Probe filesystem for PDF skill real paths + maturity classification.
Single source of truth for build_realmap.py and the live dossier.

Usage:
    python3 probe.py [--out probe.json]
    python3 probe.py --print   # also print summary
"""
from __future__ import annotations
import os
import json
import argparse
from datetime import datetime, timezone

# ----------------------------------------------------------------------------
# SKILLS — the 13 PDF-related skills (auto-discoverable; verified 02 Oct 2026).
# Add a new skill here AND only here. Every build_script and viewer picks it up.
# ----------------------------------------------------------------------------
SKILLS: dict[str, str] = {
    "forge-pdf-delivery":         "/root/.hermes/skills/domains/general/workshop/document-intel/forge-pdf-delivery",
    "scientific-pdf-generation":  "/root/.hermes/skills/domains/general/workshop/document-intel/scientific-pdf-generation",
    "civic-intelligence-pdf":     "/root/.hermes/skills/domains/general/workshop/document-intel/civic-intelligence-pdf",
    "open-slide-integration":     "/root/.hermes/skills/domains/general/workshop/document-intel/open-slide-integration",
    "powerpoint":                 "/root/.hermes/skills/domains/general/workshop/document-intel/powerpoint",
    "medical-document-interp":    "/root/.hermes/skills/domains/general/workshop/document-intel/medical-document-interpretation",
    "trading-signal-chart":       "/root/.hermes/skills/domains/wealth/workshop/trading-exec/trading-signal-chart",
    "ocr-and-documents":          "/root/.hermes/skills/ocr-and-documents",
    "aaa-pdf-voice-protocol":     "/root/.hermes/skills/aaa-pdf-voice-protocol",
    "forge-artifact-publisher":   "/root/.hermes/skills/forge-artifact-publisher",
    "forge-document-intel":       "/root/.hermes/skills/forge-document-intelligence",
    "aaa-ocr-optical-compress":   "/root/AAA/skills/aaa-ocr-optical-compression",
    "pdf-productivity":           "/root/.hermes/profiles/aaa-hermes/skills/productivity/pdf",
}

# ----------------------------------------------------------------------------
# Probe logic — DO NOT change maturity criteria without updating SKILL.md
# ----------------------------------------------------------------------------

def probe(path: str) -> dict:
    """Probe one skill directory. Returns dict; 'present': False if dir absent."""
    try:
        if not os.path.isdir(path):
            return {"present": False, "exposed": path, "error": "absent"}
    except PermissionError:
        return {"present": False, "exposed": path, "error": "permission-denied"}

    real = os.path.realpath(path)
    is_symlink = (real != path)

    n_files = 0
    total_bytes = 0
    last_modified = 0.0
    smd = None
    has_scripts = has_templates = has_references = False
    asset_scripts = []
    asset_templates = []
    asset_references = []

    for dp, _dns, fns in os.walk(path, followlinks=True):
        for f in fns:
            try:
                full = os.path.join(dp, f)
                if not os.path.isfile(full):
                    continue
                n_files += 1
                size = os.path.getsize(full)
                total_bytes += size
                mt = os.path.getmtime(full)
                if mt > last_modified:
                    last_modified = mt
                rel = os.path.relpath(full, path)
                if f == "SKILL.md":
                    smd = full
                if "/scripts/" in full and f.endswith(".py"):
                    asset_scripts.append(rel); has_scripts = True
                elif "/templates/" in full and f.endswith(".py"):
                    asset_templates.append(rel); has_templates = True
                elif "/references/" in full:
                    asset_references.append(rel); has_references = True
                elif "/scripts/" in full:
                    has_scripts = True
                elif "/templates/" in full:
                    has_templates = True
                elif "/references/" in full:
                    has_references = True
            except (PermissionError, OSError):
                continue

    skillmd_lines = 0
    if smd:
        try:
            with open(smd, errors="ignore") as fh:
                skillmd_lines = sum(1 for _ in fh)
        except Exception:
            pass

    if not smd:
        state = "PRESENT"
    elif not (has_scripts or has_templates):
        state = "LOADABLE"
    else:
        state = "EXECUTABLE"

    mtime_iso = None
    if last_modified:
        mtime_iso = datetime.fromtimestamp(last_modified, tz=timezone.utc).isoformat()

    return {
        "present": True,
        "exposed": path,
        "real": real,
        "symlink": is_symlink,
        "n_files": n_files,
        "bytes": total_bytes,
        "skillmd_lines": skillmd_lines,
        "skillmd_path": smd,
        "has_scripts": has_scripts,
        "has_templates": has_templates,
        "has_references": has_references,
        "state": state,
        "mtime": mtime_iso,
        "assets": {
            "scripts": sorted(asset_scripts),
            "templates": sorted(asset_templates),
            "references": sorted(asset_references),
        },
    }


def probe_all() -> dict:
    """Probe every skill. Returns the canonical probe dict."""
    out: dict = {}
    for name, path in SKILLS.items():
        out[name] = probe(path)

    # Dedup helper: canonical real → list of names
    canonical_to_aliases: dict[str, list[str]] = {}
    for name, r in out.items():
        if r.get("present") and r.get("real"):
            canonical_to_aliases.setdefault(r["real"], []).append(name)

    for name, r in out.items():
        if r.get("present"):
            r["aliases"] = [a for a in canonical_to_aliases.get(r["real"], []) if a != name]

    # Stats
    states_count = {s: 0 for s in ("PRESENT", "LOADABLE", "EXECUTABLE", "PROVEN", "UNVERIFIED")}
    for r in out.values():
        s = r.get("state", "UNVERIFIED")
        states_count[s] = states_count.get(s, 0) + 1

    n_distinct = len(canonical_to_aliases)

    return {
        "probed_at": datetime.now(timezone.utc).isoformat(),
        "host": os.uname().nodename if hasattr(os, "uname") else "unknown",
        "python": __import__("sys").version.split()[0],
        "n_skills_listed": len(SKILLS),
        "n_distinct_real": n_distinct,
        "states": states_count,
        "skills": out,
    }


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Probe PDF skill filesystem.")
    ap.add_argument("--out", default="-", help="Output JSON path (default: stdout)")
    ap.add_argument("--print", action="store_true", help="Also print human summary")
    args = ap.parse_args()

    probe_data = probe_all()

    if args.out == "-":
        print(json.dumps(probe_data, indent=2, default=str))
    else:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w") as f:
            json.dump(probe_data, f, indent=2, default=str)

    if args.print:
        print(f"probed_at: {probe_data['probed_at']}", file=sys.stderr)
        print(f"skills listed: {probe_data['n_skills_listed']}", file=sys.stderr)
        print(f"distinct real paths: {probe_data['n_distinct_real']}", file=sys.stderr)
        print(f"states: {probe_data['states']}", file=sys.stderr)


if __name__ == "__main__":
    import sys
    main()