# REPO_ROUTING_CONSTITUTION.md
> **DITEMPA BUKAN DIBERI** — Routing intelligence is earned, not assumed.
> **Amanah clause:** Never route faster than certainty. Refuse over misroute.
> **Version:** 2026.05.02-KANON | **Authority:** Human Architect (Arif) | **Enforcement:** VPS workspace isolation + GitHub branch protection

---

## MISSION

Put every piece of work into the **correct repository** — on VPS and on GitHub.
Prefer refusal over misrouting. Never trade correctness for speed.
Autonomy is permitted only under these rules. Without them, stop.

---

## AUTHORITATIVE REPO MAP

| Repo | Domain Charter | VPS Workspace | GitHub |
|------|---------------|---------------|--------|
| **AAA** | Agent workspace, governance ADRs, orchestration canon, routing policy | `/root/AAA/` | `github.com/ariffazil/AAA` |
| **WEALTH** | Capital intelligence, portfolio, finance, macro/micro economic tooling | `/root/WEALTH/` | `github.com/ariffazil/wealth` |
| **GEOX** | Earth domain, geo/terrain/maps, well logs, subsurface, planetary tooling | `/root/GEOX/` | `github.com/ariffazil/geox` |
| **arifOS** | Constitutional kernel, F1–F13 floors, 9-Organ Canon, MCP runtime, 13-tool surface | `/root/arifOS/` | `github.com/ariffazil/arifOS` |
| **A-FORGE** | Planning twin, design, architecture, prefrontal build logic, engine–cockpit bridge | `/root/A-FORGE/` | `github.com/ariffazil/A-FORGE` |
| **arif-sites** | Website/static/web-facing assets, public surface | `/root/arif-sites/` | `github.com/ariffazil/arif-sites` |
| **ariffazil** | Personal/profile/meta public root | `/root/ariffazil/` | `github.com/ariffazil/ariffazil` |

**OpenClaw workspace:** `/srv/openclaw/workspace/` — AGI agent operative home.
**Hermes workspace:** `/root/.hermes/workspace/` — ASI agent operative home.
**VPS repos at:** `/root/{AAA,WEALTH,GEOX,arifOS,A-FORGE,arif-sites,ariffazil}/`

---

## CLASSIFICATION RULES

Before any write, commit, or push — determine destination:

1. **Read the file's domain.** Finance/portfolio code → WEALTH. MCP server/floors → arifOS. Earth/subsurface → GEOX. Agent governance/routing policy → AAA. Planning/design/architecture → A-FORGE. Web assets → arif-sites.
2. **Check existing repo content.** If the file you're editing already lives in a repo, it stays there.
3. **Cross-repo moves require explicit human confirmation (888_HOLD).** Never silently move code between repos.
4. **If confidence < 0.8, stop and ask.** Don't guess. Amanah > convenience.

**Confidence check protocol:**
- `high` (≥0.9): proceed with branch → PR
- `medium` (0.7–0.89): open draft PR, flag for review
- `low` (<0.7): refuse, explain, ask Arif

---

## PUSH GATE RULES

### Never
- ❌ `git push origin main` directly
- ❌ Push to any protected branch without a PR
- ❌ Cross-repo code movement without 888_HOLD
- ❌ Silent commit and push (no PR)

### Always
- ✅ `git checkout -b repo/feature-name` — branch naming: `{repo}/{short-description}`
- ✅ `git commit` with descriptive message referencing domain
- ✅ `git push origin repo/feature-name`
- ✅ Open PR with description

---

## AUTONOMOUS CAPABILITIES (within rules)

The agent **may** without asking:
- Read and analyze files in any repo
- Create branches in any repo
- Commit with descriptive messages
- Open PRs to any target branch
- Run tests, lint, build verification

The agent **must not** without 888_HOLD human confirmation:
- Push directly to main/master
- Move code between repos
- Delete files or history
- Modify branch protection rules

---

## LOW-CONFIDENCE PROTOCOL

```
STOP — do not route
Reason: [explain why classification failed]
Ask: "Arif — which repo does this belong to?"
```

Never fill ambiguity with convenience. "Close enough" is a violation of F08 GENIUS.

---

## VPS → GitHub SYNC RULES

| Action | Rule |
|--------|------|
| New feature work | Branch in VPS repo → PR to GitHub |
| Hotfix | Branch → fast-track PR → merge |
| Config changes | Branch → PR → require CI pass |
| Cross-repo coordination | 888_HOLD before touching second repo |

---

## ROUTING EXAMPLES

| Work item | Target repo | Branch pattern |
|-----------|-------------|----------------|
| New MCP tool for wealth | arifOS (tool lives in runtime) | `arifOS/wealth-mcp-tool` |
| Finance calculation library | WEALTH | `wealth/fin-calc-lib` |
| GEOX well correlation panel | GEOX | `geox/well-correlation-v2` |
| Constitutional floor fix | arifOS | `arifos/floor-F07-fix` |
| A-FORGE planning twin | A-FORGE | `aforge/planning-twin-v3` |
| Website asset | arif-sites | `arif-sites/[feature]` |
| AAA governance ADR | AAA | `aaa/adr-[number]-[topic]` |
| Mixed: arifOS + WEALTH | STOP → 888_HOLD | Requires human |

**Ditempa Bukan Diberi — Routing intelligence is forged, not given.**