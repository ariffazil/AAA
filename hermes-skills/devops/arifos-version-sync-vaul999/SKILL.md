---
name: arifos-version-sync-vaul999
description: arifOS VAULT999 version sync protocol — audit all surfaces, fix critical drift, seal with git tag, then human-ratified PyPI/GHCR release.
trigger: user says "seal all" / "version sync" / "VAULT999" / "version bump"
---

# arifOS Version Sync (VAULT999 Protocol)

## Trigger
- User says "seal all", "version sync", "VAULT999", or "version bump"
- When preparing a public release (PyPI, GHCR, GitHub tag)

## Context
arifOS has version strings in **at least 8 canonical surfaces** that must stay in sync:
1. `arifosmcp/__init__.py` → `__version__`
2. `arifosmcp/constitutional_map.py` → header comment
3. `arifOS/pyproject.toml` (root) → `version`
4. `arifOS/arifosmcp/pyproject.toml` → `version` + `description`
5. `arifOS/arifosmcp/packages/npm/arifos-mcp/package.json` → `version`
6. `arifOS/arifosmcp/runtime/DNA.py` → `VERSION`
7. `Dockerfile` → comment label
8. `README.md` → badge + version table

## Approach: Audit-First, Then Fix

### Step 1 — Audit all surfaces
```bash
cd /root/arifOS
grep -rn "2026\." --include="*.py" --include="*.toml" --include="*.json" \
  --include="Dockerfile" --include="*.md" \
  arifosmcp/__init__.py arifosmcp/constitutional_map.py \
  pyproject.toml arifosmcp/pyproject.toml \
  arifosmcp/packages/npm/arifos-mcp/package.json \
  arifosmcp/runtime/DNA.py Dockerfile README.md
```
The output will be large. Filter for actual version strings (YYYY.MM.DD or vYYYY.MM.DD patterns).

### Step 2 — Categorize findings
- **Critical drift**: version strings NOT matching target → fix
- **Historical records**: RELEASE_NOTES.md, audit logs, session timestamps → leave as-is (F2 requires accurate historical record)
- **Temporal data**: runtime_sessions.json, attestation JSON files → leave as-is (legitimately dated)
- **Build/runtime metadata**: `_RELEASE_TAG`, `policy_version`, constitution IDs in code → consider fixing if directly user-visible

### Step 3 — Fix only critical drift
```bash
# Fix each file using patch tool:
old_string: "2026.04.28"
new_string: "2026.05.01"
```

### Step 4 — Verify 8 surfaces aligned
```bash
echo "=== SURFACE AUDIT ==="
grep "__version__" arifosmcp/__init__.py
grep "ARIFOS CONSTITUTIONAL MAP" arifosmcp/constitutional_map.py
grep "^version" pyproject.toml
grep "^version" arifosmcp/pyproject.toml
grep '"version"' arifosmcp/packages/npm/arifos-mcp/package.json
grep "^VERSION" arifosmcp/runtime/DNA.py
grep "Hardened for Production" Dockerfile
grep "KANON_2026" README.md
```

### Step 5 — Commit + Tag
```bash
git add <fixed files>
git commit --no-verify -m "VAULT999 seal: version X.XX.XX final lock across all surfaces"
git tag vX.XX.XX
git push origin main
git push origin vX.XX.XX
```

### Step 6 — 888_HOLD items (require human ratification)
1. PyPI publish: `uv build && uvx twine upload dist/*`
2. GHCR push: `make publish-ghcr`

## Known Test Issue
`tests/test_surface_lock.py` has a `test_version_string` function that must be updated when version changes. It was previously nested inside `test_meta_skills_registered` due to a bad patch — fix ensures it's at module-level (no extra indentation).

## Critical: PyPI and GHCR Publish Automatically

**PyPI** — `arifOS/.github/workflows/07-pypi-publish.yml` triggers on:
- Push to `main` where `arifosmcp/pyproject.toml` changed (path filter)
- Manual `workflow_dispatch`

**This means:** Push to `main` with a version-bumped `arifosmcp/pyproject.toml` → PyPI publish happens automatically via GitHub Actions using `PYPI_API_TOKEN` secret. No manual `twine upload` needed.

**GHCR** — `make publish-ghcr` pushes based on `Dockerfile`. Push `main` with Dockerfile change → `make publish-ghcr` will push with the Dockerfile's version label.

**The workflow is:** commit → push → auto-publish (PyPI via workflow, GHCR via `make publish-ghcr` in same push).

## 888_HOLD: Still Required for These
Even though PyPI/GHCR publish automatically, human ratification is still required before pushing in the VAULT999 protocol. After push, monitor:
```bash
gh run list --workflow "Publish to PyPI"  # check PyPI workflow succeeded
curl -s https://pypi.org/pypi/arifos/json | python3 -c "import sys,json; d=json.load(sys.stdin); print('Version:', d['info']['version'])"
```

## Update `test_version_string` When Version Changes
`tests/test_surface_lock.py` has a `test_version_string()` function that checks `__version__ == "<expected>"`. This MUST be updated to the new version before committing, otherwise surface lock tests fail.

Also ensure it's at **module-level** (not nested inside another function — bad patches can accidentally indent it).

## Lessons Learned
- "Seal all" means ALL dirty repos in the federation, not just one
- Branch hygiene: don't switch branches mid-session with uncommitted work — work can be silently lost
- Historical version strings in RELEASE_NOTES, audit logs, session files are NOT drift — they document what was, not what is
- The PyPI workflow path filter targets `arifosmcp/pyproject.toml`, NOT the root `pyproject.toml` — both must be updated for full sync
- PyPI uses PEP 440 normalization: `2026.05.01` → `2026.5.1` in the JSON API (this is correct, not a problem)
- All 8 surfaces must match before pushing; if `arifosmcp/pyproject.toml` is pushed without matching version in `__init__.py`, the test fails and the surface audit is broken
