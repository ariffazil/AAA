# AAA Cleanup Receipt — 2026-05-25

## Objective
Clean AAA repository to match canonical identity: **Agent Operations Cockpit / Federation Control Plane**.

## Actions Taken

### 1. Debris Archived (1.3 GB)
Moved to `_archive/aaa-cleanup-2026-05-25/` — reversible, no permanent deletions.

| Category | Items Moved |
|----------|-------------|
| **Agent workspaces** | `.apex/`, `.codex/`, `.clawhub/` |
| **Hermes runtime** | `hermes-workspace/`, `hermes-skills/` (79 dirs), `hermes-backups/`, `hermes-config/`, `hermes-memories/`, `hermes-restart.sh` |
| **Constitutional leak** | `.REPO_ROUTING_CONSTITUTION.md`, `arifOS-sentinel/`, `ROOT_CANON.yaml`, `arifos.init`, `arifos_plan/`, `VAULT999/` |
| **Project debris** | `SEARAH/` (3MB+ PDFs), `FORGE-HERMES-REPAIR-report.txt`, `ariffazil.png`, `ARIF.md.bak.*`, `portfolio-map-pending.json`, `jackie/`, `termux-ssh-agent.sh` |
| **Python orphans** | `core/`, `acp/`, `vault/`, `af1/` |
| **OpenClaw runtime** | `openclaw/` (preserved `bridge.yaml` → `a2a/federation-bridge.yaml`) |
| **Agent configs** | `opencode.json` |

### 2. Contracts Updated
- `contracts/init/000-init.yaml` — removed arifOS-specific canons (`ROOT_CANON.yaml`, `arifos.init`), now requires `README.md`, `AGENTS.md`, `agent-card.json`
- `contracts/federation/111-sense.yaml` — updated `runtime_bridge_ref` to `a2a/federation-bridge.yaml`
- `contracts/decisions/888-999-decisions.yaml` — removed vault export entries (AAA does not own vault)
- `contracts/skills/packages.yaml` — removed `openclaw/` source paths

### 3. Validate Script Updated
- `scripts/validate-aaa.mjs` — removed `openclaw/a2a/bridge.yaml` bridge checks, updated boot sequence check, added null-safe vault export guard

### 4. Documentation Updated
- `README.md` — **rewritten from 332 lines to 196 lines** (41% reduction). Replaced over-engineered protocol stacks and gWasm compiler sections with human analogies (airport control tower, org chart, dispatch desk). Added "What AAA Answers" table. Removed outdated target-state tables and APEXMax Telegram section.
- `AGENTS.md` — updated `last_verified` to 2026-05-25, added canonical identity header
- `FEDERATION_COCKPIT.md` — **new canonical authority document** defining identity, boundaries, structure, and federation mesh

## Verification
- `npm run build` ✅ — passes, dist/ generated
- `node scripts/validate-aaa.mjs` ✅ — passes with 6 agents, 3 A2A agents, 6 public surfaces
- No broken imports in `src/`, `a2a-server/`, `scripts/`

## Remaining Items (Intentionally Preserved)
- `agents/openclaw/` — agent **identity** directory (not runtime). Contains handoff-protocol.yaml created earlier today.
- `src/seed/` — imported by `src/gateway/server.ts`. Contains boot seed data for A2A gateway.
- `agents/apex/` — agent identity directory with APEX agent card and config.
- `docs/archive/`, `wiki/_archive/`, `archive/`, `_archive/` — pre-existing archives not touched.

## Git Status
- 72+ deletions (D), 8 modifications (M), 4 new files (??)
- Pre-existing uncommitted changes preserved: `a2a-server/server.js`, `wiki/log.md`, `a2a-server/agent-cards/hermes-asi.json`, `agents/openclaw/config/handoff-protocol.yaml`

### 5. Skill Library Created

Canonical skill library established under `AAA/skills/`:

| Skill | Priority | Status |
|-------|----------|--------|
| `repo-hygiene-audit` | **P0** | Full SKILL.md + examples.md |
| `mcp-smoke-test` | P1 | Full SKILL.md |
| `agent-onboarding` | P1 | Full SKILL.md |
| `github-pr-review` | P2 | Full SKILL.md |
| `service-health-triage` | P2 | Full SKILL.md |
| `secret-safety-scan` | P2 | Full SKILL.md |
| `readme-truth-check` | P2 | Full SKILL.md |
| `parallel-authority-detection` | P2 | Full SKILL.md |
| `pr-review-governance` | P2 | Full SKILL.md |
| `incident-escalation` | P2 | Full SKILL.md |
| `openclaw-a2a-bridge` | legacy | Minimal SKILL.md (workflow compatibility) |
| `geox-grounding` | legacy | Minimal SKILL.md (workflow compatibility) |

**Supporting files:**
- `skills/README.md` — Skill system overview, authority hierarchy, TREE777 audit
- `skills/SKILL_TEMPLATE.md` — Canonical template for all new skills
- `scripts/tree777-skill-audit.mjs` — Weekly skill audit script

**Registry updated:** `registries/skills.yaml` now contains 12 skills (was 2).  
**Packages updated:** `contracts/skills/packages.yaml` now contains 12 packages (was 2).  
**Validation:** `npm run validate:aaa` passes with 12 skills.

## Next Steps (Optional)
1. Review archive contents before eventual permanent deletion
2. Restart AAA A2A server (port 3001) to pick up Hermes card registration
3. Update `arifOS/SITE-AUDIT-2026-05-25.md` to reflect AAA cleanup
4. Write `tests.md` for each skill to clear TREE777 promotion blocks
5. Commit when ready

---
*SEAL: 333_MIND-DITEMPA-BUKAN-DIBERI-20260525*
