---
name: live-vs-blueprint-audit
description: Verify a live codebase against a ZIP/blueprint refactor target. Used when Arif asks "Is [system] still GOLD?" or "compare live vs target." This skill prevents the mistake of treating an aspirational blueprint as if it were the live system.
triggers:
  - "Is [repo] still gold"
  - "compare live vs zip"
  - "red team [repo] vs blueprint"
  - "is the seal still live"
  - "verify [system] vs [blueprint]"
  - "apply the zip"
  - "live vs target architecture"
category: audit
version: 1.0
ratified: 2026.05.04
seal: DITEMPA BUKAN DIBERI
---

# Live vs Blueprint Audit — Methodology

## Purpose

When Arif shares a ZIP or blueprint document claiming a refactor has been applied, verify the **live system** actually matches. The ZIP was aspirational until applied. A GOLD SEAL on a ZIP means the TARGET architecture is audited — not that it's live.

## The Critical Failure Mode

An agent (or human) reads a SEAL_999_VAULT or blueprint document and assumes the live system matches. It doesn't. The ZIP documents a **planned** refactor. Live is the **current** system. These are different.

## Methodology

### Step 1 — Extract and Map the ZIP

```bash
# Extract ZIP to temp
mkdir /tmp/audit_target
unzip /path/to/blueprint.zip -d /tmp/audit_target

# Read SPEC.md first — it defines the TARGET architecture
cat /tmp/audit_target/SPEC.md
cat /tmp/audit_target/plan.md

# Get the file manifest
ls /tmp/audit_target/project/
```

### Step 2 — Probe the LIVE system

```bash
# Verify canonical tools
cd /root/[REPO]
python -c "from contracts.canonical_registry import CANONICAL_PUBLIC_TOOLS; print(len(CANONICAL_PUBLIC_TOOLS))"

# Verify aliases
python -c "from compatibility.legacy_aliases import LEGACY_ALIAS_MAP; print(len(LEGACY_ALIAS_MAP))"

# Check for critical directories/files that should exist if refactor was applied
ls /root/[REPO]/kernel/ 2>/dev/null && echo "kernel/ EXISTS" || echo "kernel/ MISSING"
ls /root/[REPO]/contracts/resources/ 2>/dev/null && echo "resources/ EXISTS" || echo "resources/ MISSING"
ls /root/[REPO]/contracts/prompts/ 2>/dev/null && echo "prompts/ EXISTS" || echo "prompts/ MISSING"

# Verify fail-closed startup
python -c "import os; os.environ['GEOX_SECRET_TOKEN']='test'; from control_plane.fastmcp.server import is_geox; print(is_geox())"
```

### Step 3 — Compare Layer by Layer

Build a comparison table:

| Check | ZIP Target | LIVE System | Status |
|-------|-----------|-------------|--------|
| Canonical tools count | 13 | (verify) | MATCH/GAP |
| kernel/ directory | EXISTS | EXISTS/MISSING | MATCH/GAP |
| governance/ separation | 3 files | 1 monolith | GAP |
| resources/ | 15 URIs | EXISTS/MISSING | MATCH/GAP |
| prompts/ | 6 templates | EXISTS/MISSING | MATCH/GAP |
| Fail-closed startup | is_geox() | implemented? | MATCH/GAP |

### Step 4 — Read the Right Files

Use `wc -l` and `head` to understand what actually exists:

```bash
# Find the actual business logic location
find /root/[REPO] -name "*.py" -not -path "*/__pycache__/*" | xargs wc -l 2>/dev/null | sort -rn | head -20

# Check if governance is a monolith or separated
ls /root/[REPO]/contracts/governance/
wc -l /root/[REPO]/contracts/governance/*.py

# Check if the unified_13.py is a thin wrapper or a monolith
wc -l /root/[REPO]/contracts/tools/unified_13.py
head -20 /root/geox/contracts/tools/unified_13.py
```

### Step 5 — Issue the Verdict

```
🛑 VOID — The GOLD SEAL is NOT live. Blueprint is aspirational.
✅ MATCH — Live matches the target.
⚠️ PARTIAL — Some gaps exist.
```

## Thermodynamic Scoring Framework

Use this to compare live vs ZIP/target and justify the cost of applying a refactor:

```
Score = (Testability × 0.25 + Security × 0.30 + Maintainability × 0.25 + Governance × 0.20)
        × (1 − Production_Entropy) / (1 + Change_Friction)
```

**Measurable dimensions:**
- Testability: % of code testable without framework mocking (try `python -m pytest --cov` after extracting kernel)
- Security: number of CRITICAL unfixed CVEs vs fixed
- Maintainability: max file size, cyclomatic complexity, coupling
- Governance: are F1-F13 checks in separate deployable modules or inline?
- Production entropy: how tightly coupled is business logic to transport?
- Change friction: how many files must you touch to make one change?

**5-year cost of doing nothing:**
- Entropy accumulation rate × 5 years → projected entropy
- Maintenance cost premium (extra debugging hours, security patching)
- Opportunity cost (reduced feature velocity)

**Expected value of refactoring:**
- Refactor cost (engineering hours) + (risk % × production downtime cost)
- vs. 5-year thermodynamic debt of status quo

## What Changed This Session

### Finding: The GEOX ZIP (SEAL_999_VAULT_V2) vs Live GEOX

- **ZIP**: 4-layer sovereign architecture with `kernel/` (11 modules), `governance/` (3 files), `contracts/resources/`, `contracts/prompts/`
- **LIVE**: `kernel/` does NOT exist. Governance is a single 803-line `acp_logic.py`. Resources and prompts directories don't exist.
- **13 canonical tools**: LIVE ✅ matches ZIP exactly
- **85 legacy aliases**: LIVE has 85, ZIP has 54 — live has MORE
- **Fail-closed startup**: ZIP implements `is_geox()`, LIVE does not

### What to Tell Arif

The GOLD SEAL applies to the ZIP's **target state**. The live system is the "old" architecture. Arif has two choices:
- **Apply the ZIP** — execute the full refactor on live
- **Keep separate** — acknowledge ZIP is future target, maintain live as-is

## When to Use This Skill

1. Arif asks "Is [repo] still gold/sealed?"
2. Arif shares a ZIP and asks to compare with live
3. A SEAL document exists but you need to verify it's actually running
4. You're about to claim a refactor was applied but haven't checked

## Key Lesson

> A GOLD SEAL on a ZIP means the TARGET architecture passed all audits. It does NOT mean the TARGET is live. You must verify the live system independently.

The mistake is treating the blueprint as the implementation. Always probe the actual running system with actual Python import commands.
