#!/usr/bin/env python3
"""verify_take.py -- falsify a MiniMax voice take BEFORE it ships.

The whole pre-delivery gate in one command: duration floor, ASR round-trip,
normalised similarity, inserted/missing words, f0 family check against the
clone source. The ratio and the INSERTED flag are LEADS, not verdicts -- read the
transcript. A low score on dense dialect is normal; it is not a defect and not a
reason to re-roll. `--alias HEARD=WRITTEN` remains available as an optional
diagnostic if you want to see which respellings fired, but it is never required
before shipping a take.

Usage:
  python3 verify_take.py TAKE.mp3 --text line.txt
  python3 verify_take.py TAKE.mp3 --text line.txt --source clone_source.mp3
  python3 verify_take.py TAKE.mp3 --text line.txt   # then READ the transcript
  python3 verify_take.py TAKE.mp3 --text line.txt --expect 40 --tol 4

Verdicts:
  FAIL    INSERTED words -- the model spoke something absent from the input.
          Render-time contamination (the V8 checkpoint class). Input sanitising
          cannot catch it; only a text-vs-transcript diff can. Re-render.
  REVIEW  match < 85%, missing words beyond fillers, duration off the band,
          f0 median > ~15 Hz from the source, or the ASR step could not run.
  PASS    everything above clean.

Exit: 0 PASS, 1 REVIEW, 2 FAIL. Never ship a take this script has not seen.
Needs GROQ_API_KEY in the environment (source /root/.secrets/kunci-root.env).
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import sys

NUM = {
    "0": "kosong", "1": "satu", "2": "dua", "3": "tiga", "4": "empat",
    "5": "lima", "6": "enam", "7": "tujuh", "8": "lapan", "9": "sembilan",
    "10": "sepuluh", "11": "sebelas", "12": "dua belas", "20": "dua puluh",
    "30": "tiga puluh", "40": "empat puluh", "45": "empat puluh lima",
    "50": "lima puluh", "100": "seratus", "1000": "seribu",
    "2019": "dua ribu sembilan belas", "2020": "dua ribu dua puluh",
}
FILLERS = {"hmm", "hm", "ha", "oh", "eh", "ah", "aah", "la", "lah", "kan", "je"}

# PHANTOM TAIL — Whisper's stock outros. Measured 2026-10-23 on an 86 s BM take:
# the transcriber appended "terima kasih kerana menonton" and placed its last word at
# 116.1 s inside an 86.36 s file. Physically impossible, so it is invention, not audio.
# Without this list every clean long take trips INSERTED and needs the tail/EOF
# discriminator to rescue it. A known phantom should not look like render contamination.
PHANTOM_TAIL = [
    "terima kasih kerana menonton", "terima kasih kerana menonton video ini",
    "thanks for watching", "thank you for watching", "subscribe", "sila subscribe",
    "jangan lupa subscribe", "selamat menonton", "hope you enjoyed",
]


def strip_phantom_tail(heard: str) -> str:
    """Remove a stock Whisper outro that was never spoken. Only the TAIL is cut, and
    only when the phrase sits at the very end -- a phantom in the middle would be a
    real transcription error and must still fail."""
    t = heard.rstrip()
    # match on the de-punctuated tail: Whisper writes "menonton!" and "Menonton." alike.
    tl = re.sub(r"[^a-z0-9 ]+", " ", t.lower())
    tl = re.sub(r"\s+", " ", tl).strip()
    for ph in sorted(PHANTOM_TAIL, key=len, reverse=True):
        if tl.endswith(ph):
            # cut the same number of WORDS from the original, preserving earlier text
            n = len(ph.split())
            words = t.split()
            return " ".join(words[: len(words) - n]).rstrip(" .,!-")
    return t


def norm(s: str, aliases: dict[str, str]) -> str:
    s = s.lower().replace("\u2019", "'")
    s = re.sub(r"\b(\d+)\b", lambda m: NUM.get(m.group(1), m.group(1)), s)
    for k, v in aliases.items():
        s = re.sub(r"\b" + re.escape(k) + r"\b", v, s)
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def asr(path: str, lang: str = "ms") -> dict:
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        raise SystemExit("GROQ_API_KEY not set -- source the vault first; the round-trip MUST run")
    out = subprocess.run(
        ["curl", "-s", "https://api.groq.com/openai/v1/audio/transcriptions",
         "-H", "Authorization: Bearer " + key,
         "-F", "file=@" + path,
         "-F", "model=whisper-large-v3-turbo",
         "-F", "language=" + lang,
         "-F", "response_format=verbose_json"],
        capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def duration(path: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    try:
        return float(out.splitlines()[0])
    except (ValueError, IndexError):
        return 0.0


def f0(path: str):
    """(median, p90) Hz. librosa yin when present, else a numpy autocorrelation
    fallback so the identity check is never silently dark.

    Why (2026-10-23): every receipt on this lane read "librosa absent -- f0
    family check SKIPPED (not a pass)". A check that always reports "skipped"
    is not a check. The fallback is conservative: it needs voiced frames with a
    clear periodicity peak, and reports UNKNOWN rather than inventing a number.
    """
    try:
        import numpy as np
    except ImportError:
        print("  note: numpy absent -- f0 identity check UNKNOWN (not a pass)")
        return None
    try:
        import librosa
        y, sr = librosa.load(path, sr=16000, mono=True)
        f = librosa.yin(y, fmin=60, fmax=400, sr=sr, frame_length=2048, hop_length=512)
        m = np.isfinite(f) & (f > 0)
        if not m.any():
            return None
        return round(float(np.median(f[m])), 1), round(float(np.percentile(f[m], 90)), 1)
    except ImportError:
        pass

    y, sr = _load_mono_16k(path)
    if y is None or len(y) < sr // 4:
        print("  note: audio unreadable for f0 -- identity check UNKNOWN (not a pass)")
        return None
    hop, win = 320, 1024
    lo, hi = int(sr / 400), int(sr / 60)
    est = []
    for start in range(0, len(y) - win, hop):
        fr = y[start:start + win]
        fr = fr - fr.mean()
        if float(np.dot(fr, fr)) < 1e-5:
            continue
        ac = np.correlate(fr, fr, mode="full")[win - 1:]
        if ac[0] <= 0:
            continue
        seg = ac[lo:hi]
        if len(seg) == 0:
            continue
        peak = float(seg.max())
        if peak / ac[0] < 0.30:
            continue
        # OCTAVE GUARD: take the lowest lag whose peak is within 85% of the best
        # peak. Plain argmax locks onto the 2nd harmonic, which is stronger than
        # the fundamental in most male voices; that reported a phantom 300 Hz
        # p90 on a take whose real f0 was ~96 Hz.
        cand = [i for i, v in enumerate(seg) if v >= 0.85 * peak]
        lag = (cand[0] if cand else int(np.argmax(seg))) + lo
        est.append(sr / lag)
    if len(est) < 10:
        print("  note: too few voiced frames -- identity check UNKNOWN (not a pass)")
        return None
    a = np.array(est)
    # Drop octave-up frames that survived the guard: anything past 1.9x the
    # lower-half median is a doubling artefact, not a pitch excursion.
    lower = np.median(a[a <= np.percentile(a, 50)])
    a = a[(a >= 0.6 * lower) & (a <= 1.9 * lower)]
    if len(a) < 10:
        print("  note: too few stable frames -- identity check UNKNOWN (not a pass)")
        return None
    return round(float(np.median(a)), 1), round(float(np.percentile(a, 90)), 1)


def _load_mono_16k(path: str):
    """Decode any audio to mono float32 @16k via ffmpeg (already a lane dep)."""
    import subprocess
    try:
        import numpy as np
    except ImportError:
        return None, None
    try:
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000",
                            "-f", "s16le", "-"], capture_output=True, timeout=180)
    except Exception:
        return None, None
    if r.returncode != 0 or not r.stdout:
        return None, None
    return np.frombuffer(r.stdout, dtype="<i2").astype("float32") / 32768.0, 16000


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("take")
    ap.add_argument("--text", required=True,
                    help="PATH to the input line file as rendered (NOT the line text itself — "
                         "passing the raw line raises OSError: File name too long)")
    ap.add_argument("--source", help="clone source audio -- enables the f0 family check")
    ap.add_argument("--alias", action="append", default=[],
                    metavar="HEARD=WRITTEN",
                    help="transcriber substitution to normalise (e.g. plex=flex). Repeatable.")
    ap.add_argument("--expect", type=float, help="expected duration in seconds")
    ap.add_argument("--tol", type=float, default=4.0)
    ap.add_argument("--lang", default="ms")
    a = ap.parse_args()

    aliases = {}
    for pair in a.alias:
        k, _, v = pair.partition("=")
        if k and v:
            aliases[k.lower()] = v.lower()

    src = open(a.text, encoding="utf-8").read().strip()
    dur = duration(a.take)
    rate = (len(src) / dur) if dur else 0.0
    j = asr(a.take, a.lang)
    heard = strip_phantom_tail((j.get("text") or "").strip())

    ns, nh = norm(src, aliases), norm(heard, aliases)
    # TOKEN-level diff. The opcodes of a SequenceMatcher run on the normalised
    # STRINGS carry CHARACTER offsets; indexing a token list with them is a
    # category error that manufactures phantom words. Measured 2026-09-19: a
    # take reported INSERTED ['pandang'] for a word plainly present in the
    # transcript, because the char-level 'insert' opcode for the 'h' in
    # `tau`→`tahu` was used to slice the token list. Diff the token lists.
    ns_t, nh_t = ns.split(), nh.split()
    sm = difflib.SequenceMatcher(None, ns_t, nh_t)
    match = sm.ratio() * 100
    ins = [w for op in sm.get_opcodes() if op[0] == "insert" for w in nh_t[op[3]:op[4]]]
    dele = [w for op in sm.get_opcodes() if op[0] == "delete" for w in ns_t[op[1]:op[2]]]
    miss_real = [w for w in dele if w not in FILLERS]

    print(f"take     : {a.take}")
    print(f"duration : {dur:.2f}s   ({rate:.1f} chars/s of {len(src)} input chars)")
    print(f"match    : {match:.1f}%")
    print(f"INSERTED : {ins or 'none'}")
    print(f"MISSING  : {dele or 'none'}")
    print(f"heard    : {heard}")
    if aliases:
        print(f"aliases  : {aliases}")

    verdict, why = 0, []

    if ins:
        verdict = 2
        why.append("INSERTED words -> render-time contamination, re-render")
    if miss_real:
        verdict = max(verdict, 1)
        why.append("real words missing from the take")
    if match < 85:
        verdict = max(verdict, 1)
        why.append("match < 85% -- re-read BOTH normalised strings before re-rolling; "
                   "digits / loanwords / BM minimal pairs inflate the mismatch")

    if a.expect:
        if abs(dur - a.expect) > a.tol:
            verdict = max(verdict, 1)
            why.append(f"duration {dur:.1f}s vs expected {a.expect:.1f}s +-{a.tol}")
    elif dur and not (6.0 <= rate <= 16.0):
        verdict = max(verdict, 1)
        why.append(f"pacing {rate:.1f} chars/s outside the 6-16 band -- wrong speed for this voice, or truncated")

    f_take = f0(a.take)
    if f_take:
        print(f"f0 take  : med={f_take[0]} p90={f_take[1]}")
    if a.source:
        f_src = f0(a.source)
        if f_src:
            print(f"f0 source: med={f_src[0]} p90={f_src[1]}")
        if f_take and f_src and abs(f_take[0] - f_src[0]) > 15:
            verdict = max(verdict, 1)
            why.append(f"f0 median {abs(f_take[0]-f_src[0]):.1f} Hz from source -- the clone drifted")

    print("verdict  : " + ("PASS" if verdict == 0 else ("REVIEW" if verdict == 1 else "FAIL")))
    for w in why:
        print("  - " + w)
    return verdict


if __name__ == "__main__":
    sys.exit(main())
