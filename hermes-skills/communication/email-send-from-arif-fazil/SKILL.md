---
name: email-send-from-arif-fazil
description: Send email from arifbfazil@gmail.com using secrets from /root/AAA/secrets/email.env. Handles the execute_code sandbox env-var visibility issue.
category: communication
---

# Email Send — arifbfazil@gmail.com

## The Gotcha

`execute_code` (hermes_tools sandbox) CANNOT see env vars set by `email.env` via `source /root/AAA/secrets/email.env`. The sandbox has its own environment — `os.environ.get('GMAIL_APP_PASSWORD', '')` returns empty string inside `execute_code`, even though `terminal()` can see it fine.

**Always use `terminal()` Python for email send, not `execute_code()`.**

## Credentials

File: `/root/AAA/secrets/email.env`
```
GMAIL_USER=arifbfazil@gmail.com
GMAIL_APP_PASSWORD=<16-char app password>
```

## Send Email (Correct Method)

Use `terminal()` with inline Python that reads the password file directly:

```python
python3 << 'EOF'
import smtplib, os
from email.message import EmailMessage

# Read password directly from file (bypasses sandbox env-var issue)
password = None
with open('/root/AAA/secrets/email.env') as f:
    for line in f:
        if 'GMAIL_APP_PASSWORD' in line and '=' in line:
            password = line.strip().split('=', 1)[1].strip()
            break

user = "arifbfazil@gmail.com"

msg = EmailMessage()
msg["From"] = user
msg["To"] = "recipient@example.com"
msg["Subject"] = "Subject here"
msg.set_content("Body text here")

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
print("SENT OK")
EOF
```

## Port / Security

- Port 587 with `starttls()` — works from af-forge VPS
- If 587 fails, try port 465 with `SMTP_SSL`
- App password is 16 chars, prefix `zclv` — if wrong, Gmail returns `535 Username and Password not accepted`

## arifos@arif-fazil.com Alias

Sending FROM `arifos@arif-fazil.com` requires separate SMTP config — currently not set up. All outgoing email via this method only sends FROM `arifbfazil@gmail.com`.

---

## ⚠️ Critical: Gmail SMTP Silent Failure — Sent Folder ≠ Delivered

**The Problem:**
Gmail SMTP can silently REJECT your email at the auth layer. If your code saves to the Sent folder *before* calling `server.send_message()`, a Sent folder entry exists even when the SMTP call throws `SMTPAuthenticationError`. This creates a false "success" state — you see the email in Sent, but it was NEVER delivered to any recipient.

**Error signature:**
```
SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted.')
```

**Why it happens:**
- Wrong or expired app password
- Gmail detected untrusted app/device
- 2FA disabled on the Google Account (app passwords require 2FA)

**Correct verification pattern — do BOTH:**
```python
all_recipients = to_list + cc_list  # flatten first!

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        # send_message returns {} on success, dict of failures on partial/total failure
        result = server.send_message(msg, to_addrs=all_recipients)
        if result:
            print(f"⚠️ PARTIAL FAILURES: {result}")
        else:
            print(f"✅ DELIVERED to all {len(all_recipients)} recipients")
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ AUTH FAILED — email NOT sent. Fix app password at: https://myaccount.google.com/apppasswords")
    raise  # re-raise so you see the error
except Exception as e:
    print(f"❌ SMTP ERROR: {e}")
    raise
```

**Key rules:**
1. **Do NOT trust Sent folder as proof of delivery** — it only proves the MUA saved the message, not that SMTP accepted it
2. **Always flatten `to_addrs`** — `send_message(to_addrs=to_list + cc_list)`, not nested lists
3. **Catch `SMTPAuthenticationError` specifically** — it's the most common Gmail failure mode
4. **`send_message()` return value** — empty dict `{}` = all delivered; non-empty = failures per recipient

**If auth keeps failing, check:**
1. Google Account → Security → 2-Step Verification is ON (required for app passwords)
2. Google Account → Security → App Passwords → generate new 16-char password
3. Update `/root/AAA/secrets/email.env` with the new password

**Batch send (TO + CC + BCC):**
```python
TO = ["to1@example.com", "to2@example.com"]
CC = ["cc1@example.com", "cc2@example.com"]
BCC = ["bcc1@example.com"]

msg["To"] = ", ".join(TO)
msg["Cc"] = ", ".join(CC)
# BCC goes only to send_message, not in headers
all_recipients = TO + CC + BCC

server.send_message(msg, to_addrs=all_recipients)
```
