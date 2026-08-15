# FED Actor-Envelope Doctrine

> Ratified F13, 2026-08-15. Verdict: **"A externally, B internally."**
> Canon sentence (F13, 2026-08-15): **"State is no longer topology."**
> Companion SOT: `fed_signatures.yaml → actor_geometry` (cascades live there, not here).
> Parent: ACTOR_SURFACE_DOCTRINE (`/root/forge_work/2026-08-15-runtime-geometry/`).

## The geometry

```
Human
   ↓
Picker          — WHO:   agi-333 · asi-555 · forge-777 · apex-888
   ↓
arif_route 444  — HOW:   envelope resolves
   ↓                     ├─ Memory (L1–L6 / Helix)
Envelope                ├─ Modality (auto-detected)
                        ├─ Context budget
                        └─ Capability (plan|generate|inspect|repair)
   ↓
Resolver        — WHAT:  cascade member by live route_health
   ↓
Surface → Model → Provider
```

- 000 and 999 are **structure, not labor** — never in the picker.
- Old 26-group surface collapses to 4 actor entries + envelope. Capability/modality/memory lanes are request attributes, not picker nouns.

## Falsifier (the one test)

> **Next model release = 1 SOT edit (`fed_signatures.yaml → cascades`), 0 picker edits.**
> If the picker changes on a model release, the geometry failed, not the model.

## Zen eurekas (distilled from i-ARIF SWOT + external audit, 2026-08-15)

- **E1 — Cognition is metered, identity is owned.** The harness "rents" intelligence; the picker names the actor, so no model identity can leak into topology. Rented cognition stops being drift risk the moment nothing in the picker names a model.
- **E2 — Memory is an envelope, not a lane.** Saturated context (97%) and a 26-entry picker are the same disease: state promoted into topology. Cure: both ride the request envelope.
- **E3 — FED is model-blind by constitution.** An agent cannot audit itself with the apparatus that contains its blind spots (SWOT double-helix paradox). FED is the *outside* of that loop — but only while it runs on none of the models it judges. Audit independence (Gödel E3) is enforced structurally in cascade provider sets, not by discipline.
- **E4 — Live probes are the only auditor.** Static notes gate nothing. `route_health` + `token_bank` demote at runtime. (Scar: MiniMax config said EXHAUSTED while FED DB said FRESH — notes drifted, probes didn't.)
- **E5 — Fail-closed is equilibrium.** Sovereign offline ⇒ system degrades to HOLD, never chaos. Proven by KRT-JOHOR 2026-08-15: the restraint layer held even while the judge layer was unreachable.

## Guardrail (internalized)

No safety lives in vendor configs. BLOCK_NONE everywhere the vendor allows it; the constitution is the safety layer:

| Layer | Rule |
|---|---|
| Kernel | F1–F13 floors; SCT required for MUTATE-class calls |
| State | carry_forward + token_bank + route_health = live truth |
| Actuator | all mutations route through A-FORGE lease; forge-777 chat is propose-only |

## Stages

- **Stage 1 (done 2026-08-15):** picker pinned to 4 actors (`opencode.json`), `forge-777` group added to litellm, this doctrine + `actor_geometry` SOT sealed. All legacy groups intact — zero caller breakage.
- **Stage 2 (before kill-date 2026-09-15):** alias map wired into `fed-aware-middleware :4010`; legacy litellm groups (hermes-asi, i-arif-qualia, fed-*, zai-pro, gemini-*, mirrors) deleted after caller verification; dead rows (insolvent deepseek, stale order-99) swept.

*Folder bukan diberi — geometri ini dimeterai, bukan dicadangkan.*
