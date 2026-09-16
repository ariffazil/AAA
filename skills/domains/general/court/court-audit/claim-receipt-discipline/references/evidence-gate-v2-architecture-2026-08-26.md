# Evidence Gate v2 — Architecture & 8-Defect Fix (2026-08-26)

## What was built

`/opt/arifos/app/arifosmcp/runtime/evidence_gate.py` (463→~520 lines, fail-closed v2)

## Pipeline position

```
LLM response → wrap_llm_output() → _make_envelope() → gate_envelope() → envelope
```

Wired in `_make_envelope()` at `llm_client.py:385-404`. Every LLM call flows through here.

## 8 defects fixed (from Arif's audit of v1)

| # | Defect | v1 (advisory) | v2 (fail-closed) |
|---|---|---|---|
| 1 | Lexical overlap = evidence | keyword overlap between claim words and prompt words | Ollama nomic-embed-text semantic similarity (cosine ≥0.55) |
| 2 | URL+citation = verified | `has_url and has_citation → verified` | URL+citation = `cited`. `verified` requires Gate 2 content match |
| 3 | One claim upgrades envelope | `if verified > 0 → upgraded = "verified"` | Material-claim ratio: `verified/total_material` must be ≥50% |
| 4 | Line-split = atomic | `text.split("\n")` per line | Sentence boundaries + clause-level (3+ verbs → split on `, and/but/or`) |
| 5 | No verdict | risk_flags only | `EvidenceGateResult.verdict` = PROCEED/WARN/HOLD/INSUFFICIENT |
| 6 | Fail-open | `except Exception: pass` | `except → HOLD envelope + risk_flag` |
| 7 | human_decision_required pre-gate | calculated in wrap_llm_output before gate | recalculated AFTER gate_envelope runs |
| 8 | Gate 3 not wired | `should_selfcheck()` existed, async not called | `selfcheck_resample()` async function, callable from call_llm |

## Key data classes

- `AtomicClaim`: single factual claim with evidence_level, source_verification, semantic_similarity
- `EvidenceGateResult`: complete gate output with verdict, coverage_ratio, human_decision_required
- `EvidenceVerdict`: PROCEED | WARN | HOLD | INSUFFICIENT_EVIDENCE

## Coverage thresholds

```python
COVERAGE_THRESHOLD_PROCEED = 0.70     # ≥70% → PROCEED
COVERAGE_THRESHOLD_WARN = 0.40        # ≥40% → WARN
COVERAGE_THRESHOLD_INSUFFICIENT = 0.20 # <20% → INSUFFICIENT_EVIDENCE
```

## Integration with ART pipeline

ART classifies: OBSERVE | REASON | DRAFT | MUTATE | DEPLOY | IRREVERSIBLE

Gate2 verdict maps to ART:
- PROCEED → normal flow
- WARN → risk_flag appended, envelope carries advisory
- HOLD → human_decision_required=True, ART should HOLD
- INSUFFICIENT_EVIDENCE → envelope.evidence_level="claimed", envelope forces HOLD

The gate doesn't block ART directly (that's a future ART gate.js integration). It enriches the envelope so downstream gates can enforce.

## Ollama dependency

Embeddings via `http://localhost:11434/api/embeddings` with model `nomic-embed-text` (768 dims).
Graceful fallback to keyword overlap if Ollama unavailable.
Local, zero-cost, ~50ms per embedding.

## What remains

1. Old 32 tests need rewriting (they import old API: decompose_and_classify, selfcheck_compare)
2. ART gate.js integration: classifyTextOutput() for Hermes prose output
3. Full integration test: LLM → envelope → gate → terminal end-to-end
