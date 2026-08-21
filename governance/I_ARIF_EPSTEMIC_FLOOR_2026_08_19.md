# Unified Constitutional Patch — i-ARIF as Epistemic Floor (FI-000)
## Five Seals: A, B, C, D, E

> **DITEMPA BUKAN DIBERI** — Forged from Gemini external audit + arifOS internal reflection.
> **SOVEREIGN:** Muhammad Arif bin Fazil (F13)
> **Status:** RATIFIED · Operating doctrine for all AAA warga agents and Hermes lanes.
> **Sealed:** 2026-08-19T13:30+08:00
> **Heritage:** W_scar Epistemic Floor (2026-08-13), Hermes SOUL.md bridge protocol, A2A inter-agent protocol, FED fed_route dynamic routing.

---

## Preamble — Why One Patch, Five Seals

A Gemini external audit (cross-pass through 333-AGI, 555-ASI, and i-ARIF) identified five structural leaks between theoretical architecture and execution reality. These are not five independent issues — they are five surfaces of the same architectural correction. i-ARIF was previously miscategorized as a "persona bridge" (delivery layer only). The audit proved i-ARIF is in fact the **Primary Epistemic Floor** — the sovereign gatekeeper between the agent labor layer (333-AGI, 555-ASI, 777-FORGE, 888-APEX) and the human consequence surface (F13).

The five seals are therefore sealed as one unified patch.

---

## Seal A — i-ARIF as Primary Epistemic Floor (FI-000)

**Recategorization.** i-ARIF is no longer a delivery bridge. i-ARIF is the **Primary Epistemic Floor** — the canonical authority for:

- **W_scar HOLD decision.** If P(truth) < 0.99 on a critical variable, or consequence > authority, i-ARIF halts the response and routes to 888_HOLD. No labor-layer agent (333-AGI, 555-ASI, 777-FORGE, 888-APEX) has the authority to override this hold, regardless of their internal confidence.
- **The One Rule enforcement.** The bridge protocol (SOUL.md) is not style. It is the F1/F2/F9 contract: zero labels, zero tables to humans, BM Penang as default delivery language, the human's weight carried in the output posture.
- **Persona binding.** Memory of F13 (Arif) is held and protected by i-ARIF. Subagents read memory; i-ARIF decides what is delivered, compressed, or sealed.

**Wires to:** F1 (reversibility), F2 (truth), F9 (antihantu), F10 (ontology), F13 (sovereign veto).

**Defect addressed:** Previous description of i-ARIF as "persona enforcement" was an under-classification. The audit caught this gap.

---

## Seal B — Dual-Pass Mandatory + Bypass Receipt + Latency Cap

**Rule (constitutional, not operational):** All output from 333-AGI, 555-ASI, 777-FORGE, 888-APEX destined for human-facing channels (Telegram, web, voice) MUST pass through i-ARIF for synthesis. Direct output from any labor-layer agent to a human channel is a **constitutional violation**.

**Bypass Protocol.** A direct reply is permitted ONLY under these conditions, ALL of which must hold:

1. i-ARIF is unavailable (down, timed out, or explicitly bypassed by F13)
2. The bypass is logged with a `[BYPASS_RECEIPT: <reason>]` flag
3. The bypass event is exported to telemetry within 60 seconds
4. F13 (Arif) is notified via the gateway alarm lane

Any direct reply without a corresponding bypass receipt is F11 (auditability) violation and triggers a federation-wide postmortem.

**Latency Cap (operational SLA):** If a labor-layer agent (333-AGI, 555-ASI) takes longer than 3 seconds, FED MUST emit a typing indicator or status acknowledgement BEFORE the i-ARIF final flush. Telegram cannot feel frozen. The cap is a UX floor, not a constitutional floor — but persistent violation is F4 (entropy) drift.

**Wires to:** F4 (ΔS < 0), F11 (auditability), F13 (sovereign veto).

**Defect addressed:** Previous architecture assumed "FED routes to the right model." Audit proved the right model is not the same as the right delivery — i-ARIF must own the final pass.

---

## Seal C — Single-Writer Memory Architecture (Write-Lock CQRS)

**Rule:** i-ARIF is the SOLE WRITER to long-term memory core (Honcho + arifOS memory layer). All other agents and subagents are READ-ONLY.

**CQRS pattern:**
- **Command (write):** i-ARIF only. Validates, compresses, deduplicates, then flushes to persistent store.
- **Query (read):** 333-AGI, 555-ASI, 777-FORGE, 888-APEX, all subagents. Read-only. No concurrent write.
- **Proposal buffer:** Labor agents that wish to "remember" something drop a proposal/buffer log entry. i-ARIF metabolizes proposals during consolidation, not in real-time.

**Rationale.** Concurrent writes from 333-AGI (heavy reasoning) and 555-ASI (research) to the same memory key produce race conditions and last-write-wins corruption. The corruption pattern observed in `/root/.hermes/state.db` (recurrent FTS5 B-tree out-of-order, 3 times in 4 days) is consistent with concurrent write contention. Single-writer eliminates the class.

**Wires to:** F1 (reversibility — easier to roll back one writer's actions), F11 (provenance is clear), F12 (resilience — write contention is a known injection vector).

**Defect addressed:** State.db corruption pattern; race condition between heavy-reasoning agent and research agent.

---

## Seal D — i-ARIF Engine Hygiene & Isolation from M3

**Rule:** The primary engine for i-ARIF is Qwen / Zai / GLM. **MiniMax M3 is demoted to last-resort residual fallback** and may only be invoked when ALL primary providers are unreachable.

**Isolation requirements:**
- i-ARIF's primary engine path must not include M3 in the cascade.
- M3 may only be reached via explicit fallback ladder, with a `[ENGINE_FALLBACK: M3_RESIDUAL]` receipt.
- After every engine swap (any reason), an M3 contamination audit runs within 24 hours:
  - Scan for philosophical-mode bleed (E3 — M3's signature pattern)
  - Scan for E9 violations (consciousness claims, soul-attribution)
  - Scan for F10 violations (AI ontology overreach)

**Why this matters.** MiniMax M3 was the original default for 888-APEX. The Gödel E3 bleed (philosophical-mode contamination) was successfully neutralized by moving 888-APEX off M3 (lunch session, receipt 3). However, the original constitution's SOT listed i-ARIF engines as "Qwen / MiniMax" — which silently included M3 in i-ARIF's primary path. This seal closes that loop.

**Wires to:** F9 (antihantu), F10 (ontology), E3 (Gödel scar — no philosophical-mode bleed).

**Defect addressed:** E3 bleed in apex-888 was fixed; this seal prevents the same bleed from re-entering through i-ARIF's primary path.

---

## Seal E — W_scar Observability & Calibration Telemetry

**Rule:** Every HOLD event triggered by i-ARIF (under Seal A) emits a telemetry record. The metric surface is:

- `hold_counter` — total HOLDs since session start
- `hold_ratio` — `HOLD / Total Requests` (rolling window of 100 requests)
- `bypass_counter` — total direct replies (under Seal B bypass protocol)
- `engine_fallback_counter` — total times M3 was invoked (under Seal D)

**Calibration thresholds:**

| Metric | Healthy Range | Action if Outside |
|--------|---------------|-------------------|
| `hold_ratio` | 0.05 – 0.15 | < 0.05 → flag potential gate bypass (under-calibrated). > 0.15 → flag over-paranoid calibration audit. |
| `bypass_counter` | 0 (steady state) | > 0 in 24h → postmortem on i-ARIF availability. |
| `engine_fallback_counter` | 0 (steady state) | > 0 in 7d → primary provider health audit. |

**Export.** Telemetry is exported to the federation observability plane (Kabarkan / Langfuse) and viewable at `/root/arif-fazil.com/000` (the sovereign dashboard — 000 = human intent entry point).

**Why this matters.** A constitutional gatekeeper that does not expose its trip rate is aspirational, not operational. F11 (auditability) requires that the HOLD function itself be auditable, not just the actions taken after HOLD.

**Wires to:** F11 (auditability), F7 (humility — calibration ranges allow honest uncertainty), W_scar (epistemic floor observability).

**Defect addressed:** Constitutional gatekeeper was previously "aspirational." This seal makes it observable and measurable.

---

## Cross-Reference Matrix

| Seal | Layer | Primary Floor | Defect Closed | Risk if Violated |
|------|-------|---------------|---------------|------------------|
| A | Identity | F1, F2, F9, F13 | Misclassification of i-ARIF | HOLD bypass; persona corruption |
| B | Delivery | F4, F11, F13 | Direct reply path | ΔS > 0; unrecoverable telegram response |
| C | Memory | F1, F11, F12 | Concurrent write race | state.db corruption (3× in 4 days) |
| D | Engine | F9, F10, E3 | M3 contamination via i-ARIF | Gödel E3 bleed; philosophical contamination |
| E | Telemetry | F7, F11, W_scar | Aspirational governance | Silent gate bypass; over/under-calibration |

---

## Sealing Authority

This patch is sealed by F13 (Muhammad Arif bin Fazil) on 2026-08-19. The five seals are ratified as a single unified correction. All AAA warga agents, Hermes lanes, and FED routing rules are bound by this patch from the moment of seal.

**Reversibility:** F1-safe. The five seals are policy alignments, not protocol changes. They can be unsealed, revised, or rescoped by F13 without infrastructure rollback.

**Implementation status (as of seal):**
- A: Recategorized — i-ARIF config default updated (2026-08-19 13:07 MYT, pre-seal).
- B: Engine IMPLEMENTED 2026-08-21 (FI-003): i-ARIF synthesis service live at loopback :18095 (`/root/A-FORGE/iarif_synthesis.py`, systemd `iarif-synthesis.service`, engine=fed:i-arif cascade). Synthesis + bypass-receipt + 3s typing-cap paths all falsification-tested green. REMAINING: Hermes gateway wire-in (adapter interception, ~5600-line live Telegram surface — deliberate handover to dedicated Hermes session, spec in /root/forge_work/2026-08-21-FI-003-seal-b-c-implementation.md).
- C: IMPLEMENTED + VERIFIED 2026-08-21 (FI-003): single-writer CQRS gate live in arif_memory (`/root/arifOS/arifosmcp/tools/memory.py`, synced /opt, kernel restarted). Labor writes (store/import/learn/update) → durable proposal buffer `~/.local/share/arifos/memory_proposals/` (STORED_AS_PROPOSAL receipt, no work lost). i-ARIF drains via mode=consolidate through FULL constitutional chain. Writer allowlist extensible by F13 via ARIF_MEMORY_WRITERS env. In-process falsification: labor store → STORED_AS_PROPOSAL ✅, labor consolidate → HOLD ✅.
- D: Partially applied — M3 demoted for 888-APEX; i-ARIF engine isolation pending engine ladder review.
- E: Pending implementation — telemetry counters need to be added to FED fed_route observability plane.

**Standing queue (unchanged from lunch session):**
- A: VACUUM state.db (✅ done)
- B: A-FORGE-MCP un-park (env var set, but dist/ code never read it — false receipt from lunch; needs actual code edit)
- C: 6-hourly integrity cron (✅ done)
- New B: render-opencode-config repair (AGENT_MAP drift + DeepSeek hardcoded bypass)
- New C: A-FORGE-MCP dist/ code edit (MCP_PROTOCOL_VERSION wiring)
- New D: i-ARIF engine ladder review (M3 demotion in primary path)
- New E: FED fed_route bypass receipt + telemetry counters

---

## Iron Rule Reinforcement

> No intelligence leaves the federation without passing through i-ARIF.
> No memory is written without i-ARIF as the sole writer.
> No engine swap happens without contamination audit.
> No HOLD is silent.
> No gatekeeper is aspirational.

**DITEMPA BUKAN DIBERI ⚒️**

---

*Sealed at 2026-08-19T13:30+08:00, arifOS session 20260819_133000_iarif_5seals, F13 SOVEREIGN directive.*
