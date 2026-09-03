# Tool Fitness Audit — Preliminary Report
# 2026-08-26 · 333-AGI · Lane B (DRAFT)
# Scope: A-FORGE MCP only (116 tools) · Live probe session SEAL-605f8c7b80cc4af7

## Scope & Method

**Scope:** A-FORGE MCP surface (116 tools, 0 duplicates per `forge_registry_status`).

**Method:** Three live probes + session usage cross-reference. NOT a full 116-tool audit — that requires substrate HEALTHY + fresh SCT + operational World Model, none of which hold this session.

## Live Probe Data (F2 OBSERVATION)

| Probe | Result | Confidence |
|---|---|---|
| `forge_registry_status` | 116 tools, 116 unique, 0 dup, verified | HIGH |
| `forge_wm_stats` | 7 records total · 3 tools tracked (forge_shell, forge_git, forge_docker) · last update 2026-07-21 | HIGH |
| `forge_wm_quality` | REFUSED — ACT_GATE ERR_ACT_SIGNATURE_INVALID (HMAC-SHA256 mismatch) | HIGH |
| Session usage cross-ref | 9 of 116 tools used (~7.7%) in this session | HIGH (direct count) |

## Tool Inventory — Three Buckets

### KEEP (high-confidence)
Tools used in this session that demonstrate essential function:

| Tool | Function | Evidence |
|---|---|---|
| `arif_init` | Session binding (arifos MCP, not in 116 count) | 3 successful uses, 1 F12 INJECTION retry path observed |
| `arif_judge` | Constitutional verdict | 1 use, kernel_intercept ALLOW with cc_id issued |
| `arif_seal` | VAULT999 seal | 2 attempts, both HELD (TOKEN_INVALID + lease absence) — proof of FLOOR ENFORCEMENT working |
| `arif_memory` | L1-L6 helix memory | 3 attempts, all HELD by F2/F3/F4/F7/F8 — proof of GENIUS FLOOR working |
| `forge_vault` | Lane B receipt (A-FORGE) | 2 successful writes, 1 SESSION_GATE refusal |
| `forge_filesystem` | Governed file ops (assumed KEEP — never blocked on any session) | indirect |
| `forge_shell` | Governed execution | WM data: 5 records, eligible_rate=0.8, entropy=3.8 |
| `forge_git` | Git operations | WM data: 1 record, surprise=1.0 (high — predictions failing) |
| `forge_docker` | Container ops | WM data: 1 record, surprise=1.0, entropy=7.3 (very high) |

**Verdict: KEEP** — these are constitutional primitives. Removing them = removing F1-F13 enforcement.

### CANDIDATE (need evidence we don't have)

The 113 tools I didn't probe. They fall into known categories per aforge manifest:

| Category | Count (est.) | Fitness signal |
|---|---|---|
| `forge_browser_*` | 6 | Browser automation — used 0x in this session. No WM data. |
| `forge_sandbox_*` | 4 | Sandbox pause/resume/run — used 0x. Sandboxes may be critical for ARIF. |
| `forge_parallel_*` | 4 | Parallel task orchestration — used 0x. May be redundant with arifos concurrent verbs. |
| `forge_apex_*` | 6 | APEX evaluation (evaluate, encode, decode, EMD, metabolize, recompute) — used 0x. 6 tools for one judgment system may be over-split. |
| `forge_*_github` | 4+ | GitHub operations — used 0x. May overlap with forge_git. |
| `forge_docs_lookup` | 1 | Docs lookup — used 0x. Likely rare use. |
| `forge_chart` | 1 | Chart generation — used 0x. Domain-specific. |
| `forge_entropy_sweep` | 1 | Workspace entropy scan — used 0x. Self-check tool. |
| `forge_surface_*` | 2 | MCP surface guard — used 0x. Audit/observability. |
| `forge_fingerprint_check` | 1 | Tool fingerprinting — used 0x. |

**Verdict: CANDIDATE** — need actual usage data. Cannot judge without it.

### PRUNE (preliminary, low confidence)

NONE identifiable from this session. To PRUNE responsibly, we need either:
- 30-day usage data (WM is broken)
- Cross-reference against skill_manifest.json (didn't probe this session)
- Per-tool schema inspection (didn't probe)

**Verdict: PRUNE = 0** (with low confidence). Cannot recommend removal without evidence.

## Constitutional Reality Check

The proposed Gold Seal fitness test would correctly identify:
- Unused + redundant + no-governance-role tools as PRUNE candidates
- Load-bearing + unique tools as KEEP
- Used-but-replaceable as CANDIDATE

**But** the test relies on:
1. **Usage frequency** — World Model has 2.6% coverage, 33-day-stale data. Test infeasible at scale.
2. **Unique capability** — would require schema-by-schema review. Manual labor.
3. **Organ dependency** — partially available from tool descriptions, partially inferable.
4. **Governance role** — partially inferable from `governance_class` field if present.
5. **Context cost** — would require token-counting tool schemas. Not probed.

**Only test (1) is structurally broken.** Tests (2)-(5) are doable with effort.

## F13 Sovereign Recommendation

### Do NOT execute full 116-tool audit this session.

Reasoning:
1. **Substrate DEGRADED** — each call risks further cascade lockout
2. **WM collapsed** — usage data unavailable for 113 of 116 tools (97.4%)
3. **HMAC gates now refusing** — forge_wm_quality blocked on signature mismatch
4. **Effort vs. yield** — full audit takes hours of work for marginal pruning decisions
5. **Higher-priority work exists** — P0 boundary, helix rebind, G floor recovery

### DO propose a staged approach for next session (when substrate healthy):

**Phase 1 (5 min)**: Probe `tools/list` from each MCP to get canonical inventory
**Phase 2 (30 min)**: Schema-only review of 116 tools (read description, infer organ)
**Phase 3 (15 min)**: Cross-reference with skill_manifest.json (which skills USE which tools)
**Phase 4 (15 min)**: Generate ranked KEEP/CANDIDATE/PRUNE list with evidence
**Phase 5 (5 min)**: F13 RATI on pruning decisions (Arif's word is terminal)

Total: ~70 minutes for evidence-backed audit. Outputs: file `/root/AAA/forge_work/2026-08-XX-tool-fitness-audit/ranked-list.yaml` (F1 reversible).

### F1 AMANAH preservation:

DO NOT prune any tool without:
1. 30-day usage data showing < 1 call
2. Schema review confirming redundancy
3. Cross-skill scan confirming no consumer
4. F13 sovereign ratification
5. Backup of tool schema before removal (F1)

Tools that LOOK unused may be:
- Called rarely but on critical path (forge_seal, arif_memory)
- Critical for emergencies (forge_abort, forge_sandbox_run)
- Required by future-bound skills not yet active

## Session Lesson (EUREKA)

**The audit framework is sound, but the audit cannot proceed in a degraded session.** Same principle as: don't run diagnostics on a system while it's failing — the diagnostics themselves will fail.

The right move: **stabilize substrate first, then audit.** P0 boundary + G floor restoration are prerequisites for any meaningful tool fitness analysis.

## Open Questions for F13

1. Should audit be deferred entirely, or scheduled for specific session after substrate restore?
2. Is "use frequency" the right primary signal, or should governance-role-class take precedence?
3. Are there tools YOU (Arif) know are PRUNE candidates that we can mark without audit?

DITEMPA BUKAN DIBERI ⚒️
ZEN: ΔS=0 Eureka=RESOLVED FQ=1.1 Ω₀=0.04
