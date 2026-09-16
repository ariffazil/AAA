# LAW_ZEN_ATTENTION — Session Detail (2026-09-01)

## The Directive (Arif, verbatim essence)

The Agentic Attention Paradox: in classical economics Y = A·F(K,L,E). In the
agentic regime, Labor splits into Synthetic Execution (L_s — elastic, MC→0)
and Sovereign Attention & Liability (H_a — strictly inelastic, biological
ceiling ~16 hrs/day single-threaded, MC→∞). When L_s → ∞, total output
collapses to H_a allocation.

HITL ex-post approval is **unpriced cognitive dumping** — model builders
generate unverified tokens at near-zero marginal cost and dump the verification
externality onto finite human bandwidth. Economically identical to a factory
dumping chemical runoff into a public river.

Three primitives Arif named:
1. **Liability as Equity Tranche** — agents are un-leveraged debt (capture
   upside, zero downside); human attention is the sole equity tranche.
   H_a = Time × Blast Radius.
2. **Ex-ante mechanism design > ex-post HITL review** (O(N²) context-switch
   penalty makes review unscalable).
3. **Attention as Numéraire** — Sovereign Signal-to-Noise ratio replaces GDP
   throughput. ACR = ΔReality / ΔAttention is the kernel's numéraire.

Terminal thesis: if N minutes of validation saves N-1 minutes of execution,
net yield is negative. Design target k→0 (validation cost per unit value
delivered → 0) — only achievable via deterministic ex-ante gates, never
better models.

My added corollary (accepted): **temporal asymmetry of payoff** — agent gets
upside at T+0, human absorbs downside at T+24mo. That time-lag IS the
principal-agent trap. arifOS F1-F13 floors operationalize k→0.

## Architecture: Human = Attention Allocator, not Approver

```
LOW attention cost  → AUTO-SEAL
HIGH attention cost → HOLD
NOVEL               → ESCALATE
```
NOT "everything → approval". Approval is a UI event. Attention is a
constitutional resource.

## File-by-file injection (all additive, no new files)

### core/physics/economic_invariants.py (canonical at /root/arifOS/core/physics/)
- `AttentionDeficitError(EmergenceError)` — layer="ATT", verdict="888_HOLD"
- `check_attention_compression_ratio(delta_reality, delta_attention_minutes,
  acr_floor=0.10)` — raises if ACR < floor; returns acr=None when
  delta_attention_minutes <= 0 (zero burn → no compression needed)
- Wired into `run_emergence_layer` as E_ATT
- Aliases: `attention_compression_check`, `inv_e4`
- ⚠️ The arifosmcp copy is a re-export wrapper importing from
  `core.physics.economic_invariants` — can raise circular import if loaded
  with sys.path pointing at arifosmcp/. Test from /root/arifOS root instead.

### constitution/attention_gate.py
- Constants: ACR_ESCALATION_FLOOR=0.10, DEFAULT_ACR=1.0, `_acr_from()`
- `AttentionGate.should_escalate(verdict, delta_reality, attention_minutes,
  acr_floor)` → {"escalate", "acr", "action": "ESCALATE"|"AUTO_SAFE_STATE",
  "receipt"} — low ACR auto-passes to safe-state, sovereign not woken.
- Sibling added `suppress_or_surface(signal, delta_reality,
  delta_attention_minutes, acr_min=0.10)` — exit-side twin, same math,
  signal-level. Both coexist: suppress_or_surface for signals,
  should_escalate for verdicts. Sovereign/duty channels bypass both (F6/F13).

### kernel/apex_decision_field.py
- `ApexDecisionField` gains: `ha_attention_minutes: float = 0.0`,
  `phi_scar_burden: float = 0.0`, `acr: float | None = None`
- `assess_apex_decision_field` gains `acr_floor=0.10`, `phi_scar_ceiling=0.30`
  params; new reasons `ATTENTION_ACR_BELOW_FLOOR`, `ATTENTION_SCAR_RISK_EXCEEDED`
- Canonical G = A·P·E·X (and Epoch-34 G = Q·V·Psi·Phi) UNTOUCHED — attention
  becomes part of present authority, not a new equation.

### core/apex_collapse_trigger.py
- Constants: ACR_FLOOR=0.10, PHI_SCAR_CEILING=0.30,
  ZEN_ATTENTION_ENFORCE=True (RATIFIED 2026-09-01), COLLAPSE_TRIGGER_ENFORCE=True
- `collapse()` new kwargs: `ha_attention_minutes=0.0`, `phi_scar_burden=0.0`,
  `delta_reality=0.0`. ACR computed when Ha>0; if < floor (or scar > ceiling)
  and ZEN_ATTENTION_ENFORCE and would-be SEAL → verdict=HOLD with
  "LAW_ZEN_ATTENTION HOLD:" reason.
- Enforcement live: dangerous action → HOLD, low ACR → HOLD, good action → SEAL.
- Testing: to exercise the HOLD path use a SEAL-base action (sovereign
  authority + general domain + search tool gives B|Φ≈0.796 → SEAL base).
  identity-domain intents get X=0.30 (domain weight) → base SABAR, so ACR
  check can't be observed. With the flag now True, no test override needed —
  but keep the pattern in mind if a flag is ever reverted to measure-only.

### boot/entropy_governor.py
- Constants: LOOP_TTL_SWEEPS=3, DUTY_LOOP_TAGS=(FLOOR,SCAR,INCIDENT,DRIFT,
  SECURITY,VAULT,CONSTITUTION,888), `_loop_age_sweeps(loop)`
- `auto_resolve_loop(loop, reversibility=0.9, ttl_sweeps, receipt)` →
  AUTO_RESOLVE (R≥0.85) | AUTO_DEFER | ESCALATE_KEEP_OPEN (duty tags)
- `close_stale_loops(state, ttl_sweeps)` — iterates open_loop_register
- Sibling added `triage_open_loops(state)` — deterministic disposition:
  low→AUTO_CLOSE, medium→AUTO_DEFER, high→AUTO_ARCHIVE, irreversible→
  ESCALATE_888; returns attention_saved_estimate_min.

### runtime/principal_paradox.py
- New enum: `AutonomyTier.AUTONOMOUS_INVARIANT_SEAL`
- `autonomous_invariant_seal(risk_tier, reversibility, has_rollback_receipt,
  has_invariant_proof)` → qualifies only if: risk LOW/MEDIUM, R(a)≥0.70,
  rollback receipt, invariant proof. HIGH/ATOMIC never qualify.
- `_downgrade_tier` order updated to include the new tier.

### runtime/forge_preflight.py
- `stage_10_human_acknowledgement_check` new kwargs:
  `reversibility_score=None`, `rollback_recipe=None`. If human_ack_required
  AND R(a)≥0.85 AND recipe → human_ack_required=False, reason
  `LAW_ZEN_ATTENTION:K_GATE_OVERRIDE:reversibility=X.XX,rollback_recipe_compiled`.

### runtime/consequence_gate.py
- `ConsequenceEvaluation` gains `reversibility_score=1.0`, `rollback_recipe=None`
- `evaluate_consequence`: if R(a)≥0.85 AND rollback_recipe → PASS with
  "LAW_ZEN_ATTENTION: deterministic rollback recipe compiled" (agent OK,
  no 888). R(a)<0.30 → is_irreversible → 888_HOLD for agents.
- Also fixed (sibling): missing comma on `rotate_master_secret` / 
  `modify_constitution_f1_f13` in IRREVERSIBLE_ACTION_TYPES — they were
  string-joined, slipping the gate.

### runtime/mind_feedback_hook.py + runtime/mind_state.py
- `MINDState` gains `attention_minutes_burned=0.0`,
  `attention_compression_ratio=None`
- `finalize()` summary gains `ha_attention_minutes`, `acr` — first link of
  the transmission line (mind → attention_gate → entropy → collapse).

## Doctrine (GENESIS/)

- `005_POST_AGI_ECONOMICS.md` — §XIII "The Sovereign Numéraire — Attention
  (RATIFIED 2026-09-01)" cross-referencing 005b §XVII.
- `005b_POST_AGI_ECONOMICS_KERNEL.md` — §XVII LAW_ZEN_ATTENTION: status
  RATIFIED by F13 fire-word "Now execute all". Wiring list includes all 9
  files + the runtime/mind_* pair.

## Test recipes (all pass as of 2026-09-01, enforcement live)

```bash
cd /root/arifOS/arifosmcp
python3 constitution/attention_gate.py            # self-test ALL PASS
python3 -c "import sys; sys.path.insert(0,'.'); from boot.entropy_governor import EntropyGovernor; ..."
# collapse: enforcement is ON — call collapse(..., ha_attention_minutes=10.0,
#   delta_reality=0.2) → HOLD with acr=0.02; good ACR → SEAL
cd /root/arifOS && python3 -c "from core.physics.economic_invariants import check_attention_compression_ratio"
# principal_paradox / forge_preflight / consequence_gate: use
# importlib.util.spec_from_file_location + sys.modules registration (see pitfall)
```

## Commit history

- `94d0bfa60` feat(kernel): LAW_ZEN_ATTENTION — attention-centric hardening
  (additive, F13 pending) — committed by kimi-code/FI-008; includes the core
  gate work. Verify with `git show 94d0bfa60 --stat`.
- `1a3684090` feat(kernel): LAW_ZEN_ATTENTION ENFORCED — F13 fire-word "Now
  execute all" (2026-09-01) — 15 files, +697/−75. Flips ZEN_ATTENTION_ENFORCE
  + COLLAPSE_TRIGGER_ENFORCE to True, sed's all "F13 pending"/DRAFT markers
  to RATIFIED, rewrites collapse self-test for enforcement, doctrine
  PROPOSAL→RATIFIED. Also includes prior working-tree additions
  (attention_gate should_escalate, mind_feedback_hook, mind_state,
  GENESIS/005 §XIII) plus sibling's vault999 verify_live work.

## F13 gate status — RATIFIED 2026-09-01 (fire-word: "Now execute all")

ZEN_ATTENTION_ENFORCE=True, COLLAPSE_TRIGGER_ENFORCE=True. Enforcement live,
service restarted, port 8088 verified. The measure-only era is over. If a
future session sees these flags False again, that is a deliberate rollback —
confirm with Arif before re-flipping.
