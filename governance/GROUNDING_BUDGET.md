# Grounding Budget — Gate 0

> **Status:** CANON v1.0
> **Forged:** 2026-08-09 by F13 SOVEREIGN directive
> **Floors:** F2 TRUTH · F7 HUMILITY · F13 SOVEREIGN
> **Position:** Gate 0 — before arif_judge, before any MUTATE

## The Rule

> Before any material action, the system must obtain at least one piece of evidence that did not originate from a model.

This is **Gate 0**. It fires before constitutional judgment. If the grounding budget is empty, the action is **HOLD**. No exceptions.

## What Counts as Grounding

### Valid Sources

| # | Source | Example | Verification |
|---|--------|---------|-------------|
| 1 | **Measurement** | Sensor data, well log, market price, instrument reading | Source instrument + calibration chain |
| 2 | **Authoritative record** | Government filing, court document, notarized statement, registry entry | Issuing authority + timestamp |
| 3 | **Reproducible experiment** | Physics that can be repeated by independent party | Replication protocol + independent result |
| 4 | **Direct human testimony** | Statement from named, accountable source (NOT AI-generated persona) | Identity verification + accountability |
| 5 | **Observed consequence** | Outcome that has already occurred, not one that is predicted | Timestamped receipt + independent witness |

### Invalid (Do NOT Count Toward Grounding Budget)

| Source | Why Invalid |
|--------|------------|
| Model-generated text | Origin is synthetic, regardless of fluency |
| Model-extrapolated data | Interpolation without measurement anchor |
| AI-summarized document | The summary may have introduced error |
| Republication of SYN content | One source, many copies = one source |
| Predicted outcome | Has not yet met reality |

## Budget Tiers

| Action Class | Minimum Grounding | Example |
|-------------|------------------|---------|
| **OBSERVE** | 0 (read-only) | Reading health probes, git log |
| **REASON** | 0 (computation on existing evidence) | Computing NPV from known cash flows |
| **MUTATE (reversible)** | 1 grounding source | Editing a file (backed up), committing code |
| **MUTATE (irreversible)** | 2 grounding sources, independent lineages | Deploy to production, database migration |
| **SEAL** | 3 grounding sources, tri-witness channels | Constitutional seal to VAULT999 |

## Verification Protocol

When an agent claims grounding:

1. **Source check:** Is this a real measurement/record/testimony, or model output?
2. **Lineage check:** If the source traces back to AI output → RECYCLED_SYN → INVALID
3. **Independence check:** If multiple sources share a common AI ancestor → count as ONE
4. **Freshness check:** Is the grounding still valid, or has reality changed?

## Integration with Existing Floors

| Floor | How Grounding Budget Interacts |
|-------|-------------------------------|
| **F2 TRUTH** | SYN/RECYCLED_SYN labels identify model-origin claims that cannot serve as grounding |
| **F3 TRI-WITNESS** | The three witnesses (Human × AI × Earth) must have independent grounding lineages |
| **F7 HUMILITY** | Ω₀ uncertainty floor ensures the system never treats grounding as 100% certain |
| **F13 SOVEREIGN** | Arif can override grounding requirements — but the override itself becomes grounding (human testimony) |

## Anti-Patterns

- ❌ Treating 3 copies of the same AI output as 3 grounding sources
- ❌ Using a model's internal confidence as grounding
- ❌ Counting predicted outcomes as "observed consequences"
- ❌ Skipping grounding budget for "obvious" actions — obvious is a model judgment

## F13 Override

The sovereign may authorize actions with insufficient grounding budget. When this happens:
1. The override is recorded as grounding source type 4 (direct human testimony)
2. The action proceeds with the sovereign's authority
3. The grounding deficit is documented for post-hoc review

## Etymology

"Grounding budget" borrows from capital budgeting: you have a limited supply of trust, and every action must spend at least one unit of reality-grounded evidence before it can proceed. You cannot borrow grounding from the future. You cannot substitute model confidence for evidence. You must pay the grounding cost before you act.

---

*DITEMPA BUKAN DIBERI — Grounding is forged through contact with reality, not given by text.*
