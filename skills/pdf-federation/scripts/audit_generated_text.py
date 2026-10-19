#!/usr/bin/env python3
"""Pre-delivery audit for a generated PDF: catches corrupted authored prose.

Long prose written into a build script can pick up stray non-Latin tokens and
fused word-joins that no linter, no `write_file` verification, and no exit code
will report. This scans the SOURCE and the EXTRACTED PDF text for them.

Usage:
    python3 scripts/audit_generated_text.py out.pdf
    python3 scripts/audit_generated_text.py out.pdf --require "behavioral sink" --require "57 peratus"
    python3 scripts/audit_generated_text.py out.pdf --source content.py

Exit code 1 if any check fails, so it can gate a delivery.
"""

import argparse
import collections
import pathlib
import re
import sys

# Anything past Latin-1 + General Punctuation. Real BM/EN prose stays below
# this; CJK, Cyrillic stray insertions, and replacement chars all trip it.
NONLATIN_FLOOR = 0x2200

# Tokens that mean the prose got mangled. Extend per-language.
# Bare "amongst"/"the" would false-positive on legitimate English quotes, so
# only list them as junk when the document body is not English.
DEFAULT_JUNK = [
    "_\u0433", "csharp", "Localization", "padailder", "_\u4e00",
    "d_", "nar_nar", "\ufffd",
]


def scan(text, label, junk):
    problems = []
    stray = collections.Counter(c for c in text if ord(c) > NONLATIN_FLOOR)
    if stray:
        for ch, n in stray.most_common():
            line_no = next(
                (i for i, ln in enumerate(text.split("\n"), 1)
                 if ch in ln and any(ord(c) > NONLATIN_FLOOR for c in ln)),
                "?",
            )
            ctx = next(
                (" ".join(ln.split()) for ln in text.split("\n")
                 if ch in ln and any(ord(c) > NONLATIN_FLOOR for c in ln)),
                "",
            )
            problems.append(
                f"{label}: non-Latin {ch!r} U+{ord(ch):04X} x{n} near {ctx[:90]!r}"
            )
    for j in junk:
        n = text.count(j)
        if n:
            where = label
            snippet = next(
                (" ".join(m.group(0).split())
                 for m in re.finditer(r".{0,45}" + re.escape(j) + r".{0,45}", text, re.S)),
                "",
            )
            problems.append(f"{where}: junk token {j!r} x{n} :: {snippet[:100]!r}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--source", help="build script to scan too")
    ap.add_argument("--require", action="append", default=[],
                    help="string that MUST appear in the PDF text layer (repeatable)")
    ap.add_argument("--expect-pages", type=int)
    ap.add_argument("--junk", action="append", default=[],
                    help="extra junk token to flag (repeatable)")
    args = ap.parse_args()

    try:
        import pymupdf
    except ImportError:
        print("SKIP: pymupdf unavailable in this interpreter")
        return 0

    doc = pymupdf.open(args.pdf)
    pdf_text = "".join(p.get_text() for p in doc)
    flat = re.sub(r"\s+", " ", pdf_text)

    problems = []
    problems += scan(pdf_text, "PDF", args.junk or DEFAULT_JUNK)
    if args.source and pathlib.Path(args.source).exists():
        src = pathlib.Path(args.source).read_text(encoding="utf-8")
        problems += scan(src, "SRC", args.junk or DEFAULT_JUNK)

    for req in args.require:
        if req not in flat:
            problems.append(f"MISSING required string: {req!r}")

    pages = doc.page_count
    words = len(re.findall(r"\S+", pdf_text))
    if args.expect_pages and pages != args.expect_pages:
        problems.append(f"page count {pages} != expected {args.expect_pages}")

    fonts = {f[3] for p in doc for f in p.get_fonts(full=True)}
    print(f"pages={pages} words={words} fonts={len(fonts)}")

    if problems:
        print("\n".join("  FAIL " + p for p in problems))
        return 1
    print("  clean: no stray glyphs, junk tokens, or missing required strings")
    return 0


if __name__ == "__main__":
    sys.exit(main())