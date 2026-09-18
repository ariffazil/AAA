#!/usr/bin/env python3
"""Render an HTML preview with headless Chrome, then MEASURE what it actually shows.

Why this exists: judging a design by reading its CSS produces confident wrong answers. A
page that "looks dark and dull" is usually a measurement -- near-black covering >90% of the
frame while under 1% carries any colour. Measure first; then read the screenshot with
vision for composition.

Usage:
    python3 render_and_measure.py /abs/preview.html
    python3 render_and_measure.py /abs/preview.html --sizes 430x2200,1440x1250
    python3 render_and_measure.py /abs/preview.html --check clock,longdate,pct
    python3 render_and_measure.py /abs/preview.html --ground '#08080A' \\
        --ink '#F4F1EE=ink' --ink '#867D78=ink-3' --ink '#D4AF37=gold'

Writes PNGs beside the input file and prints a report on stdout.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys
from collections import Counter

CHROME_CANDIDATES = (
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
    "/opt/google/chrome/chrome",
)


def find_chrome(explicit=None):
    if explicit:
        return explicit
    for path in CHROME_CANDIDATES:
        if pathlib.Path(path).exists():
            return path
    found = shutil.which("google-chrome") or shutil.which("chromium")
    if found:
        return found
    sys.exit("no Chrome/Chromium binary found; pass --chrome /path/to/chrome")


def parse_sizes(raw):
    sizes = []
    for item in raw.split(","):
        w, _, h = item.strip().partition("x")
        sizes.append((int(w), int(h)))
    return sizes


def render(chrome, src, out, w, h, budget=5000):
    subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
         "--force-device-scale-factor=1", f"--window-size={w},{h}",
         f"--virtual-time-budget={budget}", f"--user-data-dir=/tmp/chr-{out.stem}",
         f"--screenshot={out}", f"file://{src}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180, check=False,
    )
    return out.exists() and out.stat().st_size > 0


def rel_lum(hex_colour):
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]

    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (lin(c) for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def measure(png):
    """Pixel composition of a rendered frame."""
    from PIL import Image

    im = Image.open(png).convert("RGB")
    w, h = im.size
    small = im.resize((max(1, w // 3), max(1, h // 3)))
    pixels = list(small.getdata())
    n = len(pixels)

    near_black = sum(1 for r, g, b in pixels if r < 40 and g < 40 and b < 40)
    warm = sum(1 for r, g, b in pixels if r > b + 25 and r > 80)
    cool = sum(1 for r, g, b in pixels if b > r + 20)

    # bucket to 8 levels per channel so anti-aliasing does not flood the palette
    buckets = Counter((r // 8 * 8, g // 8 * 8, b // 8 * 8) for r, g, b in pixels)

    return {
        "size": (w, h),
        "n": n,
        "corner": im.getpixel((4, 4)),
        "edge": im.getpixel((4, h // 2)),
        "near_black_pct": 100 * near_black / n,
        "warm_pct": 100 * warm / n,
        "cool_pct": 100 * cool / n,
        "palette": buckets.most_common(6),
    }


def element_text(dom, element_id):
    """Text of an element as rendered, including elements with nested tags.

    A naive `id="x"[^>]*>(.*?)</` stops at the FIRST `</`, so any element that
    contains a child tag reports truncated text -- a clock built as
    `09<span>:</span>51` reads back as `09:`, and the check that is supposed to
    prove the JS ran cannot tell a ticking clock from a frozen one. Walk to the
    matching close tag of the same element instead.
    """
    m = re.search(r'<(\w+)[^>]*\bid="%s"' % re.escape(element_id), dom)
    if not m:
        return "MISSING"
    tag = m.group(1)
    gt = dom.find(">", m.end())
    if gt == -1:
        return "MISSING"
    start, depth, i = gt + 1, 1, gt + 1
    pattern = re.compile(r"</?%s\b" % re.escape(tag), re.I)
    while depth > 0:
        nxt = pattern.search(dom, i)
        if not nxt:
            break
        if dom[nxt.start():nxt.start() + 2] == "</":
            depth -= 1
            if depth == 0:
                return re.sub(r"<[^>]+>", "", dom[start:nxt.start()]).strip()
        else:
            depth += 1
        i = nxt.end()
    return re.sub(r"<[^>]+>", "", dom[start:start + 400]).strip()


def dump_dom(chrome, src, ids):
    """Return the text of each id as the browser rendered it -- proves the JS ran."""
    dom = subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--user-data-dir=/tmp/chr-dom-check", "--virtual-time-budget=4500",
         "--dump-dom", f"file://{src}"],
        capture_output=True, text=True, timeout=180, check=False,
    ).stdout
    return {element_id: element_text(dom, element_id) for element_id in ids}


def main():
    ap = argparse.ArgumentParser(
        description="Render an HTML preview and measure what it shows.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=pathlib.Path)
    ap.add_argument("--sizes", default="430x2200,1440x1250")
    ap.add_argument("--outdir", type=pathlib.Path)
    ap.add_argument("--prefix", default="shot")
    ap.add_argument("--chrome")
    ap.add_argument("--ground", default="#08080A")
    ap.add_argument("--ink", action="append", default=[], metavar="#RRGGBB=label")
    ap.add_argument("--check", default="", help="comma-separated ids whose JS text to verify")
    args = ap.parse_args()

    src = args.html.resolve()
    if not src.exists():
        sys.exit(f"not found: {src}")
    outdir = (args.outdir or src.parent).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome(args.chrome)
    sizes = parse_sizes(args.sizes)

    print(f"chrome : {chrome}")
    print(f"source : {src}  ({src.stat().st_size} bytes)")

    print("\n--- render")
    for w, h in sizes:
        out = outdir / f"{args.prefix}-{w}.png"
        if render(chrome, src, out, w, h):
            print(f"  {w}x{h} -> {out.name}  {out.stat().st_size} bytes")
        else:
            print(f"  {w}x{h} FAILED")

    print("\n--- pixels")
    for w, _ in sizes:
        png = outdir / f"{args.prefix}-{w}.png"
        if not png.exists():
            continue
        m = measure(png)
        total_colour = m["warm_pct"] + m["cool_pct"]
        print(f"\n  {png.name}  {m['size'][0]}x{m['size'][1]}")
        print(f"    corner {m['corner']}   edge {m['edge']}")
        print(f"    near-black {m['near_black_pct']:5.1f}%   "
              f"warm {m['warm_pct']:4.1f}%   cool {m['cool_pct']:4.1f}%")
        print(f"    colour total {total_colour:5.1f}%")
        if total_colour < 1.0:
            print("    WARNING: under 1% of the frame carries colour --"
                  " this will read as an empty page")
        print("    palette: " + "  ".join(
            "#%02x%02x%02x %.0f%%" % (r, g, b, 100 * c / m["n"])
            for (r, g, b), c in m["palette"]))

    if args.ink:
        print(f"\n--- contrast against {args.ground}")
        for spec in args.ink:
            value, _, label = spec.partition("=")
            r = contrast(value, args.ground)
            verdict = "AA text" if r >= 4.5 else ("AA large only" if r >= 3 else "field only")
            print(f"  {(label or value):<14} {value:<9} {r:5.2f}:1   {verdict}")

    if args.check:
        print("\n--- did the JS write its values?")
        for element_id, value in dump_dom(chrome, src, args.check.split(",")).items():
            print(f"  {element_id:<14}: {value}")


if __name__ == "__main__":
    main()
