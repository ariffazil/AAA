---
name: evidence-bound-pdf
description: 'Use when producing a PDF report deliverable.'
tags: [pdf, evidence, qa, delivery]
---

# Evidence-Bound PDF + Governed Delivery

Naik taraf atas pdf-report-generation untuk deliverable yang mesti tahan audit luar. Terbukti penuh sesi snapshot 29 Okt v1→v3 (v1 kena audit tajam, v3 lulus).

## Enam hukum wajib

1. **Tiada angka rekaan dilabel OBS.** Kategori sahaja tanpa formula diterbit. Kesilapan v1: array `ready=[0.6,...]` taip manual, label [OBS] — F2 violation sendiri.
2. **Claim ID inline + Lampiran daftar dakwaan.** Setiap angka material ada C-001..N (dakwaan/sumber/arahan/masa/kelas OBS|MEASURED|RPT). Chart compiler terima claim_id, bukan nombor ditaip bebas.
3. **Visual QA fail-closed SEBELUM delivery.** Hermes vision boleh 404 — lane alternatif terbukti: `zai_vision analyze_image` (satu imej/call) dan `media_ingest media_vision_read` (3 PNG/call, param `question`, pulang truth_state OBSERVED). Bila semua muka kembali OBSERVED: 404 bukan bukti sifar defect — ia keputusan QA lane, tulis tarikh + lane dalam footer, dan REVALIDATE tiap render (jangan beku keputusan lane jadi doktrin kekal). `pdfimages ok` ≠ visual ok. Kalau tiada lane vision langsung: label artifact UNVERIFIED_VISUAL, jangan auto-hantar.
4. **HTML SATU fail** — jangan gabung fragmen terpotong (v1: heading berganda). Kadar % bukan jumlah mentah bila denominator beza; denominator ditulis dalam carta.
5. **Manifest sebelah PDF:** `<nama>.claims.json` (artifact sha256, v_changes, claims array, visual_qa). Resit QA visual ditulis DALAM dokumen (footer). SHA256 dihantar dalam caption Telegram.
6. **Gap diakui, bukan disembunyi.** Bila author=verifier=sender satu sesi, tulis terang dalam footer: pemisahan governed-publication belum wujud.

## Gaya yang lulus audit luar

- Status kategori (HEALTHY/DEGRADED/DRIFT) bukan skor rekaan.
- Roadmap = baris berfasa dengan gerbang lulus, bukan lingkaran bertindih.
- Legend di bawah plot, bukan atas bar.
- Dakwaan kelebihan seni bina sendiri sahaja, bukan superiority pasaran.
- Bahagian "Apa yang aku tak tahu" wajib.

## Contoh lengkap (v3 lulus)

/root/forge_work/snapshot-20261029/ (build_charts_v3.py, report_full_v3.html, snapshot-20261029-v3.pdf, claims.json)
