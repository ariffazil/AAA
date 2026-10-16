# MENU FORGE SUARA CANON — PMX · Siti · Abang Sado
## Workflow, resources, skills, tools, model, libraries & prompts
### Untuk agen masa depan · 14 Okt 2026 · F13 directed

Status: spec (tested-live engineering workflow reference, non-ratified) — authored 2026-10-14 voice-forge lane under F13 direction; holds no doctrine authority; conflicts defer to /root/AAA/audio/voice-registry.json as SOT.

---

## 1. APA NI

Satu fail rujukan lengkap: macam mana membina, menguji, dan menjaga tiga suara canon federation — PMX, Siti Nurhaliza, Abang Sado Syed. Semua jalan yang diterangkan di sini TELAH DIUJI hidup pada 14 Okt 2026. Bukan teori.

**Perkara paling penting, baca dulu:** suara-selamat ni dilindungi dua lapis —
- **Registry SOT:** `/root/AAA/audio/voice-registry.json`
- **Mint gate:** `/root/.secrets/voice-mint.allow` (tiada nama = tiada klon baru, reka bentuk F13)
- **Klon hidup di sisi provider** (MiniMax, berbayar) — bukan fail tempatan. Padam fail ≠ padam suara. Padam registry entry = putus akses, bukan padam suara.

---

## 2. WORKFLOW PENUH (6 langkah, semua diuji)

**Langkah 1 — Sample sumber.**
Keperluan: 10 saat min, 5 minit maks; mp3/m4a/wav; satu pembisik hanya; latar senyap.
Simpan kekal di `AAA/engines/f5tts/<nama>-source.wav`. Rekod sha256 (diperlukan provenance).
Contoh hidup: `pmx_canon_source.wav` = 12.0s, 24kHz, sha256 `c44ff2e1d1d591a4…`

**Langkah 2 — Kuasa mint (888 brek).**
Tambah voice_id baru (SATU baris) ke `/root/.secrets/voice-mint.allow`.
Gate `/root/scripts/voice_mint_gate.py` akan MENOLAK semua klon yang tak tersenarai. Ini sengaja. Jangan tuaiskan gate; minta F13.
Arahan F13 untuk PMX 2026-10-14: "Ni suara PMX. Please canon."

**Langkah 3 — Clone di provider.**
```bash
python3 /root/scripts/voice_clone.py clone <sample.wav> <voice-id>
```
Skrip ni: muat naik fail → dapat `file_id` → daftar klon di MiniMax → tulis resit ke `~/.hermes/voice-clones.json`.
Kunci dibaca dari `~/.mmx/config.json` (bukan kunci-mas).
Keperluan API: `file_id` WAJIB — muat naik terus ke endpoint `voice_clone` ditolak (error 2013).
Hidup 14 Okt: `pmx-live-v1` cloned, file_id `452153849856538`.

**Langkah 4 — Masuk registry canonical.**
Edit `/root/AAA/audio/voice-registry.json`, tambah entry `voices.<id>`:
```json
{
  "status": "LIVE",
  "display_name": "PMX",
  "provider": "minimax",
  "provider_voice_id": "pmx-live-v1",
  "model": "speech-2.8-hd",
  "sample_rate": 24000,
  "pitch": 0,
  "archetype": "…",
  "lane": "…",
  "source_sample": "/root/AAA/engines/f5tts/pmx_canon_source.wav",
  "source_sample_sha256": "c44ff2e1d1d591a4",
  "provenance": "…tarikh mint, arahan F13…",
  "execute": "bash /root/AAA/engines/iarif_tts_pipeline.sh <text-file> <out.wav> \"<alias>\""
}
```
Tambah aliases: `"pmx"`, `"suara pmx"`, `"pmx voice"` → sama id.
PENTING provenance: id lama `anwar-bm-20260927` = REVOKED, jangan dikaitkan. Rantaian baru = id baru.

**Langkah 5 — Uji melalui pipeline canonical.**
```bash
echo "<ayat uji ≥40 aksara>" > /tmp/t.txt
bash /root/AAA/engines/iarif_tts_pipeline.sh /tmp/t.txt /tmp/out.wav "<alias>"
```
Pipeline resolve: alias → registry → FAIL-CLOSED pada REVOKED/unknown (F1 AMANAH).
**Duration guard:** render < 2s (atau < 0.4×jawataksiran aksara/12) ditolak selepas 3 cubaan. Uji dengan ayat pendek = gagal palsu. Guna ayat ≥ 40 aksara.

**Langkah 6 — Render reference + simpan.**
Simpan satu klip rujukan kekal supaya provenance tak rujuk laluan mati:
`AAA/engines/f5tts/<id>_canon_render_ref.wav`
Contoh hidup: `pmx_canon_render_ref.wav` (6.83s, 32kHz).

---

## 3. TOOLS (semua diuji wujud pada 14 Okt)

| Tool | Laluan | Fungsi |
|---|---|---|
| Pipeline TTS canonical | `/root/AAA/engines/iarif_tts_pipeline.sh` | Satu pintu: resolve registry → synth → duration guard → format out |
| Clone script | `/root/scripts/voice_clone.py` | clone / test / list / delete di MiniMax |
| Mint gate | `/root/scripts/voice_mint_gate.py` | Tolak mint tanpa grant (JANGAN bypass) |
| Grant file | `/root/.secrets/voice-mint.allow` | Senarai id dibenarkan (1 baris = 1 id) |
| Registry SOT | `/root/AAA/audio/voice-registry.json` | Sumber kebenaran semua suara |
| Clone receipt | `~/.hermes/voice-clones.json` | file_id + tarikh clone |
| Skill | `~/.hermes/skills/voice-stack/canon-voice-forge/` (staged 14 Okt) | Prosedur ringkas versi ni |

---

## 4. AI MODEL & LIBRARIES

**Model synth (Tier 1, rented):** MiniMax `speech-2.8-hd` — endpoint `https://api.minimax.io/v1/t2a_v2`, klon via `/v1/voice_clone`.
- Tetapan canonical: `sample_rate 32000, bitrate 128000, format mp3, channel 1, speed 1.0, vol 1.0, pitch 0, emotion neutral`.
- Response audio = hex-encoded → `bytes.fromhex()`.
- **PENTING Siti:** pitch 0 + speech-2.8-hd. Speech-2.6-hd pernah menghasilkan timbre salah (insiden revoke 11 Okt). Recipe Siti canonical = SSSiti20260926v1 + 2.8-hd + pitch 0.

**Failover chain dalam pipeline** (urutan kalau MiniMax cap):
1. MiniMax (Tier 1, rented — ada cap 4-jam berasingan dari cap mingguan)
2. Piper (offline, CPU, sovereign — rung kedua)
3. MiMo — DIFALSIFIKASI untuk BM, jangan guna (nusantara-voice-stack §3)
4. edge — generic, BUKAN clone timbre; jangan sebut sebagai "suara canon"

**Kunci:**
- `~/.mmx/config.json` → `api_key` (untuk voice_clone.py)
- `/root/.secrets/kunci-mas.env` → `MINIMAX_API_KEY` (untuk pipeline; fallback `kunci-root.env`)

**F5-TTS offline lane** (`AAA/engines/f5tts/`, WIP TAK DISEAL):
- Base `F5TTS_v1_Base`: kekal pitch (118Hz vs ref 100Hz) tapi BM cacai ("pasal"→"pazal")
- Finetune `mesolitica/Malaysian-F5-TTS-v3`: BM jelas 14/14 token TAPI pitch +1 oktaf (237Hz) = hilang identiti suara
- Keputusan 29 Sep: PARKED. Jangan buka tanpa hipotesis baru. Jangan belanjakan GPU.
- **Ajaran penting dari lane ni:** verification gate yang hanya banding MFCC cosine BUTA pada F0 — gate verify mesti banding F0 terhadap rujukan.

**Library/dep sistem:** python3 (requests, urllib), ffmpeg/ffprobe (`~/.hermes/tools/ffmpeg-9.0.1/`) untuk convert format (wav/ogg/mp3, libopus 64k), `wave` module untuk duration check.

---

## 5. PROMPTS (guna semua ini, diuji)

**Render uji PMX (lulus duration guard):**
```
Kami sembang pasal kerja, pasal anak, pasal kampung. Nyanyi lagu lama, syukur masih ada.
```

**Render uji Siti:**
```
Assalamualaikum Arif. Siti di sini. Semoga hari ni hati tu tenang sikit, kerja jangan sampai lupa makan.
```

**Render uji Abang Sado:**
```
Weih Arif. Aku sado lagi hang tau. Jangan main-main dengan kontrak kita.
```

**Format mint request kepada F13 (bila ada suara baru):**
```
[VOICE MINT] Nak <display-name>, voice_id <id>, sample <laluan> (<durasi>s, sha256 <8-char>).
Sebab: <…>. Canon atau dengar-dengar je?
```

---

## 6. RESOURCES — fail yang wajib kekal (PROTECTED)

| Fail | Kenapa |
|---|---|
| `AAA/audio/voice-registry.json` | SOT semua suara — padam = buta |
| `/root/.secrets/voice-mint.allow` | Gate kawalan klon — padam = semua mint ditolak (safe-fail, tapi kemudahan rosak) |
| `AAA/engines/f5tts/pmx_canon_source.wav` | Sample sumber PMX (sha256 c44ff2e1) |
| `AAA/engines/f5tts/pmx_canon_render_ref.wav` | Render rujukan PMX |
| `AAA/engines/iarif_tts_pipeline.sh` | Satu-satunya pintu render canonical |
| `/root/scripts/voice_clone.py` · `voice_mint_gate.py` | Alat mint & gate |
| `~/.mmx/config.json` + kunci-mas.env | Kunci MiniMax (JANGAN masuk git/backup awam) |

**Yang BOLEH padam bila-bila:** semua klip output janaan (`/tmp`, `cache/scratch`) — itu hasil, bukan sumber.

**Yang JANGAN sesekali padam:** tiga suara canon di provider, registry, sample sumber, mint gate. Insiden 14 Okt (purge 416MB): yang terselamat sebab berada di provider-side dan registry — bukti reka bentuk ni betul.

---

## 7. SKILLS

- `voice-stack/canon-voice-forge` (staged 14 Okt, tunggu approve) — versi ringkas fail ni, ditulis untuk agent-loaded-on-demand.
- Berkaitan dalam kategori voice-stack: `AAA-tts-engine-catalog` (pilihan enjin), `AAA-voice-cloning-mimo-minimax` (lane MiniMax), `AAA-voice-cloning-qwen-cloud` (lane alternatif).

---

## 8. RUMUSAN SATU AYAT

Sample bermutu + kuasa mint sekali + clone di provider + registry canonical + pipeline test = suara canon. Yang melindunginya bukan fail — tapi gate yang enggan bersetuju tanpa F13.

DITEMPA BUKAN DIBERI
