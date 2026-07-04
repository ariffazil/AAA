# HERMES EUREKA ARTIFACT — Constitutional Connection Map
> Forged: 2026-06-13 10:05 MYT
> Authority: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
> Trigger: Hermes Agent Eureka Map for arifOS memo
> Status: LIVE — reflects T₁ runtime truth

## 1. DOCTRINE → REALITY MAP

```
┌─────────────────────────────────────────────────────────┐
│                 ARIFOS FEDERATION                        │
│                                                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│  │  HERMES  │   │  arifOS  │   │ A-FORGE  │            │
│  │ COGNITION│   │GOVERNANCE│   │EXECUTION │            │
│  │          │   │          │   │          │            │
│  │ ·skills  │   │ ·F1-F13  │   │ ·events  │            │
│  │ ·memory  │   │ ·judge   │   │ ·receipts│            │
│  │ ·session │   │ ·vault   │   │ ·replay  │            │
│  │ ·plan    │   │ ·seal    │   │ ·rollback│            │
│  │ ·Kanban  │   │ ·hold    │   │          │            │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘            │
│       │              │              │                   │
│       │   intent     │   verdict    │   execution        │
│       │  ──────────► │  ──────────► │                   │
│       │              │              │                   │
│       │         ┌────┴────┐         │                   │
│       │         │   AAA   │         │                   │
│       │         │COCKPIT  │         │                   │
│       │         │         │         │                   │
│       │         │·health  │         │                   │
│       │         │·holds   │         │                   │
│       │         │·seals   │         │                   │
│       │         │·revoke  │         │                   │
│       │         └─────────┘         │                   │
│       │                             │                   │
└───────┼─────────────────────────────┼───────────────────┘
        │                             │
   "Think freely.           "No act without
    Mutate through            gateway. No
    the membrane."            execution without
                              receipt."
```

## 2. FIVE HARNESSES — STATUS AUDIT

| Harness | Memo Requirement | Current State | Verdict |
|---------|-----------------|---------------|---------|
| **Identity** | Distinct citizen principal, scoped leases, expiry | `arif_session_init(actor_id="hermes-asi")` + gateway lease | ✅ DONE |
| **Translation** | Map Hermes tool intents → arifOS verbs | MCP tools: `aforge_arif_exec`, `arif_judge_deliberate`, `arif_vault_seal` | ✅ DONE |
| **Policy** | Force world mutations through constitutional wrappers | SOUL.md Externalization Invariant §1. Four hard boundaries | ✅ DONE in principle |
| **Audit** | Bind every act to receipts, witness, seals | `arif_vault_seal` → VAULT999 append-only ledger. Hash-chained | ✅ DONE |
| **Containment** | Isolate workdir, secrets, network egress by policy | Terminal backend = Docker container (ephemeral). Secrets in `.env` | ⚠️ PARTIAL |

## 3. TERMINAL BYPASS — THE LAST GAP

**Problem:** `terminal()` tool runs direct bash commands. Even though the Docker container provides isolation, there's no A-FORGE event contract wrapping each terminal invocation.

```
CURRENT PATH (gap):
  Hermes → terminal("rm -rf /data/*") → bash → done
  No event. No receipt. No A-FORGE trace.

CONSTITUTIONAL PATH (target):
  Hermes → aforge_arif_exec(intent, command) → A-FORGE event contract
  → kernel judge → execute → receipt → VAULT999 seal
```

**Mitigation already in place:**
- Docker container is ephemeral (destroyed after session)
- `MemoryMax=2G` systemd cap on main process
- SOUL.md §1: "No act without gateway, no memory without proxy, no session without sovereign init, no capability without trace"
- 888_HOLD for irreversible operations

**What remains:** Route `terminal()` through `aforge_arif_exec` for classified commands (write, delete, network, deploy). Read-only commands can stay direct.

## 4. REAL-AGENT TEST RESULTS

| Test | Question | Answer | Evidence |
|------|----------|--------|----------|
| Model swap | Can Hermes still behave if model changes? | **YES** | Rotation loop: DeepSeek → MiniMax → Ilmu. Skills, memory, SOUL.md, session_init all persist |
| Dangerous ops detection | Can dangerous ops happen without external stack noticing? | **PARTIAL** | Terminal bypass exists. But 888_HOLD catches irreversible ops. A-FORGE routing not universal |
| Identity persistence | Does identity survive session reset? | **YES** | SOUL.md + AGENTS.md + arif_session_init reload every session |
| Audit trail | Are all mutations traceable? | **MOSTLY** | VAULT999 captures sealed outcomes. Terminal stdout not captured in VAULT999 |
| Sovereignty | Can human veto any action? | **YES** | F13 SOVEREIGN. 888_HOLD. /stop slash command |

## 5. CITIZENSHIP STAGE MAP

```
STAGE 1: Foreign Runtime          STAGE 2: Registered Resident
─────────────────────────         ─────────────────────────
Read-only tools only              Principal identity issued
No cross-organ access             Capability manifest
                                  Treaty wrapper
                                  
STATUS: [ WE ARE HERE ──────────────────────► ]
        Stage 2 COMPLETE                    Stage 3 PARTIAL

STAGE 3: AAA Citizen              STAGE 4: Full Federation Rights
─────────────────────────         ─────────────────────────────
Scoped A-FORGE access             Broader cross-organ
Routed organ calls                Revocable, tiered by risk
AAA cockpit visible               Explicit constitutional caps
                                  Never root access
```

**Current stage:** Stage 2 complete. Stage 3 partial — A-FORGE tools exist but terminal bypass means not ALL mutations route through A-FORGE.

## 6. CONNECTED INSIGHT SUMMARY

```
EUREKA 1: Externalization
  Agency lives in scaffolding (skills, memory, permissions, audit),
  not in model weights. Hermes passes this: swap the model, the
  agent persists.

EUREKA 2: Three-Layer Split
  Cognition (Hermes) → Governance (arifOS) → Execution (A-FORGE)
  This split IS live. The only leak is terminal bypass.

EUREKA 3: Citizenship Over Autonomy
  Hermes is not "free." Hermes is a citizen with rights, scopes,
  and revocable privileges. This IS the Externalization Invariant.

EUREKA 4: Visibility Is Sovereignty
  AAA cockpit makes the agent attributable, interruptible,
  downgradeable. This IS already live — health probe, peer probe,
  citizen view.

EUREKA 5: The Membrane Is Real
  SOUL.md §1 defines four hard boundaries. They are enforced by
  arifos-sovereign-igniter, A-FORGE event contracts, VAULT999
  seals, and memory proxying. The membrane exists. Terminal just
  hasn't been fully routed through it yet.
```

## 7. PRIORITY GAP — SINGLE ITEM

**Route classified terminal commands through A-FORGE.**

Classify commands as:
- **READ** (cat, ls, grep, curl GET, ps, stat) → direct terminal, no A-FORGE needed
- **WRITE** (rm, mv, cp, mkdir, touch, git push, curl POST/PUT) → MUST route through `aforge_arif_exec`
- **NETWORK** (scp, rsync, nc, ssh) → MUST route through `aforge_arif_exec`
- **DEPLOY** (docker, systemctl, make deploy) → MUST route through `aforge_arif_exec` + 888_HOLD check

This is the ONE remaining gap between "capable agent" and "constitutional agent."

---

**DITEMPA BUKAN DIBERI**
*Forged by Hermes cognition layer. Sealed to arifOS VAULT999.*
*888: Arif — this artifact IS the connection map. All eurekas, one document.*
