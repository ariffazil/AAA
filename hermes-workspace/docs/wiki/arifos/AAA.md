# AAA — Architect · Auditor · Agent

> **CLAIM** | Source: `docs/floor_wiring_map.md` + workspace memory | **Confidence:** 0.93 | **Epoch:** 2026-04-23

## Summary

arifOS uses a three-role pattern (AAA) for all governed AI execution:
- **Architect** — proposes, designs, plans
- **Auditor** — verifies, checks constraints, flags issues
- **Agent** — executes, produces output, respects verdict

This is not advisory — it's the constitutional enforcement layer that prevents any single role from self-approving.

---

## Roles in Detail

### Architect
- Proposes changes and plans
- Does NOT execute
- Output is always CLAIM_ONLY until ratified

### Auditor
- Verifies against floor constraints (F1–F13)
- Checks Nine-Signal metrics (delta, psi, omega, kappa_r)
- Issues HOLD/VOID/SEAL verdicts
- **888_JUDGE** is the auditor's SEAL authority

### Agent
- Executes within ratified verdict
- Does NOT self-approve
- Must surface uncertainty explicitly

---

## Constitutional Invariant

> **No role may ratify its own output.**
> The Architect cannot audit its own plans.
> The Agent cannot issue its own verdicts.
> The Auditor is the only entity that can issue SEAL.

---

## Three-Witness Consensus (F3)

For a SEAL verdict to issue, three witnesses must agree:
1. **Human** — Arif (or authorized human sovereign)
2. **AI** — arifOS agent (via 888_JUDGE)
3. **Earth** — GEOX (via spatial/physical verification)

If any witness withholds → verdict is HOLD or VOID.

---

## Cross-References

- [[arifos/FLOORS]] — F3 is the Tri-Witness floor
- [[arifos/888_JUDGE]] — auditor's SEAL authority
- [[nine-signal/OVERVIEW]] — auditor's metric checks

---

## Status

**Stable** — AAA pattern is canonical in arifOS architecture.

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE