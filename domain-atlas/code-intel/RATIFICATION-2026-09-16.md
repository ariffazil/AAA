# Code Intelligence — Ratification Record (2026-09-16)

**Sovereign word:** "go and make it work" (F13, 2026-09-16, this session) — ratifies the merged direction assembled from the 7-report external thread (ARIF-Perplexity) × live federation probes × APEX-ZEN Git proposal (2026-09-15, pending → now ratified).

## Decision inventory (binding)

```text
ADOPT    Emerge map-sight (canonical configs: emerge-configs/, regen via /root/.tools/emerge-venv)
         import-linter + dependency-cruiser boundary gates (fail-on-NEW ratchet + expiry-dated exceptions)
         pydeps / Madge quick bounded graphs
         Purpose-specific subgraph doctrine (canonical: never "visualize the codebase")
         Mermaid generated FROM canonical config, never a parallel estate

EXTEND   CodeGraphContext CLI-first (0.6.13, embedded FalkorDB Lite) — semantic layer
         AAA understand suite / Serena LSP / ContextStream / arifFlow+kabarkan as one evidence workflow
         /etc/arifos policy files as machine-consumed graph facts (no new policy DSL)

HOLD     Sourcegraph/SCIP estate (CGC internal parsers cover immediate need)
         Cytoscape Code Atlas UI (until graph semantics stabilize; extends AAA cockpit if ever)
         OTel instrumentation beyond measured arifFlow/kabarkan blind spots

REJECT   Kuzu (FalkorDB live) · Neo4j · new arifos-code-intel-mcp (CGC exists)
         Jaeger/Tempo estate · CodeVisualizer VS Code ext · Structurizr/C4 estate
         "aclip" as present-state dependency (never existed on KVM8)
```

**Backend law:** FalkorDB Lite (embedded, per-worktree) for agent investigation — F1-reversible, no cross-agent contamination. Shared remote FalkorDB ONLY for canonical `main` + ratified facts, via controlled write path. Worktree graphs never auto-promote.

**Core law (constitutional):** an agent may propose from inference; assert only from revision-pinned evidence; execute only within a bounded capability; promote only with human authority.

## Landed state (both witnesses)

| Layer | Owner | Evidence |
|---|---|---|
| Map sight ×7 views + hubs | 333-AGI @ 6313d43e6 | emerge-configs/ + INDEX.md metrics (runtime/tools.py fan-out 179) |
| Python boundary contracts ×4 (1 KEPT, 3 BROKEN = baseline debt) | 333-AGI @ 631d43e6 | importlinter/ — transport→runtime via server.py:3765 sovereign_verify is the hot debt |
| Supply chain (SBOM+dep-graph+alerts ×5, CODEOWNERS) | 333-AGI @ 6313d43e6 | verified cyclonedx endpoint |
| Semantic layer: CGC index arifOS@cf966a98 (3,611 files / 108,449 CALLS) | FI-003 | forge_work/2026-09-16-code-intel-phase0/ |
| TS gate: A-FORGE domain purity CLEAN (446 modules) + 3 cycles (madge) | FI-003 | gates/ |
| Gate detection proven (positive control) + exceptions ledger v1 | FI-003 | ledger/exceptions-ledger.json |
| Envelope + reconciliation schemas v1 (DRAFT, unwired) | FI-003 | schema/ |
| Journey-1 real reconciliation bundle (PLAUSIBLE) | FI-003 | journeys/ |
| Skill: codebase-reality (CLI-first evidence contract) | FI-003 | skills/codebase-reality/ |

## Corrections to prior staging

1. INDEX Phase 3 "Kuzu-backed MCP" → **superseded**: CGC 0.6.13 + embedded FalkorDB Lite is the ratified engine (live-proven this session; Kuzu rejected).
2. FI-003 whole-repo GEOX map → superseded by 333-AGI GEOX-live view (archive-contamination finding).
3. Rename divergence (pyproject SEAL says arifos; tree + 333-AGI root_packages say arifosmcp is live): two witnesses now agree arifosmcp = live root. `forge_runtime_verify` remains queued for the wheel-vs-tree close-out.

## Open decisions (F13 pen)

- Envelope naming — RECOMMENDATION RECORDED (external witness #8, 2026-09-16): general construct stays **FRAME** (organ); task input = **CodeRealityEnvelope**; completed output = **CodeRealityEvidencePacket**. Drafts already match; awaiting F13 word to canonize.
- arifFlow CODE_REALITY_RECONCILIATION wiring — PREP COMPLETE: live enum is Rust `EpistemicLabel` (receipt.rs:91) = OBS/DER/INT/SPEC/SEAL — a confidence axis. Reconciliation classes are a SOURCE axis (intended/static/observed/verified/unknown) — additive extension (new variants + `evidence_source` field), NOT redefinition. Cost: Rust rebuild + arifflow daemon redeploy (/opt/arifflow/bin). Backward-compatible by design.
- Graphiti drift — CLASSIFIED (evidence: forge_work/2026-09-16-code-intel-phase0/graphiti-drift-evidence.md): container CREATED FRESH 2026-09-15T17:10Z, 11 days AFTER 888 retirement (Sep 4); no restart, no compose, manual run, group=arifos, backed by live FalkorDB. Suspected cause: a session executed mcp-shopping-list item #1 ("Graphiti — correct add") without the retirement order being marked in that guidance → **canonical guidance contradiction** (retirement order vs shopping list). CONTRADICTION_LEDGER filing candidate. F13 picks one: (a) ratify reactivation, (b) reaffirm retirement + orderly removal, (c) file contradiction first.
- Ratchet baseline — CAPTURED: `baseline-snapshot-2026-09-16.json` (this dir) — all machine-verified debt from both witnesses. CI fail-on-NEW activation still requires explicit 888 + comparator proof (moved/modified/new distinction + negative tests).

## Standing 888 HOLD

Structural mutations derived from these maps (module moves, boundary-rule removal, canonical graph writes, CI blocking activation, promotion/PR/push beyond T1 commits of THIS record set) require explicit F13 authorization. Static evidence ≠ institutional intent.

## DECIDED by F13 (2026-09-16, "D1 file, D2 yes, D3 yes no deploy, D4a ratify")

| Decision | Outcome | Execution |
|---|---|---|
| **D1** — Graphiti contradiction | **FILED** | canon/CONTRADICTION_LEDGER.json → C-002 instance `C-002-e1` (max-3-active rule respected — filed as evidence instance of Doctrine≠Runtime, not a 4th contradiction). Container untouched. A/B reactivation-vs-retirement remains open under the instance. Root fix queued: retirement orders → machine-readable recommendation constraints. |
| **D2** — Naming triad | **CANONIZED** | canon/CANONICAL_GLOSSARY.md → [CONCEPT] CODE-REALITY Naming Triad: FRAME / CodeRealityEnvelope / CodeRealityEvidencePacket. No variant abbreviations permitted. |
| **D3** — arifFlow evidence-origin | **APPROVED: design + test only** | Proposal: forge_work/.../arifflow-evidence-origin-proposal.md (two-axis: EvidenceOrigin × EpistemicLabel, additive Rust field, golden fixtures, round-trip tests). **NO daemon rebuild/deploy/restart — outside this approval.** Implementation = next focused lane. |
| **D4a** — CI ratchet | **RATIFIED, NARROW** | arifOS@ac94be1ef exactly as implemented: grimp-direct, path-scoped (arifosmcp/**+boundary/**), fail-on-NEW + expired-exception only, in-repo ledger, 2026-12-15 expiry auto-tighten. NOT ratified: expansion to other repos, whole-repo scope, legacy-debt failing, expiry/bypass changes, any broader CI enforcement. Cross-lane authority ambiguity preserved as regression finding: **future sovereign directives crossing an 888 boundary must name the exact fence, action, target, consequence class.** |
