# Skill Collision Census — v2 (2026-09-16)

> Owner: Hermes (ops-bridge) · Method: deterministic, declared-metadata only (no embeddings, no LLM)
> Script: `/root/work/skill-census/census2.py` · Machine output: `/root/work/skill-census/collisions-v2.json`
> Supersedes the *unmeasured* "28% trigger collision" figure quoted in
> `FI_CODING_MESH_2026-09-16.md` §8. That number was a model self-report, not a census.

## Why v2 exists (sensor scar, 4th instance in 24h)

v1 of this census returned a fake collision cluster: 95 "colliding" skills that all paired with
`claude-agentic-state` / `claude-meta-mesa` / `delta-omega-psi-multimodal-cognition`. Cause: those
skill `description:` fields begin with federation routing metadata —
`> [fed: tier=… floors=[F1, F2, …]]` — and the trigger extractor tokenized that metadata as if it
were the trigger clause. Every fed-tagged skill therefore "shared" the tokens `fed`, `tier`,
`floors`. **A probe that reads the label measures the label.**

v2 strips leading `[fed: …]` bracket metadata before trigger extraction. Same scar class as
`find` vs `find -L` (this session's earlier false-empties): **dereference, and de-metadata, before
measuring.**

## Measured state (v2, de-metadataed)

| Metric | Value |
|---|---|
| SKILL.md files across 6 surfaces (`os.walk(followlinks=True)`) | 1,631 |
| Distinct skill names | 573 |
| Identity collisions (one name → ≥2 distinct realpaths) | **117** |
| └ attributable to AAA ↔ hermes mirror twin | 71 |
| └ genuine (cross-harness or same-tree duplicates) | **46** |
| Case-only twins (e.g. `ASI-agent-invariants` ↔ `asi-agent-invariants`) | 10 |
| Trigger-collision skills (≥3 leading trigger tokens shared with another owner) | **182 / 573 = 31.8%** |

Per-surface file counts: AAA 510 · qwen 535 · hermes 409 · kimi 131 · opencode-overlay 31 · gemini 15.

## The two defects are different and must not be merged

**Identity collision** — one concept, two artifacts. Fix = canonicalize / supersede / alias.
Genuine examples (46):

- `AAA/skills/FORGE-onboarding/claude` vs `AAA/skills/forge-onboarding/agent-onboarding` (same tree, same name)
- `.kimi-code/skills/forge-mcp/FORGE-mcp-testing` vs `AAA/skills/domains/general/forge/mcp-ops/FORGE-mcp-testing`
- `.qwen/skills/youtube-extraction-datacenter-ip/youtube-extraction-datacenter-ip` — nested dir-in-dir **ghost**
- `apex_verdict_hold/{hermes,claude}` vs `apex_verdict_seal/{hermes,claude}` — 4 files, 1 declared name
- overlaid copies of `google-workspace-gws`, `human-state-estimation`, `malaysia-reality-interface`,
  `mcp-shopping-list-2026-09`, `asi-agent-invariants` in `.qwen/skills` (qwen shadows canonical)

**Trigger collision** — genuinely different capabilities claiming the same request phrase.
Fix = disambiguate ownership conditions. Real clusters after de-metadataing:

- **brand × variant matrix** — `claude|qwen|kimi|opencode-agentic-state` ↔ `*-meta-mesa` ↔ `*-zen-router`
  (6 files, 3 capabilities, brand as parameter — HOLD confirmed correct, cross-agent blast radius)
- `forge-act-federation-ingress` ↔ `forge-sct-federation-ingress` (act vs sct — should discriminate)
- `forge-mcp` ↔ `forge-mcp-lifeguard` ↔ `forge-fastmcp` ↔ `forge-mcp-testing`
- `hermes-claude-code-spawn` ↔ `openclaw-claude-code-spawn` ↔ `aaa-musyawarah-execution`
- `web-search` / `web-scrape` ↔ the agentic-architecture cluster

## Existing-owner proof (why no new router skill was minted)

Before proposing any selector, the existing owners were read:

| Candidate owner | What it actually owns | Verdict |
|---|---|---|
| `/root/AAA/scripts/aaa_capability_loader.py` | capability registry of **services/backends** (MCP/tool backends, authority_mode, rank) | not skills — cannot absorb |
| `/root/AAA/registry/routing/identity_resolver.py` | **identity-bound capability** gate (T2I/voice-clone/biometric; "abang sado" class-name HOLD). SCAR-2026-09-15-001 | not skill routing — cannot absorb |
| `/root/scripts/skills-census.py` (cron `37 4,10,16,22`) | skill **inventory** → registry `disk_reconciliation` block. Functions: `scan`, `census`, `write_registry` only | inventory only, no selection — **cannot absorb** |
| `/root/AAA/registry/duplicate-graph.json` (205 KB) | duplicate graph, pre-existing | inspection artifact, no decision contract |

Conclusion: **no existing owner absorbs skill selection.** The gap is real. The correct next build is
a *selection contract* (derived metadata + deterministic filter ladder), not a router agent and not a
new "Skill Router" skill.

## Proposed contract (deterministic first, model resolves only the last mile)

```
intent
  → consequence class + authority tier        (existing envelope machinery)
  → domain filter            (derived: skill path band)        573 → ~N_domain
  → authority filter         (derived: owner band / risk_tier)  → ~N_auth
  → health/host filter       (mesh-health SOT)                  → ~N_live
  → intent candidates        (trigger index, collision-aware)   → 2–5
  → model resolves the last mile                                → 1
```

Metadata must be **derived** by the census (brand prefix, path band, declared risk_tier), never
hand-written across 573 files. Identity collisions collapse first (one owner per capability, brand
as parameter) or the trigger index inherits the duplicates.

## Kill criterion

If a derived index cannot separate the 182 colliding skills into ≤5 candidates on a real intent
query with the model's last-mile pick — the index is decoration. Measure before claiming it works.
