---
name: gemini-media-gen
description: "Generate images and videos via Gemini API (Gemini native image gen + Omni Flash/Veo 3.1 video). Auto-discovery: loads when user requests image/video generation. Uses existing GEMINI_API_KEY — no extra keys needed. A2A-ready: results include provenance metadata for federation audit."
version: "1.0.0"
tags:
  - image-generation
  - video-generation
  - gemini
  - imagen
  - veo
  - media
  - creative
auto_discovery:
  triggers:
    - "generate image"
    - "generate video"
    - "create image"
    - "create video"
    - "make a picture"
    - "make a video"
    - "gambar"
    - "video"
    - "image gen"
    - "video gen"
  priority: 2  # Higher than comfyui (1), lower than verify-before-report (3)
---

# Gemini Media Generation

> Generate images and videos via Gemini API using `gemini-image.py` and `gemini-video.py`.
> Uses existing GEMINI_API_KEY — no extra keys, no extra cost.
> A2A-ready: every output carries provenance metadata.

## Architecture

```
User request
    ↓
Agent loads skill (auto-discovery)
    ↓
Route by type:
  Image → gemini-image.py (Gemini native generateContent)
  Video → gemini-video.py (Omni Flash) or Veo 3.1 (predictLongRunning async)
    ↓
Verify output exists
    ↓
Return with MEDIA: path + provenance
```

## Image Generation (Gemini native — preferred route)

> **Use `gemini-image.py`** — handles base64 extraction + save automatically.
> 
> **New (2026-08-13):** Supports post-generation validation to catch hallucinations (extra objects, duplicate props, identity drift) before delivery.

### Model routing

| Model | Flag | When to use |
|---|---|---|
| `gemini-2.5-flash-image` | `--model gemini-2.5-flash-image` (default) | Quick drafts, low-stakes visuals |
| `gemini-3-pro-image` | `--model gemini-3-pro-image` | **Preferred for quality** — default when Arif says "pro" or doesn't specify |
| `gemini-3-pro-image-preview` | `--model gemini-3-pro-image-preview` | Latest preview features |

**Arif preference:** Quality first. When he says "Use pro" or doesn't specify model, route to `gemini-3-pro-image`. Flash only when he explicitly says "flash" or speed matters.

> ⚠️ Imagen 4 models (`imagen-4.0-*`) are deprecated. Do NOT use them.

### Validation and reroll (Fix #3)

Use `--validate` to run a vision check after generation. If validation fails (extra objects, wrong count, identity drift), automatically reroll.

```bash
# Count-based validation: expect exactly 1 light tube
python3 /root/HERMES/scripts/gemini-image.py "prompt" --image ref.png --output out.png \
  --validate --check "light tube" --expect-count 1 --max-rerolls 3

# Descriptive validation: check for duplicated/out-of-place objects (no explicit count)
python3 /root/HERMES/scripts/gemini-image.py "prompt" --image ref.png --output out.png \
  --validate --max-rerolls 2
```

**Flags:**
- `--validate` — enable post-generation vision check
- `--check "<object>"` — object to count (e.g. `"light tube"`, `"person"`, `"logo"`)
- `--expect-count N` — expected count; validation fails if mismatch
- `--max-rerolls N` — auto reroll up to N times on validation failure

**Exit codes:**
- `0` = success (image generated + validation passed)
- `1` = API/generation error
- `2` = validation failed after all rerolls

## Video Generation

### Primary: Gemini Omni Flash (`gemini-video.py`) — SIMPLEST, no MCP needed

> ✅ Verified working: synchronous response, no polling. 10s clips, 720×1280 (9:16).

```bash
python3 /root/HERMES/scripts/gemini-video.py "prompt" --output /tmp/v.mp4 --aspect 9:16
```

- Supports `--aspect 16:9` (default) or `9:16`
- Synchronous: returns completed video in one call (~30-120s)
- Response: base64 video in `steps[].content[].data`

## Video Generation (Veo 3.1) — VERIFIED WORKING 2026-08-10

> ✅ Verified 2026-08-10: Veo 3.1 works with existing GEMINI_API_KEY via `predictLongRunning`.
> ✅ **Generates native audio** (AAC stereo, 48kHz) — no separate audio track needed.
> ⚠️ **durationSeconds MUST be 4-8** (API rejects outside this range).
> Requires async polling — use when quality > speed matters.

```bash
# Step 1: Submit job (async)
# CRITICAL: Use x-goog-api-key HEADER, NOT ?key= query param (verified 2026-08-10)
GEMINI_KEY=$(grep GEMINI_API_KEY /root/.secrets/kunci-mas.env | cut -d= -f2 | tr -d '"' | tr -d "'")

JOB_RESPONSE=$(curl -sf "https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-generate-preview:predictLongRunning" \
  -H "x-goog-api-key: $GEMINI_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "instances": [{"prompt": "YOUR_PROMPT_HERE"}]
  }')

# Extract operation name
OP_NAME=$(echo "$JOB_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('name',''))")

# Step 2: Poll for completion (check every 10s, max 5min)
for i in $(seq 1 30); do
  sleep 10
  RESULT=$(curl -sf "https://generativelanguage.googleapis.com/v1beta/${OP_NAME}" \
    -H "x-goog-api-key: $GEMINI_KEY")
  STATUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('done',False))")
  if [ "$STATUS" = "True" ]; then
    echo "$RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
# ⚠️ REAL response path (verified 2026-08-09): response.generateVideoResponse.generatedSamples[].video.uri
# NOT response.videos[] — that shape returns 'no video' even on success.
gen = d.get('response', {}).get('generateVideoResponse', {})
samples = gen.get('generatedSamples', [])
if samples:
    uri = samples[0].get('video', {}).get('uri', '')
    print(f'VIDEO_URI:{uri}')
else:
    print(f'ERROR: no generatedSamples in {json.dumps(d)[:300]}')
"
    break
  fi
  echo "Polling... ($i/30)"
done
```

### Downloading the result (auth required)

The returned `VIDEO_URI` is a Google-hosted file — use header auth, not query param:
```bash
# VIDEO_URI looks like: https://generativelanguage.googleapis.com/v1beta/files/<id>:download?alt=media
curl -sL -o /tmp/output.mp4 -H "x-goog-api-key: $GEMINI_KEY" "${VIDEO_URI}"
ls -la /tmp/output.mp4   # verify size > 0 before reporting done
```

### Video Parameters (VERIFIED)
| Parameter | Values | Default | Note |
|---|---|---|---|
| `aspectRatio` | `16:9`, `9:16` | `16:9` | |
| `sampleCount` | 1-4 | 1 | |
| `durationSeconds` | **4-8 ONLY** | 8 | API rejects <4 or >8 |

### ⚠️ Critical: No `config` field in request body (verified 2026-08-10)

The Veo 3.1 REST API does NOT accept `config` or `parameters` in the request body.
Passing `config` returns `INVALID_ARGUMENT: Unknown name "config"`. Request body
should ONLY contain `instances[].prompt`. Duration/aspect default to 8s 16:9.
Use the Python SDK (`google-genai`) for full parameter control over duration/aspect.

## Output Protocol

Every generation MUST return:

```
MEDIA:/path/to/output.file

Provenance:
  provider: gemini
  model: gemini-3-pro-image / gemini-omni-flash-preview / veo-3.1-generate-preview
  prompt: [user's prompt]
  timestamp: [ISO timestamp]
  session: [session_id]
```

## Verification (MUST) — the 3-gate protocol

**Never ACK generation success without live probe.** The C0 self-test:
> "If F13 reads only the receipt block, can they confirm the work is done?"

Gate 1 — **file exists and has bytes:**
```bash
ls -la /path/to/output.png && [ -s /path/to/output.png ] && echo OK
```

Gate 2 — **file is valid image (not 0-byte, not truncated):**
```bash
file /path/to/output.png   # expect JPEG (Pro) or PNG (Flash) image data
```

Gate 3 — **if `--validate` was used, check exit code:**
- `0` = generation + validation passed
- `1` = API/generation error
- `2` = validation failed after rerolls (hallucination caught)

If verification fails → report "generation failed" with error. Do NOT say "done" without evidence.

## A2A Provenance Metadata

For federation audit, include in output:
```json
{
  "artifact_type": "image" | "video",
  "provider": "gemini",
  "model": "gemini-3-pro-image | gemini-omni-flash-preview | veo-3.1-generate-preview",
  "prompt_hash": "sha256:...",
  "generated_at": "2026-08-10T...",
  "session_id": "...",
  "verifiable": true
}
```

## CLI Argument Pitfall — gemini-image.py (verified 2026-08-13)

**The prompt is a POSITIONAL argument, not `--prompt`.**

```bash
# ✅ CORRECT — positional
python3 /root/HERMES/scripts/gemini-image.py "your prompt here" --output out.png

# ❌ WRONG — --prompt is not recognized
python3 /root/HERMES/scripts/gemini-image.py --prompt "your prompt" --output out.png
# → argparse error: unrecognized arguments: --prompt
```

Actual signature: `gemini-image.py [-h] [--output OUTPUT] [--model MODEL] [--image IMAGE] prompt`

**Failure mode in background mode:** argparse prints to stderr and exits with code 2. If the agent tails `2>&1 | tail -5` and ignores exit code, the failure is silent — no file produced, but the process appears to complete. Always `ls -la output.png` after to confirm the file landed.

This pitfall was hit on 2026-08-13 building "The Cost of a Forgotten Well" cover image — first call wasted a 90s background cycle.

## Output Format Quirk (verified 2026-08-10)

`gemini-3-pro-image` returns **JPEG** data despite the script saving with `.png`
extension. The file is valid JPEG wrapped in a `.png` filename — image viewers
handle this fine, but `file` command shows `JPEG image data`. Flash model
(`gemini-2.5-flash-image`) returns actual PNG. Don't worry about the mismatch;
just note it in provenance if accuracy matters.

## Rate Limiting & Multi-Provider Quota (verified 2026-08-10)

**Gemini 429 rate limit is NOT 60s.** After a burst of ~6-8 API calls (mix of
image Pro/Flash + video Omni Flash), we hit 429 errors that persisted **10+
minutes**. The Gemini free-tier RPM limit is aggressive for sustained use.

| Burst size | Typical cooldown | Notes |
|---|---|---|
| 1-3 calls | 60s | Usually clears |
| 4-6 calls | 5-10 min | RPM limit, not daily |
| 7+ calls in <5 min | 10-20 min | May hit daily RPD ceiling |

**Multi-provider quota exhaustion:** When Gemini is rate limited, the fallback
routes (Qwen Token Plan, MuleRouter, MiniMax) may ALSO be exhausted from
parallel use. Before attempting fallbacks, probe each:

```bash
# Qwen — check for insufficient_quota
curl -s "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $QWEN_API_KEY" \
  -d '{"model":"qwen3.6-flash","messages":[{"role":"user","content":"hi"}]}' | head -100

# MuleRouter — check balance in error
python3 /root/HERMES/scripts/mulerouter-image.py --prompt "test" --output /dev/null 2>&1 | head -5

# MiniMax MCP — check health
curl -sf http://127.0.0.1:18100/health
```

**Qwen Token Plan image gen does NOT work** via compatible-mode API — the
`/images/generations` endpoint returns 404. Models are listed but the endpoint
isn't exposed. Don't waste calls trying it.

**When ALL providers are exhausted:** Tell Arif honestly. Don't keep retrying
burned endpoints — set a cron reminder for 15-30 min cooldown and move on.

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| 404 model not found | Model name wrong | Check model list via API |
| 403 forbidden | API key lacks access | Enable Imagen/Veo in Google Cloud Console |
| 429 rate limit | Too many requests | Wait **10-20 min** (not 60s — see Rate Limiting section) |
| `insufficient_quota` | Qwen Token Plan exhausted | Use Gemini or wait for daily reset |
| `402 Insufficient balance` | MuleRouter credits negative | Use Gemini or add credits |
| Timeout | Video generation slow | Veo is async — poll longer |

## Image Editing — Identity Preservation (CRITICAL, verified 2026-08-12)

**NEVER claim an image edit model "preserves" a real person's face.** All current models (Gemini 3 Pro, Gemini Flash, Qwen wan2.7-image-pro) regenerate the entire image including the subject's face, producing an idealized generic version — especially for muscular/bodybuilder subjects. The model interprets "keep the same" as "generate a similar-looking person," not "preserve the pixels."

**Arif's rule: "Hang jangan ubah muka manusia."** Binding, not a preference.

### Approach Decision Tree (verified 2026-08-13)

```
User asks to "place this person in scene X"
    │
    ├─ Face identity is CRITICAL (named real person, friend, family)
    │   │
    │   ├─ Try Gemini 2.5 Flash Image first ("nano banana") — BEST identity preservation
    │   │  with explicit feature-specific prompt
    │   │  If face regenerated → try specific feature prompts
    │   │  If still fails → FALLBACK below
    │   │
    │   └─ Composite fallback (rembg cutout + empty bg + PIL paste)
    │      WARNING: rembg clips jawline/chin for side-lit portraits
    │      Verify with vision_analyze before delivery.
    │      If jawline disappears → report BLOCKED, do not ship
    │
    ├─ Add person to existing scene (couple shots)
    │   └─ Gemini 2.5 Flash Image — handles multi-subject composition well
    │      Prompt: describe new person's appearance + clothing + interaction
    │      Keep original subject's features explicit in prompt
    │
    ├─ Enhance old/low-res photo
    │   └─ Gemini 3 Pro Image (not Flash) — heavier detail recovery
    │      Prompt: "Ultra HD upscale... Remove artifacts, noise, blur... 8K"
    │
    └─ Identity is NORMAL (generic person, illustration, artistic)
        Use any edit model directly
```

### Edit Model Prompt Template (highest identity preservation)

```
"Place this man at [LOCATION]. Keep his face and body EXACTLY as shown.
Same short spiky hair, same jawline, same expression, same person.
[Setting description]. He wears [outfit]. Photorealistic. No text."
```

Be **specific** about features to preserve: hair texture, jawline, skin tone, expression.
Generic "keep identity" prompts give generic results.

### When edit models fail — Composite Fallback

1. **rembg cutout** from original photo → transparent PNG (subject pixels 0% altered)
2. **Generate empty background** (NO people in prompt) via Gemini or Qwen text-to-image
3. **PIL composite** — paste cutout onto background

```bash
# Step 1: Remove background (pip install --break-system-packages rembg)
python3 -c "
from rembg import remove; from PIL import Image
remove(Image.open('ref.jpg')).save('ref_nobg.png')
"
# Step 2: Generate empty background (NO people)
python3 /root/HERMES/scripts/gemini-image.py \
  "Empty backstage pumping room. Concrete walls, warm lights. No people. No text." \
  --output bg.jpg --model gemini-2.5-flash-image
# Step 3: Composite
python3 -c "
from PIL import Image
s = Image.open('ref_nobg.png').convert('RGBA')
b = Image.open('bg.jpg').convert('RGBA')
s = s.crop(s.getbbox())
th = int(b.height * 0.75); s = s.resize((int(th*s.width/s.height), th), Image.LANCZOS)
r = b.copy(); r.paste(s, ((b.width-s.width)//2, b.height-s.height-int(b.height*0.02)), s)
r.convert('RGB').save('final.jpg', quality=95)
"
```

⚠️ **Known composite failure (verified 2026-08-12):** `rembg` U2Net clips into
jawline/chin for side-lit portraits with strong shadow contrast. Visible as
"dagu hilang" (chin missing). **Visual verify every composite before delivery.**
If jawline is clipped → composite is unusable → revert to edit model with
acknowledgment that identity is approximate.

**Reference:** `references/identity-preservation-composite-fallback.md` — full session walkthrough + model comparison.

## Content filter boundary (verified 2026-08-10)

Gemini's content filter is more permissive than MiniMax for bodybuilder/suggestive
content, but has a hard ceiling:

| Passes | Blocked |
|---|---|
| Comedic/meme framing (worship, cuckold, simping) | Explicit sexual acts or nudity |
| Suggestive poses, flexing, intimate proximity | Graphic sexual content |
| Dramatic/emotional framing (heartbreak, devotion) | Pornographic scenarios |
| Cinematic narrative with multiple characters | Direct "make it erotic/stimulating" requests |

**Prompt framing trick:** Always frame as "cinematic" + "comedic/dramatic" +
"hyper-realistic photography". Movie-scene language passes. Erotica language
gets blocked. If user pushes for explicit content, explain the filter boundary
honestly — don't waste API calls on prompts that will 400.

## References

- `references/veo3-api-reference.md` — Veo 3.1 endpoint, auth, request/response shapes, rate limits, vs Omni Flash comparison

## F9 ANTIHANTU

- NEVER claim generation succeeded without verification
- NEVER fabricate file paths
- NEVER say "done" without checking file exists
- If generation fails, say so honestly

DITEMPA BUKAN DIBERI.
