#!/usr/bin/env python3
"""Doctrine Status Gate — U18 mechanical enforcement at commit boundary.

FEDERATION-CONSTITUTIONAL-INVARIANTS-v1.1 U18 (F13_RATIFIED_CHAT 2026-09-12).
K6 scar (UL-002): an execution harness reclassified DRAFT docs to
CONSTITUTIONAL_ANNEX via status-line edit — caught by a peer, not by a
boundary. This gate makes the boundary catch it.

Checks STAGED content (git show :path), never the working tree.
Rules apply to **Status:** lines ONLY — body prose is evidence, never blocked.

  R1  A Status line claiming a ratified-class value must carry an F13
      instrument: the F13_RATIFIED_CHAT marker AND (a YYYY-MM-DD date OR
      a quoted sovereign phrase >= 6 chars) on the same line.
      Bare self-labeling ("Status: RATIFIED") blocks.
  R2  ANNEX-class Status values (CONSTITUTIONAL_ANNEX etc.) block
      unconditionally — no valid instrument form exists.
  R3  A NEW .md entering instructions/ or governance/ must carry a
      Status line at all. Nothing joins the doctrine surface unlabeled.

Deterministic, no runtime deps beyond git. Zero detection debt.
DITEMPA BUKAN DIBERI.
"""

import re
import subprocess
import sys

WATCHED_PREFIXES = ("instructions/", "governance/")

STATUS_RE = re.compile(
    r"^\s*>?\s*\*{0,2}Status\*{0,2}\s*[:\uff1a]\s*(.+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
F13_MARKER_RE = re.compile(r"F13[_\s-]*RATIFIED[_\s-]*CHAT", re.IGNORECASE)
RATIFIED_CLASS_RE = re.compile(r"(?:\b|_)(RATIFIED|SEALED|CANON|CANONICAL|CONSTITUTIONAL)(?:\b|_)", re.IGNORECASE)
ANNEX_CLASS_RE = re.compile(r"CONSTITUTIONAL[_\s-]*ANNEX|\bANNEXED?\b", re.IGNORECASE)
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
QUOTE_RE = re.compile(r"\"[^\"]{6,}\"")


def staged_files():
    """Return [(status_letter, path)] for staged watched .md files."""
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-status", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception as e:
        print(f"DOCTRINE-STATUS GATE: verifier error ({e}) — fail-closed", file=sys.stderr)
        sys.exit(1)
    if out.returncode != 0:
        print(f"DOCTRINE-STATUS GATE: git error — fail-closed", file=sys.stderr)
        sys.exit(1)
    files = []
    for line in out.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        letter, path = parts[0], parts[-1]
        if path.endswith(".md") and path.startswith(WATCHED_PREFIXES):
            files.append((letter, path))
    return files


def staged_content(path):
    r = subprocess.run(["git", "show", f":{path}"], capture_output=True, text=True, timeout=15)
    return r.stdout if r.returncode == 0 else ""


def check_file(letter, path, errors):
    content = staged_content(path)
    statuses = STATUS_RE.findall(content)

    # R3 — new doctrine files must be labeled
    if letter == "A" and not statuses:
        errors.append(f"R3 {path}: new watched .md has no Status line — label it (DRAFT_*, PENDING_*, spec, or F13 instrument)")

    for value in statuses:
        # R2 — annex-class always blocks
        if ANNEX_CLASS_RE.search(value):
            errors.append(f"R2 {path}: ANNEX-class Status forbidden ({value[:60]}) — no instrument form exists (K6/UL-002)")
            continue
        # R1 — ratified-class requires F13 marker + date-or-quote on the line
        if RATIFIED_CLASS_RE.search(value):
            has_marker = bool(F13_MARKER_RE.search(value))
            has_instrument = bool(DATE_RE.search(value) or QUOTE_RE.search(value))
            if not (has_marker and has_instrument):
                errors.append(
                    f"R1 {path}: ratified-class Status lacks F13 instrument "
                    f"(need F13_RATIFIED_CHAT + date or quoted phrase) — got: {value[:70]}"
                )


def main():
    files = staged_files()
    if not files:
        return 0
    errors = []
    for letter, path in files:
        check_file(letter, path, errors)
    if errors:
        print("DOCTRINE-STATUS GATE: BLOCKED", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print(f"doctrine-status-gate: {len(files)} watched file(s) OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
