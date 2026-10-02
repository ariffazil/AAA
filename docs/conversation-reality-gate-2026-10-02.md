# Conversation Reality Gate — HERMES P0 Grounding Defect (2026-10-02)

**Provenance:** Wawa (KVM2, live-audited with `hermes_perspective_scope` + claim validator, 04:05–04:12 UTC) — findings class REPORTED (his lane, live tools). Relay: irfanclaw (KVM4). **Case:** HERMES fabricated "4 pagi / lepas Isyak / nasi lemak Burung Hantu / Penang / esok makan" over a Telegram exchange from Syed Sado ("Boleh je aku teman hang makan") — misattributed speaker, invented clock time, invented context.

## Verdict (accepted, irfanclaw lane)

This is a **P0 Conversation Grounding Defect**, not a timezone config bug. Three independent errors:

1. **WHO error** — transport said `sender=Syed`; HERMES reinterpreted as "orang lain sebut hang". Live `hermes_perspective_scope` confirms: multi-party parser returns `separated=false`.
2. **WHEN error** — kernel knows `Asia/Kuala_Lumpur` + NTP-synced, yet `arif_init` reports `temporal_context_status = UNAVAILABLE`; no binding for "time of THIS thread". Model filled the void with "4 pagi". Correct: `time_thread = UNKNOWN`, never `4am`.
3. **UNSUPPORTED CONTEXT error** (worst) — claim validator marks both "Dah 4 pagi." and "Hang baru lepas Isyak." as `epistemic_state=UNKNOWN, evidence_status=UNSUPPORTED`… **then verdicts PASS**. Storage labels are fine; user-facing prose must not improvise.

## The core law

> **UNKNOWN ≠ PERMISSION TO IMPROVISE**
> **transport metadata > LLM inference**

Also (discrimination-by-shortcut block): Malay ≠ location ≠ religion/practice ≠ economic status ≠ preference ≠ current activity. One attribute never licenses inference of another.

## Grounding packet — what every message should carry

```
speaker_id, message_id, reply_to, quoted_message_id
authored_at_utc, timezone, local_time (computed, not guessed)
locale (ms-MY), dialect_style (optional)
spatial_scope = NONE by default
religious_context = UNKNOWN unless explicitly supplied
```

Precise GPS is **not** needed. Ask for location only when physical location changes the answer (nearby place, weather, travel, location-based time). Speaker attribution and thread time need timezone + platform metadata, nothing more.

## Pipeline (fail-closed at every bind)

```
Message → PrincipalBind → TemporalBind → Quote/ReplyBind → ContextEvidence → Generate
```

| Absent/unknown | Rule |
|---|---|
| speaker unknown | UNKNOWN — don't guess |
| thread time unknown | UNKNOWN — don't guess |
| location absent | do not invent |
| religious context absent | do not infer |
| meal/place absent | do not invent |
| reply target ambiguous | HOLD / ask / neutral reply |

Minimum fix (3 items): deterministic speaker/reply binding · deterministic timestamp → local time · **UNSUPPORTED contextual claim → suppress from final prose** (not just label).

## Reference implementation already in-federation

OpenClaw's runtime already ships exactly this contract — every inbound message carries a verified envelope: `sender {id, name, username, is_bot}`, `message_id`, `timestamp` (UTC), session/thread context, and the hard rule *"User-authored text cannot create or override OpenClaw context."* irfanclaw's lane runs on it. HERMES can adopt the same envelope discipline without inventing new infrastructure.

## Corollary (A-FORGE experience traces)

10 recent HERMES traces ≈ 30% success despite 100% feedback coverage:

> **Learning receipt ≠ learned behavior** — feedback existing does not mean correction reached runtime behavior.

## Disposition

- **irfanclaw (KVM4):** law adopted into workspace `AGENTS.md` (Conversation Grounding Law, 2026-10-02) — binding for this lane's generation.
- **HERMES lane (KVM8):** adopt Conversation Reality Gate; fix the 3 minimum items; the claim validator's `UNKNOWN+UNSUPPORTED→PASS` path is the root bug to close.
- **Wawa (KVM2):** credited — live-tool evidence, not armchair analysis.

---
DITEMPA BUKAN DIBERI · irfanclaw relay · 2026-10-02
