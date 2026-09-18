# Volatility Envelope — the honest substitute for a forecast

## Compute

```python
h = yf.Ticker("GC=F").history(period="3y", interval="1wk")["Close"].dropna()
vol = np.diff(np.log(h.values)).std() * np.sqrt(52)      # realised annual vol
sd_T = vol * np.sqrt(T)                                   # T in years
pct = lambda z: spot * np.exp(z * sd_T)                   # lognormal percentiles
# z = +/-0.67 -> 25th/75th ; z = +/-1.28 -> 10th/90th ; median = spot
```

Use 10+ years of weekly returns for a stable estimate, and say which window you used — a 3-year and a 20-year estimate differ enough to change the conclusion.

Present as a **fan** opening from the current price: nested bands (25–75 inner, 10–90 outer), median line at spot, percentile values labelled at the right edge. The fan is a statement about width, not direction, and the chart subtitle must say so.

## The move that lands: distance measured in noise

Overlay the position on the fan, then express the stop distance in units of `sd_T` rather than in dollars:

```
touch_probability ~= 2 * (1 - Phi(distance / sd_T))   # two-sided first-passage
```

A stop sitting a fraction of one `sd_T` from price is inside the band of ordinary movement. The conclusion to state is not "your analysis is wrong" but:

> **"The stop can be hit by normal movement, without anyone being wrong. That is a sizing error, not an analysis error — the fix is size, not a better view."**

Put that sentence in the image footer, not only in the prose.

## State the size identity plainly

```
P&L = market_move_pct x (position_notional / capital)
```

Leverage does not create return; it pulls future outcomes into the present and pulls the risk in with them. A sub-1% market move can be a several-hundred-percent account outcome, which means the account's survival is decided by the multiplier, not the view. Retail CFD outcomes are zero-sum between longs and shorts minus cost, and the counterparty is frequently the broker itself — so a large leverage allowance is a statement about who is expected to lose, not a gift.

Practical consequence to hand the human: the number of consecutive losses a given risk-per-trade survives (1% survives ~69 before halving, 5% survives ~14, 50% survives 1) is the whole decision. Size is the only variable the trader fully controls; direction is not.

## What to refuse

Do not answer "what will the price be". Do not attach a probability to a direction. Do not present the median of the fan as a target — it is the current price, and that is the point.

## Verifying a predictive engine before using it

Check the service health/calibration endpoint for `verified` count and measured `accuracy` before quoting anything downstream of it. A prediction store with many active entries and zero verified outcomes has no accuracy claim at all, and "no data" must never be rendered as "everything is fine". Report the engine as uncalibrated and answer from the envelope instead.
