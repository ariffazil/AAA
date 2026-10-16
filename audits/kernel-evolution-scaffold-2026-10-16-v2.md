# Kernel Evolution Scaffold v2 — Corrected After Spec Validation
> Forged 2026-10-16 by 333-AGI. Status: PLAN. Corrects spec claims against live probes.

## Verified Reality (OBS)

1. Session persistence mechanism EXISTS (`_FileSessionStore` → `.arifos/runtime_sessions.json` + fcntl flock) but session creation paths (5 sites in session.py: lines 519, 549, 671, 686, 985, 1084) write to `_SESSION_IDENTITY[sid]` directly without calling `_persist_store()`. Result: 0 sessions in store file despite 68+ sessions created. **Fix: add `_persist_store()` after each direct assignment. ~5 lines. NOT the SQLite rewrite the spec proposes.**

2. PUBLIC_AGENT_6 = 6 tools (not 8). arif_forge/arif_seal excluded. Spec's claim of "all 8 exposed" is false.

3. Floor scoring: health shows pass/fail only. Numeric scores not visible. Can't verify spec's "0.05 passing" claim without reading floor producer code.

4. Source = deployed (de1b916) at this moment. Drift will recur without pipeline fix.

5. Pydantic leak confirmed (errors.pydantic.dev/2.14 in error responses).

---

## Priority Matrix (corrected)

### P0: Session Persistence Fix [~30min, T2, reversible]
**NOT the SQLite WAL rewrite.** The mechanism already exists. Fix is surgical:
```python
# In session.py, after each _SESSION_IDENTITY[sid] = record (lines 519, 549, 671, 686, 985, 1084):
_persist_store()
```
This flushes the in-memory dict to the existing JSON file with fcntl flock. Sessions survive restart immediately.
**SQLite WAL is Phase 2** — better concurrency, but the JSON+flock approach is production-adequate for current traffic.

### P1: Deploy Pipeline [~1h, T2]
- Add `setuptools_scm` to pyproject.toml for git hash injection
- Wrap deploy script with `flock -n` for atomic deploys
- rsync source → site-packages as part of deploy (or `pip install -e .`)
**Goal:** source commit = deployed commit, provable.

### P2: Pydantic Leak Fix [~30min, T2]
- Global exception handler: intercept ValidationError, strip ctx/loc, return generic 422
- Test: `test_d3_type_error_does_not_leak_pydantic_internals` passes

### P3: Floor Scoring Audit [~1h, T2]
- Read floor producer code (f4_f9_probe, claims.json consumers)
- Verify threshold logic: does 0.0 == pass?
- Fix: strict positive bounds, null → quarantine
- Test: floors with 0.0 score → fail, not pass

### P4: Public Surface Alignment [~1h, T2]
- Add arif_forge/arif_seal to PUBLIC_AGENT_6 (or gate all 8 at transport level)
- Fixes W1 root cause at source level
- Test: `public_tool_names_for_mode()` returns 8

### P5: Floor Naming [~30min, T2]
- Normalize L10-L13 → F10-F13 in floor detail dict
- Fix floors_pass count (16→13)

### P6: MCP Version Consistency [~2h, T2]
- Accept 2025-06-18 on arifOS (currently rejected)
- Standardize error codes across organs

### P7: Rate Limiting [~3h, T2]
- Token bucket on transport layer
- Per-actor limits

### P8: VAULT999 Seal Path [T3, sovereign]
- Expose arif_challenge on MCP surface
- Or accept audit-file receipts as seal equivalent

---

## Spec Proposals: Adopt / Defer / Reject

| Spec Proposal | Decision | Reason |
|---|---|---|
| SQLite WAL MutableMapping | DEFER (Phase 2) | JSON+flock mechanism exists, just needs wiring. SQLite is better but not needed yet. |
| BEGIN IMMEDIATE transactions | DEFER | Only needed if SQLite adopted. |
| aiosqlite connection pool | DEFER | Same. |
| setuptools_scm | ADOPT (P1) | Correct approach for version attestation. |
| flock -n deploy | ADOPT (P1) | Already partially implemented, needs hardening. |
| Pydantic global exception handler | ADOPT (P2) | Correct fix for D3. |
| Floor threshold audit | ADOPT (P3) | Critical if 0.0 really passes. |
| PRAGMA mmap_size=30GB | REJECT | VPS has 32GB RAM, mmap_size=30GB would consume nearly all. Excessive for session store. |
| Connection pooling for SQLite | REJECT (for now) | Single-process kernel, no need for pooling until multi-process. |

---

## Success Criteria (unchanged from v1)

- [ ] Sessions survive kernel restart (P0)
- [ ] Source = deployed (P1)
- [ ] No vendor internals in errors (P2)
- [ ] Floor scores truthful (P3)
- [ ] Public surface = 8 tools (P4)
- [ ] Rate limiting before external traffic (P7)
- [ ] VAULT999 seal path (P8)

## Execution Order

P0 (30min) → P1 (1h) → P2 (30min) → P3 (1h) → P4 (1h) → rest as capacity allows.
Total critical path: ~4h.
