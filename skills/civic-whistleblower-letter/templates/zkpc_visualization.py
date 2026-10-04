#!/usr/bin/env python3
"""
ZKPC Visual Generator - Zero-Knowledge Proof of Contribution
=============================================================
Generates a cryptographic witness seal for civic whistleblower letters.
SHA-256 per data row + Merkle root, with anonymous authorship.

Usage:
    python3 zkpc_visualization.py --title "..." --subtitle "..." --rows '[{"label":"FY2024","value":"PAT RM55.1B","hash":"abc123..."}, ...]' --out seal.png
"""
import hashlib
import json
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# === MAKCICKGPT-COMPATIBLE PALETTE ===
BG = "#0a0e1a"
PANEL = "#141a2e"
NAVY = "#0e1a2b"
GOLD = "#c9a227"
CREAM = "#f4ecd8"
RED = "#c1272d"
BLUE = "#1e3a8a"
YELLOW = "#fcd34d"
GREEN = "#10b981"
MUTED = "#6b7280"


def sha256_of_dict(d):
    """Deterministic SHA-256 of a dict's sorted JSON."""
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()


def merkle_root_from_hashes(hashes):
    """Compute Merkle root from a list of hex hash strings."""
    if not hashes:
        return ""
    concat = "".join(hashes)
    return hashlib.sha256(concat.encode()).hexdigest()


def generate_zkpc_seal(title, subtitle, rows, attestation, output_path):
    """Generate the ZKPC seal visualization.

    rows: list of dicts with keys: label, value, hash, color (optional)
    attestation: short text at the bottom
    """
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "text.color": CREAM,
        "axes.labelcolor": CREAM,
        "axes.edgecolor": CREAM,
        "xtick.color": CREAM,
        "ytick.color": CREAM,
    })

    fig, ax = plt.subplots(figsize=(14, 10), dpi=180)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")

    # Title
    fig.text(0.5, 0.96, title, ha="center", fontsize=24, fontweight="bold", color=GOLD)
    fig.text(0.5, 0.93, "ZKPC -- Zero-Knowledge Proof of Contribution", ha="center", fontsize=11, color=CREAM, style="italic")
    fig.text(0.5, 0.91, subtitle, ha="center", fontsize=11, color=CREAM, style="italic", wrap=True)

    # Row layout
    n_rows = len(rows)
    box_y_start = 0.78
    box_h = 0.08
    box_w = 0.85
    box_x = 0.075

    for i, row in enumerate(rows):
        y = box_y_start - i * (box_h + 0.018)
        color = row.get("color", GREEN)
        box = FancyBboxPatch(
            (box_x, y), box_w, box_h, transform=fig.transFigure,
            boxstyle="round,pad=0.005", facecolor=PANEL, edgecolor=color, linewidth=1.5
        )
        fig.patches.append(box)

        fig.text(box_x + 0.02, y + box_h / 2, row["label"], fontsize=11, fontweight="bold", color=color, va="center", transform=fig.transFigure)
        fig.text(box_x + 0.18, y + box_h / 2, row["value"], fontsize=9, color=CREAM, va="center", transform=fig.transFigure)
        fig.text(box_x + 0.55, y + box_h / 2, f"sha256:{row['hash']}...", fontsize=8, color=MUTED, family="monospace", va="center", transform=fig.transFigure)

    # Merkle root
    line_y_end = box_y_start - (n_rows - 1) * (box_h + 0.018) - 0.05
    ax.plot([0.5, 0.5], [line_y_end + 0.18, line_y_end + 0.08], transform=fig.transFigure, color=GOLD, linewidth=2, linestyle="-")

    root_hash = merkle_root_from_hashes([r["hash"] for r in rows])
    mroot = FancyBboxPatch((0.20, line_y_end - 0.02), 0.60, 0.06, transform=fig.transFigure,
                            boxstyle="round,pad=0.005", facecolor=NAVY, edgecolor=GOLD, linewidth=3)
    fig.patches.append(mroot)
    fig.text(0.5, line_y_end + 0.01, f"MERKLE ROOT: sha256:{root_hash}",
             ha="center", va="center", fontsize=10, color=GOLD, family="monospace", fontweight="bold", transform=fig.transFigure)

    # Attestation
    fig.text(0.5, 0.04, "Saksi Tanpa Nama . Bukti Tanpa Pemalsuan",
             ha="center", fontsize=12, color=GOLD, fontweight="bold", style="italic")
    fig.text(0.5, 0.02, attestation,
             ha="center", fontsize=9, color=CREAM, wrap=True)
    fig.text(0.5, 0.005, "DITEMPA BUKAN DIBERI",
             ha="center", fontsize=8, color=MUTED)

    plt.savefig(output_path, facecolor=BG, dpi=180, bbox_inches="tight")
    plt.close()
    return root_hash


def generate_from_data(data_points, title, subtitle, attestation, output_path, row_color_field=None):
    """Higher-level helper: take a list of dicts with (label, value, hash) and produce the seal."""
    rows = []
    for dp in data_points:
        color = dp.get(row_color_field, GREEN) if row_color_field else GREEN
        rows.append({
            "label": dp["label"],
            "value": dp["value"],
            "hash": dp["hash"],
            "color": color,
        })
    return generate_zkpc_seal(title, subtitle, rows, attestation, output_path)


# === ADAPTIVE PREDATOR VISUAL ===
def generate_adaptive_predator(years, pat_values, dividend_values, output_path, highlight_idx=None):
    """Two-bar chart showing constant dividend vs falling PAT."""
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "text.color": CREAM,
        "axes.labelcolor": CREAM,
        "axes.edgecolor": CREAM,
        "xtick.color": CREAM,
        "ytick.color": CREAM,
    })

    fig, ax = plt.subplots(figsize=(14, 8), dpi=180)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    fig.text(0.5, 0.95, "PREDATOR YANG BIJAK", ha="center", fontsize=28, fontweight="bold", color=GOLD)
    fig.text(0.5, 0.91, "Dividen tidak pernah turun. Keuntungan selalu boleh turun.",
             ha="center", fontsize=14, color=CREAM, style="italic")

    x = np.arange(len(years))
    width = 0.35

    bars1 = ax.bar(x - width / 2, pat_values, width, color=BLUE, edgecolor=CREAM, linewidth=1.5, label="Keuntungan (PAT)")
    bars2 = ax.bar(x + width / 2, dividend_values, width, color=RED, edgecolor=CREAM, linewidth=1.5, label="Dividen diambil")

    for i, (p, d) in enumerate(zip(pat_values, dividend_values)):
        ax.text(i - width / 2, p + 2, f"RM{p}B", ha="center", va="bottom", fontsize=10, color=BLUE, fontweight="bold")
        ax.text(i + width / 2, d + 2, f"RM{d}B", ha="center", va="bottom", fontsize=10, color=RED, fontweight="bold")

    if highlight_idx is not None:
        ax.axvspan(highlight_idx - 0.5, highlight_idx + 0.5, alpha=0.15, color=YELLOW, zorder=0)
        extraction = round((dividend_values[highlight_idx] / pat_values[highlight_idx]) * 100, 1)
        ax.text(highlight_idx, max(pat_values) * 0.95, f"{extraction}%\nekstraksi", ha="center", va="top",
                fontsize=18, fontweight="bold", color=YELLOW,
                bbox=dict(boxstyle="round,pad=0.4", facecolor=BG, edgecolor=YELLOW, linewidth=2))

    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=12)
    ax.set_ylabel("RM (bilion)", fontsize=12, color=CREAM)
    ax.set_ylim(0, max(pat_values) * 1.15)
    ax.legend(loc="upper left", fontsize=11, facecolor=PANEL, edgecolor=GOLD, labelcolor=CREAM)
    ax.grid(axis="y", alpha=0.2, linestyle="--", color=CREAM)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.text(0.5, 0.02, "Bukti: Dividen tidak turun. Yang turun ialah kemampuan menampungnya.",
             ha="center", fontsize=10, color=CREAM, style="italic")

    plt.savefig(output_path, facecolor=BG, dpi=180, bbox_inches="tight")
    plt.close()


# === THREE HANDS VISUAL ===
def generate_three_hands(hands, output_path):
    """Three Hands institutional accountability visualization.

    hands: list of 3 dicts with keys: office, name, title, role, extract, color
    """
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "text.color": CREAM,
    })

    fig, ax = plt.subplots(figsize=(14, 9), dpi=180)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    fig.text(0.5, 0.95, "TIGA TANGAN YANG MENYAUK", ha="center", fontsize=28, fontweight="bold", color=GOLD)
    fig.text(0.5, 0.91, "Tiga institusi. Tiga manusia. Satu sumber.", ha="center", fontsize=13, color=CREAM, style="italic")

    box_y = 0.08
    box_h = 0.78
    for h in hands:
        box = FancyBboxPatch(
            (h["x"], box_y), h["w"], box_h, transform=fig.transFigure,
            boxstyle="round,pad=0.005", facecolor=PANEL, edgecolor=h["color"], linewidth=3
        )
        fig.patches.append(box)

        fig.text(h["x"] + h["w"] / 2, box_y + box_h - 0.04, h["office"], ha="center", va="top",
                fontsize=9, fontweight="bold", color=h["color"], transform=fig.transFigure)
        fig.text(h["x"] + h["w"] / 2, box_y + box_h - 0.10, h["name"], ha="center", va="top",
                fontsize=14, fontweight="bold", color=CREAM, transform=fig.transFigure)
        fig.text(h["x"] + h["w"] / 2, box_y + box_h - 0.15, h["title"], ha="center", va="top",
                fontsize=9, color=MUTED, style="italic", transform=fig.transFigure)

        div = Rectangle(
            (h["x"] + 0.02, box_y + box_h - 0.19), h["w"] - 0.04, 0.001,
            transform=fig.transFigure, facecolor=h["color"], alpha=0.5
        )
        fig.patches.append(div)

        fig.text(h["x"] + h["w"] / 2, box_y + box_h - 0.23, "PERANAN", ha="center", va="top",
                fontsize=8, fontweight="bold", color=h["color"], transform=fig.transFigure)
        fig.text(h["x"] + h["w"] / 2, box_y + box_h - 0.27, h["role"], ha="center", va="top",
                fontsize=9, color=CREAM, wrap=True, transform=fig.transFigure)

        fig.text(h["x"] + h["w"] / 2, box_y + box_h - 0.45, "YANG DILAKUKAN", ha="center", va="top",
                fontsize=8, fontweight="bold", color=h["color"], transform=fig.transFigure)
        act_box = FancyBboxPatch(
            (h["x"] + 0.02, box_y + 0.18), h["w"] - 0.04, 0.15, transform=fig.transFigure,
            boxstyle="round,pad=0.005", facecolor=BG, edgecolor=h["color"], linewidth=1.5
        )
        fig.patches.append(act_box)
        fig.text(h["x"] + h["w"] / 2, box_y + 0.255, h["extract"], ha="center", va="center",
                fontsize=10, fontweight="bold", color=h["color"], wrap=True, transform=fig.transFigure)

    fig.text(0.5, 0.03, "Identiti disebut untuk akauntabiliti F11 (AUDITABILITY) -- bukan serangan peribadi",
             ha="center", fontsize=9, color=MUTED, style="italic")

    plt.savefig(output_path, facecolor=BG, dpi=180, bbox_inches="tight")
    plt.close()


# === CLI ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate ZKPC seal for civic whistleblower letter")
    parser.add_argument("--title", default="METERAI SAKSI TANPA NAMA")
    parser.add_argument("--subtitle", default="Bukti: Setiap angka disahkan dari laporan awam. Pengarang: tidak dinamakan.")
    parser.add_argument("--rows", help="JSON list of {label, value, hash, color?}")
    parser.add_argument("--attestation", default="Sesiapa boleh menyemak setiap angka dalam laporan tahunan PETRONAS (KPMG audited).")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    rows = json.loads(args.rows) if args.rows else [
        {"label": "FY2024", "value": "PAT RM55.1B / Div RM32.0B", "hash": "171ccfa8fb38ade7", "color": GREEN},
        {"label": "FY2025", "value": "PAT RM45.4B / Div RM32.0B", "hash": "29e0343b0eb8cf60", "color": RED},
    ]
    root = generate_zkpc_seal(args.title, args.subtitle, rows, args.attestation, args.out)
    print(f"Generated: {args.out}")
    print(f"Merkle root: {root}")