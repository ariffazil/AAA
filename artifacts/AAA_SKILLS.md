# AAA Skills Audit — 2026-06-22

**Auditor:** Grok Build 4.3 (newly registered AAA citizen)  
**Scope:** /root/AAA/skills, registries/skills.yaml, contracts/skills/packages.yaml, usage in a2a-server + frontend, contrast vs federation .agents/skills  
**Context:** Follow-up to grok-build A2A registration + contrast research on AAA citizenship.

---

## Executive Summary

AAA has a **decent collection of skills** (31 SKILL.md files) and a formal packaging system, but they are under-integrated.

**Current state:** Skills exist mostly as documentation/playbooks. They are not strongly executed, discovered, governed, or composed inside AAA at runtime.

**Maturity:** Mixed. Some excellent (agent-onboarding, repo-hygiene-audit, mcp-smoke-test). Many have "pending" hashes and incomplete examples/tests.

**Biggest gap:** AAA is not yet the *active skill orchestrator and governance layer* for the federation. It is still mostly a registry + UI.

---

## Inventory

**Total SKILL.md in /root/AAA/skills:** 31

**Packaged / registered** (in registries/skills.yaml + contracts/skills/packages.yaml): ~12-15 with proper frontmatter and maturity levels.

### Categorized List

**Governance & Federation Core**
- aaa-agentic-governance
- aaa-agent-invariants
- arifos-governance
- arifos-mcp-federation
- arifos-plan-dag
- arifos-recursive-audit
- arifos-observability
- arifos-evals
- parallel-authority-detection
- drift-response

**Operational / Health**
- federation-health-scan
- service-health-triage
- mcp-smoke-test
- incident-escalation

**Code & Repo Governance**
- repo-hygiene-audit
- github-issue-triage
- github-pr-review
- github-ci-diagnose
- pr-review-governance
- readme-truth-check
- secret-safety-scan

**Agent Lifecycle**
- agent-onboarding
- agentic-dream-engine (experimental)

**Domain**
- geox-basin-interpreter
- geox-grounding
- spatial-grounding (claude / mcp / openai / openclaw variants)
- nusantara-intelligence-substrate

**Meta / Tooling**
- skill-creator
- skill-trigger-linter
- recursive-skill-forge

---

## Quality Assessment (Sample)

**Strong examples:**
- `agent-onboarding`: Excellent. Clear procedure, required files list, validation steps, forbidden actions, escalation paths. Directly relevant to what we just did registering grok-build.
- `repo-hygiene-audit`: Practical, has examples.
- `mcp-smoke-test`: Simple, focused, testable.
- `secret-safety-scan` + `incident-escalation`: Risk-tiered correctly (high/critical).

**Common weaknesses:**
- Many still have `artifact_hash: pending`
- Incomplete `examples` and `tests` sections
- Some are thin wrappers around global .agents/skills (duplication)
- Frontmatter varies in completeness

---

## How Skills Are (or Are Not) Used in AAA Today

### Runtime (a2a-server)
- "Skill" concept in server.js is **narrow**: mainly `agent-dispatch`, `agent-handoff`, `status-query`.
- These are treated more like A2A action types than rich SKILL.md playbooks.
- No automatic injection of AAA/skills/ into the gateway chat or deliberation.

### Web / Cockpit
- `MCPAppsPanel.tsx` is about **MCP Apps** (WellDesk, Earth Volume, Judge Console) — iframe-based geoscience + judge UIs. Not skills.
- `webmcp.ts` has `discover_a2a_skills` but it only pulls from the current agent's card (very limited).
- No rich skill browser, composer, or invocation UI in the cockpit.

### Packaging & Registry
- Good formal system exists (`registries/skills.yaml` + `contracts/skills/packages.yaml`).
- Defines `host_compatibility`, `maturity`, dependencies, install_hooks.
- TREE777 audit script is mentioned in README but appears lightly used.

### Contrast with Federation (.agents/skills)

| Aspect                  | AAA/skills (~31)                  | .agents/skills (~40+ top level)                  | Winner |
|-------------------------|-----------------------------------|--------------------------------------------------|--------|
| Quantity & depth        | Good coverage of governance/ops   | Extremely deep (full Cloudflare, complete GEOX epistemic suite, pydantic, durable-objects, sandbox, workers best-practices, etc.) | .agents |
| Quality & completeness  | Mixed (some excellent)            | High — many have references/, scripts/, detailed contracts | .agents |
| Duplication             | Several near-copies               | Canonical source for most arifos/geox skills     | — |
| Integration into AAA    | Documented                        | Used by agents but not centrally governed by AAA | AAA should win |
| Runtime execution       | Weak                              | Used via MCP + skills system in Grok / other harnesses | — |

**Observation:** AAA is maintaining its own copy of many federation skills instead of becoming the single source of truth and governance layer for them.

---

## Gaps — What Would Push AAA to the Next Level

### 1. Skill Execution Runtime (Biggest Gap)
AAA gateway and cockpit AI should be able to **load and invoke** skills with constitutional guards, not just list them.

Missing:
- Skill loader / injector in a2a-server
- 888/floor gate before high-risk skills
- Skill context injection into deliberation.ts

### 2. Central Skill Store + Composer
AAA should be the place where:
- Skills are discovered across organs
- Skills can be composed (e.g. repo-hygiene + github-pr-review + parallel-authority-detection)
- Versioned and attested

Currently arifos-plan-dag exists but lives mostly outside AAA control.

### 3. Cockpit UI for Skills
No equivalent of MCPAppsPanel for skills.
Humans (and agents) should be able to:
- Browse skills by risk_tier / domain
- See which agents are allowed to use them
- Trigger governed execution
- View audit trails

### 4. Lifecycle Integration
`agent-onboarding` skill is excellent on paper.
In practice we registered grok-build mostly manually via files.

The skill should be the canonical way new agents (including harnesses like grok-build) enter the system.

### 5. Attestation & Audit Automation
- Many `pending` hashes
- TREE777 audit not obviously wired into CI or daily health
- No automatic skill-trigger-linter runs on registration

### 6. Federation Skill Federation
AAA should pull/compose skills from GEOX, WEALTH, WELL, A-FORGE instead of reimplementing or duplicating.

---

## Why Bother With All This (Registration, Audits, etc.)

Because right now the federation has:
- Powerful evidence organs (GEOX / WEALTH / WELL)
- Powerful execution (A-FORGE)
- Powerful long-running agents (hermes-asi, openclaw)
- Powerful session harnesses (grok-build, opencode, claude-code, etc.)

But a **relatively weak central nervous system**.

AAA is supposed to be the cockpit + A2A mesh + 888 deliberation hub.

Registering agents and auditing skills exposes the current reality:
- Agents can be "added" but the system doesn't really *govern* them uniformly.
- Skills exist but aren't first-class governed primitives.
- The control plane is more observer than active orchestrator.

Doing the work (agent cards + skills audit) is how you turn AAA from "nice dashboard + registry" into the actual **governed execution substrate** for the entire federation.

Without this, you will keep adding powerful pieces that don't compose safely or visibly.

---

## Recommendations (Starting Points)

1. **Make skills first-class in the gateway**
   - Extend webmcp + a2a-server to load AAA/skills/ playbooks.
   - Add `invoke_skill` with floor/risk checks.

2. **Build a Skills tab/panel in Cockpit**
   - Similar to MCPAppsPanel but for skills (browse, filter by risk, see usage).

3. **Wire agent-onboarding skill**
   - Use it (or enhance it) as the actual path for future registrations like the one we just did.

4. **Centralize skill ownership**
   - Decide: Does AAA become the canonical home, or does it orchestrate references to .agents/skills + organ skills?

5. **Run the existing linters**
   - Execute `skill-trigger-linter` and TREE777-style audit on current set.
   - Fix pending hashes and incomplete tests.

6. **Skill attestation in agent lifecycle**
   - When an agent is LEASED, record which skills it is permitted to use.

---

**Next steps I can take immediately:**
- Run a full quality + trigger-linter pass on all 31 skills
- Propose a "aaa-skill-orchestrator" skill or enhancement to the gateway
- Audit how skills should be injected into deliberation.ts / chat
- Map which skills should be promoted to "core AAA platform skills"

Just say the word.

**DITEMPA BUKAN DIBERI** — but good skills make the forging repeatable and governed.
