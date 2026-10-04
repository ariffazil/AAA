#!/usr/bin/env python3
"""Parabolic SAR + Dark-Themed Financial Chart Generator

Usage:
    python3 psar_chart.py GC=F gold       # Gold futures
    python3 psar_chart.py CL=F oil         # Oil futures
    python3 psar_chart.py CL=F oil 360     # Custom lookback days
    python3 psar_chart.py GC=F gold 90 0.03 0.03 0.25  # Custom AF params

Output: /tmp/{label}_psar.png
"""
import sys
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def calc_parabolic_sar(df, af_start=0.02, af_increment=0.02, af_max=0.2):
    """Calculate Parabolic SAR (Stop and Reverse).

    Returns: (sar_array, trend_array) where trend: 1=bull, -1=bear
    """
    high = df["High"].values
    low = df["Low"].values
    n = len(df)

    sar = np.zeros(n)
    ep = np.zeros(n)
    af = np.zeros(n)
    trend = np.ones(n)

    sar[0] = low[0]
    ep[0] = high[0]
    af[0] = af_start
    trend[0] = 1

    for i in range(1, n):
        sar[i] = sar[i-1] + af[i-1] * (ep[i-1] - sar[i-1])

        if trend[i-1] == 1:
            sar[i] = min(sar[i], low[i-1], low[max(0, i-2)])
        else:
            sar[i] = max(sar[i], high[i-1], high[max(0, i-2)])

        if trend[i-1] == 1 and low[i] < sar[i]:
            trend[i] = -1
            sar[i] = ep[i-1]
            ep[i] = low[i]
            af[i] = af_start
        elif trend[i-1] == -1 and high[i] > sar[i]:
            trend[i] = 1
            sar[i] = ep[i-1]
            ep[i] = high[i]
            af[i] = af_start
        else:
            trend[i] = trend[i-1]
            if trend[i] == 1:
                if high[i] > ep[i-1]:
                    ep[i] = high[i]
                    af[i] = min(af[i-1] + af_increment, af_max)
                else:
                    ep[i] = ep[i-1]
                    af[i] = af[i-1]
            else:
                if low[i] < ep[i-1]:
                    ep[i] = low[i]
                    af[i] = min(af[i-1] + af_increment, af_max)
                else:
                    ep[i] = ep[i-1]
                    af[i] = af[i-1]

    return sar, trend


def find_flips(trend_series, n=3):
    """Find last N PSAR trend flips."""
    flips = []
    for i in range(1, len(trend_series)):
        if trend_series[i] != trend_series[i-1]:
            flips.append(i)
    return flips[-n:]


def render_chart(df, label, output_path):
    """Render dark-themed candlestick + PSAR chart."""
    df = df.copy()
    sar, trend = calc_parabolic_sar(df)
    df["PSAR"] = sar
    df["PSAR_trend"] = trend

    # Print signal summary
    last_close = df["Close"].iloc[-1]
    last_psar = df["PSAR"].iloc[-1]
    last_trend = df["PSAR_trend"].iloc[-1]
    signal = "BULLISH (buy)" if last_trend == 1 else "BEARISH (sell)"
    print(f"\n=== {label.upper()} PSAR ===")
    print(f"Last Close: ${last_close:.2f}")
    print(f"Last PSAR: ${last_psar:.2f}")
    print(f"Signal: {signal}")
    print(f"Price {'ABOVE' if last_close > last_psar else 'BELOW'} PSAR")

    # Recent flips
    flip_indices = find_flips(df["PSAR_trend"].values)
    print(f"\nRecent PSAR flips:")
    for idx in flip_indices:
        dt = df.index[idx]
        sig = "BEAR→BULL" if df["PSAR_trend"].iloc[idx] == 1 else "BULL→BEAR"
        print(f"  {dt.strftime('%Y-%m-%d')}: {sig} @ ${df['PSAR'].iloc[idx]:.2f}")

    # --- Chart ---
    fig, axes = plt.subplots(2, 1, figsize=(14, 9), gridspec_kw={"height_ratios": [5, 1]})

    ax1 = axes[0]
    ax1.set_facecolor("#131722")
    fig.patch.set_facecolor("#131722")

    # Candles
    for i in range(len(df)):
        color = "#26a69a" if df["Close"].iloc[i] >= df["Open"].iloc[i] else "#ef5350"
        ax1.plot([df.index[i], df.index[i]],
                 [df["Low"].iloc[i], df["High"].iloc[i]],
                 color=color, linewidth=0.8)
        body_bottom = min(df["Open"].iloc[i], df["Close"].iloc[i])
        body_height = abs(df["Close"].iloc[i] - df["Open"].iloc[i])
        ax1.bar(df.index[i], body_height, bottom=body_bottom,
                width=0.6, color=color, edgecolor=color)

    # PSAR dots
    bull = df["PSAR_trend"] == 1
    bear = df["PSAR_trend"] == -1
    ax1.scatter(df.index[bull], df["PSAR"][bull], marker="^",
                color="#00bcd4", s=15, zorder=5, label="PSAR (Buy)")
    ax1.scatter(df.index[bear], df["PSAR"][bear], marker="v",
                color="#ff9800", s=15, zorder=5, label="PSAR (Sell)")

    # Annotations
    last_date = df.index[-1]
    ax1.annotate(f"${last_close:.1f}", xy=(last_date, last_close),
                 fontsize=10, color="#26a69a", fontweight="bold", ha="left")
    psar_color = "#00bcd4" if last_trend == 1 else "#ff9800"
    va = "bottom" if last_trend == 1 else "top"
    ax1.annotate(f"PSAR ${last_psar:.1f}", xy=(last_date, last_psar),
                 fontsize=9, color=psar_color, ha="left", va=va)

    ax1.set_title(f"{label} — Parabolic SAR Daily", color="white",
                  fontsize=14, fontweight="bold", pad=15)
    ax1.set_ylabel("Price (USD)", color="white")
    ax1.legend(loc="upper left", fontsize=9, facecolor="#1e222d",
               edgecolor="#363a45", labelcolor="white")
    ax1.tick_params(colors="white")
    ax1.grid(True, alpha=0.15, color="#363a45")
    for spine in ["top", "right"]:
        ax1.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax1.spines[spine].set_color("#363a45")

    # Volume
    ax2 = axes[1]
    ax2.set_facecolor("#131722")
    vol_colors = ["#26a69a" if df["Close"].iloc[i] >= df["Open"].iloc[i]
                  else "#ef5350" for i in range(len(df))]
    ax2.bar(df.index, df["Volume"], color=vol_colors, alpha=0.6, width=0.6)
    ax2.set_ylabel("Volume", color="white")
    ax2.tick_params(colors="white")
    ax2.grid(True, alpha=0.15, color="#363a45")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#363a45")
    ax2.spines["bottom"].set_color("#363a45")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor="#131722", bbox_inches="tight")
    print(f"\nChart saved: {output_path}")
    return df


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: psar_chart.py <ticker> <label> [days] [af_start] [af_inc] [af_max]")
        sys.exit(1)

    ticker = sys.argv[1]
    label = sys.argv[2]
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 180
    af_start = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
    af_inc = float(sys.argv[5]) if len(sys.argv) > 5 else 0.02
    af_max = float(sys.argv[6]) if len(sys.argv) > 6 else 0.2

    end = datetime.now()
    start = end - timedelta(days=days)

    print(f"Fetching {ticker} ({days} days)...")
    df = yf.download(ticker, start=start, end=end, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    print(f"Got {len(df)} rows")

    output = f"/tmp/{label}_psar.png"
    render_chart(df, label, output)
