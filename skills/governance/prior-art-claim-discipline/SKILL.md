---
name: prior-art-claim-discipline
description: "Use when claiming novelty, priority or 'first ever'."
version: 1.0.0
floors: [F2, F9]
triggers:
  - "is this novel"
  - "first ever"
  - "nobody has proposed"
  - "priority claim"
  - "prior art"
  - "can I claim this as new"
  - "novelty audit"
---

# Prior-Art Claim Discipline

Every claim lane in a governed organ answers *"is it true?"*. None answers *"is it ours first?"* — so a
novelty assertion travels with zero evidence, because no field exists for it to fail. This skill is that
lane: how to state a novelty claim, what each evidence state permits you to write, and how to prove the
lane actually reaches a reader.

## 1. Classify before claiming

Four tiers. Only the last one is claimable, and only as provenance.

| Tier | Example shape | Verdict |
|---|---|---|
| A feature exists | "igneous rocks exist in this province" | regional fact claim, not novelty |
| A broad possibility | "intrusions may exist in the deep section" | too wide to carry priority |
| A universal method | multi-hypothesis testing, falsification, joint inversion | always predates us; never claimable |
| A parameterised, falsifiable configuration tested against named independent observations on a named target | the actual contribution | claimable as **provenance of the artifact** |

The contribution is almost never "we discovered the phenomenon". It is "we converted a specific
hypothesis into an explicit falsifiable configuration whose predictions can be tested". Say it that way
and the claim survives review; say "first ever" and it does not.

## 2. Record it as a lane, not prose

```json
{
  "claim_id": "...",
  "claim_type": "novelty",
  "claim": "...",
  "prior_art": {"status": "UNSEARCHED", "searched_sources": [], "exhaustive": false},
  "confidence": "UNKNOWN",
  "forbidden_uses": ["first_ever_assertion", "methodological_novelty_claim"],
  "falsifier": "a prior publication stating the same parameterised test for this target"
}
```

Default on creation: `status: UNSEARCHED`, `confidence: UNKNOWN`. A `falsifier` is mandatory — for a
novelty claim the falsifier is "a prior work that says the same thing", which is checkable, unlike a
confidence score.

## 3. Three states, three permissions

- **UNSEARCHED** (default) — the claim may exist internally. "first ever", "nobody has proposed",
  "novel method" are forbidden in *every* artifact, public or internal. The formulation may still be
  described on its own merits; that separation is the point.
- **PARTIAL** — sources named, gaps named. Allowed: "no prior test of this specific configuration was
  found in <named sources>". Still forbidden: "first", "nobody".
- **EXHAUSTIVE** — needs a closure argument: what was searched, and why that set is sufficient. A long
  list is not a closure argument.

## 4. Two verdicts, never merged

HOLD on the domain truth · SEAL on the provenance of the formulation. A novelty claim never upgrades a
truth class, and a truth class never licenses a novelty claim. When reporting, state both on one line so
they cannot be silently collapsed into one another.

## 5. A claim class only exists if the reader projects it

Adding a claim type to a registry is half the work. Two silent drop points sit downstream, and both look
healthy from the registry:

1. **The loader's dispatch chain.** A type with no branch is read as nothing — no error, no warning, and a
   conformance envelope still reports `conforming: true`. Extend the branch and expose the new type as its
   own top-level result key; never fold a novelty claim into a truth-class bucket where it inherits the
   wrong authority.
2. **The compact/projection allow-list.** Any host-facing compaction (a 4 KB structured payload, a UI
   summary, a whitelist of `prefer` keys) drops unknown fields. The raw tool result contains the claim;
   every consumer downstream does not.

**Verify through the same door a human uses.** A health check proves the process started, not that the
branch is reachable. Re-invoke the actual tool/endpoint and grep the response for the new field before
reporting the lane as live.

## 6. Pitfalls

- **Match the registry file's existing serialisation before rewriting it.** Re-dumping JSON with a
  different `indent` or `ensure_ascii` setting rewrites every line; a 24-line addition becomes a 500-line
  diff and the change can no longer be reviewed. Read the first lines of the file, reuse its settings, and
  confirm the diff contains only the new claim.
- **Back up the deployed copy before overwriting it.** A service that runs from a deploy tree (not the
  source tree) makes a source-only edit invisible until copied; keep the pre-deploy file so a bad copy is
  a one-command rollback, and restart the service before verifying.
- **Do not answer "is this novel?" from memory or from the internal corpus alone.** Internal records show
  what the organisation already discussed; they cannot show what the field published. Internal familiarity
  lowers novelty (it is already known here); published literature lowers it further.
- **Absence of a prior-art search is a state, not a failure.** Report `UNSEARCHED` as the honest reading
  and name what search would close it. Filling the gap with "probably nobody" converts an unknown into a
  fabricated fact that later artifacts inherit.
- **A relayed audit's novelty verdict is testimony, not evidence.** Verify each tier against the actual
  artifact and registry before adopting the wording; the audit is often right about the gap and wrong
  about what already exists.
