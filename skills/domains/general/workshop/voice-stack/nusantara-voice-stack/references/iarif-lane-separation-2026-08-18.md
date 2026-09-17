# i-ARIF Voice Refactor (2026-08-18 evening session) — lessons locked

> Companion doc to `nusantara-voice-stack/SKILL.md` §13. Read this before touching
> the i-ARIF voice pipeline again.

## 1. New lane separation (sealed 2026-08-18 23:00)

Voice output is now **three explicit lanes**, not two:

| Lane | Voice_id pattern | Register | Status on disk |
|---|---|---|---|
| **i-ARIF sovereign** (Arif biological voice, private/CLI/Arif-only) | `i-ARIF-*` | male, 110–160 Hz Penang-Besi | **PENDING** — needs fresh direct-mic recording, source sample not yet at required quality |
| **MakcikGPT / Nusantara Utara** (sibling product lane) | `makcikgpt-*` | female, ~264 Hz warm | **REFERENCE SEALED** as `makcik-penang-v1` (sample 8.68s, AIGC engine `HUABABSpeech7E01`, ProduceID `06d3a1b81fbd46d7ac24d8592b5cec87`); voice_id PENDING (sample below MiniMax 10s floor) |
| **Sado lock** (group/shared/public) | `ttv-voice-2026081808404926-BdoQh6ec` | male neutral 0.83x | **SEALED** — female voices FORBIDDEN in this lane per `references/syed-persona-lock.md` |

**Iron rule (F13):** lanes never cross. Makcik voice must not serve i-ARIF sovereign flow, and i-ARIF sovereign voice must not serve MakcikGPT lane. Even when both voice_ids are minted, the config layer enforces lane separation — not the model.

Identity card structure: `voice_lanes.<lane_id>` block per lane. Adding a lane = append the block, never edit an existing block in place (F1 AMANAH — voice identity is immutable).

## 2. Penang-Besi phonetic rewrite layer (live in voice_filters.py v0.2.0)

`/root/.hermes/voice_filters.py` now exports:

- `PENANG_PHONETIC_MAP` — 13 entries: `tahu→tau`, `faham→paham`, `bercakap→habaq`, `pergi→pi`, `datang→mai`, `sebentar→sat`, `sedikit→sikit`, `mungkin→kut`, `sangat→depang`, `sudah→dah`, `kenapa→kana`, `macam mana→macam ma na`, plus retained bases. **BM baku spelled in Penang loghat BEFORE TTS input** — hack-around for engines without native Penang dialect.
- `_PENANG_PROTECTED_TERMS` — never touched: F1-F13, arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA, VAULT999, MiniMax, Groq, Whisper, edge-tts, cosytts, Qwen, trading jargon, voice provider names. Spell-back mismatch (e.g. `F1` becoming `tau`) would corrupt technical output.
- `apply_penang_dialect(text, strict=True)` — token-boundary regex rewrite with `re.IGNORECASE`.
- `prosody_directive(mode)` — 5 mode presets returning `{speed, pitch_baseline_hz, pitch_variation_hz, pause_short_ms, pause_long_ms, emphasis_drop_hz, dry_wit_lift_hz, dry_wit_speed_pct}`: `private_arif_penang` (1.10×), `trading_briefing` (1.05×), `crisis_f1_hold` (0.95×), `casual_banter` (1.15×), `default` (1.0×).

`/root/.hermes/prompts/iarif_persona.md` got matching patch — Penang Somatic Dialect section appended after the existing Audio Tags Reference. Both files versioned together; if either drifts, the other's prosody/phonetic table needs reconciling.

## 3. V5 sovereign roadmap (STAGED, not deployed)

F5-TTS local container staged at `/root/forge_work/i-arif-voice/v5_sovereign/`:
- `F5TTS_Bridge_Spec.md` — payload mapping + honest gap (F5-TTS has no native audio tags, prosody comes from ref audio + punctuation)
- `docker-compose.f5tts.yml` — `127.0.0.1:8080` only, NVIDIA runtime gated
- `SYSTEM_LEDGER.json` — `active_engine=MiniMax`, `target_engine=F5-TTS`, `blocked_by="no GPU on current VPS"`

**Gate (F2 TRUTH):** current VPS is CPU-only (no nvidia-smi, no lspci GPU entry). F5-TTS on CPU = 5–10 s latency per utterance, kills conversational qualia. **Do not deploy V5 on this VPS.** When GPU appears (Runpod spot, bare-metal upgrade), the swap is config-level (`tts.provider` → local endpoint). Everything else in the pipeline stays put.

Honest comparison at session time:

| Axis | V4 MiniMax (active) | V5 F5-TTS (staged) |
|---|---|---|
| Cost | per-char/Token Plan quota | $0 (MIT) |
| Data privacy | MiniMax sees text + voice_id | 100% on-prem |
| Latency | network rt | depends on GPU |
| Sovereignty | partial (encode local, decode SaaS) | absolute |

## 4. Truth discipline lessons (session scars)

**Sessions kept drifting toward poetic axiom register** when Arif sealed constitutional work. When it crept into voice-pipeline replies too, Arif called it out: *"Laporan tu ukur benda salah"*, *"I hate reply like this. No meaning to me."* The home of this lesson is `hermes-response-format-fit`; duplicated here because voice sessions trigger it after G062 seals.

**Voice_id status truth:** when `__PENDING_CLONE__` is still in config line 1469, the voice is NOT live. Any prose saying "V4 dah hidup" or "voice_id sebenar dah wujud" is a F2 violation. Two independent sessions tried to assert "voice_id minted" during this work; both were rejected by ground-truth probes. The state of truth must be probed before any prose about it lands.

**Sub-agent reports on voice/audio artifacts cannot be trusted without re-probe.** The "voice_filters.py developed v0.1.0" claim from a sub-agent was true (589 lines, real implementation), but it was NOT what Arif or I had written that session — it landed via the Hermes voice-mode scaffolding pass that ran in the same window. Falsification requires `stat`/`ls -la`/`ffprobe`/`grep`, not just trusting the prose. Already documented in `nusantara-voice-stack/SKILL.md` §10 "Probe third-party agent reports before believing".

**AIGC-labeled samples MUST surface provenance before user evaluates them.** Three samples arrived labeled `ContentProducer=HUABABSpeech7E01` (China TTS engine). Each one Arif evaluated as if it were a candidate voice for i-ARIF sovereign lane. Falsification chain: `ffprobe -show_format` for `TAG:aigc` + Whisper transcript for "wrong-person" markers + F0 register analysis. If engine is AIGC, it's NOT Arif biological voice. Send to sibling lane (MakcikGPT), not sovereign.

## 5. Open F13 questions carrying into next session

1. **i-ARIF sovereign source** — does Arif re-record a fresh 15–30s Penang-Besi sample? Or accept V3 (`audio_de74d3c97c3f.ogg`, 33s, F0 237 Hz) as biological baseline despite F0 being above 110–160 Hz target band?
2. **Makcik V1 voice_id mint** — render ≥10 s sample with the same prosody engine, then run `voice_clone_pipeline.py --full` to mint `makcikgpt-*`. F13 gate: `I_ARIF_CLONE_AUTH=*** env export.
3. **V5 GPU provision** — when (Runpod spot? Runpod persistent? Bare-metal upgrade to VPS?) and at what cost? Each is F13 territory, never auto.

## Files referenced

- `/root/forge_work/i-arif-voice/archive/2026-08-18-makcik-penang-v1/MAKCIK-PENANG-V1-REFERENCE.{md,pdf}` — sealed artifact
- `/root/forge_work/i-arif-voice/archive/2026-08-18-makcik-penang-v1/SPECTRAL_PROFILE.json` — reproducible F0 metrics
- `/root/forge_work/i-arif-voice/v5_sovereign/{F5TTS_Bridge_Spec.md,docker-compose.f5tts.yml,SYSTEM_LEDGER.json}` — staged V5
- `/root/.hermes/prompts/iarif_persona.md` — patched with Penang dialect
- `/root/.hermes/voice_filters.py` — v0.2.0 with Penang layer
- `/root/AAA/agent-cards/identity/i-ARIF/identity-card.json` — `voice_lanes` section added
- `/root/HERMES/config.yaml` line 1469 — `voice_id: __PENDING_CLONE__` (truth state)
