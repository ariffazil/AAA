# ZEN 2026-09-04 — Hermes⇄AAA⇄Organ Skill Alignment + Learning Auto-Update

> Session SEAL-83defc585b5a4296 · 333-AGI · FQ=0.90 · Direction ratified by 888-APEX (SEAL, architectural coherence)
> Doctrine: **AAA = Canonical Catalog · Organ = Domain Owner · Mesh = Distribution · Agents = Consumers (mount, never own)**

## Entropy removed (all reversible — backup: /root/BACKUPS/skills-zen-20260903_195304Z)

| # | Defect | Fix |
|---|--------|-----|
| 1 | Repo-leak symlinks `capital→/root/WEALTH`, `geology→/root/GEOX` in Hermes tree (loader scanned whole organs) | removed (external_dirs covers organ skills) |
| 2 | 7 real-dir duplicates Hermes↔AAA (5 identical + 2 AAA-wins: forge-multimodal-router, token-plan-image) | Hermes copies archived, replaced with symlinks → AAA |
| 3 | `aaa-agentic-governance` misfiled in GEOX+WELL | homed to AAA, organ copies archived |
| 4 | 7 strays (`_drafts/`, `apple/`, `github/`, `apex_verdict_seal/`, `FORGE-mcp-jam-inspector/`, 2 loose .md) | archived |
| 5 | 13 broken mesh links | cleared (rollback log in backup); 0 broken remain fleet-wide |
| 6 | Organ skill dirs empty (WEALTH=0, GEOX≈0, WELL misfiled) | 15 domain skills forged |

## Organ-domain skills forged (16 ownership records)

- **GEOX (5)**: seismic-interpretation · well-log-qc · basin-evaluation · prospect-evaluation · claim-falsification
- **WEALTH (4)**: capital-primitives · ledger-discipline · market-pulse · runway-conservation
- **WELL (3)**: triadic-ops · machine-diagnose · consent-registry
- **AAA (3)**: musyawarah-execution *(the carry-forward wire — artifacts existed, behavior now too)* · skill-governor-runtime · agentic-governance (homed)
- **arifOS (1)**: eight-verb-canonical

## Mesh topology (verified)

| Mount type | Homes |
|---|---|
| Direct mount (=AAA/skills, 172 skills) | .agents · .claude · .opencode · .codex · .grok |
| Per-skill symlink mounts (12 organ skills each) | .kimi-code · .qwen · .openclaw · .gemini · .config/opencode |
| external_dirs (config-read) | Hermes → GEOX/WEALTH/WELL/AAA skills |

Broken links fleet-wide: **0**.

## Learning auto-update (sovereign directive: "skills auto-update when agents learn")

```
agent learns → .learning/queue/<atom>.json → cron hourly skill-learn-ingest.py
→ F2 gate (evidence REQUIRED) → canonical SKILL.md '## Lessons (auto)' + patch bump
→ instantly live in every mount home
```

- Protocol: `skills/SKILL_LEARNING_PROTOCOL.md` · Ingest: `scripts/skill-learn-ingest.py` · Cron: `/etc/cron.d/aaa-skill-learn`
- Proven end-to-end: first atom (333-AGI, arif_init OBSERVE_ONLY-notice lesson) MERGED ✓
- Idempotent (hash-dedupe), append-only (F4), evidence-gated (F2), F13 may purge any lesson.

## Contract standard (888-APEX gap #1)

Registry v3.0.0 now defines: **skill_contract** (frontmatter fields), **invocation_contract** (tool surface is SOT), **ownership_contract** (owner_org, NO owner_agent), **mesh_contract** (mount types). E3E divergence harness: `scripts/e3e_skill_mesh.sh` (emit prompts / tally divergence; ≥90% match = mesh works, <30% = decoration).

## Commits

AAA `5aaac5f0` · GEOX `f7aef0f4` · WEALTH `3d75f88` · WELL `bdc5f26` · HERMES `95879fd1`

## Awaits F13

1. AAA 16 dirty files = prior-session registry/constitution/reports work — not mine, not committed blindly.
2. `/root/.kimi` + `/root/.kimicode` stale twins of `.kimi-code` — recommend archive after review.
3. `/root/.gemini/skills` created fresh — verify gemini-cli actually reads the convention.
4. FLAME :18901 DOWN (pre-existing) — hermes_* free lane unavailable until revived.
5. E3E campaign: dispatch the 5 prompts to Claude/Kimi/Codex/Gemini/Qwen/Grok/OpenClaw via fi-mesh, tally divergence.
