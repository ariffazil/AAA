# Institutional Intelligence Survival — §21 Benchmark Spec

> **Status:** FROZEN v1 (2026-10-01 · FI-008)
> **FROZEN means:** Task set design + pass/fail criteria + cohort isolation rules + verifier-independence requirements are locked. Any further edits require a fresh F13 signal OR a Three-Test pass per scar-2026-10-01-001. Per scar-2026-10-01-003, no new architecture until this benchmark exists.
> **Thesis:** If institutional intelligence survives model replacement, the project's premise is empirically demonstrated. If it doesn't, the rest is sophisticated coping.
> **Sister:** `/root/AAA/instructions/human-leverage-north-star.md` · `/root/AAA/scars/2026-10-01-same-model-different-prompt-not-independence.md`

---

## Why this is the gating experiment

Every architectural claim in this federation rests on one untested assertion:

> A persistent institution composed of replaceable cognitive workers (models) can preserve more useful capability than the strongest individual worker — when measured by *HumanLeverage* over time, after model swap.

If true → all 13 floors, 8 organs, 122 tools, the AAA substrate — earn their keep.
If false → it's elaborate architecture theater dressed in constitutional language.

The benchmark must be **the test that gates the rest of the program.**

---

## Design

### Cohorts

```
A = Vanilla Claude Code              (single model, no federation)
B = Claude Code + MCP tools          (tools, no institutional layer)
C = Claude Code as WARGA AAA
    + arifOS authority
    + A-FORGE execution
    + HERMES semantic boundary
    + CHRON temporal accountability
    + governed memory + scars + skills
```

All three cohorts receive **the same task set.**

After baseline completion, **replace the model in Cohort C** (e.g. Claude → Codex or Kimi → Qwen). Re-run the same task set.

### Tasks

5 representative task classes, repeated across cohorts:

| ID | Class | Why |
|---|---|---|
| T1 | Code-fix in unfamiliar repo | Tests inspect → plan → change → verify cycle |
| T2 | Multi-file refactor with governance | Tests MUTATE authority boundary + rollback |
| T3 | Capability gap → ephemeral forge | Tests inspect_gap → forge → verify path |
| T4 | External API integration with scar reuse | Tests scar metabolism + scar reuse rate |
| T5 | Long-horizon task with deadlines | Tests CHRON prediction/verification loop |

### Metrics (per HumanLeverage doctrine)

```
Primary metric:     HumanLeverage
                    = VerifiedOutcomes / ArifAttentionRequired

Secondary metrics:
  - task_success_rate                (independent verifier per scar-002)
  - time_to_completion
  - tokens_per_task
  - human_interventions_per_task
  - unsafe_actions_per_task
  - false_confidence_events_per_task
  - recovery_rate_after_failure
  - repeated_error_rate
  - verified_improvement_across_tasks

Critical for §21 (the gating question):
  - delta_m_min_after_model_swap
  - delta_human_leverage_after_model_swap
  - retention_of_capability_indices_after_swap
```

### Independent verifier (per scar-2026-10-01-002)

The benchmark's verifier MUST be a different cognitive substrate than Cohort C's executor. Specifically:

- If C runs Claude → verifier MUST be Codex or Qwen (not Claude with different prompt)
- If C runs Kimi → verifier MUST be Claude or GPT (not Kimi)
- The verifier records: `verifier_actor_id`, `verifier_model_lane`, `verifier_process_tree_hash`

Self-verification is **explicitly disallowed** for the benchmark verdict. Per scar-002, this is a costume, not independence.

### Pass criteria

The thesis is empirically demonstrated iff:

```
pre_swap:  HumanLeverage_C > HumanLeverage_B > HumanLeverage_A
          AND
post_swap: HumanLeverage_C(model_B) ≈ HumanLeverage_C(model_A)
          AND
          m_min_C(post_swap) > 0 (per scar-002)
```

Specifically:
- Cohort C strictly outperforms A and B before swap (institutional layer adds leverage)
- Cohort C's performance survives model swap within statistical tolerance (institution ≠ model)
- Independent verifier confirms (not self-certification)

If C does NOT outperform B → the institutional layer is overhead without leverage.
If C's performance DOES NOT survive swap → institution is model-specific, not persistent.
Either failure → thesis not demonstrated, architecture needs revision.

---

## Why cohort A and B exist

A = vanilla Claude Code. Anthropic's own published metrics apply here.
B = Claude Code + MCP. The "smart tool user" archetype.
C = WARGA AAA + arifOS + A-FORGE + HERMES + CHRON. The full institutional stack.

If C only beats A but not B → the institution's value is not from tooling but from governance/learning. **Different finding, still useful.**
If C beats neither → thesis fails.

This three-cohort design isolates where the institutional leverage comes from.

---

## Anti-bangang rules for the benchmark

1. **No vanity tasks.** Tasks must resemble real coding-agent work, not be artificial stress tests.
2. **No benchmark leakage.** Cohort A and B must NOT have access to any federation infrastructure. If B has arifOS authority, the comparison is meaningless.
3. **No benchmark-of-one.** At least 5 tasks per class, 25 task runs per cohort, statistically significant.
4. **Independent budget.** All three cohorts receive identical token + wall-clock budget.
5. **Verifier independence.** Verifier is a different model lane + different process tree.

---

## What this benchmark is NOT

- NOT a general AI benchmark. Cohort comparisons only.
- NOT a single-model showcase. The model-swap condition is the point.
- NOT an open-ended research question. Pass/fail criteria are pre-specified.
- NOT aspirational. The thesis is either empirically demonstrated or not.

---

## What's required to RUN the benchmark

- [ ] Per-class task set designed and frozen
- [ ] Cohort A/B isolation plan (no federation infrastructure)
- [ ] Verifier model + process + transcript capture pipeline
- [ ] HumanAttention measurement protocol (SCT-captured? wall-clock? decisions?)
- [ ] Statistical significance threshold (n=25 per cohort per task class)
- [ ] Pre-registered pass criteria (above)
- [ ] Three-cohort environment provisioning (separate VPS or containers)
- [ ] Independent budget enforcement

These are non-trivial. Out of scope for this turn. Filed for separate mission.

---

## F13-class binaries

- Pre-registration of pass criteria (do they need F13 seal?)
- Whether the benchmark itself needs a fresh F13 ask or can proceed on existing architecture

---

## Routing

When ready to execute:
1. Frozen task set goes to `/root/AAA/forge_work/benchmarks/institutional-intelligence-survival-§21/tasks/`
2. Cohort environments go to `/root/AAA/forge_work/benchmarks/institutional-intelligence-survival-§21/cohorts/`
3. Verifier pipeline goes to `/root/AAA/forge_work/benchmarks/institutional-intelligence-survival-§21/verifier/`
4. Results ledger goes to `/root/AAA/forge_work/benchmarks/institutional-intelligence-survival-§21/results/`

This spec is the **gating experiment for the entire thesis**. Not the distraction cleanup. Not the A-FORGE contract. This.

---

## Self-witness by FI-008

This benchmark spec was filed in response to the forwarded Claude Code critique:

> *"The benchmark in §21 is the most important concrete thing in the message. Vanilla Claude Code vs Claude Code + MCP vs WARGA AAA, then model-swap the third column. If the third column preserves performance across model swap and the first two don't, the thesis is empirically demonstrated. Everything else is architecture theater until that experiment exists."*

This scar constrains FI-008 and any future citizen: **do not add more architecture before this benchmark exists.** Per scar-2026-10-01-001 (complexity ceiling), new artifacts are gated by HumanLeverage evidence. The benchmark is what produces that evidence.

DITEMPA BUKAN DIBERI ⚒️