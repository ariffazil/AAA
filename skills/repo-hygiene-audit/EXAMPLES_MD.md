# Repo Hygiene Audit — Examples

## Example 1: AAA Cleanup (2026-05-25)

**Repo:** `ariffazil/AAA`  
**Role:** control-plane  
**Depth:** deep

### Input
```
repo_path: /root/AAA
repo_role: control-plane
depth: deep
```

### Expected Findings
- Constitutional leak: `ROOT_CANON.yaml`, `arifos.init`, `.REPO_ROUTING_CONSTITUTION.md` at root
- Runtime debris: `hermes-workspace/` (40+ subdirs), `hermes-skills/` (79 dirs), `.apex/` (33 subdirs)
- Structural issue: `agent/` (singular) referenced in docs but actual dir is `agents/` (plural)
- Broken refs: `openclaw/a2a/bridge.yaml` referenced by validate script after `openclaw/` moved

### Expected Output
```markdown
## Skill Result: repo-hygiene-audit

### Summary
AAA has absorbed ~1.3GB of debris from agent workspaces, Hermes runtime,
and constitutional leaks. The repo structure has 100+ top-level items
instead of the expected 20-30 for a control plane.

### Authority Boundary
- [x] Leaks found: ROOT_CANON.yaml, arifos.init, arifOS-sentinel/

### Runtime Debris
- [x] Debris found: .apex/ (agent workspace), .codex/ (codex workspace),
  hermes-workspace/, hermes-skills/, hermes-backups/, hermes-config/,
  hermes-memories/, SEARAH/ (3MB PDFs), openclaw/ (runtime code)

### Structural Issues
- [x] Issues: README references `agent/` (singular) and `_00_META/` which do not exist

### Broken References
- [x] Broken refs: scripts/validate-aaa.mjs line 670 references archived `openclaw/a2a/bridge.yaml`

### Recommendations
1. Move constitutional leaks to `_archive/constitutional-leak/` — P0 — AAA agent
2. Move Hermes runtime to `_archive/hermes-runtime/` — P0 — AAA agent
3. Move agent workspaces to `_archive/agent-workspaces/` — P0 — AAA agent
4. Update validate script to reference `a2a/federation-bridge.yaml` — P1 — AAA agent
5. Update README directory structure — P1 — AAA agent
```

---

## Example 2: arifOS Quick Check

**Repo:** `ariffazil/arifOS`  
**Role:** kernel  
**Depth:** quick

### Expected Findings
- No constitutional leaks (this IS the kernel)
- Check for `arifos_mcp/` stub package collision with `arifosmcp/`
- Check for broken tests (`test_doctrine_diff_ci.py` imports missing module)

---

## Example 3: GEOX Standard Audit

**Repo:** `ariffazil/geox`  
**Role:** domain  
**Depth:** standard

### Expected Findings
- Verify `src/` is the canonical package root
- Check legacy shadow directories at root (`geox/`, `core/`, `engines/`)
- Verify no `arifos.init` or `ROOT_CANON.yaml` leaked
