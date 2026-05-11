---
name: third-eye-document-audit
description: 3rd-eye audit skill — extract claims from a PDF, verify against live web sources (Brave Search), produce sealed document with JSON manifest. Used for SEARAH investigation documents.
category: research
version: 1.0
sealed: 2026-05-06
owner: Arif Fazil
source: Telegram DM from Arif
---

# 3RD EYE DOCUMENT AUDIT PROTOCOL

## Purpose
Verify factual claims in a PDF document against live web sources. Produce sealed output with JSON manifest emailed to Arif.

## When to Use
- Arif sends a PDF for "audit", "3rd eye", "verify", "full 000-990"
- Any investigative document needing independent fact-check before distribution

## The Metabolic Loop (000-990)

### 000 — INIT (Extract)
```bash
pdftotext /path/to/doc.pdf - | head -c 5000  # preview
pdftotext /path/to/doc.pdf /tmp/doc_full.txt  # full text
```

### 111 — THINK (Identify Claims)
List all specific factual claims — names, dates, numbers, events, quotes.

### 333 — EXPLORE (Search Batch)
Use Brave Search for each batch of claims. Max 2 concurrent searches.

```bash
BRAVE_KEY=$(grep BRAVE_API_KEY /root/.hermes/.env | sed 's/.*=//')
curl -s -H "Accept: application/json" \
     -H "X-Subscription-Token: $BRAVE_KEY" \
     "https://api.search.brave.com/res/v1/web/search?q=YOUR+QUERY&count=8" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
for r in d.get('web',{}).get('results',[]):
    print(r.get('title',''))
    print(r.get('url',''))
    print(r.get('description','')[:250])
    print('---')
"
```

### 555 — HEART (Audit Verdict)
Classify each claim:
- **VERIFIED ✅** — confirmed by credible source
- **CONTRADICTED ❌** — source directly contradicts
- **EXAGGERATED ⚠️** — partially true but wrong magnitude/direction
- **NAME_ERROR ❌** — person/company fabricated or not found
- **UNVERIFIABLE ❓** — cannot confirm, need primary source

### 777 — REASON (Fix Report)
Compile findings. Critical issues (contradictions, fabrications) MUST be fixed before distribution.

### 888 — AUDIT (Telegram Briefing)
Send Arif a structured summary:
```
✅ Verified: N
❌ Critical: N
⚠️ Minor: N

KEY ISSUES:
1. [Claim] → [Problem] → [Fix required]

Email sent ✅
SEAL-XXX | Chain: NNN
```

### 999 — SEAL (Email + Manifest)
Always email first, then Telegram.

```python
import smtplib, json
from email.message import EmailMessage
from datetime import datetime, timezone

with open('/root/AAA/secrets/email.env') as f:
    for line in f:
        if 'GMAIL_USER' in line: user = line.split('=')[1].strip()
        if 'GMAIL_APP_PASSWORD' in line: password = line.split('=')[1].strip()

manifest = {
    "seal_id": "SEAL-XXX-DESCRIPTION-DATE",
    "chain_position": N,
    "zkpc_commitment": "auto_generated",
    "document": "filename.pdf",
    "type": "investigation_expose",
    "classification": "UNCLASSIFIED",
    "issuer": "Hermes ASI | arifOS Federation",
    "timestamp_iso": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "source_chat": "Telegram DM 267378578",
    "verification": {"claims_total": N, "verified": N, "contradicted_critical": N, "name_error": N, "unverifiable": N},
    "critical_fixes_needed": ["fix1", "fix2"],
    "verified_by": "Hermes ASI — Brave Search audit",
    "tools_used": ["brave_search", "reuters", "eni_press", "companies_house"],
    "recipients": ["arifbfazil@gmail.com"],
    "next_action": "Arif review → fix → redistribute"
}
manifest_json = json.dumps(manifest, indent=2)

msg = EmailMessage()
msg["From"] = user
msg["To"] = user
msg["Subject"] = f"[SEAL-XXX] TITLE — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
msg.set_content(f"Arif,\n\nDocument attached.\n\n=== JSON MANIFEST ===\n{manifest_json}\n\nSEAL-XXX | Chain: NNN\n")
with open('/path/to/doc.pdf', 'rb') as f:
    msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename='doc.pdf')
msg.add_attachment(manifest_json.encode(), maintype='application', subtype='json', filename='SEAL-MANIFEST.json')

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
```

## Key Lessons Learned

1. **pdftotext** — works on Linux, output encoding may have Chinese/Japanese chars (Malayalam in one doc)
2. **Brave Search** — key sources: UNCTAD, Companies House, Reuters, Eni press releases, Statista, Offshore Technology
3. **ICSID claims** — always verify causality direction (who sued whom first, not just that both filed)
4. **People names** — always cross-check against official embassy/consulate/government websites
5. **Numbers** — always get exact source for quantities (Statista vs older data can differ by 40%)
6. **Cross-reference** — if two docs on same subject exist, audit findings from one may apply to both (SEARAH Indonesia/Malaysia ratio)
