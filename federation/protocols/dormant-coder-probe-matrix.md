# Dormant Coder Probe Matrix — Pre-Activation Inventory

> **CCC-T-08 (2026-09-18)** — closes GAP-08 without adding blocks
> **Status:** PROBE MATRIX — observation only, zero capability change

## Why this exists

GAP-08 framed "dormant agents unbound on activation" as a missing gate. Per `representation-reality-invariant.md`, the correct fix is **probe-before-panic**, not a new gate. This matrix is the inventory sweep required before any dormant coder is activated.

## Sovereign decisions (2026-09-18)

Per Phase 4 CCC-T-23..25 decisions:

| Coder | Status | Activation scope |
|---|---|---|
| **Aider** (FI-006) | DORMANT → ACTIVE | housekeeping only (README, doc SOT, entropy, deploy) |
| **Qwen Code** (FI-003) | DORMANT → ACTIVE | builder/verifier, FED-routed GLM |
| **Antigravity** (FI-009 agy) | **DEFERRED Q1 2027** | no activation this quarter |

+++ claude-code, copilot, copilot-cli, continue-cli, kvm4-ccc-pool, grok-build remain dormant contract members, no activation pending.

## Probe matrix (per coder, before ACTIVATE)

For each dormant coder, this probe must PASS before activation:

```yaml
coder: <name>
probe_date: <ISO-8601 UTC>
probe_by: <333-AGI or sovereign-direct>

# 1. Binary presence
binary_present: <yes|no>          # `which <binary>` returns path
binary_version: <string>          # `<binary> --version`

# 2. Config presence
config_home: <path>               # e.g. /root/.codex
config_present: <yes|no>
config_keys: <list>                # major keys found

# 3. A2A card presence
a2a_card_path: <path>              # e.g. /root/AAA/a2a-server/agent-cards/harnesses/codex.json
a2a_card_schemaVersion: <string>   # current 2.3.0
a2a_card_authority: <string>       # ceiling from card
a2a_card_url: <string>             # https://aaa.arif-fazil.com/a2a/<id>

# 4. Hook presence (per harness type)
hook_paths: <list>                 # hook script paths found
hook_emits_envelope: <yes|no>      # has FederationEnvelope v0.1 emit

# 5. MCP presence
mcp_servers_count: <int>           # from `[mcp_servers.*]` in config
mcp_servers_list: <list>           # server names

# 6. Authorization ceiling
authority_ceiling: <string>        # OBSERVE_ONLY | DRAFT_ONLY | EXECUTE_REVERSIBLE | EXECUTE_AFTER_SEAL
authority_ceiling_source: <string> # where this is declared

# 7. Receipt path
receipt_path: <path>               # where gate receipts go

# 8. Data authority check (CCC-03)
ccc_03_injected_in_agents_md: <yes|no>

# Probe verdict
verdict: PASS | FAIL
verdict_reason: <text>
next_action: <proceed-to-canary | remain-dormant | remediation-needed>
```

## Pre-activation ritual

When sovereign says "activate <coder>":

1. Run probe matrix — collect YAML output
2. Save probe YAML to `/root/AAA/federation/probes/<coder>-<date>.yaml`
3. If verdict = PASS → canary phase (7 days, observed, read-only or limited scope)
4. If verdict = FAIL → block activation; emit scar; route to remediation
5. After 7-day canary with no scar → promote to ACTIVE
6. Update `agent-card.json` with `status: ATTESTED` + `attestation_id`

## What this does NOT do

- ❌ Does not auto-activate
- ❌ Does not require F13 sign-off (per F13-directive activation)
- ❌ Does not block tools citizens already have

## What this DOES do

- ✅ Inventory sweep before activation (probe-before-panic doctrine)
- ✅ Audit trail of activation state per coder
- ✅ Comparison capability (compare probe YAML to canonical schema)

## Verdict

GAP-08 closes via **inventory probe**, not enforcement. ΔS impact: −0.2 (single schema, reusable per coder). Citizen capability: UNCHANGED. Anti-patterns avoided: drift in dormant coder metadata; phantom absence claims like "no hook" when hook exists at alt path.

> **DITEMPA BUKAN DIBERI ⚒️**
> **Path:** `/root/AAA/federation/protocols/dormant-coder-probe-matrix.md`
> **Status:** PROBE MATRIX — observation only
