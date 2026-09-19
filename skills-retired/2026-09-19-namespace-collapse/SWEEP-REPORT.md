# Namespace collapse — sweep report

**Date:** 2026-09-19 · **Authority:** F13 sovereign, in-chat order ("buang benda bangang … pastikan ejen
in the futures lebih bijaksana") · **Scope:** canonical skill store `/root/AAA/skills` + every harness view.

**Why this pass exists:** the sovereign's diagnosis was *same capability, many identities* — capability
abundance plus taxonomy entropy, not capability famine. So this pass removes **identities**, not abilities:
every retired body is frozen with its bytes intact and an undo path in a ledger. Nothing was deleted.

## Witnesses (all re-runnable)

| Witness | Command / path | Before | After |
|---|---|---|---|
| Skill census | `/root/scripts/skills-census.py --write` | canon 709 · viewed 454 · broken 0 | canon 686 · viewed 441 · broken 0 |
| Freeze ledger | `skills-retired/2026-09-19-namespace-collapse/LEDGER.json` | — | 28 items, 80 file hashes |
| Alias repair ledger | `.../LEDGER-alias-repair.json` | — | 30 link actions |
| Git (causal ledger) | `git -C /root/AAA status --porcelain` | — | 121 tracked deletions under `skills/` |
| Full backup | `/root/AAA/backups/skills-pre-namespace-collapse-2026-09-19.tar.gz` | — | sha256 `2b2d4ab2…dadd1f` |
| Cost>value lens | `.../USAGE-COST-VALUE.txt` | — | 142 names with `use_count == 0` |

## Tier 1 — removed (identity only, body preserved)

* **6 aliases parading as skills** — body was a redirect: `mcp-shopping-list-2026-09`, `mcp-dual-era-transport`,
  `wisdom-scar-session-audit`, `sovereign-recognize`, `FORGE-mcp-testing`, `cognitive-level-assertion-protocol`.
* **3 tombstones / self-declared non-skills** — `RSI-recursive-improvement` (a 34-byte folder whose entire body
  read "RSI session endpoint documentation"), `causal555-pywhy`, top-level `wealth-claim-state`.
* **5 namespace stubs** — the `SKILL.md` of `runtime`, `scripts`, `docs`, `substrate`, `warga`; each declared
  itself "not an executable skill". The directories holding real children were kept.
* **Vendor / foreign-profile material sitting in the AAA catalog** — `.system/{imagegen, openai-docs,
  plugin-creator, review-agent, skill-installer, skill-creator}`, `.profile-archive/*` (a symlink farm into a
  third-party plugin repo), `help` (documents a product this federation does not run).
* **An archive that was still loading** — `.archive-2026-09-18/*` (its bodies were listed as live skills).
* **Case-twins** — `forge-federation-manifest`, `RSI-federation-mesh` (kept the newer twin of each).
* **Runtime scaffolding mislabelled as skills** — `docs/`, `runtime/`, `scripts/` moved out of the store;
  `skill-mesh-sync.sh` reinstalled to `/root/scripts/` and its caller in `cron/daily-drift-check.sh` repointed.

## View sweep (the part a body-level kill always forgets)

Retiring a name leaves dangling links in eight mirror trees. 30 link actions across
`~/.hermes/skills`, `~/.hermes/profiles/aaa-hermes/skills`, `~/.qwen`, `~/.claude`, `~/.codex`,
`~/.config/opencode`, `~/.kimi-code`, `~/.arifos/agents/opencode/skills`:
**repoint** where the name has a live successor, **remove** where the name itself is retired.
Census and the mesh check both return `broken 0` after the sweep.

Two dependents outside the store were repaired rather than left to rot: the daily drift cron
(hardcoded `skills/scripts/` path) and `hermes-chaos-sweep.py` (a human-reviewed "declared shell" list
naming two paths that no longer exist).

## Merge pass — delegated, running in parallel

Seven bounded jobs, each: read every body → write ONE canonical with modes/harness table → freeze the
sources → keep every old trigger phrase → ledger. Families: per-harness clones (`agentic-state`,
`zen-router`, `meta-mesa`, `propose-seal`), the control-audit family → `governance-audit`,
the voice lane → `voice-lane`, the briefing empire → `intelligence-briefing` + `person-intelligence`,
incident fossils → `recovery-playbook`.

## Findings that outlive the sweep

1. **The loader's own list is not the disk.** Names such as `token-plan-tts` and `help` appeared as
   available skills while resolving to nothing anywhere on disk. A surface that lists a name it cannot
   resolve is the same defect as a dead symlink, one layer up.
2. **The `knowledge` layer is a ghost layer.** The V3 registry declares 4 knowledge skills
   (`know-language`, `know-math`, `know-physics`, …); on disk each folder holds only `liveness.json`.
   Registry claims a capability that has no body. *Pre-existing defect, not caused by this sweep.*
3. **Cost is measurable, but only from one window.** `~/.hermes/skills/.usage.json` shows **142 names with
   `use_count == 0`** since tracking began 2026-09-04, including the largest never-touched bodies
   (`entity-failure-forensics` 57 KB, `mt5-ai-trading-agent` 49 KB, `document-pipeline` 40 KB). Caveat kept
   in the file itself: this lens covers ONE harness, so a zero here is evidence, never a verdict.
4. **Derived surfaces are where a count learns to lie.** After the sweep the stale names still sit in
   `SKILL_ALIAS_TABLE.json`, `OWNERSHIP_MAP.yaml`, `GENEALOGY.json` and `FEDERATED_SKILLS_REGISTRY_V3.yaml`.
   Reconciliation is the next action; until it is done the registry is still able to resurrect a retired name.
5. **The lesson is now loadable, not just recorded.** `skill-library-integrity` gained §6 "Retiring a NAME
   (namespace collapse)" — the six defect classes, the freeze convention, the view sweep, the merge rule —
   so the next agent follows a procedure instead of repeating the diagnosis.
