---
name: federation-housekeeping-master
description: Monthly constitutional housekeeping orchestrator — runs the federation's EXISTING audit tools in one ritual (entropy sweep, MCP surface audit, FI mesh check, secret hygiene, repo reality) and closes three real gaps (A2A mesh-vs-live diff, prompt-registry audit, doctrine contradiction scan). Ends with Capability÷Entropy executive ranking. Read-only, receipts mandatory, never self-seals, never mutates. Use when Arif says "housekeeping", "monthly audit", "entropy audit", "capability audit", or on first-Sunday cadence.
author: kimi-code (FI-008)
forged: 2026-08-30
source-artifact: /root/forge_work/2026-08-30-housekeeping-artifact/RECEIVED-ARTIFACT.md
law: Universe Bootstrap (F13, 2026-08-30) — govern capabilities, not implementations
---

# Federation Housekeeping Master — ARIFOS::HOUSEKEEPING::MASTER::v2-forged

**ORCHESTRATOR, bukan pendua.** This skill BINDS existing tools; it never re-implements them. If a bound tool gains a successor, update the pointer — not the logic.

## Law

1. **Capability ÷ Entropy** is the ranking function. Anything raising entropy faster than capability → MERGE / ARCHIVE / DISABLE / DELETE *candidate*.
2. Birth order governs: `ARIF → LAW → CAPABILITY → ORGAN → SERVICE → TOOL → MODEL`. Never audit implementations before capabilities.
3. Read-only. No deletion without evidence. Every finding carries a receipt (path+lines, tool output, or live probe).
4. Verdicts: `SEAL / PARTIAL / SABAR / HOLD / VOID`.
5. **NEVER self-seal.** Reports are *proposed* to 888. DELETE/DISABLE candidates stay candidates — execution is a separate F13 decision.

## When to use

- Arif says: "housekeeping", "monthly audit", "entropy audit", "capability audit"
- Cadence: monthly, first Sunday — **cron NOT installed, awaiting F13 888_HOLD** (F1 boundary; see FORGE-infra-crons)
- After major federation change (mass deploys, new organ, new harness)

## Ritual — phases in order

**P0 STATE** — `now` · `make health` · dirty-repo loop:
`for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL}; do git -C "$d" status -s; done`

**P1 MACHINE** — MCP `forge_entropy_sweep` (path=/root) · `well_machine_diagnose` · `forge_vps_ports`+`forge_vps_services`+`forge_vps_cron` (mode=assert) · `docker system df`

**P2 MCP ECOSYSTEM** — MCP `forge_surface_audit` (organ=all) · `forge_registry_status` · `forge_fingerprint_check` (dupes/drift)

**P3 AGENT CLI** — skill `fi-mesh-check` (live probe all coder CLIs) · skill `AUDIT-agent-skill-mesh` (cross-harness skill sync)

**P4 REPOS + DOCS** — skill `AUDIT-repo-reality` (STUB T1–T4 / ORPHAN / SHIM) · skill `drift-watch` · skill `FORGE-readme-truth-check` (per repo)

**P5 SECURITY** — skill `FORGE-secret-hygiene` · MCP `forge_security_drift_scan` · tail `/var/log/arifos/supply-chain-audit.log`

**P6 A2A DIFF** *(gap module)* — compare `/root/AAA/a2a/mesh-topology-static.json` + `/root/AAA/a2a/agent-cards/` against live A2A endpoints. Flag isolated/duplicate/dead agents, dead routes, routing loops. Output Capability→Agent and Agent→Capability maps.

**P7 PROMPT REGISTRY** *(gap module)* — scan `/root/AAA/prompts/` + `/root/.config/opencode/command/` + launcher prompts. Classify `SYSTEM / KERNEL / EXECUTION / AUDIT / MCP / A2A / AGENT / WORKFLOW`. Flag duplicates, near-duplicates, conflicts, dead prompts. Recommend Canonical Prompt Registry entries — do not create the registry unilaterally.

**P8 DOCTRINE SCAN** *(gap module)* — `/root/AAA/instructions/` + `/root/AAA/governance/` cross-checked against `/root/AAA/docs/deprecation-registry.json`. Find contradictions, duplicates, superseded doctrine. Output `ACTIVE / ARCHIVED / RETIRED` — **no deletion**.

**P9 EXECUTIVE** — per component compute: Capability Contribution, Maintenance Cost, Entropy Cost → classify `ASSET / LIABILITY / ZOMBIE / DORMANT / CANONICAL`. Apply the test: *"If this disappeared tomorrow, would capability decrease?"* — NO → housekeeping candidate. Produce TOP-20 entropy sources, TOP-20 capability sources, TOP-20 delete candidates, TOP-20 merge candidates.

## Finding format (mandatory, every finding)

```
FINDING:
EVIDENCE:   (receipt: path+lines | tool output | live probe)
IMPACT:
RECOMMENDED ACTION:
RISK:
VERDICT:
```

## Output contract

- Full report → `/root/forge_work/housekeeping/YYYY-MM/report.md`
- Chat summary to Arif: BM, verdict-first, ≤20 lines
- Everything destructive remains a *candidate*. This skill never mutates production state.

## Boundaries

- Cron install = 888_HOLD. Never self-install scheduling.
- AAA governed tree = read-only unless 888 ratifies.
- WELL degraded does not block the ritual — mark HOLD findings and continue.
- If a phase's bound tool is down, record `TOOL_DOWN` and proceed — never fabricate findings.
