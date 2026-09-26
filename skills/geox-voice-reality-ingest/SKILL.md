---
name: geox-voice-reality-ingest
description: "Convert voice notes to searchable GEOX subsurface knowledge."
version: 1.0.0
author: 333-AGI for ARIF
forged: 2026-09-24
floor_scope: [F1, F2, F4, F5, F6, F7, F9, F10, F11, F13]
extends: [AAA-audio-emd-pipeline]
tags: [geox, voice, asr, reality-capture, scar, claim, emd, knowledge-graph, sabah, kinabalu, kuota]
owner: GEOX
capability_tier: fed-long-context
ecology_state: HOT
---

# GEOX · Voice Reality Ingestion

> "Orang biasa guna kuota audio untuk suruh AI bercakap.
>  Hang guna untuk paksa GEOX mendengar."

Aset kecil bukan suara AI. Aset kecil = **11 tahun realiti Sabah Basin yang hanya
wujud dalam kepala, bilik review, dan perbualan koridor** — dan ia hilang bila
orang bertukar jabatan.

Modul: `/root/GEOX/voice/reality_ingest.py`

## Kenapa ini, bukan TTS

| | TTS (AI bercakap) | ASR (GEOX mendengar) |
|---|---|---|
| Kuota | ~10K aksara/model | **~36K saat/model (~10 jam)** |
| Variasi | ~16 | **~14 (× snapshot = kolam berasingan)** |
| Aset terhasil | bunyi, sekali dengar | **rekod kekal boleh dicari** |
| Nilai | perhiasan | **memori institusi** |

## Kejuruteraan kuota (F2: ini bukan tekaan — disahkan langsung 2026-09-24)

**Dua kunci, dua perangai:**

| Key | Lane | Bakar free quota? |
|---|---|---|
| `QWEN_API_KEY` (`sk-sp-`) | Token Plan | ❌ **TIDAK PERNAH** |
| `BAILIAN_PAYG_API_KEY` (`sk-ws-`) | PAYG Workspace | ✅ **YA — satu-satunya** |

Sumber: dokumen Alibaba — *"Token Plan or Coding Plan dedicated API keys do not
consume free quota; only a general-purpose pay-as-you-go API key draws from your
free quota."*

**Penggantian model = pengali kuota.** Setiap snapshot ada kolam **berasingan**
(dokumen: *"treated as two independent models with separate quotas"*).

Dihidupkan (6/9 lulus ujian langsung, satu API, tukar `model` sahaja):

| Model | Kolam | Luput | Status |
|---|---|---|---|
| `fun-asr` | 36K saat | 2026-09-29 | ✅ |
| `fun-asr-2025-11-07` | 36K saat | 2026-09-29 | ✅ |
| `fun-asr-mtl` | 36K saat | 2026-09-29 | ✅ |
| `fun-asr-mtl-2025-08-25` | 36K saat | 2026-09-29 | ✅ |
| `fun-asr-2025-08-25` | 36K saat | 2026-09-29 | ✅ |
| `qwen-audio-3.0-asr-flash-filetrans` | 36K saat | **2026-10-27** | ✅ |

Gagal (jangan bazir masa): `fun-asr-flash-2026-06-15` (url error),
`qwen3-asr-flash-filetrans[-2025-11-17]` (task FAILED),
`qwen3-asr-flash` via chat (mahukan URL sebenar, bukan data-URL).

**Strategi masa (F4):** bakar dahulu yang luput **2026-09-29**. Tahan
`qwen-audio-3.0-*` (luput 2026-10-27) untuk **selepas tebing**.
Default `GEOX_VOICE_HOLD_LATE=1` sudah buat ini.

## Saluran berimpak (ikut turutan nilai)

1. **Post-Review Scar Recorder** — 2 minit dalam kereta lepas CP review →
   `contested_issue`, `seismic_risk`, `scar_candidate`, `constraint`.
   Ini SCAR→LAW→ECHO, dan Scar Law memang dah wujud (`forge_scar`) — cuma
   tak pernah disambung dari suara.
2. **Kinabalu / Sabah Oral History** — kenapa WAKID-3 dipropos, andaian apa
   yang salah, siapa betul. ⚠️ **F13: perlu consent + semakan hak IP PETRONAS.**
   Mesin mengkuarantin, manusia memutuskan.
3. **Personal Cognitive Offload** — senarai tindakan petang → kad briefing.
4. **Geological Audio Notebook** — 10 minit satu-satu projek → arkib cari.

## Sempadan yang mesin TIDAK akan langgar

**Kategori Guard — gagal-tertutup.** Susunan keputusan JANGAN dibalikkan:

```
1. OVERRIDE third-party  -> QUARANTINE walau geo tinggi   [consent F13 + hak IP]
2. OVERRIDE personal     -> QUARANTINE walau geo tinggi   [F5 private]
3. trait-claim atas orang -> QUARANTINE                   [F6 maruah]
4. barulah GEOSCIENCE / OPS / UNKNOWN
```

Arah gagal-tertutup = **mengkuarantin**, bukan mengutamakan ingest.
(Ujian asal 3/6; bug: oral history + Petronas bocor ke GEOX kerana isyarat
third-party tunduk pada skor geo. Betulkan: OVERRIDE dulu. Kini lulus semua
kes adversarial.)

**Truth ceiling (F2 + state-transition-discipline):**
- Suara = `Claimed`, **bukan** `Measured`. `truth_class` SEMUA = `REPORTED`.
  Tidak pernah `OBSERVED` dari ingatan suara.
- `Stored ≠ Retrieved ≠ Relevant ≠ Current` — state = `INGESTED_UNSUPERSEDED`,
  expected_next = `CROSS_VALIDATE → DER/OBS | RETRACTED | SUPERSEDED`.
- Setiap claim **wajib** ada `falsification_path`. Tanpa laluan bantahan = SPEC.

**Claim tentang orang (hermes BIOS #8):** tentang **pernyataan** dia, bukan
**sifat** dia.
```
BETUL: "Syazwan luah risiko kesinambungan seismik"   -> attributed_statement
SALAH: "Syazwan cuai"                                 -> REJECTED_TRAIT_CLAIM
```

## Arahan

```bash
# guard sahaja (tiada API, tiada kos)
python3 /root/GEOX/voice/reality_ingest.py guard "teks di sini"

# satu fail (audio ATAU .txt transkrip)
python3 /root/GEOX/voice/reality_ingest.py ingest nota-review.ogg
python3 /root/GEOX/voice/reality_ingest.py ingest nota.txt --dry-run

# batch (bakar kuota berganda — setiap model kolam sendiri)
python3 /root/GEOX/voice/reality_ingest.py batch /root/.hermes/workspace --glob '*.ogg' --dry-run

# lihat berapa kuota sudah terbakar
cat /root/GEOX/voice/out/quota_burn.jsonl
```

**Amaran batch:** fail dalam `/root/.hermes/workspace/` sekarang kebanyakannya
`syed-*` / `sado-*` / `magnesium-*` — itu content **peribadi** (F5). Guard akan
kuarantinkan ia. Itu betul. Jangan `--force` ke GEOX.

## Keluaran

| Fail | Isi |
|---|---|
| `out/geox_claims.jsonl` | sampul claim penuh (truth_class, falsification_path) |
| `out/scar_candidates.jsonl` | scar **CANDIDATE** — 888/F13 yang SEAL, bukan mesin |
| `out/receipts.jsonl` | resit `{state, prev_state, expected_next, owner}` |
| `out/quota_burn.jsonl` | saat dibakar per model (audit kuota) |
| `quarantine/*.json` | apa yang TIDAK masuk GEOX, dan kenapa |

## Pautan Telegram (event-driven, bukan cron)

```python
# di hook voice sedia ada (anchor: voice-state-membrane):
#   event._gateway_pending_stt_transcripts = list(successful_transcripts)
from reality_ingest import ingest_file   # /root/GEOX/voice
result = ingest_file(Path(audio_path), kind="voice_note")
```

Atau: `python3 /root/GEOX/voice/hooks/telegram_voice_hook.py <fail_audio>`

DITEMPA BUKAN DIBERI ⚒️


> **Full description (pre-EO-01 intent-first pass, preserved):** GEOX Voice Reality Ingestion — penukar suara manusia jadi entiti realiti GEOX yang boleh dicari. BUKAN chatbot suara. DECODE (ASR, bakar kuota PAYG percuma) -> KATEGORI GUARD (F6/F13 sempadan) -> METABOLIZE (claim struktur + falsification_path) -> SINK (GEOX claim ledger + scar + resit). USE WHEN: 'voice note jadi pengetahuan GEOX', 'rekod CP review', 'scar dari suara', 'sejarah lisan telaga', 'oral history', 'transkrip jadi claim', 'kuota ASR Qwen', 'GEOX witness recorder', 'cognitive offload suara'. NOT untuk: TTS, voice clone, atau content peribadi/relationship (route ke relationship-memory-isolation).
