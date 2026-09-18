#!/usr/bin/env python3
"""Conformance suite for the doctrine-status gate (U18).

Run directly: python3 /root/AAA/scripts/test_doctrine_status_gate.py

WHY THIS EXISTS: on 2026-09-18 the gate blocked a merge with 8 findings, and 8 of
8 were false positives — every blocked document DID carry a Status line and an
F13 instrument. Two regex defects, both isolated:

  1. STATUS_RE required `Status:` (optionally bolded) immediately after the line
     start. Two real formats in the tree were therefore invisible:
       `> **Generated:** 2026-09-16 | **Status:** Working artifact, not sealed`
       `> **Status of this file:** SOURCE. ...`
     R3 ("new .md has no Status line") then fired on files that had one.

  2. F13_MARKER_RE accepted exactly one token, `F13_RATIFIED_CHAT`, so a line
     carrying `F13_RATIFIED_SOVEREIGN (2026-09-16) — Arif Fazil (F13).` was
     refused for "lacking an F13 instrument" while the instrument sat in plain
     sight. R1 fired on the wrong basis.

Widening a gate that is blocking your own commit is exactly the move that needs
proof, so the negatives below are the point of this file. Each one MUST still
block after the widening; if any stops blocking, the widening removed the
protection instead of a false positive, and the gate must be reverted.
"""
import importlib.util
import re
import sys
from pathlib import Path

GATE = Path(__file__).with_name("doctrine_status_gate.py")

spec = importlib.util.spec_from_file_location("dsg", GATE)
if spec is None or spec.loader is None:
    print(f"cannot load gate module at {GATE}", file=sys.stderr)
    sys.exit(2)
dsg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dsg)

fails = []


def check(label, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}{('  — ' + detail) if detail and not cond else ''}")
    if not cond:
        fails.append(label)


def value_of(line):
    """The Status value the gate would extract from a line, or None."""
    m = dsg.STATUS_RE.search(line)
    return m.group(1) if m else None


def r1_blocks(value):
    """Re-apply the gate's R1 rule to an extracted value."""
    if not dsg.RATIFIED_CLASS_RE.search(value):
        return False
    has_marker = bool(dsg.F13_MARKER_RE.search(value))
    has_instrument = bool(dsg.DATE_RE.search(value) or dsg.QUOTE_RE.search(value))
    return not (has_marker and has_instrument)


print("=" * 74)
print("R3 — STATUS DETECTION (the widening)")
print("=" * 74)

DETECT = [
    ("plain bold", "> **Status:** F13_RATIFIED_CHAT (2026-09-12)"),
    ("plain bare", "Status: DRAFT_AWAITING_F13"),
    ("inline after pipe (was invisible)",
     "> **Generated:** 2026-09-16 | **Status:** Working artifact, not sealed"),
    ("qualified 'of this file' (was invisible)",
     "> **Status of this file:** SOURCE. The operational doctrine lives at"),
    ("blockquote, no bold", "> Status: DRAFT"),
    ("full-width colon", "Status： DRAFT"),
]
for label, line in DETECT:
    check(f"detects: {label}", value_of(line) is not None, repr(line[:50]))

print()
print("=" * 74)
print("NEGATIVE CONTROLS — these MUST still block (protection intact)")
print("=" * 74)

# A new watched .md with no status line at all must still be caught by R3.
for label, body in [
    ("new .md with no Status line",
     "# Some Doctrine\n\n> **Author:** someone\n\nBody prose only.\n"),
    ("prose mentioning Status mid-sentence",
     "The Status: field is checked at commit time by the gate.\n"),
    ("heading that merely contains the word",
     "## Status of the Federation\n\nBody.\n"),
]:
    check(f"R3 still fires: {label}", value_of(body) is None, repr(body[:40]))

print()
print("R1 — INSTRUMENT STILL REQUIRED")

MUST_BLOCK = [
    ("bare self-label, no instrument", "RATIFIED"),
    ("ratified marker, NO date and NO quote", "F13_RATIFIED_CHAT"),
    ("sovereign marker, no date", "F13_RATIFIED_SOVEREIGN"),
    ("CANON with no instrument", "CANONICAL"),
    ("SEALED with no instrument", "SEALED"),
]
for label, value in MUST_BLOCK:
    check(f"R1 blocks: {label}", r1_blocks(value), value)

print()
print("SCOPE NOTE — measured limit, NOT a passing expectation")
print("  `Status: F13_SEAL` (bare, no date) is OUT of R1 territory in this gate,")
print("  because RATIFIED_CLASS_RE recognises SEALED but not bare SEAL. Measured")
print("  2026-09-18: unchanged by the widening, and PRE-EXISTING — a document can")
print("  therefore carry an un-instrumented `F13_SEAL` status and pass. A tightening")
print("  would newly affect 3 lines in the watched tree (all `PROVISIONAL_SEAL`, a")
print("  class that is arguably not a ratification at all). Left ALONE deliberately:")
print("  tightening a governance gate while that same gate is blocking your own")
print("  commit is the mirror of the widening risk. Recorded as a residual for F13.")
check("bare F13_SEAL is out of R1 scope (recorded, not asserted)",
      not r1_blocks("F13_SEAL"))

print()
print("R1 — INSTRUMENTS STILL ACCEPTED")

MUST_PASS = [
    ("F13_RATIFIED_CHAT + date", "F13_RATIFIED_CHAT (2026-09-12)"),
    ("F13_RATIFIED_CHAT + quoted phrase",
     'F13_RATIFIED_CHAT — sovereign: "seal and make it live"'),
    ("F13_RATIFIED_SOVEREIGN + date (the previously-blocked shape)",
     "F13_RATIFIED_SOVEREIGN (2026-09-16) — Arif Fazil (F13)."),
    ("F13_SEAL + date", "F13_SEAL (2026-09-13)"),
    ("F13_SEALED + date", "F13_SEALED 2026-09-16"),
    ("non-ratified class is not R1 territory at all", "DRAFT_AWAITING_F13 (2026-09-16)"),
]
for label, value in MUST_PASS:
    check(f"R1 allows: {label}", not r1_blocks(value), value)

print()
print("R2 — ANNEX CLASS STILL FORBIDDEN")
for label, value in [
    ("CONSTITUTIONAL_ANNEX", "CONSTITUTIONAL_ANNEX"),
    ("CONSTITUTIONAL ANNEX (space)", "CONSTITUTIONAL ANNEX"),
    ("ANNEXED", "ANNEXED"),
]:
    check(f"R2 blocks: {label}", bool(dsg.ANNEX_CLASS_RE.search(value)), value)

print()
print("-" * 74)
if fails:
    print(f"FAILED: {len(fails)} check(s)")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED — false positives removed, protections intact")
sys.exit(0)
