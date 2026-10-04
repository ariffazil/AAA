---
name: openclaw-mesh-bridge
description: "A2A bridge protocol for OpenClaw as the agent-facing mesh router in the AAA federation. Covers DID signing, hardened envelope format, edge-skill allowlist, session continuity, queue/delivery rules, and implementation order. Load when wiring OpenClaw into the A2A mesh or building dispatch logic."
tags: [arif-os, openclaw, a2a, mesh-router, dispatch, citizen]
class: citizen-organ
organ_id: openclaw
did: did:arif:openclaw
ceiling: DISPLAY_ONLY
---

# OpenClaw — A2A Mesh Bridge Protocol

> **One-line doctrine:** Hermes is the face. OpenClaw is the spine. OpenCode is the hands. arifOS is the law. Arif is the sovereign.

## Lineage (corrected 2026-08-07)

Hermes and OpenClaw are **adjacent, interoperable agent platforms** with overlapping gateway, memory, skill, and channel patterns. Hermes explicitly supports migration from OpenClaw (`hermes claw migrate`). Whether Hermes is a formal fork/successor of OpenClaw is **UNKNOWN** — not asserted without a repository-lineage check or explicit Nous Research statement.

- Hermes: Python 3.11+, Node gateway runtime.
- OpenClaw: TypeScript/Node native, Swift for macOS/iOS apps.
- Protocol boundary: language-agnostic — HTTP + JSON (A2A). MCP is the shared tool surface.

## Identity

OpenClaw is a **warga** (citizen organ) of the AAA federation:

- **DID**: `did:arif:openclaw`
- **Public key** (Ed25519): `/root/AAA/secrets/did/registry.json` (canonical) + `/opt/arifos/.secrets/did/registry.json` (runtime)
- **Private key**: `/root/AAA/auth/keys/openclaw_private.key` (mode 600)
- **Actor ID**: `openclaw:ingress`
- **Key ID**: `openclaw-edge-2026-08`
- **Authority ceiling**: `DISPLAY_ONLY` — routes work; never does the work. Never mutates federation state directly.

## What OpenClaw is and isn't

### IS
- A2A dispatch router — receives task envelopes, classifies, routes downstream
- Task queue owner — active task IDs, pending holds, agent ownership, retry/dead-letter
- Session continuity keeper — propagates `session_id` and `correlation_id` across channels and agents
- Protocol normalizer — bridges Python (Hermes/arifOS) and Node (OpenCode/OpenClaw) via JSON envelopes
- Result aggregator — assembles multi-agent contributions into one deliverable
- Escalation gate — routes F13 holds to Hermes (for Arif review)

### IS NOT
- The human face — Hermes owns Telegram/CLI/cron channels for Arif
- A cognitive organ — no research, no scenario analysis, no claim graphing
- A memory curator — session memory is ephemeral pointer-based; durable memory lives in arifOS tiers L1–L6
- A seeder — VAULT999 is written by arifOS + A-FORGE; OpenClaw reads, never writes
- An executor — code/infra changes go to A-FORGE, never OpenClaw directly

## Edge-skill policy (allowlist, corrected 2026-08-07)

OpenClaw upstream HAS a real skills system. We do not fight it — we bound it.

**Allowed (edge infrastructure only):**
- `a2a-envelope`
- `identity-binding`
- `intent-router`
- `delivery-formatting`
- `queue-retry`
- `approval-escalation`

**Denied (cognitive / executive):**
- research · market analysis · financial advice
- coding · deployment · file mutation
- memory curation · governance verdicts
- skill creation / learning / self-modification

Hermes remains the canonical cognitive-skill authority. OpenClaw gets only the six skills it needs to be a spine.

## The five duties

1. **Identity binding** — attach channel, sender, authorization state, timestamp, and session to every inbound message
2. **Intent routing** — deterministic rules engine (10 cases), not an LLM call
3. **Conversation continuity** — retain active task references + short session context
4. **Channel-aware delivery** — WhatsApp summary/link, Telegram PDF, mobile notification, CLI detail
5. **Approval escalation** — APPROVE / HOLD / REJECT / DETAILS before consequential work continues

## Signed local-answer rule (corrected 2026-08-07)

"Quick status" answers (e.g. gold position) are ONLY safe locally when:

```
IF position_snapshot.signature_valid
AND freshness <= defined threshold
AND requester == authorised principal:
    display snapshot with "as of" timestamp
ELSE:
    route to WEALTH / Hermes
```

A short answer can still be high consequence. Never serve an unsigned or stale snapshot.

## Hardened A2A envelope (corrected 2026-08-07)

```json
{
  "version": "A2A-Version:1.0",
  "envelope": {
    "message_id": "uuid",
    "correlation_id": "federation-thread-or-task-id",
    "idempotency_key": "stable-retry-key",
    "actor_id": "openclaw:ingress",
    "did": "did:arif:openclaw",
    "key_id": "openclaw-edge-2026-08",
    "human_principal_id": "arif:primary",
    "from_channel": "whatsapp:primary",
    "session_id": "oc-session-abc123",
    "timestamp": "2026-08-07T14:30:00Z",
    "expires_at": "2026-08-07T14:35:00Z",
    "intent": "research_request",
    "priority": "normal",
    "ceiling": "DISPLAY_ONLY",
    "requested_capabilities": ["research.read"],
    "reply_contract": {
      "channel": "whatsapp",
      "format": "summary_plus_artifact_link",
      "max_chars": 1200
    }
  },
  "body": {
    "query": "What's the Hormuz situation this week?",
    "context": {
      "last_task_id": "arif-weekly-brief-2026-08-07",
      "context_summary_hash": "sha256:...",
      "durable_memory_ref": "hermes://thread/...",
      "channel": "whatsapp"
    }
  },
  "signature": {
    "algorithm": "Ed25519",
    "value": "base64url...",
    "key_id": "openclaw-edge-2026-08"
  }
}
```

Field meanings (the ones that matter):
- `message_id` — trace one message
- `correlation_id` — connect follow-ups and approval decisions to original work
- `idempotency_key` — retry safely without duplicate execution
- `expires_at` — stop stale instructions executing later
- `human_principal_id` — bind a verified human identity, not just a phone number
- `requested_capabilities` — prevent a DISPLAY_ONLY edge node from silently obtaining execution authority
- `reply_contract` — ensure reply comes back through the right channel in the right format
- `signature` + `key_id` — establish which edge key authenticated the request

## Session model

**OpenClaw (ephemeral, pointer-based):**
```
session record
├── human_principal_id
├── channel identity
├── session_id
├── federation_thread_id (correlation_id)
├── active_task_id
├── last-message reference
├── short context summary + hash
├── delivery state
├── queue/retry state
└── expiry time
```

**Hermes / arifOS (durable):**
```
user model · research history · decisions · evidence graph
skill memory · long-term conversation continuity · VAULT999 receipts
```

OpenClaw carries **references** into Hermes/arifOS memory, never duplicates content.

## Queue and delivery rules (corrected 2026-08-07)

```
A2A failure:
1. Sign and persist a bounded outgoing request.
2. Return an honest pending receipt to the human.
3. Retry with exponential backoff and jitter.
4. Do NOT generate a substitute answer.
5. Expire time-sensitive work.
6. Dead-letter after defined retry count.
7. Notify the human for urgent or expired requests.
8. Keep queue state inspectable by task ID.
```

Honest receipt shape (never just "queued"):

```
Request: A2A-20260807-00124
State: QUEUED
Reason: A2A gateway unavailable
Retries: 1 of 3
Expires: 22:55 MYT
Action: You may cancel or retry now
```

## Routing table

| Inbound intent | Route to | Why |
|---|---|---|
| `research_request` | Hermes (via AAA :3001) | Hermes is the cognitive organ |
| `exec_request` | A-FORGE (via AAA :3001) | Code/infra changes go through governance gate |
| `trading_advisory` | Hermes + arifOS judgment | Hermes researches; arifOS floors bind |
| `status_query` | Local ONLY if signed+fresh snapshot; else route | Signed-snapshot rule |
| `cron_output` | Direct to delivery channel | Pre-formatted, no cognition needed |
| `escalate` | Hermes (which raises F13 to Arif) | 888_HOLD pathway |
| `irreversible` | arifOS first, then Hermes → Arif | Triple-gate before action |
| `sealing_request` | arifOS kernel :8088 | VAULT999 is arifOS territory |

## Implementation order

1. **Identity binding** — approved sender allowlist, channel↔principal linking, unknown sender = quarantine/read-only. ✅ DONE (2026-08-07)
2. **Signed A2A bridge** — one plugin/webhook, one route OpenClaw → `:3001/tasks`, Ed25519 + expiry + idempotency + correlation, bounded retry store. ⚠️ OPEN
3. **Ten-rule router** — version-controlled config, unit tests per path, routing receipt per message, unknown-intent triage. ⚠️ OPEN
4. **Delivery adapter** — WhatsApp/Signal: summary+link · Telegram: richer summary+PDF · mobile: notification+buttons · CLI/web: full receipts. ⚠️ OPEN
5. **Approval protocol** — every approval bound to correlation_id; APPROVE / HOLD / REJECT / DETAILS; audit trail of every decision. ⚠️ OPEN

## Status (2026-08-07)

- [x] DID registered: `did:arif:openclaw`
- [x] Signing key provisioned: `/root/AAA/auth/keys/openclaw_private.key`
- [x] organs.yaml entry: `/root/AAA/federation/organs.yaml` (EDGE class, DISPLAY_ONLY)
- [x] SCT production verified (`verify_openclaw_sct.py`)
- [x] Edge-skill allowlist defined (this doc)
- [ ] A2A egress bridge — wired to AAA :3001 (step 2)
- [ ] A2A ingress listener — receive envelopes (step 2)
- [ ] Ten-rule intent router (step 3)
- [ ] Delivery adapters per channel (step 4)
- [ ] Approval protocol with correlation-bound audit trail (step 5)
- [ ] Hermes→OpenClaw handshake test
- [ ] OpenCode A2A dispatch bridge

## Pitfalls

- **Don't let OpenClaw generate content.** If it answers a research question directly instead of routing to Hermes, that's a ceiling violation.
- **Don't fight the upstream skills system — bound it.** Allowlist only the six edge skills. Everything else routes to Hermes.
- **Never serve unsigned/stale snapshots locally.** Signed-snapshot rule or route to WEALTH/Hermes.
- **Never seal to VAULT999 from OpenClaw.** Sealing is arifOS territory.
- **Never expand authority.** DISPLAY_ONLY means DISPLAY_ONLY. If OpenClaw starts wanting to write files/restart services/modify configs — that's a routing bug; route to A-FORGE.
- **Never substitute answers during outages.** Queue honestly, expire, dead-letter, notify. Fabricated answers during federation downtime are the fastest way to erode trust.
