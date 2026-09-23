# Mutability Classification — concrete path examples + Q1/Q2/Q3 worked example

Companion to the `federation-alignment-probe` skill. The SKILL.md defines the seven classes
abstractly; this file shows typical path shapes per class and one worked F13 binary table
for a "sweep all mentions of X" request. Real path names appear in audit reports; this file
uses generic shape (`<x>/<file>`) so it never goes stale across reorganizations.

## Class 1 — Operational / mutable

These load for runtime and their content is the point of the file. Mutation allowed, with F13 envelope.

```
<x>/SOUL.md
<x>/MEMORY.md
<x>/USER.md                              ← active default loader
<x>/lanes.yaml
<x>/profiles/<name>/memories/USER.md    ← profile fixture, dormant unless profile switch
<x>/profiles/<name>/<profile-config>    ← profile-specific overlay config
<install-root>/...                      ← installed runtime; mutate via package manager, not direct edit
<x>/skills/.../SKILL.md                 ← active skill content (curator-managed)
```

Probe before mutating: read the loader-pointer config at `<x>/` to see which profile and which
memories file the active session loads. If multiple loaders are listed, the active one wins.

## Class 2 — Audit trail / immutable (F2 HOLD)

These are append-only or one-time-write evidence. Rewriting any of these is integrity violation.

```
<x>/memories/USER.md.bak-*               ← backup snapshots before trim/cut operations
<x>/.hermes_history                      ← SQLite, append-only by doctrine
<x>/logs/agent.log                       ← live agent log
<x>/cache/delegation/live/<id>/*         ← delegation manifests + task logs (even with envelopes)
<state-root>/hermes_hook_receipts.jsonl
<state-root>/hermes_envelope_emits.jsonl
<state-root>/hermes_falsification_metrics.jsonl
<vault-root>/SEALED_EVENTS.jsonl         ← kernel seal ledger
<deploy-root>/build-info.json            ← deploy artifact metadata
<repo>/.git/objects/...                  ← git packfiles (also see Class 3)
<repo>/.git/...                          ← any git object store
```

The "even with envelopes" line is important: a delegation manifest that carries parent_trace_id is
still audit trail, because the manifest records the event. The envelope presence is a property of
the evidence, not a license to rewrite the evidence.

## Class 3 — Cryptographic / immutable (corruption on touch)

These have content-addressed storage. Any write changes the SHA256 and breaks downstream verification.

```
<x>/.curator_backups/blobs/<sha256hex>   ← curator content-addressed store
<repo>/.git/objects/pack/*.idx + *.pack  ← git packfile indices
<state-root>/...                         ← if content-addressed (check by hash directory names)
<vault-root>/<organ>/...                 ← per-organ shards if hash-named
```

Touching these means the hash chain diverges from any consumer that computed against them. Not a
governance question — a math question. The fix is to retire or supersede, never to edit.

## Class 4 — Worktree / active repo

Active repos where mutation is expected, but constrained to inside the worktree.

```
<worktrees-root>/<branch>/...     ← coding worktrees
<repo>/...                        ← canonical repo working tree
<repo>/.git                       ← repo's own git, do not bypass by writing here
```

Mutate inside the worktree, commit on the correct branch, push via the canonical push path (usually
the truth node for federation repos). Never push from a read-only mirror.

## Class 5 — Archive / pristine

These preserve a "before" state. Their immutability is the point.

```
<heritage-root>/pristine-full/...   ← frozen pristine copy
<heritage-root>/agent-copy/...      ← agent-copy archive
<seed-root>/USER.md                 ← seed snapshot
<x>/.archive/...                    ← archive snapshots
<x>/.bak-<date>-.../                ← dated backup snapshots
```

Even if the archive contains a file with a claim you'd want to revise, the archive stays — its job
is to record what was. New revisions go in the canonical path (Class 1 or Class 4).

## Class 6 — Ephemeral / regeneratable

These will be replaced by the system anyway. Mutation has low blast radius.

```
<x>/cache/spillover/call_*.txt            ← tool-result spillover, auto-rotates
<x>/cache/terminal-output/out-*.log       ← terminal output cache
<x>/skills/.hub/index-cache/...           ← skill index cache, regeneratable
/tmp/<agent>-kernel-*/                    ← ephemeral kernel runner dirs
```

The `cache/delegation/live/` subdir contains Class 2 entries (active delegations are audit trail);
sibling archived delegations may be Class 6. Probe the actual file's contents (manifest present
→ Class 2) before treating it as ephemeral.

## Class 7 — User-content / private

The human's own content. Agent does not read or rewrite without explicit per-task user direction.

```
<x>/cache/pastes/paste_*.txt        ← user pastes; content is the user's
<x>/memories/MEMORY.md              ← user-authored persona memory (when present)
<user-root>/HAMPA/human-*.md       ← human cards when in user-owned path
<user-root>/evidence/...            ← user evidence directories
```

The probe rule: even grepping these for class-of-content (`grep -i <term> paste_*.txt`) is
borderline — the human's content is private unless they have named a target class. If the audit
needs to classify user-content files by path only (not content), that is Class 7. If the audit
needs to read content, that is Class 7 + explicit user authorization.

## Worked example: Q1/Q2/Q3 for "sweep all mentions of X"

The user asks for a "sweep" of a term across the system. The right move is not to start grep'ing
and rewriting — it is to present the F13 binary table with classes pre-applied.

```
Q1: Operational files (USER.md active, profile fixtures) — patch / leave?
   Files in scope: <x>/memories/USER.md (active), 3 profile fixtures
   Class: 1 — Operational / mutable
   Trade-off (patch): targeted patch on the active file removes the only runtime-loaded reference
                      at line N; profile fixtures get the same patch for consistency
   Trade-off (leave): leaves drift between active and fixtures; future profile switch exposes the
                      term again
   Recommended: PATCH active + tag fixtures for next curator pass; do NOT broadcast-rewrite

Q2: Audit trail (.bak-*, .hermes_history, logs/, git objects) — rewrite / leave?
   Files in scope: USER.md.bak-*, .hermes_history, logs/agent.log, hermes_hook_receipts.jsonl,
                   VAULT999, git objects
   Class: 2 + 3 — Audit trail / immutable
   Trade-off (rewrite): eliminates the term from history, but breaks integrity chain (F2)
                        AND is irreversible — once rewritten, the original is gone
   Trade-off (leave): keeps audit trail intact; term remains in historical artifacts but cannot
                      be served as live evidence because backups are not loaded for runtime
   Recommended: LEAVE. Backups, logs, and git objects are F2 HOLD regardless of cosmetic intent.
                Sweep the term from runtime config (Q1) and accept that historical artifacts
                record what was. Backups age out naturally on the curator cycle.

Q3: User-content (pastes/, private memory) — read / leave?
   Files in scope: pastes/paste_*.txt, user-owned MEMORY.md fragments
   Class: 7 — User-content / private
   Trade-off (read): the agent learns what the human pasted; may inform classification but crosses
                     the privacy boundary
   Trade-off (leave): agent does not know whether the term appears in user content; safe default
   Recommended: LEAVE unread. The user's pastes are the user's purview, not the audit's. If a
                paste is part of the audit's evidence surface (e.g. a pasted analysis under
                review), the user has already authorized its content; otherwise default to leave.
```

**Why this is the only correct shape.** The user asked "sweep all mentions" — a single verb that
hides seven different files with seven different mutability classes. The F13 binary table makes
the seven-class variation visible; the user decides per class. Without the table, the agent either
(a) skips the audit and just patches the operational file, hiding the rest of the surface, or
(b) commits a broadcast rewrite that breaks F2. The table is the difference between honest
classification and governance-rotten.