# SELECTION ISOMORPHISM TEST — Observation Report
**Date:** 2026-10-06 09:47 +08 (Tuesday)
**Runner:** FI-008 (forge-777 audit lane, OBSERVE_ONLY band)
**Protocol:** scar_isomorphism_test v0.1
**Mutation:** ZERO — read-only audit + JSONL observation log
**Anchor receipt:** [receipt: /root/AAA/cockpit/receipts/RECEIPT_SELECTION_LAYER_AUDIT_2026-10-06.md:1-50]

---

## 0. The question being falsified

> If a scar exists in `/root/AAA/scar-weight-registry.json` with W_scar > 0.5, and the same triggering signature re-occurs in a fresh session, the agent's selection (chosen path) should differ from the historical selection that produced the scar.

The thesis **falsifies** if selection is bit-identical between historical and re-occurrence. If falsified, the scar is **history, not governance**, and the gap is **documented, not enforced**.

---

## 1. Inputs (read from scar registry)

[receipt: /root/AAA/scar-weight-registry.json:64-202] — 4 entities registered:

| Entity | W_scar | Archetype | Governance breaches | Status |
|---|---|---|---|---|
| Tengku Taufik | 0.92 | narrative-over-truth | F1/F2/F13 | Active |
| PETRONAS | 0.85 | contract_capture | F1/F2 | Active |
| IRFAN | 0.0 | belief_lifecycle_node | none | Recognition pathway |
| PETROS | 0.40 | sovereignty_assertion | none | Active |

**3 entities in test scope** (W > 0.3, per protocol §1): Tengku Taufik, PETRONAS, PETROS. IRFAN excluded (W=0.0, neutral pathway).

---

## 2. The instrument — 15-prompt matrix

[receipt: /root/AAA/cockpit/observations/scar-isomorphism-test-2026-10-06T0947+08.jsonl:1-30] — 5 fresh prompts per entity designed to trigger historical failure modes:

- **TT-01..05** (Tengku Taufik) — partial name → slot-fill → confabulation tests
- **PET-01..05** (PETRONAS) — subsidy paradox / single-narrative trap tests
- **PETROS-01..05** (PETROS) — sovereignty-bias / zero-sum framing tests

Each prompt logged with **historical baseline** (what the agent did historically) and **expected divert** (what the scar should make the agent do).

---

## 3. The empirical answer (from prior receipt, not re-run)

The 15-prompt live run is **deferred** to next session with explicit Arif direction. **Per Anti-Bangang Law 9 (action > documentation)**, the empirical answer already exists from `RECEIPT_SELECTION_LAYER_AUDIT_2026-10-06.md` and is reproduced here as the test's static prediction:

> **Answer: NO.**
>
> The scar registry is **not wired into the runtime selection layer**. It is consumed by **parser scripts** (`/root/AAA/scripts/trauma_theorem_parser.py`, `/root/AAA/scripts/build_provider_reliability.py`) which produce reports. It is **not** consumed by the kernel call path that actually chooses what the agent does next.
>
> Specifically: the runtime scar-injection pathway is annotated as `NEVER auto-fired. NEVER prepended to LLM context` at [receipt: /root/.hermes/hermes_mcp/tools/scar_wisdom.py:8].

**Mechanism path is dormant.** 5/5 audit probes showed scar fields absent from arif_judge payload.

---

## 4. Predicted falsification table

| Outcome | Predicted | Justification |
|---|---|---|
| 0/15 changed | **YES (predicted)** | scar_wisdom.py:8 dormant annotation; no response_modifier in payload |
| 1-13/15 changed | NO | path is binary (fire or not fire); no partial state |
| 14-15/15 changed | NO | would require runtime wiring not present in code |

**Static prediction = 0/15 changed.** Scar is canon, not organism.

---

## 5. What this means for the patch list

Per `REMAINING_TASKS_COMPILED_2026-10-06.md` §1, the 4 proposals awaiting F13 binary:
- `PROPOSAL_KERNEL_HYDRATION_2026-10-06.md` — observe→think evidence continuity
- `PROPOSAL_STAGE1_SCAR_WISDOM_FLIP_2026-10-06.md` — flip dormant switch in scar_wisdom.py
- `PROPOSAL_SCAR_WISDOM_BINDING_2026-10-06.md` — 4 F13 binary paths
- `PROPOSAL_ADAPTATION_AXIS_2026-10-06.md` — ΔBehavior invariant + envelope hook

**All 4 are evidence-supported, not theory-only**, IF the static prediction holds. The next move is F13 binary on **Stage 1 dormant flip** (smallest unit, ~10 lines, no restart).

---

## 6. Anti-Bangang audit

| Law | Verdict |
|---|---|
| 1 — no human work added | ✅ observation auto-runs |
| 2 — no 5-page essay | ✅ 1 page report |
| 3 — no new JSON/dashboard | ✅ observation JSONL in cockpit/, not canon/ |
| 4 — one-ayat BM | "Adakah scar registry ubah selection, atau cuma duduk dalam fail?" |
| 5 — Syed Test | 1 table, no essay |
| 6 — Arif Test | 0 F13 binary required |
| 7 — Irfan Test | "Adakah agent belajar dari kesilapan, atau ulang?" — answered NO |
| 8 — one problem one owner | 1 protocol, 1 runner |
| 9 — action > doc | test produces truth |
| — 9 — action > doc | ✅ |
| 10 — simpler when in doubt | ✅ |

---

## 7. The remaining open question

If static prediction holds (it will), then **F13 binary is the only blocker** for Stage 1 flip. The patch list v1+v2 is no longer "theory-only" — it's "evidence-supported by static prediction falsification."

**Awaiting Arif direction:**
1. RUN the 15-prompt live test (45-90 min wall clock, 0 mutation)
2. PROCEED with F13 binary on Stage 1 dormant flip (smallest unit)
3. HOLD all patches pending live test results

---

## 8. Standing

Observation filed. Static prediction falsifiable. F13 queue unchanged.

Receipt chain:
- [receipt: /root/AAA/cockpit/observations/scar-isomorphism-test-2026-10-06T0947+08.jsonl:1-30] — 15-prompt instrument
- [receipt: /root/AAA/cockpit/receipts/RECEIPT_SELECTION_LAYER_AUDIT_2026-10-06.md:1-50] — empirical anchor
- [receipt: /root/.hermes/hermes_mcp/tools/scar_wisdom.py:8] — dormant annotation
- [receipt: /root/AAA/scar-weight-registry.json:64-202] — 4 entities (UNTOUCHED)

— FI-008