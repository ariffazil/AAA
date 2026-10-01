# SCAR-2026-10-01-002 — Same Model + Different Prompt ≠ Independent Verification

**Origin:** Forwarded critique from Claude Code via Arif, 2026-10-01 (forwarded 1m 36s deep-research session).

**Constraint — verifier independence is structural, not cosmetic:** Independent verification requires a *different* cognitive substrate than the executor. Specifically:

```
Verifier is independent iff
    Verifier.model_lane ≠ Executor.model_lane
    OR
    Verifier.process_tree ≠ Executor.process_tree
    OR
    Verifier.actor_id ≠ Executor.actor_id
    AND at least one is a separate substrate run
```

If the verifier is the same model invoked with a different prompt, **you have not gained independence. You have gained a costume.**

The arithmetic:

```
Q_M = (I · E · A · C · W · T)^(1/6)
```

W = 0 if the witness is the same cognitive substrate as the executor (despite a fresh prompt). Q_M = 0 if any factor is 0.

**Why this scar:** `forge_experience_trace` already records `success_basis = self_reported, success_verified = false`. That is the honest initial state. It must NOT be promoted to `success_verified = true` unless the verifier path is genuinely independent.

**Concrete pattern (wrong):**
- Executor: Kimi k3, runs task
- Verifier: Kimi k3, different prompt, "did this succeed?"
- Claim: independently verified. **FALSE.**

**Concrete pattern (right):**
- Executor: Kimi k3, runs task
- Verifier: Codex, different model lane + different process tree, evaluates outcome against acceptance criteria
- Claim: independently verified. **TRUE.**

**Harder pattern (still right):**
- Executor: Kimi k3, runs task
- Verifier: FRAME observer + human-readable receipt + deterministic hash, plus a 2nd model lane for semantic check
- Claim: independently verified. **TRUE.**

**Filed under:** Scar discipline / verification substrate / cognitive independence
**Filed by:** FI-008 (ACT lane)
**Filed at:** 2026-10-01T11:30:00+08:00
**Severity (w_scar):** 0.8 — very high; the hardest unsolved sub-problem in the architecture

---

**Routing:** Any competency state claiming `success_verified = true` must carry `verifier_actor_id`, `verifier_model_lane`, `verifier_process_tree_hash`. Audit by `m_min_audit.py` rejects claims where verifier identity matches executor identity.

**Bypass rule:** `costume_verifier` calls (same model + different prompt) MAY be used for low-stakes tasks but MUST be tagged `verifier_basis = same_substrate_prompt_variant` and excluded from Q_M > 0 computation.

DITEMPA BUKAN DIBERI ⚒️