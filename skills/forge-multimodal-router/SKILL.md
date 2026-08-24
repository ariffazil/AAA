---
name: forge-multimodal-router
id: forge-multimodal-router
risk_tier: low
description: 'Federation-wide multimodal routing skill. Resolves any vision/audio/video/somatic request to its canonical model + endpoint via /root/.config/federation-models.json (SOT). USE WHEN: "which model should I use for X", "route this image/audio/video to the right engine", "unify multimodal routing across agents", "I have an image/audio/video and need to know where it goes".'
version: 1.0.0
tags:
- multimodal
- routing
- vision
- audio
- video
- somatic
- tts
- asr
- image-generation
- video-generation
- federation
- SOT
- F4
- F8
floor_scope:
- F02
- F04
- F08
owner: AAA
autonomy_tier: T1
capability_tier: fed-multimodal-router
ecology_state: WARM
consumes_sot: /root/.config/federation-models.json
mirror_paths:
- /root/AAA/skills/forge-multimodal-router/SKILL.md
- /root/HERMES/skills/forge-multimodal-router/SKILL.md
- /root/.qwen/skills/aaa-canonical/forge-multimodal-router/SKILL.md
- /root/.claude/skills/forge-multimodal-router/SKILL.md
forged: 2026-08-20
forged_by: FI-003 (Qwen Code)
f13_directive: "make sure my hermes agent telegram ASI_arifos_bot know how to use this"
constitutional_floor: F11 AUDIT — every routing decision logged to VAULT999 receipts
---

# forge-multimodal-router

## Purpose

The federation supports four modalities (vision, audio, video, somatic) across 8 agents. Each modality has multiple functions (recognize, generate, edit, clone, analyze) and multiple engines (image gen, video gen, TTS, ASR, voice clone, music). Without a single routing skill, decisions are scattered across ~18 skills (`token-plan-image`, `token-plan-speech`, `token-plan-video`, `AAA-tts-engine-catalog`, `minimax-image-gen`, `creative/minimax-cli`, etc.) and 3 knowledge graphs.

This skill is the **single ingestion entry point** for any multimodal routing question. It does NOT duplicate model identity — it references the SOT.

## The authority doctrine (DO NOT VIOLATE)

| Layer | File | Owner |
|---|---|---|
| **SOT (single source of truth)** | `/root/.config/federation-models.json` | AAA/FED (Kimi-code/FI-008 writes) |
| **Reader** | `/root/AAA/scripts/fed_router.py` (`FED_SOT_PATH`) → `:7074` | FED |
| **Live health/balance** | `token_bank.db` via `:7074` (HTTP 402/200 probes) | FED runtime |
| **Tombstone** | `/root/AAA/federation/fed_signatures.yaml` — DEAD 2026-08-17 | F13 confirmed: do not resurrect |

**Rule:** Model identity lives ONLY in SOT. Skill/tool surface (Hermes config, OpenCode config, etc.) is a CONSUMER, not authority. Next model release = 1 SOT edit (RCR — Release Change Ratio).

**Picker sync rule:** AAA/FED has authority to write SOT (sqlite + json) but does NOT auto-write to picker configs (Kimi/Codex/Qwen/Claude/Go/Grok CLI). F13 holds the pen. Manual alignment audit is correct path.

## The routing decision algorithm

Given a multimodal request, ask in order:

1. **What modality?** (vision / audio / video / somatic)
2. **What direction?** (input = perception / output = generation)
3. **What function?** (recognize / generate / edit / clone / analyze / transform)
4. **What constraints?** (real-time? free quota required? Malaysian voice? identity-preserving? i-ARIF voice?)

Then resolve:

```
resolution = lookup_sot(
  modality, direction, function, constraints
)
# SOT returns: { provider_id, model_key, endpoint_url, params_override }
```

If SOT doesn't have a matching entry → STOP. Do NOT fallback to agent card or pickers. Either:
- Check `arifos-federation-provider-multimodal-discovery` skill to probe the provider
- Or forge an ephemeral skill for the new routing case

## Routing rules (read from SOT, this table is a navigation aid ONLY)

### Vision

| Request | SOT key | Engine | Notes |
|---|---|---|---|
| Image understanding (real-time, Telegram) | `dashscope/qwen-vl-max` | PRMT | Single failure domain, primary |
| Image understanding (fallback) | `dashscope/qwen3-vl-plus` | PRMT | When qwen-vl-max fails |
| OCR (multi-script) | `dashscope/qwen3-omni-flash` | OCR cascade | Tier 1 of AAA-OCR |
| OCR (Latin) | `local/tesseract-5.5` | Local | Free fallback |
| OCR (Chinese) | `local/rapidocr-3.9` | Local | Free fallback |
| Document extraction | `dashscope/qwen3-vl-ocr` | VLM specialist | See FORGE-document-intelligence |
| Face ID (deterministic) | `local/dlib-128dim` | Local | READ-ONLY, see deterministic-face-id |
| Image generation (T2I latest) | `dashscope/qwen-image-3.0-pro` | DashScope PAYG | Free quota eligible |
| Image generation (T2I fast) | `dashscope/qwen-image-3.0` | DashScope PAYG | Newest Aug 2026 |
| Image generation (T2I mass) | `dashscope/z-image-turbo` | DashScope PAYG | 8-step inference |
| Image editing (identity-preserving) | `gemini/gemini-3.1-flash-image` | NB2 | 6 Iron Rules |
| Image editing (fallback) | `dashscope/qwen-image-edit-max` | DashScope PAYG | LoRA support |
| Image generation (Malay/SEA) | `minimax/image-01` | MiniMax MCP | Default |
| Image generation (Grok Imagine T2I) | **harness** `grok-build/image_gen` | spawn `grok-multimodal.sh image` | Native Grok Build. Not FED. |
| Image editing (Grok Imagine) | **harness** `grok-build/image_edit` | spawn `grok-multimodal.sh edit REF` | Reference-first for named people |

### Audio

| Request | SOT key | Engine | Notes |
|---|---|---|---|
| ASR (short audio <5min) | `dashscope/qwen-audio-3.0-asr-flash` | DashScope PAYG | Default |
| ASR (long offline file) | `dashscope/qwen-audio-3.0-asr-flash-filetrans` | DashScope PAYG | Meetings, calls |
| ASR (real-time stream) | `dashscope/qwen-audio-3.0-asr-flash-streaming` | DashScope PAYG | Live meetings |
| ASR (Penang-Besi dialect) | `dashscope/qwen-audio-3.0-asr-flash` + custom dict | DashScope PAYG | See AAA-asr-glm-ingest |
| ASR (default) | `local/faster-whisper-base` | Local | Free fallback |
| TTS (default Malaysian) | `edge-tts/ms-MY-YasminNeural` | Edge (free) | No quota |
| TTS (multilingual) | `dashscope/qwen-audio-3.0-tts-flash` | DashScope PAYG | Free quota eligible |
| TTS (realtime full-duplex) | `dashscope/qwen-audio-3.0-realtime-plus` | DashScope PAYG | Aug 2026 |
| TTS (sovereign i-ARIF) | `minimax/speech-2.8-hd` | MiniMax | voice_id `i-ARIF-20260819T084602` |
| TTS (Penang-Besi dialect) | `mimo/mimo-v2.5-tts-voicedesign` | MiMo Token Plan | See nusantara-acoustic-infrastructure |
| TTS (voice clone) | `dashscope/voice-enrollment` | DashScope PAYG | + qwen-voice-design |
| DSP analysis | `local/librosa` | Local | See media/audio-analysis |
| Live translate (realtime) | `dashscope/qwen3.5-livetranslate-flash-realtime` | DashScope PAYG | Aug 2026 |

### Video

| Request | SOT key | Engine | Notes |
|---|---|---|---|
| Video generation (T2V newest) | `dashscope/wan3.0-video` | DashScope PAYG | ⭐ Aug 2026 |
| Video generation (T2V standard) | `dashscope/wan2.7-t2v-2026-06-12` | DashScope PAYG | Jul 2026 |
| Video generation (I2V) | `dashscope/wan2.7-i2v-2026-04-25` | DashScope PAYG | Preserve subject/style |
| Video generation (R2V) | `dashscope/wan2.7-r2v-2026-06-12` | DashScope PAYG | Up to 9 refs |
| Video generation (R2V alternative) | `dashscope/happyhorse-1.1-r2v` | DashScope PAYG | Realistic dynamic |
| Video generation (Grok Imagine I2V) | **harness** `grok-build/image_to_video` | spawn `grok-multimodal.sh video REF` | 6s/10s · 720p. Native Grok Build. |
| Video editing | `dashscope/wan2.7-videoedit` | DashScope PAYG | Local/global edits |
| Last-frame analysis | `dashscope/qwen-vl-max` (re-use) | PRMT | No temporal context |
| Video INPUT (continuous) | **GAP** | — | No skill yet — see forge-video-stream-ingest (P0) |
| A-V cross-modal fusion | **GAP** | — | Per video-intelligence-map.md §4 |

### Somatic (Music Intelligence)

| Request | SOT key | Engine | Notes |
|---|---|---|---|
| Music generation (governed) | `minimax/music-2.6` | MiniMax T2A Music | Per AAA-somatic-emd-pipeline |
| Music generation (newest) | `minimax/music-3.0` | MiniMax T2A Music | |
| Music scoring (somatic) | `federation/somatic-scorer` | WELL + scoring | Per AAA-somatic-music-doctrine |
| Songwriting + Suno | `suno/suno-v3` | Suno | Creative lane |
| DSP feature analysis | `local/librosa-scipy` | Local | See media/audio-feature-analysis |

## Constraints & override rules

### Free quota preference
- If SOT model is in Singapore region AND has International scope AND has blue quota bar in console → prefer it over PAYG
- Validate via `arifos-federation-provider-multimodal-discovery` skill before assuming free quota
- Enable **Free Quota Only** mode per model in console (default OFF for verified users)

### i-ARIF voice identity
- F13 SOVEREIGN-gated: voice identity is biometric-class
- Use `AAA-voice-cloning-mimo-minimax` for any i-ARIF request
- All i-ARIF calls seal to VAULT999 with explicit voice_id annotation

### Identity preservation (face/body)
- F13, 2026-08-12: "Hang jangan ubah muka manusia"
- Real photo edits MUST preserve face, body, skin tone 100%
- Use `media/aaa-image-editing` (6 Iron Rules) + ensemble NB2 + NB-Pro for identity-critical work

### Privacy / Sovereignty
- Voice biometric = F1 custody (vault-class)
- Face ID = local-only (no cloud round-trip)
- All auth keys via `~/.secrets/kunci-root.env` (5-R Protocol)

## How to invoke this skill

When an agent receives a multimodal request and needs to route:

1. **Classify** the modality + direction + function + constraints
2. **Look up** the SOT key (use this skill's routing table as index, then verify against `/root/.config/federation-models.json`)
3. **Verify** the SOT entry is current (F11: log the lookup with SHA256 of SOT file)
4. **Resolve** to `provider_id + model_key + endpoint_url`
5. **Call** the model via the agent's MCP surface (e.g., `mcp__aforge__forge_browser_*` for browser, or direct API call for non-MCP)
6. **If the route is Grok Imagine**: spawn `/root/.grok/bin/grok-multimodal.sh`. Those tools are harness-native to FI-007, not Hermes/OpenCode.
7. **Log** the routing decision to VAULT999 (F11 AUDIT)

### Harness-native Imagine (not a FED model)

Telephone: `/root/AAA/docs/GROK_IMAGINE.md`. Wrapper: `grok-multimodal`. **Do not** add grok to LiteLLM.

## Cross-cutting doctrine (apply across modalities)

| Concern | Skill | Authority |
|---|---|---|
| Provider capability probing | `arifos-federation-provider-multimodal-discovery` | Verifies before claiming |
| Visual structural QA | `forge-vss-verifier-suite` | Post-generation |
| Multimodal reasoning | `AGI-multimodal-bridge` | Cross-modal fusion |
| Audio quantum doctrine | `AGI-audio-quantum-cognition` | Audio substrate |
| Visual substrate | `delta-omega-psi-multimodal-cognition` | Δ·Ω·Ψ enforcement |
| Visual governance | `FORGE-visual-qa-w3` | W³ tri-witness |
| TTS engine registry | `AAA-tts-engine-catalog` | TTS routing detail |
| Voice cloning | `AAA-voice-cloning-mimo-minimax` + `AAA-voice-cloning-qwen-cloud` | Voice identity |
| Somatic music | `AAA-somatic-music-doctrine` + `AAA-somatic-emd-pipeline` | Music constitution |
| Document intelligence | `FORGE-document-intelligence` | Doc VLM |
| OCR cascade | `AAA-OCR-optical-compression` | OCR Tier 1-3 |
| Face ID | `deterministic-face-id` | READ-ONLY |
| Cross-region config | `devops/provider-routing-zen` | Operational |

## Knowledge graphs (canonical unified maps)

| Modality | KG file | Lines | Forged |
|---|---|---|---|
| Audio | `/root/AAA/knowledge-graph/audio-intelligence-map.md` | 338 | 2026-08-13 |
| Visual | `/root/AAA/knowledge-graph/visual-intelligence-map.md` | 911 | 2026-08-18 |
| Video | `/root/AAA/knowledge-graph/video-intelligence-map.md` | 529 | 2026-08-18 |
| Somatic | **MISSING** — use `AAA-somatic-music-doctrine` SKILL.md | — | — |

## Floors

- **F2 TRUTH:** Every routing decision cites the SOT entry used (provider_id + model_key + SHA256 of SOT file at lookup time).
- **F4 CLARITY:** This skill is a navigation index, not a duplicate of SOT. Single source of truth = SOT.
- **F8 GENIUS:** Cross-modal requests route through η algorithm (4 questions) before falling back to per-modality skills.
- **F11 AUDIT:** Every routing decision logged to VAULT999 receipts (provider + model + token estimate + SOT version).
- **F1 AMANAH:** Free quota preference + BlueQuotaBar check before PAYG. No surprise charges.

## Annual verification

This skill MUST be re-validated:
- On any SOT change to `/root/.config/federation-models.json` (RCR enforcement)
- On any new model release touching vision/audio/video/somatic
- Quarterly (next due: 2026-11-20)

If the routing table here drifts from SOT, the table is wrong (SOT wins). Update this skill to match SOT, never the reverse.

## Failure modes

| Failure | Action |
|---|---|
| SOT missing entry for modality+function | Use `arifos-federation-provider-multimodal-discovery` to probe provider; if real, propose SOT edit (F13 stance: 1 SOT edit per model release) |
| Provider returns 402 (insufficient balance) | Trigger `devops/qwen-provider-operations` for diagnosis |
| Provider returns 401 (auth fail) | Verify key in `~/.secrets/kunci-root.env`; rotate if needed |
| Hermes config drift from SOT | Hermes config is consumer; SOT is authority. Patch Hermes config to match SOT, NOT vice versa. |
| Cross-agent picker drift | F13 holds the pen. AAA writes SOT only, does NOT auto-sync to pickers. Manual alignment audit. |

## Audit trail

- **2026-08-25** — FI-007: Imagine spawn path for all AAA agents (`grok-multimodal.sh` + GROK_IMAGINE.md). Harness-native, not FED.
- **2026-08-20** — forged by FI-003 Qwen Code
- Driver: Arif F13 directive "now make sure my hermes agent telegram ASI_arifos_bot know how to use this"
- Builds on: 32 multimodal models wired into `/root/HERMES/config.yaml` `dashscope-payg` provider + `tts/stt.qwen-audio-payg` entries (2026-08-20)
- Builds on: 3 canonical knowledge graphs (audio + visual + video) — `/root/AAA/knowledge-graph/`
- Constraints: F2 SOT authority, F11 AUDIT, F13 picker sovereignty, RCR 1-edit-per-release
- Receipt: to be appended to `/root/forge_work/qwen-sessions/sessions.jsonl` + named receipt
