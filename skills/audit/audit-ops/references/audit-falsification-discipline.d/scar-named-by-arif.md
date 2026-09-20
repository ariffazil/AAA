# Scar patterns Arif names — repository of past hits

This is the lookup table for phrases Arif uses under audit pressure and the actual artefact each one maps to in the arifOS codebase as of 2026-08-31. Use this file as a checklist when he names one of these — the right move is to open the file path cited, confirm the scar, patch only that.

## vacuous integrity

**What he means:** a verifier, validator, or integrity check that returns `valid=True` for non-trivial inputs because its broken-flag never gets flipped.

**Where this hid before:**
- `core/vault999/verify.py` — `chain_broken = False` initialised at top of function, never reassigned to True anywhere. Whole file returns `valid: True` for any non-empty JSONL.
- Generalized pattern: `valid = broken_count == 0` where `broken_count` is only incremented on JSON parse error, never on hash mismatch.

**Repro:** `python -c "from core.vault999.verify import verify_chain; print(verify_chain('/tmp/nonexistent.jsonl'))"` — should return `valid: False`, error: vault_file_not_found.

**Fix shape:** delegate to a verifier that re-computes the chain. Don't add a new file — wire the existing audit into the legacy entry point.

## hollow success

**What he means:** a tool returns a "ok"/exit-0 but the ledger entry it claims to have made has fields showing it didn't actually do the work.

**Where this hid before:**
- `arifosmcp/runtime/vault_sealer.py` `write_audit_receipt` — passes `actor_id=actor_id` but when caller supplies `actor_id=None`, the postgres row gets `actor_id IS NULL`. The tool returned "ok" so callers believe the receipt is attributed; the receipt is unattributed.
- Generalized pattern: any tool that returns its success state without echoing the same actor/session identifier into the receipt.

**Repro:** `grep "actor_id IS NULL" $VAULT999_DB` on vault_seals — count must be near zero for live receipts from human-bound tools. For kernel-attributed receipts (`arifOS-kernel`), zero is normal; for `arif_init`/`arif_seal` receipts, zero is expected because the kernel binds the actor.

**Fix shape:** response-first attribution: read actor_id from response['actor_id'] first, fall back to kwargs. Not the other way around.

## identity fork

**What he means:** the same fact exists under two labels — one canonical, one self-declared. External auditor sees two answers to the same question.

**Where this hid before:**
- `MCP endpoint registry` and `a2a-server/server.js` `chain.actor` claim `actor: 333-AGI` — but the actual actor on the receipt in vault_seals is `arifOS-kernel`. Two names for the same row.
- `arifos-kernel-seal-ritual/SKILL.md` notes that `arif_seal` with actor `hermes` returns `actor_verified=false` because the binding rejected the claim. Identity fork starts when the failing bind is silently passed through.

**Repro:** compare `chain.actor` reported in `aaa-chain-head.json` against `actor_id` in `vault_seals` for the same `chain_hash`. They should match.

**Fix shape:** when the actor binding fails, return failure explicitly. Do not let the actor_id field carry both labels.

## unmeasured W3

**What he means:** the tri-witness consensus score `W3 = (wH × wAI × wE)^(1/3)` is reported but the three witnesses are not actually measured — `wH` is hard-coded to 1.0 because "F13 sovereign always present", `wAI` is set by chain history length, and `wExternal` is set by `vaultHealthy` boolean.

**Where this hid before:**
- `a2a-server/server.js` lines 3190-3194 — exact location where W3 is computed.

**Repro:** grep `W3` in kernel runtime. If the only mention is in the server.js router and not in any actual attestation event emitter, the score is synthetic.

**Fix shape:** do NOT fake-fix this by adding oracle feeds — surface the issue as "W3 currently reports synthetic consensus; live external timestamp feed not yet wired" and remove the synthetic score from public claims. The MEMORY BOUNDARY doctrine forbids exposing it publicly anyway.

## delta_s null

**What he means:** the F4 CLARITY compression ratio `delta_s = 1 - (novel_claims / total_claims)` is reported as null instead of computed.

**Where this hid before:**
- `arifosmcp/runtime/seal_chain.py` `build_seal_receipt` only attaches delta_s when caller passes it; the writer never computes it.
- All `AUDIT_RECEIPT` rows in `vault_seals` have `payload.echo_delta_s = null`.

**Repro:** `grep "echo_delta_s" vault_seals.payload` count must equal total audit_receipt rows. Currently 0 of N.

**Fix shape:** compute in the sealer before insert. Not a separate service — same code path.

## History of patches against these (for future reference)

| Date | Scar | File | Diff size |
|------|------|------|-----------|
| 2026-08-31 | vacuous integrity | `core/vault999/verify.py` | +18/-15 — delegate to verify_live |
| 2026-08-31 | hollow success | (open) `arifosmcp/runtime/vault_sealer.py` | pending |
| 2026-08-31 | unmeasured W3 | (open) | reporting-only fix; doctrine blocks live fix |
| 2026-08-31 | delta_s null | (open) | pending |

## When you find a new scar name

If Arif names a scar pattern that isn't in this table, **add it** before patching. The skill depends on this file being the authoritative dictionary. Format:
- name
- "what he means" — his one-liner, paraphrase
- "where this hid before" — file path + line range
- repro command
- fix shape
