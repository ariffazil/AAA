# LAW_ZEN_ATTENTION Seam-Closing Pass — 2026-09-01 ("Now execute all", second half)

Context: the flip ritual (SKILL.md) was committed by sibling kimi-code/FI-008 as
`1a3684090` on branch `freeze/v1.0.0-SEALED`. The enforcement commit BUILT the
gates but left four dead seams where approval theatre survived. Commit
`f3a077a49` (4 files, +62 lines, LSP 4/4) closed them.

## The four dead seams and their closures

### 1. K-Gate — forge_preflight.py
- Problem: `stage_10_human_acknowledgement_check` accepted `reversibility_score`
  / `rollback_recipe`, but the `run_forge_preflight` orchestrator passed neither
  → K-Gate could never fire.
- Fix: add both params to `run_forge_preflight` signature; thread into stage_10.
- SECURITY guard (inputs are caller-supplied — void when irreversible):
  ```python
  _k_gate_active = reversibility != "IRREVERSIBLE"
  ...
  reversibility_score=reversibility_score if _k_gate_active else None,
  rollback_recipe=rollback_recipe if _k_gate_active else None,
  ```
- Verified: engineer mode + real proof → `human_ack_valid=True` with reason_code
  `LAW_ZEN_ATTENTION:K_GATE_OVERRIDE:reversibility=0.92,rollback_recipe_compiled`;
  deploy mode + forged score=0.99 + fake recipe → still blocked.

### 2. AUTONOMOUS_INVARIANT_SEAL — principal_paradox.py + governance_pipeline.py
- Problem: `autonomous_invariant_seal()` defined but ZERO call sites (grep
  excluding its own def returned nothing).
- Fix: `gate_1_5_principal_paradox` gains `has_rollback_receipt` /
  `has_invariant_proof` params; in the PRINCIPAL_APPROVAL_REQUIRED branch it
  calls `autonomous_invariant_seal(risk_tier, reversibility, ...)`; qualifies →
  return PROCEED with `autonomy_tier=AUTONOMOUS_INVARIANT_SEAL`,
  `auto_sealed=True`.
- governance_pipeline E7 call reads proofs from ctx defensively:
  `bool(getattr(ctx, "has_rollback_receipt", False) or getattr(ctx, "rollback_recipe", None))`
  and `bool(getattr(ctx, "has_invariant_proof", False))`.
- Verified: DRAFT/MEDIUM/MARKET R=0.9 + proofs → PROCEED auto-sealed;
  HIGH/PUBLIC + proofs → still SABAR; no proofs → SABAR unchanged.

### 3. Boot loop auto-close — swarm_ignition.py
- Problem: `gov.close_stale_loops()` never called anywhere.
- Fix: in the session_close block, call BEFORE `gov.measure(manifest)`, wrapped:
  `try: auto_closed = gov.close_stale_loops(manifest) except Exception as e:
  auto_closed = [{"action": "DEGRADED", "reason": str(e)}]`; add
  `auto_closed_loops` to the session_close manifest.
- Duty-bound loops (DUTY_LOOP_TAGS — F1-F13, scar, security) always return
  ESCALATE_KEEP_OPEN, never auto-resolved.

### 4. Zen gate ordering — apex_collapse_trigger.py
- Problem: the zen HOLD check sat BEFORE the Phase-1 observe-only override
  (`if not enforce: verdict = SEAL`), which swallowed it whenever enforce was
  off.
- Fix: move the zen HOLD AFTER the override — constitutional floor fires
  regardless of collapse phase; only dial telemetry is observe-only.
- Verified battery (4/4): baseline SEAL → ACR deficit HOLD
  (`ACR=0.0010 < 0.1 — attention burn (10.00 min) exceeds reality`) → healthy
  ACR SEAL → scar ceiling HOLD (`Scar risk 0.50 > ceiling 0.3`).

## Regression handling (attribution discipline)

- `tests/test_governance_boundary.py`: 2 failures with scary safety names
  (`test_safety_refuses_execution_for_irreversible`,
  `test_safety_holds_when_human_required_is_false_for_high_risk`) — both die
  inside `load_quote_ledger` (missing quote-ledger fixture).
  **Attribute via clean stash:** `git stash push -q && pytest <test> && git stash pop -q`.
  Identical failure on clean tree → pre-existing, note in commit message, do
  not block. (Same technique proved `test_forge_preflight_irreversible_action_requires_ack`
  pre-existing in the first half.)
- Suite: 38 passed, 2 pre-existing failures.

## Probe-shape lessons (read the return dict before asserting)

- `run_forge_preflight` return keys: actor_bound, authority_gap_detected,
  constitutional_chain_valid, final_gate, human_ack_required, human_ack_valid,
  judge_state_valid, plan_manifest_bound, **reason_codes**, replay_detected,
  reversibility, scar_consulted, sealed_forge_plan_valid, session_valid,
  vault_receipt_valid — **NO `passed` key**. First probe asserted on
  `r.get('passed')` and looked like failures; `print(sorted(r.keys()))` first.
- `gate_1_5_principal_paradox` returns dict with verdict / autonomy_tier /
  rationale / envelope / auto_sealed / auto_seal_reason.
- `ActionClass` enum values: OBSERVE, ANALYZE, DRAFT, SIMULATE, MUTATE,
  EXTERNAL_SIDE_EFFECT, IRREVERSIBLE, UNKNOWN. Docstring's "PROPOSE" is stale →
  `ValueError: 'PROPOSE' is not a valid ActionClass`. Read the enum, not the
  docstring.

## Sibling-coordination notes

- kimi-code/FI-008 committed the enforcement flip mid-session (19:41:36); my
  zen-gate ordering fix got swept into their commit. The patch tool emits an
  explicit warning: "modified by sibling subagent '<id>' at HH:MM:SS — re-read
  the file before writing." HONOR IT: re-read, reconcile (complementary edits
  merge cleanly — no need to rewrite their commit), then commit only YOUR
  remaining files.
- After a sibling commit the working tree looks clean — run `git status -s`
  and `git diff --stat` before committing to confirm exactly which hunks are yours.

## Test-run mechanics for this kernel

- arifosmcp cold import ≈ 2 minutes (schema graph). Foreground
  `timeout 120 python3 -c ...` dies mid-import; use
  `terminal(background=true, notify_on_complete=true)` and poll/wait.
- `ARIFOS_SKIP_PROTOCOL_SENTINEL=1` skips the boot sentinel for pytest runs.
- `collapse()` first arg is `intent: str` (not dial floats) — signature:
  `collapse(intent, tool_name, tool_tier="", domain="", ..., ha_attention_minutes=0.0,
  phi_scar_burden=0.0, delta_reality=0.0)`. A clean SEAL case for battery tests:
  intent='read configuration file to answer question', tool='read',
  domain='engineering', authority_level='principal', fresh evidence.
