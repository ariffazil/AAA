# Paperclip Distill — Session 2: Code Distill + Copilot Adjudication (2026-08-14)

> **PURPOSE:** Companion to `paperclip-distill-2026-08-14.md` (session 1: landscape + 5 protocols). This file records session 2: (a) the "gitingest" code-level distill of the 9 mechanical governance patterns, (b) the Copilot-proposal adjudication, (c) Arif's state-as-public-goods framing that resolved it. Future sessions: read BOTH files before touching the Paperclip queue.

## A. Code-level distill (verified in shallow clone /tmp/paperclip — server/src = 839 .ts files, ~496K LOC)

**Discovery #0 — the bridge already exists:** `server/src/adapters/hermes-gateway-doc.ts` — Paperclip wrote a FULL Hermes adapter themselves (API_SERVER_ENABLED=true, port 8642, join approval flow, task_bridge keys with scoped capabilities). Federation can be an employee in a Paperclip company TODAY with zero code. Build-vs-integrate answer: integrate.

**9 patterns, mapped to organs:**
1. `services/quota-windows.ts` (64 LOC, pure) — `Promise.allSettled` + 20s per-adapter timeout + provider-slug mapping; one provider outage never blocks others; errors-as-data. → **FLAME, cheapest P1**.
2. `services/budgets.ts` — budgetPolicies + budgetIncidents + `cancelWorkForScope` hook + pauseReason. Breach → incident row → work CANCELLED (not a banner). → FLAME/FED: treasury that stops work; FLAME knows hit-rate but nobody cancels work when money runs out.
3. `services/decision-signing.ts` — HMAC per decision (`decision-spec-v1`), key file 0600 + owned-by-process-user enforced in code. → **VAULT999 notary upgrade**: tamper-evident, not just append-only.
4. `services/cross-issue-influence-limit.ts` — CAP 20 cross-issue writes/run, `log_only → enforce` dated migration (2026-08-11), 403 body carries the FIX. → FED blast-radius cap + "denial must teach" policy.
5. `services/change-consent-gate.ts` — consent required before agent name/role/title/capabilities + skill mutations. Identity self-change gate = F1 mechanical. → kernel/self-mutation (SOUL.md/identity mutations should gate like this).
6. `services/execution-allowlist.ts` — pure `(driver, provider, policy) → allow/deny`, zero DB, trivially unit-testable. Security-critical guards should have this shape. → A-FORGE preflight.
7. `services/low-trust-runtime-containment.ts` + trust-preset-resolver — new agents = `low_trust_review` preset: allowedToolClasses, ancestry depth bound, promotion after review. → **warga onboarding trust gradient — REAL GAP: we onboard warga with no trust ladder**.
8. `services/recovery/` — provider-failure-classification, stranded-notice, pause-hold-guard, run-liveness. Stranded runs are recognized objects, not silent deaths. Kin to SABAR-RETRY. → FLAME/FED.
9. `services/heartbeat.ts` — atomic task checkout + run resume across heartbeats (no double-work, no runaway spend). → arifFLOW cron lease semantics (when multi-run lands).

**AVOID:** org-chart UI, ticketing, multi-company isolation, plugin marketplace — that's Paperclip's identity, not our gap. Don't build an HR department for 7 organs.

## B. Copilot adjudication (Mode 6 pattern)

Arif pasted Copilot's proposal with "I don't agree that much" + his own counter-thesis: AAA = state providing basic infra + public goods to citizens. Live-probed our three repos (`gh api repos/ariffazil/{AAA,arifOS,A-FORGE}`) before ruling:

- **CANON-VIOLATING:** AAA → "intelligence layer" (SENSE/THINK/VERIFY/JUDGE/ADVISE). AAA's own README: "It routes and displays. It never judges." SOT-MANIFEST: `godel_lock: ACTIVE federation-wide`. Judging switchboard = hand becomes head.
- **ALREADY-EXISTS:** "missing STATE/INSTITUTION repo" — AAA already IS the institution (L1, "Agentic Intelligence Institution & A2A Control Plane", :3001, SOT-MANIFEST v2026.08.14: 11 FI instruments, 7 domain organs, 4 lanes, QQQ 10/10, Gödel lock active). Copilot proposed building a house on top of a standing house.
- **LAYER-INFLATION:** arifOS→STATE→AAA→A-FORGE = 4 governance layers for 7 organs = bureaucracy. Federation rule: integration over new layers.
- **VALID:** Paperclip gap analysis; "GGI" coinage as paper closing line, not architecture.

**Method note (Mode 6):** external-LLM proposals about OUR architecture get limb-by-limb falsification against LIVE repo state (README + SOT-MANIFEST + code), not paragraph-by-paragraph agreement. Arif's disagreement signal ("I don't agree that much") means supply the reasoning he senses but doesn't spell out — validate his counter-thesis with evidence, don't just agree with him either.

## C. Arif's framing (adopted): AAA = the State, public goods for warga

Public-good mapping to what :3001 already runs: roads=A2A Mesh v1.0.0 · JPN/identity=Agent Registry (11 FI, 4 lanes) · pos=Task Router (AREP) · public square/oversight=cockpit (888_HOLD queue) · courts=arifOS:8088 · kerja raya=A-FORGE:7071/72 · treasury=WEALTH:18082 · health ministry=WELL:18083 · survey dept=GEOX:8081 · public records=VAULT999 (Merkle anchor/100) · SIRIM=QQQ v1.1.1.

The state exists. Missing = departments: **(1) Treasury that stops work** = P1 quota-windows + budgets port; **(2) Public records notary** = P2 HMAC signing; **(3) Citizenship process** = P3 trust presets; **(4)** P4 atomic checkout when arifFLOW multi-run. Not a new state, not a new layer.

## D. Convergent evolution (paper material)

Paperclip independently converged on an F13-shaped human veto ("pause or terminate any agent — at any time") from the org-management direction, zero constitution doctrine. Two independent systems arriving at human-veto-on-top = structure of reality, not design choice. Their governance = managerial (what agents may DO: spend, scope); ours = epistemic (what the system may CLAIM). Different axes, both needed, neither implies the other.

Market context (gh api, OBS): OpenClaw 386K★/~9mo (~43K/mo) > Hermes 230,486★/13mo (~18K/mo) > OpenCode 197,418★ > Claude Code 141,439★ > Paperclip 78,115★/5.5mo (~14.5K/mo). Institution layer born + fast, but market still votes personal agents hardest. 5,056 open issues in 5.5 months = moving faster than stable — institution-grade software that isn't stable yet is a prototype in uniform.

## E. Session 3 follow-through (2026-08-14 late) — precedent filed, seal held

**Executive queue GO received.** OpenCode spawned as CCC orchestrator (deleg_60d90dd1) to execute the semantic-map-then-build contract: map every Paperclip capability to a federation twin (EXISTS/WEAK/MISSING, live-endpoint evidence) BEFORE writing code, then Wake Bus P1 into AAA :3001 (`/api/wake` endpoints, sha256 fingerprint dedup, 15s first-run grace, SABAR-RETRY, delivery via A2A card URL). Verified reading registry code (`agent-state/registry.js` — "REGISTERED does not mean AUTHORIZED") before touching anything.

**First self-citing precedent filed:** `SCAR_TREE777_HOLD.md` in `/root/AAA/wiki/scars/` — commit `b9a2c1b9`, manifest regenerated v2.0 (9 scars indexed), entry sha256 `25bcd018...1f330`. Precedent text: "We do not build what is not demanded." Cites DECISION_TREE777_HOLD_2026-08-14 (SEAL-b413b305). Includes the four-777 alignment map: TREE777 remembers / ATLAS333 maps / EUREKA777 resolves / VAULT999 witnesses. The wiki's first entry that cites the decision NOT to serve the wiki.

**Seal attempt = Gödel lock worked as designed:** agent (LIMITED_MUTATE) completed BIND + JUDGE (authorized, trace trc-a98d2f19846b) but `arif_seal` returned HOLD ×2 — `irreversible execution requires a prior judge packet via constitutional_chain_id and judge_state_hash`. No agent-side fix exists; vault append deferred to F13 sovereign ceremony. Nonce lesson: single-use, both attempts burned. Transport lesson: kernel MCP needs `Accept: application/json, text/event-stream` or HTTP 406.

**Adjudication-thread rule (Mode 6 extension):** external analyses that turn ratified HOLDs into "gaps" (e.g. the tree777 gap-table framing "no demand signal / no constitutional gate on reads" as failure) are ΔS>0 through the back door. A parked component with a recorded decision is DISCIPLINE, not debt. Test any "gap" list against VAULT999/corpus decisions FIRST — probe before accepting the frame. ("Probe before build" is also what Qwen confessed skipping: built the server before checking the vault for a verdict. SCAR_TREE777_HOLD now encodes this.)
