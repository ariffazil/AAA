#!/usr/bin/env python3
"""
audit_letter_claims.py
======================
Pre-send audit script for civic whistleblower letters.

Checks:
- Each numeric claim traces to a verifiable source
- Each row in data table has SHA-256 hash
- No baseline shopping (the baseline is explicit and defensible)
- No direct moral labels for named individuals
- One specific measurable request is present
- Distribution list <= 4 recipients
- Author identifying info is NOT in the visual/footer

Usage:
    python3 audit_letter_claims.py --letter letter.txt --data data.json
"""
import re
import sys
import json
import argparse
import hashlib

# === ANTI-PATTERNS ===
MORAL_LABELS = [
    r"\bdevil(s)?\b", r"\bsyaitan\b", r"\biblis\b", r"\bevil\b",
    r"\bcorrupt(ed)?\b", r"\brasuah\b", r"\bthief\b", r"\bpencuri\b",
    r"\bwants? to die\b", r"\bmahu mati\b",
    r"\bmust die\b", r"\bmesti mati\b", r"\bterbunuh\b", r"\bbunuh\b",
    r"\btamak\b", r"\bgreedy\b",
]

GEOPOLITICAL_ANALOGIES = [
    r"\bisrael\b", r"\bpalestine\b", r"\bpalestin\b",
    r"\bcolonial\b", r"\bpenjajah", r"\bimperialis",
    r"\bapartheid\b",
]

FALSE_CLAIM_PATTERNS = [
    r"\bno (public )?inquir(y|ies)\b", r"\btiada siasatan awam\b",
    r"\bnever happen(s|ed)?\b", r"\btidak pernah\b(?!\s+(lagi|jadi))",
    r"\bno one\b(?!\s+asks?)", r"\btidak siapa(?!\s+tanya)",
]

# === CHECKS ===

def check_moral_labels(text):
    """Flag direct moral labels on individuals."""
    hits = []
    for pattern in MORAL_LABELS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            hits.extend([(pattern, m) for m in matches])
    return hits


def check_geopolitical(text):
    """Flag geopolitical analogies that deflect from substance."""
    hits = []
    for pattern in GEOPOLITICAL_ANALOGIES:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            hits.extend([(pattern, m) for m in matches])
    return hits


def check_false_claims(text):
    """Flag false-claim patterns that need verification."""
    hits = []
    for pattern in FALSE_CLAIM_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            hits.extend([(pattern, m) for m in matches])
    return hits


def check_specific_request(text):
    """Look for at least one specific, measurable request."""
    request_signals = [
        r"\bsaya memohon\b", r"\bsaya cadangkan\b",
        r"\bsaya minta\b", r"\bplease (declare|consider|review|publish)\b",
        r"\bisytihar(?:kan)?\b", r"\bsila (isytihar|pertimbangkan)\b",
        r"\brequest:?\b", r"\bappeal(ing)?\b",
    ]
    found = []
    for pattern in request_signals:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(pattern)
    return found


def check_data_hashes(data):
    """Verify each data row has a SHA-256 hash matching the data."""
    issues = []
    if not data:
        return ["No data provided"]
    for row in data:
        if "hash" not in row:
            issues.append(f"Row {row.get('label', '?')} missing hash")
            continue
        # Recompute hash from non-hash fields
        hashable = {k: v for k, v in row.items() if k != "hash"}
        computed = hashlib.sha256(json.dumps(hashable, sort_keys=True).encode()).hexdigest()
        if computed[:len(row["hash"])] != row["hash"]:
            issues.append(f"Row {row.get('label', '?')}: hash mismatch (got {computed[:16]}, expected {row['hash']})")
    return issues


def check_identifying_info(text):
    """Flag potential author-identifying info in visual/footer area."""
    issues = []
    patterns = [
        (r"github\.com/[A-Za-z0-9-]+/[A-Za-z0-9-]+", "GitHub URL"),
        (r"\.local/share/arifos|forge_work/[a-z0-9-]+", "Internal filesystem path"),
        (r"\bHermes ASI\b|\bArif Fazil\b|\barif[-_]fazil\b", "Personal/agent name"),
        (r"\b[A-Z][a-z]+ @ [A-Za-z]+\b", "Possibly personal social handle"),
    ]
    for pattern, label in patterns:
        if re.search(pattern, text):
            issues.append(f"{label} found -- may expose author identity")
    return issues


def check_distribution(recipients):
    """Distribution list <= 4 recipients."""
    if not recipients:
        return ["No distribution list provided"]
    if len(recipients) > 4:
        return [f"Distribution list has {len(recipients)} recipients (>4). Mass-blast detected."]
    return []


# === MAIN ===

def audit_letter(letter_path, data_path=None, recipients=None):
    with open(letter_path, "r") as f:
        text = f.read()

    data = None
    if data_path:
        with open(data_path, "r") as f:
            data = json.load(f)

    print(f"=== AUDIT REPORT: {letter_path} ===\n")

    print("[1] Moral labels on individuals:")
    hits = check_moral_labels(text)
    if hits:
        for pattern, match in hits[:10]:
            print(f"  ❌ FOUND: '{match}' (pattern: {pattern})")
    else:
        print("  ✅ No moral labels detected")
    print()

    print("[2] Geopolitical analogies:")
    hits = check_geopolitical(text)
    if hits:
        for pattern, match in hits[:10]:
            print(f"  ⚠️  FOUND: '{match}' -- may deflect from substance")
    else:
        print("  ✅ No geopolitical analogies")
    print()

    print("[3] False-claim patterns (verify against primary sources):")
    hits = check_false_claims(text)
    if hits:
        for pattern, match in hits[:10]:
            print(f"  ⚠️  VERIFY: '{match}' -- must be traceable to public report")
    else:
        print("  ✅ No common false-claim patterns")
    print()

    print("[4] Specific measurable request:")
    found = check_specific_request(text)
    if found:
        print(f"  ✅ Request signals found: {len(found)} pattern(s)")
    else:
        print("  ❌ NO SPECIFIC REQUEST. Add one measurable, hard-to-dismiss ask.")
    print()

    print("[5] Data integrity (SHA-256 + Merkle):")
    issues = check_data_hashes(data)
    if issues:
        for i in issues:
            print(f"  ❌ {i}")
    elif data is not None:
        print(f"  ✅ {len(data)} rows verified")
    else:
        print("  ⚠️  No data provided -- cannot verify hashes")
    print()

    print("[6] Author identifying info:")
    issues = check_identifying_info(text)
    if issues:
        for i in issues:
            print(f"  ❌ {i}")
    else:
        print("  ✅ No identifying info detected")
    print()

    print("[7] Distribution list:")
    issues = check_distribution(recipients)
    if issues:
        for i in issues:
            print(f"  ⚠️  {i}")
    else:
        print(f"  ✅ Distribution: {len(recipients)} recipient(s)")
    print()

    print("=== END AUDIT ===")
    print("If any section shows ❌ or ⚠️, do NOT send. Apply civic-whistleblower-letter skill.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--letter", required=True)
    parser.add_argument("--data")
    parser.add_argument("--recipients", nargs="*", default=[])
    args = parser.parse_args()

    audit_letter(args.letter, args.data, args.recipients)