# AAA — Federation Control Plane

> **Canonical Identity:** Agent Operations Cockpit / Federation Control Plane
> **Sovereign:** Muhammad Arif bin Fazil
> **Subordinate To:** arifOS Constitutional Kernel (`ariffazil/arifOS`)
> **Repository:** https://github.com/ariffazil/AAA

---

## Identity

AAA is the **operator interface** to the arifOS Federation. It is the control
plane that governs agent discovery, registration, routing, and observability.

AAA does **not** render constitutional verdicts, execute domain calculations,
or hold live runtime state. It is the **cockpit**, not the **engine**.

---

## Authority Boundary

### AAA Owns
- **Agent Cards** — canonical A2A capability cards per agent
- **A2A Registry** — consolidated agent registry (`a2a/registry/`)
- **A2A Protocol** — federation message routing and specs
- **A2A Gateway** — standalone Express server (`a2a-server/`)
- **Cockpit UI** — React 19 operator dashboard (`src/`)
- **Observability** — Grafana/Prometheus configs (`observability/`)
- **Governance Contracts** — YAML contracts for agent binding (`contracts/`)
- **Registries** — agents, skills, tools, workflows (`registries/`)

### AAA Does NOT Own
- **Constitutional Law** — F1-F13 lives in `arifOS`
- **888_JUDGE** — verdict engine lives in `arifOS` / APEX
- **999_VAULT** — ledger sealing lives in `arifOS`
- **MCP Core Tools** — canonical 13-tool surface is `arifOS` port 8088
- **Domain Calculations** — GEOX, WEALTH, WELL own their domains
- **Live Runtime State** — each organ maintains its own state
- **Production Secrets** — secrets live in `arifOS` vault or organ repos

---

## Canonical Structure

```
AAA/
├── src/                    # React 19 cockpit UI
│   ├── gateway/            # A2A TypeScript server
│   ├── adapter/            # A-FORGE /sense bridge
│   ├── ai/                 # AI chat panel
│   ├── components/         # shadcn/ui primitives
│   └── seed/               # Control-plane seed data
├── a2a/                    # A2A specs, cards, registry
│   ├── agent-cards/        # Per-agent capability cards
│   ├── registry/           # Consolidated agent registry
│   ├── policies/           # Auth and trust policies
│   └── federation-bridge.yaml
├── a2a-server/             # Standalone A2A gateway
│   ├── server.js           # Express HTTP bridge
│   ├── agent-cards/        # Runtime agent cards
│   └── vault.js            # Vault integration client
├── agents/                 # Agent identity directories
│   ├── hermes-asi/
│   ├── hermes-ops/
│   ├── openclaw/
│   ├── opencode/
│   └── apex/
├── contracts/              # YAML governance contracts
├── registries/             # Canonical YAML registries
├── schemas/                # JSON/YAML schemas
├── public/                 # Static assets + .well-known
├── services/               # Service definitions
├── observability/          # Grafana + Prometheus
├── deploy/                 # Docker + Caddy configs
├── ops/                    # Runbooks and workflows
├── docs/                   # Architecture + federation docs
├── wiki/                   # Operational wiki
└── tests/                  # Test suite
```

---

## Validation

Run the canonical validation script:

```bash
npm run validate:aaa
# or
node scripts/validate-aaa.mjs
```

This checks registry consistency, contract cross-references, and A2A card
validity. It does **not** check constitutional compliance — that is `arifOS`'s
responsibility.

---

## Federation Mesh

| Node | Repository | Port (Live) | Role |
|------|------------|-------------|------|
| arifOS | `ariffazil/arifOS` | 8088 | Constitutional kernel |
| GEOX | `ariffazil/geox` | 18081 | Earth intelligence |
| WEALTH | `ariffazil/wealth` | 18082 | Capital intelligence |
| WELL | `ariffazil/well` | 18083 | Vitality intelligence |
| A-FORGE | `ariffazil/A-FORGE` | 7071 | Execution engine |
| AAA A2A | `ariffazil/AAA` | 3001 | A2A gateway (held) |
| APEX | `ariffazil/APEX` | 3002 | Verdict engine (held) |

---

**DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
