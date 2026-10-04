# Independent Audit Protocol — Reference (2026-08-07)

The full 6-phase audit pattern Arif pasted for verifying a worker agent's multi-deliverable output.

## When to use

- Arif asks for "Independent Audit, Validation & Seal Review"
- Worker agent has produced multi-deliverable output (audits, schemas, audits of audits)
- Same-author self-audit is acceptable but bounded — second agent for SEAL-grade
- Deliverables include structural claims (counts, ports, file paths) that must be probed live

## The six phases

| Phase | Scope | Time cost |
|---|---|---|
| 0 | Assume nothing — treat every output as a claim | mental |
| 1 | Artifact validation — files exist, line counts match, hashes match | 2 min |
| 2 | Deliverable quality — components exist, connections real, no invention | 5 min |
| 3 | Evidence audit — per-claim probe, downgrade on missing evidence | 10 min |
| 4 | Re-probe — 20% sample of live services, measure agreement rate | 5 min |
| 5 | Hallucination audit — no invented files, ports, services, counts | 3 min |
| 6 | Seal review — final verdict: SEAL / PARTIAL / HOLD / VOID | mental |

## Required output files (07/08/09 shape)

| File | Content |
|---|---|
| 07_validation_report.md | Phase 1-5 findings + artifact_validation table |
| 08_evidence_matrix.md | Per-claim: type (V/D/C/U), evidence, confidence, status |
| 09_seal_review.md | Factual correctness + evidence quality + verdict |
| SUMMARY.md | Top-level orientation (required if 6+ deliverables) |
| 10_housekeeping_report.md | Post-audit drift fixes (renames, cross-refs) |

## Live catches from this session (2026-08-07)

1. **VAULT999 count drift**: cited 38,945; live 38,947 (+2 events during audit) — trivial but real.
2. **Misnamed deliverable**: 04 called "Schema" but was a YAML proposal. Fix: rename to `*_proposal.md` with banner.
3. **Inherited trust**: worker inherited content from killed sibling without review. Auditor caught it.
4. **Doc drift**: `security.md` referenced non-existent `/opt/arifos/app/.signing_key`. Real path = `/opt/arifos/.secrets/did/registry.json` (env var override).
5. **Stale cross-refs after rename**: 5 files broke when 04 was renamed. Fix: grep + replace_all after every rename.
6. **Sibling subagent overwrites**: parallel audit overwrote each other's files. Mitigation: preserve both versions, flag divergence.
7. **Graphiti claim**: worker claimed "timeout" — auditor probed and found healthy with proper MCP handshake.

## Claim types for evidence matrix

| Type | Meaning | Confidence |
|---|---|---|
| V-claim | Probed live in this session | HIGH |
| D-claim | Derived from verified findings | MEDIUM |
| C-claim | Cited from existing files (file:line) | HIGH |
| U-claim | Made but not probed | LOW until verified |

## Seal verdict conditions

| Verdict | When |
|---|---|
| SEAL | All probes green, no fabrication, sovereign approved |
| PARTIAL | Directionally correct, specific failures downgraded, second-pass recommended |
| HOLD | Missing required deliverables, framing wrong, sovereign decision pending |
| VOID | Fabricated claims, broken methodology, unsafe |

Non-negotiable rule: **do not inherit trust from the worker.**
A seal is issued only after verification, not after agreement with conclusions.
