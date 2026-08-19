#!/usr/bin/env python3
"""
Sovereign Sound Stabilizer — i-ARIF DECODE acoustic envelope lock.
===================================================================
Implements SYSTEM_HERMES_ALIGNMENT.md sealed spec (2026-08-19):
  - F0 lock: median F0 -> 239 Hz (band 225-255)
  - Terminal pitch lift: +35 Hz at clause boundaries (log-normal tail)
  - Glottal coda truncation: amplitude dampen on final 40ms of utterance-final voiced region
  - Stress-timed amplitude: +/- dynamic range emphasis preserved from source

Method: WORLD vocoder (pyworld) -> DIO/StoneMask F0 extraction ->
per-utterance median-normalized F0 rescale -> optional terminal lift ->
synthesis. Formants (sp) preserved as-is unless formant_warp is set.

Why not the naive numpy/scipy draft:
  - signal * sin(phase_mod) replaces speech with a pure tone (destroys identity)
  - butter bandpass 300-3400Hz removes glottal source and high formants
  - WORLD decomposition separates source (f0) from filter (sp, ap) correctly.

Usage:
  python3 sovereign_sound_stabilizer.py in.mp3 out.wav [--target-f0 239] [--lift 35] [--coda-damp]
"""
import sys, subprocess, argparse
import numpy as np
import pyworld as pw

SR = 16000

def load_pcm(path):
    raw = path + ".f64.raw"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path,
                    "-ar", str(SR), "-ac", "1", "-f", "f64le", raw], check=True)
    x = np.fromfile(raw, dtype=np.float64)
    import os; os.remove(raw)
    return x

def save_wav(path, y):
    y = np.clip(y, -1.0, 1.0)
    tmp = path + ".f64.raw"
    y.astype(np.float64).tofile(tmp)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f64le", "-ar", str(SR),
                    "-ac", "1", "-i", tmp, "-c:a", "pcm_s16le", path], check=True)
    import os; os.remove(tmp)

def stabilize(x, target_f0=239.0, lift_hz=35.0, coda_damp=True, f0_floor=60, f0_ceil=500):
    f0, t = pw.dio(x, SR, f0_floor=f0_floor, f0_ceil=f0_ceil, frame_period=5.0)
    f0 = pw.stonemask(x, f0, t, SR)
    sp = pw.cheaptrick(x, f0, t, SR)
    ap = pw.d4c(x, f0, t, SR)

    voiced = f0 > f0_floor
    if voiced.sum() < 10:
        raise ValueError("no voiced frames — not speech?")

    # 1. F0 lock: rescale voiced frames so MEDIAN lands on target_f0.
    med = np.median(f0[voiced])
    ratio = target_f0 / med
    f0_new = f0.copy()
    f0_new[voiced] = f0[voiced] * ratio

    # 2. Terminal pitch lift (northern cadence): last ~450ms of voiced speech,
    #    log-normal shaped rise peaking at +lift_hz at the very end.
    v_idx = np.where(voiced)[0]
    if len(v_idx) > 20:
        last = v_idx[-1]
        span = min(len(f0_new) // 3, 90)  # ~450ms at 5ms frames
        start = last - span
        if start > v_idx[0]:
            s = np.arange(span) / span
            # log-normal-ish: slow build, steep finish
            shape = np.exp(-((np.log(s + 0.08) + 1.2) ** 2) / 1.8)
            shape = shape / shape.max()
            f0_new[start:last] += lift_hz * shape

    # 3. Glottal coda truncation: hard amplitude cut on final 40ms voiced tail
    y = pw.synthesize(f0_new, sp, ap, SR, frame_period=5.0)
    if coda_damp:
        n_cut = int(0.04 * SR)
        if len(y) > n_cut * 2:
            ramp = np.linspace(1.0, 0.0, n_cut) ** 2
            y[-n_cut:] *= ramp

    return y, dict(med_src=round(float(med), 1), ratio=round(float(ratio), 4),
                   target=target_f0, lift=lift_hz)

def measure_f0(path_or_x):
    x = load_pcm(path_or_x) if isinstance(path_or_x, str) else path_or_x
    f0, t = pw.dio(x, SR, f0_floor=60, f0_ceil=500)
    f0 = pw.stonemask(x, f0, t, SR)
    v = f0[f0 > 60]
    return round(float(np.median(v)), 1), round(float(np.percentile(v, 10)), 1), round(float(np.percentile(v, 90)), 1)

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("src"); a.add_argument("dst")
    a.add_argument("--target-f0", type=float, default=239.0)
    a.add_argument("--lift", type=float, default=35.0)
    a.add_argument("--no-coda", action="store_true")
    args = a.parse_args()

    x = load_pcm(args.src)
    y, meta = stabilize(x, args.target_f0, args.lift, coda_damp=not args.no_coda)
    save_wav(args.dst, y)
    med, p10, p90 = measure_f0(args.dst)
    meta.update(out_median=med, out_p10=p10, out_p90=p90, in_band=225 <= med <= 255)
    print(meta)
