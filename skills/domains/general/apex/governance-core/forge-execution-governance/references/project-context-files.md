# Project Context Files

Hermes injects project-level instructions into the system prompt by reading context files from the working directory. The discovery order is **first match wins** — only one project context source is loaded per session.

| File (in priority order) | Discovery | Use when |
|---|---|---|
| `.hermes.md` / `HERMES.md` | Walks parents up to the git root, stops at git root | You want hierarchical project rules (root + per-package overrides) |
| `AGENTS.md` / `agents.md` | **Cwd only** — subdirectory and parent copies are ignored | You want portable agent instructions that work the same in Hermes, Claude Code, Codex, etc. |
| `CLAUDE.md` / `claude.md` | Cwd only | Same as AGENTS.md, Claude-flavored |
| `.cursorrules` / `.cursor/rules/*.mdc` | Cwd only | Migrating from Cursor |

`SOUL.md` (in `$HERMES_HOME`) is independent and always loaded when present — it sets the agent's identity, not project rules.

### Pick the right one

- **Use `.hermes.md`** when you want Hermes-specific behavior that lives above the cwd (root + subtree), or when you want rules to inherit from a parent directory. The parent walk stops at the git root, so a home-level `.hermes.md` won't leak into every project (a git repo's root is the boundary).
- **Use `AGENTS.md`** when the same project will also be worked on by other agents (Codex, Claude Code, OpenCode). Those tools all have their own conventions for `AGENTS.md`, and the "cwd only" contract keeps the file portable.
- **Don't put project rules in `~/.hermes/AGENTS.md`** (or any other home-level location). When Hermes runs with that directory as cwd, the file loads — but only for that one directory. For cross-project context, use `SOUL.md` (in `$HERMES_HOME`, identity-only) or install a skill via `hermes skills install`.

### Size and truncation

Each context file is capped at 20,000 characters. Files longer than that get **head + tail** truncated (the middle is dropped, with a `[...truncated...]` marker). For large project rules, prefer splitting into multiple skills over cramming one file.

### Security

All context files pass through the threat-pattern scanner before reaching the system prompt. Patterns matching prompt injection or promptware are replaced with a `[BLOCKED: ...]` placeholder. This means an `AGENTS.md` containing obvious injection attempts won't reach the model — the scanner blocks the content, not the file, so the rest of the file still loads.

### Disable for one session

`hermes --ignore-rules` skips auto-injection of all project context files (`.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`) **and** `SOUL.md` identity, plus user config, plugins, and MCP servers. Use it to isolate whether a problem is your setup or Hermes itself.

### Example: a small `.hermes.md`

```markdown
# My Project

Hermes: when working in this repo, follow these rules.

## Build
- Always run `make test` before declaring a change done.
- Use `uv run` for Python, not `pip install`.

## Style
- Prefer `pathlib.Path` over `os.path`.
- No `print()` in production code — use the `logger`.
```

That file at `/home/me/projects/myrepo/.hermes.md` is auto-loaded when Hermes runs in any subdirectory of `/home/me/projects/myrepo`, but not when it runs in `/home/me/other-project`.

---

# Doctrine coverage sweep across agent harnesses

A clause that must be in force for every agent exists in one copy per harness: the CLI's own runtime
config, and often a second federation overlay copy under the agent-overlay tree. Both load, and some
harnesses read a `SYSTEM.md` or `instructions.md` rather than an `AGENTS.md`. **Enumerate the set from disk
on every audit — a hardcoded inventory of which file belongs to which harness is itself a claim, and it goes
stale the first time a harness is added or renamed.**

```bash
# 1. Discover the boot-file set from disk (bounded depth, exclude dependency trees)
find /root -maxdepth 3 \( -name AGENTS.md -o -name CLAUDE.md -o -name SYSTEM.md -o -name instructions.md \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' | sort

# 2. Coverage per file — existence tested SEPARATELY from the marker grep
for f in <the discovered list>; do
  if [ -f "$f" ]; then printf '%-56s %s\n' "$f" "$(grep -c '<CLAUSE MARKER>' "$f")"
  else printf '%-56s MISSING_FILE\n' "$f"; fi
done

# 3. Numerator and denominator, printed together
have=$(grep -l '<CLAUSE MARKER>' <list> 2>/dev/null | wc -l); need=<n>
```

## Rules that decide whether the sweep is evidence or decoration

- **`grep -c` returns 0 for a missing file and 0 for an existing file without the clause — indistinguishable
in a loop.** Test existence separately, or a shrinking denominator silently reports as full coverage.
Always print the denominator next to the numerator.
- **Choose a stable literal heading as the clause marker**, not a sentence from the clause body, so the check
stays a one-line grep after the wording is revised. A paraphrase anywhere in the estate drops out of the
count — text written for a new harness must be **copied verbatim**.
- **Generated files revert on the next render.** Fragments compose whole files; a hand-append to a generated
artifact disappears with no error. Edit the fragment or the generator's target list, re-render, then confirm
idempotency (a second render reports unchanged).
- **The health script is the tripwire.** Wire the numerator/denominator equality into the check set that runs
on every audit, so a newly added harness surfaces as a failure instead of as silence.
- **Text coverage is not enforcement.** These files declare the rule; they cannot block anything. Report the
separate existence check for any mechanical gate (the harness's own hook listing, a gate module, a hook
directory) before describing an agent estate as unable to do something.
