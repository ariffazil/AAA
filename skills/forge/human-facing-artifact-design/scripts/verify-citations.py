#!/usr/bin/env python3
"""Verify every URL cited in an artifact actually resolves.

Why: a citation-shaped string that 404s is not a source. An artifact whose
references are dead reads as authoritative and cannot be checked — the reader
trusts the format and inherits the gap. Verify BEFORE building the deliverable:
a dead link found after a PDF render costs the whole render.

Usage:
    python3 verify-citations.py <artifact> [<artifact> ...]
    python3 verify-citations.py brief.html deck.md notes.txt register.json

Accepts .html / .htm / .md / .txt / .json, or any text file containing URLs.
For a built PDF, run this against the SOURCE that produced it rather than the
PDF itself (an internal source register is the reliable place to check).

Output: one line per URL with its status, then a summary. Exit 0 if everything
resolves, 1 if anything is dead or unanswered, so it composes into a build gate.

Status semantics (a HEAD that is refused is not a failure):
    2xx / 3xx        -> live
    403 / 405 / 429  -> live: the host answered, the resource refuses HEAD
    404 / 410        -> DEAD: replace the citation or drop the claim
    000 / timeout    -> no response: investigate before shipping
"""

import re
import subprocess
import sys

URL_RE = re.compile(r"https?://[^\s\"'`<>)\]}]+[^\s\"'`<>)\]}.,;]")
TIMEOUT = 12


def extract_urls(path: str) -> list[str]:
    """Unique URLs in first-seen order."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as exc:
        print(f"  cannot read {path}: {exc}")
        return []
    seen, out = set(), []
    for url in URL_RE.findall(text):
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out


def check(url: str) -> tuple[str, bool]:
    """(status, is_live). HEAD, following redirects."""
    try:
        proc = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", str(TIMEOUT), "-L", "-I", url],
            capture_output=True, text=True, timeout=TIMEOUT + 5,
        )
        code = proc.stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        return "TIMEOUT", False

    if code in ("403", "405", "429"):
        return f"{code} (host answered)", True
    if code.startswith("2") or code.startswith("3"):
        return f"{code} OK", True
    if code in ("404", "410"):
        return code, False
    return code or "NO-RESPONSE", False


if __name__ == "__main__":
    targets = sys.argv[1:]
    if not targets:
        print(__doc__)
        sys.exit(2)

    total = dead_total = 0
    for path in targets:
        urls = extract_urls(path)
        if not urls:
            print(f"{path}: no URLs found")
            continue
        print(f"\n=== {path} — {len(urls)} URL(s) ===")
        for url in urls:
            status, live = check(url)
            total += 1
            if not live:
                dead_total += 1
            print(f"  {'PASS' if live else 'FAIL'}  {status:<20} {url}")

    print("\n" + "-" * 68)
    print(f"LIVE: {total - dead_total}/{total}   FAILED: {dead_total}")
    if dead_total:
        print("\nFix or drop the failed citations before building the artifact:")
        print("  a 404 is a claim with no source, not a footnote with a typo.")
        sys.exit(1)
    print("All citations resolve.")
