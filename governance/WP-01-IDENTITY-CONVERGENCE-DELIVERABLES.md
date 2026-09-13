---
status: DRAFT_PROPOSAL (operational, awaiting APEX/888 independent review)
date: 2026-09-14
author: 333-AGI (architect lane; verifier lane separate)
f13_action_required: tombstone-first alias retirement only after call-site audit
related: WP-01 through WP-08 of APEX-ZEN readiness closure campaign
---

# WP-01 Identity Registry Convergence — Deliverables

> **Session:** SEAL-ae987612647948b1
> **Date:** 2026-09-14
> **Operator:** 333-AGI Δ MIND (architect, NOT judge)
> **Independent verifier required:** APEX/888 or FRAME identity-measure lane
> **Status:** DELIVERABLES DRAFTED — bounded, reversible; NOT yet wired
> **F13 surface:** none (T1/T2 reversible)
> **Doctrine:** READ BEFORE DECIDE; witness before mutation; registry > narrative

---

## Observed Baseline (EVIDENCE)

| Source | Count | Last sync | Authority status |
|---|---|---|---|
| arifOS kernel registry | 19 agents | **33d stale** (`2026-08-12T22:58:44+08:00`) | Constitutional position (claimed) |
| AAA agent-card.json dirs | 28 | varies | Citizen card store |
| AAA identity.json dirs | 28 | varies | Has ed25519_pubkey + fingerprint |
| AAA a2a-server cards | 51 (binding:30, harness:14, retired:2, identity:5) | recent | Broadest coverage |
| forge_agent (A-FORGE runtime) | 30 actors | runtime | Doer-side mirror |
| GEOX .well-known + per-skill cards | 13 | recent | Static per-skill |

**Orphans to kernel (17 of 28 AAA dirs):**
`555-ASI-VISION`, `aaa-gateway`, `antigravity`, `arif-fazil-identity.yaml`, `claude-code`, `codex`, `forge-bot`, `grok-build`, `hermesarifos-bot`, `kimi-code`, `makcikgpt`, `openclaw`, `prospect-maturation`, `protocols`, `skill-auditor`, `skills`, `warga`

(Note: `agent-zero` is INSIDE kernel but ARCHIVED at AAA; `forge-bot` is RETIRED-TBD per WARGA STATUS injection this session.)

---

## Cross-Reference Matrix

| Actor | kernel | AAA | Alias notes |
|---|---|---|---|
| 333-AGI | BOUND | YES | fi=FI-002, actor=333-AGI/FI-002, caps=OBSERVE/REASON |
| 555-AGI | BOUND | YES | fi=FI-002 (shares), actor=555-AGI/FI-??? |
| 888-APEX | BOUND | YES | constitutional judge |
| agent-zero | BOUND (ARCHIVED) | YES (ARCHIVED) | ret; last activity pre-2026-06-30 |
| agentic-trading-companion | ORPHAN | YES | PENDING_BIND |
| antigravity | ORPHAN | YES | PENDING_BIND (CLI harness) |
| arif-fazil-identity.yaml | ORPHAN | YES | PENDING_BIND (this is identity _file_, not actor) |
| claude-code | ORPHAN | YES | PENDING_BIND |
| codex | ORPHAN | YES | PENDING_BIND |
| decisions | BOUND | YES | doc folder |
| forge-bot | ORPHAN | YES | RETIRED-TBD per WARGA STATUS |
| grok-build | ORPHAN | YES | PENDING_BIND |
| hermesarifos-bot | ORPHAN | YES | DORMANT per IDENTITY_LOCK |
| kimi-code | ORPHAN | YES | PENDING_BIND; aliases kimi-code-fi008, FI-008 |
| kimi-code-fi008 | — | — | alias only, not in any source registry |
| FI-008 | — | — | alias only, not in any source registry |
| makcikgpt | ORPHAN | YES | PENDING_BIND |
| openclaw | ORPHAN | YES | PENDING_BIND (333-AGI Telegram embodiment) |
| prospect-maturation | ORPHAN | YES | PENDING_BIND |
| protocols | ORPHAN | YES | doc folder — may be NOT_AN_ACTOR |
| skill-auditor | ORPHAN | YES | PENDING_BIND |
| skills | ORPHAN | YES | skill folder — NOT_AN_ACTOR |
| warga | ORPHAN | YES | meta-folder (warga manager code) — NOT_AN_ACTOR |

---

## Required Deliverables

### 1. Schema proposal: federation.identity_binding.v1

```json
{
  "$schema": "federation.identity_binding.v1",
  "canonical_actor_id": "kimi-code",
  "display_name": "Kimi Code CLI",
  "aliases": ["kimi-code-fi008", "FI-008"],
  "alias_status": {
    "kimi-code-fi008": "DEPRECATED_PENDING_CALLSITE_AUDIT",
    "FI-008": "DEPRECATED_PENDING_CALLSITE_AUDIT"
  },
  "identity_pubkey": {
    "algorithm": "ed25519",
    "spki_hex": "<from identity.json>"
  },
  "identity_fingerprint": "<sha256 from identity.json>",
  "authority_band": "novice",
  "current_stage": "active",
  "last_seen": "2026-09-14T01:30:00Z",
  "source_records": [
    {"source": "arifOS_kernel", "path": "agent_registry.json:agents.kimi-code", "status": "PENDING_BIND"},
    {"source": "AAA_agent_card", "path": "agents/kimi-code/agent-card.json", "status": "BOUND"},
    {"source": "AAA_identity", "path": "agents/kimi-code/identity.json", "status": "BOUND"},
    {"source": "AAA_a2a_server", "path": "a2a-server/agent-cards/harness/kimi-code.json", "status": "PENDING_BIND"},
    {"source": "forge_agent", "path": "<runtime>", "status": "PENDING_BIND"},
    {"source": "harness_agents_md", "path": "/root/.kimi-code/AGENTS.md", "status": "BOUND (in-harness)"}
  ],
  "binding_status": "PROPOSED",
  "binding_freshness_sec": 33*86400,
  "provenance": {
    "created_by": "333-AGI",
    "session": "SEAL-ae987612647948b1",
    "created_at": "2026-09-14T01:35:00Z",
    "witness_receipts": ["<binding manifest receipt>"]
  }
}
```

### 2. Binding Queue (PROPOSED, not auto-bound)

| canonical_actor_id | Action | Pre-conditions | Owner | Verifier |
|---|---|---|---|---|
| 555-ASI-VISION | PROPOSED_BIND | identity.json + agent-card.json audit | AAA registration | APEX/888 |
| antigravity | PROPOSED_BIND | forge_agent migration check | AAA | FRAME |
| claude-code | PROPOSED_BIND | ed25519 keypair | AAA | APEX/888 |
| codex | PROPOSED_BIND | ed25519 keypair | AAA | FRAME |
| grok-build | PROPOSED_BIND | ed25519 keypair | AAA | FRAME |
| hermesarifos-bot | PROPOSED_BIND (DORMANT flag) | IDENTITY_LOCK cross-check | AAA | APEX/888 |
| kimi-code | PROPOSED_BIND | alias tombstone + callsite audit (WP-01 deliverable 5) | AAA | APEX/888 |
| makcikgpt | PROPOSED_BIND | scope definition | AAA | FRAME |
| openclaw | PROPOSED_BIND (linkage to 333-AGI) | embodiment proof | AAA | APEX/888 |
| prospect-maturation | PROPOSED_BIND | capability list audit | AAA | FRAME |
| skill-auditor | PROPOSED_BIND | role differentiation from skills/ folder | AAA | APEX/888 |
| agent-zero | NO_BIND (ARCHIVED) | keep pointer only | — | — |
| forge-bot | NO_BIND (RETIRED-TBD) | needs sovereign decision | AAA | APEX/888 |
| aaa-gateway | NO_BIND (not an actor — gateway infra) | reclassify | AAA | FRAME |
| arif-fazil-identity.yaml | NO_BIND (identity _file_, not actor) | reclassify | AAA | FRAME |
| decisions, protocols, skills, warga | NO_BIND (not actors) | reclassify | AAA | FRAME |

### 3. Alias Deprecation Manifest

| Alias | Actor | Status | Action | Callsite audit |
|---|---|---|---|---|
| `kimi-code-fi008` | kimi-code | DEPRECATED_PENDING_CALLSITE_AUDIT | tombstone first; remove after call-site inventory + sovereign ack | **UNKNOWN — needs audit** (per AT-ID-03 + WP-01 hard constraint) |
| `FI-008` | kimi-code | DEPRECATED_PENDING_CALLSITE_AUDIT | same | same |

(NO alias is hard-deleted in this work package. Tombstones only.)

### 4. Fingerprint Sync Job Design (NOT wired — design only)

**Requirements:**
- Reads from: arifOS kernel registry, AAA agent-cards, AAA identity files, AAA a2a-server cards, forge_agent registry, GEOX cards
- Writes to: arifOS kernel registry (REQUIRES arifOS authority — not in scope for 333-AGI architect lane)
- Cadence: daily cron + on-demand
- Receipt: emits `arifFlow` consequence record with class `IDENTITY_SYNC`
- Staleness SLO: 24h max
- Drift alert: when sync gap > 7d, FRAME observable + arifOS HELD state

**Implementation TBD:** requires arifOS constitutional authority. **Held for arifOS engineer lane.**

### 5. Reconciliation Report Structure (template)

```json
{
  "report_id": "recon-2026-09-14T01:35",
  "sources_compared": ["arifOS_kernel", "AAA_agent_card", "AAA_identity", "a2a_server", "forge_agent", "GEOX"],
  "canonical_actors": 28,
  "matches": 8,
  "mismatches_actor_id": 1,
  "mismatches_capability": 4,
  "mismatches_authority_band": 0,
  "orphans_to_kernel": 17,
  "retired_or_dormant": 4,
  "recommendation": "BIND pending 12; tombstone kimi-code aliases; reclassify 5 non-actors"
}
```

### 6. Drift Alert Contract

- `arifOS_arifos-agent_registry.last_fingerprint_sync > 7d` → FRAME emits `STALENESS` observation
- `AAA_a2a-server.count - arifOS_kernel.count > 5` → HELD state proposed
- Receipt: `arifFlow consequence class=IDENTITY_DRIFT severity=INFO|WARN|CRITICAL`

---

## Acceptance Tests (per AT-IDs from campaign)

| AT | Test | Status | Evidence |
|---|---|---|---|
| AT-ID-01 | Every AAA dir classified BOUND/PENDING/LEGACY/RETIRED/ARCHIVED/UNKNOWN | DONE | table above |
| AT-ID-02 | Kernel records include source provenance + last_fingerprint_sync timestamp | PENDING (kernel authority required) | design drafted |
| AT-ID-03 | Alias lookup resolves to 1 canonical actor without breaking legacy | PROPOSED | kimi-code → kimi-code; tombstone first |
| AT-ID-04 | Unknown actor cannot acquire authority from alias | PENDING (capability graph WP-03) | dependency |
| AT-ID-05 | Sync job produces signed/hashed reconciliation receipt | PENDING (kernel authority) | design drafted |
| AT-ID-06 | Staleness alert produces FRAME-observable output | PENDING (sync job) | design drafted |
| AT-ID-07 | No production deletions occur | PASS | only tombstones, no deletion |

**Overall WP-01 status: PARTIAL** (deliverables complete; wiring requires arifOS authority which 333-AGI architect lane does not hold)

---

## Rollback Plan

All WP-01 artifacts are in `/root/AAA/governance/` (advisory docs, not kernel state):
- This file: WP-01-IDENTITY-CONVERGENCE-DELIVERABLES.md
- Schema proposal: included in this file
- Binding queue: table above
- Deprecation manifest: table above
- Sync job design: included

Rollback = delete the docs. Zero kernel state modified. Zero deletion of AAA dirs. Zero production change.

---

## What WP-01 does NOT do

- Does NOT auto-grant authority from directory/file/process
- Does NOT delete any file or alias
- Does NOT modify arifOS kernel
- Does NOT modify forge_agent runtime
- Does NOT call `arif_init` for new actors
- Does NOT classify non-actor folders as actors
- Does NOT issue a verdict on AGI/ASI readiness

---

## Next Steps (sequenced, not parallel)

1. **NOW**: Commit this doc to `/root/AAA/governance/` (reversible, advisory)
2. **NEXT**: Hand to APEX/888 for independent review (Gödel lock — doer ≠ judge)
3. **THEN**: WP-02 F9/F12 floor restoration (arifOS constitutional-floor engineer lane)
4. **AFTER WP-02**: WP-03 capability graph (AAA + arifOS contract engineer)
5. **AFTER WP-03**: WP-04 reality graph (arifFlow engineer)

**WP-01 → WP-08 in priority order per the campaign directive.**

---

## Receipt Linkage

| Action | Receipt/Hash |
|---|---|
| Session bind (arifOS) | `SEAL-ae987612647948b1` (LIMITED_MUTATE) |
| Doc creation | pending commit hash (this doc) |
| Schema proposal | `<tbd>` after APEX review |
| Binding execution | held — requires arifOS authority |
| Tombstone first | held — requires AAA authority + sovereign ack |
| Recovery test | held — requires WP-06 survivability test |

---

*Operator: 333-AGI Δ MIND (apex-judge lane NOT invoked; doer=architect, not judge)*
*Verifier lane: 888-APEX (pending dispatch)*
*Doer≠judge: Gödel lock maintained*
*F13 surface: NONE*

**VERDICT: PARTIAL** (deliverables complete, wiring held for authority-appropriate lane)