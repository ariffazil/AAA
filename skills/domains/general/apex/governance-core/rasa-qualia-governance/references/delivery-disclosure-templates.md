# Delivery disclosure templates

Four blocks. Write them in the principal's register, keep them under four lines, put them **before**
any praise or description of the artifact. Not footnotes.

## 1. Fiction label (image / video)

```
AI-generated. Bukan orang sebenar — semua yang dalam frame ni ciptaan model.
Aku yang susun scene ni, bukan dia orang.
```

English shape:

```
Machine-generated — the men in this are invented, not photographs of anyone.
```

If the principal is in frame:

```
Muka tak nampak sebab tak ada reference — silhouette dari belakang tu je yang mewakili kau.
Aku tak bagi model reka muka dan kata itu kau.
```

## 2. Voice provenance (mandatory, four fields)

```
Suara: <engine + model> · voice <voice_id> · SPEED <n> ·
SYNTHETIC (bukan clone sesiapa yang hidup) · transcript disahkan STT round-trip (<lang>).
```

Real example of the shape (verified live, MiniMax speech-2.8-hd):

```
Suara: MiniMax speech-2.8-hd · voice Indonesian_BossyLeader · speed 0.85 ·
SYNTHETIC — bukan clone sesiapa yang hidup · transcript disahkan Whisper round-trip (ms).
```

If it is a clone:

```
Suara: <engine+model> · voice_id <id> · CLONE — sumber <whose voice, with what consent basis>.
```

If the round-trip was not run, say so:

```
Transcript: aku tak round-trip take ni. Kalau ada perkataan pelik, itu sebab tu.
```

## 3. Engine honesty (when the route changed)

```
Nota: kau minta <requested lane>, tapi kunci ni tak support. Ini <actual engine/route>.
Kalau nak <requested lane>, kena <the real key-class change>. Aku boleh re-render bila ada.
```

Applies to: engine fallback, video-model fallback, an upscale standing in for a native render,
voice substitution, failed first take replaced by a different engine. Never let a swap pass silently.

## 4. STT-derived transcript

```
Transcript ni aku dapat dari mesin dengar (STT), bukan transkrip rasmi.
Nama, nombor dan perkataan campur English boleh tersalah.
```

Never quote an STT transcript as if it were what a person said.

## Combined block (default for a backstage / persona delivery)

```
AI-generated · orang dalam frame ni ciptaan model, bukan orang sebenar.
Suara sintetik: <engine> <voice_id> — bukan clone sesiapa yang hidup.
Transcript disahkan STT round-trip.
Fiksyen — nama, tempat dan watak semua rekaan.
```

## Placement rule

Order in the reply: artifact identity line → disclosure block → one line of craft framing (what is
carrying the composition) → the artifact. Never: artifact → praise → disclosure.
