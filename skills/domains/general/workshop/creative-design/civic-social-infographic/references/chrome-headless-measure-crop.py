#!/usr/bin/env python3
"""Measure content bottom of a Chrome headless render, then crop.

Usage:
    python3 chrome-headless-measure-crop.py <input_html> <output_png> [bg_hex]

Default bg_hex matches the proven dark social palette (#07070d). The browser
default-background-color flag must match this.

Mandatory companion: build HTML with body { height:auto; overflow:hidden }.
If you hard-code body height, content clips silently — this script will still
crop, but the image will be missing rows.
"""
import sys
import subprocess
import os
from PIL import Image


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    html = sys.argv[1]
    out_png = sys.argv[2]
    bg_hex = sys.argv[3] if len(sys.argv) > 3 else "07070D"
    bg = tuple(int(bg_hex[i:i+2], 16) for i in (0, 2, 4))

    tmp = "/tmp/_measure_civic.png"
    cmd = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--disable-cache",
        "--window-size=1080,2400",
        f"--default-background-color=FF{bg_hex}",
        f"--screenshot={tmp}",
        f"file://{os.path.abspath(html)}",
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    im = Image.open(tmp).convert("RGB")
    w, h = im.size
    px = im.load()
    last = 0
    for y in range(h - 1, -1, -1):
        for x in range(0, w, 40):
            if (abs(px[x, y][0] - bg[0]) +
                    abs(px[x, y][1] - bg[1]) +
                    abs(px[x, y][2] - bg[2])) > 25:
                last = y
                break
        if last:
            break

    if last == 0:
        print(f"WARNING: no content found above bg {bg}", file=sys.stderr)
        sys.exit(1)

    crop = im.crop((0, 0, w, last + 24))
    crop.save(out_png)
    print(f"content bottom: {last} of {h}")
    print(f"saved {out_png} ({crop.size[0]}x{crop.size[1]}, {os.path.getsize(out_png)} bytes)")


if __name__ == "__main__":
    main()
