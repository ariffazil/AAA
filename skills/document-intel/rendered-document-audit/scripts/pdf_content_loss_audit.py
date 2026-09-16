#!/usr/bin/env python3
"""Rendered document audit - quantify content loss in an HTML -> PDF render.

Deterministic probe behind the Rendered Document Audit skill.
Answers one question: how much of the source actually reached the page?

Usage:
    python3 pdf_content_loss_audit.py source.html out.pdf
    python3 pdf_content_loss_audit.py source.html out.pdf --slide-regex '<!-- SLIDE'
    python3 pdf_content_loss_audit.py source.html out.pdf --json

Checks:
  1. page count vs slide count in the source
  2. per-page text-layer sweep (flags heading-only and near-empty pages)
  3. content-atom loss: source text vs PDF text layer
  4. renderer furniture leaking onto pages (file:/// paths, print timestamps)
  5. zero-ink pages, via a per-page ink check

Exit status:
  0  clean
  1  content loss or a count mismatch found
  2  a required external tool is missing

Requires: pdfinfo, pdftotext (poppler-utils). PyMuPDF is optional and only
used for the zero-ink check, which is skipped when it is unavailable.
"""

from __future__ import annotations

import argparse
import html as html_mod
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

MIN_ATOM = 18
EMPTY_PAGE_CHARS = 25
HEADING_ONLY_CHARS = 140


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.stdout


def require(tool: str) -> None:
    if shutil.which(tool) is None:
        print(f"ERROR: '{tool}' not found. Install poppler-utils.", file=sys.stderr)
        sys.exit(2)


def page_count(pdf: Path) -> int | None:
    out = run(["pdfinfo", str(pdf)])
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else None


def page_size(pdf: Path) -> str:
    out = run(["pdfinfo", str(pdf)])
    m = re.search(r"^Page size:\s+(.+)$", out, re.M)
    return m.group(1).strip() if m else "unknown"


def full_text(pdf: Path) -> str:
    return run(["pdftotext", "-layout", str(pdf), "-"])


def per_page_text(pdf: Path, n: int) -> list[str]:
    return [
        run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", str(pdf), "-"])
        for i in range(1, n + 1)
    ]


def count_slides(src: str, slide_re: str | None) -> int:
    if slide_re:
        return len(re.findall(slide_re, src))
    patterns = [
        r'class="[^"]*\bslide\b[^"]*"',
        r'class="[^"]*\bpage\b[^"]*"',
        r"class='[^']*\bslide\b[^']*'",
        r"class='[^']*\bpage\b[^']*'",
    ]
    return sum(len(re.findall(p, src)) for p in patterns)


def source_atoms(src: str, slide_re: str | None) -> list[list[str]]:
    """Split the source into per-slide lists of text atoms.

    <svg> blocks are stripped before extracting text: their labels never reach
    the PDF text layer, so counting them as lost would be a permanent false
    positive.
    """
    src = re.sub(r"<style.*?</style>", " ", src, flags=re.S)
    src = re.sub(r"<script.*?</script>", " ", src, flags=re.S)

    if slide_re:
        blocks = re.split(slide_re, src)
        if len(blocks) > 1:
            blocks = blocks[1:]
    else:
        blocks = [src]

    out: list[list[str]] = []
    for block in blocks:
        block = re.sub(r"<svg.*?</svg>", " ", block, flags=re.S)
        block = re.sub(r"<img[^>]*>", " ", block)
        text = re.sub(r"<[^>]+>", " ", block)
        text = re.sub(r"\s+", " ", html_mod.unescape(text)).strip()
        atoms = [
            a.strip()
            for a in re.split(r"(?<=[.:;\u00d7])\s+|(?<=\d)\s(?=[A-Z][a-z]+ )", text)
            if len(a.strip()) >= MIN_ATOM
        ]
        out.append(atoms)
    return out


def atom_loss(source_html: Path, pdf: Path, slide_re: str | None):
    pdf_norm = re.sub(r"\s+", " ", full_text(pdf))
    src = source_html.read_text(encoding="utf-8", errors="replace")
    per_slide = source_atoms(src, slide_re)

    total = lost = 0
    detail = []
    for i, atoms in enumerate(per_slide, 1):
        miss = [a for a in atoms if a[:45] not in pdf_norm and a[-45:] not in pdf_norm]
        total += len(atoms)
        lost += len(miss)
        detail.append(
            {
                "slide": i,
                "atoms": len(atoms),
                "missing": len(miss),
                "examples": [m[:90] for m in miss[:3]],
            }
        )
    pct = (100.0 * lost / total) if total else 0.0
    return total, lost, pct, detail


def furniture(text: str) -> dict:
    return {
        "file_paths": sorted(set(re.findall(r"file:///\S+", text))),
        "timestamps": len(
            re.findall(r"\b\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*[AP]M", text)
        ),
        "page_numbers": len(re.findall(r"\b\d+/\d+\b", text)),
    }


def zero_ink_pages(pdf: Path, n: int, dpi: int = 100) -> list[int]:
    """Return page numbers carrying no ink.

    Uses a low-resolution pixel scan with a tolerance: a full-bleed dark page
    must not be reported as blank merely because it is dark.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return []

    blank: list[int] = []
    try:
        with fitz.open(pdf) as doc:
            for i, page in enumerate(doc, 1):
                pix = page.get_pixmap(dpi=dpi)
                samples = pix.samples
                if not samples:
                    blank.append(i)
                    continue
                if all(b >= 250 for b in samples[::97]):
                    blank.append(i)
    except Exception:
        return []
    return blank


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("source", type=Path, help="source HTML the PDF was rendered from")
    ap.add_argument("pdf", type=Path, help="rendered PDF to audit")
    ap.add_argument("--slide-regex", default=None, help="regex delimiting slides in the source")
    ap.add_argument(
        "--max-loss",
        type=float,
        default=20.0,
        help="fail if atom loss exceeds this percent (default 20)",
    )
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()

    require("pdfinfo")
    require("pdftotext")
    for path in (args.source, args.pdf):
        if not path.exists():
            print(f"ERROR: {path} not found", file=sys.stderr)
            return 1

    pages = page_count(args.pdf) or 0
    slides = count_slides(
        args.source.read_text(encoding="utf-8", errors="replace"), args.slide_regex
    )
    pages_text = per_page_text(args.pdf, pages)
    joined = "\n".join(pages_text)

    heading_only = [
        i
        for i, t in enumerate(pages_text, 1)
        if len(re.sub(r"\s+", "", t)) <= HEADING_ONLY_CHARS
    ]
    empty = [
        i
        for i, t in enumerate(pages_text, 1)
        if len(re.sub(r"\s+", "", t)) <= EMPTY_PAGE_CHARS
    ]
    total, lost, pct, detail = atom_loss(args.source, args.pdf, args.slide_regex)
    furn = furniture(joined)
    blank = zero_ink_pages(args.pdf, pages)

    problems: list[str] = []
    if slides and pages != slides:
        ratio = pages / slides
        problems.append(
            f"page count {pages} != slide count {slides}"
            + (
                f" (ratio {ratio:.2f}x - scale-and-break signature)"
                if 1.5 <= ratio <= 2.5
                else ""
            )
        )
    if pct > args.max_loss:
        problems.append(f"content-atom loss {pct:.0f}% exceeds {args.max_loss:.0f}%")
    if heading_only:
        problems.append(f"heading-only pages: {heading_only[:12]}")
    if furn["file_paths"]:
        problems.append(f"source path leaked onto pages: {furn['file_paths'][:2]}")
    if blank:
        problems.append(f"zero-ink pages: {blank[:12]}")

    if args.json:
        print(
            json.dumps(
                {
                    "pages": pages,
                    "slides": slides,
                    "page_size": page_size(args.pdf),
                    "atom_total": total,
                    "atom_missing": lost,
                    "loss_pct": round(pct, 1),
                    "empty_pages": empty,
                    "heading_only_pages": heading_only,
                    "zero_ink_pages": blank,
                    "furniture": furn,
                    "detail": detail,
                    "problems": problems,
                },
                indent=2,
            )
        )
    else:
        print(f"page size      : {page_size(args.pdf)}")
        print(f"pages / slides : {pages} / {slides}")
        print(f"content atoms  : {total - lost}/{total} present  ({pct:.0f}% lost)")
        if empty:
            print(f"near-empty pg  : {empty[:12]}")
        if blank:
            print(f"zero-ink pg    : {blank[:12]}")
        if furn["file_paths"]:
            print(f"path leaked    : {furn['file_paths'][:2]}")
        print()
        for d in detail:
            if d["missing"]:
                print(f"  slide {d['slide']}: {d['missing']}/{d['atoms']} atoms missing")
                for ex in d["examples"]:
                    print(f"      - {ex}")
        print()
        if problems:
            print("VERDICT: LOSS DETECTED")
            for p in problems:
                print(f"  ! {p}")
            print("\nFix the source HTML, re-render, and re-run this probe.")
        else:
            print("VERDICT: CLEAN")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
