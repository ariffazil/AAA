# Federation Reality Graph Discovery (Phase A)
**Document:** `REALITY_GRAPH.md`  
**Standard:** QQQ Protocol · F1 Truth · Actual Reality Over Narrative  
**Date:** 2026-09-14T09:49:30+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::ENTROPY_REDUCTION::REALITY_GRAPH::v1`

---

## 1. Physical Node Inventory & Live State Classification

| Node / Identifier | Purpose | Owner / Process | In / Out | Dependencies | State Classification | Evidence |
|---|---|---|---|---|---|---|
| **arifOS Kernel** | Constitutional Law & Judge | PID 3278714 (`python3 /root/arifOS`) | HTTP :8088 / JSON | Localhost, SQLite, Python 3.13 | **ALIVE** | HTTP 200 `/health` (`healthy`), commit `2a77ed920801` |
| **A-FORGE Core** | Actuator & Engineering | PID 1287666 (`node .../server.js`) | HTTP :7071 / REST | Node.js, Ollama, vault.flat.env | **ALIVE** | HTTP 200 `/health` (`healthy`), genome v2.0 |
| **A-FORGE MCP** | MCP Gateway Protocol | PID 1287666 (`node .../cli.js`) | HTTP :7072 / SSE | A-FORGE Core, Node.js | **ALIVE** | HTTP 200 `/health`, Streamable HTTP active |
| **GEOX Engine** | Earth Reasoning & Basin Physics | Systemd (`geox-static-server`) | HTTP :8081 / JSON | Python, Spatial datasets | **ALIVE** | HTTP 200 `/health` (`healthy`), commit `f154c12` |
| **WEALTH Organ** | Capital Ledger & Financial Math | Systemd (`wealth-organ`) | HTTP :18082 / JSON | Python, DuckDB | **ALIVE** | HTTP 200 `/health` (`healthy`), commit `8e1987c` |
| **WELL Organ** | Human Homeostasis & Dignity | Systemd (`well.service`) | HTTP :18083 / JSON | `state.json`, Biometrics | **ALIVE (Degraded)**| HTTP 200 `/health` (`degraded`, STALE self-report >232h) |
| **FLOW Engine** | Causal DAG & Telemetry Vector | Systemd (`arifflow.service`) | HTTP :7073 / Vector | SQLite, NATS, Python | **ALIVE** | HTTP 200 `/health` (`ok-v3-vector`) |
| **FRAME Observer** | Passive Sovereign Witness | Systemd (`frame-organ.service`) | HTTP :18085 / JSON | Python, Procfs, Disk | **ALIVE** | HTTP 200 `/health` (`ok`), 0 drifts reported |
| **FED LiteLLM Router** | Model Pool & Gateway | Container `nervous_visvesvaraya` | HTTP :4000/:4013 | Docker, Provider APIs | **ALIVE** | HTTP 200 `/health/liveliness`, 47 active models |
| **AAA-A2A Gateway** | Agent-to-Agent Mesh | PID 2371488 (`node server.js`) | HTTP :3001 / JSON | Node.js, Redis, Qdrant, NATS | **ALIVE** | HTTP 200 `/health` on 127.0.0.1:3001, commit `0b37012` |
| **KABARKAN** | Collector & Worker | Systemd (`kabarkan-*`) | HTTP :18084 / Worker | Python, Redis | **ALIVE** | HTTP 200 `/health` (`ok`) |
| **VAULT999 Writer** | Merkle Audit Ledger | Systemd (`vault999-writer`) | HTTP :5001 / JSON | Python, Disk | **ALIVE** | Port 5001 listening, Merkle tree sealed |
| **agentgateway-shadow** | Legacy Gateway Shadow | PID 3894767 (Fossil) | Socket / Daemon | `/root/forge_work/agw/...` | **ORPHAN** | Binary deleted from disk; running purely from RAM |
| **apa-*-bridge (5 units)** | Composio Bridges | PIDs running (Fossils) | Bridges | `/root/venvs/composio/...` | **ORPHAN** | Virtualenv deleted; units active until reboot |
| **FLAME Service** | Retired Free-Tier Proxy | Decommissioned (2026-09-04)| None | None | **DORMANT / DEAD** | Process stopped, port 18901 dead; config residue persists |
| **Ollama Local LLM** | Local Vector & Completion | PID 2432656 (`ollama`) | HTTP :11434 | GPU / RAM | **ALIVE** | Bound 127.0.0.1:11434, memory footprint managed |
| **Qdrant Vector DB** | Memory Store | Docker `qdrant` | HTTP :6333 | Docker | **ALIVE** | 18 collections, healthy |
| **PostgreSQL DB** | Relational Data Substrate | Docker `postgres` | Port 5432 | Docker | **ALIVE** | Healthy (12 days uptime) |
| **MinIO Object Store**| S3 Storage Substrate | Docker `minio` | Ports 9000-9001 | Docker | **ALIVE** | Healthy (12 days uptime) |
