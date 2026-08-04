# Federation topology

> **Canonical map (human):** [`/root/AAA/docs/ORGAN.md`](/root/AAA/docs/ORGAN.md)
> **Machine twin:** [`/root/AAA/federation/organs.yaml`](/root/AAA/federation/organs.yaml)
> **Workspace topology:** [`/root/AAA/federation/workspace.yaml`](/root/AAA/federation/workspace.yaml)
> **Truth rule:** `live :port/health` beats every prose table. Re-probe before any SEAL-grade claim.

## Core organs

| Organ | Port | Class | Role | Authority ceiling |
|---|---|---|---|---|
| **arifOS** | 8088 | CORE · KERNEL | Constitutional kernel — 13 Floors · 888 JUDGE · VAULT999 | `JUDGE_ONLY` |
| **A-FORGE** | 7071/7072 | CORE · EXECUTE | Engineering actuator — plan, dry-run, apply, verify, rollback | `EXECUTE_AFTER_SEAL` |
| **GEOX** | 8081 | CORE · EARTH | Earth intelligence — basin, seismic, petrophysics, prospect | `COMPUTE_ONLY` |
| **WEALTH** | 18082 | CORE · CAPITAL | Capital intelligence — NPV / EMV / risk / market | `COMPUTE_ONLY` |
| **WELL** | 18083 | CORE · VITALITY | Human readiness — homeostasis / dignity / reliability | `REFLECT_ONLY` |
| **AAA** | 3001 | CORE · COCKPIT | Control plane + A2A gateway + registry home | `DISPLAY_ONLY` |
| **arifFLOW** | 7073 | METABOLISM | Receipt metabolism, FQ pulse, attention checkpointing | `METABOLIZE_ONLY` |

## Memory, advisors, edges

| Component | Class | Port | Role |
|---|---|---|---|
| **VAULT999** | MEMORY | filesystem | Immutable sealed receipts (append-only hash chain). Canonical: `/root/arifOS/VAULT999/outcomes.jsonl` |
| **FED** | ADVISORY | 7074 | Model route advisor — answers *where* to call |
| **FLAME** | ADVISORY | 18901 | RM0 free-loop inference mesh |
| **HERMES** | EDGE | 18087/18789 | Multimodal Telegram bridge |
| **OpenClaw / OpenCode** | EDGE | (Telegram) | Edge agent bridge |

## Substrate services (data plane — Docker / local only)

PostgreSQL `:5432` · Redis `:6379` · Qdrant `:6333` · FalkorDB `:6380` ·
Graphiti MCP `:8000` · MinIO `:9000-9001` · NATS `:4222` · SearXNG `:8080` ·
MCPJam `:6274/:6277` · Headscale `:8083` · Caddy `:80/:443` · Cloudflared.

## Public MCP doors

| Organ | Public | Local |
|---|---|---|
| arifOS | `https://arifos.arif-fazil.com/mcp` | `127.0.0.1:8088` |
| A-FORGE | `https://mcp.arif-fazil.com/mcp` | `127.0.0.1:7072` |
| GEOX | `https://geox.arif-fazil.com/mcp` | `127.0.0.1:8081` |
| WEALTH | `https://wealth.arif-fazil.com/mcp` | `127.0.0.1:18082` |
| WELL | `https://well.arif-fazil.com/mcp` | `127.0.0.1:18083` |
| AAA | `https://aaa.arif-fazil.com` | `127.0.0.1:3001` |

## Repository layout

```
/root/
├── AGENTS.md                         ← generated from AAA/instructions/ fragments
├── CLAUDE.md                         ← AAA-grade executor doctrine
├── arifOS/   A-FORGE/   AAA/   GEOX/   WEALTH/   WELL/   HERMES/
├── forge_work/        ← receipts / drafts / daily sweeps (hash-chained)
├── VAULT999 → /root/arifOS/VAULT999/outcomes.jsonl (append-only)
├── .secrets/          ← KUNCI-MAS vault
├── .local/share/arifos/  ← carry_forward.json, flow_state.json
└── arif-fazil.com/    ← public sites
```

**Source ↔ runtime invariant:** `/root/<organ>` source must equal `/opt/<organ>/app` runtime. Deploy = `rsync` → `systemctl restart <unit>`.

## Live health probe

```bash
for p in 8088 7071 7072 7073 3001 8081 18082 18083; do
  curl -sf http://127.0.0.1:$p/health >/dev/null 2>&1 && echo "✅ $p" || echo "❌ $p"
done
```
