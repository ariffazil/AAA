# VOICE MAP — UNIFIED ⚒️
> **Generated:** 2026-09-28 · **Source:** MiniMax API + AAA voice-registry.json + Qwen Cloud enrollments
> **Canonical SOT:** `/root/AAA/audio/voice-registry.json` (resolver source)
> **Pulse:** `source /root/.secrets/kunci-root.env && curl -s -X POST "https://api.minimax.io/v1/get_voice" -H "Authorization: Bearer $MINIMAX_API_KEY" -d '{"voice_type":"all"}'`

---

## ⚡ LIVE PERSONA VOICES (the ones that matter)

| Display Name | Handle | voice_id (MiniMax) | Model | Status |
|---|---|---|---|---|
| **I-ARIF SOVEREIGN** | `iarif` | `ttv-voice-2026082515384726-njTJ5yOR` | speech-2.8-hd | ✅ LIVE V9 |
| **SUARA SITI** | `siti` / `suara siti` | `SSSiti20260926v1` | speech-2.8-hd | ✅ LIVE |
| **ABANG SADO SYED (LIVE)** | `abang sado syed` / `suara syed` | `abang-sado-live-v1` | speech-2.8-hd | ✅ LIVE L1 |
| **PMX ANWAR IBRAHIM** | `pmx` / `suara pmx` / `anwar` | `anwar-bm-20260927` | speech-2.8-hd | ✅ LIVE (HOLD) |
| **Abang Sado Alpha (synth)** | `abang sado syed alpha` | `ttv-voice-2026091602501026-szbvcVGx` | speech-2.8-hd | ✅ LIVE |
| **Abang Sado Clone Ref01** | (internal) | `abangSadoRef01` | speech-2.8-hd | ✅ LIVE |
| **Arif Buddy** | `arif buddy` | `arif-buddy-v1` | speech-2.8-hd | ✅ LIVE |
| **Makcik Penang** | `makcik penang` | `makcik-penang-v1` | speech-2.8-hd | ✅ LIVE |

### Qwen Omni Realtime Voices

| Display Name | Handle | voice_id (Qwen) | Target Model | Status |
|---|---|---|---|---|
| **Pegawai Rasmi Baku** | `pegawai` | `qwen-omni-vc-pegawai-voice-20260924163155364-5cbe` | qwen3.5-omni-flash-realtime | ✅ LIVE |
| **Makcik Sopan Utara** | `makcik utara` | `qwen-omni-vc-makcik-voice-20260924163219880-faea` | qwen3.5-omni-flash-realtime | ✅ LIVE |
| **Abang Sado Omni** | `sado omni` | `qwen-omni-vc-sado-voice-20260924163223561-d6d4` | qwen3.5-omni-flash-realtime | ✅ LIVE |

---

## 🔴 REVOKED

| Voice | voice_id | Reason |
|---|---|---|
| I-ARIF V8 | `i-ARIF-20260819T084602` | Checkpoint contamination — injected unrequested clauses at render time |

---

## 📊 ALIAS MAP (from registry)

```
"abang sado syed"        → abang-sado-live-v1
"suara abang sado syed"  → abang-sado-live-v1
"suara syed"             → abang-sado-live-v1
"abang sado syed alpha"  → abang-sado-alpha
"siti"                   → siti
"suara siti"             → siti
"Siti voice"             → siti
"pmx"                    → anwar-bm-20260927
"anwar"                  → anwar-bm-20260927
"suara pmx"              → anwar-bm-20260927
"suara anwar"            → anwar-bm-20260927
"anwar ibrahim"          → anwar-bm-20260927
"suara anwar ibrahim"    → anwar-bm-20260927
"suara pmx anwar"        → anwar-bm-20260927
```

---

## 🗑️ LEGACY / HISTORICAL (MiniMax voice_cloning)

| voice_id | Created | Status |
|---|---|---|
| `iarif-sovereign-v1` | 2026-08-18 | HISTORICAL |
| `iarif-sovereign-v2` | 2026-08-18 | HISTORICAL |
| `iarif-sovereign-v3` | 2026-08-18 | HISTORICAL |
| `iarif-sovereign-v4` | 2026-08-18 | HISTORICAL |
| `iarif-sovereign-v8` | 2026-08-19 | HISTORICAL (pre-V9) |
| `i-ARIF-20260819T081435` | 2026-08-19 | HISTORICAL |
| `iarif-sovereign-v9` | 2026-08-19 | HISTORICAL (alias now points to ttv variant) |
| `i-ARIF-20260819T084443` | 2026-08-19 | HISTORICAL |
| `i-ARIF-20260819T084602` | 2026-08-19 | 🔴 REVOKED |
| `abang-sado-v1` | 2026-09-16 | HISTORICAL |

---

## ⚙️ PIPELINE

```
Trigger: "suara <handle>" / voice request in any lane
    ↓
Resolver: /root/AAA/audio/voice-registry.json → provider_voice_id
    ↓
Execute: bash /root/AAA/engines/iarif_tts_pipeline.sh <text> <out.wav> "<handle>"
    ↓
Provider: POST https://api.minimax.io/v1/t2a_v2 (speech-2.8-hd)   OR
          Qwen Omni realtime (qwen3.5-omni-flash-realtime)
    ↓
Verify: ASR round-trip (groq whisper-large-v3-turbo) — MANDATORY for cloned voices
```

---

## 🗺️ SYSTEM VOICE COUNT (MiniMax)

| Language | Count |
|---|---|
| Chinese (Mandarin) | 80+ |
| English | 40+ |
| Japanese | 30+ |
| Korean | 25+ |
| Spanish | 25+ |
| Portuguese | 25+ |
| Indonesian | 9 |
| French | 6 |
| German | 3 |
| Russian | 7 |
| Italian | 4 |
| Dutch | 2 |
| Vietnamese | 1 |
| Arabic | 2 |
| Turkish | 2 |
| Ukrainian | 2 |
| Thai | 4 |
| Polish | 4 |
| Romanian | 4 |
| Greek | 3 |
| Czech | 3 |
| Finnish | 3 |
| Hindi | 3 |

**Total system voices: ~300+**

---

## 🔐 DISTRIBUTION RULES

| Voice | Rule |
|---|---|
| I-ARIF SOVEREIGN | F13-private lane only. Never a default for any bot. |
| SUARA SITI | Internal only. Do not publish. |
| ABANG SADO SYED | Shadow mode only. F5-private. Never Hermes assistant default. |
| PMX ANWAR | **DISTRIBUTION_HOLD**. Demo only. Do not publish. Not consented. |
| Abang Sado Alpha | Shadow mode only. 100% synthetic — safe to share. |
| Abang Sado Omni | Realtime audio-to-audio lane only. |

---

## ✅ VERDICT

- **SUARA SITI:** LIVE — `SSSiti20260926v1` on MiniMax speech-2.8-hd ✅
- **ABANG SADO LIVE:** LIVE — `abang-sado-live-v1` on MiniMax speech-2.8-hd ✅ (sovereign's own voice notes)
- **PMX:** LIVE — `anwar-bm-20260927` on MiniMax speech-2.8-hd ✅ (DISTRIBUTION_HOLD)
- **I-ARIF SOVEREIGN:** LIVE V9 — `ttv-voice-2026082515384726-njTJ5yOR` ✅
- **Registry aliases:** 16 handles mapped, 0 broken ✅
- **Distribution labels:** all 3 requested voices have proper labels ✅

*DITEMPA BUKAN DIBERI ⚒️*