# Outbound send lanes — two options for disclosure correspondence

The lane used to send a vendor acknowledgment, a correction, or any external correspondence from this estate.

## Option 1: Governed lane (`gov_email.py`) — DEFAULT

`/root/.hermes/lanes/email_lane/gov_email.py` wraps the Brevo transactional REST API with a governance layer: prepare → confirm token → send, with an append-only hash-chained audit ledger.

### Probe
```bash
cd /root && python3 /root/.hermes/lanes/email_lane/gov_email.py status
```
Returns `{status, lane, sender, auth_check, ledger, reads_available}`. `status: READY` with `auth_check.http_status: 200` means sends work.

### Prepare (READ_ONLY — no network call)
```bash
cd /root && python3 /root/.hermes/lanes/email_lane/gov_email.py prepare \
  --to "recipient@example.com" \
  --subject "Re: ..." \
  --body "..." \
  --actor arif
```
Returns `{status: PREPARED, confirm_token, expires_utc}`. The token is valid for the window; re-run prepare if it expires.

### Send (MUTATE_IRREVERSIBLE — requires confirm token)
```bash
cd /root && python3 /root/.hermes/lanes/email_lane/gov_email.py send \
  --to "recipient@example.com" \
  --subject "Re: ..." \
  --body "..." \
  --actor arif \
  --confirm "<token-from-prepare>"
```
**The payload (to/subject/body) must be IDENTICAL to prepare.** Different payload → token rejected → zero network calls.

Returns `{status: SENT, message_id, lane: email:brevo, ledger_entries}`. The `message_id` is the Brevo messageId for delivery tracking.

### Audit trail
- Ledger: `/root/.hermes/lanes/email_lane/audit/email_ledger.jsonl`
- INTENT entry written and fsynced BEFORE the network call; SENT entry written after.
- Every entry is hash-chained; tampering breaks the chain.
- Drafts: `gov_email.py drafts` shows any pending prepares.

### Key facts
- Sender: `arifbfazil@gmail.com` (Brevo-verified).
- Reads (inbox) are DEAD — Gmail OAuth expired. Cannot search or retrieve incoming mail through this lane.
- The `--confirm` token is single-use; a second `send` with the same token is rejected.

---

## Option 2: APA email bridge (`forge_email` :18093)

Endpoint: `http://127.0.0.1:18093/` (loopback only, no auth header). Backed by the systemd unit `apa-email-bridge.service`.

### Probe
```bash
curl -s -m 6 http://127.0.0.1:18093/health
```
Returns `{ok, backends, brevo_configured, gmail_configured, sender, status}`.

- `status: READY` with `backends: ["brevo-send"]` means **sends work**.
- A dead READ lane (`gmail_configured: false`) does **not** block sending.
- `sender` is the From address — confirm it matches what the counterparty expects before sending.

### Send
```python
import json, urllib.request
req = urllib.request.Request(
    "http://127.0.0.1:18093/",
    data=json.dumps({"mode": "send", "to": "<addr>", "cc": "<addr>",
                     "subject": "...", "body": body}).encode(),
    headers={"Content-Type": "application/json"}, method="POST")
```
Returns `{ok, mode, result: {message_id, status, provider, sha256, timestamp}}`.

- `to` / `cc` accept a single address or a list.
- `body` is plain text; the bridge also wraps it for HTML clients.

### Route facts
- **Only two routes exist:** `GET /health` and `POST /`.
- `GET /` returns `{"error": "not found"}`. There is **no** `/openapi.json`.
- `/health`'s `verbs` list describes the bridge's full verb set, but `search` / `read` / `list_labels` need Gmail IMAP credential. Only `send` works on the Brevo key alone.

### Receipt
- No sent-items store. Write body to `~/.hermes/cache/outbound/<name>.txt` first for hash reproducibility.
- Report `message_id`, `sha256`, and `timestamp` to the principal.

---

## Choosing between lanes

| | Governed (`gov_email.py`) | APA bridge (`forge_email`) |
|---|---|---|
| **Audit trail** | Hash-chained JSONL ledger | Content hash in response only |
| **Send guard** | Requires confirm token | No guard (immediate send) |
| **Sender** | arifbfazil@gmail.com | Configurable (check /health) |
| **Default for** | All disclosure correspondence | Non-disclosure sends, or when governed lane is unavailable |

**Default:** governed lane.

## Corrections and follow-ups

When a follow-up corrects something an earlier message claimed, send it **on the same thread** with the same subject line. A promised follow-up that never arrives is what turns a friendly counterparty into a public critic.