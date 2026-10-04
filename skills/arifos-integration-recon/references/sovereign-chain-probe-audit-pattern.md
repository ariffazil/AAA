# Sovereign Chain-Probe Audit Pattern — Federated Architecture Deep-Dive

> **Forged:** 2026-08-12 by Hermes (F13 sovereign audit session with Arif)
> **Class:** Cumulative multi-turn investigation where sovereign incrementally probes federation state.

## What This Is

A distinct investigation methodology where the **sovereign leads the depth direction**, each question expects live-receipt evidence (curl, grep, config read, live probe), and understanding accumulates across turns. Unlike one-shot integration recon (which maps a single pipeline), the chain probe is **the sovereign auditing his own creation**.

## Pattern

```
SOVEREIGN: "Is X ready?"
  → PROBE: live check (curl /health, grep config, read file)
  → RECEIPT: raw data + honest verdict

SOVEREIGN: "What's the difference between A and B?"
  → PROBE: parallel comparison (both configs, both routing tables)
  → RECEIPT: side-by-side table + key insight

SOVEREIGN: "How does Y embed in Z?"
  → PROBE: trace the injection path (source → runtime → context window)
  → RECEIPT: architecture diagram + gap identification

SOVEREIGN: "Does W still exist?"
  → PROBE: live state check (MCP resources, docker, systemd, code)
  → RECEIPT: evidence table (what's alive, what's dead, what's partial)

SOVEREIGN: "How to wire it properly?"
  → CLASSIFY: map current state to action tiers
  → RECEIPT: 3-tier action table (verify → test → sovereign-level)
```

## Key Differences from One-Shot Integration Recon

| Aspect | One-Shot Recon | Chain-Probe Audit |
|---|---|---|
| Direction | Agent-led (agent maps the pipeline) | Sovereign-led (sovereign decides depth) |
| Scope | Single pipeline or integration point | Multi-layer federation state |
| Evidence | Single pass + reference file | Cumulative across turns |
| Output | Wiring recipe + gap ledger | Architecture understanding + gap map |
| Trigger | "How does X work?" | "Is X ready? What's the difference? How does Y embed?" |

## Probe Methods (Tiered)

| Tier | Method | When |
|---|---|---|
| T0 | `curl /health`, `ss -tlnp`, `docker ps` | Quick state check |
| T0 | `grep -rn`, `cat`, `find` | File/config existence |
| T1 | `curl /v1/models`, MCP `resources/read` | API surface verification |
| T1 | `python3 -c "import json; ..."` live probe | Runtime behavior verification |
| T2 | Full pytest run against target | Integration test |
| T2 | `arif_init` → tool call chain | End-to-end federation path |

## Anti-Patterns

- **Don't narrate observations before receipts.** SOVEREIGN expects probe results first, analysis second. Receipts → prose, never prose → receipts.
- **Don't speculate when probe is possible.** "I think X routes to Y" without curl = fabricate risk. Run the probe.
- **Don't stop at one layer.** Chain probes are DEEP by design. If sovereign asks about model identity, check litellm config, not just the model name.
- **Don't treat partial as complete.** If MCP probe fails, say "probe failed" not "it's down." Different things.
- **Don't classify before evidence.** Classification (drift vs divergence vs convergence) comes AFTER all probes complete, not during.

## Findings from 2026-08-12 Session (Arif Fazil Audit Chain)

### i-ARIF Model Identity
- `i-arif` is a litellm alias, NOT a fine-tuned model
- Routes to MiMo V2.5 (primary), Qwen 3.8-max (fallback)
- `hermes-asi` shares the SAME fallback chain
- Difference: identity layer (SOUL.md + AGENTS.md + memory), not model weights
- i-arif-qualia: GLM-5.2 (Z.ai) — separate provider (Gödel E3 diversity)

### Memory Embedding Architecture
- Memory is prompt-layer injection only (no RAG, no fine-tuning, no vector embedding of personal data)
- 3 layers: System Prompt (fixed) → User Profile + Memory (dynamic) → Lane Context (per-person)
- Char limits: memory 6000, user 3000, transient 4000
- Model weights have ZERO inherent knowledge of Arif Fazil

### ATLAS333 Wiring Status
- EXISTS as cognitive geometry substrate in arifOS kernel (:8088)
- MCP resources: `arifos://atlas333/*` (INDEX, paradox/list, zones, organs, thresholds, activation)
- Code: `/root/arifOS/arifosmcp/resources/atlas333.py` (720 lines)
- NOT a separate service — embedded in kernel
- Boot injection: `_atlas333_boot_context()` in every `arif_init`
- Live MCP probe failed (2026-08-12) — possible session binding or interface drift

### Taxonomy: Drift vs Divergence vs Convergence vs Federation vs Eureka vs Memory vs Dream

| Concept | arifOS Definition | Indicator |
|---|---|---|
| DRIFT | Canonical declares, runtime diverges | `aaa_drift_check.py` exit 2 = HOLD |
| DIVERGENCE | Bilateral split (source vs runtime) | `source_commit ≠ deployed_commit` |
| CONVERGENCE | Strands align, reality contact achieved | Eureka margin closed IDs |
| FEDERATION | Multi-agent coordination through constitutional contract | Active A2A mesh, SCT calls |
| QUANTUM EUREKA | Paradox resolution without collapse | APEX-G reflection R1-R6 |
| MEMORY | Double helix H↔L, scars/ECHO/ATLAS | `/root/HERMES/profiles/*/memories/` |
| DREAM | Nightly consolidation episodic → canon | Dream engine scheduled batch |

## Pitfalls

- **Probe failure ≠ system down.** MCP probe can fail due to session binding (F13 DEPLOYMENT_DRIFT), protocol mismatch (MCP 2026-07-28 vs 2025-11-25), or auth gate. Classify the failure before declaring state.
- **Cumulative context = cumulative assumptions.** Each answer builds on the previous. If a prior answer was partial/wrong, the chain inherits the error. Re-probe when switching from one topic to a related one.
- **Classification is output, not input.** Don't label "this is drift" mid-probe. Complete all probes, then classify.
