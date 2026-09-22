---
name: email-outbound
description: Use when sending email from the VPS. Check Brevo lane first.
version: 1.0.0
author: hermes
license: proprietary
tags: [email, brevo, gmail, notifications]
floor_scope: [F1, F2, F13]
autonomy_tier: T1
metadata:
  hermes:
    tags: [email, brevo, gmail]
    related_skills: []
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Outbound Email from the Federation VPS

Class-level skill for any "send this email / email the bank / notify X by email" task.

## Lane selection — ALWAYS check this first

Do NOT start by setting up Gmail OAuth. Check what already works:

1. `source /root/.secrets/kunci-root.env && env | grep -i -E "brevo|smtp|mail"`
2. If `BREVO_API_KEY` + `BREVO_SENDER_EMAIL` exist → use the Brevo transactional lane below. Verified working 2026-08-25 (CIMB unblock request, messageId returned first try).
3. Only fall back to Gmail OAuth (`gws`) when the From address MUST literally be the Gmail account AND Arif can complete browser consent from a device that can reach the VPS callback. See `references/gmail-oauth-lane.md`.

## Brevo transactional lane (default)

Inline payload shape (POST to `api.brevo.com/v3/smtp/email`):
- `sender: {name, email}` — MUST be a Brevo-verified sender (currently arifbfazil@gmail.com).
- `to: [{email, name}]`, `subject`, `htmlContent` (escape `&` as `&amp;`).
- Response: `{"messageId": "<...>"}` — quote it back to Arif; delivery trackable in Brevo dashboard (Transactional → Logs).
- `env | grep BREVO_API_KEY` → kunci-root.env has it; never echo into chat.

## Attachments (governed lane only)

The Brevo lane carries file attachments. One file per `--attach`, repeatable:

```bash
python3 gov_email.py prepare --to a@b.com --subject S --body B \
  --html "$(cat body.html)" --attach /abs/path/file.pdf --actor hermes-asi
python3 gov_email.py send    --to a@b.com --subject S --body B \
  --html "$(cat body.html)" --attach /abs/path/file.pdf --actor hermes-asi --confirm <token>
```

- `--attach` takes an **absolute path**; `--html` takes the **HTML string** (use `"$(cat f.html)"`). The two flags read differently — mixing them silently ships a filesystem path as your body.
- Attachment **SHA-256 + size are bound into the confirm digest**, so a file swapped between `prepare` and `send` invalidates the token. Change the file → re-run `prepare`.
- Attachment-free payloads keep a byte-identical digest, so this stayed additive and did not invalidate older prepared tokens.
- Brevo caps the whole request (~10 MB, and base64 inflates ~33 %); keep attachments well under.
- `mcp_server.py` does **not** expose attachments — use the CLI for anything with a file.

**Order of operations that catches the real defect:** build the artifact → `sha256sum` it → paste that hash into the body → `prepare` → confirm `prepare` echoes the same `attachments[].sha256` → `send`. Quoting a hash computed *before* a later rebuild is the standard trip-up: the PDF changes (a label fix, a provenance note) and the body's hash silently becomes a false claim about the bytes the recipient will verify. Re-hash after every rebuild.

## Content discipline (financial / official correspondence)

- NEVER invent personal data. IC, phone, account/card digits, registered email — fill ONLY from what Arif typed in chat.
- Content must be Arif's words or explicitly approved by him. Sending on his explicit instruction is authorized.
- Keep bank-facing HTML minimal (p/ul/ol/strong). Emojis sparingly.
- Signature block carries his full name as given.

## Governed lane (preferred entry point)

`/root/.hermes/lanes/email_lane/` wraps the Brevo lane with a governance layer — use it instead of hand-rolling a `urllib` POST, so the send is witnessed.

- `gov_email.py status|verify|drafts|prepare` = READ_ONLY_AUTONOMOUS, no confirmation.
- `gov_email.py send` = MUTATE_IRREVERSIBLE: needs `--actor` + `--confirm <token>` from `prepare` with an identical payload. Missing/wrong token → `HOLD`, zero network calls.
- Append-only hash-chained ledger: `audit/email_ledger.jsonl` (INTENT written and fsync'd BEFORE the network call; SENT after). If the ledger is unwritable the send is refused.
- `mcp_server.py` exposes the same gates as MCP tools; the MCP surface cannot bypass them.
- `--dry-run` proves the credential via `GET /v3/account` without putting a message on the wire.

## Google Workspace lane is currently dead (do not debug it, re-authorise once)

`forge_gmail`/`forge_calendar` were commented out of the A-FORGE MCP surface (`core.ts`, commit `21e8a608` 2026-08-17, "Phase 2 ZEN Sweep"), but the backing APA bridges (18093/18094/18097/18098/18099) still run as systemd units. They report `AWAITING_CREDENTIALS` because `/root/.secrets/google_token.json` returns `invalid_grant` from the OAuth token endpoint, and the IMAP `app_password` in `/root/.secrets/email/gmail.json` is a placeholder. Re-authorising once restores gmail read+send, calendar, drive and sheets together — a single fix, not four. Do not patch the bridges; the defect is the credential.

## Pitfalls

- **Sender identity vs registered email:** Brevo sends From arifbfazil@gmail.com. If the recipient expects mail from Arif's registered address (e.g. CIMB registered = ariffazil@live.com), state the registered email clearly in the body so their verification isn't blocked — and warn Arif about the mismatch before sending.
- **Don't restart OAuth flows repeatedly** while handing Arif links — each `gws auth login` binds a new random localhost port and invalidates prior links.
- **Never dump BREVO_API_KEY** into chat, receipts, or files outside /root/.secrets.
- Brevo sender verification for any NEW sender address requires mailbox confirmation — stop and tell Arif, don't loop retries.

## Verification

After send: non-empty messageId in response → report recipient + subject + messageId to Arif. Auth error → re-source kunci-root.env. Sender rejection → sender not verified in Brevo; stop and report.
