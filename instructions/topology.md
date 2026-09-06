# Federation topology

> **Canonical map (human):** [`/root/AAA/docs/ORGAN.md`](/root/AAA/docs/ORGAN.md)
> **Machine twin:** [`/root/AAA/federation/organs.yaml`](/root/AAA/federation/organs.yaml)
> **Workspace topology:** [`/root/AAA/federation/workspace.yaml`](/root/AAA/federation/workspace.yaml)
> **Truth rule:** `live :port/health` beats every prose table. Re-probe before any SEAL-grade claim.

> **MACHINE AXIS (3-node mesh, since 2026-09-03):** [`/root/AAA/docs/MACHINE_MAP.md`](/root/AAA/docs/MACHINE_MAP.md) is SOT.
> **KVM8 af-forge** = Truth/seat — everything in this file is KVM8-local ·
> **KVM4 kvm4-forge** = Execution (FED litellm `100.64.0.5:4000`; Hermes gateway KVM4 = DORMANT backup — LIVE gateway re-homed to KVM8 `hermes-asi-gateway` + `~/.hermes` per MACHINE_MAP resolution 2026-09-04 13:58; FED :4000 below is KVM8 HAProxy → KVM4) ·
> **KVM2 azwaos** = Azwa's civilization + Witness-pending (its `arifosmcp` is a fork, NOT the judge).
> Ports change meaning per machine (7073 = arifFlow here, arifosmcp-fork on KVM2). Fingerprint before cross-machine calls:
> `echo "$(hostname) $(ip -4 addr show | grep -oE '100\.64\.0\.[0-9]+' | head -1)"` → .2=KVM8 · .5=KVM4 · .4=KVM2

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
| **FRAME** | 18085 | CORE · MEASUREMENT | Independent drift observer — baseline, trend, probe; evidence never verdict | `ADVISORY_ONLY` |

## Memory, advisors, edges

| Component | Class | Port | Role |
|---|---|---|---|
| **VAULT999** | MEMORY | filesystem | Immutable sealed receipts (append-only hash chain). Canonical: `/root/arifOS/VAULT999/outcomes.jsonl` |
| **FED** | ADVISORY | 7074 | Model route advisor — answers *where* to call |
| **FLAME** | DECOMMISSIONED 2026-09-04 | 18901 | RM0 free-loop inference mesh — replaced by FED flash lane (KVM4 :4000). Registry: flame-api.service, F13 ack 2026-09-06 |
| **HERMES** | EDGE | 18089/18789 | Multimodal Telegram bridge |
| **OpenClaw / OpenCode** | EDGE | (Telegram) | Edge agent bridge |

## Substrate services (data plane — Docker / local only)

PostgreSQL `:5432` · Redis `:6379` · Qdrant `:6333` ·
MinIO `:9000-9001` · NATS `:4222` · SearXNG `:8080` ·
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
for p in 8088 7071 7072 7073 3001 8081 18082 18083 18085; do
  curl -sf http://127.0.0.1:$p/health >/dev/null 2>&1 && echo "✅ $p" || echo "❌ $p"
done
```

## Dynamic awareness — when the system moves

The map is alive only if it propagates. Binding protocol for ANY topology change
(port, organ, systemd unit, path, machine):

1. **Update the map sources** — `federation/organs.yaml` (machine twin) + this fragment +
   `UNIVERSE.yaml` (additive recompile ledger entry — never edit sealed layers in place).
2. **Re-render the root terminal** — `/root/scripts/render-agents.sh` refreshes
   `/root/AGENTS.md` + `/root/CLAUDE.md`. Every harness (Kimi, Claude, Codex, Qwen,
   OpenCode, Grok, Hermes) reads these at boot — this IS the awareness channel.
3. **Commit AAA** — an uncommitted map is fiction for every machine that is not KVM8.
4. **Sentinel verifies** — `scripts/universe-drift-sentinel.sh` (hourly,
   `/etc/cron.d/aaa-universe-drift`) holds a line in `terminal/holds.txt` until the map
   is re-rendered and committed; resolution deletes it. It cannot render or commit —
   it only makes silent movement impossible.

A doctrine edit without a render = the system moved and the agents weren't told.
The sentinel exists so that cannot happen silently.
