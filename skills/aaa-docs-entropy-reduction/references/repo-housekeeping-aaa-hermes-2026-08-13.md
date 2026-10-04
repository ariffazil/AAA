# Repo Housekeeping: AAA + HERMES (2026-08-13)

> Agent: I-ARIF (subagent) · 2 repos · README truth-check, SoT drift, entropy audit, git commit+push

## What was done

Multi-repo housekeeping pass across `/root/AAA` and `/root/HERMES`:

1. **README SOT-MANIFEST drift** — verified `live_commit` and `last_verified` fields in the HTML comment block at the top of each README
2. **Stale prose count verification** — verified hardcoded counts like "31+ skills" against actual filesystem
3. **Entropy audit** — `.bak` file scan, `.gitignore` coverage check, broken/self-referential symlink detection
4. **Dependency check** — all README-referenced files exist, no broken relative links
5. **Git commit+push** — single atomic commit per repo with structured message

## Findings

### AAA (`a091b432` → pushed)

- **SOT-MANIFEST stale**: `live_commit: 59d79cae` but actual HEAD was `dc0d4df8` (3 commits stale). `last_verified` was 3 days old.
- **`.bak` entropy**: 11 untracked `.bak` files in active skills/ directories. Root cause: `.gitignore` had `*.bak-*` (timestamped) but not plain `*.bak`.
- **Fix**: Added `*.bak` to `.gitignore`. All 11 .bak files immediately excluded from staging.
- **Registries**: CAPABILITY_INDEX (261 tools), AGENT_MODEL_MAP, person-register — all modified with significant content additions. Committed as-is (registry sync).
- **No broken symlinks**, no missing referenced files.

### HERMES (`64b60b1` → pushed)

- **SOT-MANIFEST stale**: `live_commit: pending-push` (never updated after previous push). `last_verified` 3 days old.
- **Stale prose count**: README claimed "31+ skills" in two places (prose table + mermaid diagram). Actual: 428 SKILL.md files across 236 directories.
- **Self-referential symlink**: `mcp_servers/mcp_servers` → points to its own parent directory (`/root/HERMES/mcp_servers`). Infinite recursion risk.
- **Missing `.gitignore` patterns**: `.mcp-discovery.lock`, `SOUL.md.bak.*`, `MEMORY.md.bak.*`, `MEMORY.md.drift-backup` — all runtime artifacts not gitignored.
- **Dead symlinks**: `skills/primitives`, `skills/workflows` — deleted by previous operations, showing as `D` in git status.
- **Profile skill mirror**: 1151 files under `profiles/aaa-hermes/skills/` — legitimate skill copies, not duplicates. Committed.
- **No secret files staged**: verified `credential-health.sh` is a skill script, not actual credentials.

## Techniques

### SOT-MANIFEST drift detection

```bash
# Extract claimed commit from README HTML comment
head -20 README.md | grep -oP 'live_commit: \K[0-9a-f]+'
# Compare to actual HEAD
git rev-parse --short HEAD
```

The SOT-MANIFEST `live_commit` field is the single most stale item in federation READMEs. It's an HTML comment that nobody sees when browsing GitHub, so it silently rots.

### Stale prose count verification

```bash
# README says "31+ skills" — verify
find skills/ -name 'SKILL.md' -not -path '*/_retired/*' -not -path '*/.archive*' | wc -l
# Result: 428. Count in README was off by 13x.
```

Always check prose counts in both the main body AND diagrams (mermaid, ASCII art). The "31+ skills" appeared in a table cell AND in a mermaid node label — both needed updating.

### Self-referential symlink detection

```bash
# Find symlinks that resolve to their own parent directory
find . -type l -not -path '*/.git/*' | while read l; do
  target=$(readlink "$l")
  dir=$(dirname "$l")
  if [ "$(cd "$dir" && cd "$target" 2>/dev/null && pwd)" = "$(cd "$dir" && pwd)" ]; then
    echo "SELF-REF: $l -> $target"
  fi
done
```

Found: `mcp_servers/mcp_servers` → `mcp_servers` (its own parent). This is worse than a broken symlink because it doesn't show as broken — it silently creates infinite directory traversal.

### .gitignore coverage audit

```bash
# Find .bak files NOT in archive paths
find . -name '*.bak' -not -path '*/.git/*' -not -path '*/archive/*' -not -path '*/.archive*'
# Check if *.bak is in .gitignore
grep -q '^\*\.bak$' .gitignore && echo "COVERED" || echo "MISSING"
```

Pattern: `.gitignore` often has `*.bak-*` (timestamped backups from tools like `config.yaml.bak.20260801`) but misses plain `*.bak` (from manual `cp SKILL.md SKILL.md.bak`). Add `*.bak` as a catch-all.

## Pre-commit secret scan

Before `git add -A && git commit`, scan staged files for potential secrets:

```bash
git diff --cached --name-only | grep -iE '\.key$|\.pem$|secret|credential|password|token'
```

In this session: matched `credential-health.sh` (skill script, not secrets) and `FORGE-secret-hygiene/SKILL.md` (skill about secrets, not containing them). Both safe. Manual verification of grep hits is essential.

## Commit message pattern for housekeeping

```
housekeeping(<repo>): SOT drift fix, entropy cleanup, <specific fixes>

README:
- SOT-MANIFEST: update live_commit <hash>, last_verified <date>
- Fix stale <count> in prose: <old> → <new> (<actual> actual)

Entropy cleanup:
- <specific items removed/fixed>
- .gitignore: add <patterns>

<Other sections as relevant>

No .bak files tracked (entropy audit clean)
```
