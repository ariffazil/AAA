# arifOS Definitive Upgrade Plan: FED & Constitutional Skill Mesh

> **Document ID:** AAA-UPGRADE-FED-2026-V1  
> **Status:** APPROVED (F13 SOVEREIGN)  
> **Forged:** 2026-08-10 by 333-AGI + F13 SOVEREIGN  
> **Location:** `/root/AAA/governance/FED_UPGRADE_ROADMAP.md`  
> **Target:** Full system upgrade across FED router, Qdrant skill mesh, sidecar ingestion, and A2A trace propagation.

---

## Executive Upgrade Roadmap

### P0 — Critical Infrastructure Revival & Schema Tagging

| # | TODO | Status | Owner | Notes |
|---|---|---|---|---|
| 1 | **LiteLLM :4011 Revive & Config Injection** | ❌ Not started | A-FORGE | Kill hung process (67 CPU hours), restart with capability alias config |
| 2 | **FED :4000 Capability Alias Routing** | 🔧 Partial | FED | Static 15-model mapping exists; needs dynamic capability signature resolution |
| 3 | **Qdrant Skill Mesh Population** | ❌ Not started | AAA | Create `arifOS_skill_mesh` collection, batch embed 184 skills |
| 4 | **Skill Capability Tagging** | ❌ Not started | AAA | Inject `capability_tier` + `ecology_state` metadata into all SKILL.md files |

### P1 — JIT Intent Retrieval & Zero-Trust Interception

| # | TODO | Status | Owner | Notes |
|---|---|---|---|---|
| 5 | **FED Middleware (JIT Context Injection)** | ❌ Not started | FED | Hook `build_jit_context` into FED pre-request pipeline |
| 6 | **Sidecar Auto-Ingest Transport Wrapper** | ❌ Not started | arifFlow | Socket-layer middleware on FED :7074 → arifFlow :7073 |
| 7 | **A2A Trace Propagation Headers** | ❌ Not started | AAA | `traceparent` + `arif_trace_id` across Hermes/OpenCode/OpenClaw |

### P2 — Ecology Lifecycle & Automated Benchmarking

| # | TODO | Status | Owner | Notes |
|---|---|---|---|---|
| 8 | **Ecology Lifecycle Daemon (HOT/WARM/COLD)** | ❌ Not started | arifFlow | Health scoring: H = (Success/Invocations) × e^(-Latency/5000) |
| 9 | **MCP Auto-Discovery Watcher** | ❌ Not started | AAA | Endpoint poller → auto-embed → Qdrant index |
| 10 | **FED Benchmark Suite** | ❌ Not started | AAA | TTFT, schema fidelity, fallback resilience tests |

### P3 — Provider Key Resolution & Provenance Invariants

| # | TODO | Status | Owner | Notes |
|---|---|---|---|---|
| 11 | **Provider Gap Resolution** | ❌ Not started | FED | Kimi endpoints, OpenCode Go keys, Qwen rate limit backoff |
| 12 | **Provenance Block Auto-Fill** | ❌ Not started | arifFlow | Inject UNKNOWN state into unpopulated apex/flow/projection blocks |
| 13 | **Causal DAG Enforcement (R1–R7)** | ❌ Not started | arifFlow | Parent-child span lineage, ΔS > 0 entropy checks |

---

## Meta-Mesa Execution Principles

1. **Decouple Task from Provider:** Never hardcode provider names. Always use capability aliases (`fed-reasoning-heavy`, `fed-agent-subagent`).
2. **Fail-Closed by Design:** Missing telemetry = incomplete execution. No silent local fallback without trace span.
3. **Minimize Context Footprint:** Static prompts lean. Qdrant Intent Retriever injects JIT schemas (<10ms).
4. **Zero-Trust Telemetry:** Infrastructure observes execution. Sidecar interception is law. Agent self-attestation is banned.

---

## Implementation Dependencies

```
P0.1 (LiteLLM) → P0.2 (FED aliases) → P1.5 (JIT middleware) → P2.8 (Ecology daemon)
P0.3 (Qdrant collection) → P0.4 (Skill tagging) → P1.5 (JIT middleware)
P0.3 (Qdrant) → P2.9 (MCP auto-discovery)
P1.6 (Sidecar) → P1.7 (A2A trace) → P2.10 (Benchmark)
P3.11 (Provider keys) → independent
P3.12 (Provenance) → P3.13 (DAG enforcement)
```

---

*DITEMPA BUKAN DIBERI — The upgrade plan is forged, not given. Every TODO is a commitment. Every dependency is a constraint. Execute in order. ⚒️*
