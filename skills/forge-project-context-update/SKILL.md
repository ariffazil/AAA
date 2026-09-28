---
id: forge-project-context-update
name: forge-project-context-update
version: 1.0.0
description: "Merge-update an existing AGENTS.md surgically."
autonomy_tier: T1
risk_tier: low
floor_scope: [F2, F4, F9]
owner: AAA
capability_tier: fed-long-context
ecology_state: WARM
tags: [agents-md, project-context, merge-edit, surgical, doc-authoring]
host_compatibility:
  - claude-code
  - codex
  - opencode
  - kimi
  - kimi-code
---

# forge-project-context-update — merge-update existing AGENTS.md

> **Read the file. Preserve the user's wording. Add what's missing. Surgical edits only.**

This is the WRITE discipline for the `/init` workflow when the project already has an AGENTS.md. It is the opposite of `forge-repo-intelligence` (read-only audit) and `forge-readme-truth-check` (drift detection). It does not regenerate from scratch and it does not append a "what I did this session" footer — it merges in only the missing or verifiably-stale facts.

## When to use

- `/init` prompt asks to UPDATE an existing AGENTS.md at a known path.
- A user asks to "improve", "tighten", "complete", or "refresh" an existing project-context file.
- The file exists, contains user's wording in frontmatter / sections / footer notes that must survive.

## When NOT to use

- File does not exist → write a fresh class-level AGENTS.md following the repo's existing docs convention instead.
- Task is to audit whether the AGENTS.md matches reality → use `forge-readme-truth-check` (drift detection), not this skill.
- Task is to remove or refactor the AGENTS.md structure → needs explicit F13 + musyawarah, not a merge.

## Procedure

### 1. Inspect the repo first (read-only)

Before touching AGENTS.md, probe the repo to learn what an agent actually needs. Order matters — manifests first, conventions second, pitfalls third:

```text
a. Manifests and toolchain
   - pyproject.toml / package.json / Cargo.toml / go.mod / Makefile / tox.ini / CI workflows
b. Existing docs
   - README.md, docs/, FEDERATION.md, ARCHITECTURE.md, STATE.md
c. Directory layout (top-level ls)
d. Test / lint configuration
e. Files that hint at pitfalls:
   - .gitignore (runtime artifacts, secrets)
   - *.lock / *.flock / *.pid (concurrent-writer protection)
   - *.bak.* siblings (rotation in progress — do not touch the active file mid-rotation)
   - *.disabled or *.phase1.bak (in-flight mutation)
```

Probe before you assert. If a manifest does not exist, that absence is the fact (e.g. "No Makefile. No package.json. Python is the only toolchain.").

### 2. Read the FULL existing AGENTS.md

Not from a snippet in the conversation. Not from a cached copy. **Fresh read with `read_file`** of every page — for files needing `offset`/`limit`, paginate.

The merge requires the exact current content because:

- **Frontmatter** (YAML between `---` markers) may carry identity / authority / `loaded_at` fields that must survive unchanged.
- **Footer HTML comments** often hold provenance notes ("this section was removed by X and restored by Y — SOUL.md owns it again") that the user keeps on purpose.
- **Wording the user picked** (e.g. "Jangan jadi engineer yang pandai menyusahkan manusia") is binding — re-paraphrasing it is a quality regression.

### 3. Identify the merge shape

Before writing anything, classify every existing line into one of four buckets:

| Bucket | Action |
|---|---|
| **PRESERVE** — frontmatter, user's exact wording, footer provenance | Leave untouched |
| **PRESERVE-AND-EXTEND** — section that needs a sibling added | Append, do not rewrite |
| **STALE** — command, path, or fact that contradicts the repo | Surgical replace with the verified replacement |
| **MISSING** — repo fact that is not yet in the file but is load-bearing for a coding agent | Add a new section |

Default: PRESERVE. The bar to mutate is "verifiably contradicted by an artifact in the repo I just probed."

### 4. Write the merged file

Use `write_file` with the FULL merged content. The tool will refuse with `stale_write_blocked` if you have not freshly read the file in this task — that refusal is correct, not a bug. Reload with `read_file`, merge, retry once.

Forbidden moves:

- Append-only modes ("ADD: …" at the bottom without reorganising). Future readers cannot tell what is original and what is new.
- Wrapper-prefix modes ("# Updated by <agent> on <date>"). The file is a pointer or constitution; provenance belongs in frontmatter or a footer comment, not as a heading.
- Regenerate-from-scratch. The user said "update", not "rewrite". If you cannot justify why a sentence must change, do not change it.

### 5. Verify the merge landed

After `write_file`, the tool returns `verified: true` with the on-disk hash. Do not re-read the file to check; the hash is the receipt. Only re-read if you suspect the verifier ran against a different file or you are about to claim a hash in a downstream report.

Confirm to the user: the exact path written and a one-line summary of what was added/changed. Not a paragraph; one line.

## Pitfalls (durable rules)

- **The stale-write guard is correct, not a bug.** `Refusing to overwrite … this task has not seen its full current content` fires when a `write_file` target was not freshly read in the current task. Do not work around it by reading only the first 50 lines — paginate the whole file with `offset`/`limit`, then write. Reading a snippet earlier in the conversation does NOT satisfy the guard.

- **Existing frontmatter is identity, not decoration.** A `compartment: A2H` or `loaded_at:` field in YAML frontmatter may be enforced by an external loader. Preserve it verbatim unless the task explicitly says to change identity metadata.

- **Footer HTML comments carry provenance, not litter.** Lines like `<!-- 2026-09-24: section removed by compression a602128, restored sha f3057f1a — SOUL.md owns it again -->` exist because the user tracks SHA-level edit history. Do not strip them as "noise"; they are the audit trail.

- **Pointer files are not live surfaces.** A common shape is: "AGENTS.md is a pointer to /root/AGENTS.md; load that for full doctrine." The pointer file is read by agents but its content rarely reaches runtime caches. Do not put governed rules in a pointer file — they will not fire.

- **Fossil names are not bugs.** When a YAML contract or config keeps both an old and a new value (e.g. `runtime_origin: KVM4` AND `authority_origin: KVM8` after a federation migration), the duplicate is provenance, not drift. F2 TRUTH = provenance. Do not "clean up" by deleting one.

- **`.bak.<timestamp>` siblings mean rotation in progress.** If `config.yaml` has 20 `.bak.*` siblings, an in-flight mutation is happening on a different lane. Hand-edit the active file only if you are the lane doing the rotation; otherwise wait or escalate.

- **A "verified command" requires a verified artifact.** "Build with `make build`" must come from a Makefile you read. "Test with `npm test`" must come from package.json. Inventing a command because it is "what projects usually do" is the most common drift source — and the quality bar explicitly bans it.

- **Markdown pitfall format = imperative + WHY.** A pitfall in a skill is `Rule + WHY (mechanism)`. Not a narrative. Not a date. Not a PR number. Future readers have no context — write the rule so it stands alone.

## Quality bar (mirror of the /init quality bar)

- **CONCISE** — target under 100 lines for AGENTS.md. Every line costs context for every agent every session.
- **Commands must be exact** — verified from manifests, not invented.
- **No generic advice** — "write tests" / "follow best practices" is banned.
- **Conventions must be observed** — naming, error handling, commit messages — only what the code shows.
- **Pitfalls are project-specific** — required env vars, generated files not to edit, slow tests, ports already in use. Skip the section if you found none.
- **Flat and scannable** — short title + one-paragraph overview, then focused sections. No deep nesting.

## Reference files

- `references/merge-templates.md` — concrete before/after merge examples for common shapes (frontmatter + footer; bare sections; no frontmatter at all).

## Related skills

- `forge-repo-intelligence` — read-only repo observation lane (census, drift, audit). Use when the task is "is this file accurate?" not "update this file".
- `forge-readme-truth-check` — README-vs-reality drift detector. Use when the project has a README-as-context but no AGENTS.md and you need to argue for one.
- `forge-cross-repo-doc-zen` (absorbed into `forge-repo-intelligence`) — federation-wide doc graph reconciliation. Use when many federations all need cross-references fixed at once.
- `forge-onboarding` — register a NEW agent identity. Different class entirely; do not confuse.

---

*DITEMPA BUKAN DIBERI ⚒️ — class-level skill for the Hermes /init merge-update workflow.*
