#!/usr/bin/env python3
"""make_honest_bar_chart.py — embeddable honest bar chart PNG.

Per infographic-generation SKILL.md: matplotlib bar chart with y-axis from 0,
peak/dip annotations, and an honest data-label caption. Generates the
embeddable chart PNG used by the propa-vs-reality infographic layout.

Honesty rules enforced here (they are the point of the script):
  * y-axis ALWAYS starts at 0 — no truncated-axis exaggeration
  * peak and dip are annotated explicitly, so the reader's eye is told
    where the extremes are rather than being left to the visual slope
  * the caption states the data label/source verbatim, so the chart cannot
    be lifted out of context without its provenance

Usage:
  python3 make_honest_bar_chart.py \
      --out chart.png \
      --title "Malaysia OPR, 2024-2026 (%)" \
      --caption "Source: BNM MPC statements, read 2026-09-01" \
      --labels 2024 2025 2026 --values 3.00 2.75 2.50

  # or read labels/values from a JSON file:
  python3 make_honest_bar_chart.py --out chart.png --json data.json
  #   data.json: {"title": ..., "caption": ..., "labels": [...], "values": [...]}
"""
import argparse
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def make_chart(labels, values, title, caption, out, ylabel=None,
               figsize=(10, 5.5), dpi=200):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    bars = ax.bar([str(l) for l in labels], values,
                  color="#2b6cb0", edgecolor="#1a365d", linewidth=0.8)

    # HONESTY: y-axis floor is always 0.
    ax.set_ylim(bottom=0)

    # Peak / dip annotation.
    vmax, vmin = max(values), min(values)
    for bar, v in zip(bars, values):
        if v == vmax:
            b, tag, col = bar, "PEAK", "#c53030"
        elif v == vmin:
            b, tag, col = bar, "DIP", "#b7791f"
        else:
            continue
        ax.annotate(f"{tag} {v}",
                    xy=(b.get_x() + b.get_width() / 2, b.get_height()),
                    xytext=(0, 10), textcoords="offset points",
                    ha="center", fontsize=9, fontweight="bold", color=col)
        ax.text(b.get_x() + b.get_width() / 2, 0,
                f"{v}", ha="center", va="bottom", fontsize=8, color="white")

    ax.set_title(title, fontsize=13, fontweight="bold", color="#1a202c")
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linestyle=":")
    ax.set_axisbelow(True)

    # HONESTY: the data label / source travels with the image.
    fig.text(0.5, 0.01, caption, ha="center", fontsize=8,
             color="#4a5568", wrap=True)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--caption", required=True)
    ap.add_argument("--labels", nargs="*", default=[])
    ap.add_argument("--values", nargs="*", type=float, default=[])
    ap.add_argument("--ylabel", default=None)
    ap.add_argument("--json", default=None, help="JSON with title/caption/labels/values")
    args = ap.parse_args()

    title, labels, values = args.title, args.labels, args.values
    if args.json:
        with open(args.json) as fh:
            d = json.load(fh)
        title = d.get("title", title)
        labels = d.get("labels", labels)
        values = d.get("values", values)

    if not labels or len(labels) != len(values):
        raise SystemExit("--labels and --values must be equal length (or supply --json)")

    path = make_chart(labels, values, title, args.caption, args.out,
                      ylabel=args.ylabel)
    print(path)


if __name__ == "__main__":
    main()
