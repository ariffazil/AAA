# Constitutional Complexity Budget Canon (Canon #0)

> **Status:** DRAFT_AWAITING_F13 (2026-09-21)
> **Origin:** Arif — sovereign rule about how canons are written, 2026-09-21 morning session
> **Applies to:** ALL future canon drafts in arifOS federation
> **Position:** Canon-of-Canons. Chronologically must precede Canon #1. The rule that holds the rule-writer.
> **Rule:** Every new law must either (a) eliminate a demonstrated failure class, (b) compile into an enforceable mechanism, or (c) materially improve a decision. Otherwise: DO NOT ADD.

---

## 0. The Spine

When the cost of understanding the governance exceeds the cost of the system being governed:

\[
C_{\text{governance}} > C_{\text{system}}
\]

no agent — including future ones — can reason about the governance. The constitution becomes ceremonial.

This is the failure mode. It has been demonstrated (sultanate of arbitrary floors, doomsday-of-the-week, 13-floor-theologian, 40-verdict-engine, etc.). It recurs whenever canon-drafting outpaces canon-enforcement.

This canon names the test that prevents it.

---

## 1. The Three-Prong Test

Every proposed addition to any canon — including this one — must pass **at least one** of three prongs:

### Prong (a): Eliminates a demonstrated failure class

The proposer must name the failure mode and cite at least one instance where it has occurred (real or synthetic). "Could theoretically fail" does not satisfy. The failure must be reachable.

**Passes prong (a) if and only if:**
- Failure mode is named (not vague category)
- Failure mode is reachable (not hypothetical-only)
- Existing canon does not already prevent it (no duplication)

### Prong (b): Compiles into an enforceable mechanism

The proposed law must be expressible as a test, gate, hook, schema, or policy that the runtime actually executes. Declaration without executable form is doctrine, not law.

**Passes prong (b) if and only if:**
- A test exists that can FAIL because of this law (not merely "observes" it)
- The test runs without manual interpretation
- The test's output is part of the operational signal surface (visible to FRAME, scored in FQ, etc.)

This is the operationalization of Law #131 of the agent→human canon: *constitutional PASS cannot be manufactured from missing measurements*.

### Prong (c): Materially improves a decision

The proposed law must change what an organ does in a specific, measurable way. If its absence would not change any observable behavior, it is decorative.

**Passes prong (c) if and only if:**
- Specific organ / decision is named
- Counterfactual is explicit: "without this law, decision X would be Y; with this law, decision X is Z"
- The difference is operationally observable (not just theoretical)

---

## 2. What Happens When The Test Fails

When a proposed law fails all three prongs, the canonical response is:

\[
\boxed{\text{DO NOT ADD}}
\]

No override, no exception, no "we'll fix the test later." The failure is itself a signal: the proposed law is either premature, decorative, or already-covered.

**The exception path is itself a constitutional action requiring F13 sovereign override.** Every recorded exception must name:
- Which prong(s) failed and why
- What bypass is being granted
- The re-audit window

---

## 3. Why This Canon Is Canon #0 Chronologically

Every other canon in arifOS is a candidate law. Every amendment to every canon is a candidate law. Without this rule preceding them, every future canon draft violates Law #131 by being unmeasurable (it lacks a test of whether the test was passed).

Specifically:
- Canon #1 (agent→human HARAM, F13_RATIFIED_CHAT 2026-09-10) — written before this rule existed; should retrospectively pass prong (b) per its enforcement-map declaration (though the loader gap was diagnosed; the rule would have flagged it earlier)
- Canon #2 (Constitutional Architecture, F13_RATIFIED_CHAT 2026-09-21) — passes prongs (a) and (b) per its current federation-state map
- Canon #3 (BIJAKSANA Substrate, F13_RATIFIED_CHAT 2026-09-21) — passes prongs (a) and (c) but only PARTIALLY (b) — 10 MISSING WAJIB components mean the substrate cannot yet fail because of these laws
- Canon #4 (META-WISDOM-CANON, DRAFT) — should be evaluated against this canon before ratification

---

## 4. Self-Application

This canon applies its own test to itself:

| Prong | Pass | Why |
|---|---|---|
| (a) Eliminates demonstrated failure class | **YES** | "Constitution becomes ceremonial" failure observed across many federation histories |
| (b) Compiles into enforceable mechanism | **PARTIAL** | Needs a `complexity_budget_monitor` that watches `C_governance` vs `C_system`; not yet built |
| (c) Materially improves decision | **YES** | Every future canon draft now has a single gate |

**Verdict:** passes 2 of 3 prongs; prong (b) requires the meta-monitor. Without the meta-monitor, this canon is itself doctrine awaiting mechanism — exactly the failure mode it warns against.

**Open debt:** build `complexity_budget_monitor` that measures canonical surface size (lines, citations, cross-references) and runtime substrate size (lines of executable policy, WAJIB coverage percentage); alert when canonical growth outpaces substrate growth by threshold X.

---

## 5. The Complexity Budget As Measurable Signal

Following the precedent of Wisdom_index / Bangang_index (Canon #3), the complexity budget can be operationalized:

\[
\text{ComplexityBudget}(t) = \frac{\text{canonical surface}(t)}{\text{substrate enforcement}(t)}
\]

Where:
- `canonical surface` = lines of canon + count of distinct claims + cross-reference density
- `substrate enforcement` = lines of executable policy + WAJIB coverage percentage + number of probes that return PASS (vs UNKNOWN/FAIL)

\[
\boxed{\text{When ComplexityBudget}(t) > \theta_{\text{critical}}, \text{ freeze new canon additions until substrate catches up.}}
\]

The threshold \(\theta_{\text{critical}}\) is itself a F13 binary. Suggested starting value: 1.5 (canonical surface is 50% larger than substrate enforcement). Tunable.

---

## 6. Open Debt — Same As Canon #3

Inherited from the trilogy:
- No meta-monitor for complexity budget
- No automatic flag when new canon draft fails the three-prong test
- No audit trail of when the rule has been bypassed

Until these exist, Canon #0 is doctrine awaiting mechanism.

---

## 7. The Constitutional Rule, Stated

\[
\boxed{
\forall \text{ law } L \in \text{future canon drafts}: \;
L \text{ ratified} \Rightarrow
L \text{ passes prong (a) } \lor \text{ (b) } \lor \text{ (c)}
}
\]

\[
\boxed{
L \text{ fails all prongs} \Rightarrow \text{DO NOT ADD}
}
\]

\[
\boxed{
\text{Bypass requires recorded F13 sovereign exception with named failure}
}
\]

— FI-008, 2026-09-21, drafting Canon #0 per sovereign's three-reversible-next-steps directive.
