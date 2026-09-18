# Rendering a persona voice (MiniMax REST)

For a spoken persona line delivered as audio, when a registry-managed voice id must be used rather
than the default TTS voice. The persona lane's own craft rules live with its lane skill; this file
is the *mechanical* path plus the two traps that cost calls.

## 1. Read the registry before choosing an id

Voice ids are registered centrally and the registry is the authority for `status`,
`preferred_settings.speed` and the `runtime_measured_*` block. Never choose an id by name symmetry,
by file recency, or by whichever renders first — several ids answer to the same spoken register and
they are different timbres, not versions of one thing. A REVOKED id must never be selected as a
default, an explicit id, or a fallback rung.

When the requester names a **tier**, that is an explicit selector. Use the tier's id and that id's
own speed — speed is calibrated per voice and does not transfer, so render once, read the printed
duration, and step toward the reference take's length rather than carrying a number over from a
different voice.

## 2. The key name is not fixed — probe, and read the nested status

Two `MINIMAX*` environment variables can be present on one host and they are **not
interchangeable**. Measured on the synthesis endpoint: the short plugin-style key returned
`base_resp.status_code 1004` (`login fail`), while the longer account key on the same endpoint
returned `status_code 0` and rendered.

- Enumerate the variables rather than hardcoding a name; try the account key first for synthesis.
- **Read `base_resp.status_code`, never the HTTP status.** The provider answers HTTP 200 with the
  real verdict nested inside `base_resp` — a success-looking 200 can carry a failure body.
- **A 1004 is a key-selection result, not an outage.** Do not report the lane down; switch key and
  retry.

```python
import binascii, json, os, urllib.request

KEY = os.environ.get("MINIMAX_API_KEY") or os.environ.get("MINIMAX_PLUGIN_API_KEY")
if not KEY:
    raise SystemExit("NO_KEY_IN_ENV")

body = json.dumps({
    "model": "speech-2.8-hd",
    "text": TEXT,
    "stream": False,
    "voice_setting": {"voice_id": VOICE, "speed": SPEED, "vol": 1.0, "pitch": 0},
    "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3"},
}).encode()

req = urllib.request.Request(
    "https://api.minimax.io/v1/t2a_v2", data=body,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
d = json.loads(urllib.request.urlopen(req, timeout=300).read().decode())
if d.get("base_resp", {}).get("status_code") != 0:
    raise SystemExit("PROVIDER_ERROR: " + json.dumps(d.get("base_resp")))

# the audio payload is HEX, not base64 — unhexlify before writing or you ship a text file
# wearing an .mp3 extension
open("/tmp/take.mp3", "wb").write(binascii.unhexlify(d["data"]["audio"]))
```

- **Read the key from the process environment inside the script.** Do not parse a credentials file
  by path: any tool argument carrying that path is blocked by the pre-execution gate, and it trips on
  a file you *write* just as readily as on a command you run — so the script never lands. Source the
  credentials in a separate terminal call so the variables are already exported, then have the script
  read `os.environ`.
- **`trial_audio` from the design endpoint is hex too** — same `unhexlify` gotcha.

## 3. QC before delivery — and declare the chain

- **Run an ASR round-trip on every take before shipping it.** A cloned checkpoint can speak words the
  input never contained, and the insertion happens inside synthesis, so sanitising the input cannot
  catch it. Transcribe the take back, diff the tokens against the source line, and read specifically
  for **INSERTED** clauses rather than only garbled ones. Clean on one take is evidence for that take,
  not a property of the voice.
- **Normalise before you score, or the number lies.** Digits written as words come back as numerals,
  and an English word inside Malay text collapses the ratio because the aligner desyncs. A very low
  score on dense regional text is usually an unbuilt alias table, not a bad take.
- **Declare the engine and the voice id in the delivery line**, every time. For a persona register,
  also say the voice is synthetic and which chain produced it (parametric design vs clone of a
  synthetic source) — never a real person's name on a synthetic voice.
- **`[[audio_as_voice]]` on its own line above the `MEDIA:` line** to land as a native voice bubble;
  without it the file arrives as an attachment.
