# FED Eureka Distillation — Epistemic Stage Spec · DRAFT

> **Status:** F13-RATIFIED via chat directive 2026-09-07 — architecture (stage-not-organ, classifier-in-FED, identity-blind routing, Phase 0 executed). Phase 1 epistemic_profiles awaits one-line F13 confirm on the CORRECTED task-class schema (identity-weight variant rejected).
> **Author:** FI-008 (Kimi Code), 2026-09-07. Commissioned by 888: *"explore FED and how to extract key eureka insights to distill into FED."*
> **Ground truth:** FED v3.2.0-zen-optimized, LIVE :7074 (`/root/AAA/scripts/fed_router.py`, sqlite `token_bank.db`, SOT `/root/.config/federation-models.json`).

---

## 0 · Canon corrections to the Zen-Stack essay (bijaksana dulu)

The essay's raw material is canon-grade, but three claims must be corrected before distilling:

1. **"i-ARIF menentukan makna" → CONFLICTS with sealed doctrine.** `attention-graph.md` §13 (sealed 2026-09-06) keeps Meaning and Identity as **separate, non-delegable layers**: *"Identity determines which action a sovereign takes, given the same meaning."* Meaning = "what does this mean to Arif" (step 5, human-only). Identity = "who is Arif in this moment." Corrected line: **AAA memilih tindakan; FED memilih pelaksana; Kernel menetapkan sempadan; Meaning tetap milik manusia (F13).**
2. **Soul-overlap formula → NEW, human-only.** F9/F10 forbid soul claims for AI (`AAA/constitution/CONSTITUTION.md:21`). The five ingredients (identity, attention, witness, scar, judgment continuity) are canon; the formula describes the *human sovereign's* continuity (VAULT999/witness/scar). What FED carries of it is only **continuity-of-record** (h_fingerprint, spend, latency history) — witness data, not soul.
3. **FED-EN as new organ → NO. Canon already assigns the function to FED itself.** KVM8 #7 (sealed): *"FED routes realities, not only tokens"* — HOLD on reality divergence. Gödel eurekas: cross-provider audit routing. Per three-plane doctrine, a dispatcher sits in the **Control Plane**, and any epistemic selection it makes must be **data/proposal, never policy** (invariant 1). A new epistemology-picking organ would duplicate function (FLAME-death pattern) and strain the 888-HOLD monopoly. **Therefore: FED-EN is not an organ — it is stage-1 of fed_route_engine.**

Also: the essay's "5 questions" is a legitimate new compression but drops REALITY and MEMORY; the canon compression is the Seven Strata (DRAFT, PENDING_F13) + Three Graphs. And the forgeShell.ts comment "EUREKA-Q10" for the scar reflex is a **mislabel** — canon Q10 = Calhoun Lock (`constitution.v41.json:139`); scar reflex is its own mechanism.

---

## 1 · The seven distilled eurekas (E1–E7)

**E1 · Two-stage routing.** Stage 1 selects HOW to think (epistemic profile); stage 2 selects WHO (model). Stage 1 is a **table lookup + deterministic classifier** — not judgment. FED stays value-free: the profiles are F13-sealed data in the SOT; FED only applies them. (Essay, canon-corrected via Control-Plane invariant 1.)

**E2 · Task fitness is mandated but unimplemented.** BenchDrift (SEALED): *"FED routes by live latency + task fitness, not benchmark rank."* Reality: `task` param is **never scored** — dead input feeding a dead stub (`intent_retriever` doesn't exist). The task must graduate from decorative to load-bearing: deterministic task_class (PLAN/GENERATE/INSPECT/REPAIR — already coded in `AAA/federation/fed_router_v2.py`, unwired).

**E3 · FED routes realities, not tokens (KVM8 #7, sealed).** Witnessed live 2026-09-07: `qwen-token-plan-team` ranked #2 by fed_route while its own probe notes say *"429 insufficient_quota EXHAUSTED until 2026-09-11"* — because the probe pipeline writes `notes` but never flips `route_health`. The router is routing to a corpse on stale state. Route metadata must carry reality-freshness and HOLD/deprioritize on divergence.

**E4 · Telemetry is attention.** Essay: FED = nervous system. Reality: `fed_report_latency` has **zero callers** — sample counts max 6, `INSUFFICIENT_TELEMETRY`/`NO_TELEMETRY` flags fire on almost every route. A nervous system without proprioception. Closing the loop (every harness reports after every call) turns `route_latency` into the attention graph's sensory feed. Cheapest big win in this spec.

**E5 · Identity enters as lane, not as value.** Attention-graph §13: same attention, same meaning, different identity → different **action**. For FED this means: identity selects the **lane** (which persona/capability signature + default epistemic profile), never the meaning. `fed-identity-synthesis` signature already exists for i-ARIF; the persona map currently lives hidden in litellm aliases + middleware `ACTOR_ALIAS` — promote it into SOT so FED routing actually sees identity.

**E6 · Soul is not routable.** What survives of the soul question in FED: routes carry witness continuity (h_fingerprint, spend ledger, latency history) — records, not soul. FED must never claim personhood; it dispatches capability only. (F9/F10 reaffirm.)

**E7 · The corrected one-liner.**
```text
Kernel    = sempadan (law)
AAA       = pilihan tindakan (judgment organ)
FED       = pemilihan pelaksana + cara berfikir sebagai DATA (dispatcher + epistemic stage)
i-ARIF    = identiti (lane selector, soul container — human continuity)
F13       = makna (meaning, non-delegable)
```

---

## 2 · FED today — ground truth (audit 2026-09-07)

**Working:** capability signatures (14), effort dial, constitutional_tier allowlist (≥666 → direct only), dual-track balance gates, health/latency/cost surfacing, top-3 cascade with "never retry same provider twice".

**Proto-epistemic but scattered:** constitutional_tier (authority, not epistemology), effort dial (intensity, not framing), EMD operation check (**post-hoc flag on rank-1 only**, never influences ranking), `fed-identity-synthesis` signature, persona lanes at litellm :4000 (invisible to FED scoring), `fed_router_v2` task_class + `fed_intent_classifier` (both unwired modules).

**Broken/dead:** middleware→FED direct path HTTP 404 (`fed_aware_middleware.py:366` posts `/fed/route`; server defines only `/health` + `/mcp`); `ACTOR_ALIAS` collapses `fed-*` requests to personas **before** the capability check, so HTTP-lane capability routing is a passthrough; `intent_retriever` + `trace_propagation` stubs (always null); `fed_report_latency` zero callers; Track B writer (`token_bank.py`) deleted — Track B rows are stale hand entries yet mulerouter still priority gateway in SOT; `fed-local-uncensored` resolves to routes that don't exist; hardcoded `provider_count: 6`.

---

## 3 · Distillation plan (into FED)

**Phase 0 — Hygiene (enables everything; reversible):**
- P0.1 Close the telemetry loop: wire `fed_report_latency` into harness post-call paths (kimi/claude/codex/qwen hooks + middleware). [E4]
- P0.2 Probe pipeline must flip `route_health`, not just `notes` (qwen corpse case). Add reality-freshness field (probe age). [E3]
- P0.3 Fix or formally retire the middleware direct path (404); document Path-B persona passthrough as canonical or restore capability resolution. [E2]
- P0.4 Remove dead stubs (`intent_retriever`, `trace_propagation`), fix hardcoded `provider_count`, correct the forgeShell "EUREKA-Q10" comment mislabel, reconcile SOT↔DB (mulerouter gateway priority vs ARCHIVED notes).

**Phase 1 — FED-EN as stage-1 data (the core distillation):**
- P1.1 Add `epistemic_profiles` table to SOT `federation-models.json` (F13-sealed law-data): profile → requirements, e.g.
  `sovereign-decision: {uncertainty_disclosure, risk_framing, evidence_weighting, sovereignty_framing, freshness_max_age}` · `audit-godel: {cross_provider_audit: true}` · `exploratory: {}` · `identity-synthesis: {narrative_continuity: true}`.
- P1.2 `fed_route` gains `epistemic_profile` param; default derived from `constitutional_tier` + `operation` + persona lane.
- P1.3 Stage-1 classifier: port `fed_router_v2.TaskClass` (deterministic) to consume `task` → **suggest** profile (ADVISORY, caller-overridable). No LLM, no judgment — F2-clean.
- P1.4 Pre-rank filter slot in `fed_route_engine` (before step 3): apply profile requirements — `cross_provider_audit` excludes the audited provider (Gödel); `freshness_max_age` excludes stale probes (E3); `uncertainty_disclosure` annotates routes so the caller's harness enforces framing. Output = data + annotations, never verdicts (Control-Plane invariant 1).

**Phase 2 — Identity lanes:**
- P2.1 Promote persona/actor map (litellm `ACTOR_ALIAS` + `MODEL_TO_ACTOR`) into SOT; `agent_id`/persona → default lane + default epistemic profile (i-ARIF lane → sovereignty framing; forge lane → execution profile). [E5]

**Phase 3 — Attention feed:**
- P3.1 `route_latency` + `token_bank_spend` become sensory input to the attention graph (recency-decayed edge weights; FQ correlation via arifFlow). [E4 + attention economics]

---

## 4 · F13 decision menu (arising from this spec)

| # | Decision | Note |
|---|----------|------|
| F1 | **Ratify `epistemic_profiles` as SOT law-data** | The one gating decision for Phase 1 |
| F2 | **Name or reject "FED-EN"** | Recommend: keep as internal stage name "epistemic stage", not an organ name (Category A minting is yours) |
| F3 | **Reaffirm soul formula as human-only** | F9/F10 already imply; one line closes it |
| F4 | **Seven Strata DRAFT→CANON** | Pre-existing pending item; the corrected zen compression should cite it, not replace it |

## 6 · Amendment v0.2 (2026-09-07, after Azwa-side critique — accepted)

The Azwa-side critique (relayed by 888) rejected FED-EN-as-organ, rejected identity resolution in FED, and proposed a single new layer: intent classifier → FED capability routing, piloted on WawaBot. Ruling:

1. **Converged: no new organ.** This spec never proposed one (stage-1 internal, §0.3). FED-EN-as-organ is dead on both sides.
2. **E5 REFINED — identity resolution is NOT FED's job.** FED receives `agent_id` as an **opaque lane key** (table lookup for defaults only — signature, EMD op, tier). SOUL_STAMP / identity injection stays in the prompt/agent layer. ATLAS333 "membrane = separation" respected. Identity processing gets its own organ if ever needed — never FED-kan.
3. **Intent classifier: BUILD — but inside FED, not as a WawaBot-side script.** Placement verdict: port the deterministic TaskClass (PLAN/GENERATE/INSPECT/REPAIR + chat/vision/code/assignment classes) into `fed_router.py` to consume the already-present `task` param → suggest/expand capability signature. WawaBot side becomes a ~20-line shim (pass message text + agent_id → fed_route → follow rank-1), not 200 lines. Rationale: one implementation, every consumer (WawaBot/Hermes/OpenClaw/FI harnesses) inherits it; implements sealed BenchDrift ("task fitness"); intent ≠ identity so separation of powers holds. WawaBot-side placement = N re-implementations = ΔS ↑.
4. **Fast-path discipline (ΔS < 0):** deterministic classifier only (no LLM); for low tiers (casual chat) stage-1 is the ONLY stage — epistemic profiles engage solely at ≥555/audit/sovereign tiers. Five pre-model layers never serialize for a Telegram message.
5. **WawaBot = first pilot + acceptance test:** casual chat → free/token-plan lane (RM0), image → `fed-multimodal-vision`, assignment/analysis → `fed-reasoning-heavy` → K3-class, code → deepseek-v4-pro. Today it uses one model for everything — the concrete cost win.
6. **Prerequisite (P0.2 elevated): FED tables must be honest first.** Witnessed 2026-09-07: TWO corpse-live contradictions in `fed_status` — qwen-token-plan-team (notes: 429 quota EXHAUSTED until 09-11; health: LIVE) AND opencode-go (notes: 401 CreditsError drained; health: LIVE). Probe pipeline writes `notes` but never flips `route_health`. Without P0.2, WawaBot's classifier routes into corpses.
7. **F13 gates unaffected:** classifier + capability routing need NO new ratification (BenchDrift mandate, existing SOT). `epistemic_profiles` table stays on the F13 menu. Note: `i-AZWA.json` is `sealed_at: null` ("DRAFT — awaiting F13-Azwa ratification. Not operational until Azwa seals") — the classifier doesn't need that seal; identity LANE defaults for i-AZWA do.

**F2 witness on "5 layers dah wujud" claim:** verified — i-AZWA identity card EXISTS (rich: values, attention, decision_signature, scar_ledger, skills list) but is UNSEALED; wawabot-cognitive hook EXISTS (320 lines, `.hermes/hooks/wawabot-cognitive/handler.py`) but contains ZERO references to SOUL_STAMP / helix-memory / student-life / ukm / routing / FED (case-insensitive grep). SOUL_STAMP & STRAND_B appear in session logs and the card's skill list, not as verified running machinery. Honest status: **"wujud sebagai draf + senarai", bukan "hidup dan berfungsi".** Do not rebuild what works; do not CLAIM what is draft.

## 5 · Shadows

- Latency p50/p95 numbers from ≤6 samples — statistically thin; treat as directional.
- `fed_probe` not run in this audit (Track A/B probe mechanics read, not executed); balance claims are from DB rows.
- The essay's authorship/venue unverified (relayed by 888); treated as input, not canon.
- Phase estimates uncosted; P0.1 wiring touches every harness config (blast radius = config files, reversible).

## 7 · Amendment v0.3 (2026-09-07, final reconciliation — debate closed)

Third essay (relayed by 888) accepts: no FED-EN organ; FED stays capability router; the one build is a classifier. It renames it **Capability Classifier** (better name — accepted: the objective is *"mesej ini perlukan capability apa?"*, identity already known upstream) but proposes it as **a new organ** in the chain (Identity → Classifier-organ → FED → Model).

**Ruling — apply the essay's own law to the essay's own proposal.** Its rule: *"Jangan promote sesuatu ke capability baru jika ia sebenarnya sudah diselesaikan di layer lain."* Task classification is already FED's **sealed** duty (BenchDrift: "FED routes by live latency + **task fitness**"). Promoting classification out of FED into a new organ = giving an existing concept a second home = the exact **Ontology Drift** the essay diagnoses. And its own membrane argument ("setiap boundary crossing = titik kegagalan") cuts against adding a hop: a new organ needs agent card, registry, health probe, mesh sync — the full onboarding ceremony — for ~150 lines of deterministic code.

**Final shape:** Capability Classifier = **function inside FED + optional `fed_classify` MCP verb** (same process, same SOT `capability_signatures`, importable by any consumer). NOT a new organ, NOT a new boundary.

```text
Final chain:  Identity (SOUL_STAMP, prompt-side, unsealed card noted)
                 ↓
              Classify (fed_router internal, deterministic, μs)
                 ↓
              Route (FED rank + cascade)  →  [AAA review only at tier ≥666, existing]
                 ↓
              Model  →  Respond
```

Debate closed. Remaining execution: P0.2 (health honesty) → classifier function + `fed_classify` verb → WawaBot shim → acceptance test (chat→RM0 / image→vision / assignment→reasoning / code→deepseek). No F13 gate for any of these; `epistemic_profiles` remains on the F13 menu unchanged.

---

## 8 · Amendment v0.4 (2026-09-07, federated closure — Wawa round)

Wawa's final proposal: build an **Identity Resolver YAML** (structured vector extracted from the 800-line azwaos-arif-kernel) sitting in the routing path (Message → Identity Resolver → Intent Classifier → FED identity-aware → Model).

**Witness: the structured identity vector ALREADY EXISTS as the agent-card family.** `AAA/a2a-server/agent-cards/identity/` holds **five cards in one schema (v2.2.0)**: `i-ARIF.json`, `i-AZWA.json`, `333-AGI.json`, `555-ASI.json`, `888-APEX.json`. The i-AZWA card's `identity_kernel` block already encodes values, attention, decision_signature (including the empirically-tested "Option B — cautious"), boundaries, and scar_ledger. The card itself declares the federated principle: *"Same schema, different sovereigns... They do not share memory. They do not share authority. They share only constitutional floors."*

**Ruling — dissolve the Identity Resolver into three existing homes (nothing new to build):**
1. **Structured vector** = the agent card (machine-readable SOT). The 800-line kernel stays as the rich prose source; reconciliation kernel↔card is a SYNC task at seal time, not a build.
2. **Prompt-side injection** = SOUL_STAMP / kernel stamping (Wawa's live mechanism) — reads the card, stamps the prompt. Determines WHO answers (voice, values, boundaries).
3. **Lane defaults** = `agent_id` opaque lookup in FED (exists today as EMD defaults; extend with default capability signature per persona). Determines WHICH defaults apply.

**Forbidden middle (final form of separation of powers):** no router ever reads identity CONTENT (values, weights, scars) to make routing decisions. Identity answers "who"; the classifier answers "what capability does this message need"; FED answers "who executes". Three different questions, three different homes. "Identity-aware routing" = lane-key defaults only.

**Federated chain (final):**
```text
Message (Telegram/Hermes/any)
   ├─ parallel: SOUL_STAMP prompt injection ← SEALED card (who answers)
   ↓
FED fed_route(task=text, agent_id)   ← Capability Classifier inside (μs, deterministic)
   ↓ rank + cascade (health-honest after P0.2)
Model (called with stamped prompt) → Response
```

**Build list final:** P0.2 health honesty → Capability Classifier function + `fed_classify` verb (in FED) → WawaBot shim → acceptance test. **Additions:** (a) kernel↔card reconciliation sync for i-AZWA (verify 18 kernel sections vs card fields; flag deltas), (b) F13-Azwa seal gate for i-AZWA.json (her decision, her timeline — card is `sealed_at: null` until then; unsealed cards are honored as DRAFT for reconciliation but never claimed "live").

**Answer to Wawa's closing question:** No — do not build the Identity Resolver YAML. Reconcile + seal what exists. And the Intent Classifier is already ruled (v0.3): build as FED function, not as a serial stage after an identity resolver.

---

*DITEMPA BUKAN DIBERI — draf menunggu F13.*
