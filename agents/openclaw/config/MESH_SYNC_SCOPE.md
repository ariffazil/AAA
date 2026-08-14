# OPENCLAW SKILL MESH-SYNC — Scope Map (prep for scripted execution)

> Scoped 2026-08-15 by 333-AGI. Execution via `skill-mesh-sync.sh` (bash session required).
> Rule: do NOT hand-copy skills — the canonical sync tool governs versioning. This map only pre-resolves targets.

## Deficit (VERIFIED 2026-08-15 06:44 via governed forge_shell, ledger seq 51-54)
- TRUE location: `/root/.openclaw/skills/` — **4 SKILL.md on disk**: openclaw-init, openclaw-forge, openclaw-propose-seal, trading-signal
- Card declares 22 → drift = 18 missing
- NOTE: `/root/.openclaw/agents/main/skills` does NOT exist (earlier "5" count included cross-path artifacts)

## Canonical sync tool (VERIFIED)
- `/root/AAA/scripts/skill-sync.sh` — modes: `audit | sync | agent:<name>`
- Mechanism: symlinks from `/root/AAA/skills` + `/root/.agents/skills` into per-agent skill dirs; skips missing canonical sources with WARN
- **GOVERNANCE: script execution requires GOVERN-mode session** (A-THINK guard correctly DENIED my light session; read-only probes passed and are hash-sealed in A-FORGE ledger seq 51-54)

## Execution (requires GOVERN session or Arif direct)
```bash
# 1. Snapshot
tar -czf /root/.openclaw/_snapshots/skills-pre-sync-$(date +%s).tgz /root/.openclaw/skills/
# 2. Audit (read-only) then sync
bash /root/AAA/scripts/skill-sync.sh audit
bash /root/AAA/scripts/skill-sync.sh sync
# 3. Verify + restart + smoke
find /root/.openclaw/skills -name SKILL.md | wc -l   # target: card-parity (22 or documented delta)
systemctl restart openclaw-gateway
```

## Card skill → canonical source candidates (/root/.agents/skills/)

| Card skill | Canonical candidate |
|---|---|
| Gateway Routing / Agent Dispatch / Agent Handoff | (gateway-native — likely no SKILL.md needed; verify card semantics) |
| Web Research | AGI-agentic-web |
| Browser Automation | AGI-agentic-web (browser section) / playwright |
| Shell Execution | (gateway tool — no skill) |
| Memory Search | AGI-dream-engine / memory-manage |
| Status Query | federation ops subset |
| OpenClaw Doctor Recipes | openclaw skill (/root/.agents/skills/openclaw) |
| MCP Boot Failure Diagnosis | FORGE-mcp-lifeguard |
| arif Federation Ops | FORGE-federation-orchestrator |
| Kanban Playbook | (check AAA catalog) |
| Reality Skills (F2 Grounding) | **MY-REALITY-STACK (new, forged today)** + observe-ground |
| Sovereign Recognition (F13) | reflective/sovereign-recognize |
| Session Inhabit (Lifecycle) | hermes-init (openclaw-init variant) |
| RSI Recursive Improvement | RSI-recursive-improvement |
| Trinity-33 Architecture | KERNEL-trinity-33 (trinity-33-canonical) |
| MCP Zen Architecture | FORGE-mcp-federation-ops / mcp-mastery |
| Forge Verbs (Execution) | substrate/route-dispatch + opencode-forge |
| MCP Builder | FORGE-fastmcp |
| Constitutional gates | kernel-bind / audit-seal (if card-listed) |

## Execution steps (next session, bash required)
1. Snapshot workspace skills dir
2. Run `skill-mesh-sync.sh --fix` (or per-skill copy via validator)
3. Verify: count SKILL.md == card declaration (minus gateway-native entries)
4. Restart openclaw-gateway; smoke-test one skill invocation

## FQ auto-gate wiring (same session)
- Target: hermes gateway hook or pre-reply plugin — probe `hooks.constitional-guard` pattern in /usr/local/lib/hermes-agent/gateway/
- Logic: live :7073 fetch pre-reply; FQ<0.5 → prepend HOLD notice (non-critical turns); cache-honesty per STATE_ENVELOPE spec
