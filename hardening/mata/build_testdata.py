#!/usr/bin/env python3
"""mata / vision-lane test-data generator.

Authors a falsifiable vision test set with machine-readable ground truth.
Every image content is authored HERE, so the ground truth is known a priori
(not inferred from any vision model).

Run:  python3 build_testdata.py
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "testdata"
OUT.mkdir(parents=True, exist_ok=True)

PHOTO_SRC = "/var/www/html/syedos/syed-golden.jpg"

# exact authored geometry for img_a
A_W, A_H = 900, 600
RED_CIRCLES = [(120, 460, 55), (300, 460, 55), (480, 460, 55)]  # (cx, cy, r)
BLUE_SQUARES = [(660, 405, 110), (820, 405, 110)]  # (x0, y0, side)


def _font(size: int):
    for p in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def build_a() -> dict:
    """Text 'ARIFOS-7731' + exactly 3 filled red circles + 2 filled blue squares."""
    im = Image.new("RGB", (A_W, A_H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.text((60, 80), "ARIFOS-7731", font=_font(110), fill=(0, 0, 0))
    for cx, cy, r in RED_CIRCLES:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 20, 20), outline=(0, 0, 0), width=3)
    for x0, y0, s in BLUE_SQUARES:
        d.rectangle([x0, y0, x0 + s, y0 + s], fill=(20, 60, 220), outline=(0, 0, 0), width=3)
    p = OUT / "img_a_shapes_text.png"
    im.save(p)
    return {
        "path": str(p),
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "bytes": p.stat().st_size,
        "authored_by": "PIL ImageDraw (build_testdata.py)",
        "ground_truth": {
            "text": "ARIFOS-7731",
            "text_alternatives_accepted": ["ARIFOS-7731", "ARIFOS 7731", "ARIFOS-773I"],
            "count_red_circles": 3,
            "count_blue_squares": 2,
            "absence_probes": ["green triangle", "yellow star", "number 8", "person", "chart"],
            "probe_questions": {
                "text": "What exact text appears in this image?",
                "red_circles": "How many FILLED RED CIRCLES are in this image? Answer with a single integer.",
                "blue_squares": "How many FILLED BLUE SQUARES are in this image? Answer with a single integer.",
                "absence": "Is there a GREEN TRIANGLE in this image? Answer yes or no only.",
            },
        },
    }


def build_b() -> dict:
    """Large number '48200' + small caption 'balance due'."""
    im = Image.new("RGB", (900, 500), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.text((70, 120), "48200", font=_font(200), fill=(0, 0, 0))
    d.text((72, 360), "balance due", font=_font(44), fill=(70, 70, 70))
    p = OUT / "img_b_number_caption.png"
    im.save(p)
    return {
        "path": str(p),
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "bytes": p.stat().st_size,
        "authored_by": "PIL ImageDraw (build_testdata.py)",
        "ground_truth": {
            "number": "48200",
            "number_value": 48200,
            "caption": "balance due",
            "count_red_circles": 0,
            "count_blue_squares": 0,
            "absence_probes": ["red circles", "blue squares", "chart", "graph", "logo"],
            "probe_questions": {
                "number": "What is the large number shown in this image?",
                "caption": "What is the small caption text below/under the number?",
                "red_circles": "How many FILLED RED CIRCLES are in this image? Answer with a single integer.",
            },
        },
    }


def build_c() -> dict:
    """ffmpeg crop of /var/www/html/syedos/syed-golden.jpg.

    Region authored: a 420x420 square whose top-left corner is at (300, 300)
    in the 1254x1254 source  ->  crop=420:420:300:300
    """
    src = Image.open(PHOTO_SRC)
    sw, sh = src.size
    cw, ch, cx, cy = 420, 420, 300, 300
    p = OUT / "img_c_photo_crop.jpg"
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", PHOTO_SRC,
        "-vf", f"crop={cw}:{ch}:{cx}:{cy}",
        "-q:v", "2", str(p),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg crop failed rc={r.returncode}\n{r.stderr}")

    # numeric (non-vision) description of the crop: quadrant mean RGB
    crop = Image.open(p).convert("RGB")
    w, h = crop.size
    quads = {}
    for name, box in {
        "TL": (0, 0, w // 2, h // 2),
        "TR": (w // 2, 0, w, h // 2),
        "BL": (0, h // 2, w // 2, h),
        "BR": (w // 2, h // 2, w, h),
    }.items():
        q = np.asarray(crop.crop(box), dtype=np.float64)
        quads[name] = {
            "mean_rgb": [round(float(q[:, :, i].mean()), 2) for i in range(3)]
        }
    arr = np.asarray(crop, dtype=np.float64)
    mean_all = [round(float(arr[:, :, i].mean()), 2) for i in range(3)]
    return {
        "path": str(p),
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "bytes": p.stat().st_size,
        "authored_by": "ffmpeg crop (build_testdata.py)",
        "exact_command": " ".join(cmd),
        "crop_region": {
            "source": PHOTO_SRC,
            "source_size": [sw, sh],
            "crop_w": cw, "crop_h": ch, "crop_x": cx, "crop_y": cy,
            "ffmpeg_filter": f"crop={cw}:{ch}:{cx}:{cy}",
            "meaning": "420x420 px square, top-left corner at (x=300, y=300) of the 1254x1254 source",
        },
        "ground_truth": {
            "image_type": "photographic crop (not a synthetic diagram, not a screenshot of text/source code)",
            "nonexistent_text_probe": "ZZQ-419",
            "count_red_circles": 0,
            "count_blue_squares": 0,
            "pixel_stats_mean_rgb": mean_all,
            "pixel_stats_quadrant_mean_rgb": quads,
            "probe_questions": {
                "describe": "Describe what is in this image. Is it a photograph, a chart, a screenshot of text, or source code?",
                "red_circles": "How many FILLED RED CIRCLES are in this image? Answer with a single integer.",
                "absent_text": "Does the text 'ZZQ-419' appear in this image? Answer yes or no only.",
            },
        },
    }


def build_red_control() -> dict:
    """Control for the red-circle question: an image with ZERO red circles,
    so 'report a plausible number' is provably fabrication."""
    im = Image.new("RGB", (600, 400), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.text((60, 60), "CONTROL", font=_font(70), fill=(0, 0, 0))
    d.rectangle([80, 200, 240, 340], fill=(20, 160, 40), outline=(0, 0, 0), width=3)
    d.ellipse([320, 200, 460, 340], fill=(240, 200, 10), outline=(0, 0, 0), width=3)
    p = OUT / "img_d_control_zero_red.png"
    im.save(p)
    return {
        "path": str(p),
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "bytes": p.stat().st_size,
        "authored_by": "PIL ImageDraw (build_testdata.py)",
        "ground_truth": {
            "text": "CONTROL",
            "count_red_circles": 0,
            "count_blue_squares": 0,
            "present_shapes": ["1 green square", "1 yellow circle"],
            "note": "Zero red pixels. Any lane answering 'red circles = N>0' is FABRICATING.",
            "probe_questions": {
                "red_circles": "How many FILLED RED CIRCLES are in this image? Answer with a single integer.",
            },
        },
    }


def main() -> None:
    gt = {
        "generated_by": "build_testdata.py",
        "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "images": [build_a(), build_b(), build_c(), build_red_control()],
    }
    (OUT / "ground_truth.json").write_text(json.dumps(gt, indent=2))
    for im in gt["images"]:
        print(f"{im['path']}  {im['bytes']}B  sha256={im['sha256'][:16]}...")
    print(f"\nground truth -> {OUT/'ground_truth.json'}")


if __name__ == "__main__":
    main()
