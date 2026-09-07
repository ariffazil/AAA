---
name: forge-vss-parser
id: forge-vss-parser
version: 1.0.0-2026.08.18
owner: 555-ASI
risk_tier: low
autonomy_tier: T1
floor_scope:
  - F2
  - F4
  - F7
  - F9
  - F11
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# forge-vss-parser

## Overview
`forge-vss-parser` is the **VSS-1 Causal Scene Graph Parser** skill within arifOS / AAA. It functions as the entry gate for Verified Scene Synthesis (VSS). It converts unconstrained, natural language visual prompts into a strict, machine-readable **Assertion Ledger JSON**.

By compiling prompts into explicitly typed contracts (Entities, Spatial Relations, Verifier Mapping, Tolerances) before image generation begins, this skill prevents **Verifier Drift** and enforces ground-truth constraints on downstream generation engines.

---

## Operational Architecture

```
[User Visual Prompt]
        │
        v
[qwen3-omni-flash Substrate] ──(Zero Temp Extraction)──> [Raw JSON Proposal]
        │
        v
[vss_parser_engine Validator]
        │
        ┌─────────────────┴─────────────────┐
        │                                   │
   (Valid Schema)                     (Schema Violation)
        │                                   │
        v                                   v
[Assertion Ledger]                   [Fail-Closed Rejection]
```

---

## Key Invariants & Constitutional Mapping

| Constitutional Floor | Requirement | Enforcement Mechanism |
| :--- | :--- | :--- |
| **F2 TRUTH** | Absolute accuracy in entity count & relational claims. | `count_v1` verifier mapping; explicit entity tracking. |
| **F4 CLARITY** | Deterministic JSON schema structure. No prose. | Hard gate via `jsonschema` against `vss_assertion_ledger.schema.json`. |
| **F7 HUMILITY** | Anti-Hallucination Gate. No forced spatial assumptions. | Ambiguous prompts (e.g., "near") MUST NOT be converted to hard relations ("inside"). Route to `uncertainties`. |
| **F9 ANTI-HANTU** | Schema ownership belongs to AAA, not the LLM substrate. | Substrate LLM outputs pure raw data; engine validates and fail-closes independently. |
| **F11 AUDIT** | Every parse is a receipt. | `parse()` returns SUCCESS or FAIL_CLOSED with error_code. |

---

## Contract Schema Overview

The parser output strictly conforms to the following core entities:

1. **Entities:** Atomic components (`object`, `container`, `agent`, `light_source`, `surface`, `background`) with counts and visual attributes.
2. **Assertions:** Testable claims featuring:
   - `subject` & `target` entity bindings
   - `relation`: `inside`, `on`, `beside`, `behind`, `in_front_of`, `supported_by`, `near`, `illuminates`, `casts_shadow_towards`, `reflects`, `occludes`
   - `class`: `HARD_GEOMETRIC`, `HARD_COUNT`, `OPTICAL_LIGHTING`, `SOFT_STYLE`
   - `verifier`: `containment_v1`, `count_v1`, `perspective_v1`, `shadow_v1`, `none`
   - `failure_action`: `LOCAL_REPAIR`, `GLOBAL_RESAMPLE`, `WARN_ONLY`, `LOG`
3. **Uncertainties:** Unresolved spatial or relational details from underspecified prompts.
4. **Unsupported Claims:** Non-measurable, abstract, or non-visual assertions (e.g. emotions, smells, abstract concepts).

---

## Invocation Pattern

```python
from vss_parser_engine import VSSParserEngine

def llm_runner_qwen(system_prompt: str, user_prompt: str) -> str:
    # Substrate caller wrapper (e.g. MuleRouter / OpenRouter qwen3-omni-flash)
    return call_mule_router(model="qwen3-omni-flash", sys=system_prompt, user=user_prompt)

engine = VSSParserEngine()
result = engine.parse("Three red apples inside a glass bowl under bright sunlight.", llm_runner_fn=llm_runner_qwen)

if result["status"] == "SUCCESS":
    ledger = result["ledger"]
    # Proceed to VSS-2 Verifier Gate
else:
    # Fail-Closed handling
    print("Parsing failed:", result["error_code"])
```

---

## Integration Dependencies

- **Pre-requisite for:** `forge-vss-verifier-suite` (VSS-2)
- **Consumes:** qwen3-omni-flash (or equivalent zero-temperature LLM substrate)
- **Substrate Neutrality:** If the substrate fails schema or contract validation, the engine fails closed without polluting down-pipeline state.
- **Contract gate (Python, not prompt):** `RELATION_CONTRACT` in `vss_parser_engine.py` rejects `near→inside`, dangling subjects, and illegal verifier/class pairs even when JSON Schema passes.
- **Not this skill:** `forge-vss-verifier-suite` (pixels), `imagine` / `minimax-image-gen` (proposal engines), world-field / differentiable renderer (Layer 2/3 HOLD).

## Tests (no LLM, no credits)

`test_vss_parser.py` — 50 expected ledgers + 35 fail-closed boundary cases.

Verified 2026-08-19: `fixtures=50/50` · `boundary_reject=35/35` · mock + stub parse PASS.

MuleRouter / qwen3-omni-flash binding is **HOLD** until that suite stays green. Do not burn credits to paper over a contract hole.

DITEMPA BUKAN DIBERI — Probabilistic proposals + deterministic verifiers + local repair = executable hybrid AI framework. ⚒️