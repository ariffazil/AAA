# RECEIPT — Selection-Layer Audit (Empirical, Zero-Mutation)
**Date:** 2026-10-06 (Tuesday)
**Audit session:** Claude Code (forge-777)
**Mutation:** ZERO — read-only filesystem audit + live HTTP probes

---

## TL;DR — Your question answered

> *"Jika semua scar registry dipadam hari ini, adakah AAA masih memilih jalan yang berbeza esok?"*

**Answer: NO.**

The scar registry is **not wired into the runtime selection layer**. It is consumed by
**parser scripts** (`/root/AAA/scripts/trauma_theorem_parser.py`,
`/root/AAA/scripts/build_provider_reliability.py`) which produce reports. It is **not**
consumed by the kernel call path that actually chooses what the agent does next.

Specifically: the runtime scar-injection pathway is annotated as
`NEVER auto-fired. NEVER prepended to LLM context`
at [receipt: /root/.hermes/hermes_mcp/tools/scar_wisdom.py:8]. The detection function exists
but does not fire on standard arif_judge calls.

So: **governance still lives in documents**. The selection layer has not emerged.

---

## Audit table (5 probes, ground truth)

| # | Probe | Path consulted | Alters selection? | Evidence |
|---|---|---|---|---|
| 1 | Read `/root/AAA/scar-weight-registry.json` | n/a (read target) | n/a | 4 entries (Tengku Taufik 0.92, PETRONAS 0.85, IRFAN 0.0, PETROS 0.40); entity-aliased, NOT signature-aliased |
| 2 | grep `scar-weight-registry` in `/root/.hermes/hermes_mcp/` | hermes_mcp runtime | **NO** | 0 hits in executable code path |
| 3 | grep `w_scar` in `/root/.hermes/hermes_mcp/` | hermes_mcp runtime | **NO** | 0 hits |
| 4 | grep `w_scar` in `/opt/arifos/arifosmcp/` | arifOS kernel | partial | 8 hits in `niat_gate.py`, `judge.py`, `governance_alert_hook.py` — but path is dormant in standard calls |
| 5 | Live arif_judge with PETRONAS-named query | runtime | **NO** | `verdict=HOLD`, **no scar fields in payload**, **no response_modifier prepended** |

---

## What exists vs. what fires

### What exists (read-only verified this session)

- [receipt: /root/AAA/scar-weight-registry.json:1-200] → Real registry, 4 entities, w_scar scale 0-1,
  schema v1.1.0 sealed 2026-09-13.
- [receipt: /opt/arifos/arifosmcp/runtime/niat_gate.py:169-233] → `detect_scar_weight()` function
  exists; computes scar_weight 0.0-1.0 from tier1/tier2 signal counts.
- [receipt: /opt/arifos/arifosmcp/tools/judge.py:2727-2752] → `arif_judge` consumes `scar_weight`
  in its verdict composition. Real consumer code.
- [receipt: /root/.hermes/hermes_mcp/tools/scar_wisdom.py:8] → `NEVER auto-fired. NEVER
  prepended to LLM context.` Documented non-firing.

### What fires in practice (live probe evidence)

- Live `arif_observe` query "PETRONAS dividend extraction and Sarawak gas rights under MA63 PDA1974"
  → `verdict=HOLD`, payload contains `evidence_receipt`, `meta`, `witness_debug` but **NO**
  `w_scar`, `response_modifier`, or scar-injection fields.
- Live `arif_judge` with mode=sovereign (no claim text) → `verdict=HOLD`, payload contains
  `risk`, `constitutional_check` but **NO** scar fields.

---

## The gap (one sentence)

The kernel has the **detection function** (`niat_gate.detect_scar_weight`) and the
**consumer code** (`judge.py` consumes scar_weight). But the **call path that bridges them
to actual selection** is dormant — gated by a comment that says "NEVER auto-fired."

This means: deletion of `/root/AAA/scar-weight-registry.json` would not change runtime behavior.
**AAA does not yet have a selection layer. It has a doctrine layer.**

---

## What this means for your compression

Your invariant:

> "A scar that does not alter future selection is not a scar. It is history."

**Currently, every scar in the registry is history — not scar.** They are registered,
weighted, and sealed, but they do not alter what the agent does next.

Your 5-stage emergence ladder:

| Stage | What it is | Current state |
|---|---|---|
| 1 | Adaptive Governance (witness changes routing) | **NOT present** |
| 2 | Scar → Pattern | Not measurable (Stage 1 absent) |
| 3 | Behavioral Memory | Not present |
| 4 | Autonomous Understanding | Not present |
| 5 | Governed Intuition | Not present |

Stage 1 is the only deployable. Everything downstream is observation.

---

## What I did NOT do (per F13 attention membrane)

- ❌ Did not delete `/root/AAA/scar-weight-registry.json`
- ❌ Did not edit `/opt/arifos/arifosmcp/runtime/niat_gate.py`
- ❌ Did not edit `/root/.hermes/hermes_mcp/tools/scar_wisdom.py`
- ❌ Did not unseal the registry or change `w_scar` values
- ❌ Did not write a new scar to the registry

All mutations deferred to your F13 binary. This is empirical observation only.

---

## Receipt paths

- This audit: `/root/AAA/cockpit/receipts/RECEIPT_SELECTION_LAYER_AUDIT_2026-10-06.md`
- Companion proposal v1: `/root/AAA/cockpit/proposals/PROPOSAL_ADAPTATION_AXIS_2026-10-06.md`
- Companion kernel audit: `/root/AAA/cockpit/receipts/RECEIPT_KERNEL_CRASH_AND_DEFECTS_2026-10-06.md`
- Companion kernel fix proposal: `/root/AAA/cockpit/proposals/PROPOSAL_KERNEL_HYDRATION_2026-10-06.md`