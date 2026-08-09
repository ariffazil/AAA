# arifOS — External Architecture Reference
> **For:** Paste into any AI platform to load full system context
> **Owner:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
> **Last verified:** 2026-08-10

---

## PROMPT TEMPLATE (copy this into any AI)

```
Read these URLs to understand the arifOS federation architecture:

SITE OVERVIEW:
- https://arif-fazil.com/llms.txt (machine-readable site overview — START HERE)

AGENT DISCOVERY:
- https://arif-fazil.com/.well-known/agent.json (identity + capabilities)
- https://arif-fazil.com/.well-known/identity.json (W3C identity)
- https://arif-fazil.com/.well-known/capability.json (capability manifest)
- https://arif-fazil.com/.well-known/did.json (W3C DID document)
- https://arif-fazil.com/.well-known/webmcp.json (WebMCP tool surface)
- https://arif-fazil.com/.well-known/arifos-federation.json (federation manifest)

CONSTITUTIONAL FLOORS:
- https://arif-fazil.com/floors.json (F1-F13 machine-readable)
- https://arif-fazil.com/policy.json (public action policy)

FEDERATION GRAPH:
- https://arif-fazil.com/graph.json (organ nodes + edges)
- https://arif-fazil.com/knowledge/corpus.json (knowledge sources index)
- https://arif-fazil.com/llms.json (structured route map)

HUMAN CONTEXT:
- https://arif-fazil.com/000/claims.json (sovereign claims — Gödel Lock, ZKPC)

GITHUB REPOS (all public):
- https://github.com/ariffazil/arifOS (constitutional kernel)
- https://github.com/ariffazil/A-FORGE (execution shell)
- https://github.com/ariffazil/AAA (control plane + A2A gateway)
- https://github.com/ariffazil/GEOX (earth intelligence)
- https://github.com/ariffazil/WEALTH (capital intelligence)
- https://github.com/ariffazil/WELL (human readiness)
- https://github.com/ariffazil/HERMES (Telegram edge bridge)
- https://github.com/ariffazil/arifFLOW (receipt metabolism)

PUBLIC MCP ENDPOINTS:
- https://mcp.arif-fazil.com/mcp (MCP gateway — streamable HTTP)
- https://arifos.arif-fazil.com/health (kernel health)
- https://geox.arif-fazil.com/health (earth health)
- https://wealth.arif-fazil.com/health (capital health)
- https://well.arif-fazil.com/health (vitality health)
- https://arifos.arif-fazil.com/mcp (kernel MCP)

PUBLIC DOCTRINE PAGES:
- https://arif-fazil.com/words/doctrine (13 Floors visual canon)
- https://arif-fazil.com/doctrine/apex-theory (APEX Theory architecture)
- https://arif-fazil.com/000 (genesis + sovereign identity)
- https://arif-fazil.com/999 (proof + verification)

After reading these, explain back:
1. What arifOS is (constitutional kernel, not an LLM)
2. The 6-organ federation topology + their ports + authority ceilings
3. The 13 constitutional floors (F1-F13) with types
4. The 8 canonical MCP tools (Holy 8 verbs)
5. The APEX Theory of Intelligence (3 layers)
6. The EUREKA 6-plane execution architecture
7. The EMD reflex arc (OpenClaw=SENSE, Hermes=COORDINATE, OpenCode=EXECUTE)
8. The authority chain (human → kernel → execution → seal → vault)
```

---

## REALITY CONTEXT (what's actually live right now)

### Live Organs (all 200 OK as of 2026-08-10)

| Organ | Public URL | Local | Role |
|-------|-----------|-------|------|
| arifOS | `arifos.arif-fazil.com` | :8088 | Constitutional kernel — judges, never executes |
| A-FORGE | `forge.arif-fazil.com` | :7071/:7072 | Execution shell — mutates after SEAL |
| AAA | `aaa.arif-fazil.com` | :3001 | Control plane + A2A gateway |
| GEOX | `geox.arif-fazil.com` | :8081 | Earth intelligence (geoscience) |
| WEALTH | `wealth.arif-fazil.com` | :18082 | Capital intelligence (NPV/EMV) |
| WELL | `well.arif-fazil.com` | :18083 | Human readiness reflection |
| Hermes | (Telegram) | :18089 | Telegram edge bridge |
| arifFlow | (internal) | :7073 | Receipt metabolism + FQ pulse |

### 8 Canonical MCP Tools (the Holy 8)

```
arif_init → arif_observe → arif_think → arif_route → arif_memory
          → arif_judge → arif_forge → arif_seal
```

Only `arif_seal` writes to VAULT999. Only `arif_judge` issues verdicts.
arifOS is the brain. It judges. It never executes.

### EUREKA 6-Plane Architecture

```
┌──────────────────────────────────────────────┐
│  S1 INTENT        Human enters at /000       │
│  S2 CONSTITUTION  F1-F13 floors apply        │
│  S3 THINKING      333-AGI reasons            │
│  S4 EVIDENCE      GEOX/WEALTH/WELL verify    │
│  S5 EXECUTION     A-FORGE mutates            │
│  S6 SEAL          VAULT999 immutably stores   │
└──────────────────────────────────────────────┘
```

### Authority Chain

```
ARIF (F13 SOVEREIGN)
    → arifOS KERNEL (F1-F13 enforcement)
        → 888-APEX JUDGE (verdict)
            → A-FORGE (authorized execution)
                → VAULT999 (immutable seal)
                    → /999 (public verification)
```

---

## APEX THEORY OF INTELLIGENCE

**Source:** https://github.com/ariffazil/AAA (docs/canon/APEX_THEORY.md + docs/APEX_THEORY.md)
**Public:** https://arif-fazil.com/doctrine/apex-theory

### Three Layers

```
L3: CIVILIZATION INTELLIGENCE (ASI)
    What should we do? Why? What does it mean?
    ← Hermes, AAA

L2: GOVERNED EXECUTION (AGI)
    How should we do it? What are the constraints?
    ← A-FORGE, OpenClaw

L1: SUBSTRATE INTELLIGENCE (Domain)
    What are the facts? What is true?
    ← GEOX (earth), WEALTH (capital), WELL (vitality)
```

**Key insight:** No layer can replace the one above it.
- L1 provides evidence but cannot set direction
- L2 executes governance but cannot override L3's purpose
- L3 sets direction but cannot touch reality without L1/L2

**Falsifiable core claim:** An unanchored AI (no sovereign human at /000) cannot produce output with equivalent multi-dimensional structural coherence to anchored arifOS output.

### APEX vs arifOS

| Concept | What |
|---------|------|
| APEX Theory | The theoretical framework — 3-layer intelligence model |
| 888-APEX | The constitutional judge lane — applies the theory |
| arifOS | The kernel — hosts the constitutional floors that APEX enforces |

---

## DOCTRINE SUMMARY

**arifOS is a constitutional intelligence kernel** — not an LLM wrapper, not an agent framework. It is the operating system kernel for autonomous intelligence, enforcing 13 constitutional floors before any tool call, code mutation, or capital decision.

**DITEMPA BUKAN DIBERI** — Forged, Not Given.

| Principle | Meaning |
|-----------|---------|
| Probe before act | `:port/health` and `tools/list` are truth |
| Reversible-first | Irreversible actions → 888_HOLD |
| Floor-checked | Every action passes F1-F13 |
| Sealed-on-truth | No intelligence leaves without a seal |
| Human at /000 | Sovereign human anchors the entire system |

---

## DISCOVERY REGISTRIES

- **Glama:** https://glama.ai/mcp/servers/ariffazil/arifos
- **Smithery:** https://smithery.ai/server/arifos
- **MCP Endpoint:** https://mcp.arif-fazil.com/mcp (streamable HTTP)
