---
id: hermes-browser-skills-mesh-snap
name: hermes-browser-skills-mesh-snap
description: Use when browser tooling or skills federation comes up.
version: 1.0.0
risk_tier: low
owner: F13 SOVEREIGN — Muhammad Arif
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Hermes · Skills-Mesh · Browser Convergence — Snapshot 2026-08-13

> Durable facts captured because MEMORY.md hit a drift guard (backup:
> /root/.hermes/memories/MEMORY.md.bak.1786598284). Re-save into memory
> when the drift is resolved. DITEMPA BUKAN DIBERI.

## Browser convergence (Nous upstream)
- Upstream Nous retired 12 atomized browser tools (navigate/click/type/snapshot/…)
  → a SINGLE `browser_exec` tool (Browser Use CLI 3.0 driver; agent writes
  Python and runs it in the browser; click/type/drag/scrape in one script).
  Reported ~60% token cut, same accuracy.
- F1 guard: `browser_exec` IS ONLY offered when the terminal toolset is present
  (`model_tools.py` L572: if browser_exec present and terminal not → discard).
  Messaging-locked surfaces keep the built-in tools as fallback.
- Local Hermes updated 0.18.2 → v0.20.0 (2026-08-13). Backup:
  `/root/hermes_phaseA_backup_20260813-110210/` (baseline 68a940961, bundle 262MB).
- Config: `browser.engine: auto` (Browser Use mode when CLI runnable, else built-in),
  `allow_private_urls: true` (DO NOT disable — private/loopback arifOS/GEOX/WEALTH dashboards).
- `hermes update` resets to origin/main (6541 commits) and AUTO-STASHES local
  worktree changes; carried commits are NOT merged — recover via stash/git bundle.
- Vision-disclaimer hardening (NO_VISION_DISCLAIMER) was cherry-picked back to v0.20.
  NOT upstreamed, still absent in upstream. Do not re-apply duplicates.

## AAA Skills Mesh reality (live disk, not audit claims)
- AAA/skills = 194 canonical · Hermes ~/.hermes/skills = 418 (271 orphans) ·
  profile aaa-hermes = 436 (262 profile-specific) · Kimi = 254 (67 orphans) ·
  OpenClaw = 4 · OpenCode = 5.
- Mesh is copy-paste, NOT federated (no runtime discovery, no MCP tool registration).
  Registry FEDERATED_SKILLS_REGISTRY_V3.yaml is stale (says 95 / 2026-07-25; reality 194+).
- Two SKILL.md trees are distinct, NOT one: ~/.hermes/skills (418) vs profile aaa-hermes (436).
- Skills frontmatter is ALREADY rich and consistent: name(198) description(196)
  risk_tier(145) floor_scope(144) capability_tier(185) ecology_state(185)
  id(142) owner version autonomy_tier dependencies(37) version_lock tests host_compatibility.

## TREE777 / ATLAS333 / arifFLOW / PRL — all LIVE
- arifFLOW (:7073) — UP, FQ verdict OPTIMAL, ~1000 receipts.
- ATLAS333 — `arifos://atlas333/*` MCP resources (36 paradoxes, flow, quotes).
- TREE777 — `tree777://skills/*`, `//concepts`, `//scars`, `//registry/tools` (13 sealed tools).
- PRL/HANG INGAT BALIK — `.agents/lib/prl_gate.py`, called by mind_reason +
  arif_action_classifier (PRL_TAU=0.35; docstring stale says 0.95).
- BROKEN ARROW: TREE777 WIKI_ROOT = env TREE777_WIKI_ROOT, defaults to
  `/root/AAA/wiki` which is EMPTY (0 SKILL.md). REAL skills live at
  `/root/AAA/skills` (194). Fix the path to point at /root/AAA/skills — do NOT
  invent a new system.

## Arif's binding preference (F13-endorsed decision)
- Prefer INLINE YAML frontmatter binding (Laluan A): add `required_tools: [...]`
  + `tool_gate: permissive|strict` to existing SKILL.md frontmatter, plus ONE
  lightweight "compass" script that reads frontmatter → per-skill tool allowlist
  used to filter which tool schemas get injected into the system prompt.
- Rejected external DB / Neo4j (Laluan C) and vector RAG (Laluan B) as primary —
  "relaks tapi tajam, no bloatware". Vector discovery already covered by PRL.
- Rejects hallucinated audit numbers — ALWAYS probe-before-act (disk reality wins).
- F13 isolation: profile/identity/business-specific skills (nasi-lemak*, syedos,
  apex-*, arifos-*, multiuser, kunci-mas/secrets) MUST NOT be federated to AAA.

## Promoted to AAA/skills this session (SPOF removed)
- `image-text-editing` (~/.hermes/skills/creative/ → AAA/skills/creative/)
- `aaa-image-editing` (profile aaa-hermes/skills/media/ → AAA/skills/media/)