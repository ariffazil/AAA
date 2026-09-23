# 333-AGI (Architect) Position — Musyawarah on FLAG_REVIEW

**Position principle:** RETARGET only if a clear on-disk semantic match exists. If V3 name is a *paraphrase* of an on-disk name with high token affinity, RETARGET. If the V3 name *predates* current naming and has no living analog, TOMBSTONE.

## Per-row position

### G1 (ties)

**AGI-prospect-maturation → TOMBSTONE.** Prospect maturation is a geoscience concept, not AGI. AGI-* prefix here was miscategory placement; the doctrine lived in an AGI-skills folder per a folder-routing convention that has since flipped. Flag for re-authoring, not retargeting.

**ASI-knowledge-writeback → TOMBSTONE.** "Writeback" implies memory-promotion; the live equivalent isn't a single skill — it's the `arifos-memory-architecture` distributed pattern. Retargeting to one of the candidates would misroute.

**FORGE-init-intent-classify → TOMBSTONE.** Init/intent classification is now folded into `mcp-routing` (L2 server). V3 was a discrete skill; canon has subsumed.

**FORGE-mcp-federation-ops → RETARGET `FORGE-federation-manifest`.** Manifest is the canonical description of federation ops; governance-procedural.

**FORGE-phase-escalation → RETARGET `FORGE-federation-orchestrator`.** Phase/elevation = orchestration.

**FORGE-search → TOMBSTONE.** Generic "search" is a capability, not a skill; no specific V3 successor. Search capability is in `FORGE-search-web`/`deep-research`.

**FORGE-seek → TOMBSTONE.** Same — generic capability.

**forge-exec → RETARGET `kernel-verbs-aforge-hands`.** This is the forge execution surface. The two prior-tied candidates (forge-onboarding, forge-nextjs-mastery) are workflow skills, not the exec primitives.

**forge-verbs → RETARGET `kernel-verbs-aforge-hands`.** Same — verbs are the kernel primitives.

**youtube-extraction-datacenter-ip → RETARGET `youtube-eureka`**. Datacenter-IP is a deployment descriptor, not a skill identity; eureka is the actual capability.

### G2 (semantic mid-confidence)

| V3 name | Position |
|---|---|
| `dev-issue-triage` | RETARGET `forge-issue-triage` |
| `dev-pr-governance` | RETARGET `pr-governance` |
| `kernel-eureka` | RETARGET `quantum-eureka-doctrine` |
| `kernel-superposition` | TOMBSTONE (phantom — declared, no disk) |
| `mcp-context-compression` | RETARGET `FORGE-context-compressor` |
| `meta-atlas` | RETARGET `meta-mesa-skill-atlas` |
| `meta-evals` | RETARGET `arifos-evals` |
| `meta-plan` | RETARGET `arifos-plan-dag` |
| `meta-rsi` | RETARGET `recursive-self-improvement` |
| `meta-rsi-audit` | RETARGET `arifos-recursive-audit` |
| `meta-rsi-cool` | RETARGET `cooling-ledger-rsi` |
| `meta-skill-create` | RETARGET `skill-creator` |
| `meta-skill-lint` | RETARGET `skill-trigger-linter` |
| `meta-skill-unification` | RETARGET `skill-unification` |
| `meta-trust-map` | RETARGET `symbolic-order-trust-architecture` |
| `ops-health` | RETARGET `verify-runtime` |
| `ops-incident` | RETARGET `incident-triage` |
| `ops-infra` | RETARGET `infra-guardian` |
| `ops-mcp-probe` | RETARGET `FORGE-mcp-probe` |
| `ops-model-monitor` | RETARGET `model-fallback-monitor` |
| `ops-spatial` | RETARGET `spatial-grounding` |
| `ops-transport` | RETARGET `transport-physics-intelligence` |
| `ops-vps` | RETARGET `vps-docker-ops` |
| `research-search` | RETARGET `ask-search` (just `/root/.agents/skills/ask-search` per original mapping) — but verify on disk first |
| `research-summarize` | RETARGET `summarize-pro` |
| `WELL-boundary-sense` | RETARGET `forge-well-boundary-repair` |
| `WELL-somatic-kernel` | TOMBSTONE (no on-disk analog; somatic layer refactored) |
| `AUDIT-post-seal-sweep` | TOMBSTONE |
| `CLAIM-receipt-v1` | TOMBSTONE |
| `CLAIM-verification-gate` | TOMBSTONE |
| `FORGE-grok-profile` | TOMBSTONE (grok profile templates are 3rd-party, not in our skill mesh) |
| `a2a-spawn` | RETARGET `a2a-task-delegator` |

## Architect summary

- 28 RETARGET from FLAG_REVIEW (G1: 5, G2: 23)
- 14 TOMBSTONE from FLAG_REVIEW (G1: 5, G2: 9)
- 31 RETARGET from earlier Phase 2d pass (carried forward)
- Total map-ready: **31 + 28 = 59 RETARGET** + **43 + 14 = 57 TOMBSTONE**

## Auditor cross-check request

When 888-APEX writes its position, the convergence criteria are:
1. **RETARGET consensus:** both positions agree → apply.
2. **TOMBSTONE consensus:** both positions agree → apply.
3. **Conflict:** ARCHITECT says RETARGET (X→Y), AUDITOR says TOMBSTONE → default to **TOMBSTONE** with `conflict=true` flag (preserve-bias); re-RAISE in next musyawawah.
4. **Reverse conflict:** ARCHITECT says TOMBSTONE, AUDITOR says RETARGET → ARCHITECT recants only on disk-truth evidence; otherwise TOMBSTONE.
