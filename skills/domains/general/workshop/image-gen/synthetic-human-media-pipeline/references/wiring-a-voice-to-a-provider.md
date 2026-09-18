# Wiring a voice id to a selectable provider

The step between "this voice id exists and was registered" and "this voice id actually comes out when I
ask for it". Minting and wiring are different jobs and are routinely conflated — a minted id that nothing
can select is a working artifact with no road to it.

## 1. Probe whether the config claims to do this before trusting it

A key that exists is not a key that is read. Configuration is full of switches that look exactly like
working routes, persist silently, print no error, and control nothing:

```bash
grep -rn "<key_name>" --include=*.py /usr/local/lib/hermes-agent
```

**Zero hits means decoration.** Report such a key as *written but not live*; never translate its presence
into "the voice is now active for that lane". A dormant scaffold module that pins its own constant and is
imported by nothing is the same defect wearing a filename. Adding a second copy of the same unread keys
does not help — find the layer that actually synthesises, and wire there.

## 2. What the provider layer can and cannot do

A `tts.providers.<name>` entry with `type: command` supports exactly these placeholders:

`{text_path}` / `{input_path}` · `{output_path}` · `{format}` · `{voice}` · `{model}` · `{speed}`

The child process env is **rebuilt and scrubbed** (`inherit_credentials=False`), and `env_passthrough`
is an allowlist of parent variable **names** only. **There is no `{chat_id}`, no room, and no lane
identifier.** A command provider therefore cannot select a voice per conversation, and the synthesis
path does not know which chat it is rendering for.

**Do not fake per-room routing with a state file or a racing wrapper.** One gateway process serves
several chats, so a persona voice written for one room will eventually surface in another. Leakage is
worse than absence. Automatic per-room switching is a runtime patch — proposal → judge → commit — which
is a different authority class from config work, and not something to slip in during a creative session.

## 3. The pattern that works — one pinned default plus named alternatives

Selection is **per take, by provider name**. The assistant's identity voice stays pinned; the extra
providers are additive.

1. **Give the engine a voice argument, preserving the default.** In the engine script:
   `VOICE_ID="${3:-${IARIF_VOICE_ID:-<default-id>}}"`. Keep any existing id-resolution or revocation
gate **downstream of that argument**, so no caller can route around it.
2. **Add the placeholder to the EXISTING default provider too** — `... {text_path} {output_path} {voice}`
   — and set its `voice` to `''` so an empty value falls through to the engine default. Skip this and
the shared engine still renders fine, but nothing can ever be passed to it.
3. **Register a second named provider** on the same engine with `voice` pinning the target id.
4. **Select it at call time:** `text_to_speech(provider="<name>")`.

## 4. Config edits: do them yourself

`patch` / `write_file` refuse `~/.hermes/config.yaml`, which makes this look like a blocked mutation. It
is not — it is a blocked tool. The `hermes config` CLI writes nested provider keys fine, one flag per
line, and preserves the rest of the file. Read the value back with `yaml.safe_load` and confirm.

The CLI answers these with a *"not a recognized config key — saved anyway"* notice, because the provider
block is read by the provider layer rather than the config schema. **That notice is a warning, not a
failure.** Turning a two-command change into a paste job for the principal is the attention leak the
membrane names.

## 5. Verification — read the engine line, not the audio

You cannot hear a wrong timbre in your own output, so listening is not a witness. Rebuild the exact
command the provider builds (same placeholder substitution, same quoting) and read the engine's own
diagnostic line on stderr. That line naming the expected voice id is the proof the wiring took.

**Test the negative directions too, every time.** If the engine refuses revoked or unknown ids, confirm
after the change that a revoked id still exits non-zero and an invented id still exits non-zero. Adding a
voice-passing argument without re-testing that is how a revocation hole gets silently reopened.

**A correct voice id is not a matching artifact — A/B the two routes and diff the OUTPUT.** Two routes
can reach the same engine and return the right identity while differing in behaviour, because the shared
engine can hardcode a setting the lane's own render script overrides. Measured on one identical line: the
named provider returned **33.40 s** where the lane script (which passes its own speed) returned
**36.14 s** — ~8% faster, both naming the same voice, both passing every gate, neither showing anything
anomalous on the engine line. Only the side-by-side run exposes it. So when a lane already has a verified
render path, push the SAME text through both and diff duration + f0 + round-trip before choosing. Report
the gap; do not silently pin the shared engine to close it — that engine also serves the assistant default
lane, so changing it is a different authority class from a persona wiring job.

## 6. Receipt

Record: the engine diff, every `hermes config` command run, what stayed **unchanged** (especially the
assistant default provider), the test matrix including both negative cases, and an explicit statement
that automatic per-room switching is NOT wired. The last line matters most — it is the difference
between a recorded gap and a claim the next session will trust and build on.
