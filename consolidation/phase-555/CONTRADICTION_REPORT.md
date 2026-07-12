# Contradiction Report — Phase 555

**Created:** 2026-07-12T05:35Z

## Critical Contradictions

### C1: FEDERATION_CONTRACT.md — 5 Different Versions

| Repo | Hash | Lines | Status |
|------|------|-------|--------|
| arifOS | 5f4b86da52fd | 342 | CANONICAL |
| A-FORGE | c2344655533d | 92 | DERIVATIVE |
| AAA | f7b4320544fa | 84 | DERIVATIVE |
| geox | 1efc1525d38e | 90 | DERIVATIVE |
| WEALTH | 1eeba127723b | 85 | DERIVATIVE |

**Risk:** HIGH — agents reading different contracts get different authority rules.
**Resolution:** arifOS owns canonical. Others should import or symlink.
**Migration:** Replace independent copies with references to arifOS canonical.

### C2: AGENTS.md — 6 Different Versions

| Repo | Hash | Lines |
|------|------|-------|
| arifOS | 84205bbede77 | 221 |
| A-FORGE | b4fcfdd03ba6 | 427 |
| AAA | f74195fa6b06 | 351 |
| geox | 7fefe0af5062 | 422 |
| WEALTH | 77cba0bf13c6 | 184 |
| WELL | cbc90489e2c6 | 194 |

**Risk:** MEDIUM — per-organ bootstraps are acceptable, but independent doctrine is not.
**Resolution:** AAA owns canonical AGENTS.md. Per-organ files should be thin bootstraps.

### C3: Tool Count Claims — Wildly Inconsistent

Docs claim: 5, 11, 13, 16, 32, 48, 58, 72 tools across different files.
Actual: arifOS=12, A-FORGE=59 (from live endpoints).

**Risk:** MEDIUM — agents may expect tools that don't exist.
**Resolution:** All docs must reference live endpoint counts, not hardcoded numbers.

### C4: Port :7072 in Docs — A-FORGE Runs on :7071

Some docs reference port :7072 for A-FORGE, but A-FORGE actually runs on :7071.

**Risk:** LOW — health probes fail, agents fall back to correct port.
**Resolution:** Fix all references to :7071.

### C5: forge_* Tool Names in Docs Not in Source

Docs reference forge_systemctl, forge_accessible, forge_audit, etc. — these don't exist in A-FORGE source.

**Risk:** MEDIUM — agents may try to call non-existent tools.
**Resolution:** Remove references to non-existent tools from docs.

### C6: WELL "degraded" vs "down" Semantics

WELL health returns "degraded" (biometrics expired 73 days), but some code/docs treat any non-"healthy" status as "down."

**Risk:** HIGH — federation conformance harness originally failed on this.
**Resolution:** "degraded" = evidence freshness degraded, NOT organ down. Code must accept "degraded" as valid.

