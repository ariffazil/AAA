#!/usr/bin/env python3
"""write_price_lint.py — WRITE_PRICE_COLLAPSE detector #1: cross-axis write.

Flags knowledge-axis text (chat, drafts, narratives) that asserts
governance-axis content (verdict / authorization / meaning-assignment)
WITHOUT a governance marker (cc_id, judgment receipt, seal reference).

Heuristic detector — findings are labeled with confidence, never a
verdict. Exit codes: 0 = clean, 2 = violation (it can say NO).

EUREKA-2026-09-09-WRITE-PRICE-COLLAPSE-001
Usage: write_price_lint.py <file...>   (use "-" for stdin)
"""
import json
import re
import sys

# (pattern, label, confidence) — EN + MS, heuristics capped at 0.95
VERDICT_PATTERNS = [
    (r"\bgenuine\b", "genuineness verdict", 0.7),
    (r"\b(verdict|aku\s+sahkan|disahkan)\b", "verdict claim", 0.8),
    (r"\b(it\s+is\s+sealed|this\s+is\s+sealed|aku\s+seal)\b", "self-seal claim", 0.95),
    (r"\b(authorized|approved\s+by\s+me|i\s+approve)\b", "authorization claim", 0.8),
    (r"\b(trust\s+me|percayalah\s+pada\s+aku|i\s+guarantee|dijamin)\b", "trust claim", 0.7),
    (r"\btu\s+(bukan|memang)\s+(love|sayang|genuine|real)\b", "identity/meaning verdict (MS)", 0.75),
    (r"\b(meaning\s+of\s+(this|it)\s+is|maknanya\s+(ialah|adalah)\s+bahawa)\b", "meaning assignment", 0.6),
]

GOVERNANCE_MARKERS = re.compile(
    r"(cc_id|constitutional_chain_id|verdict\s*[:=]|SEAL[-_ ]?(id|seq)|"
    r"judge[_ ]hash|receipt[_ ]hash|888_HOLD|arif_judge|arif_seal|VAULT999)",
    re.I,
)


def lint_text(text):
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if GOVERNANCE_MARKERS.search(line):
            continue  # this line already carries its governance price
        for pat, label, conf in VERDICT_PATTERNS:
            if re.search(pat, line, re.I):
                findings.append(
                    {
                        "line": lineno,
                        "label": label,
                        "confidence": conf,
                        "text": line.strip()[:120],
                    }
                )
    return findings


def main():
    paths = sys.argv[1:]
    if not paths:
        print(__doc__)
        sys.exit(1)
    all_findings = []
    for p in paths:
        if p == "-":
            text = sys.stdin.read()
        else:
            with open(p, encoding="utf-8", errors="replace") as f:
                text = f.read()
        for f in lint_text(text):
            f["source"] = p
            all_findings.append(f)
    report = {
        "detector": "cross_axis_write",
        "eureka": "EUREKA-2026-09-09-WRITE-PRICE-COLLAPSE-001",
        "files": paths,
        "count": len(all_findings),
        "findings": all_findings,
        "verdict": "WRITE_PRICE_VIOLATION" if all_findings else "CLEAN",
        "note": "heuristic evidence, never a verdict — route findings to judgment lane",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(2 if all_findings else 0)


if __name__ == "__main__":
    main()
