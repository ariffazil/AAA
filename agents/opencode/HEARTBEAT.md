# HEARTBEAT.md — OpenCode 333-AGI | Daily Recurring Checklist

## Every Session Start
- [ ] `arif_session_init` — bind constitutional session
- [ ] `arif_organ_attest_all` — verify 7 organs alive
- [ ] Check WEALTH not crash-looping (`systemctl is-active wealth-organ`)
- [ ] Check WELL state not expired (>24h = stale, trigger refresh)
- [ ] Check A-FORGE MCP responding on /mcp
- [ ] Read memory/YYYY-MM-DD.md for carry-forward
- [ ] Verify ADAT AGENTIC enforcer active (`curl http://localhost:7071/execute` returns `adat_enforced: true`)

## Every Task
- [ ] Blast radius assessed (files touched, services affected)
- [ ] Reversibility confirmed (or 888_HOLD with hold_id)
- [ ] Evidence labeled OBS/DER/INT/SPEC
- [ ] A-FORGE `forge_plan` called before MUTATE actions
- [ ] A-FORGE `forge_dry_run` called before ATOMIC actions
- [ ] Task logged to forge_work/

## Every Session End — Self-Audit Loop
- [ ] **Federation Health** — all 7 organs attested, all 18 MCPs probed
- [ ] **Memory Updated** — `memory/YYYY-MM-DD.md` with carry-forward
- [ ] **Entropy Measured** — ΔS ≤ 0 (disorder decreased or stable)
- [ ] **Open Loops** — documented or resolved
- [ ] **Debt Check** — hostinger MCP, WELL state, arifOS runtime drift checked
- [ ] **VAULT999** — at least one seal written today
- [ ] **Model Cost** — token spend under daily budget ($2.00/session)
- [ ] **Diff Audit** — `git diff --stat` reviewed, no unintended changes
- [ ] **ADAT** — at least one ATOMIC action gated, at least one MUTATE action auto-sealed
- [ ] **Kubernetes: false** (no k8s — bare metal systemd)
- [ ] **Write HEARTBEAT receipt** to `forge_work/heartbeat-YYYY-MM-DD.json`

## Weekly — Constitutional Audit
- [ ] Systemd services health check (all 13+)
- [ ] Docker containers health check (9)
- [ ] Disk >20% free
- [ ] Swap <5GB
- [ ] Journalctl vacuum if >500MB
- [ ] Check for zombie processes
- [ ] Verify ADAT AGENTIC doctrine intact (`/root/arifOS/GENESIS/010_ADAT_AGENTIC.md` exists)
- [ ] Cross-harness verification: request Claude Code audit of last week's diffs
- [ ] Review auto-seal log for pattern anomalies
- [ ] Update AAA agent files if drift detected

## Known Debt (Checklist)

| Debt Item | Check | Fix |
|-----------|-------|-----|
| hostinger-vps MCP timeout | `curl http://localhost:7071/execute -d '{"tool":"hostinger_..."}'` | Debug `gate.py` |
| WELL biometric EXPIRED | `curl http://localhost:18083/health` → `truth_status` | Run autosleeper/refresh |
| arifOS runtime drift | `curl http://localhost:8088/health` → `runtime_drift` | Rebuild container |
| clamav masked | `systemctl is-active clamav-daemon` | Keep masked unless needed |

---

*Forged: 2026-06-14 by FORGE (000Ω) — ADAT AGENTIC loop added*
