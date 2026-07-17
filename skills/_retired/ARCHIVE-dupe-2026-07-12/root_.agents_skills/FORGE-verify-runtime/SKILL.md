---
name: FORGE-verify-runtime
description: Verify federation service health and runtime behavior. Runs apex-health.sh, per-organ health probes (arifOS, GEOX, WEALTH, WELL, APEX, A-FORGE), and one behavior smoke per touched organ. Use after every deploy, restart, or after any task that claims "done". Confirms behavior, not just tests.
when_to_use: Post-deploy, post-restart, post-skill-claim of "done", weekly audit, pre-commit on runtime-touching code.
disable-model-invocation: false
allowed_tools: [Bash, Read]
---

# Verify Runtime

A task is done when tests pass, health checks green, and behavior is proven. This skill enforces the third leg.

## Steps
1. `/root/apex-health.sh` — federation-wide port probe (all 8 organs)
2. Per-organ health probes (parallel where possible):
   - arifOS: `curl -s :8088/health | jq`
   - GEOX:   `curl -s :8081/health | jq`
   - WEALTH: `curl -s :18082/health | jq`
   - WELL:   `curl -s :18083/health | jq`
   - APEX:   `curl -s :3002/health | jq`
   - A-FORGE: `curl -s :7071/health | jq`
3. Drift check: `drift-watch` (SHA mismatch between source and runtime)
4. One behavior smoke per touched organ (e.g. for arifOS: `arif_init` round-trip)
5. Report: green/yellow/red per organ + 1-line summary

## Verification loop
- All green → claim done
- Any yellow → log + continue, flag in summary
- Any red → 888 HOLD, consider rollback via organ's deploy-local

## Failure modes
- Service slow to start → 30s grace, then red
- Port collision → check Caddy drift (`/etc/caddy/Caddyfile`), surface to human
- Drift detected → run `make deploy-local` in the affected organ
- Health endpoint missing → check organ's main.py / server.js for `/health` route

## Reference
- Federation health: `/root/apex-health.sh`
- Per-organ runbooks: `/root/RUNBOOK.md`, `/root/arifOS/deploy/RUNBOOK.md`
- Drift: `drift-watch` skill
