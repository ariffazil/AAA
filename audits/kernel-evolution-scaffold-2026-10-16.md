# Kernel Evolution Scaffold — External Production Readiness
> Forged 2026-10-16 by 333-AGI. Status: PLAN, not execution.

## Priority Order (dependency-aware)

### R1: D3 Pydantic Leak Fix [LOW, ~30min]
**File:** `arifosmcp/tools/vault.py` and `arifosmcp/tools/judge.py` — validation error handler
**Problem:** Wrong-typed arguments return raw Pydantic error with vendor URL + version.
**Fix:** Wrap validation errors in generic contract error envelope. Strip Pydantic internals.
```python
# Pattern: catch pydantic.ValidationError, return:
{"status": "HOLD", "verdict": "HOLD", "reasons": ["CONTRACT_VIOLATION: <field> expected <type>"],
 "meta": {"failure_type": "INPUT_VALIDATION"}}
```
**Test:** `test_d3_type_error_does_not_leak_pydantic_internals` should pass.
**Authority:** T2 (kernel code). Reversible.

### R2: D4 state_version Design [MED, ~2h design + 1h code]
**File:** `arifosmcp/runtime/tools.py` — arif_init response builder
**Problem:** No monotonic counter on verdict envelopes. Band/scope flips uncorrelatable.
**Design options:**
1. Session-scoped counter — increment on band change within session. Cheap, local.
2. Global kernel counter — increment on every arif_init. Cross-session.
3. Epoch-scoped — tie to kernel_epoch (already exists but doesn't move within a run).
**Recommendation:** Option 1. Add `session_state_version: int` to session store. Increment on band change. Expose via `echo_canonical_session()`.
**Authority:** T2 + F13 decision on semantics.

### R3: VAULT999 Seal [T3, sovereign action required]
**Paths:**
- (a) Arif seals from sovereign DM: `arif_seal(mode="session_close", ack_irreversible=true)`
- (b) Expose `arif_challenge` on MCP surface → agent self-verify → seal
- (c) Accept audit-only receipts as seal equivalent for non-sovereign sessions
**Recommendation:** (a) now. (b) for production.

### R4: External Production Readiness

#### R4.1 Session Persistence [CRITICAL]
Sessions in-memory → kernel restart loses all active sessions. Fix: persist to SQLite/JSON. TTL expiry.
**File:** `arifosmcp/runtime/tools.py` `_SESSIONS` store. Authority: T2.

#### R4.2 Public Surface Alignment [HIGH]
`PUBLIC_AGENT_6` = 6 tools, `KERNEL_ABI_8` = 8. `arif_forge`/`arif_seal` excluded → bypass session gate.
Fix: add to public surface or gate all 8 at transport level regardless. Authority: T2.

#### R4.3 MCP Protocol Version Consistency [MED]
arifOS rejects 2025-06-18. A-FORGE silently downgrades 2026-07-28. GEOX/WEALTH fail-closed differently.
Fix: accept all 4 versions everywhere. Consistent error codes. Authority: T2 (multi-organ).

#### R4.4 Floor Naming Consistency [LOW]
Mixed keys (F1-F9, L10-L13, F11-F13). F10 absent. floors_pass=16 vs target=13.
Fix: normalize to F<N>. Remove L<N> aliases. Authority: T2.

#### R4.5 Public Health Payload Consistency [MED]
arifos.arif-fazil.com/health = 15B stub vs localhost 15,794B full. WELL: 60B vs 2,773B.
Fix: proxy full payload or add `?full=true` param. Authority: T1 (config).

#### R4.6 Anonymous Call Enforcement [DONE — W1]
Monitor via witness tests on `witness/identity`.

#### R4.7 Deployment Sync [MED]
Source in 3 places: /opt/arifos/app/, /root/arifOS/, site-packages. Drift inevitable.
Fix: `pip install -e .` or rsync pipeline. Single source of truth. Authority: T2.

#### R4.8 Rate Limiting [HIGH for production]
Public MCP surface has no per-actor rate limits on tool calls.
Fix: token bucket on transport layer. Authority: T2.

#### R4.9 Observability Manifest [MED]
External agents need: tools, floors, auth requirements, verification flow, public keys.
Fix: `.well-known/arifos.json`. Authority: T1 (additive).

---

## Execution Order

1. **R1** — D3 fix (quick win)
2. **R4.2** — public surface alignment (W1 root cause)
3. **R4.1** — session persistence (production critical)
4. **R2** — state_version (needs F13 decision)
5. **R4.3** — MCP version consistency (multi-organ)
6. **R4.5** — public health consistency
7. **R4.7** — deployment sync pipeline
8. **R4.8** — rate limiting (before external traffic)
9. **R4.9** — observability manifest
10. **R3** — VAULT999 seal (sovereign ready)
11. **R4.4** — floor naming (cosmetic)

## Success Criteria: "External Production Ready"

- [ ] 8/8 witness tests passing
- [ ] Sessions survive kernel restart
- [ ] Public surface consistent on both doors
- [ ] MCP negotiation consistent across organs
- [ ] Rate limiting on public surface
- [ ] VAULT999 seal path for verified agents
- [ ] No vendor internals in error responses
- [ ] Source = deployed (single pipeline)