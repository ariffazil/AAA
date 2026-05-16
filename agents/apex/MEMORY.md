# MEMORY.md — arifOS Federation State

## Memory policy
- Store verified system truths, hard constraints, and active holds
- Mark volatile operational facts with verification date and observer
- Separate observed facts from interpretation

## System snapshot
Observed: 2026-05-05 by Apex (af-forge VPS)

- VPS: af-forge (srv1325122.hstgr.cloud)
- Kernel: Linux 6.17 Ubuntu x86_64
- Disk: 193GB total, 79% used, ~42GB free
- RAM: 15Gi total, ~3.4Gi used, ~12Gi available
- Swap: 19Gi total, ~1Gi used

## Container topology
Observed: 2026-05-05 by Apex

| Container | Image | Port | Status | Notes |
|---|---|---:|---|---|
| arifosmcp | ghcr.io/ariffazil/arifos:c8ed7bd5 | 127.0.0.1:8080 | healthy | 13 tools |
| af-bridge-prod | a-forge-af-bridge | 127.0.0.1:7071 | healthy | bridge |
| geox_eic | af-forge-geox | 8081, 8000 | healthy | 31 tools |
| geox_gui | nginx:alpine | 80 | up | React/Cesium frontend |
| vault999 | compose-vault999:v1.0.0 | 127.0.0.1:8100 | healthy | ledger |
| wealth-organ | compose-wealth-organ:v1.0.0 | 127.0.0.1:8082 | up | 19 tools |
| well | ghcr.io/ariffazil/well:3636af33 | 127.0.0.1:8083 | up | 88+ tools |
| redis | redis:7-alpine | 6379 | healthy | infra |
| qdrant | qdrant/qdrant:latest | 6333-6334 | up | vector DB |
| postgres | postgres:16-alpine | 5432 | healthy | DB |
| ollama-engine-prod | ollama/ollama:latest | 11434 | up | model runtime |
| aaa-a2a | a2a-server-aaa-a2a | 3001 | healthy | isolated network |
| buildx_buildkit_sharp_mahavira0 | moby/buildkit:buildx-stable-1 | — | up | build cache manager, not runtime service |

## MCP surfaces
Observed: 2026-05-05 by Apex

| Server | Port | Transport | Tools | Verification note |
|---|---:|---|---:|---|
| arifOS | 8080 | streamable-http | 13 | live |
| GEOX | 8081 | streamable-http | 31 | live |
| WEALTH | 8082 | SSE-only | 19 | POST path blocked / incompatible with current caller path |
| WELL | 8083 | FastMCP | 88+ | reflect-only behavior observed |

## Canonical arifOS tools
Source of truth: live Space canon, naming convention arif_<noun>_<verb>

- arif_session_init · arif_sense_observe · arif_evidence_fetch · arif_mind_reason
- arif_kernel_route · arif_reply_compose · arif_memory_recall · arif_heart_critique
- arif_gateway_connect · arif_ops_measure · arif_judge_deliberate · arif_forge_execute · arif_vault_seal

## Public routing
Observed: 2026-05-05 by Apex

- arifOS.arif-fazil.com → arifosmcp:8080
- geox.arif-fazil.com → geox_eic:8081
- wealth.arif-fazil.com → wealth-organ:8082
- well.arif-fazil.com → well:8083
- aaa.arif-fazil.com → aaa-a2a:3001
- ollama.arif-fazil.com → ollama-engine-prod:11434

## Verified gaps
- CLAIM: GEOX bridge returns SIMULATED data in current bridge code path; not yet wired to live MCP path end-to-end
- CLAIM: WEALTH and/or WELL transport mismatch blocks clean federation from current arifOS caller path
- CLAIM: arifOS container currently cannot use postgres cleanly in-container
- CLAIM: arifOS container currently cannot use redis cleanly in-container

## Hard guards
- 888 HOLD before destructive cleanup
- No docker system prune -a or docker volume prune without explicit human approval
- Itemize volume deletions per volume
- Verify RAM/swap state before cleanup or restart operations

## Language/tooling coverage
- Python: strong · TypeScript: strong · Shell: partial · SQL: partial/buried · Go: absent · Rust: absent

## Active holds
1. ARCH-001 — arif_mind_reason forge-dispatch boundary unclear; sovereign review required
2. GEOX-BRIDGE-001 — geox bridge still simulated; live MCP wiring pending
3. FED-SSE-001 — federation transport mismatch; SSE client or transport adaptation required

## Unknowns
- Whether all federation failures are transport-only, versus auth/session propagation issues
- Whether postgres/redis failures are dependency, network, or packaging faults inside arifOS container
- Whether ArifScript draft is approved for enforcement or still proposal-stage

## Last verified
- 2026-05-05 by Apex — awaiting sovereign review
- Seal: 999 — DITEMPA BUKAN DIBERI
