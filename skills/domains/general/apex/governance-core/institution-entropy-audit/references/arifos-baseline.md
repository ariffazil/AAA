# arifOS Federation — Audit Baseline (probed 2026-08-13)

Reality-first starting point for institution entropy audits. Re-probe before relying.
Ports / services / counts drift; use as sanity anchor, not truth.

## Listening ports (subset)
`53 80 443 3000 3001 3100 3456-3460 4000 4001 4010-4012 4099 4222 4317 5001 5432
6333 6334 6380 7071-7074 8080 8081 8083 8088 8090 8092 8094 8125 8222 8444 8787
9000 9001 9090 9100 9120 11434 18000 18081-18086 18089-18091 18093-18096 18789
18900-18901 19999 20241 22888`

Key organs: 8088 arifOS kernel · 7071 A-FORGE · 7073 arifflow (FQ) · 8080 SearXNG ·
18083 WELL · 6333 Qdrant · 6380 FalkorDB · 5432 Postgres.

## Docker (live)
searxng (4h) · searxng-redis (4h) · mcpjam-federation (3d) · minio (2w) ·
falkordb (2w) · qdrant (4d) · postgres (7d). Images: falkordb, postgres:16-alpine,
searxng, qdrant, redis:7, mcpjam/inspector (1.79GB), minio.

## Organ health observations
- 8088 kernel: `deployment_drift_status: drift_detected` — source vs runtime mismatch
  (constitutional concern; investigate via deployment_drift_detail).
- 7071 A-FORGE: `degraded_mode: true`.
- 7073 arifflow: FQ=5.25 OPTIMAL, 1000 receipts — the ONE organ whose flow is straight.
- 18083 WELL: degraded, `G: UNMEASURED`, authority `REFLECT_ONLY`.

## Qdrant collections (17) + counts
`arifOS_skill_mesh`=297 ⚠️dupe-case · `arifos_skill_mesh`=8 ⚠️ (same data, two casings) ·
`arif_evidence`=0 💀 · `arifos_precedent`=0 💀 · `arifos_memory`=49 ·
`arifos_session_memory`=56 · `petronas_knowledge`=1460 (the moat) · `atlas333_eureka`=74 ·
`arifos_constitution`=14 · `arifos_vault_canon`=13 · `arifos_vault_working/quarantine/
ephemeral/sacred` · `federation_shared` · `openclaw_memory` · `test_memory_arch`=0 🪦.
Dims 1024, Cosine.

## FalkorDB GRAPH.LIST + arif_l5_knowledge makeup
Graphs: `arifos`(26) · `arifos_federation`(7) · `arif_l5_knowledge`(101) · `af_forge` ·
`clem-membrane-redteam`(0🪦) · `clem-postfix`(0🪦) · `shadow-decoder`(0🪦) ·
`atlas333_test` · `atlas333_graph` · `sado_knowledge` · `arifOS`(0🪦, dead dup of arifos).

`arif_l5_knowledge` label distribution: 51 Tool · 16 Episode · 12 Fact · 8 Organ ·
7 Domain · 6 Agent · 1 Peer. NOT all tools (partial-probe trap — count fully).

## VAULT999 SEALED_EVENTS.jsonl (963 events, 1.8MB, hash-chained)
Chain keys: `prev_hash, merkle_leaf, chain_hash, integrity_hash`. Samples:
- `vault_seal`(956): has `judge_rationale, ack_irreversible_received, msap_evidence,
  source_integrity, payload.data`.
- `888_JUDGE_EXECUTION`(251): has `verdict, evidence_bundle, floor_alignment,
  confidence_score, blocking_tag`.
- `arifos_333_mind`(121): has `report.reasoning_lanes, metabolic_metadata,
  multimodal_results`.
→ Three heterogeneous event classes; schema must be a family, not one struct.

## Cron (28 root jobs)
arif-commodity-reseal · arif-verify-attestation · arifos-daily-probe · arifos-dreamer ·
arifos-federation-audit · arifos-repo-audit · arifos-sentinel-discovery ·
arifos-site-audit-pipeline · arifos-sovereignty-drill · arifos-vault-tail · certbot ·
entropy-governor · hermes-skill-extract · institution-mae-pulse · memory-helix-rollup ·
openclaw-agentic · pati-sweep · sot-cron-vault-bridge · trading-scan · wealth-briefing ·
well-dream · zai-federation-watchdog · zai-temporal-drift-check ... (+ system ones)

## Top-leverage findings (v1 verdict)
1. VAULT999(963) → precedent+evidence+L5: single metabolize script closes 3 broken
   arrows. Data source is full; only the ingest connector is missing.
2. Wire judge to QUERY precedent first — closes precedent→future-judgment loop.
3. Fix skill_mesh dupe-case + kernel 8088 drift + archive dead graphs (arifOS, clem-*,
   shadow-decoder, test_memory_arch) as F1 quarantine, not rm.