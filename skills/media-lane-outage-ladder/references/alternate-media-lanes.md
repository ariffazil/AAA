# Alternate Media Lanes — Recipes

Lanes proven to render when the primary stack is gated, with the call shape, the parameter limits,
and the way each one fails. Keys come from the root vault environment; never inline a key or a vault
path in a command argument — a pre-execution gate classifies that as T3 and blocks the call.

## Image — Alibaba DashScope-intl, Wan T2I

Auth `DASHSCOPE_PAYG_API_KEY` (`sk-ws-`). Keys are per-region: a key that 401s on one host may be
valid on the intl host, so probe before declaring it dead.

Models: `wan2.2-t2i-flash` (fast) · `wan2.2-t2i-plus` (better skin/fabric fidelity, slower).

```python
import json, os, urllib.request
KEY = os.environ["DASHSCOPE_PAYG_API_KEY"]
SUBMIT = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
TASK   = "https://dashscope-intl.aliyuncs.com/api/v1/tasks/{}"

body = {"model": "wan2.2-t2i-plus",
        "input": {"prompt": prompt},
        "parameters": {"size": "960*1280", "n": 1}}
req = urllib.request.Request(SUBMIT, data=json.dumps(body).encode(),
    headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json",
             "X-DashScope-Async": "enable"})
task_id = json.loads(urllib.request.urlopen(req, timeout=120).read())["output"]["task_id"]
# poll GET TASK.format(task_id) every ~6 s until output.task_status == SUCCEEDED,
# then download output.results[*].url
```

- **`X-DashScope-Async: enable` is required** and submit returns a `task_id`, not an image. A script
  that reads `output.results` off the submit response gets nothing.
- **`size` uses a STAR separator** — `"960*1280"`, never `960x1280`.
- **Submitting several prompts at once trips `Throttling.RateQuota`** (429 on the *submit*). Submit
  one, keep the id, move on — a submit-rate 429 is a pacing instruction, and the earlier prompts
  usually still complete.
- Minutes per image; budget before promising a delivery time.
- Renders muscular / bare-chested / two-figure registers without input filtering, but it will not obey
  a "hide the faces" instruction — asked for a chest-to-chest hug it composed both faces frontal on
  every seed. Compose the frame so the faces are outside it instead.

## Image — Cloudflare Workers AI, FLUX.1-schnell

Auth `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_WORKERS_AI_TOKEN`.

```python
URL = ("https://api.cloudflare.com/client/v4/accounts/%s/ai/run/"
       "@cf/black-forest-labs/flux-1-schnell" % os.environ["CLOUDFLARE_ACCOUNT_ID"])
body = {"prompt": prompt, "steps": 8}          # steps 4-8; higher is slower, not better here
# response: {"success": true, "result": {"image": "<base64 jpeg>"}}
```

- **Body takes ONLY `prompt` and `steps`.** `width`, `height`, `seed`, `negative_prompt` all return
  `400 Additional or unevaluated properties`. Output is fixed 1024×1024 — crop to the delivery ratio.
- **Its input filter is the dominant failure** (`code 8007 Input prompt contains NSFW content`): it
  rejected forward-facing bare-chest and POV prompts while accepting clothed, from-behind, all-back
  compositions. That is a routing consequence, not a lane defect — reword or move to DashScope.
- It drops figures: a two-person brief repeatedly rendered **one**, and when it did render two it
  gave the rear figure a bun/topknot and left both pairs of ears in frame. Under-specified second
  figures get filled with a default sex and hairstyle — name them explicitly.

## Voice — substitutes when the primary TTS is quota-gated

Measured on one 84-char BM line, same gate (ASR round-trip `language=ms`, `librosa.yin` f0 median):

| Lane | Text fidelity | f0 med | What it is |
|---|---|---|---|
| the MiniMax clone in use | clean | ~96 Hz | the lane |
| edge-tts `ms-MY-OsmanNeural` | clean (~98%) | ~157 Hz | words survive; **a different speaker's timbre** |
| MiMo `mimo_default` | ~0% — recited the *user instruction* beside the target text | ~203 Hz | unusable for a persona line |
| MiMo `mimo-v2.5-tts-voicedesign` | ~38% — word-level BM collapse (`Ada`→`Ida`, `tulis`→`gulis`) | ~91 Hz | male register holds, words do not |

- **A `mimo_default` transcript scoring ~0 is its own failure class, not a mangled line** — it spoke
  the instruction, so check which string was recited before recording a pronunciation verdict.
- **Do not carry a speed/calibration figure across voices.** Re-derive it from the render's own
  duration against the accepted reference take.
- MiMo runs on a separate quota bucket, so it will render while the primary is blocked — "it produced
  a file" is not "it is a valid substitute". Score it before offering it.
- The image endpoint of the same account shares the primary's quota gate: a missing still during a
  voice outage is the same outage, not a separate prompt problem.
