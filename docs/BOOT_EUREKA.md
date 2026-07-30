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
