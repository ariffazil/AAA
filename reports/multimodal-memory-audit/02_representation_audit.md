# 02 — Representation Audit (Multimodal Memory Architecture Audit)

**Audit:** MMA-2026-08-07
**Author:** hermes
**Status:** Ingestion pathway inventory + lossiness analysis.

---

## Executive summary

Every ingestion pathway in the federation **flattens to text before storage**. There is no native ASR, no VLM captioning, no audio embedding pipeline. The federation receives chat (text), JSONL events (text), and structured payloads (text-shaped bytes). Voice, video, image, and document modalities are absent at the ingestion layer — they may *exist* as artifacts on disk but are not represented in memory.

This audit maps each pathway to its transformations and lossiness.

---

## Ingestion pathway matrix

### Pathway 1 — Text (chat / agent prompt)
```
INPUT: ASCII / UTF-8 user message
TRANSFORMATIONS:
  1. None (or trivial strip)
STORED REPRESENTATION:
  - L1 Redis: ephemeral TTL
  - L2 Redis: session range
  - L5 Graphiti: episode → entities + edges (after extraction)
  - L3 Qdrant: text embedding via bge-m3 (1024d)
RETRIEVAL REPRESENTATION:
  - Vector similarity (L3) + graph traversal (L5) + session scan (L1/L2)

signal_preserved: full literal text
signal_lost:     paralinguistic (only available in voice input, not chat)
reversible:      yes (raw text retained in L2 Redis session; L1 ephemeral)
irreversible:    no
```

### Pathway 2 — Audio (voice notes, Telegram voice)
```
INPUT:           binary .ogg / .m4a
TRANSFORMATIONS: NONE in federation today
                 OpenCode detected "edge-tts --voice ms-MY-OsmanNeural" in config but no ASR pipeline exists
STORED:          file on disk only (NOT sealed, NOT indexed)
RETRIEVAL:       none — binary is dark to retrieval

signal_preserved: full waveform on disk
signal_lost:      all meaning until a human transcribes
reversible:       yes (file on disk)
irreversible:     meaning-loss is irreversible absent ASR
```

**Gap:** TTS generation exists (edge-tts) but no inverse ASR path. Voice notes received from Arif would land as files in `/root/HERMES/voice_cache/` or similar with no semantic projection. The federation is **blind to voice**.

### Pathway 3 — Video
```
INPUT:           .mp4 / .mov
TRANSFORMATIONS: NONE in federation today
STORED:          file on disk only (if at all)
RETRIEVAL:       none

signal_preserved: full pixels + audio track on disk
signal_lost:      every frame, every motion, every tone
reversible:       yes (file)
irreversible:     yes (no keyframe extraction, no captioning)
```

### Pathway 4 — Image
```
INPUT:           .png / .jpg / .webp
TRANSFORMATIONS: NONE in federation today (no VLM pipeline)
STORED:          file on disk (when sent via Telegram, may persist in HERMES cache)
RETRIEVAL:       none — federation cannot describe an image

signal_preserved: full pixels on disk
signal_lost:      semantic content
reversible:       yes
irreversible:     yes
```

**Note:** the Telegram gateway *can* receive images; the agent can `vision_analyze` them at conversation time, but **nothing persists** into memory. The conversation turn that processed the image is text-only after the response is sealed.

### Pathway 5 — Document (PDF, .md, .docx)
```
INPUT:           .pdf / .md / .docx / .txt
TRANSFORMATIONS:
  - pymupdf/marker-pdf extraction → text
  - chunks for embedding
STORED:
  - text extracted into L4/L5 if processed
  - file on disk
RETRIEVAL:       via text embeddings + L4 relational

signal_preserved: full text after extraction
signal_lost:      formatting, layout, figures-as-images, charts (unless extracted)
reversible:       text-extraction is lossy for layout, near-lossless for prose
irreversible:     image content inside PDFs is lost (no VLM integration with PDF pipeline)
```

### Pathway 6 — Chat (multi-turn conversation)
```
INPUT:           sequence of text messages
TRANSFORMATIONS:
  - each turn → L1 Redis (ephemeral)
  - aggregated → L2 Redis (session)
  - post-session → Graphiti episode extraction
  - embeddings → L3 Qdrant
  - sealed events → L6 VAULT999
STORED:          composite (L1–L6)
RETRIEVAL:       composite query via arif_memory.recall

signal_preserved: full text + metadata (timestamps, session_id, actor)
signal_lost:      prosody (text only — voice never entered), reactive latency (not stored)
reversible:       yes (all layers retained)
irreversible:     no
```

### Pathway 7 — Event (system events, webhook receipts)
```
INPUT:           JSON envelope (e.g. webhook payload from SIGNAL)
TRANSFORMATIONS:
  - schema validation (SIGNAL 6 chambers)
  - epistemic label assignment (OBS/DER/INT/SPEC)
  - hash chain (VAULT999)
STORED:
  - L4 Redis aaa:federation:memory:L6 (mirrored)
  - L6 VAULT999 outcomes.jsonl
  - arifFlow /var/lib/arifflow/receipts.jsonl
RETRIEVAL:       chain query (hash), payload reconstruction (hash pointer)

signal_preserved: full structured payload
signal_lost:      none — events are by definition structured
reversible:       yes (chain walks back to genesis)
irreversible:     append-only guarantee prevents tampering
```

### Pathway 8 — Meeting (calls, video conferences)
```
INPUT:           audio + video stream (zoom/teams/etc.)
TRANSFORMATIONS: NONE in federation
STORED:           not applicable — meetings are not ingested
RETRIEVAL:       not applicable

signal_preserved: zero (not stored)
signal_lost:      everything
reversible:       no (not stored)
irreversible:     yes
```

**Note:** the `teams-meeting-pipeline` skill exists in HERMES, suggesting meeting summary pipelines *can* be invoked on demand, but the output is text — meetings are flattened to transcript→embedding like audio.

---

## Lossy transformation catalog (every arrow)

| # | Transformation | Where | Reversibility | Notes |
|---|---|---|---|---|
| 1 | text → L1 Redis TTL | arif_memory | full | ephemeral but recoverable within TTL |
| 2 | text → L2 Redis range | arif_memory | full | session-scoped retention |
| 3 | text → Graphiti episode (entities + edges) | Graphiti | partial | entity resolution is lossy (paraphrases collapse) |
| 4 | text → bge-m3 1024d vector | Qdrant | irreversible | dense projection; minority signals lost |
| 5 | episode → L4 Supabase row | L4 durable | partial | typed columns capture schema, lose prose |
| 6 | episode → L6 VAULT999 sealed receipt | VAULT999 | full (chain) | provenance + chain hash preserved |
| 7 | audio → (no transform) | federation | n/a | dead path; no pipeline exists |
| 8 | video → (no transform) | federation | n/a | dead path |
| 9 | image → (no transform) | federation | n/a | dead path; vision_analyze exists at conversation layer only |
| 10 | document → text (pymupdf) | PDF tool | partial | layout lost |
| 11 | meeting → text (transcript) | teams pipeline | partial | prosody lost at transcript step |

## What gets preserved vs lost (matrix)

| Pathway | semantic | relational | temporal | affective | artifact |
|---|---|---|---|---|---|
| text chat | ✅ full | ✅ Graphiti entities | ✅ timestamp | ❌ | ❌ (text is the artifact) |
| audio | ❌ | ❌ | ❌ | ❌ | ⚠️ file on disk only |
| video | ❌ | ❌ | ❌ | ❌ | ⚠️ file on disk only |
| image | ❌ | ❌ | ❌ | ❌ | ⚠️ file on disk only |
| document (text-based) | ✅ after extraction | ⚠️ if manually entity-resolved | ⚠️ if doc has metadata | ❌ | ⚠️ file on disk only |
| chat session | ✅ full | ✅ composite | ✅ full | ❌ | ❌ |
| event/receipt | ✅ structured | ✅ via payload refs | ✅ timestamp | ❌ | ✅ payload hash (not binary) |
| meeting | ⚠️ if transcript exists | ⚠️ | ⚠️ | ❌ | ❌ |

---

## Top 10 architectural gaps (representation-level)

1. **No ASR pathway.** Voice → text transformation does not exist; voice notes are dark to retrieval.
2. **No VLM image captioning.** Image → text transformation does not exist; agent vision is conversation-only, never persists.
3. **No video keyframe extraction.** Video → caption transformation does not exist.
4. **No audio embedding.** No CLAP-style audio embeddings; voice prosody has no index.
5. **Document pipeline strips layout.** pymupdf extracts text, not figure-as-image, not table-as-structure.
6. **Graphiti entity resolution collapses paraphrases.** Two sentences meaning the same thing merge; minor differences lost.
7. **Vector quantization is fixed at 1024d (bge-m3).** No multimodal embedding model integration; CLIP-style joint embedding absent.
8. **Affective features have no extraction path.** Pause density, speech rate, pitch variance are never measured because audio never enters.
9. **Visual engagement signals absent.** No eye-tracking, no face-detection, no gesture recognition — none of the multimodal affect signals even have a defined capture point.
10. **Binary artifacts have no sealed path.** Files exist on disk; VAULT999 payload_hash covers only structured payloads.

## Top 10 quick wins (representation-level)

1. **Wire `whisper.cpp` or `faster-whisper` as an ingestion service** behind a new `signal/audio` endpoint (T2 ingestion).
2. **Add a `clip-ViT-B/32` image embedder to Qdrant pipeline** (T2 ingestion).
3. **Capture raw payload bytes into VAULT999 by extending `payload_hash` to `payload_bytes`** (schema change, T1).
4. **Add `source_modality` field to all envelope schemas** (T1 schema-only).
5. **For Telegram voice messages, route through an ASR service before L1 ingestion** (T2).
6. **Store image attachments alongside the conversation turn with a `MEDIA:` URI** (T2, no schema change).
7. **Pre-process PDFs with figure extraction + captioning** (T2 ingestion).
8. **Sample 1 fps from any video frame and caption via VLM** (T2 ingestion, future).
9. **Add prosody features (pause density, speech rate, pitch) as extractable metadata** when ASR lands (T3 retrieval).
10. **Define a `preflight.artifact_index` tool that scans `/root` for unindexed binary files** (T3 retrieval).

## Highest-risk assumptions

- **Assumption F:** "Multimodal inputs are rare; text dominates." — Verified TRUE for the federation's current traffic pattern, but the parent conversation establishes that the *white space* is the affective + artifact layers. Sticking with text-only preserves current operations but blocks Wave 3 entirely.
- **Assumption G:** "If a file is on disk, it's accessible." — Verified FALSE: no federation indexer scans disk for media; files are dark.
- **Assumption H:** "vision_analyze covers images." — Verified FALSE: it operates at conversation time only; nothing persists.
- **Assumption I:** "Teams pipeline handles meetings." — Verified TRUE for transcript output; the meeting audio/video is not stored.

## Recommended first implementation step

**T2 ingestion, single-pathway:** Wire ASR (faster-whisper, already a M3 dependency or readily installable) behind a new `signal/audio_ingest` webhook endpoint on SIGNAL (:18084). For every Telegram voice message, ASR → transcript → L1/L2/L5/L3/L6 path identical to text. Add `source_modality=audio` field. Don't change the pipeline shape; add the front door.

This is the **smallest change** that makes voice a first-class modality without touching any other organ.

## Success condition (Phase 2)

Every pathway from the 8-modality matrix has either:
(a) an explicit transformation path documented, or
(b) an explicit "no path — gap" entry.
This audit documents all 8. Phase 3 (gap analysis) confirms whether the layers downstream of ingestion are equipped to handle the artifact + affective faces.

---

**delta_s (representation):** High — first complete inventory of ingestion lossiness in the federation.
**evidence_paths:**
- `/root/hermes-agent/skills/` (autonomous-ai-agents for opencode, a2a-gateway-protocol)
- `/root/HERMES/profiles/*/config.yaml` (hermes memory config)
- `/root/.local/share/opencode/auth.json` (OpenCode Kimi provider)
- `/root/arifOS/deploy/graphiti-config.yaml:17` (bge-m3 1024d embedder)
- `/root/arifOS/scripts/` (verify_vault_chain, repair_vault999, drift_check_live)
- `/root/AAA/contracts/mcp_surface.yaml` (MCP surface contract)
- `:18084/health` (SIGNAL 6-chamber healthy verified)

**Verified vs claim:** every pathway was inspected against the codebase or probed live. The "no path" claims are verified by grep across the federation source trees.
