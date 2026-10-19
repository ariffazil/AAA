---
name: voice-identity-provisioning
description: "Use when adding or repairing a voice in the registry."
version: 1.0.0
author: Hermes
license: arifOS
tags: [voice, tts, registry, persona, provisioning, f0, edge-tts, minimax]
metadata:
  hermes:
    category: audio
    related_skills: [voice-engine-fallback-chain, voice-render-verification, persona-voice-binding, abang-sado-tenderness-arc]
---

# Voice Identity Provisioning

Owning the *birth* of a voice: choosing it from what the machine already has, measuring it, writing
the registry entry, wrapping it in a script, and announcing it honestly.

Triggers: a persona needs a voice not yet in the registry; the registry has no voice for a register the
principal asked to hear; every metered TTS engine is empty and a wallet-free lane is needed; an entry
must be corrected, aliased, or re-pointed at a provider id.

This skill does NOT own the failover ladder (→ `voice-engine-fallback-chain`) or the render gate
(→ `voice-render-verification`). Do the procedure here, then obey those two for engine choice and
verification.

## 1. Inventory before you buy

Never open with a provider proposal. Open with what is already installed:

```bash
which edge-tts piper ffmpeg
edge-tts --list-voices | grep -i -E "^ms-|^id-"      # Malay / Indonesian registers
```

A local neural TTS binary costs nothing per character and survives an empty wallet — the right
material for a fallback identity. It is a DIFFERENT VOICE, so it gets its own registry entry (§3),
never a silent substitution into an existing one.

## 2. Measure the candidate before choosing it

A voice name describes a language and a default register; it does not describe what the principal will
hear. Render a one-line take per candidate at the intended pitch/rate, then measure median f0.

No librosa? Autocorrelation is enough (numpy in any project venv; a bare `python3` here may lack it):

```python
import subprocess, numpy as np
x = np.frombuffer(subprocess.check_output(["ffmpeg","-v","quiet","-i",P,"-ac","1","-ar","16000","-f","f32le","-"]), np.float32)
SR, WIN, HOP = 16000, 640, 320
vals = []
for i in range(0, len(x)-WIN, HOP):
    fr = x[i:i+WIN]
    if np.sqrt(np.mean(fr**2)) < 0.02: continue
    fr = fr - fr.mean()
    ac = np.correlate(fr, fr, "full")[WIN-1:]; ac /= (ac[0] + 1e-9)
    lo, hi = int(SR/300), int(SR/60); k = int(np.argmax(ac[lo:hi])) + lo
    if ac[k] > 0.30: vals.append(SR/k)
print(len(vals), np.median(vals), np.percentile(vals, [10, 90]))
```

With librosa, prefer the pyin recipe in `voice-render-verification` §6; the two should agree within a
few Hz on a clean take. Autocorrelation can latch an octave out on noisy or breathy takes.

Choosing rules:

- Low f0 is the single largest contributor to a perceived heavy / calm / alpha register.
- Pushing a bright voice down with a large `--pitch` offset sounds hollow or artefacted; a naturally
  low voice at a small offset sounds relaxed. Probe both — do not reason from the name.
- Accent and f0 trade off. Say which one you gave up instead of presenting the result as free.
- Report the measured median, and label one take as a snapshot, not an invariant.
- `speed` / `pitch` are the only knobs on a fixed provider voice id. Timbre cannot be tuned.

## 3. Registry entry shape (the load-bearing part)

The registry is the single source of truth (`/root/AAA/audio/voice-registry.json`). A new voice is
invisible to every resolver until it is in here.

Required for a parametric (non-clone) voice:

| Field | Value |
|---|---|
| `status` | `LIVE` |
| `provider` / `provider_voice_id` | engine name + the id the engine actually consumes |
| `pitch` / `rate` | exact offsets used, so the render is reproducible |
| `provenance` | `parametric_voice_design — <engine> <id> with offsets; NOT a clone, NOT derived from any real person's audio` |
| `identity_note` | one line: synthetic archetype, not a recording of anyone |
| `fallback_of` | the precedent voice's id, when one exists |
| `measured_<date>` | f0 median + method + STT round-trip figure, labelled as a snapshot |
| `lane` | what register it serves |

Then all three, or the entry is half-wired:

1. **Alias** the principal's natural trigger phrase in `aliases` (`"abang sado edge"`, `"suara X"`).
2. **Add it to `lane_precedence.<lane>.alternates`** and write a `fallback_rule` naming the condition
   ("only when the precedent voice's provider returns a credit/quota failure") and requiring an
   announcement in the same turn.
3. **Never touch `precedent_voice`.** A new rung is `fallback_of`, not a replacement. Demoting the
   precedent is the principal's call, not the agent's.

Back the file up first (`voice-registry.json.bak-pre-<change>`), write with `json.dump(indent=2,
ensure_ascii=False)` so diffs stay readable, then re-read the entry.

## 4. Wrapper script, not hand-typed steps

Every take is the same six steps: render → gate → deliver → receipt. Hand-typing them is how a step
gets dropped. Ship a script BESIDE the existing lane script, never inside it:

- `say <textfile|-> [--no-deliver]`
- resolve the voice **from the registry by key**; abort if `REVOKED` (fail closed)
- render into a fresh `take-<timestamp>/`, chmod 700 dir / 600 files
- run the STT round-trip gate; a gate failure NEVER delivers
- deliver to the declared target from the config file, not from ambient context
- write `receipt.json` in the take dir: gate text, match %, inserted/missing, engine id

Exit codes carry meaning: `0` ok, `1` gate REVIEW, `2` gate FAIL, `3` render/transport, `4` usage.
A caller that only checks 0/non-zero cannot tell "wrong words" from "no wallet".

## 5. Announce the swap, always

Same turn as the artifact, name: engine, voice id, measured f0, and the compromise (accent,
brightness, missing expressiveness). State that this lane is now the fallback and the primary resumes
when topped up.

A fallback that lands indistinguishable from the primary is a claim. One that names its own compromise
is a receipt.

## Pitfalls

- **A CLI's own config file can beat the environment.** Exporting the correct API key into the shell
  still uses whatever key sits in the tool's config file (`~/.mmx/config.json` for `mmx`). Resolve the
  key from the config file, back it up before editing, re-probe — a wrong-plan key reports as a
  quota/credit error and is indistinguishable from an empty wallet.
- **"insufficient credit" is not interval quota.** Quota resets on a timer; an empty wallet does not.
  Probe the exact message before telling the principal when the lane returns.
- **One good render does not mean the lane is alive for the next request.** A metered engine can drain
  between takes; probe with a one-word render before promising a long one.
- **Do not re-render to satisfy an ASR collapser.** A gate `MISSING` of a numeral or a doubled word is
  a transcription artifact, not a dropped word — diff the token streams before spending another
  render, and report the verdict as REVIEW with your reasoning beside it (`voice-render-verification`
  §3.1). A numeral in the script (`dua tiga kali`) is the most common false MISSING.
- **A parametric voice is never a clone.** Write `provenance: parametric_voice_design` and say it out
  loud. If a clone already exists for that persona, the parametric one is a fallback rung, not a
  better version of it.
- **Do not hardcode a fallback voice id inside another skill's body.** Point at the registry key; ids
  drift, and the alias is what the principal actually types.

DITEMPA BUKAN DIBERI ⚒️