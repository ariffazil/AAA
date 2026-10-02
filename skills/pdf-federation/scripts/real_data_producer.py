#!/usr/bin/env python3
"""
real_data_producer.py — P5 closure.

Renders a REAL well-log figure from the Volve 15/9-19 LAS file (Equinor open
dataset, present on this host). This is a READ + render — it does NOT mutate
GEOX state, so it runs within OBSERVE_ONLY authority.

The figure is truth_class=OBSERVATION because the source is a real measured
dataset. The ingest-into-GEOX path (a write) is separately SOVEREIGN_HOLD.

Usage:
    python3 real_data_producer.py --out /path/out_dir
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from datetime import datetime, timezone

# Real measured dataset on this host (Equinor Volve field, open licence).
REAL_LAS = "/root/GEOX/data/real_wells/q15_15_9_19/q15_15_9_19.las"
SYNTHETIC_LAS = "/root/GEOX/fixtures/_DEMO_SYNTHETIC/DEMO_WELL_A_SANDAKAN.las"


def sha256_file(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def render_real_welllog(las_path: str, out_png: str) -> dict:
    import lasio, numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    las = lasio.read(las_path)
    depth = las.index
    curves = {c.mnemonic: c.data.astype(float) for c in las.curves}
    # apply NULL masking
    for k in curves:
        curves[k] = np.where(curves[k] <= -999.0, np.nan, curves[k])

    tracks = [("GR", "GR (API)", "#2d6a4f"),
              ("DEN", "DEN (g/cc)", "#c0392b"),
              ("NEU", "NEU (v/v)", "#2980b9"),
              ("AC", "AC (us/ft)", "#8e44ad"),
              ("RDEP", "RDEP (ohm.m)", "#e67e22")]
    present = [(m, lab, c) for (m, lab, c) in tracks if m in curves]

    # Add petrophysical interpretation tracks (real computed curves in the LAS)
    interp = [("VSHALE", "VSHALE (v/v)", "#7f8c8d"),
              ("SW", "SW (v/v)", "#16a085"),
              ("PHI_DN", "PHI_DN (v/v)", "#d35400")]
    present += [(m, lab, c) for (m, lab, c) in interp if m in curves]

    fig, axes = plt.subplots(1, max(len(present), 1), figsize=(11.5, 8), sharey=True)
    if len(present) == 1:
        axes = [axes]
    for ax, (mn, lab, col) in zip(axes, present):
        ax.plot(curves[mn], depth, color=col, lw=0.7)
        ax.set_xlabel(lab, fontsize=8)
        ax.invert_yaxis()   # depth increases downward
        ax.grid(alpha=0.3, lw=0.4)
        ax.tick_params(labelsize=7)
    fig.suptitle(f"Well {las.well.WELL.value} — real measured log ({os.path.basename(las_path)})",
                 fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(out_png, dpi=130)
    plt.close(fig)

    return {
        "well": las.well.WELL.value,
        "start_m": float(las.well.STRT.value),
        "stop_m": float(las.well.STOP.value),
        "step_m": float(las.well.STEP.value),
        "depth_samples": int(len(depth)),
        "curves": sorted(curves.keys()),
        "tracks_rendered": [m for (m, _, _) in present],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/root/.hermes/cache/scratch/mission")
    ap.add_argument("--las", default=REAL_LAS)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    src_sha = sha256_file(args.las)
    out_png = os.path.join(args.out, "fig_welllog_real.png")
    meta = render_real_welllog(args.las, out_png)
    png_sha = sha256_file(out_png)

    receipt = {
        "figure_id": "fig-welllog-real",
        "type": "well_log",
        "truth_class": "OBSERVATION",
        "claim_state": "ACTIVE",
        "source_path": args.las,
        "source_sha256": src_sha,
        "render_hash": png_sha,
        "data_hash": src_sha,   # data == the LAS bytes; hashes are the same object here
        "renderer_name": "matplotlib well-log tracks",
        "mime_type": "image/png",
        "width": 1495, "height": 1040,
        "alt_text": f"Well {meta['well']} GR/RHOB/NPHI/DT/RES log tracks vs depth",
        "domain_metadata": {
            "well": meta["well"],
            "depth_reference": "MD",
            "units": "m",
            "curves": meta["curves"],
            "tracks": meta["tracks_rendered"],
            "depth_start_m": meta["start_m"],
            "depth_stop_m": meta["stop_m"],
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provenance": {
            "dataset": "Equinor Volve field, open data licence",
            "ingest_authority": "OBSERVE_ONLY (read + render; no GEOX state mutation)",
        },
    }
    rpath = os.path.join(args.out, "fig_welllog_real.receipt.json")
    json.dump(receipt, open(rpath, "w"), indent=2)
    print(json.dumps(receipt, indent=2)[:1200])
    print(f"\n[out] {out_png}")
    print(f"[receipt] {rpath}")


if __name__ == "__main__":
    main()
