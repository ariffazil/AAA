---
name: AAA-voice-suara-siti
description: "Suara Siti (alias SS / suara SS / voice SS) — the sealed Bahasa Melayu voice clone. Load when any agent must speak as suara Siti, generate BM voice notes, or answer Arif's 'SS' trigger. Contains the working call, the HEX-not-base64 trap, and the never-overwrite-i-ARIF rule."
version: 1.0.0
author: irfanclaw (openclaw/FI-017) for ARIF
forged: 2026-09-26
floor_scope:
  - F1
  - F2
  - F9
  - F11
  - F13
extends:
  - AAA-voice-cloning-mimo-minimax
  - AAA-tts-engine-catalog
  - AAA-audio-emd-pipeline
tags:
  - audio
  - tts
  - voice
  - suara-siti
  - ss
  - minimax
  - identiti
  - f13
owner: AAA
capability_tier: fed-realtime-voice
ecology_state: WARM
---

# AAA · Suara Siti (SS) — Voice Operating Binding

> Kalau Arif cakap **"SS"**, **"suara SS"**, atau **"voice SS"** — ini suara yang dia maksud.
> Jangan teka. Jangan ganti dengan voice lain.

DITEMPA BUKAN DIBERI.

## 1. Identiti

| Field | Value |
|---|---|
| Alias | `SS` · `suara SS` · `voice SS` |
| voice_id | **`SSSiti20260926v1`** |
| Provider | MiniMax |
| Model | `speech-2.8-hd` |
| Endpoint | `https://api.minimax.io/v1` |
| Key | `MINIMAX_API_KEY` (env) |
| Bahasa | Bahasa Melayu |
| Register | female, mid-age, tenang, jelas |
| Clone source | *Apa Cerita?* Ep.26 (29 Jul 2024), window `8499.7–8529.7s` |
| F0 | source 197.1 Hz · clone 207–216 Hz |
| Seal | `SS-VOICE-SEAL-2026-09-26-F13` (F13-authorised local record) |

## 2. Cara Panggil

### 2a. Kanonik (curl)

```bash
curl -s -X POST "https://api.minimax.io/v1/t2a_v2" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "speech-2.8-hd",
    "text": "Teks yang nak disebut.",
    "stream": false,
    "voice_setting": { "voice_id": "SSSiti20260926v1", "speed": 1.0 },
    "audio_setting": { "sample_rate": 24000, "format": "mp3" }
  }'
```

### 2b. RESOLVER (paling senang, kalau ada)

Cari resolver pada host ni (dua lokasi diketahui):

```bash
# KVM4 (forge / openclaw)
/root/.openclaw/workspace/scripts/voice_alias.sh "teks" /path/out.mp3
# KVM2 (azwaos / wawabot)
/root/.hermes/voice/SS/voice_alias.sh "teks" /path/out.mp3
```

Resolver auto-cari key sendiri. Kalau tiada resolver, guna curl §2a dengan key dari
`/root/.secrets/kunci-root.env` (live) — jangan guna `/root/.hermes/.env` kalau ia mati.

### 2c. Telegram voice bubble

```bash
ffmpeg -y -i out.mp3 -c:a libopus -b:a 48k -ar 16000 -ac 1 out.ogg
```

## 3. PITFALL — WAJIB TAHU

1. **`data.audio` ialah HEX, bukan base64.**
   ```python
   raw = bytes.fromhex(resp["data"]["audio"])   # BETUL → mula dengan ID3\x04
   # base64.b64decode(...)                       # SALAH → sampah
   ```
   Semak berjaya: `base_resp.status_code == 0`.

2. **MiMo Token Plan BUKAN engine ni.** `token-plan-sgp.xiaomimimo.com` (`tp-…` key)
   pulangkan `429 quota exhausted`, dan tiada route `/t2a_v2`, `/voice_clone`,
   `/files/upload` (semua 404). Guna **MiniMax direct** `api.minimax.io` (`sk-cp-…` key).

3. **JANGAN tulis ganti i-ARIF.** `SSSiti20260926v1` ialah lane berasingan.
   Voice sovereign i-ARIF kekal `i-ARIF-20260819T084602`. `voice_clone` boleh
   tulis ganti voice_id tanpa amaran — jangan guna semula nama.

4. **Versioning:** tag voice_id baru dengan tarikh (`SSSiti<YYYYMMDD>vN`). Jangan tulis ganti.

## 4. Di Mana Benda Ni Duduk

| Benda | KVM4 (forge) | KVM2 (azwaos) |
|---|---|---|
| Resolver | `/root/.openclaw/workspace/scripts/voice_alias.sh` | `/root/.hermes/voice/SS/voice_alias.sh` |
| Source 30s | `/root/.openclaw/workspace/voice/SS/source_siti_30s.mp3` | `/root/.hermes/voice/SS/source_siti_30s.mp3` |
| Manual penuh | `/root/HERMES/skills/hermes-voice-config/references/ss-siti-voice-2026-09-26.md` | `/root/.hermes/voice/SS/ss-siti-voice-2026-09-26.md` |
| Kad | `/root/.openclaw/workspace/voice/SS/SS-VOICE-CARD.json` | `/root/.hermes/voice/SS/SS-VOICE-CARD.json` |
| Rekod seal | `/root/VAULT999/identity/SS-VOICE-SEAL-2026-09-26-F13.json` (KVM4) | — |

**Key live:** `/root/.secrets/kunci-root.env` (`MINIMAX_API_KEY`, prefix `sk-cp-5_`).
Kalau `status_code=2049 invalid api key`, host tu pegang key mati — betulkan dulu.

## 5. F9 / Governans — jujur

- SS ialah **clone orang sebenar** (Siti Nurhaliza), dibuat atas arahan F13 2026-09-26.
- Dakwaan lama *"not a clone of any real person including Siti Nurhaliza"* telah
  **dipalsukan** oleh kewujudan voice_id ini, dan telah **dibuang** dari kanun
  (2026-09-26). Jangan masukkan semula.
- "Seal" di sini = **rekod berwibawa**, bukan penguatkuasaan kernel. Kernel
  `arif_seal` menolak (actor tidak disahkan kriptografi → `OBSERVE_ONLY`).
- Kalau nak jiwa (rujukan semangat) bukan clone orang sebenar → guna voice
  i-ARIF `i-ARIF-20260819T084602` melalui provider `i-arif-sovereign`.

## 6. Bila Load Skill Ni

- Arif cakap `SS` / `suara SS` / `voice SS`.
- Nak hasilkan voice note Bahasa Melayu dalam suara ini.
- Nak audit provenance voice_id sebelum guna.
- Nak debug output kosong / sampah (pitfall §3.1).

## Integration Points

- **Sibling**: `AAA-voice-cloning-mimo-minimax` (4-phase clone protocol)
- **Catalog**: `AAA-tts-engine-catalog` (routing semua engine)
- **Pipeline**: `AAA-audio-emd-pipeline` (Phase 3 ENCODE)
- **HERMES manual**: `/root/HERMES/skills/hermes-voice-config/references/ss-siti-voice-2026-09-26.md`
- **Kad identiti i-ARIF**: `/root/AAA/agent-cards/identity/i-ARIF/identity-card.json`

---

*Operational binding forged 2026-09-26 by irfanclaw (openclaw/FI-017). F13 authority: Arif bin Fazil.
F2 evidence: live probes (upload 200 / voice_clone 200 / t2a_v2 200) + measured F0 + STT round-trip.*

promoted_from: /root/.claude/skills/AAA-voice-suara-siti
promoted_by: opencode/FI-001
promoted_at: 2026-10-09T15:52:36Z
promotion_basis: KVM4-local original absent from federation library; promoted per sovereign recursive-upgrade directive 2026-10-09
