# SKILL MESH — VERIFIED CONFLICT REGISTER (inode-deduped)

> **Status:** receipt, not doctrine · **Derived:** 2026-09-16 ~14:00 MYT · **Method:** `os.stat` inode dedup across 4 roots + `difflib.SequenceMatcher` pairwise on physical-distinct files.
> **Why this file exists:** a sibling session reported "598 files / 524 names / 75 duplicates / 4 true conflicts (sovereign-recognize, agi-decisions-reflect, fi-mesh-check, forge-context-compressor)" and "the quartet resolves uniquely." Those numbers are contaminated. This is the re-derived count. *"A count that has not been re-derived from source is a rumour"* — hermes-rasa.md §15.

## 1. The corpus, deduped by inode

`/root/.agents/skills` is a **symlink** to `/root/AAA/skills`; `/root/HERMES/skills` shares **inodes** with `/root/.hermes/skills`. Counting all four roots double-counts every mirrored skill. That is the source of the inflated numbers (412 / 598 / 555 all appear in circulation; they are the same corpus at different scope).

| Measure | Value |
|---|---|
| physical SKILL.md files (inode-deduped) | **593** |
| unique skill names | **555** |
| names that are pure symlink mirrors (1 physical file) | 518 |
| names with **>1 physically distinct file** | **37** |

Of the 37: **4 are true conflicts** (similarity < 0.70), ~13 are partial/drift (0.86–0.99), ~20 are sim=1.0 identical-content-different-inode (pure mirror noise, not even drift).

## 2. The four TRUE conflicts (sim < 0.70) — the only real owner work

| skill | sim | sizes | note |
|---|---|---|---|
| `sovereign-recognize` | 0.03 | 1146 b vs 5582 b | two different skills, one name. `~/AAA/skills/reflective/` vs `~/AAA/skills/domains/general/aaa/substrate/reflective/` |
| **`APEX-humility-godel`** | **0.04** | **3115 b vs 2882 b** | **two different skills, one name — and this is the sibling's OWN Owner 3.** `.hermes/...` (5-reflex protocol) vs `AAA/...` (quartet "Owner 3" card) |
| `claude` | 0.05 | 10767 / 10767 / 5780 | three files; two identical, one is a different `FORGE-onboarding/claude` |
| `fi-mesh-check` | 0.46 | 5011 b vs 2545 b | `.hermes/` vs `AAA/` |

**The sibling's list was wrong on 2 of 4.** It named `agi-decisions-reflect` and `forge-context-compressor` as conflicts — both are **sim = 1.00** (identical copies = mirror, not conflict). It **missed** the two that matter: `APEX-humility-godel` and `claude`.

## 3. The load-bearing correction: the quartet does NOT resolve uniquely

Sibling claim: *"Now keempat-empat owner resolve unik."* Measured:

| Owner | resolves uniquely? |
|---|---|
| 1 `hermes-rasa-doctrine` | ✓ 1 physical copy |
| 2 `audience-scoped-disclosure` | ✓ 1 physical copy |
| 3 `APEX-humility-godel` | ✗ **2 distinct copies, sim 0.04** |
| 4 `disclosure-advisory` | ✓ 1 physical copy |

**3 of 4.** Owner 3 is two-headed: a `.hermes` copy (the original 5-reflex self-critique protocol) and an `AAA` copy (a newer "Owner 3 of the quartet" card). A choke point cannot be two different skills wearing one name — routing to "APEX-humility-godel" is ambiguous today. This must be reconciled **before** it can serve as the quartet's self-correction owner.

Sibling byte sizes also drift from disk (claimed rasa-doctrine 5055 b / actual 5475 b; audience-scoped 6355 b / actual 7592 b; APEX 3096 b / actual two copies 3115+2882 b). Minor, but it shows the report was not a clean single read.

## 4. What is CONFIRMED true from the sibling relay

- **WELL REGISTRY_DRIFT — live-verified this session:** `well_registry_status` returned intended=10, registered=40, exported=19, callable=10, unexpected_public=9, verdict REGISTRY_DRIFT, authority ADVISORY_ONLY, final_authority ARIF. The relay reported these exact numbers. Honest.
- **`well_system_registry_status` vs `well_registry_status`** name divergence: plausible (blueprint surface ≠ runtime surface); not independently re-tested here.
- The drift-vs-conflict **frame** is correct and useful. The **process** (subtract one, stop, don't mass-delete) was right. Only the **counts** are contaminated.

## 5. Self-finding — the rasa MCP is already in Artifact C's bloat trap

Artifact C (MCP translation) warns: converting skills into many MCP tools = `SkillBloat → ToolSchemaBloat`; the surface should be ~5 conceptual verbs (discover/retrieve/validate/analyze/adjudicate), not dozens of overlapping ones.

Measured on the rasa MCP hardened this session: **9 tools at 13:33 → 23 tools now**, server.py 22,151 b → 43,904 b. 23 `hermes_*` verbs vs ideal ~5 = **460% of the recommended surface.** Several overlap (`hermes_shadow_map` / `hermes_paradox_map` / `hermes_discrepancy` / `hermes_counterstory` / `hermes_agent_shadow` / `hermes_projection_guard`). By Artifact C's own law this surface should collapse to a handful of conceptual operations with doctrine behind MCP **resources**, not 23 always-listed tool schemas.

## 6. Open decisions (T2 — touch other agents' skills; not executed without F13 naming them)

1. **`APEX-humility-godel`** — which copy is canonical? Pick one, the other becomes a pointer-stub. Blocks Owner 3 from being a real choke point.
2. **`sovereign-recognize`** — same: 1146 b stub vs 5582 b full. Pick the owner.
3. **`claude`** (3 files) and **`fi-mesh-check`** (2 files) — reconcile or scope-rename.
4. **rasa MCP 23→~6 verbs** — collapse to conceptual surface per Artifact C, doctrine to resources. Large, staged, not tonight.

The ~33 drift/mirror entries are a **sync** problem (one reconcile pass), not an owner problem — but the count is ~33, not the 48/96 the relay implied, because most "duplicates" are the same inode behind a symlink.

DITEMPA BUKAN DIBERI ⚒️

---

## ADDENDUM (2026-09-16 ~14:45) — the live tool surface vs the v1.1 canon audit

Verified over the MCP wire (`tools/list` against the running `hermes-rasa` server), not from source:

| Layer | Count | Source |
|---|---|---|
| live tools on the wire | **23** | `tools/list` runtime response |
| `@mcp.tool` decorators in server.py | 23 | source |
| tools the v1.1 canon ownership-audit accounts for | **12** | `hermes-v1-canon.md` §"Canonical Tool Surface" (8 distinct + 3 ambiguous + paradox_map) |

The relayed design note reasoned about **"12 live HERMES tools."** That 12 is the *audited subset*, not the live surface. **11 tools are on the wire and absent from the canon's ownership ruling:**

```
hermes_counterstory   hermes_qualia_boundary   hermes_shadow_provenance
hermes_projection_guard   hermes_context_split   hermes_rasa_hold
hermes_human_revision   hermes_uncreated   hermes_agent_shadow
hermes_cross_layer_check   hermes_adjudicate_claim
```

This is a **layerless count** — conflating the design layer (12 audited) with the runtime layer (23 callable). It is exactly the error the same artifact's new rule **UL-009** (`Count(value, layer, timestamp)`) forbids. The canon is self-consistent in prose and inconsistent with its own runtime.

**Consequence:** the v1.1 ruling "Internal capability ⇏ Public tool / SemanticOwnerAmbiguity → 0" cannot be satisfied while 11 live tools sit outside the audit. Either the audit is extended to all 23, or those 11 are withdrawn from the public surface. Until one happens, the surface is 23 tools regardless of what the canon says — and Artifact C's `ToolSchemaBloat` warning (it prescribed ~8 tools, ~6 prompts, a resource graph) is live and unmet: **23 tools, 0 prompts, 0 resources, 0 `hermes://` URIs.**

**What IS confirmed good in the v1.1 canon:** the etymology overclaim I patched (Rasa "never split"/qualia "residue") was folded into §"v1.1 Corrections"; the SEP-sourced Lewis 1929 attribution checks out; the dual law (`ActivateCapabilityMinimally` / `RetainHumanDataMinimally`), the `ε_qualia` logical-not-scalar guard, `ProfileCompleteness=forbidden`, and `Signal ≠ Diagnosis / Priority ≠ Authority` are sound and need no change.

DITEMPA BUKAN DIBERI ⚒️
