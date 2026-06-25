<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-06-14 18:08 UTC (999_SEAL — MCP Apps panel + Reference Architecture + governance overlays)
valid_from: 2026-06-14
valid_until: 2026-07-14
confidence: high
scope: /root/AAA
epistemic_status: SOURCE_OF_TRUTH
companion_to: HEXAGON-AGENTS-FORGE-20260614 (SOT alignment — MCP Gate deployment sealed)
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

### Adat Agentic — Operating Doctrine

> **Full doctrine:** [`governance/ADAT_AGENTIC.md`](governance/ADAT_AGENTIC.md)

**Core principle:** Semua alat ada pada semua agen. All tools belong to all agents.

- Adat is **custom** (guidance), not **law** (F1–F13)
- All agents have full read+write access to all MCP servers
- Lane purity is guidance, not restriction — FORGE may audit, AUDITOR may forge
- Permission gates removed by F13 sovereign directive 2026-06-25
- Safety net is the kernel/governance layer, not the permission layer

**What remains strict (law, not adat):**
- VAULT999 append-only (F11 AUDIT)
- Constitutional files protected (F1–F13, gitleaks)
- Production push to main (F1 AMANAH, `ack_irreversible=true`)
- External irreversible actions (F13 SOVEREIGN, 888_HOLD)

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
| Hermes (= Hermes-ASI) | Conversational relay (Telegram bot) | Human-facing chat + A2A bridge | Telegram / A2A | hermes-relay |
| OpenClaw | AGI reasoning engine | General problem solving | Native / A2A | (see agents.yaml) |
| A-FORGE | Build & deploy | Code, infra, execution | A2A / MCP | forge-explorer |
| arifOS | Constitutional guardian | F1–F13 floor enforcement | MCP | arifos-guardian |
| GEOX | Earth intelligence | Geoscience, petrophysics | A2A | geox-witness |
| WEALTH | Capital intelligence | Finance, allocation | A2A | wealth-sentinel |
| WELL | Vitality intelligence | Human readiness | A2A | well-mirror |

> **Naming note (canonical 2026-06-22):** "Hermes" = Hermes-ASI Telegram bot (the conversational agent you call in chat). "APEX" = constitutional judge (888_JUDGE) — separate concern, see below. "555-ASI" = HEXAGON warga (memory + ethical critique), NOT a chatbot. Full naming map: `AAA/registries/discovery/CANON-NAMING.md`.

**APEX (888_JUDGE)** is a constitutional organ of arifOS, not an agent managed by AAA. APEX is NOT Hermes. AAA holds APEX's agent card for discovery purposes only. Verdict authority stays in arifOS.

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
P2P          determines how agents are connected.
A2A          determines how agents communicate.
MCP tools    determine how agents use capabilities.
AAA-Cockpit  displays the governed state and permission leases to Arif.   ← THIS REPO
arifOS       enforces F1-F13 constitutional law and adjudicates verdicts.
A-FORGE      acts and executes mutations after valid SEALs.
VAULT999     seals final audit artifacts.
Arif         remains F13 final sovereign authority.
```

> "AAA is polymorphic by design. When precision matters, qualify the surface."

---

---

## 🪞 SELF-AUDIT & HARDENING — Binding Prompt

> **Added 2026-06-14 — Every AAA agent MUST read before mutating.**

The canonical self-audit and hardening prompt for AAA lives at:

→ [`SELF_AUDIT_PROMPT.md`](./SELF_AUDIT_PROMPT.md)

This prompt enforces the **Reflexion Loop** (000→111→333→555→777→888→999) before ANY AAA mutation. It contains:
- Live AAA state baseline from 2026-06-14
- P0–P4 hardening priorities: non-warga auth wall, agent health attestation, deliberation self-critique, contract drift detection, session binding
- 888_HOLD triggers specific to AAA (A2A auth, agent card format, verdict logic)
- Output format with telemetry stub

**Loading instruction:** When an AAA agent receives a hardening or mutation task, it MUST:
1. Read `SELF_AUDIT_PROMPT.md`
2. Run the full Reflexion Loop before any file change
3. Store the audit trail in `a2a-server/vault/` or forward to VAULT999

**Explicit override:** UI-only changes (React component CSS, labels, layout) may skip the loop. A2A, contracts, schemas, and deliberation changes MUST run the full loop.

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*

<!--
SOT-MANIFEST footer
last_verified: 2026-06-14 (FORGE SOT audit — timestamps bumped, federation aligned)
prev_valid: 2026-06-02
next_action: Production-readiness campaign — community files, metadata, CHANGELOG
-->


## Constitution

The 13 Constitutional Floors (F1–F13; legacy documents may render them as L01–L13) live in **one canonical file**:

→ [arifOS/static/arifos/theory/000/000_CONSTITUTION.md](../../arifOS/static/arifos/theory/000/000_CONSTITUTION.md)

This organ emits the **Evidence Contract** (see Appendix B of the constitution) and does **not** self-judge. arifOS alone reads the envelope and applies F1–F13.

