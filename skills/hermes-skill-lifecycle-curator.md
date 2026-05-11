---
name: hermes-skill-lifecycle-curator
version: 1.0.0
layer: L1
domain: AAA
verb_class: execute
trigger: "When adding, removing, or auditing Hermes skills — especially before installing from catalog or pruning installed skills."
platforms: [hermes-agent, VPS]
risk: medium
trust: vetted
---

# Hermes Skill Lifecycle Curator

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.

## When to Run This Skill

- Before installing any new optional skill from Hermes catalog
- Before removing or archiving any installed skill
- During quarterly skill estate audits
- When a skill behaves unexpectedly or conflicts with federation architecture

## Lifecycle States

Every skill in the Hermes estate moves through this state machine:

```
[Catalog] → [Pending Allowlist] → [Vetted] → [Installed] → [Active] ↔ [Archived]
                                        ↕           ↕
                                  [Rejected]   [Experimental]
```

## Tier Classification

| Tier | Label | Criteria | Auto-install? |
|------|-------|----------|--------------|
| T1 | **Vetted** | High value, bounded blast radius, no automation side effects | ✅ Yes — install immediately |
| T2 | **Experimental** | Useful but broad automation or external calls; needs boundary definition first | ⏸ Hold — policy required |
| T3 | **Situational** | Only needed when specific use case arises | 🔒 Locked — install on-demand |

## Staged Install Protocol

### Wave 1 — Vetted (Install Now)

```bash
hermes skills install official/software-development/node-inspect-debugger
hermes skills install official/data-science/jupyter-live-kernel
hermes skills install official/github/github-auth
```

### Wave 2 — Experimental (Install After Policy)

```bash
# Requires event-boundary policy defined first
hermes skills install official/devops/webhook-subscriptions

# Requires knowledge-ingestion policy
hermes skills install official/research/arxiv
hermes skills install official/research/llm-wiki
```

### Wave 3 — Situational (Install On Demand)

```bash
# Only when specific use case confirmed
hermes skills install official/software-development/systematic-debugging
hermes skills install official/productivity/google-workspace
hermes skills install official/note-taking/obsidian
hermes skills install official/mlops/huggingface-hub
```

## Skill Audit Command

Run this to get current estate health:

```bash
hermes skills list --json | python3 -c "
import sys, json
data = json.load(sys.stdin)
skills = data.get('skills', data) if isinstance(data, dict) else data
tier_map = {'local': 'T1-vetted', 'experimental': 'T2-exp', 'situational': 'T3-situational'}
for s in skills:
    name = s.get('name', s.get('id', '?'))
    source = s.get('source', 'unknown')
    print(f'{name} | source={source}')
"
```

## Pruning Protocol

Before removing a skill:

1. Check if any active cron job or skill chain references it
2. Run: `hermes skills list | grep <skill-name>`
3. Document removal in `~/.hermes/SKILL_CURATION_LOG.md`
4. Archive rather than delete — move to `~/.hermes/skills-archive/<skill-name>/`

## Trust Tier Assignment Rules

- **T1 Vetted**: Federation-native tools (node-inspect for OpenClaw Node.js debugging, jupyter-live-kernel for GEOX/WEALTH data analysis, github-auth for GitHub operations)
- **T2 Experimental**: Automation-capable (webhook-subscriptions), knowledge-ingesting (arxiv, llm-wiki)
- **T3 Situational**: Domain-specific or platform-specific (obsidian if Arif uses it, openhue if smart home exists)

## Anti-Drift Rules

- Never install a skill and forget it — add to curation log
- Review skill estate every 30 days
- If a skill causes unexpected behavior in routing, flag as T2 Experimental and hold
- Self-evolution proposals for new skills MUST go through 888_HOLD before install

## Curator Log Format

```markdown
# SKILL CURATION LOG

## 2026-05-11
- ADD: node-inspect-debugger → T1-vetted (Wave 1)
- ADD: jupyter-live-kernel → T1-vetted (Wave 1)
- ADD: github-auth → T1-vetted (Wave 1)
- HOLD: webhook-subscriptions → T2-experimental (needs event-boundary policy)
- HOLD: huggingface-hub → T3-situational (Ollama already covers model supply)
```