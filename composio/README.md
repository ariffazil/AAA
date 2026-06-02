# arifOS × Composio — Embodiment in AAA

**Ratified:** 2026-06-02 · **Authority:** 888 (Arif bin Fazil, F13 SOVEREIGN) · **Seal:** AAA-COMPOSIO-EMBODIMENT-2026-06-02

---

## What this is

AAA is the canonical **tool-orchestration surface** for the arifOS federation. Organs (GEOX, WEALTH, WELL, A-FORGE) and PENTAGON agents (333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE) call external SaaS through AAA, not directly through Composio.

The actual execution layer lives in HERMES (`/root/HERMES/scripts/composio_bridge.py`, Python) under "Path B" — Google Workspace access. This AAA module is the **governance surface** that wraps it: tool registry, per-organ policy, write gate, audit doctrine.

```
Organ / PENTAGON agent
          ↓
       AAA (this module)
       ├── registry.json   — what toolkits/accounts exist
       ├── policy.yaml     — per-organ + per-agent read/write scope
       ├── service.ts      — gate logic (F1-F13, VAULT999)
       └── README.md       — this context doc
          ↓
   HERMES composio_bridge.py (Path B execution)
          ↓
     Composio API → OAuth'd SaaS
```

---

## Three layers of tool

### 1. Personal reach (sovereign OAuth `pg-test-...`)

Broad read across 6 personal SaaS, all bound to the sovereign's OAuth identity.

| Toolkit | Account | Status | Default scope |
|---|---|---|---|
| Gmail | `ca_4W804Z2adkIv` | Active | read-only |
| Google Drive | `ca_ygnSTDy1imSv` | Active | read-only |
| YouTube | `ca_dfufcQtLR5n8` | Active | read-only |
| Reddit | `ca_CWe4H0pLdH33` | Active | read-only |
| Google Maps | `ca_iKCW5yws-43B` | Active | read-only |
| LinkedIn | `ca_6YXfnZgo5dRz` | Active | read-only |

**Write posture:** All writes BLOCKED until VAULT999 chain is repaired. LinkedIn write would additionally require F1 + F13 + SALAM ack triple-gate (sovereign identity is reputation-loaded).

### 2. Workspace (per-organ Supabase)

Workspace DBs, one per organ (when organ mapping locks).

| Account | Status | Intended organ |
|---|---|---|
| `ca_ikoeG8G6Tr1c` | Active | TBD (WEALTH / A-FORGE / AAA) |
| `ca_o17l0FiTnRf2` | Initializing | TBD |
| `ca_Zxyuw3OnJ6TW` | Initializing | TBD |

**Write posture:** Writes are per-organ F1 + F13 + VAULT999 pre-SEAL gated. Reads are F2/F3 evidence layer.

### 3. Compute (capability tools)

| Tool | Auth | Status | Floor |
|---|---|---|---|
| PerplexityAI | API Key | No account yet | F9 anti-hallucination — citation receipt per claim |

Perplexity is read-only by nature (search + citations). No write verbs.

---

## Constitutional gate

### Read calls

```
organ/agent → AAA → policy_check (toolkit in caller's scope)
            → composio_bridge.execute → audit_log
```

- **Preconditions:** agent identity verified, toolkit in caller scope
- **Floor:** F2 (truth) + F3 (evidence receipt)
- **VAULT999:** not required (reads are not irreversible)

### Write calls (BLOCKED until VAULT999 chain repaired)

```
organ/agent → AAA → 333-AGI draft → 555-ASI critique
            → 888-APEX arbitrate (F1-F13) → VAULT999 pre-SEAL
            → 000-SALAM ack (if destructive)
            → composio_bridge.execute → VAULT999 post-SEAL
            → audit_log
```

- **Preconditions:** VAULT999 CONNECTED, F1 + F13 passed, SALAM ack if destructive
- **Blocked when:** VAULT999 BROKEN
- **Fallback:** 000-SALAM_MANUAL_ACK — Arif must ack each write verb in chat

---

## Phase status

| Phase | Status | Notes |
|---|---|---|
| 1. Read-only reach | **ACTIVE** | 6 personal toolkits connected, all read-only |
| 2. Per-organ sessions | PENDING | 1/3 Supabase accounts Active; 2 Initializing |
| 3. Trigger bus | PENDING | Needs AAA webhook endpoint + event router |
| 4. Governed writes | **BLOCKED** | VAULT999 chain repair (120 gaps, last seal #80) |
| 5. BYO OAuth | PENDING | Needs GCP redirect URI for `gen-lang-client-0385068353` |

The single hard block on the entire forward path is **VAULT999 chain repair**. Until that's resolved, AAA's writes policy is constitutional theatre — no write can be SEALed even if approved.

---

## How organs use this

### Listing available tools

```ts
import registry from './composio/registry.json';

const myTools = registry.personal_reach_layer.auth_configs; // or workspace/compute
```

### Checking policy

```ts
import policy from './composio/policy.yaml';

const myPolicy = policy.organs.WEALTH; // per-organ scope
const isAllowed = myPolicy.intended_tools.includes('supabase');
```

### Calling a tool (read)

```ts
// Future: AAA-side TypeScript gate
const result = await composioGateway.call({
  caller: 'WEALTH',
  toolkit: 'supabase',
  action: 'SUPABASE_LIST_TABLES',
  arguments: { schema: 'public' },
  mode: 'read',
});
```

### Calling a tool (write)

```ts
// BLOCKED until VAULT999 chain is repaired
// Will require: 333-AGI draft → 555-ASI critique → 888-APEX arbitrate
//              → VAULT999 pre-SEAL → 000-SALAM ack → execute
```

---

## How to extend

To add a new toolkit:

1. **Connect in Composio dashboard** (or via API). Note the `auth_config_id` and `connected_account`.
2. **Add to `registry.json`** under the appropriate layer (personal / workspace / compute).
3. **Add per-organ `intended_tools` entries** in `policy.yaml`.
4. **If write-capable:** add to dangerous action list in HERMES `composio_bridge.py`.
5. **Update this README's** "Three layers" table.
6. **Commit on current AAA branch; await sovereign push approval.**

---

## Files in this module

| File | Purpose |
|---|---|
| `registry.json` | Auth config + account mapping (machine-readable, source of truth) |
| `policy.yaml` | Per-organ + per-agent policy (human-readable governance) |
| `README.md` | This context doc + integration architecture |

---

## What this is NOT

- **Not a replacement for HERMES composio_bridge.py.** That's still the execution layer. This is the AAA-side governance surface.
- **Not an enforcement mechanism.** AAA can refuse to forward calls, but the actual policy enforcement is in HERMES bridge + (future) AAA service.ts.
- **Not a secret store.** API keys, OAuth tokens, and other secrets live in `/root/.secrets/`, not here.

---

## Cross-references

- HERMES bridge: `/root/HERMES/scripts/composio_bridge.py`
- HERMES policy (runtime): `/root/HERMES/config/agent_policies/composio.yaml`
- HERMES audit log: `/root/HERMES/audit/composio_bridge.jsonl`
- VAULT999 state: `/root/arifOS/VAULT999/state.json` (BROKEN as of 2026-06-02)
- Composio dashboard: https://app.composio.dev

---

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
