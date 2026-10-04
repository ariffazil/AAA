# 2026-08-15 — Node Institution Map + Stale-Swap Session

Session that produced the PSI/multi-swapfile learnings now embedded in §1 and §5b of this skill.

## Context

Sovereign asked: "machine node institution — map all + how to push to next level (resource allocation & deployment, don't overengineer)."

## Full live map captured (77 systemd services + 7 docker containers, 8 cores / 31Gi RAM / 387G disk)

| Layer | Components |
|---|---|
| Brain | arifOS kernel :8088 (PID via `ss -tlnp`), arifosd, NATS heartbeat |
| Hands | A-FORGE :7071/7072, opencode ×3 (one hot 71% CPU — protected, live session) |
| Edge nerves | openclaw-gateway :18789 + headless Chrome :18800 + kimi agent (620MB+2 MCP launchers) |
| Hermes stack | gateway :8444, ASI-gateway (689MB), MCP, A2A listener, real-bridge, kabarkan-worker |
| Memory | Postgres, Redis, Qdrant, FalkorDB, MinIO, ollama (embedding only: bge-m3 1.2G, nomic 274M, qwen2.5:3b 1.9G UNUSED-for-role) |
| Domain organs | GEOX, WEALTH, WELL, arifFlow, frame/signal-organ, gold/gas/KLCI/USD-MYR APIs |
| Doors | Caddy 80/443, cloudflared, haproxy :4000 (FED), litellm :4011 (1.65GB) |
| Mirrors | netdata + grafana + prometheus (~630MB combined, overlapping function) |
| Mesh | Tailscale 100.64.0.2 + Headscale; WAWA node (srv1642546, azwaos) runs Hermes v0.20.1 carry fork |

Top RAM consumers: openclaw-gateway 4.5G (Node bloat, expected), litellm 1.7G, ollama 1.1G, hermes-asi-gateway 0.7G.

## The stale-swap finding (main lesson)

- `free -h`: Swap 8.0G/8.0G used, 27Mi free — looked critical.
- `/proc/pressure/memory`: `full avg10=0.00` → NOT thrashing. Stale parking: cold pages sat in swap for ~2 weeks (uptime 23d), never forced to reclaim because RAM was never exhausted.
- Load 2.0/8 cores. Zero OOM/earlyoom kills in 48h.
- Fix: `swapoff /swapfile2 && swapon /swapfile2` (the LOWER-priority file, -3). <30s. Swap → 4.0G free, held after settle. Mem used jumped 14→19G during reset (pages returning to page cache) — expected, drains on its own.
- `drop_caches` (3) ran first: 15Gi buff/cache → 2.1Gi, freed 16Gi available.

## The zram observation (candidate next step, NOT yet executed)

`lsmod | grep zram` → module loaded but no zram swap device active (`swapon --show` shows only the two swapfiles). CPU shows `842_decompress/lz4` deps loaded too. Proposal on the table: zstd zram swap at higher priority than disk swapfiles → swap at RAM speed, disk untouched. 30-min job, not yet done — do not describe as implemented.

## OpenClaw "what does it actually do" finding

- openclaw-gateway = Telegram-facing edge surface (@AGI_ASI_bot) + A2A bridge :18789, spawns headless Chrome (browser tool), talks to :8081 (litellm).
- openclaw-bot = SEPARATE python bot (@arifOS_bot, opencode zen agent wrapper) with MemoryMax=256M + CPUQuota=25% — a good systemd-cap example already in production.
- The gateway's 4.5G is Node/V8 heap bloat over 10h uptime; Chrome subtree adds ~1.2G (pids under gateway). Pattern matches "cap + scheduled restart" recommendation.

## Dead-weight finding: /root/comfy (6.4G)

Fresh ComfyUI clone + venv + torch 2.12 + SD1.5 checkpoint (4G) from 2026-08-10 14:10. **Never started** — port 8188 never listened, no service, no journal entries, `output/` empty, input only the repo's example.png. Host has no GPU → SD1.5 on CPU = 5–15 min/image, redundant vs working Gemini image lane. Recommended deletion (recoverable: re-clone + re-download). Sovereign decision pending at session end.

## Next-level list given to sovereign (ROI order, no k8s)

1. zram swap (module already loaded) — 30 min
2. Cap openclaw-gateway via systemd MemoryMax + off-peak weekly restart timer
3. Ollama diet: keep bge-m3 (embedding role), drop qwen2.5:3b 1.9G + nomic 274M → ~2G back
4. Disk lifecycle: /root 75% full; forge_work 21G, snapshots 6.8G, comfy 6.4G, _archive 1.9G — compress/archive >30-day snapshots
5. De-layer mirrors (netdata vs grafana+prometheus) — sovereign decision, ~600MB
6. Deployment pattern going forward: stateless edge agents on cheap nodes (WAWA model) via Headscale; state stays central — scale by adding nodes, not by growing this box
