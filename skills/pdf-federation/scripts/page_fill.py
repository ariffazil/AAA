#!/usr/bin/env python3
"""Per-page content-fill audit for a generated PDF.

Usage:
    python3 page_fill.py out.pdf [--footer-band 800] [--min-fill 65]
                                 [--expect-cover]

Why this exists: taking max(y1) over every text block is a footgun. The footer is
drawn near the bottom of every page, so every page measures ~97% full while half
of them may really end a third of the way down (a forced page break per section).
Blocks whose y1 falls inside the footer band are excluded before measuring.

Exit 1 if any page fills less than --min-fill per cent, or if --expect-cover is
given and page 1 is not cover-only (more than 4 non-footer blocks).
"""
import argparse
import sys

try:
    import pymupdf
except ImportError:  # older wheels ship the same API under the legacy name
    import fitz as pymupdf


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--footer-band", type=float, default=800.0,
                    help="PDF points (origin top-left); blocks below this are footer")
    ap.add_argument("--min-fill", type=float, default=65.0)
    ap.add_argument("--expect-cover", action="store_true")
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    flagged = []
    for n, page in enumerate(doc, 1):
        height = page.rect.height
        blocks = [b for b in page.get_text("blocks") if b[4].strip()]
        body = [b for b in blocks if b[3] < args.footer_band]

        if not body:
            print(f"p{n}: EMPTY")
            flagged.append(n)
            continue

        if n == 1 and args.expect_cover and len(body) > 4:
            print(f"p{n}: COVER DIRTY - {len(body)} blocks on page 1; a full-page "
                  "cover must keep its own page (a missing add_page() after the "
                  "cover draws body text over the dark rect)")
            flagged.append(n)

        end = max(b[3] for b in body)
        pct = 100.0 * end / height
        head = body[0][4].strip().replace("\n", " / ")[:46]
        mark = "  <-- SPARSE" if pct < args.min_fill else ""
        print(f"p{n}: ends {pct:5.1f}%{mark}  head={head}")
        if pct < args.min_fill:
            flagged.append(n)

    print(f"\n{doc.page_count} pages; flagged: {sorted(set(flagged)) or '-'}")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
