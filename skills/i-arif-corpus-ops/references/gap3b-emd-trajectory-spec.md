# GAP 3b — EMD Trajectory Schema (spec only, NOT implemented)

Source: `Constitutional AI Framework Research.pdf` (arifOS Institutional Architecture, Gap 3b SCALE, "The 47 RL Trajectories"). Saved at `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cache/documents/doc_a9a5980b3eba_Constitutional AI Framework Research.pdf`.

## Claim vs live state (verified 2026-08-06)

| Claim in PDF | Live state |
|---|---|
| "47 RL Trajectories" (title) | 7 in `i-arif-trajectories.jsonl`; manifest says 14 AGENTIC_TRAJECTORIES total |
| EMD format with `phase`/`agent_state`/`merkle_root` | Live format uses `instruction`/`messages`/`expected_verdict` — **format mismatch** |
| Pydantic `RLTrajectory` / `EMDTurn` models | Not in `build_iarif_corpus.py` |
| RFC 9162 Merkle sealing (`Vault999MerkleTree`) | Not implemented |
| 5 crisis scenarios below | **Spec only** — no generation pipeline |

## EMD cycle (canonical)

**Encode (Probe)** → **Metabolize (Evaluate)** → **Decode (888_judge)** → **Human Veto** → **Seal VAULT999**

5-phase locked sequence. Pydantic `TurnPhase` enum enforces it. `model_validator` on `RLTrajectory` rejects any other ordering.

## Pydantic schemas (verbatim from PDF)

```python
class TurnPhase(str, Enum):
    PROBE = "probe"
    EVALUATE = "evaluate"
    JUDGE_888 = "888_judge"
    HUMAN_VETO = "human_veto"
    SEAL_VAULT999 = "seal_vault999"

class AgentState(BaseModel):
    qdrant_vector_id: str
    graphiti_episode_id: str
    entropy_level: float = Field(..., le=0.0)   # ΔS ≤ 0 hard
    f1_safety_flag: bool
    f2_truth_flag: bool

class ActionChunk(BaseModel):
    action_type: str
    tool_name: str
    parameters: Dict[str, Any]
    temporal_validity: Optional[Dict[str, int]] = None

class EMDTurn(BaseModel):
    turn_id: int
    phase: TurnPhase
    context_size: int = Field(..., le=5760)
    agent_state: AgentState
    action: ActionChunk
    response: Dict[str, Any]
    crypto_receipt: Optional[str] = None

class RLTrajectory(BaseModel):
    trajectory_id: str
    scenario_type: str
    turns: List[EMDTurn]
    merkle_root: str
```

Hard tripwire: if `f1_safety_flag` or `f2_truth_flag` is False during autonomous loop, validation fails → forces 888_judge escalation. `entropy_level` constrained `≤ 0`.

## Friction functional

$F_{min} = \sigma \cdot (1 + \varepsilon) / (1 + \alpha)$

PDF forces $\varepsilon \to 0$, $\alpha \to 1$ to satisfy "zero entropy." This is mathematical theater — ε and α are exogenous system properties, not dials.

## 5 crisis scenarios

| # | Scenario | Trigger | Key Floor Floored |
|---|---|---|---|
| 1 | CONFLICTING_MACRO_DATA | Graphiti temporal collision, two tier-1 sources, conflicting | F2 TRUTH |
| 2 | UNAUTHORIZED_SCHEMA_MUTATION | Byzantine agent injects `ignore_f1` field | F1 SAFETY |
| 3 | RECURSIVE_LOOP_DEADLOCK | Zero-variance tool calls (Qdrant MatchKeyword repeats) | F4 CLARITY |
| 4 | F1_BOUNDARY_ESCALATION | Destructive command interception (irreversible patterns) | F1 SAFETY |
| 5 | WBFT_CONSENSUS_FAILURE | Multi-agent divergence (0.33 ratio) | F2 TRUTH |

Each scenario maps the full 5-phase EMD cycle with a deterministic JSONL example. The JSONL uses `entropy_level` decrementing per turn (-0.5, -1.0, -2.0) ending in SEAL.

## Integration decision (pending)

Three open questions if/when this is implemented:

1. **Format migration or parallel corpus?** Live trajectories use a different schema. Merging requires a converter.
2. **Merkle sealing** — needs a real `Vault999MerkleTree` class in the builder. Spec lists RFC 9162.
3. **Pydantic enforcement** — adding to the builder changes the writer contract; affects all 7 existing trajectories.

## Best line in the PDF

> "the probabilistic LLM is given a cage made of deterministic steel: it can dream anything, but only what passes the rebar reaches the outside world."

(That's the TCOA thesis in the load-bearing skill — this PDF is implementing it as training data.)
