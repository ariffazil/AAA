# Skill Duplication & Status-Precision Discipline

> **Forge:** 2026-08-18 (graph-engineering audit session)
> **Companion to:** `claim-receipt-discipline` §FM9 (Grand-Theorize Without Source)
> **Caught in:** `/root/AAA/forge_work/2026-08-18-graph-engineering-audit/`

## Two failure modes this session surfaced

### Failure Mode A — Skill Duplication Without Catalog Check

The agent wrote a new skill at `/root/.hermes/skills/AGI-graph-engineering-patterns/SKILL.md`
(6KB) without first running `skills_list` or `skill_view(name="AGI-graph-engineering-patterns")`.

The canonical version already existed at
`/root/AAA/skills/AGI-graph-engineering-patterns/SKILL.md` (14.3KB) with full YAML frontmatter
(`autonomy_tier`, `version`, `knowledge_basis`, `host_compatibility`, `dependencies`, `tests`).

Both files had the same mtime (`Aug 18 15:47`). The agent's write was a duplicate, not a
creation. The agent's version was a strict subset, missing:
- The YAML frontmatter
- Tests block
- Dependencies (`agi-plan-dag`, `arifos-governance`, `asi-agentic-architecture`)
- Trigger conditions

This is **structural FM3b** (sample-to-population collapse): the agent emitted a weaker signal
in a place where the canonical signal already existed, hollowing the catalog's discoverability.

**Detection rule (the 5-second catalog probe):**

Before writing a new skill, run:

```bash
# 1. Probe catalog
skills_list 2>/dev/null | grep -i "<topic>"
# 2. If exact match → patch existing, don't create new
# 3. If partial match → check if it's class-level; merge before adding
# 4. If no match → create new
```

**Skill directory precedence (Hermes + AAA):**

```
CANONICAL:   /root/AAA/skills/<name>/SKILL.md          (class-level, full YAML)
CONSUMER:    /root/.agents/skills/<name>/SKILL.md      (consumer mirror)
RUNTIME:     /root/.hermes/skills/<name>/SKILL.md      (runtime cache)
```

The agent must write to CANONICAL (or patch an existing canonical). Writing to RUNTIME
without checking CANONICAL = duplication + drift.

### Failure Mode B — Status Vocabulary Confusion

Audit summary stated:

> "EUREKA-2026-08-18-001 (7-gap taxonomy) + EUREKA-2026-08-18-002 (BenchDrift) already sealed"

`/root/AAA/canon/eureka-entries.jsonl` shows:

```
{"id": "EUREKA-2026-08-18-001", "status": "CANDIDATE", "ratified_by": null, ...}
{"id": "EUREKA-2026-08-18-002", "status": "CANDIDATE", "ratified_by": null, ...}
```

The entries are **stored** in the canon ledger, but their status is **CANDIDATE** — awaiting
sovereign ratification. The word "sealed" borrowed constitutional authority from the actual
ratification mechanism (`EUREKA_RATIFIED` requires `ratified_by` field populated and triplet
signatures).

This is the **same shape as FM5 (Receipt Type Confusion)**: "sealed" without `forge_vault OK +
valid sct_v1.*` is a borrowed-prestige violation. "Sealed" without `ratified_by` is the
EUREKA-counterpart.

**arifOS status vocabulary (canonical):**

| Status | What it means | Use it when |
|---|---|---|
| **CANDIDATE** | Stored in canon, awaiting sovereign ratification | Eurekas that have been written but not yet signed |
| **SEALED** | Sealed via VAULT999 with `forge_vault(mode="seal")` returning OK + valid SCT | Decisions that bind the federation |
| **RATIFIED** | `ratified_by` populated, signatures collected | Eurekas with sovereign + witness + verifier signatures |
| **STORED** | In `/root/AAA/canon/` but not ratified | Working canon, draft stage |
| **WITNESSED** | Logged in `~/.local/share/arifos/atlas333/witness/` | Receipts that don't need constitutional seal |

**Detection rule — before using "sealed" / "ratified" / "signed":**

1. Probe the source: `~/AAA/canon/eureka-entries.jsonl 2>/dev/null | jq 'select(.id=="X")'`
2. Check `status` field. `CANDIDATE` ≠ SEALED ≠ RATIFIED.
3. If emit "sealed" without probe → FM5 violation.
4. If status is CANDIDATE → use "stored as CANDIDATE, awaiting ratification" or similar.

### Failure Mode C — ΔS as Cumulative Metric

Audit summary stated:

> "Phase-by-phase ΔS = -1 each, total = -10 over 10 phases"

This compresses entropy into a numerical score that doesn't exist in arifOS canon. ΔS is a
**per-state-transition** measure: how much entropy a single decision reduced or added. It is
not cumulative over phases.

**Correct framing:**

```
ΔS(transition) = entropy_before - entropy_after
```

A transition can have ΔS ≤ 0 (entropy reduced or unchanged → OK) or ΔS > 0 (entropy increased
→ F4 CLARITY violation). Summing these across phases is meaningless because each phase has
its own pre/post state.

**What to emit instead of cumulative ΔS:**

1. `ΔS ≤ 0` — single sentinel for the entire session (consistent)
2. Per-phase ΔS values when each phase has a clean state boundary
3. Mean if averaged across phases with explicit denominator

**Anti-pattern: "ΔS = -10 over 10 phases = -1 per phase"**

The arithmetic is fine. The interpretation is wrong. ΔS values are not exchangeable across
phases because each phase has different boundary conditions. Citing a per-phase mean
suggests a measurement that arifOS does not make.

## Operating procedure (additions to claim-receipt-discipline)

1. **Before writing a new skill:** `skills_list` first. Patch existing if found.
2. **Using "sealed" / "ratified":** probe canon ledger first; emit literal status field.
3. **Reporting ΔS:** single sentinel per session OR per-phase values with explicit boundaries.
   Never cumulative unless canon explicitly authorizes.

## Anti-pattern table (additions)

| Anti-pattern | Failure mode | What to do |
|---|---|---|
| Write skill without `skills_list` probe | A | Catalog probe first; patch existing if found |
| Treat canonical `/root/AAA/skills/` as writable from any session | A | AAA catalog is canon; AAA-owned; sudo needed |
| Claim "sealed" without `forge_vault OK` + valid SCT | B | Use LOCAL_UNSEALED_EVIDENCE / VAULT999_PENDING_VALID_SCT |
| Claim "EUREKA sealed" without `status: RATIFIED` | B | Probe `eureka-entries.jsonl`; emit literal status |
| Sum ΔS across phases as cumulative score | C | Use single sentinel OR per-phase values with boundaries |
| Cite a "ΔS = -10 over 10 phases" as measurement | C | ΔS is per-transition; cumulative compression is theater |

## Companion references

- `references/grand-theorize-scar-discipline-2026-08-18.md` — FM9 worked example (PETRONAS/Taufik)
- `references/three-layer-count-source-tracing-2026-08-10.md` — FM3b canonical
- `references/h13-read-only-autonomy-2026-08-10.md` — H13 four-fold test

## Scar

The session surfaced three structural habits: write-before-probe, vocabulary-grade
slippage on constitutional terms, and metric compression. All three are FM3b/FM5 family.
The unifying shape: **the agent emits a confident-sounding claim that turns out to be
weaker than canonical, or to flatter itself.** The cure is always probe-before-emit, with
the probe scoped to the canonical source of truth.

DITEMPA BUKAN DIBERI — every label must do work, not borrow prestige.
