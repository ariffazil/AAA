# AUTHORITY MAP — generated projection (do not hand-edit)

- generated_at: 2026-10-22T12:05:50Z · generator: `/root/scripts/projection_pipeline.py`
- CONSUMER: every warga agent + human governance review
- FAILURE CLASS: authority enforcement lived as prompt-law while its mechanical sources were undocumented
- RULE: generated from mechanism evidence. Policy stays in F13-owned canon.

> **Namespace warning:** `lane:555-ASI` (agent lane) ≠ `KERNEL 555` (verb number). Two number systems — always label.

## Authority classes (kernel ABI — mechanical)

`ANONYMOUS → OBSERVER → TRUSTED_AGENT → EXECUTOR → SOVEREIGN`

Action classes: `OBSERVE | PREPARE | MATERIAL | IRREVERSIBLE`

SOVEREIGN is a kernel authority class, not an agent: sole power to widen authority and to approve memory promote/forget.

## Lanes

| Lane | Roles | Mechanical enforcement | Prompt-law only |
|---|---|---|---|
| `SOVEREIGN (Arif)` | widen authority, memory promote/forget approval, F13 decisions | kernel authority_required=SOVEREIGN; arif_memory human_approval gate | — |
| `lane:333-AGI` | propose, explore, synthesize | session bind -> authority band (arif_init); forge_lease max_action_class | role boundary vs lane:555-ASI (no cross-lane lease exists) |
| `lane:555-ASI` | verify, challenge, falsify | read-only tool surface (no mutate verbs on lane) | independence beyond provider diversity (scar-2026-10-002: same-model-different-prompt = costume verifier) |
| `lane:888-APEX` | judge, prioritize, authorize | arif_judge verdict -> seal_verdict_id chain (arifosmcp/runtime/tools.py) | verdict independence beyond provider diversity |
| `A-FORGE (executor)` | execute, mutate, deploy | arif_forge requires seal_verdict_id; lease scope/forbidden/max_action_class (src/domain/types/mcp-bridge.ts); tools_sot.yaml per-tool access | — |

## Mechanical enforcement inventory (A4 gap table)
- **lease** — evidence: `/root/A-FORGE/src/domain/types/mcp-bridge.ts` · {"fields": ["scope", "forbidden", "max_action_class"]}
- **tool_surface_slices** — evidence: `/root/A-FORGE/tools_sot.yaml` · {"tool_count": 115}
- **kernel_gate** — evidence: `/root/arifOS/arifosmcp/runtime/tools.py` · {"chain": "arif_judge -> seal_verdict_id -> arif_forge", "capabilities_tracked": 8}
- **hooks_live** — evidence: `/root/.arifos/agents/kimi/hooks` · {"files": [".bak-acah2-20261016-aaa-witness-post.sh", "aaa-completion-check.sh", "aaa-danger-warn.sh", "aaa-mcp-boot-readiness.sh", "aaa-notify.sh", "aaa-prompt-enrich.sh", "aaa-session-close.sh", "aaa-session-end.sh", "
- **governance_default** — evidence: `/root/AAA/arifos_kernel/abi/capability_registry.json` · {"rule": "missing arifos_governance -> BLOCKED (requires_888_hold)"}

## A-FORGE verbs (ceiling per verb)

| Verb | Authority ceiling | Candidates |
|---|---|---|
| `forge_inspect` | OBSERVE_ONLY | 26 |
| `forge_plan` | OBSERVE_ONLY | 0 |
| `forge_change` | OBSERVE_ONLY | 0 |
| `forge_run` | MUTATE | 17 |
| `forge_verify` | OBSERVE_ONLY | 0 |
| `forge_extend` | OBSERVE_ONLY | 0 |
| `forge_control` | MUTATE | 1 |

## Notable
- lane:888-APEX: **may commit permanence** (VAULT999 append = seal); **cannot mutate runtime systems**. Seal IS a write.
- kernel capabilities tracked: 8 · A-FORGE tool surface: 115 · registered agents: 16
- hooks live (/root/.arifos/agents/kimi/hooks): .bak-acah2-20261016-aaa-witness-post.sh, aaa-completion-check.sh, aaa-danger-warn.sh, aaa-mcp-boot-readiness.sh, aaa-notify.sh, aaa-prompt-enrich.sh, aaa-session-close.sh, aaa-session-end.sh, aaa-session-start.sh, aaa-subagent-stop.sh, aaa-turn-classify.sh, aaa-witness-post.sh, aaa-witness-pre.sh, skill-selection-witness.sh
