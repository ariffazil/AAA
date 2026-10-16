# DOKTRIN SETPOINT FQ — Lane A (F13: "a sah", 2026-10-15)

**Status:** F13-disahkan dalam sesi (kata asal: "a sah"). Naik kanon: perlu ritual Lane A
(arif_seal + f13_ack) apabila pengangkutan identiti membenarkan; artifak ini resit sesi.

## Keputusan

Setpoint FQ **terbit dari kalibrasi CHRON** (Laluan A). Ia bukan pemalar manual.
Tiada pemalar baharu direka sementara menunggu — jalur sedia ada (`fq_required`
ikut risk_class, lantai 0.1) kekal sehingga pencetus tiba.

## Pencetus matematik

CHRON **n ≥ 50 ramalan disahkan** (OBS 2026-10-15: n=27, ketepatan 0.873,
Brier 0.149, CI95 [0.59, 0.89]). Pada n≥50, terbitkan jalur fasa-relatif:

    FQ_band(fasa) = f(skor Brier aktor-atas-fasa, risiko kelas)

Fungsi tepat ditulis HANYA pada pencetus — menulisnya hari ini (n=27, CI lebar)
adalah Larutan B yang menyamar sebagai A.

## Pemalsu

1. Pada n≥50, kalau CI95 Brier masih >0.2 lebar → lanjut menunggu (doktrin ini
   membatalkan dirinya sehingga data cukup).
2. Kalau jalur terbit menahan aktor yang skor kalibrasinya baik (jalur bercanggah
   dengan kalibrasi) → formula salah, bukan aktor salah.

## Garis keturunan (lineage)

- Soalan binari F13 (2026-10-15, sesi arifFLOW doctrine): "Laluan A atau B?"
- Jawapan F13: "a sah"
- Rantai bukti: saksi tolok (serpihan identiti, semak mekanikal), fq_g ukur-dahulu
  ("ambang sengaja tidak dicipta"), doktrin loop fasa-relatif ARIF 2026-10-15.
- Induk doktrin: APEX-ZEN alignment (F13-ratified 2026-09-16); arifFlow AGENTS.md
  (ukur-dahulu; eskalasi hanya topologi/retensi/pecah protokol).
