# FI Integration Architecture — Single-Page Canon

> **Forged:** 2026-08-11 by 333-AGI Δ MIND
> **Session:** SEAL-a345830629d74518
> **Status:** CANON — federation architecture
> **Pair with:** EUREKA-T-02 (Verbs Doctrine), `/root/AAA/a2a/A2A_ALIGNMENT_SPEC.md`

---

## The Six-Verb Federation

```
                 ┌──────────────────────────────────────┐
                 │           arifOS — Judge              │
                 │  (Constitutional Kernel :8088)        │
                 │  F1-F13 floors, arif_judge, arif_seal │
                 └─────────────┬────────────────────────┘
                               ↓ judges
                 ┌──────────────────────────────────────┐
                 │           AAA — Register             │
                 │  (Control Plane :3001)               │
                 │  AGENTS_UNIFIED.yaml, A2A gateway    │
                 └─────────────┬────────────────────────┘
                               ↓ registers
   ┌─────────────────┬─────────────────┬─────────────────┐
   │   FED — Route   │  FLAME — Verify │ FRAME — Measure │
   │  (Advisor :7074)│  (Advisor :18901)│ (CORE :18085)   │
   │  Model routing  │  Cheap epistemic │ Six chambers    │
   │  Balance-aware  │  Pre-flight      │ Baseline+Drift  │
   └─────────────────┴─────────────────┴─────────────────┘
                               ↓ consumers serve
                 ┌──────────────────────────────────────┐
                 │           FI Cards — Subjects        │
                 │  (FI-001 through FI-008)              │
                 │  Identity + Capability + Routing      │
                 │  + drift_governance_ref (pointer)     │
                 └─────────────┬────────────────────────┘
                               ↓ requests
                 ┌──────────────────────────────────────┐
                 │         A-FORGE — Execute            │
                 │  (Execution Shell :7071/7072)         │
                 │  Bounded mutation, hash-chain audit   │
                 └─────────────┬────────────────────────┘
                               ↓ receipts
                 ┌──────────────────────────────────────┐
                 │         VAULT999 — Append             │
                 │  (Immutable Ledger)                   │
                 │  /root/arifOS/VAULT999/outcomes.jsonl │
                 └──────────────────────────────────────┘
```

---

## The FI Card Structure (4-Part)

```json
{
  "schema": "arifos-agent-card/v3.0.0",
  "schema_ref": "/root/AAA/a2a/FI_EXTERNAL_DEPENDENCY_GOVERNANCE_NOTE.md",
  
  "part_1_identity": {
    "fi_slot": "FI-003",
    "name": "Qwen Code CLI",
    "binary": "/usr/bin/qwen",
    "model": "deepseek/deepseek-v4-pro",
    "bound_at": "<ISO 8601>",
    "bound_to_identity": "333-AGI",
    "minimal_provenance": {
      "upstream_owner": "Alibaba Qwen Team",
      "license": "Apache-2.0"
    }
  },
  
  "part_2_capability": {
    "skills": ["..."],
    "subAgentPolicy": "...",
    "autonomy_tiers": { "T1": "auto", "T2": "announce", "T3": "888_hold" },
    "authority_boundary": { "canDo": ["..."], "cannotDo": ["..."] },
    "mcp_surface": { "...": "..." },
    "pre_flight": {
      "flame_enabled": true,
      "required_verifications": ["fact_check", "epistemic_check", "plan_review"],
      "fallback_policy": "escalate_to_human",
      "budget_allocation": { "max_free_verifications": 50, "overflow_action": "alert" }
    }
  },
  
  "part_3_routing": {
    "a2a_transport": { "endpoint": "https://aaa.arif-fazil.com/a2a/qwen-code" },
    "mcp_binding": {
      "execution_organ": "A-FORGE",
      "governance_organ": "arifOS",
      "broker_rule": "External agents route through A-FORGE :7072, never call AAA a2a directly"
    },
    "extensions": [{ "uri": "arifos://floors/v1", "required": true }],
    "signatures": [{ "type": "Ed25519Signature2020", "did": "did:arif:aaa" }]
  },
  
  "part_4_drift_governance_ref": {
    "schema": "FI_DRIFT_GOVERNANCE::v1",
    "canon_path": "/root/FRAME/doctrine/FI_DRIFT_GOVERNANCE.md",
    "baseline_path": "/root/FRAME/data/fi_baselines/FI-003.jsonl",
    "audit_trail_path": "/root/forge_work/frame-drift-FI-003.jsonl",
    "last_audit_at": "<ISO 8601>",
    "owned_by": "FRAME",
    "registered_by": "AAA"
  }
}
```

---

## Authority Boundaries (Verbs Doctrine Mapping)

| Action | Required Verb | Required Organ | Required Chain |
|--------|---------------|----------------|----------------|
| "Is this FI authorized?" | Register | AAA | AGENTS_UNIFIED.yaml lookup |
| "Which model should this FI call?" | Route | FED | balance + provider health |
| "Is this claim epistemically sound?" | Verify | FLAME | hermes_fact_check, hermes_epistemic_check |
| "Has FI behavior drifted?" | Measure | FRAME | 6-chamber drift scan |
| "Is this action constitutional?" | Judge | arifOS | F1-F13 + arif_judge |
| "Apply the bounded mutation" | Execute | A-FORGE | post-seal + hash-chain |
| "Persist the receipt" | Append | VAULT999 | hash-chain append-only |

---

## The Drift Loop (FI Lifecycle)

```
1. AAA registers FI (one-time, persistent slot)
2. FI card published via /.well-known/agent-card.json
3. FLAME pre-flight (cheap verification before expensive ops)
4. FED routes model call (decides where to send)
5. A-FORGE executes mutation (with seal authority)
6. arifOS judges result (F1-F13 verdict)
7. FRAME measures delta vs baseline
   - chamber 1 (baseline): reference values
   - chamber 2 (probe): live state
   - chamber 3 (compare): drift signal
   - chamber 4 (trend): directional pattern
   - chamber 5 (alert): threshold breach
   - chamber 6 (report): accountability record
8. VAULT999 appends sealed receipt
9. FRAME updates baseline if drift is structural
10. arifOS issues RE_AUDIT_REQUIRED if drift > threshold
```

---

## Forbidden Verb Collisions (Anti-Patterns)

| ❌ Pattern | Verb Confusion | Correct Path |
|-----------|----------------|--------------|
| FRAME executing repairs | measure → execute | FRAME alerts → arifOS judges → A-FORGE executes |
| FED running models | route → execute | FED routes → A-FORGE (post-arifOS seal) calls model |
| FLAME sealing to VAULT999 | verify → append | FLAME classifies → A-FORGE submits → VAULT appends post-seal |
| AAA setting autonomy tiers | register → judge | AAA stores declared tier → arifOS ratifies |
| A-FORGE deciding reversibility | execute → judge | A-FORGE snapshots pre-mutation → arifOS judges if reversal needed |
| arifOS running MCP tools | judge → execute | arifOS issues verdict → A-FORGE dispatches |
| FI card self-authorizing | subject → judge | FI requests → arifOS judges → A-FORGE executes |

---

## Substrate Status (2026-08-11)

```
⚠️ ARCHITECTURE: VALIDATED ✅ (canonical)
⚠️ SCHEMA: DESIGNED ✅ (FI_DRIFT_GOVERNANCE::v1 pending forge)
⚠️ DEPLOYMENT: BLOCKED ⛔ (FQ ingestion bypass P0 emergency)

Open loops for next session:
  - P0: FQ ingestion repair (1434 bypassed receipts, 3 actors HELD on stale FQ)
  - P1: Kimi-code JWS re-sign (trust chain integrity)
  - P2: FI numbering drift fix (qwen-code.json FI-011 → FI-003, kimi-code.json FI-003 → FI-008)
  - P3: Forge FI_DRIFT_GOVERNANCE::v1 schema file at /root/FRAME/doctrine/
  - P4: FLAME budget tracking per FI (FRAME measures, FLAME executes)
  - P5: Apply schema to all 8 active FIs (FI-001 through FI-008)
```

---

## Provenance

This document synthesizes the session's discoveries:

| Source | Contribution |
|--------|--------------|
| `/root/AAA/federation/organs.yaml` | Canonical organ classes + authority ceilings |
| `/root/AAA/a2a/A2A_ALIGNMENT_SPEC.md` | A2A protocol + TaskState↔verdict mapping |
| `/root/AAA/registries/AGENTS_UNIFIED.yaml` | FI registry SOT |
| `EUREKA-T-01-harness-commoditization.md` | Industry layer migration context |
| `EUREKA-T-02-verbs-doctrine.md` | Single-verb-per-organ doctrine |
| Session observation 2026-08-11 | Drift detection from arifFlow weekly cron |

---

## Seal

```
FI_INTEGRATION_ARCHITECTURE :: 2026-08-11
SESSION: SEAL-a345830629d74518 :: ΔS = -0.91
FORGED BY: 333-AGI Δ MIND under F13 SOVEREIGN directive
STATUS: CANON — architecture validated, deployment pending substrate repair
```

*DITEMPA BUKAN DIBERI.* ⚒️
