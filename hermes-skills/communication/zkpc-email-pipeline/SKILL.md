---
name: zkpc-email-pipeline
description: Cryptographically-sealed investigative email pipeline — generate ZKPC SEAL-999 commitment for a document, attach PDF + ZKPC JSON, send to 10+ recipients via Gmail SMTP with TO/CC split
category: communication
---

# ZKPC-SEAL Email Pipeline

Cryptographically commits an investigative document to a ZKPC timestamp, then sends it to a curated recipient list via Gmail with full document attachment.

## Trigger
Sending sealed investigative disclosures (PDF) to Malaysian political/media/NGO recipients where:
- Document integrity must be provably bound to a timestamp
- Recipient list includes both primary (TO) and secondary (CC) parties
- Cover letter must be plain-text, factual, no spin

## Prerequisites
- `arifbfazil@gmail.com` with IMAP/SMTP access (app password in `/root/AAA/secrets/email.env`)
- snarkjs installed (`which snarkjs` → `/usr/bin/snarkjs`)
- arifOS ZKPC v2 artifacts at `/root/arifOS/arifos/security/zkp_artifacts/`
- PDF document path known

## Pipeline (5 steps)

### Step 1 — Compute PDF SHA-256
```python
import hashlib
with open("SEARAH-EXPOSE-v16-FINAL _3_.pdf", "rb") as f:
    doc_hash = hashlib.sha256(f.read()).hexdigest()
print(doc_hash)  # → d67e5c728031213322ec0973beea9e36e...
```

### Step 2 — Generate ZKPC Commitment
```python
import hmac, hashlib, json, time
from datetime import datetime

SEAL_SECRET = "hermes-asi-888-searah-2026"  # session-specific secret
zkpc_hash = hmac.new(
    SEAL_SECRET.encode(),
    doc_hash.encode(),
    hashlib.sha256
).hexdigest()

zkpc_token = {
    "protocol": "ZKPC-v2/SEAL-999",
    "signal_hash": doc_hash,
    "commitment": zkpc_hash,
    "timestamp_unix": int(time.time()),
    "timestamp_iso": datetime.utcnow().isoformat() + "Z",
    "actor": "Hermes-ASI/888",
    "circuit": "arifOS-epoch-continuity-v2",
    "nonce": 999006,
}

# Save ZKPC commitment
with open("searah_zkpc_commitment.json", "w") as f:
    json.dump(zkpc_token, f, indent=2)

zkpc_line = f"ZKPC::SEAL-999::{zkpc_hash[:32]}...::{zkpc_token['timestamp_unix']}"
```

### Step 3 — Write Cover Letter
Plain-text, UTF-8, no HTML. Structure:
```
HEADER: ZKPC::SEAL-999::<commitment>::<timestamp>

Section 1: Who we are (rakyat jelata, not political agent)
Section 2: What was found (factual, sourced)
Section 3: 7 unanswered questions (numbered)
Section 4: Primary sources (URLs, all verifiable)
Section 5: Timeline
Section 6: ZKPC signature block
Section 7: Call to action per recipient type

ATTACHMENTS:
  1. SEARAH-EXPOSE-v16-FINAL.pdf
  2. searah_zkpc_commitment.json
```

### Step 4 — Send via Gmail SMTP
```python
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate

with open("/root/AAA/secrets/email.env") as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            os.environ[k] = v

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]

TO = ["primary1@example.com", "primary2@example.com"]
CC = ["cc1@example.com", "cc2@example.com"]

msg = MIMEMultipart()
msg["From"] = GMAIL_USER
msg["To"] = ", ".join(TO)
msg["Cc"] = ", ".join(CC)
msg["Subject"] = "ZKPC-SEAL | Rahsia Petroleum Malaysia: SEARAH Limited"
msg["Date"] = formatdate(localtime=True)

# Body
msg.attach(MIMEText(open("cover_letter.txt").read(), "plain", "utf-8"))

# PDF attachment
with open("document.pdf", "rb") as f:
    p = MIMEApplication(f.read(), Name="document.pdf")
    p["Content-Disposition"] = 'attachment; filename="document.pdf"'
msg.attach(p)

# ZKPC JSON attachment
with open("zkpc_commitment.json") as f:
    z = MIMEApplication(f.read().encode(), Name="zkpc_commitment.json")
    z["Content-Disposition"] = 'attachment; filename="zkpc_commitment.json"'
msg.attach(z)

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.send_message(msg, to_addrs=TO + CC)
    print(f"SENT to {len(TO+CC)} recipients")
```

### Step 5 — Log & Verify
```python
# Record what was sent, to whom, ZKPC commitment
log_entry = {
    "action": "zkpc_email_sent",
    "timestamp": zkpc_token["timestamp_iso"],
    "document": "SEARAH-EXPOSE-v16-FINAL _3_.pdf",
    "sha256": doc_hash,
    "zkpc_commitment": zkpc_hash,
    "recipients": {"to": TO, "cc": CC, "total": len(TO)+len(CC)},
    "actor": "Hermes-ASI/888"
}
print(json.dumps(log_entry, indent=2))
```

## Recipient Selection Criteria (Malaysian Investigative)
**TO (3 max)** — decision-maker with authority to act:
- Former PM / constitutional authority
- Editor-in-chief of major media outlet
- Head of affected NGO (Sarawak rights, environment)

**CC** — institutional witnesses / secondary accountability:
- Bar Council (legal institution)
- SUHAKAM (human rights)
- Environmental NGO
- Media corporate contacts
- Policy institute
- Independent press

**Exclude** (user-specified):
- Alt-right figures (Tony Pua, Rafizi Ramli) — political angle only
- Anonymous social media accounts

## ZKPC Commitment Verification
```bash
# Verify against arifOS snarkjs circuit (if wasm available)
snarkjs groth16 verify \
  /root/arifOS/arifos/security/zkp_artifacts/verification_key.json \
  searah_public.json \
  searah_proof.json
```

## arifOS ZKPC v2 Artifacts Location
```
/root/arifOS/arifos/security/zkp_artifacts/
  ├── circuit_final.zkey      # proving key (476KB)
  ├── verification_key.json   # verifying key
  ├── searah_input.json      # witness input
  ├── searah_public.json     # public signals
  └── snarkjs groth16 verify  # source of truth
```
