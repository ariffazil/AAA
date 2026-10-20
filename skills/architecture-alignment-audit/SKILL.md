---
name: architecture-alignment-audit
description: "Audit external research documents, agent proposals, or architectural blueprints against locked AAA/arifOS doctrine. Checks: (1) claims that don't match live state, (2) Phase E+ solutions proposed during Phase A-C, (3) naming sovereignty — external brands never rename locked vocabulary, (4) contradictions with explicitly rejected directions. Triggers: PDF/DOCX/architecture proposals from Gemini/Claude/architect, 'does X align with our system', external standard proposals, design specs from research. Covers: Gemini AIMS/HDP/IBCT/x402 audits, naming registry creation, Hermes FED reasoning_content patches."
tags: []
related_skills:
  - verify-sibling-ops-reports
  - constitutional-institution-mapping
  - federation-agent-card-ops
---

# Architecture Alignment Audit

Audit external research documents, proposals, and architectural blueprints against locked AAA/arifOS doctrine. This is a **verification-of-alignment** discipline, not a synthesis task.

When external research proposes changes, first ask: **does this contradict what we've already decided?**

## 1. When to use this skill

Use when:
- Gemini Deep Research, Claude, or any agent delivers a multi-page architecture proposal
- External IETF RFC drafts or protocol proposals (AIMS, HDP, IBCT, x402, AP2, PEER) are surfaced as potential integration targets
- A sibling agent proposes an architectural change
- Someone pastes a "future architecture" report that includes naming conventions

Do NOT use for:
- Operational claims about what was done (→ `verify-sibling-ops-reports`)
- Theoretical framework mapping onto F1–F13 (→ `constitutional-institution-mapping`)
- Agent card geometry or 3-layer classification (→ `federation-agent-card-ops`)

## 2. The four-gate audit

Before acting on any external proposal, run through all four gates:

### Gate 1: Claims vs Live State (F2 verification)

For every factual claim in the proposal:

1. Extract the specific claim (e.g., "165M transactions across 69K agents")
2. Verify against live state: `state-probe.sh`, `curl :port/health`, repo commits, web search
3. Label: **OBS** (verified), **DER** (inferred from verified data), **SPEC** (unverifiable), **UNKNOWN** (contradicts live state)

Example from 2026-08-09 Gemini PDF audit:
```
Claim: "x402 processes 165M transactions across 69,000 active agents"
Reality: 119M on Base + 35M on Solana ≈ 154M. 69K agents unverifiable.
Label: SPEC
```

### Gate 2: Phase Mismatch (the critical gate)

The proposal implicitly assumes the system is in a different phase than it actually is. This is the most dangerous failure mode: **Phase E solutions for Phase A problems**.

Before the audit, confirm current phase:
```bash
/root/AAA/scripts/state-probe.sh
# Verify: STATE_READY? What phase are we in?
cat /root/AAA/docs/STATE.md | head -10
```

Then classify every proposal in the document:

| Phase the proposal targets | Is it the current phase? | Action |
|---|---|---|
| Phase A (ops state) | ✅ YES | Evaluate and execute now |
| Phase B (citizens) | After A is boring | Note as Phase B candidate |
| Phase C (mesh maturity) | After citizens | Note as Phase C candidate |
| Phase D (thin control plane) | Ongoing | Monitor, not build |
| Phase E+ (economic sovereignty, legal, external interop) | Months away | **Park it.** File as horizon intelligence. |

The pitfall: "solving problems AAA doesn't have yet." Example: building x402 payment rails when the telephone hasn't been dialed once. Building payment infrastructure for non-existent commerce is the definition of unused telephone.

### Gate 3: Naming Sovereignty (the branding gate)

External research introduces terminology. AAA already has its own names. The rule:

> **External standards may MAP; they do not RENAME the institution.**

For every external concept in the proposal:
1. Check: does AAA already have a name for this?
2. If yes → map it in the translation table, never adopt the external brand
3. If no → flag as "new concept, needs sovereign decision before adoption"
4. New names for existing concepts = **BLOCKED** (unless explicitly forged)

**Canonical naming registry:** `/root/AAA/docs/IDENTITY_NAMING_REGISTRY.md`

The translation table pattern (from 2026-08-09 sealed doctrine):

| External concept | AAA name | Status |
|---|---|---|
| AIMS (IETF) | Landscape only | Not adopted |
| SPIFFE/SPIRE | `arif_init` + ACT + organ keys | Map, not install |
| WPT (short-lived creds) | ACT (`act_v1.*`) | Already named |
| W3C VC | warga passport / `warga_status` | Already planned |
| HDP/IBCT | ACT chain / hop receipt | Research alias, not brand |
| DID | `did:web:arif-fazil.com` | Already named |

**Forbidden from the registry:**
- No SPIRE/AIMS organ
- No `spiffe://` as directory primary
- No HDP/IBCT identifiers in code until multi-hop is deliberately forged
- No replacement of Ed25519+ACT with X.509-SVID as doctrine

### Gate 4: Doctrine Contradictions

Compare the proposal against explicitly locked doctrine. Look for:

1. **"Explicitly not next" violations** — the sovereign listed things that are explicitly deferred
2. **Ceiling violations** — proposal asks AAA to become something it's not (e.g., AAA = judge or executor, when AAA is DISPLAY_ONLY)
3. **Irreversibility proposed as T1** — external standard adoption may require irreversible commitment (e.g., SPIRE server = new organ = needs sovereign)

## 3. Output format

Always produce a structured audit:

```
AUDIT of: [document name]
Date: [date]
STATE check: [STATE_READY / DEGRADED / DOWN]

## Gate 1: Claims verified
| Claim | Reality | Label |
|---|---|---|

## Gate 2: Phase map
| Proposal item | Target phase | Action |
|---|---|---|

## Gate 3: Naming sovereignty
| External term | AAA name | Adopt? |
|---|---|---|

## Gate 4: Doctrine contradictions
| Proposal | Locked doctrine | Conflict? | Resolution |
|---|---|---|---|

## Verdict
Aligned / Partially aligned / Misaligned
Top 3 actions (if any)
Top 3 risks (if any)
```

## 4. Post-audit: what to do with parked intelligence

Items classified as "parked" (Phase C/D/E+) should:
- NOT trigger any code changes
- NOT create new organs or new ports
- Be filed as horizon intelligence (knowledge, not architecture)
- Be re-evaluated when the relevant phase begins

The discipline: "Read the map, don't build the road."

## Pitfalls

- **Don't skip Gate 2.** The most dangerous failure mode is treating a Phase E proposal as a Phase A action. The external research LOOKS good technically — the problem is TIMING.
- **Don't adopt external naming.** Even if the external term is "cleaner" or "better-known." AAA's vocabulary is locked by sovereign decision. Research maps; it doesn't rename.
- **Don't build payment rails for non-existent commerce.** This is the general pattern: building infrastructure for a problem AAA doesn't have yet. The telephone must work before the payment system.
- **Don't confuse "technically sound" with "right next."** The proposal can be 100% correct about the technology AND be the wrong priority. Phase mismatch ≠ technical error.
- **F2 matters even in alignment audits.** A proposal that cites fabricated or inflated stats (e.g., "165M transactions" when reality is ~154M) loses credibility on all gates, even if the directional logic is correct.
- **Re-apply reasoning_content patch after Hermes upgrades.** The FED thinking-pad patch (`_needs_fed_thinking_proxy()`) lives under `/usr/local/lib/hermes-agent/run_agent.py` — reapply script at `/root/forge_work/2026-08-09-hermes-reasoning-pad/reapply_pad_patch.py`. This is an operational pitfall, not a doctrine issue.

## Support files

- `references/identity-naming-registry-2026-08-09.md` — the sealed naming translation table (AIMS→AAA, HDP→ACT, etc.) with forbidden creations list
- `references/reasoning-pad-patch-2026-08-09.md` — FED thinking backend detection, patch location, reapply instructions

<!-- SKILL-WITNESS-NOTE (auto, additive-only) -->
Witnessed reality moved this skill's selection to **ROUTE or MERGE**.
Scar signatures: 2026-09-07-w3-degradation-during-doctrine-writing
Do not treat this skill as neutral until the signatures are resolved.
<!-- /SKILL-WITNESS-NOTE -->
