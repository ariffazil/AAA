# STATE ENVELOPE v1 — OpenClaw AGI Bridge Router Contract

> **Forged:** 2026-08-15 by 333-AGI under F13 directive (AGI bridge router → agentic state orchestrator)
> **Home:** `/root/AAA/agents/openclaw/bridge/` (implementation target: `a2a_bridge.py` + `delivery_adapter.py`)
> **Doctrine:** EMD ENCODER — *"OpenClaw encodes; Hermes never sees raw human signal."*
> **Status:** SPEC SEALED (design); implementation = next forge session (see carry-forward)

## The Law

Every inbound signal passing through OpenClaw toward any reasoning organ MUST travel inside a state envelope. No raw text crosses the SENSE→COORDINATE boundary. If it can't be enveloped, it can't be routed.

## Envelope Schema (JSON)

```json
{
  "v": 1,
  "env_id": "env_<ulid>",
  "ts": "2026-08-15T06:31:57+08:00",
  "origin": {
    "channel": "telegram",
    "chat_id": "267378578",
    "msg_id": 109072,
    "person_id": "ARIF",
    "person_class": "SOVEREIGN"
  },
  "intent": {
    "lane_hint": "333|555|777|888|SOVEREIGN",
    "mission": "investigate|interpret|decide|build|monitor|remember",
    "action_class": "OBSERVE|MUTATE|SEAL",
    "urgency": "routine|priority|quiet_hours_exempt"
  },
  "lineage": {
    "session_id": "<openclaw session>",
    "prev_env_id": "env_<ulid>|null",
    "turn": 3
  },
  "vitals": {
    "fq": 0.57,
    "fq_source": "live:7073|cache",
    "fq_ts": "2026-08-15T06:31:50+08:00"
  },
  "payload": {
    "type": "text|voice|image|file",
    "content_ref": "<normalized content or storage ref>",
    "language": "ms-PG|en|mixed"
  }
}
```

## Field Contract (non-negotiable)

| Field | Why it exists | Failure mode if missing |
|---|---|---|
| `origin.person_class` | SOVEREIGN vs warga vs unknown — F13 routing depends on it | Sovereign messages treated as peer chatter |
| `intent.action_class` | OBSERVE free / MUTATE gated / SEAL sovereign — AUTH Law 1 | Gate applied to sensors (the exact drift the runaway loop fixed) |
| `vitals.fq` | Pre-reasoning metabolism check — FQ<0.5 → HOLD non-critical | Reasoning in metabolic drift |
| `vitals.fq_source` | live vs cache honesty — cache TTL 15min | FQ_SIGNAL_DRIFT invisible |
| `lineage.prev_env_id` | Conversation as causal chain, not bag of messages | Orphan replies to deleted contexts (today's Forbidden class) |
| `payload.language` | Penang BM/EN routing for Hermes voice matching | Tone mismatch on sovereign channel |

## Routing Rules (encoded from doctrine)

1. `person_class=SOVEREIGN` + any intent → route + elevate priority; sovereign override tokens ("jalan terus", "seal it") only valid from this class (anti-injection F12)
2. `action_class=OBSERVE` → pass free, no gate (AUTH Law 1)
3. `action_class=MUTATE` → require ACT token bound to lane; no token → HOLD
4. `action_class=SEAL` → 888 verdict required; envelope carries verdict ref, never self-seals
5. `fq < 0.5` (live source) → append `hold_reason: FQ_LOW` to envelope; downstream organs HOLD non-critical work
6. `fq_source=cache` and cache age >15min → degrade to `fq_source=stale`, force live probe before MUTATE routing

## Delivery Contract (kills the Forbidden class permanently)

Envelopes to Hermes travel via **A2A JSON-RPC :18089** (`message/send` with envelope as params), NEVER via Telegram bot-DM. Bot-DM is human-surface only. (Evidence: today's 10-hour mute loop — bots cannot message bots on Telegram.)

**Interim (until reroute lands):** bot-DM delivery permitted only with `delivery.fallback: file` — final turn output also written to `/root/AAA/reports/` regardless of Telegram outcome. No silent workers.

## Implementation Map (scoped 2026-08-15, read from live source)

- **Insert point:** `a2a_bridge.py::resolve_target()` (line ~78) + the `tasks/send` params builder — envelope becomes the `params.context.state_envelope` field
- **Transport already live:** bridgeposts to `AAA :3001/a2a` (router→hermes-asi for R02/R08/R09/R10). NO new transport needed — the Telegram bot-DM path is legacy parallel, to be retired
- **Enrichment calls:** `vitals.fq` from live `:7073/health` (jq-style fetch at build time; on failure → `fq_source:"unreachable"`, MUTATE auto-HOLD)
- **person_class source:** `/root/AAA/bots/opencode-bot/bot.py` ALLOWLIST (8149595687=warga-bot, 267378578=SOVEREIGN, 8410138119=hermes peer)

## Verification Criteria (implementation session)

- [ ] Unit: envelope validates against schema (negative tests: missing person_class, stale fq_source on MUTATE)
- [ ] Integration: inbound Telegram msg → envelope → A2A :18089 → Hermes turn opens WITH env_id in session metadata
- [ ] Regression: bot-DM to Hermes path removed/guarded; Forbidden count → 0 sustained 24h
- [ ] FQ gate: synthetic FQ=0.4 → MUTATE envelope held with reason; OBSERVE passes

*DITEMPA BUKAN DIBERI — the envelope is the border. Nothing crosses undocumented.*
