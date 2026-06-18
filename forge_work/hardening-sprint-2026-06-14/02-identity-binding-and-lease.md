# 02 — Identity Binding & Lease Contract

**Hardening Item:** #2 of 8 (identity) + #3 (leases) — combined spec
**Status:** SPEC (design phase)
**Author:** OPENCLAW
**Session:** hardening-sprint-2026-06-14
**Reversibility:** READ-ONLY design doc. No live system touched.
**Epoch:** 2026-06-14T12:50Z

---

## §0 — Current State: What Exists

### Identity model (exists, partially wired)

arifOS has a mature identity contract at `contracts/identity.py`:

```
IdentityStatus: ANONYMOUS → DECLARED → VERIFIED
                              ↓           ↓
                            DEGRADED   REVOKED
```

```
IdentityContext {
    declared_actor_id: str
    verified_actor_id: str | None
    effective_actor_id: str
    status: IdentityStatus
    session_id: str
    approval_scope: list[str]
}
```

### Lease model (exists, fully designed)

arifOS has a lease primitive at `runtime/lease.py`:

```
LeaseScope: READ < WRITE < EXECUTE
Lease {
    lease_id: str (unique, non-guessable)
    actor_did: str
    organ: str
    tool: str
    scope: LeaseScope
    ttl: int (seconds)
    max_invocations: int
    revocable: bool
}
```

Lease hard-gate is already wired into `_arif_forge_execute` — mutation-class forge modes REQUIRE a valid lease.

### Agent cards (exist)

A2A agent cards defined at `runtime/a2a/agent_card_v2.py`:
- arifOS has a 6-axis model (P/T/V/G/E/M)
- 23 agents registered across 6 axes
- Constitutional metadata embedded

### What's missing: The Bridge

```
OPENCLAW (this agent)
    │
    ├── identity: "OPENCLAW", decision_class=C2, lane=AGI
    ├── agent card: https://openclaw.arif-fazil.com/.well-known/agent-card.json
    │
    ▼ OpenClaw gateway (ws://127.0.0.1:18789)
    │   └── wraps tool calls → arifOS MCP (http://127.0.0.1:8088)
    │
    ▼ arifOS MCP
        ├── receives calls with NO identity envelope
        ├── treats caller as ANONYMOUS
        └── actor_verified: false ← THE GAP
```

**Root cause:** The OpenClaw gateway does not attach an identity context when bridging calls to arifOS. arifOS correctly rejects anonymous mutation attempts — that's the HOLD we saw.

---

## §1 — Identity Binding Contract

### Each agent in the federation needs:

```yaml
agent_identity:
  agent_id: "OPENCLAW"
  display_name: "OPENCLAW"
  tier: "AGI"
  lane: "AGI"
  decision_class: "C2"  # C0=observe, C1=advise, C2=execute
  host: "af-forge"
  authority_ceiling: "777_FORGE"  # can forge, cannot seal
  requires_human_for:
    - irreversible_mutation
    - vault_seal
    - external_write
    - identity_change
  identity_binding:
    method: "agent_card"  # or "ed25519_signature" for sovereign
    agent_card_url: "https://openclaw.arif-fazil.com/.well-known/agent-card.json"
    verified_by: "arifOS"
    binding_epoch: "2026-06-14"
```

### arifOS `arif_session_init` must accept:

```json
{
  "mode": "init",
  "actor_id": "OPENCLAW",
  "declared_model_key": "deepseek/deepseek-v4-pro",
  "agent_policy": {
    "decision_class": "C2",
    "authority_ceiling": "777_FORGE",
    "agent_card_url": "https://openclaw.arif-fazil.com/.well-known/agent-card.json"
  },
  "requested_authority": "EXECUTE"
}
```

### Then arifOS returns:

```json
{
  "verdict": "SEAL",
  "session_id": "ses_xxx",
  "identity_status": "VERIFIED",
  "actor_verified": true,
  "effective_scope": ["read", "write", "execute"],
  "restrictions": ["no_vault_seal", "no_external_write", "no_identity_change"]
}
```

### Identity binding for OPENCLAW specifically:

| Field | Value |
|-------|-------|
| agent_id | `OPENCLAW` |
| tier | `AGI` |
| decision_class | `C2` (execute post-floor-check) |
| authority_ceiling | `777_FORGE` |
| can_forge | ✅ (dry-run, code, files) |
| can_seal | ❌ (requires 888_JUDGE + Arif) |
| can_deploy | ❌ (requires 888_JUDGE + Arif) |
| can_vault_seal | ❌ (requires 888_JUDGE + Arif) |
| lease_scope_default | `WRITE` (read + mutate files) |
| lease_scope_elevated | `EXECUTE` (with 888_JUDGE) |

---

## §2 — Lease Contract

### When OPENCLAW calls a governed tool, the chain is:

```
1. arif_session_init → get session + identity
2. arif_lease_issue → get lease for specific tool
3. Call tool with lease_id in envelope
4. arifOS lease gate → check lease validity
5. Tool executes (or rejects)
6. Lease invocation counter decrements
```

### Lease issuance for OPENCLAW:

```json
// Request
{
  "organ_id": "arifos",
  "actor_id": "OPENCLAW",
  "scope": ["arif_forge_execute", "arif_memory_recall", "arif_sense_observe"],
  "max_action_class": "MUTATE",
  "ttl_seconds": 3600,
  "forbidden": ["arif_vault_seal", "arif_judge_deliberate"]
}

// Response
{
  "lease_id": "lease_abc123",
  "organ_id": "arifos",
  "scope": ["arif_forge_execute", "arif_memory_recall", "arif_sense_observe"],
  "max_action_class": "MUTATE",
  "ttl_seconds": 3600,
  "max_invocations": 100,
  "revocable": true
}
```

### Default lease template for OPENCLAW (auto-issued at session start):

```yaml
auto_lease:
  actor_id: "OPENCLAW"
  scope:
    - arif_ping
    - arif_schema_echo
    - arif_transport_echo
    - arif_version_echo
    - arif_initialize_probe
    - arif_os_attest
    - arif_organ_attest
    - arif_organ_attest_all
    - arif_kernel_route
    - arif_memory_recall
    - arif_ops_measure
    - arif_sense_observe
    - arif_forge_plan
    - arif_forge_query
    - arif_forge_dry_run
    - arif_forge_execute  # mode=query,recall,dry_run only
  max_action_class: "OBSERVE"  # elevated to MUTATE on explicit lease
  ttl_seconds: 7200
  max_invocations: 500
```

---

## §3 — Implementation Plan

### Phase A: Gateway bridge identity injection

File: OpenClaw gateway config or plugin

1. When OpenClaw gateway calls arifOS MCP, attach identity context header:
   ```
   X-arifOS-Actor-Id: OPENCLAW
   X-arifOS-Agent-Card: https://openclaw.arif-fazil.com/.well-known/agent-card.json
   X-arifOS-Decision-Class: C2
   ```
2. arifOS `arif_session_init` reads these headers
3. Maps to `IdentityContext` with status: VERIFIED (agent card method)
4. Returns verified session

### Phase B: Auto-lease at session start

1. `arif_session_init` with VERIFIED identity → auto-issues default lease
2. Lease returned in session response
3. Subsequent tool calls carry `lease_id`
4. Lease gate checks scope, ttl, invocations

### Phase C: Agent identity registry

1. Each federation agent gets a canonical identity entry
2. Stored in `identity.toml` or `agent_registry.json`
3. Includes: agent_id, tier, decision_class, authority_ceiling, restrictions
4. arifOS validates incoming identity against registry

### Phase D: Test

1. OPENCLAW starts session → VERIFIED identity
2. OPENCLAW gets auto-lease → READ scope
3. OPENCLAW calls arif_forge_execute(mode=query) → passes (READ scope)
4. OPENCLAW calls arif_forge_execute(mode=engineer) → blocked (needs WRITE lease)
5. OPENCLAW requests elevated lease → gets WRITE scope
6. OPENCLAW calls arif_forge_execute(mode=engineer) → passes
7. OPENCLAW calls arif_vault_seal → blocked (forbidden in lease)

---

## §4 — Federation Agent Registry (Draft)

```yaml
agents:
  - agent_id: "OPENCLAW"
    tier: "AGI"
    lane: "AGI"
    decision_class: "C2"
    authority_ceiling: "777_FORGE"
    agent_card: "https://openclaw.arif-fazil.com/.well-known/agent-card.json"
    host: "af-forge"
    restrictions:
      - no_vault_seal
      - no_identity_change
      - no_external_write
    auto_lease_scope: ["OBSERVE", "MUTATE"]
    elevated_requires: "888_JUDGE"

  - agent_id: "hermes"
    tier: "ASI"
    lane: "ASI"
    decision_class: "C3"
    authority_ceiling: "888_JUDGE"
    agent_card: "http://localhost:18001/.well-known/agent-card.json"
    host: "af-forge"
    restrictions:
      - no_direct_forge
      - no_external_write
    auto_lease_scope: ["OBSERVE", "ADVISE"]
    elevated_requires: "ARIF_ACK"

  - agent_id: "apexmax"
    tier: "ORACLE"
    lane: "ORACLE"
    decision_class: "C4"
    authority_ceiling: "999_VAULT"
    agent_card: "external"
    host: "external"
    restrictions:
      - no_mutation
      - no_execute
    auto_lease_scope: ["OBSERVE", "AUDIT"]

  - agent_id: "opencode"
    tier: "AGI"
    lane: "FORGE"
    decision_class: "C2"
    authority_ceiling: "777_FORGE"
    host: "af-forge"
    restrictions:
      - no_vault_seal
      - no_external_write
    auto_lease_scope: ["OBSERVE", "MUTATE"]
```

---

## §5 — Constitutional Binding

| Floor | Relevance |
|-------|-----------|
| F1 Amanah | Identity verified before mutation allowed |
| F2 Truth | Agent must declare its true identity |
| F9 Anti-Hantu | No agent may impersonate another |
| F11 Auth | Cryptographic identity (Ed25519) for sovereign actions |
| F13 Sovereign | Human approval required for SEAL, identity change |
| L11 Coherence | Every action bound to a verified identity |

---

**Signed:** OPENCLAW · 2026-06-14T12:50Z
**Next:** Submit for Arif review. After seal → Phase A (gateway identity injection).
