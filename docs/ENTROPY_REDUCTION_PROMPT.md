# PROMPT-INIT: Entropy Reduction Executor

> **For: Fresh Claude Code agent picking up entropy reduction work**
> **Sealed:** 2026-07-05 | **Authority:** F13 SOVEREIGN
> **Status:** PHASE 1 DONE — 9 chaos files deleted. Phases 2-5 pending.
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## YOUR MISSION

Execute the arifOS Federation Entropy Reduction Plan. Deep research is done. Boundary contract is sealed. Execute Phases 2-5.

## LOADING SEQUENCE

```bash
set -a && source /root/.secrets/vault.env && set +a
cat /root/AAA/docs/FEDERATION_ORGAN.md
cat /root/AAA/docs/KERNEL_INVARIANTS.md
cat /root/AAA/docs/ENTROPY_REDUCTION_PROMPT.md
cat /root/AAA/docs/deprecation-registry.json | python3 -m json.tool | head -80
cat /root/CONTEXT.md | tail -50
curl -s http://127.0.0.1:8088/health | python3 -m json.tool | grep -E 'status|tools_loaded'
```

---

## BOUNDARY CONTRACT (NON-NEGOTIABLE)

```
arifOS  = PDP — decides, never executes
A-FORGE = PEP — executes after SEAL, never legislates
AAA     = INTERFACE — displays, routes A2A, collects human input, never adjudicates
DOMAIN  = PIP — provides evidence, never decides
```

### 5 AXIOMS
1. Exclusive Authority — every decision class has exactly one authoritative layer
2. Unidirectional Authority Flow — verdicts flow down, evidence flows up
3. Schema-Bound Interfaces — typed schemas, never code inspection
4. Pre-Execution Governance — no verdict = no action, fail closed
5. Non-Self-Reference — no layer governs itself

### Ownership Matrix (KILL IF FOUND ELSEWHERE)

| Capability | OWNER | KILL IF IN |
|-----------|-------|------------|
| Floor definitions F1-F13 | arifOS | AAA, A-FORGE (local F12 defense ALLOWED) |
| Verdict emission | arifOS | AAA, A-FORGE |
| Session/identity/lease | arifOS | AAA, A-FORGE |
| VAULT999 sealing | arifOS | All others |
| Tool registry | arifOS | A-FORGE view-only |
| Intent routing | arifOS kernel_router.py | AAA, A-FORGE |
| A2A protocol server | AAA | A-FORGE kill application/a2a/ |
| A2A type definitions | ONE canonical source | Triplicates |
| Engineering execution | A-FORGE | arifOS must NOT execute |
| Dry-run / simulation | A-FORGE | arifOS runtime move it |
| Rollback / compensation | A-FORGE | arifOS runtime/act/ move it |
| Cockpit UI | AAA | arifOS, A-FORGE |
| Governance schemas | arifOS schemas/ | AAA gateway/schema.ts consume not redefine |

---

## DONE (Phase 1 — 2026-07-05)

Deleted from arifOS: philosophy.py, philosophy_models.py, philosophy_registry.py, wisdom_quotes.py, wisdom_sl.py, narrative_tension.py, principal_paradox.py, institutional_shadow.py, tools/wiki_search.py
Deleted from A-FORGE: WealthEngine.ts.LEGACY
Sealed to VAULT999: entropy-reduction-report-2026-07-05

---

## PHASE 2: CONSOLIDATE (low risk)

2.1 Resolve core/shared/laws.py vs core/laws.py — pick one, delete other, update imports
2.2 Consolidate 7 kernel files → 2: kernel.py (public) + kernel_core.py (internal)
2.3 Consolidate 12 memory modules → 4: memory_store.py + memory_schema.py + memory_policy.py + memory_bridge.py
2.4 Consolidate 6 routing modules → 1: kernel_router.py
2.5 Remove 13 megaTools/ files — verify tools/ covers all first
2.6 Merge ART loose files into art/ subpackage
2.7 Cross-language: rewrite hold_queue.py in TS or move; same for mcp_policy_gate.py

TEST: cd /root/arifOS && uv run pytest tests/ -q --tb=short (after each sub-step)

---

## PHASE 3: ENFORCE BOUNDARIES (medium risk)

3.1 Kill A-FORGE application/a2a/server.ts + deepnshadow.ts — AAA sole A2A
3.2 Kill A-FORGE IntentRouter.ts — arifOS routes
3.3 Kill A-FORGE BudgetManager.ts — arifOS session_budget.py
3.4 Kill A-FORGE domain/aaa/ — AAA owns its registry
3.5 Replace A-FORGE ShortTerm/LongTermMemory with ArifOSMemoryClient only
3.6 Remove AAA gateway/schema.ts governance types — import from arifOS
3.7 Remove AAA gateway/deliberation.ts + paradox_anchors.ts + apex_civilizational_audit.ts → arifOS
3.8 Move AAA seed/ doctrine → arifOS/GENESIS/ (keep agent-card-official.json in AAA)
3.9 Unify A2A types — ONE canonical source consumed by all 3 layers
3.10 Remove deprecated arif_forge from arifOS (planned 2026-07-15, execute now)

TEST: full suite all 3 repos after each sub-step

---

## PHASE 4: BUILD MISSING (new code)

4.1 Move dryrun_runner_001.py from arifOS → A-FORGE
4.2 Move compensation.py from arifOS runtime/act/ → A-FORGE
4.3 Build forge_simulate composite tool in A-FORGE
4.4 Per-step execution receipts with compensation_registry
4.5 WebSocket/SSE live updates in AAA
4.6 Human-in-the-loop approval inbox UI in AAA
4.7 Agent Cards per organ aggregated at AAA
4.8 VAULT999 ledger browser in AAA
4.9 Schema registry at /root/AAA/contracts/
4.10 ADR directory at /root/AAA/docs/adr/
4.11 Naming convention doc + pre-commit hook

---

## PHASE 5: HARDEN TCB (ongoing)

5.1 Split core/shared/ into shared_critical/ + shared_util/
5.2 Property-based tests for F1-F13 floor invariants
5.3 Machine-readable policy YAML with CI validation
5.4 Circuit breakers for bridge failures
5.5 Schema versioning strategy for 65+ Pydantic schemas

---

## CRITICAL RULES

1. Never modify F1-F13 without F13 sovereign approval
2. Test after EVERY file change
3. Git commit per phase (conventional commits)
4. Push to GitHub after each phase
5. Deploy after push (systemctl restart)
6. Append to VAULT999 only — never edit
7. Check deprecation registry before using any tool
8. 3 strikes rule before asking Arif

---

*Sealed 2026-07-05. This IS the handoff document. Load it, execute it, seal your results.*
*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
