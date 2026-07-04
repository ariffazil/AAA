---
title: "SKILL: GitHub Issues Monitor"
type: skill
version: 2.0.0
category: governance
risk_band: LOW
floors: []
evidence_required: false
sources: [/root/.opencode/skills/github-issues/SKILL.md]
confidence: high
---

# SKILL: GitHub Issues Monitor

> **Source:** `/root/.opencode/skills/github-issues/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Monitoring open GitHub issues across federation repos
- Triage, PR review, repo health assessment
- Issue prioritization
- Keywords: GitHub issues, open issues, PR review, repo health, issue triage

---

## Repos to Monitor

| # | Repo | Role |
|---|------|------|
| 1 | ariffazil/arifOS | Constitutional AI kernel |
| 2 | ariffazil/A-FORGE | Execution / Forge engine |
| 3 | ariffazil/GEOX | Earth intelligence |
| 4 | ariffazil/wealth | Capital intelligence |
| 5 | ariffazil/well | Vitality intelligence |
| 6 | ariffazil/AAA | Control plane |
| 7 | ariffazil/arif-sites | Static sites |
| 8 | (HERMES) | Local only, no public remote |

---

## Issue Check Commands

```bash
# Per repo
gh issue list -R ariffazil/arifOS --state open --limit 20
gh issue list -R ariffazil/A-FORGE --state open --limit 20
gh issue list -R ariffazil/GEOX --state open --limit 20

# PRs needing review
gh pr list -R ariffazil/arifOS --state open
gh pr list -R ariffazil/A-FORGE --state open
```

---

## Output Format

For each repo: `[REPO] [OPEN_ISSUES] [OPEN_PRS] [OLDEST_ISSUE_DATE]`

---

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- GitHub PAT with repo scope

---

## Related Pages

- [[federation-entities]] — all federation repos
- [[skill-arifos-federation]] — federation atlas
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Issues tracked. Federation monitored.*
