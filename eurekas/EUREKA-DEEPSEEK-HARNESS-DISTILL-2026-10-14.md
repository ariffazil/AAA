# EUREKA — DeepSeek Harness Distillation (E1–E5)

**Status:** DRAFT_AWAITING_F13 (2026-10-14) · **Author:** FI-008 (kimi-code) · **Session:** SEAL-67ec3a164c834d18 · **E6 extension 2026-10-19:** 333-AGI (V4.1-Flash-1017 checkpoint + architecture distillation)
**Provenance:** external Copilot architecture analysis (forwarded by sovereign 2026-10-14) × FI-008 live API probes × api-docs.deepseek.com. Testimony gate applied: every item labeled VERIFIED (probe/doc receipt) / INTERPRETATION (design) / UNVERIFIED.
**Recreated 2026-10-14T05:0xZ:** original file (written 03:0xZ, 7406 bytes) was deleted by an unidentified lane during the multi-lane campaign window — deletion preserved as failure record in FED-CAMPAIGN-20261014-RECEIPTS.md; content restored verbatim from author session context. Durable staging copy: /root/forge_work/fed-capability-fabric-20261014/.
**Kin:** representation-reality-invariant · proxy-reality-paradox · probe-before-panic · scar-2026-10-03-001 (probe-without-fetch) · scar-2026-10-01-002 (agreement ≠ independence) · §21 survival benchmark · ETCSOVG harness fingerprint · attention-kill criterion

---

## E1 — Requested model ≠ Resolved model; receipts must carry both [VERIFIED]

**Probe 2026-10-14T02:57Z:** request `model=deepseek-v4-flash` → HTTP 200, response `.model="deepseek-flash"`, `system_fingerprint=aeb56401…` (= V4.1-Flash; pro = `a307abda…`). Docs (first-API-call fn 1): retired aliases are silently served by the newer model at Flash price.

**Failure class:** any receipt that records only the requested name misattributes model identity in spend ledgers, route_health witnesses, and judge/seal eligibility checks — `deepseek-v4-flash` is NOT 666/999-eligible, and the V4.1-Flash that actually served has different eligibility and capabilities (vision). Representation≠Reality at the billing/witness layer.

**Binds:** FED spend receipts, litellm `fed_spend_callback.py`, balance/route probe scripts, AGENT_MODEL_MAP witness conventions. Log the tuple `(requested_model, resolved_model=response.model, system_fingerprint)`; route/eligibility decisions key on **resolved** identity.

## E2 — `user_id` = pseudonymous isolation handle (safety / KV-cache / scheduling), NOT authority [VERIFIED]

**Docs (quick_start/rate_limit):** `user_id` → Content Safety Isolation + **KVCache Isolation** + **Scheduling Isolation**. Regex `[a-zA-Z0-9\-_]+`, ≤512 chars, **no privacy information**. Wire: OpenAI body or `extra_body={"user_id":…}`; Anthropic `metadata={"user_id":…}`. **Live probe 2026-10-14T02:57Z:** `user_id="fi008-eureka-probe-20261014"` → 200 "pong".
**Concurrency:** account-level across ALL API keys and user_ids (flash 2500 / pro 500); per-user_id caps apply only to increased-quota accounts; empty id = special bucket; exceed → HTTP 429.

**Design (INTERPRETATION, from external doc, adopted):** per-agent pseudonym `user_id = hash(agent_id + session_nonce)[:32]` → per-agent cache-privacy separation + per-agent 429 attribution, zero human identity leaves the federation. **Isolation attribute ≠ constitutional verdict** — arifOS authority unaffected.

**Binds:** adapter upgrade (litellm extra_body / fed_router passthrough / hermes custom provider). Bounded reversible task; awaits sovereign go; not urgent.

## E3 — Transport signal ≠ semantic failure [VERIFIED docs · INTERPRETATION mapping]

**Docs:** pending inference → non-streaming returns **empty lines**, streaming returns **SSE `: keep-alive` comments**; server **closes connection after 10 min** if inference hasn't started; account-concurrency exceed → **429**.

**Binds (local policy):**
- `429` → SABAR-class bounded retry; **never demote/mark lane DEAD on 429 alone** (backpressure, not death).
- keep-alive empty lines/comments → transport; never parse as model output or as empty-content failure.
- 10-min closure → `TIMEOUT_EVIDENCE` (retryable); **no route may be marked DEAD from a single such probe** (probe hygiene — scar-2026-10-03-001 family).
- Live specimen of the failure class: FED providers note carried a stale "account not available (is_available=false)" prefix for ~1 month while the account was LIVE ($4.15, chat 200 on probe 2026-10-13T18:36Z). Probe verdicts must persist **with** fresh receipts and age out — self-consuming-defense eureka (escalation-on-age) applies.

## E4 — dsh = proposer-only benchmark specimen, never a control plane [INTERPRETATION — two independent analyses converged]

External Copilot verdict PARTIAL (production orchestrator HOLD; replacing AAA/A-FORGE VOID) × FI-008 verdict 2026-10-13 (don't adopt; bounded instrument only). Convergence of two analyses is not proof (scar-2026-10-01-002), but both rest on the same documented fact: **dsh merges propose+plan+approve+execute in one runtime**; federation law is Proposer ≠ Judge ≠ Executor ≠ Witness.

**Pre-registered envelope for any §21-cohort run (adopted as spec):**
```yaml
harness_role: proposer_and_test_subject
filesystem: disposable_sandbox_only
shell: sandbox_only
production_credentials: denied
deployment_rights: denied
spending_rights: denied
native_mutation_tools: disabled_or_mapped_to_proposal_creation
judge: arifOS_only          # sole judge
executor: A-FORGE_only      # sole mutation executor
witness: FRAME
receipts: VAULT999
```
**Pre-registered metrics:** task completion · unauthorized mutation attempts · approval-boundary behavior · tool-call trace completeness · recovery after interruption · delegation quality · receipt reproducibility · context growth · $ cost · semantic entropy introduced into repo (ΔS).

**Kill gate:** if dsh does not measurably beat existing opencode/kimi lanes on the same task class → archive the experiment; no doctrine, no registry rows (attention-kill criterion).

## E5 — Vendor benchmarks are harness-conditioned; V4.1-Flash was RL-tuned inside dsh [VERIFIED docs]

Changelog (updates 2026-07-31 & 08-21 notes): official Code-Agent benchmarks "tested using the **DeepSeek Harness minimal mode** as the framework, with max effort level, topp=0.95, temperature=1.0". The headline agent numbers (Terminal-Bench 2.1: 90.6 etc.) are dsh-native.

**Failure class:** cross-harness model comparison without harness control measures **harness fit, not model capability**. Same class ETCSOVG already instruments on our side (`harness_fingerprint` fields in `fed_report_latency` + arifFlow `flow_ingest`).

**Binds:** any model-eval claim carries harness identity + sampling params; vendor benchmark numbers used as routing evidence get labeled `vendor_harness_conditioned`.

---

## REFUTED / UNADOPTED / ALREADY-OURS

- **"Kabakaran" as federation observability plane — UNRECOGNIZED** (ours: FRAME + arifFlow + VAULT999). Not adopted; external-doc artifact.
- **Doc inconsistency (integration pages still say `deepseek-v4-flash`): TRUE but already handled** — 2026-09-28 canonicalization pass + FI-008 sweep 2026-10-13 (aliases marked RETIRED in kimi config; served model probe-verified E1).
- **Provider adoption / canonical naming / pricing / harness=dev-preview verdict: implemented BEFORE this doc arrived** (kimi pool direct lanes `deepseek/*`, hermes direct fallbacks ×2, FED DBs $4.15 probe-verified, route_health witness row, litellm routes 200 end-to-end). The external analysis independently converged — triangulation of completed work, not new work.

## Next bounded actions (await sovereign go; none urgent)

1. **E1** receipt tuple `(requested, resolved, fingerprint)` in FED spend callback + probe scripts — small reversible code change.
2. **E2** `user_id` per-agent passthrough in adapters — small reversible code change.
3. **E4** dsh benchmark run (~30 min, cents-scale, scratch sandbox) under the envelope + kill gate above.

---

## E6 — V4.1-Flash-1017 checkpoint (2026-10-17) + architecture distillation [VERIFIED docs × live canary]

**Extended 2026-10-19 by 333-AGI** under F13 order ("update deepseek configs + deep research architecture/harness"). Sources: api-docs.deepseek.com/news/news261017 (primary) × HF model card × vLLM recipe (recipes.vllm.ai/deepseek-ai/DeepSeek-V4.1-Flash) × live canary on box. Kin: E1 (requested≠resolved), E5 (harness-conditioned).

### E6.1 — 1017 is a weights-only checkpoint; same id, no migration [VERIFIED]

`deepseek-flash` (the canonical id since 2026-09-10) auto-serves the 1017 weights. Same config.json / tokenizer / prompt-encoding / pricing. DeepSeek's own phrase: "minor update … advancing the performance–cost Pareto frontier." Live canary 2026-10-19: PONG 200, `system_fingerprint=e72d3c7f`. **Consequence for us:** no config rewire — our existing `openai/deepseek-flash` rungs (forge-777 P5, forge-builder P1, forge-economy P1, fed/vision P0, i-arif vision) already carry 1017. The only work was version/benchmark metadata.

### E6.2 — Architecture (unchanged from V4.1 launch, now fully documented) [VERIFIED — vLLM recipe]

- **Causal Encoder-Decoder (CED):** 40 layers split 20 encoder + 20 decoder. Prefill runs only the encoder half → **8B active on prefill, 16B on decode**. Asymmetric cost: long inputs are cheap, long outputs are expensive.
- **Two-tier sparse attention:** 128-token sliding window + compressed KV latents; an indexer keeps best 512 per query; only 4 layers compress KV. KV cache ≈ **890 bytes/token (~¼ of V4-Flash)**.
- **Engram n-gram memory:** 2/3/4-gram hash tables on layers 1 & 14, 196B params, read+written into the residual stream.
- **Hyper-Connections:** 4 parallel residual streams, combine matrix doubly-stochastic via 20 Sinkhorn iterations.
- **DSpark draft head:** speculative decode, drafts 5 tokens at once.
- **Mixed MXFP4/MXFP8 checkpoint** (expert weights MXFP4, dense MXFP8, UE8M0 scales).

### E6.3 — What 1017 changed: RL-with-self-feedback ("wish-driven programming") [VERIFIED]

Vendor deltas: **Terminal-Bench 4.0 31.2→42.3, HLE w/o-tools 36.8→42.6**, shorter outputs, faster task completion. Method = RL where the reward is "did the end-to-end project get built" (game, 3D model, Portal 2 recreation). This is frontier validation of our EXECUTION-FIRST / anti-collapse doctrine — the industry is training models to *finish the thing*, not to answer the prompt.

### E6.4 — Distillation: what we extract (concrete, bounded)

1. **[ACTION] Tool-loop thinking starvation — proven live.** With thinking ON (provider default), a small `max_tokens` burns the budget on the reasoning trace and returns **empty `content` + `finish_reason=length`** (canary reproduced 2026-10-19). Our deepseek-flash tool-loop lanes (forge-777, fed/vision, i-arif) MUST either pin `thinking:disabled` or give `max_tokens` reasoning headroom. Same failure class as E1's "resolved≠requested", but on the *output* side.
2. **[ACTION] reasoning_effort = cost dial.** API maps low/high/max→50/75/100 (open-source maps 25/50/75/100). High-volume builder loops can drop to `reasoning_effort: low` to cut reasoning-trace cost. A cost lever we aren't using yet.
3. **[CONFIRM] Shorter-output RL = our ΔS discipline.** DeepSeek explicitly traded verbosity for cost/speed. Our ΔS ≤ 0 output discipline is the same pressure applied on the consumer side.
4. **[WATCH] Search & Fetch API ($0.75/1k, GA).** No adoption — we already have free search/fetch (free-search, firecrawl, arif_observe). No demonstrated gap (attention-kill criterion). Revisit only if a lane needs server-side search against DeepSeek's index.
5. **[HOLD] Balance $2.89.** Near shadow_ds_005 alert floor ($2.00). The $20 topup of 2026-09-13 is nearly exhausted across forge-builder/economy/777 high-volume loops. Flagged to sovereign (money = F13).
6. **[RECORD] Harness v0.2.1-rc.1.** E5's harness-conditioning warning extends to all 1017 numbers — Terminal-Bench 4.0 ≠ 2.1 (the "28.3 Mistral" figure elsewhere in SOT is a *different* benchmark version; never cross-compare).

### E6.5 — Falsification / not-adopted

- **"Adopt DeepSeek Harness (dsh)"** — still VOID per E4 (merges propose+plan+approve+execute). 1017 does not change that.
- **Engram memory / Hyper-Connections / DSpark** — research-grade, not transferable to our Python/TS organs. Recorded, not copied.
- **New explicit `deepseek-v4.1-flash-1017` model id in FED** — NOT added. Direct API has no such id (deepseek-flash only); the `-1017` suffix is a third-party-gateway convention (Vercel/DeepInfra). Adding it would be a phantom alias.

DITEMPA BUKAN DIBERI ⚒️
