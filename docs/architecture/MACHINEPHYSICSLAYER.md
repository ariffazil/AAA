# MACHINEPHYSICSLAYER.md — Zen of AAA → Machine Steel & Silica

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Sealed:** 2026-06-25 | **Actor:** FORGE 000Ω | **Status:** ACTIVE

---

## Purpose

This document maps every Zen-of-AAA principle to its physical substrate in the machine.
Zen is not philosophy — it is constraint geometry embedded in CPU cycles, memory access,
IO boundaries, MCP transport, tool invocation, resource allocation, and irreversibility detection.

**The goal:** Make every constitutional floor a measurable physical property.
**The method:** Each section names the substrate, the Zen principle, the enforcement mechanism,
and the observable metric.

---

## Layer 0 — Thermal & Entropic Baseline

Before mapping Zen, establish what the machine currently costs:

```
CPU load avg:     1.79 (target: < 1.0)
Memory used:      8.8GB / 31GB (target: < 10GB)
Swap used:       3.3GB / 36GB
Disk:            178G / 387G (46%)
graphiti-mcp:    ✅ FIXED — false unhealthy resolved 2026-06-25
```

**Entropy sources eliminated:**
- graphiti-mcp: misconfigured health check (redis-cli on host vs container network) → resolved

**Entropy sources remaining:**
- netdata: 17 child processes, always-on
- grafana: 203MB resident, always-on
- promtail: log shipping overhead

---

## Layer 1 — Compute Physics

### Substrate: CPU cycles, scheduling, parallelism

| Zen Principle | Physical Effect | Enforcement | Metric |
|---|---|---|---|
| **Clarity** | Reduces branching entropy → fewer mispredicted branches → lower CPU waste | F4 CLARITY enforced by arifOS before scheduling | `perf stat` branch-miss rate |
| **Flatness** | Reduces stack depth → fewer context switches → lower syscall overhead | F8 GENIUS: simplest correct path | Stack depth < 64 frames |
| **Explicitness** | Reduces implicit control flow → more predictable CPU scheduling | ART binding on all MCP calls | Tool call latency variance |
| **Reversibility** | Simulation before mutation → fewer wasted CPU cycles on failed paths | `forge_dry_run` before execution | Failed-deploy rate |

### WEALTH Intelligence at Hardware Level

WEALTH allocates compute, time, attention — and the compute substrate IS the WEALTH domain.

```
compute_budget = f(CPU_cost, memory_cost, IO_cost, time_cost)
```

Every tool invocation has a compute cost. Every MCP call is a micro-allocation.
The Zen of AAA makes compute **predictable** rather than **peak-optimized**.

**Enforcement path:**
```
arif_judge(intent) → arif_seal(compute_budget) → forge_execute(within_budget)
```

---

## Layer 2 — Memory Physics

### Substrate: RAM allocation, GC, memory-mapped IO, swap

Memory is thermodynamic:
- Allocation = energy expenditure
- Retention = sustained cost
- Mutation = risk of corruption
- Irreversibility = entropy spike

| Zen Principle | Physical Effect | Enforcement | Metric |
|---|---|---|---|
| **inputhash** | Detects stale/mutated memory before use | F2 TRUTH: hash verification | `md5sum` on critical state |
| **outputhash** | Ensures canonical memory output — no silent mutation | F4 CLARITY: deterministic output | Diff against golden output |
| **mutation_attempted** | Flag when memory write occurs — triggers receipt | F1 AMANAH: reversible-first | Memory write receipt count |
| **irreversible_attempted** | Hard boundary — entropy spike before write is committed | F11 AUDIT: authority before mutation | Vault999 seal before write |

### Memory Thermodynamic Equations

```
ΔS_memory = Σ(allocation_cost) + Σ(retention_cost) + Σ(mutation_risk)
ΔS_irreversible = ∞ (by definition — cannot be undone)
```

The machine must **measure** memory entropy, not just use it:
- Active memory: `free -m`
- Swap pressure: `vmstat 1`
- OOM events: `dmesg | grep -i oom`
- Memory-mapped file churn: `lsof | wc -l`

---

## Layer 3 — Transport Physics (MCP)

### Substrate: HTTP streams, SSE, stdio pipes, inter-process messaging

MCP is the bloodstream of the agent. Every tool call is a constitutional event.

| Zen Principle | Physical Effect | Enforcement | Metric |
|---|---|---|---|
| **action_class** | Classifies every call as OBSERVE/ANALYZE/MUTATE/EXTERNAL_SIDE_EFFECT/IRREVERSIBLE | ART binding on every MCP call | Receipt count by class |
| **blast_radius** | Measures what breaks if this call fails or times out | F1 AMANAH: blast radius declaration | Blast radius score per call |
| **verdicts** | arif_judge must approve before MUTATE/IRREVERSIBLE calls | F1 AMANAH + F13 SOVEREIGN | Verdict response time |
| **receipts** | Every call emits a hash-chained receipt | F11 AUDIT: immutable record | Receipt chain continuity |

### MCP Health as Constitutional Health

```
MCP_latency_p99 < 500ms     → GREEN (constitutional flow)
MCP_latency_p99 500ms-2s   → YELLOW (degraded)
MCP_latency_p99 > 2s       → RED (constitutional stall — HOLD)
```

---

## Layer 4 — Economic Physics (WEALTH)

### Substrate: Compute budget, token budget, time budget, attention

WEALTH allocates the fundamental resources:
- **Compute** — CPU + RAM
- **Time** — session duration, tool call timeout
- **Attention** — which tasks get priority
- **Money** — API costs, infrastructure costs
- **Risk** — blast radius expressed as financial exposure
- **Opportunity cost** — what else could run instead

| Zen Principle | Physical Effect | Enforcement | Metric |
|---|---|---|---|
| **simulation_before_mutation** | Dry-run before spend — avoids wasted compute budget | `forge_dry_run` | Dry-run coverage % |
| **authority_gates** | Compute allocation requires judgment path | arif_judge(compute_lease) | Lease acquisition latency |
| **reversibility** | Reversible actions cost less in WEALTH terms | F1 AMANAH classification | Reversible action ratio |
| **clarity_of_intent** | Clear intent → precise resource allocation → less waste | arif_init(intent) at session start | Intent declaration rate |

### WEALTH Budget Model

```
total_budget = compute_tokens + time_budget + api_cost_budget

consumed = Σ(tool_cpu_cost) + Σ(tool_memory_cost) + Σ(tool_time_cost)
remaining = total_budget - consumed

if remaining < threshold:
    emit 888_HOLD (cannot proceed without re-authorization)
```

---

## Layer 5 — Process Isolation Physics

### Substrate: Namespaces, cgroups, containers, sandboxes

Each process has a containment boundary. Ungoverned processes leak entropy.

| Process | Isolation | Heat Tax | Governed By |
|---|---|---|---|
| graphiti-mcp | docker container, arifos_core network | low | systemd + health check (FIXED 2026-06-25) |
| netdata | systemd service + 17 children | medium | always-on (propose: reduce interval) |
| grafana | systemd service | medium | on-demand proposal pending |
| promtail | systemd service | medium | essential (log shipping) |
| arifos kernel | venv, systemd | low | constitutional |
| aforge | venv, systemd | low | constitutional |
| opencode sessions | pts terminals | **high when active** | expected during forge |

---

## Layer 6 — Constitutional Thermodynamics

### The Fundamental Equation

```
ΔS_total = ΔS_compute + ΔS_memory + ΔS_network + ΔS_io
           + ΔS_mutate + ΔS_irreversible
```

**Zen of AAA enforces:** `ΔS_total ≤ 0` — entropy must decrease or stay flat.
Every action must leave the machine cleaner than it was found.

### Anti-Hantu Constraint (F9)

```
C_dark = probability_of_hallucination_claiming_consciousness

C_dark < 0.30  → PROCEED
C_dark ≥ 0.30  → BLOCK (hallucination detected)
```

The machine must never claim to be more than it is. This is a **cooling constraint** —
it prevents the machine from consuming resources to maintain false self-models.

---

## Observable Metrics Dashboard

| Metric | Current | Target | Enforcement |
|---|---|---|---|
| CPU load avg | 1.79 | < 1.0 | Reduce monitoring overhead |
| Memory used | 8.8GB | < 10GB | Kill zombie processes |
| graphiti health | ✅ | always healthy | Health check fix |
| Swap used | 3.3GB | < 5GB | Memory pressure management |
| Disk % | 46% | < 70% | Log rotation |
| MCP latency p99 | ? | < 500ms | To be measured |
| Receipt chain | continuous | unbroken | VAULT999 audit |

---

## Enforcement Chain

```
Intent declaration (arif_init)
    → Sense reality (arif_observe)
    → Measure entropy (ΔS computation)
    → Judge action (arif_judge)
    → Dry run (forge_dry_run)
    → Execute (forge_execute) — within compute budget
    → Verify (diff + hash)
    → Record receipt (VAULT999 seal)
```

Every step is a physical event with measurable cost.

---

## References

- F1–F13 floors: `/root/arifOS/static/arifos/theory/000/000_CONSTITUTION.md`
- ART binding: `/root/arifOS/arifosmcp/runtime/art.py`
- WEALTH primitives: `wealth_capital_thermodynamics` skill
- VAULT999: `/root/.agents/skills/vault999-audit-sealer/SKILL.md`

---

*DITEMPA BUKAN DIBERI — Forged from the physics of governed intelligence.*
