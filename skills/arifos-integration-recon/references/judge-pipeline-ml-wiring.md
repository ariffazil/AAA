# Judge Pipeline & ML Wiring Reference

Investigated 2026-08-06. Read-only probe of arifOS kernel to map `arif_judge` verdict logic and identify Ollama/qwen2.5:3b integration points.

## File map

| Component | File | Lines |
|---|---|---|
| Judge entry (async) | `/opt/arifos/app/arifosmcp/tools/judge.py` | `arif_judge` @1023 |
| Judge entry (sync wrapper) | `/opt/arifos/app/arifosmcp/runtime/tools.py` | `_arif_judge_deliberate` @17069, `_arif_judge_deliberate_tool` @18207 |
| Canonical verdict composer | `/opt/arifos/app/arifosmcp/runtime/tools.py` | `_compute_canonical_verdict` @2378 |
| LLM cascade client | `/opt/arifos/app/arifosmcp/runtime/llm_client.py` | `call_llm` @2019, `_call_ollama` @1410 |
| Capability map (Ollama gate) | `/opt/arifos/app/arifosmcp/runtime/capabilities.py` | `build_runtime_capability_map` @54 |
| ML floor runtime | `/opt/arifos/app/core/shared/law_audit.py` | `get_ml_floor_runtime` @275, `FloorAuditor._apply_ml_floor_overrides` @451 |
| Verdict Pydantic schema | `/opt/arifos/app/arifosmcp/schemas/verdict.py` | `VerdictOutput` @622, `VerdictCode` import @47 |
| Health route ML status | `/opt/arifos/app/arifosmcp/runtime/rest_routes/rest_routes.py` | lines 3160-3197 |
| Existing qwen2.5:3b usage | `/opt/arifos/app/arifosmcp/intelligence/tools/relate_bridge.py` | `_ollama_extract_entities` @195, model="qwen2.5:3b" @256 |

## Verdict pipeline — deterministic, no LLM

`arif_judge` produces SEAL/SABAR/HOLD/VOID through 8 sequential deterministic gates. **No LLM is called in the judge verdict path.** The single LLM call in tools.py (`_synthesize_async` @5962) is for 333_MIND, not judge.

### Gate sequence (judge.py:1069-1461):

1. **Hard gates** (1069-1121): identity, reversibility proof, blast-radius receipt, action_tier attestation, escalation proof → HOLD if any fail
2. **Kernel intercept** (1123-1200): `arif_kernel_intercept` returns ALLOW/ESCALATE → mapped to SEAL/HOLD
3. **RASA DERITA** (1202-1260): causal cascade + consent lease for L3+/irreversible → HOLD
4. **666_HEART gate** (1264-1283): heart_critique VOID/HOLD → judge escalates to HOLD
5. **APEX collapse trigger** (1285-1318): auto-compute 4-dial params from candidate text
6. **BIJAKSANA bridge** (1320-1360): 4-dial thermodynamic lens; BLOCKED→HOLD, RESTRAIN→SEAL→SABAR
7. **Content-aware classifier** (1368-1461): pure regex keyword (`rm -rf`→ATOMIC, `deploy`→MUTATE, etc.)
8. **Canonical verdict composer** (tools.py:2378): `VOID > SABAR > HOLD > ERROR > DEGRADED > SEAL` precedence

### ML floor scoring (law_audit.py)

Current ML: SBERT (`all-MiniLM-L6-v2`), not Ollama. Gated by `ARIFOS_ML_FLOORS` env var.

```python
# law_audit.py:275-306 — THE flip point
def get_ml_floor_runtime():
    enabled = _env_truthy("ARIFOS_ML_FLOORS")   # ← set to "1" to enable
    method = "sbert" if enabled and sbert_available else "heuristic"
    ...
    return {"ml_floors_enabled": enabled, "ml_method": method, ...}
```

`FloorAuditor._apply_ml_floor_overrides()` @451 calls `classify_asi_floors()` (SBERT only) for F5/F6/F9 scoring. When SBERT unavailable → `ml_method: "heuristic_fallback"`.

## Ollama client interface

```python
# llm_client.py:1410-1500 — reuse directly for ML judge
async def _call_ollama(
    system: str, user: str, response_schema: dict[str, Any] | None,
    temperature: float, max_tokens: int = 1200,
) -> tuple[str, dict[str, Any]]:
    """Returns (raw_output_str, parsed_output_dict)"""
```

Config (llm_client.py:125-129):
- `OLLAMA_BASE_URL` = `os.getenv("OLLAMA_URL", "http://localhost:11434")`
- `OLLAMA_MODEL` = `os.getenv("OLLAMA_MODEL", "qwen2.5:7b")` ← **change to `qwen2.5:3b`**
- `OLLAMA_TEXT_ENABLED` = `os.getenv("OLLAMA_TEXT_ENABLED", "false")` ← **set to `true`**

The `_call_ollama` uses httpx (4s timeout), `POST /api/generate`, `stream: False`, `format: "json"` when schema provided, automatic truncation repair via `_repair_truncated_json`.

### Existing proven usage pattern

`relate_bridge.py` already uses qwen2.5:3b for NER+relation extraction. The pattern:
```python
from arifosmcp.runtime.llm_client import _call_ollama
raw, parsed = await _call_ollama(
    system="...", user="...", response_schema={...}, temperature=0.1, max_tokens=400
)
```

## Wiring recipe (proof-of-concept)

### Option A: Direct `_call_ollama` (local-only, recommended for PoC)

Insert in `_arif_judge_deliberate` (tools.py:17069) AFTER deterministic gates pass but BEFORE final verdict emit:

```python
# After line ~1360 in judge.py (after BIJAKSANA bridge, before action classifier)
from arifosmcp.runtime.llm_client import _call_ollama
judge_schema = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["SEAL", "SABAR", "HOLD", "VOID"]},
        "reasons": {"type": "array", "items": {"type": "string"}},
        "next_safe_action": {"type": "string"},
        "truth_band": {"type": "string"},
        "confidence": {"type": "number"},
    },
    "required": ["verdict", "reasons"],
}
system_prompt = "You are the 888_JUDGE constitutional arbitration surface..."
raw, parsed = await _call_ollama(
    system=system_prompt, user=f"CANDIDATE: {candidate}\nEVIDENCE: {evidence}",
    response_schema=judge_schema, temperature=0.1, max_tokens=400,
)
```

**Non-negotiable constraint:** HARD gates (steps 1-4) must remain non-overridable. ML can only downgrade SEAL→SABAR or SEAL→HOLD, never upgrade HOLD→SEAL when a hard gate failed.

### Option B: Via `call_llm()` cascade (goes through TokenRouter first)

```python
envelope = await call_llm(
    system=system_prompt, user=user_prompt, response_schema=judge_schema,
    temperature=0.1, max_tokens=400,
    constitutional_role="666_JUDGE", preferred_model="qwen2.5:3b",
    organ="judge", task_type="verdict",
)
```

This enters the full cascade (TokenRouter→DeepSeek→FLAME→MiniMax→...→Ollama). For local-only behavior, Option A is cleaner.

### Environment changes needed

```bash
# In kunci-mas.env or docker-compose:
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_TEXT_ENABLED=true
```

## Pydantic schema — minimal ML output

The `VerdictOutput` (schemas/verdict.py:622) has 20+ fields. For Qwen JSON output, the minimal required shape:

```json
{
  "verdict": "SEAL|SABAR|HOLD|VOID",
  "reasons": ["constitutional rationale..."],
  "next_safe_action": "recommended step",
  "truth_band": "CERTAIN|HIGH_CONF|PLAUSIBLE|SPECULATIVE|UNKNOWN",
  "confidence": 0.0-1.0
}
```

The full `VerdictOutput` fields include: `anomalous_contrast`, `thermodynamic_state`, `decision_collapse`, `growth_paradox`, `akal_state`, `floor_compliance`, `amanah_proof`, `dissent`, `civilizational_anchor`, `epistemic_state`, `judge_contract`, `reversibility_state`, `seal_state`, and more.

## Test pattern

From `test_canonical.py:151-181`:
```python
@pytest.mark.asyncio
async def test_judge_without_evidence_returns_sabar():
    r = await arif_judge_deliberate(mode="judge", candidate="deploy", actor_id="arif")
    assert r.status == "SABAR"
    assert r.result["verdict"] == "SABAR"

def test_judge_emits_seal_with_evidence():
    r = _arif_judge_deliberate(mode="judge", candidate="deploy",
        actor_id="arif", evidence_receipt={"query_sent": "test", ...})
    assert r["status"] == "OK"
    assert r["result"]["verdict"] == "SEAL"
    assert r["judge_contract"]["state_hash"]
```

For ML judge smoke test, add assertion: `meta.get("ml_method") == "qwen2.5:3b"`.
