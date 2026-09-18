#!/usr/bin/env python3
"""Recompute a broker P&L screenshot and print the numbers that decide the grade.

Fill the INPUTS block from the image, then run. Every value is listed so a reviewer
can diff it against the screenshot; nothing is inferred about the instrument.

Prints: book checks, the four denominators, floating-vs-realised, distance-to-zero,
and the leverage split. Deliberately prints NO verdict - the verdict is a judgement.
"""

# --- INPUTS -- read off the screenshot --------------------------------------
IMAGE            = "path/to/screenshot.jpg"   # provenance for the claim
BALANCE          = 0.0     # account currency
EQUITY           = 0.0
FLOATING         = 0.0
MARGIN           = 0.0
FREE_MARGIN      = 0.0
MARGIN_LEVEL_PCT = 0.0
USD_PER_ACCOUNT  = 0.0     # e.g. USD/MYR when the account is not USD
OZ_PER_LOT       = 100.0   # XAUUSD convention
# (lots, entry, now, reported_pnl) -- one tuple per open position
POSITIONS = [
    # (0.2, 4509.45, 4412.96, 7843.87),
]
# ---------------------------------------------------------------------------


def main() -> None:
    print(f"SOURCE: {IMAGE} (read-only; values as displayed)\n")

    # --- Recompute the book: does the screenshot agree with itself? ---------
    print("=== BOOK CHECKS ===")
    print(f"  balance + floating = {BALANCE + FLOATING:,.2f} vs equity {EQUITY:,.2f}"
          f"  (diff {abs(BALANCE + FLOATING - EQUITY):,.2f})")
    if MARGIN:
        print(f"  equity / margin    = {EQUITY / MARGIN * 100:,.2f}%"
              f" vs shown {MARGIN_LEVEL_PCT:,.2f}%")
        print(f"  equity - margin    = {EQUITY - MARGIN:,.2f}"
              f" vs shown free {FREE_MARGIN:,.2f}")

    if not POSITIONS:
        print("\n  no positions supplied - cannot derive implied FX or recheck P&L")
        return

    oz = sum(lot for lot, _, _, _ in POSITIONS) * OZ_PER_LOT
    usd = sum((entry - now) * lot * OZ_PER_LOT for lot, entry, now, _ in POSITIONS)
    fx = FLOATING / usd if usd else 0.0
    print(f"  implied USD/account = {fx:.4f}"
          f"   (stated {USD_PER_ACCOUNT:.4f} - if these disagree the book is inconsistent)")
    for i, (lot, entry, now, reported) in enumerate(POSITIONS, 1):
        print(f"  pos{i} recomputed {((entry - now) * lot * OZ_PER_LOT * fx):,.2f}"
              f" vs shown {reported:,.2f}")

    price = POSITIONS[0][2]
    notional = oz * price * fx

    # --- The four denominators ---------------------------------------------
    print("\n=== THE PERCENTAGE - the denominator decides ===")
    if BALANCE:
        print(f"  vs BALANCE   {FLOATING / BALANCE * 100:,.1f}%   (return on capital)")
    print(f"  vs EQUITY    {FLOATING / EQUITY * 100:,.1f}%   (share that is UNREALISED)")
    if MARGIN:
        print(f"  vs MARGIN    {FLOATING / MARGIN * 100:,.1f}%   (return on collateral)")
    print(f"  vs NOTIONAL  {FLOATING / notional * 100:.2f}%   (exposure {notional:,.0f})")

    # --- Floating vs realised ----------------------------------------------
    print("\n=== FLOATING vs REALISED ===")
    print(f"  unrealised = equity - balance = {EQUITY - BALANCE:,.2f}")
    if MARGIN and EQUITY > MARGIN * 3:
        print("  -> almost the entire result is OPEN. Nothing is banked.")

    # --- Distance to zero ---------------------------------------------------
    if MARGIN and fx and oz:
        print("\n=== DISTANCE TO ZERO ===")
        for mult, label in ((1.00, "margin call"), (0.50, "stop-out   ")):
            move = (EQUITY - MARGIN * mult) / fx / oz
            print(f"  {label}  underlying +{move:,.2f} -> {price + move:,.2f}"
                  f"  ({move / price * 100:.2f}%)")

    # --- Leverage vs skill --------------------------------------------------
    print("\n=== LEVERAGE vs SKILL ===")
    print(f"  every 1.00 of underlying against the position = {oz * fx:,.0f} account units")
    if MARGIN:
        print(f"  exposure / collateral ~ 1:{notional / MARGIN:,.0f}")
    if BALANCE:
        print(f"  exposure / equity     = {notional / BALANCE:,.1f}x")

    # --- Four axes: a judgement, not an arithmetic output -------------------
    print("\n=== GRADE (judgement - fill in; do NOT let the arithmetic decide) ===")
    for axis in ("Direction", "Sizing", "Discipline", "Sample"):
        print(f"  {axis:12} _______")
    print("  sample counts independent DECISIONS, not positions.")
    print("  same direction at two prices = one decision executed twice = N=1.")


if __name__ == "__main__":
    main()
