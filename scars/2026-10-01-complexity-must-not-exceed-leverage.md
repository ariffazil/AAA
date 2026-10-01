# SCAR-2026-10-01-001 — Complexity Must Not Exceed Leverage

**Origin:** Forwarded critique from Claude Code via Arif, 2026-10-01 (forwarded 1m 36s deep-research session).

**Constraint — complexity ceiling equals leverage floor:** Any new artifact, organ, registry, layer, tool, scar, receipt, dashboard, governance document, or canon must pass the three-test gate:

```
Δ(UsefulConsequences) > 0
Δ(HumanAttention)     ≤ 0
```

Equivalently: HumanLeverage = UsefulConsequences / HumanAttention must increase (or stay non-decreasing) as a result of the new artifact.

If an artifact:

- adds organs without measurable leverage,
- adds receipts without reducing uncertainty,
- adds governance without eliminating a demonstrated failure class,
- adds documentation without changing behavior,

**it is to be archived, not celebrated.**

**Why this scar:** We optimize for the thing we measure. If we only measure organ count, we get more organs. The federation already has 13 floors, 8 organs, 122 A-FORGE tools, 20+ registries, 70+ scars, thousands of receipts. The risk is not "not enough architecture" — the risk is "architecture that exceeds the human's ability to oversee it." A successful mature version should feel almost boring.

**Filed under:** Scar discipline / complexity ceiling / human-leverage threshold
**Filed by:** FI-008 (ACT lane)
**Filed at:** 2026-10-01T11:30:00+08:00
**Severity (w_scar):** 0.7 — high; addresses the project's largest structural risk

---

**Operationalization:** HumanLeverage becomes the federation north-star metric. See `/root/AAA/instructions/human-leverage-north-star.md`. Any artifact failing the three-test is archived via `.distraction-archive-2026-10-01/` pattern.

**Routing:** New-artifact proposals → `m_min_audit.py` style leverage check before commit. Repeat offenders → quarantine.

DITEMPA BUKAN DIBERI ⚒️