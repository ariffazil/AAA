---
name: google-workspace-gws
description: Use when needing Gmail, Google Drive, Calendar, Docs, or Sheets from any agent on forge VPS — wired via official gws CLI (OAuth live, verified 2026-09-16). Triggers "gmail", "drive", "google calendar", "google docs", "spreadsheet", "send email", "google workspace".
---

# Google Workspace via gws CLI (official @googleworkspace/cli)

**Status: LIVE on forge (KVM8).** OAuth refresh token valid, encrypted store at `/root/.config/gws/`, no plaintext creds. Verified 2026-09-16 (Drive/Gmail/Calendar real reads). Canonical wiring doc: `/root/docs/google-ecosystem-wiring.md`.

## The rule

`gws` is installed at `/usr/bin/gws` and works from ANY agent shell on this VPS. No MCP server exists for it by design (removed upstream at v0.8.0 — 200-400 tool context bloat). Skills+CLI beat MCP 17-32x. Call it via bash directly.

## Discipline (from forge-google-workspace skill — load it for full runbook)

1. **Schema-first**: `gws schema <service.resource.method>` before first use of any method.
2. **Dry-run writes**: `--dry-run` on every create/update/delete/send before real execution.
3. **Stable IDs**: resolve file/message/event IDs before mutating. Never write against ambiguous names.
4. **Bounded pagination**: `--page-all` only with `--page-limit`.
5. **Sanitize external text**: `--sanitize <template>` when content feeds an autonomous prompt (F12).

## Verified patterns

```bash
gws drive files list --params '{"pageSize": 5}'                      # OBS: list files
gws gmail users labels list --params '{"userId":"me"}'               # OBS: mailbox
gws gmail users messages list --params '{"userId":"me","maxResults":5}'
gws calendar events list --params '{"calendarId":"primary","timeMin":"<ISO>","maxResults":5,"singleEvents":true,"orderBy":"startTime"}'
gws drive files get --params '{"fileId":"ID"}' --output /tmp/x       # download
gws sheets spreadsheets values get --params '{"spreadsheetId":"ID","range":"A1:D10"}'
gws schema drive.files.list                                          # introspect before new calls
```

## Scopes granted (2026-09-16 consent)

`drive` (rw) · `gmail.send` + `gmail.readonly` · `calendar.events` (rw primary) · `documents` (rw) · `spreadsheets` (rw) · openid/profile.
**NOT granted:** calendar.readonly (calendarList metadata → 403 — use events, not list), gmail.modify/labels (advanced), any cloud-platform scope. NEVER request `--full`.

## Escalation

- Writes to Arif's real email/calendar/docs that reach OTHER humans → F13 territory (external consequence), dry-run + surface to Arif.
- Scope expansion → requires new browser consent (Arif) — stage the exact `gws auth login --scopes` command, never widen silently.
- Re-auth if `invalid_grant` returns: token died — see `/root/docs/google-ecosystem-wiring.md` §Phase 1 for the tunnel+consent procedure.

## Known surfaces

| Surface | Path |
|---|---|
| Wiring doc | `/root/docs/google-ecosystem-wiring.md` |
| gws config | `/root/.config/gws/` (encrypted) |
| Legacy bridges | `apa-email-bridge.service`, `apa-calendar-bridge.service` still on app-passwords — do NOT delete `/root/.secrets/email/gmail.json` / `/root/.secrets/calendar/google.json` until bridges migrate |
