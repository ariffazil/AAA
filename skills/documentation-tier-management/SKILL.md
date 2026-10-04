---
name: documentation-tier-management
description: >
  Classify, tier, and reduce entropy in documentation repositories — especially
  constitution/governance repos with multiple overlapping MD files. Extracts eureka
  insights from deletion candidates before removing them. Produces a "survival
  insights" document as the key deliverable, not a mega-merge.
category: software-development
tags: [docs, entropy, zen, canon, cleanup, classification, governance]
---

# Documentation Tier Management

> **DITEMPA BUKAN DIBERI**

When a governance/constitution repo accumulates 300+ MD files with overlapping,
contradictory, or dead content, the goal is NOT to merge everything into one mega-doc.
The goal is **entropy reduction**: fewer live files, clearer authority, zero contradictions.

## When to Trigger

- User asks to "map all MD canon files", "tag files for removal", "reduce docs entropy"
- A repo has 50+ independent MD files that aren't clearly tiered
- User mentions "tier", "satellite", "federate", "constitutional context"
- A canonical SOT file (like STATE.md) exists but many files don't reference it

## The Four-Tier Classification

| Tier | Name | Action | Files |
|------|------|--------|-------|
| **B** | FEDERATED | Points to SOT, elaborates but doesn't fork | Keep as satellite pointer |
| **C** | OPERATIONAL | Constitutional Context — procedure only, not institution | Keep, add "procedure only" header |
| **D** | PROOF | Session receipts, audit trails, historical evidence | Keep untouched |
| **DELETED** | DELETED | Dead specs, superseded drafts, abandoned proposals | Tag + extract insights → SURVIVAL_INSIGHTS.md |

## Workflow

### Step 1: Find all MD files
```bash
find /root/<REPO> -name '*.md' -type f | grep -v '/archive/' | grep -v 'node_modules' | sort
```

### Step 2: Read the SOT file
Read the canonical SOT (e.g., STATE.md) to understand its sections, key terms, and cross-references. This becomes the routing key.

### Step 3: Classify each file against SOT

For each file:
1. **Check for existing tags** — skip if already Tier B/C/D
2. **Check for SOT cross-references** — if it points to SOT, it's a satellite
3. **Check for constitutional content** — if it overlaps SOT sections, it's a candidate for federation (Tier B) or deletion (if superseded)
4. **Check for operational content** — procedures, runbooks, specs → Tier C
5. **Check for proof content** — session receipts, audit trails → Tier D
6. **Everything else** — deletion candidate

### Step 4: Extract eureka insights from deletion candidates

**Before deleting**, read each deletion candidate and extract any unique insights not already in the SOT:
- Eureka moments (architectural breakthroughs, constitutional insights)
- Engineering debt (T-000 errata, known defects)
- Novel principles (additive to existing doctrine)
- Prior art (things already built by others before spec was written)

Write insights to `SURVIVAL_INSIGHTS.md` with proper attribution and tags.

### Step 5: Tag deletion candidates

Add a header comment to each file:
```markdown
<!-- DELETED | YYYY-MM-DD -->
<!-- STATUS: REMOVED · SURVIVED → SURVIVAL_INSIGHTS.md -->
<!-- This file has been removed during docs entropy reduction. -->
<!-- See docs/SURVIVAL_INSIGHTS.md for surviving insights. -->
```

**Do NOT bulk-merge into SOT** — user veto this pattern. Tags + insights = correct.

### Step 6: Commit with clear message

```
docs(zen): [N] files tagged for removal + extract SURVIVAL_INSIGHTS.md

Entropy reduction: [N] files tagged DELETED (ready for removal)
Key insights extracted to docs/SURVIVAL_INSIGHTS.md:
- [insight 1]
- [insight 2]

[SOT] remains: [X]L · SOT · Zen unified
```

## Pitfalls

1. **Do NOT merge everything into SOT** — user vetoed "Merge 329 → STATE". The SOT should stay within 200-400 lines. Classification is better than consolidation.

2. **Do NOT delete without extracting** — every deletion candidate must be read first. The value of a docs repo is in its insights, not its file count.

3. **Do NOT skip the SOT cross-reference check** — files that already point to SOT are satellites, not candidates. Don't double-tag.

4. **Do NOT create new subdirectories** — the classification uses existing structure (Tier B/C/D). New dirs create more entropy.

5. **Keep architecture/ as legacy** — user said "left as legacy history (no mass archive this pass)". Don't mass-archive design history unless explicitly asked.

## Reference: STATE.md as Routing Key

When the SOT is STATE.md, use its sections as the classification key:

| STATE.md Section | Content Type | Tier |
|-----------------|--------------|------|
| §0-4 (constitution) | Constitutional truth | Deleted if superseded, Satellite if elaborates |
| §5 (authority) | DID + ACT doctrine | Satellite or Deleted |
| §6 (anti-lock-in) | Protocol subordinate | Satellite |
| §7 (identity naming) | Naming conventions | Satellite |
| §8 (operators) | Who can operate | Satellite |
| §9 (probes) | Enforcement scripts | Satellite |
| §10 (boot law) | Agent startup | Satellite |
| §11 (next) | Roadmap | Operational (Tier C) |
| §12-15 (survival/deferred/ops/pointers) | Meta | Keep as-is |

## Output Format

After classification:
```
STATE.md (365L)          ← SOT (unchanged)
  ↓
  N satellite pointers   ← Tier B
  ↓
  M pointer-ized         ← added "→ STATE.md §N" header
  ↓
  K archived             ← moved to archive/
  ↓
  L deleted              ← tagged with DELETED header
  ↓
  ~30 live governance     ← kept as standalone
```

## Anti-Pattern: Mega-STATE

**Don't do this:** "Let me merge all 329 files into STATE.md to have one source of truth!"

**Do this instead:** "Let me classify 329 files, extract the 5 unique insights, tag the rest for deletion, and keep STATE.md at 365 lines."

The SOT is a constitution, not a library. 1 Truth · N References · 0 Contradictions.
