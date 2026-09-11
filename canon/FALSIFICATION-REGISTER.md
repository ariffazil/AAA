# FALSIFICATION REGISTER — Living Document

> **Created:** 2026-09-12 · **Origin:** multi-session night (FI-008 External-Witness seal · FED compilation · Majlis PARTIAL-SEAL)
> **Governing law:** *A watch without a data path and a named consumer is attention debt* (scar_1788798276791 · Signal-without-Consumer · sealed 2026-09-12)
> **Rules:** (1) Every watch carries: failure signal · check command · deadline · owner. (2) Verdicts append to this file + git commit. (3) Resolved watches move to Archive with receipt. (4) Cron wiring for automated checks = 888_HOLD (FORGE-infra-crons).
> **Named consumers:** weekly RSI mesh pass · every session-close carry_forward · the 2026-11-12 upgrade decision for `EUREKA-CAPABILITY-DISCOVERY-OUTRUNS-DECAY`.

---

## Active Watches

### W-1 · Claim-without-handle class (30-day zero-recurrence)
**Deadline:** 2026-10-12 · **Owner:** all FI harnesses · **Source:** EXTERNAL-WITNESS-SEAL §2/§3
**Failure signal:** any completion claim ("dah log/simpan/deploy") without a co-cited handle in the same output.
**Check:** Stop-gate (aaa-completion-check.sh) logs + `grep -c 'REALITY-CLAIM-REFUSAL' /root/.arifos/ritual.log` trend (refusals = gate alive; claims-without-handle in outputs = failure).

### W-2 · Dead-Key Gravity (60-day)
**Deadline:** 2026-11-12 · **Owner:** FED lane · **Source:** Majlis PARTIAL-SEAL criteria 1
**Failure signal:** a dead key appearing in Order 1–10 and receiving real workload.
**Check:** `grep -B2 "order: [1-9]$\|order: 10" /root/A-FORGE/litellm-config.yaml` key identities + FED error log 429/auth-failure scan by lane.

### W-3 · Fallback Latency Trap (60-day)
**Deadline:** 2026-11-12 · **Owner:** FED lane · **Source:** Majlis criteria 2
**Failure signal:** agent trapped in retry cycle on quota-exhausted model instead of jumping to live fallback <2s.
**Check:** route_latency table (fed_report_latency) — p95 per chain; alert if any exhausted-provider chain retains traffic across a day.

### W-4 · Declaration Gap (60-day)
**Deadline:** 2026-11-12 · **Owner:** FED lane · **Source:** Majlis criteria 3
**Failure signal:** model floating with no explicit context contract (None/32K default where real capability differs).
**Check (data path, reproducible):** count null context in `/root/.config/federation-models.json` — **baseline 2026-09-12: 202 models, 149 declared, 53 null** (null-count must be class-audited: LLM-class nulls → zero; non-LLM entries → declared N/A explicitly). Note: registry-wide "sifar None" was falsified tonight; the 92/92 claim held only for the touched subset.

### W-5 · Instruction-only drift (Wawa prediction)
**Deadline:** next sandboxed persona-clone test · **Owner:** Wawa lane (KVM2)
**Failure signal (for the prediction):** instruction-only clone does NOT drift within 3–5 sessions → falsifies; drifts → confirms Structure-Governs.
**Check:** clone log + drift telemetry comparison vs structured twin.

### W-6 · Discovery→Mutation Delay, next 10 (compounding test)
**Deadline:** after 10 sealed mutations · **Owner:** all lanes
**Failure signal:** median ≥24h OR any new 70-day tail.
**Check:** this register's append dates vs scar occurred_at (baseline n=6: median 1–2d, range <1d–70d, direction falling; marker `a43616ebd84e…`).

### W-7 · Governance-pays efficiency audit (monthly, recurring)
**Owner:** A-AUDIT lane · **Source:** META-EUREKA 4 boundary (ratified 2026-09-12)
**Failure signal:** any efficiency-class gate consuming more attention than it saves (bounded damage confirmed) without removal/repair — OR any authority-class gate bypassed or firing wrongly.
**Check:** monthly 3-gate sample; ACSC instrumentation precondition (data path + named consumer) still open.

---

## Upgrade Decision (2026-11-12)

`EUREKA::CAPABILITY_DISCOVERY_OUTRUNS_DECAY` → **Constitutional Runtime Primitive** iff W-2, W-3, W-4 all record zero violations by this date. Any violation → remains Candidate Law; scar the violation, re-derive.

## Archive

*(empty — first verdicts expected 2026-10-12)*
