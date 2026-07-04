# AAA Skill Registry Draft — 2026-06-23

> **Authority:** ARIF directive `ARIFOS::AAA_FEDERATED_SKILL_ALIGNMENT::v1`  
> **Purpose:** Map every discovered skill scope into AAA's canonical view, identify entropy, and propose consolidation.  
> **Status:** DRAFT — awaits ARIF approval before any quarantine/merge.

## Scope Inventory

| Scope | Path | Count | Governance Owner |
|---|---|---|---|
| Kimi Code user-scope | `/root/.arifos/agents/kimi/skills/` | 7 | Kimi Code CLI / AAA |
| Project-scope | `/root/.agents/skills/` | 45 | AAA (project-wide) |
| AAA-scope | `/root/AAA/skills/` | 40 | AAA federation control plane |
| OpenCode-scope | `/root/.arifos/agents/opencode/skills/` | 48 | OpenCode CLI / AAA |
| HERMES-scope | `/root/HERMES/skills/` | ~30 | HERMES ASI deliberative relay |
| arifOS-scope | `/root/arifOS/skills/` | ~5 | arifOS constitutional kernel |
| WELL-scope | `/root/WELL/skills/` | ~2 | WELL human readiness |
| .forge-scope | `/root/.forge/skills/` | 3 | Forge instrument |
| .grok-scope | `/root/.grok/skills/` | 10 | Grok instrument |

## OpenCode Skills — Full Catalog

| # | Skill ID | Purpose | Frontmatter | Has Examples/Tests/Bindings | Proposed Action |
|---|---|---|---|---|---|
| 1 | `777-forge-agi-contrast` | Spawn validation gate | ❌ none | ❌ | Merge into `contrast-engine` |
| 2 | `777-forge-apex-contrast` | Sovereign verifiability gate | ❌ none | ❌ | Merge into `contrast-engine` |
| 3 | `777-forge-asi-contrast` | Independent verification gate | ❌ none | ❌ | Merge into `contrast-engine` |
| 4 | `aaa-workspace` | AAA workspace operations | ✅ YAML | ❌ | Standardize + add tests |
| 5 | `agent-zero` | Agent Zero ops | ❌ none | ❌ | Add frontmatter + tests |
| 6 | `architect-agi-contrast` | Architecture contrast | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 7 | `architect-apex-contrast` | Final pre-emit check | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 8 | `architect-asi-contrast` | Self-empathy check | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 9 | `arifOS-federation` | Federation repo mapping | ✅ YAML | ❌ | Update stale ports, add tests |
| 10 | `arifos-kernel` | arifOS kernel entrypoint | ✅ YAML | ❌ | Standardize, add bindings |
| 11 | `arifos-operator` | Governed MCP operations | ✅ YAML | ❌ | Standardize, add bindings |
| 12 | `backup-dr` | Backup / disaster recovery | ✅ YAML | ❌ | Standardize |
| 13 | `caddy-cloudflare` | Caddy + Cloudflare ops | ✅ YAML | ❌ | Standardize |
| 14 | `claude-code-ops` | Claude Code maintenance | ✅ YAML | ❌ | Standardize |
| 15 | `constitutional-advisor` | F1-F13 quick reference | ✅ YAML | ❌ | Possible merge with AAA `arifos-governance` |
| 16 | `constitutional-reasoning` | Governance reasoning lens | ✅ YAML (rich) | ❌ | Standardize |
| 17 | `cross-domain-reasoning` | Anomalous contrast | ❌ none | ❌ | Add frontmatter |
| 18 | `database-tuning` | DB tuning | ✅ YAML | ❌ | Standardize |
| 19 | `docker-security` | Docker security | ✅ YAML | ❌ | Standardize |
| 20 | `docker-thermodynamics` | Docker thermodynamics | ✅ YAML | ❌ | Standardize |
| 21 | `fastmcp-deploy` | FastMCP VPS deployment | ✅ YAML | ❌ | Add examples/tests |
| 22 | `fff-sweep` | FFF sweep | ✅ YAML | ❌ | Standardize |
| 23 | `final-agi-contrast` | Final contrast | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 24 | `final-apex-contrast` | Final apex check | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 25 | `final-asi-contrast` | Final asi check | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 26 | `github-issues` | GitHub issue triage | ✅ YAML | ❌ | **Add EXAMPLES_MD.md + tests.md** |
| 27 | `hermes-ops` | HERMES operations | ✅ YAML | ❌ | Standardize |
| 28 | `integrator-agi-contrast` | Integrator contrast | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 29 | `integrator-apex-contrast` | Integrator apex | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 30 | `integrator-asi-contrast` | Integrator asi | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 31 | `mcp-builder` | MCP server development | ✅ YAML + references | ❌ | **Add EXAMPLES_MD.md + tests.md** |
| 32 | `microsoft-eureka-integration` | Microsoft Eureka | ✅ YAML | ❌ | Standardize |
| 33 | `rsi-agi-contrast` | RSI contrast | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 34 | `rsi-apex-contrast` | RSI apex | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 35 | `rsi-asi-contrast` | RSI asi | ✅ YAML | ❌ | Merge into `contrast-engine` |
| 36 | `secret-hygiene` | Secret hygiene | ✅ YAML | ❌ | Standardize |
| 37 | `secret-rotation-guide` | Secret rotation | ✅ YAML | ❌ | Standardize |
| 38 | `skill-reflector` | Self-audit loop | ✅ YAML + audit-log | ❌ | Standardize |
| 39 | `software-development` | Software dev guide | ❌ file not in dir | ❌ | Move into directory + add frontmatter |
| 40 | `staff-engineer-review` | Staff engineer review | ✅ YAML | ❌ | Standardize |
| 41 | `vault-integrity` | Vault integrity | ✅ YAML | ❌ | Standardize |
| 42 | `vault999-ops` | VAULT999 ops | ✅ YAML | ❌ | Standardize |
| 43 | `vps-audit` | VPS audit | ✅ YAML | ❌ | Standardize |
| 44 | `vps-docker` | VPS Docker | ✅ YAML | ❌ | Standardize |
| 45 | `vps-management` | VPS management | ✅ YAML | ❌ | Standardize |
| 46 | `well-governance-ops` | WELL governance | ✅ YAML | ❌ | Standardize |
| 47 | `witness-effect` | Witness effect | ✅ YAML | ❌ | Standardize |

## GitHub-Related Skills Across Scopes

| Skill ID | Scope | Purpose | Overlap / Notes | Proposed Canonical |
|---|---|---|---|---|
| `github-issues` | OpenCode | Monitor/triage federation GitHub issues | Narrow scope | **OpenCode canonical** |
| `github-workflow` | AAA agent-card | Umbrella GitHub ops | Class-level, not file | Promote to AAA-scope skill |
| `github-ci-diagnose` | AAA | Parse failing CI logs | No OpenCode equivalent | AAA canonical |
| `github-issue-triage` | AAA | Issue triage workflow | Overlaps `github-issues` | Merge/align with `github-issues` |
| `github-pr-review` | AAA | PR review governance | No OpenCode equivalent | AAA canonical |
| `github-runbook` | AAA | Git & CLI operations | No OpenCode equivalent | AAA canonical |

## MCP-Related Skills Across Scopes

| Skill ID | Scope | Purpose | Overlap / Notes | Proposed Canonical |
|---|---|---|---|---|
| `mcp-builder` | OpenCode | Build MCP servers | Most complete | **OpenCode canonical** |
| `fastmcp-deploy` | OpenCode | Deploy FastMCP servers | Deployment-specific | **OpenCode canonical** |
| `arifos-kernel` | OpenCode | Use arifOS MCP tools | Operational | **OpenCode canonical** |
| `arifos-operator` | OpenCode | Governed MCP operations | Operational | **OpenCode canonical** |
| `arifos-mcp-federation` | AAA | Route across federation MCPs | Strategic routing | AAA canonical |
| `mcp-federation-ops` | AAA | Build/operate MCP servers | Overlaps `mcp-builder` | Reference OpenCode `mcp-builder` |
| `mcp-smoke-test` | project-scope | Validate MCP servers | Testing | project-scope canonical |
| `mcp-fastmcp-builder` | Kimi user-scope | Build FastMCP substrates | Overlaps `mcp-builder` | Keep as Kimi canonical |

## Cross-Scope Duplicates / Overlaps (Post-Quarantine State)

| Concept | Scopes | Resolution |
|---|---|---|
| Constitutional governance | OpenCode `constitutional-advisor` / AAA `arifos-governance` | AAA owns canonical doctrine; OpenCode skill should reference AAA |
| MCP federation routing | OpenCode `arifos-operator` / AAA `arifos-mcp-federation` | AAA owns strategy; OpenCode owns operational invocation |
| GitHub issue triage | OpenCode `github-issues` / AAA `github-issue-triage` | Converge on one canonical; AAA for governance, OpenCode for execution |
| Contrast gates | 15 OpenCode `*-agi/apex/asi-contrast` skills | Merge into parameterized `contrast-engine` skill |

## External Best Practices to Apply

From Anthropic MCP spec, GitHub MCP server, OpenCode docs, and agent-skills community:

1. **Tool annotations are mandatory safety signals** — `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` must be set on every tool.
2. **Service-prefix tool naming** — `{service}_{action}_{resource}` (e.g., `github_create_issue`) to avoid collisions.
3. **Top-level `title` field** (MCP 2025-11-25) — deprecated `annotations.title` in favor of top-level title.
4. **Structured outputs / `outputSchema`** (MCP 2025-06-18) — declare output schemas for programmatic consumers.
5. **Elicitation support** — when required args are missing, request clarification from the client instead of failing silently.
6. **Context budget discipline** — disable unused MCP servers; GitHub MCP alone adds ~5,000 tokens.
7. **Progressive disclosure for skills** — load metadata first, full body only when triggered.
8. **Skill packaging standard** — `SKILL.md` + `EXAMPLES_MD.md` + `tests.md` + `bindings/` per skill.
9. **Input validation** — Zod (TS) or Pydantic v2 (Python) with `.strict()` / `extra='forbid'`.
10. **Least-privilege auth** — fine-grained PATs, `env:` references, no hardcoded secrets.
11. **Pagination & character limits** — `has_more`, `next_offset`, default 25k char limit.
12. **Server per domain** — one MCP server per bounded context (GitHub, Linear, DB, etc.).

## Entropy Reduction Plan

### Phase 1 — Stabilize OpenCode skill packaging (low blast radius)
- [ ] Add `EXAMPLES_MD.md` and `tests.md` to `github-issues` and `mcp-builder` first.
- [ ] Add `bindings/cli.yaml` to all OpenCode skills.
- [ ] Standardize frontmatter for 5 skills missing YAML.
- [ ] Move `software-development.md` into a proper directory.

### Phase 2 — Merge contrast skills (medium blast radius)
- [ ] Forge a single `contrast-engine` skill parameterized by role (777-forge, architect, integrator, rsi, final) and lens (agi, apex, asi).
- [ ] Quarantine the 15 individual contrast skills after `contrast-engine` is tested.

### Phase 3 — Align with AAA canonicals (medium-high blast radius)
- [ ] Converge GitHub skills: either promote `github-issues` to AAA or merge with `github-issue-triage`.
- [ ] Converge MCP skills: `mcp-builder` (OpenCode) remains build canonical; `arifos-mcp-federation` (AAA) remains routing canonical.
- [ ] Update `arifOS-federation` stale port info (8080 → 8088, HERMES port ambiguity).

### Phase 4 — Federation-wide registry (low blast radius)
- [ ] Promote this draft to `AAA_SKILL_REGISTRY.md`.
- [ ] Add an automated skill auditor that validates frontmatter, examples/tests, bindings, and trigger collisions.

## Risk Gating

- **READ_ONLY:** This registry draft.
- **PROPOSE_ONLY:** Frontmatter standardization, adding examples/tests.
- **GUARDED_WRITE:** Moving `software-development.md`, merging contrast skills.
- **IRREVERSIBLE:** None planned.
