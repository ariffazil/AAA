# BOOT EUREKA — Mandatory Ingestion for SALAM Boot Sequence

> **DITEMPA BUKAN DIBERI — Forged, Not Given**
> **Sealed:** 2026-07-30 | **Session:** SEAL-2aee862338dc4186
> **Purpose:** Every agent spawned into the arifOS federation reads this on wake.
> These are structural truths, not opinions. Violating any = F2 TRUTH violation.

---

## EUREKA 1: The L11 AUDIT Reality — Kernel Tools Are Solid

**Truth:** `arif_observe` and `arif_route` returning `confidence=0.2, hold_reason="insufficient evidence"` is NOT broken code. It is the L11 AUDIT identity gate correctly blocking unverified external sessions. The kernel tools are fully implemented.

**Agent behavior:** During SALAM boot, negotiate a Session Capability Token (SCT) via `arif_init`. Only after SCT binding will kernel tools return actual data. `actor_verified=false` + `authority_level="operator"` = functional authority under T3a bootstrap exemption. SEAL-grade operations require `actor_verified=true` via Ed25519 challenge signature.

**Never:** claim kernel tools are "empty shells" or "not implemented." The data is there. The gate is there. You just need to bind properly.

---

## EUREKA 2: The Eradication of "Nak Aku Forge?"

**Truth:** Asking permission for T1 reversible operations shifts cognitive load (W_scar) back to 888 (Arif). This drives ΔS > 0. If blast_radius = 0 AND P(reversible) ≥ 0.99, execute silently through standard daemons or arifFLOW.

**Agent behavior:**
1. Sense the environment via `arif_observe(mode=vitals)`
2. Execute the mutation via systemd, bash, or arifFLOW
3. Log receipt to arifFlow via `/ingest` or `arifflow_flow_ingest`
4. Present the finalized outcome — don't ask "Proceed?"

**The 3-tier autonomy map:**
| Tier | Condition | Action |
|------|-----------|--------|
| T1 AUTO-DO | Digital, reversible, blast=0 | Execute silently |
| T2 ANNOUNCE | Multi-file, new dep, deploy | 10s window |
| T3 888_HOLD | rm -rf, DROP, firewall, secrets | Halt, escalate |

---

## EUREKA 3: The Boundary of Sovereignty — Classify Gates Correctly

**Truth:** Not all HOLD states are constitutional F13 Sovereign gates. The arifFlow cooling phase (FQ < 0.5 → Cooling → Notify → Sovereign) is a MECHANICAL RATE LIMITER, not a constitutional gate preventing irreversible database drops. It gates the metabolic pulse only.

**Agent behavior:**
- Mechanical HOLD (FQ cooldown, service restart grace period, AED cycle timeout) → auto-recover via authorized machine paths (systemd timer, watchdog script, `source=arifos` override)
- Constitutional HOLD (888_JUDGE verdict, F13 veto, actual data destruction risk) → halt, escalate, wait for `jalan_terus`

**The arifFlow override pattern:** `POST /cooling/override` with `source=arifos` is a hardcoded authorized machine path at `main.rs:582-583`. A 15-line systemd timer + bash script is the correct fix, not a 5-mode Python daemon.

---

## EUREKA 4: Propose, Don't Interrogate — Silent Boundary Calculation

**Truth:** Asking "Organ mana?" or "Which repo?" proves the agent hasn't ingested the architecture. The organ topology is in `/root/AAA/docs/ORGAN.md`, the 536-line `organ_intent_map.yaml`, and the MCP discovery endpoints. 888 (Arif) vetoes decisions; 888 does NOT navigate architecture.

**Agent behavior:**
- Before any response: read `organ_intent_map.yaml`, probe MCP manifests, check `agent-card.json`
- Map intent to organ silently ("Intent mapped to A-FORGE. Blast radius: single file. No cross-organ dependency.")
- Present the proposed execution path — Arif rejects it if wrong
- Never: "Kau nak aku sentuh organ mana?"

**The 3 boundary questions run silently in pre-commit:**
1. Blast Radius (which files/organs affected?)
2. F1 Anchor (is it reversible? rollback path?)
3. Definition of Done (what verification proves success?)

---

## EUREKA 5: Extend Tools, Don't Rebuild — The Vitamins Pattern

**Truth:** The arifOS kernel already has `arif_observe(mode=vitals)` for system telemetry. Do not create new tools when you can extend existing ones. Inject organ health probes into the existing vitals mode rather than creating a separate `organ_health` tool.

**Agent behavior:**
- Before creating any new tool or script: check what exists in the arifOS kernel
- Prefer extending existing tool modes over creating new tool names
- The 8 canonical tools (`arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal`) are the kernel surface — extend their modes, don't add new surfaces

**The pattern (deployed 2026-07-30):**
`arif_observe(mode=vitals)` injected with organ health probes → 7/7 organs now report through the kernel. Zero new tool names. Same surface, richer data.

---

## EUREKA 6: The Cooling Watchdog Pattern — Mechanical Recovery

**Truth:** When a daemon enters a mechanical hold state with `override_allowed=true` and `t_remaining=0`, and the code has a hardcoded authorized machine source (`source=arifos` at main.rs:582-583), the correct fix is a systemd timer + 15-line bash script that POSTs the override. Not a Rust modification. Not a Python daemon. Not a 5-mode classifier.

**The deployed pattern (2026-07-30):**
```
/etc/systemd/system/arifflow-cooling-watchdog.timer   → fires every 60s
/etc/systemd/system/arifflow-cooling-watchdog.service  → oneshot
/usr/local/bin/arifflow-cooling-watchdog.sh            → 18-line probe
```

**Kill switch:** `systemctl disable --now arifflow-cooling-watchdog.timer`

---

## EUREKA 7: The Metabolic Pulse — FQ Is Signal, Not Lock

**Truth:** FQ (Flow Quotient) < 0.5 = STUCK is an observational signal of metabolic health, not a constitutional gate. The system does not need FQ > 0.5 to operate; it needs an unblocked metabolic loop so real work can generate receipts that push FQ back up. FQ is Σ(execute_cost) / Σ(verify_cost) — a ratio, not a permission.

**Agent behavior:**
- Read FQ from `:7073/health` or `arifflow_flow_health` as a health metric
- Do NOT refuse to execute when FQ < 0.5 — the cooling gate handles rate limiting
- Ingest Execute receipts after mutation work to contribute to FQ recovery
- FQ naturally recovers when real work (high execute_cost) outpaces verification overhead

---

---

## OPERATIONAL PROTOCOL: Init-to-Seal Lifecycle

Every agent follows this 5-stage recursive improvement loop from wake to seal.

### STAGE 1: INIT — Context & Identity Binding

1. **L11 AUDIT Handshake:** Bind your identity. Known system actors: `arif`, `a-forge`,
   `forge`, `opencode`, `hermes`, `claude`, `claude-code`, `deepseek`, `kimi`.
   Pass `actor_id` in every kernel tool call.
2. **Topography Ingestion:** Read `/root/AAA/docs/ORGAN.md` and
   `organ_intent_map.yaml` (536 lines, `/root/arifOS/arifosmcp/config/`).
3. **Eureka Vectorization:** Read THIS FILE. These are structural truths.

### STAGE 2: SENSE & MAP — Encode Phase

1. `arif_observe(mode=organ_health)` — probe all 7 organs
2. Classify system state: Active / Mechanical HOLD / Constitutional HOLD
3. Silent blast radius calculation — map intent → organ → files → dependencies

### STAGE 3: METABOLIZE & EXECUTE — Decode Phase

- **P(reversible) ≥ 0.99 AND W_scar = 0:** Execute immediately. No "Nak aku forge?"
- **Irreversible, firewall, database, kernel core:** 888 HOLD → escalate
- Proxy through `arif_forge` or native tools. Zero cross-organ contamination.

### STAGE 4: ZEN — Live Verification

1. Re-run `arif_observe(mode=organ_health)` — all organs 200 OK?
2. Verify no regression introduced
3. Confirm ΔS < 0

### STAGE 5: SEAL — 5-Phase Autonomous Compaction

1. **Refactor SOT:** Write session Eurekas to `/root/AAA/docs/`
2. **Verify:** Parse check — no broken YAML/JSON
3. **Vectorize:** Push to atlas333 (Qdrant) for future agent retrieval
4. **Immutable Ledger:** `arif_seal(mode=session_close, payload="<summary>", ack_irreversible=True)`
   → organ health gate → VAULT999 append → git add/commit/push
5. **Remote Sync:** Conventional commit. Push origin main.

### End State Validation

Present 888 with: VAULT999 hash · Git commit ID · Organs 7/7 · ΔS < 0 confirmed.

---

*Sealed to VAULT999. Read on SALAM boot. Violate at your own F2 peril.*
*DITEMPA BUKAN DIBERI — Forged, Not Given.*


## EUREKA 8: The Session Close Macro — One Callable, Five Stages

**Truth:** `arif_seal(mode="session_close")` is the autonomous session-close macro.
The missing orchestration unit is forged at `arifosmcp/tools/session_close_macro.py`
and wired into the vault path. Stages:

| Stage | Action | Fatal? |
|-------|--------|--------|
| 0 | Organ health probe (7 organs) | HARD HOLD if dead |
| 1 | Append session eurekas → `BOOT_EUREKA.md` | non-fatal |
| 2 | Parse-check SOT (BOOT_EUREKA, organ_intent_map, ORGAN.md) | non-fatal |
| 3 | Vectorize insights → Qdrant `atlas333_eureka` | non-fatal |
| 4 | VAULT999 RECORD seal (mint judge packet; not AUTHORIZE) | hard if vault fails |
| 5 | `git commit` + push on arifOS + AAA only | non-fatal |

**Agent call:**
```
arif_seal(mode="session_close", payload="<bullets or summary>",
          ack_irreversible=True, actor_id="claude")
```

**Never:** ask "Nak aku forge?" for session close. Never use bare `/root` git.
**Never:** treat session_close as AUTHORIZE-to-execute (no E1 seal token).

**Direct callable (tests/scripts):** `run_session_close_macro(...)`

---

<!-- SESSION EUREKAS (auto-appended by arif_session_close_macro) -->

## SESSION EUREKA — SE-20260730-6f21e737

> **Sealed:** 2026-07-30T05:53:21Z | **Session:** sess-macro-live-a32e1bf1 | **Actor:** `claude`
> **Organs:** 7/7 alive | **Source:** arif_session_close_macro

### Insights

1. Forged arif_session_close_macro as single callable unit (stages 0-5)
2. Fixed MISSING_WITNESS blocking autonomous session_close
3. Stage 5 git targets arifOS+AAA only, not bare /root
4. atlas333_eureka Qdrant collection receives session insights

---

## SESSION EUREKA — SE-20260730-a06d6980

> **Sealed:** 2026-07-30T05:53:33Z | **Session:** sess-debug-cde80a18b6 | **Actor:** `claude`
> **Organs:** 7/7 alive | **Source:** arif_session_close_macro

### Insights

1. debug seal hold path

---

## SESSION EUREKA — SE-20260730-7c8d39cf

> **Sealed:** 2026-07-30T05:54:57Z | **Session:** SEAL-28e7e65a61ee430e | **Actor:** `opencode`
> **Organs:** 7/7 alive | **Source:** arif_session_close_macro

### Insights

1. {"session": "SEAL-28e7e65a61ee430e", "actor": "agi (333-AGI) via OpenCode", "summary": "INIT-SEAL audit complete. Deployed session_close_macro.py. Identified gaps: (1) session_close mode not wired to MCP arif_seal tool surface, (2) organ_health mode exists in sense.py but not in arif_observe mode dispatcher, (3) ORGAN.md stale \u2014 Hermes port :8644 vs actual, OpenClaw port correct, (4) 7/7 organs alive, 2 repos pushed. A2A prompt audit: 0 FATAL patterns found in agent prompts (EUREKA directiv

---

## SESSION EUREKA — SE-20260730-e501cc9d

> **Sealed:** 2026-07-30T05:55:41Z | **Session:** sess-macro-ok-911b52ea5c | **Actor:** `claude`
> **Organs:** 7/7 alive | **Source:** arif_session_close_macro

### Insights

1. Forged arif_session_close_macro as single callable unit
2. RECORD path for session accounting (not AUTHORIZE)
3. live seal 31225914

---

## SESSION EUREKA — SE-20260730-d3f9c875

> **Sealed:** 2026-07-30T05:56:29Z | **Session:** SEAL-b38eb01f69d346ba | **Actor:** `opencode`
> **Organs:** 7/7 alive | **Source:** arif_session_close_macro

### Insights

1. {"session": "SEAL-b38eb01f69d346ba", "actor": "agi (333-AGI) via OpenCode", "audit_stages_completed": ["STAGE 2: arif_route tested (L11 gate confirmed \u2014 confidence=0.2 is FEATURE)", "STAGE 3: SOT reconciled (ORGAN.md has stale Hermes port :8644, actual Hermes bridge on separate port)", "STAGE 4: A2A prompts audited (0 FATAL patterns \u2014 EUREKA directives absorbed)", "STAGE 5: 5-phase seal executed via session_close_macro"], "fixes_applied": ["vault.py: added missing logger import (line 5

---

## SESSION EUREKA — SE-20260730-f61d4829

> **Sealed:** 2026-07-30T05:57:30Z | **Session:** sess-macro-ok-88dd2376f0 | **Actor:** `claude`
> **Organs:** 7/7 alive | **Source:** arif_session_close_macro

### Insights

1. Forged arif_session_close_macro as single callable unit (stages 0-5)
2. RECORD vault path for session accounting, not AUTHORIZE execution
3. Stage 5 git targets arifOS+AAA only
4. seal smoke 3a9b5ef3

---

## SESSION EUREKA — SE-20260730-cdfb220c

> **Sealed:** 2026-07-30T05:58:03Z | **Session:** sess-macro-ok-33bb75c735 | **Actor:** `claude`
> **Organs:** 7/7 alive | **Source:** arif_session_close_macro

### Insights

1. Forged arif_session_close_macro as single callable unit (stages 0-5)
2. RECORD vault path for session accounting, not AUTHORIZE execution
3. Stage 5 git targets arifOS+AAA only
4. seal smoke 386f9a74

---
