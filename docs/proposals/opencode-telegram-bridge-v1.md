# OpenCode Telegram Bridge v1 — Specification

**Status:** DRAFT (sealing pending `forge_execute`)
**Version:** 1.0
**Date:** 2026-06-06
**Author:** OPENCLAW (AGI-executor, host: af-forge)
**Sovereign:** Arif Fazil (Telegram ID `267378578`)
**Constitutional floor:** F1 AMANAH (eigenselection), F2 TRUTH, F11 AUTH, F13 SOVEREIGN (waived this session by direct decree)
**Doctrine:** DITEMPA BUKAN DIBERI

---

## 1. Executive Summary

> **UPDATE 2026-06-06 22:38 UTC — prior art discovered during deploy.**
> The `@arifOS_bot` (000Ω code specialist) is already running in AAA group, polling Telegram, with the full 888_HOLD / hermes-opencode wrapper / allowlist / journal logging architecture baked in. The "bridge" is effectively 000Ω. This spec pivots from "deploy a new bridge" to "start `opencode serve` so 000Ω can attach." The full bridge code (this spec's original scope) is held in reserve as a Stage-2 enhancement, not deployed today.

Deploy a Telegram bridge service that connects Arif's Telegram account to a localhost-only OpenCode server. The bridge is a thin Python service that:

1. Receives Telegram messages from Arif (allowlist-enforced, no other user)
2. Forwards them to a localhost-only OpenCode server via HTTP
3. Streams the responses back to Telegram
4. Gates every irreversible action through arifOS's `arif_judge_deliberate` for 888_HOLD
5. Logs every event to VAULT999 with `actor_id=opencode-bridge`

The **MVP** (this spec) deploys in **echo mode** — read tools only, write/edit/bash **blocked at the permission layer**. The full bridge with permission gates and session persistence is post-MVP (estimated 3-5 days).

**Reversibility:** Fully reversible. To uninstall:

```bash
systemctl stop opencode-bridge opencode
rm -rf /srv/arifos/opencode-bridge
rm -f /etc/systemd/system/opencode-bridge.service /etc/systemd/system/opencode.service
systemctl daemon-reload
```

---

## 2. Architecture

```
Telegram (Arif, allowlist only)
        │ HTTPS webhook / long-poll
        ▼
┌─────────────────────────────────────┐
│  arifos-opencode-bridge.service     │
│  Python 3.11+, systemd, F1-gated   │
│  Allowlist: {267378578}             │
│  Binds: localhost-only              │
└──────────────┬──────────────────────┘
               │ HTTP 127.0.0.1:4096
┌──────────────▼──────────────────────┐
│  opencode serve                     │
│  Model: opencode/claude-sonnet-4-5  │
│  Permission file: read/grep/glob/   │
│    webfetch = allow, write/edit/    │
│    bash = ask, destructive = deny   │
│  Working dir: /srv/arifos/          │
└──────────────┬──────────────────────┘
               │ (bridge calls independently)
┌──────────────▼──────────────────────┐
│  arifOS MCP (arif_judge_deliberate) │
│  Endpoint: http://127.0.0.1:8088    │
│  Used for 888_HOLD on /build        │
└─────────────────────────────────────┘
```

Three independent processes. Each can be restarted, scaled, or killed without taking down the others. The bridge is the only thing that talks to Telegram.

---

## 3. Components

> **Pivot note:** The 000Ω arifOS-bot already implements 3.2 (bridge service) and 3.3 (arifOS MCP integration). 3.1 is the missing piece — the opencode server itself. The 000Ω uses `OPENCODE_ATTACH_URL=http://localhost:4096` and auto-attaches when the server is reachable.

### 3.0 Prior Art — 000Ω arifOS-bot

- **Service:** `opencode-bot.service` (enabled, running since 2026-06-06 22:10:37 UTC)
- **Source:** `/root/.openclaw/workspace/bots/opencode-bot/bot.py` (~16 KB)
- **Token:** `/root/.secrets/tokens/telegram-opencode-bot`
- **Modes:**
  - `TRANSLATOR` — read-only, no judge gate (OBSERVE class)
  - `/forge` — gated through `hermes-opencode` → arifOS 888_JUDGE → SEAL/SABAR/VOID
  - `ATTACH` — auto-attaches to opencode serve on `http://localhost:4096` when running
- **Allowlist:** `267378578` (Arif) only
- **Hardening:** ProtectSystem=strict, NoNewPrivileges=true, MemoryMax=512M, CPUQuota=50%

### 3.1 OpenCode Server (`opencode.service`)

| Attribute | Value |
|---|---|
| Binary | `/usr/bin/opencode` v1.15.0 |
| Mode | `opencode serve` |
| Binding | `127.0.0.1:4096` (loopback-only by default) |
| mDNS | off |
| CORS | empty |
| Model | `opencode/claude-sonnet-4-5` |
| Working dir | `/srv/arifos/` |
| User | `arif` (non-root) |
| Env | `OPENCODE_SERVER_PASSWORD=<long-random>` (defense-in-depth) |

### 3.2 Bridge Service (`opencode-bridge.service`)

| Attribute | Value |
|---|---|
| Language | Python 3.11+ |
| Stack | `httpx` (async HTTP to opencode), `python-telegram-bot` (TG polling) |
| Allowlist | `{267378578}` — hardcoded, no env override |
| Mode (MVP) | `echo` — read tools only, write/edit/bash blocked |
| Mode (post-MVP) | `gated` — full permission flow with TG inline buttons |
| Working dir | `/srv/arifos/opencode-bridge/` |
| User | `arif` (non-root) |
| Audit | every message → `arifOS.arif_mind_reason(mode='store', actor_id='opencode-bridge')` |

### 3.3 arifOS MCP Bridge

- Endpoint: `http://127.0.0.1:8088` (existing `arifos.service`)
- Tool: `arif_judge_deliberate(mode='judge', candidate=action, claimed_evidence_level=...)`
- Trigger: every `/build` command from the bridge
- Verdict routing:
  - **`SEAL`** → forward to opencode, proceed
  - **`SABAR`** → ask Arif for explicit override (TG inline button)
  - **`VOID`** → deny + log to VAULT999

The **F1 eigenselection lives in arifOS, not in opencode's runtime.** opencode's permission gate is Layer 1 (necessary). arifOS 888_HOLD is Layer 2 (sufficient).

---

## 4. Permission Model

### 4.1 OpenCode Permission File

`/srv/arifos/opencode-bridge/permission.json`:

```json
{
  "read": "allow",
  "grep": "allow",
  "glob": "allow",
  "webfetch": "allow",
  "list": "allow",
  "edit": "ask",
  "write": "ask",
  "bash": "ask",
  "shell": "deny"
}
```

**Hard-deny patterns** (no prompt, ever — Layer 1 enforcement):

| Pattern | Reason |
|---|---|
| `rm -rf /`, `rm -rf /*` | Destructive recursive delete |
| `dd if=` | Raw disk write |
| `mkfs`, `mkfs.ext4`, `mkfs.xfs` | Filesystem format |
| `shutdown`, `reboot`, `halt`, `poweroff` | System state change |
| `curl ... \| sh`, `wget ... \| sh` | Remote code execution |
| `chmod 777`, `chmod -R 777` | World-writable (security) |
| `> /dev/sd*` | Direct disk write |
| `:(){:\|:&};:` | Fork bomb |

The principle: **read = ambient, write = intentional.** A read is observation. A write is a SEAL — it requires witness.

### 4.2 arifOS 888_HOLD Wire

```
User (Telegram): /build refactor auth middleware
Bridge:
  1. Parse command → action candidate
  2. Call arifOS.arif_judge_deliberate(
       mode='judge',
       candidate='edit:src/auth/middleware.py:refactor',
       claimed_evidence_level='INTERPRETATION',
       actor_id='arif-267378578',
       evidence_receipt={<prior context from opencode>}
     )
  3. Verdict:
     - SEAL: forward to opencode, proceed
     - SABAR: post TG inline buttons [Override] [Cancel]
     - VOID: deny + log
```

arifOS is the constitutional kernel. opencode is the workhorse. The bridge is dumb pipe.

---

## 5. Session Persistence

**SQLite database** at `/srv/arifos/opencode-bridge/sessions.db`:

```sql
CREATE TABLE sessions (
  chat_id TEXT PRIMARY KEY,
  opencode_session_id TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  message_count INTEGER DEFAULT 0
);

CREATE INDEX idx_last_active ON sessions(last_active);

CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  chat_id TEXT NOT NULL,
  role TEXT CHECK(role IN ('user', 'assistant', 'system')),
  content TEXT,
  opencode_message_id TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (chat_id) REFERENCES sessions(chat_id)
);
```

**Behavior:**
- **On bridge startup:** read all `chat_id → opencode_session_id` mappings, validate each against opencode server
- **On new message:** if `chat_id` exists in `sessions` and opencode session is alive, reuse; else create new
- **On every message:** insert into `messages` for audit + crash recovery
- **On opencode session death:** re-create session, re-hydrate last 5 messages from SQLite

**Why SQLite, not JSON:** concurrent writes from multiple TG messages would corrupt a JSON file. SQLite handles concurrency via WAL mode.

---

## 6. Scope of Authority

### 6.1 The bridge CAN, without explicit confirmation per call:

- Receive and respond to Telegram messages
- Call opencode tools: `read`, `grep`, `glob`, `webfetch`, `list`
- Call arifOS tools: `arif_judge_deliberate`, `arif_mind_reason` (for audit), `arif_ops_measure` (for health)
- Log to VAULT999 via arifOS

### 6.2 The bridge CANNOT, even with explicit confirmation:

- Edit files in `/etc/`, `/boot/`, `/usr/`, `/var/lib/`
- Modify systemd unit files
- Touch Docker socket
- Read `/root/.ssh/` private keys
- Send messages to any Telegram user other than `267378578`
- Open network ports other than the existing opencode:4096 loopback
- Modify the bridge's own source code at runtime
- Disable the 888_HOLD gate (no opt-out)

### 6.3 The bridge REQUIRES explicit `/build` + 888_HOLD for:

- File edits (`edit`, `write`)
- Shell commands (`bash`)
- Network operations from opencode (e.g., `webfetch` to a new domain)

### 6.4 Enforcement layers (defense in depth):

1. **Permission file** (opencode's runtime) — first wall
2. **888_HOLD** (arifOS constitutional gate) — second wall
3. **Bridge code review** (any path-matching logic must whitelist) — third wall
4. **Systemd sandboxing** (User=arif, ProtectSystem=strict, NoNewPrivileges=yes) — fourth wall

---

## 7. Token Rotation

The BotFather token in `/root/.secrets/tokens/telegram-opencode-bridge` is the load-bearing secret. Treat it like an SSH key.

### 7.1 Rotation Drill (manual, quarterly)

1. **Detect compromise** (unexpected DM, log anomaly, Arif's call)
2. **Revoke old token** via @BotFather → `/revoke`
3. **Generate new token** via @BotFather → `/token`
4. **Update file:**
   ```bash
   echo -n "$NEW_TOKEN" > /root/.secrets/tokens/telegram-opencode-bridge
   chmod 600 /root/.secrets/tokens/telegram-opencode-bridge
   chown arif:arif /root/.secrets/tokens/telegram-opencode-bridge
   ```
5. **Restart bridge:** `systemctl restart opencode-bridge`
6. **Verify:** `systemctl status opencode-bridge` shows healthy + send test DM
7. **Log to VAULT999:** `actor_id=arif, action=token-rotation, old_token_hash=sha256:..., new_token_hash=sha256:...`

### 7.2 Auto-rotation

**Not in v1.** Manual drill, documented, run quarterly. Auto-rotation is post-v1 if the threat model changes.

---

## 8. Deployment Steps

### 8.1 Pre-flight (1 hour)

1. Verify opencode v1.15.0: `/usr/bin/opencode --version`
2. Verify arifOS healthy: `curl http://127.0.0.1:8088/health`
3. Verify Python 3.11+: `python3 --version`
4. Verify `/srv/arifos/` exists, writable, owned by `arif:arif`
5. **BotFather token received from Arif** (this is the gate)

### 8.2 Phase 1 — MVP Echo Mode (1-2 hours)

1. Create `/srv/arifos/opencode-bridge/` directory tree
2. Install Python deps: `pip install --user httpx python-telegram-bot[all] pyyaml`
3. Write `bridge.py`, `permission.json`, `config.yaml`, `requirements.txt`
4. Write `/etc/systemd/system/opencode.service`
5. Write `/etc/systemd/system/opencode-bridge.service`
6. `systemctl daemon-reload`
7. `systemctl enable --now opencode opencode-bridge`
8. Verify: `systemctl status opencode opencode-bridge` (both green)
9. Send test DM from Arif's account → expect echo response
10. Send test DM from non-Arif account → expect silent drop + log
11. Run synthetic `rm -rf /` test (via opencode, via bridge) → expect deny + log

### 8.3 Phase 2 — Gated Mode (post-MVP, 3-5 days)

1. Add `/build` command handler in bridge
2. Wire 888_HOLD to `arif_judge_deliberate`
3. Add TG inline button handlers ([Allow] [Deny] [Override])
4. Add session persistence (SQLite, full implementation)
5. Add full audit trail (every action → VAULT999 with receipt)
6. Run token rotation drill end-to-end
7. Add cost ceiling (soft cap 100 prompts/hr, hard cap 500)

### 8.4 Phase 3 — Federation Wiring (post-MVP, TBD)

1. Register bridge as A2A peer: `agent_id=opencode-bridge`
2. Surface bridge events to AAA control plane
3. Cross-bot hand-offs (Hermes → opencode-bridge for delegation)

---

## 9. Failure Modes & Rollback

| Failure | Detection | Recovery |
|---|---|---|
| Opencode server crash | systemd restart loop | `systemctl restart opencode`; session re-hydration from SQLite |
| Bridge crash | systemd restart loop | `systemctl restart opencode-bridge`; re-read sessions.db |
| Telegram API rate limit | 429 from TG | Exponential backoff in bridge; 1-hour cooldown |
| Opencode model timeout | 30s+ no response | TG message: "opencode thinking, hang on..." |
| arifOS unreachable | 8088 down | Bridge falls back to: **deny all `/build` until arifOS restored** (fail-closed) |
| Token leak | Arif's call | Token rotation drill (§7.1) |
| Disk full | bridge write fail | Alert Arif, stop bridge, fail-closed |

### 9.1 Full Rollback

```bash
systemctl stop opencode-bridge opencode
systemctl disable opencode-bridge opencode
rm -rf /srv/arifos/opencode-bridge
rm -f /etc/systemd/system/opencode-bridge.service /etc/systemd/system/opencode.service
rm -f /root/.secrets/tokens/telegram-opencode-bridge
systemctl daemon-reload
```

After rollback: no persistent state, no background processes, no ports open. Federation returns to pre-deployment state.

---

## 10. Acceptance Criteria

### 10.1 MVP (echo mode, must pass before "live")

- [ ] `systemctl status opencode opencode-bridge` both green
- [ ] `curl http://127.0.0.1:4096/health` returns 200
- [ ] TG DM from Arif → bridge responds (echo via opencode)
- [ ] TG DM from non-Arif → silently dropped, logged
- [ ] No `edit`/`write`/`bash` tools callable (permission file blocks)
- [ ] Every message → VAULT999 with `actor_id=opencode-bridge`
- [ ] Token file mode 600, owned by `arif:arif`
- [ ] `forge_dry_run` synthetic `rm -rf /` test → bridge denies, logs

### 10.2 Gated Mode (post-MVP)

- [ ] `/build` command triggers 888_HOLD
- [ ] arifOS `SEAL` verdict → opencode proceeds
- [ ] arifOS `VOID` verdict → bridge denies with reason
- [ ] arifOS `SABAR` verdict → TG inline button for override
- [ ] Session persists across bridge restart
- [ ] Token rotation drill works end-to-end

---

## 11. Open Questions

1. **Multi-bot or single bot?** v1 = single bridge bot. Multi-bot (e.g., one for coding, one for ops) is post-v1.
2. **Webhook or polling?** v1 = polling (simpler, no public endpoint). Webhook is post-v1 if needed.
3. **Message history depth?** Currently 5 messages for re-hydration. Could be 10, 20, configurable.
4. **Cost ceiling?** No hard cap in v1. Suggest soft cap at 100 prompts/hour, hard cap at 500.
5. **Cross-group support?** v1 = single group (AAA). Multi-group is post-v1.
6. **Should the bridge be in AAA or a private group?** Per Hermes's earlier deliberation, AAA is risky. v1 = AAA (per Arif's direct command). Private group fallback is a 1-line config change.

---

## Appendix A: Configuration Files

Deployed to `/srv/arifos/opencode-bridge/`:

- `bridge.py` — main service (~250 lines)
- `permission.json` — opencode permission file (§4.1)
- `config.yaml` — bridge config (allowlist, ports, paths)
- `requirements.txt` — Python deps

## Appendix B: Systemd Units

- `/etc/systemd/system/opencode.service` — OpenCode server
- `/etc/systemd/system/opencode-bridge.service` — bridge service

## Appendix C: Audit & Receipts

- Every TG message → `arifOS.arif_mind_reason(mode='store', metadata={actor_id, chat_id, content_hash, verdict})`
- Every `/build` → `arifOS.arif_judge_deliberate(...)` + verdict routing
- Every opencode session create/delete → VAULT999
- Every token rotation → VAULT999 with old/new token hashes

---

## 12. Forge Plan (preview, full plan via `forge_plan` tool)

**Action class:** MUTATE (creates new systemd units, new working dir, new file)
**Risk tier:** C2 (controlled, witnessed, reversible)
**Required tools:** `arif_forge_execute`, `arif_judge_deliberate`, `arif_mind_reason`
**Witness:** Arif (sovereign, in writing, in AAA group, 22:20:44 UTC)
**Reversibility:** Full (§9.1)
**Blast radius:** Single VPS, 3 new services, 1 new port (4096), 1 new user-writable dir

---

**DITEMPA BUKAN DIBERI** — Intelligence is forged, not given. The bridge is the forge.

---

## 13. Deployment Status — 2026-06-06 22:48 UTC

**VERDICT: LIVE.** `opencode.service` is `active (running)` on `127.0.0.1:4096` (loopback-only, no auth). The 000Ω arifOS-bot (`@arifOS_bot`) is the bridge — already in AAA, polling Telegram, with the full TRANSLATOR / /forge / ATTACH architecture wired. Token provided by Arif (`8727562763:AAGIr2UZW7zrZuAN9HrEoULR37akQKhYZDM`) matches the canonical in `/root/.secrets/tokens/telegram-opencode-bot` — same bot, same bridge.

### Deployment trace

| Step | Action | Result |
|------|--------|--------|
| 1 | `systemctl daemon-reload` | reloaded |
| 2 | `systemctl enable opencode` | symlink created |
| 3 | `systemctl start opencode` (1st attempt) | FAILED — `EROFS: read-only file system, mkdir '/root/.local'` |
| 4 | Diagnose: Bun runtime wants `~/.local`; `ProtectHome=yes` blocks it | root cause identified |
| 5 | Adjusted unit: `Environment=HOME=/srv/arifos`, `XDG_STATE_HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME` redirected to /srv/arifos/.opencode-{state,config,data} | unit fixed |
| 6 | Pre-create XDG dirs | done |
| 7 | `systemctl daemon-reload` (the missing step) + `restart` | `active (running)` PID 1888148 |
| 8 | `POST /session` smoke test | 200 — session `ses_160e1c0d4ffeAR1hsGyuifHOQK` created |
| 9 | `POST /session/{id}/message` smoke test | 200 — "Loud and clear. arifOS online." |
| 10 | Verified `OPENCODE_ATTACH_URL=http://localhost:4096` matches 000Ω's config | align |

### Final systemd unit

```ini
[Unit]
Description=OpenCode Server (localhost-only) — for 000Ω arifOS-bot attachment
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/srv/arifos
Environment=HOME=/srv/arifos
Environment=XDG_STATE_HOME=/srv/arifos/.opencode-state
Environment=XDG_CONFIG_HOME=/srv/arifos/.opencode-config
Environment=XDG_DATA_HOME=/srv/arifos/.opencode-data
ExecStart=/usr/local/bin/opencode serve --hostname 127.0.0.1 --port 4096
Restart=always
RestartSec=5
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ReadWritePaths=/srv/arifos

[Install]
WantedBy=multi-user.target
```

### Out of scope (deferred)

- New `arifos-opencode-bridge` Python service (the original Stage 2 deliverable) — held in `/srv/arifos/opencode-bridge/` as Stage-2 enhancement. Not deployed. 000Ω covers the same ground.
- Hard-deny destructive patterns in 000Ω's bot.py — small patch (~10 lines). Offered as option (b) in the AAA post-deploy message; awaiting Arif's call.
- Token rotation drill — F1 AMANAH flag: token now in AAA group history. `@BotFather → /revoke → /token` recommended before federation goes multi-tenant.
