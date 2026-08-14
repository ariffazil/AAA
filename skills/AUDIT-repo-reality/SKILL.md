---
name: AUDIT-repo-reality
id: audit-repo-reality
risk_tier: low
description: 'REPO_REALITY_AUDIT::v1.2 — Sovereign doctrine (F13, 2026-08-14). Audit codebase reality, not AI output. Categories: STUB Tiers T1-T4, ORPHAN, SHIM, REALITY_LEAK, AUTHORITY_LEAK, CLAIM_DRIFT (A comment/B architecture/C metric), FAKE_METRIC. Pipeline: SCAN→CONTEXT→REACHABILITY→RUNTIME_IMPACT→VERDICT. HEURISTIC≠MEASUREMENT semantics. Nuclear Rule: no abstract feature without concrete consumer. USE WHEN: audit repo, find stubs, reality audit, orphan/shim detection, verify implementation claims.'
version: 2026.08.14.2
tags: [audit, reality, stub, dead-code, orphan, shim, reality-leak, authority-leak, F2, F7, F11]
floor_scope: [F02, F04, F07, F11]
owner: F13 SOVEREIGN (Arif) — forged by 333-AGI
autonomy_tier: T0
reference: REPO_REALITY_AUDIT::v1.2
---

# AUDIT-repo-reality — Repository Reality Auditor

Operating posture: NO TRUST. Regex flags, context judges, reachability determines risk, reality determines verdict. Scanner output = CANDIDATES only.

## Reality Chain
EXISTENCE → REACHABILITY → EXECUTION → DEPLOYMENT → OBSERVABILITY → REALITY. Weakest link = chain verdict: PHANTOM / DEAD / ORPHAN / STUB / SHIM / FAKE_METRIC / THEATRE.

## Stub Tiers (classify before severity)
T1 DOCUMENTARY (comment only, code works) → LOW/REFUTED · T2 DORMANT (exists, zero refs) → ORPHAN · T3 REACHABLE (called, body empty/logs) → HIGH · T4 CONSTITUTIONAL (feeds seal/receipt/vault/ledger) → CRITICAL (authority simulation, false reality factory).

## Categories
REALITY_LEAK: claim about reality without traceable source (health=healthy / W3=0.9 with no derivation). AUTHORITY_LEAK: claim of authorization without verifiable authority chain (regex/format/boolean/Math.random as "approval"). CLAIM_DRIFT: stated reality ≠ implemented reality (A comment / B architecture / C metric). HEURISTIC vs FAKE: labeled prior/rule-based estimate = HEURISTIC (innocent); heuristic presented as measurement = REALITY_LEAK.

## Signatures
SOVEREIGN_TOKEN_THEATRE: Math.random near token generation + approval/sovereign keywords + format-only validation downstream → CRITICAL auto-candidate. COMMENT_LIE: docstring/comment asserts verification the code does not perform. SILENT_FAILURE: try{}catch{}-swallowed authority/bootstrap operations whose downstream failure is untraceable.

## Verdicts + Report
Per-finding: FILE / LINE / SEVERITY / EVIDENCE / WHY_CANDIDATE → agent adds WHY_IT_IS_FAKE or REFUTED (context may acquit). Corruption Score = STUBS×5 + ORPHANS×3 + DEAD×3 + FAKE_METRICS×10 + REALITY_LEAK×10 + TODOS×2 + UNUSED×2; weekly trend, rising = falling health. Insufficient evidence → VERDICT=UNKNOWN. Never invent findings. Reality > diagrams. Running code > docs. Execution trace > claims.
