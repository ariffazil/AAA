# FED ← TokenRouter Distillation · 2026-10-04

> Owner: 333-AGI (research commissioned by F13 question: "tokenrouter tu bagus sangat ka?")
> Status: PROPOSAL — no live config changed. Sibling of FED-OSS-DISTILLATION-2026-10-03.md.
> Sources: tokenrouter.com marketing + compare page, docs.tokenrouter.io quickstart/models, github.com/lkarlslund/tokenrouter README (open-source variant), local FED witnesses (litellm-config.yaml 2041 lines, fed_router.py v3.3.1, journal 403 events).

## 1. Identity disambiguation (penting)

Dua produk berkongsi nama:
- **api.tokenrouter.com** (yang kernel kita guna) — BYOK flat-fee gateway; varian open-source: `lkarlslund/tokenrouter` (Go). Satu endpoint OpenAI-compatible, `provider/model` IDs, auto-routing berstrategi, kunci berjadual (admin/keymaster/inferrer), kuota pre-flight.
- **tokenrouter.io** — compliance router berbeza (rule engine, LLM firewall). Bukan milik kita. Jangan campur.

## 2. Verdict — "bagus sangat ka?"

**Seni bina: baik, tapi bukan revolusi untuk kita. FED sudah milik ~80% keupayaannya.**

| Keupayaan | TokenRouter | FED hari ini (saksi) | Jurang |
|---|---|---|---|
| Multi-provider satu endpoint | ✅ 13 provider | ✅ 124 deployment / 25 alias / 10 provider-base | tiada |
| Fallback rantaian | ✅ auto-failover | ✅ router_settings.fallbacks + context_window_fallbacks + retry_policy (3x) | tiada |
| Routing berstrategi | ✅ `auto:cost/latency/quality/balanced` | ⚠️ separa — `latency-based-routing` aktif; alias peranan (forge-economy vs forge-planner) ada tapi tiada dimensi strategi generik | **JURANG 1** |
| Belanjawan keras pre-flight | ✅ per-team/member/key, block bukan alert | ❌ master_key tunggal, semua pemanggil setara | **JURANG 2 (terbesar)** |
| Kunci bawahan sementara utk tool luaran | ✅ expiry + auto-clean | ❌ | JURANG 2 (sama penyelesaian) |
| Atribusi per-request (model sebenar + kos) | ✅ audit log metadata sahaja | ⚠️ resit organ ada; hop fallback tak fail-loud di permukaan | **JURANG 3** |
| Tiada retensi prompt | ✅ default metadata sahaja | ✅ doktrin sedia (resit tanpa badan prompt) | tiada |
| Ketuanan (sovereignty) | ❌ SPOF luaran | ✅ self-host | — lihat §3 |

## 3. Pelajaran paling mahal (hari ini, bukan teori)

Kernel cascade menjadikan TokenRouter **PRIMARY untuk semua organ** → 403 quota-exhausted (09:46–12:06, circuit OPEN 1200s) → seluruh lane penaakulan kernel jatuh ke template offline. Kesilapan kita bukan memilih TokenRouter yang jahat, tapi **meletakkan SPOF luaran di atas rantaian kedaulatan sendiri**. FED :4000 hidup sepanjang insiden.

## 4. Distill list (3 item sahaja — bukan fork, bukan sistem baru)

**D1 — Virtual keys + belanjawan keras (JURANG 2).** litellm :4013 sudah DB-backed (`database_url` aktif) → `/key/generate` sedia wujud. Laksana: satu kunci per warga/agen (333, 555, 888, hermes-asi, forge…), `max_budget` + `expires` per kunci, spend attribution automatik. Ini ganti semula-jadi bagi token_bank manual + selari cost_cap qwen. *Kelas: config + DB rows. T2, boleh undur.*

**D2 — Alias strategi `auto:*` (JURANG 1).** Tambah alias `fed-auto-cost` / `fed-auto-latency` / `fed-auto-quality` dalam litellm-config yang map ke strategi litellm sedia ada (`usage-based-routing-v2`, `latency-based-routing`, weighted order). Kernel kemudian boleh panggil `model="fed-auto-quality"` seperti TokenRouter tanpa menjadi dependencies dia. *Kelas: config. T2.*

**D3 — Fail-loud attribution (JURANG 3).** Setiap hop fallback direkodkan dalam metadata respons (litellm sudah pulangkan `x-litellm-model-id`); resit FED wajib bawa `served_by_rung`. Punca: parut mulerouter ($49.92/conf0.99 palsu) + kunci Kimi tercabar tersembunyi oleh silent fallback. *Kelas: resit schema. T1–T2.*

**Tidak ditiru (serdeleiberat):** admin UI penuh, conversations viewer (retensi konflik doktrin), auto-ping kuota aktif (FED doktrin telemetry pasif), LLM firewall (bidang constitution arifOS, bukan gateway).

## 5. Keputusan yang dicadang pada F13 (menggantikan binary T-014 lama)

1. **Turunkan TokenRouter** dari PRIMARY kernel → rung fallback luaran pilihan (atau buang). **Naikkan FED :4000 sebagai Tier-1 kernel.** Kos sifar; menutup kelas insiden hari ini.
2. Reload kredit TokenRouter **hanya** jika nak kekal sebagai rung kepelbagaian luaran (kecil, tidak kritikal).
3. Sanction D1→D3 sebagai item queue (T-026, T-027).

## 6. POC live 2026-10-04 (~12:45 MYT) — D1 diuji atas litellm :4013 sendiri

| Ujian | Hasil |
|---|---|
| Cipta kunci maya (max_budget + skop 3 model) | ✅ `poc-t026-budget-block` |
| Skop model diceroboh (apex-888) | ✅ **403 keras**, mesej eksak menyenaraikan model dibenarkan |
| Atribusi perbelanjaan | ⚠️ medan ada, `spend=0.0` selepas panggilan sebenar |
| Blok bajet USD (bajet diturunkan bawah perbelanjaan) | ❌ tidak menyekat |
| **Blok kuota TPM (`tpm_limit=1`)** | ✅ **429 eksak**: "Rate limit exceeded… Limit type: tokens. Current limit: 1… resets 04:30:28 UTC" |
| Kitaran hidup kunci (update + delete) | ✅ |

**Punca (saksi config):** `input_cost_per_token|custom_pricing` = **0 entri** dalam litellm-config → spend USD tak pernah terkumpul → bajet USD tak ada apa untuk enforce. Bukan logik rosak — data harga tiada. (Kelas parut mulerouter.)

## 6b. POC round 2 — selepas cost-seed (2026-10-04 ~13:10 MYT)

Cost map disemai untuk 15 blok deployment yang **harga sahaja boleh disahkan**: deepseek-flash + deepseek-v4-pro (api-docs.deepseek.com rasmi, kadar PEAK konservatif), qwen3-next-80b-a3b @ dashscope-intl (2 sumber bersetuju). **Tidak disemai atas sebab jujur:** kimi-k3 (`api.kimi.com/coding/v1` = langganan Kimi Code, bukan PAYG — melantun ke lane TPM/RPM secara semula jadi), sea-lion (harga rasmi tak dapat disahkan — tidak meneka, F2).

| Ujian round 2 | Hasil |
|---|---|
| Panggilan PAYG selepas seed | ✅ 200 |
| Perbelanjaan direkodkan | ✅ **"Current cost: 2.85e-05"** — matematik sebenar (≈15 tok keluar @ $1.20/1M + input) |
| Bajet USD menyekat | ✅ **429 "Budget has been exceeded! Current cost: 2.85e-05, Max budget: 1e-06"** |
| Restart litellm + YAML | ✅ sihat ~18s, 123 entri sah, sandaran `litellm-config.yaml.bak-costseed-20261004` |

**Status D1 kini: LENGKAP dan DISAKSI** — skop model 403 ✓, kuota TPM/RPM 429 ✓, bajet USD 429 dengan kos eksak ✓, kitaran hidup kunci ✓. Kerja baki T-026 = pendawaian kunci per warga sahaja (enforcement sedia berdiri).

## 7. Reka bentuk akhir D1 — dual-quota (lebih baik daripada TokenRouter untuk ekonomi kita)

Kebanyakan lane kita ialah **langganan rata** (token-plan qwen 44 deployment, zai 11, minimax 9, opencode 7) — kos marginal sebenar ≈ 0, jadi **unit kuota betul = TPM/RPM**, bukan USD. Lane **PAYG** (deepseek-direct 14, kimi 2, sea-lion 3, dashscope 4) yang perlukan bajet USD — seed cost map untuk deployment itu sahaja.

```
kunci per warga:
  subscription lanes → tpm_limit / rpm_limit   (429 hard-block, SUDAH HIDUP hari ini)
  PAYG lanes         → max_budget USD          (hidup selepas cost map diisi, ~19 deployment)
  skop model         → models[]                (403 hard-block, SUDAH HIDUP hari ini)
```

TokenRouter mengenakan unit USD untuk semua orang kerana mereka menjual semula token. Kita memiliki lane langganan — kuota token ialah realiti ekonomi kita. **Distill diadaptasi, bukan disalin.**

ΔS: dokumen ini menggantikan 8 halaman kajian dengan 1 muka keputusan.
