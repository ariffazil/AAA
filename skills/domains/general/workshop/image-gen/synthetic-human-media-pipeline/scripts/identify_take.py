#!/usr/bin/env python3
"""Identify which previously rendered take an incoming audio file is.

Usage:
    python3 identify_take.py <input_audio> <candidate_dir_or_file> [more...]
                             [--top 8] [--hop 160] [--min-corr 0.5] [--aliases]

Why this exists
---------------
A requester points at an earlier artifact ("you generated this before"), replies to an old
clip, or forwards a take whose line you half-recognise. Re-rendering on a guessed voice
spends a take and answers a different question. Resolve the artifact first.

Method
------
64-band mel spectrogram, 16 kHz mono, 10 ms hop. Per-file global mean removal, then an
exhaustive sliding window over each candidate at the query's exact frame count, scored by
cosine of the mean-removed windows.

Read the TOP TWO, not the top one. Measured bands on real persona takes:
    same take, re-encoded (ogg <- mp3) ........ 0.998 - 1.000, offset 0.00 s
    same line, same voice, different take ..... 0.85  - 0.95
    different voice id, same persona register . 0.53  - 0.80
So the score separates "same take" from "same register" cleanly, and the GAP between #1
and #2 is what carries the verdict. A lone high number below ~0.99 means same register,
not same artifact.

No network, no environment variables, no writes: reads audio, prints rows.
"""

import argparse
import glob
import hashlib
import os
import sys

import numpy as np

AUDIO_EXT = {'.mp3', '.wav', '.ogg', '.m4a', '.flac', '.opus', '.aac'}


def _load_librosa():
    try:
        import librosa  # noqa: F401
    except ImportError:
        sys.exit(
            "librosa not importable. Run this with the interpreter that has numpy+librosa "
            "(the DSP venv), or: pip install librosa soundfile"
        )
    import librosa
    return librosa


def mel_feats(path, librosa, sr=16000, hop=160, n_mels=64, fmax=8000):
    """Return (mean-removed unit-norm mel-dB matrix, duration_s)."""
    y, _ = librosa.load(path, sr=sr, mono=True)
    if y.size == 0:
        raise ValueError("empty audio")
    s = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, hop_length=hop, fmax=fmax)
    logmel = librosa.power_to_db(s, ref=np.max)
    logmel = logmel - logmel.mean()
    logmel = logmel / (np.linalg.norm(logmel) + 1e-12)
    return logmel, y.size / sr


def md5(path, chunk=1 << 20):
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for block in iter(lambda: fh.read(chunk), b''):
            h.update(block)
    return h.hexdigest()


def expand(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for ext in sorted(AUDIO_EXT):
                out.extend(glob.glob(os.path.join(p, '**', '*' + ext), recursive=True))
        elif os.path.isfile(p):
            out.append(p)
        else:
            out.extend(glob.glob(p, recursive=True))
    seen, uniq = {}, []
    for p in sorted(set(out)):
        try:
            key = md5(p)
        except OSError:
            continue
        if key in seen:
            seen[key].append(p)
        else:
            seen[key] = [p]
            uniq.append(p)
    return uniq, seen


def best_offset(query, cand, step_div=8):
    """Slide `cand` under `query` (both unit-norm), return (cosine, offset_frames)."""
    q = query.shape[1]
    if cand.shape[1] < q:
        return None, None
    step = max(1, q // step_div)
    best, best_off = -1.0, 0
    for off in range(0, cand.shape[1] - q + 1, step):
        c = float(np.sum(query * cand[:, off:off + q]))
        if c > best:
            best, best_off = c, off
    return best, best_off


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input', help='the incoming audio to identify')
    ap.add_argument('candidates', nargs='+', help='dirs, files, or globs to search')
    ap.add_argument('--top', type=int, default=8, help='ranked rows to print (default 8)')
    ap.add_argument('--hop', type=int, default=160,
                    help='mel hop in samples, 10 ms at 16 kHz (default 160)')
    ap.add_argument('--min-corr', type=float, default=0.5, help='hide rows below this (default 0.5)')
    ap.add_argument('--aliases', action='store_true',
                    help='also list same-content filename aliases')
    args = ap.parse_args()

    librosa = _load_librosa()
    qfeat, qdur = mel_feats(args.input, librosa, hop=args.hop)
    print('input     : %s  (%.2f s, %d frames)' % (args.input, qdur, qfeat.shape[1]))
    print('method    : 64-mel, hop=%d, mean-removed sliding cosine' % args.hop)

    cands, by_hash = expand(args.candidates)
    cands = [c for c in cands if os.path.abspath(c) != os.path.abspath(args.input)]
    print('candidates: %d unique file(s)  (%d filename alias(es) collapsed)'
          % (len(cands), sum(len(v) - 1 for v in by_hash.values())))
    print('')

    rows, too_short = [], 0
    for c in cands:
        try:
            cf, cdur = mel_feats(c, librosa, hop=args.hop)
        except Exception as exc:
            print('  SKIP %s (%s)' % (c, exc))
            continue
        corr, off = best_offset(qfeat, cf)
        if corr is None:
            too_short += 1
            continue
        rows.append((corr, off * args.hop / 16000.0, cdur, c))

    if not rows:
        print('no candidate at least as long as the input (%d shorter skipped)' % too_short)
        return 1

    rows.sort(reverse=True)
    for i, (corr, off, dur, path) in enumerate(rows[:args.top]):
        if corr < args.min_corr:
            break
        print('%2d. corr=%.3f  at t=%5.2fs  dur=%6.2fs  %s' % (i + 1, corr, off, dur, path))

    print('')
    top = rows[0][0]
    second = rows[1][0] if len(rows) > 1 else None
    if second is None:
        print('verdict   : SINGLE CANDIDATE corr=%.3f — no gap, no identification claim' % top)
    elif top >= 0.99 and (top - second) >= 0.10:
        print('verdict   : MATCH — %.3f vs %.3f, same take re-encoded, offset %.2f s'
              % (top, second, rows[0][1]))
    elif (top - second) < 0.05:
        print('verdict   : AMBIGUOUS — %.3f vs %.3f; near-identical takes. Transcribe both and '
              'compare the words before claiming which one it is.' % (top, second))
    else:
        print('verdict   : SAME REGISTER, DIFFERENT TAKE — %.3f vs %.3f; this is not the artifact '
              'pointed at' % (top, second))

    if args.aliases:
        print('')
        print('same-content aliases:')
        for c in [r[3] for r in rows[:args.top]]:
            others = [o for o in by_hash.get(md5(c), []) if o != c]
            if others:
                print('  %s -> also %s' % (c, ', '.join(others)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
