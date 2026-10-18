---
name: aforge-google-workspace
description: Use when fixing A-FORGE Google Workspace bridges & email.
---

# A-FORGE Google Workspace capability

Operate and fix A-FORGE's own GWS stack: the `apa-*-bridge` systemd services, the `forge_gmail`/`forge_drive`/`forge_sheets`/`forge_calendar` MCP tools, and the email send/read lanes. This is A-FORGE's Python OAuth bridge chain — NOT the `gws` npm CLI (that is the separate `forge-google-workspace` skill).

## Component map

| Layer | Path |
|---|---|
| systemd services | `apa-gmail-bridge.service` (18097), `apa-drive-bridge` (18099), `apa-sheets-bridge` (18075), `apa-calendar-bridge` (18094) |
| bridge code | `/root/A-FORGE/bridges/{gmail,drive,sheets,calendar}_bridge.py` + `google_bridge_base.py` |
| MCP handler | `src/capabilities/google-workspace/forgeGoogleWorkspace.ts` (`bridgeCall`, `gateMutate`, per-service handlers) |
| CLI bridge | `src/capabilities/google-workspace/gws_bridge.py` (spawned by handler, calls `google_workspace.py`) |
| API impl | `src/capabilities/google-workspace/google_workspace.py` (`google_gmail_send`, `google_gmail_read_unread`, `google_drive_*`, `google_sheets_*`, `google_calendar_*`) |
| token | `/root/.secrets/google_token.json` — LIVE OAuth token (drive + gmail.modify + gmail.send + spreadsheets + calendar) |
| F12 gate | `src/domain/governance/f12Injection.ts` |

## Build + deploy loop (after any `.ts` change)

```bash
cd /root/A-FORGE
npx tsc -p tsconfig.json && node scripts/copy-handwritten-js.mjs
sudo systemctl restart a-forge-mcp.service      # or apa-*-bridge.service for .py changes
```

A-FORGE MCP runs the COMPILED `dist/` tree (`/root/A-FORGE/dist/src/interfaces/mcp/cli.js`). Editing `src/` without `tsc` leaves the live service on stale code. Verify with `curl -s http://127.0.0.1:7072/health` (`tools_listed` is the only live tool count to quote).

## Bug class (each is a rule, not an incident)

1. **`SERVICE_FN` must be `staticmethod(_service_factory)`.** `google_bridge_base` calls `self.SERVICE_FN(creds)`. A plain function assigned to a class attribute binds `self` as the first arg → `TypeError: _service_factory() takes 1 positional argument but 2 were given`. Any new connector must copy the `staticmethod` wrapper from `calendar_bridge.py`.

2. **`SCOPES` must match what the token actually holds.** `Credentials.from_authorized_user_file(path, SCOPES)` requests exactly the listed scopes. Scope the token lacks → refresh returns `invalid_scope` (bridge reports `AWAITING_CREDENTIALS`). Narrow read-only scope (`gmail.readonly`) while the token has `gmail.modify`+`gmail.send` → write verbs fail even though the token is capable. Send requires `gmail.modify`+`gmail.send` in the bridge's `SCOPES` list.

3. **`execFileSync` arg array, never `execSync` string.** The MCP handler builds the bridge command from user-supplied args (email body, subject). `execSync(parts.join(" "))` runs it through a shell → an email body containing `(` becomes `Syntax error: "(" unexpected`. `execFileSync(python, [bridge, service, verb, ...flagValuePairs])` passes argv with no shell. Every bridge invocation must use the arg-array form.

4. **F12 `SHELL_METACHARS` false-positives on free-text → add the tool to `CODE_ACCEPTING_TOOLS`.** Unicode em-dash, emoji, `&`, `#`, `()` in email bodies / sheet values trip the F12 shell-metachar floor and VOID the call even with no shell present. Once a tool executes via `execFileSync` (no shell) and mutation is gated by `gateMutate`, add it to `CODE_ACCEPTING_TOOLS` in `f12Injection.ts` (`forge_gmail`/`forge_drive`/`forge_sheets`/`forge_calendar` are already there).

5. **Token path lists must include the LIVE path.** `google_workspace.py` `_TOKEN_PATHS` resolves by `Path.exists()`; if every entry points at a non-existent file, send fails with "token.json not found". Keep `/root/.secrets/google_token.json` first in the list.

6. **systemd `User=` must be able to read the token.** The GWS bridges defaulted to `User=forge`, which cannot traverse `/root/.secrets/` (root-only). Symptom: `journalctl -u apa-gmail-bridge.service` logs "token file missing: /root/.secrets/google_token.json" while the file exists. Set `User=root` (match `apa-calendar-bridge.service`) or move the token to a path the service user can read.

## Send/read verification (cheap, reversible, no real mail)

- Read: `forge_gmail` verb `search`/`read_unread` returns `status: OK` with `emails[]`.
- Write (reversible): `draft_create` then `draft_delete` proves the write path without firing email.
- Definitive: `forge_gmail` verb `send` with `to` = self address and a clean ASCII body returns `message_id`. For unicode/emoji bodies, confirm the F12 allowlist (rule 4) is in place first.
- `gateMutate` treats `gmail.send`/`gmail.draft_send` as F13-authorized (passes), defaulting `actor_id` to `arif` for audit — send is a sovereign-authorized lane, not a HOLD.
