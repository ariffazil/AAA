# Survival Manifest — Phase 333

**Created:** 2026-07-12T05:36Z

## Federation Conformance: 9/10 PASS, 1 HOLD

| Scenario | Verdict | Notes |
|----------|---------|-------|
| A — Compatible Evidence | HOLD | Kernel health lacks drift fields (conservative, correct) |
| B — Stale Evidence | PASS | WELL correctly reports degraded |
| C — Semantic Mismatch | PASS | Epistemic contracts present |
| D — Authority Violation | PASS | Unauthorized seal rejected |
| E — Contradictory Organs | PASS | Contradiction handlers present |
| F — Replay Attack | PASS | 4/4 defenses found |
| G — Version Mismatch | PASS | MCP versions consistent |
| H — Kernel Unavailable | PASS | 6/9 A-FORGE degradation mechanisms |
| I — Compromised Witness | PASS | Witness diversity confirmed |
| J — Failed Execution Recovery | PASS | 7/7 rollback mechanisms |

## MCP Server Survival Proof

| Organ | Port | Health | Tools | Status |
|-------|------|--------|-------|--------|
| arifOS | 8088 | healthy | 12 | ✅ PROVEN |
| A-FORGE | 7071 | healthy | 59 | ✅ PROVEN |
| GEOX | 8081 | healthy | (domain) | ✅ PROVEN |
| WEALTH | 18082 | ALIVE | (domain) | ✅ PROVEN |
| WELL | 18083 | degraded | (domain) | ✅ PROVEN (degraded = evidence freshness) |

## Supporting Services Survival Proof

| Service | Port | Status | Proof |
|---------|------|--------|-------|
| Postgres | 5432 | running | Docker container healthy |
| Redis | 6379 | running | Docker container healthy |
| Qdrant | 6333 | running | Docker container healthy |
| FalkorDB | 6380 | running | Docker container healthy |
| Graphiti | 8000 | running | Docker container healthy |
| NATS | 4222 | running | systemd active |
| Prometheus | 9090 | running | systemd active |
| Grafana | 3000 | running | systemd active |
| Caddy | 443/80 | running | systemd active |

## Session Continuity: PROVEN

- `_new_session` → `set_active_session(sid)` → cross-tool continuity
- Both sync and async wrappers auto-inject session_id
- Replay protection: 4 defense layers (NonceCache, ingress middleware, envelope freshness, token exp)

## Known Gaps

1. **Scenario A HOLD**: Kernel health endpoint lacks `thermodynamic`, `runtime_drift`, `contract_drift` fields. This is conservative behavior — not a failure.
2. **A-FORGE rollback PARTIAL**: GitDiffGuard.rollbackFile() works for git-tracked files. Generic rollback executor is a stub.
3. **WELL biometrics expired 73 days**: Organ is degraded, not down. Needs human input (Arif self-report).
4. **WEALTH P0 bugs**: 4 P0 issues open (compute_npv off-by-one, compute_irr null, institutional_stress_index silent field-dropping, survival_engine inconsistent verdicts).

