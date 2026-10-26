#!/usr/bin/env python3
"""voice_identity.py — measured speaker identity for a synthesized take.

WHY THIS EXISTS
The f0 family check inside verify_take.py compares pitch medians. Pitch is not
identity: the same throat at a different register measures a different f0, and
two different throats can land on the same median. Measured 2026-10-23 on real
takes: the clone source (93.8 Hz median) and tonight's alpha take (151.8 Hz)
differ by 58 Hz — a number that says nothing about whether it is the same person.

ECAPA-TDNN speaker embeddings answer the actual question. Measured on this lane
2026-10-23 (7 files, cosine on L2-normalised embeddings):

    same person:      0.706 .. 0.973
    different person: -0.009 .. 0.221   (siti, pmx, osman)

Separation factor 3.2x, so the decision threshold sits at 0.45 — the midpoint of
the two measured populations, not a guessed round number.

Runs in its own venv (/root/.venvs/voiceid) because it needs torch + speechbrain.
This is deliberate: the render gate must stay light, and a missing dependency
must never masquerade as a pass.

Exit codes: 0 SAME, 1 DIFFERENT, 2 UNMEASURED.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

THRESHOLD = 0.45          # midpoint of measured same/different populations
MODEL_DIR = "/root/.cache/sb/ecapa"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("take", help="the rendered audio")
    ap.add_argument("--source", required=True, help="the clone reference audio")
    ap.add_argument("--threshold", type=float, default=THRESHOLD)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    for p in (a.take, a.source):
        if not os.path.exists(p):
            print(json.dumps({"ok": False, "error": "missing " + p}))
            return 2

    try:
        import warnings
        warnings.filterwarnings("ignore")
        os.environ.setdefault("HF_HOME", "/root/.cache/huggingface")
        import torch
        import librosa
        from speechbrain.inference.speaker import EncoderClassifier
    except Exception as e:
        print(json.dumps({"ok": False, "error": "deps: %s: %s" % (type(e).__name__, e)}))
        return 2

    clf = None
    for src in ("speechbrain/spkrec-ecapa-voxceleb", MODEL_DIR):
        try:
            clf = EncoderClassifier.from_hparams(source=src, savedir=MODEL_DIR,
                                                 run_opts={"device": "cpu"})
            break
        except Exception:
            continue
    if clf is None:
        print(json.dumps({"ok": False, "error": "model unavailable (offline?)"}))
        return 2

    def emb(path):
        y, sr = librosa.load(path, sr=16000, mono=True)
        sig = torch.tensor(y[:16000 * 60]).unsqueeze(0)
        with torch.no_grad():
            e = clf.encode_batch(sig).squeeze()
        return e / e.norm()

    cos = float(torch.dot(emb(a.take), emb(a.source)))
    verdict = "SAME" if cos >= a.threshold else "DIFFERENT"

    if a.json:
        print(json.dumps({"ok": True, "cosine": round(cos, 3),
                          "threshold": a.threshold, "verdict": verdict}))
    else:
        print("identity : cosine=%.3f vs source  (threshold %s) -> %s" % (cos, a.threshold, verdict))
        if verdict == "DIFFERENT":
            print("  - measured speaker does not match the clone reference -- do not ship")
    return 0 if verdict == "SAME" else 1


if __name__ == "__main__":
    sys.exit(main())
