# External-AI Stack Proposal Adjudication — 2026-10-15 (Mode 6 + Mode 4)

**Input:** ChatGPT architecture proposal (pasted by Arif 2026-10-15). 10 repos proposed: Inspect AI, OpenSandbox, Temporal, NATS/JetStream, GEPA, Langfuse (+ conditional LangGraph, OPA, Nous Hermes Agent, Agent Lightning). Proposal's own framing: "retain arifOS as authority kernel."
**Session:** SEAL-40c01758f24548c1 (OBSERVE_ONLY band — audit is observation-class). Kernel healthy, 13 floors, vault healthy.

## Probe evidence (OBS, 2026-10-14T20:08Z)

| Report recommends | Live state probed | Verdict |
|---|---|---|
| NATS/JetStream organ transport | `nats-server.service` + 5 JetStream streams LIVE: `kabarkan-ingest` (501,401 msgs, last 79ms), `arifos-governance` (49,503), `arifos-organs` (7,577), `agent_memory` (3,352), `arifos-consequence` | **ALREADY RUNNING** — report unaware |
| Nous Hermes Agent as runner | 6 hermes-* services: asi-gateway, a2a, mcp-server, rasa-mcp, voice-governor, health | **ALREADY RUNNING** — strongest proof report never probed us |
| GEPA improvement proposals | Skill `forge-hermes-self-evolution` (AAA-owned, T3, F13-gated); staged clone `/root/forge_work/2026-08-25-hermes-self-evolution/upstream` @ 0a929e3; isolated-venv + candidates-to-forge_work + 888-gate rules already written | **ALREADY STAGED + GOVERNED** — never executed (888 hasn't named a skill) |
| Inspect AI eval infra | FRAME (drift) + CHRON (calibration: 33 verified preds, acc 0.8686, Brier 0.150) + bespoke evals: `/root/thinkingbox-eval` (results.jsonl, has run), `/root/HOLDOUT` (challenge verdicts + MANIFEST.sha256), `/root/chron_abtest` | **PACKAGING GAP** — eval discipline exists bespoke; no unified framework |
| OpenSandbox isolation | Docker 12 containers incl. playwright-service (browser sandbox), firecrawl stack, A-FORGE full DDD tree w/ EgressPolicy | **PARTIAL** — code-exec sandbox lane for canaries is thin add |
| Langfuse traces | `hermes-otelcol` (OTel collector) + kabarkan + chron + VAULT999 (115 entries) | **PLANE COVERED** — UI gap only → LAW 8 hold |
| Temporal durable workflows | Absent (no service/port/pkg). No sealed scar of lost mid-mission state; 2/27 cron errors are delivery-class | **PARK** — LAW 3: no demonstrated failure class. Trigger: sealed scar of lost mission state |
| OPA policy engine | arifOS kernel F1-F13 + ACT/SCT + A-FORGE EgressPolicy = the policy engine | **REJECT** — second policy authority = constitutional duplicate |
| LangGraph agent graphs | AAA graph doctrine + Hermes/OpenCode runners | **REJECT for now** — duplicate orchestration layer |
| Agent Lightning (RL on weights) | Different plane (weights vs prompt/skill/agent) | **DEFER** — agree with report |

## Findings

1. Report knew our *names* (arifOS, VAULT999, FRAME, CHRON, A-FORGE — likely from public docs) but not our *state*: 2 of its 6 primary recommendations are already running, 1 staged with governance rules stricter than the report's own.
2. Report's contracts checklist (shared task identity, exact-action auth, duplicate-action protection, independent outcomes, controlled promotion+rollback) maps to existing organs: trace_id, ACT binding, kernel `idempotency_key` param, CHRON, F13+git. Idempotency key exists as kernel param (DER — wiring coverage unverified).
3. Real bottleneck is operational, not architectural: the RSI loop (GEPA staged → FRAME eval → arifOS canary) has never been run end-to-end.
4. Report citation defect: [2] table says `opensandbox-group/OpenSandbox`, href goes to `alibaba/OpenSandbox` — provenance drift inside its own text. Per-repo capability claims = vendor-attributed, unreproduced.
5. Candidate recurring failure for bounded experiment (probed): cron errors `Weekly Governance Digest`, `Memory Federation kvm8→kvm4` (2/27 jobs, last_status=error).

## Decision boundary presented to Arif

GO/HOLD: one bounded RSI experiment on existing organs (recommended target: `Memory Federation kvm8→kvm4` cron — recurring, measurable, low blast radius). Zero new installs. GEPA run + canary remains 888/F13-gated per staged skill rules.
