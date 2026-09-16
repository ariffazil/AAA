# Outbound send lane — APA email bridge (`forge_email`)

The lane used to send a vendor acknowledgment, a correction, or any external correspondence from this estate. Verified working for sends.

Endpoint: `http://127.0.0.1:18093/` (loopback only, no auth header). Backed by the systemd unit `apa-email-bridge.service`.

## Probe first

```bash
curl -s -m 6 http://127.0.0.1:18093/health
```

Returns `{ok, backends, brevo_configured, gmail_configured, sender, status}`.

- `status: READY` with `backends: ["brevo-send"]` means **sends work**.
- A dead READ lane (`gmail_configured: false`) does **not** block sending. Do not diagnose a send failure from the read-lane flag.
- `sender` is the From address — confirm it matches what the counterparty expects before sending.

## Send

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

## Route facts — do not waste calls

- **Only two routes exist:** `GET /health` and `POST /`.
- `GET /` returns `{"error": "not found"}`. There is **no** `/openapi.json` — do not hunt for a schema.
- `/health`'s `verbs` list (`search`, `read`, `send`, `list_labels`) describes the bridge's full verb set, but `search` / `read` / `list_labels` need the Gmail IMAP credential. Only `send` works on the Brevo key alone.

## The response is the receipt

The lane keeps no sent-items store. So:

1. **Write the body to a file first** (`~/.hermes/cache/outbound/<name>.txt`) — then the hash is reproducible and the exact text can be re-derived later.
2. **Report all three back to the principal:** `result.message_id`, `result.sha256`, `result.timestamp`. The `sha256` is the content hash of the message.

That hash is the only durable evidence of *what text* went out. It is what lets a later audit compare a recovered draft against what was actually sent — without it, a draft on disk and a send record in a transcript cannot be reconciled.

## Corrections and follow-ups

When a follow-up corrects something an earlier message claimed (e.g. "this is not in the release" → "the release landed"), send it **on the same thread** with the same subject line. A promised follow-up that never arrives is what turns a friendly counterparty into a public critic.
