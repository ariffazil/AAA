#!/usr/bin/env python3
"""Population lift test for a predictive claim.

Question: does SIGNAL carry information about OUTCOME, across the whole panel?

Default demo = 'death cross' (EMA50 < EMA200, monthly) vs a >=50% drawdown in the
next 24 months, over large caps with long history.

Always prints the CONTROL row (no signal) beside the signal row, plus every
denominator. A rate without its n is not evidence.

Read-only. Source: yfinance monthly closes (adjusted).
Edit TICKERS / HORIZON / DRAWDOWN, and swap the signal for your own claim.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import yfinance as yf

TICKERS = ["AAPL","MSFT","AMZN","NVDA","JPM","XOM","WMT","KO","PG","JNJ","DIS","BA",
           "GE","C","F","T","PFE","INTC","CSCO","ORCL","IBM","MCD","NKE","HD",
           "CVX","MRK","VZ","PYPL","NFLX","TSLA"]
HORIZON = 24          # months forward
DRAWDOWN = -50.0      # outcome threshold, percent


def ema(x, n):
    out = np.zeros_like(x, dtype=float); out[0] = x[0]; m = 2 / (n + 1)
    for i in range(1, len(x)):
        out[i] = x[i] * m + out[i - 1] * (1 - m)
    return out


sig, out = [], []
for t in TICKERS:
    try:
        c = yf.Ticker(t).history(period="max", interval="1mo")["Close"].dropna().values.astype(float)
    except Exception:
        continue
    if len(c) < 180:
        continue
    e50, e200 = ema(c, 50), ema(c, 200)
    for i in range(200, len(c) - HORIZON):
        fwd = c[i + 1:i + 1 + HORIZON]
        sig.append(bool(e50[i] < e200[i]))
        out.append(bool((fwd.min() / c[i] - 1) * 100 <= DRAWDOWN))

sig = np.array(sig); out = np.array(out)
if len(sig) == 0:
    raise SystemExit("no observations - check tickers/network")

base = out.mean() * 100
tp = int((sig & out).sum()); fn = int((~sig & out).sum())
fp = int((sig & ~out).sum()); tn = int((~sig & ~out).sum())

sens = tp / (tp + fn) * 100 if (tp + fn) else 0.0
spec = tn / (tn + fp) * 100 if (tn + fp) else 0.0
ppv  = tp / (tp + fp) * 100 if (tp + fp) else 0.0
npv  = tn / (tn + fn) * 100 if (tn + fn) else 0.0

print(f"observations                                   : {len(sig)}")
print(f"base rate  outcome occurs at all               : {base:.1f}%")
print()
print(f"SIGNAL present   -> outcome: {ppv:5.1f}%   (n={tp+fp})")
print(f"signal absent    -> outcome: {fn/(fn+tn)*100:5.1f}%   (n={fn+tn})   <- CONTROL")
print()
print(f"sensitivity (catches the bad ones)             : {sens:.1f}%")
print(f"specificity (correctly clears)                 : {spec:.1f}%")
print(f"negative predictive value                      : {npv:.1f}%")
print(f"lift vs base rate                              : {ppv/base:.2f}x")

print()
if ppv / base < 1.3:
    print("VERDICT: lift near 1 - the signal carries nothing. Do not present it as a predictor.")
else:
    print("VERDICT: some information, but check sensitivity. Low sensitivity = a filter, not a predictor.")
