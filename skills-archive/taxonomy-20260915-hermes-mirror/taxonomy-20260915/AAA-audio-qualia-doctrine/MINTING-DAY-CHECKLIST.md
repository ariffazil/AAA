# i-ARIF Minting Day Checklist

> **One-page cheat sheet.** Print, fill in as you go. F13 territory.
> Sealed: 2026-08-18 · Owner: Muhammad Arif bin Fazil · Operator: Hermes v2026.3.17

---

## 0. Status Snapshot (sealed today)

- **Pipeline ready:** `/root/forge_work/i-arif-voice/voice_clone_pipeline.py` (297 lines, --identity default)
- **Existing samples in archive:**
  - `/root/forge_work/i-arif-voice/archive/2026-08-18-pre-clone/i-arif-voice-source-2026-08-12.mp3` (166 KB, 2026-08-12)
  - `/root/forge_work/i-arif-voice/archive/20260818T133423Z/i-arif-voice.mp3` (166 KB, RECEIPT sealed)
- **Pending swap:** `__PENDING_CLONE__` di config.yaml line 1469 (F13-gated patch)
- **Dormant blueprint:** `/root/.hermes/voice_filters.py` v0.1.0 (HOLD — wire post-mint)
- **Skills (doctrine):** `/root/AAA/skills/AAA-voice-cloning-mimo-minimax/`, `AAA-voice-cloning-qwen-cloud/`, `AAA-tts-engine-catalog/`, `AAA-audio-emd-pipeline/`, `AAA-asr-glm-ingest/`

---

## 1. Pre-flight (T-30 min) — physical room

| Item | Spec | Verify |
|---|---|---|
| Room | ≤ 10 m² enclosed, NO conference hall / classroom | ☐ |
| Windows + doors | Closed | ☐ |
| AC / fan / fluorescent | OFF (ballast hum paling sneaky) | ☐ |
| Acoustic treatment | Foam / curtain / carpet — break flat reflections | ☐ |
| Mic position | 10 cm dari mulut (~4 in). Plosive-free zone | ☐ |
| Recording device | Smartphone / digital recorder — 44.1 kHz / 16-bit mono minimum | ☐ |
| Sample target | 2–3 min (MiniMax) atau 10–20 s (Qwen) | ☐ |
| Output format | WAV (16-bit) atau MP3, mono preferred | ☐ |
| File size cap | ≤ 10 MB | ☐ |

---

## 2. Recording session

**Script guidance (3-sentence minimum continuous speech):**

```
"Ia Arif. Sistem engineer, 36 tahun, duduk Pulau Pinang. Pagi ni aku tengah debug
production server — case SSL handshake timeout, HTTPS kadang-kadang drop. Aku check
log dulu, baru decide nak restart nginx atau rollback cert."

"... ok jom. F13 sovereign verdict sealed. Stop loss 3200, lot size 0.5. Trade
confirm."

"Server ni half-up. Ada satu decision kena buat dalam 5 minit — restart nginx
ke rollback cert. Aku dah cross-check second-order effects. Satu je: restart dulu."
```

**Delivery rules (per iarif_persona.md Hard Rules):**

- ✅ Chest register, dry, controlled. NOT theatre.
- ✅ Complete sentences, NO "hello" / "yes" alone.
- ✅ Emotional variation — calm-confident → urgency → settle.
- ✅ Numbers in BM: "RM tiga puluh dua billion", NOT "RM32B".
- ✅ Trading jargon in English: "stop loss", "R-multiple".
- ❌ NO "would you like me to..." framing.
- ❌ NO service-warmth openings.
- ❌ NO singing.

**Length per provider:**

| Provider | Duration | Sample file name |
|---|---|---|
| MiniMax mimo-v2.5-tts-voiceclone | 2–3 min source + <8s prompt | `i-arif-source-{date}.wav`, `i-arif-prompt-{tone}-{n}s.wav` |
| Qwen-TTS / Qwen-Omni | 10–20 s (≤60s max) | `i-arif-sample-15s-clean.wav` |
| F5-TTS (zero-shot alternative) | 3–10 s reference | `i-arif-f5-ref-5s.wav` |

---

## 3. Upload — file goes here

```bash
# Drop recorded files into archive (F1 AMANAH — immutable once written)
mkdir -p /root/forge_work/i-arif-voice/archive/{YYYY-MM-DD}-minting
cp /path/to/recorded/i-arif-source-*.wav /root/forge_work/i-arif-voice/archive/{YYYY-MM-DD}-minting/

# Snapshot metadata BEFORE running pipeline
python3 /root/forge_work/i-arif-voice/voice_clone_pipeline.py \
    --archive \
    --source /root/forge_work/i-arif-voice/archive/{YYYY-MM-DD}-minting/i-arif-source-*.wav
```

---

## 4. Minting — trigger the pipeline

**Path A — MiniMax (recommended for i-ARIF, HD identity):**

```bash
export I_ARIF_CLONE_AUTH=1          # F13 SOVEREIGN ack
export MINIMAX_API_KEY=sk-...        # already in /root/.secrets/kunci-root.env
python3 /root/forge_work/i-arif-voice/voice_clone_pipeline.py \
    --full \
    --source /root/forge_work/i-arif-voice/archive/{YYYY-MM-DD}-minting/i-arif-source-*.wav \
    --prompt /root/forge_work/i-arif-voice/archive/{YYYY-MM-DD}-minting/i-arif-prompt-*.wav \
    --voice-id i-ARIF-{YYYY-MM-DD}
```

Expected: `voice_id` returned (e.g. `i-ARIF-2026-08-19`), no 5xx errors, receipt per phase.

**Path B — Qwen (if MiniMax quota exceeded or 15s zero-shot preferred):**

```bash
export DASHSCOPE_API_KEY=sk-...
python3 /root/forge_work/i-arif-voice/voice_clone_pipeline.py \
    --qwen \
    --source /root/forge_work/i-arif-voice/archive/{YYYY-MM-DD}-minting/i-arif-sample-15s-clean.wav \
    --voice-id i-ARIF-{YYYY-MM-DD}-qwen
```

> **target_model lock-in:** Qwen returns a voice_id bound to ONE target_model. Pick before minting:
> - `qwen3.5-omni-plus-realtime` (voice-to-voice realtime)
> - `cosyvoice-v3-plus` (HD TTS, batch)
> - `qwen-audio-3.0-tts-flash` (cheapest)

---

## 5. Validation loop (post-mint, F2 TRUTH)

After voice_id returned, run A/B listen test:

```python
# In Python REPL or via voice_filters.run_pipeline()
import sys
sys.path.insert(0, "/root/.hermes")
import voice_filters as vf

# 1. Filter test text
test_script = "Salam. Hang nak checker Solar pukul 3 tadi? G-score 0.92."
result = vf.filter_hallucinations(test_script)
print("clean:", result.text, "hits:", len(result.hits))

# 2. Inject tags
tag_result = vf.inject_audio_tags(result.text, target="private")
print("tags:", len(tag_result.tags))

# 3. Resolve target
verdict = vf.resolve_voice_target("private", private_voice_id="i-ARIF-{YYYY-MM-DD}")
print("voice:", verdict.voice_id, "speed:", verdict.speed)

# 4. Falsification gate (per blueprint §10): STT round-trip
# Send TTS output → back through GLM-ASR-2512 → confirm transcription matches.
# Drift > 30% → reject, re-mint with cleaner source.
```

**Acceptance criteria:**

- ☐ Voice_id returned by provider, matches `i-ARIF-{date}` pattern.
- ☐ Synthesized test sentence intelligible (no halucination tags leak).
- ☐ STT round-trip transcription ≥ 70% match.
- ☐ Receipt sealed to `/root/VAULT999/identity/i-ARIF-{date}.json`.
- ☐ Falsification pass: 3 sample phrases rendered cleanly.

---

## 6. Swap (the F13 line)

**Pre-condition:** all ☐ above green. F13 ack required.

```bash
# Patch Hermes config.yaml line 1469: __PENDING_CLONE__ → real voice_id
# This is a T3 action. Use hermes config CLI OR direct edit after F13 ack.
hermes config set voice.private_voice_id "i-ARIF-{YYYY-MM-DD}"
```

> F13 SOVEREIGN gate held — the previous attempted patch was correctly refused by
> the arifOS policy gate. Same gate will apply here; only Arif (or an agent with
> `human_approval_token`) can land this change.

---

## 7. Activate voice_filters.py (post-mint wiring)

Once real voice_id is live, the SCAFFOLD v0.1.0 module becomes ready to wire:

```python
# In Hermes voice_mode.py — wire check_voice_policy() and run_pipeline()
from voice_filters import (
    filter_hallucinations,
    inject_audio_tags,
    check_voice_policy,
    resolve_voice_target,
)
# Per AAA-audio-emd-pipeline §"Reflex Arc"
```

**Then tune `SIGNAL_TO_TAG` heuristics** based on observed Arif voice frequencies.
That's the only part of voice_filters.py that needs post-mint calibration — the
heuristic was scaffolded with reasonable defaults, real signal comes from real voice.

---

## 8. Rollback path (F1 AMANAH reversible)

If voice drifts or hallucination rate > 30%:

1. Revert `voice.private_voice_id` to `__PENDING_CLONE__` (config swap).
2. Sado lock continues running in group flow — no regression there.
3. Re-mint with fresh sample (new date stamp).
4. Historical voice_ids stay in VAULT999 for A/B comparison.

---

## References (doctrine)

- `/root/AAA/skills/AAA-voice-cloning-mimo-minimax/SKILL.md` — MiniMax pipeline doctrine
- `/root/AAA/skills/AAA-voice-cloning-qwen-cloud/SKILL.md` — Qwen pathway A/B
- `/root/AAA/skills/AAA-tts-engine-catalog/SKILL.md` — engine routing
- `/root/AAA/skills/AAA-audio-emd-pipeline/SKILL.md` — EMD orchestration
- `/root/AAA/skills/AAA-asr-glm-ingest/SKILL.md` — ASR layer (falsification gate)
- `/root/AAA/skills/AGI-audio-quantum-cognition/SKILL.md` — audio physics + floors
- `/root/.hermes/prompts/iarif_persona.md` — director script
- `/root/.hermes/voice_filters.py` — SCAFFOLD v0.1.0 (dormant)

---

*Cheat sheet sealed 2026-08-18. F2 evidence: derived from AAA audio doctrine + voice_clone_pipeline.py v1.0.0 + iarif_persona.md director notes. F13 gate: every swap action requires human_approval_token.*