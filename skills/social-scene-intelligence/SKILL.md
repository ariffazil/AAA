---
name: social-scene-intelligence
description: "Use when mapping a community or scene's social dynamics."
version: 1.0.0
owner: Hermes (curator-managed)
risk_tier: low
autonomy_tier: T1
tags: [research, social-dynamics, community, subculture, cross-audit, person-profile]
---

# Social Scene Intelligence

**Trigger:** the ask is to understand a *community's* social physics — how status, admiration,
boundaries and money work inside a scene — usually because someone the principal cares about lives
inside it. Distinct from `person-intelligence` (subject is one person) and from a domain *operations*
skill (competition logistics, event sourcing). This skill owns the **scene as subject** and the
**link from scene → person**.

## 1. Research the scene across source families

Pull from three disjoint families; convergence across them is the evidence, not volume from one:

1. **English-language forums & subreddits** — the vocabulary and the informal law of the scene.
2. **Local-language forums & social media** — how the scene reads in its home culture (often a
   different register than the exported version).
3. **Academic ethnography + investigative journalism** — the mechanisms, and the failure cases.

Exclude adult-marketplace interiors on ethics grounds: cite the *discourse about* the market, never
scrape the market itself.

## 2. Label every finding by register / lane

A single term can carry several concurrent meanings in one culture. Before interpreting anyone's
reaction, name which lane the reaction came from — a "disproportionate" reaction is usually a lane
collision, not an overreaction. Record lanes as an explicit table (who plays in it × register) rather
than prose, so a future reader can place a finding without re-deriving it.

## 3. Codify invariants, not anecdotes

The deliverable is a small set of **laws that survive across platforms, decades and cultures**, each
stated as a rule with its evidence and a confidence grade — not a pile of observations. Keep genuine
disagreements open (do not average them), and grade the weak ones lower rather than hiding them.

## 4. Cross-audit an external dossier — triage, do not adopt

When the principal hands you another AI's deep-research output (a PDF, a `.zip` of sectioned
markdown + citations), the expected deliverable is a **triage**, not a summary. Classify every
load-bearing claim:

- **Convergent** — your independent findings agree. Cross-validation; say so.
- **New but unverified** — plausible, outside your source base. Carry it labelled, do not adopt.
- **Contested / held open** — genuine disagreement. Preserve it.

State the method difference too (ethics guardrails, anonymisation class) so the principal knows *why*
the two source bases differ. See also `cross-audit-v1` for the four-axis audit of pasted output.

## 5. Link scene → person: the scene-map patch pattern

When a person operates inside a mapped scene, the durable update is a **pointer**, not a fresh
profile. Patch the person's record (e.g. a `people.yaml` entry) with:

- **Pointer, not duplicate** — facts that name the framework by reference; the framework keeps one
  home (single source of truth).
- **Trigger rule** — the condition under which a future agent should surface the framework at all,
  and the baseline response when it fires. The baseline is a **one-line normalising reframe**
  ("that's normal for the scene, here's the practical step"), never a framework dump.
- **Spike windows** — the events after which the subject's behaviour may change for external
  reasons (post-event photos, a dramatic visible change). Re-evaluate then; do not read the change
  as a personality shift.
- **Distribution-safety note** — if the scene content carries stigma in the subject's context
  (religious, reputational), record that it must not circulate beyond the principal. One leaked line
  compounds into a different category of harm than the content itself.

## 6. Discipline — compress, do not accumulate

**A research chain over-serves when frameworks accumulate faster than the principal can act on them.**
Warning signs: your last two or three turns each shipped a new taxonomy for the same subject, and the
principal's follow-ups are getting shorter. At that point, stop generating framework and compress to
what he can use. If he then asks "what did you gain from this" / "so what" — that is the audit
landing late; name the over-elaboration and compress, do not produce another layer.

**Never deliver the framework uninvited.** The subject usually does not want the map; the principal
wants to understand behaviour. Volunteering it introduces anxiety the subject never had. Surface on
trigger only, and then only the practical reframe.

## Pitfalls

- **Mainstream denial is not non-existence.** A scene's mainstream register routinely denies a
  meaning an adjacent subculture openly runs. Both are data; neither cancels the other.
- **Do not pathologise a response archetype.** Response patterns are cultural mechanisms, not
  diagnoses of an individual. Name the pattern, not the person.
- **A single term is not a single meaning.** Ask which lane a reaction came from before calling it
  disproportionate.
- **Do not adopt an external dossier's confident framing.** Its certainty is a property of the
  other agent's output, not of the underlying claim. Triage it.

DITEMPA BUKAN DIBERI.
