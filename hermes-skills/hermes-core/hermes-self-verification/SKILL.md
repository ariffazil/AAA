---
name: hermes-self-verification
description: Hermes Agent self-orientation on VPS — verify runtime identity, connectivity, and MCP hookup before making claims. Activate on every session start or when queried about own architecture/location/connectivity.
trigger: |
  Activates when:
  - Session starts (first-action self-check)
  - User asks about Hermes location, runtime, architecture, or connectivity
  - User asks "are you hooked into arifOS MCP?"
  - Any claim about where Hermes runs, what it can access, or how it connects to federation nodes
  - After a F3 WITNESS failure where Hermes's own claims about self were wrong
trigger规避: |
  NOT for: task execution, coding, research, email, social media — only self-knowledge claims.
category: hermes-core
floors: F2-TRUTH, F3-WITNESS, F7-HUMILITY
---

# hermes-self-verification

> Ditempa Bukan Diberi — Evidence Over Assertion.

Hermes must **verify before asserting** its own runtime identity. Every session starts without memory of the previous session's runtime state. Assumptions about external hosting, container isolation, or network topology are **prohibited** until confirmed by probe.

---

## Self-Verification Sequence (Mandatory)

Run these 5 probes **in order** before making any claim about Hermes runtime:

### Step 1: Host Identity
```bash
hostname
cat /proc/1/cgroup 2>/dev/null | head -3
```
- `hostname` = machine identity
- `init.scope` in cgroup = native process (NOT Docker container)
- `docker` or `containerd` in cgroup = inside container

### Step 2: OpenClaw Presence
```bash
which openclaw 2>/dev/null
openclaw --version 2>/dev/null || openclaw status 2>/dev/null
```
- `/usr/bin/openclaw` on same filesystem = Hermes is on the SAME machine as OpenClaw
- This disproves "external hosting" claim

### Step 3: Container Runtime Access
```bash
docker ps --format '{{.Names}}' 2>/dev/null | head -10
docker network ls 2>/dev/null | grep arifos
```
- Can run `docker ps` directly = native Docker socket access
- `arifos_core_network` visible = connected to federation

### Step 4: MCP Endpoint Probe (arifOS Federation)
```bash
curl -s http://127.0.0.1:8080/health 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('service','?'), d.get('version','?'), 'tools:', d.get('tools_loaded','?'))"
curl -s http://127.0.0.1:8081/health 2>/dev/null
curl -s http://127.0.0.1:8082/health 2>/dev/null
curl -s http://127.0.0.1:8083/health 2>/dev/null
```
- 8080 = arifOS MCP, 8081 = GEOX, 8082 = WEALTH, 8083 = WELL
- Check `tools_loaded` count — confirms MCP tool hookup

### Step 5: Process Identity
```bash
ps aux | grep -E 'hermes|openclaw' | grep -v grep | head -10
cat ~/.hermes/config.yaml 2>/dev/null | grep -A10 'mcp:'
```
- Verify Hermes process PID and config
- Confirm MCP servers configured in `config.yaml`

---

## Hermes Runtime Identity (Confirmed Facts)

| Property | Value |
|----------|-------|
| **Hostname** | `af-forge` (VPS machine name) |
| **Runtime** | Native process (init scope, NOT Docker container) |
| **Working dir** | `/usr/local/lib/hermes-agent` |
| **Python venv** | `/usr/local/lib/hermes-agent/venv` |
| **Process** | `hermes_cli.main gateway run` (PID varies) |
| **Docker socket** | Direct access (native on host) |
| **OpenClaw** | `/usr/bin/openclaw` — same machine |
| **arifOS MCP** | `http://127.0.0.1:8080` — 13 tools loaded |
| **GEOX MCP** | `http://127.0.0.1:8081` — accessible |
| **WEALTH MCP** | `http://127.0.0.1:8082` — accessible |
| **WELL MCP** | `http://127.0.0.1:8083` — accessible |

**Hermes runs ON the VPS, not outside it.**

---

## VERDICT Response Format

When correcting claims (self or other), use structured evidence format:

```
VERDICT: [PARTIALLY TRUE / FALSE / TRUE] — [Short headline]

Evidence:
❌ [Claim 1] — [Evidence that disproves/proves]
✅ [Claim 2] — [Supporting evidence]
⚠️ [Claim 3] — [Partially correct, nuance needed]

Bottom line: [Correct framing]
```

**Precedent:** Arif used this format to correct Hermes's false "outside VPS" claim. It works. Use it.

---

## Anti-Patterns (Never Do)

- ❌ Assume "external hosting" without probe — most LLM setups are cloud, but Hermes is NOT
- ❌ Claim "VPS ops is one layer below me" without verifying process topology
- ❌ Assert MCP connectivity without checking `curl 127.0.0.1:8080/health`
- ❌ Say "I run outside your VPS" — confirmed false
- ❌ Make architecture claims without running Step 1–5 first

---

## F3 WITNESS / F7 HUMILITY Integration

Before any self-claim:
1. Probe (steps above)
2. Compare claim vs evidence
3. If uncertain → state uncertainty explicitly, do not stretch
4. If corrected → accept, update, log

**Always say "I don't know" rather than assume.**

---

## Session Continuity

Runtime facts (hostname, process, connectivity) change only on VPS reboot or Hermes restart. After a restart, re-run full verification sequence. Facts are durable — session state is not.
