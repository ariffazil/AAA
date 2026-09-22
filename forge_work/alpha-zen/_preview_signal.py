#!/usr/bin/env python3
"""Render the SIGNAL-ONLY preview ALONGSIDE the current build_html output.

Read-only with respect to the shared renderer: it imports alpha_zen_card and
calls the functions directly, so neither build_html nor render() is touched.
This exists because `signal only` has two readings and prose cannot settle it:

  A) DECLUTTERED GRID  — same 9 rows x 2 columns, decoration removed
  B) SIGNAL PROJECTION — 4-8 sentences, ranks collapsed to what matters today

Both are rendered from today's REAL card content; only the presentation differs.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/root/AAA/scripts")
import alpha_zen_card as az  # noqa: E402

OUT = Path("/root/AAA/forge_work/alpha-zen/_preview")
OUT.mkdir(parents=True, exist_ok=True)

# --- B: the projection. Every line grounded in today's delivered card ---
signals = [
    {"who": "shared",
     "text": "Selat Hormuz masih tutup, tapi Brent bacaan sistem 99.36 dan trend dia "
             "DOWNTREND keyakinan 0.95. Pasaran dah bayar perang tu lebih awal — "
             "yang tinggal cuma siapa tersangkut bila lega.",
     "source": "WEALTH capital_market oil 2026-09-21"},
    {"who": "arif",
     "text": "PETRONAS untung RM27.2 bilion separuh tahun, tapi dividen 2026 dipotong 38% "
             "jadi RM20 bilion — terendah sembilan tahun. Minyak naik, kerajaan dapat "
             "kurang, sebab bil subsidi naik lebih laju dari harga.",
     "source": "PETRONAS H1 2026 / MOF dividend 2026"},
    {"who": "syed",
     "text": "Emas 4,363.30, EMA masih susun bullish, RSI 59.3. Tapi verdict sistem "
             "SABAR — reward-to-risk cuma 1.0. Arah betul, harga belum bagi.",
     "source": "WEALTH capital_market gold 2026-09-21 07:16 MYT"},
    {"who": "shared",
     "text": "Fed naik 25 basis mata 16 September — kali pertama sejak 2023. BoJ ikut, "
             "1.25%, paras tertinggi dalam 31 tahun. Dua-dua ketat, dan pasaran masih "
             "duduk diam.",
     "source": "CNBC / Reuters 2026-09-18"},
    {"who": "syed",
     "text": "ACSM keluar Position Stand latihan rintangan 2026 — kemas kini pertama "
             "dalam tujuh belas tahun, 137 kajian, lebih 30,000 peserta. "
             "Mesej dia satu: konsisten kalahkan sempurna.",
     "source": "ACSM Position Stand 2026 / PubMed 41843416"},
    {"who": "arif",
     "text": "Yang di-Pertuan Besar batalkan semua pelantikan exco Negeri Sembilan, dan "
             "AGC kata exco tak pernah ada kuasa buat kenyataan tu. Kuasa bukan benda "
             "yang kau dakwa — ia benda yang orang bagi.",
     "source": "FMT / NST / Malay Mail 2026-09-20"},
    {"who": "shared",
     "text": "MET Malaysia masih amaran angin kencang dan laut bergelora sampai 24 "
             "September, ombak sampai 3.5 meter — aktiviti air bahaya. "
             "Darat Pulau Pinang pula ramalan kering sepanjang hari.",
     "source": "MET Malaysia warning API, dibaca 2026-09-21 09:5x MYT"},
]

card_b = {
    "mode": "morning",
    "date": "2026-09-21",
    "headline": "Minggu ni semua benda yang sepatutnya bising — dan pasaran jawab "
                "paling kuat masa dia senyap.",
    "signals": signals,
    "yin_quote": {"text": "x", "author": "x"},
    "yang_quote": {"text": "x", "author": "x"},
    "rows": json.loads(
        Path("/root/AAA/forge_work/alpha-zen/cards/2026-09-21-morning.json").read_text()
    )["rows"],
}

html_b = OUT / "signal-B.html"
html_b.write_text(az.build_signal_html(card_b), encoding="utf-8")

png = OUT / "PREVIEW-B-signal-only.png"
r = subprocess.run(
    ["google-chrome", "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
     "--default-background-color=FFFFFFFF", "--window-size=1080,4200",
     f"--screenshot={png}", f"file://{html_b}"],
    capture_output=True, text=True, timeout=180,
)
if not png.exists():
    raise SystemExit(f"render B failed: {r.stderr[:400]}")
w, h = az._autocrop(png)

# --- A: the current shared renderer's output, re-rendered clean ---
card_a = json.loads(
    Path("/root/AAA/forge_work/alpha-zen/cards/2026-09-21-morning.json").read_text()
)
html_a = OUT / "grid-A.html"
html_a.write_text(az.build_html(card_a), encoding="utf-8")
png_a = OUT / "PREVIEW-A-grid.png"
r2 = subprocess.run(
    ["google-chrome", "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
     "--default-background-color=FFFFFFFF", "--window-size=1080,4200",
     f"--screenshot={png_a}", f"file://{html_a}"],
    capture_output=True, text=True, timeout=180,
)
if not png_a.exists():
    raise SystemExit(f"render A failed: {r2.stderr[:400]}")
w2, h2 = az._autocrop(png_a)


def noise(path: Path) -> dict:
    """What machine scaffolding is still visible in the rendered page?"""
    t = path.read_text()
    toks = ["KENA TAHU", "SUKA TAHU", "EUREKA", "ARIF", "SYED", "KOMPONEN",
            "SIGNAL", "class=\"src\"", "YIN", "YANG"]
    return {k: t.count(k) for k in toks}


print(f"A  grid   : {png_a.name}  {w2}x{h2}   {noise(html_a)}")
print(f"B  signal : {png.name}    {w}x{h}   {noise(html_b)}")
print(f"B signals counted by the card itself: {len(signals)}")
