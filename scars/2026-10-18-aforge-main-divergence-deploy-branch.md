# SCAR-2026-10-18-006 — A-FORGE Main Divergence: Fix Branch Is De Facto Deploy Branch

**Filed:** 2026-10-18 by AGY CLI (Deploy Closeout)
**Weight:** w_scar = 0.95
**Class:** BRANCH_DIVERGENCE + SOT_DRIFT + SILENT_REGRESSION_RISK
**Status:** RESIDUAL_ACTION_REQUIRED

## What happened & Current reality

Pemeriksaan cawangan Git di `/root/A-FORGE` membuktikan bahawa `main` bukan sekadar "ketinggalan satu komit", tetapi berlaku **perpecahan dua cawangan secara struktural (*two-branch structural divergence*)**:

1. Cawangan `fix/test-exit-status-20261016` mendahului `main` sebanyak **7 komit**, merangkumi:
   - `3e17d403` — fail-closed scar reflex (`forgeShell.ts`) + `arif_init validate` timeout
   - `8f50940e` — LiteLLM master key env + cleanup
   - `0dd9bc02` — actor metabolic gate + honest register verdict
   - `03285e87` — AGENTIC-README-DOCTRINE v1 restructure
   - `5ace5fec`, `b1647203`, `6b407ae8` — kemas kini dependensi (@supabase/supabase-js, jsdom, mcp-stack)
2. Cawangan `main` mempunyai **1 komit** yang tiada dalam cawangan `fix`:
   - `a1851072` — `fed: align KVM4 to SOT + unlock voice-clone + harden deploy`
3. Tag rilis rasmi **`v2026.10.16`** terletak di atas cawangan `fix/test-exit-status-20261016`, bukan di atas `main`.

**Kesimpulan:** Cawangan `main` sudah **bukan lagi cawangan deploy sebenar** sekurang-kurangnya untuk satu kitaran rilis penuh.

## Risiko regresi senyap (The Hazard)

Binari langsung (*live binary*) yang sedang berjalan di pelayan membawa pembaikan kritikal daripada komit `3e17d403` (iaitu `SCAR-INDEX-MISSING-FAIL-CLOSED`).

Jika mana-mana ejen atau skrip masa hadapan membina semula (*rebuild*) atau mendeploy A-FORGE daripada cawangan `main`, sistem akan **mengalami regresi senyap (*silent regression*) kembali kepada `SCAR-INDEX-MISSING-FAIL-OPEN`**. Pelajaran yang telah dibayar akan terbatal tanpa sebarang amaran.

## Syor penyelesaian kanonik (Recommended Resolution)

1. **Tetapkan Cawangan Deploy Rasmi:**
   Tandakan dan namakan semula cawangan `fix/test-exit-status-20261016` sebagai cawangan deploy kanonik (contohnya `release/deploy` atau `production`), dan daftarkan peranan ini secara rasmi dalam Source of Truth (SOT).
2. **Rekonsiliasi Komit Main Secara Berasingan:**
   Komit tunggal `a1851072` pada `main` perlu diteliti dan direkonsiliasikan ke cawangan deploy sebagai tugasan audit terasing.

## Larangan keras (Explicit Non-Recommendation)

❌ **HARAM: Jangan sesekali melakukan bulk-merge 7 komit yang belum diaudit ini ke dalam `main` semata-mata untuk "catch up".** Tindakan mencampurkan dependency bumps, kunci persekitaran LiteLLM, dan get metabolik tanpa semakan bebas akan merosakkan integriti audit perlembagaan.
