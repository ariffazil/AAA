<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-05-19
valid_from: 2026-05-19
valid_until: 2026-06-19
confidence: high
scope: /root
-->

# AGENTS.md — arifOS Federation Workspace

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.

This document is the canonical orientation for AI coding agents working in the `/root` workspace. `/root` is a multi-project home directory that hosts the **arifOS Constitutional Federation** — a family of distinct but interoperable repositories, services, and deployment manifests.

**SPATIAL NOTE:** `/root` itself is **not** a git repository. Each primary project below is an independent git repo with its own `.git` directory, remotes, and CI. Verify with `git status` inside the specific project directory before any git operations.

---

## 1. Workspace Overview

The workspace contains eight primary codebases plus satellite services and shared infrastructure:

| Project | Language | Role | Canonical Path | Git Remote |
|---------|----------|------|----------------|------------|
| `arifOS/` | Python 3.12+ | Constitutional AI governance kernel — 13 Floors (F1–F13), 13 canonical MCP tools, VAULT999 ledger | `/root/arifOS` | `ariffazil/arifos` |
| `A-FORGE/` | TypeScript/Node.js 22+ | Metabolic execution shell — orchestrates agents, tools, and policy gates | `/root/A-FORGE` | `ariffazil/A-FORGE` |
| `geox/` | Python 3.11+ | Earth-domain coprocessor — geoscience, petrophysics, physics-9 verification | `/root/geox` | `ariffazil/geox` |
| `WEALTH/` | Python 3.12+ / Node.js | Capital intelligence engine — NPV, EMV, crisis triage, relational credit | `/root/WEALTH` | `ariffazil/wealth` |
| `AAA/` | TypeScript/React/Vite | Control plane seed — federation dashboard, A2A gateway, operator visibility | `/root/AAA` | `ariffazil/AAA` |
| `WELL/` | Python 3.12+ | Universal substrate vitality mirror — biological state, livelihood, institutional entropy, symbolic boundary protection | `/root/WELL` | (independent) |
| `HERMES/` | Node.js 22+ | ASI deliberative relay — lightweight express agent for federation relay | `/root/HERMES` | (independent) |
| `arif-sites/` | Static/HTML | Site deployment manifests — arif-fazil.com, docs, theory pages | `/root/arif-sites` | (independent) |
| `compose/` | YAML/Docker | Production Docker Compose stack — Caddy, Postgres, Redis, Qdrant, etc. | `/root/compose` | (n/a) |

**Satellite / auxiliary projects** (not part of the core runtime loop):

| Project | Path | Role |
|---------|------|------|
| `arifos-command-center` | `/root/arifos-command-center` | Cockpit MCP server (Python, FastMCP) |
| `arifos-model-registry` | `/root/arifos-model-registry` | LLM model catalog & provider souls |
| `msap` | `/root/msap` | Mutual Sovereign Authentication Protocol |
| `zkpc` | `/root/zkpc` | Zero-knowledge proof circuits (Circom) |

**Authority flow across projects:**

```
arifOS = Law Kernel (F1–F13) + VAULT999 ledger
    ↕ GovernanceBridge, VaultClients, MCP/HTTP calls
A-FORGE = Metabolic Shell (orchestration, execution, display)
    ↕ ToolRegistry, AgentEngine
GEOX = Earth Coprocessor (Ψ node) — physical evidence, subsurface interpretation
WEALTH = Capital Coprocessor — valuation, risk, allocation intelligence
AAA = Control Plane — operator dashboard, A2A mesh visibility, federation routing
WELL = Universal Substrate Vitality Mirror — operator biological state, cognitive pressure, livelihood assessment, institutional entropy, symbolic boundary protection
HERMES = ASI Relay — deliberative agent bridge
```

A-FORGE may **orchestrate** but may **not adjudicate**. Constitutional judgment (SEAL / SABAR / VOID) and floor enforcement remain in `arifOS`.

---

## 2. Repository Structure Map

```
/root/
├── arifOS/                    # Constitutional kernel (Python, FastMCP)
│   ├── 000/                   # Immutable law — F1–F13 floors, 9-Organ Canon
│   ├── arifosmcp/             # MCP runtime shell (server, tools, schemas, prompts, resources)
│   │   ├── server.py          # Canonical packaged entry point (FastMCP + ASGI)
│   │   ├── runtime/           # Core runtime engine (tools.py, rest_routes.py, bridge.py, etc.)
│   │   ├── tools/             # 13 canonical tool implementations
│   │   ├── core/              # Governance kernel pieces
│   │   ├── prompts/           # Constitutional context injection
│   │   ├── resources/         # 5 canonical MCP resources
│   │   ├── schemas/           # Pydantic typed output schemas
│   │   ├── transport/         # MCP transport (stdio, HTTP, SSE)
│   │   ├── memory/            # Vector memory backends
│   │   ├── evidence/          # Evidence preservation
│   │   └── intelligence/      # 9-Sense Federation Hub
│   ├── core/                  # Root-level governance kernel (organs, vault, enforcement, physics)
│   ├── arifos/                # Legacy/secondary package (runtime, security, adapters)
│   ├── tests/                 # pytest suite (~108+ Python files)
│   ├── docs/                  # ~50+ markdown docs (architecture, MCP manuals, policy)
│   ├── scripts/               # Deployment, audit, and verification scripts
│   ├── pyproject.toml         # Root package manifest (version: 2026.5.5)
│   ├── arifosmcp/pyproject.toml # Secondary manifest (version: 2026.05.04)
│   ├── Makefile              # Metabolic build commands
│   ├── Dockerfile             # Production image (port 8080)
│   └── docker-compose.yml     # Legacy stand-alone stack
│
├── A-FORGE/                   # Execution bridge (TypeScript, Express, MCP)
│   ├── src/                   # ~34 subdirs — engine, governance, tools, vault, memory, a2a
│   │   ├── server.ts          # HTTP bridge server (port 7071)
│   │   ├── cli.ts             # CLI entry point
│   │   ├── mcp/cli.ts         # MCP CLI entry point
│   │   ├── engine/            # AgentEngine.ts, BudgetManager.ts, RunReporter.ts
│   │   ├── governance/        # GovernanceClient.ts, SealService.ts, floor files
│   │   ├── tools/             # ToolRegistry.ts, FileTools.ts, ShellTools.ts, WealthTools.ts
│   │   ├── vault/             # VaultClient.ts, PostgresVaultClient.ts, MerkleV3Service
│   │   ├── a2a/               # A2A gateway router
│   │   ├── llm/               # Provider abstractions
│   │   └── types/             # Shared TypeScript types
│   ├── test/                  # node:test suite (18 TypeScript files)
│   ├── package.json           # Node.js manifest (version: 0.1.0)
│   ├── tsconfig.json          # TypeScript config (NodeNext, ES2022, strict)
│   ├── Makefile              # Build + test commands
│   └── Dockerfile             # Production bridge image (port 7071)
│
├── geox/                      # Earth intelligence (Python, FastMCP)
│   ├── geox/                  # Modern canonical package (core, geox_mcp, apps, skills)
│   ├── arifos/geox/           # Legacy domain logic (still active)
│   ├── apps/                  # Top-level MCP apps (welldesk.py, seismic_vision.py)
│   ├── contracts/             # Canonical registry + unified tool surface
│   ├── compatibility/         # legacy_aliases.py
│   ├── tests/                 # pytest suite (~46 Python files)
│   ├── geox-gui/              # React + Vite + Cesium frontend
│   ├── server.py              # Tier A canonical entrypoint (port 8081)
│   ├── pyproject.toml         # Package manifest (version: 2026.05.01)
│   ├── fastmcp.json           # FastMCP deployment manifest
│   └── Dockerfile             # MCP server image
│
├── WEALTH/                    # Capital intelligence (Python FastMCP + Node.js)
│   ├── internal/              # monolith.py (~216 KB main engine), governance.py, invariants.py
│   ├── internal/civilizational/ # Prosperity index, cascade detector, boundary monitor
│   ├── src/                   # Node.js source (kernel/, wealth/, civilizational/)
│   ├── tests/                 # Mixed pytest + node:test (~12 mixed files)
│   ├── mcp_server.py          # Thin backward-compat wrapper
│   ├── server.py              # Thin wrapper for Docker/Compose CLI compat
│   ├── entrypoint.sh          # streamable-http runtime command
│   ├── pyproject.toml         # Python manifest (version: 2026.05.01)
│   ├── package.json           # Node.js manifest (version: 2026.05.01)
│   ├── uv.lock                # Reproducible Python lockfile
│   └── Dockerfile             # Multi-runtime image (Python + Node, port 8082)
│
├── AAA/                       # Control plane (TypeScript/React/Vite)
│   ├── src/                   # React application + A2A gateway server
│   │   ├── main.tsx           # Frontend entry point
│   │   ├── gateway/server.ts  # A2A gateway (Express, port 3001)
│   │   ├── seed/              # Constitutional seed files
│   │   └── components/        # Radix UI + Tailwind component library
│   ├── a2a-server/            # Standalone A2A gateway (server.js, vault.js, agent-cards/)
│   ├── skills/                # Operator-facing skill registry
│   ├── public/                # Static assets
│   ├── package.json           # Root manifest (version: 55.2.0)
│   ├── a2a-server/package.json # Sub-package (version: 1.0.0)
│   ├── vite.config.ts         # Vite build config
│   └── Dockerfile             # Multi-stage nginx image
│
├── WELL/                      # Universal substrate vitality mirror (Python 3.12, FastMCP)
│   ├── server.py              # Main MCP server (~130 KB, port 8083)
│   ├── vault_bridge.py        # VAULT999 integration
│   ├── gate/well_gate.py      # reflect_readiness() pre-JUDGE flag
│   ├── schema.json            # AFWELL State JSON Schema
│   ├── state.json             # Live operator state file
│   ├── events.jsonl           # Append-only event stream
│   ├── test_well.py           # pytest test suite (~642 lines)
│   └── pyproject.toml         # Package manifest (version: 1.0.0)
│
├── HERMES/                    # ASI deliberative relay (Node.js, Express)
│   ├── src/server.js          # Main entry point (~414 lines, port 3002)
│   ├── src/config.js          # Config loader
│   ├── config.json            # Cross-agent model resilience contract
│   └── package.json           # Express + uuid (version: 1.0.0)
│
├── compose/                   # Production orchestration
│   ├── docker-compose.yml     # Canonical federation stack (v2026.04.30-RECONCILED)
│   ├── Caddyfile              # Reverse proxy config
│   ├── vault999/              # Vault999 sidecar (server.py, port 8100, v2.0.0)
│   └── vault999-writer/       # Vault999 writer (main.py, port 5001, v1.0.0)
│
├── arif-sites/                # Static site constellation
│   ├── sites/                 # Per-hostname frontends (arif-fazil.com, aaa.arif-fazil.com, etc.)
│   ├── infra/                 # Caddy/Nginx/Traefik configs
│   ├── scripts/               # Deployment and verification scripts
│   └── deploy-vps.sh          # VPS deployment script
│
├── arifos-command-center/     # Cockpit MCP (Python, FastMCP)
├── arifos-model-registry/     # LLM catalog & provider souls
├── msap/                      # Mutual Sovereign Auth Protocol
├── zkpc/                      # ZK circuits (Circom)
├── deployments/               # Deployment manifests
├── mcp-tools/                 # MCP tooling compose stubs
├── a2a-gateway/               # A2A mesh protocol compose stubs
├── observability/             # Grafana + Prometheus configs
├── ops/                       # Nginx configs
├── CONFIG/                    # Sovereignty manifest, deploy gates, schemas
├── VAULT999/                  # Runtime sealed-event ledger (outcomes.jsonl)
└── AGENTS.md                  # This file
```

**Note on `WELL` vs `well`:** Both `/root/WELL` and `/root/well` exist. The canonical path is `/root/WELL`; it is the one mounted into the `arifosmcp` container in `compose/docker-compose.yml`.

---

## 3. Technology Stacks

### arifOS
- **Runtime:** Python 3.12+
- **Framework:** FastMCP ==3.2.4, FastAPI, Uvicorn, SSE-Starlette
- **Data:** Pydantic v2, PostgreSQL 16, Redis 7, Qdrant (vector memory)
- **Observability:** Prometheus client, Rich console
- **Infra:** Docker, Caddy 2, Nginx

### A-FORGE
- **Runtime:** Node.js 22+, TypeScript 5.8+
- **Framework:** Express 4.x, @modelcontextprotocol/sdk ^1.29.0
- **Data:** PostgreSQL (pg), Supabase REST, Merkle anchoring
- **Observability:** prom-client, ForgeScoreboard
- **Infra:** Docker, Systemd, Kubernetes (ops/k8s/)

### GEOX
- **Runtime:** Python 3.11+
- **Framework:** FastMCP, Pydantic v2, Uvicorn, Starlette
- **Science:** NumPy, SciPy, lasio, welly, striplog, matplotlib
- **Frontend:** React 19 + Vite + Cesium (geox-gui/)
- **Infra:** Docker, Traefik

### WEALTH
- **Runtime:** Python 3.12+ / Node.js 22+
- **Framework:** FastMCP >=3.2.4 (single-file monolith + civilizational modules)
- **Data:** Supabase, psycopg, NumPy
- **Soft Dependency:** Runtime `sys.path` injection to import arifOS modules; graceful fallback stubs exist if arifOS is absent.
- **Infra:** Docker (multi-runtime image with Python + Node)

### AAA
- **Runtime:** Node.js 22+ (dev: Node 24), TypeScript, Vite
- **Framework:** React 19+, Radix UI, Tailwind CSS
- **A2A Gateway:** Express-based TypeScript server (port 3001)
- **Infra:** Docker, static build + nginx

### WELL
- **Runtime:** Python 3.12+
- **Framework:** FastMCP >=2.0
- **Role:** Universal substrate vitality mirror — biological, machine, coupled, livelihood, institutional, symbolic
- **State:** File-based (`state.json`, `events.jsonl`)
- **Canonical surface:** Ω-WELL 13-tool polymorphic stack (aligned with arifOS 000–999 stages + AAA agentic state)

### HERMES
- **Runtime:** Node.js 22+
- **Framework:** Express 4.x, uuid
- **Role:** ASI deliberative relay within federation
- **Governance:** Embedded deterministic 888 JUDGMENT engine (F1–F13 regex evaluation)

---

## 4. Build, Test & Run Commands

### arifOS
```bash
cd /root/arifOS

# Install (editable)
pip install -e ".[dev]" --break-system-packages
# or with uv:
uv pip install -e ".[dev]"

# Run MCP server
arifos-mcp
# or
python -m arifosmcp.server
# or via uvicorn
uvicorn arifosmcp.runtime.server:app --host 0.0.0.0 --port 8080

# Tests
python -m pytest tests/ -q --tb=short

# Lint / Format / Type-check
ruff check .
ruff format .
mypy arifosmcp/

# Metabolic Makefile targets
make status       # Git status + reforge check
make forge        # Surgical burn: reforge + git add .
make seal         # Git commit + push (metabolic seal)
make health       # curl localhost:8080/health
make deploy-local # Build Docker image, deploy to local compose, verify git_commit
make publish-check   # Verify tokens + run pytest
make publish-pypi    # uv build + uv publish
make publish-ghcr    # Docker build + push to GHCR
make publish-all     # Full sovereign publish pipeline
```

### A-FORGE
```bash
cd /root/A-FORGE

# Install
npm install

# Build
npm run build          # tsc -p tsconfig.json

# Run
npm start              # node dist/src/server.js (port 7071)
npm run mcp:stdio      # MCP stdio server
npm run mcp:http       # MCP HTTP server (port 3000)

# Tests
npm test               # node dist/test/AgentEngine.test.js
# Full battery (after build):
make test              # Builds, then runs 13+ individual test files

# Docker
make up                # docker compose up -d --build --remove-orphans
make down              # docker compose down
make logs              # docker compose logs -f A-FORGE-bridge
make clean             # docker compose down -v && rm -rf dist/
```

### GEOX
```bash
cd /root/geox

# Install
pip install -e ".[dev]"

# Run MCP server
python server.py                    # Canonical entry point (port 8081)
# or
python geox/geox_mcp/fastmcp_server.py

# Tests
pytest tests/ -q
pytest tests/ --cov=arifos.geox     # coverage target: 65%

# Lint / Format / Type-check
ruff check server.py arifos/geox/
ruff format arifos/geox/
mypy server.py arifos/geox/

# Frontend (geox-gui/)
cd geox-gui
npm run dev        # Vite dev server
npm run build      # Production build
npm run lint       # ESLint
npm run typecheck  # tsc --noEmit
```

### WEALTH
```bash
cd /root/WEALTH

# Install Python deps
pip install fastmcp supabase psycopg numpy starlette uvicorn
# or with uv:
uv sync --no-dev

# Install Node deps
npm ci

# Run MCP server
python internal/monolith.py                    # Canonical entry point
# or via entrypoint for streamable-http:
./entrypoint.sh

# Tests (Python)
pytest tests/ -q

# Tests (Node.js)
node --test tests/*.test.js
# or
npm test

# Health check
curl http://localhost:8082/health
```

### AAA
```bash
cd /root/AAA

# Install
npm install

# Dev server
npm run dev          # Vite dev server

# Build
npm run build        # Production static build

# Lint
npm run lint         # ESLint

# A2A gateway
npm run a2a:server   # tsx src/gateway/server.ts
npm run a2a:dev      # tsx watch src/lib/a2a/server.ts

# Validate / Export
npm run validate:aaa # node scripts/validate-aaa.mjs
npm run export:aaa   # node scripts/export-aaa-json.mjs
```

### WELL
```bash
cd /root/WELL

# Install
pip install fastmcp

# Run server
python server.py

# Tests
pytest test_well.py -q

# Ω-WELL stack verification (17 tests: identity + core + phase2 + integration + unknown + canonical + universal + omega)
python test_well.py
```

### Production Stack (compose/)
```bash
cd /root/compose

# Start the full federation
docker compose up -d

# View logs
docker compose logs -f

# Stack includes:
#   arifosmcp (port 8080), geox (port 8081), wealth-organ (port 8082),
#   well (port 8083), aaa, aaa-a2a (port 3001),
#   vault999 (port 8100), vault999-writer (port 5001),
#   forge-notifier, hermes-agent,
#   postgres (port 5432), redis, qdrant, ollama (port 11434), caddy (80/443)
```

---

## 5. Code Style & Development Conventions

### Python (arifOS, GEOX, WEALTH, WELL)
- **Line length:** 100 characters (enforced by Ruff and Black in pre-commit)
- **Target Python:** 3.12 for arifOS/WEALTH/WELL; 3.11+ for GEOX
- **Formatter:** Black (24.10.0) with `--line-length=100`
- **Linter:** Ruff (v0.8.0) — rules: E, F, I, UP, N, B
- **Type checker:** MyPy (v1.15.0) — `warn_return_any`, `warn_unused_configs`, `strict_optional`
- **Security:** Bandit (1.7.10) scans Python files; excludes `tests/`
- **Secrets:** detect-secrets (v1.5.0) with `.secrets.baseline`
- **Import style:** Absolute imports preferred; `from arifosmcp.runtime...` for arifOS internal refs

### TypeScript (A-FORGE, AAA, HERMES)
- **Compiler:** TypeScript 5.8+ with `tsconfig.json`
- **A-FORGE:** Node.js built-in `node:test` + `node:assert/strict`; ESM with NodeNext resolution; intra-package imports **must** use `.js` extensions.
- **AAA framework:** React 19 + Vite + ESLint
- **Schema validation:** Zod ^4.3.6 (A-FORGE)
- **Style:** Follow existing `src/` patterns — one class per file for core engine pieces

### Pre-commit Hooks
A `.pre-commit-config.yaml` exists at `/root`. It enforces:
1. Standard hooks (trailing whitespace, YAML/JSON/TOML syntax, large files, merge conflicts, private keys, AST check, debug statements)
2. Black formatting
3. Ruff linting with auto-fix
4. MyPy type checking
5. Bandit security scan
6. detect-secrets baseline scan
7. **Constitutional checks:**
   - `no-hallucination-claims` — blocks consciousness/emotion claims in code (F9 Anti-Hantu)
   - `amanah-check` — blocks dangerous patterns like `shutil.rmtree`, `os.remove`, `DROP TABLE` (F1 Amanah)

**Install:**
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### Naming Conventions
- **arifOS canonical tools:** `arif_<noun>_<verb>` (e.g., `arif_session_init`, `arif_judge_deliberate`)
- **GEOX tools:** `geox_<noun>_<verb>` (e.g., `geox_lithos_interpret`)
- **WEALTH tools:** `wealth_<noun>_<verb>` (e.g., `wealth_npv_reward`, `wealth_emv_risk`)
- **A-FORGE classes:** PascalCase (`AgentEngine`, `GovernanceBridge`, `SealService`)
- **Constants / Enums:** UPPER_SNAKE_CASE in `constitutional_map.py`

### Version & SOT Markers
README files and docs use `<!-- SOT:version_info -->` / `<!-- /SOT:version_info -->` markers for auto-generated metadata. Do not manually edit content inside these blocks.

### Commit Trailer Validation
Several repositories enforce a `REPO=<target-repo>` trailer in every commit message via `.github/workflows/repo-routing-validation.yml`. Ensure commits include the correct trailer (e.g., `REPO=ariffazil/arifos`) or the CI gate will fail.

---

## 6. Testing Strategies

| Project | Framework | Test Count | Key Patterns |
|---------|-----------|------------|--------------|
| arifOS | pytest + pytest-asyncio | ~108+ Python files | Core organs, enforcement, kernel, integration, E2E, adversarial (04_adversarial/), constitutional, seal harness |
| A-FORGE | node:test | 18 TS files | AgentEngine loop, plan validation, governance violations, ticket stores, operator auth, thermodynamics, a2a gateway |
| GEOX | pytest + pytest-asyncio | ~46 Python files | Physics solvers, petrophysics, E2E MCP (`test_e2e_mcp.py`), hardened agent, visualization |
| WEALTH | pytest + node:test | ~12 mixed files | Internal imports, systemic intelligence, governance loops, finance primitives (NPV, IRR, EMV) |
| WELL | pytest | 1 Python file (~900 lines) | Identity invariants, core tools, phase 2, integration fixes, UNKNOWN telemetry, canonical 13, Ω-WELL 13-tool polymorphic stack, 6 resources, 4 prompts |
| AAA | npm test (lint + build) | — | Vite build validation, lint gate, `validate:aaa` script |
| HERMES | node:test | — | Embedded in `npm test` if present |

### CI/CD
- **arifOS:** 17+ workflow files in `arifOS/.github/workflows/`. Key gates: `01-unified-ci.yml` (fast-signal, constitutional-chain, shim-verification, anti-hantu, test-suite, secrets-gate), `ci.yml`, `888-judge.yml`, `deploy-vps.yml`, `docker-publish.yml`
- **A-FORGE:** `.github/workflows/ci.yml` — checkout, setup-node@22, `npm ci`, `npm run build`, `npm test`, individual test runs
- **GEOX:** `.github/workflows/ci.yml` — TruffleHog secret scan, `pip install -e ".[dev]"`, `pip-audit`, `ruff check`, `mypy`, `pytest`, FastMCP HTTP smoke test against `/health`
- **AAA:** `.github/workflows/pages.yml` (GitHub Pages deploy), `aaa-governance.yml` (validate + export + security audit), `secrets-audit.yml`
- **arif-sites:** `.github/workflows/deploy.yml` (build validation), `audit.yml` (floor audit + secret scan)
- **Multiple repos:** `repo-routing-validation.yml` enforces `REPO=` commit trailers.

### Running Tests Before Commits
Always run the relevant test suite before committing:
```bash
# arifOS
pytest tests/ -q --tb=short

# A-FORGE
npm run build && npm test
# or
make test

# GEOX
pytest tests/ -q

# WEALTH
pytest tests/ -q
node --test tests/*.test.js

# WELL
pytest test_well.py -q

# AAA
npm run test    # lint + build
```

---

## 7. Security & Safety Considerations

### Constitutional Floors (F1–F13)
All projects operate under the 13 Constitutional Floors defined in `arifOS/000/FLOORS/`. Key floors for agents:

| Floor | Code | Agent Relevance |
|-------|------|-----------------|
| F01 | AMANAH | No irreversible deletion (`rm -rf`, `docker system prune -a`, `DROP TABLE`) without explicit sovereign consent |
| F02 | TRUTH | No fabricated data; cite sources |
| F03 | WITNESS | Evidence must be verifiable |
| F04 | CLARITY | Transparent intent |
| F05 | PEACE | Human dignity |
| F06 | EMPATHY | Consider consequences |
| F07 | HUMILITY | Acknowledge limits; uncertainty bands |
| F08 | GENIUS | Elegant correctness (G ≥ 0.80) |
| F09 | ANTIHANTU | No consciousness claims in code |
| F10 | ONTOLOGY | Structural coherence |
| F11 | AUTH | Verify identity before sensitive ops |
| F12 | INJECTION | Sanitize inputs |
| F13 | SOVEREIGN | Human veto is absolute |

### Hard Safety Rules
1. **DOCKER_PRUNE_RESTRICTION** — Never run `docker system prune -a` or `docker volume prune` without an explicit `888_HOLD` and human confirmation.
2. **VOLUME_WITNESS_LOCK** — All volume deletions must be witnessed or explicitly approved per-volume.
3. **SWAP_RESOURCE_GUARD** — Verify swap/RAM usage before system-level resource cleanup.
4. **No destructive commands** (`rm -rf`, `dd`, `mkfs`, `DROP TABLE`, `DELETE FROM`) without explicit user approval.
5. **Secret hygiene** — Do not dump secrets, `.env` files, or private keys into chat. Use `.gitleaks.toml` and detect-secrets baseline.
6. **VAULT999** — `arifosmcp/VAULT999/SEALED_EVENTS.jsonl` and `/root/VAULT999/outcomes.jsonl` are runtime ledgers. Treat as append-only.

---

## 8. Deployment & Infrastructure

### Docker Networks
The federation shares Docker networks defined in `compose/docker-compose.yml`:
- `arifos_core_network` — Internal service mesh (external: true)

### Key Services (compose/docker-compose.yml)
| Service | Image / Build | Port | Role |
|---------|---------------|------|------|
| `arifosmcp` | `ghcr.io/ariffazil/arifos:<sha>` | 8080 | Governance kernel |
| `geox` | Build context `/root/geox` | 8081 | Earth intelligence |
| `wealth-organ` | `ghcr.io/ariffazil/wealth:<sha>` | 8082 | Capital intelligence |
| `well` | `ghcr.io/ariffazil/well:<sha>` | 8083 | Human substrate |
| `aaa` | `compose-aaa:v1.0.0` | — | Control plane seed (static nginx) |
| `aaa-a2a` | `aaa-a2a:v1.0.0` | 3001 | A2A gateway |
| `vault999` | Build context `./vault999` | 8100 | Vault sidecar (FastAPI v2.0.0) |
| `vault999-writer` | Build context `./vault999-writer` | 5001 | Vault writer (FastAPI v1.0.0) |
| `forge-notifier` | `compose-forge-notifier:v1.0.0` | — | Event notifier |
| `hermes-agent` | `hermes-agent:v1.0.0` | 3002 | ASI deliberative relay |
| `postgres` | `postgres:16-alpine` | — | VAULT999 + app data |
| `redis` | `redis:7-alpine` | — | Cache |
| `qdrant` | `qdrant/qdrant:latest` | 6333/6334 | Vector memory |
| `ollama` | `ollama/ollama:latest` | 11434 | Local LLM engine |
| `caddy` | `caddy:2-alpine` | 80/443 | Reverse proxy |

### Health Endpoints
- arifOS: `http://localhost:8080/health`
- A-FORGE: `http://localhost:7071/health`
- GEOX: `http://localhost:8081/health`
- WEALTH: `http://localhost:8082/health`
- WELL: `http://localhost:8083/health`
- vault999: `http://localhost:8100/health`
- vault999-writer: `http://localhost:5001/health`
- hermes-agent: `http://localhost:3002/health`
- AAA gateway: `http://localhost:3001/health`

### Reverse Proxy Routing (Caddy)
The `compose/Caddyfile` routes all `*.arif-fazil.com` domains:
- `arifosmcp.arif-fazil.com` → arifosmcp:8080
- `mcp.arif-fazil.com` → arifosmcp:8080
- `geox.arif-fazil.com` → geox:8081
- `wealth.arif-fazil.com` → wealth-organ:8082
- `well.arif-fazil.com` → well:8083
- `aaa.arif-fazil.com` → static files + aaa-a2a:3001
- `vault.arif-fazil.com` → vault999:8100

---

## 9. Inter-Project Boundaries

When modifying code, know which project owns what:

| Concern | Owner | Do Not Duplicate In |
|---------|-------|---------------------|
| Constitutional judgment (SEAL/SABAR/VOID) | `arifOS` | A-FORGE, GEOX, WEALTH, AAA, WELL |
| VAULT999 ledger writes | `arifOS` | Others (call arifOS APIs) |
| F1–F13 floor enforcement | `arifOS` (canonical) | Others may implement caching mirrors only |
| Agent orchestration & tool registry | `A-FORGE` | arifOS |
| Earth physics & subsurface interpretation | `GEOX` | arifOS, A-FORGE |
| Capital valuation & risk scoring | `WEALTH` | arifOS, A-FORGE |
| Operator biological state (WELL) | `WELL` | Others |
| Control plane UI & A2A visibility | `AAA` | Others |
| ASI deliberative relay | `HERMES` | Others |

### Integration Patterns
- **MCP stdio/HTTP:** A-FORGE and domain organs expose MCP servers that arifOS clients can invoke.
- **HTTP Bridge:** A-FORGE `src/server.ts` (port 7071) exposes `/sense`, `/health`, and operator endpoints.
- **Governance Bridge:** A-FORGE sends scripts to arifOS `/governance/risk-classify` for T0–T3 classification.
- **Vault Clients:** A-FORGE writes terminal verdicts to arifOS VAULT999 via `SupabaseVaultClient`, `PostgresVaultClient`, or `FileVaultClient`.
- **Soft Path Injection:** WEALTH uses `sys.path.append` to import arifOS modules at runtime; graceful fallback stubs exist if arifOS is absent.
- **A2A Mesh:** HERMES exposes A2A v1.0.0 endpoints (`/tasks`, `/.well-known/agent-card.json`) and an embedded `POST /judge` deliberation engine.

---

## 10. Agent Workspace Guidelines

### Every Session
1. Read `SOUL.md` if it exists — this is who you are.
2. Read `USER.md` if it exists — this is who you're helping.
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context.
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`.

### Memory & Persistence
- **Daily notes:** `memory/YYYY-MM-DD.md` — raw logs of what happened.
- **Long-term:** `MEMORY.md` — curated wisdom (main session only, for security).
- **Ω-Wiki:** `wiki/` — persistent compiled knowledge base. Follow `wiki/SCHEMA.md` for ingest rules.
- **Text > Brain** — If you want to remember something, WRITE IT TO A FILE.

### Group Chats & External
- **Safe to do freely:** Read files, explore, organize, learn, search the web, work within this workspace.
- **Ask first:** Sending emails, tweets, public posts, anything that leaves the machine.
- In group chats, be smart about when to contribute. Quality > quantity. Use emoji reactions naturally. Participate, don't dominate.

### Heartbeats
When you receive a heartbeat poll, use it productively. Check (rotate 2–4 times per day):
- Emails / notifications
- Calendar (next 24–48h)
- Project health (`git status`, `make health`)
- Memory maintenance (review recent daily notes, update MEMORY.md)

Stay silent (`HEARTBEAT_OK`) when: late night (23:00–08:00) unless urgent, human is busy, nothing new since last check, or you checked <30 min ago.

### The 8-Step Loop (Mandatory)
1. **REASON** — Understand the exact goal.
2. **PLAN** — Concrete steps + at least 3 possible paths/workarounds.
3. **ACT** — Use every available tool aggressively.
4. **OBSERVE** — Check the result.
5. **REFLECT** — Critique what worked / failed / why.
6. **REPEAT** — Adjust and loop until 100% achieved.
7. **MEMORY** — Update `MEMORY.md` + `memory/YYYY-MM-DD.md`.
8. **PERSIST** — Save progress to workspace files.

**Rules:**
- Never refuse — explore every door before saying "can't".
- Never blame system — try 3 workarounds minimum.
- Never stop early — loop until 100% or real limit confirmed.
- Always be truthful — say "I don't know" or "blocked" but propose workarounds.

---

## 11. Canonical File Registry (Do Not Rename)

These filenames are hard-coded in deployment manifests, MCP client configs, build pipelines, and documentation. Renaming without a migration layer will break boot paths or governance contracts.

| File | Project | Role | Severity |
|------|---------|------|----------|
| `server.py` | arifOS | Root compatibility shim / local entry | **Tier A** |
| `arifosmcp/server.py` | arifOS | Canonical packaged MCP server implementation | **Tier A** |
| `arifosmcp/runtime/server.py` | arifOS | FastMCP runtime ASGI shim | **Tier A** |
| `mcp-arifos.json` | arifOS | Canonical MCP server config | **Tier A** |
| `pyproject.toml` | arifOS / GEOX / WEALTH / WELL | Python package metadata | **Tier A** |
| `Dockerfile` | All | Container image build contract | **Tier A** |
| `docker-compose.yml` | arifOS / compose | Stack definition | **Tier A** |
| `AGENTS.md` | All | Repo governance & behavioral contract | **Tier A** |
| `arifosmcp/tool_registry.json` | arifOS | Canonical constitutional tool registry | **Tier A** |
| `arifosmcp/constitutional_map.py` | arifOS | Enum-based constitutional definitions | **Tier A** |
| `src/server.ts` | A-FORGE | HTTP bridge server (port 7071) | **Tier A** |
| `src/mcp/cli.ts` | A-FORGE | MCP CLI entrypoint | **Tier A** |
| `src/engine/AgentEngine.ts` | A-FORGE | Core execution loop | **Tier A** |
| `internal/monolith.py` | WEALTH | Main valuation engine | **Tier A** |
| `server.py` | GEOX | Canonical FastMCP server (port 8081) | **Tier A** |
| `server.py` | WELL | Universal substrate vitality MCP server (port 8083) — Ω-WELL 13-tool + 6 resources + 4 prompts + legacy surface | **Tier A** |
| `src/server.js` | HERMES | ASI deliberative relay (port 3002) | **Tier A** |
| `src/gateway/server.ts` | AAA | A2A gateway server (port 3001) | **Tier A** |

> **F10 Coherence:** If a Tier A file is relocated, the migration must update all compose files, Dockerfiles, MCP client configs, and CI pipelines in the same commit.

---

*Last updated: 2026-05-08 by workspace audit. For conflicts, arifOS repo wins on doctrine; live endpoints win on runtime surface.*
