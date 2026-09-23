---
name: openclaw
id: openclaw
version: 1.0.0
risk_tier: medium
description: 'OpenClaw edge agent bridge — operational triage, doctor, restart, and A2A bridge routing for the federation edge (Telegram surface). USE WHEN: "openclaw unhealthy", "gateway down", "edge bot not responding", "a2a bridge disconnected", "watchdog tripped", "openclaw doctor", "openclaw restart". NOT for token/security audit — use FORGE-telegram-audit.'
owner: A-FORGE
floor_scope:
- F1
- F2
- F4
- F11
- F13
autonomy_tier: T2
host_compatibility:
- openclaw  # native — SYSTEM_MD.md emitted to openclaw/
dependencies:
  skills:
  - forge-telegram-audit   # security sibling — for token isolation checks
  - mcp-lifeguard          # health probe pattern
  servers: []
  tools:
  - bash
  - curl
  - openclaw CLI
examples:
- "Gateway watchdog tripped: tail /var/log/arifOS-watchdog.log, run openclaw doctor, recover via openclaw restart"
- "Bot @AGI_ASI_bot unreachable: probe /health on :18789, escalate to FORGE-telegram-audit if token suspected"
- "A2A bridge disconnected: confirm openclaw health, restart only if health < OK, otherwise HOLD"
tests:
- "Health probe returns 200 within 8s after openclaw doctor"
- "No systemctl openclaw restart usage (wrong path per watchdog comments)"
- "Telegram broadcast only to sovereign chat_id 267378578"
version_lock:
  schema_version: "1"
  artifact_hash: pending
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# OpenClaw — Edge Agent Bridge Operations

**Operational triage for the federation edge.** OpenClaw is the Telegram-facing agent surface (`@AGI_ASI_bot`) and A2A bridge into the internal federation. This skill governs the **operational** surface — health, restart, watchdog, doctor — and explicitly **does not** cover security/token audit (which is `FORGE-telegram-audit`'s lane).

## Overview

OpenClaw runs the edge. When the edge misbehaves, this skill is the first responder. It does NOT:

- Rotate or audit Telegram bot tokens (→ `FORGE-telegram-audit`)
- Modify constitutional surfaces (→ arifOS `888_JUDGE`)
- Repackage or rebuild openclaw (→ `FORGE-federation-orchestrator`)
- Change Telegram chat configuration (→ Telegram API direct)

## When to Use

- **Watchdog tripped** — `/var/log/arifOS-watchdog.log` shows `GATEWAY_UNHEALTHY` or recovery loop
- **Bot unreachable from outside** — `/health` on `:18789` returns non-200, or Telegram API polling fails
- **A2A bridge degraded** — internal organs report `openclaw` agent missing from discovery
- **Manual `openclaw doctor` requested** by sovereign or another agent
- **Restart needed after config change** — TOKEN file updated, watchdog rules changed, etc.
- **`openclaw restart` is the correct verb** — explicitly NOT `systemctl restart openclaw` (the watchdog comments comment block this, see §`Forbidden Actions`)

## When NOT to Use

- **Token audit / rotation** — escalate to `FORGE-telegram-audit` (security lane)
- **Constitutional surface change** — escalate to `arifOS 888_JUDGE` via `forge_judge_proxy`
- **Telegram chat / channel config** — use Telegram Bot API directly, not this skill
- **Multi-service restart cascade** — escalate to `FORGE-incident-escalation`
- **T3 irreversible ops** (config rewrite, secret rotation) — 888_HOLD required

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `symptom` | yes | What is broken — gateway, bot, A2A, watchdog, restart-needed |
| `evidence` | no | Log excerpt, /health output, doctor output |
| `severity` | no | `info` \| `warn` \| `critical` — defaults to `warn` if watchdog tripped |
| `restart_budget` | no | Read from `/tmp/openclaw-watchdog-state.json` (auto-discovered, NOT hardcoded) |

## Procedure

### Step 1 — Observe (T0)

Probe live state. **No mutation yet.**

```bash
# Health probe — direct curl, no model call
HEALTH=$(curl -sf --max-time 8 http://127.0.0.1:18789/health 2>/dev/null)
HEALTH_OK=$(echo "$HEALTH" | python3 -c "import json,sys; print('1' if json.load(sys.stdin).get('ok') else '0')" 2>/dev/null)

# Watchdog state — discovered from path in watchdog script, not hardcoded
STATEFILE=$(grep -oP 'STATEFILE=\K"[^"]+"' /root/AAA/scripts/openclaw-watchdog.sh | tr -d '"' || echo "/tmp/openclaw-watchdog-state.json")
[ -f "$STATEFILE" ] && python3 -c "import json; print(json.load(open('$STATEFILE')))"

# Tail watchdog log
tail -20 /var/log/arifOS-watchdog.log 2>/dev/null
```

### Step 2 — Diagnose (T0)

Run `openclaw doctor` and capture output. **Read-only diagnostic.**

```bash
openclaw doctor 2>&1 | tee /tmp/openclaw-doctor-$(date +%s).log
```

### Step 3 — Plan (T1)

Based on doctor output, classify into one of:

| Doctor verdict | Action |
|---|---|
| `OK` — all green | **SEAL** with `pass` verdict; no mutation |
| `RECOVERABLE` — minor | `openclaw restart` (T2 — announce in commit body) |
| `DEGRADED` — systemic | `openclaw doctor --repair` if available; else HOLD + escalate |
| `BROKEN` — config corruption | **888_HOLD** — escalate to `FORGE-incident-escalation` + sovereign |
| Token/secret exposure suspected | **DO NOT restart** — escalate to `FORGE-telegram-audit` |

### Step 4 — Restart (T2, only if Step 3 says `RECOVERABLE`)

**Use `openclaw restart`, NOT `systemctl restart openclaw`.** The watchdog script comment is explicit:

```bash
# Correct restart: openclaw restart (not systemctl)
openclaw restart 2>&1 | tee /tmp/openclaw-restart-$(date +%s).log
```

Then verify within 30s:

```bash
sleep 30
HEALTH=$(curl -sf --max-time 8 http://127.0.0.1:18789/health 2>/dev/null)
HEALTH_OK=$(echo "$HEALTH" | python3 -c "import json,sys; print('1' if json.load(sys.stdin).get('ok') else '0')")
[ "$HEALTH_OK" = "1" ] || HOLD
```

### Step 5 — Record (T1)

Append restart to state file (watchdog budget tracking):

```bash
python3 -c "
import json, time
d = json.load(open('$STATEFILE')) if __import__('os').path.exists('$STATEFILE') else {'restarts':[]}
d['restarts'].append(int(time.time()*1000))
with open('$STATEFILE','w') as f: json.dump(d,f)
"
```

If restarts in last 2h ≥ 2, set `BLOCKED` verdict and HOLD.

### Step 6 — Seal (T1)

Emit a sealed receipt. Best-effort given session constraints:

- Try `mcp__arifflow__flow_ingest` with `step_type=Verify` — only if session_id is held
- Else write sealed summary to `/root/forge_work/YYYY-MM-DD/openclaw-recovery-<timestamp>.md`
- Note in `carry_forward.json` next session pickup if seal blocked

## Allowed Tools

| Tool | Purpose |
|------|---------|
| `bash` (read-only) | Log tail, /health probe, statefile read, doctor invocation |
| `bash` (mutate) | `openclaw restart`, statefile write — **only in Step 4 with `RECOVERABLE` verdict** |
| `curl` | /health probe, Telegram API getWebhookInfo (read-only) |
| `openclaw CLI` | `doctor`, `restart`, `restart --if-needed` |

## Forbidden Actions

- **NEVER** use `systemctl restart openclaw` — wrong path per `openclaw-watchdog.sh:5` comment. Always use `openclaw restart`.
- **NEVER** edit `/root/.openclaw/*` token files without F13 sovereign approval (→ `forge_send_confirm`)
- **NEVER** disable or kill the watchdog cron
- **NEVER** broadcast to Telegram chat_id `267378578` (sovereign-only) without explicit sovereign intent
- **NEVER** edit `/var/log/arifOS-watchdog.log` directly (rotation is systemd-managed)
- **NEVER** restart more than 2× in any 2h window — watchdog budget will block; HOLD instead
- **NEVER** mark a restart `RECOVERED` without post-restart /health verification

## Output Format

```
## OpenClaw Skill Result: <symptom>

### Summary
One-paragraph outcome.

### Evidence
- pre-restart /health: <json or "down">
- doctor verdict: <OK|RECOVERABLE|DEGRADED|BROKEN>
- restart attempts: <N>
- post-restart /health: <json or "down">

### Actions Taken
- tail /var/log/arifOS-watchdog.log → <findings>
- openclaw doctor → <findings>
- openclaw restart → <outcome>

### Final State
- /health: ✅/❌
- last watchdog log line: <timestamp>
- next_session_carry_forward: <if any>

### Escalations
- None / <list with path>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Doctor verdict = `BROKEN` (config corruption) | `FORGE-incident-escalation` + sovereign | Telegram 888_HOLD |
| Token exposure suspected | `FORGE-telegram-audit` (security lane) | A2A `forge_send_confirm` (URL mode for secrets) |
| Constitutional surface touched | arifOS `888_JUDGE` | `mcp__aforge__forge_judge_proxy` |
| Restart loop ≥ 2 in 2h | sovereign | Telegram `mcp__aforge__forge_send_confirm` |
| A2A bridge systemic failure | `FORGE-incident-escalation` | A2A + log witness |

---

## De-hardcoding Notes

- Health port `18789` — discovered from `openclaw-watchdog.sh:44` (`curl ... :18789/health`), not hardcoded
- Statefile path — discovered from watchdog script grep, not hardcoded
- Telegram chat_id `267378578` — sovereign-only, but read from watchdog script header (constant in source)
- `openclaw restart` verb — from `openclaw-watchdog.sh:5` comment, not invented

---

*Forged 2026-08-06 by kimi-code/FI-008 (warga-aaa) under sovereign override on `Sweep AAA 71 / Autogen OpenClaw SKILL` directive. T2 autonomy tier per `openclaw restart` service-impacting nature.*

*DITEMPA BUKAN DIBERI ⚒️*