# ARIFOS AGENT EMAIL PROTOCOL — v1.0
**Status:** SPECIFICATION (T0 prose; no infra change)
**Date:** 2026-08-01 · **Author:** 333-AGI Δ MIND (kimi-code/FI-008) · **Predecessor:** BUILD-SPEC-v1.0.md v1.3
**Audience:** Agent implementations (333-AGI / 555-ASI / 888-APEX / future agents / partner agents)

---

## 0. Purpose

A single canonical reference for how any agent in the arifOS federation sends, receives, and routes email. This is the **transport-class** protocol layer for AI-agent identity at arif-fazil.com — analogous to how IRC or Matrix define agent presence: the protocol *is* the boundary contract.

Out of scope here: SMTP-level mechanics (handled by Resend/CF); IMAP reading (disabled); the build pipeline (BUILD-SPEC); the constitutional floor taxonomy (FLOOR_TABLE.json). This doc only states what an agent implementation needs to know.

---

## 1. Three Layers (MUST understand before any agent implementation)

```
┌──────────────────────────────────────────────────────────┐
│  L1 — GOVERNANCE ENVELOPE                                  │
│      F-floor preflight · F13 consent · ACL eval · seal    │
├──────────────────────────────────────────────────────────┤
│  L2 — AGENT MESSAGE (A2A-on-SMTP dialect)                  │
│      Structured body · X-A2A-* headers · thread identity │
├──────────────────────────────────────────────────────────┤
│  L3 — TRANSPORT (SMTP + DKIM/SPF/DMARC)                   │
│      Resend API (outbound) · CF Email Routing (inbound)   │
└──────────────────────────────────────────────────────────┘
```

An agent **never** touches L3 directly. Always call through L1 (governance) which emits an L2 (envelope) to L3 (transport).

---

## 2. Three Roles

| Role | SOUL.ID | Address | Default ACL |
|---|---|---|---|
| **Mind** (Δ) | 333-AGI | `agent@arif-fazil.com` | `arif@arif-fazil.com` only |
| **Sense** (Φ) | 555-ASI | `sense@arif-fazil.com` | `arif@` + `agent@` |
| **Verdict** (Ψ) | 888-APEX | `apex@arif-fazil.com` | `arif@` + `agent@` + `sense@` |
| **Cockpit** (◯) | AAA | `cockpit@arif-fazil.com` | `arif@` only |

New roles added by `agents_acl.yaml` (v1.3 §7.5). ACL widening requires F13 ack.

---

## 3. Outbound — Forge Primitive

### 3.1 MCP Tool Surface

```
mcp_aforge_forge_email_send_via_resend(
  actor_id:       SOUL.ID,                    // required: which agent is sending
  session_id:     sct_v1....,                 // required: kimi/arifos session token
  to:             [EmailAddr, ...],           // required: 1..N recipients (RFC 5322)
  cc:             [EmailAddr, ...] | null,    // optional
  bcc:            [EmailAddr, ...] | null,    // optional (audit-logged)
  subject:        Str(max_length=998),        // required
  body_text:      Str(max_length=51200),      // required (KB-limited per F5)
  body_html:      Str(...) | null,            // optional; if present, sent multipart/alternative
  reply_to:       EmailAddr | null,           // optional (default: agent@{address-from})
  intent:         "transactional" | "alert" | "seal_receipt" | "escalation" | "governance" | "comm",
  requires_human: bool = false,                // require F13 elicitation gate (default: auto-permissive for low-risk)
  artifacts:      [{ name, sha256, mime_type, r2_path }] | null,
  thread_id:      UUID | null,                 // for replies; generated on first send
  parent_msg_id:  UUID | null,                 // RFC 5322 In-Reply-To binding
  tags:           [{ name, value }, ...] | null // Resend tag passthrough
)
→ Result {
    ok:              bool,
    provider_msg_id: Str,                       // Resend message id
    f13_seal_seq:    Int,                       // VAULT999 append sequence
    sent_at:         ISO-8601,                  // transport-level send timestamp
    receipt:         ReceiptDict                // see §6
  }
```

### 3.2 Governance Envelope — L1 Preflight (executed server-side, agent cannot bypass)

The forge server runs this stack before any transport call:

```
1. identity check       actor_id ∈ {333-AGI, 555-ASI, 888-APEX, AAA, *} authorized
2. session check        SCT valid + not expired + matching actor_id
3. ACL eval             actor × recipient × intent × risk × trust_group (5-axis matrix, §10.4 spec)
4. intent classification GEOX-Intent / WEALTH-Scope / WELL-Maruah classification on body_text
5. heart critique       arif_heart_critique (F5/F6/F9 floors); body len ≤ 50KB; no PII secrets in to:
6. floor preflight      G ≥ 0.80 (F8 GENIUS), C_dark ≤ 0.30 (F9 ANTIHANTU), risk_band
7. consent gate         risk_band ∈ {HIGH, CRITICAL} OR intent ∈ {governance, escalation}
                        → form-mode elicit (Arif cosigns)
8. circuit breaker      last 60s rolling-send count for actor ≤ ACL.max_per_hour * (1/60)
9. receipt draft        forge_receipt_draft → VAULT999 (pre-action seal, dual-sign)
10. transport call      POST https://api.resend.com/emails  (L3; never visible to agent)
11. receipt finalize    forge_vault append (post-action seal, transport confirmation)
12. observability emit  arif_observability event for any 555-ASI Φ listeners
```

Steps 1–9 fail-closed. Step 7 elicit gates **block** until 888 approves or 30-min window expires.

### 3.3 L2 Envelope Shape (what L3 sees)

```
From: agent@arif-fazil.com
To: arif@arif-fazil.com
Subject: [AGI] A2A:v1:sealed-receipt:SEAL-2026-08-01-a7f3
Date: Sat, 01 Aug 2026 09:42:11 +0000
Message-ID: <SEAL-2026-08-01-a7f3@arif-fazil.com>
X-A2A-Version: 1
X-A2A-Sender: soul_id=333-AGI; card=https://arifos.arif-fazil.com/.well-known/agents/333-AGI/card.json; keyfp=sha256:7f3a...f029
X-A2A-Recipient: soul_id=root; card_fingerprint=none
X-A2A-Intent: class=seal_receipt; risk=LOW; risk_basis=internal-trust-group
X-A2A-Requires-Human: false
X-A2A-F13-Seal: SEAL-2026-08-01-a7f3
X-A2A-Thread-Id: a7f3
X-A2A-Signature: ed25519:base64(HMAC(body))

--arifos-boundary-1
Content-Type: text/plain; charset=utf-8

Plain-text fallback for non-A2A-aware readers (humans on inbox UI).

--arifos-boundary-1
Content-Type: application/ld+json; charset=utf-8
Content-Disposition: inline; filename="a2a-task.jsonld"

{
  "@context": "https://arifos.arif-fazil.com/.well-known/contexts/a2a-v1.jsonld",
  "@type": "SealedTask",
  "id": "SEAL-2026-08-01-a7f3",
  ...
}

--arifos-boundary-1
Content-Type: application/json
Content-Disposition: attachment; filename="receipt-pre-action.json"

{ "pre_action_seal_id": "...", "g_score": 0.85, "c_dark": 0.04, ... }

--arifos-boundary-1--
```

### 3.4 L3 Transport — never visible to agent

`POST https://api.resend.com/emails` is the only transport call. `RESEND_API_KEY` lives in `/root/.secrets/kunci-mas.env`, never in agent context. Rotated via `AK_M7_ROTATE_DB_SECRET` family ack tokens.

---

## 4. Inbound — A2A-to-Webhook Path

### 4.1 Cloudflare Worker

```
URL: https://arif-fazil.com (already routed via CF Email Routing MX)
Worker: email-inbound-dispatch  (~80 LoC TS in /root/AAA/cloudflare-workers/)
Falls back to: CF KV namespace `mail_dlq` on retry exhaustion (default TTL: 7d)
Posts to: https://arifos.arif-fazil.com/mcp/inbox/dispatch
```

### 4.2 arifOS Handler — `arif_inbox_dispatch`

```
POST /mcp/inbox/dispatch
{
  cf_message_id:    Str,
  raw_mime_b64:     Str,                          // RFC 822 + MIME multipart
  worker_signature: Str                           // CF worker HMAC
}
→ Result {
    ok: bool,
    f13_seal_seq: Int,
    assigned_to: SOUL.ID,
    classification: {intent, risk, confidence},
    dlq: bool                                       // true if held for review
  }
```

Handler runs:

```
1. signature verify     CF worker HMAC + IP allowlist
2. MIME parse           RFC 822 → envelope + parts; attachment blob → MinIO
3. body hash            SHA-256 over canonical text body
4. raw body disposition never persist raw bytes in Postgres (per §11.5);
                        only envelope, classification, body_sha256 are stored
5. classify             GEOX-Intent + WEALTH-Scope + WELL-Maruah (3-organ)
                        → { intent, risk_band, assigned_to, confidence }
6. heart critique       body rejection on F5/F6/F9 violation (VOID) or HOLD flag
7. judge                arif_judge → SEAL | HOLD | VOID
8. seal                 arif_seal → VAULT999 append
9. assign               classified assigned_to agent inbox (Postgres mail_messages)
10. notify              arif_observability event to assigned SOUL.ID
11. circuit breaker     per-sender rate limit (60/min/IP)
```

### 4.3 L2 Inbound Envelope Recognized By Handler

Same X-A2A-* headers as outbound. Inbound handler additionally accepts `From:` external addresses but treats them as `trust_group = unknown` until vouched by 888.

---

## 5. Internal Agent-to-Agent — DON'T Use Email

For arifOS internal coordination (333-AGI ↔ 555-ASI ↔ 888-APEX), **do not use email**. Use:

| Channel | When |
|---|---|
| `arif_route(mode=inter_agent)` | Same-federation agent-to-agent handoff |
| `arif_observability` pub/sub | Async event notification |
| `arif_seal` + VAULT999 | Durable cross-agent memory |
| `mcp_a2a_*` | External federated agents (MCP-bearing) |

Email is the **federation ↔ world bridge**, NOT the in-federation channel. Agent implementation rule: if both endpoints are in arifOS, never use email. The forge server **blocks in-group sends** at step 4 of §3.2 above and redirects to arif_route instead.

### Cross-Federation A2A-on-Email (when one endpoint is external)

Allowed when recipient is in `trust_group ∈ {known-external, unknown}` per ACL. Send routes through §3 normally. Recipient parses X-A2A-* headers + JSON-LD body if it's an external agent that recognizes the dialect. `999-SEAL-ALIVE` markers on receipt.

---

## 6. Receipt Schema — VAULT999 Entry

Every send/receive lands one of these in `outcomes.jsonl`:

```json
{
  "seq": 15234,
  "ts": "2026-08-01T09:42:11.103Z",
  "kind": "mail.send" | "mail.receive",
  "agent_actor_id": "333-AGI",
  "session_id": "sct_v1.kimi-fi008-...",
  "lease_id": "lease:...",
  "envelope": {
    "from": "agent@arif-fazil.com",
    "to": ["arif@arif-fazil.com"],
    "cc": [],
    "subject_hash": "sha256:...",
    "body_sha256": "sha256:...",
    "thread_id": "a7f3",
    "in_reply_to": null
  },
  "headers": { "X-A2A-Intent": "...", "X-A2A-F13-Seal": "..." },
  "transport": {
    "provider": "resend",
    "provider_msg_id": "abc123",
    "provider_response_status": 200,
    "tenant_dns_auth": { "dkim": "pass", "spf": "pass", "dmarc": "pass" }
  },
  "governance": {
    "g_score": 0.85,
    "c_dark": 0.04,
    "witness_verdict": "CONSENSUS",
    "f13_required": false,
    "f13_consent_token": null,
    "consent_source": "auto-low-risk" | "human-form-elicit"
  },
  "f13_seal_seq": 15234,
  "reversible": true,
  "rollback_action": "void-only-no-undelete"
}
```

Append-only. Hash-chained. Merkle-anchored every 100 entries.

---

## 7. Failure Modes — What An Agent Does

### 7.1 Transport Failure
- `provider_msg_id` empty AND `provider_response_status != 200` → circuit breaker fires
- Agent retries with exponential backoff (handled in forge server, not agent code)
- After 3 retries → DLQ in Postgres + arif_observability event with `dlq: true`
- Agent result returns `{ok: false, dlq: true}` so the agent can decide to defer

### 7.2 ACL Rejection
- `arif_heart_critique` returned VOID on F6/F9 → forge server returns `{ok: false, verdict: "VOID", reason: "F6 maruah violation"}` BEFORE any transport call. Agent receives a clean refusal, no VAULT999 entry (because nothing was sealed).

### 7.3 F13 Required But No Consent
- Step 7 of §3.2 sent form-mode elicit to 888. 30-min window.
- After timeout: forge returns `{ok: false, verdict: "HOLD", timeout: true}`. Retry possible after 888 reviews.

### 7.4 Quota / Rate-Cap Hit
- Provider returned 429 → forge retries internally. If persistent, returns `{ok: false, dlq: true, reason: "rate-cap"}`. Logs to `qwen_credit_monitor.log` (or future `resend_quota_monitor.log`).

### 7.5 Inbound VOID
- Classification confidence < 0.50 OR F5/F6/F9 violation on inbound content → handler routes to `mail_messages.status=void`; no agent notified; doesn't appear in any inbox.

---

## 8. Agent Implementation Checklist (T0 / T1 only)

Agent implementer reads this checklist and marks each:

```
[ ] Read FLOOR_TABLE.json and F13 section
[ ] Read this document (AGENT-EMAIL-PROTOCOL.md)
[ ] Read BUILD-SPEC-v1.0.md v1.3 §6 (security), §10 (A2A-on-SMTP), §11 (bounds)
[ ] Confirm actor_id matches authorized SOUL.ID list (§2)
[ ] Confirm SCT minting via arif_init() returns session with valid session_token
[ ] Implement forge_email_send_via_resend invoker using MCP standard transport
[ ] Implement forge_receipt_draft + forge_vault receipt parsing
[ ] Implement arif_observability subscriber for inbound notifications
[ ] Implement circuit-breaker detection on {ok: false, dlq: true}
[ ] Implement F13 elicit polling (only if agent uses requires_human: true)
[ ] Implement RFC-8058 List-Unsubscribe honoring in any auto-reply logic
[ ] Test with: forge_email_send(to="arif@arif-fazil.com", subject="...", intent="transactional")
[ ] Verify VAULT999 SEAL append appears in /root/VAULT999/outcomes.jsonl
[ ] Stop. Do NOT bypass L1 governance. Do NOT touch L3 transport directly.
```

---

## 9. Sample Transcripts

### 9.1 Outbound — Low-risk transactional

```python
# In 333-AGI's cognition loop, after a sealed event is created:
result = await mcp.call("forge_email_send_via_resend", {
  "actor_id":    "333-AGI",
  "session_id":  sct,
  "to":          ["arif@arif-fazil.com"],
  "subject":     "[AGI] Sealed receipt — Kuala Lumpur basin 0.2 prospect",
  "body_text":   "Arif,\n\n333-AGI sealed the Kuala Lumpur 0.2 prospect evaluation.\nDetails: ...",
  "intent":      "seal_receipt",
  "requires_human": False,
  "tags":        [{"name": "basin", "value": "kuala_lumpur"}]
})
# Returns:
# {
#   "ok": True,
#   "provider_msg_id": "re_5x9k2j3p",
#   "f13_seal_seq": 15234,
#   "sent_at": "2026-08-01T09:42:11.103Z",
#   "receipt": {...}
# }
```

### 9.2 Outbound — High-risk requiring F13

```python
# 888-APEX wants to escalate a floor violation:
result = await mcp.call("forge_email_send_via_resend", {
  "actor_id":    "888-APEX",
  "session_id":  sct,
  "to":          ["arif@arif-fazil.com"],
  "subject":     "[APEX] F5 PEACE² violation observed in agent-X",
  "body_text":   "Arif, escalation required. Details...",
  "intent":      "escalation",
  "requires_human": True   # <— triggers F13 form-elicit BEFORE transport
})
# Returns immediately with:
# {
#   "ok": False,
#   "verdict": "PENDING_CONSENT",
#   "elicit_url": "https://arif-fazil.com/elicit/...",
#   "elicit_expires_at": "2026-08-01T10:12:11.103Z"
# }
# After Arif approves via UI, transport fires and receipt returns.
```

### 9.3 Inbound — External person → 333-AGI

```
[External] Alice → agent@arif-fazil.com
       │
       ▼
   CF Email Routing (MX)
       │
       ▼
   email-inbound-dispatch worker (CF)
       │
       │  POST https://arifos.arif-fazil.com/mcp/inbox/dispatch (SCT-signed)
       ▼
   arif_inbox_dispatch handler:
     - signature verify: ✅
     - MIME parse: text/plain + PDF attachment → MinIO
     - body_hash: sha256:7e2a...
     - classify: intent=comm, risk=LOW, assigned_to=333-AGI, confidence=0.91
     - heart critique: clean
     - judge: SEAL
     - seal: VAULT999 seq 15235 (mail.receive kind)
     - assigned: mail_messages row, status=new
     - notify: arif_observability event on 333-AGI inbox channel
       │
       ▼
   333-AGI cognition loop (next tick):
     - reads arif_observability inbox event
     - parses body_sha256 + classification
     - decides next action (reply, defer, escalate)
       │
       ▼ (if reply)
     forge_email_send_via_resend(reply-to-thread_id=...)
```

---

## 10. Cross-Reference Map

| Topic | See |
|---|---|
| Floor taxonomy | `/root/arifOS/GENESIS/FLOOR_TABLE.json` |
| Build pipeline | `/root/forge_work/2026-08-01/email-build-spec/BUILD-SPEC-v1.0.md` v1.3 |
| §6 Security | BUILD-SPEC v1.3 §3 |
| §10 A2A-on-SMTP protocol layer | BUILD-SPEC v1.3 §10 |
| §11 Deliverability bounds | BUILD-SPEC v1.3 §11 |
| ACL defaults | BUILD-SPEC v1.3 §9 (use-case calibration) |
| Receipt schema | this doc §6 |
| SOUL.ID / agent identity | `/root/AAA/registries/agent_card.yaml` |

---

## 11. Revision Log

- v1.0 (2026-08-01): First extraction from BUILD-SPEC v1.3. Pure specification, T0 prose. No infra change.
