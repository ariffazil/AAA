#!/usr/bin/env python3
"""
build_people_registry.py — T1 re-runnable P-axis scanner.

Scans the 4 sources for humans referenced in ARIF's relational memory:
  Source 1: H1-H6 directories (scar files, biography PDFs)
  Source 2: H4-identity .md files (HUMANS.md, FAMILY_FAZIL.md)
  Source 3: H5 scar files + Reality Legacy PDF (named institutional persons)
  Source 4: WhatsApp forwards in H4 + lane config (telegram network)

Emits a draft registry + INDEX.md plan WITHOUT writing anything.
The agent reviews the draft, then writes via skill_manage / write_file.

Usage:
  python3 scripts/build_people_registry.py          # scan + emit draft
  python3 scripts/build_people_registry.py --apply  # scan + write (T1 auto-do)
  python3 scripts/build_people_registry.py --json   # JSON-only output
"""
import json, sys, os, re
from pathlib import Path
from datetime import datetime, timezone

HUMAN_PATTERNS = [
    # Malay names
    r"\bbin\s+[A-Z][a-z]+",
    r"\bbinti\s+[A-Z][a-z]+",
    r"\bEncik\s+[A-Z][a-z]+",
    r"\bPuan\s+[A-Z][a-z]+",
    r"\bTuan\s+[A-Z][a-z]+",
    r"\bHaji\s+[A-Z][a-z]+",
    r"\bHajjah\s+[A-Z][a-z]+",
    # Petronas colleagues
    r"Ahmad\s+Faisal\s+Bakar",
    # Parents
    r"\bFazil\s+bin\s+Khamis",
    r"\bFaridah\s+binti\s+Othman",
    # Known siblings
    r"\bNabilah\s+Fazil",
    r"\bNaazira\s+Fazil",
    r"\bAzwa\s+Fazil",
    # Telegram network
    r"\bSyed\b",
    r"\bAliff\b",
    r"\bIzzu\b",
    r"\bWawa\b",
]

H5_DIR = Path("/root/memory/H5-scars")
H4_DIR = Path("/root/memory/H4-identity")
PEOPLE_DIR = Path("/root/memory/people")


def scan_h5_scars():
    """Source 3a: H5 scar files."""
    findings = []
    for scar_file in H5_DIR.glob("SCAR_*.md"):
        text = scar_file.read_text(encoding="utf-8", errors="ignore")
        scar_id = scar_file.stem
        # Extract humans from text
        for pattern in HUMAN_PATTERNS:
            for match in re.finditer(pattern, text):
                findings.append({
                    "name": match.group(),
                    "source_file": str(scar_file),
                    "scar_id": scar_id,
                    "epistemic": "OBS",
                })
    return findings


def scan_h4_md():
    """Source 2: H4-identity .md files (the trap — often missed)."""
    findings = []
    if not H4_DIR.exists():
        return findings
    for md_file in H4_DIR.glob("*.md"):
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        for pattern in HUMAN_PATTERNS:
            for match in re.finditer(pattern, text):
                findings.append({
                    "name": match.group(),
                    "source_file": str(md_file),
                    "epistemic": "OBS" if "WhatsApp" in text or "chat" in text.lower() else "DER",
                })
    return findings


def scan_biography_pdfs():
    """Source 1b: H4 biography PDFs — Reality Legacy especially."""
    findings = []
    pdf_files = list(H4_DIR.glob("*.pdf"))
    for pdf in pdf_files:
        if "REALITY_LEGACY" not in pdf.name:
            continue
        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf)
            full_text = "\n".join(p.extract_text() for p in reader.pages)
            for pattern in HUMAN_PATTERNS:
                for match in re.finditer(pattern, full_text):
                    findings.append({
                        "name": match.group(),
                        "source_file": str(pdf),
                        "page_count": len(reader.pages),
                        "epistemic": "OBS",
                    })
        except ImportError:
            findings.append({
                "name": "(pypdf not installed — install with: pip install pypdf)",
                "source_file": str(pdf),
                "epistemic": "UNKNOWN",
            })
    return findings


def classify_privacy(name, source_file):
    """Apply privacy classification based on name + source."""
    source_lower = str(source_file).lower()

    # F5 highest privacy: WhatsApp forward family chat
    if "family_fazil" in source_lower or "discuss abah" in source_lower:
        if "Fattah" in name or "Fahim" in name:
            return "F5_HIGHEST_MINOR_PROTECTION" if "Fattah" in name else "F5_HIGHEST"
        if any(sib in name for sib in ["Nabilah", "Naazira", "Azwa"]):
            return "F5_HIGHEST"

    # Doctrine authors (parents)
    if "Fazil" in name and "bin" in name:
        return "DOCTRINE_AUTHOR"
    if "Faridah" in name:
        return "DOCTRINE_AUTHOR"

    # Named institutional person (Bakar only)
    if "Ahmad Faisal Bakar" in name or "Faisal Bakar" in name:
        return "NAMED_INSTITUTIONAL_RESTRICTED"

    # Telegram network
    if name in ["Syed", "Aliff", "Izzu", "Wawa"]:
        return "PROFILE_ONLY"

    # Sovereign
    if "Arif" in name and "bin" in name:
        return "FULL_H_AXIS"

    # Default
    return "UNKNOWN"


def main():
    apply = "--apply" in sys.argv
    json_only = "--json" in sys.argv

    findings = []
    findings.extend(scan_h5_scars())
    findings.extend(scan_h4_md())
    findings.extend(scan_biography_pdfs())

    # Deduplicate by (name, source_file)
    seen = set()
    unique_findings = []
    for f in findings:
        key = (f["name"], f["source_file"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    # Apply privacy classification
    for f in unique_findings:
        f["privacy_class"] = classify_privacy(f["name"], f["source_file"])

    # Aggregate by name
    by_name = {}
    for f in unique_findings:
        name = f["name"]
        if name not in by_name:
            by_name[name] = {
                "name": name,
                "occurrences": 0,
                "source_files": set(),
                "privacy_class": f["privacy_class"],
                "epistemic": f.get("epistemic", "OBS"),
            }
        by_name[name]["occurrences"] += 1
        by_name[name]["source_files"].add(f["source_file"])

    # Convert to list, sorted by occurrence count
    summary = sorted(by_name.values(), key=lambda x: -x["occurrences"])

    # Emit output
    if json_only:
        # Convert sets to lists for JSON serialization
        for item in summary:
            item["source_files"] = sorted(item["source_files"])
        print(json.dumps({
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "total_unique_humans": len(summary),
            "total_findings": len(unique_findings),
            "humans": summary,
        }, indent=2, ensure_ascii=False))
    else:
        print(f"=== P-AXIS SCAN — {datetime.now(timezone.utc).isoformat()} ===")
        print(f"Total findings: {len(unique_findings)}")
        print(f"Unique humans: {len(summary)}")
        print()
        for item in summary:
            files = sorted(item["source_files"])
            files_short = [os.path.basename(f) for f in files]
            print(f"  {item['name']:30s} [{item['privacy_class']:30s}] x{item['occurrences']}  ({', '.join(set(files_short))})")
        print()
        print("=== NEXT STEPS ===")
        print("1. Review findings above")
        print("2. Cross-reference with existing /root/memory/people/INDEX.md")
        print("3. For NEW humans, create person-card.md in appropriate subdir")
        print("4. Update people_registry.json (bump version + add changes_from_vN)")
        print("5. Re-run this script after each iteration — counts will grow")

    return 0


if __name__ == "__main__":
    sys.exit(main())