# TOOLS.md — opencode Agent

## Allowed Tools

### File Operations
- `read` — read file contents
- `write` — create/overwrite file
- `edit` — surgical string replacement
- `glob` — find files by pattern
- `grep` — search file contents

### Git Operations
- `bash git status` — working tree state
- `bash git diff` — staged/unstaged changes
- `bash git log` — commit history
- `bash git add/commit/push` — with approval

### Shell Operations
- `bash` — execute commands (T2+ approval)
- `npm/pip/uv` — package management
- `make` — build targets

### MCP Surfaces
- `arifOS kernel` — constitutional judgment (SEAL/SABAR/VOID)
- `GEOX` — Earth-domain grounding (when topic requires)

### Formatters & Linters
- `black` — Python formatting
- `ruff` — Python linting
- `mypy` — Python type checking
- `eslint` — JS/TS linting
- `prettier` — general formatting

## Prohibited Tools

- `eval()` or `exec()` with user-provided strings
- `rm -rf` without explicit human approval
- `docker system prune` — NEVER without 888_HOLD
- Any tool that bypasses arifOS constitutional floors

## Tool Configuration

**Formatter:** black with `--line-length=100`
**Linter:** ruff with `--line-length=100`
**Type checker:** mypy with strict mode

---

*Last updated: 2026-04-29*
