---
name: mimo-vision
description: "FEDERATED Xiaomi MiMo vision lane — image AND video understanding via mimo-v2.5, plus token estimators and a PAIRED-fixture perception canary. Use for image description/classification/OCR-adjacent reading, video analysis, multi-image comparison, or before claiming a visual lane dead. MATA-aligned. NOT image generation. Trigger phrases: 'look at this image', 'what is in this picture', 'describe this video', 'video understanding', 'image understanding', 'how many tokens for this video'. [fed: tier=fed-multimodal-vision]"
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# MiMo Vision — image + video understanding (AAA canonical)

> Understanding, not generation. MATA keeps those lanes separate on purpose.
> "Sebelum cakap takde, tengok dulu." · DITEMPA BUKAN DIBERI.

**Primitive:** `/root/scripts/mimo-vision` → symlinked to **`/usr/local/bin/mimo-vision`** (on PATH for
every process, stdlib only, no pip deps in any agent home). Also on `/root/HERMES/skills/` for the
i-ARIF gateway home.

**Contracts SOT:** `/root/.config/federation-models.json` → `mimo/mimo-v2.5` (`multimodal_api.image_in`,
`video_in`, `audio_in`). Canonical visual map: `/root/AAA/knowledge-graph/MATA.md`.

## Verbs

| Verb | Purpose |
|---|---|
| `see` | image understanding — `--file` (comma-separated = multi-image), `--url`, `--protocol openai\|anthropic`, `--question` |
| `watch` | video understanding — `--file`, `--url`, `--fps` (0.1–10, default 2), `--resolution default\|max` |
| `tokens` | image-token estimate (vendor formula, **no API call**) |
| `vtokens` | video-token estimate (vendor `estimate_video_tokens`, **no API call**) |
| `vcanary` | **paired-fixture perception canary** — the only honest test |
| `doctor` | endpoints + env + real 1px image canary + arifFlow health |

## Contracts (vendor-confirmed 2026-09-13)

**Images** — [doc](https://mimo.mi.com/docs/en-US/quick-start/usage-guide/multimodal-understanding/image-understanding)
`{"type":"image_url","image_url":{"url": "<https-url | data:MIME;base64,...>"}}`
Formats **JPEG, PNG, GIF, WebP, BMP** · URL ≤ **50 MB** · base64 ≤ **50 MB** per image · multi-image ok.
Anthropic wire also takes images: `{"type":"image","source":{"type":"url"|"base64",…}}` at `/anthropic/v1/messages`.

**Video** — [doc](https://mimo.mi.com/docs/en-US/quick-start/usage-guide/multimodal-understanding/video-understanding)
`{"type":"video_url","video_url":{"url":…}, "fps": N, "media_resolution":"default|max"}`
Formats **MP4, MOV, AVI, WMV** · URL ≤ **300 MB** · base64 ≤ **50 MB** · `MAX_FRAMES 2048`.
`fps` trades temporal fineness against tokens; `max` resolution improves small-object/texture detail.
Video carries **both** `video_tokens` and `audio_tokens`.

**Neither lane supports multipart/local upload** — URL or base64 data-URI only.

## Cost discipline — price it before you spend it

Video is the most token-hungry lane. Vendor estimator, validated by independent hand-derivation on the
doc's own example (1080p / 60 s / fps 2) → **17 240** tokens (vision 16 560 + timestamps 180 +
special 122 + audio 378). `fps=5` → 42 830 · `media_resolution=max` → **123 080** (ceiling 131 072) ·
`--mute` → 16 862.

Always run `vtokens` before a large `watch`. Estimates are `*_EST_DER`; the API meter
(`*_OBS`) is authoritative — observed to deviate (240 est vs 320 actual on a small 320×240 fixture,
because the min-pixel upscaling branch under-estimates short/small sources).

## The canary that counts

`FED_VIDEO_CANARY_LEDGER.yaml` records a past failure: a single canary on a model that *described*
audio looked correct but was answerable by **output bias**, not hearing. Therefore `vcanary` builds
**paired opposite fixtures** (identical static grey visuals; audio ASCENDING 440→880→1320 Hz in A,
DESCENDING in B) and asks one question with *opposite* correct answers.

```
A (ascending)  → "RISE" ✓     B (descending) → "FALL" ✓     → PERCEPTION_VERIFIED
```

Both-same ⇒ `OUTPUT_BIAS_SUSPECTED`. This test cannot be passed by guessing.

## Trap: reasoning-budget blank-success

`mimo-v2.5` is a **reasoning** model — `max_tokens` is shared by the reasoning channel *and* the
answer. Too small a budget returns **HTTP 200 with EMPTY content** (observed: image ingested,
`image_tokens` billed, content blank). `see`/`watch` detect it, retry at a wider budget, and stamp
`retry_note`. **General rule: empty content + non-empty reasoning = budget exhaustion, not capability
failure.** (MATA Scars #5.)

## Governance

Every `see`/`watch`/`vcanary` emits a Flow Receipt v1 — `Verify` / **`T0Observe`** — to arifFlow
`:7073/ingest` (L1 metabolism of the Reality Graph); failures are reported inside the artifact, never
silently dropped. APEX-ZEN labels: **OBS** dims/bytes/`image_tokens`/`video_tokens`/`audio_tokens` ·
**DER** token estimates · **INT** `content_INT`/`reasoning_INT` (F7 cap ≤ 0.75).

**L2 Witness Graph is NOT written** — `REALITY_GRAPH.md` §6 forbids edges without `vault_seq`.

## Overlap to reconcile

GEOX ships an organ-scoped VLM surface (`geox_vision_mimo_inference` / `MiMoVLMAdapter`). This CLI is
the federation-wide primitive. They must share the contract (formats, caps, token formula) or they
will drift. GEOX-owner decision; not taken unilaterally.
