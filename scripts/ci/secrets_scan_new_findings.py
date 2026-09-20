#!/usr/bin/env python3
"""Report secrets that are NEW relative to .secrets.baseline.

Exit codes
----------
0  no new secrets vs baseline      (gate PASS)
1  new secrets found               (gate FAIL, findings printed)
2  scanner error                   (gate FAIL, diagnostic printed)

Why this exists
---------------
The gate previously embedded this logic as Python inside a shell command
substitution in `.github/workflows/secrets-audit.yml`:

    SCAN_RESULT=$(python3 -c "..." 2>&1)
    echo "$SCAN_RESULT"
    echo "$SCAN_RESULT" | tail -1 | grep -q "NEW_SECRETS_FOUND=0" || exit 1

Two defects made that gate fail *blind* (nothing printed, no cause visible):

1. `2>&1` redirected detect-secrets' stderr into the variable, so a crashed
   scan produced diagnostics that were captured and never shown.
2. Under `set -e`, a non-zero exit from the command substitution aborted the
   step *before* `echo "$SCAN_RESULT"` ran. The step exited 1 with no output.

Consequence: CI reported `##[error]Process completed with exit code 1.` with an
empty log, and the offending finding was invisible. Extracting the logic here
(and invoking it without `set -e` masking in the workflow) makes the failure
self-diagnosing.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

# Must stay in sync with the patterns used to generate .secrets.baseline —
# detect-secrets records them in `filters_used`, so drift here would show up
# as a spurious baseline diff on the next regeneration.
EXCLUDE_PATTERNS = [
    "_archive/.*",
    "archive/.*",
    "docs/.*",
    "memory/.*",
    "reports/.*",
    "secrets/.*",
    "agents/.*/runtime/.*",
    "wiki/.*",
    # Narrow FP exclusion (disposition 2026-09-13, SEAL-42dad7d3d9334310):
    # canon/PETRONAS/qdrant_backup_*.json — single match is an Obsidian article
    # URL slug; masked scan confirms no live-credential-shaped remaining hits.
    # Review: 2026-12-13.
    r"canon/PETRONAS/qdrant_backup_.*\.json",
    r"skills/.*/_meta\.json",
    ".secrets.baseline",
]


def _die(message: str, exc: Exception | None = None) -> int:
    """Emit a scanner error with as much context as we have, then fail."""
    print(f"ERROR: {message}", file=sys.stderr)
    if exc is not None:
        print(f"  {type(exc).__name__}: {exc}", file=sys.stderr)
    print("NEW_SECRETS_FOUND=unknown")
    return 2


def main() -> int:
    workspace = os.environ.get("GITHUB_WORKSPACE") or os.getcwd()
    baseline_path = os.path.join(workspace, ".secrets.baseline")

    cmd = ["detect-secrets", "scan", "."]
    for pattern in EXCLUDE_PATTERNS:
        cmd += ["--exclude-files", pattern]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=workspace, check=False
        )
    except FileNotFoundError as exc:
        return _die("detect-secrets not found on PATH", exc)

    if result.returncode != 0:
        print("ERROR: detect-secrets scan failed", file=sys.stderr)
        print(f"  exit code: {result.returncode}", file=sys.stderr)
        if result.stderr.strip():
            print("  stderr:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
        print("NEW_SECRETS_FOUND=unknown")
        return 2

    try:
        current = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print("ERROR: detect-secrets returned unparseable JSON", file=sys.stderr)
        print(f"  {exc}", file=sys.stderr)
        print("  stdout head:", file=sys.stderr)
        print(result.stdout[:2000], file=sys.stderr)
        return 2

    baseline: dict = {}
    if os.path.exists(baseline_path):
        try:
            with open(baseline_path) as handle:
                baseline = json.load(handle)
        except json.JSONDecodeError as exc:
            return _die(f"baseline {baseline_path} is not valid JSON", exc)
    baseline_results = baseline.get("results", {})

    new_findings = []
    for filename, entries in current.get("results", {}).items():
        known = {e["hashed_secret"] for e in baseline_results.get(filename, [])}
        for entry in entries:
            if entry["hashed_secret"] not in known:
                new_findings.append((filename, entry))

    if not new_findings:
        print("✅ No new secrets detected")
        print("NEW_SECRETS_FOUND=0")
        return 0

    print(f"❌ {len(new_findings)} finding(s) not present in .secrets.baseline:")
    for filename, entry in sorted(
        new_findings, key=lambda item: (item[0], item[1].get("line_number", 0))
    ):
        print(
            f"  🚫 {entry['type']} in {filename}:{entry['line_number']} "
            f"(hash {entry['hashed_secret'][:16]}…)"
        )
    print()
    print("If every finding above is a reviewed FALSE POSITIVE (for example a")
    print("secret *reference* such as \"api_key_ref\": \"secrets::SOME_VAR\"),")
    print("refresh the baseline after human review — never to silence a real key:")
    print("  detect-secrets scan . --exclude-files ... > .secrets.baseline")
    print("NEW_SECRETS_FOUND=" + str(len(new_findings)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
