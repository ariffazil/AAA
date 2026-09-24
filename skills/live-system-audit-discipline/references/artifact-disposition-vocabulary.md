# Artifact Disposition Vocabulary — for files under review

> Six precise status terms. Each carries a different *kind* of action, and conflating them is the
> same defect class as the IRFAN-EUREKA-SEAL self-ratification: an authority-verb used inside the
> file's own contents to describe the file's own standing.

## The six terms

| Status | Meaning | Who can apply it | Mutates the file? |
|---|---|---|---|
| **PRESENT_IN_WORKSPACE** | Artifact exists at a known path; presence observed | Inventory tool / agent | No |
| **UNRATIFIED** | Not approved as canonical / constitutional / ratified | Agent may *report*; F13 alone decides promotion | No |
| **RATIFICATION_REFUSED** | The artifact *cannot* be treated as ratified under current governing constraints (clauses listed) | Agent may issue with clause-level reasons | No |
| **QUARANTINED_REGISTRY_ONLY** | A registry record blocks promotion/use pending review; original remains untouched | Agent may propose/apply within registry scope | No |
| **CANONICAL** | Approved source of reusable system truth | F13 via canon-mutate workflow | Yes — canonical registry/write path |
| **ARCHIVED** | Retained historical artifact, not active operating input | F13 or approved lifecycle workflow | Potentially |

## Allowed actions per status

| Status | read | extract candidate claims | propose promotion | canonical write | move / delete |
|---|---|---|---|---|---|
| PRESENT_IN_WORKSPACE | ✅ | ✅ | ✅ | ❌ | ❌ |
| UNRATIFIED | ✅ | ✅ | ✅ | ❌ | ❌ |
| RATIFICATION_REFUSED | ✅ | ✅ | ❌ (with reasons listed) | ❌ | ❌ |
| QUARANTINED_REGISTRY_ONLY | ✅ | ✅ | ❌ (gate blocked) | ❌ | ❌ |
| CANONICAL | ✅ | ✅ | ✅ | ✅ (canonical-mutate only) | F13 decision |
| ARCHIVED | ✅ | (extract only) | ❌ | ❌ | F13 decision |

## The false-claims the agent must avoid

- **"Hermes held the file."** Holding implies custody. The agent's relationship with the file is
  one of *judgment* (refusal, classification, registry record), not custody. State the actual
  capability-or-path condition: "the file remained at its original path because the agent
  could not write to its intended location" — not "the agent held it".

- **"The agent sealed the file."** Sealing is a verb reserved for the principal (F13). The
  agent may *propose a seal package* (artifact + claim + evidence + contradiction check +
  diff); the principal alone *ratifies*. Writing the word SEAL over a document without a
  ratification chain is the defect this vocabulary exists to prevent.

- **"The agent moved the file to quarantine."** Quarantine is a *registry label*, not a file
  move. Original integrity is preserved. The agent may apply the label inside its own registry
  scope; it must not move, rename, chmod, or otherwise touch the file.

- **"The incident is closed."** `closed` is reserved for a finding whose root cause has been
  reproduced, patched, and verified. Anything less specific stays at `mitigated_not_root_caused`,
  `operationally_stable_not_root_caused`, or `partially_characterized` with a daylight test
  named. See `live-system-audit-discipline` SKILL.md §P1 rule 3 for the closure vocabulary.

## Incident status vocabulary (companion)

For incident receipts (incidents.md artefacts), the closure-language set is:

| Status | When |
|---|---|
| `mitigated_not_root_caused` | Service is back; cause not yet reproduced; daylight test named |
| `operationally_stable_not_root_caused` | Service is observed healthy, monitoring materially improved; closure is operational, not epistemic |
| `partially_characterized` | One cause family identified; sibling causes not yet reproduced |
| `superseded_by_<receipt>` | Replaced by a later probe; preserved for causal record, never retracted |
| `closed` | Root cause reproduced, patched, verified end-to-end — used sparingly |

## Why this vocabulary exists

When an artifact's own front matter declares `status: ratified` and cites itself as the
ratification authority, every downstream consumer inherits the false authority. The vocabulary
above separates:

- **The artifact's claim about itself** (UNRATIFIED) from **the principal's ratification** (CANONICAL).
- **The agent's judgment on the artifact** (RATIFICATION_REFUSED) from **the registry's treatment of the artifact** (QUARANTINED_REGISTRY_ONLY).
- **The artifact's presence** (PRESENT_IN_WORKSPACE) from **its standing** (the next four).
- **The incident's operational state** (mitigated / stable) from **its epistemic state** (root-caused or not).

Use the smallest term that fits. When two could fit, prefer the one with fewer implied
authorities. Three true defaults:

1. If unsure whether something is canonical → UNRATIFIED.
2. If an agent's own output declares itself ratified → RATIFICATION_REFUSED.
3. If a closure was chosen without a daylight test → operationally_stable_not_root_caused.