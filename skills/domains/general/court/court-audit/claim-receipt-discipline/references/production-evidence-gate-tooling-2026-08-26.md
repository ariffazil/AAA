# Production Evidence Gate Tools (Catalog — 2026-08-26)

## Purpose

Companion to FM13 (Snippet-to-Narrative Collapse) and `synthesis-verification-gate` skill.
Production tooling that enforces "don't say what you can't prove" at the code level —
not via prompt rules. These are the structural solutions FM13 identified as needed.

---

## Tool 1: AgentClaimGuard — Drop-in Claim Gate

**URL:** https://github.com/konoeph/AgentClaimGuard | **Install:** `pip install agentclaimguard`
**License:** Apache 2.0
**Adapters:** LangGraph, LangChain, Dify, DSPy, RAGFlow
**Core motto:** "No evidence, no claim. No tool result, no numeric conclusion. No source, no compliance judgment."

### How it works

Claims are structured Pydantic objects with explicit evidence/tool-result references.
A policy (YAML) defines per-claim-type requirements: minimum evidence counts, forbidden
patterns, and fallback verdicts. Claims that don't satisfy the policy are BLOCKED with
a safe fallback verdict — they never reach the user.

### Key schema

```python
# Core claim model
class Claim(BaseModel):
    id: str
    text: str
    type: str                    # "numeric_conclusion", "citation_required_answer", etc.
    verdict: str | None = None
    evidence_refs: list[str]     # References to evidence items
    tool_result_refs: list[str]  # References to tool outputs
    confidence: float | None     # 0.0-1.0
```

### Example: blocking an unsupported numeric claim

```python
from agentclaimguard import AgentClaimGuard, Policy

claims = [
    {
        "id": "claim_1",
        "type": "numeric_conclusion",
        "text": "Revenue increased by 15%.",
        "evidence_refs": ["ev_1", "ev_2"],
        "tool_result_refs": [],  # No calculator result → BLOCKED
    }
]
evidence = [
    {"id": "ev_1", "type": "retrieved_context", "content": "Revenue was 100M last year."}
]
# Result: status=blocked, claim_status=tool_required, safe_verdict=insufficient_evidence
```

### Policy YAML

```yaml
name: generic_rag
claim_types:
  citation_required_answer:
    required_evidence:
      - type: retrieved_context
        min_count: 1
    forbidden: [answer_without_citation]
    fallback:
      verdict: insufficient_evidence
      reason: "Answers must cite retrieved context."
```

### Built-in validators

| Validator | What it checks |
|---|---|
| `evidence_required.py` | Minimum evidence count per type |
| `citation_binding.py` | Claims tied to source citations |
| `tool_required.py` | Numeric claims without calculator/tool results |
| `conflict_check.py` | Contradictory evidence detection |
| `forbidden_verdict.py` | Policy-enforced forbidden claim patterns |

### Best for

General LLM agent output gating. Drop-in for any RAG/tool-use pipeline.

---

## Tool 2: SARC-DQ — Academic Foundation (Pre-Action Evidence Gate)

**URL:** https://github.com/besanson/dqSarc | **Paper:** https://arxiv.org/abs/2607.26313
**License:** Apache 2.0
**Status:** Research artifact, 30 pre-registered seeds, deterministic analysis pipeline.

### Core thesis

"Enforcement placement beats model intelligence." A metadata-aware Pre-Action Gate
at the point of action, with downstream-only remediation. Paper proves: across 4 model
tiers spanning ~15x inference price, metadata-borne defect conversion rate stays flat.
**Capability does not buy skepticism.**

### Payload/metadata split (the key insight)

```python
@dataclass(frozen=True)
class RecordMetadata:
    source: str            # "erp.pricing"
    as_of_day: int         # day the value was valid
    retrieved_day: int     # day agent read it
    version: int = 1
    lineage: tuple[str, ...] = ()

@dataclass(frozen=True)
class EvidenceRecord:
    record_id: str
    payload: dict[str, Any]     # What the agent SEES
    metadata: RecordMetadata    # What the agent CANNOT SEE
    # ground_truth is NEVER shown to any agent
```

The defect (stale price, superseded record) lives in metadata — invisible to the agent's
context window. The agent acts on it confidently because it literally cannot see the defect.

### Predicate-based gate config (YAML)

```yaml
constraints:
  - id: c_freshness
    class: hard
    response: quarantine_substitute
    predicate:
      name: freshness
      params: { max_age_days: 30 }
    targets: [stale_master_data]   # metadata-borne

  - id: c_schema
    class: hard
    response: block
    predicate: { name: schema_conformant }
    targets: [schema_drift]        # payload-visible

  - id: c_cross_source
    class: escalation
    response: escalate
    predicate:
      name: cross_source_consistent
      params: { tolerance: 0.02 }
    targets: [cross_source_contradiction]  # payload-visible
```

### Response protocol

| Response | Meaning |
|---|---|
| `block` | Action refused entirely |
| `degrade` | Autonomy degraded to conservative default |
| `escalate` | Routed to human (no autonomous execution) |
| `quarantine_substitute` | Offending value quarantined; known-good value substituted from governed buffer |

### Best for

Systems where evidence quality (freshness, schema, cross-source consistency) is the
primary concern. Enterprise data pipelines, financial decision agents, procurement bots.

---

## Tool 3: Xenon — Evidence Runtime (Code Agent)

**URL:** https://github.com/xianyu-sheng/Xenon
**License:** MIT
**SWE-bench:** 40.0% instance-level pass rate (+6.7pp over same model without harness)

### Core principle

**Tool results = Evidence. LLM outputs = Claims.** Enforced separation at code level.
The Evidence Runtime ensures LLM output (Claims) cannot override tool output (Evidence)
without passing verification gates.

### 5-layer responsibility model

| Layer | Responsibility |
|---|---|
| Inference | 7 interchangeable reasoning paradigms |
| Tools | Side effects recorded, 7-stage pipeline |
| Constraints | Path fencing + permission gates + injection interception |
| **Verification** | **Evidence Runtime: tool results = Evidence, LLM = Claim** |
| Measurement | SWE-bench harness + same-model A/B + seed persistence |

### Best for

Coding agents, tool-use agents, any system where tool outputs should be the
ground truth and LLM outputs need verification.

---

## Tool 4: Swarm Orchestrator — Anti-Gaming Evidence Ledger

**URL:** https://github.com/moonrunnerkc/swarm-orchestrator
**Install:** `npm install swarm-orchestrator`

### Core guarantee

"The model can say whatever it likes. It cannot make a gate pass, it cannot mark a
claim verified, and it cannot change a record after the fact. Those are the harness's
to decide, and the run exports a signed, hash-chained bundle that anybody can check
without installing this tool."

### Key mechanisms

1. **Hash-chained append-only ledger** — Every tool call, gate evaluation, claim
   immutably recorded
2. **Numeric ratchet** — Retries failures with a ratchet that REFUSES a fix which
   trades away tests, assertions, or coverage (prevents gate-gaming)
3. **Signed bundle** — Export a signed, hash-chained bundle anyone can verify offline
4. **Chokepoint recording** — All edits go through a chokepoint recording every tool call

### The ratchet anti-pattern it prevents

```
gate_fail → retry → new claim → gate_fail → retry with DIFFERENT approach
     (ratchet REFUSES approach that reduces test/coverage metrics)
```

### Best for

Coding agents where audit trails and anti-gaming are critical. Systems where you
need a verifiable chain from claim → evidence → gate → outcome.

---

## Tool 5: Evidence Gate Action — Blind Gates for CI/CD

**URL:** https://github.com/evidence-gate/evidence-gate-action | https://evidence-gate.dev/
**Install:** GitHub Action (uses: evidence-gate/evidence-gate-action@v1)
**29 gate types** | Free for open-source

### The Blind Gate insight

"When an LLM writes your code AND your tests, every visible threshold becomes a
target to optimize against — not a quality standard to meet."

### How it works

Evidence Gate API evaluates criteria **server-side** against private criteria.
The pipeline — and the AI agent driving it — only receives pass or fail.
**Never the criteria themselves.**

```yaml
uses: evidence-gate/evidence-gate-action@v1
with:
  gate_type: "nemoclaw_blueprint"
  phase_id: "deploy"
  evidence_files: "blueprint.yaml"
```

### Trust Levels (L1-L4)

| Level | Name | Definition |
|---|---|---|
| L1 | Declaration | Pipeline claims something happened |
| L2 | Attestation | Third party confirms the claim |
| L3 | Verification | Claim is independently reproducible |
| L4 | Proven | Cryptographically verified |

### Enforcement modes

| Mode | Behavior |
|---|---|
| `enforce` | Block on gate failure (default) |
| `warn` | Emit warnings but step succeeds |
| `observe` | Shadow mode — log results without blocking |

### Best for

CI/CD pipelines, infrastructure governance, any system where AI agents produce
artifacts that need quality gates but you can't let the agent see the thresholds.

---

## Pattern Summary

| Tool | Pattern | Key Innovation |
|---|---|---|
| AgentClaimGuard | Claim schema + policy YAML | Drop-in; Pydantic claims + YAML policy |
| SARC-DQ | Metadata predicates + governed buffer | Payload/metadata split; model capability doesn't buy skepticism |
| Xenon | Evidence/Claim type separation | Tool output = Evidence, LLM = Claim, code-enforced |
| Swarm Orchestrator | Ratchet + immutable ledger | Anti-gaming via numeric ratchet; signed offline-verifiable bundles |
| Evidence Gate Action | Blind Gates + CI/CD | Criteria hidden from AI agent; only pass/fail exposed |

### Common architecture

All five enforce evidence-before-synthesis **structurally**, not via prompt rules.
The key insight from SARC-DQ applies to all: enforcement placement beats model intelligence.

---

## Mapping to arifOS constitutional floors

| Floor | How tools enforce it |
|---|---|
| F2 TRUTH | AgentClaimGuard blocks unsupported claims; SARC-DQ catches stale data |
| F4 CLARITY | Separated claim/evidence schemas prevent narrative confusion |
| F7 HUMILITY | Confidence caps in Claim schema; abstention as default |
| F9 ANTI-HANTU | Structured verification prevents hallucination from reaching output |
| F11 AUDIT | Swarm Orchestrator hash-chain; Evidence Gate SHA-256 chains |
| F9/F12 | Synthetic output gate (the F9/F12 philosophy) → structural enforcement |

---

## Research references (supporting this catalog)

- Besanson, "SARC-DQ: Runtime Data-Quality Gating for Agentic AI," arXiv:2607.26313 (2026)
- Besanson, "One Gate Is Not Enough: Composing Stateful Pre-Action Controls for Agentic AI," arXiv:2608.18360 (2026)
- Asai et al., "Self-RAG: Learning to Retrieve, Generate and Critique through Self-Reflection," ICLR 2024
- "Lessons from Training Grounded LLMs with Verifiable Rewards," arXiv:2506.15522 (2025)
- "Enhancing Factual Accuracy and Citation Generation in LLMs via Multi-Stage Self-Verification," arXiv:2509.05741 (2025)
- Arthur AI, "Agent Guardrails: Pre-LLM & Post-LLM Best Practices," Apr 2026
