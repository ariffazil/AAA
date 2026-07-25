---
id: FLAME-router
name: FLAME-router
version: "2026.07.25"
description: >
  Classify inference work into the stateless FLAME tool lane or the governed
  constitutional agent lane, with Arif-ratified division of labor (2026-07-24)
  and L3 Task-Routing doctrine (2026-07-25).
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope:
  - F1
  - F2
  - F4
  - F9
  - F13
---
# 🔥 FLAME-router — Tool Lane vs Agent Lane Routing

> **Skill ID:** FLAME-router · **Version:** 2026.07.25 · **Axis:** routing
> **Ratified:** 2026-07-24 by Arif (F13 SOVEREIGN)
> **Upgraded:** 2026-07-25 — 4-core insight doctrine from Mage-Flow architecture session
> **Load when:** Any agent needs to decide between FLAME (tool lane) and constitutional cascade (agent lane).
> **Do NOT load for:** Constitutional judgment, SEAL/HOLD decisions, human-facing responses.

## The Clean Division of Labor (Arif-ratified 2026-07-24)

| Layer | Role | Model Tier |
|---|---|---|
| **FLAME** | Tools, workers, fallback throughput | Free/cheap, tiered by availability, disposable |
| **Hermes** | Epistemic/human-life reasoning | Premium, high-effort, reasoning-preserved |
| **OpenCode** | Execution/coding actuation | Budget-to-premium depending on task complexity |
| **arifOS** | Judgment, audit, sealing | Policy logic — not a model tier at all |

## What FLAME Answers

```
"Can something respond right now, cheaply, without breaking rate limits?"
```

FLAME **never** answers: "Is this answer true or authorized?"

## The Two-Lane Rule

```
TOOL LANE (FLAME):     Tools, workers, batch jobs, classifiers, embedders.
                       Cascading availability ladder — 12 tiers.
                       RM0. Hit-rate adaptive. ADVISORY output only.
                       Zero constitutional authority.

AGENT LANE (cascade):  Agents, reasoning, judgment, governance.
                       TokenRouter→MiniMax→MiMo→Groq→Gemini→Cerebras→SEA-LION→Ollama→HOLD.
                       F1-F13 gated. Constitutional.
```

---

## ⚔️ FOUR-CORE INSIGHT DOCTRINE (2026-07-25)

> Forged from Mage-Flow architecture session. These are structural constraints,
> not tips. Every FLAME agent MUST internalize these before routing any inference.

### 1. PROFILE > PING — Task Fitness Over Latency

**The Trap:** Agents default to `min(latency)` — pick the fastest model.

**The Law:** Route by `max(task_fitness)` first, then `min(cost)` second.

| Task | Profile Requirement | Best Model (not fastest) | Why |
|---|---|---|---|
| Classification | Deterministic, schema-strict | Groq 8B / MiniMax-M3 | JSON-native output |
| Summarization (large) | 1M context window | Gemini flash-lite | Avoid chunking entropy |
| BM-native content | Bahasa Malaysia fluency | SEA-LION Qwen v4 | Tokenizer trained on BM |
| Contradiction scan | Deep reasoning, multi-hop | Groq 70B / Sambanova DeepSeek | Logical chains |
| Code generation | Fill-in-middle, syntax | Codestral / Qwen 3.6 | Code-native tokenizer |
| Gap-fill (rare models) | Unique free-tier access | OpenRouter :free aggregator | Models FLAME can't reach directly |

**Enforcement:** `TASK_CLASS_CHAINS` in `flame_router.py` reorders tiers at call-time.
Agents must pass `task_class` parameter when calling FLAME.

**Anti-pattern:** `flame.call(prompt)` without `task_class` → suboptimal routing.
**Correct:** `flame.call(prompt, task_class="classification")` or `task_class="bm_malay"`.

### 2. IDLE = HARAM — Zero-Idle-Cost Is a Constitutional Gate

**The Trap:** Agents see "$0.90/hr GPU = cheap" and recommend Hugging Face Endpoints.

**The Law:** `W_scar` (financial risk to 888) is an absolute variable. If a GPU sits idle
23 hours/day at $0.90/hr, that's $648/month wasted — a direct F1 AMANAH violation.

**Enforcement:**
- `scale-to-zero` and `zero idle cost` are HARD REQUIREMENTS for any external GPU integration
- Agents proposing GPU infrastructure MUST compute `W_scar = idle_hours_per_day × hourly_cost × 30`
- If `W_scar > $10/month`, the proposal is INADMISSIBLE
- Exception: only if a hard auto-pause mechanism (not a prompt, not a config — executable code)
  guarantees zero billing during idle

**Approved pattern:** Modal.com serverless GPU (pay-per-second, $0 idle)
**Rejected pattern:** Hugging Face Endpoints (pay-per-hour, continuous billing)
**Rejected pattern:** AWS SageMaker real-time endpoint (pay-per-instance, continuous)

### 3. PHYSICAL DEFENSE — Code, Not Prompts

**The Trap:** Security boundaries enforced via system prompt or LLM behavior.

**The Law:** Every security boundary between FLAME and governed surfaces MUST be
hardcoded in executable code — not documented, not prompted, not configured.

**The Zero-Fly Zone (implemented in `flame_router.py:ZeroFlyZone`):**

```
Layer 1 — CALLER IDENTITY GATE (hardcoded set):
  arif_judge, arif_seal, arif_init, arif_forge
  well_assess_homeostasis, well_validate_vitality, well_guard_dignity
  capital_wisdom, capital_diagnose, capital_ledger
  → REJECT before HTTP. No configuration can override.

Layer 2 — VERB PATTERN GATE (hardcoded patterns):
  "arif_judge", "arif_seal", "well_", "forge_execute",
  "forge_approve", "forge_seal", "forge_vault", "forge_lock"
  → Pattern match on caller_id. Immediate REJECT.

Layer 3 — CONTENT SENSITIVITY GATE (hardcoded triggers):
  "mykad", "nric", "petronas internal", "password:", "token:"
  → SOVEREIGN data NEVER leaves VPS through FLAME.
```

**Why this matters:** A model rotation or jailbreak cannot bypass hardcoded Python checks.
A system prompt can be ignored. A `set` lookup cannot.

**Current state:** 20 `FORBIDDEN_CALLERS` + 31 `FORBIDDEN_VERB_PATTERNS` + 17 `SOVEREIGN_CONTENT_TRIGGERS`.
All executed at line 1125 of `flame_router.py` — BEFORE any HTTP call.

### 4. BLIND CIRCUIT BREAKER — Provider-Specific Error Vocabulary

**The Trap:** Conventional `exponential backoff` on HTTP 429 — relies on standard headers.

**The Law:** When providers don't implement standard rate-limit headers (Cloudflare Workers AI,
MiniMax body codes), build provider-specific error vocabulary parsers. Read the response
BODY, not just the HTTP status code.

**Pattern:**
```python
PROVIDER_ERROR_VOCABULARY = {
    "cloudflare": {
        "rate_limit_body_codes": [3036, 1027],
        "auth_failure_codes": [10000],
    },
    "minimax": {
        "rate_limit_body_codes": [1004],
        "quota_exhausted_codes": [1008],
    },
}

def detect_rate_limit(provider: str, status_code: int, body: dict) -> bool:
    vocab = PROVIDER_ERROR_VOCABULARY.get(provider, {})
    rate_codes = vocab.get("rate_limit_body_codes", [])
    if status_code == 429:
        return True  # standard
    if body.get("code") in rate_codes:
        return True  # provider-specific
    return False
```

**Why this matters:** Exponential backoff on 429 is useless if the provider never sends
`Retry-After` or `RateLimit-Reset` headers. The circuit breaker must learn each provider's
unique error language.

**Current state:** FLAME's OpenRouter tier has 429 cooldown logic. Other providers
fall through to generic "HTTP != 200" → skip tier. Needs upgrade for body-code parsing.

---

## FLAME Tier Structure (2026-07-25)

Tiers are a cascading **availability ladder**, not a reasoning hierarchy. Higher tiers are more trusted/available — not "smarter." The chain exists so *something* always responds.

```
T1-T5:  Core — Groq (2 tiers) + SEA-LION (3 tiers) = fastest + BM-native
T6-T7:  Core — Gemini flash + Cerebras gemma = general + volume
T8-T10: Experimental — gpt-oss-120b variants (low-weight)
T11:    OpenRouter :free — gap-fill bridge (Cohere, InclusionAI, Poolside, NVIDIA)
T12:    Ollama qwen2.5-coder:3b — local survival knife
```

## Decision Matrix

| Task | Lane | Why |
|---|---|---|
| Summarize a log file | **FLAME** | No judgment needed |
| Classify 1000 documents | **FLAME** | Pure throughput |
| Generate embeddings | **FLAME** | Stateless transform |
| Non-binding fact check | **FLAME** | Advisory only |
| Plan safety review | **FLAME** | Advisory only |
| Geoscience evidence synthesis (non-seal) | **FLAME** | Compute, not judgment |
| Market signal interpretation | **FLAME** | Interpretation, never allocates |
| Reason about architecture | **Agent** | Needs constitutional grounding |
| Judge a constitutional question | **Agent** | arifOS 666_JUDGE domain |
| Respond to Arif | **Agent** | Human-facing, governed |
| Execute a forge mutation | **Agent** | Lease + judge required |
| Epistemic/human-life reasoning | **Agent** | Hermes premium reasoning domain |
| Seal to VAULT999 | **Agent** | arifOS 999_SEAL domain |

## Task-Class Chains (reorder tiers by task type)

```bash
flame --task-class coding "Write a function to..."
flame --task-class bm_malay "Terangkan maksud..."  
flame --task-class gap_fill "Query needing unique free model"
```

| Task Class | Preferred Tiers | Why |
|---|---|---|
| `coding` | Groq 70B → OR → Cerebras | Deep reasoning first |
| `epistemic` | Groq 70B → Gemini | Reasoning + context |
| `bm_malay` | SEA-LION Qwen → SEA-LION Llama | BM-native priority |
| `classification` | Groq 8B → MiniMax M3 → Gemini Lite | Deterministic, JSON-native |
| `summarization` | Gemini flash-lite → Groq 70B | 1M context, no chunking |
| `extraction` | MiniMax M3 → Qwen 3.6 | JSON-native, precise |
| `contradiction` | Groq 70B → Sambanova DeepSeek | Deep reasoning |
| `evidence_synthesis` | Groq 70B → Mistral Nemo → Gemini | Fluent synthesis |
| `gap_fill` | OpenRouter only | Models FLAME can't reach directly |
| `destructive` | **NEVER FLAME** | Governed cascade only |

## Constitutional Boundary

**FLAME NEVER:**
- Judges (arifOS only — `GOVERNED_USE["constitutional_judgment"]`)
- Seals (VAULT999 only — `GOVERNED_USE["constitutional_seal"]`)
- Primary epistemic reasoning (Hermes domain)
- Human-life/substrate reasoning (WELL domain)
- Sovereign data (PII, myKad, PETRONAS — SENSITIVITY hard gate)
- Execution authorization (A-FORGE lease domain)
- Uses paid models (RM0 hard gate)
- Uses OpenRouter auto/auto-beta router (F11 AUDITABILITY violation)
- Routes agent work (use agent cascade)

**FLAME ONLY:**
- Advisory, classification, extraction, summarization, embedding
- Stateless text → transform → output
- ADVISORY authority — consumers MUST validate
- Emergency fallback when governed cascade exhausted

## FLAME Commands

```bash
free-llm "prompt"                          # Single inference
free-llm --mode probe                      # Health check all 12 tiers
free-llm --mode stats                      # Hit-rate dashboard
free-llm --mode snapshot-checksum          # Integrity hash
free-llm --batch file.txt                  # Batch processing
free-llm --task-class coding "prompt"      # Task-class chain reorder
free-llm --sensitivity PUBLIC "prompt"     # Declare data sensitivity
free-llm --caller hermes_fact_check "..."  # Caller identity for audit
```

## ATLAS333 Context

FLAME activates 8 ATLAS333 paradoxes (Memory: M6,M7,M8 · Mind: R1,R4,R7 · Contour: C1,C2). Key tensions: speed vs. quality (R1), stability vs. reordering (M6), free access vs. constitutional boundary (C1).

## When FLAME returns HOLD

1. Try agent lane cascade (may have different model availability)
2. Check FLAME health: `free-llm --mode probe`
3. Check hit-rates: `free-llm --mode stats`
4. If all tiers exhausted: escalate to agent lane with degraded flag

## Reference

- Implementation: `/root/A-FORGE/flame/flame_router.py` (2015 lines)
- Zero-Fly Zone: `ZeroFlyZone` class, lines 240-416 — executable constitutional law
- Task-class chains: `TASK_CLASS_CHAINS`, lines 421-492
- Full surface map: `/root/HERMES/skills/devops/flame-free-loop-mesh/references/81-surface-flame-map.md`
