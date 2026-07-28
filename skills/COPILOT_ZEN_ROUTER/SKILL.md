---
name: COPILOT_ZEN_ROUTER
description: >
  META-MESA: Orthogonal skill taxonomy + intent→skill router for Copilot CLI.
  THE single skill that tells Copilot which domain skill to load based on task context.
  Load this FIRST when uncertain which skill to use. Covers all 147 federation skills
  organized into 9 orthogonal layers. DO NOT load domain skills blindly — route through this.
trigger_phrases:
  - what skill
  - which skill
  - skill routing
  - zen router
  - meta mesa
  - skill taxonomy
  - find skill
  - load skill
  - route to skill
  - skill activation
harness: copilot-cli
domain: meta
risk_tier: LOW
autonomy: T1
forged: 2026-07-28
version: 1.0.0
---

# 🎯 COPILOT ZEN ROUTER — The Meta-Mesa

> **DITEMPA BUKAN DIBERI** — One skill to route them all. The mesa above the terrain sees every path.

## How Copilot Uses This

When you receive a task, check this taxonomy. Each layer lists exact skill names — load ONLY the matching skill(s). Never load more than 5 domain skills at once. The 9 BOOTSTRAP skills are pre-loaded.

---

## L0 · BOOTSTRAP — Always Loaded (9 skills)

These fire at session start via `BOOTSTRAP_MANIFEST.json`. You already have them.

| # | Skill | Kernel Verb | What It Does |
|---|-------|-------------|--------------|
| 1 | `kernel-bind` | arif_init | Session governance binding |
| 2 | `observe-ground` | arif_observe | Evidence before narrative |
| 3 | `route-dispatch` | arif_route | Right organ for right intent |
| 4 | `memory-manage` | arif_memory | Memory lifecycle discipline |
| 5 | `verify-gate` | arif_verify | 4-gate verification |
| 6 | `audit-seal` | arif_seal | Decision logging + sealing |
| 7 | `know-physics` | arif_observe | Physical law veto |
| 8 | `know-math` | arif_verify | Mathematical reasoning |
| 9 | `know-language` | arif_compose | Linguistic competence |

---

## L1 · GOVERNANCE — Constitutional Floor Enforcement

**Load when:** judging, sealing, floor-checking, authority questions, constitutional matters.

| Skill | Trigger | Use Case |
|-------|---------|----------|
| `ASI-agent-invariants` | "is this safe", "check floors", "constitutional" | 10 invariants + 12 governance rules |
| `ASI-constitutional-reasoning` | "apply F1-F13", "floor check", "governed action" | F1-F13 reasoning before any governed action |
| `ASI-mcp-governor` | "MCP routing", "tool authority", "governed MCP" | F1-F13 gated MCP routing |
| `APEX-humility-godel` | "am I overconfident", "confidence check", "Gödel" | Self-critique before SEAL-grade claims |
| `APEX-fff-loop-protocol` | "audit loop", "FFF loop", "recursive audit" | 5-pass recursive audit sequence |
| `APEX-quantum-eureka` | "insight", "contradiction", "eureka moment" | Cross-domain synthesis |
| `delta-omega-psi-multimodal-cognition` | "multimodal", "image + data", "cross-modal" | Δ·Ω·Ψ multimodal cognition rules |

**When in doubt between these:** Start with `ASI-agent-invariants`, escalate to `ASI-constitutional-reasoning`.

---

## L2 · SENSE — Observation & Evidence

**Load when:** searching web, fetching URLs, grounding claims, observing state.

| Skill | Trigger | Use Case |
|-------|---------|----------|
| `AGI-multimodal-bridge` | "analyze image + data", "visual + textual evidence" | Multi-modal reasoning bridge |
| `FORGE-spatial-grounding` | "where am I", "VPS location", "spatial context" | Geo-awareness for CLI operations |
| `geox-grounding` | "earth evidence", "geo context", "basin" | Geological grounding layer |
| `FLAME-router` | "route to FLAME", "free-tier model" | FLAME inference routing |
| `FLAME-operator` | "FLAME health", "FLAME hit rate", "model diagnostics" | FLAME health monitoring |

**Tools for SENSE (MCP — no skill needed):**
- `forge_fetch` (mode=search) — web search via SearxNG
- `forge_fetch` (mode=readable) — URL content extraction
- `brave_web_search` — Brave Search API
- `arif_observe` — kernel sense verb

---

## L3 · THINK — Reasoning & Planning

**Load when:** reasoning, planning, analyzing, summarizing, binding skills.

| Skill | Trigger | Use Case |
|-------|---------|----------|
| `AGI-plan-dag` | "multi-step plan", "DAG", "execution graph" | Build execution DAGs with checkpoints |
| `AGI-explorer-intelligence` | "explore", "hypothesize", "falsify", "verify" | OBSERVE→HYPOTHESIZE→FALSIFY→VERIFY loop |
| `ASI-skill-binding` | "discover skill", "bind skill", "compose skills" | Cross-organ skill discovery + composition |
| `ASI-summarize` | "summarize", "condense", "TL;DR" | Summarize long content |
| `ASI-context-window-mgr` | "context full", "compress", "token budget" | Context window lifecycle management |
| `AGI-claude-xml-structured-reasoning` | "structured reasoning", "XML boundaries" | XML-tagged structured reasoning |
| `AGI-codex-chain-of-thought` | "stepwise planning", "chain of thought" | Private stepwise CoT for Codex-style tasks |
| `causal555-pywhy` | "causal inference", "counterfactual", "do-calculus" | Causal reasoning with PyWhy |
| `atlas333-cognitive-geometry` | "cognitive geometry", "thought geometry" | Cognitive geometry analysis |

**Tools for THINK (MCP — no skill needed):**
- `arif_think` — kernel reasoning verb (modes: reason, reflect, verify, plan)
- `sequential-thinking` — MCP sequential thinking tool

---

## L4 · ACT — Execution (FORGE Skills — 62 total)

### L4a · GIT & GITHUB

**Load when:** git operations, PRs, commits, GitHub workflows.

| Skill | Trigger |
|-------|---------|
| `FORGE-github-ops` | "git push", "PR", "branch", "clone", "remote" |
| `FORGE-github-workflow` | "CI/CD", "GitHub Actions", "workflow yaml" |
| `FORGE-pr-review` | "review PR", "code review", "pull request review" |
| `FORGE-pr-governance` | "governed PR", "PR governance", "approval gate" |
| `FORGE-precommit-review` | "pre-commit", "before commit", "commit check" |
| `FORGE-precommit-gate` | (loaded with precommit-review) |
| `code-review` | "review this code", "code quality" |

### L4b · INFRA & DOCKER

**Load when:** VPS operations, Docker, infrastructure, service management.

| Skill | Trigger |
|-------|---------|
| `FORGE-vps-docker` | "Docker", "container", "docker compose", "docker ps" |
| `FORGE-vps-runbook` | "restart service", "systemctl", "VPS runbook" |
| `FORGE-infra-guardian` | "Caddy", "SSL", "Cloudflare", "DNS", "tunnel" |
| `FORGE-infra-crons` | "cron job", "crontab", "scheduled task" |
| `FORGE-docker-entropy` | "docker cleanup", "orphan container", "docker prune" |

### L4c · MCP & SKILLS

**Load when:** MCP server/tool work, skill creation/audit.

| Skill | Trigger |
|-------|---------|
| `FORGE-mcp-ops` | "MCP server", "MCP tool", "MCP transport" |
| `FORGE-mcp-lifeguard` | "MCP health", "MCP down", "MCP recovery" |
| `FORGE-mcp-smoke-test` | "test MCP", "MCP probe", "MCP smoke" |
| `FORGE-mcp-federation-ops` | "federation MCP", "cross-organ MCP" |
| `FORGE-mcp-a2a-agentic` | "A2A agent", "agent card", "agent mesh" |
| `FORGE-fastmcp` | "FastMCP", "build MCP server", "Python MCP" |
| `FORGE-skill-creator` | "create skill", "new skill", "forge skill" |
| `FORGE-skill-linter` | "lint skill", "skill quality", "skill audit" |

### L4d · WEB & SITES

**Load when:** building/deploying websites, frontend work.

| Skill | Trigger |
|-------|---------|
| `FORGE-agentic-web-builder` | "deploy site", "site down", "audit pages", "404" |
| `FORGE-nextjs-mastery` | "Next.js", "React SSR", "Vercel" |
| `FORGE-react-spa-discipline` | "React", "SPA", "Vite", "frontend app" |
| `FORGE-tailwind-tokens` | "Tailwind", "CSS tokens", "design system" |
| `AGI-web-optimization` | "SEO", "llms.txt", "web optimization" |

### L4e · SECURITY

**Load when:** secrets, tokens, security scans, injection defense.

| Skill | Trigger |
|-------|---------|
| `FORGE-secret-hygiene` | "secret leak", "token check", "vault hygiene" |
| `FORGE-sct-federation-ingress` | "SCT", "session token", "federation ingress" |

### L4f · CI/CD & DEPLOY

**Load when:** CI pipelines, Docker builds, deployment.

| Skill | Trigger |
|-------|---------|
| `FORGE-cicd-docker-deploy` | "CI/CD pipeline", "Docker build", "deploy pipeline" |
| `FORGE-ci-diagnose` | "CI broken", "workflow failed", "GitHub Actions fail" |

### L4g · CODE ANALYSIS

**Load when:** analyzing repos, code quality, developer metrics.

| Skill | Trigger |
|-------|---------|
| `FORGE-code-analysis` | "analyze repo", "developer metrics", "code quality" |
| `FORGE-repo-intelligence` | "repo overview", "repository map", "codebase" |
| `FORGE-context-compress` | "compress output", "large log", "truncate" |
| `FORGE-context-compressor` | (loaded with context-compress) |

### L4h · OPS & MONITORING

**Load when:** monitoring, federation health, drift detection.

| Skill | Trigger |
|-------|---------|
| `FORGE-route-least-power` | "least power", "route optimization" |
| `FORGE-verify-runtime` | "verify runtime", "runtime check", "SOT check" |
| `FORGE-federation-orchestrator` | "federation orchestrate", "cross-organ" |
| `FORGE-federation-manifest` | "federation manifest", "organ manifest" |
| `FORGE-telemetry-watchdog` | "telemetry", "watchdog", "monitoring" |
| `FORGE-model-monitor` | "model monitor", "LLM metrics" |
| `FORGE-symlink-audit` | "symlink audit", "broken links" |

### L4i · DOCS & TRUTH

**Load when:** documentation, README, cross-repo docs.

| Skill | Trigger |
|-------|---------|
| `FORGE-readme-truth-check` | "README check", "SOT stamp", "doc staleness" |
| `FORGE-cross-repo-doc-zen` | "cross-repo docs", "doc consistency" |
| `FORGE-governance-jsonld` | "JSON-LD", "governance context", "linked data" |

### L4j · AGENT ORCHESTRATION

**Load when:** spawning sub-agents, cross-agent work.

| Skill | Trigger |
|-------|---------|
| `FORGE-subagent-spawn` | "spawn agent", "sub-agent", "parallel agent" |
| `FORGE-cross-agent-handoff` | "handoff", "transfer task", "delegate" |
| `FORGE-onboarding` | "onboarding", "new agent setup" |
| `FORGE-t3a-binding-matrix` | "T3A matrix", "tool binding", "authority matrix" |

### L4k · INCIDENT RESPONSE

**Load when:** incidents, outages, escalation.

| Skill | Trigger |
|-------|---------|
| `FORGE-incident-escalation` | "escalate", "incident", "SEV1" |
| `FORGE-incident-triage` | "triage incident", "assess severity" |
| `FORGE-issue-triage` | "triage issue", "GitHub issue", "prioritize" |

### L4l · DATA & STORAGE

**Load when:** database, Redis, Qdrant, Postgres.

| Skill | Trigger |
|-------|---------|
| `FORGE-postgres-schema-design` | "Postgres schema", "database design", "migration" |
| `FORGE-redis-qdrant-integration` | "Redis", "Qdrant", "vector store", "cache" |
| `FORGE-data-compression` | "compress data", "archive", "storage optimization" |

### L4m · SPECIALIZED EXECUTION

| Skill | Trigger |
|-------|---------|
| `FORGE-did-web-identity` | "DID", "decentralized identity", "WebID" |
| `FORGE-google-workspace` | "Google Docs", "Gmail", "Google Drive" |
| `FORGE-kimi-code` | "Kimi", "Moonshot AI", "Kimi agent" |
| `FORGE-grok-profile` | "Grok profile", "X AI", "Grok config" |
| `FORGE-fastapi-api-builder` | "FastAPI", "Python API", "REST endpoint" |
| `FORGE-vault999-witness` | "VAULT999 witness", "seal chain witness" |
| `FORGE-seal-a-close` | "seal session", "close session", "session handoff" |
| `FORGE-visual-qa-w3` | "visual QA", "screenshot audit", "W3 witness" |
| `forge-document-intelligence` | "PDF", "OCR", "document scan", "extract text" |
| `FORGE-well-boundary-repair` | "WELL boundary", "medical boundary" |
| `FORGE-telegram-audit` | "Telegram audit", "Hermes Telegram" |
| `FORGE-mcp-gui` | "MCP GUI", "MCP inspector", "MCP UI" |

---

## L5 · SEAL — Memory & Vault

**Load when:** sealing, vault operations, session closure.

| Skill | Trigger |
|-------|---------|
| `ASI-session-seal-copilot` | "seal session", "end session", "handoff" (Copilot specific) |
| `ASI-session-seal` | "seal session", "end session" (general) |
| `audit-seal` | "audit seal", "vault seal", "seal receipt" |
| `AUDIT-recursive-audit` | "audit skills", "skill overlap", "skill portfolio" |
| `AUDIT-drift-detector` | "check drift", "manifest drift", "registry drift" |

---

## L6 · META — Self-Improvement & Skill Management

**Load when:** managing skills, self-audit, improvement cycles.

| Skill | Trigger |
|-------|---------|
| `AUDIT-skill-atlas` | "skill atlas", "skill inventory", "gap detection" |
| `AGI-skill-unification` | "skill unity", "skill mesh", "multi-harness skills" |
| `RSI-recursive-improvement` | "RSI cycle", "self improve", "recursive improve" |
| `ASI-drift-watch` | "drift watch", "SOT drift", "source drift" |
| `ASI-fabrication-prevention` | "verify existence", "artifact check", "no fabrication" |
| `ASI-observability` | "observability", "telemetry", "skill metrics" |
| `check-work` | "check my work", "verify output" |
| `create-skill` | "create skill", "bootstrap skill" |

---

## L7 · DOMAIN — Organ-Specific Intelligence

### GEOX (Earth Intelligence)

| Skill | Trigger |
|-------|---------|
| `geox-grounding` | "basin context", "geological evidence" |
| `geox-production-cockpit` | "GEOX dashboard", "production cockpit" |

**Tools (MCP — no skill needed):** `geox_basin`, `geox_petrophysics`, `geox_seismic_*`, `geox_well_*`, `geox_prospect`, `geox_claim`, etc.

### WEALTH (Capital Intelligence)

| Skill | Trigger |
|-------|---------|
| `wealth-claim-state` | "wealth claim", "capital claim", "financial state" |

**Tools (MCP — no skill needed):** `capital_primitive`, `capital_health`, `capital_market`, `capital_wisdom`, etc.

### WELL (Human Readiness)

**Tools (MCP — no skill needed):** `well_assess_homeostasis`, `well_validate_vitality`, `well_classify_substrate`, etc.

---

## L8 · KNOWLEDGE — Reference Substrate

**Always available, never "loaded" — these are the knowledge floor.**

| Skill | Purpose |
|-------|---------|
| `knowledge` | Federation knowledge substrate |
| `docs` | Documentation reference |
| `runtime` | Runtime environment reference |
| `scripts` | Script reference |
| `substrate` | Substrate reference |
| `reflective` | Reflection reference |

---

## L9 · SPECIALIZED — Niche Domains

**Load only when the task explicitly matches these domains.**

| Skill | Trigger |
|-------|---------|
| `aaa-pdf-voice-protocol` | "PDF voice", "voice protocol", "audio PDF" |
| `AGI-dream-engine` | "dream engine", "memory consolidation", "nightly seal" |
| `AGI-emd-decode` | "EMD decode", "decode upstream output" |
| `AGI-emd-encode` | "EMD encode", "encode observation" |
| `AGI-emd-metabolize` | "EMD metabolize", "memory promotion" |
| `AGI-entropy-lock-prime` | "entropy lock", "ΔS gate", "entropy reduction" |
| `AGI-hermes-system-prompt-voice` | "Hermes voice", "system prompt style" |
| `AGI-nusantara-substrate` | "Nusantara", "cultural dignity", "sovereignty lens" |
| `ASI-agentic-architecture` | "design agent", "agent architecture" |
| `ASI-agentic-governance` | "AAA governance design", "AREP declaration" |
| `ASI-fabrication-prevention` | "no hallucination", "verify before claim" |
| `apex-formal-constitution` | "formal constitution", "constitutional law" |
| `apex_audit_coverage_check` | "audit coverage", "test coverage audit" |
| `apex_authority_check` | "authority check", "who can do this" |
| `apex_floor_check` | "floor check", "F1-F13 check" |
| `apex_reversibility_test` | "reversibility", "can we undo" |
| `apex_scope_check` | "scope check", "blast radius" |
| `apex_tool_approval_gate` | "tool approval", "register tool" |
| `apex_verdict_hold` | "HOLD verdict", "pause action" |
| `apex_verdict_seal` | "SEAL verdict", "approve action" |
| `asi_evidence_tier_express` | "evidence tier", "evidence classification" |
| `asi_intent_hear` | "intent hearing", "understand intent" |
| `asi_interface_adapt` | "interface adaptation", "adapt output" |
| `asi_position_contrast` | "position contrast", "counter-position" |
| `asi_tone_read` | "tone reading", "emotional tone" |
| `asi_uncertainty_signal` | "uncertainty", "confidence interval" |
| `causal555-pywhy` | "causal inference", "do-calculus" |
| `federation-connect-headscale` | "Headscale", "Tailscale", "VPN mesh" |
| `federation-release-attestation` | "release attestation", "deploy attest" |
| `HERMES-opencode-protocol` | "Hermes OpenCode", "Hermes protocol" |
| `KERNEL-trinity-33` | "Trinity 33", "final repo map", "3-axis" |
| `warga` | "warga", "citizenship", "AAA membership" |
| `xauusd-trading` | "XAUUSD", "gold trading", "forex" |
| `code-review` | "code review", "review this" |
| `help` | "help", "what can I do" |
| `imagine` | "imagine", "creative", "generate idea" |

---

## ROUTING ALGORITHM — How to Select

```
1. Is this a BOOTSTRAP function? → Already loaded (L0)
2. Is this about constitutional floors/authority? → L1 GOVERNANCE
3. Is this about observing/searching/gathering? → L2 SENSE
4. Is this about reasoning/planning? → L3 THINK
5. Is this about executing/building? → L4 ACT (sub-route by domain)
6. Is this about sealing/vault/memory? → L5 SEAL
7. Is this about managing skills/self-improvement? → L6 META
8. Is this about a specific organ (GEOX/WEALTH/WELL)? → L7 DOMAIN
9. Is this a niche/specialized domain? → L9 SPECIALIZED
```

**ANTI-PATTERN: Load multiple FORGE skills for one task.** Pick the ONE most specific. Example:
- "deploy site" → ONLY `FORGE-agentic-web-builder` (not infra-guardian + vps-docker + cicd)
- "review PR" → ONLY `FORGE-pr-review` (not github-ops + precommit + code-review)

**PANIC RULE: Still unsure?** Load `AUDIT-skill-atlas` — it's the master skill inventory.

---

## Orthogonal Design Principles

1. **No overlap:** Each skill has one clear domain. If two skills trigger on the same phrase, merge them.
2. **Layered loading:** Bootstrap → Governance → Domain → Seal. Never skip layers on high-stakes work.
3. **Harness-aware:** Skills tagged `harness: copilot-cli` are native. Others may still work — test first.
4. **Minimal loading:** ≤5 domain skills per task. The agent is smart enough without overloading.
5. **Tool-first:** Many MCP tools (geox_*, capital_*, forge_*) need NO skill — just call them directly.

---

*DITEMPA BUKAN DIBERI — Forged 2026-07-28 for Copilot CLI as the single meta-mesa routing layer. This skill IS the orthogonal taxonomy. Load it whenever the task spans multiple domains or the right skill is unclear.*
