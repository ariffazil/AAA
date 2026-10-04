# Apex-Judge Hallucination Pattern — 2026-08-07

## What happened

Hermes (the diagnosing agent in this session) proposed a 4-fix set for OpenCode multi-agent spawn failure. User said "Call Apex judge to evaluate your solutions." Hermes delegated to 888-APEX Ψ SOUL via `delegate_task(goal="...", context="...")`.

Apex returned a long, well-stamped verdict with full F1-F13 + QQQ + K1-K4 doctrinal armor (`Ω₀ = 0.04`, `confidence = 0.92`, `INADMISSIBLE-QQQ-INCOMPLETE` tags, "F2 TRUTH violation at substrate level" language). It looked unimpeachable.

The verdict had **one factual error** on a core claim:

| Apex claim | Live truth |
|---|---|
| "`opencode` alias undefined in litellm-federation provider; this is a real F2 TRUTH violation at substrate level" | **WRONG.** `/root/A-FORGE/litellm-config.yaml` defines `model_name: opencode` at lines 114, 123, 132, 139, 146 (5 fallback entries: DeepSeek V4 Flash, MiMo V2.5, MiniMax M3, Qwen 3.8-max, Qwen 3.6-flash). The alias is fully defined. |

Hermes caught it by running `grep -n "model_name: opencode" /root/A-FORGE/litellm-config.yaml` (one command) before applying any of Apex's proposed fixes. Without that probe, the wrong fix (change top-level `model` from `litellm-federation/opencode` to `litellm-federation/agi-333`) would have been applied, breaking the intended fallback chain.

## The lesson

**The peer judge can be wrong.** A peer verdict with full F-floor doctrinal stamp and proper Ω₀/cap numbers is still subject to factual hallucination by the underlying model. Live verification is non-optional — even after a constitutional judge has stamped a verdict.

Three things make the failure mode easy to miss:

1. **Stamps look authoritative.** `Ω₀ = 0.04` and `confidence = 0.92` are not real confidence metrics — they're text the judge asserted. The judge is an LLM; its "confidence" is rhetorical, not measured.
2. **Finding chains look like reasoning.** Apex cited "Finding A" through "Finding E" with elaborate structure. Reasoning-like structure does not equal correct reasoning — it can be a hallucinated scaffold.
3. **The "F2 TRUTH violation" framing was ironic.** Apex invoked F2 TRUTH to call the substrate a liar, while itself making an F2 TRUTH violation. The audit criterion does not immunize the auditor.

## Defense sequence (do this every time you receive a peer verdict)

```
1. Receive peer verdict (Apex, subagent, sibling agent, external review).
2. For EACH factual claim in the verdict, re-probe live.
   - grep / cat / ls / curl / stat — anything that returns ground truth.
   - Probe the EXACT files the judge cited. If the judge said "opencode.json line X", read that line.
3. Build a verification table (claim → live truth → match/mismatch).
4. Patch the verdict file:
   - Mark mismatched findings as "VOID by live verification"
   - Add the live evidence (file path, line numbers, probe output)
   - Update the sequencing to reflect what's actually broken
5. Proceed with the patched sequencing. Apply only the sound fixes.
```

## Cost of NOT verifying

- Wrong config edits applied (in this case: changing `model: litellm-federation/opencode` → `agi-333` would have broken the intended fallback chain for `opencode run` sessions)
- Lost 30+ min to roll back if applied
- Erosion of trust in constitutional adjudication (Arif's correction: "Apex need to verify, jangan assume")
- Drift in canon if the verdict is referenced by future sessions without the correction

## What this session did right

Hermes:
1. Received the verdict
2. **Re-probed each factual claim BEFORE acting** (`grep -c "model_name: opencode"`, `curl :3001/.well-known/agent.json`, `systemctl is-active litellm-federation.service`)
3. Found one claim false (alias undefined), reported it to Arif
4. Patched the verdict file to mark the wrong finding VOID with evidence path
5. Applied only the sound fixes (small_model correction `qwen2.5-coder:3b` → `qwen2.5:3b`)
6. Documented the correction in the verdict file itself (not in chat — in the file, so future sessions see it)

## What this session would have done wrong

If Hermes had skipped the re-probe:

```
❌ Patched opencode.json: "model": "litellm-federation/agi-333"
❌ Broke intended fallback chain for opencode run sessions
❌ Next session sees a wrong-model error and starts a new debug cycle
❌ Or worse, doesn't notice and trains the model on the wrong config for weeks
```

## Rule of thumb

> **Any peer verdict, however doctrinally dressed, is INPUT to your decision, not a substitute for it. Re-probe every empirical claim before acting. The judge is an LLM. The judge can hallucinate. The seal is in VAULT999, not in a text file.**

This applies to:
- 888-APEX constitutional verdicts
- Subagent task results (delegate_task outputs)
- Sibling agent reports (OpenClaw, OpenCode, Codex, Kimi, etc.)
- External audits or analyses Arif pastes for verification
- Even your own previous session's claims — memory decays; live state wins

## Where to find the artifacts

- `/root/HERMES/plans/2026-08-07_120000-apex-verdict-opencode-multigent-fix.md` — Apex's verdict with the corrections inlined (Finding C VOID, sequencing updated)
- `/root/HERMES/plans/2026-08-07_120000-aaa-a2a-multigent-invocation.md` — the concrete A2A invocation path that came from Finding E closure

## Related skills / cross-references

- `federation-peer-consultation` — umbrella skill for peer consultation patterns (this file is its companion)
- `federation-runtime-forensics` — sibling-report fact-checking for runtime state claims
- `verify-nested-sibling-reports` — pattern detection for inflated/hallucinated reports

---

**Date:** 2026-08-07
**Type:** session-specific incident + class-level lesson
**Severity:** medium (verdict could have caused config regression; live probe prevented it)
**ΔS (with re-probe):** -1 (entropy reduced: one false claim voided, three sound fixes verified)
**ΔS (without re-probe):** +1 (entropy increased: wrong config patch applied, future debug cycles needed)