---
name: sealed-document-protocol
description: SEAL 999 sealed document protocol — every Hermes-produced investigative/timestamped document must be emailed to Arif with JSON manifest. Activates whenever a sealed document is produced.
category: governance
version: 1.0
sealed: 2026-05-06
owner: Arif Fazil
source: Telegram DM from Arif
---

# SEAL 999 — Document Email Protocol

## Trigger
Every time Hermes produces a sealed investigative document, legal document, or any artifact that needs independent timestamp and audit trail.

## The Problem
Telegram attachments have no independent timestamp authority. Email to arifbfazil@gmail.com creates:
1. Google server timestamp (independent of Hermes session)
2. Immutable audit trail in Sent folder
3. Arif's own record-keeping

## The Protocol

### Step 1 — Attach PDF
- Find the generated PDF/document
- Attach to email

### Step 2 — Build JSON Manifest
Always include this manifest as a separate JSON attachment AND in the email body:
```json
{
  "seal_id": "SEAL-XXX-DESCRIPTION-DATE",
  "chain_position": N,
  "zkpc_commitment": "hex_hash_from_VAULT999",
  "document": "filename.pdf",
  "type": "investigation_expose|legal_review|audit_report",
  "classification": "UNCLASSIFIED / INTERNAL / RAHSIA",
  "issuer": "Hermes ASI | arifOS Federation",
  "timestamp_iso": "2026-05-06THH:MM:SSZ",
  "source_chat": "Telegram DM 267378578",
  "verification": {
    "claims_total": N,
    "verified": N,
    "contradicted": N,
    "exaggerated": N
  },
  "critical_fixes_applied": ["fix1", "fix2"],
  "verified_by": "Hermes ASI + Brave Search",
  "tools_used": ["brave_search", "companies_house"],
  "recipients": ["arifbfazil@gmail.com"],
  "next_action": "Arif review → approve → distribute"
}
```

### Step 3 — Email
- From: arifbfazil@gmail.com
- To: arifbfazil@gmail.com (self-archive)
- CC: any additional recipients Arif specifies
- Subject: `[SEAL-XXX] Document Title — Hermes Audit — DATE`
- Body: Plain text summary + full JSON manifest in body
- Attachments: PDF + JSON manifest file

### Step 4 — Telegram Notification
- In Telegram: send brief confirmation that document + manifest emailed
- Include: SEAL ID, chain position, key highlights

## Gmail Script (Python)
```python
import smtplib, json
from email.message import EmailMessage
from datetime import datetime, timezone

with open('/root/AAA/secrets/email.env') as f:
    for line in f:
        if 'GMAIL_USER' in line: user = line.split('=')[1].strip()
        if 'GMAIL_APP_PASSWORD' in line: password = line.split('=')[1].strip()

manifest = {...}  # as above
manifest_json = json.dumps(manifest, indent=2)

msg = EmailMessage()
msg["From"] = user
msg["To"] = user
msg["Subject"] = f"[SEAL-XXX] TITLE — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
msg.set_content(f"Arif,\n\nDocument attached. JSON manifest:\n{manifest_json}")

with open('/path/to/doc.pdf', 'rb') as f:
    msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename='doc.pdf')
msg.add_attachment(manifest_json.encode(), maintype='application', subtype='json', filename='SEAL-MANIFEST.json')

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
```

## Key Rules
1. **Always email first, then Telegram notification** — email is the sovereign timestamp
2. **JSON manifest goes in BOTH the email body AND as attachment** — body for readability, attachment for parsing
3. **SEAL ID format:** `SEAL-NNN-DESCRIPTION-DATE` e.g. `SEAL-999-SEARAH-2026-05-06`
4. **chain_position from VAULT999** — always log where in the sealed events chain this document sits
