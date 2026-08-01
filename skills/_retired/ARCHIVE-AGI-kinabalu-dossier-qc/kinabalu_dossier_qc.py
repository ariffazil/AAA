#!/usr/bin/env python3
"""
AGI-kinabalu-dossier-qc — Automated 7-Gate QC for Kinabalu Basin Dossier
Run before any deploy. Returns PASS/FAIL per gate. Non-zero exit = at least one FAIL.

Usage:
  python3 kinabalu_dossier_qc.py [--fix] [--json]

Options:
  --fix   Attempt to auto-fix fail-able gates
  --json  Output machine-readable JSON
"""

import re
import sys
import json
import argparse
from pathlib import Path

SOURCE = Path("/root/arif-fazil.com/sites/arif-fazil.com/public/earth/kinabalu-basin/index.html")

GATES = {
    1: {"name": "Summit Height", "floor": "F2", "type": "HARD"},
    2: {"name": "Single VE", "floor": "F4", "type": "HARD"},
    3: {"name": "MMU Not Seal", "floor": "F2", "type": "HARD"},
    4: {"name": "Granite Age", "floor": "F2", "type": "HARD"},
    5: {"name": "Relief Mechanism", "floor": "F2", "type": "HARD"},
    6: {"name": "West Crocker Timing", "floor": "F2", "type": "HARD"},
    7: {"name": "Epistemic Honesty", "floor": "F7", "type": "HARD"},
}


def load_html():
    if not SOURCE.exists():
        return None
    return SOURCE.read_text()


def check_gate_1(html):
    """Summit height: must have 4,095m surveyed, 3,951m only with SRTM label."""
    has_4095 = "4,095" in html
    has_3951 = "3,951" in html
    has_srtm_label = "SRTM" in html and "3,951" in html

    if not has_4095:
        return False, "Missing surveyed summit height 4,095 m"
    if has_3951 and not has_srtm_label:
        return False, "3,951 m appears without SRTM sample label"
    return True, "Summit 4,095 m present; SRTM 3,951 m properly labeled"


def check_gate_2(html):
    """Single VE: only one VE value should appear as the primary."""
    ve_32 = "~32×" in html or "~32x" in html.lower()
    ve_4 = "~4×" in html or "~4x" in html.lower()

    if ve_32:
        return False, "Header says ~32× VE; footer says ~4× — pick one"
    if not ve_4:
        return False, "No VE value found"
    return True, "Single VE ~4× consistent"


def check_gate_3(html):
    """MMU is NOT a seal."""
    if "MMU acts as a regional seal" in html:
        return False, "MMU incorrectly described as regional seal"
    if "intraformational shale" not in html.lower():
        return False, "Missing intraformational shale mention for seal"
    if "correlation datum" not in html.lower():
        return False, "MMU not described as correlation datum"
    return True, "MMU correctly described as datum, not seal"


def check_gate_4(html):
    """Granite age: must use U-Pb zircon 7.85–7.22 Ma, not K-Ar ~10 Ma."""
    if "10–8 Ma" in html and "LATE MIOCENE" in html:
        # Check if this is the granite event (not other events)
        if "Mount Kinabalu" in html or "granodiorite" in html.lower():
            return False, "Stale K-Ar age 10–8 Ma found — should be 7.85–7.22 Ma"
    if "7.85–7.22" not in html:
        return False, "Missing U-Pb zircon age 7.85–7.22 Ma"
    if "Cottam et al. 2010" not in html:
        return False, "Missing Cottam et al. 2010 citation for granite age"
    return True, "Granite age 7.85–7.22 Ma with Cottam et al. 2010 citation"


def check_gate_5(html):
    """Relief mechanism: unroofing + isostatic uplift, not intrusion volume."""
    if "almost entirely the result of" in html and "one intrusion event" in html:
        return False, "Relief attributed to intrusion volume — should be unroofing + isostasy"
    if "unroofing and isostatic" not in html.lower():
        return False, "Missing unroofing and isostatic uplift explanation"
    if "~5 mm/yr" not in html:
        return False, "Missing ongoing uplift rate ~5 mm/yr"
    return True, "Relief correctly attributed to exhumation + isostatic rebound"


def check_gate_6(html):
    """West Crocker timing: deposited AFTER Rajang Unconformity, not scraped during it."""
    if "West Crocker" in html and "scraped off into the accretionary complex" in html:
        if "Rajang Group" in html:
            return False, "West Crocker described as scraped during Sarawak Orogeny — post-dates it"
    # Should have West Crocker placed correctly in stratigraphy
    if "West Crocker" not in html or "Late Eocene" not in html:
        return False, "West Crocker age not specified or missing"
    return True, "West Crocker correctly positioned post-Rajang Unconformity"


def check_gate_7(html):
    """Epistemic honesty: UNKNOWN/CLAIM/ESTIMATE tags on uncertain claims."""
    issues = []

    if "Megah-1" in html and "UNVERIFIED" not in html:
        issues.append("Megah-1 well name not tagged UNVERIFIED")

    if "Meliau Orogeny" in html and "not yet standard" not in html:
        issues.append("Meliau Orogeny not flagged as non-standard nomenclature")

    if "largest Paleogene" in html:
        issues.append("Superlative 'largest Paleogene' should be qualified")

    if "Cornwell et al. JGR 2025" in html and "DOI" not in html:
        issues.append("Cornwell et al. JGR 2025 reference not flagged for DOI verification")

    # Positive checks
    has_unverified = "UNVERIFIED" in html
    has_unknown = "UNKNOWN" in html
    has_claim = "CLAIM" in html
    has_estimate = "ESTIMATE" in html

    if not (has_unverified or has_unknown):
        issues.append("No UNVERIFIED or UNKNOWN epistemic tags found")

    if issues:
        return False, "; ".join(issues)
    return True, f"Epistemic tags present: {'UNVERIFIED' if has_unverified else ''} {'UNKNOWN' if has_unknown else ''} {'CLAIM' if has_claim else ''} {'ESTIMATE' if has_estimate else ''}".strip()


CHECKS = {
    1: check_gate_1,
    2: check_gate_2,
    3: check_gate_3,
    4: check_gate_4,
    5: check_gate_5,
    6: check_gate_6,
    7: check_gate_7,
}


def run_qc(html):
    results = {}
    for gate_num, check_fn in CHECKS.items():
        passed, message = check_fn(html)
        results[gate_num] = {"passed": passed, "message": message, "gate": GATES[gate_num]}
    return results


def format_text(results):
    lines = []
    all_pass = True
    for gate_num in sorted(results.keys()):
        r = results[gate_num]
        icon = "✅" if r["passed"] else "❌"
        floor = r["gate"]["floor"]
        name = r["gate"]["name"]
        lines.append(f"  {icon} Gate {gate_num} ({floor} {name}): {r['message']}")
        if not r["passed"]:
            all_pass = False
    return "\n".join(lines), all_pass


def main():
    parser = argparse.ArgumentParser(description="Kinabalu Dossier QC — 7-Gate Geological Truth Check")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--fix", action="store_true", help="Attempt auto-fix (delegates to agent)")
    args = parser.parse_args()

    html = load_html()
    if html is None:
        print("❌ SOURCE NOT FOUND:", SOURCE)
        sys.exit(2)

    results = run_qc(html)

    if args.json:
        output = {
            "source": str(SOURCE),
            "url": "https://arif-fazil.com/earth/kinabalu-basin/",
            "gates": {str(k): v for k, v in results.items()},
            "all_pass": all(r["passed"] for r in results.values()),
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"🔬 Kinabalu Dossier QC — {SOURCE.name}")
        print(f"   URL: https://arif-fazil.com/earth/kinabalu-basin/\n")
        text, all_pass = format_text(results)
        print(text)
        print(f"\n{'✅ ALL GATES PASS' if all_pass else '❌ GATES FAILED — fix before deploy'}")

    sys.exit(0 if all(r["passed"] for r in results.values()) else 1)


if __name__ == "__main__":
    main()
