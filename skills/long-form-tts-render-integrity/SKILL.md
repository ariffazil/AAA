---
name: long-form-tts-render-integrity
description: "Use when a TTS render runs long or in chunks."
version: 1.0.0
tags: [tts, voice, audio-integrity, minimax, pipeline]
---

# Long-form TTS Render Integrity

Scope: any spoken artifact built from more than one synthesis call — a 3-minute persona act, a
multi-paragraph answer, a paragraph-per-call loop. Act structure and persona craft live in the arc
skills; this skill owns the plumbing claim: **the file that ships contains every word that was written,
at the length that was predicted, from the credential that actually has credit.**

## 1. Size from a LONG take, never a short one

A cloned voice at speed 0.95 on this host lands **11.7–12.1 chars of input per second** of audio
across 2–3 minute takes (measured: 1465 ch → 123.8 s, 2053 ch → 175.4 s, 2000 ch → 165.0 s,
2066 ch → 174.5 s). A 20 s probe reads ~13 chars/s and over-predicts a 3-minute script by ~15 %.

- Budget at **11.8 chars/s**; a 3-minute act is ~2050–2100 characters.
- Hit the duration by editing prose, never by raising speed — speed changes f0 scatter
  non-monotonically and does not buy clean time.
- Print `round(len(text)/11.8, 1)` before rendering, and re-probe after the first real take:
  engine-side chars/s drifts with text, so the band is a budget, not an invariant.

## 2. The chunk loop must FAIL CLOSED

A clause/paragraph loop that skips a chunk which produced no audio will still concatenate the rest:
the take sounds finished, the ASR ratio lands in the 80s, and the gate reports `REVIEW` — never
`FAILED` — so a truncated act can ship with a plausible-looking receipt.

```python
for i, cl in enumerate(clauses, 1):
    ok = False
    for attempt in range(1, 4):
        run_render(cl, mp)
        if os.path.exists(mp):
            ok = True; break
        time.sleep(2 * attempt)
    if not ok:
        die(3, f"clause {i}/{len(clauses)} failed: {last_err}")   # abort, do not continue
```

Rules:
- Retry a couple of times (transient provider errors are real), then **abort with a non-zero exit**
  naming the clause index and the partial count.
- Never deliver on a `REVIEW` whose `MISSING` list is a contiguous tail of the script — that is a
  truncation signature, not an alignment artefact.
- A per-clause render is 1–3 s of wall clock, but 45 clauses takes ~3 minutes: budget **two long takes
  per foreground call** (600 s cap) and keep each act's output in its own work directory so a resumed
  run does not overwrite finished chunks.

## 3. Resolve WHICH credential the engine reads

A render that fails with `insufficient credit`, or an `HTTP 404` for a voice id that worked yesterday,
is usually credential routing, not the voice:

- The `mmx` CLI reads `api_key` from **`~/.mmx/config.json`**, not `MINIMAX_API_KEY` from the
  environment. A retired key parked in that file shadows a funded env key and presents as an empty
  wallet. Compare without printing either value:

```bash
python3 - <<'EOF'
import json, os, hashlib
h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]
cfg = json.load(open('/root/.mmx/config.json'))['api_key']
print('config', h(cfg), 'env', h(os.environ.get('MINIMAX_API_KEY','')))
EOF
```

  Back the file up, write the live key in, re-probe one short line.
- `--base-url` takes the **host only** (`https://api.minimax.io`). Passing the synthesis path
  (`.../v1/t2a_v2`) returns `HTTP 404` — a routing error wearing the costume of a missing voice.
- A registry status of `LIVE` proves the registry, nothing about credit. Verify with one 3-word render
  and check the file exists and has a sane duration before spending 3 minutes of chunked calls.

## 4. Gate noise specific to long Malay takes

- **Hyphenated reduplication.** `main-main`, `lama-lama`, `kadang-kadang` transcribe as two separate
  tokens and the aligner flags one as `MISSING`, dragging the ratio to 96–98 %. Read the `heard` string:
  if the compound is present in un-hyphenated form and duration sits in band, the take is clean —
  re-rendering identical text reproduces the same flag.
- **Dialect respellings are not defects**: `sado`→`sadur`, `gelak`→`gelap`, `puja`→`puyak`. Judge by
  whether a listener hears the written word, not by token equality.
- Confirm the close of the script appears in `heard`. The last line is where a truncated or
  seam-defective take shows up first.

## 5. Convert and re-probe after the gate

Gate the engine's own `take.mp3`, then convert for delivery and re-read duration on the converted file:

```bash
ffmpeg -y -loglevel error -i take.mp3 -c:a libopus -b:a 48k -ar 48000 out.ogg
ffprobe -v error -show_entries format=duration -of csv=p=0 out.ogg
```

Report each act's real runtime from `ffprobe`, not from the estimate. If an act lands short of the
requested length, say the true number — never pad with filler sentences to make the clock.

## Pitfalls

- A short check take is the worst duration oracle. Calibrate on the artifact you actually ship.
- A `continue` in a chunk loop is a silent truncation primitive. Any loop that can drop a unit of
  text must end in an explicit abort.
- Do not change voice id, model or speed to explain a provider error. Probe the credential and base URL
  first; the voice is the last suspect.
- `librosa` absent on the host's bare `python3` → the f0 family check reports `SKIPPED (not a pass)`.
  Do not read that line as verification; state it as unmeasured.
- Registry work is append/propose, not rewrite: pull the entry into the report, do not silently re-seal it.
