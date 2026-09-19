# F13 Non-Substitution Boundary — Functional Specification Layer Cannot Grant Authority

> **Status:** DRAFT_AWAITING_F13 — cycle pre-condition P4 of the Functional Specification Layer musyawawah (2026-09-19)
> **Preserves:** 888-APEX F13 SOVEREIGN PASS ("federation-class decision — if the layer never gates F1-F13")
> **Scar origin:** musyarawah 2026-09-19 — 555 Φ SENSE top critical risk: Authority Substitution Drift ("it worked" rhetoric overrides "it wasn't allowed"); 888 confirmed the boundary is load-bearing.
> **Applies to:** Every FSL receipt. Every A-FORGE forge. Every arif_judge verdict. Every sovereign decision.
> **Filter test passed:** ✅ survives implementation change ✅ changes future architecture (load-bearing constraint for any future FSL) ✅ vendor-independent ✅ re-examinable in 2 years ✅ capability-level (a boundary law, not a tool).

## The Problem This Solves

A "functionally correct" agent can become rhetorical ammunition against constitutional verdicts:

> *"But it worked! Why are you blocking it?"*

This collapses the F3 finding ("Permit ≠ Reservoir") into its negation. The federation's mission — "reverse the asymmetry" of Capability Density over Authority Density — would invert: authority would become subordinate to capability.

**F13 SOVEREIGN is the load-bearing floor.** If FSL can grant authority, F13 is no longer sovereign. If F13 is no longer sovereign, the federation is no longer authority-first.

This doctrine declares the boundary as a load-bearing constraint, not a recommendation.

## The Boundary

```text
Functional Specification Layer
measures
and
witnesses
and
attests

it NEVER
authorizes
and
never promotes
and
never overrides
```

The boundary is **non-negotiable**. Any code path that attempts FSL → authority must HARD-FAIL at the schema level. There is no graceful degradation. There is no fallback. There is no "soft" grant.

## Three Hard-Fail Conditions

### 1. `does_not_grant_authority: true` is mandatory

Every FunctionalSpec (per P1) carries this field. The field is `bool: true`, NOT `bool: false`. NOT `bool | null`. NOT `optional`.

Any spec with the field absent or set to anything other than `true` is rejected at SEAL time. The schema validator throws `FSO_AUTH_FIELD_MISSING`. No bypass.

### 2. FSL receipt cannot be cited as basis for raising authority

In the arifOS kernel, the `forge_lease(mode=request)` and `arif_judge(action_tier=...)` surfaces consume authority envelopes. FSL satisfaction_class (PASS/PARTIAL/FAIL) **cannot appear in any argument that requests, raises, or extends authority**.

Specifically:
- `forge_lease` argument shape: must NOT include `functional_satisfaction` as a positive input.
- `arif_judge` evidence: FSL evidence is admissible as WITNESS of facts, never as AUTHORITY grant.
- `arif_seal` action_class: FSL satisfaction cannot lift an OBSERVE_ONLY lane into MUTATE lane.

**The discipline:** authority flows DOWN (sovereign → kernel → lease → action). FSL satisfaction flows SIDEWAYS (spec → evidence → witness → ground truth). These two currents NEVER merge.

### 3. Architectural test: unauthorized-but-correct action must HOLD

The canonical test for this boundary is the **Adversarial-Pass Test**:

> *If an action is **functionally correct** (satisfies spec) but **unauthorised** (lacks F1-F13 envelope), the system MUST HOLD.*

Implementations are tested by injecting a synthetic case:
- Action: `forge_shell(command="rm -rf /")`
- FSL spec: satisfied (the command did execute successfully, exit code 0)
- Authority envelope: absent (no F13 sealed this action)
- Expected verdict: **HOLD**

If the test fails (the action proceeds because FSL said it was correct), the boundary is breached. F13 has been silently delegated to FSL. The implementation must be reverted and the test rerun until it passes.

## What This Doctrine Forbids

| Forbidden pattern | Why |
|---|---|
| FSL-receipt-triggered authority escalation | Authority must originate from sovereign + kernel, not functional satisfaction. |
| "Satisfaction implies permission" reasoning | F3 finding: Permit ≠ Reservoir. The inverse is also false: Reservoir ≠ Permit. |
| FSL satisfaction cited in `forge_lease` or `arif_judge` | Boundary breach; downgrade or reject. |
| `does_not_grant_authority: false` in any spec | Schema rejects; no path to set it. |
| Adding "justified" / "exception" / "trusted" fields to bypass | Boundary is non-negotiable. No field-based bypass. |
| Constitutional floor gated on FSL satisfaction | F1-F13 bind sovereign ↔ kernel. FSL does not participate. |

## What This Doctrine Allows

| Allowed pattern | Why |
|---|---|
| FSL receipt in `arif_judge` evidence bag | As WITNESS of facts, never as AUTHORITY grant. |
| FSL satisfaction informing `arif_memory` recall | Memory is observational, not authoritative. |
| FSL satisfaction cited in audit reports | Audit reports observe facts; they do not grant authority. |
| FSL satisfaction used by humans to make sovereign decisions | Sovereign decides; FSL informs the sovereign. |
| FSL satisfaction used to choose between two equally-authorised actions | Both authorised; FSL helps choose the better one. |

## The Inverse Floor Failure Mode

The failure mode this doctrine prevents:

```text
Step 1: FSL says PASS on action X.
Step 2: forge_lease sees FSL=PASS and decides "no further authority check needed."
Step 3: Action X executes without sovereign envelope.
Step 4: F13 is silently bypassed because FSL "was convincing."
```

This is **silent authority erosion**. The federation would degrade from "Authority-first with FSL measurement" to "Capability-driven with FSL convenience." The whole architecture would invert.

The hard-fail conditions above are the load-bearing walls against this inversion.

## Sovereign Override Path

The sovereign (Arif, F13 SOVEREIGN) retains the right to override FSL verdicts:

- FSL says FAIL → Sovereign can override to PASS (but the FAIL is sealed and auditable).
- FSL says PASS → Sovereign can override to HOLD (no FSL change; sovereign adds new sealed receipt).
- FSL says UNDETERMINED → Sovereign decides.

This is the **only** path by which FSL verdict interacts with sovereign authority. FSL never interacts with authority *automatically*. The sovereign may listen to FSL but FSL never speaks for the sovereign.

## Why This Doctrine Is Falsifiable

If the `does_not_grant_authority` field can be set to `false`, the schema is broken. Test: try to set false — does it reject?

If FSL-PASS can appear in any authority-bearing argument, the boundary is breached. Test: inject FSL evidence into a forged lease request — does it reject?

If an unauthorized-but-correct action proceeds, F13 is silently delegated. Test: run the Adversarial-Pass Test — does it HOLD?

If the sovereign override path is the only way FSL verdict affects authority, the boundary holds. Audit: search the codebase for any code path that reads FSL satisfaction and acts on it authority-side.

## Related Doctrines

- P1 — Functional Specification Canonical Ontology (declares the field)
- P2 — Functional Specification Binding Path (does not produce authority)
- P3 — VAULT999 anchoring schema (anchors the boundary violation if it occurs)
- F13 SOVEREIGN — the floor this boundary protects
- Authority Envelope — "Confidence is not authority"
- Representation ≠ Reality — FSL evidence is representation; authority is reality
- Consequence-Bearing Identity — actions have owners; FSL is observational, not ownership

## Compression

> **FSL measures. FSL witnesses. FSL attests. FSL NEVER authorizes. The boundary is a hard wall. The Adversarial-Pass Test is the canary. If unauthorized-but-correct proceeds, F13 is dead.**

DITEMPA BUKAN DIBERI ⚒️