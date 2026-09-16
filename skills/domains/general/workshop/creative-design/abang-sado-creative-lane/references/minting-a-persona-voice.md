# Minting a new persona voice

When the voice a request needs does not exist yet. Applies to any persona register: the commands and
mechanics below are provider-level, the prompt is the register-specific part.

## 1. Decide first: design or clone

Two independent questions, asked in this order. Only the first can make the ask out of scope; the second
decides which artifact to build.

**Q1 — where did the source audio come from?**

| The source | The lane |
|---|---|
| A synthetic render: a take you produced earlier, or a provider's stock/system voice (`Indonesian_BossyLeader` and friends) | **Clone is in scope.** No human waveform is anywhere in the chain. |
| His own recorded voice | Clone is in scope (ownership). |
| A named third party, a public figure, audio found online or forwarded in a voice note | **HOLD / design only** — when the agent decided on its own initiative, or a third party is asking. A human voice is a biometric identity and clone-without-consent is forbidden, not gated. |
| The same case, but the sovereign directs it in his own orbit and has answered the consent probe | **In scope, with the gap on the record.** Probe once, re-probe the file state, then execute and record `consent asserted by F13 in-chat, no entry on file for this speaker` in the work-dir receipt. His judgement governs his own lane; the registry holds the record, not the decision. Holding a second time is the permission-lecture failure; proceeding with no provenance line is the mirror failure. |

Performing the clone is not the same act as writing the consent. One move stays forbidden no matter who
asserts what: putting a consent entry under `/root/WELL/envelopes/_consent/` on someone else's behalf —
only the person themselves can grant one — or promoting the id into the identity registry as a Hermes
default. Direction taken + provenance line written keeps "he directed it" honest instead of laundered.

**Q2 — if the source is synthetic, which artifact does the ask actually want?**

"Same voice, redone" means *preserve the timbre that already exists* — run the clone. A design render is
a DIFFERENT voice. Measured against the reference it was written from: a provider-side clone lands at
MFCC cosine ≈0.999 and Δf0 ≈0 Hz, while a design in the same register lands ≈0.993 with a ~15 Hz f0 gap.
Substituting a design for a requested clone ships an artifact that does not match the brief, and the
requester says so — *"dah ada, buat ja"*. Design is the FALLBACK, for exactly two situations: the source
is a human without consent, or the clone lane is genuinely dead. Probe the lane before assuming the
second (see the invalid-id probe below) — a capability you did not test is not absence.

Cloning a stock voice is not a copy of anything a person owns: the stock voice is the vendor's own
synthetic model, and what comes back is a derived synthetic voice on the account. Declare the chain in
one line — "cloned from the synthetic render, no human audio in the chain" — and move on. Not a
paragraph, and never an explanation of why a design would have been better.

## 2. Where the capability lives

The `mmx` CLI synthesizes an EXISTING voice id (`speech synthesize` / `generate` / `voices`). It has no
design or clone verb, so both are REST calls. Use the same key the CLI uses and read
**`base_resp.status_code`**, not the HTTP status: MiniMax answers HTTP 200 with the real result nested
inside `base_resp`.

```python
import json, re, binascii, urllib.request

env = {}
for line in open('/root/.secrets/kunci-root.env'):
    m = re.match(r'^(?:export\s+)?([A-Za-z0-9_]+)=(.*)$', line.strip())
    if m: env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
KEY = env['MINIMAX_PLUGIN_API_KEY']

req = urllib.request.Request(
    "https://api.minimax.io/v1/voice_design",
    data=json.dumps({"prompt": PROMPT, "preview_text": PREVIEW}).encode(),
    headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
d = json.loads(urllib.request.urlopen(req, timeout=180).read().decode())
open("trial.mp3", "wb").write(binascii.unhexlify(d["trial_audio"]))   # HEX, not base64
# d["voice_id"] is usable immediately as `--voice` in the CLI
```

- **`trial_audio` is hex.** `binascii.unhexlify` it before writing, or you ship a large text file
  wearing an `.mp3` extension.
- **Probe a capability without creating anything.** Call with a deliberately invalid id and read the
  error instead of assuming: `POST /v1/voice_clone {"file_id": 999999999, "voice_id":
  "probeNotCreated"}` returns `base_resp.status_code 2013 "invalid params, file_id not exist"`. That
  proves the verb exists and the key reaches it, with zero side effects and no billing. Do this before
  declaring a lane unavailable, and before spending a real upload on it.
- **Clone mechanics.** The endpoint consumes a file already in MiniMax storage, not a local path:
  1. `POST /v1/files/upload` — multipart, `purpose=voice_clone`, `file=@ref.mp3` → `file.file_id`
  2. `POST /v1/voice_clone` — `{"file_id": …, "voice_id": "abangSadoRef01", "model": "speech-2.8-hd"}`
     → `base_resp.status_code 0`. This payload was accepted without `text` and without
     `clone_prompt.prompt_audio`; if the API answers `2013 prompt_audio or audio_url is required`, add a
     5–8 s clip uploaded with `purpose=prompt_audio` (under 5 s → `2037 too short`, over 10 s →
     `2048 too long`).
  3. Synthesise with `--voice <voice_id>` — usable immediately, no hydration wait.
  `voice_id` rules: ≥8 chars, starts with a letter, contains both a letter and a digit, no trailing
  `-`/`_`; a duplicate id returns `2039` and the existing clone still works. Billed on first use.
- **Reference length and cleanliness set the fidelity ceiling.** A clean 42 s single-voice render cloned
  at MFCC cosine 0.9997 / Δf0 0.2 Hz against its source. The 10 s API minimum is a floor, not a target.
- **A cloned checkpoint can speak words the input never contained**, and input sanitisation cannot catch
  it because the insertion happens inside synthesis. Every delivery on a clone needs an ASR round-trip
  (`language=ms`) diffed against the input line — read it for INSERTED clauses, not only garbled ones.
  Clean on one take is evidence for that take, not a property of the voice.
- **Sourcing a vault script is not the same as sourcing the shell.** `set -u` plus a secrets file
  holding `$apr1$…`-style hashes aborts on `unbound variable` before any key loads. Use `set +u; set
  -a; source <env> 2>/dev/null; set +a; set +u` — the failure presents as a missing key.

## 3. Prompt rules (they matter more than the template)

Four facets, prose not keywords: identity (age, gender, ethnicity/region) · vocal quality (pitch,
resonance, breathiness, texture) · accent/language · pace and delivery (what the voice DOES).

- Conflicting descriptors cancel — the model picks one and drops the other.
- "Theatrical / dramatic / exaggerated" produces over-acting. Name the restraint instead.
- One accent, not two.
- Say what it NEVER does ("never hurried", "no shouting, no pleading"). Negatives carve harder than
  positives here.
- Close on pitch, and treat that close as a request, not a promise — the rendered pitch can land well
  below what was asked for. Measure the take; do not quote the brief back.

## 4. Register it before it ships

The id goes into `/root/AAA/audio/voice-registry.json` before any take leaves the building. Back the
file up first (`cp voice-registry.json voice-registry.json.bak-$(date -u +%Y%m%dT%H%M%SZ)`), add the
entry, bump `updated_at` / `updated_by`. Never delete or rewrite an existing entry — revocation is
append-only: flip `status` to `REVOKED` and record `revoked_at` / `revoked_by`.

Carry: `provider_voice_id`, `model`, `endpoint`, `archetype`, `provenance`, `consent`,
`f9_compliance`, `preferred_settings`, and a `runtime_measured_*` block.

`provenance` + `consent` are the load-bearing pair. The entry that passes reads
`parametric_voice_design — original voice from a written description; NOT derived from any real
person's audio`. If you cannot state in one line where the voice came from, it does not ship.

**Never write a `consent` value that reads as a granted consent you did not receive.** A clone whose
source was a human voice and whose clearance exists only as a sovereign assertion carries that
sentence verbatim in the field — `sovereign-asserted in-chat, no consent entry on file for this
source` — plus the date. That is what distinguishes a recorded gap from a forged record: the field
tells the next session exactly what evidence exists, so it can re-ask if it should. A designed voice,
or a clone of a synthetic source, is simply `original_voice_from_qualia_description` /
`synthetic_source_no_human_audio` and needs no such caveat.
`runtime_measured_*` records what was MEASURED, not what the design spec claimed — a declared figure
that does not survive a re-render belongs under `design_spec_declared`, marked as such.

## 5. Recalibrate, then QC

Speed does not transfer between voices. Render once with the new id, read the printed `duration_ms`
(or `ffprobe`), and compare against the accepted reference take for the same line; step the speed
toward 1.0 until the two match. Then run the gate on the calibrated take —
`python3 scripts/verify_take.py take.mp3 --text line.txt --source <reference.mp3>` covers the
round-trip, the normalised diff and the f0 comparison in one pass (`scripts/tts_roundtrip_qc.sh`
remains the lighter text + timestamps version).

Compare the two takes on measured median f0 (`librosa.yin`, 60–350 Hz) as well as duration — that is
what makes "deeper" a claim rather than a vibe, and it catches a design that landed far from the
brief.
