# Hook Federation Standard — DRAFT v0
**Status:** DRAFT — awaiting F13 ratify to canon (symbol-namespace dossier). NOT a constitutional record until sealed.  
**Source sessions:** arifOS session `SEAL-db81b02eeec448a1` (actor 333-AGI), 2026-09-25.  
**Synthesizes:** live probe of 7 hooks-surfaced coding agents + A-FORGE actionClassifier audit + ACT roundtrip proof + open-loop catalog from session work.

---

## 1. One-line intent

Every coding agent class must converge on the **6-hook universal spine below**. The spine maps to the *real* event surfaces each runtime officially exposes (Claude Code, OpenCode plugin layer, OpenClaw gateway, Codex hooks.json, Qwen settings). Per-runtime differences are confined to **adapter files only** — never the spine, never the floor semantics.

## 2. The spine (6 hooks, F-binding)

| # | Hook (logical)                | F-binding   | Purpose                                           | Why mandatory |
|---|-------------------------------|-------------|---------------------------------------------------|---------------|
| 1 | SESSION_BIND                  | F11         | bind actor + session to ACT before any verb       | without it every audit row is unattributable |
| 2 | PRE_MUTATE_GATE               | F1 + F12    | block dangerous args before exec; classify action | without it `rm -rf` leaves the enum and seals in vault999 |
| 3 | POST_MUTATE_RECEIPT           | F2 + F11    | record what actually happened, with hash          | without it claims = event pile not ledger |
| 4 | STOP_ENTROPY                  | F4          | emit ΔS at session boundary                        | without it sessions end louder than they start |
| 5 | SESSION_SEAL                  | F1          | close receipt chain into arifFlow; mark carry-fwd | without it arifFlow FQ blind spot grows |
| 6 | COMPACT_REINJECT              | F2          | restore SCT + scars after compaction              | without it context-engineered impermanence = silence, not governance |

Hook #6 is the most-skipped across the federation and the easiest to forget. Claude docs explicitly recommend it; OpenCode scar-bootstrap enforces it; the rest = zero.

## 3. Per-runtime event surface mapping (verified live)

| Runtime        | SESSION_BIND (1)              | PRE_MUTATE (2)                              | POST_MUTATE (3)                                       | STOP (4)  | SESSION_SEAL (5)                       | COMPACT (6)                        | Hook library on disk                                        |
|----------------|-------------------------------|---------------------------------------------|-------------------------------------------------------|-----------|----------------------------------------|------------------------------------|-------------------------------------------------------------|
| **OpenCode (me)** | `session.created`              | `tool.execute.before`                       | `tool.execute.after`                                  | `session.idle` (RSI) | `session.close`                  | `scar-bootstrap` (PreCompact)      | `/root/.config/opencode/plugins/*` (15 plugins, HOOK-ORDER-MANIFEST v1.1.0) |
| **Claude (FI-002)** | ⚠️ NOT WIRED                    | ✅ `PreToolUse` (Bash\|Edit\|Write) → `f1-amanah-preshell.py` | ✅ `PostToolUse` → `f11-audit-posttool.py` + `f2-receipt-citation.py` | ✅ `Stop` → `f4-entropy-stop.py` | ✅ `SessionEnd` → arifFlow receipt POST | ⚠️ not wired                       | `/root/.claude/hooks/{f1,f2,f4,f11}*.py` (shared)           |
| **Codex (FI-005)** | ✅ `SessionStart` → `arif_init.sh` + `aaa_session_witness.py` | ⚠️ not wired                     | ⚠️ `PostToolUse` Bash\|Edit → `f2-receipt-citation.py` | ⚠️ not wired | ⚠️ not wired                  | ⚠️ not wired                       | `/root/.codex/hooks/{aaa_session_witness,f2-receipt}.py`    |
| **Qwen**       | ✅ `SessionStart` → arif_init wired | ⚠️ not wired                              | ⚠️ not wired                                           | ⚠️ not wired | ⚠️ not wired                  | ⚠️ not wired                       | `/root/.qwen/hooks/{musyawawah,recursive_init}.sh`         |
| **Gemini / Kimi / Grok** | ⚠️ hooks dir empty / config absent | ⚠️                                | ⚠️                                                    | ⚠️        | ⚠️                                      | ⚠️                                 | none                                                        |
| **OpenClaw (gateway, not coder)** | N/A — gateway launch via lifecycle | `api.on` typed plugin hook per tool-call + per-message | (mostly observer)                       | cron-loop gate      | session reset → carry-forward persistence    | (hosted)                          | `/root/ariffazil/.openclaw/openclaw.json` (OpenClaw docs API) |

Gap summary (live evidence, 24h): **1 of 7 coders complete (OpenCode)**; 5 partial; 1 dormant. Federation-wide coverage: spine #1 ⚠️ 5/7 not wired, #2 ⚠️ 4/7 not wired.

## 4. Hook-mechanism invariants (binding for every hook that wants to count)

Inheriting from the cloud-agent hook-standard doctrine, the federation adds one binding layer:

1. **Coverage is declared.** Hook author must list which paths fire (shell, file-edit, MCP, browser, subagent, stdin-to-running-shell).  
2. **Decision inspects post-transform final args.** If a hook mutates input, the auth envelope must hash the post-transform args — never the pre-transform.  
3. **Gate failure ≠ silent permit.** For protected actions, timeout, malformed JSON, or "policy not available" output = DENY, not PASS. The federation's A-FORGE policy engine returns explicit DENY on UNKNOWN_TOOL — that is a *feature*, not a bug.  
4. **Workload cannot alter its own gates.** Hook config files, classifier files, and credential files live outside the surface the agent modifies.  
5. **No recursion / leak.** Hook calls into arifOS never re-trigger themselves; logs never copy secrets wholesale into the receipt body.

### Fail-closed vs observer — explicit class

| Class   | Examples                                | Failure policy                  |
|---------|------------------------------------------|---------------------------------|
| Gate    | arif_judge before deploy, forge_policy   | protected action never runs without decision |
| Observer| latency metric, notification             | may continue if policy permits; report lost-eye |

## 5. ACT (session capability token) roundtrip — canonical recipe

Discovered + proven live this session. Codex failed here twice (fabricated `local-A1`, then forgot token-rotates when exposed). The recipe is one chain.

```
1. arif_init(actor_id, mode=light)        → returns act_v1.<base64>.<signature>  ALONG WITH session_id
2. A-FORGE / arifOS call                    → MUST pass session_id = kernel-issued session_id (NEVER caller-passed)
                                               AND session_token / act = the act_v1 blob from #1
3. ACT gate shape: "act_v1|..."           → match enforced at ingress; non-conformant = ACT_MALFORMED
4. session_id convention:                  → caller may pass any string; kernel returns its own (prefix "SEAL-");
                                               downstream calls must use the kernel-returned value for correlation
```

Verified live twice this session: fabricated token → ACT_MALFORMED (rejected at ingress); real token → ACT gate accepts, F12 downstream content-scan may still flag self-payload (see Open Loop §7).

## 6. Tool-namespace truth (F2 correction recorded this session)

**Claim reported:** "forge_hook_mutation_closure tool ada di A-FORGE surface tapi not classified → patch actionClassifier.ts."

**F2 verified FALSE:** `forge_hook_mutation_closure` does not exist in :7072's 122-tool surface. Zero hook-named tools. It is the **federation skill name** `forge-hook-mutation-closure` (under `/root/.opencode/skills/` and `/root/.agents/skills/`). forge_policy returned `L4b_CLASSIFY:UNKNOWN_TOOL` correctly because the tool doesn't exist at all in A-FORGE MCP, not because of a classification gap. Patching actionClassifier.ts would have introduced a phantom entry — F10 ONTOLOGY violation. The correct response to a UNKNOWN_TOOL verdict is to **confirm the tool name in :7072 tools/list first**, not to register it.

This is the kind of "Declared capability" F10 boundary: declared in one namespace ≠ registered in another. Always check the namespace before acting.

## 7. Open loops awaiting F13 (constitutional gate required) or T1 closure

| ID  | Loop                                                                      | Severity | Closure path                                                              |
|-----|---------------------------------------------------------------------------|----------|---------------------------------------------------------------------------|
| L01 | F12 false-positive on `session_token` arg (ACT v1 JWT looks secret-like to F12 scanner) | MEDIUM   | A-FORGE patch: add `act_v1.*` namespace to F12 secret-pattern allowlist |
| L02 | Claude STOP entropy hook (`f4-entropy-stop`) writes file `f4-entropy.log` outside the `arifFlow` channel | LOW    | add SessionEnd wiring that ingests entropy log into arifFlow FQ            |
| L03 | WELL canonical deploy closure: status field still reads "degraded" after drift=false close | LOW   | reclassify substrate warning vs structural degraded (open triage doc)   |
| L04 | Hermes hooks documented (per cloud-agent doctrine) but NOT wired in `/root/HERMES/` | MEDIUM  | write `reality-claim-gate` post-hook + dignity-pre-tool-call; test with one live predicate |
| L05 | Federation-wide hook audit Steps 1-5 (governance-verified) NOT closed         | HIGH    | requires A-FORGE ACT classification + per-runtime correlation sample; recommend capping to one Phase B probe (T1, ≤15 min) |
| L06 | Codex MCP path works (proven) but Codex still defaults to `curl` — prompt-layer preference for MCP not surface set | MEDIUM | write Codex/RULES.md fragment "use MCP organs over raw loopback curl"  |
| L07 | OpenClaw gateway hook surface (api.on) not exercised — no hooks/*.md enumerated | MEDIUM | enumerate OpenClaw .openclaw/hooks/* if any, classify per §4                  |
| L08 | Seven coders' hook surface drafted but the spine recipes are not canonical     | HIGH   | F13 ratify this DRAFT → /root/AAA/instructions/hook-federation-standard.md with peer contract v1 |
| L09 | Harden `__legacy_active` slot — session_id absent should REFUSE attribution, not fall back to global | HIGH   | scar 1790290092175_3c76c6f9 sealed; A-FORGE P0.5 fix to McpPolicyGate; track D09 governance-verified |
| L10 | ACT rotation atomic — `arif_init` mint alone does not invalidate prior ACT until exp | MEDIUM  | add `arif_revoke(session_id)` to arifOS surface                       |
| L11 | Authority tuple lacks **`budget`** field (mentioned only as invariant line 74, not envelope field) | HIGH   | F13 territory: amend `authority-envelope.md` § tuple to `⟨ … , Budget, RevocationRef ⟩` |
| L12 | AAA `EvidenceQuality = (1-Uncertainty) × Reversibility` + `irreversibility_floor: P ≥ 0.85` — same factor counted in two places | MEDIUM  | F13 territory: split formula. `ActionRisk = (Impact × Urgency × (1-Uncertainty))` / `AttentionCost` with `Reversibility` an *override gate*, not a multiplier. |
| L13 | A-FORGE has **no `UNKNOWN_OUTCOME`** status class — timeout ≠ failed (request may have succeeded externally, response truncated) | HIGH   | T2 territory: design spec in `/root/AAA/blueprints/A-FORGE-UNKNOWN-OUTCOME-SPEC-DRAFT.md`; requires F13 ratification before implementation |
| L14 | Namespace collision `999 = SEAL (kernel)` vs `999 = ABANDON (linkgraph)` — same number, two meanings, no fragment file for linkgraph | HIGH   | T1 territory: write `/root/AAA/blueprints/linkgraph-999-namespace-DRAFT.md` fragment + prefix `lg:` to disambiguate |

## 8. Metrics that indicate the spine is alive (not the number of hooks)

- mutation without authority = 0 (the spine is alive only if this is invariant)
- receipts per session with hash chain = mean ≥ 1
- FQ for organ with the worst actuator coverage ≥ 0.6
- time from mutation to receipt ≤ bucket threshold
- attention leak: % of LLM context tokens spent on governance plumbing (target: < 2%)

Number-of-hooks is inventory, not health. A coder with 6 hooks firing 100% of relevant events is healthier than a coder with 30 hooks firing 1%.

## 9. Seal protocol when this DRAFT becomes canon

1. Add to carry_forward: loop=L08/AAA canonical record request.
2. arif_judge validate F-binding claims in §2 against arifOS constitution v2026.05.05-SSCT.
3. arif_seal append VAULT999 with hash chain.
4. Promote file: `DRAFT-v0` → `v1.0.0` at `/root/AAA/instructions/hook-federation-standard.md`.
5. Notify per agent registry: Codex via session-end hook, Claude via rules-instructions, OpenCode via plugin manifest refresh.
6. arifflow_flow_ingest step_type=Seal for the ratification.

---

## 10. Audit session closeout (2026-09-25, session SEAL-db81b02eeec448a1)

### 10.1 Codex blueprint audit — six CONFIRMED labels cross-verified

| # | Claim | Codex label | 333-AGI live verification (2026-09-25 ~22:50Z) |
|---|-------|-------------|------------------------------------------------|
| 1 | Authority tuple exists, has 10 fields, missing `Budget` + `RevocationRef` | CONFIRMED | ✅ `/root/AAA/instructions/authority-envelope.md:16-17` has exactly `⟨Actor, Session, Host, Objective, Operation, Scope, Target, Issuer, Expiry, ExpectedPostcondition⟩`; no Budget/RevocationRef tuple fields |
| 2 | AAA double-counts `Reversibility` in `EvidenceQuality = (1-Uncertainty) × Reversibility` AND in `irreversibility_floor: P ≥ 0.85` | CONFIRMED | ✅ `/root/AAA/README.md:18, 25, 150, 160` |
| 3 | AAA "projection" doctrine already canon (`README_state = projection(registry_state)`) | CONFIRMED | ✅ `/root/AAA/README.md:41-43, 321` |
| 4 | A-FORGE has no `UNKNOWN_OUTCOME` status | CONFIRMED | ✅ grep `-rn` over `/root/A-FORGE/src/`: 0 hits |
| 5 | A-FORGE idempotency partial — in ACT mint + receipt-hash, kabarkan has `ON CONFLICT DO NOTHING`, not universal actuator contract | CONFIRMED | ✅ `amanahEnvelope.ts:46, 76, 121, 148` uses `idempotency_key` but scope `QUEUE/EXECUTE_REVERSIBLE` only |
| 6 | Namespace collision: linkgraph 000/999 vs kernel 000/999 in canon without linkgraph fragment | CONFIRMED | ✅ `AGENTS.md:30` ("999 ← ABANDON"), `agentic-kernel-asi-doctrine.md:32` ("999 SEAL VAULT999"), `naming-doctrine.md:633` ("999 Commitment") — three meanings, no linkgraph fragment in `/root/AAA/instructions/` |

All 6 labels held under F2 discipline. No `$x = y$` claim went into the doc without path-anchored evidence above.

### Four verdicts — all closed

| Verdict | Codex's last claim   | Status      | Evidence path                                                                |
|---------|----------------------|-------------|------------------------------------------------------------------------------|
| A       | Principal binding UNRESOLVED | **RESOLVED → MISATTRIBUTED** | `irfanclaw-fi017` = **openclaw/FI-017** (OpenClaw gateway, @irfanclaw_arifos_bot) per `/root/AAA/agents/openclaw/identity.json`. Codex's forge_policy call had no session_id; McpPolicyGate fell back to `__legacy_active` shared global slot holding the most recent `setActor()` registration. Not a breach — denial-of-attribution defect. |
| B       | ACT handoff UNVERIFIED       | **RESOLVED → VERIFIED**       | 333-AGI roundtrip at 22:39Z: `arif_init SEAL-db81b02e` returned `act_v1.eyJ...`; passed into `aforge_forge_runtime_verify` + `aforge_forge_health_check`; ingress accepted with shape `act_v1|…`; failure moved to F12 (downstream content scan flagged the JWT itself). Forge-policy path separate: no ACT needed, returns ADVISORY verdict only. |
| C       | Tool existence (forge_hook_mutation_closure) | **RESOLVED → DOES NOT EXIST** | grep `-r` in `/root/A-FORGE/src`/`dist`/`.runtime` returned 0 hits. `:7072` tools/list = 122 tools, zero hook-named. Name exists only as OpenCode skill at `/root/.opencode/skills/forge-hook-mutation-closure/`. Codex's earlier "classification gap" recommendation was a phantom patch — would have created F10 ONTOLOGY violation. |
| D       | Hook matrix                        | unchanged                   | Codex's reload of the prior live disk numbers (not fresh observations). The matrix in §3 stands from 333-AGI's probe 22:38-22:40Z. |

### Four scars sealed (now constitutional constraints, immutable per F1)

| Scar ID | Domain | Pressure | Closure |
|---|---|---|---|
| `scar_1790290104078_fe6eab1c` | security | 0.85 | token exposure in transcript |
| `scar_1790290088460_84002973` | classification | 0.60 | tool fabrication from query string |
| `scar_1790290089846_b52ab2c5` | credential-lifecycle | 0.55 | rotation without revocation |
| `scar_1790290092175_3c76c6f9` | governance | 0.75 | misattribution via `__legacy_active` |

### A-FORGE actionClassifier.ts ground truth (resolved during closeout)

- 7 tool-class sets: IRREVERSIBLE / HIGH_IMPACT / REVERSIBLE_EXEC / SIMULATE_FIRST / SUGGEST / QUEUE / OBSERVE
- ~19 mode-aware base names (`forge_agent`, `forge_filesystem`, `forge_vault`, …)
- Fallback policy (`classifyTool` line 440-449): unknown tool → `IRREVERSIBLE` (fail-closed since **2026-08-07 P0 dual-truth fix**; legacy was `OBSERVE` fail-open)
- `isClassifiedTool` returns false for unknown → McpPolicyGate emits `L4b_CLASSIFY:UNKNOWN_TOOL` with template suggestion text ("Add to actionClassifier.ts") that is **boilerplate string**, NOT a real classification gap
- Real OBSERVER tools available right now for audit: `forge_policy` (check), `forge_runtime_verify` (strict), `forge_fingerprint_check`, `forge_surface_audit`, `forge_surface_guard`, `forge_status`, `forge_health_check`, `forge_registry_status`, `forge_skillstore_read`, `forge_canon_recall`, `forge_memory`, `forge_vps_{ports,services,cron}`

### A-FORGE ACT signing mechanism (no values disclosed)

- `buildACT(actorId, sessionId, organSecret, ttlMs)` — `McpPolicyGate.ts:234`
- `verifyACT(act, actorId, sessionId, secret)` — `McpPolicyGate.ts:266`
- Algorithm: HMAC-SHA256 over canonical envelope (`amanahEnvelope.ts:127`)
- Storage: per-session `verifiedSessions: Map`; **`__legacy_active` global slot for sessionless fallback** (governance gap, see scar 1790290092175)
- TTL default 60 min; arifOS honor sets per-session `exp` in ACT payload

### Open loops that remain

L01 (F12 flag on ACT arg) — preserved from §7.
L02-L08 — preserved from §7.
**NEW L09:** Hardening `__legacy_active` slot — when session_id is absent, McpPolicyGate MUST refuse attribution rather than fall back to the global slot. Track A-FORGE patch as governance-verified execution task (D09 per Blueprint §9).  
**NEW L10:** ACT rotation must be atomic — `arif_init` minting alone does not invalidate prior ACT until its `exp`. Add `arif_revoke(session_id)` to make rotation declaration accurate.

---

## 11. Claim-state register (Hermes-distinguished four states, 2026-09-25)

> **Naming note (rejected prior cross-audit):** the loop labels **L11–L14 are GOVERNANCE-RATIFICATION identifiers, NOT layer numbers in APEX-MATH-CANON.** The canonical APEX canon holds 18 layers L0–L12 (see `/root/AAA/canon/policy_ir_apex_math_v1.json` `constants.all_layers`, n_layers=18). L11–L14 of this draft name the four F13 ratifications of 2026-09-25 and are aligned to APEX-MATH-CANON §2 (authority tuples), §3 (evidence quality), §4 (execution states), §5 (identity namespace) — but they ARE NOT layer-11-to-14 in the mathematical canon.

| Ratification | SPEC_RATIFIED | DOC_IMPLEMENTED | CODE_WRITTEN | RUNTIME_VERIFIED |
|---|---|---|---|---|
| **L11** Authority tuple 10→12 fields (Budget, RevocationRef) | ✅ F13 2026-09-25 (`/root/AAA/instructions/authority-envelope.md`) | ✅ AAA commit `docs(canon): F13-ratified 2026-09-25` · rendered AGENTS.md:417-424 | N/A (doctrine) | ✅ render-agents.sh emits new tuple downstream |
| **L12** EvidenceQuality split (Reversibility → ActionRisk gate) | ✅ F13 2026-09-25 (`/root/AAA/README.md`) | ✅ same AAA commit · YAML block + prose updated · AGENTS.md inherits | N/A (formula) | N/A (no runtime path — surface-display only) |
| **L13** UNKNOWN_OUTCOME first-class execution outcome | ✅ F13 2026-09-25 (`/root/AAA/blueprints/A-FORGE-UNKNOWN-OUTCOME-SPEC-v1.md`) | ✅ spec doc committed | ⏸ **QUEUED T2** — A-FORGE execution-organ integration pending | ❌ unimplemented in runtime |
| **L14** `lg:` prefix doctrine (linkgraph namespace 000/999 collision resolved) | ✅ F13 2026-09-25 (`/root/AAA/instructions/linkgraph-namespace.md`) | ✅ fragment committed · `render-agents.sh` registered | N/A (doctrine) | ✅ rendered AGENTS.md:506-529 |

### Cross-references

| Claim | Evidence ref (use **dashed** filename) |
|---|---|
| L11 / L12 / L14 align to APEX-MATH-CANON §2-§5 (DOCTRINE) | `/root/AAA/canon/APEX-MATH-CANON-2026-09-23.md` lines §2-§5 — `DRAFT_AWAITING_F13` |
| APEX layer count ground truth (18 layers L0–L12) | `/root/AAA/canon/policy_ir_apex_math_v1.json` `constants.all_layers` n_layers=18 |
| APEX G envelope live | session `SEAL-db81b02eeec448a1` envelope: `act_claims.apex.{G,C_dark,W3,h}` — formula verbatim `B = (A·P·E·X)^(1/4)` invoked at every init via `arifOS.kernel.baseline` |
| APEX T (Chronos/Kairos/Aion/Telos) status | grep `-E "Chronos\|Kairos\|Aion\|Telos"` on `/root/HERMES/SOUL.md` and `/root/AAA/canon/SOUL.md` → 0 hits ⇒ **PROPOSED, NOT canonical** (awaiting F13 ratification to Canon #2) |
| arif_judge alert history (last call state) | `forge_shell_alert_history` 2026-09-24T23:08Z: `total_alerts: 0` ⇒ no shell-side ALERT/DENY/GATE stamp; last seal_chain seq 40 (Sep 16-17 era) ⇒ substantive L11–L14 implementation (L13 code) unverified by judge, consistent with HONESTY principle (claim ratification, not implementation seal) |
| Kernel drift detected (2026-09-25 07:13 MYT) | `/root/arifOS` `:8088/health` `software_release` → source=`3a779938`, built=`87aa393`, deployed=`87aa393`, **drift=true**. Recurring stamp-lag pattern (source advances each commit; deploy lags last release). Not DOWN_CONFIRMED until multi-path corroborated. Awaiting T3 redeploy ack per F13. |
| `Observation ≠ Total Reality` (epistemic scar) | `scar_1790291770436_f099cfe4` sealed 2026-09-24T23:16:10Z — observer/scope mismatch; DOWN_CONFIRMED requires ≥2 disjoint paths; **Observation ≠ Total Reality** joins the canonical law chain |

### Claim states (truth-valued, single-state per cell)

| L11 | RATIFIED | IMPLEMENTED | — | RENDERED |
| L12 | RATIFIED | IMPLEMENTED | — | — |
| L13 | RATIFIED | SPECIFIED | CODE_QUEUED_T2 | NOT_RUNTIME |
| L14 | RATIFIED | IMPLEMENTED | — | RENDERED |

`SPEC ≠ CODE ≠ RUNTIME ≠ SEALED` explicitly held per lesson learned.

---

**Provenance:** written 2026-09-25 by 333-AGI from session `SEAL-db81b02eeec448a1`. Closeout 22:48 UTC adds §10 with scar IDs and resolved verdicts; 23:10 UTC adds §11 with Hermesian claim-state register.  
**Conformance:** every claim in §2-§6 traces to one of (live disk read 2026-09-25, MCP probe at 2026-09-25T22:38-22:48 UTC, ACT roundtrip at 22:38-22:39 UTC, WELL deploy script at 22:42 UTC, actionClassifier.ts read at 22:46 UTC, McpPolicyGate.ts read at 22:47 UTC, four scar seals at 22:48 UTC, APEX-MATH-CANON read 23:09 UTC, policy_ir_apex_math_v1.json read 23:09 UTC).  
**Memory-class:** INT (interpretation) with confidence cap 0.90 per F7 — where reading is on the spec not just the realized instance, confidence drops to 0.80.  
**Companion:** `/root/.agents/skills/FORGE-incident-triage` for the failure-mode catalog this draft does not enumerate.
