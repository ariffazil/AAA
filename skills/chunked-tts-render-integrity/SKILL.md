---
name: chunked-tts-render-integrity
description: "Use when a TTS take is rendered in chunks."
version: 1.0.0
tags: [tts, voice, integrity, render-pipeline]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Chunked TTS Render Integrity

Applies to any synthesis path that renders one script in pieces — clause-split / sentence-by-sentence
rendering, per-paragraph batches, multi-act arcs — and then concatenates them into a single take.
The corpus this came from is BM persona voice (`/root/scripts/sado --clause`), but these are chunk-loop
rules, not engine rules.

## 1. A chunk loop must fail CLOSED

The failure shape to look for in any renderer:

```python
for chunk in chunks:
    render(chunk, out)
    if not os.path.exists(out):
        continue          # <-- the defect
    parts.append(out)
```

`continue` concatenates the survivors. The take ships **missing its tail**, the script file on disk is
complete, and nothing raises. Downstream the only signal is a match ratio dropping from ~97% to ~80%
with a ~40-token `MISSING` list — which reads exactly like ASR noise, so it gets waved through.

Rule: bounded retry per chunk (3 attempts, short backoff), then abort the whole take with the chunk
index, the total chunk count and the provider error, and exit non-zero. A partially rendered take must
never reach the gate, let alone the human.

## 2. Measure length against the full input, not the file

- Calibrate the rate once with a short take: `chars_per_sec = len(text) / duration`. BM persona clones
  land ~10–13 chars/s with clause gaps; a system voice with paragraph pauses runs ~13.
- `expected = len(full_script) / chars_per_sec`. Rendered duration under ~85% of expected is a
  truncation, whatever the gate verdict says.
- Independently confirm the **final scripted clause** appears in the ASR `heard` string. On a 2–3
  minute take the tail is the entire payload.

## 3. Triage a gate REVIEW on a long take — three different causes

- `MISSING` words absent from `heard` at a short clause junction → genuine swallow; reword the clause
  and render once.
- `MISSING` words plainly present in `heard` → aligner phantom; ship unmodified.
- `MISSING` list of dozens of tokens that are all at the END of the script → truncated take; fix the
  loop (§1) and re-render the whole act.

Score alone cannot separate these: a long take dilutes the ratio, so one real defect and one phantom
both read as "96% and a bit". Read `heard`.

## 4. Chunking and pacing that actually helps

- One sentence per chunk, 0.32–0.42 s silence between. Render clause-split whenever a single-shot call
  flattens the pitch: one long call rides a single contour and loses the breath between sentences.
- Hyphenated BM reduplication (`main-main`, `lama-lama`) can round-trip as one token and produce a
  phantom `MISSING` of the second half. Do not re-render for it; if the score drops, say so in one
  clause when delivering.
- Long takes are slow to render (a 3-minute act at clause level ≈ 2–4 minutes of wall time). Render at
  most two long acts per foreground call; a loop of four gets promoted to a background job you then
  have to poll, and the deliverable arrives late.

## 5. Before blaming the wallet, check credential resolution

An "insufficient credit" message is not evidence the account is empty. CLI TTS wrappers often read
their key from their own config file, not from the shell's env var, so a stale key in config fails
while a live key for the same provider sits unused in the environment. See
`references/provider-credential-and-endpoint.md` for the diagnostic order and the fake-404 trap.

## 6. Delivery line

State duration and the gate verdict, name the voice id once, and do not narrate retries or pipeline
internals. If an act came out short of the requested length, say the number and that you did not pad
it with filler — never inflate a script to hit a clock.
