# Dual Verdict Paths — Wrapper vs Judge Composer

The arifOS kernel has TWO independent verdict derivation pipelines. They must agree on what gates SEAL, but they enforce different sets of constraints. This is a rich source of contradictions.

## Path A: Wrapper path (`_compute_canonical_verdict`)

**Location**: `runtime/tools.py` line 2472
**Used by**: Every MCP tool via `_enforce_nine_signal` (line ~4463)
**Signature**:
```python
def _compute_canonical_verdict(
    *, tool_name, status, meta, result_payload, out, actor_verified,
) -> tuple[str, list[str]]:
```

**8-step pipeline**:
1. Initial verdict from `status` (OK → SEAL)
2. Sub-gate verdicts (post_observe_gate, sabar_gate) — narrows SEAL → DEGRADED
3. Degraded flags from `out` — narrows SEAL → DEGRADED
4. Inner verdicts from result payload
5. Authority resolution (session_actor_mismatch scar)
6. **Affordance narrowing** — `_derive_affordance_verdict` using `_get_affordance_contract(tool_name)` (NO mode param)
7. Nine_signal consistency
8. Verdict monotonicity floor

**Key property**: NO G gate. NO `_standing_apex` integration. NO `session_authority_band` integration.

## Path B: Judge path (`compose_effective_verdict`)

**Location**: `runtime/verdict.py` line 153
**Used by**: `arif_judge` via `tools/judge.py` line 1575
**Signature**:
```python
def compose_effective_verdict(
    inner_verdict=None, *, session_authority_band=None, drift=None,
    explicit_reason=None, g_score=None,
) -> EffectiveVerdict:
```

**Gates**:
- F1 AMANAH: `OBSERVE_ONLY` band → SEAL downgrades to OBSERVE_ONLY
- Drift: non-empty → HOLD
- **F8 GENIUS G gate** (D series, 2026-08-06): `g_score < 0.30` → HOLD, `< 0.50` → SABAR, `< 0.80` → SABAR
- Void + no authority → stays VOID

**Key property**: HAS G gate. HAS authority band integration.

## The contradiction

A tool like `arif_seal` returning `verdict=SEAL`:
- Wrapper path emits SEAL (no G gate, no band check)
- Judge path would emit HOLD/SABAR if `g_score < 0.80`

But `arif_seal` doesn't go through the judge path. So:
- `arif_seal` can SEAL when `G < 0.30` (no gate)
- `arif_judge` cannot SEAL when `G < 0.30` (gated)

This breaks F8 GENIUS symmetry across the kernel. Any sealed entry from `arif_seal` is not G-gated, only judge-issued SEALs are.

## When this matters

- **Audit**: A reviewer looking at VAULT999 entries sees SEALs from tools with low G scores. They are F8 TRUTH violations but not detected.
- **Cross-tool chains**: If a workflow calls `arif_forge` (wrapper path) without first calling `arif_judge` (judge path), G is never checked.
- **Recovery**: The degraded-dominance gate in `_arif_judge_deliberate` and `_arif_vault_seal` independently checks substrate health — but that's not the same as G.

## Investigation pattern

When asked "why does tool X SEAL when G is low?":

1. `grep -n "compose_effective_verdict\|_compute_canonical_verdict" arifosmcp/runtime/tools.py | head -10` — find both paths
2. Trace which path tool X uses (likely `_enforce_nine_signal` → `_compute_canonical_verdict`)
3. Check if `g_score` is ever computed/passed in that path (it's not in the wrapper)
4. Check `_arif_judge_deliberate` vs the tool's wrapper — judge path has G gate, wrapper doesn't

## Fix sketch

Add optional `g_score: float | None = None` to `_compute_canonical_verdict`, and the same threshold ladder as `compose_effective_verdict`. Compute G in `_enforce_nine_signal` (similar to how `_standing_apex.get("G")` works in the judge path) and pass it down.

## Related reading

- `references/dual-contract-system.md` — mode override gap (also a path divergence)
- `references/d-series-defects-20260806.md` — D-series fixes introduced and partially wired