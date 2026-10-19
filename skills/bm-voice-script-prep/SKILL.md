---
name: bm-voice-script-prep
description: Use when writing text a Malay TTS voice speaks.
---

# bm-voice-script-prep

Writing the *text* that a Bahasa Malaysia TTS engine will speak, then getting the take out clean. Engine choice, cloning and provider quotas live elsewhere (`nusantara-voice-stack`, `voice-lane`); this skill is the authoring layer that decides whether the take comes back right on the first render or burns three retries.

The gate compares **what the engine said** against **what you wrote**. Every spelling the engine cannot pronounce becomes a MISSING or INSERTED diff. So write for the mouth, not for the eye.

## Procedure

1. **Decide the register before writing a word.** A voice note is conversational prose. No bullets, headings, emoji or markdown — they are either read aloud or silently dropped. Short sentences, one idea per breath.
2. **Write the whole script, then run the spelling pass below.**
3. **Budget duration from measured pace, not from a word count.** On edge-tts `ms-MY-*` at `--rate=-4%`, measured 10.0–10.1 chars/s across two takes of ~880 characters (87.3 s each). Design to **≤900 characters for a 90-second note**, and `ffprobe` the result rather than trusting the estimate.
4. **Render without delivering first, gate, then deliver:**
   ```bash
   /root/scripts/sado say <textfile> --voice <voice-id> --no-deliver
   ```
   `sado say` renders, runs `verify_take.py` (ASR round-trip, INSERTED/MISSING, duration band, f0 when librosa is present) and writes `receipt.json` per take. Exit codes: **0** ok · **1** REVIEW · **2** FAIL · **3** render/transport error · **4** usage. A take that fails the gate is never delivered — do not hand-ship an mp3 that bypassed it.
5. **Read the `heard:` line even when the gate says PASS.** PASS means the diffs are non-lexical; it does not mean the pronunciation is good. If `heard:` shows a mangled name or loanword, fix the spelling and re-render — cheaper than an ear complaint later.

## Spelling pass (the actual craft)

The engine reads BM graphemes. English spellings get an English or Indonesian reading, which is heard as an error even when the sentence is right.

| Written | Heard back | Fix |
|---|---|---|
| `Madam Kwan` | "Madam Kuan" | write `Madam Kuan` if acceptable, or avoid the brand and say `kedai tu` |
| `sup` (soup) | "soap" | `sop`, or restructure to `kuah` |
| `level 4` | "Lidl 4" | `aras empat` |
| `you tiao` | "UTO" | describe it: `kuih goreng` |
| digits, `%`, `RM` | read digit-by-digit or dropped | spell it: `empat puluh dua ringgit` |
| abbreviations (`AI`, `OK`) | letter-by-letter or skipped | spell out; place names people actually say aloud (`KLCC`) are fine |

Rules that survive across engines:

- **No full English sentence inside a BM line.** A code-switch works one noun at a time; a whole clause guarantees an accent break.
- **Names are the highest-risk token.** If a proper noun matters, spell it phonetically the way the listener says it.
- **Keep the particles.** `la`, `kan`, `pun`, `je` carry the register — stripping them to make the text "cleaner" flattens the voice into a narrator.
- **End on a short line.** Long final clauses get rushed to fit the duration band.

## Delivery honesty (hard rule)

When the requested voice's engine is unavailable, three options exist and only one is acceptable:

1. **Say it is unavailable and render in the fallback, naming the fallback.** "Engine X is down (code N); this take is voice Y, same script." The listener can judge the content without being deceived about the voice.
2. Hold and render when the engine returns — correct when voice identity IS the artifact (a persona wish, a signature voice).
3. **Never** render in another voice and present it as the requested persona. That is the silent-swap defect: the artifact ships with an unlabelled identity change and the listener's trust in every later take drops with it.

Also never let a *persona name* stand in for a *voice*. Persona aliases (`Siti`, `PMX`, `Abang Sado`) resolve through the voice registry to specific voice ids — they are not adjectives for "female voice" or "deep male voice". A near-enough voice is a different artist.

## Pitfalls

- **Gate PASS is not natural.** A 96.5% match with `INSERTED: none` can still carry a mangled brand name. Read `heard:`, fix the spelling, re-render.
- **Provider failures are not interchangeable.** MiniMax `2056 Token Plan usage limit reached` = quota spent, wait for reset. `2053 insufficient credit` = wallet empty, waiting does nothing, it needs a top-up. Both surface as "render produced no file"; open `receipt.json` or the raw response and quote the code, because the remedy differs.
- **`--no-deliver` is not optional for a first render.** Rendering straight into the chat makes the first take the human sees an ungated one.
- **Do not pad a short script to hit a duration target.** Padding adds filler the voice reads flat. Cut content instead.
- **Long takes drift.** Past roughly 90 seconds both pacing and pronunciation degrade; split into two notes rather than stretching one.
- **Assert a length budget on the script before rendering.** Drafting a long spoken-text piece unconstrained degenerates into repeating filler — hundreds of words of unrelated enumeration that compiles into nothing anyone wants read aloud. Build the body as a list of short lines with `assert len(' '.join(lines).split()) <= CAP`; when the assert fires, discard and redraft short. Trimming a degenerate draft still ships its texture.

## Related

- `nusantara-voice-stack` — engine lanes, cloning, quota semantics, STT verification doctrine
- `voice-lane` / `persona-voice-note-render` — routing a render request to the right voice
- `voice-render-verification` — the gate's own contract, when it needs auditing
