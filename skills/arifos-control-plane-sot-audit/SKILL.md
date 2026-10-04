---
name: arifos-control-plane-sot-audit
description: "Map and rank cross-SOT contradictions across the AAA control plane (organ SOTs, topology YAMLs, A2A registries, authority-ceiling YAMLs, live runtime, skill mesh). Use when someone asks 'audit the control plane', 'rank drifts by severity', 'find contradictions between SOTs', 'does X match Y federation-wide', 'are my agents in sync right now', or 'where do the org charts disagree'. NOT for single-organ verification (use federation-infra-verification), NOT for sibling-report fact-checking (use verify-nested-sibling-reports), NOT for fixing specific runtime failures (use arifos-federation-ops)."
---

# arifOS Control-Plane Cross-SOT Audit

Methodology for mapping the multi-SOT disagreement landscape in the AAA control plane. Distinct from single-organ verification (one drift, one fix) and sibling-report verification (one claim, one probe). The audit's deliverable is a **ranked contradiction table** that holds across organs and across SOT axes.

## 1. The 6 SOT axes that disagree

For any federation organ, the canonical claim is duplicated across at least these 6 axes — they routinely disagree:

| # | Axis | Files (examples) |
|---|---|---|
| 1 | **Tool surface SOT** | `arifOS/tools_sot.yaml` (regenerated from `constitutional_map.py`), `A-FORGE/contracts/mcp_surface.yaml`, `A-FORGE/contracts/tools.yaml`, `AAA/registries/tools.yaml` |
| 2 | **Topology YAML** | `AAA/federation/organs.yaml` (machine SOT), `AAA/federation/workspace.yaml` (canonical_repos), `AAA/federation/federation-manifest.yaml` (deployment), `AAA/federation/repos.yaml` (tool counts), `AAA/docs/ORGAN.md` (human map), `ROOT_AGENT_CONFIG.yaml` (runtime peers) |
| 3 | **A2A registry** | `AAA/a2a/registry/agents.yaml` (operational), `AAA/registries/AGENTS_UNIFIED.yaml` (identity lanes, FI slots) |
| 4 | **Authority-ceiling SOT** | `organs.yaml::authority_ceiling` (6-band vocabulary) vs `A-FORGE/a_think/organ_authority_ceilings.yaml` (APEX §8 5-band scale) |
| 5 | **Live runtime** | `:port/health` endpoint per organ |
| 6 | **Skill mesh SOT** (verified 2026-08-08) | `AAA/skills/<name>/SKILL.md` (catalog — source of truth) vs `~/.hermes/skills/<name>/SKILL.md` (Hermes view) vs `~/.kimi-code/skills/<name>/SKILL.md` (Kimi view). Each tree carries its own `version:` field — sync is assumed, not propagated-by-symlink. The mesh health check is the `AUDIT-agent-skill-mesh` skill; the runnable recipe is `scripts/skill-mesh-probe.sh`. |

## 2. Audit methodology

Per organ, run this 7-step recipe — read top-of-file claim, then bottom-of-file state, then probe live:

1. **Human map first.** Open `AAA/docs/ORGAN.md` §1 anatomy. Read the descriptive text.
2. **Machine SOT.** Open `AAA/federation/organs.yaml::components`. Get port, unit, role, forbidden_domains, authority_ceiling, live_probe_*.
3. **Two other topology SOTs.** Open `workspace.yaml` and `federation-manifest.yaml`. Diff them.
4. **Tool surface SOT.** Open `tools_sot.yaml` or `mcp_surface.yaml`. **Note `last_verified` timestamp** — stale SOTs are the #1 cause of disagreement.
5. **Source code.** Open the organ's chamber/verb definitions in source (e.g. `signal_organ/chambers.py`, `frame_organ/main.py`). Count actual functions/handlers.
6. **Live probe.** `curl :port/health` — record tool count, chamber count, governance state.
7. **Cross-check authority ceilings.** `organs.yaml::authority_ceiling` field (6-band scale: JUDGE_ONLY/EXECUTE_AFTER_SEAL/COMPUTE_ONLY/REFLECT_ONLY/OBSERVE_ONLY/DISPLAY_ONLY/...) vs `organ_authority_ceilings.yaml::ceiling_band_equivalent` (APEX §8 5-band scale). They use **different vocabularies**; map them manually. `EXECUTE_AFTER_SEAL ≈ FULL`, `DISPLAY_ONLY` has no APEX equivalent and is suspect, `EDGE_AGENT` has no equivalent either.

For axis 6 (skill mesh), append:

8. **Skill mesh probe.** Run `scripts/skill-mesh-probe.sh` (or `AUDIT-agent-skill-mesh` §1). Classify each row SYNC / DIVERGED / MISSING_FROM_X. Treat placeholders (`version: semver`, `version: {semver}`) as UNPARSEABLE → flag, don't equate.

## 3. The 7 recurring contradiction patterns (verified 2026-08-08)

| # | Pattern | What to grep for | Fix shape |
|---|---|---|---|
| 1 | **Multi-SOT tool-count disagreement** | grep `tool_surface\|tools_public\|stateless_tools\|mcp_reported` across 4 files for same organ | Regenerate from a single source (e.g. `tools_sot.yaml` codegen from `constitutional_map.py`); add contract test rejecting deploy when live ≠ registered |
| 2 | **Dual authority-ceiling vocabulary** | grep `DISPLAY_ONLY\|T3_888_HOLD\|COMPUTE_ONLY\|OBSERVE_ONLY` across `organs.yaml` and `organ_authority_ceilings.yaml` | Pick APEX §8 5-band as canonical; rewrite `organs.yaml::authority_ceiling` to the band; keep role descriptors in a separate `role:` field |
| 3 | **Chamber-count split (declared N vs implemented M)** | grep `chamber_[0-9]` in organs.yaml and `chamber_[0-9]`/chamber list in organ's source | Either ship the missing chambers OR correct organs.yaml to M |
| 4 | **workspace.yaml missing new organs** | `grep '<newname>' workspace.yaml` for any organ that exists in organs.yaml with a port | Add to workspace.yaml `canonical_repos:` and bump `sot_manifest.version` |
| 5 | **`aaa-drift-check.py` scope gap** | list what the drift checker checks (in `AAA/scripts/aaa_drift_check.py` ~263 lines) vs what cross-SOT patterns exist | The drift checker is AAA-internal-only; it can never catch cross-organ contradictions. Either extend it (read organ SOTs too) or build a separate federation-wide checker |
| 6 | **FED alias ↔ A2A model-metadata drift** (verified 2026-08-07) | grep `fed_alias`/`litellm-federation/`/`model:` across `AAA/a2a/registry/agents.yaml`, `AAA/registries/AGENTS_UNIFIED.yaml`, `A-FORGE/litellm-config.yaml`, and live `:4000/model/info` | Canonical binding map (`AAA/federation/federation-model-bindings.yaml`) + drift-gate script (`AAA/scripts/aaa_a2a_sync.py`) diffing declared vs live aliases, exit 1 on drift. Runtime can succeed while A2A control plane is blind. |
| 7 | **Skill mesh divergence across AAA/Hermes/Kimi** (verified 2026-08-08) | `find /root/AAA/skills /root/.hermes/skills /root/.kimi-code/skills -maxdepth 2 -name 'SKILL.md' \| xargs grep '^version:'` — sort by skill, diff versions per tree | Status per skill: SYNC / DIVERGED / MISSING_FROM_X. Escalation: DIVERGED → flag (no fix on first sight); `>3 sessions` DIVERGED → fix (align to AAA version); MISSING_FROM_X → propagate from AAA (catalog is SOT). Orphan in non-AAA tree (MISSING_FROM_aaa) → reverse-propagate first. |

## 4. Ranked findability by blast radius

Order the found contradictions for the user's attention (worst-first):

1. **Multi-SOT tool-count disagreement** — affects every integration that trusts any one SOT (ChatGPT connector, MCP clients, SOT pinning for CI)
2. **FED alias ↔ A2A model-metadata drift** — A2A gateway cannot route, audit, or display what model is powering each agent; runtime may still work via OpenCode inline `litellm-federation/*` references that bypass the broken A2A declarations
3. **Skill mesh divergence** (pattern #7) — silent: agents behave differently from the catalog because propagation failed, but the AAA catalog still claims SYNC. Answer to "are my agents in sync right now?" is unreliable until the mesh is probed. Cheapest to detect (one `find + xargs grep`), slowest to drift back (a single `rsync` from AAA closes every MISSING row).
4. **Dual authority-ceiling vocabulary** — silent disagreement at governance time; an agent that passes one SOT may FAIL another
5. **Missing workspace.yaml organs** — renderers that re-emit AGENTS.md silently drop unlisted organs
6. **Chamber-count split** — incorrect SOT values bleed into runbook/manifest
7. **`aaa-drift-check` coverage gap** — the audit tool itself doesn't catch any of patterns 1-6

## 5. The aaa-drift-check scope audit (run before trusting it)

The drift checker at `AAA/scripts/aaa_drift_check.py` (~263 lines, exit codes 0=SEAL / 1=PARTIAL / 2=HOLD / 3=VOID) only checks AAA-internal paths. Verified 2026-08-06:

| It checks | It MISSES |
|---|---|
| `AAA/a2a/registry/agents.yaml` agent cards resolve | `A-FORGE/contracts/mcp_surface.yaml` tool counts |
| `AAA/registries/AGENTS_UNIFIED.yaml` FI slot uniqueness | `arifOS/tools_sot.yaml` tool counts |
| `AAA/skills/*/SKILL.md` ↔ `skills.yaml` registration | Cross-organ port matches |
| Deprecated/tombstone files in active paths | Authority-ceiling YAML agreement |
| A2A alignment spec exist-checks | FRAME/SIGNAL/arifFlow chamber counts |
| 333-AGI / 555-ASI / 888-APEX identity files | VAULT999 hash-chain coverage |
| NI-LOCKED tools (authority/gate/risk hint presence) | I-ARIF corpus vs manifest drift |

**Note (verified 2026-08-08):** pattern #7 (skill mesh) sits in a third gap — `aaa-drift-check.py` checks `AAA/skills/*/SKILL.md` ↔ `skills.yaml` registration (AAA-internal only), but does NOT compare AAA versions against `~/.hermes/skills/` or `~/.kimi-code/skills/`. The mesh drift is invisible to `aaa-drift-check`. Use `scripts/skill-mesh-probe.sh` (or the `AUDIT-agent-skill-mesh` skill) instead.

When asked "does the drift checker catch X?" — the answer is "yes" only for AAA-internal check items, "no" for any cross-organ, cross-tree, or organ-source claim.

## 6. The I-ARIF flip-point (honest framing template)

I-ARIF lives at `rasa_wiring_config.py` (5 modes: OFF/SHADOW/ENFORCE_CRISIS/ENFORCE_DISTRESS/ENFORCE_ALL). Live kernel state: `ml_floors_enabled:false, ml_method:heuristic, ml_runtime_ready:false, ml_hold_state:disabled`.

Flip point requires all 3 met:
1. `RASA_WIRING_ENABLED=1` opt-in (F13 SOVEREIGN)
2. SentenceTransformers dep available
3. Graphiti embedding runtime verified

Honest framing template for the user (do NOT echo the design-landed framing as if execution is imminent):

> "RASA lives at PHASE3_GATES_WIRED+TRL_DESIGN_LANDED, status 888_HOLD. The flip point is conditional on 3 things; 0 of 3 are met. Real verdict: no flip point achievable in current state."

See `references/i-arif-flip-point-2026-08-06.md` for the live wiring-config values and F2/F7/F13 binding statement.

## 7. FRAME / SIGNAL / arifFlow consistency probe (repeatable)

```bash
# SIGNAL chamber-count
ORGAN=$(yq '.components[] | select(.id=="signal").chambers | length' /root/AAA/federation/organs.yaml)
CODE=$(grep -c '^async def chamber_' /root/SIGNAL/src/signal_organ/chambers.py || true)
echo "SIGNAL: orgs.yaml=$ORGAN chambers vs code=$CODE"

# FRAME baseline floor defaults vs live arifOS values
curl -sf http://127.0.0.1:18085/frame/baseline | python3 -m json.tool | grep -A1 'f7_humility\|f8_genius'
curl -sf http://127.0.0.1:8088/health | python3 -m json.tool | grep -E '"F[0-9]+"|"L1[0-3]"'
# Default-matched FRAME baseline f7_humility.avg_omega: 0.04 == arifOS live F7=0.04, but the default is hardcoded; when kernel shifts, FRAME drifts silently.

# arifFlow invariants declared
grep -E '^A[0-9]\|^F[0-9]' /root/arifFlow/src/governance/invariants.rs | wc -l  # expect 12 (F0-F6 + A1-A6)

# Skill mesh probe (pattern #7) — append to the cross-organ consistency table
/root/AAA/skills/autonomous-ai-agents/arifos-control-plane-sot-audit/scripts/skill-mesh-probe.sh
```

## Pitfalls

- **Multi-SOT drift is the default, not the exception.** Every organ has ≥3 SOTs. When asked to "verify X matches Y," expect them to disagree. Cite live ground truth + the SOT that's regeneratable, don't try to harmonize n SOTs by hand.
- **Two parallel authority-ceiling vocabularies (6-band scale vs APEX §8 5-band scale).** If a sibling or A-FORGE contract says `ceiling: T3_888_HOLD` and organs.yaml says `authority_ceiling: DISPLAY_ONLY` for the same organ, that's two different vocabularies trying to express the same idea. **Map them, don't pick one.** Several ceilings in organs.yaml (`EDGE_AGENT`, `DISPLAY_ONLY`, `UI_EDGE`, `METABOLIZE_ONLY`, `ACTUATE_AFTER_LEASE`) have **no equivalent** in the APEX 5-band scale — these need either a separate role-descriptor field or a re-derived value.
- **Live-probe chamber counts lie.** SIGNAL `:18084` claims `all_6_chambers: active` per organs.yaml, but `signal_organ/chambers.py` only exports 3. FRAME `:18085` declares 6 chambers in organs.yaml but `frame_organ/main.py` exports 7 (`rsi_verify` added without YAML update). The "chambers active" claim is sourced from the in-code dict literal, which lies about its YAML state. **Probe the source-tree functions, not the YAML.**
- **Port collisions.** `organs.yaml` declares two organs on `:18084`: SIGNAL (port 18084, mcp_port 18084) and WELL-Witness (port 18084). Hermes is `:18086` in `organs.yaml::hermes.mcp_port` but `:18089` in `workspace.yaml::canonical_repos.hermes.port`. Always `ss -tlnp | grep :PORT` to see what actually binds — YAML disagreement doesn't mean an outage, just docs drift.
- **`aaa-drift-check.py` cannot catch cross-organ or cross-tree drift.** Don't promise "drift check passed" when the contradiction is cross-organ (or — verified 2026-08-08 — cross-tree across the skill mesh). The script is a complement, not a substitute, for federation-wide audit.
- **The "chamber 7" trap.** When an organ's source grows a new chamber/endpoint after `organs.yaml` was last updated, the YAML drifts. Don't trust the in-code `chambers` dict literal as proof of canonical registration — always grep `organs.yaml` for the chamber name.
- **RASA "design landed" framing is misleading.** Status `PHASE3_GATES_WIRED+TRL_DESIGN_LANDED` describes pre-deploy design completeness, not runtime enablement. Do NOT echo this as if execution is imminent. The 3-condition flip-point is the right framing.
- **A-FORGE stale SOT markers:** `last_verified` field dates `2026-07-01` (mcp_surface.yaml) and `2026-05-19` (tools.yaml) are the canonical "do not trust" markers. Any tool-count claim sourced from these files is by definition ≥ 29 days stale.
- **Runtime success hides A2A drift** (verified 2026-08-07): OpenCode subagents (333-AGI/555-ASI/888-APEX) route via inline `litellm-federation/{agi-333,asi-555,apex-888}` strings and work correctly. The A2A registry declares them as `virtual-agent` with **no `model:` field** — the gateway is blind. Always probe the consumer config AND the registry; never declare alignment from runtime success alone. See `references/fed-aaa-drift-2026-08-07.md`.
- **Skill mesh command at `-maxdepth 1` returns empty** (verified 2026-08-08). The canonical `find … -maxdepth 1 -name 'SKILL.md' | xargs grep '^version:'` command was specified for the mesh-sync protocol, but on this federation the skill directories nest one level deeper (`/root/AAA/skills/<skill>/SKILL.md`), so `-maxdepth 1` matches ZERO files. Use `-maxdepth 2` for a live comparison (281 SKILL.md bodies observed across the 3 trees). The `AUDIT-agent-skill-mesh` skill documents both the spec command and the operational variant; prefer the operational variant until the mesh is flattened.
- **Skill mesh placeholders are unparseable.** A few files use `version: semver`, `version: {semver}`, or `1.0.0-2026.07.06` date-suffixed strings. Treat those as **UNPARSEABLE → flag**, do not silently equate. `semver`/`{semver}` are linter placeholders, not real versions.
- **`skill_linter.py` schema is out-of-sync with the catalog** (verified 2026-08-08). The linter (`AAA/skills/skill-evolution/skill_linter.py`) requires 14 invariant-schema fields (`purpose`, `owns`, `refuses`, `cause_class`, `cost_class`, `tier`, `permissions`, `dependencies`, `precedence`, `conflicts_with`, `contract`, `reversibility`, `owner_organ`, `accountability`) that no skill in the catalog currently carries — `FORGE-mcp-probe` exits with the same 18 errors. The linter's `id` regex (`^[A-Z][A-Z0-9-]+$`) rejects lowercase, but every catalog skill uses lowercase kebab-case. `--all` mode crashes (`AttributeError: 'list' object has no attribute 'get'`). Lint is not a reliable gate for "did my new skill pass?" — when scope explicitly forbids contract-schema retrofit (parent spec only mandates `id`/`version`/`owner`/`risk_tier`/`autonomy_tier`), the right answer is "matches surrounding house style" + "self-dogfood: skill is discoverable by its own protocol", not "passes lint."

## Support files

- `references/contradiction-table-2026-08-06.md` — full 5-section ranked contradiction table from the session that produced this skill, with evidence paths and recommended fix approaches for each.
- `references/i-arif-flip-point-2026-08-06.md` — exact wiring-config contents, mode state, dep status, and the 3-condition flip-point recipe.
- `references/aaa-drift-check-scope-audit-2026-08-06.md` — line-by-line audit of what aaa-drift-check.py covers vs misses, with cross-references to scripts/source.
- `references/fed-aaa-drift-2026-08-07.md` — pattern #6 (FED alias ↔ A2A model-metadata drift). Trinity had no `model:` field in A2A, 3 phantom FED aliases (`asi-555-audio`/`asi-555-video`/`dispatch`) had no A2A registration, AGENTS_UNIFIED forge models were stale vs FED cascade. Runtime worked because OpenCode's inline `litellm-federation/*` references bypassed the broken A2A declarations. Plan saved at `/root/.hermes/plans/2026-08-07_114400-fed-aaa-a2a-zen.md`.
- `references/skill-mesh-divergence-2026-08-08.md` — pattern #7 (skill mesh divergence across AAA/Hermes/Kimi). Live mesh snapshot (281 SKILL.md bodies), the `-maxdepth 1` empty-output pitfall, placeholder-version unparseable cases, the `skill_linter.py` schema mismatch, and the `AUDIT-agent-skill-mesh` skill escalation protocol.
- `scripts/cross-sot-probe.sh` — one-shot script probing the FRAME/SIGNAL/arifFlow consistency row in §7 across `:18085`, `:18084`, and the arifFlow invariants file. Returns a "chamber count, organ tool count, dr fit count" table.
- `scripts/skill-mesh-probe.sh` — one-shot script probing pattern #7 (skill mesh SOT). Runs the `find … -maxdepth 2 | xargs grep '^version:'` command, classifies each row SYNC / DIVERGED / MISSING_FROM_X, and prints the "are my agents in sync right now?" summary line.
