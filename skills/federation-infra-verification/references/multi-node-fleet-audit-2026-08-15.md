# Multi-Node Fleet Resource Audit — 2026-08-15

Session: Arif asked "machine node institution — map all, resource allocation + deployment, don't overengineer."
Live-probed every node from the forge box. This reference captures the probe recipe, the verified node/port map, and the interpretation rules.

## The node inventory (as of 2026-08-15 14:53 MYT)

| Node | Tailscale | Hardware | Role | Load |
|---|---|---|---|---|
| **forge** (main VPS, af-forge) | 100.64.0.2 | 8 vCPU / 31GB / 387GB (75% used) | Everything: 25+ systemd organs + docker data-plane | ~2.0 |
| **azwaos / flow-edge** | 100.64.0.4 | ~8GB RAM (7.7Gi) | Hermes edge (WAWA, hermes-agent.service), arifosmcp, arifflow-internal + arifflow-pulse, caddy | 0.03 (idle) |
| **arifs-s24** (phone) | 100.64.0.1 | android | offline 15d — not a factor | — |

## Probe recipe (one pass per node)

```bash
# LOCAL node (forge): everything in one sweep
uptime; nproc; free -h; df -h / 
cat /proc/pressure/memory                      # PSI — the truth behind "swap full"
vmstat 1 2 | tail -1                           # si/so columns — actual paging activity
swapon --show
systemctl list-units --type=service --state=running --no-pager --no-legend   # filter organ names
ss -tlnp | awk '{print $4}' | sort -u          # who actually listens
docker ps --format '{{.Names}}\t{{.Status}}' ; docker stats --no-stream
# per-unit memory: systemctl show <unit> -p MemoryCurrent --value
# disk hogs: du -sh /root/* | sort -rh | head

# REMOTE node: resolve via tailscale status FIRST (node nicknames are NOT ssh hosts)
tailscale status | grep -v offline
ssh root@100.64.0.4 "uptime; free -h | head -3; systemctl list-units --type=service --state=running --no-pager --no-legend"
```

### Pitfall: node nickname ≠ SSH hostname
`ssh azwaos` → "Could not resolve hostname". The nickname in tailscale status resolves only via MagicDNS if enabled; the reliable form is `ssh root@<tailscale-ip>`. `tailscale status` output columns: `IP  nickname  tags  os  last-seen`.

## Interpretation rules (verified this session)

1. **Swap full ≠ crisis. Check PSI + vmstat.** forge showed 8/8GB swap used — sounds catastrophic. But `/proc/pressure/memory` = `some/full avg10=0.00 avg60=0.00` and vmstat si/so = 0 → cold dormant pages, zero memory pressure. Meaning: no headroom (worry if load grows), but nothing is thrashing NOW. Report as "full but cold", not "server dying". Conversely swap full + PSI some>10 = real thrash.
2. **Fleet imbalance is the resource story, not per-node tuning.** One node at load 2 with swap full + one node at load 0.03 with 6.2GB free = the allocation question answers itself. The fix class is relocation of decoupled services (data-plane: minio, searxng), not new hardware, not k8s.
3. **Fat-process identification.** `systemctl show -p MemoryCurrent` per unit found: openclaw-gateway 4.7GB/214 tasks (biggest single consumer), litellm-federation 1.7GB, arifos 0.5GB, hermes units ~30-320MB each. Two stray opencode CLI sessions (one at 70% CPU) were interactive leftovers, not services — kill or ignore, don't "fix".
4. **"Degraded" on :18089 was the real finding.** hermes-a2a-listener health = `{"status":"degraded","mcp_connected":false}` — the cross-node nerve half-dead while everything else looked green. In fleet audits, hunt for `degraded` in health JSONs, not just DEAD ports. This one is P1 carry-forward (OpenClaw→Hermes delegation reroute depends on it).

## Port map correction (supersedes the old 8080-8083 MCP table)

The legacy "MCP endpoints 8080-8083" mapping (still in the bundled FORGE-federation-orchestrator skill) is WRONG for current deployment. Live-verified 2026-08-15:

| Port | Service | Verified state |
|---|---|---|
| 8080 | **searxng** (docker, NOT MCP) | healthy |
| 8088 | arifOS kernel | degraded (deployment_attestation drift — known) |
| 7071 / 7072 | A-FORGE sense / MCP | healthy |
| 7073 | arifFlow (FQ pulse) | alive |
| 7074 | FED router | healthy |
| 3001 | AAA A2A gateway | healthy |
| 18081 | vault bridge | ok |
| 18082 | WEALTH | healthy |
| 18083 | WELL | degraded (known, MOCK/reflect-only) |
| 18084 / 18085 | SIGNAL / FRAME | ok |
| 18089 | hermes-a2a-listener | **degraded, mcp_connected:false** |
| 18900 / 18901 | aaa-signing / FLAME API | ok |
| 4000 | HAProxy → LiteLLM door | listening |
| 11434 | Ollama (localhost) | embeddings only |

Truth rule stands: re-probe before trusting this table; `ss -tlnp` is the authority on who listens.

## Zombie-artifact probe (the ComfyUI class)

Question from Arif: "Comfy tu buat apa? Working or not?" — 6.4GB sitting in /root. Five-signal dead-install check:

```bash
ps aux | grep -i comfy          # 1. process?
curl -m 3 http://127.0.0.1:8188/system_stats   # 2. port?
ls <dir>/venv                   # 3. venv/python env ever built?
ls -lt <dir>/output | head      # 4. any output EVER produced?
systemctl list-unit-files | grep -i comfy   # 5. unit?
```

ComfyUI verdict: cloned 2026-08-10, 4GB checkpoints downloaded, **no venv, no process, no port, no unit, output dir empty** — never ran once. Plus the capability check: the VPS has **no GPU**, so it never could. Dead weight on a 75%-full disk; models are re-downloadable so deletion is effectively reversible.

**Generalized:** before reporting a big directory as "infrastructure", run the 5 signals. Cloned-but-never-installed experiments (no venv + empty output + no unit) are cargo, not capability. Also check hardware prerequisite (GPU-bound tool on CPU-only box = dead on arrival regardless of install state). Counterpoint to remember: existing API image-gen lanes (Gemini, Bailian) already cover the need — the zombie duplicated a solved capability.

## Resource/deployment doctrine confirmed (Arif's constraint)

- "Don't overengineer" → two nodes + phone is enough for 2-3x growth. No k8s, no node 3, no new orchestration layer.
- Ranked relocation plan (cheapest+reversible first): 1) fix A2A nerve :18089, 2) rebuild arifOS from source (kill drift), 3) move data-plane (minio/searxng) to flow-edge (~0.5-1GB RAM freed), 4) swap reset on forge (restart cold-page daemons), 5) only then consider moving openclaw-gateway (4.7GB, Telegram-coupled, biggest blast radius).
- All moves RM0 — reallocation, not purchase. Arif reports cost in RM, never tokens.
