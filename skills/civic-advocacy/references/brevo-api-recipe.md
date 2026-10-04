# Brevo Email API Recipe (Verified 2026-08-09)

## Authentication
- API Key: `BREVO_API_KEY` from `/root/.secrets/kunci-mas.env`
- Sender: `arifbfazil@gmail.com` / `AAA Federation`
- SMTP password ≠ API key — use REST API only

## Send Email with Attachment

```python
import requests, json, base64, os

API_KEY = os.environ.get('BREVO_API_KEY')
SENDER_EMAIL = os.environ.get('BREVO_SENDER_EMAIL')
SENDER_NAME = os.environ.get('BREVO_SENDER_NAME')

# Read file
with open('/path/to/file.pdf', 'rb') as f:
    content = base64.b64encode(f.read()).decode('utf-8')

# Send
headers = {
    "api-key": API_KEY,
    "accept": "application/json",
    "content-type": "application/json"
}

email_data = {
    "sender": {"email": SENDER_EMAIL, "name": SENDER_NAME},
    "to": [{"email": "recipient@example.com", "name": "Name"}],
    "cc": [{"email": "cc@example.com", "name": "CC Name"}],
    "subject": "Subject Line",
    "htmlContent": "<html><body><p>Email body</p></body></html>",
    "attachment": [
        {
            "name": "filename.pdf",
            "content": content  # base64 encoded
        }
    ]
}

resp = requests.post(
    "https://api.brevo.com/v3/smtp/email",
    headers=headers,
    json=email_data
)

if resp.status_code == 201:
    print("✅ Sent successfully")
    print(f"Message ID: {resp.json().get('messageId')}")
else:
    print(f"❌ Failed: {resp.status_code}")
    print(resp.text)
```

## Key Points
1. **Attachment format:** Array with `name` and `content` (base64)
2. **Status 201:** Success
3. **CC field:** Use `"cc"` array, not `"to"` for carbon copies
4. **HTML content:** Use `"htmlContent"` for rich formatting
5. **No SMTP needed:** REST API only, no port/auth issues

## Common Errors
- `400 Invalid attachment`: Check base64 encoding and array format
- `401 Unauthorized`: Check API key
- `403 Forbidden`: IP not authorized (add to Brevo dashboard)
