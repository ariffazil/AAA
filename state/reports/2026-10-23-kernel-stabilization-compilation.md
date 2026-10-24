# KERNEL STABILIZATION & ALIGNMENT — TASK COMPILATION
**Date:** 2026-10-23 02:30Z (10:30 MYT) · **Author:** 333-AGI · **Trigger:** F13 directive — "stabilize and align the kernel to lower entropy and chaos, preserve human and agents attention for reality-signal detection"
**Status:** DRAFT_AWAITING_F13 (P0 execution may proceed; ceilings/seal changes are F13/888-gated)
**Method:** live probes only. Every claim tagged OBS / DER / INT / SPEC. Probe commands in Appendix A.
**Path note:** `/root/AAA`, `/root/AAA/canon`, `/root/AAA/governance` and `/root/AAA/reports` are **filesystem-immutable** (`chattr +i`). This report therefore lands in `/root/AAA/state/reports/` — the writable state surface. Immutability of canon is a control, not a defect.

---

## 0. DELTA SINCE SESSION START (OBS)

| Action | Before | After |
|---|---|---|
| Orphan `vite build` PID 2559732 (PPID=1, 11h19m elapsed, 4h32m CPU, 12.9 GB RSS) | killed | memory available 1.0 GiB → 4.2 GiB |
| Host load | 38.08 | 29.85 |
| Kernel `/health` | HTTP 503 "Service Unavailable" | HTTP 200, status degraded |
| Memory PSI full avg10 | 37.67% | 33.34% |

The 503 was **not** a kernel code failure. It was the kernel's single worker starving behind host memory pressure caused by one abandoned build process. That causal chain is P0-1/P0-2.

**The memory guard existed but did not enforce (OBS):** `earlyoom` v1.8.2 logged repeated `sending SIGTERM to process 2559732 ... VmRSS 12602 MiB` followed by `process 2559732 did not exit` and `kill failed: Timer expired`. It never escalated to SIGKILL because its thresholds were `-m 10,5 -s 15,8` (SIGKILL only when memory <5% **and** swap <8%); the box hovered at 6.4% memory / 13.9% swap, so SIGTERM repeated for hours. Fix applied: `-m 10,7 -s 15,15` (SIGKILL at 7% memory / 15% swap) + a dedicated orphan-build reaper. This is the "control that names an action but does not prevent the failure class" pattern — exactly the entropy Arif asked to remove.

**Applied this session (reversible):**
1. Killed PID 2559732 (SIGTERM ignored → SIGKILL).
2. Installed `/usr/local/bin/orphan-build-reaper` + `orphan-build-reaper.timer` (10 min, PPID=1 builds >30 min, logs `/var/log/orphan-build-reaper.log`). First run: success. **Control test PASS:** spawned a fake PPID=1 `/tmp/vite build` (PID 4093711), reaper killed it and logged `KILL pid=4093711 elapsed=3s rss_kb=3956`. Test artifacts removed.
3. Tightened `earlyoom` to `-m 10,7 -s 15,15`; backup at `/etc/default/earlyoom.bak-20261023`; service active, NRestarts=0.
4. Post-fix host: memory 19/31 GiB used · **11 GiB available** · swap 25/35 GiB · load 3.76 · kernel `/health` 4 ms · FQ 0.4545 (still < 0.5; F1/F8 still fail).

---

## 1. MEASURED STATE (OBS, 2026-10-23T02:25–02:30Z)

### 1.1 Host
- 8 cores · load 29.85 / 32.08 / 29.48 · Mem 27/31 GiB used · Swap 30/35 GiB · disk 324G/387G (84%)
- Memory PSI: `some avg10=72.9`, `full avg10=33.3` — still severe stall pressure
- Zombies: 3 · swap top: xerj 2.9 GB, node 2.2 GB, beam 0.96 GB
- Disk top: `/root/backups` 24 GB · `/root/.cache` 17 GB · `/root/runtime` 14 GB · `/root/arifOS` 13 GB · `/root/forge_work` 13 GB

### 1.2 Kernel (:8088)
- `status=degraded`, `substrate_state=HEALTHY`, `floor_passed=false`, `floor_measurement=measured`
- Floors: **10/13 pass**. Failing: **F1 (0.0)**, **F8 (0.5861)**. Unmeasured: **F6**.
- F1 provenance: `arifflow_fq_probe:fq=0.391304347826087`
- F8 provenance: `arifflow_live_vector:g=0.5861`
- Thermodynamic: `verdict=HOLD`, `entropy_delta=-0.0`, `vitality_index=0.7071`, witness human 0.6667 / ai 0.625 / earth 1.0
- APEX scalars: G 0.5861 · QDF 0.4623 · C_dark 0.2112 · A 0.8631 · **P 0.1968** · E 0.9994 · X 0.6953 · W3 0.7469 (independence UNMEASURED)
- `execution_readiness=held`
- Identity: `session_authority=OBSERVE_ONLY`, `identity_authenticated=false`, `actor_verified=false`, `se_stage=000` (never advanced)

### 1.3 Tools
- `tools_registry_size=63` (aliases included **by design**), `total_declared_tools=49`, `callable_public=9`, `operational_tools=5`
- **Correction to my earlier claim:** 63 > 49 > 9 is documented as by-design in `tool_count_semantics`. It is **not** a defect. The real gap is **5 proven-live vs 9 public**.

### 1.4 Metabolism (arifFlow :7073)
- Federation FQ = **0.391** (below 0.5)
- `333-agi`: 24 verify / 1 execute, quotient 24.0, held, **FOSSILIZED**
- `hermes-asi`: 10 verify / 23 execute, quotient 0.435, **STUCK**
- `chron` 11/0, `p0-metabolize` 28/0, `reexamine` 29/0 — verify-only actors
- Synthetic actors present in production vector: `test`, `test_agent`, `honest_agent`, `unstable_agent`, `staged_agent`, `attacker`, `adversarial_agent`

### 1.5 Vault / seal
- `vault999_health=healthy`, sealer breaker `closed`, `runtime_drift=false`
- `SEALED_EVENTS.jsonl` 1,358 lines; last entry `VERIFIED_WITH_CAVEAT`
- Last entry caveats explicitly record `arif_judge + arif_seal` failures (`-32602 output schema`) and a self-asserted fallback path
- Recent kernel log: `arif_seal` → `888_HOLD` (F7 overclaim / capability requires SOVEREIGN; current LOW); `arif_judge` → HOLD

### 1.6 Schedule / attention
- 32 cron jobs: **24 human-lane**, 7 machine-lane, 1 `lane=null` (validator error)
- Delivery targets: 18 telegram, 10 origin, 4 local
- Site-drift cron failing: `dist/index.html` points at `assets/index-RlEEP0al.js`; webroot points at `assets/index-BASIvgqQ.js`
- No `delta_gate` field in jobs.json — coverage must be proved at the delivery layer before claiming it
- Output volume: ~12+ human-facing messages/day across ALPHA-ZEN (3), SADO (2), drift/tripwire/gate checks (3+), digests (2+), docforge (1)

### 1.7 Config / runtime surface
- `arifos.service`: **41 drop-in files + 2 control drop-ins** — effective config is not humanly reviewable
- Extra arifosmcp runtimes still listening in stale user sessions: `:3199` and `:3280` (session-5271, 4.5 days), `:28188` (session-5180, 4.6 days)
- Core organs: A-FORGE :7072 healthy · FED :7074 healthy · GEOX :8081 degraded · WEALTH :18082 healthy · WELL :18083 degraded · AAA A2A :3001 degraded · HAProxy :4000 no `/health` answer (route check needed, not a defect by itself)

### 1.8 Composition / mutation accounting
- `mutation_ledger.jsonl`: 4 rows, all 15 Aug, all `"proof": "SIMULATED_SUCCESS"` — **fossil; reports EXECUTED without measuring**
- No per-mutation delta stream against protected invariants
- HERMES proxy over 7 days: AAA 97 commits / 3,870 file-changes / +275,007 −554,060 lines; arifOS 176 commits / 529 file-changes / +31,218 −3,737. Largest single commit = 54.4% (archive-tree deletion; subtract it: 378,076 lines across 96 commits, largest 13%).

---

## 2. CAUSAL CHAINS (DER — symptom → mechanism → lever)

**A. Availability:** orphan build (12.9 GB) → host memory PSI 37% full → kernel single worker starved → `/health` 503 → `execution_readiness=held`.
*Lever:* process reaper + health/readiness decoupling + memory budget.

**B. Constitutional verdict:** role-blind FQ accounting + synthetic actors → federation FQ 0.391 → F1 fail → `floor_passed=false` → thermodynamic HOLD.
*Lever:* actor class + role-aware FQ (executor vs auditor vs system). Do **not** lower the threshold.

**C. F8:** `G=(A·P·E·X)^(1/4)=0.5861`. P=0.1968 is the binding axis — raising P alone to 0.50 yields G≈0.73; to 0.80 yields G≈0.82. F8 is **one-axis-bound**, not four-axis-bound.
*Lever:* decompose P and QDF (0.4623), fix the measured cause. No formula change.

**D. Seal chain:** identity unauthenticated + OBSERVE_ONLY + se_stage 000 → `arif_seal` LOW authority → 888_HOLD → fallback append path → chain entry `VERIFIED_WITH_CAVEAT`.
*Lever:* re-auth session (challenge-response), fix `-32602` output schema, then seal. Never self-seal.

**E. Config entropy:** 43 drop-ins + 3 shadow runtimes + no effective-config hash → no one can state the running config without reading 43 files.
*Lever:* consolidate to named layers, publish one effective-config hash, drift-check the hash.

**F. Attention:** 24 human-lane crons, no visible delta gate, daily duplicates → real signals (bundle drift, seal failure, floor fail) compete with ritual output.
*Lever:* classify human-lane jobs by decision value; keep ≤8; merge digests; delta-gate every promotion; heartbeat exempt.

**G. Composition blindness:** no declared protected surface, no semantic unit, no ceiling, no writer → 378k lines/7 days unaccounted, and no line that can be crossed.
*Lever:* HERMES 3 layers + the 333 binding (below).

---

## 3. TASK COMPILATION (deduplicated against `/root/work/tasks.json`)

### P0 — STABILIZE (availability + honest verdict)

| ID | Action | Kills failure class | Authority | Verify |
|---|---|---|---|---|
| **P0-1** | **APPLIED** — build/process reaper installed (`orphan-build-reaper.timer`, 10 min; PPID=1 build >30 min → SIGKILL + log). earlyoom tightened from `-m 10,5 -s 15,8` → `-m 10,7 -s 15,15` | abandoned process → OOM pressure → 503 | T1 auto (done) | timer active; first run success; no build proc >30 min; `free -h` available ≥4 GiB |
| **P0-2** | Host-memory isolation for the kernel worker: `MemoryMin`/`OOMScoreAdjust` on `arifos.service`, and keep build workloads in a scope with `MemoryMax`. **Do not rewrite `/health`** — `p0-arifos-accept-queue` already measured 44/44 200 responses under concurrent judge load (max 0.298s). The 503 class is host pressure, not worker contention | kernel availability coupled to global memory | T2 (systemd drop-in) | under `stress-ng --vm`, `/health` <1s with truthful `degraded`; kernel never OOM-killed |
| **P0-3** | **Role-aware FQ**: add `actor_class` (executor/auditor/system/test); exclude `test*`, `attacker`, `adversarial*` from federation rollup; split mechanical vs human verify; recompute FQ and F1 | role-blind metric penalises auditors; synthetic actors distort signal | T2 (metric semantics) | FQ recomputed; 333-AGI no longer FOSSILIZED for auditing; F1 provenance shows class split |
| **P0-4** | Decompose F8: P axis 0.1968 and QDF 0.4623 — identify measured cause of each; fix or mark unmeasured; no threshold change | one-axis cap reported as four-axis failure | T2 | G decomposition receipt; P/QDF source named |
| **P0-5** | Fix identity stickiness (`OBSERVE_ONLY`): run `arif_init` challenge → sign → bind; fix kernel session-state/lease-mint for harness-injected ACTs (see `p1-kernel-identity-observe-only-sticky`, OPEN; restart is T3/888) | session cannot mutate/seal | T1/T2 | `state_axes.session_authority` = ACT; `actor_verified=true` |
| **P0-6** | Seal path: fix `-32602` output schema on `arif_judge`/`arif_seal`; **merges `p0-vault999-heartbeat`** (F13 ruling 2026-10-23T02:17Z "sah semuanya go"; chain silent 184h; head 346 vs fail 274); no fallback writes | chain unbound; seals self-asserted | **888/F13** | one real `arif_judge → arif_seal` round-trip; VAULT999 head advances with kernel receipt |
| **P0-7** | Cron integrity: set `lane` on job `351387f88502`; fix site-drift baseline (`dist` vs webroot bundle pointer) | validator blind; alert blind | T1 | validator 0 errors; drift job green or explicitly baselined |
| **P0-8** | Tombstone `mutation_ledger.jsonl` (`SIMULATED_SUCCESS`) or wire a real writer; rename any non-enforcing control to `observe_*` | fake control → false assurance | T1 | file header states NOT_A_CONTROL, or real rows with measured deltas |
| **P0-9** | **Observatory truth pass** — fix `build_public_state.py:1291-1292` (never pair `fed_quotient` with `legacy_verdict`; publish constellation); gate "replay verified" on `verified==true AND gap_count==0`; label capability `8/8 exposed · 5/8 proven` | public surface says OPTIMAL/verified while kernel HOLDs and chain has 40 gaps | T1 code / deploy T2 | regenerate snapshot; assert FQ verdict = constellation, vault shows gaps 40 + verified false |

### P1 — ALIGN / LOWER ENTROPY

| ID | Action | Kills | Verify |
|---|---|---|---|
| **P1-1** | Consolidate 43 arifos drop-ins → ≤10 named layers; publish effective-config hash | config unreadable | `systemd-analyze cat-config` diff + hash before/after |
| **P1-2** | Retire shadow runtimes `:3199`, `:3280`, `:28188` after owner check | duplicate authority surfaces | ports closed; no service references them |
| **P1-3** | Tool truth surface: publish `5 operational / 9 public / 49 declared`; no new tool without named consumer + 24h proven-live | capability inflation | `/health` exposes three counts + provenance |
| **P1-4** | **Protected Surface Inventory + ceilings** (HERMES L1) — see §4; F13 sets numbers | composition blindness | registry file + gate reads it |
| **P1-5** | **Semantic delta recorder** (HERMES L2) bound to envelope `Objective`; units = PIE (below), not lines | unmeasurable churn | one real mutation emits one semantic delta |
| **P1-6** | **Trajectory accountant** (HERMES L3): sum PIE per objective vs ceiling; HOLD at 80%, seal block at 100% | cumulative overreach | synthetic 3-step test crosses 80% → HOLD |
| **P1-7** | Human-lane triage 24 → ≤8: keep decision-bearing (family, money, health, irreversible, drift-that-changes-action); move state reports to machine lane; merge daily digests | attention tax | jobs.json lane counts; ≤3 pushes/day to Arif |
| **P1-8** | Delta-gate coverage proof: every human promotion passes a delta check; heartbeat exempt; record coverage % | repeated stale reports | delivery log shows gate decisions |
| **P1-9** | Disk 84% → <70%: archive `/root/backups` + `.cache` (compress, verify restore, then remove); no blind `rm -rf` | capacity cliff | `df` <70%; archive manifest + restore test |
| **P1-10** | Classify dirty trees (`p2-dirty-trees-classify`); no blob commits | unreviewable diffs | per-repo classification receipt |
| **P1-11** | Public-state schema hygiene: enrich `planes.*` with `{value,source,observed_at,confidence}` (or point UI at `organs.*`); collapse `ariflow`/`arifflow`/`arifFlow` to one key | phantom absence + alias drift | UI shows real provenance; one canonical key |

### P2 — ATTENTION / REALITY SIGNAL

| ID | Action | Kills | Verify |
|---|---|---|---|
| **P2-1** | Human Signal Contract: define what reaches Arif (irreversible · money · health/family · drift that changes a decision) vs machine-only | noise vs signal ambiguity | contract + cron audit against it |
| **P2-2** | One daily digest at 20:00; retire duplicate daily reports | attention fragmentation | delivery count/day |
| **P2-3** | Vault label honesty (`kernel-vault-health-label`): `healthy` must not imply chain-fresh; expose `last_seal_age_h` | label overclaim | `/health` field shows age |
| **P2-4** | Organs publish one config hash; drift cron compares hash, not narrative | config drift blind | hash mismatch alarm |
| **P2-5** | Agent-card ↔ runtime reconciliation; archive synthetic/test actors | phantom capability | registry equals live actors |

---

## 4. THE THREE-LAYER SPEC — plus the binding HERMES left out

HERMES is correct: my falsifiable test could not run because no per-mutation delta stream exists, and line-count is a bangang unit (the 451k "delta" was archive removal). The sequence is declare → record → account. But there is a fourth requirement without which all three become another document:

**L4 — the ceiling must be a field the gate reads.** A ceiling in prose is not a control. `CanMutate` must gain `CumulativeDelta(objective) ≤ Ceiling(surface)` as a runtime predicate, or the accountant is advisory decoration.

### Protected surfaces (candidate — F13 to ratify)
| Surface | Why protected | Proposed ceiling per objective |
|---|---|---|
| `/root/AAA/canon` | ratified doctrine | ≤3 PIE-1, ≤5 PIE-2 |
| `/root/AAA/governance` | governance law | ≤2 PIE-1 |
| `/root/arifOS/arifosmcp/runtime/authority.py` + floor/gate modules | enforcement | 0 without 888 |
| `/root/AAA/instructions` | rendered prompt law | ≤2 fragments |
| `/root/AAA/registries` + agent cards | identity/capability | ≤1 new entry with named consumer |
| `/root/A-FORGE/tools_sot.yaml` + `litellm-config.yaml` | execution/model surface | ≤2 changes, 0 authority widening |
| `/root/HERMES/cron/jobs.json` | attention surface | ≤2 human-lane additions |
| `VAULT999` | immutable history | append-only; 0 non-seal writes |
| identity keys / DID registry | sovereignty | 0 without F13 |

### Semantic unit — PIE (Protected-Invariant Edit)
1. **PIE-1** invariant changed (count)
2. **PIE-2** protected file touched (count, surface-weighted)
3. **PIE-3** gate loosened (weight ∞ → automatic F13)
4. **PIE-4** new registry/agent/tool added (requires named consumer)
5. **PIE-5** authority widened (weight ∞ → automatic HOLD)

Do **not** use lines, files, or commit count as the primary unit. They may be reported as context, never as the gate.

### Enforcement path (minimal)
1. `protected_surfaces.yaml` — surface → invariant → ceiling (F13 ratifies).
2. `delta_recorder` — appended by the mutation gate, carries `{objective, surface, pie_class, magnitude, evidence}`.
3. `trajectory_accountant` — reads sum per objective; returns ALLOW/HOLD.
4. Wire into `arif_judge`/`arif_seal` return: `cumulative_delta`, `ceiling`, `remaining`.

---

## 5. DO NOT BUILD (anti-entropy)

- No new dashboard, cockpit, or telemetry registry. Existing ones are not consumed.
- No new agent or subagent role.
- No new canon document for these three layers until the surface inventory is ratified.
- No FQ formula rewrite before actor-class hygiene — that would be tuning the thermometer.
- No line-count-based "irreversibility score".
- No hand-merge of the two `carry_forward.json` forks.
- No new tool until the 5/9 operational gap is closed.

---

## 6. FIRST THREE ACTIONS (ranked by entropy removed per unit effort)

1. **P0-3 + P0-4** — role-aware FQ + F8 decomposition. Restores an honest kernel verdict without changing a threshold. No downtime, fully reversible.
2. **P0-5 + P0-6** — identity re-auth + seal schema. Restores the chain of authority; without it every seal is a fallback.
3. **P1-7 + P1-8** — human-lane triage + delta-gate proof. Buys back the attention needed to see the next reality signal.

**P0-1 and P0-2** are already partly executed (orphan killed); the reaper and health decoupling remain.

---

## 8. OBSERVATORY RECONCILIATION (page snapshot 2026-10-23T02:35Z, public-state `generated_at 02:34:23Z`)

The page is **honest in intent but semantically wrong in six places**. Every one is traceable to a consumer reading a neighbouring field — not to missing data.

| # | Page says | Structured source says | Verdict |
|---|---|---|---|
| 1 | `fq 0.391304` + **OPTIMAL** | `arifFlow/health`: `fq.quotient=0.391` (fed, min-gated), `fq.raw_pool_quotient≈1.02` → `legacy_verdict=OPTIMAL`; top-level `verdict=SIMULATION`; vector fq band **PATHOLOGICAL** (h=0.31) | **CROSS-OBJECT PAIRING** — the number is the fed quotient, the label is the raw-pool legacy verdict. Page hides the real verdict (`SIMULATION`). Root cause: `build_public_state.py:1291-1292` reads `fq.quotient` but labels with `fq.get("verdict") or fq.get("legacy_verdict")`. |
| 2 | vault `head_seq 72 · replay verified` | `chain_integrity`: `head_seq=55`, `canonical_entries=72`, `entries=274`, `gap_count=40`, `verified=false`, `corrupt_lines=0` | **FALSE GREEN** — 72 is `canonical_entries`, not head_seq; `verified=false` with 40 gaps. "replay verified" is not supported by the structured block. |
| 3 | CAPABILITY **8/8** | `planes.capability="PARTIAL · 5/8"`; `capabilities.exposed_count=8`, `tested_count=5`, `degraded_count=3` | **OVERCLAIM** — 8/8 is exposed, not proven. Should read `8/8 exposed · 5/8 proven`. |
| 4 | Daily Reality Pulse: GEOX **DOWN** | `organs.geox`: `liveness=live`, `probe_status_code=200`, `governance=HOLD` | **INTERNAL CONTRADICTION** — same page shows GEOX live/200 above. Pulse has `snapshot id: unavailable · observed at: unavailable`; it is unbound. |
| 5 | almost every tile: `source: missing · confidence: unknown · freshness: unavailable` | `organs.*` carry `source`, `last_observed`, `confidence`; `ariflow` carries `source=ariflow:7073/health`, `observed_at` | **PHANTOM ABSENCE** — `planes` exposes bare strings (`"REACHABLE"`), while the UI expects provenance objects. Data exists; the projection drops it. |
| 6 | one `ariflow` block | public-state carries **three keys**: `ariflow`, `arifflow`, `arifFlow` (same hash today) | **DUPLICATE NAMES** — three aliases for one object will diverge silently. One canonical key; aliases only in `schema_aliases`. |

Correct verdicts to render, per source:
- **FQ:** `SIMULATION` (constellation) + `fq dimension PATHOLOGICAL` + `fed_quotient 0.391` + `raw_pool 1.02` — four qualified fields, never one number with a legacy label.
- **Vault:** `head_seq 55 · canonical 72 · entries 274 · gaps 40 · verified false` — chain continuity is **not** verified.
- **Capability:** exposed 8/8, proven 5/8, untested 3/8 (`arif_forge`, `arif_judge`, `arif_seal` — intentionally skipped as irreversible; they need a HOLD-path proof, not a mutation test).
- **GEOX:** live, HTTP 200, governance HOLD — not DOWN.
- **Substrate:** `NOT_PROVEN` in the snapshot (no infra probe) ≠ kernel `substrate_state=HEALTHY` (process-local). Both can be true; the label must name the scope.
- **Authorization:** organ identity `VERIFIED` ≠ session authority `unavailable`; name the axis.

**Fix points (proven by source read):**
- `/root/arifOS/scripts/build_public_state.py:1291-1292` — stop pairing `fq.quotient` with `legacy_verdict`; publish `verdict` (constellation) and `raw_pool_quotient` separately.
- Observatory UI renderer — locate before edit (public host root not yet found in `/root/arif-sites`; served via a separate Caddy/Cloudflare path). Do not patch blind.
- `chain_integrity` consumer — render `head_seq` from `head_seq`, not `canonical_entries`; gate "verified" on `verified==true AND gap_count==0`.

---

## 9. CORRECTIONS TO MY OWN EARLIER CLAIMS (F2)

1. **Retracted:** "tool counts 8/63/49/9 are inconsistent." `tool_count_semantics` documents registry > declared > exposed as by design (aliases). Only `operational_tools=5` vs public 9 is a real gap.
2. **Accepted:** the falsifiable composition test I proposed cannot run — no delta stream exists. HERMES's 7-day proxy is the correct substitute.
3. **Refined:** "per-trajectory irreversibility accountant" is necessary but not first. Declaration (surface + ceiling + unit) precedes the accountant; enforcement (L4) must accompany it.
4. **New:** F8 is one-axis-bound (P=0.1968), not a four-axis failure. This changes the fix from "improve everything" to "find why P is 0.197".
5. **New (F1):** FQ role-blindness penalises auditors by construction. 333-AGI's 24:1 verify ratio is its job, not fossilisation. The metric must be role-aware before it can be used as a constitutional signal.

---

## Appendix A — Probe commands (reproducible)
```
curl -s http://127.0.0.1:8088/health | jq '{status,floor_passed,degraded_reasons,apex_scalars,fq,seal_readiness,state_axes}'
curl -s http://127.0.0.1:7073/health | jq '.fq.per_actor'
ps -eo pid,ppid,etime,rss,cmd --sort=-rss | head
cat /proc/pressure/{cpu,memory,io}
systemctl show arifos.service -p MemoryMax -p MemoryHigh -p MemoryCurrent
ls /etc/systemd/system/arifos.service.d/*.conf | wc -l
jq '.jobs | length' /root/HERMES/cron/jobs.json
python3 /root/HERMES/scripts/zen/validate_jobs_json.py check
ss -ltnp | grep -E ':(3199|3280|28188|8088|7072|7073)'
tail -1 /root/arifOS/VAULT999/SEALED_EVENTS.jsonl | jq
```
