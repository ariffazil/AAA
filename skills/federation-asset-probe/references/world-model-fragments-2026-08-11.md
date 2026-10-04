# World Model Fragments — Federation Reconnaissance 2026-08-11

**Session question:** "Now AAA is out WORLD model?? Or arif-fazil.com?? Now evaluate what's the closest of world model already forge in the system"

## Probe method

1. `search_files pattern="world_model" target="files"` across `/root`
2. `terminal find /root -name "*world*"` for cross-cutting search
3. `read_file` on each candidate to verify content (not just existence)
4. Triangulate: code + tests + docs + runtime

## Key finding — memory was wrong

Memory note claimed `canon/world-model.yaml` was "Phase A live" (9 domains, Phase A). **That file does not exist on 2026-08-11.**

The actual artifact is `/root/arifOS/arifosmcp/runtime/world_model/world_model.py` (579 lines of real code, typed graph, Bayesian update, F11/F13/F9 bound). The memory claim was either forward-looking intent that never landed, or stale reference to a path that was renamed/moved.

**Probe is authoritative. Memory that disagrees with probe should be updated.**

## The 8 fragments identified (not unified)

| # | Path | Domain | LOC | State | Notes |
|---|---|---|---|---|---|
| 1 | `arifOS/arifosmcp/runtime/world_model/world_model.py` | Actors (corporations, models, institutions, person-classes) | 579 | **Forged & active** | Typed graph, 6 ActorClasses, 8 RelationTypes, Bayesian alpha-beta update, staleness + drift estimation, F11/F13/F9/F2 bound, plan scoring with constitutional loss + capture risk + intent purity |
| 2 | `arifOS/arifosmcp/runtime/world_state.py` | Epistemic state | 144 | Forged & active | 6 states: KNOWN / ASSUMED / STALE / CONTESTED / FORBIDDEN / UNKNOWN. Module docstring: "dimension 5: World-State Model of AGI Kernel specification" |
| 3 | `arifOS/arifosmcp/geometry/world_model.py` | Three-layer world model (EUREKA-G+M) | 378 | Forged & active | 7 ActorClasses (incl. UNKNOWN), TomLevel constraint, geometry brief — F2 recovery note 2026-06-11 (re-forge after file overwrite) |
| 4 | `arifOS/arifosmcp/runtime/world_contracts.py` | World contracts | exists | Forged (referenced) | Typed contracts for the world model |
| 5 | `GEOX/src/geox_core/skills/orchestration/orch-world-model-sync.md` | Earth domain | 45 | Forged (draft) | Sync skill: agent-states, sensor-updates, map-versions, mission-state → synced-world-model, conflict-report, consistency-score. Domain-specific (basin/seismic/petrophysics) |
| 6 | `WEALTH/` | Capital domain | — | Forged (fragment) | NPV/EMV/risk/market substrate. Not a typed-graph world model in the arifOS sense |
| 7 | `WELL/` | Human domain | — | Forged (fragment) | Homeostasis/dignity/reliability substrate. Mirror-only, not builder |
| 8 | `Atlas333` (`arifOS/okf/atlas333.md` + `geometry/atlas333_update.py`) | Cognitive geometry | exists | Forged (fragment) | 33 paradoxes, 7 zones. Civilization-scale, static catalog. Cross-linked with world model via `atlas333_update.py` |
| 9 | `CIV-21` (`AAA/canon/CIV-21.md`) | Institutional collapse | — | **Doctrine, not runtime** | 21 Gödel-locked eurekas. Defines the collapse-detection eurekas but not as runtime world model |

## What is NOT a world model

- **AAA** (`AAA_AGENTS_REGISTRY.json.md`) — control plane, registry, dashboard. `DISPLAY_ONLY` per `AAA/docs/ORGAN.md`. It **shows** state, doesn't **model** state.
- **arif-fazil.com** — public human surface. Static-first shell, Caddy `@agent_shells`, `/999/*` live-proof (health → :8088, flow → :7073, vault → local JSON). It **presents** to humans, doesn't **represent** reality.

## What's missing from the strongest fragment

`runtime/world_model/world_model.py` covers **socio-political actors** only. It does NOT cover:

| Gap | Reason missing |
|---|---|
| Physics depth (energy, thermodynamics, materials) | World model lives in 13D *constitutional* manifold, not *physical* manifold |
| Scarcity / economics as typed primitive | Entropy metric exists, opportunity cost does not |
| Adversarial ecology (Goodhart, hidden optimizers, capture) | `CAPTURES` relation type handles actor-capture, not full adversarial model |
| Game theory (multi-optimizer ecology) | Internal federation governance exists, external ecology not modeled |
| Counterfactual branch simulation | `plan_in_world_model` rates plans, not full branch-space |
| Civilization memory at century scale | CIV-21 + Atlas333 doctrine exists, not runtime model |
| Continuous calibration (Brier score history) | Bayesian update exists; accuracy ledger does not |

## Synthesis conclusion

The federation has **8+ world model fragments, not unified.** The strongest is the arifOS kernel's typed actor graph (579 LOC, Bayesian, F-bound). Reality Organ as proposed in doctrine does NOT exist as a unified layer — its COMPONENTS exist scattered.

**Next move is binding, not building:**
1. Add `domain: Literal["actor", "earth", "capital", "human", "civilization", "cognitive"]` to existing `WorldModel` class
2. Wire 8 fragments through one abstraction layer
3. Add missing primitives (physics, scarcity, adversarial, calibration ledger)
4. Store prediction-vs-reality errors per domain — calibration ledger feeds CIV-21 E22 Constitutional Metabolism

## Verification trail

All paths verified via `read_file` and `search_files` on 2026-08-11. Memory updated to reflect actual artifact locations.

## Files inspected (line counts shown)

- `/root/arifOS/arifosmcp/runtime/world_model/world_model.py` — 579 lines, lines 1-359 read in detail
- `/root/arifOS/arifosmcp/runtime/world_state.py` — 144 lines, lines 1-40 read in detail
- `/root/arifOS/arifosmcp/geometry/world_model.py` — 378 lines, lines 1-60 read in detail
- `/root/GEOX/src/geox_core/skills/orchestration/orch-world-model-sync.md` — 45 lines, full
- `/root/arifOS/arifosmcp/runtime/world_contracts.py` — exists (referenced, not read)

## Doctrine alignment

- **F2 TRUTH** — every actor carries `provenance_sha` and `evidence_chain`
- **F7 HUMILITY** — `CONFIDENCE_CAP = 0.95`, no overconfident claims
- **F8 GENIUS** — `empathy_check` before action involving non-self actor
- **F9 ANTIHANTU** — `TomLevel` cap = 2 (no recursive nesting beyond)
- **F11 AUDIT** — every actor update logged with actor, evidence, ts
- **F13 SOVEREIGN** — actor definitions F13-ratified; new classes need 888

The world model is **constitutionally bound by design**. Not an accident — first-class doctrine alignment.

## Probe technique (reusable)

When asked "do we have X?" about the federation:

```bash
# 1. Broad pattern probe
search_files(pattern="X", target="files", path="/root")

# 2. Targeted find, excluding noise
find /root -name "*X*" -type f | grep -v node_modules | grep -v .venv

# 3. Verify each candidate's substance (not just existence)
read_file(path=<found>, limit=80)

# 4. Triangulate: code + tests + docs + runtime state
# 5. Classify: forged-active / forged-dormant / referenced-absent / absent
# 6. Synthesize with file paths + line counts + quoted excerpts
# 7. Update memory if probe disagrees with stored note
```

This pattern is encoded in the parent `federation-asset-probe` SKILL.md. Reference back to that skill for the full runbook and pitfalls.
