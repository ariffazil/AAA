# Federation Skill Audit Report

**Generated:** 2026-06-23T10:27:34.086546+00:00
**Scopes audited:** 7
**Skills scanned:** 244
**ERROR:** 100
**WARNING:** 322
**INFO:** 128

## Summary by scope

| Scope | Skills | ERROR | WARNING | INFO |
|---|---|---|---|---|
| aaa | 40 | 1 | 48 | 42 |
| arifos | 53 | 38 | 80 | 11 |
| hermes | 48 | 18 | 41 | 37 |
| kimi | 7 | 0 | 0 | 4 |
| opencode | 46 | 29 | 53 | 9 |
| project | 49 | 14 | 82 | 18 |
| well | 1 | 0 | 2 | 1 |

## Cross-scope findings

| Severity | Skill | Check | Message |
|---|---|---|---|
| WARNING | vault999-audit-sealer | duplicate_name | Skill name appears in multiple scopes: kimi, project |
| WARNING | federation-router | duplicate_name | Skill name appears in multiple scopes: kimi, project |
| WARNING | arifos-kernel-operator | duplicate_name | Skill name appears in multiple scopes: kimi, project |
| WARNING | auditor-validator-kutip-sampah | duplicate_name | Skill name appears in multiple scopes: kimi, project |
| WARNING | aaa-doctrine-loader | duplicate_name | Skill name appears in multiple scopes: kimi, project |
| WARNING | mcp-fastmcp-builder | duplicate_name | Skill name appears in multiple scopes: kimi, project |
| WARNING | aforge-execution-governor | duplicate_name | Skill name appears in multiple scopes: kimi, project |
| WARNING | github-issue-triage | duplicate_name | Skill name appears in multiple scopes: aaa, project |
| WARNING | arifos-plan-dag | duplicate_name | Skill name appears in multiple scopes: aaa, project |
| WARNING | repository-hygiene-audit | duplicate_name | Skill name appears in multiple scopes: aaa, project |
| WARNING | github-pr-governance-review | duplicate_name | Skill name appears in multiple scopes: aaa, project |
| WARNING | github-ci-diagnose | duplicate_name | Skill name appears in multiple scopes: aaa, project |
| WARNING | aaa-agentic-governance-(aaa-cockpit,-canonical) | duplicate_name | Skill name appears in multiple scopes: aaa, arifos, hermes, well |
| WARNING | vps-docker | duplicate_name | Skill name appears in multiple scopes: arifos, opencode |
| WARNING | hermes-opencode-intelligence-protocol | duplicate_name | Skill name appears in multiple scopes: arifos, hermes |
| WARNING | github | duplicate_name | Skill name appears in multiple scopes: arifos, hermes |
| INFO | GitHub Issue Triage / GitHub Issue Triage | description_similarity | Description similarity 1.00 — possible trigger collision |
| INFO | arifos-plan-dag / arifOS Plan DAG | description_similarity | Description similarity 1.00 — possible trigger collision |
| INFO | Repository Hygiene Audit / Repository Hygiene Audit | description_similarity | Description similarity 1.00 — possible trigger collision |
| INFO | GitHub PR Governance Review / GitHub PR Governance Review | description_similarity | Description similarity 1.00 — possible trigger collision |
| INFO | GitHub CI Diagnose / GitHub CI Diagnose | description_similarity | Description similarity 1.00 — possible trigger collision |
| INFO | AAA Agentic Governance (AAA-Cockpit, canonical) / AAA Agentic Governance (AAA-Cockpit, canonical) | description_similarity | Description similarity 1.00 — possible trigger collision |

## aaa findings

| Severity | Skill | Check | Message |
|---|---|---|---|
| WARNING | PR Review Governance | missing_use_when | No 'Use When' section found |
| INFO | PR Review Governance | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | arifOS Evals | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Docker Entropy Ops | missing_use_when | No 'Use When' section found |
| INFO | Docker Entropy Ops | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | GEOX Grounding | missing_use_when | No 'Use When' section found |
| INFO | GEOX Grounding | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | Recursive Skill Forge | description_length | Description is 610 chars (recommended ≤ 400) |
| WARNING | Recursive Skill Forge | vague_description | Description contains vague verbs (help/assist/improve) without strong object |
| WARNING | Recursive Skill Forge | missing_use_when | No 'Use When' section found |
| INFO | Recursive Skill Forge | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Skill Trigger Linter | vague_description | Description contains vague verbs (help/assist/improve) without strong object |
| INFO | Skill Trigger Linter | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Agentic Dream Engine — Federation Memory Consolidation | name_mismatch | Skill name 'Agentic Dream Engine — Federation Memory Consolidation' does not match directory 'agentic-dream-engine' |
| WARNING | Agentic Dream Engine — Federation Memory Consolidation | missing_use_when | No 'Use When' section found |
| INFO | Agentic Dream Engine — Federation Memory Consolidation | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | arifOS MCP Federation | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | spatial-grounding | missing_skill_md | SKILL.md not found |
| INFO | arifos-governance | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Nusantara Intelligence Substrate | missing_use_when | No 'Use When' section found |
| INFO | Nusantara Intelligence Substrate | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Vault999 Integrity — Operational Lens | name_mismatch | Skill name 'Vault999 Integrity — Operational Lens' does not match directory 'vault999-integrity' |
| WARNING | Vault999 Integrity — Operational Lens | missing_use_when | No 'Use When' section found |
| INFO | Vault999 Integrity — Operational Lens | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Code Wiki — Codebase Documentation Generator | name_mismatch | Skill name 'Code Wiki — Codebase Documentation Generator' does not match directory 'code-wiki' |
| WARNING | Code Wiki — Codebase Documentation Generator | missing_use_when | No 'Use When' section found |
| INFO | Code Wiki — Codebase Documentation Generator | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Kimi Code AAA Configuration | name_mismatch | Skill name 'Kimi Code AAA Configuration' does not match directory 'kimi-code-aaa' |
| WARNING | Kimi Code AAA Configuration | missing_use_when | No 'Use When' section found |
| INFO | Kimi Code AAA Configuration | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | AAA Agentic Governance (AAA-Cockpit, canonical) | name_mismatch | Skill name 'AAA Agentic Governance (AAA-Cockpit, canonical)' does not match directory 'aaa-agentic-governance' |
| INFO | AAA Agentic Governance (AAA-Cockpit, canonical) | description_length | Description is 600 chars (recommended ≤ 400) |
| WARNING | AAA Agentic Governance (AAA-Cockpit, canonical) | missing_use_when | No 'Use When' section found |
| INFO | AAA Agentic Governance (AAA-Cockpit, canonical) | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Incident Escalation Protocol | name_mismatch | Skill name 'Incident Escalation Protocol' does not match directory 'incident-escalation' |
| WARNING | Incident Escalation Protocol | missing_use_when | No 'Use When' section found |
| INFO | Incident Escalation Protocol | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | GitHub Issue Triage | missing_use_when | No 'Use When' section found |
| INFO | GitHub Issue Triage | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | arifOS Plan DAG | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Multi-Discipline Critique | missing_use_when | No 'Use When' section found |
| INFO | Multi-Discipline Critique | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Unified Skill Binding (Orthogonal + Cross-Organ) | name_mismatch | Skill name 'Unified Skill Binding (Orthogonal + Cross-Organ)' does not match directory 'unified-skill-binding' |
| WARNING | Unified Skill Binding (Orthogonal + Cross-Organ) | missing_use_when | No 'Use When' section found |
| INFO | Unified Skill Binding (Orthogonal + Cross-Organ) | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Drift Response | missing_use_when | No 'Use When' section found |
| INFO | Drift Response | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | arifOS Recursive Audit | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Repository Hygiene Audit | name_mismatch | Skill name 'Repository Hygiene Audit' does not match directory 'repo-hygiene-audit' |
| WARNING | Repository Hygiene Audit | missing_use_when | No 'Use When' section found |
| INFO | Repository Hygiene Audit | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Agent Onboarding | missing_use_when | No 'Use When' section found |
| INFO | Agent Onboarding | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | GitHub Runbook — Federation Git & CLI Operations | name_mismatch | Skill name 'GitHub Runbook — Federation Git & CLI Operations' does not match directory 'github-runbook' |
| WARNING | GitHub Runbook — Federation Git & CLI Operations | missing_use_when | No 'Use When' section found |
| INFO | GitHub Runbook — Federation Git & CLI Operations | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Incident Triage | missing_use_when | No 'Use When' section found |
| INFO | Incident Triage | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | arifOS ACT — Constitutional Reflex | name_mismatch | Skill name 'arifOS ACT — Constitutional Reflex' does not match directory 'arifos-act' |
| WARNING | arifOS ACT — Constitutional Reflex | missing_use_when | No 'Use When' section found |
| INFO | arifOS ACT — Constitutional Reflex | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | OpenClaw A2A Bridge | missing_use_when | No 'Use When' section found |
| INFO | OpenClaw A2A Bridge | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | GitHub PR Governance Review | name_mismatch | Skill name 'GitHub PR Governance Review' does not match directory 'github-pr-review' |
| WARNING | GitHub PR Governance Review | missing_use_when | No 'Use When' section found |
| INFO | GitHub PR Governance Review | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | VPS Docker Runbook | missing_use_when | No 'Use When' section found |
| INFO | VPS Docker Runbook | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | AAA Agent Operating Invariants | name_mismatch | Skill name 'AAA Agent Operating Invariants' does not match directory 'aaa-agent-invariants' |
| WARNING | AAA Agent Operating Invariants | missing_use_when | No 'Use When' section found |
| INFO | AAA Agent Operating Invariants | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Secret Safety Scan | missing_use_when | No 'Use When' section found |
| INFO | Secret Safety Scan | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Parallel Authority Detection | missing_use_when | No 'Use When' section found |
| INFO | Parallel Authority Detection | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | MCP Federation Operations | name_mismatch | Skill name 'MCP Federation Operations' does not match directory 'mcp-federation-ops' |
| WARNING | MCP Federation Operations | missing_use_when | No 'Use When' section found |
| INFO | MCP Federation Operations | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Federation Service Health Triage | name_mismatch | Skill name 'Federation Service Health Triage' does not match directory 'service-health-triage' |
| WARNING | Federation Service Health Triage | missing_use_when | No 'Use When' section found |
| INFO | Federation Service Health Triage | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Precommit Gate | missing_use_when | No 'Use When' section found |
| INFO | Precommit Gate | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | Federation Health Scan | missing_use_when | No 'Use When' section found |
| INFO | Federation Health Scan | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | GitHub CI Diagnose | description_length | Description is 419 chars (recommended ≤ 400) |
| WARNING | GitHub CI Diagnose | missing_use_when | No 'Use When' section found |
| INFO | GitHub CI Diagnose | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | arifOS Observability | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | README Truth Check | missing_use_when | No 'Use When' section found |
| INFO | README Truth Check | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |

## arifos findings

| Severity | Skill | Check | Message |
|---|---|---|---|
| ERROR | metabolic-trinity | frontmatter_missing | No YAML frontmatter found |
| ERROR | metabolic-trinity | missing_name | Frontmatter missing 'name' field |
| WARNING | metabolic-trinity | missing_description | Frontmatter missing 'description' field |
| WARNING | metabolic-trinity | missing_version | Frontmatter missing 'version' field |
| WARNING | metabolic-trinity | missing_use_when | No 'Use When' section found |
| INFO | metabolic-trinity | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | vps-docker | missing_version | Frontmatter missing 'version' field |
| WARNING | vps-docker | missing_use_when | No 'Use When' section found |
| ERROR | trinity-forger | frontmatter_missing | No YAML frontmatter found |
| ERROR | trinity-forger | missing_name | Frontmatter missing 'name' field |
| WARNING | trinity-forger | missing_description | Frontmatter missing 'description' field |
| WARNING | trinity-forger | missing_version | Frontmatter missing 'version' field |
| WARNING | trinity-forger | missing_use_when | No 'Use When' section found |
| INFO | trinity-forger | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | agi-autonomous-controller | missing_version | Frontmatter missing 'version' field |
| WARNING | agi-autonomous-controller | missing_use_when | No 'Use When' section found |
| ERROR | well | missing_skill_md | SKILL.md not found |
| WARNING | agent-foundation | missing_version | Frontmatter missing 'version' field |
| WARNING | agent-foundation | missing_use_when | No 'Use When' section found |
| INFO | agent-foundation | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | health-probe | missing_version | Frontmatter missing 'version' field |
| WARNING | health-probe | missing_use_when | No 'Use When' section found |
| ERROR | memory-search | missing_skill_md | SKILL.md not found |
| ERROR | wealth | missing_skill_md | SKILL.md not found |
| ERROR | RSI-recursive-improvement | frontmatter_missing | No YAML frontmatter found |
| ERROR | RSI-recursive-improvement | missing_name | Frontmatter missing 'name' field |
| WARNING | RSI-recursive-improvement | missing_description | Frontmatter missing 'description' field |
| WARNING | RSI-recursive-improvement | missing_version | Frontmatter missing 'version' field |
| WARNING | RSI-recursive-improvement | missing_use_when | No 'Use When' section found |
| ERROR | hermes-opencode-intelligence-protocol | missing_skill_md | SKILL.md not found |
| WARNING | arif-a2a-call | missing_use_when | No 'Use When' section found |
| INFO | openclaw-ops | description_length | Description is 592 chars (recommended ≤ 400) |
| WARNING | openclaw-ops | missing_version | Frontmatter missing 'version' field |
| WARNING | openclaw-ops | missing_use_when | No 'Use When' section found |
| ERROR | geox | missing_skill_md | SKILL.md not found |
| ERROR | memory-query | missing_skill_md | SKILL.md not found |
| WARNING | notion | missing_version | Frontmatter missing 'version' field |
| WARNING | notion | missing_use_when | No 'Use When' section found |
| WARNING | browser | missing_version | Frontmatter missing 'version' field |
| WARNING | browser | missing_use_when | No 'Use When' section found |
| WARNING | AAA Agentic Governance (AAA-Cockpit, canonical) | name_mismatch | Skill name 'AAA Agentic Governance (AAA-Cockpit, canonical)' does not match directory 'aaa-agentic-governance' |
| INFO | AAA Agentic Governance (AAA-Cockpit, canonical) | description_length | Description is 600 chars (recommended ≤ 400) |
| WARNING | AAA Agentic Governance (AAA-Cockpit, canonical) | missing_use_when | No 'Use When' section found |
| ERROR | entropy-optimization | frontmatter_missing | No YAML frontmatter found |
| ERROR | entropy-optimization | missing_name | Frontmatter missing 'name' field |
| WARNING | entropy-optimization | missing_description | Frontmatter missing 'description' field |
| WARNING | entropy-optimization | missing_version | Frontmatter missing 'version' field |
| WARNING | entropy-optimization | missing_use_when | No 'Use When' section found |
| WARNING | git-sync | missing_version | Frontmatter missing 'version' field |
| WARNING | git-sync | missing_use_when | No 'Use When' section found |
| WARNING | architect-explainer | missing_version | Frontmatter missing 'version' field |
| WARNING | architect-explainer | missing_use_when | No 'Use When' section found |
| WARNING | tasks | missing_version | Frontmatter missing 'version' field |
| WARNING | tasks | missing_use_when | No 'Use When' section found |
| ERROR | deep-research | missing_skill_md | SKILL.md not found |
| WARNING | os-health | missing_version | Frontmatter missing 'version' field |
| WARNING | os-health | missing_use_when | No 'Use When' section found |
| ERROR | code-refactor | missing_skill_md | SKILL.md not found |
| ERROR | forge-program | frontmatter_missing | No YAML frontmatter found |
| ERROR | forge-program | missing_name | Frontmatter missing 'name' field |
| WARNING | forge-program | missing_description | Frontmatter missing 'description' field |
| WARNING | forge-program | missing_version | Frontmatter missing 'version' field |
| WARNING | forge-program | missing_use_when | No 'Use When' section found |
| WARNING | skill-composer | missing_version | Frontmatter missing 'version' field |
| WARNING | skill-composer | missing_use_when | No 'Use When' section found |
| INFO | skill-composer | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | constitutional-governance | frontmatter_missing | No YAML frontmatter found |
| ERROR | constitutional-governance | missing_name | Frontmatter missing 'name' field |
| WARNING | constitutional-governance | missing_description | Frontmatter missing 'description' field |
| WARNING | constitutional-governance | missing_version | Frontmatter missing 'version' field |
| WARNING | constitutional-governance | missing_use_when | No 'Use When' section found |
| INFO | constitutional-governance | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | list-models | missing_skill_md | SKILL.md not found |
| WARNING | notebooklm-bridge | missing_version | Frontmatter missing 'version' field |
| WARNING | notebooklm-bridge | missing_use_when | No 'Use When' section found |
| ERROR | security-audit | missing_skill_md | SKILL.md not found |
| ERROR | git-ops | missing_skill_md | SKILL.md not found |
| ERROR | arifos-status | missing_skill_md | SKILL.md not found |
| ERROR | recovery | missing_skill_md | SKILL.md not found |
| ERROR | vps-monitor | missing_skill_md | SKILL.md not found |
| WARNING | github | missing_version | Frontmatter missing 'version' field |
| WARNING | github | missing_use_when | No 'Use When' section found |
| WARNING | arif-init-wrapper | missing_version | Frontmatter missing 'version' field |
| WARNING | arif-init-wrapper | missing_use_when | No 'Use When' section found |
| WARNING | memory-archivist | missing_version | Frontmatter missing 'version' field |
| WARNING | memory-archivist | missing_use_when | No 'Use When' section found |
| ERROR | deepnshadow | frontmatter_missing | No YAML frontmatter found |
| ERROR | deepnshadow | missing_name | Frontmatter missing 'name' field |
| WARNING | deepnshadow | missing_description | Frontmatter missing 'description' field |
| WARNING | deepnshadow | missing_version | Frontmatter missing 'version' field |
| WARNING | deepnshadow | missing_use_when | No 'Use When' section found |
| INFO | deepnshadow | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | arifos-deploy | missing_version | Frontmatter missing 'version' field |
| WARNING | arifos-deploy | missing_use_when | No 'Use When' section found |
| INFO | arifos-deploy | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | google-workspace | missing_version | Frontmatter missing 'version' field |
| WARNING | google-workspace | missing_use_when | No 'Use When' section found |
| WARNING | arifOS-Langfuse | name_mismatch | Skill name 'arifOS-Langfuse' does not match directory 'langfuse-arifos' |
| WARNING | arifOS-Langfuse | missing_version | Frontmatter missing 'version' field |
| WARNING | arifOS-Langfuse | missing_use_when | No 'Use When' section found |
| WARNING | agentic-governance | missing_version | Frontmatter missing 'version' field |
| WARNING | agentic-governance | missing_use_when | No 'Use When' section found |
| INFO | agentic-governance | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | constitutional-check | missing_skill_md | SKILL.md not found |
| ERROR | orthogonal-abstraction | frontmatter_missing | No YAML frontmatter found |
| ERROR | orthogonal-abstraction | missing_name | Frontmatter missing 'name' field |
| WARNING | orthogonal-abstraction | missing_description | Frontmatter missing 'description' field |
| WARNING | orthogonal-abstraction | missing_version | Frontmatter missing 'version' field |
| WARNING | orthogonal-abstraction | missing_use_when | No 'Use When' section found |
| ERROR | restart-gateway | missing_skill_md | SKILL.md not found |
| WARNING | arifos-mcp-call | missing_version | Frontmatter missing 'version' field |
| WARNING | arifos-mcp-call | missing_use_when | No 'Use When' section found |
| WARNING | postcheck-verifier | missing_version | Frontmatter missing 'version' field |
| WARNING | postcheck-verifier | missing_use_when | No 'Use When' section found |
| ERROR | site-health-monitor | missing_skill_md | SKILL.md not found |
| ERROR | apex-docs | frontmatter_missing | No YAML frontmatter found |
| ERROR | apex-docs | missing_name | Frontmatter missing 'name' field |
| WARNING | apex-docs | missing_description | Frontmatter missing 'description' field |
| WARNING | apex-docs | missing_version | Frontmatter missing 'version' field |
| WARNING | apex-docs | missing_use_when | No 'Use When' section found |
| INFO | apex-docs | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | github-repo-manager | missing_version | Frontmatter missing 'version' field |
| WARNING | github-repo-manager | missing_use_when | No 'Use When' section found |
| ERROR | deployment | missing_skill_md | SKILL.md not found |
| ERROR | epistemic-integrity | frontmatter_missing | No YAML frontmatter found |
| ERROR | epistemic-integrity | missing_name | Frontmatter missing 'name' field |
| WARNING | epistemic-integrity | missing_description | Frontmatter missing 'description' field |
| WARNING | epistemic-integrity | missing_version | Frontmatter missing 'version' field |
| WARNING | epistemic-integrity | missing_use_when | No 'Use When' section found |

## hermes findings

| Severity | Skill | Check | Message |
|---|---|---|---|
| INFO | software-development | description_length | Description is 742 chars (recommended ≤ 400) |
| WARNING | software-development | missing_use_when | No 'Use When' section found |
| WARNING | architect-prompt-hygiene | missing_version | Frontmatter missing 'version' field |
| WARNING | architect-prompt-hygiene | missing_use_when | No 'Use When' section found |
| INFO | architect-prompt-hygiene | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | social-media | missing_skill_md | SKILL.md not found |
| WARNING | arifos | missing_use_when | No 'Use When' section found |
| INFO | arifos | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | devops | description_length | Description is 560 chars (recommended ≤ 400) |
| WARNING | devops | missing_use_when | No 'Use When' section found |
| INFO | scar-forge | description_length | Description is 1021 chars (recommended ≤ 400) |
| WARNING | scar-forge | missing_use_when | No 'Use When' section found |
| INFO | scar-forge | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | dream-engine | missing_use_when | No 'Use When' section found |
| INFO | dream-engine | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | hermes-opencode-intelligence-protocol | frontmatter_missing | No YAML frontmatter found |
| ERROR | hermes-opencode-intelligence-protocol | missing_name | Frontmatter missing 'name' field |
| WARNING | hermes-opencode-intelligence-protocol | missing_description | Frontmatter missing 'description' field |
| WARNING | hermes-opencode-intelligence-protocol | missing_version | Frontmatter missing 'version' field |
| WARNING | hermes-opencode-intelligence-protocol | missing_use_when | No 'Use When' section found |
| INFO | hermes-opencode-intelligence-protocol | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | sovereign-ai | missing_skill_md | SKILL.md not found |
| WARNING | AAA Agentic Governance (AAA-Cockpit, canonical) | name_mismatch | Skill name 'AAA Agentic Governance (AAA-Cockpit, canonical)' does not match directory 'aaa-agentic-governance' |
| INFO | AAA Agentic Governance (AAA-Cockpit, canonical) | description_length | Description is 600 chars (recommended ≤ 400) |
| WARNING | AAA Agentic Governance (AAA-Cockpit, canonical) | missing_use_when | No 'Use When' section found |
| INFO | AAA Agentic Governance (AAA-Cockpit, canonical) | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | telegram-mode-guards | missing_version | Frontmatter missing 'version' field |
| WARNING | telegram-mode-guards | missing_use_when | No 'Use When' section found |
| INFO | telegram-mode-guards | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | media | missing_skill_md | SKILL.md not found |
| WARNING | _template | missing_use_when | No 'Use When' section found |
| WARNING | A3 Self-Test (Awareness-Authority-Auditability) | name_mismatch | Skill name 'A3 Self-Test (Awareness-Authority-Auditability)' does not match directory 'a3-selftest' |
| WARNING | A3 Self-Test (Awareness-Authority-Auditability) | missing_use_when | No 'Use When' section found |
| INFO | A3 Self-Test (Awareness-Authority-Auditability) | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | news-risalah-komuniti | description_length | Description is 441 chars (recommended ≤ 400) |
| WARNING | news-risalah-komuniti | missing_use_when | No 'Use When' section found |
| INFO | news-risalah-komuniti | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | productivity | description_length | Description is 552 chars (recommended ≤ 400) |
| WARNING | productivity | missing_use_when | No 'Use When' section found |
| ERROR | note-taking | missing_skill_md | SKILL.md not found |
| WARNING | multimodal | missing_use_when | No 'Use When' section found |
| ERROR | gaming | missing_skill_md | SKILL.md not found |
| INFO | fff-loop-protocol | description_length | Description is 688 chars (recommended ≤ 400) |
| WARNING | fff-loop-protocol | missing_use_when | No 'Use When' section found |
| INFO | fff-loop-protocol | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | diagramming | missing_skill_md | SKILL.md not found |
| ERROR | domain | missing_skill_md | SKILL.md not found |
| ERROR | health | missing_skill_md | SKILL.md not found |
| INFO | personal | description_length | Description is 650 chars (recommended ≤ 400) |
| WARNING | personal | missing_use_when | No 'Use When' section found |
| ERROR | security | missing_skill_md | SKILL.md not found |
| WARNING | prompt-format-detector | missing_version | Frontmatter missing 'version' field |
| WARNING | prompt-format-detector | missing_use_when | No 'Use When' section found |
| INFO | prompt-format-detector | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | email | missing_use_when | No 'Use When' section found |
| INFO | skill-rationalization | description_length | Description is 533 chars (recommended ≤ 400) |
| WARNING | skill-rationalization | missing_version | Frontmatter missing 'version' field |
| INFO | skill-rationalization | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | daily-pulse-architecture | description_length | Description is 928 chars (recommended ≤ 400) |
| WARNING | daily-pulse-architecture | missing_use_when | No 'Use When' section found |
| INFO | daily-pulse-architecture | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | github | missing_skill_md | SKILL.md not found |
| INFO | mlops | description_length | Description is 478 chars (recommended ≤ 400) |
| WARNING | mlops | missing_use_when | No 'Use When' section found |
| INFO | news-analysis | description_length | Description is 890 chars (recommended ≤ 400) |
| WARNING | news-analysis | missing_use_when | No 'Use When' section found |
| INFO | news-analysis | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | creative | description_length | Description is 531 chars (recommended ≤ 400) |
| WARNING | creative | missing_use_when | No 'Use When' section found |
| INFO | canonical-surface-enforcement | description_length | Description is 438 chars (recommended ≤ 400) |
| WARNING | canonical-surface-enforcement | missing_use_when | No 'Use When' section found |
| INFO | canonical-surface-enforcement | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | data-science | missing_skill_md | SKILL.md not found |
| ERROR | inference-sh | missing_skill_md | SKILL.md not found |
| INFO | research | description_length | Description is 500 chars (recommended ≤ 400) |
| WARNING | research | missing_use_when | No 'Use When' section found |
| ERROR | agentic | missing_skill_md | SKILL.md not found |
| WARNING | computer-use | missing_use_when | No 'Use When' section found |
| INFO | hermes-human-life | description_length | Description is 600 chars (recommended ≤ 400) |
| WARNING | hermes-human-life | missing_use_when | No 'Use When' section found |
| INFO | hermes-human-life | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | smart-home | missing_skill_md | SKILL.md not found |
| WARNING | substrate-gate-telegram | missing_description | Frontmatter missing 'description' field |
| WARNING | substrate-gate-telegram | missing_use_when | No 'Use When' section found |
| WARNING | orthodoxy-auditor | missing_use_when | No 'Use When' section found |
| INFO | orthodoxy-auditor | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | mcp | description_length | Description is 487 chars (recommended ≤ 400) |
| WARNING | mcp | missing_use_when | No 'Use When' section found |
| INFO | autonomous-ai-agents | description_length | Description is 582 chars (recommended ≤ 400) |
| WARNING | autonomous-ai-agents | missing_use_when | No 'Use When' section found |
| INFO | autonomous-ai-agents | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | gifs | missing_skill_md | SKILL.md not found |
| WARNING | paste-intent-classifier | missing_version | Frontmatter missing 'version' field |
| WARNING | paste-intent-classifier | missing_use_when | No 'Use When' section found |
| INFO | paste-intent-classifier | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | apple | missing_skill_md | SKILL.md not found |

## kimi findings

| Severity | Skill | Check | Message |
|---|---|---|---|
| INFO | vault999-audit-sealer | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | arifos-kernel-operator | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | auditor-validator-kutip-sampah | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | aforge-execution-governor | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |

## opencode findings

| Severity | Skill | Check | Message |
|---|---|---|---|
| INFO | skill-reflector | description_length | Description is 401 chars (recommended ≤ 400) |
| WARNING | skill-reflector | vague_description | Description contains vague verbs (help/assist/improve) without strong object |
| WARNING | skill-reflector | missing_use_when | No 'Use When' section found |
| ERROR | constitutional-advisor | frontmatter_parse | Frontmatter YAML parse error |
| ERROR | agent-zero | frontmatter_missing | No YAML frontmatter found |
| ERROR | agent-zero | missing_name | Frontmatter missing 'name' field |
| WARNING | agent-zero | missing_description | Frontmatter missing 'description' field |
| WARNING | agent-zero | missing_version | Frontmatter missing 'version' field |
| WARNING | agent-zero | missing_use_when | No 'Use When' section found |
| WARNING | vps-docker | missing_use_when | No 'Use When' section found |
| ERROR | claude-code-ops | frontmatter_parse | Frontmatter YAML parse error |
| WARNING | integrator-asi-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | integrator-asi-contrast | missing_use_when | No 'Use When' section found |
| WARNING | vps-management | missing_use_when | No 'Use When' section found |
| ERROR | constitutional-reasoning | frontmatter_parse | Frontmatter YAML parse error |
| ERROR | fff-sweep | frontmatter_parse | Frontmatter YAML parse error |
| WARNING | aaa-workspace | missing_use_when | No 'Use When' section found |
| WARNING | mcp-builder | missing_version | Frontmatter missing 'version' field |
| WARNING | mcp-builder | missing_use_when | No 'Use When' section found |
| INFO | mcp-builder | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | cross-domain-reasoning | frontmatter_missing | No YAML frontmatter found |
| ERROR | cross-domain-reasoning | missing_name | Frontmatter missing 'name' field |
| WARNING | cross-domain-reasoning | missing_description | Frontmatter missing 'description' field |
| WARNING | cross-domain-reasoning | missing_version | Frontmatter missing 'version' field |
| WARNING | cross-domain-reasoning | missing_use_when | No 'Use When' section found |
| INFO | cross-domain-reasoning | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | rsi-apex-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | rsi-apex-contrast | missing_use_when | No 'Use When' section found |
| WARNING | rsi-asi-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | rsi-asi-contrast | missing_use_when | No 'Use When' section found |
| WARNING | caddy-cloudflare | missing_use_when | No 'Use When' section found |
| ERROR | arifOS-federation | frontmatter_parse | Frontmatter YAML parse error |
| WARNING | final-agi-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | final-agi-contrast | missing_use_when | No 'Use When' section found |
| WARNING | vps-audit | missing_use_when | No 'Use When' section found |
| WARNING | integrator-agi-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | integrator-agi-contrast | missing_use_when | No 'Use When' section found |
| ERROR | 777-forge-apex-contrast | frontmatter_missing | No YAML frontmatter found |
| ERROR | 777-forge-apex-contrast | missing_name | Frontmatter missing 'name' field |
| WARNING | 777-forge-apex-contrast | missing_description | Frontmatter missing 'description' field |
| WARNING | 777-forge-apex-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | 777-forge-apex-contrast | missing_use_when | No 'Use When' section found |
| ERROR | secret-hygiene | frontmatter_parse | Frontmatter YAML parse error |
| WARNING | arifos-kernel | missing_version | Frontmatter missing 'version' field |
| WARNING | arifos-kernel | missing_use_when | No 'Use When' section found |
| INFO | arifos-kernel | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | architect-asi-contrast | frontmatter_parse | Frontmatter YAML parse error |
| WARNING | final-asi-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | final-asi-contrast | missing_use_when | No 'Use When' section found |
| INFO | final-asi-contrast | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | staff-engineer-review | missing_version | Frontmatter missing 'version' field |
| WARNING | staff-engineer-review | missing_use_when | No 'Use When' section found |
| ERROR | hermes-ops | frontmatter_parse | Frontmatter YAML parse error |
| ERROR | microsoft-eureka-integration | frontmatter_parse | Frontmatter YAML parse error |
| ERROR | 777-forge-agi-contrast | frontmatter_missing | No YAML frontmatter found |
| ERROR | 777-forge-agi-contrast | missing_name | Frontmatter missing 'name' field |
| WARNING | 777-forge-agi-contrast | missing_description | Frontmatter missing 'description' field |
| WARNING | 777-forge-agi-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | 777-forge-agi-contrast | missing_use_when | No 'Use When' section found |
| ERROR | secret-rotation-guide | frontmatter_parse | Frontmatter YAML parse error |
| WARNING | architect-apex-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | architect-apex-contrast | missing_use_when | No 'Use When' section found |
| ERROR | 777-forge-asi-contrast | frontmatter_missing | No YAML frontmatter found |
| ERROR | 777-forge-asi-contrast | missing_name | Frontmatter missing 'name' field |
| WARNING | 777-forge-asi-contrast | missing_description | Frontmatter missing 'description' field |
| WARNING | 777-forge-asi-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | 777-forge-asi-contrast | missing_use_when | No 'Use When' section found |
| WARNING | architect-agi-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | architect-agi-contrast | missing_use_when | No 'Use When' section found |
| INFO | architect-agi-contrast | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | docker-security | frontmatter_parse | Frontmatter YAML parse error |
| ERROR | arifos-operator | frontmatter_parse | Frontmatter YAML parse error |
| WARNING | integrator-apex-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | integrator-apex-contrast | missing_use_when | No 'Use When' section found |
| INFO | integrator-apex-contrast | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | vault999-ops | frontmatter_parse | Frontmatter YAML parse error |
| WARNING | fastmcp-deploy | missing_use_when | No 'Use When' section found |
| ERROR | docker-thermodynamics | frontmatter_parse | Frontmatter YAML parse error |
| WARNING | rsi-agi-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | rsi-agi-contrast | missing_use_when | No 'Use When' section found |
| WARNING | final-apex-contrast | missing_version | Frontmatter missing 'version' field |
| WARNING | final-apex-contrast | missing_use_when | No 'Use When' section found |
| INFO | final-apex-contrast | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | vault-integrity | frontmatter_parse | Frontmatter YAML parse error |
| ERROR | backup-dr | frontmatter_parse | Frontmatter YAML parse error |
| WARNING | well-governance-ops | missing_version | Frontmatter missing 'version' field |
| WARNING | well-governance-ops | missing_use_when | No 'Use When' section found |
| INFO | well-governance-ops | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| ERROR | witness-effect | frontmatter_parse | Frontmatter YAML parse error |
| ERROR | github-issues | frontmatter_parse | Frontmatter YAML parse error |
| ERROR | database-tuning | frontmatter_parse | Frontmatter YAML parse error |

## project findings

| Severity | Skill | Check | Message |
|---|---|---|---|
| WARNING | logfire-ui | name_mismatch | Skill name 'logfire-ui' does not match directory 'pydantic-logfire-ui' |
| INFO | logfire-ui | description_length | Description is 520 chars (recommended ≤ 400) |
| WARNING | logfire-ui | missing_version | Frontmatter missing 'version' field |
| WARNING | logfire-ui | missing_use_when | No 'Use When' section found |
| WARNING | agentic-toolcheck | missing_version | Frontmatter missing 'version' field |
| WARNING | agentic-toolcheck | missing_use_when | No 'Use When' section found |
| WARNING | geox-expiry-replan | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-expiry-replan | missing_use_when | No 'Use When' section found |
| INFO | agents-sdk | description_length | Description is 431 chars (recommended ≤ 400) |
| WARNING | agents-sdk | missing_use_when | No 'Use When' section found |
| WARNING | arifos-untrusted-sandbox | missing_use_when | No 'Use When' section found |
| INFO | arifos-untrusted-sandbox | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | geox-gui-alignment | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-gui-alignment | missing_use_when | No 'Use When' section found |
| WARNING | wrangler | missing_use_when | No 'Use When' section found |
| ERROR | vault999-audit-sealer | frontmatter_missing | No YAML frontmatter found |
| ERROR | vault999-audit-sealer | missing_name | Frontmatter missing 'name' field |
| WARNING | vault999-audit-sealer | missing_description | Frontmatter missing 'description' field |
| WARNING | vault999-audit-sealer | missing_version | Frontmatter missing 'version' field |
| INFO | vault999-audit-sealer | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | geox-sandbox-simulation | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-sandbox-simulation | missing_use_when | No 'Use When' section found |
| WARNING | cloudflare | missing_use_when | No 'Use When' section found |
| WARNING | frontend-design | missing_use_when | No 'Use When' section found |
| WARNING | GitHub Issue Triage | missing_use_when | No 'Use When' section found |
| INFO | GitHub Issue Triage | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | geox-contradiction-engine | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-contradiction-engine | missing_use_when | No 'Use When' section found |
| WARNING | geox-test-forge | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-test-forge | missing_use_when | No 'Use When' section found |
| WARNING | replicate-prompting | missing_version | Frontmatter missing 'version' field |
| WARNING | replicate-prompting | missing_use_when | No 'Use When' section found |
| WARNING | geox-render-contracts | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-render-contracts | missing_use_when | No 'Use When' section found |
| WARNING | geox-redteam-hantu | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-redteam-hantu | missing_use_when | No 'Use When' section found |
| WARNING | Repository Hygiene Audit | name_mismatch | Skill name 'Repository Hygiene Audit' does not match directory 'repo-hygiene-audit' |
| WARNING | Repository Hygiene Audit | missing_use_when | No 'Use When' section found |
| INFO | Repository Hygiene Audit | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | geox-merge-gatekeeper | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-merge-gatekeeper | missing_use_when | No 'Use When' section found |
| ERROR | federation-router | frontmatter_missing | No YAML frontmatter found |
| ERROR | federation-router | missing_name | Frontmatter missing 'name' field |
| WARNING | federation-router | missing_description | Frontmatter missing 'description' field |
| WARNING | federation-router | missing_version | Frontmatter missing 'version' field |
| ERROR | arifos-kernel-operator | frontmatter_missing | No YAML frontmatter found |
| ERROR | arifos-kernel-operator | missing_name | Frontmatter missing 'name' field |
| WARNING | arifos-kernel-operator | missing_description | Frontmatter missing 'description' field |
| WARNING | arifos-kernel-operator | missing_version | Frontmatter missing 'version' field |
| INFO | arifos-kernel-operator | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| INFO | pydantic-ai-harness | description_length | Description is 440 chars (recommended ≤ 400) |
| WARNING | pydantic-ai-harness | missing_version | Frontmatter missing 'version' field |
| WARNING | pydantic-ai-harness | missing_use_when | No 'Use When' section found |
| WARNING | sandbox-sdk | missing_use_when | No 'Use When' section found |
| ERROR | auditor-validator-kutip-sampah | frontmatter_missing | No YAML frontmatter found |
| ERROR | auditor-validator-kutip-sampah | missing_name | Frontmatter missing 'name' field |
| WARNING | auditor-validator-kutip-sampah | missing_description | Frontmatter missing 'description' field |
| WARNING | auditor-validator-kutip-sampah | missing_version | Frontmatter missing 'version' field |
| INFO | auditor-validator-kutip-sampah | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | geox-constitution | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-constitution | missing_use_when | No 'Use When' section found |
| INFO | geox-constitution | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | workers-best-practices | missing_use_when | No 'Use When' section found |
| WARNING | GitHub PR Governance Review | name_mismatch | Skill name 'GitHub PR Governance Review' does not match directory 'github-pr-review' |
| WARNING | GitHub PR Governance Review | missing_use_when | No 'Use When' section found |
| INFO | GitHub PR Governance Review | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | geox-epistemic-ladder | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-epistemic-ladder | missing_use_when | No 'Use When' section found |
| INFO | cloudflare-email-service | description_length | Description is 508 chars (recommended ≤ 400) |
| WARNING | cloudflare-email-service | missing_use_when | No 'Use When' section found |
| ERROR | aaa-doctrine-loader | frontmatter_missing | No YAML frontmatter found |
| ERROR | aaa-doctrine-loader | missing_name | Frontmatter missing 'name' field |
| WARNING | aaa-doctrine-loader | missing_description | Frontmatter missing 'description' field |
| WARNING | aaa-doctrine-loader | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-mcp-contracts | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-mcp-contracts | missing_use_when | No 'Use When' section found |
| INFO | web-perf | description_length | Description is 453 chars (recommended ≤ 400) |
| WARNING | web-perf | missing_use_when | No 'Use When' section found |
| WARNING | geox-petrophysics-bounds | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-petrophysics-bounds | missing_use_when | No 'Use When' section found |
| WARNING | logfire-query | name_mismatch | Skill name 'logfire-query' does not match directory 'pydantic-logfire-query' |
| INFO | logfire-query | description_length | Description is 604 chars (recommended ≤ 400) |
| WARNING | logfire-query | missing_version | Frontmatter missing 'version' field |
| WARNING | logfire-query | missing_use_when | No 'Use When' section found |
| ERROR | mcp-fastmcp-builder | frontmatter_missing | No YAML frontmatter found |
| ERROR | mcp-fastmcp-builder | missing_name | Frontmatter missing 'name' field |
| WARNING | mcp-fastmcp-builder | missing_description | Frontmatter missing 'description' field |
| WARNING | mcp-fastmcp-builder | missing_version | Frontmatter missing 'version' field |
| WARNING | godel-humility-lock | missing_version | Frontmatter missing 'version' field |
| WARNING | godel-humility-lock | missing_use_when | No 'Use When' section found |
| WARNING | replicate-models | missing_version | Frontmatter missing 'version' field |
| WARNING | replicate-models | missing_use_when | No 'Use When' section found |
| WARNING | geox-claim-grammar | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-claim-grammar | missing_use_when | No 'Use When' section found |
| WARNING | logfire-instrumentation | name_mismatch | Skill name 'logfire-instrumentation' does not match directory 'pydantic-logfire-instrumentation' |
| INFO | logfire-instrumentation | description_length | Description is 508 chars (recommended ≤ 400) |
| WARNING | logfire-instrumentation | missing_version | Frontmatter missing 'version' field |
| WARNING | logfire-instrumentation | missing_use_when | No 'Use When' section found |
| WARNING | building-pydantic-ai-agents | name_mismatch | Skill name 'building-pydantic-ai-agents' does not match directory 'pydantic-ai-agents' |
| WARNING | building-pydantic-ai-agents | missing_version | Frontmatter missing 'version' field |
| WARNING | building-pydantic-ai-agents | missing_use_when | No 'Use When' section found |
| INFO | GitHub CI Diagnose | description_length | Description is 419 chars (recommended ≤ 400) |
| WARNING | GitHub CI Diagnose | missing_use_when | No 'Use When' section found |
| INFO | GitHub CI Diagnose | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | geox-binary-transport | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-binary-transport | missing_use_when | No 'Use When' section found |
| ERROR | aforge-execution-governor | frontmatter_missing | No YAML frontmatter found |
| ERROR | aforge-execution-governor | missing_name | Frontmatter missing 'name' field |
| WARNING | aforge-execution-governor | missing_description | Frontmatter missing 'description' field |
| WARNING | aforge-execution-governor | missing_version | Frontmatter missing 'version' field |
| INFO | aforge-execution-governor | authority_claim | Skill references sovereign/judge/seal authority — ensure it does not override constitutional kernel |
| WARNING | geox-drift-detector | missing_version | Frontmatter missing 'version' field |
| WARNING | geox-drift-detector | missing_use_when | No 'Use When' section found |
| WARNING | durable-objects | missing_use_when | No 'Use When' section found |

## well findings

| Severity | Skill | Check | Message |
|---|---|---|---|
| WARNING | AAA Agentic Governance (AAA-Cockpit, canonical) | name_mismatch | Skill name 'AAA Agentic Governance (AAA-Cockpit, canonical)' does not match directory 'aaa-agentic-governance' |
| INFO | AAA Agentic Governance (AAA-Cockpit, canonical) | description_length | Description is 600 chars (recommended ≤ 400) |
| WARNING | AAA Agentic Governance (AAA-Cockpit, canonical) | missing_use_when | No 'Use When' section found |

## Rot classification

| Rot class | Count |
|---|---|
| doc-rot | 164 |
| trigger-rot | 25 |
| unused-rot | 0 |
| api-rot | 90 |
| fake-rot | 0 |
| creep-rot | 89 |
