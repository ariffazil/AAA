---
name: gmail
description: Read and send emails via arifbfazil@gmail.com using Gmail IMAP/SMTP
category: communication
---

# Gmail Email Skill

## Trigger
Any task involving email — read inbox, send message, search emails, check unread.

## Credentials
Stored in: `/root/AAA/secrets/email.env` (mode 600)
Also available as env vars: `GMAIL_USER`, `GMAIL_APP_PASSWORD`

## IMAP (Read)
```python
import imaplib, email, os
from email.header import decode_header

user = os.environ.get("GMAIL_USER", "arifbfazil@gmail.com")
password = os.environ.get("GMAIL_APP_PASSWORD", "")

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(user, password)
mail.select("INBOX")

# Fetch last 10 emails
_, msgs = mail.search(None, "ALL")
ids = msgs[0].split()
for uid in ids[-10:]:
    _, data = mail.fetch(uid, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])
    subject = msg["Subject"]
    sender = msg["From"]
    date = msg["Date"]
    print(f"{date} | {sender} | {subject}")

mail.logout()
```

## SMTP (Send)
```python
import smtplib, os
from email.message import EmailMessage

user = os.environ.get("GMAIL_USER", "arifbfazil@gmail.com")
password = os.environ.get("GMAIL_APP_PASSWORD", "")

msg = EmailMessage()
msg["From"] = user
msg["To"] = "recipient@example.com"
msg["Subject"] = "Subject here"
msg.set_content("Body text here")

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
```

## Search Inbox
```python
# Unread only
mail.select("INBOX")
_, msgs = mail.search(None, "UNSEEN")

# Search by subject
_, msgs = mail.search(None, 'SUBJECT "keyword"')

# Search by sender
_, msgs = mail.search(None, 'FROM "someone@gmail.com"')
```

## Actions
- **Read inbox** → fetch N recent emails, show sender/subject/date
- **Send email** → compose and send via SMTP
- **Search** → search by sender, subject, keyword
- **Unread count** → report unread email count
- **Mark read** → mark specific email as read

## From address
All outgoing emails show From: `arifbfazil@gmail.com` — no alias support via IMAP/SMTP.
If you need to send from `arifos@arif-fazil.com`, requires Cloudflare/Resend API instead.
