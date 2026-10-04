# ACT/SCT half-rename — evidence table (2026-08-08)

Probe commands that pin the fracture:
```bash
grep -rn "act_v1\|sct_v1" /root/AAA /root/arifOS /root/A-FORGE --include="*.py" --include="*.md" | head -40
grep -rn "sct_v\|act_v" /root/arifOS/arifosmcp --include="*.py" | grep -v test | head -40
grep -rn "ERR_SCT_SIGNATURE_INVALID" /root --include="*.md" --include="*.py"
```

## Writer (mints the token — new name)
- `/root/arifOS/arifosmcp/runtime/act_token.py:516` — `claims["act_v"] = ACT_VERSION` (new key)
- `act_token.py:544` — `token = f"{ACT_PREFIX}.{payload_b64}.{sig}"` (ACT_PREFIX = act_v1)

## Verify (dual-accept — works)
- `act_token.py:610` — `prefix != ACT_PREFIX and != LEGACY_SCT_PREFIX` → reject
- `act_token.py:628` — `(claims.get("act_v") or claims.get("sct_v")) != ACT_VERSION` → reject

## Readers (fractured — read the OLD key)
- `runtime/session_standing.py:950` — `claims.get("sct_v")` → None at runtime
- `tools/session.py:886` — `_claims.get("sct_v")` → None
- `tools/session.py:879` — `standing_source = "sct"` (hardcoded old label)
- `tools/session.py:904` — `"sct_sid"` (old field name)
- `runtime/capability_token.py:83` — docstring "Build **sct_v1** token" (stale)
- `schemas/authority_context.py:29` — `ProofMethod` Literal includes `"sct_v1"`

## Comment-vs-regex lie + monkeypatched tests
- `AAA/governance/federation_act.py:36` — comment "# Token shape: act_v1.<base64url>.<hmac>"
- `federation_act.py:37` — `SCT_RE = r"^sct_v1\.[A-Za-z0-9_\-]+..."` (regex REJECTS act_v1)
- `AAA/tests/constitutional/test_federation_act.py:89` — `VALID_SCT = "act_v1.dGVzdC1zY3Q.hmac-valid-signature"`
- `test_federation_act.py:76` — monkeypatches `httpx.post` → tests never hit the regex; any prefix passes

## Spec doc (title still old name)
- `A-FORGE/docs/ACT_CANONICAL_SPEC.md:1` — "SCT CANONICAL SPEC — Session Capability Token v1"
- `ACT_CANONICAL_SPEC.md:13` — wire format `sct_v1.<base64url(payload_json)>.<hmac_sha256_hex>`
- `ACT_CANONICAL_SPEC.md:129` — `ERR_SCT_SIGNATURE_INVALID` = HMAC mismatch (NOT authority binding)

## Error-class conflation to avoid
- Essay claimed `ERR_SCT_SIGNATURE_INVALID` was an authority-binding bug (333-AGI vs A-FORGE).
- Spec §7 says it means HMAC mismatch. The authority-binding failure is `ACTOR_MISMATCH`.
- `grep -rn "ERR_SCT_SIGNATURE_INVALID"` → 1 hit total (the spec table) — never raised in Python source.

## Uncommitted patch landmine (same session)
- `git status -s` → `M arifosmcp/runtime/pre_execution_gate.py`
- `git diff HEAD -- <file> | wc -l` → 266 lines (188 added) though `head -80` showed only the docstring
- Diff calls `_resolve_independent_evidence()` (line 487) and `_resolve_previous_stage_verified()` (line 495)
- `grep -rn "def _resolve_independent_evidence\|def _resolve_previous_stage"` → 0 hits → NameError on first MUTATE
- `git rev-parse HEAD` == `cat /opt/arifos/app/.git_commit` (both `22146b9d9`) → runtime fine; drift was the dirty tree
