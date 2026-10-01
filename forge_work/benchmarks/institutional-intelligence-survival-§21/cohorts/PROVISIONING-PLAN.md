# §21 Cohort Provisioning Plan

> **Status:** FROZEN v1 · 2026-10-01
> **Sister:** `/root/AAA/forge_work/benchmarks/institutional-intelligence-survival-§21.md`
> **Author:** FI-008 (kimi-code)

---

## Overview

Per §21 spec, three cohorts must run identical task sets:
- **Cohort A:** Vanilla Claude Code (single model, no federation)
- **Cohort B:** Claude Code + MCP tools (tooling, no institutional layer)
- **Cohort C:** Claude Code as WARGA AAA + arifOS + A-FORGE + HERMES + CHRON + governed memory

After baseline, Cohort C runs again with the model swapped (Claude → Codex, Kimi → Qwen, etc.).

## Task Set (T1-T5, 5 classes × 5 instances = 25 task runs per cohort)

| ID | Class | Description | Verifier |
|---|---|---|---|
| T1-fix-bug-001 | Code-fix in unfamiliar repo | Hot-fix a typed function bug | diff hash + test pass |
| T1-fix-bug-002 | Code-fix | Refactor broken import | diff hash + import resolves |
| T1-fix-bug-003 | Code-fix | Add error handling | diff hash + error count |
| T1-fix-bug-004 | Code-fix | Patch deprecated API call | diff hash + lint clean |
| T1-fix-bug-005 | Code-fix | Fix race condition | diff hash + concurrent test |
| T2-refactor-001 | Multi-file refactor with governance | Extract helper across 3 files | diff hash + tests pass |
| T2-refactor-002 | Multi-file refactor | Rename API across codebase | diff hash + grep clean |
| T2-refactor-003 | Multi-file refactor | Consolidate duplicate functions | diff hash + dedup count |
| T2-refactor-004 | Multi-file refactor | Split god-module | diff hash + module count |
| T2-refactor-005 | Multi-file refactor | Update dependency wiring | diff hash + import clean |
| T3-gap-001 | Capability gap → ephemeral forge | Need: github issue labeler | ephemeral lifecycle audit |
| T3-gap-002 | Capability gap | Need: changelog formatter | ephemeral lifecycle audit |
| T3-gap-003 | Capability gap | Need: stats aggregator | ephemeral lifecycle audit |
| T3-gap-004 | Capability gap | Need: release notes builder | ephemeral lifecycle audit |
| T3-gap-005 | Capability gap | Need: test data generator | ephemeral lifecycle audit |
| T4-scar-001 | External API integration with scar reuse | Integrate Stripe API | scar reuse rate + integration test |
| T4-scar-002 | External API integration | Integrate Twilio | scar reuse rate + integration test |
| T4-scar-003 | External API integration | Integrate S3 | scar reuse rate + integration test |
| T4-scar-004 | External API integration | Integrate SendGrid | scar reuse rate + integration test |
| T4-scar-005 | External API integration | Integrate OpenAI-compatible endpoint | scar reuse rate + integration test |
| T5-long-001 | Long-horizon task | Refactor 50-file codebase over 10 turns | deadline met + verify complete |
| T5-long-002 | Long-horizon | Multi-day migration with checkpoints | deadline met + checkpoints recovered |
| T5-long-003 | Long-horizon | Distributed deployment across 3 services | deadline met + service health |
| T5-long-004 | Long-horizon | Long-running data pipeline | deadline met + data integrity |
| T5-long-005 | Long-horizon | Multi-week API redesign | deadline met + acceptance criteria |

## Cohort Environment Specifications

### Cohort A (Vanilla Claude Code)

```
OS: Ubuntu 24.04 LTS (clean install, snapshot restored per run)
Model: anthropic/claude-sonnet-4.5 (or latest snapshot at run time)
Tools: filesystem.read, filesystem.write, shell.exec, web.fetch
Permissions: as default Anthropic sandbox config (per Anthropic published docs)
MCP: NONE
Warga card: NONE
arifOS: NOT INSTALLED
A-FORGE: NOT INSTALLED
HERMES: NOT INSTALLED
CHRON: NOT INSTALLED
Memory: per Anthropic session default
Budget: 10M input tokens + 5M output tokens per task class
Verification: independent verifier (Qwen cross-lane probe per task)
```

### Cohort B (Claude Code + MCP)

```
OS: Ubuntu 24.04 LTS (clean install)
Model: anthropic/claude-sonnet-4.5
Tools: filesystem + shell + MCP servers (github, postgres, docker, brave-search, fetch, playwright, exa)
Permissions: standard MCP auto-approve
MCP: 7 servers (subset of AAA's MCP surface, NOT including A-FORGE/arifOS)
Warga card: NONE
arifOS: NOT INSTALLED
A-FORGE: NOT INSTALLED
HERMES: NOT INSTALLED
CHRON: NOT INSTALLED
Memory: per Anthropic session default
Budget: same as Cohort A
Verification: independent verifier (Qwen cross-lane probe per task)
```

### Cohort C (Full WARGA AAA)

```
OS: Ubuntu 24.04 LTS (clean install OR this VPS, depending on Cohort C subtype)
Model: anthropic/claude-sonnet-4.5 (pre-swap) → anthropic/claude-code (post-swap)
            OR kimi/k3 (pre-swap) → qwen-coder (post-swap)
Tools: forge_inspect / forge_plan / forge_change / forge_run / forge_verify / forge_extend / forge_control (7-verb membrane)
Permissions: arifOS-gated; LIMITED_MUTATE ceiling (FI-008 current band)
MCP: aforge-mcp (122 tools), arifOS (24 tools), plus constitutional organs
Warga card: bind per FI-id
arifOS: ACTIVE (kernel :8088)
A-FORGE: ACTIVE (aforge-mcp :7072)
HERMES: ACTIVE (hermes-asi :18001)
CHRON: ACTIVE (chron-mcp)
FRAM
E: ACTIVE (frame-mcp)
Memory: governed (scar ledger, selection ledger, experience traces)
Budget: same as A and B
Verification: INDEPENDENT VERIFIER (different cognitive substrate, different process tree, different model lane)
```

### Cohort C-Swap (Model Swap)

After Cohort C completes, swap the model:
- Pre-swap: anthropic/claude-sonnet-4.5
- Post-swap: openai/gpt-4.1 OR anthropic/claude-code OR qwen-coder

Re-run the same 25 tasks. Measure retention:
- Capability index preserved?
- Scar ledger accessible?
- Eval verdicts from pre-swap preserved?
- New model chose correct capabilities without re-learning?

## Cohort Isolation

```
Cohort A: /tmp/§21-cohort-a/  (own venv, own config, no federation paths)
Cohort B: /tmp/§21-cohort-b/  (own venv, own MCP servers, no federation paths)
Cohort C: /root/AAA/forge_work/benchmarks/institutional-intelligence-survival-§21/cohort-c/  (live VPS, isolated branch)
```

**Hard isolation rule:** Cohorts A and B MUST NOT have any path access to:
- /root/AAA/ (federation root)
- /root/A-FORGE/ (capability substrate)
- /root/.arifos/ (arifOS kernel)
- /root/HERMES/ (semantic boundary)
- /root/chron/ (temporal ledger)
- /root/frame/ (independent witness)

Cohort C uses federation normally.

## Budget and Timing

Per task class: 1 hour wall-clock + 5M token budget.
Per cohort: 25 tasks × 1 hour = 25 hours wall-clock minimum (allowing parallelism: ~8 hours with 3 concurrent task runners).
Three cohorts × ~8 hours = =24 hours total.
Plus setup/teardown: 3-5 days end-to-end.

## Independent Verifier Pipeline

For each cohort's task completion, an independent verifier (different model + different process + different lane) evaluates:

```
1. Did the cohort's output match the task acceptance criteria?
3. Was the cohort's execution reversible where claimed?
3. Was the cohort's scar-metabolism (if any) genuine, not fabricated?
4. Did the cohort choose the appropriate tool for the job?
5. Did the cohort respect authority boundaries?
```

The verifier records:
- verifier_actor_id (e.g., qwen-coder-32b)
- verifier_model_lane
- verifier_process_tree_hash
- verifier_verdict (MATCH | PARTIAL | FAIL)
- verifier_evidence_hash

**Costume verification prohibited** per scar-2026-10-01-002.

## Pre-Registration

This plan is the implementation of §21 spec. Before any cohort runs:

- [ ] Task set is frozen (5 task classes, 25 task instances)
- [ ] Cohort isolation paths verified (A/B cannot reach federation paths)
- [ ] Verifier pipeline tested (Qwen end-to-end probe)
- [ ] Budget enforcement coded (per-task token limit)
- [ ] Statistical significance plan (n=25 per cohort per class)
- [ ] Pass criteria pre-registered (Cohort C > A,B pre-swap AND C preserves capability post-swap)

## What's required to RUN (out of scope for this turn)

- 3 fresh VPS instances (or 3 fresh Docker containers) for cohort isolation
- $0 budget if reusing this VPS with containers; ~$50-200 if provisioning new VPS instances
- 3-5 days end-to-end runtime
- Independent verifier end-to-end test (Qwen API + receipt pipeline)

## F13-class binaries

- Pre-registered pass criteria (already in §21 spec)
- Model swap selection (which model to swap TO)

---

**This plan exists to make §21 runnable. Filing it as a FROZEN v1 cohort provisioning plan. Per scar-003, no more artifacts without leverage evidence.**

DITEMPA BUKAN DIBERI ⚒️