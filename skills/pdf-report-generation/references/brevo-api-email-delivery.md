# Brevo API Email Delivery

## When to use
- Sending PDF reports/letters via email with attachments
- Brevo (formerly Sendinblue) API is configured in kunci-mas.env

## Environment variables
```
BREVO_API_KEY=xkeysib-...
BREVO_SENDER_EMAIL=arifbfazil@gmail.com
BREVO_SENDER_NAME=AAA Federation
```

## Critical: Attachment format (proven 2026-08-09)

**WRONG:** Single object
```json
"attachment": {"name": "file.pdf", "content": "base64..."}
```

**CORRECT:** Array of objects
```json
"attachment": [{"name": "file.pdf", "content": "base64..."}]
```

## API endpoint
```
POST https://api.brevo.com/v3/smtp/email
Headers: api-key: {BREVO_API_KEY}, Content-Type: application/json
```

## Full send pattern
```python
import requests, json, base64, os

API_KEY = os.environ['BREVO_API_KEY']
SENDER = os.environ['BREVO_SENDER_EMAIL']
NAME = os.environ['BREVO_SENDER_NAME']

# Read and encode PDF
with open('report.pdf', 'rb') as f:
    content = base64.b64encode(f.read()).decode('utf-8')

# Send
resp = requests.post("https://api.brevo.com/v3/smtp/email",
    headers={"api-key": API_KEY, "Content-Type": "application/json"},
    json={
        "sender": {"email": SENDER, "name": NAME},
        "to": [{"email": "recipient@gmail.com", "name": "Name"}],
        "cc": [{"email": "cc@gmail.com", "name": "CC Name"}],
        "subject": "Subject line",
        "htmlContent": "<html><body>Cover letter HTML</body></html>",
        "attachment": [{"name": "report.pdf", "content": content}]
    }
)
# Returns 201 with messageId on success
```

## Pitfalls
- API key ≠ SMTP password. Brevo SMTP requires separate password from dashboard.
- IP must be authorized in Brevo dashboard (Settings → Authorized IPs)
- Attachment content must be base64-encoded string, not bytes
- "to" and "cc" fields are arrays, not single objects
- **Attachment format is array, not single object** (proven 2026-08-09, 3 failed attempts). The API returns `invalid_parameter` with single object. Always use `[{name, content}]` array format.

## External AI audit pattern (proven 2026-08-09)
Before publishing high-stakes documents, send to an external AI for peer review:
```python
# Use FED proxy to call Gemini for external audit
resp = requests.post("http://127.0.0.1:4000/v1/chat/completions",
    headers={"Authorization": f"Bearer {LITELLM_MASTER_KEY}"},
    json={
        "model": "gemini-flash",
        "messages": [
            {"role": "system", "content": "Independent external AI auditor. Review this document for: (1) Strengths, (2) Weaknesses, (3) Missing data, (4) Legal risks, (5) Virality, (6) Verdict. Be brutally honest."},
            {"role": "user", "content": document_text}
        ],
        "temperature": 0.3
    }
)
```
Gemini audit found: commodity cycle blindness (PAT drop was industry-wide), dividend mechanics (MoF decides, not CEO), geopolitical analogy too inflammatory. Led to tersurat/tersirat rewrite.
