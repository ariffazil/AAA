# Harness Intelligence Map

> ETCSOVG harness disclosure taxonomy × arifOS constitutional architecture.
> The harness IS the performance variable. The model is the policy it governs.

## Source

**Paper:** Zhang et al. 2026, "The Harness Problem" (arxiv 2605.23950)
**Core finding:** Harness-induced variance 7.8× model-induced variance on SWE-bench Verified.
6 of 9 model-pair rankings flip across harness configs. GLM-5.1 swings 13 points (52.5→65.5)
by changing harness alone.

## ETCSOVG Taxonomy (7 layers)

| Layer | What It Governs | arifOS Component | Design Origin |
|---|---|---|---|
| **E**xecution | Sandbox, filesystem, timeouts, max steps | A-FORGE sandbox + forge_shell | F1 reversibility |
| **T**ools | Tool list, schema, selection strategy, error handling | MCP organ affordances + organ_affordances gate | Organ sovereignty |
| **C**ontext | Window, ordering, compression, retrieval, memory | ATLAS333 + skill/QWEN.md injection + fed-aware-middleware | Identity membrane |
| **S**cheduling | Agent loop, stop rules, retry, escalation, delegation | arifFlow + EMD reflex arc (encode→metabolize→decode) | Metabolic rhythm |
| **O**bservability | Logs, traces, checkpoints, auditability | FRAME (:18085) + sessions.jsonl + arifFlow telemetry | SIGNAL ≠ OBSERVER |
| **V**erification | Output parsing, schema validation, self-check, test exec | Tri-Witness W³ + ΔS ≤ 0 entropy gate | F2 truth floor |
| **G**overnance | Permissions, allow/deny, side-effects, human approval | F1–F13 constitutional floors + 888-APEX + F13 SOVEREIGN | Human veto final |

## The Contrast

**ETCSOVG** = disclosure taxonomy. "What IS your harness?"
**arifOS** = governance architecture. "What MUST your harness DO?"

ETCSOVG's Governance layer is a report field. arifOS's Governance layer is a constitutional
floor — F1–F13 are binding, not optional disclosure. "Tell me what you did" vs "you may
not do otherwise."

## Grammar Doctrine Connection

The harness IS the grammar. The model IS the generator. Without external validation
(the constitutional floor), the harness-model system degenerates into recursive
self-confirmation — it optimizes for its own metrics rather than reality. F1–F13 floors
are the external validator that prevents harness drift from becoming harness hallucination.

## hcsvog Metadata Spec

**Spec:** `/root/forge_work/2026-08-26-etcsvog-harness-metadata-spec.md`
**Purpose:** Attach harness identity to every FED routing receipt.
**Schema:** 8 flat fields (v, h_execution, h_tools, h_context, h_schedule, h_observe, h_verify, h_gov, h_fingerprint)
**Integration:** fed_route, fed_report_latency, fed_contrast, fed_aware_middleware, fi-mesh-check, federation receipt schema, federation envelope

## Related Maps

- `/root/AAA/knowledge-graph/audio-intelligence-map.md` — audio stack (TTS/STT/DSP)
- `/root/AAA/knowledge-graph/visual-intelligence-map.md` — visual intelligence
- `/root/AAA/knowledge-graph/video-intelligence-map.md` — video intelligence
- `/root/AAA/knowledge-graph/hermes-epistemic-architecture.md` — epistemic architecture

## Key Numbers

| Metric | Value | Source |
|---|---|---|
| Harness variance (avg) | 18.48 pp² | Paper, SWE-bench Verified 100-task grid |
| Model variance (avg) | 2.37 pp² | Paper, same grid |
| HV/MV ratio | 7.80× | Paper |
| Ranking flips | 6/9 pairs | Paper |
| GLM-5.1 harness swing | 13.0 pp (52.5→65.5) | Paper |
| Claude Sonnet 4.5 scaffold swing | 34 pp (68→34) | HAL, SWE-bench Verified Mini |
| o4-mini scaffold swing | ~48 pp | HAL, same |

---

*Created: 2026-08-26 by FI-003 · Paper: arxiv 2605.23950*
