---
id: fi-mesh-check
name: fi-mesh-check
version: 1.0.0
description: "Probe all FI coder CLIs live (qwen/kimi/opencode/codex/claude/grok/gemini) with a minimal falsification prompt and report the mesh matrix. Use when Arif says 'mesh check', 'test all coder CLIs', 'FI mesh health', 'are all harnesses alive', or before/after cross-FI plumbing work."
owner: 333-AGI
risk_tier: low
floor_scope: [F2, F4]
---

# FI Mesh Check — falsification probe

Probe every FI coder CLI in the federation with a minimal falsification prompt. For each: run the CLI's one-shot mode asking it to reply with an exact marker string, capture output tail, and classify **PASS / FAIL / EXTERNAL**.

## Current invocations (verify against disk before trusting — these drift)

- Kimi: `kimi -m zai-coding-plan/glm-5.3 -p "Reply with exactly: KIMI-MESH-OK"`
- OpenCode: `opencode run --model litellm-federation/forge-777 "Reply with exactly: OPENCODE-MESH-OK"`
- Codex: `codex exec --skip-git-repo-check "Reply with exactly: CODEX-MESH-OK"` (goes through :4010 middleware)
- Grok: `grok -p "..."` (402 = balance exhausted → EXTERNAL flag, not a mesh defect)
- Gemini: `GEMINI_CLI_TRUST_WORKSPACE=true gemini -p "..."` (429 = quota → EXTERNAL)

## Rules

- Timeout each probe at 90s; one retry only for transient network.
- **Never mask an error as pass. One marker mismatch = FAIL.** A CLI can exit 0 while printing no marker (codex prints OTel DEBUG and the marker may not land in `tail -6`) — always `grep` the full output for the marker, never trust the last lines or `rc`.
- Classify external billing/quota failures (402/429) separately from mesh defects — EXTERNAL ≠ FAIL.
- **Money-gated states flip within minutes.** 2026-09-16: a manual `grok -p` returned 402 balance-exhausted at 03:22:56Z while the sentinel marked grok PASS at 03:25:14Z. Two probes two minutes apart disagreed. Report the conflict as a money-boundary, not as "alive" or "dead" from a single sample.
- Probe the correct layer before claiming absence: 401 on a health endpoint = service UP (auth-gated); conn-refused/timeout = DOWN.
- When a CLI reports "high demand" / load errors, probe its endpoint directly — middleware faults masquerade as vendor load (scar: :4010 responses-path, 2026-08-21).

## FI identity — do not escalate numbering to the sovereign

**FI-007 = Grok Build. FI-010 = Gemini CLI, DECEASED (F13 2026-09-13); slot vacant.**
SOT: `/root/AAA/registries/forge_instruments.yaml` (self-declared live registry). Corroborated by
`a2a-server/scripts/seed-agents.js`, the grok-build agent card, and `AGENTS_UNIFIED.yaml`
("No agent claims FI-009 or FI-010"). The stale satellite `docs/agent-skill-binding-map.md`
(grok→FI-010) is 2026-08 schema and now carries a STALE banner.
Rule: an FI-number conflict is a **provenance** problem, not a sovereign question. Find the
canonical owner, trace which assignment superseded which, return RESOLVED — escalate only if two
equally authoritative sources disagree. Resolution receipt: `FI_CODING_MESH_2026-09-16.md` §9a.

## Collision census (skill library) — method fixed 2026-09-16

When asked about skill count / duplication / "trigger collisions":

- **Dereference every tree** (`find -L` / `os.walk(followlinks=True)` / `realpath`). A probe that
  reads the symlink measures the map, not the territory. Fourth sensor-scar occurrence in 48h.
- **Strip metadata before measuring triggers.** Skill descriptions embed `[fed: tier=…, floors=[…],
  auto=…, risk=…]` and the bracketed form contains `]`, so a naive `\[[^\]]*\]` strip leaves
  `auto=T1, risk=low]` behind and manufactures fake collisions. Filter by document frequency
  (>8% of all descriptions) as well.
- **Key identity on the frontmatter `name`/`id`**, not the directory basename — the router keys on
  the declared identity, and nested sub-skills share a basename with their parent.
- **Separate the three classes:** (1) loader alias symlink (one owner + alias — NOT a collision),
  (2) brand-variant family (`claude-/qwen-/opencode-` × one capability — legitimate scope, brand as
  parameter), (3) genuine multi-owner duplicate (two real directories, one capability). Only (3) is
  a defect.
- Measured 2026-09-16 over 698 distinct skills / 5 surfaces: **identity duplication 115 groups /
  260 skills (37%)** — overwhelmingly harness-local mirrors of canonical AAA skills — and
  **trigger collision 26 pairs / 22 skills (3.2%)**. The widely-cited "28% trigger collision"
  does NOT reproduce; treat it as a measurement artifact.
- Re-runnable: `/root/forge_work/skill_collision_{census,pass2,pass3}.py`.
- **Before building any selection layer, prove no owner exists.** `/root/arifOS/core/capability_index/`
  ingests tools + MCP only (zero skill ingestion) — so the gap is real; extend that one index rather
  than minting a "skill router" agent.

## Output

End with the matrix table (FI × verdict × latency × note) + any root-cause fix performed. Root-cause fixes go to the responsible FI lane, not self-assigned cross-lane edits.
