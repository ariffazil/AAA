---
name: symbol-namespace-integrity
description: "Use when importing outside material or minting notation."
version: 1.0.0
owner: AAA
category: governance
tags: [notation, namespace, intake, collision, doctrine, governance]
floors: [F2, F4, F11]
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Symbol Namespace Integrity

> **One line:** concepts travel, notation does not. A symbol in this federation is not a label — it
> carries floors, enforcement, history, and agents that already read it a certain way.

## Use when

1. An external artifact — another model's reply, an audit, a benchmark, a spec, a taxonomy, an
   architectural map, a folder layout — is about to be adopted in whole or in part.
2. You are about to mint notation: a new tier scale, band, axis, prefix, acronym, or numeric ladder.
3. A document proposes a classification scheme and you are deciding whether to encode it.
4. A proposal says "I corrected the notation" — a revision needs its own probe, not trust.
5. You are about to REUSE a symbol you did not define — citing it in a report, a doctrine, a commit
   message, or a handoff. A symbol already in circulation needs the same probe as a new one, because
   the catalog line that advertises it is not the file that owns it.

## Do not use when

1. The artifact is pure prose with no notation, and you are only extracting facts (normal claim audit).
2. You are editing existing canon that already owns its symbols — the table is the reference, not a gate.
3. The task is code/artifact verification rather than notation (use `external-artifact-verdict`).

## The One Rule

**Probe the live namespace before a single symbol is accepted.** A concept can be exactly right while
its notation is destructive, and that is the more dangerous case: tests pass, folders look clean, and
the damage surfaces months later as two agents reading the same symbol differently.

**A linter asks "does T1 exist?" — yes, so it passes. The only question that protects meaning is:
"does T1 mean the same thing to every agent?"**

## Reserved symbols — never redefine, never mint over

| Symbol | Means (binding) | Owner |
|---|---|---|
| `F1–F13` | kernel constitutional floors | `arifOS/GENESIS/FLOOR_TABLE.json` |
| `C1–Cn` | doctrine-layer floors (bind via rendered canon; do not gate a verdict) | `AAA/instructions/human-meaning-membrane.md` |
| `R0–R5` | **consequence domains** — World · Human · Machine · Witness · Who-pays · Governance | `AAA/instructions/three-consequence-domains.md` |
| `T0–T3`, `T1.5` | **authority/autonomy tier** — T0 read/probe · T1 edit/test/commit/restart-one-service (auto-do) · T1.5 proposals-only · T2 announce-then-act · T3 888_HOLD | `AAA/instructions/autonomy.md` |
| `W1–W6` | **attention-waste classes** with a 3-strike kill — sole enforcement authority | `AAA/instructions/attention-kill-criterion.md` |
| `W888` | sovereign attention cost — the scarcest resource | `AAA/instructions/sovereign-attention-preservation.md` |
| `Φ` | governance phi — bare `Φ` prohibited in cross-organ interfaces | `AAA/canon/CANONICAL_GLOSSARY.md` |
| `K3`/`K4` | already name a model and a node in federation text | — (avoid a `K0–K4` scale) |

Machine-readable: `/root/AAA/canon/SYMBOL_TABLE.json`. Add a symbol to it when a federation symbol
becomes binding; never duplicate the table into a second file.

## Procedure

### 1. Extract every token that looks like notation

Symbols, axes, tiers, bands, labels, acronyms, numeric scales, folder taxonomies. Do this as a
mechanical pass, not by reading for meaning — the whole failure mode is notation that reads fine.

### 2. Probe, before reading for content

```bash
python3 /root/scripts/symbol-probe.py <artifact>
python3 /root/scripts/symbol-probe.py --text "R0-R5 tier table ..."
cat artifact.txt | python3 /root/scripts/symbol-probe.py -
```

Run it **first**. Reading for content before probing is how the notation gets absorbed before it is
checked. Exit codes: `1` FATAL · `2` AMBIGUOUS/NEW_AXIS · `0` CLEAR.

### 3. Apply the verdict

| Verdict | Means | Action |
|---|---|---|
| `CLEAR` | no collision detected | import as-is |
| `FATAL` | the symbol already means something else here | **do not import the notation.** Import the concept in neutral words |
| `AMBIGUOUS` | the symbol is in use but not as a scale | spell it out in words; do not mint an indexed scale on it |
| `NEW_AXIS` | a free letter used at ≥2 indices while the document talks about tiers/bands/levels | a free letter is still an axis — **stage** it, do not mint it in the same breath |

### 4. Import the concept in neutral words

The safe form is always the same: state the concept, name the dimension in plain language, and let
canon assign any symbol.

```
not:  "I propose T0–T3 for authority"
but:  "I propose an authority-tier concept; map it to existing federation taxonomy.
       No symbols assigned until the namespace probe passes."
```

### 5. Compose, never rebrand

A capability's classification is the **product** of existing dimensions, not a new scale:

```
(consequence_domain) x (authority_tier) x (witness_state) x (kill_state) x (constitutional_floor)

consequence domain : world | human | machine | witness | who-pays | governance
authority tier     : T0 | T1 | T1.5 | T2 | T3
witness state      : none | self-check | tool-log | independent | human   (words until a prefix is assigned)
kill condition     : no-undo-needed | reversible | retractable-with-cost | irreversible
```

Overloading one letter with two meanings is the defect. Composing dimensions never collides.

### 6. Check for an existing owner before minting anything

A proposed concept is usually already owned — often at a *higher* layer than the artifact assumes.
Grep the live corpus for the concept before accepting a new artifact into canon:

```bash
# does any existing skill already own this concept?
grep -rli "<concept-term>" /root/.hermes/skills/*/SKILL.md
# is it owned by an always-on fragment instead?
grep -rli "<concept-term>" /root/AAA/instructions/*.md
```

**Moving an always-on rule into an on-demand skill is a governance downgrade**, not a refactor. A
fragment rendered into `base.md` binds every turn; a skill fires only if the agent loads it. Patch
the existing owner instead of minting a parallel skill.

### 7. Record the outcome

Log the accepted delta, the rejected collision, and the reason — so a future session cannot re-import
the same rejected notation. Put it in the owner fragment's **Correction Log**, and log the artifact as
the *source* while the doctrine stays the *owner*.

## Pitfalls

- **Self-correction is not verification.** An artifact that fixes one collision routinely introduces
  fresh ones on the replacement symbols — because the author is reasoning about meaning, not probing
  a table. Run the probe on **every revision**, not only the first. Responsiveness is not correctness.
- **A "hypothetical future scale" is still a scale.** Proposals that sketch a possible tier table
  "for discussion" have already minted the notation in the reader's head; the collision lands whether
  or not the author intended to import it. Probe the sketch, not just the final proposal.
- **A notation-only rejection is easy to misread as rejecting the concept.** Say plainly which half
  was accepted. "Concept correct, notation rejected, delta folded into owner X" — otherwise the next
  reader either re-proposes the notation or discards the concept.
- **Do not fork the probe or the table.** Run the installed probe by path and read the single
  `SYMBOL_TABLE.json`. A second copy in a skill directory drifts from the wired one and re-creates the
  exact defect being hunted.
- **A competing hand-maintained taxonomy loses to a derived index.** Before accepting a proposed folder
  layout, check whether the system already derives one from storage (e.g. `skill-matrix.py` computes a
  domain × organ × capability coordinate rather than storing it). A new hand-kept taxonomy has to be
  reconciled forever; structure proposals must beat the derived view on evidence, not on neatness.
- **The rendered index is a CLAIM, not the definition — resolve a symbol to its owner file before citing it.**
  A label can be misattributed in the always-loaded catalog (the generated `AGENTS.md` fragment table, a
  skill's "Adjacent skills" row, a registry one-liner, a report) while the file that actually owns the
  symbol says something else. Every session loads the index; almost none loads the owner — so a wrong
  index line propagates through each agent that quotes it, and each of them believes the notation was
  verified *because it appears in canon*. Measured: an always-loaded index bound two doctrine labels to
  a mechanism file, while the symbol table assigned those same labels to a **different** owner at
  `collision_class: FATAL`; two agents used the labels across a whole session, both citing the index,
  neither opening the definition. The probe this skill already prescribes applies unchanged — run it
  against the **definition file**, and grep the symbol to learn who defines it, *before the first
  citation*, not after the correction. Generated output is a view; when it disagrees with the owner,
  that disagreement is an index defect to report, never licence to pick whichever meaning is convenient.
- **A symbol with a live owner cannot be extended by appending to it.** Proposing `X.1`/`X.2` under a
  reserved prefix, or `X-b` under a live letter, is the same FATAL collision as minting it fresh — the
  reader of `X.1` cannot tell which parent it belongs to, and the parent already means something else.
  Stage the concept in neutral words, or take a genuinely free namespace and register it first.

## Verification

```bash
python3 /root/scripts/symbol-probe.py <artifact>          # expect the verdict you are claiming
python3 -c "import json;json.load(open('/root/AAA/canon/SYMBOL_TABLE.json'))"   # table still valid
```

A probe that has never returned `FATAL` on a real artifact is untested. Keep at least one fixture of a
known-colliding artifact and re-run it after any change to the table or the probe.

## Support files

- `references/collision-register.md` — the worked collision classes with the exact symbol pairs, how
  to recognise a notation proposal in prose, and how to extend the symbol table safely.

## Adjacent skills

| Skill | Relationship |
|---|---|
| `skill-library-integrity` | Sibling integrity class — that one governs the skill tree, this one governs the symbol namespace. |
| `external-artifact-verdict` | Verifies runnable artifacts (code); this verifies notation. Different intake gate, same posture. |
| `aaa-doctrine-sealing` | Owns the intake reference (`references/external-artifact-intake.md`) the symbol probe is step 0 of. |
