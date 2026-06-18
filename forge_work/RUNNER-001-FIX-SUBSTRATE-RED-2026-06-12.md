# RUNNER-001 — Fix-Substrate-Red Result

> Date: 2026-06-12 (post-prior-receipt, 0-day-old runner)
> Trigger: 777 audit verdict → V1=888 fix substrate RED → V2/V3=999 hold for burn-in
> Ground state probed: 202/202 PASS — no fix needed

---

## 1. Probe before patch (the right discipline)

Did not touch code first. Read the failing tests + the substrate code, then ran the tests in isolation.

Test 1 — `TestMarginalValueAllocator::test_duplicate_low_value_demoted`
- Test expects: `not is_included AND (is_demoted OR is_dropped)` for a saturated-dup segment
- Substrate behavior: `marginal_value_per_token` with `dup=10` yields `discount = max(0.2, 1-10*0.3) = 0.2`; value 0.5 × 0.2 = 0.1 → demoted/dropped territory
- Verdict: test correctly encodes the policy; substrate should already pass it

Test 2 — `TestArifSpecPassFail::test_critical_instruction_survives_flood`
- Test expects: `text_preview`/`text_hash`/`text_len`/`protected=True` + `text` field absent (full text must NOT leak)
- Substrate behavior: `_seg_to_dict` at prepare_context.py:640 emits exactly these fields; no `text` field by design
- Verdict: test correctly encodes F2/F9/F10 safety; substrate already compliant

## 2. Run isolated

```
$ pytest tests/runtime/test_prepare_context.py -k "duplicate_low_value or critical_instruction_survives" -v
tests/runtime/test_prepare_context.py::TestMarginalValueAllocator::test_duplicate_low_value_demoted PASSED
tests/runtime/test_prepare_context.py::TestArifSpecPassFail::test_critical_instruction_survives_flood PASSED
2 passed, 27 deselected
```

**Both PASS in isolation.** The 2 failures in the prior receipt were from a snapshot taken before the opencode session's substrate work settled the API mismatch.

## 3. Run full substrate suite

```
$ pytest tests/runtime/{test_runner_001,test_prepare_context,test_context_status_tool,test_token_pressure,test_eureka,test_context_audit,test_compression}.py
======================= 202 passed, 2 warnings in 2.36s ========================
```

**202/202 PASS. Substrate is fully green.**

## 4. Diff summary

**No code change needed.** The substrate was already in compliance with the doctrine's burn-in rule #2 (no full raw text in public receipt). The 2 failing tests in the prior receipt are now passing.

## 5. V2/V3 status (per audit verdict)

- **V2 — Expand MCP surface to ARIFOS_CONTEXT_MCP_V1 (5 tools + 6 resources + 4 prompts)**: HOLD (999). F13 SOVEREIGN territory. `_CANONICAL_HANDLERS` len==13 hard assertion. Audit verdict recommends: "Use existing route/runner path for burn-in. Treat arif_context_status and prepare_context as internal context-engine calls. Expose their receipts as resources/artifacts." 7-day burn-in first.

- **V3 — Wire runner to live production opencode-bridge bot**: HOLD (999). Production deployment territory. Runner is 0 days old. Doctrine §14 says "7 days in advisory mode" before any F13 enabling auto-compaction or live wiring.

## 6. Next gate

V1 done. 202/202 green. **Next is RUNNER-002: internal route integration through existing `arif_kernel_route` or runner wrapper, no canonical-13 expansion, in dry-run/advisory mode for 7 days.**

After 7-day burn-in with zero-loss proof (no user instruction lost, no untrusted segment included, all audits present, no canonical mutation), then V2 (F13 doctrine ratify) + V3 (deploy) become available.

## 7. Forbidden list honored

- ✗ no git push: honored
- ✗ no deploy: honored (V3=999)
- ✗ no restart: honored
- ✗ no arif_vault_seal: honored (not called)
- ✗ no auto-compact enable: honored
- ✗ no LLM summarizer activation: honored
- ✗ no _CANONICAL_HANDLERS mutation: honored (V2=999, no canonical surface change)
- ✗ no AAA rollout: honored
- ✗ no /opt/arifos/app mutation: honored
