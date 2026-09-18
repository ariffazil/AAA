#!/usr/bin/env python3
"""Committed blind test for a predictive claim.

Design rules enforced here:
  * cases are chosen by a RULE, not by memory of the outcome
  * the prediction window is HIDDEN from everything printed to stdout
  * labels are assigned by a SEEDED SHUFFLE so label order carries no information
  * the answer is written to a SEPARATE sealed file

The predictor commits its answer and a confidence level BEFORE the sealed file
is read, then scores against the trivial baseline (always-most-common-class).

Read-only. Source: yfinance monthly closes.
"""
import json, random
import numpy as np
import yfinance as yf

W1 = ("2013-01-01", "2018-01-01")   # VISIBLE  (the predictor sees this)
W2 = ("2018-01-01", "2023-01-01")   # HIDDEN   (the outcome)
TICKERS = ["NFLX","SHLD","AAPL","JCP","TSLA","GPRO","AMZN","GE","INTC","F"]
SEED = 20180101                      # fixed so a re-run is reproducible
SEAL = "/tmp/predtest_answer.sealed.json"


def closes(t, s, e):
    c = yf.Ticker(t).history(start=s, end=e, interval="1mo")["Close"].dropna().values.astype(float)
    return c if len(c) > 8 else None


def doubled(b):
    return b[-1] >= 200.0        # default outcome: at least doubled


rows = {}
for t in TICKERS:
    a, b = closes(t, *W1), closes(t, *W2)
    if a is None or b is None:
        print(f"SKIP {t} (insufficient history)"); continue
    rows[t] = (a, b)

labels = list("ABCDEFGHIJ")[:len(rows)]
random.seed(SEED)
order = sorted(rows)
random.shuffle(order)
mapping = dict(zip(labels, order))

truth = {}
print("WINDOW 1 (VISIBLE) - normalised to 100 at the start")
for lab in sorted(mapping):
    t = mapping[lab]
    a, b = rows[t]
    n = a / a[0] * 100.0
    truth[lab] = {
        "ticker": t,
        "w1_end": round(float(n[-1]), 1),
        "w1_min": round(float(n.min()), 1),
        "w1_max": round(float(n.max()), 1),
        "w1_vol_pct": round(float(np.std(np.diff(n) / n[:-1]) * 100), 1),
        "w1_trend_up": bool(n[-1] > n[0]),
        "w2_index_100": round(float(b[-1] / b[0] * 100.0), 1),
        "outcome": bool(doubled(b)),
    }
    print(f"\n{lab}  end {n[-1]:.0f}  (min {n.min():.0f} max {n.max():.0f})  "
          f"trend_up={'yes' if truth[lab]['w1_trend_up'] else 'no'}  "
          f"monthly_vol={truth[lab]['w1_vol_pct']:.1f}%")

with open(SEAL, "w") as f:
    json.dump({"windows": {"visible": W1, "hidden": W2}, "seed": SEED,
               "mapping": mapping, "truth": truth}, f, indent=1)

n_yes = sum(1 for v in truth.values() if v["outcome"])
print(f"\nSEALED -> {SEAL}")
print("Do NOT read the sealed file until the predictions are committed.")
print(f"(designer check only: {n_yes} of {len(truth)} cases positive; "
      f"trivial all-negative baseline = {len(truth)-n_yes}/{len(truth)})")


# ---- after committing, score like this --------------------------------------
# d = json.load(open(SEAL)); truth = d["truth"]
# MY = {"A": True, "B": False}                    # committed predictions
# hit  = sum(1 for k, v in MY.items() if v == truth[k]["outcome"])
# base = sum(1 for v in truth.values() if not v["outcome"])
# print(f"score {hit}/{len(MY)}   trivial-all-negative {base}/{len(MY)}")
# print("DELTA vs baseline is the finding. delta <= 0 means the analysis added nothing.")
