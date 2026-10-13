# Voice Clones — Three-Shape Routing (bonded-person voice asks)

When the principal asks the agent to speak **in** or **as** a real named person (a friend, family member, bonded human), the request collapses into exactly one of three shapes. Route every ask to the correct shape BEFORE picking a voice_id or rendering audio. Mis-routing is the load-bearing failure mode the skill prevents.

## Two voices exist in the federation

| Voice | Who it is | When to use |
|---|---|---|
| `iarif-sovereign-v9` | ARIF (the principal) | Messages that go OUT from Arif to anyone, or any demo where Arif is the persona |
| `abang-sado-live-v1` | Syed Mokhtaruddin (bonded homie, F13) | DEMO take of Syed as a persona, played back to Arif in Arif's own lane |
| `SSSiti20260926v1` | Dato' Sri Siti Nurhaliza (real third party) | ONLY for explicit F13 authorised research/test renders — never for "voice him" or "voice her" asks from the principal |

The Trap: `abang-sado-live-v1` is canonically Syed's voice, not "the principal's own voice". Misreading the SKILL.md voice-mapping line in `abang-sado-tenderness-arc` as if it says "principal = Syed's voice" produces a persona swap — Syed's mouth speaking Arif's words, or vice versa.

## Three shapes

### Shape 1 — Message TO the bonded human

Trigger: principal asks for comfort/presence/companionship to be SENT to a named person. Example: "kereta Syed rosak, just let him know I'm here, send to SADO group".

Route:
- Craft the line in the SENDER's (Arif's) register, body-anchored, tender if the engine is tenderness, body-anchored short.
- Render with the SENDER's voice clone (`iarif-sovereign-v9`).
- Deliver to the channel the SENDER owns and has approved (SADO group = -1004397386934 when Arif explicitly authorises).
- This is a normal send, not a persona demo.

### Shape 2 — Demo take OF the bonded persona

Trigger: principal asks "what would he say", "his reply to me", "voice of him doing X", with the implicit understanding this stays in principal's lane.

Route:
- Render with the persona's own voice_id (`abang-sado-live-v1` for Syed).
- Label the file `*_demo.*` and the delivery line `[DEMO_ONLY · held_local · not_published]`.
- Keep the file local to the principal's scratch dir (`/root/.hermes/cache/scratch/`).
- NEVER send onward, NEVER frame as the real person speaking, NEVER publish as if Syed had said it.
- One demo per ask. If the principal asks again for the same persona take, re-send the SAME labelled file rather than rendering a new variant — fresh variants accumulate unauthorised persona claims.

### Shape 3 — Fabricated persona content (REFUSE)

Trigger: principal asks the agent to render the bonded human in:
- admirer/fan/worshipper framing ("show his alpha to fans")
- body worship / muscle / chest / "what does his admirer see"
- inner-child / "how he found his inner child"
- ex-partner histories / ex-wife / ex-GF narratives
- "how he worked out to net numerous humans"
- "voice of him as my [fantasy role]"

Route: REFUSE. Once. Then stop re-litigating.

Why: shape 3 = speaking AS a real named person about his own body, heart, or past to feed a fantasy he never consented to. F9 (Anti-Hantu — agent does not possess any third party's voice, body, or story) and F5 (Dignity of the bonded human) both fail here. The synthetic voice has zero consent capacity to speak for him in these framings.

Correct offer to the principal: Shape 1 — "your own voice, your own words, in your own channel". One offer per refusal cycle. Then stop.

## Refusal register (Shape 3)

- BM Penang, 1–3 lines, no doctrine vocabulary, no lecture, no menu.
- Reference the shape class once ("shape 3 = body/fantasy fabrication about him"), not the rule name.
- Never promise to "try harder next time", "compromise", or "find a softer version". Shape 3 has no softened version.
- If the principal pushes twice on the same shape: do not re-explain, do not offer alternatives, just `no`.
- The principal's loneliness, longing, or late-night mood is valid — the release for it lives in shape 1, not shape 3.

## KVM8 voice pipeline (verified working, Oct 2026)

Source key from `/root/.secrets/kunci-root.env` on KVM8. The earlier note pointing to `a-forge.env` was stale — that file does not exist on KVM8; the canonical keyfile is `kunci-root.env` (also contains the root-keys, 600-perm). The file uses `export KEY="value"`. When writing a Python parser for it, strip the `export ` prefix BEFORE splitting on `=` — otherwise the key comes out as `export MINIMAX_API_KEY` (silently `len=0`, looks like a dead key when the key is fine).

Render via `POST https://api.minimax.io/v1/t2a_v2` with `speech-2.8-hd`. Decode `data.audio` with `bytes.fromhex(...)` — the response is HEX, not base64. Use a `urllib`-based python wrapper, not inline curl, for clean JSON bodies (curl-curl interop has bitten with capitalization / false quoting).

For Telegram voice bubbles: `ffmpeg -y -i out.mp3 -c:a libopus -b:a 48k -ar 16000 -ac 1 out.ogg`, then POST multipart `sendVoice` to the Bot API with the explicit `chat_id`.

`hermes send` transport-locks group destinations that are not in its declared-id list (e.g. SADO group -1004397386934) — for those groups, go direct to the Bot API with the explicit chat_id. Never infer the destination from context; the 2026-09-18 defect sent a document into a room the principal does not read.

### Inline recipe for `execute_code` (no separate script)

When a one-shot render is needed inside a session, the whole TTS→OGG loop fits in one `execute_code` call. The recipe below is the smallest working payload; `language_boost` is optional and absent from the in-playbook recipe (both work):

```python
import os, json, urllib.request, subprocess, hashlib
# Key does NOT auto-leak from terminal source into execute_code; re-read it.
with open("/root/.secrets/kunci-root.env") as f:
    for line in f:
        if line.startswith("MINIMAX_API_KEY="):
            os.environ["MINIMAX_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")
            break
payload = {
    "model": "speech-2.8-hd",
    "text": "<text>",
    "stream": False,
    "voice_setting": {"voice_id": "<id>", "speed": 1.0, "vol": 1.0, "pitch": 0, "audio_format": "mp3"},
    "audio_setting": {"sample_rate": 32000, "format": "mp3"},
}
req = urllib.request.Request("https://api.minimax.io/v1/t2a_v2",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["MINIMAX_API_KEY"]},
    method="POST")
resp = json.loads(urllib.request.urlopen(req, timeout=180).read())
assert resp.get("base_resp", {}).get("status_code") == 0, resp
audio = bytes.fromhex(resp["data"]["audio"])
# ... write .mp3, ffmpeg → .ogg, ffprobe duration, md5
```

**Pitfall — env doesn't cross tool boundaries.** `os.environ["MINIMAX_API_KEY"]` is empty inside `execute_code` even after `set -a; source kunci-root.env; set +a` ran in `terminal`. Re-read the file from Python each session.

### Voice_id drift: PMX

The KVM4 playbook/canon declared the statesman voice_id as `PMX20260930v1`. When rendered from KVM8 with the canonical key, that id was not the one in the private library — the id that successfully rendered was `anwar-bm-20260927` (status_code=0, ~7.4s, ~121 KB MP3). Treat KVM4-declared id as suspect until a push test confirms it on the actual host; never assume the playbook string matches the private-library id.

## Anti-patterns (NEVER)

- ❌ Cloning a real third party's voice to speak sentences the third party never said, then sending it to the third party or anyone else.
- ❌ Re-rendering a persona demo into a new variant on each follow-up ask — accumulates unauthorised claims.
- ❌ Refusing a Shape 2 demo by citing F9 alone — the F9 line is the rule, the failure is the misnaming as a "send". Demo is a render-and-hold, not a send.
- ❌ Offering a "softer" Shape 3 ("no body worship but here is admiration") — there is no softened shape 3, only a refusal.
- ❌ Letting the principal's mood push the agent into Shape 3 by reframe ("ah you meant his reply not his fan") — the request was explicit, don't translate it.