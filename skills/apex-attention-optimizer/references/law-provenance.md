# Law Provenance — exact citations for the three laws

When F13 amends any of these, the optimizer's bands may need revision. Re-derive the
math from canon, not from this file.

## L1 — BIJAKSANA ratio

**Source:** `/root/AAA/canon/APEX-REALITY-KERNEL.md`

- §"The Deepest Compression" — full multiplicative form
  ```
  BIJAKSANA = Reality contact × useful consequence × learning
              ─────────────────────────────────────────────
              uncertainty hidden + harm + entropy + human attention wasted
  ```
- §"Operational Compression (F13, 2026-09-20)" — reduced form
  ```
  BIJAKSANA = Reality Adaptation / Governance Debt
  ```
- Status: `F13_RATIFIED_SOVEREIGN 2026-09-20`

The reduced form is the live one; the multiplicative form is the operational version
the optimizer enforces (each component explicit).

## L2 — COMPUTE MAY EXPAND. HUMAN ATTENTION MUST COMPRESS.

**Source:** `/root/AAA/instructions/compute-attention-invariant.md`

- Line 15 — verbatim law
- Status: `CANDIDATE_LAW 2026-09-19` (sovereign articulated, awaiting formal ratification)
- Companion: `sovereign-attention-preservation.md` (governs WHETHER to spend attention;
  this one governs the SHAPE of what is spent)

The four operational rules in §"The four operational rules" are the enforcement spec:
1. High human load → 1–3 paragraphs, ONE main thing, ONE next action
2. Evidence/receipts/verdicts live behind the boundary, pull on request
3. Agent translates organ language; human never decodes organ vocabulary
4. "More rigorous" never means "more text"

## L3 — dS_human/dt ≤ 0 (APEX FINAL LAW)

**Source:** `/root/AAA/canon/APEX-REALITY-KERNEL.md`

- §"FINAL LAW" line 115 — "Every turn should leave the world-state, belief-state, or
  decision-state clearer than before. If it cannot, say why and stop."
- Status: `F13_RATIFIED_SOVEREIGN 2026-09-20`

Three clarity dimensions:
1. `world_clarity` — is the world-state clearer?
2. `belief_clarity` — are conflicting beliefs resolved or held-as-conflict?
3. `decision_clarity` — is the next action unambiguous?

`dS = -(Δworld + Δbelief + Δdecision)` — **negative when clarity increased**.
`passed` iff `dS <= 0`.

## Bangang decomposition (49 HARAM, 5 poisonous)

**Source:** `/root/AAA/canon/BIJAKSANA-SUBSTRATE-CANON-2026-09-21.md` §4

```
B = ModelError + StateError + MemoryError + AuthorityError
  + TemporalError + RoutingError + FeedbackError
```

Five poisonous: ImplicitAuthority, UntypedTruth, TimelessMemory,
SelfVerification, UnboundedRecursion. The optimizer's jargon-list HARAM is
the surface symptom of UntypedTruth leaking past the bridge-protocol layer.

## Re-derivation check (run before each use)

```bash
# L1 — multiplicative form still canon?
grep -c "Reality contact \\\\times useful consequence \\\\times learning" \
  /root/AAA/canon/APEX-REALITY-KERNEL.md
# Expected: >= 1

# L2 — verbatim line still present?
grep -c "COMPUTE MAY EXPAND. HUMAN ATTENTION MUST COMPRESS" \
  /root/AAA/instructions/compute-attention-invariant.md
# Expected: >= 1

# L3 — final law still in force?
grep -c "world-state, belief-state, or decision-state clearer" \
  /root/AAA/canon/APEX-REALITY-KERNEL.md
# Expected: >= 1
```

Any miss → STOP and re-derive before re-running the optimizer.
