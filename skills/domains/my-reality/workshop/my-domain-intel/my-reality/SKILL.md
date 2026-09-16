---
name: my-reality
description: "Malaysia reality adapters — prayer (JAKIM), weather/warning (MET), flood (JPS 15-min), FX + Kijang Emas (BNM). Keyless, live-verified. One pulse for daily briefs."
version: 1.0.0
triggers:
  - "waktu solat"
  - "prayer times"
  - "cuaca"
  - "weather"
  - "amaran cuaca"
  - "banjir"
  - "flood"
  - "kadar mata wang"
  - "exchange rate"
  - "harga emas"
  - "kijang emas"
  - "reality pulse"
  - "my-reality"
verified_on: 2026-08-15
---

# my-reality — Malaysia Reality Adapters (P0)

Lived-reality data layer untuk Hermes EDGE. Semua adapter: stdlib-only, keyless,
timeout 15s, fail-loud (exit nonzero + sebab), tiada fallback reka-reka.

## Senarai adapter (semua live-verified 2026-08-15 dari VPS)

| Adapter | Sumber | Kekerapan | Status |
|---|---|---|---|
| `prayer.py` | AlAdhan method=17 (JAKIM), lat/lon Penang default | harian | ✅ verified |
| `weather.py` | api.data.gov.my MET forecast + warning | harian/event | ✅ verified |
| `flood.py` | api.data.gov.my flood-warning (JPS/DID) | 15 minit | ✅ verified |
| `fx.py` | api.bnm.gov.my exchange-rate | harian | ✅ verified |
| `gold.py` | api.bnm.gov.my kijang-emas | harian | ✅ verified |
| `quake.py` | api.data.gov.my earthquake (jarak-dari-MY built-in) | event | ✅ verified |
| `opr.py` | api.bnm.gov.my OPR | mesyuarat MPC | ✅ verified |
| `base_rate.py` | api.bnm.gov.my base-rate (35 bank) | bulanan | ✅ verified |
| `pulse.py` | composite — semua di atas, satu paparan | on-demand | ✅ verified |

## Guna

```bash
python3 /root/.hermes/skills/my-reality/pulse.py                    # pulse penuh (BM)
python3 /root/.hermes/skills/my-reality/adapters/prayer.py          # waktu solat Penang
python3 /root/.hermes/skills/my-reality/adapters/prayer.py 3.1445 101.6958   # KL
python3 /root/.hermes/skills/my-reality/adapters/weather.py         # forecast + warning
python3 /root/.hermes/skills/my-reality/adapters/flood.py           # stesen PP + Selangor
python3 /root/.hermes/skills/my-reality/adapters/fx.py USD          # kadar BNM
python3 /root/.hermes/skills/my-reality/adapters/gold.py            # Kijang Emas 1oz
```

Semua output JSON satu-objek — sesuai untuk cron/caller parse. `pulse.py` keluar
teks BM kompak siap untuk brief.

## Prinsip

1. **Adapter expose reality, jangan reason.** Tiada nasihat, tiada interpretasi —
   data + sumber + timestamp sahaja.
2. **Fail-loud.** Endpoint mati → exit nonzero + sebab. Jangan pernah fabricated
   nombor "daripada ingatan". (Scar: 2026-08-15 ASI lane claim 'adapters forged'
   tanpa kod — F2.)
3. **Keyless-first.** Sumber perlu auth → masuk registry sebagai candidate, bukan
   adapter, sampai ada key governance.
4. **Satu sumber satu kebenaran.** JAKIM waktu solat: AlAdhan ialah wrapper
   method=17; e-Solat ialah autoriti. Jika diverge > 2 minit, flag.

## Registry & roadmap

`MY_REALITY_REGISTRY.json` — P0 verified + P1/P2 candidates (fuel/holiday/transit/
news/dengue/AQI). Candidate = belum verified, JANGAN build tanpa consumer betul
(rule: no abstract feature without concrete consumer).

## Pitfalls

- data.gov.my kadang perlu `User-Agent` header — semua adapter dah set.
- BNM kijang-emas field berubah antara `one_oz`/`buying/selling` — parser
  defensive; jika struktur berubah, adapter keluarkan keys + exit 2, bukan teka.
- Flood API besar (~460 stesen) — adapter filter state, jangan dump semua.
- **BNM memerlukan `Accept: application/vnd.BNM.API.v1+json`** — plain application/json = 404.
  False-negative jenis kedua (bukan path salah, tapi contract salah). Semua adapter BNM dah set.
- **Earthquake feed ialah katalog penuh (800+ event historis)** — adapter filter 7 hari + mag≥4.5.
