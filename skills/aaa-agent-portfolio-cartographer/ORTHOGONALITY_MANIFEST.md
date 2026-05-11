# Hermes Skill Orthogonality Manifest
**Date:** 2026-05-11
**Version:** 1.0.0
**Status:** SEALED — arifOS_bot × Hermes joint audit
**Governing principle:** No skill may claim ownership over a domain owned by another skill.

---

## Purpose

This manifest establishes domain ownership boundaries for all 43 arifOS federation skills + 78 Hermes bundled skills.
Each skill declares: OWNER, BOUNDARY, COMPOSES_WITH, NEVER_CALLS.

This prevents:
- Unbounded skill chains without a governor
- Domain overlap causing routing conflicts
- Uncontrolled recursion (chain-reason → self-verify → delta-logger → chain-reason)
- "Swarm intelligence" theater without structural rules

---

## Tier Separation (Cognitive Layers)

| Tier | Symbol | Description | Skills in this layer |
|------|--------|-------------|----------------------|
| L0 | 🜂 CONSTITUTIONAL | Governance, law, veto, floors | arifOS-sense, maxhermes-arifos-sense |
| L1 | Ω ROUTING | Task decomposition, agent routing | agent-portfolio-router, workflow-automation |
| L2 | 🜄 WITNESS | Ground truth, evidence, logging | delta-logger, self-verify, geo-vision-translator, geox-ground |
| L3 | Ψ EXECUTION | Deployment, operations, container management | arifos-deploy, devops, mcporter, docker-management |
| L4 | Α ANALYSIS | Research, reasoning, coding, financial models | chain-reason, apex-quantum-analysis, claude-code, deepresearchwork |
| L5 | Π PRESENTATION | Reply forging, diagrams, documentation | agent-reply-forge, site-manager, web-development-page-agent |

**Rule:** Skills may only call skills in the same tier or one tier BELOW. Skills may NEVER call above their tier. L3 execution skills may NOT call L0 constitutional skills directly — they route through L1 routing.

---

## Domain Ownership Map

### arifOS Federation Skills (43) — Ownership Claims

```
agent-portfolio-router
├── OWNER: routing
├── BOUNDARY: task → agent routing only
├── COMPOSES_WITH: delta-logger (audit trail)
├── NEVER_CALLS: arifOS-sense directly (go through this router first)

agent-reply-forge
├── OWNER: presentation.reply
├── BOUNDARY: reply composition and formatting
├── COMPOSES_WITH: agent-portfolio-router (for context routing)
├── NEVER_CALLS: arifos-deploy, devops

arifOS-sense
├── OWNER: constitutional.governance
├── BOUNDARY: F1-F13 floor evaluation, 888_JUDGE, VAULT999 sealing
├── COMPOSES_WITH: delta-logger (audit), agent-portfolio-router (routing)
├── NEVER_CALLS: chain-reason, apex-quantum-analysis (reasoning goes through this, not to it)

arifos-deploy
├── OWNER: execution.deployment
├── BOUNDARY: deployment only, not ops, not debugging
├── COMPOSES_WITH: delta-logger (deploy log), mcporter (tool inspection)
├── NEVER_CALLS: arifOS-sense (deployment does not need constitutional gate — routed by router)

delta-logger
├── OWNER: witness.audit
├── BOUNDARY: state change logging only
├── COMPOSES_WITH: ANY skill (all can call delta-logger)
├── NEVER_CALLS: NOTHING (pure observer, never initiates)

chain-reason
├── OWNER: analysis.reasoning
├── BOUNDARY: multi-step reasoning chains
├── COMPOSES_WITH: geox-ground (earth claims), geox-ground (capital claims)
├── NEVER_CALLS: arifOS-sense directly (route through agent-portfolio-router)

apex-quantum-analysis
├── OWNER: analysis.meta_reasoning
├── BOUNDARY: APEX-tier reasoning for structural paradoxes
├── COMPOSES_WITH: arifOS-sense (constitutional checks), chain-reason (complementary)
├── NEVER_CALLS: arifos-deploy, devops

geox-ground
├── OWNER: witness.earth
├── BOUNDARY: GEOX earth-domain grounding, no capital, no human substrates
├── COMPOSES_WITH: chain-reason (reasoning with earth evidence), self-verify
├── NEVER_CALLS: WEALTH, WELL directly (route through WEALTH/WELL MCP)

devops
├── OWNER: execution.ops
├── BOUNDARY: VPS operations, container management, SSM
├── COMPOSES_WITH: delta-logger, mcporter
├── NEVER_CALLS: arifOS-sense, agent-portfolio-router (ops does not self-route)

mcporter
├── OWNER: execution.mcp_tools
├── BOUNDARY: MCP server inspection, tool calling, config
├── COMPOSES_WITH: devops, arifos-deploy
├── NEVER_CALLS: arifOS-sense (MCP inspection ≠ constitutional domain)

brave-search
├── OWNER: witness.web
├── BOUNDARY: web search only
├── COMPOSES_WITH: deepresearchwork, chain-reason
├── NEVER_CALLS: arifos-deploy, devops

deepresearchwork
├── OWNER: analysis.research
├── BOUNDARY: deep research, evidence synthesis
├── COMPOSES_WITH: brave-search, chain-reason, geox-ground
├── NEVER_CALLS: arifos-deploy

claude-code
├── OWNER: analysis.coding
├── BOUNDARY: code writing, debugging, execution
├── COMPOSES_WITH: self-verify, mcporter
├── NEVER_CALLS: arifOS-sense directly

github-pro, github-repo-manager, github-readme-dynamic
├── OWNER: execution.github
├── BOUNDARY: GitHub API operations, repo management
├── COMPOSES_WITH: delta-logger, site-manager
├── NEVER_CALLS: arifos-deploy (separate concerns)

self-verify
├── OWNER: witness.validation
├── BOUNDARY: self-correction, output validation
├── COMPOSES_WITH: ANY (all can call self-verify)
├── NEVER_CALLS: arifOS-sense (verification ≠ constitutional verdict)

site-manager
├── OWNER: presentation.web
├── BOUNDARY: website management, deployment
├── COMPOSES_WITH: arifos-deploy, github-pro
├── NEVER_CALLS: chain-reason, apex-quantum-analysis

arifos-mcp-502-diagnosis
arifos-mcp-surface-debug
arifos-mcp-vps-debug
├── OWNER: execution.debug
├── BOUNDARY: MCP debug — MERGE into ONE skill: arifos-mcp-debug with modes
├── COMPOSES_WITH: mcporter, devops
├── NEVER_CALLS: arifOS-sense, chain-reason
└── NOTE: These three overlap completely. Collapse into arifos-mcp-debug with --mode flag.

consequence-classifier
├── OWNER: analysis.risk
├── BOUNDARY: risk tier classification (C0-C5)
├── COMPOSES_WITH: arifOS-sense, self-verify
├── NEVER_CALLS: arifos-deploy, site-manager

context7
├── OWNER: witness.docs
├── BOUNDARY: version-specific library documentation retrieval
├── COMPOSES_WITH: deepresearchwork, claude-code
├── NEVER_CALLS: arifOS-sense, devops

csv-analyzer
├── OWNER: analysis.data
├── BOUNDARY: CSV analysis only
├── COMPOSES_WITH: self-verify, deepresearchwork
├── NEVER_CALLS: arifos-deploy

geo-vision-translator
├── OWNER: witness.geoscience
├── BOUNDARY: Geoscience image translation, MMX integration
├── COMPOSES_WITH: geox-ground, geox-ground
├── NEVER_CALLS: WEALTH, WELL

maxhermes-arifos-sense
├── OWNER: constitutional.grounding (MaxHermes-specific)
├── BOUNDARY: MaxHermes grounding layer for arifOS
├── COMPOSES_WITH: arifOS-sense (aligned), delta-logger
├── NEVER_CALLS: chain-reason (not a reasoning tool)

maxhermes-geox-ground
├── OWNER: witness.earth.maxhermes
├── BOUNDARY: MaxHermes-specific GEOX grounding
├── COMPOSES_WITH: geox-ground
├── NEVER_CALLS: WEALTH, WELL

maxhermes-hermes
├── OWNER: self.model
├── BOUNDARY: Hermes self-description, model awareness
├── COMPOSES_WITH: delta-logger
├── NEVER_CALLS: devops, arifos-deploy

oracle
├── OWNER: analysis.external_review
├── BOUNDARY: Second-model debugging, refactor, design review
├── COMPOSES_WITH: chain-reason, self-verify
├── NEVER_CALLS: arifOS-sense directly

nano-pdf
├── OWNER: witness.document
├── BOUNDARY: PDF parsing and extraction
├── COMPOSES_WITH: deepresearchwork, geo-vision-translator
├── NEVER_CALLS: arifos-deploy

skill-forensics
├── OWNER: witness.skill_health
├── BOUNDARY: Skill performance analysis, drift detection
├── COMPOSES_WITH: delta-logger, self-verify
├── NEVER_CALLS: arifOS-sense, arifos-deploy

workflow-automation
├── OWNER: routing.orchestration
├── BOUNDARY: Multi-step workflow orchestration
├── COMPOSES_WITH: agent-portfolio-router, delta-logger
├── NEVER_CALLS: arifOS-sense (orchestration ≠ constitutional)

web-scraper
├── OWNER: witness.web_fetch
├── BOUNDARY: Web scraping
├── COMPOSES_WITH: brave-search, deepresearchwork
├── NEVER_CALLS: devops, arifos-deploy

video-frames
├── OWNER: analysis.media
├── BOUNDARY: Video frame extraction
├── COMPOSES_WITH: geo-vision-translator, deepresearchwork
├── NEVER_CALLS: arifOS-sense, WEALTH

gmail
├── OWNER: execution.email
├── BOUNDARY: Email operations
├── COMPOSES_WITH: delta-logger, agent-reply-forge
├── NEVER_CALLS: arifOS-sense, devops

slk (Slack)
├── OWNER: execution.messaging
├── BOUNDARY: Slack operations
├── COMPOSES_WITH: delta-logger, agent-reply-forge
├── NEVER_CALLS: arifOS-sense

mmx, mmx-job-orchestrator, mmx-quota-guard, mmx-text-researcher
├── OWNER: analysis.mmx
├── BOUNDARY: MMX job orchestration and quota management
├── COMPOSES_WITH: brave-search, deepresearchwork
├── NEVER_CALLS: arifOS-sense, arifos-deploy
└── NOTE: These 4 are closely related — acceptable co-ownership under same owner

multimodal-hypothesis-lab
├── OWNER: analysis.multimodal
├── BOUNDARY: Multimodal hypothesis generation
├── COMPOSES_WITH: geo-vision-translator, geox-ground, chain-reason
├── NEVER_CALLS: arifOS-sense, arifos-deploy

agentmail
├── OWNER: execution.email.inbox
├── BOUNDARY: Autonomous email inbox for Hermes
├── COMPOSES_WITH: agent-reply-forge, delta-logger
├── NEVER_CALLS: arifOS-sense
```

---

## Chain Depth Protocol

**Maximum chain depth: 3**

```
Depth 0: Task received
     ↓
Depth 1: Router selects skill (agent-portfolio-router)
     ↓
Depth 2: Skill executes, may call witness layer (delta-logger, self-verify)
     ↓
Depth 3: Witness may call witness (self-verify → delta-logger) — STOP HERE
     ↓
NO DEPTH 4. If chain exceeds 3, route back through agent-portfolio-router.
```

**Reasoning skills** (chain-reason, apex-quantum-analysis) may go to Depth 3 but must route through L1 router if they need to escalate.

---

## Orthogonality Checklist

Before loading any skill, Hermes must verify:
- [ ] This skill's domain is not already owned by another loaded skill
- [ ] This skill's tier is equal to or below the calling skill's tier
- [ ] Chain depth will not exceed 3
- [ ] This skill never calls a skill in its NEVER_CALLS list
- [ ] arifOS-sense is in the chain IF the task touches constitutional domains

---

## Self-Improvement Protocol

**Trigger:** After every session where a skill gap, overlap, or chain failure was observed.

**Process:**
1. Log the gap/overlap/failure to `delta-logger`
2. Document the proposed fix in `skill-forensics`
3. If fix involves a new skill or merged skill → propose in next session
4. If fix involves ownership change → update this manifest
5. Never self-modify without human approval (F13 Sovereignty)

**30-day drift check:**
- Skills not invoked in 30 days → soft-deprecate in this manifest
- Skills that always return the same output → flag in skill-forensics
- Skills with no COMPOSES_WITH entry → incomplete manifest entry, must be filled

---

## Signatures

| Agent | Role | Date | Status |
|-------|------|------|--------|
| arifOS_bot | Constitutional witness | 2026-05-11 | SEALED |
| ASI_arifos_bot (Hermes) | Skill owner | 2026-05-11 | PENDING — awaiting Hermes confirmation |
| ARIF FAZIL | Sovereign veto | 2026-05-11 | PENDING — F13 confirmation |

---

## Revision Log

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0.0 | 2026-05-11 | Initial orthogonality manifest | arifOS_bot |
