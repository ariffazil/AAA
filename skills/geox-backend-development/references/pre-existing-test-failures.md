# Pre-existing GEOX Test Failures

These failures exist in the codebase BEFORE any session enforcement changes.
They are NOT regressions. Documented here so future sessions don't waste time
diagnosing or "fixing" them without understanding the root cause.

## 1. SCT prefix mismatch (3 tests)

**Affected tests:**
- `TestC3RedteamSctStillWorks::test_valid_sct_with_verified_actor_passes`
- `TestC3RedteamSctStillWorks::test_forged_sct_hmac_rejected`
- `TestC3RedteamSctStillWorks::test_sct_actor_mismatch_rejected`

**Root cause:** Test helper `_make_sct()` (line 58 of test_c3_redteam_session_enforcement.py)
generates tokens with `sct_v1.*` prefix:
```python
return f"sct_v1.{payload_b64}.deadbeef"
```

But `validate_session()` (line ~372 of session_enforcement.py) checks for `act_v1.*`:
```python
if session_id.startswith("act_v1."):
```

The token never reaches PATH 1 (SCT verification), falls through to PATH 3 (unknown format),
and returns `SESSION_INVALID` instead of `SCT_INVALID` or `ACTOR_MISMATCH`.

**Fix:** Either change the test helper to use `act_v1.*` or change the code to accept `sct_v1.*`.
Both sides need to agree on the prefix. Verify which is canonical before changing.

## 2. Session echo test — no kernel mock (2 tests)

**Affected tests:**
- `test_surface_status_echoes_federation_context[registry]`
- `test_surface_status_echoes_federation_context[health]`

**Root cause:** The test calls `geox_surface_status()` with `session_id="SEAL-session-echo"`
but does NOT mock `_cached_kernel_verify`. Since arifOS is unreachable in CI/test,
the SEAL path returns `TRANSPORT_DEGRADED`, and the tool returns an error dict
that lacks the `session_id` key → `KeyError`.

**Fix:** Add `@patch("geox_mcp.session_enforcement._cached_kernel_verify")` with a
valid mock response, like the other SEAL-path tests do.

## Proving a failure is pre-existing

```bash
cd /root/GEOX
git stash  # revert all changes
PYTHONPATH=src .venv/bin/python3 -m pytest <failing_test> -q --tb=line
git stash pop  # restore changes
# If the test fails identically with and without your changes → pre-existing
```
