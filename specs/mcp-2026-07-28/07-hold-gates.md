# HOLD / SEAL Gates — MCP 2026-07-28 Alignment

**Status:** SPEC READY · gates compile into enforceable mechanisms per Canon #0
**Date:** 2026-09-29
**Owner:** FI-008 (kimi-code)
**Canon grounding:** Canon #0 three-test gate; Constitutional Architecture Canon; Shadow Authority Doctrine

---

## 0. Purpose

Per APEX-ZEN: execute within authority. This document catalogs every HOLD/SEAL gate blocking execution of the patches in `01-P0-arifos-patches.md`, `02-geox-outputschema-patches.md`, `04-l1-attribute-contracts.md`, `05-12-conformance-gates.md`, and `06-miec-acceptance-benchmark.md`.

For each gate: WHY HOLD · WHO UNBLOCKS · HOW · CANON-#0-GATE · SEVERITY.

---

## 1. Authority gates

### G-AUTH-1: OBSERVE_ONLY session

**WHY HOLD:** My session is `OBSERVE_ONLY` (`mutation_allowed: false, seal_allowed: false`). Cannot forge code, cannot seal records.
**WHO UNBLOCKS:** Sovereign (F13) via `arif_init` with Ed25519-signed nonce.
**HOW:**
```bash
# Sovereign signs nonce and re-inits
NONCE=$(curl -sS -X POST $ENDPOINT -d '...' | jq -r .challenge.nonce)
SIGNED=$(echo -n "$NONCE" | openssl pkeyutl -sign -inkey /root/.arifos/keys/sovereign_ed25519.pem | base64)
curl -sS -X POST $ENDPOINT -d "{
  \"mode\":\"init\",
  \"actor_id\":\"arif\",
  \"nonce\":\"$NONCE\",
  \"actor_signature\":\"$SIGNED\"
}"
```
**CANON #0:** (a) bearer-leak prevention ✓, (b) enforced via Ed25519 ✓, (c) production delegation decision enabled ✓
**SEVERITY:** BLOCKING

### G-AUTH-2: Signing-lane key drift

**WHY HOLD:** `challenge_required: true` by default. Every full-authority init needs Ed25519 signature. The signing key may have drifted.
**WHO UNBLOCKS:** Sovereign + AAA (key rotation ceremony).
**HOW:** Rotate `kid: default` → new key; publish public key on arif-fazil.com/000; distribute to trusted agents.
**CANON #0:** (a) identity-spoofing prevention ✓, (b) Ed25519 ✓, (c) audit trail intact ✓
**SEVERITY:** BLOCKING for production

---

## 2. Substrate gates

### G-SUB-1: DEPLOYMENT_DRIFT

**WHY HOLD:** Live arifOS reports `substrate.state: DEGRADED, reason_code: DEPLOYMENT_DRIFT, software_release.drift: true`. `built_commit: b9eeec7` ≠ `deployed_commit: b9eeec7e6f3c0776233369e112483b6985411e4b`.
**WHO UNBLOCKS:** A-FORGE team (build/deploy reconciliation).
**HOW:**
```bash
# 1. Compare source vs built vs deployed
git -C /opt/arifos/source rev-parse HEAD
cat /opt/arifos/current/venv/lib/python3.13/site-packages/arifosmcp/.built_commit
ps -p 2552832 -o cmd
# 2. Rebuild source → built → redeploy
cd /opt/arifos/source && git pull && make wheel && pip install --force-reinstall dist/*.whl
# 3. Restart service
systemctl restart arifos
# 4. Verify
curl -sS $HEALTH | jq '.substrate.state, .software_release.drift'
```
**CANON #0:** (a) silent-corruption prevention ✓, (b) explicit reconciliation procedure ✓, (c) health-check gating ✓
**SEVERITY:** BLOCKING for live deploy

### G-SUB-2: Receipt chain gaps

**WHY HOLD:** `receipt_chain_valid: false, status: gaps-found, entries: 61, corrupt_lines: 0, anchor_ref: https://arif-fazil.com/000`. Note: "integrity only — veracity requires external replay".
**WHO UNBLOCKS:** AAA audit team.
**HOW:**
```bash
# 1. Replay proof spine
arifos proof-replay --mission PROOF-SPINE-20260731T023927Z --verify
# 2. Find gaps
arifos receipt-audit --canonical --report-gaps
# 3. Patch gaps (this is a sensitive operation — requires sovereign approval)
```
**CANON #0:** (a) audit-trail-tampering prevention ✓, (b) replay mechanism exists ✓, (c) decision-traceability restored ✓
**SEVERITY:** BLOCKING for E2E_PROOF_SPINE_V1 claim

### G-SUB-3: Probe-Before-Panic doctrine compliance

**WHY HOLD:** Per F13_RATIFIED_CHAT 2026-09-13 doctrine: "vision-blind scar; no 'down' declaration before inventory sweep + alternate-lane test". Before declaring any organ "down", must:
1. Inventory sweep across all reachable endpoints
2. Alternate-lane test (different transport, different port, different protocol era)
3. Document negative-warrant with same rigor as positive
**WHO UNBLOCKS:** Self (compliance is checkable).
**HOW:** Before any "X is broken" claim, run the inventory probe; attach results.
**CANON #0:** (a) same-warrant-for-negative ✓, (b) probe pattern ✓, (c) prevents panic-declarations ✓
**SEVERITY:** ALWAYS ON

---

## 3. Sovereignty gates (require F13 SOVEREIGN binary)

### G-SOV-1: PETRONAS data residency (Path A vs Path B)

**WHY HOLD:** Block H 3D is PETRONAS CONFIDENTIAL. Moving to arif-fazil.com VPS likely crosses data boundary; carries HR/legal exposure. Spec docs are safe; data ingestion is not.
**WHO UNBLOCKS:** Sovereign (F13).
**OPTIONS:**
- **Path A:** GEOX runs inside PETRONAS infrastructure. Block H 3D stays on PETRONAS side. GEOX consumed as service.
- **Path B:** GEOX receives only derived numbers (no coordinates, no volumes). Caps what can be done — no spatial reasoning, no canopy coalescence.
**CANON #0:** (a) data-leak prevention ✓, (b) explicit path choice ✓, (c) institutional risk avoided ✓
**SEVERITY:** BLOCKING for actual Block H ingestion

### G-SOV-2: Production deployment authorization

**WHY HOLD:** Patches A1, A2, A3, B1-B8 touch production paths. Cannot deploy without sovereign sign-off.
**WHO UNBLOCKS:** Sovereign (F13) + A-FORGE.
**HOW:** Sovereign signals go; A-FORGE applies patches in staging first; conformance gates pass; then production.
**CANON #0:** (a) change-control ✓, (b) staged rollout ✓, (c) audit trail ✓
**SEVERITY:** BLOCKING for go-live

### G-SOV-3: Constitutional canon amendments

**WHY HOLD:** Some patches may require updates to constitutional canon (e.g., new floor, new authority band). Canon changes need F13 SOVEREIGN ratification per the constitutional path.
**WHO UNBLOCKS:** Sovereign (F13) via documented ceremony.
**CANON #0:** (a) governance-stability ✓, (b) ceremony-bound ✓, (c) avoids drift-by-patch ✓
**SEVERITY:** AS NEEDED (only if patches touch constitution)

---

## 4. Calibration gates (waiting on data)

### G-CAL-1: L0 attribute chaos cut-off threshold

**WHY HOLD:** Threshold for "is this chaos high enough to call this a chimney?" needs calibration on labelled Morley bodies (Figs. 5–21 on Block H 3D).
**WHO UNBLOCKS:** PETRONAS geoscience team (after Path A decision).
**HOW:**
1. Load Morley reference bodies (Figs. 5–21)
2. Compute variance/coherence/chaos on each
3. Hand-label "yes chimney" / "no chimney"
4. ROC analysis → optimal threshold
5. Encode as default in L1 detector
**CANON #0:** (a) default-misclassification prevention ✓, (b) ROC-derivable ✓, (c) decision-threshold calibrated ✓
**SEVERITY:** BLOCKING for production classifier

### G-CAL-2: Rim/core amplitude ratio threshold

**WHY HOLD:** Same as G-CAL-1 but for "is the rim amplitude high enough relative to the core to call this a geobody?"
**WHO UNBLOCKS:** Same.
**SEVERITY:** BLOCKING

### G-CAL-3: Contrast shell radius (200 vs 500 m)

**WHY HOLD:** Shell radius (the 200–500 m annulus around the core) needs validation against labelled bodies.
**WHO UNBLOCKS:** Same.
**SEVERITY:** BLOCKING

### G-CAL-4: Polarity convention for Morley data

**WHY HOLD:** Polarity gate requires confirmed convention. Morley's stated convention is "black = peak" but needs to be registered via `geox_calibration_register_witness` before any L0 ingestion.
**WHO UNBLOCKS:** PETRONAS geoscience team.
**SEVERITY:** BLOCKING

---

## 5. Test gates (machine-checkable, run before declaring done)

### G-TEST-1: 12 conformance gates Q1-Q12

**WHY HOLD:** Cannot declare "aligned with MCP 2026-07-28" without all 12 gates green.
**WHO UNBLOCKS:** Self-executable once patches A1-A3 + B1-B7 land.
**HOW:** Run `arif_conformance_test.sh` from `05-12-conformance-gates.md`.
**CANON #0:** (a) falsifiable ✓, (b) reproducible ✓, (c) measurable improvement ✓
**SEVERITY:** GO/NO-GO gate for alignment claim

### G-TEST-2: MIEC acceptance benchmark (5 sub-gates)

**WHY HOLD:** Cannot declare "MIEC identification works" without all 5 sub-gates green.
**WHO UNBLOCKS:** Self-executable once L0/L1/L2 + calibration done.
**HOW:** Run `test_miec_acceptance.py` from `06-miec-acceptance-benchmark.md`.
**CANON #0:** (a) falsifiable ✓, (b) reproducible ✓, (c) measures EUREKA-binding invariant ✓
**SEVERITY:** GO/NO-GO for production MIEC workflow

---

## 6. Canon-compliance gates

### G-CANON-0: Three-test gate per new canon

**WHY HOLD:** Canon #0 (F13_SEAL 2026-09-21) requires every new law to pass three tests:
- (a) eliminate demonstrated failure class
- (b) compile into enforceable mechanism
- (c) materially improve a decision
**WHO UNBLOCKS:** Self (every patch above passes; this is a meta-check).
**SEVERITY:** ALWAYS ON

### G-CANON-1: Anti-overengineering (Anti-Bangang LAW 8)

**WHY HOLD:** "Satu masalah. Satu owner. Satu jalan." — no duplicate systems.
**WHO UNBLOCKS:** Self (verify no new system unless failure class demonstrated).
**SEVERITY:** ALWAYS ON

### G-CANON-2: Probe-Before-Panic (F13_RATIFIED 2026-09-13)

**WHY HOLD:** Same-warrant-for-negative doctrine.
**WHO UNBLOCKS:** Self.
**SEVERITY:** ALWAYS ON

### G-CANON-3: Reality > Everything (APEX-ZEN Runtime Prompt)

**WHY HOLD:** APEX-ZEN principle. No claim without reality ground.
**WHO UNBLOCKS:** Self.
**SEVERITY:** ALWAYS ON

### G-CANON-4: Anti-Shadow (Shadow Authority Doctrine 2026-09-29)

**WHY HOLD:** "The strongest authority is rarely the loudest authority; transformation path > everything; documentation ≠ runtime; count transitions not components."
**WHO UNBLOCKS:** Self.
**SEVERITY:** ALWAYS ON

---

## 7. Open questions (carry_forward.json → open_questions)

Per F13_RATIFIED 2026-09-25: unresolved questions are first-class primitives, not missing values.

| ID | Question | Why unresolved | Unblock |
|---|---|---|---|
| Q-OPEN-1 | Should `mcp_versions_supported` default to 2026-07-28 or stay 2025-11-25 until legacy clients migrate? | Dual-era migration timeline | Sovereign + AAA |
| Q-OPEN-2 | Does the Ed25519 public key need re-publication on arif-fazil.com/000 after rotation? | Identity binding for sovereign | Sovereign |
| Q-OPEN-3 | Should L0 export format be SEG-Y + sidecar JSON, or ZGY + native metadata? | Interoperability with Petrel/DSG | PETRONAS Path A team |
| Q-OPEN-4 | Does hermes witness need its own MCP server, or share arifOS? | Federation topology | Sovereign |

---

## 8. Summary — what unblocks what

```
                    ┌─────────────────────────────────────┐
                    │ Sovereign grants MUTATE band        │ G-AUTH-1
                    │ (Ed25519-signed nonce)              │
                    └────────────┬────────────────────────┘
                                 ▼
                    ┌─────────────────────────────────────┐
                    │ A-FORGE reconciles DEPLOYMENT_DRIFT │ G-SUB-1
                    └────────────┬────────────────────────┘
                                 ▼
                    ┌─────────────────────────────────────┐
                    │ AAA replays receipt chain           │ G-SUB-2
                    └────────────┬────────────────────────┘
                                 ▼
                    ┌─────────────────────────────────────┐
                    │ Forge team applies P0 patches       │ A1+A2+A3
                    │ (REDACT, discover, stateless)       │
                    └────────────┬────────────────────────┘
                                 ▼
                    ┌─────────────────────────────────────┐
                    │ Sovereign chooses PETRONAS Path A/B │ G-SOV-1
                    └────────────┬────────────────────────┘
                                 ▼
                    ┌─────────────────────────────────────┐
                    │ L0 attributes ingested              │ G-CAL-1..4
                    │ (calibrated on Morley reference)    │
                    └────────────┬────────────────────────┘
                                 ▼
                    ┌─────────────────────────────────────┐
                    │ L1 detectors + L2 classifiers built │ C1-C3
                    │ (topology × strat axis on)          │
                    └────────────┬────────────────────────┘
                                 ▼
                    ┌─────────────────────────────────────┐
                    │ 12 conformance gates pass           │ G-TEST-1
                    │ MIEC acceptance benchmark passes    │ G-TEST-2
                    └────────────┬────────────────────────┘
                                 ▼
                    ┌─────────────────────────────────────┐
                    │ Production deployment               │ G-SOV-2
                    │ (sovereign go + A-FORGE apply)      │
                    └─────────────────────────────────────┘
```

**Critical path:** G-AUTH-1 → G-SUB-1 → G-SUB-2 → A1+A2+A3 → G-SOV-1 → G-CAL-* → C1-C3 → G-TEST-1 → G-TEST-2 → G-SOV-2

**Parallel paths:** G-CANON-* (always on) · G-SOV-3 (only if patches touch constitution)

---

## 9. EUREKA binding

> **Every HOLD gate is a measurable criterion, not a feeling.** When a gate flips green, the next patch is permitted. When a gate flips red, the patch is barred. The system never relies on a human "I think we're ready" — it relies on a machine-checkable invariant.

This is the F13 SOVEREIGN/AGI separation of powers: humans decide intent, machines decide readiness, governance decides authority.

---

DITEMPA BUKAN DIBERI ⚒️
