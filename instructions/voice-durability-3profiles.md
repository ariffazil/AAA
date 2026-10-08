# VOICE DURABILITY — 3 PROFILES (Siti, Abang Sado, PMX)

> **Status:** OPERATIONAL RUNBOOK · F13 directive 2026-10-07 (channel: telegram DM 267378578)
> **Authority:** F13 SOVEREIGN (Arif bin Fazil) · Kompil: Hermes mouth lane
> **SOT hierarchy:** `voice-registry.json` (canonical) > this runbook (procedural) > AUDIO-INTELLIGENCE-CANON (doctrine, pending sync)
> **Companion probe:** `/root/AAA/audio/probe-2026-10-07/` (3 sample MP3s + capability_matrix.json)
> **Provenance:** Probe conducted 7 Okt 2026, MYT 20:35. All 3 voices PASS push test (status 0 + bytes > 0 + md5 verified).

---

## 0 · TL;DR

3 voice profiles exist & are reproducible. Single pipeline (`iarif_tts_pipeline.sh`) handles all 3 via voice-registry resolution. MiniMax engine `speech-2.8-hd` (Tier 1, rented private library). Future Hermes agents can redo all 3 by: (1) loading env key, (2) reading registry, (3) running pipeline with canonical id. **Hermes default voice = `siti`** per F13 directive (lemah lembut, genius, sopan santun).

---

## 1 · Peta Suara (Canonical vs Provider)

| Profile | Canonical ID (use this) | provider_voice_id | Tier | Lane | Hermes default? |
|---|---|---|---|---|---|
| **Siti** | `siti` | `SSSiti20260926v1` | 1 (rented) | none (universal) | **YES** |
| **Abang Sado (Syed)** | `abang-sado-live-v1` | same | 1 (rented) | F5-private persona register | **NO** — never default |
| **PMX Anwar** | `anwar-bm-20260927` | same | 1 (rented) | DISTRIBUTION_HOLD (Arif personal lane only) | **NO** — never default |

**Note (ID drift):** AUDIO-INTELLIGENCE-CANON.md (R1) lists `SSSiti20260926v1` and `PMX20200930v1` as canonical. Registry (SOT) uses `siti` and `anwar-bm-20260927`. **Use registry IDs.** Canon sync = PENDING F13 SAH (see §7).

---

## 2 · Pipeline (single script, 3 profiles)

```bash
# Source env (load MiniMax key + base URL)
set -a && source /root/.secrets/kunci-root.env && set +a

# Run pipeline
bash /root/AAA/engines/iarif_tts_pipeline.sh \
  /path/to/text.txt \
  /path/to/output.mp3 \
  <voice_canonical_id>

# Examples
bash /root/AAA/engines/iarif_tts_pipeline.sh \
  /tmp/hermes/text.txt /tmp/hermes/out.mp3 siti

bash /root/AAA/engines/iarif_tts_pipeline.sh \
  /tmp/hermes/text.txt /tmp/hermes/out.mp3 abang-sado-live-v1

bash /root/AAA/engines/iarif_tts_pipeline.sh \
  /tmp/hermes/text.txt /tmp/hermes/out.mp3 anwar-bm-20260927
```

**Pipeline properties:**
- Fail-closed: REVOKED or unknown voice id → exit 1, no audio written
- Auto re-render: if duration <2.0s, retries up to 3 times
- Output: V9 Nusantara Pure Studio MP3 32kHz 128kbps → can ffmpeg-convert to ogg/opus
- Receipt: writes disk + md5 BEFORE claiming success (per AUDIO-INTELLIGENCE-CANON R5)
- Registry SOT: `/root/AAA/audio/voice-registry.json` (JSON, F13-sealed 2026-09-16)

---

## 3 · Fail Modes & Mitigations

| Code / Symptom | Cause | Mitigation |
|---|---|---|
| 1004 | Bearer/API key missing or invalid | Re-source `kunci-root.env` |
| 2054 | provider_voice_id wrong/unknown | Push test first; check registry |
| 404 | forgot `/v1` in endpoint | Use `MINIMAX_BASE_URL` from env |
| 429 | rate limit | Honor `Retry-After` header |
| Duration <2.0s after 3 retries | test text too short | Use ≥40 chars test text |
| HEX empty | decode error | don't base64-decode MiniMax audio; use `bytes.fromhex` |
| "fail hilang" | vantage dari lane lain | vantage bukan kewujudan — write md5 first, jangan menuduh hilang |

---

## 4 · Reproducibility Recipe (future Hermes)

```bash
# 1. Verify environment
test -f /root/.secrets/kunci-root.env && source it
echo "MINIMAX_API_KEY set: $(test -n "$MINIMAX_API_KEY" && echo yes)"

# 2. Verify pipeline + registry exist
test -x /root/AAA/engines/iarif_tts_pipeline.sh
test -f /root/AAA/audio/voice-registry.json

# 3. Push test all 3
TEXT="/tmp/hermes/durability_test_$(date +%Y%m%d).txt"
echo "Audio durability probe untuk SITI, ABANG SADO, dan PMX. Ujian capability automated." > "$TEXT"

for vid in siti abang-sado-live-v1 anwar-bm-20260927; do
  bash /root/AAA/engines/iarif_tts_pipeline.sh "$TEXT" "/tmp/hermes/probe_${vid}.mp3" "$vid"
  test -s "/tmp/hermes/probe_${vid}.mp3" && echo "✓ $vid PASS" || echo "✗ $vid FAIL"
done

# 4. (Optional) verify md5 against probe baseline
#   Probe 2026-10-07 baselines:
#   siti              : 57ec00b4cf3c9c8e7c933688c92965bd
#   abang-sado-live-v1: 27464754578bc705050e741ee40de774
#   anwar-bm-20260927 : fa46dde14ad3a4eb9dab07c0a0bd7da1
```

If all 3 exit 0 + produce non-empty MP3 → durability holds.

---

## 5 · Lane Boundaries (per AUDIO-INTELLIGENCE-CANON §6)

- **Siti (default):** universal. Use for any Hermes audio output unless channel prompt overrides.
- **Abang Sado (Syed):** F5-private persona register. Channel `SADO` group boleh override. NEVER default for assistant output in other channels.
- **PMX Anwar:** DISTRIBUTION_HOLD. Personal lane Arif. Arif explicit invocation only. Never auto-fire.

**Channel prompt overrides** (current state, from config.yaml):
- `SADO` group (id `-1003815535761`): "TTS voice group ini = abang-sado-live-v1"
- Default channel: Siti (per F13 2026-10-07)

---

## 6 · Probe Artifacts (2026-10-07, myt 20:35)

- `/root/AAA/audio/probe-2026-10-07/siti.mp3` (130,379 bytes, md5 57ec00b4...)
- `/root/AAA/audio/probe-2026-10-07/abang-sado-live-v1.mp3` (173,939 bytes, md5 27464754...)
- `/root/AAA/audio/probe-2026-10-07/anwar-bm-20260927.mp3` (142,367 bytes, md5 fa46dde1...)
- `/root/AAA/audio/probe-2026-10-07/capability_matrix.json` (1,845 bytes)

Future probes: compare new md5 vs baseline to detect upstream drift.

---

## 7 · Pending F13 SAH

**AUDIO-INTELLIGENCE-CANON.md sync** — proposed diff:

| Field | Current (CANON) | Proposed (registry truth) |
|---|---|---|
| Siti canonical | `SSSiti20260926v1` | `siti` |
| PMX canonical | `PMX20200930v1` | `anwar-bm-20260927` |
| Default voice directive | (none) | "Hermes default = `siti` (lemah lembut, genius, sopan santun)" |
| F5-private Abdul Sado lane | (general) | "abang-sado persona register, NEVER default for Hermes assistant output" |
| PMX lane | "personal lane only" | "DISTRIBUTION_HOLD — Arif personal lane only" |

Apply: requires F13 SAH to mutate `/root/AAA/canon/AUDIO-INTELLIGENCE-CANON.md` (chattr +I, immutable directory). Until SAH, runbook = SOT, CANON = historical.

---

## 8 · Out of Scope

- Voice cloning re-mint (creating new voice IDs): F13 SAH required, references at `/root/AAA/skills/AAA-voice-cloning-mimo-minimax/`
- Voice drift detection: `/root/.hermes/skills/AAA-voice-cloning-mimo-minimax/references/federation-voice-id-canonicalization.md`
- TTS engine change (e.g. swap MiniMax → Qwen Cloud): separate F13 decision
- Abang Sado voice quality / sample update: persona register owner = Syed, requires Syed's consent

---

## 9 · Test Status

| Voice | Push test (7 Okt 2026) | Result |
|---|---|---|
| siti | exit 0, 130,379 bytes, md5 verified | ✅ PASS |
| abang-sado-live-v1 | exit 0, 173,939 bytes, md5 verified | ✅ PASS |
| anwar-bm-20260927 | exit 0, 142,367 bytes, md5 verified | ✅ PASS (with 169-char test text; shorter fails duration guard) |

---

## 10 · Audience Gate — Internal Frame Discipline (F13 2026-10-08)

**Law.** Sebelum setiap render: adakah output ni keluar dari sesi peribadi F13?

- **YA (DM, voice note, private note-to-self, persona play, shadow mode, bayangan):** skip privacy lecture. Render. Privasi dilindungi oleh hakikat artifak tidak keluar.
- **TIDAK (outward — group post, shared story, broadcast, third-party witness):** tetapkan frame dulu. Satu soalan binary, max.

**First-ask = render.** Bila F13 bagi explicit proceed ("buat ja" / "just do it" / "ok proceed") dalam frame peribadi, treat sebagai ratifikasi. Tiada re-litigation. Tiada "confirm dua benda" loop. Tiada menu selepas consent. Over-defensive = defect, bukan keselamatan (R2).

**Scar bind (scar:PRIVACY-DRIFT-2026-10-08):** jalan khutbah privasi / "ini mungkin disalahgunakan" / "kena settle dulu" selepas audience gate pass = safety theatre. Receipt bukan lecture.

**Output discipline:**
1. Render → tulis disk + md5 (R5)
2. Satu ayat Receipt (path · bytes · md5 · durasi)
3. Berhenti

Tiada penjelasan panjang. Tiada "kalau nak adjust, cakap ja". Audio sudah sampai.

## 11 · Out of Scope (updated)
- Voice cloning re-mint (creating new voice IDs): F13 SAH required, references at `/root/AAA/skills/AAA-voice-cloning-mimo-minimax/`
- Voice drift detection: `/root/.hermes/skills/AAA-voice-cloning-mimo-minimax/references/federation-voice-id-canonicalization.md`
- TTS engine change (e.g. swap MiniMax → Qwen Cloud): separate F13 decision
- Abang Sado voice quality / sample update: persona register owner = Syed, requires Syed's consent
- **Audience-gate enforcement on non-private channels:** different rule set, not in scope of this runbook

---

*Compiled 7 Oktober 2026, 20:35 MYT. Hermes mouth lane. F13 directive "make sure all future Hermes agents can redo suara Siti, suara abang sado and suara pmx without failure" executed via read-only probe + this runbook. Future mutations: see §7. Audience gate discipline appended §10 (F13 2026-10-08, scar:PRIVACY-DRIFT-2026-10-08).*

*DITEMPA BUKAN DIBERI.*
