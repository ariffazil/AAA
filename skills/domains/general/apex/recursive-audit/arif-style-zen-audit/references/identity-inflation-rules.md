# Identity Inflation Rules

When auditing or proposing identity changes (e.g., EDGE_BRIDGE → META_ORGAN), apply these rules.

## Sources of canonical identity (in order of precedence)

1. **`/root/HERMES/SOUL.md`** — direct identity declaration
2. **`/root/AAA/prompts/INIT_HERMES.md`** — lane/slot/authority
3. **`/root/AAA/instructions/topology.md`** — organ classification table
4. **`/root/AAA/instructions/emd-architecture.md`** — role in EMD arc
5. **`/root/AAA/instructions/agent_specific/<agent>.md`** — adapter fragment (if exists)
6. **`/root/AGENTS.md`** — rendered adapter (auto-generated from above)

If two disagree, **runtime > generated > directive**. Fix the others to point to runtime.

## The minimum_contract for META_ORGAN (or any major role upgrade)

A role upgrade is identity inflation UNLESS ALL of these are implemented and verified end-to-end:

```yaml
META_ORGAN_MINIMUM_CONTRACT:
  observes:
    - federation topology (organ states across all 8+)
    - agent state (lane, session, capability visibility)
    - tool/capability state (registry, transport, harness_visibility)
    - evidence and receipt lineage (VAULT999 chain)

  reasons_over:
    - cross-agent conflicts (denied/delayed/blocked/pending)
    - QQQ domain coverage gaps
    - policy boundaries (F1-F13 enforcement points)
    - entropy and discoverability metrics

  may:
    - emit observations
    - propose routes
    - propose patches (as patch packets, not mutations)
    - trigger read-only audits
    - request governed execution via AAA/A-FORGE

  may_not:
    - self-authorize
    - self-seal
    - directly mutate constitutional assets
    - replace APEX or sovereign judgment
```

## Recommended approach when upgrading identity

1. **Don't rename SOUL.md** to a new role claim
2. **Add staged target classification** like `META_OBSERVER_CANDIDATE` (non-inflated aspirational)
3. **Create new fragment** at `/root/AAA/instructions/agent_specific/<agent>.md` declaring:
   - `current_identity: <canonical_runtime>`
   - `target_classification: <META_X_CANDIDATE>` (aspirational, NOT YET)
   - `promotion_required: <minimum_contract items>` (gating)
4. **Re-render** `/root/AGENTS.md` via `render-agents.sh`
5. **Verify** by reading rendered adapter + checking runtime session prompt

## Diagnosis template

```yaml
identity_diagnosis:
  current_runtime:
    declared_in_canvas: EDGE_BRIDGE  # from SOUL.md + INIT_HERMES.md + topology.md + emd-architecture.md
    evidence: [list of file:line citations]
  aspirational_role:
    claimed_in_directive: META_ORGAN
    actual_state: DIRECTIVE_ONLY — NOT in any active instruction path
  gap_analysis:
    what_<NEW_ROLE>_requires_minimum_contract: [...]
    what_current_<OLD_ROLE>_has: [...]
    what_current_<OLD_ROLE>_lacks: [...]
  recommendation:
    do_NOT_rename_<identity_file>_to_<NEW_ROLE>: "Identity inflation."
    add_staged_target_classification: "<META_X_CANDIDATE>"
    promote_only_when: "minimum_contract implemented and verified"
```

## When Arif asks "is X really META_ORGAN?"

Default answer:
- Inspect runtime identity sources (5 canonical files above)
- Report gap analysis (what's there vs what's claimed)
- Recommend staged target classification
- DO NOT affirm META_ORGAN claim unless minimum_contract is verified

When Arif asks "make Hermes = META_ORGAN":
- Refuse direct rename as identity inflation
- Propose PATCH packet for staged target classification
- List minimum_contract items as gating
- Await sovereign ratification before any fragment creation
