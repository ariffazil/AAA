---
title: "WORKFLOW: TREE777 Agent Cron Loop (777/888/999)"
created: 2026-05-20
updated: 2026-05-20
version: 1.0.0
type: workflow
status: canonical
tags: [workflow, TREE777, cron, automation, 777, 888, 999, agents, phoenix72]
risk_band: MEDIUM
prerequisites: [skill-agent-onboarding, skill-trace-capture, skill-skill-promote]
sources: [wiki/concepts/MD.md, wiki/SCHEMA.md]
confidence: high
contested: false
---

# WORKFLOW: TREE777 Agent Cron Loop (777/888/999)

Canonical automation loop for each AAA agent, including **phoenix72**.

## Intent

Run the TREE777 growth loop on schedule so intelligence compounds without waiting for manual prompting:

1. Daily **777 health pulse** (counts, freshness, orphan links)
2. Twice-weekly **888 promotion review** (proposed-page queue)
3. Weekly **999 anchor** (growth receipt + ledger link)

## Runtime scripts

- `/root/AAA/scripts/tree777_health_pulse.sh`
- `/root/AAA/scripts/tree777_promotion_review.sh`
- `/root/AAA/scripts/tree777_weekly_anchor.sh`
- `/root/AAA/scripts/install_tree777_agent_crons.sh`

## Install / refresh cron block

```bash
/root/AAA/scripts/install_tree777_agent_crons.sh
```

The installer rewrites only the managed block:

- `# >>> TREE777_AGENT_LOOPS >>>`
- `# <<< TREE777_AGENT_LOOPS <<<`

## Output surfaces

- Runtime reports: `wiki/_runtime/reports/*.json`
- Per-agent cron logs: `wiki/_runtime/cron-<agent>.log`
- Anchor ledger: `VAULT999/tree777/tree777_anchors.jsonl`
- Human-readable audit trail: `wiki/LOG_MD.md`

## Governance notes

- Agent list is auto-discovered from `/root/AAA/agents/*`
- `phoenix72` is force-included even if not present as a directory
- Scheduling uses `CRON_TZ=Asia/Kuala_Lumpur`
- Jobs are staggered per-agent to reduce collision load
