"""
test_hermes_entity_classifier.py — P0 2026-09-21 (S7 federation-convergence).

Regression canaries for the HERMES entity classifier scar:

    "The"         → PERSON  (function word, must be UNKNOWN)
    WEALTH        → PERSON  (organ, must be AI_ORGAN)
    Parliament    → PERSON  (institution, must be LEGISLATURE)
    Unity Govt    → PERSON  (collective, must be COALITION)
    September     → PERSON  (month, must be TIME)

Doctrine: Institution ≠ Person.
The parser MUST NOT classify an institution as a person.

This test imports the deterministic classifier from HERMES:
    /root/HERMES/mcp/hermes-rasa/principal_type_classifier.py

Constitutional:
    F2 TRUTH   — every assertion cites the input + expected type
    F6 MARUAH  — humans are not typed slots; UNKNOWN is the safe default
    F11 AUDIT  — every classification carries a rule for receipt
"""

from __future__ import annotations

import sys
from pathlib import Path

# Import the deterministic classifier
sys.path.insert(0, "/root/HERMES/mcp/hermes-rasa")
from principal_type_classifier import (  # noqa: E402
    classify_principal_type,
    PrincipalType,
)

CANARIES = [
    # Required regression (per F13 2026-09-21)
    ("Anthony Loke", PrincipalType.PERSON, "named person → PERSON"),
    ("DAP", PrincipalType.POLITICAL_PARTY, "party → POLITICAL_PARTY"),
    ("WEALTH", PrincipalType.AI_ORGAN, "federation organ → AI_ORGAN"),
    ("Parliament", PrincipalType.LEGISLATURE, "legislature → LEGISLATURE"),
    ("Malaysia", PrincipalType.STATE, "country → STATE"),
    ("September", PrincipalType.TIME, "month → TIME"),
    ("Budget 2027", PrincipalType.DOCUMENT, "event-document → DOCUMENT"),
    ("PETRONAS", PrincipalType.CORPORATION, "federal corp → CORPORATION"),
    # Historical-failure regressions (must NOT regress)
    ("The", PrincipalType.UNKNOWN, "function word → UNKNOWN (was PERSON)"),
    ("Unity Government", PrincipalType.COALITION, "collective → COALITION"),
    # Edge cases (additional coverage)
    ("Anwar Ibrahim", PrincipalType.PERSON, "named person → PERSON"),
    ("Ministry of Health", PrincipalType.INSTITUTION, "institution suffix → INSTITUTION"),
    ("Kuala Lumpur", PrincipalType.CITY, "city → CITY"),
    ("GE", PrincipalType.UNKNOWN, "ambiguous acronym → UNKNOWN"),
    ("", PrincipalType.UNKNOWN, "empty string → UNKNOWN"),
]


def _check(label, ok, detail=""):
    glyph = "✓" if ok else "✗"
    line = f"  {glyph} {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return ok


def main() -> int:
    print("=" * 70)
    print("FEDERATION E2E — HERMES principal-type classifier")
    print("  Test ID: P0-2026-09-21-S7")
    print("  Doctrine: Institution ≠ Person")
    print("=" * 70)

    all_ok = True
    for name, expected, desc in CANARIES:
        cls = classify_principal_type(name)
        ok = cls.principal_type == expected
        all_ok &= _check(desc, ok,
                         f"got={cls.principal_type.value} rule={cls.matched_rule} conf={cls.confidence}")

    print()
    print("=" * 70)
    if all_ok:
        print("RESULT: PASS — HERMES principal-type classifier resolves correctly")
        print("  - 8 required canaries pass")
        print("  - historical failure modes (The/Unity) blocked")
        return 0
    else:
        print("RESULT: FAIL — classifier still routes institution-as-person")
        return 1


if __name__ == "__main__":
    sys.exit(main())
