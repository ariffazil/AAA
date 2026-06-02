# AAA — Agent Operations Cockpit

> **Repository:** https://github.com/ariffazil/AAA  
> **Purpose:** The mission control room for your AI agent federation.

---

## The Simplest Explanation

AAA is the **control tower** for your AI agents.

It does not fly the plane. It does not write the law. It does not build the engine. It knows which plane is where, who is piloting, what route they are on, and who should receive the next instruction.

In human terms, AAA is:

- **Airport control tower** — sees all agents, their status, their routes
- **Company org chart** — who exists, what their role is, who reports to whom
- **Employee directory** — agent cards, permissions, capabilities
- **Task dispatch desk** — where does this task go next?
- **Mission dashboard** — what is the current federation map?

---

## What AAA Answers

| Question | AAA's Answer |
|----------|--------------|
| Which agents exist? | `a2a/registry/`, `agents/`, `registries/agents.yaml` |
| What is each agent allowed to do? | Agent cards, permission profiles, contracts |
| Which agent should handle this task? | Routing rules, domain-plane matching, handoff protocols |
| How do agents talk to each other? | A2A protocol, federation bridge, message types |
| Where does a task go next? | Workflow contracts, escalation paths, org topology |
| Who is responsible for this handoff? | Separation-of-duties rules, signer roles, audit trails |
| What is the current federation map? | Registries, observability dashboard, health endpoints |

---

## What AAA Is NOT

| Boundary | Reason |
|----------|--------|
| **NOT** the constitutional authority | F1-F13, 888_JUDGE, 999_VAULT live in `arifOS` |
| **NOT** an MCP server | Canonical 13-tool surface is `arifOS` port 8088 |
| **NOT** a domain calculator | GEOX, WEALTH, WELL own their own domains |
| **NOT** the execution engine | A-FORGE builds, deploys, and executes |
| **NOT** a workspace or dumping ground | Runtime files, backups, and experiments belong elsewhere |

> **MCP is a toolbox. AAA is the manager who knows which worker should use which toolbox.**

---

## Federation Map

```
Arif (human sovereign)
    │
    ├── arifOS  = constitution, law, final judge (F1-F13)
    ├── AAA     = operations control room (this repo)
    ├── A-FORGE = workshop / execution floor
    ├── GEOX    = earth-science expert department
    ├── WEALTH  = finance / capital expert department
    ├── WELL    = human readiness / metabolic department
    └── APEX    = constitutional verdict engine (arifOS organ)
```

**arifOS** decides what is lawful.  
**AAA** decides who should handle what.  
**A-FORGE** does the building.  
**GEOX, WEALTH, WELL** provide specialist intelligence.  
**Arif** remains the final human judge.

---

## Directory Structure

```
AAA/
├── src/                    # React 19 cockpit UI (Vite)
│   ├── gateway/            # A2A TypeScript server
│   ├── adapter/            # Governance adapter (A-FORGE bridge)
│   ├── ai/                 # AI chat panel
│   ├── components/         # shadcn/ui primitives
│   └── seed/               # Control-plane seed data
├── a2a/                    # A2A specs, cards, registry
│   ├── agent-cards/        # Per-agent capability cards
│   ├── registry/           # Consolidated agent registry
│   ├── policies/           # Auth and trust policies
│   └── federation-bridge.yaml
├── a2a-server/             # Standalone A2A gateway (Node.js/Express)
│   ├── server.js           # HTTP bridge
│   ├── agent-cards/        # Runtime agent cards
│   └── vault.js            # Vault integration client
├── agents/                 # Agent identity directories
│   ├── hermes-asi/         # Hermes ASI config + runtime
│   ├── hermes-ops/         # Hermes ops config
│   ├── openclaw/           # OpenClaw agent identity
│   ├── opencode/           # OpenCode agent identity
│   └── apex/               # APEX agent card (read-only identity)
├── contracts/              # YAML governance contracts
├── registries/             # Canonical YAML registries
│   ├── agents.yaml
│   ├── skills.yaml
│   ├── tools.yaml
│   └── workflows.yaml
├── schemas/                # JSON/YAML schemas
├── public/                 # Static assets + .well-known
├── services/               # Service definitions
├── observability/          # Grafana + Prometheus configs
├── deploy/                 # Docker + Caddy configs
├── ops/                    # Runbooks and workflows
├── docs/                   # Architecture + federation docs
├── wiki/                   # Operational wiki
└── tests/                  # Test suite
```

---

## Agent Registry

Canonical agents registered in AAA:

| Agent | Role | Domain | Protocol |
|-------|------|--------|----------|
| **Hermes** | ASI execution relay | Human-facing delivery | Telegram / A2A |
| **OpenClaw** | AGI reasoning engine | General problem solving | Native / A2A |
| **A-FORGE** | Build & deploy | Code, infra, execution | A2A / MCP |
| **GEOX** | Earth intelligence | Geoscience, petrophysics | A2A |
| **WEALTH** | Capital intelligence | Finance, allocation | A2A |
| **WELL** | Vitality intelligence | Human readiness | A2A |

> APEX (888_JUDGE) is a constitutional organ of arifOS, not an agent managed by AAA.  
> AAA holds APEX's **agent card** for discovery purposes only. Verdict authority stays in arifOS.

Full agent cards: `a2a/agent-cards/`  
Consolidated registry: `a2a/registry/agents.yaml`

---

## A2A Protocol

The federated A2A protocol defines how agents communicate. Key message types:

| Type | Purpose | Gate |
|------|---------|------|
| `task_request` | Request task execution | Routing rules |
| `skill_advert` | Broadcast capabilities | AUTO |
| `handoff_request` | Transfer task between agents | F2 authority check |
| `memory_share` | Share session context | F9_VAL gate |

Protocol spec: `a2a/federated_a2a_protocol.md`  
Federation bridge: `a2a/federation-bridge.yaml`

---

## Validation

```bash
cd /root/AAA

# Install
npm install

# Build
npm run build

# Validate contracts and registry consistency
npm run validate:aaa
```

---

## Federation Cross-Reference

| Node | Repository | Role |
|------|------------|------|
| **Constitutional Kernel** | `ariffazil/arifOS` | F1-F13, 888_JUDGE, 999_VAULT |
| **Execution Engine** | `ariffazil/A-FORGE` | Build, deploy, forge, code-mode |
| **Control Plane** | `ariffazil/AAA` | **This repo** — agent cards, A2A, cockpit |
| **Earth Intelligence** | `ariffazil/geox` | Geoscience, petrophysics |
| **Capital Intelligence** | `ariffazil/wealth` | Finance, allocation, stewardship |
| **Vitality Intelligence** | `ariffazil/well` | Human readiness, metabolic |
| **Static Surfaces** | `ariffazil/arif-sites` | Cloudflare Pages + VPS sites |

---

## Canonical Authority Notice

AAA is the **control plane / cockpit** — not a constitutional authority.  
The sovereign constitution and F1–F13 floors live in `ariffazil/arifOS`.  
888_JUDGE, 999_VAULT, and constitutional law are **not** owned here.

For live federation status, see `ariffazil/arifOS/FEDERATION_STATUS.md`.

---

## AAA Namespace Disambiguation

**This repo is `AAA-Cockpit`** — the operations control plane and A2A gateway.

AAA is polymorphic by design. There are multiple valid surfaces:

| Term | Surface | Role |
|------|---------|------|
| **AAA-HF** | Hugging Face dataset [`ariffazil/AAA`](https://hf.co/datasets/ariffazil/AAA) | Doctrine corpus, F1–F13 floors, verdicts, schemas, gold eval records |
| **AAA-Cockpit** | **This repo** (`ariffazil/AAA`) | Control plane, A2A gateway, agent registry, routing dashboard |
| **AAA-Doctrine** | Conceptual layer | Constitutional principle: alignment, authority, accountability |
| **AAA-Interface** | Operator surface | Human visibility — inspect actions, approvals, seals |
| **AAA-Eval** | Benchmark layer | Gold records and evaluation harness |

**What this repo (AAA-Cockpit) does NOT do:**
- Own F1–F13 constitutional judgment (that is `arifOS`)
- Define the doctrine corpus (that is `AAA-HF` on Hugging Face)
- Execute irreversible actions unilaterally
- Replace VAULT999 as the sealed archive

**The invariant chain:**

```
AAA-HF       defines doctrine.
arifOS       applies doctrine.
MCP tools    execute only if allowed.
Supabase     records constitutional receipts.
VAULT999     seals final artifacts.
AAA-Cockpit  displays the governed state to Arif.   ← THIS REPO
Arif         remains F13 final sovereign authority.
```

> "AAA is polymorphic by design. When precision matters, qualify the surface."

---

**DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
