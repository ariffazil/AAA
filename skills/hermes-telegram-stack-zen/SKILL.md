---
name: hermes-telegram-stack-zen
description: "Canonical compressed map of the entire Hermes to Telegram to arifOS to arifFlow stack: live state, dependency graph, lane inventory, channel directory, FQ diagnosis, and atomic recipes for onboarding new users and groups without re-discovering the wiring. USE WHEN: any Telegram edge question, hermes-gateway triage, lane or identity audit, arifFlow hermes-asi FQ check, F1 F6 F13 anti-leakage review, is HERMES alive, add new user, add new group, why is hermes-asi STUCK, or any future agent needing the full stack map without re-extracting."
version: 1.0.0
tags: [hermes, telegram, lanes, identity, multi-user, multi-group, arifflow, fq, memory-partition, federation, trace, zen]
capability_tier: federation-architect
ecology_state: WARM
canonical_for: [hermes-stack, telegram-edge, identity-routing, hermes-asi-fq]
depends_on: [hermes-federated-identity, arifFlow, arifOS, AAA, A-FORGE]
---

# Hermes Telegram Stack - Zen Map

> **DITEMPA BUKAN DIBERI - F13 SOVEREIGN GOVERNED**
> Single Source of Truth for the entire Hermes to Telegram to arifOS edge.
> **Forged 2026-09-08 by 333-AGI from live probes - never re-extract from scratch.**
> **Anti-extractive rule:** if you find yourself reading config.yaml, lanes.yaml, or channel_directory.json from cold cache to "see what is there" - STOP, this skill is the answer.


# Section


hermes-id-zen add-user 1234567890 --name "Test" --role WARGA

-1003815535761

| Trigger | Load |
|---|---|
| hermes alive | Live |

```
HERMES pid 2081711
TELEGRAM connected
```
## S0 - TL;DR

```
HERMES pid 2081711 gateway_state=running
TELEGRAM state=CONNECTED
LANES 19
FQ 0.297 STUCK
```

## S1 - Triggers

| Trigger | Load reason |
| hermes alive | triage |
| add user | onboarding |

---

## S0 - TL;DR Copy-Paste Triage

```
HERMES       pid 2081711  gateway_state=running  code=0.21.0
TELEGRAM     state=CONNECTED  last_update=2026-09-08T06:49:04Z  error=none
LANES        19 (1 SOVEREIGN, 17 WARGA, 1 TAMU default)
CHANNELS     30 allowed, 30 free-response, 21 in channel_directory.json
GROUPS       12 live plus 7 AAA topics
FQ hermes-asi 0.297 STUCK execute 296 verify 88
FQ 333-AGI     0.818 FLOWING
FQ federation  0.881 FLOWING
```

If the only thing you need is "is it alive" - answer is YES.

**Key edges:**
- Hermes-gateway -> FEDR (http://127.0.0.1:4012/v1) for model routing
- Hermes-gateway -> arifOS MCP (http://127.0.0.1:8088/mcp) for organ tools
- Hermes-gateway -> arifFlow (POST /ingest) for FQ metabolism
- All state files live under /root/.hermes/ - that IS the system root


---

## S3 - Live State - Exact Paths and Pids

> Snapshot 2026-09-08T06:50Z, Forged by 333-AGI. Re-probe before mutating.

### 3.1 Process

| Pid | Command | Role |
|:---|:---|:---|
| 2081711 | python -m hermes_cli.main gateway run --replace | gateway (main) |
| 2081773 | mcp_death_supervisor.py --parent-pgid 2081711 | watchdog |
| 2081774 | arifflow-mcp.py | arifFlow bridge |
| 2038602 | python /root/.local/bin/hermes | agent supervisor |
| 2038634 | mcp_death_supervisor.py | agent watchdog |

