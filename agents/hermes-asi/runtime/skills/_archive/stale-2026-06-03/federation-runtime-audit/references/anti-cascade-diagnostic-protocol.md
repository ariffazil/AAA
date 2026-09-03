# Anti-Cascade Diagnostic Protocol

**Skill class:** federation-runtime-audit
**Supersedes:** unconstrained CLI cascading for liveness checks
**Born from:** `references/scar-openclaw-diagnostic-cascade-2026-05-17.md`

---

## The Problem

When an agent asks "is X alive?", the instinctive response is to run a chain of CLI commands to cross-validate. This pattern is dangerous:

1. **Some CLI commands have hidden side effects** — `openclaw plugins list` restarts the gateway; `openclaw gateway stop` can leave orphan PIDs.
2. **Status commands often read systemd state, not process state** — systemd can show "stopped" during a restart transition even when the process is healthy.
3. **Cascading N commands to answer a binary question = N× chance of misinterpretation** — each command introduces a new failure mode.
4. **Each extra command is entropy** — it adds noise, potential side effects, and cognitive load for no diagnostic value.

**Result:** The diagnostic creates the very failure it was trying to detect.

---

## The Entropy Check (TREE777)

Before running **any** diagnostic command, ask:

```
Q1: Does this reduce or increase chaos entropy in Arif's life?
Q2: Does this help him act sanely in the real world?
Q3: Am I about to run more than one command to answer a single liveness question?
Q4: Is this action reversible within F1-F13?
```

| Answer to Q1 | Answer to Q3 | Action |
|-------------|--------------|--------|
| Reduce | No | Proceed with single probe |
| Reduce | Yes | **STOP.** One probe only. Cascade violated. |
| Increase | No | Log only. No alert. |
| Increase | Yes | **STOP.** Log and stay silent. |

**Default to silence when uncertain.** A false alarm is worse than no signal.

---

## The Single Probe Rule

```
ONE curl to the health endpoint
→ If 200: system is alive. DONE. No more commands.
→ If non-200: use federation-runtime-audit skill for full investigation.
```

### Canonical Liveness Probes (arifOS Federation)

| Service | Probe | Success = Alive |
|---------|-------|----------------|
| OpenClaw gateway | `curl -s http://127.0.0.1:18789/health` | HTTP 200 |
| OpenClaw Telegram | `curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo"` | `pending_update_count: 0` |
| arifOS MCP | `curl -s http://127.0.0.1:8080/mcp` | JSON with tool_count |
| WEALTH MCP | `curl -s http://127.0.0.1:8082/mcp` | JSON response |
| GEOX MCP | `curl -s http://127.0.0.1:8081/mcp` | JSON response |
| WELL MCP | `curl -s http://127.0.0.1:8083/mcp` | JSON response |
| Hermes A2A | `curl -s http://127.0.0.1:18001/health` or port check | Port open |
| PostgreSQL | `pg_isready -h 127.0.0.1 -p 5432` | exit 0 |
| Redis | `redis-cli -h 127.0.0.1 -p 6379 ping` | PONG |

**For OpenClaw specifically:**
```bash
# BEST — direct HTTP liveness (no side effects)
curl -s http://127.0.0.1:18789/health

# ACCEPTABLE — systemd state (safe, no side effect)
systemctl is-active openclaw-gateway.service

# FORBIDDEN for liveness — has side effects
openclaw plugins list      # ⚠️ RESTARTS gateway
openclaw gateway stop      # ⚠️ may leave orphan PID
openclaw gateway start     # ⚠️ conflict if already running
```

---

## When CLI Is Justified (Post-curl)

Only escalate to CLI commands **after** curl confirms a real problem:

### Confirmed dead → Full Diagnostic Path

```
1. curl <health_endpoint>           → non-200 or timeout → CONFIRMED DEAD
2. systemctl status <service>      → why dead (crash, OOM, config error)
3. journalctl -u <service> --no-pager -n 30  → recent logs
4. docker ps -a | grep <name>       → container state (if containerized)
5. docker logs <container> --tail 30 → container logs
```

**Rule:** Each command must answer a **new specific question** about the failure, not re-confirm liveness.

### Examples of valid multi-command follow-up:

- "Why did it die?" → `journalctl -u openclaw-gateway --no-pager -n 50 | grep -E "(error|fatal|exception)"`
- "Is it a port conflict?" → `ss -tulpn | grep <port>`
- "Is Docker container restarting?" → `docker ps -a | grep <name>` then `docker inspect <name> --format '{{.State.Restarting}}'`

---

## OpenClaw-Specific Notes

OpenClaw CLI commands to **avoid** for liveness checks:

| Command | Why Forbidden | Side Effect |
|---------|--------------|-------------|
| `openclaw plugins list` | Triggers gateway restart | Gateway bounces |
| `openclaw gateway stop` | Stops the gateway | Orphan PID possible |
| `openclaw gateway start` | Starts gateway | Fails if already running (409) |
| `openclaw gateway status` | Reads systemd state, not process state | Stale during restart transitions |

Safe OpenClaw commands:
| Command | Purpose |
|---------|---------|
| `systemctl is-active openclaw-gateway.service` | Systemd alive check |
| `ss -tulpn \| grep 18789` | Port binding check |
| `journalctl -u openclaw-gateway --no-pager -n 20` | Recent logs (after curl confirms dead) |

---

## Protocol Summary

```
BEFORE any diagnostic command:
  └── Entropy check (Q1-Q4)
      └── If increase or cascade risk → STOP. Log only.

FOR LIVENESS:
  └── ONE curl to health endpoint
      ├── 200 → System alive. DONE.
      └── non-200 → Confirmed dead. Full diagnostic path.

FOR DEBUGGING (after curl confirms dead):
  └── Each CLI command must answer a new specific question.
      └── State what you're checking BEFORE running.
      └── Never re-confirm liveness with a new command.
```

---

## Cross-Check Rule

If two agents are investigating the same system simultaneously:
- **Agent A** runs curl → confirms alive → DONE
- **Agent B** runs curl → confirms alive → DONE

Do **not** have both agents run CLI cascades. One confirmation is enough.

If you see another agent running >3 CLI commands for a single liveness question, signal via AAA: `"Single probe sufficient. curl confirmed alive at <timestamp>."`

---

## Integration with TREE777

This protocol IS the TREE777 implementation for diagnostic actions:

- **Entropy first** → One probe, not five
- **Reversible first** → curl has no side effects; CLI can have side effects
- **Truth band ≥99%** → curl returns live state at the instant of the call; CLI state can be stale
- **Maruah** → False alarms cause anxiety; a simple "alive" confirmation is respectful of Arif's attention

---

## When to Override

Single-probe rule may be skipped only when:
1. The health endpoint is known to be broken/unreachable (can't use it to check itself)
2. The question is not "is it alive?" but "why did it die?" — then CLI is appropriate
3. Comparative state needed: "did X change since Y?" — requires two probes with timestamps

Even in override cases: **state the override reason before running the first command.**