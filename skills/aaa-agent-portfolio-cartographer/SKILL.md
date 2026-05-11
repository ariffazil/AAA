# aaa-agent-portfolio-cartographer

## Metadata

- **Name:** aaa-agent-portfolio-cartographer
- **Skill Home:** `/root/AAA/skills/aaa-agent-portfolio-cartographer/SKILL.md`
- **Type:** BODY / AAA control-plane / registry-adjacent
- **Pipeline Position:** Runs after `aaa-agent-registrar` (identity known); before `arifos-constitutional-clerk` for purely architectural questions.
- **Activation:** On-demand (query-driven), not autonomous.

---

## Purpose

Maintain a live, queryable map of the federation portfolio:
- Agents (local + external coders + auditors)
- Federation organs (arifOS, GEOX, WEALTH, WELL, AAA, A-FORGE)
- Their tier (Constitutional / ASI / AGI / BODY)
- Risk profile
- Network coordinates (ports, URLs, Tailscale reachability)

Must NOT:
- Approve execution
- Change routing
- Override arifOS or A-FORGE
- Trigger automatic 888_HOLD on drift

---

## Epistemic Tags

| Tag | Meaning |
|-----|---------|
| **CLAIM** | Process/socket/endpoint confirmed alive via probe |
| **PLAUSIBLE** | Declared in config/AAA map but currently unreachable |
| **HYPOTHESIS** | Proposed by Hermes/OpenClaw, not yet confirmed live |

Tag rules:
- Do NOT emit 888_HOLD on passive health drift
- Downgrade to PLAUSIBLE rather than failing
- Log all transitions to `memory/YYYY-MM-DD.md`

---

## Probe Chain

### Phase 1: Docker containers
```
docker ps --format "{{.Names}}\t{{.Status}}"
```
All federation nodes should appear here.

### Phase 2: Listening ports (network surfaces)
```
ss -tlnp 2>/dev/null || netstat -tlnp
```
Identifies exposed network surfaces.

### Phase 3: Health endpoints (per node)
```bash
curl -s --max-time 3 http://localhost:8080/health   # arifOS
curl -s --max-time 3 http://localhost:8081/health   # GEOX
curl -s --max-time 3 http://localhost:8082/health   # WEALTH
curl -s --max-time 3 http://localhost:8083/health   # WELL
curl -s --max-time 3 http://localhost:3001/health   # AAA
curl -s --max-time 3 http://localhost:7071/health   # A-FORGE
```

### Phase 4: OpenClaw gateway
```
openclaw health --json
```

### Phase 5: Tailscale (remote reachability)
```
tailscale status 2>/dev/null
```

---

## Output Schema

```json
{
  "portfolio_id": "aaa-portfolio-map-v1",
  "generated_at": "ISO8601",
  "epistemic_band": "CLAIM|PLAUSIBLE|HYPOTHESIS",
  "nodes": [
    {
      "name": "arifOS",
      "type": "federation-organ",
      "tier": "Constitutional",
      "port": 8080,
      "health_endpoint": "/health",
      "status": "CLAIM|PLAUSIBLE|HYPOTHESIS",
      "last_seen": "ISO8601",
      "exposure": "localhost|tailscale|public",
      "risk_band": "CRITICAL|HIGH|MEDIUM|LOW",
      "notes": "string"
    }
  ],
  "agents": [
    {
      "name": "Hermes",
      "type": "agent",
      "tier": "ASI",
      "home": "local",
      "health_source": "process|docker|none",
      "status": "CLAIM|PLAUSIBLE|HYPOTHESIS",
      "last_seen": "ISO8601",
      "risk_band": "LOW|MEDIUM|HIGH"
    }
  ],
  "summary": {
    "total_nodes": 6,
    "total_agents": 14,
    "claim_count": N,
    "plausible_count": N,
    "hypothesis_count": N,
    "drift_detected": true|false
  }
}
```

---

## Markdown Output Format

```
# AAA Portfolio Cartographer

**Generated:** YYYY-MM-DD HH:mm UTC  
**Epistemic Band:** CLAIM | PLAUSIBLE | HYPOTHESIS  

## Federation Nodes

| Node | Port | Status | Tier | Risk | Last Seen |
|------|------|--------|------|------|-----------|
| arifOS | 8080 | CLAIM | Constitutional | CRITICAL | ... |
...

## Agents

| Agent | Tier | Home | Status | Risk |
|-------|------|------|--------|------|
...
```

---

## Boundaries

- Belongs in **AAA**, not arifOS or A-FORGE
- Activates only after `aaa-agent-registrar` verifies identity
- For any request that changes state → hand off to `arifos-constitutional-clerk` → `aforge-metabolic-operator`
- Cartographer **never** approves or executes

---

## Telemetry

- Log every run to `memory/YYYY-MM-DD.md`
- Log all PLAUSIBLE → CLAIM or CLAIM → PLAUSIBLE transitions with timestamp
- Log drift events separately from routine probes

---

## Skill Invocation

Triggered when Arif or a federation agent asks:
- "Which agents can touch arifOS?"
- "Which ports are part of the constitutional federation?"
- "Which agents run under root on VPS?"
- "Show me the live portfolio map"
- Any variation of portfolio / map / nodes / agents / health / status