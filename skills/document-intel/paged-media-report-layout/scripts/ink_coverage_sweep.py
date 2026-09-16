#!/usr/bin/env python3
"""Ink-coverage sweep: detect blank, split, or sparsely-filled pages in a PDF.

The page count tells you how many pages were emitted. This tells you whether
anything is on them. Run it after every layout edit, not just at the end.

Usage:
    python3 ink_coverage_sweep.py report.pdf [--dpi 110] [--threshold 3.0]

Exit code 1 if any page falls below the threshold, so it can gate a pipeline.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile


def sweep(pdf_path, dpi=110, threshold=3.0):
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow not available on this interpreter; probe first with "
                 "`python3 -c 'import PIL'` and pick an interpreter that has it.")

    if not shutil.which("pdftoppm"):
        sys.exit("pdftoppm not found (install poppler-utils)")

    tmp = tempfile.mkdtemp(prefix="ink_sweep_")
    try:
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), pdf_path,
                        os.path.join(tmp, "page")], check=True)
        pages = sorted(glob.glob(os.path.join(tmp, "page-*.png")))
        if not pages:
            sys.exit("no pages rendered - is the file a real PDF?")

        rows, low, high = [], [], []
        for f in pages:
            im = Image.open(f).convert("L")
            w, h = im.size
            px = im.load()
            dark = total = 0
            for y in range(0, h, 3):
                for x in range(0, w, 3):
                    total += 1
                    if px[x, y] < 235:
                        dark += 1
            pct = 100.0 * dark / total
            rows.append((os.path.basename(f), pct))
            if pct < threshold:
                low.append((os.path.basename(f), round(pct, 2)))
            if pct > 60:
                high.append((os.path.basename(f), round(pct, 2)))

        for name, pct in rows:
            flag = "  <-- SPARSE" if pct < threshold else ("  <-- full-bleed" if pct > 60 else "")
            print(f"{name}  {pct:6.2f}%{flag}")

        print(f"\npages: {len(rows)}  min: {min(p for _, p in rows):.2f}%  "
              f"max: {max(p for _, p in rows):.2f}%")
        if low:
            print(f"SPARSE PAGES ({len(low)}): {low}")
            print("  -> usually forced page breaks eating the slack, or a block that "
                  "overflows and splits. Remove forced breaks; add "
                  "page-break-inside: avoid to figures/tables/callouts.")
        if high:
            print(f"FULL-BLEED PAGES ({len(high)}): {high}")
            print("  -> fine on screen; flag if the deliverable is meant to be printed.")
        if not low:
            print("PASS - no sparse pages.")
        return 1 if low else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--threshold", type=float, default=3.0)
    a = ap.parse_args()
    sys.exit(sweep(a.pdf, a.dpi, a.threshold))
