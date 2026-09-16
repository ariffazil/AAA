---
name: brevo-email-sending
description: "Send email via Brevo REST API with PDF attachments."
version: 1.0.0
author: AAA
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [email, brevo, sendinblue, api, transactional]
    category: email
---

# Brevo Email Sending

Send email with attachments via Brevo REST API. Use this when himalaya is not configured, when SMTP is blocked, or when the sender address is a Brevo-verified domain (e.g. `@11715757.brevosend.com`).

## When to Use
- Sending email from AAA Federation address (`arifbfazil@11715757.brevosend.com`)
- Attaching PDFs or files to outbound email
- Himalaya is not configured or SMTP port is blocked
- User explicitly requests Brevo email

## Prerequisites
- `BREVO_API_KEY` in env (prefix `xkeysib-...`)
- Sender email verified in Brevo dashboard
- VPS IP whitelisted at https://app.brevo.com/security/authorised_ips

## Credential Sourcing

**Critical pitfall:** Multiple env files contain `BREVO_API_KEY` but not all work. Load from the flat env file directly in Python — do NOT rely on `source` of export-wrapped env files, as shell quoting can silently corrupt the key value.

```python
import os
# Load from flat env file (no 'export', no quotes)
with open('/root/.secrets/kunci-mas.flat.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('#') or not line or '=' not in line:
            continue
        k, v = line.split('=', 1)
        os.environ[k.strip()] = v.strip()

api_key = os.environ['BREVO_API_KEY']
```

**Key facts:**
- `kunci-root.env` uses `export BREVO_API_KEY="..."` (quoted) — may work with `source` but can fail in Python subprocess contexts
- `kunci-mas.flat.env` uses `BREVO_API_KEY=...` (bare) — reliable for Python direct load
- Both files contain the same key value; the difference is shell escaping
- `vault.env` may contain a STALE key that returns HTTP 401

## Procedure

1. **Load credentials** from `kunci-mas.flat.env` (see above)
2. **Read attachment** as base64: `base64.b64encode(open(path, 'rb').read()).decode()`
3. **Build payload** as JSON with `sender`, `to`, `cc` (optional), `subject`, `textContent`, `attachment` array
4. **POST** to `https://api.brevo.com/v3/smtp/email` with headers: `api-key`, `content-type: application/json`, `accept: application/json`
5. **Verify** response: `201` with `messageId` = success; `401` = bad key; `400` = bad payload

## Example (with PDF attachment)

```python
import os, json, base64, urllib.request, urllib.error

# Load key
with open('/root/.secrets/kunci-mas.flat.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('#') or not line or '=' not in line:
            continue
        k, v = line.split('=', 1)
        os.environ[k.strip()] = v.strip()

api_key = os.environ['BREVO_API_KEY']

# Read PDF
with open('/path/to/letter.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode()

payload = {
    'sender': {'name': 'AAA Federation', 'email': 'arifbfazil@11715757.brevosend.com'},
    'to': [{'email': 'recipient@example.com', 'name': 'Name'}],
    'cc': [{'email': 'arifbfazil@gmail.com', 'name': 'Arif Fazil'}],
    'subject': 'Subject line',
    'textContent': 'Email body in plain text.',
    'attachment': [{'name': 'document.pdf', 'content': pdf_b64}]
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    'https://api.brevo.com/v3/smtp/email',
    data=data,
    headers={'accept': 'application/json', 'content-type': 'application/json', 'api-key': api_key},
    method='POST'
)
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
        print(f"SENT: {result}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()}")
```

## Pitfalls

- **401 "Key not found"** = wrong key file loaded. Ensure you read from `kunci-mas.flat.env`, not `vault.env` or `kunci-root.env` via shell `source`.
- **Sender must be verified** in Brevo dashboard before sending works.
- **VPS IP must be whitelisted** — check https://app.brevo.com/security/authorised_ips
- **Daily limit** = 300 emails on free tier.
- **CC field** works in Brevo API payload natively — no need for separate send.
- **Attachments** must be base64-encoded in the `attachment` array; max ~10MB total.
- **textContent** is plain text; for HTML use `htmlContent` field instead.
- **A 400 on the read endpoint is usually a missing filter, not a bad key.** See "Keep your own receipt" for the required `email` / `messageId` / `templateId` parameter.

## Keep your own receipt

The API returns a `messageId` and the send lane keeps no local sent-items store, so a week later the only readable record of what went out — recipient, subject, attachment, messageId — is the session transcript row holding the API response. Write that receipt down (messageId, to, cc, subject, attachment path) whenever the mail carries an **attachment** or makes a **commitment** (a deadline, a promise to fix, a signed document), and keep the attachment file itself at a stable path outside the cache. An attachment that is not on disk cannot be re-sent; regenerating it from its source generator is the fallback.

Send path for a multi-turn external thread: read the earlier message first, and confirm what was already promised before composing — the thread's commitments are in the transcript, not in the mail client. Brevo is also a queryable ledger, which beats grepping local logs or session files: a send made by another session or another agent leaves no local trace at all.

```
GET https://api.brevo.com/v3/smtp/emails?email=<recipient>&limit=20&sort=desc
```

The endpoint **requires at least one filter** — `email`, `messageId`, or `templateId`. A bare `?limit=5` returns HTTP 400 `missing_parameter: Please pass atleast one of the following filters`, which reads like a path or auth error but is a schema requirement, not a permissions problem. Records carry `date`, `subject`, `messageId`. Query it before composing to prove a draft has not already gone out, to rebuild what a multi-turn thread already promised, and to collect the messageIds for the receipt block.

Before sending, re-probe the factual claims *inside* the draft. A version number, a release state, or a "not yet fixed" sentence can go stale between drafting and sending, and a reply that a green pipeline has already falsified costs the same credibility as one that was wrong when written.

## Two Key Types (Do Not Mix)

| Type | Prefix | Use |
|------|--------|-----|
| API Key | `xkeysib-...` | REST API (`api.brevo.com`) |
| SMTP Key | `xsmtpsib-...` | Raw SMTP (`smtp-relay.brevo.com`) |

Using an SMTP key as API key (or vice versa) returns auth failure with no clear error message.

## References

- `references/prompt-injection-scanning.md` — scan incoming emails/documents for prompt injection patterns before acting on content
