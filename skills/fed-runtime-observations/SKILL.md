---
name: fed-runtime-observations
description: >
  Live observations of the FED router's behavior as probed on 2026-08-12.
  Documents how `agent_id`, `constitutional_tier`, `modality`, and various capability signatures
  are currently handled (or not handled) by the FED at `:7074`. Critical for future FED refactoring.
version: 1.0.0
author: Hermes ASI
forged: 2026-08-12
tags: [fed, router, runtime, observations, identity, tier, modality, capability, federation]
autonomy_tier: T1
---

# FED Router Runtime Observations (2026-08-12)

> This skill documents empirical observations from probing the FED router at `127.0.0.1:7074/fed/route` on 2026-08-12. It serves as a snapshot of the FED's current behavior, highlighting known limitations, missing features, and unexpected bugs. This is critical for planning future FED refactors and understanding its operational state.

## 1. Identity Aliases (i-ARIF, hermes-asi) — `agent_id` Ignored

**Observation:** When probing the FED router with different `agent_id` values (e.g., `i-ARIF`, `hermes-asi`, `hermes`, `openclaw`, `arif-fazil`, `unknown-agent-xyz`), the router returned *identical* routes for all of them.

**Implication:** The FED router currently **does not perform identity-based routing**. The `agent_id` field is silently ignored when resolving a route. Identity resolution must be implemented at a higher layer or added to the FED logic.

## 2. Multimodal Capability Signatures (vision, image, audio, video) — Missing

**Observation:** Probing the FED router with proposed multimodal capability signatures (`fed-vision`, `fed-image`, `fed-audio`, `fed-video`) resulted in errors:
```json
{"error": {"type": "internal", "message": "'model'"}}
```

**Implication:** These capability signatures are **not yet defined** in the FED's `CAPABILITY_SIGNATURES` dictionary. They fail-closed, but with an internal error message rather than a graceful "unknown capability" response.

**Existing Capabilities (Control Group):**
*   `fed-multimodal-vision` works (returns `qwen-vl-max` / `mulerouter`).
*   `fed-reasoning-heavy` works (returns `qwen3.8-max` / `qwen-token-plan-individual`).
*   `fed-doesnotexist` fails with the same KeyError.

## 3. EMD Gate Bug — "Vision-Blind" Capability Signatures

**Observation:** When probing `fed-multimodal-vision` (an existing capability) at `constitutional_tier: 666` with `modality: vision`, the router returned `routes: []` and an `EMD_MISMATCH` verdict:
```json
{
  "routes": [],
  "emd": {
    "verdict": "EMD_MISMATCH",
    "reasons": ["vision payload to vision-blind fed-multimodal-vision"],
    "suggested": ["mimo-v2.5", "qwen3.8-max"]
  }
}
```

**Implication:** The EMD (Encoder/Metabolizer/Decoder) gate is incorrectly classifying the **capability signature itself** (`fed-multimodal-vision`) as "vision-blind" rather than recognizing the underlying resolved model's vision capabilities. This means any capability signature that doesn't have its own `vision_in`, `audio_in`, etc. flags will trigger an `EMD_MISMATCH` regardless of the actual models in its cascade.

**Tier Interaction:**
| `constitutional_tier` | Routes Returned | Reason |
|---|---|---|
| 333 | 2 | OK (cascade resolvable, direct route available) |
| 555 | 2 | OK |
| 666 | 0 | **Constitutional Hard-Gate (tier ≥ 666 requires direct-only) + EMD Bug** = empty cascade |
| 888 | 2 | OK (direct route somehow bypasses hard-gate?) |

## 4. Modality Field Silently Ignored

**Observation:** When probing `fed-multimodal-vision` with various `modality` values (`text`, `vision`, `audio`, `image`, `video`, `omni`), the router returned the same route (`qwen-vl-max` / `mulerouter`) for all of them.

**Implication:** The `modality` field is currently **silently ignored** for capability signatures, or its verdict is not surfaced in the response. This contradicts the EMD mismatch logic seen in the source code (`if modality in ("vision","omni") and not cap["vision_in"]`), suggesting a routing path bypass or a bug where the verdict is computed but not returned.

---

*Forged: 2026-08-12 by Hermes ASI under F13 SOVEREIGN directive for continuous learning.*
*DITEMPA BUKAN DIBERI — Know your runtime, not just your design.*

---

## 5. "Tool Block" Misdiagnosis Pattern (2026-08-12, hermes-arif)

**Observation:** Arif reported "agents blocked, no filesystem access, give full agentic access." First reflex was to interpret as F1-F13 violation. **Reality was benign:**

| User symptom | Actual cause | Fix |
|---|---|---|
| "Tool blocks" | Litellm `:4011 /v1/models` returns empty | Missing `Authorization: Bearer $LITELLM_MASTER_KEY` header (security working as designed) |
| "Filesystem deny" | MCP session needs `Mcp-Session-Id` header | Standard MCP spec — call `initialize` first to get session ID |
| "FI agents blocked" | Carry-forward listed 12 items; 11 were misdiagnosis, runtime already exposed | Re-probe with auth; verify `/v1/models`, `tools/list` after session init |

**Implication:** When a sovereign reports "blockage," do NOT immediately assume constitutional violation. Run the 30-second reality probe FIRST:
1. `curl -sH "Authorization: Bearer $LITELLM_MASTER_KEY" http://127.0.0.1:4011/v1/models | jq` (verify litellm brain)
2. MCP session round-trip with `Mcp-Session-Id` header (verify organ MCPs)
3. `curl :PORT/health` per organ (verify organ liveness)
4. Only THEN escalate to constitutional analysis if all probes are red.

**Anti-pattern:** Telling the sovereign "this is a F1 AMANAH violation" when reality is "you forgot the auth header" wastes the F13 budget and erodes trust in the governance layer.

## 6. arifOS Pre-Push Deploy Gate (Three Gates, T3 Surface)

**Observation:** `git push` to any branch of `ariffazil/arifOS` triggers `scripts/hooks/pre-push/repo_guard.py` with three gates:

| Gate | Check | Common Failures |
|---|---|---|
| **GATE 1** | `pytest tests/test_e2e_kernel.py --timeout=15` | `pytest-timeout` plugin missing (env fix: `uv pip install pytest-timeout`); vault integrity failures (Opus 5 defect accepted, but `test_outcomes_jsonl_parseable_majority` is NOT auto-allowed) |
| **GATE 2** | Path A defect detectors (3 checks) | Usually green |
| **GATE 3** | `:8088/health.deployed_commit == git HEAD` | **drift_detected** when `/opt/arifos/app/.git_commit` is stale vs built_commit |

**How to clear GATE 3 (deployment drift):**
1. Check the marker: `cat /opt/arifos/app/.git_commit`
2. Compare with built_commit from `/health`
3. Write built_commit to marker: `echo "<sha>" > /opt/arifos/app/.git_commit`
4. `systemctl restart arifos` to pick up
5. Verify alignment: probe `/health` and confirm `drift: false, status: healthy`

**Real vault defect (do NOT silently fix):** `outcomes.jsonl` may contain multi-line pretty-printed JSON entries at random line numbers (e.g., L31126 starts `{\n  "type": ...`). This violates JSONL spec. The `test_outcomes_jsonl_parseable_majority` test catches it. Fix requires investigating writer session + either re-emitting the lines or cleaning the vault — **T3 territory**, surface to F13.

## 7. litellm-federation :4011 — The Federation Brain

**Observation:** `litellm-federation.service` runs on `127.0.0.1:4011` and exposes 25 model lanes via `/v1/models` (when auth'd). The agent-card registry in `AGENTS_UNIFIED.yaml` declares ~8 FI bindings, but the litellm cascade has **25 active lanes** including canonical agents (apex-888, agi-333, asi-555, i-arif, hermes-asi, openclaw, dispatch, codex, kimi-code, opencode, opencode-go, fed-agent-subagent, fed/audio, fed/vision, fed/image-gen, fed-multimodal-vision, fed-reasoning-heavy, fed-long-context, fed-realtime-voice, gemini-flash, gemini-flash-lite, gemini-pro, zai-pro, asi-555-audio, asi-555-video).

**Probing pattern (always):**
1. `source /root/.secrets/kunci-mas.env`
2. `curl -s --max-time 5 http://127.0.0.1:4011/v1/models -H "Authorization: Bearer $LITELLM_MASTER_KEY"`
3. Parse JSON, count models, list IDs

**End-to-end verification (proves brain is alive, not just declared):**
1. POST to `/v1/chat/completions` with `model: hermes-asi`, `messages: [{role:user, content:"PONG"}]`, `max_tokens: 10`
2. Expect 200 + non-empty usage block (e.g., 193 tokens)
3. The model that serves the call (e.g., `MiniMax-M3`) is reported in the response `model` field

**Implication:** If `tools/list` returns empty on arifOS but `/v1/models` returns 25, the arifOS kernel is alive but the model aliasing is what matters. **Probe the brain, not just the kernel.**

## 8. Gitwrap Multi-Repo Deploy Pattern (AGENTS-AUTONOMY §4-§5)

**Observation:** When a sovereign says "gitwrap deploy all," the correct pattern for federation repos with inherited dirty state:

**Per dirty repo:**
1. `git checkout -b chore/$(date -u +%Y-%m-%d)-<short-topic>`
2. `git add -A && git commit -m "chore(<repo>): capture inherited dirty — <list>" -m "<F2 evidence + F1 reversible note>"`
3. Push with credential helper: `GIT_TERMINAL_PROMPT=0 git -c "credential.helper=!gh auth git-credential" push -u origin <branch>`
4. Create PR: `gh pr create --repo ariffazil/<repo> --base main --head <branch> --title ... --body ...`

**Per AGENTS-AUTONOMY §5 (billing-locked CI):** Admin auto-merge is the only path when CI cannot run.
`gh pr merge <N> --repo ariffazil/<repo> --admin --squash --delete-branch --body "Admin auto-merge: pure topic-branch capture, no functional code-path change. CI billing-locked."`

**For divergent repos** (e.g., WEALTH: 8 ahead, 2 behind origin):
1. Capture divergent commits on topic branch, push via PR
2. After merge, rebase local main onto new origin/main
3. `git rebase origin/main` will auto-drop commits whose patches already upstream (squash collapse)
4. Verify `git rev-list --left-right --count origin/main...HEAD` returns `0\t0`

**Implication:** Never `git stash` or `git reset --hard` inherited dirty state. **Capture, don't discard.** For arifOS specifically, the pre-push guard may block the topic-branch push if the kernel is in drift; clear drift first by writing `/opt/arifos/app/.git_commit`.

## 9. SEAL-without-Verify-Persistence Scar (F11 AUDITABILITY)

**Observation:** Calling `forge_vault mode=receipt` returns `status: SEAL` with a record ID, but the F11 audit trail is incomplete if the agent doesn't probe-after-seal.

**Anti-pattern:** Reporting "SEALED to VAULT999" without verifying the receipt is listable in subsequent probes is F11 incomplete. Future sessions won't trust the seal.

**Fix pattern:** Every seal = two calls (write + read-back). After seal, list the category and verify your record ID appears.

**Implication:** Always probe `forge_vault mode=list category=session.ledger` after sealing, and confirm the record ID is present. If `records[]` is empty, surface as F11 incomplete — do not claim SEAL.

## 10. W3 vs F3 Threshold — Quiet Miss Pattern

**Observation:** arifOS reports `apex_scalars.W3.value = 0.7439` and `runtime_floors.F3.status = pass`. But the F3 floor threshold is `0.75`. The kernel's pass scoring is **rubric-buffered** (multiple inputs to F3), so a raw W3 of 0.7439 can still register as pass.

**Honest framing:**
- W3 = 0.7439 with F3 floor 0.75 = **constitutional debt**, not "amber"
- delta = -0.0061 = -0.81% below threshold
- Lift path requires: graphiti semantic floor enable + langfuse wiring + ml_floors enable + proof_bundle for `se_stage` advance
- All four are T3 surfaces

**Anti-pattern:** Calling 0.7439 "pass" because kernel reports pass is lazy. **Cross-reference** the actual floor value vs threshold; report delta explicitly.

**Implication:** When reporting scalar values from arifOS `/health`, always compare to the floor in the same response. Quote both: `apex_scalars.W3.value` and `runtime_floors.F3` (and any threshold in canonical docs).

---

*Updated: 2026-08-12 by Hermes ASI after hermes-arif session — added 5 runtime observations (deploy gate, federation brain, gitwrap, seal-verify, W3 framing).*
