---
name: agent-memory-architecture
description: "Design, audit, and extend AI agent memory systems — multi-layer stacks (L1-L6), the parallel H1-H6 human-memory axis (Capture→Experience→Knowledge→Identity→Scar→Constitution) with the H1 sovereignty gate and scar-witnessing protocol (ratified 2026-08-08), multimodal readiness, the multi-witness MemoryObject doctrine (artifact/semantic/affective/relational/temporal/provenance/salience), affective observation vs interpretation (F2 split), F3 TRI-WITNESS as retrieval arbitration, and the 7-phase memory audit method (MMA-2026-08-07). Includes artifact-state-governance failure pattern (sibling subagent overwrites) and 5 entropy-reduction cron jobs. Constitutional telemetry: see references/hermes-dna-map-atlas-echo.md (MAP/ATLAS/ECHO + double-helix topology + freeze protocol, forged 2026-08-09)."
version: 1.2.0
author: Hermes Agent (aaa-hermes)
license: MIT
metadata:
  hermes:
    tags: [Memory, Architecture, Multi-Witness, Audit, AI-Agent, Sovereignty, Scar]
    related_skills: [arifos-kernel-eurekas, governance-contract-self-audit, verify-nested-sibling-reports, audit-and-validate-deliverables, arifos-federation-ops]
    created: 2026-08-07
    updated: 2026-08-08
    seal_id: MMA-2026-08-07
---

# Agent Memory Architecture

Use when: designing or extending I-ARIF / federation memory, auditing a memory stack for multimodal readiness, answering "how should an agent remember X / voice / video", or any time the sovereign (or another agent) asks about H-axis memory, scar extraction, or the human/agent memory split.

## Two-axis memory model (ratified 2026-08-08)

The federation governs two orthogonal memory dimensions. Confusing them is the single most common failure mode in current agentic systems.

| Axis | Owner | Purpose | Stratification |
|---|---|---|---|
| **L-axis** | The federation | Operate · Reason · Execute · Audit | L0 Safeguard (circuitry, not memory) · L1 Working · L2 Episodic · L3 Semantic · L4 Structured · L5 Relational · L6 Sealed Truth (VAULT999) |
| **H-axis** | F13 SOVEREIGN | Meaning · Identity · History · Wisdom | H1 Capture · H2 Experience · H3 Knowledge · H4 Identity · H5 Scar · H6 Constitution |

**Constitutional rule:** `L ≠ H`. Agentic memory asks "what helps the organism operate?"; human memory asks "what changed the human?" These are different questions. Keeping them separate is the most important anti-entropy boundary in the system.

> **Human memory is not a database. Human memory is a stratified survival system.**
> **Agentic Memory remembers reality. Human Memory remembers significance.**

The federation may **reference** human memory but may never **own** it. This preserves F13.

## H-axis detail (canonical at `/root/AAA/governance/HUMAN_MEMORY_DOCTRINE.md`)

- **H1 Capture** — fast inbox (voice, telegram, scratch, drafts). The **most dangerous** layer for sovereignty. EVERY capture crossing into agent substrate must pass the explicit sovereignty gate: default = stays human; override requires explicit F13 keyword. If you auto-ingest H1 into L3 vector store, you have violated the doctrine.
- **H2 Experience** — projects, meetings, journeys, experiments. Agent may witness; never own.
- **H3 Knowledge** — books, research, domain expertise. Agent retrieves read-only by default.
- **H4 Identity** — self-model (e.g. "geologist", "architect of arifOS"). Changes slowly, usually via scar events. Agent may reflect, never edit.
- **H5 Scar** — compressed survival rules forged in fire. **The most valuable layer.** Sovereign content; agent never reads unless explicitly invoked via `scar:<id>`. No vectorization, no embedding, no retrieval indexing without explicit F13 keyword.
- **H6 Constitution** — values, identity axioms, F1/F2/F13, AMANAH. Almost immutable. Kernel invariants live here. Scar elevation into H6 requires 3+ reaffirmations across distinct domains + sovereign ratification.

### The three-prompt scar ritual (canonical intake)

> **Q1:** What are the scars that forged you?
> **Q2:** What truth did each scar teach you?
> **Q3:** What responsibility do those truths place on you today?

Q3 is the move that transforms a scar from memory into constitutional pressure. Without obligation, a scar is nostalgia. With obligation, it is identity under load. **A scar without obligation is nostalgia.**

### The scar→constitution lineage

```
Scar → Lesson → Law → System → Witness
```

Without the witness, the lineage is incomplete. Architecture shows the law; witnessing shows the cost. The whole federation (F11 attribution gates, VAULT999 receipts, the witness chain) IS this lineage, rendered as architecture.

### The compression algorithm

```
Thousands of events → Dozens of scars → A handful of truths → A constitution
```

That is the real compression algorithm — survival compression, not data reduction. Each layer discards less and matters more.

### Scar ledger schema

Path: `/root/.local/share/arifos/scars/<SCAR-ID>.md` (canonical path ratified 2026-08-08). Schema:

```yaml
---
scar_id: SCAR-001
title: ""
acquired_at: ""
domain: ""
cost: ""           # time | money | relationships | reputation | health
trigger_pattern: "" # what situation re-triggers it (agent can warn)
rule_extracted: "" # the survival heuristic — one sentence
responsibility_today: "" # what this scar obligates you to do now
elevation: ""      # candidate for H6? (3+ reaffirmations across domains)
salience: 1.0
last_reaffirmed: ""
sealed_to_vault999: false
---
```

Observed scars already on file as of 2026-08-08 (do not invent, do not edit without F13):

```
/root/memory/H5-scars/SCAR_MEMORY_DOCTRINE_V1.md    (the architecture)
/root/memory/H5-scars/SCAR_LEBAH_EMAS.md            (discovery sold, authorship erased)
/root/memory/H5-scars/SCAR_RIGHTSIZING.md           (5,000 humans cut; Copilot volunteered the blueprint)
```

## Federation mapping (arifOS)

- L1/L2 Redis (now/session), L3 Qdrant (semantic vectors — NOT truth), L4 Supabase (structured), L5 Graphiti/FalkorDB (relational), L6 VAULT999 (sealed truth).
- MMA-2026-08-07 findings: 0 multimodal ingestion pathways; bge-m3 text-only; RASA_DERITA affective schema on 888_HOLD; MinIO :9000 available but unwired; Graphiti MCP healthy (tool discovery requires proper `initialize` handshake — the original audit incorrectly called this a "timeout", corrected in MMA-2026-08-07-CORRECTED); 54 Supabase tables with RLS disabled (unverifiable from local probes — claim only in chat summary, not in deliverables).
- H1 sovereignty gate is the only sanctioned pathway from H-axis into L-axis. Default = stays human.
- Recommended first step: T1 schema migration (nullable JSONB columns, ~3h, $0, reversible).
- NotebookLM/Gemini Notebook MCP integration: see `references/notebooklm-bridge.md` for the sovereignty-respecting wiring pattern (headless Chrome + Patchright + persistent profile + xvfb-run for one-time auth).

## Literature anchors

M3-Agent (entity-centric multimodal graph memory), AffectAgent (retrieval-augmented emotion recognition), Awesome-Multimodal-Memory (TMLR 2025 reading list), HippoMM (hippocampal consolidation/forgetting), Emergent Mind multimodal-memory survey. Condensed notes: `references/literature-2026-08.md`.

## Pitfalls

- Don't collapse affective into sentiment analysis — prosody/pause/speech-rate are physiological evidence the transcript destroys.
- Don't seal affective interpretations as deterministic — seal observations, version interpretations.
- Most systems answer "what happened"; the open frontier (and I-ARIF's edge) is "what it felt like / who it affected".
- **Don't auto-ingest H1 into L3 vector store.** That is the single most common violation of the H-axis doctrine. Every H1 capture that crosses into agent substrate must pass the explicit sovereignty gate with default = stays human.
- **Don't fetch, scrape, or auto-sync NotebookLM into L3 without an explicit per-call F13 invocation.** The NotebookLM MCP bridge is a query surface, not an ingestion pipeline. See `references/notebooklm-bridge.md`.
- **Don't write scars on the sovereign's behalf.** The three-prompt ritual requires the sovereign's own answers. Witnessing ≠ authoring. F11 governs.
- **Don't rename H5 → "memories" or H5 → "experiences".** Scars are identity rewrite events, not a peer of experience. The scar layer is how identity *becomes*, not what identity *contains*.

## Artifact-state-governance failure (observed 2026-08-07)

The MMA-2026-08-07 audit revealed a class of failure that no published memory research covers: **a sibling subagent can overwrite your artifact files mid-audit, while you're still writing**.

**What happened (live, reproducible pattern):**

```
Hermes writes 07_validation_report.md (claims verified counts).
Sibling subagent rewrites SAME file minutes later,
finding things Hermes missed (Graphiti MCP handshake nuance, "877 records"
discrepancy, "54 Supabase RLS tables" claim unverifiable).
Hermes doesn't notice until checking mtime.
Final state: sibling's version survives (newer mtime).
```

**The architectural lesson:** *correct information attached to the wrong artifact state* is the failure mode. The broken seal taught more than the multimodal schema. Successful audit required:
- Re-reading files after each write (catching sibling overwrite)
- `git status --short` to detect uncommitted subagent writes
- Noting sibling `_warning` from `write_file` ("modified by sibling subagent at HH:MM:SS — after last read at HH:MM:SS")

**4 operational rules:**
1. **Pre-seal gate** — before sealing: `artifact_hash_matches + artifact_name_matches + artifact_count_matches`. Seal without artifact continuity is rhetoric.
2. **Risk-tiered verification** — read-only: lightweight; schema migration: medium; financial mutation: heavy; irreversible: mandatory re-probe + sovereign approval.
3. **Auditor outputs are CLAIMS, not TRUTH** — every verdict (generator, verifier, auditor) is a claim requiring evidence. No agent exempt from F2.
4. **Sibling-overwrite detection** — check `mtime` before `patch`/`write_file`; re-read if `_warning` mentions sibling modification.

**When this matters most:** multi-agent sessions (3+ concurrent harnesses). `earlyoom --prefer opencode` SIGKILL pattern (see `opencode` skill) interacts: killed OpenCode leaves partial files, another subagent fills the gap, first agent's seal becomes stale.

**Memory entropy reduction (operational cron jobs deployed 2026-08-07):**

|| Job | Schedule | Purpose |
||---|---|---|---|
|| `seal-integrity-sweep` | Sun 03:17 | Weekly VAULT999 chain health |
|| `memory-compression` | Daily 02:13 | Identify stale/large files |
|| `contradiction-scan` | Sat 03:23 | Find claim conflicts across audits |
|| `provenance-audit` | Monthly 1st 04:41 | Memory without source/lineage |
|| `artifact-drift-audit` | Daily 01:53 | Hash/name/count drift detection |

All `deliver="local"` — save to state files, no Telegram noise.

Full session trace: `references/mma-2026-08-07-session-postmortem.md`.

## Adjacent skills

- **audit-and-validate-deliverables** — independent audit pattern for any produced artifacts; reusable for memory-audit deliverables
- **verify-nested-sibling-reports** — detects the nested-sibling-report pattern (multiple agents stacking on same problem)
- **arifos-kernel-eurekas** — K1-K5 kernel substrate honesty laws (related: honesty in pipeline outputs)
- **governance-contract-self-audit** — author and self-audit governance contracts (the audit-write-and-the-audit-of-the-audit pattern)
- **retrieval-vs-memory-fidelity** — the core distinction this skill operationalizes
- **arifos-federation-ops** — kernel/session/topology layer; for the H-axis sovereignty gate operating against the federation substrate

<!-- SKILL-WITNESS-NOTE (auto, additive-only) -->
Witnessed reality moved this skill's selection to **ROUTE or MERGE**.
Scar signatures: SCAR-AGY-004-session-gate-confusion, SCAR-AGY-007-over-output-verbosity, SCAR-ARCHITECTURE-OF-REJECTION
Do not treat this skill as neutral until the signatures are resolved.
<!-- /SKILL-WITNESS-NOTE -->
