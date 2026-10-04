---
name: infrastructure-topology
version: 1.0.0
description: "Federation infrastructure wiring topology — how services connect across Docker, config, env, and systemd. Reference class for infrastructure verification."
tags: [infrastructure, topology, searxng, docker, config, wiring, verification]
floor_scope: [F1, F2, F4, F11]
autonomy_tier: T0
---

# Infrastructure Topology — Federation Wiring Reference

> How services are wired end-to-end. Use this to verify, troubleshoot, or explain infrastructure to humans.

## Purpose

When someone (another agent, a human report, a resolution log) claims "X is wired to Y" or "infrastructure resolved", this skill tells you **how to verify the full chain** — not just the endpoint, but every link between the claim and reality.

## The Verification Principle

Every infrastructure claim has **links**. A claim like "Hermes uses SearXNG for search" is actually a chain:

```
Docker process → Port binding → Config file → Per-profile config → A-FORGE code → Env vars → Systemd
```

**All 7 links must be verified independently.** A report that checks only the endpoint (curl :8080) is incomplete — the endpoint might work while the config is wrong, meaning a future restart will break it.

## Worked Example: SearXNG Sovereign Search

**Full topology:** `references/searxng-topology.md`

The chain for "all agents use SearXNG for web search":

| # | Link | How to verify |
|---|---|---|
| 1 | Docker service running | `ps aux \| grep searxng` |
| 2 | Port binding | `ss -tlnp \| grep :8080` |
| 3 | Functional endpoint | `curl "localhost:8080/search?q=test&format=json"` |
| 4 | Hermes global config | `grep -A3 "web:" /root/.hermes/config.yaml` |
| 5 | Per-profile configs | Check each `profiles/*/config.yaml` for `search_backend: searxng` |
| 6 | A-FORGE code defaults | `grep -n "searxng" /root/A-FORGE/src/interfaces/mcp/proxyTools.ts` |
| 7 | Env vars | `grep SEARXNG /root/.secrets/kunci-mas.env` |
| 8 | Systemd loads env | `systemctl show <service> \| grep SEARXNG` |

**Partial verification trap:** A report can truthfully say "config.yaml says searxng" (link 4) while link 1 (Docker process) is actually down. Always probe the FULL chain.

## When to Use This Skill

1. **Receiving a resolution report** — someone says "infrastructure fixed" → verify before endorsing
2. **Post-deploy verification** — you changed infrastructure → verify all links before claiming done
3. **Troubleshooting** — search/web/extraction fails → walk the chain to find which link broke
4. **Onboarding a new agent** — agent needs web search → verify it's wired to SearXNG, not external APIs

## Quick Verification Script

```bash
#!/bin/bash
# Verify SearXNG full chain (run from any AAA agent)
echo "=== SearXNG Topology Verification ==="

# 1. Process
echo -n "Process: "; ps aux | grep -c "[s]earxng" | xargs -I{} echo "{} processes"

# 2. Port
echo -n "Port 8080: "; ss -tlnp | grep ":8080" | wc -l | xargs -I{} echo "{} listeners"

# 3. Functional
echo -n "Functional: "; curl -s "localhost:8080/search?q=test&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d.get(\"results\",[]))} results')" 2>/dev/null || echo "FAIL"

# 4. Hermes config
echo -n "Global config: "; grep -c "searxng" /root/.hermes/config.yaml 2>/dev/null | xargs -I{} echo "{} matches"

# 5. Per-profile
echo -n "Profiles wired: "; grep -rl "searxng" /root/.hermes/profiles/*/config.yaml 2>/dev/null | wc -l | xargs -I{} echo "{} profiles"

# 6. A-FORGE
echo -n "A-FORGE default: "; grep -c "localhost:8080" /root/A-FORGE/src/interfaces/mcp/proxyTools.ts 2>/dev/null | xargs -I{} echo "{} references"

# 7. Env var
echo -n "SEARXNG_URL: "; grep -c "SEARXNG_URL" /root/.secrets/kunci-mas.env 2>/dev/null | xargs -I{} echo "{} entries"
```

## Pitfalls

- **Empty response ≠ service down** (Verified 2026-08-12): Transient timing issues after restarts can cause curl to return empty. Re-probe once before declaring down. Limit: 2 attempts.
- **Confirmation bias** (Verified 2026-08-12): Reports that list "what was fixed" often omit "what is still broken." Check ancillary services (Honcho, MCP servers) not just the primary target.
- **Config ≠ runtime** (always true): A config file saying `backend: searxng` does not mean the runtime is using it. Gateway plugins, environment overrides, and profile-specific configs can shadow the global setting.

## Adding New Infrastructure

When a new Docker service or infrastructure component is added to the federation:
1. Add its wiring chain to `references/` as a new `.md` file
2. Add a row to the verification script
3. Update the service map below

## Current Service Map (Verified 2026-08-12)

| Service | Port | Owner | Docker | Config |
|---|---|---|---|---|
| PostgreSQL | :5432 | continuity | ✅ | pinned 16-alpine |
| Redis | :6379 | continuity | ✅ | pinned 7-alpine |
| FalkorDB | :6380 | intelligence | ✅ | — |
| Qdrant | :6333 | intelligence | ✅ | — |
| SearXNG | :8080 | ALL (shared) | ✅ | `references/searxng-topology.md` |
| MinIO | :9000 | continuity | ✅ | — |
| arifOS | :8088 | governance | python | — |
| A-FORGE | :7071 | execution | node | — |
| arifFlow | :7073 | flow | python | — |
| WEALTH | :18082 | intelligence | python | — |
