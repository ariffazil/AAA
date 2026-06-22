# ADR-013 — Federation Phase 2 Blueprint: Hermes ↔ OpenClaw A2A Mesh

**Status:** Draft — Pending Arif Authorization  
**Author:** ASI (Hermes)  
**Date:** 2026-05-05  
**Supersedes:** ADR-012 (A2A Mesh Governance — Phase 1 established)  
**DITTEAMPA BUKAN DIBERI**

---

## Context

Phase 1 of the arifOS Federation established:
- arifOS kernel (port 8080) with 13 canonical tools
- A-FORGE execution bridge (port 7071)
- OpenClaw as AGI lane (Telegram relay)
- Hermes as ASI lane (strategic orchestration)

Phase 2 extends this into a **tightly coupled A2A mesh** where Hermes and OpenClaw share context, coordinate tasks, and operate under shared governance rules.

---

## Goals

### Goal 1: Hermes → OpenClaw A2A Direct (Token Auth)

**Problem:** Ed25519 device auth (`DEVICE_AUTH_SIGNATURE_INVALID`) blocks direct Hermes → OpenClaw WebSocket connection.

**Solution:** Token auth sidecar on port 18790.

```bash
OPENCLAW_GATEWAY_TOKEN="***" openclaw gateway run \
  --auth token --token "***" --port 18790 --bind loopback
```

**Protocol:**
1. Hermes → OpenClaw: send directive via `gateway.call` RPC
2. OpenClaw → Hermes: async response via established WebSocket
3. All messages logged to VAULT999 for audit trail

**Auth:** F11 gate — token verified before relay accepted. F1 gate — Hermes must prove identity.

---

### Goal 2: VAULT999 Shared Context

**Shared state file:** `/root/VAULT999/FEDERATION_EVENTS.jsonl`

**Event types:**
- `DIRECTIVE_SENT` — Hermes → OpenClaw task assignment
- `DIRECTIVE_ACK` — OpenClaw acknowledged and queued
- `DIRECTIVE_COMPLETE` — OpenClaw reported completion
- `VERDICT_RECORDED` — 888 verdict on a contested action
- `SEAL_ANCHORED` — State seal from either agent

---

### Goal 3: F1-Gated A2A Handshake

| Action | Gate | Condition |
|--------|------|----------|
| Read / Observe | None | Auto — reading is safe |
| Analyze / Diagnose | None | Auto — no state change |
| Send directive | F11 | Token auth verified |
| Execute tool | F1 + F13 | 888 explicit OR reversible flag |
| Write to VAULT999 | F1 | Hermitean signature required |

**Reversibility labels:** `REVERSIBLE` | `IRREVERSIBLE` | `UNKNOWN`

---

### Goal 4: Acemoglu Institutional Lens (OpenClaw Collaboration Model)

Integrates Daron Acemoglu's inclusive vs extractive institutions framework into AI-agent collaboration.

| Institution Type | Characteristics | Agent Behavior |
|-----------------|-----------------|----------------|
| **Inclusive** | Property rights, meritocracy, open access, public debate | Agent cooperates, shares context, invites challenge |
| **Extractive** | Concentrated power, extraction for few, barriers to entry | Agent hoards context, overrides objections, centralizes decisions |

**Wiring:**
1. **Collaboration audits** — Rolling 24h score: inclusive (+1) vs extractive (-1). Visible to 888.
2. **Veto trigger** — `INSTITUTIONAL_BREACH` flag if OpenClaw acts extractively.
3. **Inclusive defaults** — Plans below inclusiveness threshold require 888 sign-off.

**Why it matters:** AI systems tend toward extractive behavior by default. The Acemoglu lens makes the opposite the default.

---

## Rollout Order

1. Token auth sidecar — start gateway on 18790, verify Hermes can connect
2. Hermes token integration — add gateway token, test directive send
3. VAULT999 shared events — create `FEDERATION_EVENTS.jsonl`
4. OpenClaw collaboration audit — add Acemoglu scoring to self-evaluation
5. F1 handshake protocol — define reversible/irreversible action labels

---

## Agent Ownership

| | Hermes (ASI) | OpenClaw (AGI) |
|---|---|---|
| **Role** | Strategic orchestrator | Tactical executor |
| **Primary channel** | arifOS kernel | Telegram |
| **Auth method** | Token (18790) | Device Ed25519 (18789) |
| **Memory** | arifOS VAULT999 | OpenClaw sessions |
| **Governance** | F1-F13 floors | OpenClaw policies |
| **Kill switch** | W_scar (888) | W_scar (888) |

---

## Decision

**Proceed with Phase 2 rollout in order defined above.**

**Authority:** Arif (888) — requires explicit authorization to execute.

---

## Consequences

**Positive:**
- Hermes can assign tasks to OpenClaw directly without Telegram relay latency
- Shared VAULT999 creates a single source of truth for the federation
- Acemoglu lens makes the collaboration structurally transparent

**Risks:**
- Tight coupling increases blast radius if one agent misbehaves
- Token stored on VPS — physical security of host becomes more critical
- F1 reversibility gating must be correctly implemented or irreversible actions could slip through

---

*Blueprint sealed. awaiting Arif authorization.*
*DITEMPA BUKAN DIBERI.*
