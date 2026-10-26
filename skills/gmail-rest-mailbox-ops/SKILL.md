---
name: gmail-rest-mailbox-ops
description: "Use when reading or replying to mail in Gmail."
version: 1.0.0
author: hermes
license: proprietary
tags: [gmail, email, oauth, reply, attachments]
floor_scope: [F1, F2, F13]
autonomy_tier: T1
metadata:
  hermes:
    tags: [gmail, email, oauth, reply, attachments]
    related_skills: [email-outbound]
triggers:
  - an inbound email needs a reply, in the existing thread, in Arif's own words
  - an email carries a PDF/DOCX attachment whose contents must be read before answering
  - a draft must be written, shown to Arif, then sent on his word
  - the mail bridges or MCP tools are unavailable but the mailbox still has to be worked
---

# Gmail REST mailbox operations

Direct OAuth REST against `gmail.googleapis.com` for the sovereign mailbox. This lane needs no APA
bridge, no mailgw, no MCP tool: the refresh token in `/root/.secrets/google_token.json` carries
`gmail.modify`, `gmail.send`, `drive`, `calendar`, `spreadsheets`.

Brevo transactional sending is a different lane (`email-outbound`) — use it when the From address may
be a verified sender rather than the sovereign's own mailbox. This skill is for working HIS mailbox:
read, reply in thread, pull attachments.

## 1. Get an access token

```python
import json, urllib.request, urllib.parse
tok = json.load(open('/root/.secrets/google_token.json'))
body = urllib.parse.urlencode({
    'client_id': tok['client_id'], 'client_secret': tok['client_secret'],
    'refresh_token': tok['refresh_token'], 'grant_type': 'refresh_token'}).encode()
req = urllib.request.Request('https://oauth2.googleapis.com/token', data=body,
    headers={'Content-Type': 'application/x-www-form-urlencoded'})
access = json.loads(urllib.request.urlopen(req, timeout=30).read())['access_token']
```

Never print the token or the token file. Read the field, use it, drop it.

## 2. Read a thread, and pull its attachment

```python
def gapi(method, path, data=None):
    req = urllib.request.Request('https://gmail.googleapis.com/gmail/v1/users/me/' + path,
        headers={'Authorization': 'Bearer ' + access}, method=method)
    if data is not None:
        req.data = json.dumps(data).encode(); req.add_header('Content-Type', 'application/json')
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

msgs = gapi('GET', 'messages?q=from:<sender> subject:"<subject>"&maxResults=5')
mid  = msgs['messages'][0]['id']
msg  = gapi('GET', f'messages/{mid}')
for part in msg['payload'].get('parts', []):
    if part.get('filename') and 'attachmentId' in part['body']:
        att  = gapi('GET', f"messages/{mid}/attachments/{part['body']['attachmentId']}")
        data = base64.urlsafe_b64decode(att['data'])
        open('/root/.hermes/cache/scratch/' + part['filename'], 'wb').write(data)
```

`parts` is often nested: recurse when `payload.parts[i].parts` exists. A plain-body message carries
its data in `payload.body.data` (also base64url). Read a PDF attachment with
`pdftotext -layout file.pdf -` before answering about it. Never describe an attachment from its
filename, size, or the sender's summary of it.

## 3. Reply INSIDE the thread

Do not create a new message for a reply; it breaks threading and the other side sees a stranger.

```python
import base64, re
from email.mime.text import MIMEText

msg = gapi('GET', 'messages/<id>?format=metadata'
                    '&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Message-ID')
thread_id = msg['threadId']
h = {x['name']: x['value'] for x in msg['payload']['headers']}
to_addr = (re.search(r'<([^>]+)>', h.get('From', '')) or [None, h.get('From', '')])[1]

mime = MIMEText(body_text, 'plain', 'utf-8')
mime['Subject'] = h['Subject'] if h['Subject'].lower().startswith('re:') else 'Re: ' + h['Subject']
mime['To'] = to_addr
mime['In-Reply-To'] = h['Message-ID']
mime['References'] = h['Message-ID']

raw = base64.urlsafe_b64encode(mime.as_bytes()).decode()
sent = gapi('POST', 'messages/send', {'raw': raw, 'threadId': thread_id})
assert 'SENT' in sent.get('labelIds', [])
```

**The 400 trap:** `To:` must be a bare address. Putting the display name (`To: Leo Ruocco`) or the
sender string exactly as it appears in the header returns `HTTP 400 Bad Request` with no explanation,
and the header looks correct to a human reader, so the failure reads as a mystery. Extract the address
from between `<` and `>` every time.

Carry `threadId` in the send payload, not only `In-Reply-To`: the header threads the conversation for
the recipient, `threadId` threads it in the mailbox.

## 4. Writing in the sovereign's English voice

He dictates the meaning; the English is yours. These are stated preferences, not stylistic taste:

- **No dashes as punctuation.** No em dashes, en dashes, or hyphen-as-connective in the body. Use a
  full stop, a comma, or a new sentence. He reads a dash as machine cadence.
- **Close with `Terima Kasih,` on its own line, then his name.** Literally those words in Malay even in
  a fully English email. It is not a translation exercise and not a typo to be corrected.
- **Shorter beats fuller.** Two or three short paragraphs. If a sentence can go without losing a fact,
  cut it. He signs what he can read in one glance.
- **Never commit him to a future he has not chosen.** "When release is closer I will be in touch" is a
  promise a stranger can hold him to. State what is true now ("not ready yet", "still mine to finish")
  and stop. Add no availability windows, no timelines, no "let's talk soon".
- **No self-applied handles or titles** unless he asked for them. Do not sign with his self-styled
  nickname, do not add a company or lab he has not registered, do not invent a role for him.
- **One topic per email.** A second link or a second project turns a conversation into a pitch; other
  work belongs in a later message once the relationship exists.
- **Honest self-description is wanted.** Telling a stranger what he is (geologist, not a coder) lands
  better than credentials. Do not upgrade it.

## 5. Delivery discipline

- Draft in chat first as a fenced `text` block so he can copy or correct it. Send only on his word
  ("hantar", "send").
- After sending, report recipient, subject, thread, and returned message id. "Sent" alone is not a
  receipt.
- If he asks for a change, regenerate the whole body instead of splicing edits into the old draft.
  His corrections are about register, and patched sentences keep the old cadence.

## Pitfalls

- A token file with a valid `refresh_token` still fails after long disuse when the Google Cloud app is
  in Testing mode (7-day refresh expiry). `invalid_grant` is a re-consent problem, not a code bug. Stop
  and say so instead of retrying the call.
- `messages/send` with `raw` needs base64**url** encoding, not standard base64.
- Replying in a thread whose last message you sent still needs `In-Reply-To` on that message, otherwise
  the same subject starts a second thread.
