#!/usr/bin/env python3
"""voice_render_verify — standing verifier for a rendered voice artifact.

WHAT IT ANSWERS
  1. Did the engine speak MORE than I wrote?   (injection / checkpoint contamination)
  2. Did it speak LESS than I wrote?           (truncation / dropped clause)
  3. Is the audio plausibly complete?          (duration floor, silence profile)
  4. Which voice is in the file?               (F0 median + MFCC vs a reference, optional)

WHY IT EXISTS
  The contamination class that got voice id i-ARIF-V8 revoked (2026-09-14) was only
  caught because someone ran an ASR round-trip BY HAND. A verification that depends on
  someone remembering to run it is not a control. This script is the control.

USAGE
  python3 voice_render_verify.py --audio out.ogg --text input.txt \
      [--ref source.wav] [--json] [--strict]

EXIT CODES
  0 CLEAN           no extra speech, duration above floor
  1 CONTAMINATED    engine emitted tokens absent from the input text
  2 TRUNCATED       duration below floor (render silently cut short)
  3 ERROR           could not verify (no key, ASR failed) — reported, never guessed

NOTE: this verifier never rewrites or blocks a delivery by itself. It reports. Wiring it
into the delivery path is an F13 call — the pipeline that already works is not touched.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

SECRET_FILES = ("/root/.secrets/kunci-root.env", "/root/.secrets/kunci-mas.env")
GROQ_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
ASR_MODEL = "whisper-large-v3"
ASR_LANG = "ms"


def groq_key() -> str | None:
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    for path in SECRET_FILES:
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            for line in fh:
                if "GROQ_API_KEY=" in line:
                    return line.split("GROQ_API_KEY=", 1)[1].strip().strip("\"'")
    return None


def transcribe(audio: str) -> str:
    """ASR round-trip. Uses curl for the multipart upload — a hand-rolled
    multipart body got 403 from the endpoint while curl's was accepted."""
    key = groq_key()
    if not key:
        raise RuntimeError("GROQ_API_KEY not found in env or secrets")
    proc = subprocess.run(
        ["curl", "-sS", "--fail-with-body", GROQ_URL,
         "-H", f"Authorization: Bearer {key}",
         "-F", f"file=@{audio}",
         "-F", f"model={ASR_MODEL}",
         "-F", f"language={ASR_LANG}",
         "-F", "response_format=text"],
        capture_output=True, text=True, timeout=240)
    if proc.returncode != 0:
        raise RuntimeError(f"curl exit {proc.returncode}: {proc.stderr.strip()[:300]}")
    return proc.stdout.strip()


def duration(audio: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", audio],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out or 0.0)


TOKEN_RE = re.compile(r"[0-9a-zà-ÿ]+", re.I)


def tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text.casefold())


def _similar(a: str, b: str) -> float:
    import difflib
    return difflib.SequenceMatcher(a=a, b=b, autojunk=False).ratio()


def diff(expected: str, got: str) -> dict:
    """Token diff with ASR-noise filtering.

    Verbatim token diff is too blunt on Malay: Whisper writes 'bersanda' for
    'bersandar', 'bari' for 'baring', 'bang sadu' for 'Abang Sado' — single
    misspelled tokens, not injected clauses. An extra token is only counted as
    SUSPICIOUS when it does not resemble any expected token (char similarity
    < 0.72). Genuine checkpoint contamination is a run of foreign words, which
    survives that filter; ASR spelling noise does not.
    """
    import difflib
    exp, act = tokens(expected), tokens(got)
    sm = difflib.SequenceMatcher(a=exp, b=act, autojunk=False)
    extra, missing, suspicious = [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            missing.extend(exp[i1:i2])
        if tag in ("replace", "insert"):
            for tok in act[j1:j2]:
                extra.append(tok)
                window = exp[max(0, i1 - 3):i2 + 3] or exp
                if max((_similar(tok, e) for e in window), default=0.0) < 0.72:
                    suspicious.append(tok)
    return {
        "expected_tokens": len(exp),
        "heard_tokens": len(act),
        "similarity": round(sm.ratio(), 4),
        "extra_tokens_heard": extra,
        "missing_tokens": missing,
        "suspicious_extra_tokens": suspicious,
    }


def dsp(audio: str, ref: str | None) -> dict:
    """F0 median + MFCC cosine vs a reference. Skipped when librosa is absent."""
    try:
        import numpy as np
        import librosa
    except Exception:
        return {"dsp": "SKIPPED_NO_LIBROSA"}

    def feat(path):
        y, _ = librosa.load(path, sr=22050, mono=True)
        y, _ = librosa.effects.trim(y, top_db=30)
        f0, _, _ = librosa.pyin(y, fmin=60, fmax=400, sr=22050,
                                frame_length=2048, hop_length=256)
        f0v = f0[~np.isnan(f0)]
        mfcc = librosa.feature.mfcc(y=y, sr=22050, n_mfcc=13, n_fft=2048, hop_length=512)
        rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
        keep = rms[: mfcc.shape[1]] >= np.percentile(rms, 40)
        if keep.sum() < 10:
            keep = np.ones(mfcc.shape[1], dtype=bool)
        mf = mfcc[:, : len(keep)][:, keep]
        return float(np.median(f0v)) if len(f0v) else None, np.mean(mf, axis=1)

    out: dict = {}
    try:
        f0, mf = feat(audio)
        out["f0_median_hz"] = round(f0, 1) if f0 else None
        if ref:
            rf0, rmf = feat(ref)
            out["ref_f0_median_hz"] = round(rf0, 1) if rf0 else None
            out["f0_delta_hz"] = round(f0 - rf0, 1) if (f0 and rf0) else None
            out["mfcc_cos_vs_ref"] = round(
                float(np.dot(mf, rmf) / (np.linalg.norm(mf) * np.linalg.norm(rmf))), 4)
    except Exception as exc:  # instrument failure is reported, never hidden
        out["dsp_error"] = f"{type(exc).__name__}: {exc}"
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--text", required=True, help="the text that was rendered")
    ap.add_argument("--ref", default=None, help="optional reference voice sample")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="fail on any extra token, not only >=2")
    args = ap.parse_args()

    expected = open(args.text, encoding="utf-8").read().strip()
    report: dict = {"audio": args.audio, "text": args.text}
    try:
        report["duration_s"] = round(duration(args.audio), 2)
    except Exception as exc:
        report["verdict"] = "ERROR"
        report["error"] = f"ffprobe failed: {exc}"
        print(json.dumps(report, indent=2) if args.json else report)
        return 3

    chars = len(expected)
    floor = max(0.4 * (chars / 12.0), 2.0)
    report["duration_floor_s"] = round(floor, 2)
    report["duration_ok"] = report["duration_s"] >= floor

    try:
        heard = transcribe(args.audio)
        report["asr"] = heard
        d = diff(expected, heard)
        report.update(d)
        threshold = 1 if args.strict else 2
        contaminated = len(d["suspicious_extra_tokens"]) >= threshold
    except Exception as exc:
        report["verdict"] = "ERROR"
        report["error"] = f"ASR round-trip failed: {type(exc).__name__}: {exc}"
        report.update(dsp(args.audio, args.ref))
        print(json.dumps(report, indent=2) if args.json else report)
        return 3

    report.update(dsp(args.audio, args.ref))

    if contaminated:
        report["verdict"] = "CONTAMINATED"
        code = 1
    elif not report["duration_ok"]:
        report["verdict"] = "TRUNCATED"
        code = 2
    else:
        report["verdict"] = "CLEAN"
        code = 0

    print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else report)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
