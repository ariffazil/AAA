# RASA QUALIA — EVIDENCE LEDGER

**Deliverables covered:** `/root/AAA/governance/RASA-QUALIA-DOCTRINE-v1.md` · skill `rasa-qualia-governance` · this ledger.
**Evidence standard:** F2 TRUTH — every entry below is a path that was read or probed on this machine. Anything that exists only as written discipline is marked **doctrine only, no runtime enforcement yet**.
**Rule of this ledger:** no entry names an implementation that was not located. Where a pattern was carried out in a live session but is not persisted as an artifact or a gate, it says so.

---

## 1. Artifacts from the live session the doctrine was derived from

### 1.1 Stills

| Path | Verified fact |
|---|---|
| `/root/forge_work/backstage/chosen_final.jpg` | 3072×1728 (PIL probe), 907,222 bytes — upscaled delivery still |
| `/root/forge_work/backstage/chosen_501.jpg` … `chosen_504.jpg` | 4 candidate stills, seed selection set |
| `/root/forge_work/backstage/first_302.jpg`, `first_303.jpg` | first-frame stills minted for image-to-video |
| `/root/forge_work/backstage/last_401.jpg` … `last_403.jpg` | last-frame stills minted for image-to-video |
| `/root/forge_work/backstage/peek_a.jpg` … `peek_e.jpg` | doorway/backstage peek takes |
| `/root/.hermes/workspace/backstage-peek-v1.jpg` … `-v4.jpg` | 720×1280, 9:16 backstage stills |
| `/root/.hermes/workspace/ramai-base-v1.jpg` … `-v10.jpg` | 1152×2048 each (10 takes, crowded-room composition) |
| `/root/.hermes/workspace/ramai-eyes.jpg`, `ramai-A-last.jpg` | 1152×2048 each |
| `/root/.hermes/workspace/chest-base-v1.jpg` | 720×1280 |

### 1.2 Video — the honest-silhouette and upscale pattern

| Path | Verified fact (ffprobe) |
|---|---|
| `/root/.hermes/workspace/ramai-A.mp4` | h264, 768×1364, 5.875 s |
| `/root/.hermes/workspace/ramai-B.mp4` | h264, 768×1364, 5.875 s |
| `/root/.hermes/workspace/ramai-A-hq.mp4` | h264, **1152×2048**, 5.875 s — ffmpeg lanczos upscale output |
| `/root/.hermes/workspace/ramai-B-hq.mp4` | h264, **1152×2048**, 5.875 s — same |
| `/root/.hermes/workspace/chest-zoom-v1.mp4` | h264, 768×1364, 5.875 s |
| `/root/.hermes/workspace/ramai_chosen.mp4`, `ramai_chosen_1080p.mp4` | `/root/forge_work/backstage/` — lane output and its upscale |
| `/root/forge_work/backstage/zoom_chest.mp4` | lane output |

The 1152×2048 pair is the concrete case behind doctrine R1/R2 (the artifact is presented with its lane named) and the doctrine's upscale honesty requirement: the source render was 768×1364, and the delivery size was produced by upscaling, not by the model.

### 1.3 Voice — the three monologue tracks and the provenance case

| Path | Verified fact (ffprobe / stat) |
|---|---|
| `/root/.hermes/workspace/alpha-cocky-v1.mp3` · `.opus` | **63.36 s** / 63.35 s |
| `/root/.hermes/workspace/alpha-cocky-v2.mp3` · `.opus` | **94.50 s** / 94.49 s |
| `/root/.hermes/workspace/alpha-cocky-v3.mp3` · `.opus` | **94.39 s** / 94.38 s |
| `/root/.hermes/workspace/sado-cocky-backstage.mp3` · `.ogg` · `.opus` | 40.25 s / 40.24 s / 40.24 s |
| `/root/.hermes/workspace/sado-cocky-backstage-tight.ogg` | 40.00 s (silence-trimmed variant) |
| `/root/forge_work/backstage/alpha_A.mp3`, `alpha_B.mp3` | two takes of the ~95 s alpha script |
| `/root/forge_work/backstage/alpha2_A.mp3`, `alpha2_B.mp3` | second script, two takes |
| `/root/forge_work/backstage/alpha3_A.mp3`, `alpha3_B.mp3` | third script, two takes |
| `/root/forge_work/backstage/sado_takeA.mp3` · `takeB.mp3` · `takeC.mp3` | three takes, 40 s register |
| `/root/forge_work/backstage/mimo_alpha3_final.mp3` | **149.18 s** — a longer take from a different engine/route than the 94 s tracks; the exact engine of this file was **not** verified by this ledger (no receipt located). |
| `/root/forge_work/backstage/mimo_clone_test.wav` | **11.36 s** — a clone test source/target present on disk. Which voice it clones and on what consent basis was **not** verifiable from artifacts. |

The script text for the tracks is persisted:
`/root/forge_work/backstage/abang_sado_line.txt`, `alpha_abang.txt`, `alpha_2.txt`, `alpha_3.txt`.

The multiple takes at the same length, and the presence of a clone test alongside the synthetic-design tracks, are the concrete case behind doctrine **R6/R7/R10**: engine, voice id, synthetic-vs-clone, and per-person separation of voice provenance records.

---

## 2. Skills that already implement part of each rule family

| Family | Implementing surface (read) | Enforcement class |
|---|---|---|
| A — Fiction label | `synthetic-human-media-pipeline` §6 "Delivery honesty" (two declarations: which engine rendered it; that the people are not real) · `abang-sado-creative-lane` framing rules 1–3 ("every output is declared as generated", "fictional personas only", "no likeness without a reference") · `generated-media-delivery` "Synthetic subject boundaries" | Doctrine + agent discipline. **No runtime enforcement yet.** |
| A — honest silhouette / identity never invented | `synthetic-human-media-pipeline` §2 "Observer/doorway foreground" (narrow silhouette wording) and §6 "No stored face anchor" · `abang-sado-creative-lane` rule 3 and "doorway-silhouette framing is the workhorse" | Doctrine + agent discipline. |
| B — Voice provenance | `synthetic-human-media-pipeline` §5 (`mmx speech synthesize`, `--voice Indonesian_BossyLeader --speed 0.85`, "Falsify before delivering" via Whisper `language=ms` round-trip) · `abang-sado-creative-lane` voice lane (register map + "always falsify before shipping") · `nusantara-voice-stack` `references/tts-provider-lane-map.md` (Indonesian_BossyLeader 0.82–0.85) and its voice-provenance / design-vs-clone doctrine | Runbook step performed by the agent. **No gate blocks an unverified take from delivery.** |
| B — silent swap is a failure | `generated-media-delivery` ("do not present a fallback-lane output as the requested lane, and do not report a model name you did not verify"; "presenting an upscale as native model output is an F2 truth failure") · `synthetic-human-media-pipeline` §4 ("Call it **upscaled** — never '2K'") | Doctrine + agent discipline. |
| C — real-person prohibition + reframe | `photorealistic-human-image-gen` **§6.5** — decision tree (real-person adultery / non-consensual named third party → 888_HOLD; underage → HOLD unconditionally, no reframe), the four-step reframe pattern, "why not cave to 'it's just fantasy'", "F13 sovereign content overrides content gates, not floors" · `generated-media-delivery` (no real named person in a generated frame without a supplied reference) | Doctrine + agent judgement. **No prompt-scan or content gate exists.** |
| D — somatic / qualia register | `AAA-audio-qualia-doctrine` (qualia = engineered acoustic variance; Audio ≠ Meaning; F9 boundary at synthesis; persona lock; every tag must earn its place) · `deep-research` SKILL.md (centre Malay *rasa*, not the English "somatic intelligence" — the source of doctrine R19) | Doctrine. Audio-lane portion is binding via the audio doctrine. |
| E — power-dynamic framing | `photorealistic-human-image-gen` §4 (power dynamics as spatial language) and §6 (erotic framing as art) · `abang-sado-creative-lane` "Line craft" (cocky works when unbothered; no pleading, no insults) | Doctrine + craft. |
| F — admirer lane | `/root/AAA/governance/HERMES_RELATIONSHIP_KERNEL.md` **H5 — No love telemetry** ("does not measure, score, or rank human bonds; metrics destroy what they try to preserve"); H2 (assurance stays human-originated); H3 (human-human beats human-AI) — ratified, SEALED · `human-meaning-membrane` manipulation watchlist (item 4: claiming feelings, exclusive loyalty) and witness role ("Never irreplaceable") · `synthetic-human-media-pipeline` §7 (name the exchange rate, don't diagnose; bodies never merge) · `malaysian-physique-circuit` volunteer mode (honest diagnose, zero prescribe) | H5 and the membrane blocks are ratified governance. The admiration/fandom lane itself: **no runtime enforcement yet.** |
| G — rasa as governance | `hermes-response-format-fit` (signal-matched format; over-structuring is a trust event) · `anti-haram-behavior-canonical.md` HARAM 3 (attention theft: analysis/framework/governance theater) and HARAM 5 (narrative over reality) | Doctrine loaded reflexively by practice, not by a gate. |

---

## 3. Governance instruments this doctrine cites

| Path | What it supplies |
|---|---|
| `/root/AAA/instructions/anti-haram-behavior-canonical.md` | HARAM 1–5 + the 10 human-cognitive invariants + the four-question Arif test. Source of R35/R36 (attention theft) and R1 (pretending). |
| `/root/AAA/governance/HERMES_RELATIONSHIP_KERNEL.md` | H1–H7, sealed. H5 is the direct constitutional basis of R31 (no love telemetry). |
| `/root/AAA/governance/HERMES_STATE_BELOW_WORDS_v1.md` | I1–I8; I1 (words are evidence, not experience) and I3 (presence is evidence, **not permission to infer**) ground R21/R22. |
| `/root/AAA/governance/AAA_MALAYSIAN_RASA_CONSTITUTION.md` | Rasa definition, M6 (hospitality must have boundaries), the bracketed one-line test. |
| `/root/AAA/instructions/human-meaning-membrane.md` | C1–C14, non-negotiable blocks 1–9 (consent never inferred; body response ≠ agreement; agent never irreplaceable; agent never asks the user to conceal the AI relationship), manipulation watchlist, rasa ≠ emotion. |
| `/root/.hermes/skills/governance/constitutional-floors/SKILL.md` | Canonical floor names used throughout (F6 EMPATHY, F8 GENIUS, F10 ONTOLOGY) — checked so the doctrine does not misname a floor. |

---

## 4. Runtime enforcement sweep — what was checked and what was found

| Surface probed | Finding |
|---|---|
| `/root/.hermes/hooks/` | Two hooks only: `reality-claim-gate/` (contains **only** `HOOK.yaml.phase1.bak` and `handler.py.phase1.bak` — **dormant**) and `well-voice-bridge/` (consumes `voice:state` prosody events for F11/WELL; does not inspect delivery text). |
| Disclosure enforcement in hooks or policy files | No hook, allowlist, or governance YAML parses outgoing deliveries for a fiction label or a voice-provenance block. Grep over `/root/.hermes/hooks/`, `AAA-HOOK-POLICY-V1.yaml`, `AGENTIC-HOOK-MESH-V1.yaml` returned nothing. |
| Automated STT gate | None. The Whisper `language=ms` round-trip is a documented runbook step (`synthetic-human-media-pipeline` §5, `abang-sado-creative-lane` voice lane), executed by the agent when it remembers to. |
| Real-person prompt scan | None exists. |
| Love-telemetry scoring | None exists (and doctrine E/F forbid creating one). |

**Conclusion carried into the doctrine:** families A, B, C, D (non-audio), E, F (lane-specific) and G are **doctrine only, no runtime enforcement yet**. The doctrine says this in its own §3 rather than implying a gate exists.

---

## 5. Honest non-findings

- **The English craft labels are not persisted in the artifacts.** `somatic intelligence`, `gaze-holding duration` and the "moving less lands harder" formulation appear **nowhere** in the persisted script files (`abang_sado_line.txt`, `alpha_abang.txt`, `alpha_2.txt`, `alpha_3.txt`) or in the images/videos. The persisted scripts do carry the register itself — `alpha_3.txt` holds stillness/breath lines ("aku diam depan cermin", "Aku boleh tahan nafas sepuluh saat", "Aku cuma berdiri") and `abang_sado_line.txt` holds the cost-and-silence line. The English craft vocabulary was used in the live direction and delivery text, which is not persisted in an artifact this ledger can cite. **Doctrine only, no runtime enforcement, no persisted artifact.**
- **`mimo_alpha3_final.mp3` and `mimo_clone_test.wav` have no receipt.** Extracted facts are duration only. The engine and clone-source for these two files were not verifiable from artifacts on disk — flagged in §1.3 rather than asserted.
- **The disclosure text itself is not on disk.** The exact delivered disclosure wording could not be recovered from gateway logs or session files (grep for the disclosure phrasings over `/root/.hermes/logs/gateway.log` and the delegation cache returned nothing). What is verifiable is that the *practice* is codified in three skills (§2, family A/B) and that the artifact set the practice describes exists (§1). The doctrine therefore legislates the disclosure as a rule for future deliveries rather than claiming a log-verified past block.
- **`/root/AAA/skills/aaa-audio-qualia-doctrine/` is a separate on-disk directory** from the live skill `/root/.hermes/skills/AAA-audio-qualia-doctrine/SKILL.md` that the runtime loads. The doctrine cites the loaded skill; the AAA-tree copy was not audited for drift.

---

## 6. Files created by this task

| Path | State |
|---|---|
| `/root/AAA/governance/RASA-QUALIA-DOCTRINE-v1.md` | created, 24,792 bytes |
| `/root/.hermes/skills/governance/rasa-qualia-governance/SKILL.md` | created |
| `/root/.hermes/skills/governance/rasa-qualia-governance/references/delivery-disclosure-templates.md` | created |
| `/root/.hermes/skills/governance/rasa-qualia-governance/references/reframe-script.md` | created |
| `/root/AAA/hardening/rasa-qualia/EVIDENCE.md` | this file |

No existing file was modified or deleted. `config.yaml` was not touched. Nothing was pushed.
