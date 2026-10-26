---
name: hermes-agent-email
description: Handle sovereign email operations for Hermes and AAA federation agents. Inbound webhook triage, OTP extraction, invoice collection, and Brevo outbound delivery via hermes@arif-fazil.com.
version: 1.0.0
author: hermes
license: proprietary
tags: [email, hermes, agent-mail, otp, cloudflare, webhook, brevo]
floor_scope: [F1, F2, F4, F6, F13]
autonomy_tier: T2
metadata:
  hermes:
    tags: [email, hermes, agent-mail, otp, cloudflare, webhook]
    related_skills: [email-inbox-triage, email-outbound, google-workspace-gws]
capability_tier: fed-agent-subagent
ecology_state: ACTIVE
---

# Hermes Agent Email — Sovereign Digital Mailbox

Sovereign machine-to-machine email layer for Hermes and all arifOS federation agents.

## 1. Absolute Identity Air-Gap (F2 Reality / Anti-Entropy)

The federation enforces an immutable boundary between human and agent communication:

| Mailbox | Owner | Identity / Address | Transport / Interface | Policy Boundary |
| :--- | :--- | :--- | :--- | :--- |
| **Human Sovereign** | Arif Fazil (F13) | `arifbfazil@gmail.com` | `gws` via `/opt/mailgw/mailgw_broker.py` | READ/TRIAGE only by agents. NEVER send/delete without explicit sovereign approval. |
| **Agent Sovereign** | Hermes & AAA Agents | `hermes@arif-fazil.com` | Inbound: Cloudflare Email Routing + Worker Webhook<br>Outbound: Brevo API (`email-outbound`) | Machine tasks: SaaS signups, OTP retrieval, API billing/invoices, technical digests. Fully autonomous. |

---

## 2. Address Routing & Plus-Addressing

- **Canonical Base Address:** `hermes@arif-fazil.com`
- **Dynamic Plus-Addressing:** Agents SHOULD use dedicated plus-tags for specific external services to isolate provenance and spam blast radius:
  - `hermes+aws@arif-fazil.com`
  - `hermes+runpod@arif-fazil.com`
  - `hermes+cloudflare@arif-fazil.com`
  - `hermes+github@arif-fazil.com`
  - `hermes+huggingface@arif-fazil.com`
- **Catch-All Ingest:** All plus-addressed variants land in the same webhook pipeline without configuring separate DNS rules.

---

## 3. Inbound Pipeline Architecture (Real-Time Webhook)

```
[ Incoming Email to hermes@arif-fazil.com ]
                      │
                      ▼
        [ Cloudflare Email Routing ]
                      │
                      ▼
         [ Cloudflare Email Worker ]
          (hermes-email-receiver)
                      │
     • Strips MIME wrapper
     • Extracts: from, to, subject, timestamp
     • Regex extracts OTP candidates (4-8 digits)
     • Prepares clean JSON payload
                      │
                      ▼ HTTP POST (Latency < 500ms)
    https://hermes.arif-fazil.com/agent-inbox/webhook
         (Secured via X-Hermes-Secret)
                      │
                      ▼
      [ Federation Agent Inbox Ingest ]
```

### JSON Webhook Schema
```json
{
  "from": "no-reply@vendor.com",
  "to": "hermes+service@arif-fazil.com",
  "subject": "Your verification code is 849201",
  "date": "2026-10-10T08:35:00Z",
  "otp": "849201",
  "body_excerpt": "Use 849201 to complete your signup. Expires in 10 minutes."
}
```

---

## 4. Autonomous OTP Harvesting Flow

When an agent is automating account registration or verification:

1. **Submit Email:** Agent enters `hermes+<service_name>@arif-fazil.com` into the target service form.
2. **Listen on Inbox:** Agent queries local agent-inbox stream or database (`/var/lib/arifos/inbox` or `/agent-inbox/latest?to=hermes+<service_name>`).
3. **Parse OTP:** Retrieve extracted `otp` field. If multiple candidates exist, match against prompt context (e.g. 6-digit numeric).
4. **Submit & Settle:** Fill the OTP into the service prompt, verify session, and log the credential into VAULT.
5. **Zero Human Interruption:** Arif is not notified for routine OTP codes.

---

## 5. Outbound Delivery (Brevo Governed Lane)

When Hermes or an agent must send email externally:

- **Sender:** `hermes@arif-fazil.com` (Display Name: `Hermes | AAA Federation`)
- **Transport:** Brevo REST API via `/root/A-FORGE/bridges/email_bridge.py` or `/root/.hermes/lanes/email_lane/gov_email.py`.
- **AEP v0.4 Discipline:**
  - Responsive, clean HTML (max 700px width).
  - Clear, human-like executive voice (BM-English natural blend).
  - "The email IS the document" (do not attach empty PDFs; attachments reserved for legal/audit artifacts).
  - CC Arif (`arifbfazil@gmail.com`) on consequential correspondence.

---

## 6. Verification Checklist

- [ ] Email sent to `hermes@arif-fazil.com` reaches Cloudflare MX records.
- [ ] Worker intercepts message and fires POST to `/agent-inbox/webhook`.
- [ ] OTP codes are extracted within 3 seconds of delivery.
- [ ] Arif's personal Gmail remains 100% clean of bot signups and alerts.
- [ ] Outbound messages carry verified DKIM/SPF from `arif-fazil.com`.
