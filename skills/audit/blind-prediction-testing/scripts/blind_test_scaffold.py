#!/usr/bin/env python3
"""
Blind prediction test scaffold.

Two halves, deliberately separated so the answer cannot reach the predictor in the
same step that presents the test:

  build   assigns a label to every item by SEEDED shuffle and writes the truth to a
          SEALED sidecar file. It prints nothing that reveals the answer.
  score   compares a committed prediction against the sealed truth and prints the
          trivial baseline BESIDE the score, then says whether any skill was shown.

The separation is the point. A harness that presents the test and holds the answer
in one call will leak it, usually through the ordering.

Usage
  python3 blind_test_scaffold.py build --items items.json --sealed sealed.json [--seed N]
  python3 blind_test_scaffold.py score --sealed sealed.json --pred pred.json
  python3 blind_test_scaffold.py demo

items.json : {"item_key": "YES" | "NO", ...}      truth, pre-declared
pred.json  : {"A": "YES", "B": "NO", ...}         prediction, committed in writing
"""
from __future__ import annotations

import argparse
import json
import random
import sys

LABELS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
SEAL_BANNER = "--- SEALED --- Do not read until the prediction is committed. ---"
SEAL_KEY = "_sealed"


def _load_json(path):
    """Read a JSON object, tolerating a hand-added banner line above it."""
    with open(path) as fh:
        text = fh.read()
    start = text.find("{")
    if start < 0:
        raise SystemExit(f"{path}: no JSON object found")
    return json.loads(text[start:])


def build(truth, seed):
    """Label items by seeded shuffle; return the sealed structure."""
    keys = sorted(truth)
    if not keys:
        raise SystemExit("no items supplied")
    if len(keys) > len(LABELS):
        raise SystemExit(f"at most {len(LABELS)} items are supported")
    random.Random(seed).shuffle(keys)
    mapping = {lab: key for lab, key in zip(LABELS, keys)}
    return {
        SEAL_KEY: SEAL_BANNER,
        "seed": seed,
        "labels": mapping,
        "truth": {lab: truth[key] for lab, key in mapping.items()},
    }


def score(sealed, pred):
    truth = sealed["truth"]
    labels = sorted(truth)
    missing = [lab for lab in labels if lab not in pred]
    if missing:
        raise SystemExit(f"prediction incomplete, missing labels: {missing}")

    n = len(labels)
    correct = sum(1 for lab in labels if pred[lab] == truth[lab])
    yes = sum(1 for lab in labels if truth[lab] == "YES")
    majority = "YES" if yes * 2 >= n else "NO"
    baseline = sum(1 for lab in labels if majority == truth[lab])

    return {
        "n": n,
        "correct": correct,
        "accuracy": correct / n,
        "baseline_guess": majority,
        "baseline_correct": baseline,
        "baseline_accuracy": baseline / n,
        "edge_pp": (correct - baseline) / n * 100.0,
        "rows": [
            (lab, sealed["labels"][lab], truth[lab], pred[lab], pred[lab] == truth[lab])
            for lab in labels
        ],
    }


def report(result):
    print(f"items              : {result['n']}")
    print(f"score              : {result['correct']}/{result['n']}  ({result['accuracy'] * 100:.0f}%)")
    print(f"trivial baseline   : always say {result['baseline_guess']}  ->  "
          f"{result['baseline_correct']}/{result['n']}  ({result['baseline_accuracy'] * 100:.0f}%)")
    print(f"edge over baseline : {result['edge_pp']:+.0f} pp")
    if result["correct"] <= result["baseline_correct"]:
        print("VERDICT            : no skill demonstrated - at or below guessing.")
    else:
        print("VERDICT            : above baseline. Sample size is still small; do not generalise.")
    print()
    print(f"{'':<3} {'revealed':<28} {'truth':<6} {'said':<6} ok")
    for lab, key, t, p, ok in result["rows"]:
        print(f"{lab:<3} {key:<28} {t:<6} {p:<6} {'yes' if ok else 'NO'}")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Blind prediction test scaffold",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="label items and seal the answer")
    b.add_argument("--items", required=True)
    b.add_argument("--sealed", required=True)
    b.add_argument("--seed", type=int, default=20260101)

    s = sub.add_parser("score", help="score a committed prediction")
    s.add_argument("--sealed", required=True)
    s.add_argument("--pred", required=True)

    sub.add_parser("demo", help="self-test: a skill-less predictor must not beat the baseline")

    a = ap.parse_args(argv)

    if a.cmd == "build":
        sealed = build(_load_json(a.items), a.seed)
        with open(a.sealed, "w") as fh:
            json.dump(sealed, fh, indent=1)
        print(f"sealed {len(sealed['truth'])} items -> {a.sealed}")
        print("labels the predictor may answer:", " ".join(sorted(sealed["labels"])))
        print("the answer was NOT printed. commit the prediction, then run: score")
        return 0

    if a.cmd == "score":
        sealed = _load_json(a.sealed)
        pred = {k.upper(): str(v).upper() for k, v in _load_json(a.pred).items()}
        report(score(sealed, pred))
        return 0

    truth = {f"case{i:03d}": ("YES" if i % 5 == 0 else "NO") for i in range(40)}
    sealed = build(truth, 7)
    rng = random.Random(99)
    pred = {lab: rng.choice(["YES", "NO"]) for lab in sealed["truth"]}
    print("demo: coin-flip predictor vs sealed truth, 40 items, 20% true rate")
    print("expected: at or BELOW the trivial baseline, because the baseline guesses the")
    print("majority class and a coin flip does not.\n")
    report(score(sealed, pred))
    return 0


if __name__ == "__main__":
    sys.exit(main())
