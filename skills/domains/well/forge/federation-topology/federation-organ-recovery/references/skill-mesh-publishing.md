# Skill Mesh Publishing — Served Root vs Live Mesh

> The arifOS kernel serves skills from `ARIFOS_SKILL_ROOT` (production: `/etc/arifos/skills`).
> This directory is a **snapshot**, not a live view. It drifts from the live mesh
> (`/root/AAA/skills`) as skills are added, renamed, or pruned.

## The Drift Pattern

Measured 2026-09-19: served root held 155 skills; live mesh held 555. 428 skills were
unreachable over `skill://`. 9 entries were symlinks resolving out of the root (kernel's
traversal guard correctly refused them).

## The Publishing Tool

`/root/scripts/publish_skills.py` augments the served root from the live mesh.

Design rules (each learned from a failure):
1. **AUGMENT, never replace.** The served root also carries skills from outside the mesh
   (e.g. `/root/.understand-anything/...`). A rebuild would silently drop them.
2. **COPY, never symlink.** The kernel guard resolves the path and requires it under the
   root; a symlink out of root is refused by design.
3. **Name = the skill directory's own basename**, so nested taxonomy skills
   (`substrate/audit-seal`) answer at `skill://audit-seal/SKILL.md`.
4. **Harness overlay dirs are not skills** (`claude/`, `openai/`, `kimi/`, `qwen/`, …).
5. **Collisions are reported, never resolved silently.**
6. **Never overwrite an entry that already resolves.** Gaps filled, breaks repaired.

## Usage

```bash
# Dry run (always first)
python3 /root/scripts/publish_skills.py --json

# Apply
python3 /root/scripts/publish_skills.py --apply
```

## Open Debt

The served root is still a copy, not a view. Skills added to the mesh are invisible over
MCP until `publish_skills.py` runs. The fix is a trigger (timer or post-commit hook), which
is not yet built.

## See Also

- `skill://index` — the kernel's skill directory resource (now returns names + descriptions,
  not just counts — fixed 2026-09-19, commit `4b4c7c89d`)
- `/root/arifOS/arifosmcp/resources/namespace_index.py` — the kernel code that serves
  `skill://index`
