# GitHub skill aliases — archived 2026-10-19 (single-door consolidation)

These six names were symlinks to `github-ops`. They resolved to the same SKILL.md but
appeared as six separate skills in every harness picker, which taught agents that there
were six procedures. There is one.

Canonical skill: `/root/AAA/skills/github/github-ops/SKILL.md` (v3.0.0, INIT → DEPLOY).

Restore (only if a harness config hard-codes an old name):
    ln -s github-ops /root/AAA/skills/github/<name>

Do not restore all six. Add the old name to `aliases:` in the canonical frontmatter instead.
