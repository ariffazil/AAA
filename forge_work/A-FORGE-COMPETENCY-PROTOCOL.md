# A-FORGE ↔ AAA Competency Protocol v1 — Task Index

> Compiled 2026-10-01 by FI-008 · session: distraction cleanup + protocol v1
> Status: WIP — auto-executed in order; F13-class binaries preserved

## Architectural correction (in this turn)

Previous mistake: `AFORGE_CAPABILITY_MAP.json` was hand-maintained. Arif's correction: don't store another map, **compile the WARGA view from existing machine truths**. So:

```
C_warga = C_live ∩ C_affordance ∩ C_kernel ∩ C_authority
```

WARGA_AFORGE_VIEW is a projection, not a stored artifact.

## Compiled task list (priority order)

### T0 — Architectural correction (this turn)
- [x] Identify the hand-maintained-vs-projection mistake
- [x] Repurpose AFORGE_CAPABILITY_MAP.json → AFORGE_VERB_SCHEMA.json (just verb shapes, no tool bindings)
- [x] Build the generator script (`scripts/aforge_warga_view_generator.py`)
- [x] Run generator → `state/aforge/warga-capabilities.json` (the projection output)

### T1 — Competency state schema
- [x] `instructions/aforge-competency-schema.md` — 5 dimensions: identity / citizenship / aforge_competency / trust / active_authority
- [x] Sample state `state/aforge/competency/FI-008-kimi-code.json` — initial state reflects honest E2-E8 = PENDING

### T2 — Competency eval suite (8 evals, per Arif's E1-E8)
- [x] `instructions/aforge-competency-evals.md` — E1-E8 documented
- [x] First harness `tests/aforge-competency/test_E1_inspect.py`

### T3 — Update citizenship binding
- [x] `ROOT_AGENT_CONFIG.yaml::forge_citizenship_contract` updated to reference generator + schema + state
- [x] `AGENTS.md` table row added

### T4 — F13-class binaries (BLOCKED — pending Arif ratification)
- [ ] 7 verb names — `forge_inspect / plan / change / run / verify / extend / control` (DRAFT_AWAITING_F13)
- [ ] Promotion criteria — `RepeatedUse ∧ IndependentSuccess ∧ SelectionAdvantage ∧ LowScarPressure ∧ NetAttentionGain`
- [ ] Competency eval threshold — pass-rate per eval
- [ ] Failure-degradation policy — degraded competency ≠ citizenship revoked

### T5 — From earlier conversation (still pending)
- [ ] **Verifier ownership** — CODE_VERIFY independent judge (A-FORGE cannot be its own judge per Canon #1)
- [ ] **Substrate stability probes**:
  - [ ] arifOS verdict envelope divergence (L13 hold)
  - [ ] WELL machine reliability (I/O pressure, swap, faults)
  - [ ] forge_ephemeral templates=0 instantiations (why unused?)
  - [ ] WEALTH MCP timeouts
- [ ] **Mail entry fragmentation** — gws vs mailread (one should be folded)
- [ ] **Federation-wide compression audit** — GEOX (26 canonical but connector 1), WELL (40→10 in progress), HERMES (15 OK), arifOS (8 OK)
- [ ] **Patch-proposals backlog** — proposals/ has 15+ files, no triage dashboard
- [ ] **The 10-step A-FORGE program**:
  - [ ] Step 2 capability ontology over all 122 tools
  - [ ] Step 5 ephemeral CODE_INTEL/CODE_EDIT/CODE_VERIFY
  - [ ] Step 6 world-model dataset 22→100 trajectories
  - [ ] Step 7 selection credit instrumentation
  - [ ] Step 10 recursive self-improvement (depends on all above)

### T6 — Distraction follow-up (from earlier turn)
- [ ] Compress `.distraction-archive-2026-10-01/` (432M) to tarball — only if Arif confirms nothing needed

## Architectural truth chain (final form)

```
declared → callable → competent → verified
```

Each transition requires evidence:
- declared: agent card says so
- callable: runtime allows it
- competent: eval suite passes
- verified: real task completion independently witnessed

## Identity separation (canonical)

```
Identity          ≠  Citizenship      ≠  Trust            ≠  Competency      ≠  ActiveAuthority
(kimi-code FI-008)   (warga-aaa)        (scar count)        (E1-E8 verdicts)   (current lease scope)
```

Each is a separate dimension. Per-agent state exposes all 5.

## Competency equation

```
K_AF = R × A × E × V × L

where:
R = Routing competence
A = Authority competence
E = Execution/tool-selection competence
V = Verification competence
L = Learning competence
```

If any is zero, K_AF = 0.

## Refs

- Contract: `/root/AAA/instructions/aforge-citizen-contract.md`
- Verb schema (cold): `/root/AAA/registries/AFORGE_VERB_SCHEMA.json`
- Generator: `/root/AAA/scripts/aforge_warga_view_generator.py`
- Projection output (hot, regenerable): `/root/AAA/state/aforge/warga-capabilities.json`
- Competency schema: `/root/AAA/instructions/aforge-competency-schema.md`
- Competency evals: `/root/AAA/instructions/aforge-competency-evals.md`
- Sample competency state: `/root/AAA/state/aforge/competency/FI-008-kimi-code.json`
- Test harness (E1): `/root/AAA/tests/aforge-competency/test_E1_inspect.py`

DITEMPA BUKAN DIBERI ⚒️