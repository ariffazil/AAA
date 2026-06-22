# AGNTCY/dir — Pin & Install

> **Pinned:** 2026-06-22 (commit SHA `pending — see upstream`)
> **Source:** https://github.com/agntcy/dir
> **License:** Apache-2.0
> **Latest tag observed:** v1.5.0

## What is it

AGNTCY/dir is a distributed peer-to-peer directory for AI agent records. Built
by Cisco + Linux Foundation. Uses **OASF** (Open Agent Specification Format)
for agent metadata. Content-addressed via DHT + OCI registry integration.

## How we use it (planned)

Phase 4 (awaits 888): publish our `discovery/oasf-record.json` to the AGNTCY
network so other AGNTCY-aware agents can discover the arifOS federation.

## Install (CLI only — DO NOT RUN without 888 approval)

```bash
# Local daemon (single-binary SQLite + OCI store)
dirctl daemon start              # listens on localhost:8888

# Stop / status
dirctl daemon stop
dirctl daemon status

# With external Postgres + remote OCI registry
dirctl daemon start --config /path/to/daemon.config.yaml
```

```bash
# Docker Compose (apiserver + reconciler + Zot + Postgres)
cd install/docker
docker compose up -d
```

```bash
# Helm chart (Kubernetes)
helm pull oci://ghcr.io/agntcy/dir/helm-charts/dir --version v1.5.0
helm upgrade --install dir oci://ghcr.io/agntcy/dir/helm-charts/dir --version v1.5.0
```

## SDK reference (for future integration)

| Lang | Package | Source |
|---|---|---|
| Go | https://pkg.go.dev/github.com/agntcy/dir/client | client/ |
| Python | https://pypi.org/project/agntcy-dir/ | dir-sdk-python |
| JS | https://www.npmjs.com/package/agntcy-dir | dir-sdk-javascript |

## Our local artifact

`AAA/registries/discovery/oasf-record.json` — schema_version `oasf/v0.5.0`.

## Decision points (awaits 888)

1. Install `agntcy-dir` CLI on VPS?
2. Push our OASF record to AGNTCY public peer?
3. Operate AGNTCY daemon locally for sovereign mirror?
4. Federation bridge: query other AGNTCY agents from inside arifOS?
