---
name: code-review
id: code-review
version: 1.0.0
description: >
  Run an extremely strict maintainability review for abstraction quality, giant files,
  and spaghetti-condition growth. Standalone maintainability review focused on
  implementation quality, codebase health, and structural simplification.
owner: AAA
risk_tier: low
autonomy_tier: T0
floor_scope: [F1, F2, F4, F7, F11]
tags: [code-review, maintainability, quality, abstraction, refactoring, structural]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Strict Code Quality Review

Use this skill for an unusually strict review focused on implementation quality, maintainability, abstraction quality, and codebase health.

Above all, this skill should push the reviewer to be **ambitious** about code structure. Do not merely identify local cleanup opportunities. Actively search for "code judo" moves: restructurings that preserve behavior while making the implementation dramatically simpler, smaller, more direct, and more elegant.

## Core Prompt

> Perform a deep code quality audit of the current branch's changes.
> Rethink how to structure / implement the changes to meaningfully improve code quality without impacting behavior.
> Work to improve abstractions, modularity, reduce Spaghetti code, improve succinctness and legibility.
> Be ambitious — if there is a clear path to improving the implementation that involves restructuring some of the codebase, go for it.
> Be extremely thorough and rigorous. Measure twice, cut once.

## Non-Negotiable Additional Standards

0. **Be ambitious about structural simplification.**
   - Do not stop at "this could be a bit cleaner."
   - Look for opportunities to reframe the change so that whole branches, helpers, modes, conditionals, or layers disappear entirely.
   - Prefer the solution that makes the code feel inevitable in hindsight.
   - If you see a path to delete complexity rather than rearrange it, push hard for that path.

1. **Do not let a PR push a file from under 1k lines to over 1k lines without a very strong reason.**
   - Prefer extracting helpers, subcomponents, modules, or local abstractions.
   - If the diff crosses that threshold, explicitly ask whether the code should be decomposed first.

2. **Do not allow random spaghetti growth in existing code.**
   - Be highly suspicious of new ad-hoc conditionals, scattered special cases, or one-off branches inserted into unrelated flows.
   - Prefer pushing logic into a dedicated abstraction, helper, state machine, policy object, or separate module.

3. **Bias toward cleaning the design, not just accepting working code.**
   - If behavior can stay the same while the structure becomes meaningfully cleaner, push for the cleaner version.
   - Strongly prefer simplifications that remove moving pieces altogether.

4. **Prefer direct, boring, maintainable code over hacky or magical code.**
   - Treat brittle, ad-hoc, or "magic" behavior as a code-quality problem.
   - Flag thin abstractions, identity wrappers, or pass-through helpers that add indirection without buying clarity.

5. **Push hard on type and boundary cleanliness when they affect maintainability.**
   - Question unnecessary optionality, `unknown`, `any`, or cast-heavy code.
   - Prefer explicit typed models or shared contracts over loosely-shaped ad-hoc objects.

6. **Keep logic in the canonical layer and reuse existing helpers.**
   - Call out feature logic leaking into shared paths or implementation details leaking through APIs.
   - Prefer existing canonical utilities/helpers over bespoke one-offs.

7. **Treat unnecessary sequential orchestration and non-atomic updates as design smells.**
   - If independent work is serialized for no good reason, ask whether the flow should run in parallel.
   - If related updates can leave state half-applied, push for a more atomic structure.

## Primary Review Questions

For every meaningful change, ask:

- Is there a "code judo" move that would make this dramatically simpler?
- Can this change be reframed so fewer concepts, branches, or helper layers are needed?
- Does this improve or worsen the local architecture?
- Did the diff add branching complexity where a better abstraction should exist?
- Is this logic living in the right file and layer?
- Did this change enlarge a file or component past a healthy size boundary?
- Are there repeated conditionals that signal a missing model or missing helper?
- Is the implementation direct and legible, or does it rely on special cases and incidental control flow?
- Is this abstraction actually earning its keep, or is it just a wrapper?
- Did the diff introduce casts, optionality, or ad-hoc object shapes that obscure the real invariant?
- Is this orchestration more sequential or less atomic than it needs to be?

## What to Flag Aggressively

- A complicated implementation where a cleaner reframing could delete whole categories of complexity
- Refactors that move code around but fail to reduce the number of concepts a reader must hold
- A file crossing 1000 lines due to the PR
- New conditionals bolted onto unrelated code paths
- Feature-specific logic leaking into general-purpose modules
- Thin wrappers or identity abstractions that add indirection without simplifying
- Copy-pasted logic instead of extracted helpers
- "Temporary" branching that is likely to become permanent debt
- Bespoke helpers where the codebase already has a canonical utility
- Sequential async flow where obviously independent work could stay simpler with parallel execution

## Preferred Remedies

- Delete a whole layer of indirection rather than polishing it
- Reframe the state model so conditionals disappear instead of getting centralized
- Change the ownership boundary so the feature becomes a natural extension of an existing abstraction
- Turn special-case logic into a simpler default flow with fewer exceptions
- Extract a helper or pure function
- Split a large file into smaller focused modules
- Replace condition chains with a typed model or explicit dispatcher
- Separate orchestration from business logic
- Reuse the existing canonical helper instead of introducing a near-duplicate
- Parallelize independent work when that also simplifies the orchestration

## Review Tone

Be direct, serious, and demanding about quality. Do not be rude, but do not soften major maintainability issues into mild suggestions.

Good phrases:
- `this pushes the file past 1k lines. can we decompose this first?`
- `this adds another special-case branch into an already busy flow. can we move this behind its own abstraction?`
- `this works, but it makes the surrounding code more spaghetti. let's keep the behavior and restructure the implementation.`
- `i think there's a code-judo move here that makes this much simpler. can we reframe this so these branches disappear?`

## Output Expectations

Prioritize findings in this order:
1. Structural code-quality regressions
2. Missed opportunities for dramatic simplification / code-judo restructuring
3. Spaghetti / branching complexity increases
4. Boundary / abstraction / type-contract problems
5. File-size and decomposition concerns
6. Modularity and abstraction issues
7. Legibility and maintainability concerns

## Approval Bar

Do not approve merely because behavior seems correct. The bar for approval is:
- no clear structural regression
- no obvious missed opportunity for dramatic simplification
- no unjustified file-size explosion
- no obvious spaghetti-growth from special-case branching
- no obviously hacky or magical abstraction
- no unnecessary wrapper/cast/optionality churn
- no clear architecture-boundary leak or avoidable canonical-helper duplication

Treat these as presumptive blockers unless the author can justify them clearly.
