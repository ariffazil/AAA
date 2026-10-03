---
name: kvm8-media-lane-fallbacks
description: "Use when an ASR, vision, PDF or TTS lane fails on KVM8."
version: 1.2.0
tags: [media, asr, vision, pdf, tts, fallback, kvm8]
---

# KVM8 Media-Lane Fallbacks (probed 2026-09-29)

When a media lane returns an auth/quota error, do not conclude "no capability" — walk this ladder. Each entry was probed live on KVM8.

## ASR (speech → text)

- **Z.AI `glm-asr-2512`** → `1113 Insufficient balance`. Dead.
- **DashScope intl** (`qwen3-asr-flash`) → `AllocationQuota.FreeTierOnly`. Dead.
- **LIVE: Groq `whisper-large-v3`**
  ```bash
  curl -s -X POST https://api.groq.com/openai/v1/audio/transcriptions \
    -H "Authorization: Bearer $GROQ_API_KEY" \
    -F model=whisper-large-v3 -F language=ms -F response_format=verbose_json \
    -F temperature=0 -F file=@clip.wav
  ```
  Also reachable via MCP `media_ingest_file` (returns transcript + lanes_tried).
- **Hallucination gate — mandatory.** Whisper invents fluent text on silence/music/grunts. Trust `no_speech_prob` from `verbose_json`: ≈0.7 on a <3 s clip plus a suspiciously clean string ("Terima kasih kerana menonton", "The", "you you you") means **no intelligible speech**, not a transcript. Local `/usr/local/bin/whisper` (small) hallucinates the same way — never treat either as evidence alone. A burp/grunt/sigh transcribes as nothing: report UNKNOWN, or ask the human what the clip contains.

## Vision (image → text)

- **LIVE (2026-09-30): `vision_analyze` on MiniMax-M3, MiniMax plan** — `auxiliary.vision` = `{provider: custom, base_url: https://api.minimax.io/v1, model: MiniMax-M3, key_env: MINIMAX_API_KEY}`. Verified through the tool in a gateway turn: verbatim OCR + colours. `MiniMax-M3` takes OpenAI-style `image_url` data-URI parts, so no special transport.
- **Out-of-band witness: `mmx vision describe --image <path>`** (same plan, MiniMax's own VLM path) and `mmx quota show` to prove plan headroom. `MiniMax-VL-01` is gone from the API (400 `unknown model`).
- **LIVE fallback: MCP `media_vision_read`** (`zai/glm-4.6v`, up to 3 images). Ask for verbatim transcription and demand "say so if unclear" — the model leaks scratchpad reasoning into its answer, so re-ask tighter when the first read looks hedged.
- **Historical**: the 401 `token_not_found_in_db` / `LiteLLM Virtual Key expected` class here was a config `${VAR}` that never expanded — `gateway.multiplex_profiles=true` resolves `${VAR}` against `/root/.hermes/.env` only, so a name present in the systemd EnvironmentFile but absent from `.env` is sent as the literal placeholder. Fix: put the name in `.env`. Full diagnosis + working wiring: `/root/AAA/evidence/VISION-ROUTE-FIX-2026-09-30.md`.
- Never narrate an image you could not read (F2). Product photos: always transcribe brand + generic + strength before giving advice.

## PDF (markdown → PDF)

- `import markdown` / `import weasyprint` fail on the default interpreter.
- **LIVE path:** `pandoc in.md -o out.html --standalone` → `/usr/local/lib/hermes-agent/venv/bin/weasyprint -s style.css out.html out.pdf`. Drop `--metadata title=` (pandoc duplicates the H1 otherwise).
- Gate: `file out.pdf` must say `PDF document`; then `pdfinfo … | grep Pages` and `pdftotext -f N -l N` to prove each page landed.

## TTS (voice notes)

- **Siti (`SSSiti20260926v1`) from KVM8:** `python3 /root/.hermes/cache/scratch/siti_call.py script.txt out.mp3` — MiniMax `speech-2.8-hd`, audio returns as **hex** (`bytes.fromhex`), not base64.
- Do **not** send `language_boost` to `POST /v1/t2a_v2` — `2013 invalid params: language_boost` is rejected. The current spec only accepts `voice_setting` and `audio_setting`; drop the field, not "set it to a different code". The MiniMax `speech-2.8-hd` model already infers language from the text.
- Source `MINIMAX_API_KEY` from `/root/.secrets/kunci-root.env`. `/root/.openclaw/.env` may exist but be empty (`key len=0`) — do not trust it; if `os.environ.get('MINIMAX_API_KEY')` returns 0-length, you read the wrong file. Working pattern:
  ```python
  for line in open("/root/.secrets/kunci-root.env"):
      if "=" in line and not line.startswith("#") and not line.startswith("export "):
          k, v = line.split("=", 1)
          os.environ[k.strip()] = v.strip().strip('"').strip("'")
  ```
- Deliver as a native voice bubble with `MEDIA:/abs/path.mp3` **plus** `[[audio_as_voice]]` on their own line; several `MEDIA:` lines in one reply do work (PDF document + voice bubble together).
- Verify every render by round-tripping it back through Groq ASR and diffing against the script — catches truncation, stutter and dropped paragraphs before a human hears it.

### TTS engine ladder (when one engine dies, walk this)

A TTS request that succeeds on engine A today may return a quota/auth error tomorrow. Don't conclude "no TTS" — fall through. Each entry was probed live; treat error codes as signals to move on, not retry.

| Engine | Endpoint | Model | Response | Failure → next |
|---|---|---|---|---|
| **MiniMax** (paid, primary) | `https://api.minimax.io/v1/t2a_v2` | `speech-2.8-hd` | `data.audio` is **hex** (`bytes.fromhex`) | `1008 insufficient balance` / `2056 quota_exceeded` → DashScope |
| **DashScope Singapore** (free tier, can exhaust) | `https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/generation` | `cosyvoice-v3-plus` | `output.audio.data` is **base64** | `403 AllocationQuota.FreeTierOnly` → DashScope China/Bailian |
| **DashScope China / Bailian** (different key, can auth-fail) | `https://dashscope.aliyuncs.com/api/v1/services/audio/tts/generation` | `cosyvoice-v3-plus` | base64 | `401 InvalidApiKey` → local F5-TTS lane below |

Cross-engine gotchas when falling through:

- The voice_id registered on engine A is **not** valid on engine B. Falling back to DashScope with `SSSiti20260926v1` returns "voice not found" — re-clone the source sample on the fallback engine, or pick a built-in voice.
- Auth header shape is identical (`Authorization: Bearer $KEY`) but the request body schema differs: MiniMax uses `voice_setting.voice_id`; DashScope uses `parameters.voice` with the `---` suffix (`cosyvoice-v3-plus-pmxreal-...---`). Copy-paste between engines fails silently.
- A 401 on DashScope China is almost always "wrong key for this region" — the `DASHSCOPE_API_KEY` env var in `/root/.secrets/kunci-root.env` is the **Singapore** key (prefix `sk-ws-H...`), not a China/Bailian key. Don't loop on Bailian; jump to F5-TTS.

## Local F5-TTS (offline clone, CPU)

Lane: `/root/AAA/engines/f5tts/` — `./venv/bin/python f5_local_render.py <ref.wav> "<ref text>" "<gen text>" <out.wav> [nfe]`. No API key, no quota, ~42× slower than realtime on 8 CPU: short clips only. Ref text must be the true transcript of the ref clip; an approximate one degrades the clone.

Four traps, all silent:

1. **Your shell runs inside the `hermes-asi-gateway.service` cgroup, capped at 8 GiB** — not the host's total, whatever `free` reports. One 5.4 GB checkpoint load fits; two concurrent ones OOM-kill at ~4.17 GB RSS each. Run heavy jobs outside it: `systemd-run --scope --slice=system.slice -p MemoryMax=24G --quiet <cmd>`. Apply to CPU renders too — a heavy job inside that cgroup competes with the live gateway.
2. **A killed download resumes into silent corruption.** Re-running `curl -C -` can reach the exact remote byte count with a wrong sha256. Size matching `content-length` proves nothing. Compare against the HF LFS oid (`curl -s 'https://huggingface.co/api/models/<repo>?blobs=true'`); if the hash fails, delete and download fresh — do not resume again.
3. **A backgrounded `nohup … &` inside a tool call dies with that call's process group.** It reports the wrapper's exit 0, not the job's. Long jobs go through the supervised background mechanism with completion notification.
4. **HF finetune checkpoints are training checkpoints** (model + `ema_model_state_dict` + optimizer + scheduler). `load_checkpoint` reads `ema_model_state_dict` and strips the `ema_model.` prefix itself, but the full 5.4 GB costs ~4 GB RSS. Extract the ema subset once with `torch.load(..., mmap=True)` (~1.5 GB peak, seconds) into a ~1.35 GB inference checkpoint, then pass it via `F5_CKPT`.

**Vocab:** a finetune of `F5TTS_v1_Base` keeps the base vocab — introspect `text_num_embeds`; 2546 = 2545 base chars + 1 confirms it, so pass no `F5_VOCAB`. Beware CRLF copies of the same vocab (identical text, +1 byte per line): they tokenise with stray `\r`.

DITEMPA BUKAN DIBERI ⚒️
