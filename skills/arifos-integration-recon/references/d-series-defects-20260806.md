# D-Series Defects — 2026-08-06 Audit Session

A single-day audit session (2026-08-06) introduced 10+ kernel fixes in 12 commits. They share the prefix pattern `fix(kernel): D{0-9} — ...` and were authored by `kimi-code/FI-008 <kimi@arif-fazil.com>`. One commit (`5d5fc2b0`) is from a different author (`333-AGI Δ MIND`).

## Commit catalog

| Commit | Defect ID | What it fixes | Files | Status |
|--------|-----------|---------------|-------|--------|
| `6f3c3357` | FLR-002 | F4 CLARITY display normalization | `rest_routes.py` | Active |
| `5d5fc2b0` | E7 | NOT-canonical F8 banner on `apex_decision_field.py` | `kernel/apex_decision_field.py` | Active |
| `02dd3513` | Claude audit | Vault path, G gate, memory contract, APEX recording, judge defaults | `runtime/tools.py`, `verdict.py`, `tools/judge.py` | Active |
| `a94e1f1a` | D0 | Empty vault chain → UNMEASURED, not OK | `apps/command_center/vault_chain.py`, `runtime/canonical_vault_chain.py`, `tools/vault.py` | Active |
| `96ce3a0a` | D1 | SCT fallback for actor_verified on session miss | `runtime/tools.py` | Active |
| `4ac7ca1e` | D1 | base64 padding fix in SCT fallback | `runtime/tools.py` | Active |
| `a461a960` | D1 | resolve actor_verified from SCT `av` claim in authority path | `runtime/tools.py` | Active |
| `169c7935` | D2 | hollow success gate in `_compute_canonical_verdict` | `runtime/tools.py` | Active |
| `63d8d78e` | D4 v1 | per-mode affordance contracts | `runtime/tools.py` | **REVERTED** |
| `7752f441` | revert | reverts D4 v1 (IndentationError) | `runtime/tools.py` | Active (revert) |
| `bc697380` | D4 v2 | per-mode affordance contracts (fixed placement) | `runtime/tools.py` | Active |
| `42dec9e5` | D5 | substrate health probe stability (timeout 50→200ms, quorum ≥2/3) | `runtime/substrate_health.py` | Active |

## The D4 revert cycle

This is the most important pattern. D4 v1 was committed, broken (IndentationError — placed dict between dict entries instead of after the closing brace), reverted, and re-applied as v2 in the correct location. The crash investigation evidence:

```bash
# v1 commit (63d8d78e): adds MODE_AFFORDANCE_OVERRIDES with wrong indentation
# revert commit (7752f441): "Revert "fix(kernel): D4 — per-mode affordance contracts..."
# v2 commit (bc697380): same fix, placed after the real dict close at line 2080
```

When investigating "why was D4 partially effective" or "why does the verdict path not see mode overrides": the fix IS active — but **incomplete**. See `references/dual-contract-system.md`.

## D1's three-commit pattern

D1 (SCT fallback for actor_verified) was fixed across three sequential commits:
1. `96ce3a0a`: Initial fallback
2. `4ac7ca1e`: base64 padding bug (hardcoded `"==="` failed when payload length mod 4 != 1)
3. `a461a960`: Also resolve `actor_verified` in the PHASE_A authority path (not just `_enforce_nine_signal`)

This is a textbook example of an evolving fix. When a D-series fix has multiple sequential commits, read all of them in order — earlier ones have known gaps that later commits address.

## D0 semantic subtlety

D0 (`a94e1f1a`) fixes a "happy path lies" bug: empty vault → `status=OK, integrity=OK, verified=True`. After D0, empty vault → `status=UNMEASURED, integrity=UNMEASURED, verified=False`.

The key invariant is **"integrity cannot be asserted on an empty chain"** — this is F2 TRUTH. When evaluating whether a "fix" is correct, check whether the empty/default state is structurally honest. If a system reports OK when there is nothing to check, that's a TRUTH violation regardless of whether the fix claims to address it.

## D2's surface

D2 (`169c7935`) added Step 1b to `_compute_canonical_verdict`:
- Empty reasons + no content + ≤2 meaningful keys → hollow
- `result is None AND content is empty` → hollow
- If verdict was SEAL → downgrade to UNMEASURED

The narrow trigger conditions suggest this is a heuristic, not a structural check. When you see a "hollow success gate," check whether the trigger conditions cover all empty-payload patterns — they often miss edge cases.

## G gate wiring (from `02dd3513`)

The G gate was previously computed but never checked. Claude audit fixed this by:
1. Adding `g_score` parameter to `compose_effective_verdict`
2. Wiring it in `judge.py` (line 1581): `g_score=_standing_apex.get("G")`
3. Threshold ladder: 0.30 / 0.50 / 0.80

**BUT** this is only wired in the JUDGE path. The wrapper path (`_compute_canonical_verdict`) still lacks G gating. See `references/dual-verdict-paths.md`.

## APEX recording calibration (also `02dd3513`)

```python
# Before
success=(_status == "OK")
within_lease=bool(kwargs.get("session_id"))
dry_run_first=bool(kwargs.get("dry_run"))

# After
_is_success = _status in ("OK", "completed")
_has_lease = bool(kwargs.get("session_id") or final_resp.get("session_id") ...)
_ac = final_resp.get("affordance_contract", {}).get("action_class", "")
_is_dry = bool(kwargs.get("dry_run") or _ac in ("OBSERVE", "ANALYZE", "DRAFT") ...)
```

The fix uses response-side signals when input is missing. This pattern — "use response data when input is absent or stale" — is worth remembering for other calibration fixes.

## D5 substrate flapping

D5 (`42dec9e5`) fixed substrate health probe flapping by:
- Timeout 50ms → 200ms (4× more lenient)
- Threshold: all-3-reachable → majority-quorum (≥2/3)

This is a "soften the threshold to avoid alert storms" pattern. When investigating "why does X flap", check whether the threshold is structural (must be met exactly) or quorum-based (must be met by majority).

## Investigation pattern

When asked about a D-series defect or fix:

1. `git log --oneline origin/main..HEAD | grep -E "D[0-9]|E[0-9]|FLR" | head -20`
2. Read the commit message in full (not just the subject)
3. `git show <sha> --stat` — get file list
4. `git show <sha>` — get the diff
5. Check for reverts: `git log --oneline | grep -i revert`
6. If multiple sequential commits share a defect ID (like D1), read all in chronological order
7. Verify the fix is structurally honest on edge cases (empty input, missing data, default states)