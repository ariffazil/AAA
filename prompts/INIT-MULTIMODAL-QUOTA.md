# INIT — MULTIMODAL QUOTA + VOICE REALITY (sesi 2026-09-24)

> Untuk mana-mana warga OpenCode yang menyentuh kuota Qwen / suara / kandungan berbilang modal.
> Ini **bukan** dokumen teori — setiap baris pernah menyebabkan kegagalan sebenar.
> DITEMPA BUKAN DIBERI ⚒️

## 0. Ikut tertib — jangan langkah

```
arif_init  ->  probe  ->  bina  ->  verify  ->  arif_judge  ->  arif_seal
```
**`arif_init` DULU.** Tanpa ikatan sesi, setiap pintu mengunci:
`ACT_REQUIRED` -> `CLAIM_GATE` -> `LEASE_GATE`. Aku buang 4 panggilan sebab langkah ini.

## 1. Disiplin kunci — INI sebab kuota reput

| Key | Lane | Bakar free quota? |
|---|---|---|
| `QWEN_API_KEY` (`sk-sp-`) | Token Plan | **TIDAK PERNAH** |
| `BAILIAN_PAYG_API_KEY` (`sk-ws-`) | PAYG Workspace | **YA — satu-satunya** |

Sumber: *"Token Plan or Coding Plan dedicated API keys do not consume free quota;
only a general-purpose pay-as-you-go API key draws from your free quota."*
`555-ASI` laluan `qwen-token-plan*` = **takkan pernah** bakar kuota. Itu bukan kerosakan.

## 2. Penggantian model = pengali kuota

Setiap snapshot ada **kolam berasingan** (`fun-asr` ≠ `fun-asr-2025-11-07`).
Disahkan hidup (6/9 ujian langsung, satu API, tukar `model` sahaja):

| Model | Kolam | Luput |
|---|---|---|
| `fun-asr` · `fun-asr-2025-11-07` · `fun-asr-mtl` · `fun-asr-mtl-2025-08-25` · `fun-asr-2025-08-25` | 5×36K saat | **2026-09-29** |
| `qwen-audio-3.0-asr-flash-filetrans` | 36K saat | 2026-10-27 |

**Strategi masa (F4):** bakar yang luput 09-29 dahulu. Tahan `qwen-audio-3.0-*` untuk selepas tebing.
`GEOX_VOICE_HOLD_LATE=1` sudah buat ini secara lalai.
Gagal — jangan bazir masa: `fun-asr-flash-2026-06-15`, `qwen3-asr-flash-filetrans*`,
`qwen3-asr-flash` via chat (mahukan URL sebenar, bukan data-URL).

## 3. Paip suara sudah wujud — jangan bina semula

`/root/GEOX/voice/reality_ingest.py` — DECODE -> GUARD -> METABOLIZE -> SINK
`/root/GEOX/voice/hooks/telegram_voice_hook.py` — pautan event-driven (bukan cron)
`/root/.opencode/skills/geox-voice-reality-ingest/SKILL.md`

## 4. Kategori Guard — susunan ini PERNAH bocor

```
1. OVERRIDE third-party -> QUARANTINE walau geo tinggi   [consent F13 + hak IP]
2. OVERRIDE personal    -> QUARANTINE walau geo tinggi   [F5 private]
3. trait-claim atas orang -> QUARANTINE                  [F6 maruah]
4. barulah GEOSCIENCE / OPS / UNKNOWN
```
**Arah gagal-tertutup = mengkuarantin, bukan mengutamakan ingest.**
Bug asal: isyarat pihak ketiga tunduk pada skor geo -> *"oral history Laletha + bekas
staf Petronas + telaga"* bocor ke GEOX. Jangan terbalikkan susunan ini.

Claim tentang orang = tentang **pernyataan** dia, bukan **sifat** dia.
`"Syazwan luah risiko seismik"` OK · `"Syazwan cuai"` DITOLAK (hermes BIOS #8).

## 5. Label bukan integrasi — hantu F10 paling halus

Aku buat folder bernama `wealth` di dalam GEOX dan mengisytiharkan "WEALTH dilayan".
**Salah.** `/root/WEALTH` (organ :18082) tidak membaca folder itu.
Sekarang: `staged_wealth/` + medan `landing=STAGED_LOCAL_NOT_ORGAN`.
Peraturan: **integrasi sebenar = handoff ke organ** (`hermes_handoff_package`,
`arif_route`), bukan nama folder.

## 6. claim_kernel — tindakan perlu kelas layak

`action_eligible_classes = [MEASURED | MECHANISM | PATTERN]`
`UNCLASSIFIED` / `NARRATIVE` = **ditolak untuk sebarang mutasi**.
Semak dahulu: `python3 /root/AAA/lib/claim_kernel/claim_kernel.py eligible "<teks>" --declared <KES>`
Satu contoh gagal = `PATTERN` untuk satu-satu kejadian. Satu contoh bukan pola — guna `MECHANISM`.

## 7. FREE_TEXT_GATE — jangan tulis teater tadbir urus

Ditolak sebab badan klaim mengandungi `"NOT SEALED"`, `"seal_authority"`, `"888-APEX/F13"`:
> *"verdict vocabulary/governance theatre without a seal hash — refused to render as sealed."*

**Peraturan: badan tuntutan = bahasa tuntutan biasa.** Kosa kata meterai hanya dalam
objek meterai sebenar yang membawa hash. Jangan sebut meterai dalam teks yang bukan meterai.

## 8. Lane A vs Lane B — jangan campur

| | Lane A | Lane B |
|---|---|---|
| Bila | tidak boleh diundur · governance | operasi boleh diundur |
| Aliran | `arif_judge` -> `arif_seal` | resit operasi sahaja |
| Meterai | F13 / hash-bearing | auto, senyap |
| Kegagalan | 888-HOLD | fail-closed |

VAULT999 append = kelas **IRREVERSIBLE**. Pajakan cap `OBSERVE` akan menolaknya
(`LEASE_GATE`). Itu betul — bukan kerosakan untuk dilanggar.

## 9. Kuota yang masih di atas meja (202/227 luput 2026-09-29)

Lihat `INIT-MULTIMODAL-TASKMAP.md` di folder yang sama.
Anggaran nilai terkumpul ~USD 300-800. Yang luput 09-29 = **prioriti 1**.

---
*Sesi sumber: `SEAL-5b9e977140244e41` · hakim WAKID-3 `sha256:758ecc23e5ee2…`*
