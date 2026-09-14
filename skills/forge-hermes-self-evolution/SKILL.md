---
name: FORGE-hermes-self-evolution
description: >
  Stage and operate Nous hermes-agent-self-evolution (DSPy + GEPA) against
  arifOS Hermes skills. Use when Arif says evolve a skill, GEPA, DSPy
  self-evolution, or hermes-agent-self-evolution. Never auto-writes live
  skills. Never pip-installs into the production Hermes venv. 888_HOLD
  before any evolve run (paid API ~$2-10).
version: 1.0.0
owner: AAA
floor_scope: [F1, F2, F12, F13]
autonomy_tier: T3
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Hermes self-evolution (DSPy + GEPA) — F13 gated

Upstream: https://github.com/NousResearch/hermes-agent-self-evolution
Staged clone (read-only until 888): `/root/forge_work/2026-08-25-hermes-self-evolution/upstream`
HEAD at stage: `0a929e3`

## Hard rules

1. **Do not** `pip install` into `/usr/local/lib/hermes-agent/venv`.
2. **Do not** write evolved `SKILL.md` into `/root/.hermes/skills` or `/root/AAA/skills`.
3. **Do not** run GEPA/MIPRO without an explicit 888 go for that skill name.
4. Isolated venv only, under the forge_work tree.
5. Output candidates go to `forge_work/2026-08-25-hermes-self-evolution/candidates/` for human review. Activation is a separate F13 act.

## When 888 has named a skill

```bash
cd /root/forge_work/2026-08-25-hermes-self-evolution
python3 -m venv .venv
.venv/bin/pip install -e './upstream[dev]'
export HERMES_AGENT_REPO=/usr/local/lib/hermes-agent
# then upstream evolve_skill --dry-run first; live compile only after 888
```

Cost: ~$2–10 per run via API. No GPU. Darwinian evolver is AGPL — do not vendor it into arifOS.

## Not this skill

- Generic optional `dspy` tutorial under `optional-skills/mlops/research/dspy` (Orchestra, not Nous GEPA).
- `hermes update` (drops fork carries).
- Mass skill commits from dirty `/root/HERMES`.
