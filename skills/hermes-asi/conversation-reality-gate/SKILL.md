---
name: conversation-reality-gate
description: "P0 Conversation Grounding Defect fix — fail-closed speaker/time/context binding. Use when HERMES state.context lacks speaker_id, thread time, or reply target, or when LLM prose improvises time/place/religious context from a message that did not contain it."
version: 0.1.0
risk_tier: low
floor_scope: [F1, F2, F4, F6, F7, F9, F11, F12]
autonomy_tier: T2
owner: HERMES ASI runtime
forged: 2026-10-02
scar: P0-Conversation-Grounding-Defect (Arif 2026-10-02)
---

# Conversation Reality Gate — P0

## Why this skill exists

Arif diagnosed three correlated errors on 2026-10-02 that the previous
HERMES structural validator allowed through:

1. **WHO error** — message from Syed Sado read as "someone else talking about hang"
2. **WHEN error** — temporal context unavailable but model filled space with "4 pagi"
3. **UNSUPPORTED CONTEXT error** — claim validator returned `verdict=PASS` even when
   `epistemic_state=UNKNOWN` and `evidence_status=UNSUPPORTED`

The structural validator labelled `UNKNOWN` correctly but the human-facing prose
still contained the invention. Bug at module level, not config.

arifOS kernel itself confirms the gap — `arif_init(mode='light')` returns zero
`temporal_*` fields. The kernel knows the wall-clock time of MCP transport,
but exposes no envelope for "time of the message the user is currently asking
about". Same gap exists for `speaker_id`, `reply_to`, `quoted_message_id`.

## The law (Arif 2026-10-02)

```
Transport metadata  >  LLM inference
Timestamp + timezone → local time    (computed, not inferred)
UNKNOWN             ≠  PERMISSION TO IMPROVISE
```

## What this skill does

Pre-generation **fail-closed gate** that runs BEFORE any reply is constructed.
Produces a `GroundingPacket` the response layer must consume.

The packet carries:

- **SpeakerBinding** — `speaker_id`, `speaker_type`, `confidence=TRANSPORT|INFERRED|NONE`
- **TemporalBinding** — `authored_at_utc`, `timezone`, `local_time`, `method=COMPUTED|UNKNOWN`
- **QuoteReplyBinding** — `reply_to`, `quoted_message_id`, `quoted_author_id`
- **ContextEvidence** — `locale`, `dialect_style`, `spatial_scope=NONE`, `religious_context=UNKNOWN`,
  `meal_context=UNKNOWN`, `place_context=UNKNOWN`

Hard-fail rules:

| Field           | If UNKNOWN    | Surface rule                              |
|-----------------|---------------|-------------------------------------------|
| speaker_id      | UNKNOWN       | Address the channel, not a specific name  |
| thread_time     | UNKNOWN       | Don't say "pagi/malam/4am"; say "tidak pasti" |
| spatial_scope   | NONE          | Don't infer city/state/location           |
| religious_ctx    | UNKNOWN       | Don't infer solat/puasa/waktu sembahyang |
| meal/place_ctx  | UNKNOWN       | Don't pick a meal or venue               |

Forbidden improvisation list (regex, fail-closed):

`pukul N`, `N am/pm`, `pagi|petang|malam|tengah hari`,
`subuh|maghrib|isyak|zohor|asar`,
`lepas (isyak|...)`, `solat|puasa`,
`nasi lemak|restoran|cafe|makan (kat|di)`,
`Burung Hantu`, `esok|kelmarin|semalam`,
`Jumaat|Isnin|Selasa|Rabu|Khamis|Sabtu|Ahad`,
`kat/di [Place]`.

## Usage

```python
from conversation_reality_gate import (
    bind_from_telegram, override_tz, suppress_unsupported_context,
)

pkt = bind_from_telegram(telegram_payload)   # mandatory transport metadata
pkt = override_tz(pkt, "Asia/Kuala_Lumpur")   # if known; else leave UNKNOWN

# In the generation step:
verdict = suppress_unsupported_context(claim_text, evidence_status, packet=pkt)
if not verdict["allowed_in_prose"]:
    # suppress the claim, OR rewrite to: "Aku tak pasti [thing]"
    ...
```

## Acceptance — runnable

```bash
/usr/bin/python3 /root/AAA/skills/hermes-asi/runtime/conversation_reality_gate.py --gate-test
/usr/bin/python3 /root/AAA/skills/hermes-asi/runtime/conversation_reality_gate.py --demo-binding
```

Expected output of `--gate-test`: `6/6 PASS` covering:

- scenario_A_4am_isyak — "Dah 4 pagi. Hang baru lepas Isyak." → SUPPRESS
- scenario_B_nasilemak_penang — meal/place/time combo → SUPPRESS
- scenario_C_supported_passes — supported claim passes through
- scenario_D_speaker_transport — speaker_id from transport, not re-interpreted
- scenario_E_tz_override — tz bound → local_time computed deterministically
- scenario_F_no_tz — no tz → local_time stays UNKNOWN

Evidence file: `/root/.hermes/cache/scratch/P0_CONVERSATION_REALITY_GATE_TEST.json`

## Runtime location

`/root/AAA/skills/hermes-asi/runtime/conversation_reality_gate.py`

Deterministic library — no LLM call, no remote probe. Only host facts the
channel surfaces plus per-thread bindings.

## Anti-pattern (the bug we are NOT going to repeat)

```
UNKNOWN  →  LLM prose  →  human sees "4 pagi / Isyak / nasi lemak"
```

Replaced by:

```
Transport metadata  →  GroundingPacket  →  generation constrained by packet
```

The packet enforces that `UNKNOWN` reaches the human as `tidak pasti`, not
filled with a hallucinated time / place / religious practice.

## Follow-up

This gate covers the symptom. The upstream root cause is that arifOS kernel
needs to expose `thread_time_binding` as a first-class envelope field.
Tracking: SOVEREIGN_HOLD on arifOS kernel contract.