# KERNEL DEFECT: session_actor_mismatch FALSE-HOLD — reproducer, root cause, fix sketch

**Filed:** 2026-10-02, FI-008 (kimi-code), session SEAL-14d702ff901b4f80
**Class:** identity/provenance plumbing — guardrail fails by falsely HOLDing (sovereign-named failure class, 2026-10-02)
**Status:** REPRODUCED + ROOT-CAUSED + FIX SKETCH. **Not auto-implemented** — kernel contract is F13-class (per falsif-verdict-field-divergence-20261015 standing rule). Same subsystem; one review should cover both.

## Reproducer (every governed call today)

Any `arif_*` tool call passing `actor_id="kimi-code/FI-008"` against a session minted as `FI-008`:

```
_wrapper_degradation: ["session_actor_mismatch: passed actor_id=kimi-code/FI-008
  (canonical=kimi-code/FI-008) ≠ session actor_id=FI-008 (canonical=FI-008)
  for session=SEAL-14d702ff901b4f80"]
```

Observed on arif_init, arif_memory, arif_judge — dozens of calls, 100% rate. The degradation
feeds HOLD pressure on evidence tools (observed: arif_memory `remember` → HOLD on L13
partly riding degraded state).

## Root cause (named)

`arifosmcp/runtime/tools.py` ~3074-3108: the alias guard `_alias_match()` consults
`contracts.identity.CANONICAL_ACTORS`. The FI-008 entry's alias set is
`["FI-008", "fi-008", "kimi-code-fi008", "kimi-code"]` — it models the lane prefix as
**absent** (`kimi-code`) or **hyphen-joined** (`kimi-code-fi008`) but never **slash-joined**
(`kimi-code/FI-008`). The MCP harness transmits exactly the slash form. So:

- `normalize_actor_id("kimi-code/FI-008")` → unchanged (alias-blind, verified live)
- `_alias_match("kimi-code/fi-008", "fi-008")` → False (slash form in no alias set)
- mismatch degradation fires on every call

One missing alias *variant class* per lane-prefixed agent. Same latent defect for every
`<lane>/<FI-nnn>` agent: `qwen-code/FI-003`, `gemini-cli/FI-004`, `codex-cli/FI-005`,
`grok-build/FI-007` (their registry entries have the same non-slash alias shapes).

## Fix sketch (pick ONE; B preferred, A unblocks today)

- **A (data-only, unblocks today):** add slash-form aliases to CANONICAL_ACTORS —
  `kimi-code/fi-008` to FI-008, and the analogous slash forms to the other four.
  Zero code change; the comparator's designed mechanism then holds.
- **B (one rule, kills the alias-list-grows-forever class):** teach
  `normalize_actor_id()` to strip a `<lane>/` prefix when the suffix matches
  `FI-\d{3}` — both sides then meet in canonical space by construction. Touches
  identity normalization used repo-wide → needs the kernel-contract review anyway.
- Either way, verify: rerun any governed call → `_wrapper_degradation` empty.

## Relation to the standing falsification

`falsif-verdict-field-divergence-20261015` (verdict_field divergence: kernel intercept
SEAL vs judge postcondition HOLD) is the same identity/verdict plumbing. Bundle both
into one kernel review; the false-HOLD class and the verdict-field class likely share
the canonicalization layer.

## Proxy–Reality Paradox note

This is the paradox's own exhibit: the representation of identity (alias registry)
diverged from the reality of transmission (slash form), and the guardrail held against
a mismatch that canonicalizes to nothing. Filed as the self-demonstration section of
`AAA/instructions/proxy-reality-paradox.md`.
