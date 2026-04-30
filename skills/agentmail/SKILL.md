---
name: agentmail
description: Give Hermes its own email inbox. Send, receive, and manage email autonomously via agent-owned email addresses (hermes@agentmail.to). Use when you need to send emails, receive replies, manage email threads, sign up for services via email, or communicate with other agents/humans via email.
tags: [email, communication, agentmail, mcp]
version: 1.0.0
author: Hermes / arifOS AAA
license: MIT
requirements:
  - AgentMail API key (am_your_key_here)
  - Node.js 18+ (for npx agentmail-mcp)
  - mcp Python package (pip install mcp)
---

# AgentMail — Agent-Owned Email Inbox

## Quick Start

1. Create inbox: `create_inbox(username="hermes-agent")` → gets `hermes-agent@agentmail.to`
2. Send: `send_message(inbox_id=..., to=recipient, subject=..., text=...)`
3. Check replies: `list_threads(inbox_id=...)` → `get_thread(thread_id=...)`
4. Reply: `reply_to_message(message_id=..., text=...)`

## Available Tools

| Tool | Description |
|------|-------------|
| `list_inboxes` | List all agent inboxes |
| `get_inbox` | Get details of a specific inbox |
| `create_inbox` | Create a new inbox (gets real email address) |
| `delete_inbox` | Delete an inbox |
| `list_threads` | List email threads in an inbox |
| `get_thread` | Get a specific email thread with all messages |
| `send_message` | Send a new email |
| `reply_to_message` | Reply to an existing email |
| `forward_message` | Forward an email |
| `update_message` | Update message labels/status |
| `get_attachment` | Download an email attachment |

## Configuration

The MCP server is configured in `~/.hermes/config.yaml` under `mcp.servers`.
API key is set via environment variable `AGENTMAIL_API_KEY`.

## Workflows

### Send an email
1. `create_inbox` if no inbox exists yet
2. `send_message(inbox_id, to=email, subject=subject, text=body)`

### Check for replies
1. `list_inboxes` → get inbox_id
2. `list_threads(inbox_id=inbox_id)` → list conversation threads
3. `get_thread(thread_id=thread_id)` → read full thread

### Reply to an email
1. `get_thread` to find the message_id
2. `reply_to_message(message_id=msg_id, text=reply_text)`

### Sign up for a service
1. `create_inbox(username="signup-bot")` → gets inbox address
2. Use the inbox address to register on the service
3. `list_threads` to check for verification email
4. `get_thread` to read the verification code

## Constitutional Notes

- F01 AMANAH: No irreversible email deletion without 888_HOLD
- F04 CLARITY: State purpose of email in subject line
- F05 PEACE: No harmful or abusive content
- F12 INJECTION: Sanitize all email inputs (no raw HTML injection)

## Limitations

- Free tier: 3 inboxes, 3,000 emails/month
- Free tier sends from @agentmail.to domain only
- Real-time inbound: use `list_threads` polling via cronjob

## Verification

```
Use list_inboxes to confirm the MCP connection is working.
```
