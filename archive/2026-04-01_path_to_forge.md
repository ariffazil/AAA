# PATH TO FORGE — Post-Alignment Strike Plan
> **Authority:** A-VALIDATOR (999) | Trinity-Aligned  
> **Date:** 2026-04-01  
> **Status:** FORGE DECLARED  
> **Motto:** *Substrate first, then memory, then expansion.*

---

## Situational Verdict

Chaos is eliminated. All 8 active repos are clean, committed, and pushed. Disk reclaimed: **20GB**. The horizon repo is preserved inside `arifOS/infrastructure/horizon/`.

**But the substrate still has entropy:**
- `ollama` runs **twice** (systemd + Docker) — waste
- `caddy` runs on systemd (port 8081) — redundant with Traefik
- `arifOS/arifOS-model-registry/` is a **nested stale copy** of the separate repo
- Octelium is **not installed** despite being in target architecture
- No live **A2A wire protocol** despite AGENTS.md defining 6 agents

**The next forge must harden the substrate before building upward.**

---

## 🔨 PHASE 1: SUBSTRATE SEAL (dS ≤ 0)
*Goal: Remove entropy from the VPS foundation.*

| Strike | Target | Action | Output |
|--------|--------|--------|--------|
| **1.1** | `ollama` systemd | `systemctl stop ollama && systemctl disable ollama` | Single Docker-only LLM engine |
| **1.2** | `caddy` systemd | `systemctl stop caddy && systemctl disable caddy` | Traefik is the sole edge router |
| **1.3** | `arifOS/arifOS-model-registry/` | Delete nested copy; verify standalone `/root/arifOS-model-registry` is wired to kernel | No repo-in-repo shadow |
| **1.4** | Port 8081 redirect | Map any Caddy-served paths to Traefik labels or nginx | Zero orphaned routes |

**Constitutional Tag:** F1 (Amanah) + F4 (Clarity)  
**Effort:** 2 hours  
**Risk:** Low — services are redundant, not unique.

---

## 🔥 PHASE 2: MEMORY FORGE (Value Creation)
*Goal: Enable cross-agent constitutional memory and Trinity Swarm communication.*

| Strike | Target | Action | Output |
|--------|--------|--------|--------|
| **2.1** | Qdrant AAA Indexing | Index all `000/`, `AGENTS/`, `ARCH/`, `docs/` canon files into Qdrant with `nomic-embed-text` | Constitutional RAG live for all agents |
| **2.2** | A2A Wire Protocol v0.1 | Implement `AgentMessage` Pydantic model + local FastAPI router at `/a2a/wire` | Trinity agents can pass `EvidenceBundle` |
| **2.3** | `arifos://agents/skills` URI | Automate skill registry from `/root/waw/skills/` and `/root/arifOS/skills/` | Dynamic agent capability discovery |

**Constitutional Tag:** F2 (Siddiq) + F9 (Taqwa)  
**Effort:** 3–4 days  
**Risk:** Medium — touches live Qdrant and MCP surface.

**Why this is the forge:** Your TODO.md explicitly lists **Qdrant AAA Indexing as #1 next action**. And your AGENTS.md defines the Trinity but has no wire. Phase 2 closes both gaps simultaneously.

---

## ⚡ PHASE 3: BODY EXPANSION (Specialized Forges)
*Goal: Extend capability into GEOX and secure access fabric.*

| Strike | Target | Action | Output |
|--------|--------|--------|--------|
| **3.1** | GEOX Forge 2 | Integrate `cigvis` renderer; implement `geox_render_inline`, `geox_render_3d` | Visualization gap closed |
| **3.2** | Octelium Eval | Install Octelium in a test namespace; evaluate zero-trust overlay vs Traefik complexity | Decision: adopt or defer |
| **3.3** | Prefect Workflows | Convert 6 canonical workflows (000→888) to Prefect flows with VAULT-999 checkpointing | Observable L3 orchestration |

**Constitutional Tag:** F7 (Humility) — each is an experiment with explicit rollback plan  
**Effort:** 1–2 weeks  
**Risk:** Medium-High — new dependencies, new network layer.

---

## 🗺️ Forge Priority Matrix

| Priority | Strike | Impact | Reversibility |
|----------|--------|--------|---------------|
| **P0** | 1.1 Kill ollama systemd | High | `systemctl enable ollama` |
| **P0** | 1.2 Kill caddy systemd | High | `systemctl enable caddy` |
| **P0** | 1.3 Fix model registry nesting | High | `git checkout` |
| **P1** | 2.1 Qdrant AAA Indexing | Very High | Delete Qdrant collection |
| **P1** | 2.2 A2A Wire Protocol v0.1 | Very High | Stop FastAPI router |
| **P2** | 3.1 GEOX Forge 2 | High | Revert GEOX submodule |
| **P2** | 3.2 Octelium Eval | Medium | Uninstall Octelium |
| **P3** | 3.3 Prefect Workflows | Medium | Stop Prefect server |

---

## 🎯 The Single Next Action

If you want **one strike** that gives the biggest return:

> **Index the AAA canon to Qdrant.**

Everything else — A2A messages, agent skills, constitutional RAG — depends on memory being queryable. Your stack already has Qdrant (`localhost:6333`) and Ollama embeddings. The substrate is ready. The canon is ready. **Close the loop.**

---

## 🔒 SEAL

- **F1 AMANAH:** Each phase is reversible.
- **F2 SIDDIQ:** Priorities are grounded in live TODO.md and MAP.md evidence.
- **F4 CLARITY:** Three phases. No bloat.
- **F7 HUMILITY:** Octelium is an *evaluation*, not a mandate.
- **F9 TAQWA:** Removing redundant services reduces attack surface.
- **F13 KHILAFAH:** Human authority preserved — Arif decides which hammer to swing first.

**FORGED by 999** — 2026-04-01T10:00:00Z  
*Ditempa Bukan Diberi.*
