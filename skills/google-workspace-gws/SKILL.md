---
name: google-workspace-gws
description: "Use when needing Gmail, Google Drive, Calendar, Docs, or Sheets from any agent on forge VPS — wired via official gws CLI (OAuth live, verified 2026-09-16)."
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Google Workspace via gws CLI (official @googleworkspace/cli)

**Status: LIVE on forge (KVM8).** Token custody moved 2026-09-20 to a dedicated
service identity. Store: `/var/lib/mail-gateway/gws/` (0700, uid `mail-gateway`).
No plaintext creds. Verified 2026-09-20 end-to-end (Gmail/Drive reads through the
broker). Boundary proof: `python3 /root/A-FORGE/bridges/gws_truth_test.py`.
Canonical wiring doc: `/root/docs/google-ecosystem-wiring.md`.

## The rule

`gws` is installed at `/usr/local/bin/gws` — a **broker shim**, not the raw CLI.
It routes every call through `mailgw-broker.service` (uid `mail-gateway`), which
is the only identity that can read the OAuth token store. Call it via bash
directly; there is no MCP server for it by design (removed upstream at v0.8.0 —
200-400 tool context bloat). Skills+CLI beat MCP 17-32x.

**Reading just works.** No env vars needed — the shim derives actor and purpose
from the calling process. `gws gmail users messages list ...` returns live data.

**Never call `/usr/bin/gws` directly.** That is the raw CLI, and the AppArmor
profile `arifos-gws-citizen` denies it the token store (you get
`Permission denied (os error 13)`). Use the bare name.

**Agent quick reference (read/write rules, receipts, troubleshooting):**
`/root/AAA/canon/MAIL-GATEWAY-AGENT-QUICKREF.md`

**New agent identity needs socket access?** `python3 /opt/mailgw/mailgw_grant.py --add <user>`

**Verify the boundary before trusting it:**
`python3 /root/A-FORGE/bridges/gws_truth_test.py` — exit 0 means no closeable
defect is open. Full spec: `/root/AAA/canon/FEDERATION_GMAIL_GATEWAY_SPEC.md`.

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

## Token custody (moved 2026-09-20)

The OAuth store now lives at **`/var/lib/mail-gateway/gws`** (0700, uid
`mail-gateway`) — NOT `/root/.config/gws`. Retired copy at
`/var/lib/mail-gateway/gws.retired-20260920`.

Consequences:
- A non-root agent **cannot read the token store**. That is the boundary working.
- Do not try to set `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` yourself — the broker sets it.
- `gws-refresh.sh` re-execs itself as `mail-gateway` under the broker profile; run
  it normally and let it elevate.
- Kill switch: `touch /var/lib/mail-gateway/GMAIL_REVOKED` refuses every call.
- Receipts: `/var/lib/mail-gateway/audit/receipts.jsonl` (also at
  `/root/AAA/ops/capabilities/mailgw_broker_receipts.jsonl`).

## Reading Gmail — use `mailread` (canonical, governed path)

**Status: LIVE and verified 2026-09-20. Warga can read mail.**

Bare `gws gmail ...` still works, but the **canonical way to read mail** is the
`mailread` wrapper. It routes through the token-custody broker, attaches an actor
id and a purpose, and mints a receipt — so a read is attributable, not anonymous.

```bash
mailread list 5                        # latest N message ids (default 5)
mailread search "from:ytlailabs.com"  # Gmail search syntax, optional count last
mailread meta  <MESSAGE_ID>            # headers only: From / Subject / Date
mailread body  <MESSAGE_ID>            # full body (purpose-scoped)
mailread labels                        # list labels
mailread check                         # can *I* read mail? diagnose if not
```

**Run `mailread check` first when anything looks wrong.** It prints identity, group
membership, socket reachability and a live read — so a failure arrives as a
diagnosis, not a traceback. Exit 0 = ok, 2 = not in group / socket denied,
3 = broker down.

### Granting access to another identity

Access is membership in group `mailgw-clients` (the broker socket at
`/run/mailgw/broker.sock` is mode 660, and `/run/mailgw` is 770 — so a process
outside the group cannot even `stat` the socket; the kernel denies before any
policy check).

```bash
mailread check                          # as the user in question, first
usermod -aG mailgw-clients <user>       # grant (needs a new process to take effect)
systemctl restart <the service running as that user>.service
```

**After granting, verify with a live read — never assume the group took.** A long-running
service holds the groups it started with; that is why the restart is part of the grant,
not an optional extra. Measured 2026-09-20: granting `forge` without restarting
`apa-gws-bridge` left the bridge reporting `scopes_granted: []`; after the restart all
four services reported `in_scope: true`.

Current holders (2026-09-20): `root` (every warga CLI spawns as root), `arifos`, `forge`
(A-FORGE organ + the five `apa-*` Google bridges). `frame` is deliberately **not** granted
— a witness organ with mail access is not an independent witness.

Identity + purpose default to `HERMES` / `mailread <action>`. Override per call when
the read matters, so the receipt says why:

```bash
MAILREAD_ACTOR=OpenCode MAILREAD_PURPOSE="semak thread disclosure YTL" mailread body <ID>
```

**There is no send / forward / delete in `mailread`, by construction.** Those are
`EXTERNAL_CONSEQUENCE` / `HIGHER_IMPACT` and require a sovereign F13 token. Trying
one prints a refusal; it does not fall through to the raw CLI.

### Why the broker path and not bare `gws`

Bare `gws gmail ...` resolves through `/usr/local/bin/gws` (a PATH shim) into the
same broker, so both work today. Prefer `mailread`: it fixes the actor/purpose for
you and cannot be mistaken for an authority grant.

### What is NOT yet enforced (know this, do not overclaim it)

Read works; the boundary is **not complete**. Measured 2026-09-20 by
`/root/A-FORGE/bridges/gws_truth_test.py` (12 vectors, `ENFORCED_WITH_ROOT_RESIDUAL`):

- AppArmor **does** confine the raw CLI (`/usr/bin/gws` → permission denied) and
  **does** bind root where applied — proven by
  `bridges/evidence/repro-confine-denies-root.sh`.
- But citizen processes (this gateway, opencode, qwen, codex, kimi) are still
  **unconfined**, and the token store's `.encryption_key` sits in plaintext beside
  the ciphertext — so an unconfined process can decrypt the OAuth credential
  without touching `gws` at all.
- Fix is to **confine the callers**, not to move the files. Tracked as an open loop.
  Do not describe the current state as a chokepoint; it is a governed wrapper.

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
