# Tool Health Checker — OpenClaw Skill

## Purpose
Smoke-test critical MCP tools across all organs. Reports PASS/FAIL/UNTESTABLE per tool. Runnable as daily cron or manual command.

## Usage
```bash
python3 /root/.openclaw/workspace/skills/tool-health-check/tool_health_check.py
```

## What It Tests

### arifOS OBSERVE tools (9 smoke-tested)
- `arif_os_attest` — kernel self-attestation
- `arif_ops_measure` — system vitals
- `arif_heartbeat` — organ liveness
- `arif_organ_attest_all` — cross-organ attestation
- `arif_observe` — vitals observation
- `arif_memory_recall` — memory search
- `gateway_health` — gateway liveness
- `gateway_receipts` — audit receipt listing
- `gateway_lease_inspect` — lease inspection

### arifOS UNTESTABLE tools (6 — require full session)
- `arif_init`, `arif_lease_issue`, `arif_judge`, `arif_seal`, `arif_forge_execute`, `arif_gateway_connect`

### Organ tools (3 smoke-tested)
- `GEOX: geox_system_registry_status`
- `WEALTH: wealth_system_registry_status`
- `WELL: well_system_registry_status`

### Infrastructure probes (4)
- NATS connectivity
- A-FORGE /health
- arifOS /health
- AAA gateway /health

## Live Result (2026-06-14 06:55 UTC)
- **Summary**: OK
- **Pass**: 16/22
- **Fail**: 0/22
- **Untestable**: 6/22
- **Duration**: 6,950ms
- **Slowest**: arif_memory_recall (3892ms), arifOS /health (1582ms), arif_ops_measure (975ms)

## Cron Integration
```bash
# Daily at 04:00 MYT (20:00 UTC)
0 20 * * * python3 /root/.openclaw/workspace/skills/tool-health-check/tool_health_check.py >> /var/log/openclaw/tool_health.log 2>&1
```

## Reversibility
Read-only. No mutations. Safe to run anytime.
