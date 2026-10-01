# HumanLeverage — Federation North-Star Metric

> **Status:** DRAFT_AWAITING_F13 (2026-10-01 · written by FI-008)
> **Sister:** `/root/AAA/instructions/aforge-citizen-contract.md` · `/root/AAA/scars/2026-10-01-complexity-must-not-exceed-leverage.md`
> **Doctrinal anchor:** This metric **above** all others. Anything not improving this ratio is, by definition, not earning its keep.

---

## The equation

```
HumanLeverage
  = UsefulConsequences
    ÷ HumanAttention
```

`UsefulConsequences` = verified task completions + durable rule improvements + verified scar metabolism.

`HumanAttention` = Arif's decisions-per-task + agentic prompts-per-task + clarifying questions answered.

## Falsifiability

This metric is **falsifiable** in two directions:

- **Increasing** HumanLeverage means the system produces more useful verified outcomes per unit of Arif's attention. **The thesis works.**
- **Decreasing** HumanLeverage means the system is becoming bureaucracy for machines. **The thesis fails.**

## What this metric REPLACES

| Replaced | Why |
|---|---|
| Tool count | Volume ≠ value. We optimize for the thing we measure. |
| MCP server count | Federated tool interoperability ≠ institutional leverage. |
| Organ count | 13 floors, 8 organs, etc. — already at risk of exceeding attention. |
| Scar count | Scars should *prevent* repetition, not be a vanity metric. |
| Memory size | Receipts grow; verified improvement is the test. |
| Agent count | Citizens don't auto-mean leverage. |
| GitHub stars | External marketing ≠ internal value. |

## What this metric ACCEPTS

| Accepted | Why |
|---|---|
| Verified task completion rate | Real outcomes, independently witnessed. |
| Human escalations per task | Should decrease as institution matures. |
| Recovery rate | Self-repair without human rescue. |
| Model swap retention | Does capability survive Claude → Qwen? |
| Scar reuse rate | Do previous failures prevent repetition? |
| Prediction Brier score | Calibration improves decisions. |
| Policy improvement rate | Verified outcomes → changed behavior. |
| Attention compression ratio | `machine_events / human_attention_events` |

## Operational rules

1. **Above the others.** This metric binds organ count, scar count, doc count, etc. — not the reverse.

2. **Three-test for new artifacts.** Any new layer must pass:
   ```
   Δ(UsefulConsequences) > 0
   Δ(HumanAttention)     ≤ 0
   ```
   If both fail, archive via `.distraction-archive-YYYY-MM-DD/` pattern. Do not commit.

3. **Receipts-graded-not-celebrated.** A receipt that increases uncertainty without decreasing decision-attention gets archived, not celebrated. Per scar 2026-10-01-003.

4. **No vanity metrics.** Measuring something changes what's optimized. If we measure organ count, we get more organs. Measuring HumanLeverage focuses on what Arif actually wants.

## Where this metric LIVES

- **Doctrine:** This file (`/root/AAA/instructions/human-leverage-north-star.md`)
- **Binding:** `ROOT_AGENT_CONFIG.yaml::human_leverage_north_star`
- **Audit:** `scripts/human_leverage_audit.py` (TODO — separate mission)
- **Linked scars:** `/root/AAA/scars/2026-10-01-complexity-must-not-exceed-leverage.md` · `/root/AAA/scars/2026-10-01-agent-turn-vs-institution-optimization.md`

## What this metric does NOT measure

- Model intelligence (different question)
- Tool completeness (different question)
- Agent count (different question)
- Code coverage (different question)
- Documentation size (different question)
- Anything not affecting Arif's attention-vs-outcome ratio

## F13-class binaries

- Thresholds for what counts as "verified" in `UsefulConsequences`
- What counts as "human attention" (SCT-captured? wall-clock? decisions?)
- How to discount self-reported outcomes (Brier-style calibration)

## Per the SCAR-2026-10-01-001 self-witness:

> *"Without that scar, every future agent will keep adding layers because layers are easy and proving leverage is hard. We optimize for the thing we measure. If we only measure organ count, we get more organs."*

This file exists because that scar was filed first. Without it, HumanLeverage is just another metric. With it, HumanLeverage is **the metric that gates the others**.

DITEMPA BUKAN DIBERI ⚒️