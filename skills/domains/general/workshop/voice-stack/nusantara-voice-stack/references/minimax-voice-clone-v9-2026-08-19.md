# MiniMax Voice Clone — V9 Session Lessons (2026-08-19)

## 1. Clone API: 10s hard minimum, padded sources work

MiniMax `voice_clone` requires ≥10s audio. A 9.65s source (just under) fails with:
- MCP tool: clear error `"voice duration too short"` (error 2037)
- REST API `/v1/voice_clone`: vague `"invalid params"` (error 2013) — less diagnostic

**Workaround:** Pad the source to 11s: `ffmpeg -i source.mp3 -af "apad=pad_dur=1.5" -ar 32000 -ac 1 padded.mp3`. The clone succeeds, the voice identity is preserved.

## 2. MCP vs REST: MCP is more informative

For voice clone debugging, always prefer the MCP path (port 18100) over direct REST:
- MCP returns specific error codes (2037 = duration, 2013 = invalid params)
- REST returns generic 2013 for multiple different failure modes

MCP client template (from `forge-minimax-mcp-direct-invoke`):
```python
# voice_clone MCP schema: voice_id, file (PATH not file_id), text, output_directory
result = await session.call_tool("voice_clone", {
    "voice_id": "iarif-sovereign-v9",
    "file": "/path/to/source_padded.mp3",
    "text": "Test sentence",
    "output_directory": "/tmp/out"
})
```

**Key difference from REST:** MCP `voice_clone` takes a file path, not a file_id. REST requires uploading first then referencing file_id.

## 3. voice_design F0 ceiling: ~205 Hz max in practice

Three batch-minted variants of a "bright soprano, 239 Hz" description:
- v6a: 162.7 Hz median
- v6b: 205.7 Hz median (closest to band)
- v6c: 175.4 Hz median

Best achieved was 205 Hz — well below the 239 Hz target. Design is for timbre/character, NOT pitch control. If F0 lock is needed, add a WORLD vocoder DSP wrapper as a second stage.

## 4. Clone preserves timbre, shifts F0

Source synthetic voice F0: 210.0 Hz median → Clone raw F0: 191.0 Hz median (19 Hz drop, same general register). Clone demo: 195.7 Hz. Clone preserves the voice character well (STT round-trip perfect), but F0 shifts slightly toward MiniMax's own average. Factor this in when targeting specific pitch bands.

## 5. Existing voice_ids: silent overwrite on same account

If a voice_id already exists on the account, `voice_clone` returns 2039 "duplicate" — it does NOT overwrite. You must choose a new name (`iarif-sovereign-v9` instead of `v8`). Old IDs persist and can still be used for synthesis.

## 6. Consent architecture for sovereign voice work

Arif's voice pipeline went through 7 iterations:
- V4: re-pointed to female register (unverified provenance, retired)
- V5: voice_design at wrong band (170 Hz, retired — Declare-vs-Reality gap)
- V6a/b/c: voice_design at wrong band (max 206 Hz, retired)
- V7: clone from Arif's natural voice note (10.17s WAV, F0 170→240 Hz locked)
- V8: contaminated from prior session (266 Hz, wrong voice, retired)
- V9: clone from Arif's own synthetic voice (9.65s padded to 11s, F0 191 Hz raw)

**Final consent model:** Arif gave explicit instruction "Use this as sample" + sent the audio file = sovereign self-clone (F13 authority). This resolved the design-vs-clone question permanently for i-ARIF.
