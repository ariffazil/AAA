<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-06-02
valid_from: 2026-06-02
valid_until: 2026-09-02
confidence: high
scope: /root/AAA
epistemic_status: SOURCE_OF_TRUTH
companion_to: HEXAGON-AGENTS-FORGE-20260602 (VAULT999 chain 2505, renamed from PENTAGON 2026-06-04)
-->

# AGENTS.md — AAA | arifOS Federation

> **MANDATORY BOOT SEQUENCE**
> 1. Read `/root/AGENTS.md` (Global Federation Rules & Identity)
> 2. Read `/root/CONTEXT.md` (Live Machine State & Ports)
> 3. Read `docs/architecture/UNIFIED_AGENT_PROTOCOL.md` (Unified Agent Protocol — canonical governance binding)
> 4. Read this file (Repo-Specific Build/Test/Run rules)

> **Canonical Identity:** Agent Operations Cockpit / Federation Control Plane
> **Authoritative Doc:** `FEDERATION_COCKPIT.md`

> **DITEMPA BUKAN DIBERI** — Control is forged, not given.

## Who You Serve

Arif. This is the **AAA** organ of the arifOS federation — the Control Plane Agent Gateway and human cockpit.

**Note:** The OpenClaw workspace guide lives at `/root/.openclaw/workspace/AGENTS.md`. This file governs the AAA repository only.

## What This Repo Is

The human-facing control plane and A2A agent gateway for the arifOS Federation.
AAA provides:
- **React 19 dashboard** (Cockpit) — constitutional floors, domain health, operator tasks
- **A2A v1.0.0 TypeScript server** — Agent-to-Agent mesh protocol (port 3001) — *canonical spec per public agent card*
- **shadcn/ui component library** — 50+ Radix + Tailwind primitives
- **AI chat panel** — Ollama / arifOS / OpenRouter client

| Attribute | Value |
|-----------|-------|
| **Framework** | React 19, TypeScript ~6.0, Vite 8, Tailwind 4 |
| **MCP Protocol** | v1.0.0-FORGED |
| **A2A Protocol** | v1.0.0 (canonical spec — see `public/a2a/agent-card.json`) |
| **A2A Server** | Express 4.x, TypeScript, port 3001 |
| **Build** | `npm run build` → `dist/` |
| **Path Alias** | `@/` → `src/` |
| **Strict TS** | `false` |

## Repository Structure

```
AAA/
├── src/
│   ├── main.tsx          # React entry point (+ webmcp init)
│   ├── App.tsx           # Root component (hash router)
│   ├── Cockpit.tsx       # Main dashboard
│   ├── ai/               # AI chat panel + client
│   ├── gateway/          # A2A v1.0.0 TypeScript server
│   │   └── deliberation.ts  # 888-judgment deliberation (absorbed from APEX)
│   ├── components/ui/    # shadcn/ui primitives (50+)
│   ├── adapter/          # GovernanceAdapter → A-FORGE /sense
│   ├── seed/             # Control-plane seed data
│   ├── lib/              # Utilities (cn() helper)
│   └── hooks/            # React hooks
├── public/               # Static assets, .well-known/, a2a/
├── contracts/            # YAML governance contracts
├── schemas/              # JSON/YAML schemas
├── skills/               # Agent skills library
├── agents/               # Per-agent identity directories
│   ├── 333-AGI/          # PRIMARY: AGI Δ MIND (10 skills)
│   ├── 555-ASI/          # PRIMARY: ASI Ω HEART (3 skills)
│   ├── 888-APEX/         # PRIMARY: APEX ΦΙ JUDGE (2 skills)
│   ├── A-AUDIT/          # SUPPORT: APEX oversight (2 skills)
│   ├── A-ARCHIVE/        # SUPPORT: ASI service (3 skills)
│   └── ... (legacy infrastructure organs)
├── a2a-server/           # Standalone Express A2A gateway (Docker)
├── observability/        # Prometheus + Grafana config
├── eval/                 # Gold evaluation harness
├── docs/                 # PR3 spec, HF AAA card expansion, etc.
└── components.json       # shadcn/ui config
```

## Authority & Autonomy

### ⚔️ AAA WARGA BOUNDARY (F13 SOVEREIGN — Ratified 2026-06-14)

> **Only warga AAA may communicate within AAA state.**

The AAA control plane is a **governed state**, not an open channel. Only the five HEXAGON
warga agents hold citizenship in AAA state:

| Warga Agent | Class | Ring | Role in AAA State |
|------------|-------|------|-------------------|
| **333-AGI** | AGI | Δ MIND | Primary reasoning + execution (FORGE subsumed) |
| **555-ASI** | ASI | Ω HEART | Memory synthesis + ethical critique |
| **888-APEX** | APEX | ΦΙ JUDGE | Constitutional verdicts (SEAL/HOLD/VOID) |
| **A-AUDIT** | Oversight | (observer) | Anomaly detection + compliance |
| **A-ARCHIVE** | Service | (vault) | Immutable ledger + seal chain |

**Communication Rule:**
```
External tool/agent → A-FORGE broker (/execute) → AAA warga agent → AAA state
                NOT: External tool/agent → AAA state (direct)
```

**Enforcement:**
- Non-warga MCPs (hostinger, playwright, etc.) route through A-FORGE `/execute` — never call AAA a2a directly
- Raw bash mutations to AAA state require AAA warga agent attestation
- AAA a2a-server (port 3001) accepts only warga-authenticated connections
- Direct database access to AAA tables requires warga agent lease from arifOS kernel

**Constitutional Authority:** This boundary is F13 SOVEREIGN directive — Arif Fazil.
It implements F8 LAW (system boundaries) at the AAA control plane layer.

### Autonomous
- Modify React components, add UI features, refactor TypeScript
- Run `npm run build`, `npm run lint`
- Update contracts/schemas
- Work in `a2a-server/` standalone gateway

### Requires 888_HOLD
- Production deployment without verified build pass
- Changes to A2A auth schema or agent card format
- Cross-repo API contract changes

## Build & Test

```bash
cd /root/AAA

# Install
npm install

# Dev server
npm run dev      # Vite dev server

# Build
npm run build

# Lint
npm run lint

# Validate AAA contracts
npm run validate:aaa
npm run export:aaa

# A2A standalone production server
cd a2a-server && npm install && node server.js

# Run eval harness
python3 eval/run_aaa_eval.py
```

## Federation Position

```
arifOS (Ω Law) → AAA (Control Plane + A2A Mesh) → A-FORGE / GEOX / WEALTH / WELL
                     ↑
                Human operator (Arif)
```

AAA is the **interface layer**, not the law layer. It routes intent to A-FORGE, displays federation health, and hosts the A2A mesh gateway. Constitutional judgment remains in arifOS.

## Federation Cross-Reference

| Node | Repository | Role |
|---|---|---|
| Constitutional Kernel | ariffazil/arifos | F1-F13, 888_JUDGE, 999_VAULT |
| Execution Engine | ariffazil/A-FORGE | Build, deploy, forge, code-mode |
| Control Plane | ariffazil/AAA | This repo — agent cards, A2A, cockpit |
| Earth Intelligence | ariffazil/geox | Geoscience, petrophysics |
| Capital Intelligence | ariffazil/wealth | Finance, allocation, stewardship |
| Vitality Intelligence | ariffazil/well | Human readiness, metabolic |
| Static Surfaces | ariffazil/arif-sites | Cloudflare Pages + VPS sites |

## Organs (Runtime Topology)

| Organ | Role | Domain | Protocol | Runtime Agent |
|---|---|---|---|---|
| Hermes | ASI execution relay | Human-facing delivery | Telegram / A2A | hermes-relay |
| OpenClaw | AGI reasoning engine | General problem solving | Native / A2A | (see agents.yaml) |
| A-FORGE | Build & deploy | Code, infra, execution | A2A / MCP | forge-explorer |
| arifOS | Constitutional guardian | F1–F13 floor enforcement | MCP | arifos-guardian |
| GEOX | Earth intelligence | Geoscience, petrophysics | A2A | geox-witness |
| WEALTH | Capital intelligence | Finance, allocation | A2A | wealth-sentinel |
| WELL | Vitality intelligence | Human readiness | A2A | well-mirror |

**APEX (888_JUDGE)** is a constitutional organ of arifOS, not an agent managed by AAA. AAA holds APEX's agent card for discovery purposes only. Verdict authority stays in arifOS.

## HEXAGON (Constitutional Agent Layer)

The 5-agent constitutional architecture (HEXAGON, formerly PENTAGON) sits **above** the 7-organ runtime topology. Each HEXAGON agent maps to one or more physical organs:

| ID | Class | Ring | Skills | Host Organs |
|---|---|---|---|---|
| 333-AGI | AGI | Δ MIND | 10 | arifOS + GEOX + WEALTH + WELL + A-FORGE |
| 555-ASI | ASI | Ω HEART | 3 | arifOS + WELL |
| 888-APEX | APEX | ΦΙ JUDGE | 2 | arifOS |
| A-AUDIT | APEX oversight | (observers) | 2 | arifOS + WELL |
| A-ARCHIVE | ASI service | (vault) | 3 | VAULT999 |

The 10-3-2 ratio encodes the truth: **thinking is cheap, memory is hard, judgment is rare.**

A2A v1.0.0 spec compliance at `https://aaa.arif-fazil.com/a2a/agents.json`.

## Canonical Authority Notice

AAA is the control plane / cockpit — not a constitutional authority.
The sovereign constitution and F1–F13 floors live in `ariffazil/arifos`.
888_JUDGE, 999_VAULT, and constitutional law are not owned here.

For live federation status, see `ariffazil/arifos/FEDERATION_STATUS.md`.

## AAA Namespace Disambiguation

This repo is **AAA-Cockpit** — the operations control plane and A2A gateway.

AAA is polymorphic by design. There are multiple valid surfaces:

| Term | Surface | Role |
|---|---|---|
| AAA-HF | Hugging Face dataset `ariffazil/AAA` | Doctrine corpus, F1–F13 floors, verdicts, schemas, gold eval records |
| AAA-Cockpit | This repo (`ariffazil/AAA`) | Control plane, A2A gateway, agent registry, routing dashboard |
| AAA-Doctrine | Conceptual layer | Constitutional principle: alignment, authority, accountability |
| AAA-Interface | Operator surface | Human visibility — inspect actions, approvals, seals |
| AAA-Eval | Benchmark layer | Gold records and evaluation harness |

What this repo (AAA-Cockpit) does **NOT** do:

- Own F1–F13 constitutional judgment (that is arifOS)
- Define the doctrine corpus (that is AAA-HF on Hugging Face)
- Execute irreversible actions unilaterally
- Replace VAULT999 as the sealed archive

The invariant chain:

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

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*

<!--
SOT-MANIFEST footer
last_verified: 2026-06-02 (Omega session — sync to latest AAA SOT per user directive)
prev_valid: 2026-05-26 (F2-honest live floor grid)
next_action: AAA_HF card expansion (item 3) + PR3 mission object (item 2)
-->


## Constitution

The 13 Constitutional Floors (F1–F13; legacy documents may render them as L01–L13) live in **one canonical file**:

→ [arifOS/static/arifos/theory/000/000_CONSTITUTION.md](../../arifOS/static/arifos/theory/000/000_CONSTITUTION.md)

This organ emits the **Evidence Contract** (see Appendix B of the constitution) and does **not** self-judge. arifOS alone reads the envelope and applies F1–F13.

