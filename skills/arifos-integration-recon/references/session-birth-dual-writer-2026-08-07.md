# session_birth vs effective_state — Dual-Writer Identity (2026-08-07)

## Finding

`arif_init` (actor_id="arif-fazil") returns a SINGLE payload with two contradicting identity/verification stories:

| Field | Value | Verdict |
|---|---|---|
| `result.actor_id` | `arif-fazil` | claimed identity preserved ✓ |
| `result.session_birth.actor_id` | `ARIF` (uppercase) | identity rewritten ✗ |
| `result.effective_state.actor_verified` | `true` | verified ✓ |
| `result.session_birth.actor_verified` | `false` | unverified ✗ |
| `result.session_birth.authority_source` | `identity_band` | vs `standing_source: sct` |

`contradiction_detector.py` (line 97) reads `session_birth.actor_verified` — a false here is treated as L11 AUTH failure on a session that `effective_state` says is verified. This is K7 class #2 (dual-identity) at a NEW site: not top-level vs `standing.actor`, but two session-lifecycle writers disagreeing inside one payload.

## Code site

- `arifosmcp/runtime/tools.py:250-263` — two independent population paths for `session_birth` vs `effective_state`
- `arifosmcp/runtime/contradiction_detector.py:97` — the consumer that flags the false as L11 failure
- `arifosmcp/runtime/authority.py:196,503` — exempt actors marked verified by definition; `session_birth` may predate that marking

## Detector

```python
# arif_init actor_id="arif-fazil" →
sb = payload["result"]["session_birth"]
es = payload["result"]["effective_state"]
assert sb["actor_id"] == payload["result"]["actor_id"], "identity rewrite"
assert sb["actor_verified"] == es["actor_verified"], "verification contradiction"
```

## Related: entropy_dS consumer gap (same session)

STAB-2026-08-07e/f/i killed `delta_S=0.0` fabrication at the producers. But `runtime/tools.py:8497-8498` only forwards `delta_S` when the key EXISTS in the inner result:

```python
if isinstance(result, dict) and "delta_S" in result:
    delta_S = result["delta_S"]
```

An inner handler that now omits the key silently falls back to the pre-block default — the "honest None" never propagates. Lesson: killing a fabrication requires auditing every consumer that branches on key presence.
