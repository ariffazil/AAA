# STAGED F13 ITEMS — awaiting Arif ratification
**Sealed at:** 2026-10-03 10:46 +08
**Compiled by:** FI-005 per F13 directive
**Status:** STAGED — no mutation performed. Setiap item perlu "SAH" Arif.

## BATCH A — REAL BUGS CONFIRMED LIVE (3 items)

### A1. [B-1.B] _ORGAN_REGISTRY unseeded at boot (F8/F13 grade)
- **Live evidence:** `/root/arifOS/arifosmcp/runtime/organ_attestation.py:122` declares `_ORGAN_REGISTRY: dict = {}` (empty). Only populated via `attest_organ()` line 416. No auto-seed at boot.
- **Impact:** Session authority state reads `unseeded in-memory _ORGAN_REGISTRY` until something calls `attest_organ()`. Affects F13 path that requires `execution_readiness=ready + session_authority_state=VERIFIED` at session start.
- **Fix options (pick one):**
  - A. Seed self-attestation at boot/first-init
  - B. Treat absence as "must attest" (not failed)
  - C. Document as design (current behavior intentional)

### A2. [B-1.A] SCT decision-events writer path dead (F11 grade)
- **Live evidence:** `/root/A-FORGE/forge_work/2026-07-17/sct_decision_events/sct_decisions_2026-08-07.jsonl` last write 2026-08-08 00:09. ACT events go to `act_decision_events/` (live, current). SCT writer code no longer in `/root/A-FORGE/src/`. New `forge_work/sct_decisions/` dir empty since Sept 18.
- **Impact:** 56-day F11 audit trail gap for SCT-class decisions. Constitutional.
- **Fix options:**
  - A. Restore SCT writer to its previous path (revert refactor)
  - B. Wire new SCT writer to `forge_work/sct_decisions/` (forward fix)
  - C. Confirm SCT is no longer needed (consolidate into ACT)

### A3. [B-3.B] ACT LANE OUTAGE — signing service degraded
- **Live evidence:** `curl http://localhost:18900/health` returns `{"status":"degraded","can_sign":false,"sovereign_presence_guard":"UNCONFIGURED","pam_module_available":true}`. Key loaded but cannot sign.
- **Impact:** Structural F13 path broken — chat authorization → mutation cannot complete because challenge never signed.
- **Fix options:**
  - A. Configure sovereign_presence_guard (PAM module is available)
  - B. Bypass and accept unsigned F13 challenges (NOT recommended — F11 violation)
  - C. Migrate to a different signing mechanism

## BATCH B — F13-RATIFIED PENDING (from carry_forward, 10 items)

These are carry_forward items where another agent already staged a plan and awaits Arif's "SAH" or specific binary choice. (Already cited in EXECUTION-PLAN-2026-10-03.md.)

- B1. **D1 reader choice** (e-8f999a05): A=Grafana PG, B=FRAME-as-reader, C=stop-write. **Hermes recommends A then B.**
- B2. **D2 organ taxonomy** (e-10286dd4): Draf v2 of organs.yaml. Awaits Arif ratify.
- B3. **D3 otelcol retire vs elevate** (e-d56ce74f): Retire=in-process, Elevate=single gateway. Arif's trust of collector ops is tie-breaker.
- B4. **D4 infra-write lock doctrine** (e-c3791311): Draf exists. Ratify.
- B5. **VOICE-GOVERNOR graft** (e-aee86f33): Draf di `AAA/agents/makcikgpt/VOICE-GOVERNOR-DRAFT.md`. "graft" = arah.
- B6. **AppArmor-confine citizen processes** (e-0ee2a9f6): hermes gateway, opencode, qwen-code, codex, kimi.
- B7. **CANON SEAL** (e-c1e3aa39): L05 seal held since 2026-09-25. Self-reality witness report at `/root/forge_work/2026-09-25-FI003-self-reality-...`.
- B8. **T-06/B13 floor reconcile** (e-559da4): ACT token 'G' carries QDF=0.3149, but T-06 actIngress compares G>=0.80. Token schema vs threshold mismatch.
- B9. **TELUK 1 — 'purge' sejarah WELL** (e-b12ce9): 4 blob rekod intake suara di repo PRIVAT ariffazil/WELL. Purge atau keep?
- B10. **mode_first_gate overlay wire** (e-40ba31): To arif_route intent_canon. Currently heuristic, plugin overwrites with UNKNOWN (99.7%).

## BATCH C — F13-RATIFIED FROM ORIGINAL 10 (additional context)

- C1. **F6 hazard rule** (e-da75fb, e-fadd57): "FRAME observes → FRAME reports → arifOS judges → A-FORGE mutates. No organ may both observe AND mutate same object in one cycle."
- C2. **M3 executor full receipt hook** (e-e34678): Parallel lane, 7 dirty files, coordinate via A-FORGE dirty state.
- C3. **Uncommitted parallel labor** (e-b776a1): DO NOT REVERT (Arif's pref).
- C4. **Graphiti A/B decision** (e-dca981): Reactivate vs retire.
- C5. **D3 arifFlow evidence-origin** (e-dca981): Design approved, no deploy.
- C6. **golden-test canary fixtures** (e-dca981): For audit-repository-entropy.

## BATCH D — F13 binary in need of immediate decision

- D1. **deploy cb2411928** (e-09588447): "F13 BINARY PENDING: deploy cb2411928? yes -> bash /root/arifOS/scripts/deploy-memory-mode-fix.sh"
- D2. **AppArmor for citizens** (e-0ee2a9f6): same as B6
- D3. **mode_first_gate** (e-40ba31): same as B10

## HOW TO RESPOND (Arif)

Per Auto-Seal doctrine: **satu perkataan per item**. Saya akan parse:
- "SAH" → execute the **default** option (the one I'd recommend, marked in CAPS)
- "SAH B" → execute option B
- "TANGGUH" → leave as-is, do not touch
- "VOID" → close the loop without action

Format: `A1=SAH A2=SAH B B7=TANGGUH ...` — saya akan execute in order, dengan receipt per item.

**Atau kalau Arif nak satu perkataan untuk semua yang tak kritikal:** "SAH DEFAULT" — saya apply recommended option untuk semua kecuali A3 (ACT signing), B5 (VOICE-GOVERNOR), B7 (CANON SEAL) — ini saya TANGGUH secara default sebab ia menyentuh identity/canon.

## Mutation this turn

**ZERO.** Semua disusun untuk ratification. Tiada source code diubah.

## Receipts

- [receipt: /root/AAA/docs/audit-receipts/EXECUTION-PLAN-2026-10-03.md:0be426e5]
- [receipt: /root/AAA/docs/audit-receipts/CLUSTER-B1-AUDIT-SHADOWS-2026-10-03.md:0506c283]
- [receipt: /root/AAA/docs/audit-receipts/CLUSTER-B2-B3-B4-2026-10-03.md:87df8bd0]
- [receipt: /root/arifOS/arifosmcp/runtime/organ_attestation.py:line-122-empty-registry]
- [receipt: aaa-signing-18900:can_sign=false,sovereign_presence_guard=UNCONFIGURED]
- [receipt: /root/A-FORGE/forge_work/2026-07-17/sct_decision_events/sct_decisions_2026-08-07.jsonl:mtime-Aug-08]
