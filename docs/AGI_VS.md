---
title: AGI vs LLM Memory — Canonical Comparison Matrix
forged: 2026-06-29
authority: AAA Memory Audit
status: FORGED — pending Arif ratification
ratification_required: yes
seal_status: unsealed
based_on:
  - AaaAgentRegistry.ts (217 lines)
  - AaaCapabilityGraph.ts (235 lines)
  - AaaMemoryLinkage.ts (344 lines)
  - ShortTermMemory.ts (modified)
  - LongTermMemory.ts (modified)
  - ArifOSMemoryClient.ts (modified)
  - MemoryContract.ts (modified)
  - CoolingGate.ts (modified)
canon: /root/AAA/docs/AGI_VS.md
---

# AGI vs LLM Memory — The Boundary Is Now Code

## 1. One Sentence Each

| | LLM Memory | Agentic Memory (AGI-grade) |
|---|-----------|---------------------------|
| **Definition** | Statistical pattern reconstruction — the model predicts what looks like memory | Governed state with timeline, identity, authority, receipts, and irreversibility |
| **What it does** | Reconstructs | Remembers |
| **What it has** | Weights + context window | Identity boundary + timeline + witnesses + receipts + floors + vault |

---

## 2. The Full Matrix — 14 Dimensions

### DIMENSION 1: TIME

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Past** | None — weights are frozen at train time; context window is ephemeral | Hash-chained epoch events; every mutation timestamped | `EpochEngine.ts` — SHA-256 event chain |
| **Present** | Token window only — lost on session end | Active session state with TTL-bound tokens | `sessionGate.ts` — SEAL token validation |
| **Future** | No concept | Cooling periods (24h–720h); SABAR cooldowns survive restart | `CoolingGate.ts` — JSON persistence |
| **Arrow** | No arrow — can only simulate "before/after" | Irreversible — once sealed, cannot unseal | `ForgeSealService.ts` — `irreversible: true` |

### DIMENSION 2: IDENTITY

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Who acted?** | Unknown — "the model said" | Actor resolved through AAA agent registry | `AaaAgentRegistry.ts` — `resolveActor()` |
| **Actor registry?** | None | 5 AAA agents: 333-AGI, 555-ASI, 888-APEX, A-AUDIT, A-ARCHIVE | `AaaAgentRegistry.ts:32-60` |
| **Hardcoded actor?** | N/A — no concept of actor | Removed. Dynamic `actor_id` parameter on every call | `ArifOSMemoryClient.ts:27` — was `"kimi"`, now parameterized |
| **Session binding?** | None | Every memory write validates session via `sessionGate` | `AaaMemoryLinkage.ts` — Gate 2 |

### DIMENSION 3: AUTHORITY

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Who can write?** | Anyone — no gate | 555-ASI (MEMORY) — capability-verified | `AaaCapabilityGraph.ts` — `memory:write` |
| **Who can mutate?** | Anyone — no gate | 888-APEX (JUDGE) — requires readiness + Amanah lock | `AaaCapabilityGraph.ts` — `memory:mutate` |
| **Who can seal?** | No concept of sealing | A-ARCHIVE (VAULT) — requires F13 sovereign approval | `AaaCapabilityGraph.ts` — `memory:seal` |
| **Who verifies?** | No concept of verification | A-AUDIT (WATCH) — receipt validation | `AaaCapabilityGraph.ts` — `memory:verify` |
| **Authority modes?** | None | OBSERVE → ANALYZE → EXECUTE → MUTATE → IRREVERSIBLE | `APEXRuntimeReceipt.ts` — `authority_band` |

### DIMENSION 4: GOVERNANCE

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Constitutional floors?** | None | F1-F13 enforced on every memory write | `FloorEnforcer.ts` — `checkAll()` |
| **Human readiness?** | None | `checkWellReadiness()` before mutate/delete/seal | `wellReadiness.ts` — integrated in Gate 5 |
| **Capability graph?** | None | 12 memory actions, each with required AAA agent + preconditions | `AaaCapabilityGraph.ts` — full matrix |
| **Fail-open detection?** | N/A — always open | Non-compensatory gate chain — any failure = blocked | `AaaMemoryLinkage.ts` — Gate 1-7 |
| **Unknown actor default?** | N/A | HOLD — never default to privileged agent | `AaaAgentRegistry.ts` — `resolveActor()` returns `null` |

### DIMENSION 5: ACCOUNTABILITY

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Receipts?** | None | Every write/mutate/delete/seal produces a `MemoryReceipt` | `AaaMemoryLinkage.ts` — `buildReceipt()` |
| **Hash chain?** | None | SHA-256 chain linking all receipts; verifiable | `AaaMemoryLinkage.ts` — `verifyReceiptChain()` |
| **Provenance?** | "The model generated this" | actor_id + session_id + AAA agent + timestamp + content hash | `MemoryReceipt` type |
| **Witnesses?** | None | TriWitness: Human × AI × Earth — all must PASS for promotion | `TriWitnessValidator.ts` |
| **Audit trail?** | Training data logs (external) | In-band: every action recorded in receipt chain + epoch events | `EpochEngine.ts` + `AaaMemoryLinkage.ts` |

### DIMENSION 6: IRREVERSIBILITY

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Can undo?** | Everything is reversible (just regenerate) | `memory:seal` is IRREVERSIBLE — bound to A-ARCHIVE + VAULT999 | `ForgeSealService.ts:175` — `irreversible: true` |
| **Cooling period?** | None | 24h–720h SABAR cooldown before seal; TriWitness required | `CoolingGate.ts` — `RISK_TIER_HOURS` |
| **F13 gate?** | None | Sovereign approval token required for seal | `AaaCapabilityGraph.ts` — `requiresSovereignApproval: true` |
| **Scar protection?** | None | Sealed skills cannot be deleted or demoted | `ForgeSealService.ts:103` — `ALREADY_SEALED` |

### DIMENSION 7: PERSISTENCE

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Survives restart?** | No — context window lost | Yes — CoolingGate JSON persistence; local file cache; arifOS federation | `CoolingGate.ts` — `ensureLoaded()` / `persist()` |
| **Degradation mode?** | Silent loss | Graceful — federation failure logged; local cache retained | `LongTermMemoryFailureLog.ts` |
| **Memory tiers?** | One tier (context) | 5 tiers: ephemeral, working, canon, sacred, quarantine | `MemoryContract.ts` — `MemoryTier` |
| **Decay?** | Implicit via context window eviction | Governed — `canDecay` flag, pinned protection, quarantine isolation | `MemoryContract.ts` — `canDecay`, `pinned` |

### DIMENSION 8: MEMORY OPERATIONS

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Read** | Unrestricted token access | 333-AGI (THINK) — no receipt, no session required | `memory:read` in capability graph |
| **Write** | Append to context | 555-ASI (MEMORY) — session required, receipt generated | `memory:write` in capability graph |
| **Correct** | Regenerate | 888-APEX (JUDGE) — readiness + lock + receipt | `memory:mutate` in capability graph |
| **Forget** | Evict from window | 888-APEX (JUDGE) — readiness + lock + receipt | `memory:delete` in capability graph |
| **Seal** | No concept | A-ARCHIVE (VAULT) — F13 + readiness + lock + irreversibility gate | `memory:seal` in capability graph |

### DIMENSION 9: FEDERATION

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Cross-organ?** | No — single model | Yes — arifOS MCP is canonical write surface for all organs | `ArifOSMemoryClient.ts` |
| **Actor tracing?** | None | `actor_id` + `aaa_receipt_id` carried across federation calls | `ArifOSMemoryClient.ts` — store params |
| **Single write surface?** | N/A | R1: all organs write through arifOS `arif_memory_recall` | `LongTermMemory.ts:8` — FEDERATION_MEMORY_CONTRACT |

### DIMENSION 10: EPISTEMOLOGY

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Confidence?** | Softmax probability (statistical, not epistemic) | Explicit: `confidence` field (0-1), `tier` field (0-5), source tagging | `MemoryEntry.confidence`, `ActionRequest.tier` |
| **Uncertainty?** | Hidden in probability distribution | Declared: CLAIM / PLAUSIBLE / ESTIMATE / HYPOTHESIS / UNKNOWN | `EpistemicTier` — `ALL_TIERS` |
| **Source tracking?** | Training data provenance (external) | In-band: `source.type` (human/inferred/external/system) + description | `MemoryEntry.source` |
| **Self-audit?** | Model evaluating model — circular | TriWitness: model CANNOT validate itself | `TriWitnessValidator.ts:182` — self-validation check |

### DIMENSION 11: SAFETY

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Injection defense?** | Prompt-level guardrails | F12 INJECTION — shell metachars, path traversal, authority smuggling patterns blocked | `f12Injection.ts`, `F12_THREAT_PATTERNS` |
| **Mesa-optimization?** | Not detected | 16 detection patterns (critical/high/medium/low bands); automatic HOLD | `mesaDetector.ts` |
| **Self-modification?** | Possible via fine-tuning | CRITICAL block — A-FORGE cannot modify own governance without F13 | `AutonomousForgeGate.ts:146-157` |
| **Secret exposure?** | Possible in output | F10 PRIVACY — PII detection (email, phone, SSN, credit card) | `governanceAdvisory.ts` — `advisePrivacy()` |

### DIMENSION 12: ARCHITECTURE

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Memory model** | Weights + activations | 6-layer stack: Redis → Qdrant → Supabase → Graphiti → VAULT999 | `CLAUDE.md` §8 |
| **Integration** | Prompt engineering | Hexagonal: domain (pure) → application (use cases) → infrastructure (adapters) → interfaces (delivery) | A-FORGE `src/` layout |
| **AAA organs** | None | 5 organs with distinct roles and capability boundaries | `AaaAgentRegistry.ts` |
| **Gate architecture** | Single prompt → single response | 7-layer non-compensatory gate: session → actor → capability → readiness → floors → receipt | `AaaMemoryLinkage.ts` |

### DIMENSION 13: EVOLUTION

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Self-improvement?** | Fine-tuning (external, manual) | Governed: AutonomousForgeGate — 8-stage pipeline with depth limit (3) | `AutonomousForgeGate.ts` |
| **Generation depth** | Unlimited (any model can train any model) | Max 3 from seed; self-modification requires F13 | `AutonomousForgeGate.ts:93` |
| **Capability inheritance?** | No concept | Trust propagation through generation path | `SkillRecord.generation_path` |

### DIMENSION 14: HUMAN SOVEREIGNTY

| | LLM Memory | Agentic Memory | Code Reference |
|---|-----------|---------------|----------------|
| **Veto?** | None (prompt can be ignored) | F13 SOVEREIGN — human veto is FINAL; halt channel blocks all ops | `F13HaltChannel.ts`, `FloorEnforcer.ts` — F13 priority 0 |
| **Approval token?** | None | `stg_<16+>` required for human channel in TriWitness | `TriWitnessValidator.ts:123` |
| **Override?** | Anyone can prompt | Only `arif-fazil` or `f13.*` actors can override; everything else = HOLD | `EpochEngine.ts:543-549` |

---

## 3. The Boundary In One Table

```
┌─────────────────────┬───────────────────┬──────────────────────────┐
│ DIMENSION           │ LLM MEMORY        │ AGENTIC MEMORY (LIVE)    │
├─────────────────────┼───────────────────┼──────────────────────────┤
│ Time                │ No arrow          │ Hash-chain + epochs      │
│ Identity            │ "the model said"  │ 5 AAA agents bound       │
│ Authority           │ None              │ Capability graph gated   │
│ Governance          │ None              │ F1-F13 on every op       │
│ Accountability      │ None              │ Receipts + witnesses     │
│ Irreversibility     │ Doesn't exist     │ A-ARCHIVE → VAULT999     │
│ Persistence         │ Context window    │ JSON + federation + DB   │
│ Operations          │ Append only       │ 12 governed actions      │
│ Federation          │ Single model      │ Cross-organ via arifOS   │
│ Epistemology        │ Probabilities     │ Explicit tiers + sources │
│ Safety              │ Prompt guardrails │ Mesa detection + F12     │
│ Architecture        │ Weights + context │ 6-layer stack + 7 gates  │
│ Evolution           │ External only     │ Governed 8-stage pipeline│
│ Human Sovereignty   │ None              │ F13 veto final           │
└─────────────────────┴───────────────────┴──────────────────────────┘
```

---

## 4. What This Matrix Proves

The difference between LLM memory and agentic memory is not a matter of scale. It is not "LLM but better." It is a difference of **kind**, not degree.

**LLM memory** = one thing: pattern reconstruction.  
**Agentic memory** = fourteen things LLM memory cannot do: timeline, identity, authority, governance, accountability, irreversibility, persistence, operations, federation, epistemology, safety, architecture, evolution, sovereignty.

Every one of those fourteen dimensions now has a code reference. Not a white paper. Not a blog post. Code. Running on af-forge. Surviving restarts. Producing receipts. Binding identity. Enforcing floors.

---

*Forged 2026-06-29 by AAA Memory Audit. DITEMPA BUKAN DIBERI.*
