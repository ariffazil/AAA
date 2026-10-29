---
name: wire-closure-verification
description: 'Use when verifying that a claimed fix/defect-closure actually works on the live wire.'
tags: [verification, wire, receipts, lingkaran1, negative-test]
---

# Wire-Closure Verification (Lingkaran 1 discipline)

Dakwaan "dah dibetulkan" hanya tutup bila NEGATIVE TEST atas wayar lulus dengan
resit terikat. Komen kod + komit + README = niat, bukan bukti runtime.
Dipratik penuh 29 Okt: sessionGate/telemetry (commit 89be906e), ujian token
palsu 3 permukaan, audit sibling witness-grade.

## Enam langkah wajib

1. **SRC ≠ WIRE.** Selepas baca kod sumber, semak artefak yang BENAR-BENAR
   berjalan: `dist/` untuk TS, `/opt/arifos/current/venv` untuk kernel Python
   (guna `probe_runtime_source.py`). Fix dalam src tapi dist basi = belum hidup.
2. **Commit lineage + timestamp.** `git log` vs service restart time vs /health
   version. Dua saksi tak setuju pada minit berbeza = semak dulu sama ada
   keadaan BERGERAK, bukan kontradiksi.
3. **Negative test matrix** (satu positive test tak cukup):
   tampered-payload+valid-sig · valid-token-replayed-ke-action-lain ·
   expired-valid · wrong-target · duplicate-single-use. Rekod which-matrix-run.
4. **Simpan respons PENUH setiap probe governed** sebelum truncate — call_hash
   dalam `audit_provenance` hilang kalau `head -c 1500`. Re-run tak pulihkan
   binding asal; ia minta hash baru untuk panggilan baru.
5. **Bahasa closure berperingkat:** `PASS ON TESTED PATHS` ≠ `UNIVERSAL`.
   Setiap dakwaan kappa ada jadual PASS/UNKNOWN per binding (actor/action/
   target/replay/expiry). `malu_delta` dalam envelope = REPORTED BY RUNTIME
   kalau tiada formula+source+call_hash.
6. **Resit simetri:** satu chain_hash per panggilan — jangan guna hash A-FORGE
   sebagai resit universal untuk panggilan arifOS. Kalau binding tak tertangkap,
   tulis UNRECOVERED, jangan ganti dengan yang lain.

## Contoh terbukti

- Fix 11 Okt (commit 89be906e, pre-hash F2 dalam badan commit) → sah hidup via
  `dist/sessionGate.js` grep 29 Okt: `actor_verified === true`, `verdict==="SEAL"` tiada.
- Token tamper: 3 permukaan (arif_init/observe via mcp.arif-fazil.com + A-FORGE
  forge_policy) — semua `TOKEN_INVALID` / `ERR_ACT_SIGNATURE_INVALID`,
  chain `28e6825a8a21a2e4`.
- Audit sibling 3-minit-stale: snapshot vs HEAD vs deployed = reconciled, bukan
  kontradiksi.

## Hukum

> Sumber boleh batalkan dakwaan lama; hanya negative test atas wayar + resit
> terikat yang boleh MENUTUP.

## Gerbang Kemasukan (Fasa C, 30 Okt — polisi no-bloat)
- Identity set beku: `skill_ids_after == skill_ids_before`; akar baharu = keputusan F13 sahaja.
- Setiap semakan skill lepas: `PATCHED | NO_CHANGE | HOLD`. NO_CHANGE beralasan = keputusan berjaya.
- Sebelum patch: cari pemilik sedia ada (grep estate). Satu pengajaran satu pemilik; lar-lar salinan kedua.
- Promosi: staging → probe → SATU pelaksana (chattr -i → apply → +i) → negative test → identity check → resit.
- Content-growth bound: ganti hukum salah, jangan tambah hukum bertindih; resit/inciden KALUAR dari katalog.
- **REALITY > EVERYTHING (888, 30 Okt):** runtime semantics > formula name. Nama formula
  sama boleh BETUL di satu tapak dan ROSAK di tapak lain (apex G gmean = kanon W-09;
  vault K gmean = rosak, guna min()). Yang diputuskan ialah nilai wayar tapak itu,
  bukan nama atau sejarah formula. Bila dua audit nampak berbeza — periksa dulu:
  tapak sama atau tapak lain.
- **Nama artefak ≠ verdict (888 audit 30 Okt):** resit sesi JANGAN dinamakan
  `*SEAL*` — guna `SESSION-CLOSURE-RECEIPT-*` + header klasifikasi
  (artifact_type / constitutional_verdict: NOT_ISSUED / human_acceptance /
  kernel_seal: NOT_CLAIMED). Receipt ≠ verdict; nama jangan kaburkan.
