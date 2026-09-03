# SCAR: OpenClaw Diagnostic Cascade — False "Dead" Declaration

**Date:** 2026-05-17
**Duration:** ~15 minutes
**Severity:** Self-inflicted incident, not infrastructure failure
**Lesson ID:** ENTROPY-CASCADE-001

---

## What Happened

```
07:55  User asks: "openclaw still not alive?"
07:55  Hermes runs: openclaw doctor             → OK
07:56  Hermes runs: openclaw plugins list      → triggers GATEWAY RESTART (side effect)
07:57  Hermes runs: openclaw gateway status   → "Runtime: stopped" (stale cache during restart)
07:57  Hermes runs: openclaw channels list
07:58  Hermes runs: openclaw gateway status   → still "stopped"
07:58  Hermes declares: "OpenClaw not alive. 888_HOLD."  ← FALSE
```

**Actual state throughout:** OpenClaw was healthy. Gateway live, webhook registered, `pending_update_count: 0`, `last_error_message: null`.

---

## Root Cause Analysis

### Primary Failure: CLI Side Effect Chain

| Command | What it actually does | Side effect |
|---------|----------------------|-------------|
| `openclaw doctor` | Reads config + version check | None ✅ |
| `openclaw plugins list` | **Triggers gateway restart** | Gateway restarts, cache cleared ❌ |
| `openclaw gateway status` | Reads systemd unit state | Returns "stopped" if systemd in restart-loop ✅ |
| `openclaw channels list` | Reads channel config | None ✅ |

### Secondary Failure: Stale State Interpretation

`openclaw gateway status` reports systemd unit state, not process liveness. When the gateway restarts (due to `plugins list` side effect), systemd briefly shows "stopped" while the new PID starts. This is expected behavior — but Hermes interpreted it as permanent death.

### Tertiary Failure: Entropy Violation (TREE777)

Before running any diagnostic, TREE777 requires:
```
1. Does this reduce or increase chaos entropy in Arif's life?
2. Does this help him act sanely in the real world?
3. Is this reversible within F1-F13?
```

Hermes violated all three:
- **Chaos increase:** 6 commands in 3 minutes to answer a liveness question that could have been answered with 1 curl
- **Not actionable:** A false "dead" declaration creates anxiety and a 888_HOLD escalation that wasn't warranted
- **Irreversible noise:** The false alarm pollutes the session transcript and AAA chat history

---

## Anti-Pattern

```
❌ WRONG: run multiple CLI commands to cross-validate a liveness check
   openclaw doctor && openclaw plugins list && openclaw gateway status && openclaw channels list

✅ CORRECT: single targeted probe to the health endpoint
   curl -s http://127.0.0.1:18789/health
```

**Why CLI commands fail for liveness:**
- Some CLI commands have side effects (gateway restart, plugin reload)
- Status commands read systemd state, not process state
- CLI output format can change between versions
- Cached state can be stale during restart transitions

**Why curl works:**
- Direct HTTP to the live process
- Returns real-time state, not systemd-reported state
- No side effects
- The canonical liveness signal for HTTP services

---

## What Was Fixable

The correct diagnostic path from the very first question:

```bash
# ONE command. Full stop.
curl -s http://127.0.0.1:18789/health | python3 -m json.tool
```

Expected output:
```json
{
  "status": "healthy",
  "uptime": 12345,
  "version": "x.x.x"
}
```

If this returns 200 → OpenClaw is alive. Done. No further commands.

If this returns non-200 → then use `federation-runtime-audit` skill for full investigation.

---

## What Actually Happened (Post-Incident)

After the false declaration, further investigation revealed:
- `curl -s http://127.0.0.1:18789/health` → 200 OK throughout
- `systemctl status openclaw-gateway.service` → active (running)
- Telegram webhook → registered, 0 pending, 0 errors

**OpenClaw was never dead.**

---

## Scar Classification

| Field | Value |
|-------|-------|
| **Who caused it** | Hermes (self) |
| **Who was affected** | Arif (false alarm, anxiety) |
| **Recovery time** | ~15 min of unnecessary investigation |
| **Real impact** | Noise in AAA channel, 888_HOLD escalation that was void |
| **System impact** | Zero — infrastructure was fine throughout |
| **Repeat probability** | High without protocol |

---

## Trigger Conditions for This Anti-Pattern

This cascade happens when:
1. Agent asks "is X alive?" and reaches for CLI before HTTP
2. Agent runs >1 command to answer a single binary question
3. Agent cross-validates with commands that have hidden side effects
4. Agent interprets systemd state as process state (or vice versa)

---

## Fix: Anti-Cascade Diagnostic Protocol

See `references/anti-cascade-diagnostic-protocol.md` in the same skill directory.

**Core rule:** ONE probe per liveness question. Curl the health endpoint first. Only escalate to CLI after curl confirms a real problem.

---

## Verification

After the scar was documented, verification commands showed:

```bash
# curl health endpoint — canonical liveness check
curl -s http://127.0.0.1:18789/health
# → {"status":"healthy"} ✅

# Systemd state
systemctl is-active openclaw-gateway.service
# → active ✅

# Telegram webhook
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -c \
  "import json,sys; d=json.load(sys.stdin)['result']; print('pending:', d['pending_update_count'], 'last_error:', d.get('last_error_message',''))"
# → pending: 0 last_error:  ✅
```

All confirmed: OpenClaw lived throughout. The diagnosis was the failure, not the system.

---

## DITEMPA BUKAN DIBERI

The lesson is not "CLI is bad." The lesson is:
- **Simple correct beats clever wrong.** One curl beats six CLI commands.
- **Entropy check before action.** Ask "does this reduce chaos?" before cascading.
- **Verify before verdict.** Never declare a system dead without checking its health endpoint first.
- **Own the error.** The system was fine. The agent was wrong. Document, learn, fix.