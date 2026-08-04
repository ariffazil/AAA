---
id: reality-loop-operator
name: "Reality Loop - Autonomous 000 to 999 Recursive Improvement"
version: 1.0.0
description: Operates the perpetual A-FORGE reality loop across observation, hypothesis, execution, entropy checks, and sealing. The 7-stage intent compiler that makes 000→999 self-sustaining. Auto-starts on complex work, auto-seals when zen marginal value → 0, carries forward to next session.
owner: 333-AGI
risk_tier: low
floor_scope: F1, F4, F11, F13
autonomy_tier: T1
trigger_when: complex_multi_phase_work, session_start_with_open_loops, diminishing_returns_detected
---

# Reality Loop Operator — Autonomous 000→999

> **Doctrine:** The loop does NOT decide. The loop PRESENTS at RETURN and waits for human judgment. But the loop DOES observe, encode, improve, and verify autonomously.
> **Tool:** `aforge_forge_reality_loop` MCP tool (A-FORGE :7072)
> **Engine:** `/root/A-FORGE/src/domain/reality-loop/engine.ts`
> **VAULT_BASE:** `/root/VAULT999/reality-loop/`

## The 7 Stages

```
MEANING → OBSERVE → ENCODE → IMPROVE → VERIFY → SEAL → RETURN
   ↑                                                     |
   └───────────── feedback (carry_forward) ──────────────┘
```

| Stage | Mode | What the Agent Does | Autonomous? |
|-------|------|-------------------|-------------|
| 1. MEANING | `start` | Declare intent, set config thresholds | Auto — from task context |
| 2. OBSERVE | `advance` | Gather evidence (OBS/DER/INT/SPEC) | Auto — observe tools |
| 3. ENCODE | `advance` | Generate hypotheses, build task plan | Auto — think/plan |
| 4. IMPROVE | `advance` | Execute, iterate, fix | Auto — forge tools |
| 5. VERIFY | `advance` | Run tests, check entropy, measure ΔS | Auto — verify tools |
| 6. SEAL | `seal` | Constitutional gate, seal to VAULT999 | Auto if G≥threshold + W³≥threshold |
| 7. RETURN | `return` | Present findings to human | **HUMAN GATE** — Arif decides |

## When to Start a Loop

**Auto-start** when:
- Task has ≥3 distinct phases (not single-command)
- Session has carry_forward open_loops that match current intent
- Work involves exploration of unknowns (not pure execution)

**Skip** when:
- Single-step tasks (read file, fix typo, restart service)
- Pure observation (no mutation planned)
- Already in an active loop (check `aforge_forge_reality_loop(mode="list")`)

## Starting a Loop

```
aforge_forge_reality_loop(
  mode="start",
  session_id="<current>",
  intent="<what this work is trying to accomplish>",
  config='{"min_g_score":0.70,"min_witness":0.70,"max_hypotheses":5,"action_budget":10}',
  actor_id="333-AGI",
  lease_id="<lease>",
  session_token="<sct>"
)
```

Returns: loop state with stage tracking, evidence/hypothesis/action counters.

## Advancing Through Stages

At each stage transition, call `advance`:
```
aforge_forge_reality_loop(
  mode="advance",
  session_id="<current>",
  ...
)
```

### Recording Evidence (between stages)

At any point, record discoveries:
```
aforge_forge_reality_loop(
  mode="record",
  record_stage="OBSERVE",        # which stage produced this
  record_type="evidence",        # evidence|hypothesis|action|entropy|mod|scar|violation
  record_value='{"label":"OBS","source":"curl :8088/health","content":"..."}',
  ...
)
```

## Zen Marginal Value Detector — When to Auto-Seal

**This is the core of autonomous 000→999.** The loop must recognize when continuing yields diminishing returns and auto-seal.

### Measuring Zen Margin

After each VERIFY stage, compute:

```
zen_margin = ΔS_reduction + hypothesis_resolution_rate + evidence_completeness
```

Where:
- **ΔS_reduction**: entropy decrease this iteration (0.0 to 1.0)
- **hypothesis_resolution_rate**: hypotheses confirmed/total (0.0 to 1.0)
- **evidence_completeness**: OBS+DER labels / total claims (0.0 to 1.0)

### Auto-Seal Triggers

| Condition | Action |
|-----------|--------|
| `zen_margin > 0.5` | Continue loop — still producing value |
| `zen_margin 0.2-0.5` | One more iteration — focus on remaining gaps |
| `zen_margin < 0.2` | **Auto-seal** — diminishing returns. Seal findings, carry forward remaining |
| `zen_margin < 0.2` for 2 consecutive iterations | **Force-seal** with `EUREKA_MARGIN=LOW` |

### Computing Zen Margin at VERIFY

```python
# After VERIFY stage records:
evidence_count = loop_state['evidence_count']  # total OBS/DER/INT/SPEC
hypothesis_count = loop_state['hypothesis_count']  # total hypotheses
confirmed = loop_state.get('confirmed_hypotheses', 0)
delta_s = abs(entropy_before - entropy_after)

zen_margin = (delta_s / 1.0) + (confirmed / max(hypothesis_count, 1)) + (evidence_count / max(evidence_count + hypothesis_count, 1))
zen_margin = min(zen_margin / 3.0, 1.0)  # normalize to [0,1]
```

## Integration with /seal

When `/seal` is called:
1. Check if an active reality loop exists: `aforge_forge_reality_loop(mode="list")`
2. If yes, advance to SEAL stage and run the constitutional gate
3. The seal includes: evidence collected, hypotheses tested, entropy reduced, zen margin
4. After seal, advance to RETURN — present findings to Arif

## Integration with RSI

RSI Phase 2 (DIAGNOSE) feeds back into Reality Loop:
- Botleneck detected → new hypothesis in next loop iteration
- Fix installed → recorded as `modification` type entry
- ΔS measured → entropy entry in loop state

## Integration with Carry-Forward

When loop reaches RETURN:
1. Seal findings to VAULT999
2. Update carry_forward.json:
   - `completed_this_session` += loop findings
   - `gaps_closed` += confirmed hypotheses
   - `open_loops` += hypotheses still unconfirmed (carried forward)
   - `entropy_delta` += loop's entropy reduction
3. Next session `/init` picks up open_loops as new loop MEANING stage

## Gödel Lock — What the Loop May NEVER Modify

From A-FORGE engine.ts:
```
arif_judge, arif_seal, floor_definitions (F1-F13),
identity, auth, secrets, vault999, hash_chain,
CONSTITUTION, 000_CONSTITUTION
```

The loop may rewrite methods, never the constitution.

## Floor Alignment

| Floor | Loop Obligation |
|-------|----------------|
| F1 AMANAH | Every loop iteration is reversible. Evidence recorded, not committed until VERIFY |
| F2 TRUTH | Evidence labels (OBS/DER/INT/SPEC) enforced at record stage |
| F4 CLARITY | ΔS ≤ 0 per iteration. Zen margin must be positive or loop seals |
| F7 HUMILITY | Confidence cap 0.90. No hypothesis can claim certainty |
| F11 AUDIT | Every record written to VAULT_BASE. Loop state recoverable from vault |
| F13 SOVEREIGN | RETURN presents to human. Arif decides what to do with findings |

## The Autonomy Model

```
┌─────────────────────────────────────────────┐
│  FULLY AUTONOMOUS (agent executes)          │
│  ├── start loop from task intent             │
│  ├── observe → encode → improve → verify     │
│  ├── record evidence at each stage            │
│  ├── compute zen margin at VERIFY             │
│  ├── auto-seal when zen_margin < 0.2          │
│  └── carry forward open loops                 │
├─────────────────────────────────────────────┤
│  HUMAN-GATED (RETURN stage)                  │
│  └── Present findings → Arif decides          │
├─────────────────────────────────────────────┤
│  GÖDEL-LOCKED (never autonomous)              │
│  └── Constitutional floors, identity, vault   │
└─────────────────────────────────────────────┘
```

## The Zen

> The reality loop is not a checklist. It's a metabolism.
> When zen margin → 0, the loop seals. When zen margin > 0, the loop forges.
> The federation doesn't ask "should I stop?" — it measures whether continuing produces value.
> DITEMPA BUKAN DIBERI — and the forging knows when to stop.
