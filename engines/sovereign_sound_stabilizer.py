#!/usr/bin/env python3
"""
Sovereign Sound Stabilizer — i-ARIF DECODE acoustic envelope lock.
===================================================================
CPU-only. No GPU. WORLD vocoder (pyworld) — source (f0) / filter (sp) / aperiodicity (ap).

Jiwa Siti Nurhaliza is NOT a prompt adjective here. It is a constraint
on the analytic signal z(t) = A(t) exp(j φ(t)), f(t) = (1/2π) dφ/dt.

    A(t)  amplitude  — unhurried. Silence (breath) is structure, never filled.
    f(t)  frequency  — still. Median lock 239 Hz, jitter compressed, terminal lift.
    φ(t)  phase      — intact. WORLD keeps source-filter split; coda is ending adab.

Fourier is the measurement, not a metaphor:
    STFT centroid std is OBS. If extras inflate it, extras revert (fail-open).
    Naive phase-mod / brickwall bandpass DESTROYS identity. Do not reintroduce.

Order (scar 2026-08-19): formant warp on sp FIRST, then F0 lock.
F0-then-formant leaked ~20 Hz into the pitch track.

F9: no Siti waveform. F10: physics, not meaning. F1: extras fail-open.

Usage:
  python3 dsp_stabilizer.py in.mp3 out.wav [--target-f0 239] [--lift 35] [--no-coda]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

import numpy as np
import pyworld as pw

SR = 16000
FRAME_MS = 5.0
F0_FLOOR = 60.0
F0_CEIL = 500.0
BAND = (225.0, 255.0)
TARGET_F1 = 750.0
FORMANT_CAP = (0.92, 1.08)  # ±8% — wider warps add artifact, not character
JITTER_CV_MAX = 0.14  # stillness, not monotone
CENTROID_INFLATE_MAX = 1.35


def load_pcm(path: str) -> np.ndarray:
    raw = path + ".f64.raw"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", path, "-ar", str(SR), "-ac", "1", "-f", "f64le", raw],
        check=True,
    )
    x = np.fromfile(raw, dtype=np.float64)
    os.remove(raw)
    return x


def save_wav(path: str, y: np.ndarray) -> None:
    y = np.clip(y, -1.0, 1.0)
    tmp = path + ".f64.raw"
    y.astype(np.float64).tofile(tmp)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "f64le", "-ar", str(SR), "-ac", "1", "-i", tmp,
            "-c:a", "pcm_s16le", path,
        ],
        check=True,
    )
    os.remove(tmp)


def _stft_centroid_stats(x: np.ndarray, n_fft: int = 1024, hop: int = 256) -> tuple[float, float]:
    """OBS: spectral centroid mean/std via real FFT. No librosa (segfault-prone here)."""
    if len(x) < n_fft:
        return 0.0, 0.0
    w = np.hanning(n_fft)
    freqs = np.fft.rfftfreq(n_fft, 1.0 / SR)
    cents = []
    for i in range(0, len(x) - n_fft, hop):
        mag = np.abs(np.fft.rfft(x[i : i + n_fft] * w))
        s = mag.sum()
        if s < 1e-9:
            continue
        cents.append(float((freqs * mag).sum() / s))
    if len(cents) < 4:
        return 0.0, 0.0
    arr = np.asarray(cents, dtype=np.float64)
    return float(arr.mean()), float(arr.std())


def _estimate_f1_hz(sp: np.ndarray) -> float | None:
    """Peak of mean cheaptrick envelope in the F1 band. OBS, not a singer formant table."""
    n_bins = sp.shape[1]
    freqs = np.linspace(0.0, SR / 2.0, n_bins)
    env = np.mean(sp, axis=0)
    mask = (freqs >= 250.0) & (freqs <= 950.0)
    if not np.any(mask):
        return None
    peak = float(freqs[mask][int(np.argmax(env[mask]))])
    # Band-edge peaks are window artifacts, not F1. Skip warp (F2).
    if peak <= 270.0 or peak >= 930.0:
        return None
    return peak


def _warp_sp(sp: np.ndarray, shift: float) -> np.ndarray:
    """Frequency-axis interpolate of WORLD spectral envelope. y(f) = x(f/shift)."""
    if abs(shift - 1.0) < 0.005:
        return sp
    n_bins = sp.shape[1]
    freqs = np.linspace(0.0, SR / 2.0, n_bins)
    src = np.clip(freqs / shift, 0.0, SR / 2.0)
    out = np.empty_like(sp)
    for i in range(sp.shape[0]):
        out[i] = np.interp(freqs, src, sp[i])
    return out


def _clamp_jitter(f0: np.ndarray, voiced: np.ndarray) -> tuple[np.ndarray, float, bool]:
    """Compress F0 deviations toward median if CV too high. Stillness, not flatline."""
    v = f0[voiced]
    med = float(np.median(v))
    if med <= 0 or v.size < 8:
        return f0, 0.0, False
    cv = float(np.std(v) / med)
    if cv <= JITTER_CV_MAX:
        return f0, cv, False
    gain = JITTER_CV_MAX / cv
    out = f0.copy()
    out[voiced] = med + (v - med) * gain
    return out, cv, True


def _amplitude_stillness(y: np.ndarray) -> tuple[np.ndarray, dict]:
    """
    Hilbert envelope A(t) = |analytic(y)|.
    Smooth A on voiced energy. Restore silence frames exactly (breath is structure).
    Fail-soft: gain clipped so we never punch or hollow the take.
    """
    from scipy.signal import hilbert

    z = hilbert(y)
    A = np.abs(z)
    amax = float(A.max()) if A.size else 0.0
    if amax < 1e-8:
        return y, {"silence_frac": 1.0, "amp_applied": False}
    silence = A < (0.02 * amax)
    win = max(3, int(SR * 0.025))
    kernel = np.ones(win, dtype=np.float64) / win
    A_s = np.convolve(A, kernel, mode="same")
    A_s[silence] = A[silence]
    gain = np.ones_like(A)
    nz = A > 1e-8
    gain[nz] = A_s[nz] / A[nz]
    gain = np.clip(gain, 0.65, 1.35)
    return y * gain, {"silence_frac": float(silence.mean()), "amp_applied": True}


def stabilize(
    x: np.ndarray,
    target_f0: float = 239.0,
    lift_hz: float = 35.0,
    coda_damp: bool = True,
    f0_floor: float = F0_FLOOR,
    f0_ceil: float = F0_CEIL,
) -> tuple[np.ndarray, dict]:
    c_mean_in, c_std_in = _stft_centroid_stats(x)

    f0, t = pw.dio(x, SR, f0_floor=f0_floor, f0_ceil=f0_ceil, frame_period=FRAME_MS)
    f0 = pw.stonemask(x, f0, t, SR)
    sp = pw.cheaptrick(x, f0, t, SR)
    ap = pw.d4c(x, f0, t, SR)

    voiced = f0 > f0_floor
    if voiced.sum() < 10:
        raise ValueError("no voiced frames — not speech?")

    # 0. Formant warp on FILTER first (order scar). Cap ±8%.
    f1_native = _estimate_f1_hz(sp)
    formant_shift = 1.0
    formant_applied = False
    if f1_native and f1_native > 0:
        formant_shift = float(np.clip(TARGET_F1 / f1_native, *FORMANT_CAP))
        if abs(formant_shift - 1.0) >= 0.005:
            sp = _warp_sp(sp, formant_shift)
            formant_applied = True

    # 1. F0 lock: rescale voiced frames so MEDIAN lands on target_f0.
    med = float(np.median(f0[voiced]))
    ratio = target_f0 / med
    f0_new = f0.copy()
    f0_new[voiced] = f0[voiced] * ratio

    # 1b. Stillness: compress residual jitter after lock.
    f0_new, cv_pre, jitter_clamped = _clamp_jitter(f0_new, voiced)

    # 2. Terminal pitch lift (northern cadence): last ~450ms voiced, log-normal tail.
    v_idx = np.where(voiced)[0]
    if len(v_idx) > 20:
        last = int(v_idx[-1])
        span = min(len(f0_new) // 3, 90)
        start = last - span
        if start > int(v_idx[0]):
            s = np.arange(span) / span
            shape = np.exp(-((np.log(s + 0.08) + 1.2) ** 2) / 1.8)
            shape = shape / shape.max()
            f0_new[start:last] += lift_hz * shape

    y = pw.synthesize(f0_new, sp, ap, SR, frame_period=FRAME_MS)

    # 3. Amplitude stillness on the analytic envelope. Breath gaps stay gaps.
    y, amp_meta = _amplitude_stillness(y)

    # 4. Glottal coda truncation: 40 ms ending adab.
    if coda_damp:
        n_cut = int(0.04 * SR)
        if len(y) > n_cut * 2:
            ramp = np.linspace(1.0, 0.0, n_cut) ** 2
            y[-n_cut:] *= ramp

    # 5. Fourier OBS — if extras inflated centroid variance, revert to F0+lift+coda only.
    c_mean_out, c_std_out = _stft_centroid_stats(y)
    extras_reverted = False
    inflate = (c_std_out / c_std_in) if c_std_in > 1.0 else 1.0
    if inflate > CENTROID_INFLATE_MAX:
        f0_plain = f0.copy()
        f0_plain[voiced] = f0[voiced] * ratio
        if len(v_idx) > 20:
            last = int(v_idx[-1])
            span = min(len(f0_plain) // 3, 90)
            start = last - span
            if start > int(v_idx[0]):
                s = np.arange(span) / span
                shape = np.exp(-((np.log(s + 0.08) + 1.2) ** 2) / 1.8)
                shape = shape / shape.max()
                f0_plain[start:last] += lift_hz * shape
        y = pw.synthesize(f0_plain, pw.cheaptrick(x, f0, t, SR), ap, SR, frame_period=FRAME_MS)
        if coda_damp:
            n_cut = int(0.04 * SR)
            if len(y) > n_cut * 2:
                y[-n_cut:] *= np.linspace(1.0, 0.0, n_cut) ** 2
        extras_reverted = True
        formant_applied = False
        jitter_clamped = False
        amp_meta = {"silence_frac": amp_meta.get("silence_frac", 0.0), "amp_applied": False}
        c_mean_out, c_std_out = _stft_centroid_stats(y)

    meta = {
        "med_src": round(med, 1),
        "ratio": round(float(ratio), 4),
        "target": target_f0,
        "lift": lift_hz,
        "f1_native_hz": round(f1_native, 1) if f1_native else None,
        "formant_shift": round(formant_shift, 4),
        "formant_applied": formant_applied,
        "f0_cv_pre_clamp": round(cv_pre, 4),
        "jitter_clamped": jitter_clamped,
        "centroid_in_hz": round(c_mean_in, 1),
        "centroid_in_std": round(c_std_in, 1),
        "centroid_out_hz": round(c_mean_out, 1),
        "centroid_out_std": round(c_std_out, 1),
        "centroid_inflate": round(float(inflate), 3),
        "extras_reverted": extras_reverted,
        "silence_frac": round(float(amp_meta.get("silence_frac", 0.0)), 3),
        "amp_applied": bool(amp_meta.get("amp_applied", False)),
        "gpu": False,
        "method": "world+analytic",
        "jiwa": "A_f_phi_constraint",
    }
    return y, meta


def measure_f0(path_or_x):
    x = load_pcm(path_or_x) if isinstance(path_or_x, str) else path_or_x
    f0, t = pw.dio(x, SR, f0_floor=F0_FLOOR, f0_ceil=F0_CEIL)
    f0 = pw.stonemask(x, f0, t, SR)
    v = f0[f0 > F0_FLOOR]
    return (
        round(float(np.median(v)), 1),
        round(float(np.percentile(v, 10)), 1),
        round(float(np.percentile(v, 90)), 1),
    )


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("src")
    a.add_argument("dst")
    a.add_argument("--target-f0", type=float, default=239.0)
    a.add_argument("--lift", type=float, default=35.0)
    a.add_argument("--no-coda", action="store_true")
    args = a.parse_args()

    x = load_pcm(args.src)
    y, meta = stabilize(x, args.target_f0, args.lift, coda_damp=not args.no_coda)
    save_wav(args.dst, y)
    med, p10, p90 = measure_f0(args.dst)
    meta.update(out_median=med, out_p10=p10, out_p90=p90, in_band=BAND[0] <= med <= BAND[1])
    print(meta)
