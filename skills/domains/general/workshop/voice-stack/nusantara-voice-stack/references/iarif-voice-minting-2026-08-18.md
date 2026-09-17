# i-ARIF Voice Minting Ceremony — 2026-08-18

**Status:** F13 territory. Script + checklist + sample archive on disk. Minting not yet executed.

This file is the reusable trace for cloning Arif's voice into i-ARIF. The pipeline + checklist + scaffolded filters exist; what is missing is Arif's typed F13 stamp on three decisions.

---

## 1. Three F13 Decisions Required to Mint

A future agent picking this up MUST NOT execute `--full` until all three of these are answered in chat by Arif:

1. **Sample primary** — `(a)` `/root/forge_work/_cold-storage/2026-08-18-zen-cleanup/2026-08-12/i-arif-voice.mp3` (27.79s, 12 Aug experimental design) · `(b)` `/root/.hermes/cache/audio/audio_97adfcfcb227.mp3` (18.29s, the "caringman-test" sample Arif dropped 2026-08-18 21:30) · `(c)` fresh recording by Arif on a new morning.
2. **POST probe authorization** — Arif must type `probe yes` (or equivalent) before any `python3 voice_clone_pipeline.py --probe` runs. Default mode is `--identity --archive` (zero network).
3. **Source provenance + consent** — `(a)` Arif's own voice with self-attestation; `(b)` Syed's voice with prior consent file; `(c)` synthetic designed voice (no real human clone). This determines `consent_status` in `identity-card.json > voice_clone_pipeline` section.

If any of the three is missing → HOLD. Do not promote `--probe` to a warm suggestion.

---

## 2. Pipeline Layout (on disk)

| File | Purpose |
|---|---|
| `/root/forge_work/i-arif-voice/voice_clone_pipeline.py` | 297-line Python pipeline. Modes: `--identity` (default, no network), `--archive`, `--probe` (POST with empty voice_id, expect 4xx = endpoint live), `--full` (requires `I_ARIF_CLONE_AUTH=1` env var). |
| `/root/forge_work/i-arif-voice/MINTING-DAY-CHECKLIST.md` | 219-line printable cheat sheet (8 sections, pre-flight → rollback). |
| `/root/forge_work/i-arif-voice/archive/2026-08-18-pre-clone/` | 12 Aug sample archived before any mutation. SHA256 in `BEFORE.json`. |
| `/root/forge_work/i-arif-voice/archive/20260818T133423Z/` | Second archive snapshot from same source, post-falsification-on-pipeline default run. RECEIPT.json records actions taken. |
| `/root/.hermes/voice_filters.py` | 589-line SCAFFOLD v0.1.0 — `HallucinationFilter`, `PersonaTagInjector`, `VoicePolicyGate`. **DORMANT.** Not loaded by Hermes core yet. Will be wired post-mint after real TTS output exists for tuning. |
| `/root/.hermes/prompts/iarif_persona.md` | Director script for `auxiliary.tts_audio_tags`. Defines `[breath] [emph] [dry] [settle] [literal] [hold]` mapping. |

---

## 3. Config Patch State

`/root/HERMES/config.yaml` lines 1465–1475:

```yaml
  i-arif-voice-clone:
    api: https://api.minimax.io/v1
    key_env: MINIMAX_API_KEY
    model: mimo-v2.5-asr
    voice_id: __PENDING_CLONE__
    clone_source:
      primary: /root/forge_work/_cold-storage/2026-08-18-zen-cleanup/2026-08-12/i-arif-voice.mp3
      prompt: /root/.hermes/cache/audio/audio_97adfcfcb227.mp3
      archive: /root/forge_work/i-arif-voice/archive
```

**Note:** the model field reads `mimo-v2.5-asr` — this is NOT what was intended for the synth call. Should be `speech-2.8-hd`. Cleanup needed before `--full`. Either this is a stale hand-edit by another agent or a typo during the forge. Verify before mint.

`voice.sado_locked_voice_id` = `ttv-voice-2026081808404926-BdoQh6ec` lives at line ~1647 — confirmed separate lane, **NOT affected by i-ARIF clone**.

`identity-card.json > voice_clone_pipeline` has `consent_status: F13_PROVISIONAL` — patch only when Arif's source-provenance answer is known.

---

## 4. Falsification Gate (per GENESIS/062 §2)

After every TTS render of the cloned voice, run STT round-trip:

```bash
source /root/.secrets/kunci-root.env
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file="@/tmp/tts_output.mp3" \
  -F model="whisper-large-v3-turbo" \
  -F language="ms"
```

**Acceptance threshold:** transcription levenshtein-distance vs input text ≤ 0.30 (i.e., ≥ 70% match). Lower quality → re-mint with cleaner sample.

---

## 5. Rollback Path (F1 AMANAH)

Voice minting is designed to be reversible:

1. Revert `voice.sado_locked_voice_id`-style swap → restore `__PENDING_CLONE__`.
2. Archived `voice_id_*` stays in VAULT999 with timestamp.
3. Re-mint with new timestamped `voice_id`: `i-ARIF-{YYYY-MM-DD-v2}`. Never overwrite.

---

## 6. STT Probe Data Point (already collected)

Whisper transcription of `/root/.hermes/cache/audio/audio_97adfcfcb227.mp3`:

> "Here, you go first. I want to treat you a little bit like a child, not my mind. One institution in the telephone, not the office, not the headcount, not the person who does it."

If Arif chooses (b) as primary sample, this transcript is what the cloned voice should sound like reading BM — that's the falsification anchor.

---

## 7. Sovereign Lane vs Default Lane Question (Arif asked 2026-08-18 20:50)

Q: "Should I change my Hermes default model to I-ARIF?"

Answer (Hermes memo, accepted):
- Hermes default = tenant-agnostic, role-recoverable, dialect-agnostic. **Keep.**
- I-ARIF = Arif-tuned sovereign substrate (Hang's own work). **Sovereign lane, not default.**
- Mixed = contamination. A third tenant hitting the VPS would get Penang loghat geopolitical analysis. Don't.

Same lane logic governs the voice: i-ARIF voice = private/CLI Arif only. Public/Syed/Telegram = sado lock or no voice clone activated.

---

## 8. Pending (open)

- [ ] `voice_id` swap on `--full` success
- [ ] `identity-card.json > voice_policy.sado_locked_voice_id` gap patch — currently in config but not card
- [ ] `voice_filters.py` activation after first real TTS render produced (so the 26-phrase list can be tuned against actual slips)
- [ ] Decide MiniMax vs Qwen vs F5-TTS route for the actual `--full` run (currently MiniMax scaffolded; Qwen blueprint received but not consumed)
- [ ] Confirm i-arif-voice-clone `model:` field — currently `mimo-v2.5-asr`, should be `speech-2.8-hd`

