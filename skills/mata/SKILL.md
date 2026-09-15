---
name: mata
description: Unified visual intelligence truth-pane for arifOS — before ANY claim about image/video generation or understanding capability (or its absence), run mata. Kills stale-prose lies ("no API key", "quota habis", "404") with live canaries. Covers gemini, minimax (Hailuo video), mimo, kimi, dashscope VL, bailian wan2.7, qwen token-plans, ComfyUI, FED, pollinations. Trigger phrases - "generate image", "generate video", "no vision model", "quota habis", "no api key", "can we make video", "which vision model", anything visual-capability-related. [fed: tier=fed-multimodal-vision]
capability_tier: fed-multimodal-vision
ecology_state: WARM
---

# MATA — Sebelum cakap takde, tengok dulu (look before claiming absence)

MATA is the federation's single truth surface for visual capability (image gen, video gen, image/video understanding). Canonical map: `/root/AAA/knowledge-graph/MATA.md`.

## The law this skill enforces

Human Zero-Visibility Invariant HARAM-3: never claim a visual lane (or its absence) without a live probe within 24h. Models-list 200 ≠ generation quota. "Not probed" ≠ "exhausted".

## Usage

```bash
set -a; source /root/.secrets/kunci-root.env; set +a
/root/scripts/mata.sh          # pane — one line per lane, verdict + latency
/root/scripts/mata.sh --json   # machine snapshot → ~/.local/share/arifos/mata_last.json
/root/scripts/mata.sh --gen    # adds REAL generation canaries (spends quota — ask first for paid lanes)
```

Agents without shell: read `~/.local/share/arifos/mata_last.json` (check `probed_at` < 24h; if stale, ask a shell-capable agent to re-run).

## Routing quick-table (verify with pane first)

- **Image gen:** bailian wan2.7-image(-pro) → pollinations fallback → ComfyUI local (start if down) → qwen-indiv (check reset)
- **Video gen:** MiniMax-Hailuo-2.3 (3/day, 6s|10s; POST /v1/video_generation → poll query → files/retrieve) → happyhorse-1.1 t2v/i2v/r2v on qwen-indiv → Veo (needs gemini prepay top-up = F13 decision)
- **Understanding (img/video in):** mimo-v2.5 omni → zai-vision (GLM-5.3-Flash / @z_ai/mcp-server) → MiniMax-M3 → k3 (resolve 401 first) → gemini family (video-native, canary-verified)
- **OCR:** zai-vision (extract_text_from_screenshot / GLM-5.3-Flash) / M3 / mimo-v2.5 (dashscope VL fleet = 403 dead until payment-info wall resolved)

## Scars baked in (read MATA.md §Scars before extending)

1. Models-list trap (gemini: auth 200, gen 429)
2. Console-redaction stub keys (13-char `sk-cp-…` ≠ key — sweep sibling env vars)
3. Wrong-path 404s (probe endpoint variants with empty-body POST: 400/200 = EXISTS)
4. SOT staleness (anything `last_verified` > 7d = STALE)

---

## MiMo vision lane — federated primitive + real canary (2026-09-13)

Directed by F13: *"now for vision intelligence organs mata"*. Mirrors the audio treatment.

### The primitive

`mimo-vision` → `/root/scripts/mimo-vision`, symlinked to **`/usr/local/bin/mimo-vision`** (on PATH,
stdlib only, every agent can call it).

| Verb | Purpose |
|---|---|
| `see` | image understanding via **mimo-v2.5** — `--file` (comma-separated = multi-image), `--url`, `--protocol openai\|anthropic`, `--question` |
| `tokens` | image-token estimate using the **vendor scaling formula** — no API call, no quota spent |
| `doctor` | endpoint + env + **real 1px vision canary** + arifFlow health |

**This is understanding, not generation.** MATA keeps those lanes separate; do not blur them.

### The canary — SCAR #1 closed for this lane

`mata.sh` previously judged MiMo on `/v1/models` alone — the **exact trap SCAR #1 names**
(*"models-list 200 ≠ capability"*). The pane now carries **two** rows:

```
mimo-tp-list     LIVE   6 models listed
mimo-tp-vision   LIVE   REAL vision canary OK — image_tokens=9 cached=192
```

A 1×1 PNG is POSTed as an `image_url` data-URI; the verdict requires `image_tokens > 0` from the
API meter. A 200 with no image tokens reports **AMBIGUOUS**, never LIVE.

### Vendor contract (image-understanding doc)

- model: **mimo-v2.5 only**
- formats: **JPEG, PNG, GIF, WebP, BMP**
- size: **URL ≤ 50 MB** per image; **base64 string ≤ 50 MB** per image
- multi-image supported; **no multipart/local-file upload** — URL or base64 data-URI only
- **both wires accept images**: OpenAI `{"type":"image_url","image_url":{"url":…}}` and
  Anthropic `{"type":"image","source":{"type":"url"|"base64",…}}` at `/anthropic/v1/messages`
- billed as tokens; `usage.prompt_tokens_details.image_tokens` is authoritative

### Image token formula — validated, not assumed

Vendor scaling: `PATCH_SIZE=16`, `SPATIAL_MERGE=2` (factor 32), `IMAGE_MIN_PIXELS=8192`,
`IMAGE_MAX_PIXELS=8388608`; `tokens = (grid_h × grid_w) // 4` after normalisation.

| Image | Estimate (DER) | API meter (OBS) |
|---|---|---|
| 256×256 | **64** | **64** ✅ |
| 128×128 (prior receipt, 2026-09-07) | 16 | 16 ✅ |

### Empty-content trap (found live, now handled)

`mimo-v2.5` is a **reasoning** model: `max_tokens` covers the reasoning channel *plus* the answer.
A small budget returns **HTTP 200 with empty content** — a blank success, worse than an error.
`see` detects it, retries at a wider budget, and records `retry_note` in the artifact instead of
handing back silence.

### APEX-ZEN labels

**OBS** pixel dims, bytes, payload MB, `image_tokens`, `cached_tokens` ·
**DER** `image_tokens_EST_DER` (vendor formula) · **INT** `content_INT`, `reasoning_INT` (F7 ≤ 0.75).

### arifFlow + Reality Graph

Every `see` emits a Flow Receipt v1 — `Verify` / **`T0Observe`** — verified **ingested** to
`/var/lib/arifflow/receipts.jsonl`. L2 (Witness Graph) is **not** written: `REALITY_GRAPH.md` §6
forbids edges without `vault_seq`. Same guard as the audio lane.

### Overlap to reconcile (flagged, not silently merged)

GEOX already ships an organ-level VLM surface: `geox_vision_mimo_inference`
(`GEOX/src/geox_mcp/tools/vision.py`) via `MiMoVLMAdapter`. That tool is **geological-vision
scoped inside the GEOX organ**; this CLI is the **federation-wide image-understanding primitive**.
Two surfaces over one model is a drift risk — they should share the contract (formats, size caps,
token formula) rather than diverge. Routing the GEOX adapter through this contract is a GEOX-owner
decision; it was **not** taken unilaterally.

---

## MiMo video understanding — lane + PAIRED canary (2026-09-13)

Vendor page: [video-understanding](https://mimo.mi.com/docs/en-US/quick-start/usage-guide/multimodal-understanding/video-understanding).

### Verbs added to `mimo-vision`

| Verb | Purpose |
|---|---|
| `watch` | video understanding via **mimo-v2.5** — `--file`, `--url`, `--fps` (0.1–10, default 2), `--resolution default\|max`, `--question` |
| `vtokens` | vendor `estimate_video_tokens` algorithm — **no API call, no quota spent** |
| `vcanary` | **paired-fixture perception canary** — the only honest test |

### Contract

- model **mimo-v2.5 only**; wire: `{"type":"video_url","video_url":{"url":…}, "fps":N, "media_resolution":"default|max"}`
- formats **MP4, MOV, AVI, WMV**; URL ≤ **300 MB**; base64 string ≤ **50 MB**; **no multipart/local upload**
- `fps` trades temporal fineness against tokens; `media_resolution: "max"` improves small-object/texture detail
- `MAX_FRAMES = 2048`; both `video_tokens` (visual) **and** `audio_tokens` are reported — video carries audio

### Token estimator — validated by hand, honest about deviation

The vendor algorithm was ported and **independently hand-derived**, matching exactly on the doc's own
example (1080p / 60 s / fps 2): `vision 16 560 + timestamps 180 + special 122 + audio 378 = 17 240`.
At `fps=5` → 42 830; at `media_resolution=max` → 123 080 (approaching the 131 072 ceiling); `--mute` → 16 862.

**Deviation observed:** for a tiny 320×240 / 6 s fixture the estimate was 240 vision tokens vs the
meter's **320**. The min-pixel upscaling branch makes short/small sources under-estimate. This is why
every field is labelled: `*_EST_DER` (formula) vs `*_OBS` (API meter, authoritative).

### The canary that actually proves perception

`FED_VIDEO_CANARY_LEDGER.yaml` records a past failure: a single canary on a model that *described*
audio looked correct but was answerable by **output bias**, not hearing. So `mimo-vision vcanary`
builds **paired opposite fixtures** with ffmpeg — identical static grey visuals, audio **ascending**
(440→880→1320 Hz) in A and **descending** (1320→880→440 Hz) in B — and asks one question whose
correct answers are *opposite*: RISE or FALL.

```
fixture A (ascending)  → "RISE"   ✓
fixture B (descending) → "FALL"   ✓
VERDICT: PERCEPTION_VERIFIED   (opposite fixtures answered oppositely)
```

A model answering both the same would be `OUTPUT_BIAS_SUSPECTED`. This test cannot be passed by
guessing — which is exactly why it is the one that counts.

`watch` on the same fixture: *"A static grey screen is visible. A sequence of test tones plays
throughout the clip."* — accurate.

### Governance

`watch` and `vcanary` emit Flow Receipt v1 — `Verify` / `T0Observe` — **ingested** to
`receipts.jsonl`. APEX-ZEN labels: **OBS** `video_tokens`/`audio_tokens`/`cached_tokens`,
**DER** `vtoken_estimate_DER`, **INT** `content_INT`/`reasoning_INT` (F7 ≤0.75). Same
reasoning-budget guard as images. L2 Witness Graph still not written (`vault_seq` rule).

### MATA pane

Rows `mimo-tp` (list), `mimo-tp-vision` (image canary), `mimo-tp-video` (paired video canary),
`mimo-tp-audio`. The **video** canary is on-demand only — it costs video tokens, so it is not
in the cheap pane. `mimo` lane id unchanged for `mata_last.json` consumers.
