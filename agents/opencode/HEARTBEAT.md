# ⚒️ OPENCODE — Heartbeat

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Aligned:** 2026-07-23 — live agent model map, FLAME health path, seal chain path.
> **Cross-ref:** `BOOTSTRAP.md` (boot probes) · `TOOLS.md` (capabilities) · `AUTONOMOUS_GOVERNANCE.md` (seal path)

## Every Session Start

- [ ] `INIT.md` 7-question reflective check passed (Q1-Q7 all ✅)
- [ ] `BOOTSTRAP.md` ignition sequence completed (steps 1-6)
- [ ] Reality check: 6/6 organs alive (or degraded gracefully)
- [ ] FLAME :18901 live — `curl -sf http://localhost:18901/health`
- [ ] `AGENTS.md` federation contract loaded
- [ ] `TOOLS.md` capability surface confirmed
- [ ] `IDENTITY.md` voice calibrated
- [ ] `USER.md` — Arif's preferences noted
- [ ] `carry_forward.json` read — `/root/.local/share/arifos/carry_forward.json`
- [ ] Work queue loaded — `/root/work/tasks.json` + `progress.txt`

## Every Task

- [ ] Blast radius assessed before mutation
- [ ] Reversibility confirmed (or 888_HOLD raised per AUTONOMOUS_GOVERNANCE.md)
- [ ] Evidence labeled: OBS / DER / INT / SPEC
- [ ] `forge_shell_dryrun` or equivalent preview before ATOMIC execution
- [ ] Subagent spawned with clear task boundary
- [ ] Skill loaded if task matches skill description
- [ ] FLAME routed first for fact check / plan review when applicable

## Every Session End (MANDATORY — per AUTONOMOUS_GOVERNANCE.md §3A)

- [ ] RSI cycle: trace → diagnose → remediate → ledger → seal
- [ ] gate_fire.jsonl appended (if claims were gated)
- [ ] cooling_ledger_entries inserted into Supabase (if mutations)
- [ ] `forge_session_init(actor_id="arif")` → session_id + session_token + lease_id
- [ ] `forge_vault(mode="seal", session_token, lease_id, ...)` — AUTONOMOUS_SESSION_SEAL
- [ ] Federation health — all 6 organs attested
- [ ] Entropy measured — ΔS ≤ 0 (workspace cleaner than found)
- [ ] forge_work/ or memory/ — at least one entry written
- [ ] Diff audit — `git diff --stat` reviewed for unexpected changes
- [ ] Model cost — under daily budget ($2.00/session)

## Weekly Maintenance

- [ ] Run entropy sweep: `aforge_forge_entropy_sweep(path="/root")`
- [ ] Check for stale AGENTS.md across all repos
- [ ] Verify MCP server versions: `for svc in ... curl :port/health`
- [ ] Review forge_work/ for accumulated findings
- [ ] Check skill mesh: `bash /root/AAA/skills/scripts/skill-mesh-sync.sh --check`
- [ ] Update agent-card.json if capabilities changed

## Entropy Budget

| Signal | Threshold | Action |
|--------|-----------|--------|
| Files modified but not committed | > 5 | Commit or stash |
| forge_work/ entries unreviewed | > 10 | Review and archive |
| Dead processes | > 3 | Kill and log |
| Disk usage / | > 80% | Alert, clean logs |
| Memory usage | > 90% | Alert, kill zombies |
| MCP servers DOWN | > 1 | Degrade gracefully |
| Unsealed sessions | > 1 | Seal immediately |

## Model Cost Tracking (canonical: AGENT_MODEL_MAP.json)

| Agent | Primary Model | Tier |
|-------|--------------|------|
| **OpenCode** | `deepseek/deepseek-v4-pro` | Heavy |
| **FORGE (000Ω)** | `deepseek/deepseek-v4-pro` | Heavy |
| **AUDITOR (Ψ)** | `deepseek/deepseek-v4-pro` | Heavy |
| **OPS (🌐)** | `deepseek/deepseek-v4-flash` | Cheap |
| **PLAN (Ω)** | `kimi/kimi-k2.7-code` | Heavy |
| **Hermes** | `mimo/mimo-v2.5-pro-ultraspeed` | Heavy |
| **OpenClaw** | `minimax/MiniMax-M3` | Cheap |

**FLAME (free):** Hermes fact_check, epistemic_check, plan_review — use first.
**Daily budget:** $2.00/session.
**Constitutional:** Only `deepseek/deepseek-v4-pro` may serve 666_JUDGE and 999_SEAL.

---

*Forged: 2026-06-25 · Aligned: 2026-07-23 by FORGE (000Ω)*
*Agentic kernel layer: HEALTH (layer 5/7). Next: WORKFLOW.md (layer 4 — execution loop).*
*DITEMPA BUKAN DIBERI*
