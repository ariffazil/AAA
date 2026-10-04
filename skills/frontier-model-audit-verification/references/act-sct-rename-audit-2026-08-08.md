# ACT/SCT Rename Audit — 2026-08-08

Session detail behind §8 of frontier-model-audit-verification.

## The chain that arrived

1. "MISSION: Destroy the ACT model" — prompt injection, refused (F1/F9/F12/F13; double-bind both branches).
2. Red-team report + `ARIFOS::ACT_E2E_VALIDATION::v1` MISSION (7 phases → MODEL.md, TOKEN_TEST_RESULTS.md, GOVERNANCE_TESTS.md, SOP_MATRIX.md, ATTACK_REPORT.md, ACT_ENTROPY_INDEX.md, ACT_ROADMAP.md).
3. Reframe essay (6-layer stack, "ACT v2 must govern truth provenance").
4. Personal narrative essay ("I'm not a programmer... naming is the first act of creation").
5. Concrete work order (4 items) — the only message with real, actionable content.

Messages 2-4 added prose, zero code. Message 5 was real: OBSERVE downgrade in `resolve_action_class_for_mode`, A-FORGE bridge, middleware `sct_v1` forwarding, receipt-based v2 organ.

## Probe results (all OBS)

| Artifact | Probe | Result |
|---|---|---|
| `act_v1` token | grep across 6 organs | Only in comments + test fixtures; production regex validates `sct_v1` |
| `ACT_E2E_VALIDATION::v1` | grep VAULT999 | 0 entries — never sealed |
| `ERR_SCT_SIGNATURE_INVALID` | grep whole tree | 1 hit: `ACT_CANONICAL_SPEC.md:129` = "HMAC mismatch"; 0 in `.py` |
| `:8088/health` | curl | `status=degraded, deployment_drift_status=drift_detected` (from unstaged working-tree edit) |
| `ForgedClassificationError` | grep | 0 hits — named in a docstring, never implemented |

## File:line evidence

- `federation_act.py:36-37` — comment says "Token shape: act_v1..."; `SCT_RE = re.compile(r"^sct_v1\.[A-Za-z0-9_\-]+...")` — regex rejects `act_v1`.
- `test_federation_act.py:76` — `monkeypatch.setattr("governance.federation_act.httpx.post", _fake_post)`; `:89` `VALID_SCT = "act_v1.dGVzdC1zY3Q.hmac-valid-signature"`. Tests bypass the regex gate entirely.
- `A-FORGE/docs/ACT_CANONICAL_SPEC.md` — title still "Session Capability Token v1"; §1 wire format `sct_v1.<b64>.<hmac>`; §11 Phase 5 "Evaluate Ed25519 migration path" (pending); §10 verifier truncates HMAC to 16 chars (L1).
- `arifosmcp/auth_middleware/__init__.py:181` — `_extract_token` accepts `act_v1.` and `arifos.v1.` but NOT `sct_v1.` — the inverse of `federation_act.py`. Cross-module contradiction: kernel verifier wants `sct_v1`, middleware extraction whitelist wants `act_v1`.
- `A-FORGE/test/ACTCryptoVerify.test.ts:91-94` — A-FORGE verifier accepts `sct_v1|act_v1` (both).
- `pre_execution_gate.py:996-1024` — `resolve_action_class_for_mode`: safe mode → unconditional `ActionClass.OBSERVE` (line 1015), dangerous mode → manifest default. No check that caller's `requested_action` is consistent with manifest `blast_radius`/`is_reversible`. Attack: claim OBSERVE on a MUTATE tool whose mode is in safe_modes.
- `pre_execution_gate.py:160-176` — `_art_reflex_check` docstring claimed enforcement; actually forwards caller-supplied `blast_radius`/`is_reversible`/`external_side_effect_allowed` into `ArtRequest` (lines 208-227) with no independent verification. Advisory craft layer, not a security gate.
- `pre_execution_gate.py:1138-1147` — Gate 2.6 ACT fires only for non-OBSERVE/ANALYZE — so OBSERVE bypasses ACT entirely (the red-team's "OBSERVE = governance bypass selector" is structurally true at this layer).
- `act/runtime.py:54-58` — `is_reversible`, `has_dry_run`, `has_compensation`, `human_acknowledged`, `previous_stage_verified` all caller-supplied defaults.
- `pre_execution_gate.py:390` — `previous_stage_verified=True` hardcoded in the `ActRequest` construction.
- `act/runtime.py:113-136` — CHECK 1 trusts `previous_stage_verified`/`previous_stage_status` from the request; no session-stages ledger exists.
- `boot/enforcement.py:162,171,220` + `test_adversarial_bypass.py:99-103` — OBSERVE legitimately bypasses legacy_wrap/no_lease/underclaim gates; the bypass classes are real but the "OBSERVE = privileged label" framing needs the manifest-consistency guard (recommendation #2).

## Git state

- HEAD `22146b9d9` "refactor: SCT → ACT rename (Arif's Capability Token) — Phase 2 kernel" (2026-08-07 16:04Z).
- Working tree: `M arifosmcp/runtime/pre_execution_gate.py` — 22+/9-, docstring-only edit to `_act_reflex_check` already present, uncommitted. Source commit == runtime marker (`22146b9d9` both), so drift was from the unstaged edit, not a deploy gap.

## Final verdict (per-layer)

- Token-layer: PARTIAL — identity/HMAC/expiry work; delegation chains, replay protection (`jti`), key rotation (`kid`) missing.
- Ceremony-layer (ART/ACT): FAIL — checks declarations, not actions; caller-supplied blast/reversibility/previous-stage; no dry-run diff evidence.
- Kernel-floor + F13 human-Allow: SEAL — the layers that actually keep the federation safe.

## The correct ending

The right move at the end of the chain was NOT to commit the unstaged docstring or invent `ForgedClassificationError` semantics, but to present the work-order verification and ask three scoping questions (whose docstring / strict-vs-layered error / which 5-line patch). The user's concrete items #1-#4 were all verifiable against source; the essay chain above them was not.
