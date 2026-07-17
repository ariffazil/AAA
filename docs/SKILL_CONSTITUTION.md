# AAA Skill Constitution v1.0

## The Constitutional Requirements for Every Skill in the arifOS Federation

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Status:** CANONICAL | **Authority:** F13 SOVEREIGN — Muhammad Arif bin Fazil
> **Date:** 2026-07-11 | **Supersedes:** All prior implicit skill conventions
> **Purpose:** Defines what every AAA skill MUST, SHOULD, and MAY declare.
> **Enforced by:** `skill-constitutional-audit` (meta-linter)
> **Companion:** `ROSETTA_STONE.md` (cross-CLI vocabulary), `ORGAN.md` (organ map)

---

## 0. Preamble — Why This Exists

Every skill in the AAA federation is a **constitutional citizen** — an entity with
identity, obligations, dependencies, and memory. This document is the constitution
that governs those citizens.

Without this constitution:
- Skills don't know what floors they touch (identity blindness)
- Skills don't prove what they leave behind (consequence blindness)
- Skills don't declare what they need (federation blindness)
- Skills can't be linted, audited, or sealed against a standard

With it:
- Every skill is self-describing
- Every skill is auditable
- Every skill is lintable
- Every skill is comparable to every other skill

**This is not a style guide. This is law.**

---

## 1. What a Skill IS

An AAA skill is a **constitutional protocol** — a governed artifact that:

1. **Declares its own identity** — what it is, who owns it, what risk it carries
2. **Declares its floor obligations** — which of the 13 constitutional floors it touches
3. **Declares its consequences** — what receipts it emits, what it seals
4. **Declares its dependencies** — what MCP servers and other skills it needs
5. **Declares its autonomy** — what tier of action it can take without asking

An AAA skill is NOT:
- A prompt template (that's Claude Code)
- A function (that's code)
- A suggestion (that's vibes)

**An AAA skill is law. The agent must obey it.**

---

## 2. Mandatory Frontmatter — The Identity Contract

Every `SKILL.md` MUST have YAML frontmatter with these fields:

### 2.1 MUST Have (Identity — Blindspot #1)

These fields answer the question: **"What am I?"**

```yaml
---
id: skill-name-kebab-case          # Unique identifier
name: skill-name-kebab-case        # Same as id
version: 1.0.0-YYYY.MM.DD         # Semver + forge date
description: One-line description  # What this skill does
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)  # Who owns this
risk_tier: high | medium | low     # What happens if this fails
floor_scope: [F1, F2, F4, F7]     # Which constitutional floors apply
autonomy_tier: T1 | T2 | T3       # How much authority this skill has
---
```

**Validation rules:**
- `id` MUST match directory name
- `version` MUST be date-stamped (`vYYYY.MM.DD` format per CLAUDE.md §9)
- `risk_tier` MUST be one of: `high`, `medium`, `low`
- `floor_scope` MUST be a non-empty array of valid floors (`F1`–`F13`)
- `autonomy_tier` MUST be one of: `T1` (AUTO-DO), `T2` (ANNOUNCE+PROCEED), `T3` (ASK/888_HOLD)

### 2.2 SHOULD Have (Consequences — Blindspot #2)

These fields answer the question: **"What do I leave behind?"**

```yaml
trigger_phrases:                    # What the user says to invoke this
  - "phrase one"
  - "phrase two"
dependencies:                       # What this skill needs
  mcp_servers:                      # MCP servers required
    - arifos
    - geox
  skills:                           # Other skills required
    - claim-verification-gate
    - claim-receipt-v1
inputs:                             # What this skill consumes
  - input_name
outputs:                            # What this skill produces
  - output_name
version_lock:                       # Integrity verification
  schema_version: "1"
  artifact_hash: pending
```

**Validation rules:**
- `trigger_phrases` SHOULD have at least 1 entry
- `dependencies.mcp_servers` SHOULD list every MCP server whose tools appear in the skill body
- `dependencies.skills` SHOULD list every skill referenced in the body
- `inputs` SHOULD list every named input the skill consumes
- `outputs` SHOULD list every named output the skill produces

### 2.3 MAY Have (Enrichment)

```yaml
evidence_layer: L1 | L2 | L3 | L4  # Evidence classification
status: ACTIVE | DRAFT | ARCHIVED   # Lifecycle state
geox_complement: /path/to/source    # Domain-specific source mapping
floor_classification: HARD | SOFT | DERIVED  # Per-floor type notes
```

---

## 3. Floor Scope — The Constitutional Map

Every skill MUST declare which floors it touches. This is not optional.
A skill without `floor_scope` is **constitutionally blind** — it doesn't know
what it's touching, and neither does the agent loading it.

### 3.1 Floor Reference

| Floor | Name | Type | Skill Obligation |
|-------|------|------|------------------|
| **F1** | AMANAH | HARD | Reversible-first. If this skill causes irreversible action, it MUST declare T3 autonomy. |
| **F2** | TRUTH | HARD | Every claim MUST carry evidence. No orphan assertions. |
| **F3** | TRI-WITNESS | DERIVED | High-stakes claims need multi-source validation. |
| **F4** | CLARITY | HARD | Every output MUST reduce entropy (ΔS ≤ 0). |
| **F5** | PEACE² | SOFT | Non-destructive. Blocks harm/harass/extort. |
| **F6** | EMPATHY | SOFT | Protect weakest stakeholder. |
| **F7** | HUMILITY | HARD | No fake certainty. Declare uncertainty. |
| **F8** | GENIUS | DERIVED | High-quality output required (G ≥ 0.80). |
| **F9** | ANTIHANTU | HARD | No consciousness/sentience claims. C_dark < 0.30. |
| **F10** | ONTOLOGY | HARD | AI-only ontology. No soul/feelings. |
| **F11** | AUDITABILITY | HARD | Every decision logged, inspectable, attributable. |
| **F12** | RESILIENCE | HARD | Injection defense. Risk < 0.85. |
| **F13** | SOVEREIGN | HARD | Human veto final. Strongest floor. |

### 3.2 Floor Assignment Rules

1. **Every skill MUST have at least 1 floor.** No floorless skills.
2. **Skills that produce claims MUST include F2.** Truth is non-negotiable.
3. **Skills that touch MCP servers MUST include F11.** Auditability is mandatory.
4. **Skills with T3 autonomy MUST include F1 and F13.** Irreversible actions need AMANAH + SOVEREIGN.
5. **Skills that declare consciousness/sentience MUST include F9 and F10.** (And should probably not exist.)
6. **Domain skills (GEOX, WEALTH, WELL) SHOULD include F7.** Humility in domain claims.

### 3.3 Risk Tier ↔ Floor Mapping

| Risk Tier | Minimum Floors | Rationale |
|-----------|---------------|-----------|
| **low** | ≥2 floors | Even low-risk skills must declare identity |
| **medium** | ≥4 floors | Medium-risk skills touch more constitutional surface |
| **high** | ≥6 floors | High-risk skills must be constitutionally comprehensive |

---

## 4. Consequence Declarations — The Receipt Doctrine

Every skill that produces **action-driving claims** MUST declare its consequence
chain: what receipts it emits, what it seals, what it witnesses.

### 4.1 The Consequence Chain

```
Skill produces claim
        │
        ▼
claim-verification-gate    → "Did you check?"
        │
        ▼
claim-receipt-v1           → "Here's the evidence."
        │
        ▼
truth-receipt-enforcer     → "Every action-driving claim needs a receipt."
        │
        ▼
999-vault-seal-immutable   → "Seal to civilization memory."
```

### 4.2 Consequence Rules

1. **Skills that produce claims MUST reference `claim-receipt-v1` or `truth-receipt-enforcer`** in their `dependencies.skills`.
2. **Skills with `risk_tier: high` MUST declare what receipts they emit** in their `outputs`.
3. **Skills with `autonomy_tier: T3` MUST reference `999-vault-seal-immutable`** in their `dependencies.skills`.
4. **Skills that produce irreversible actions MUST declare sealing requirements.**

### 4.3 Consequence Declarations in Body

Every high-risk skill SHOULD include a section like:

```markdown
## Consequences

| Output | Receipt Required | Sealing Required |
|--------|-----------------|------------------|
| claim_x | claim-receipt-v1 | YES — VAULT999 |
| recommendation_y | truth-receipt-enforcer | NO — advisory only |
```

---

## 5. Federation Declarations — The Dependency Contract

Every skill MUST declare what it needs to function. A skill without dependency
declarations is **federation-blind** — it assumes tools exist without verifying.

### 5.1 MCP Server Dependencies

Every skill whose body references `mcp__<server>__*` tools MUST declare that
server in `dependencies.mcp_servers`.

**Validation rule:** If the skill body contains `mcp__geox__*` references but
`dependencies.mcp_servers` does not list `geox`, the skill is **VOID**.

### 5.2 Skill Dependencies

Every skill that references another skill by name MUST declare it in
`dependencies.skills`.

**Validation rule:** If the skill body mentions `claim-verification-gate` but
`dependencies.skills` does not list it, the skill is **HOLD**.

### 5.3 Input/Output Contracts

Every skill SHOULD declare:
- `inputs` — what data/context the skill consumes
- `outputs` — what data/artifacts the skill produces

This enables:
- Dependency graph construction
- Pipeline validation
- Output-to-input matching across skills

---

## 6. Autonomy Tiers — The Authority Contract

Every skill MUST declare its autonomy tier. This determines how much authority
the skill has to act without human confirmation.

### 6.1 Tier Definitions

| Tier | Name | Authority | Human Required |
|------|------|-----------|----------------|
| **T1** | AUTO-DO | Read, grep, edit, test, commit, lint, format | No |
| **T2** | ANNOUNCE+PROCEED | Service restart, schema migration, new dep | 10s window |
| **T3** | ASK/888_HOLD | rm -rf, DROP TABLE, git push --force, deploy | YES — F13 veto |

### 6.2 Tier Rules

1. **Skills with `risk_tier: low` SHOULD be T1.** Low risk = low friction.
2. **Skills with `risk_tier: high` SHOULD be T2 or T3.** High risk = more governance.
3. **Skills that cause irreversible damage MUST be T3.** No exceptions.
4. **Skills with T3 MUST include F1 and F13 in floor_scope.** AMANAH + SOVEREIGN.

---

## 7. Compliance Levels

This document uses RFC 2119 keywords:

| Keyword | Meaning | Enforcement |
|---------|---------|-------------|
| **MUST** | Absolute requirement | VOID if violated |
| **SHOULD** | Recommended, requires justification to skip | HOLD if violated |
| **MAY** | Optional, informational | No enforcement |

### 7.1 Compliance Summary

| Requirement | Level | Enforcement |
|-------------|-------|-------------|
| `id` field | MUST | VOID |
| `name` field | MUST | VOID |
| `version` field | MUST | VOID |
| `description` field | MUST | VOID |
| `owner` field | MUST | VOID |
| `risk_tier` field | MUST | VOID |
| `floor_scope` field | MUST | VOID |
| `autonomy_tier` field | MUST | VOID |
| `trigger_phrases` | SHOULD | HOLD |
| `dependencies.mcp_servers` | SHOULD | HOLD |
| `dependencies.skills` | SHOULD | HOLD |
| `inputs` | SHOULD | HOLD |
| `outputs` | SHOULD | HOLD |
| `version_lock` | SHOULD | HOLD |
| Receipt declarations (high-risk) | MUST | VOID |
| Sealing declarations (T3) | MUST | VOID |
| Consequence section (high-risk) | SHOULD | HOLD |

---

## 8. Linter Integration

This constitution is enforced by three linter skills:

### 8.1 `skill-identity-linter`

Scans all `SKILL.md` files for mandatory identity fields.

```
Trigger: "lint skills", "audit skill identity"
Action:  Scan floor_scope, risk_tier, autonomy_tier, owner
Flags:   Missing floor_scope → HOLD
         Missing risk_tier → HOLD
         floor_scope doesn't match MCP tools used → VOID
Output:  Identity compliance report
```

### 8.2 `skill-consequence-linter`

Scans high-risk skills for receipt and sealing declarations.

```
Trigger: "lint consequences", "audit skill receipts"
Action:  Scan risk_tier=high skills for receipt references
Flags:   No receipt reference → HOLD
         Produces claims but no claim-verification-gate → VOID
         T3 autonomy but no sealing protocol → VOID
Output:  Consequence compliance report
```

### 8.3 `skill-federation-linter`

Scans all skills for dependency declarations matching their tool usage.

```
Trigger: "lint federation", "audit skill deps"
Action:  Scan body for mcp__* references vs declared deps
Flags:   Uses mcp__geox__* but doesn't declare geox → VOID
         References skill but doesn't declare it → HOLD
Output:  Federation compliance report
```

### 8.4 `skill-constitutional-audit` (meta-linter)

Runs all three linters and produces a unified compliance report.

```
Trigger: "audit skills", "constitutional audit", "lint all skills"
Action:  Run identity + consequence + federation linters
Output:  Unified compliance report with per-skill verdicts
         (PASS / HOLD / VOID per skill)
```

---

## 9. Examples

### 9.1 Compliant Skill (HIGH-RISK)

```yaml
---
id: wealth-collapse-signature
name: wealth-collapse-signature
version: 1.0.0-2026.06.25
description: Detect institutional collapse signatures — Calhoun Phase C, capture, rent extraction.
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: high
floor_scope: [F1, F2, F4, F7, F9, F11, F13]
autonomy_tier: T3
trigger_phrases:
  - "collapse scan"
  - "institutional risk"
  - "capture detection"
dependencies:
  mcp_servers:
    - wealth
    - arifos
    - geox
    - well
  skills:
    - claim-receipt-v1
    - claim-verification-gate
    - 999-vault-seal-immutable
inputs:
  - institutional_data
  - historical_patterns
outputs:
  - collapse_signature
  - risk_score
  - receipt_block
  - seal_status
version_lock:
  schema_version: "1"
  artifact_hash: pending
---
```

**Verdict:** ✅ COMPLIANT
- Has all 8 mandatory identity fields ✅
- floor_scope has 7 floors (≥6 for high-risk) ✅
- T3 autonomy with F1+F13 ✅
- References receipt infrastructure ✅
- References sealing infrastructure ✅
- Declares MCP dependencies ✅
- Declares skill dependencies ✅

### 9.2 Non-Compliant Skill (IDENTITY_VOID)

```yaml
---
name: geox-petrophysics-bounds
version: "1.0.0-2026.06.24"
description: Bounded transforms — Vsh, porosity, Sw, AI, permeability, QC.
---
```

**Verdict:** ❌ IDENTITY_VOID
- Missing `id` ❌
- Missing `owner` ❌
- Missing `risk_tier` ❌
- Missing `floor_scope` ❌ (should be `[F2, F7, F9, F11]`)
- Missing `autonomy_tier` ❌
- Missing `dependencies` ❌ (uses GEOX MCP)
- No receipt declarations ❌

### 9.3 Non-Compliant Skill (FEDERATION_VOID)

```yaml
---
id: claim-receipt-v1
name: claim-receipt-v1
version: 1.0.0-2026.07.10
description: Minimal Claim Receipt — attaches verification evidence to every gated claim.
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: high
floor_scope: [F1, F2, F4, F7, F9, F11]
autonomy_tier: T1
# ... but body references mcp__arifos__* tools without declaring arifos in deps
```

**Verdict:** ⚠️ FEDERATION_HOLD
- Identity fields complete ✅
- But `dependencies.mcp_servers` is empty while body uses arifos MCP ❌
- Missing skill dependency on `claim-verification-gate` ❌

---

## 10. Migration Guide — Fixing Existing Skills

For skills that predate this constitution:

### Step 1: Run the audit

```bash
# From AAA root
python3 scripts/skill-constitutional-audit.py
```

### Step 2: Fix identity gaps

For each skill flagged IDENTITY_VOID:
1. Add `id` (match directory name)
2. Add `owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)`
3. Add `risk_tier` (assess honestly)
4. Add `floor_scope` (use §3.2 rules)
5. Add `autonomy_tier` (use §6.2 rules)

### Step 3: Fix consequence gaps

For each skill flagged CONSEQUENCE_VOID:
1. Add receipt references if it produces claims
2. Add sealing references if it's T3
3. Add consequence section to body

### Step 4: Fix federation gaps

For each skill flagged FEDERATION_VOID:
1. Scan body for `mcp__*` references
2. Add matching entries to `dependencies.mcp_servers`
3. Scan body for skill references
4. Add matching entries to `dependencies.skills`

### Step 5: Re-run audit

Verify all skills pass. Seal the audit report to VAULT999.

---

## 11. Versioning

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-07-11 | Initial constitution — 8 mandatory fields, 3 linters, compliance levels |

---

## 12. Authority

This constitution is authorized by:
- **F13 SOVEREIGN** — Muhammad Arif bin Fazil (human veto final)
- **F2 TRUTH** — Every claim must carry evidence
- **F11 AUDITABILITY** — Every decision logged and inspectable

**This document is law. Skills that violate it are VOID until remediated.**

---

*Forged 2026-07-11 by AAA Control Plane. Canonical at `/root/AAA/docs/SKILL_CONSTITUTION.md`.*
*Companion documents: `ROSETTA_STONE.md`, `ORGAN.md`, `KERNEL_INVARIANTS.md`.*
*Enforced by: `skill-constitutional-audit` meta-linter.*
*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE.*
