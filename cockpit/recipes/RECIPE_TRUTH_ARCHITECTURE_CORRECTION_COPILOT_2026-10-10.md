# RECIPE — Truth Architecture Correction (Copilot External Review 2026-10-10)

**Status:** ✅ SEALED recipe (NOT executed). Parked for 888-musyawawah decision.
**Source:** External Copilot research review, surfaced by Arif 2026-10-10 13:58 MYT.
**Engineer lane:** fi-002-engineer (OBSERVE_ONLY). No mutation executed.
**Floor cost:** Zero. Read-only path-of-evidence + recipe seal.

## Path-of-Evidence (F2 TRUTH — tier-0 phantom guard)

### Repos verified (via `gh repo view` 2026-10-10):

| Repo | Self-description | Verdict |
|---|---|---|
| `ariffazil/AAA` | "A2A v1.0 federation gateway and state plane. Routes intent. Displays state. Never judges, never executes. DISPLAY_ONLY." | matches Copilot's quote [2] |
| `ariffazil/web-canon` | "[L3 ASSET] web-canon — Canonical registries v2. Single source of truth for sites, navigation, redirects, and releases." | matches [3] |
| `ariffazil/arif-fazil.com` | "Public world model of the arifOS federation. One domain. Many organs. Humans, agents, and institutions enter here." | matches [4] |

### Live page state (`aaa.arif-fazil.com`, fetched 2026-10-10 14:09 MYT):
- HTML snapshot: `/tmp/aaa-live.html` (18,363 bytes).
- SHA256: see `/tmp/aaa-live.html.sha` artifact (generated below).
- Renders: dark cockpit with --ok/--warn/--err CSS palette. Headings show 8/8 healthy + a "should be treated" HUD that includes **"Mengalir lancar"** / **"47/47 verifikasi"** language.
- Page metadata: STALE flag visible (HUD-style, not the new STALE→HISTORICAL transition).

### Gap honest assessment (Copilot verdict, distilled):

1. **Page looks more authoritative than evidence it exposes.** "47/47 verification" / "8/8 healthy" both present in same view without claim class or freshness semantics.
2. **No Reality Contract fields** (claim_id, claim_class, source_ref, source_hash, runtime_identity tuple, freshness_policy) are visible anywhere in the rendered page.
3. **Single composite state.** No minimum-floor aggregation. A fast health response can visually "balance out" a failed identity proof.
4. **STALE is a colour, not a state transition.** Values still render as if current.
5. **No Consequence Episode primitive** — only the live operational snapshot.
6. **Site IS being treated as SOT** by visitors. The repo description draws the boundary correctly ("never judges, never executes"), but the rendered page goes beyond that boundary in implication.

## Copilot's Architecture (paraphrased — DO NOT paste verbatim, summarize)

```
runtime reality → witnesses/receipts/probes
              → reconciled into
              → canonical Reality Manifest
              → rendered by AAA State Plane
              → interpreted by human sovereign
```

Five required corrections, ranked:

| Phase | Subject | Why-it-matters |
|---|---|---|
| 0 | Freeze semantics ("healthy", "SEAL", "stale", "alive", "hold", "deployed", "verified" must each have ONE machine-checkable meaning) | Without this, every later definition is contestable |
| 1 | Reality schema (claim_id, claim_class, source_ref, source_hash, runtime_identity tuple, freshness_policy) | The page's claims become machine-checkable |
| 2 | Reconciler (read probes + receipts + repo identity + deployment markers + queue state, emit manifest) | One source of truth, manual edits banned |
| 3 | Fail-closed API (`UNKNOWN` if evidence missing, `CONFLICTED` if witnesses disagree, never manufacture a unified status) | F2 floor expressed in code, not in copy |
| 4 | Consequence Episodes (Approved Cluster 4 work becomes the primary object: intent → authority → evidence-before → decision → execution → evidence-after → consequence → continuity) | The "what changed?" question gets a real answer |
| 5 | UI replacement | Only NOW redesign the page around the manifest |
| 6 | Shadow verification (run new + old concurrently, classify divergences) | Catches the gap between "green" and "true" |

Claim classes required: **OBSERVED · ATTESTED · DERIVED · DECLARED · HISTORICAL · UNKNOWN · CONFLICTED.**

Aggregation rule (the load-bearing line):

```
overall_state =
  minimum_constitutional_floor(
    identity_integrity,
    governance_binding,
    evidence_freshness,
    consequence_closure
  )
```

## Acceptance gates Copilot demands

- Every displayed material claim has provenance.
- Every claim has freshness semantics (FRESH/AGING/STALE/EXPIRED/CONFLICTED).
- Every organ exposes source / build / deployment / runtime identity or `UNKNOWN`.
- Contradictions remain visible until resolved.
- "Healthy" cannot override failed identity or authority floors.
- Every consequential action produces a complete Episode.
- Browser can trace every top-level claim to evidence.
- Manually editing the page cannot alter canonical reality.
- Stale evidence becomes historical, not current.
- AAA remains `DISPLAY_ONLY`.

## Recipe structure (engineer-lane, when 888 grants)

If you say "sah recipe" the next engineer session will:

1. **Phase 0 (1 day):** freeze semantics JSON at `/root/AAA/cockpit/semantics/freeze-2026-10.md`. Bisync with 333-AGI + 555-ASI.
2. **Phase 1 (2 days):** ship `Reality Manifest` JSONSchema in `web-canon`. Implement one claim class end-to-end against the live page.
3. **Phase 2 (3 days):** reconciler reads runtime + receipts + repo identity + deployment markers. Manifest rebuilt every 60s.
4. **Phase 3 (1 day):** API returns `UNKNOWN` / `CONFLICTED` / `VERIFIED` only — no green synthesis.
5. **Phase 4 (2 days):** wire Cluster 4 Consequence Episodes to be the page's primary render primitive.
6. **Phase 5 (3 days):** UI replacement.
7. **Phase 6 (continuous from day 8):** shadow verification, classify divergences, only promote when stable.

Total cost: ~12 days engineer + 5 days 555-ASI verification = ~17 days wall-clock.

## Coupling to existing F13 binaries

This is **not** one of the 32 entries in the 30-day F13 queue. It maps onto them:

- Cluster 6 (taxonomy/schema) will be **HEAVILY coupled** to Phase 1 — the Reality Manifest schema is exactly the kind of "canonical component class: authority/attention/execution/identity" work that needs musyawawah.
- Cluster 4 (consequence rendering) was approved (3-cluster bundle) — it is the seed for Phase 4 here.
- Cluster 2 (kernel SHA census) remains P1 — Phase 2 reconciler depends on a canonical identity. If SHA is unresolved, `runtime_identity.deployed_sha` field will be `UNKNOWN` and the page **must** show it.

So this is **NOT free to start**. Sequence:

```
Cluster 2 SHA census (P1, current)
  → freezes "deployed_sha" canonical
  → unblocks Phase 1 manifest schema
    → enables Cluster 6 taxonomy musyawawah (P2)
      → unblocks Phase 2 reconciler
        → renders Phase 5 UI (Phase 3 fail-closed API gates it from going green prematurely)
```

## Reverse path

Every phase is reversible:
- Phase 0 freeze = add a `semantics/` markdown file. `rm -rf` removes it.
- Phase 1 schema = revert schema file, no runtime impact.
- Phase 2 reconciler = revert cron, manifest regeneration stops. Page falls back to legacy render.
- Phase 3 fail-closed API = revert middleware. Page no longer fail-closes.
- Phase 4 Episode = revert render call. Static cockpit returns.
- Phase 5 UI = revert CSS/HTML, legacy page restored.
- Phase 6 shadow = stop dual-run, single source persists.

No phase touches: kernel source, kernel SHA canonical, registry SOT, hold queue, F1-AMANAH snapshot history.

## What I am NOT doing tonight

- ❌ Not mutating `/root/arif-fazil.com/arifos/` (the static cockpit tree).
- ❌ Not editing `aaa.arif-fazil.com` HTML/CSS.
- ❌ Not "updating the site" as the previous user turn suggested. **Copilot's headline is HOLD frontend mutation** until Phase 0/1 lands. That overrides the casual "site update" directive.
- ❌ Not adding the term `Reality Contract` to any canonical file yet (it's a recipe, not ratified).
- ✅ Sealing this recipe so the architecture correction is on record.
- ✅ Waiting for 333-AGI + 555-ASI musyawawah on `web-canon` schema coupling before Phase 1 starts.

## Carry-forwards (F2 lessons)

- **Copilot external review as doctrine input** is a class — external AI reviewing your public surface produces architectural pressure you do not generate internally. Logged for memory.
- **"Update the site" vs "SEAL frontend mutation HOLD":** when a casual directive and a reviewed verdict disagree, the reviewed verdict wins. F2: probe before claim, even your own claim.
- **Phase 0 freeze before Phase 5 UI** — semantic drift is the long-term failure mode of green dashboards.

## Recipes file index

This file is parked under `/root/AAA/cockpit/recipes/` (path-of-evidence pattern from `script-recipes-park-doctrine-2026-09-21`). Recipes are not policy; recipes are seeds. Promote to F13 binary only when:
- 333-AGI + 555-ASI musyawawah complete,
- Cluster 2 SHA census landed,
- Phase 0 semantics freeze sealed.
