# ⚒️ FORGE-cross-repo-doc-zen — Federation Documentation Graph-Connect

> **Skill Class:** Meta · **Axis:** Cross-Repo · **ATLAS333:** P9 Layer/Collapse, P22 Unity/Diversity
> **FORGED:** 2026-07-20 by FORGE (000Ω) · **Supersedes:** ad-hoc per-repo cleanup

## USE WHEN
- Auditing documentation across multiple federation repos
- Finding orphan markdown files anywhere in the federation
- Fixing contradictory floor names or deprecated tool references
- Creating cross-repo documentation indexes
- Mapping docs to ATLAS333 cognitive geometry
- Reducing entropy in the documentation graph

## DO NOT USE WHEN
- Single-file edits (use native edit tools)
- Writing new documentation (use standard FORGE workflow)
- Code changes (use FORGE-code-analysis or standard tools)

## THE ZEN RULE
> **Delete the container, keep the signal.**
> Before archiving, extract eurekas. Before creating, measure entropy.

## WORKFLOW

### Phase 1: SCAN
```bash
# Count all MD files in a repo
find /root/<REPO> -name "*.md" -not -path "*/.git/*" -not -path "*/node_modules/*" | wc -l

# Find wrong floor names
grep -rn "F2.*Haqq\|F3.*Shahada\|F5.*Hikmah\|F6.*Adl\|F9.*Rahmah\|F4.*Nur" --include="*.md" /root/<REPO>/ -l

# Find deprecated tool names
grep -rn "arif_judge_deliberate\|arif_vault_seal\|arif_session_init\|arif_sense_observe\|arif_mind_reason\|arif_kernel_route\|arif_forge_execute" --include="*.md" /root/<REPO>/ -l
```

### Phase 2: FIX
```bash
# Fix floor names (batch sed)
sed -i \
  -e 's/F2.*Haqq/F2 TRUTH/g' \
  -e 's/F3.*Shahada/F3 WITNESS/g' \
  -e 's/F4.*Nur/F4 CLARITY/g' \
  -e 's/F5.*Hikmah/F5 WISDOM/g' \
  -e 's/F6.*Adl/F6 MARUAH/g' \
  -e 's/F9.*Rahmah/F9 ANTI-HANTU/g' \
  -e 's/F13.*Khalifah/F13 SOVEREIGN/g' \
  <files>

# Fix deprecated tool names
sed -i \
  -e 's/arif_judge_deliberate/arif_judge/g' \
  -e 's/arif_vault_seal/arif_seal/g' \
  -e 's/arif_session_init/arif_init/g' \
  -e 's/arif_sense_observe/arif_observe/g' \
  -e 's/arif_mind_reason/arif_think/g' \
  -e 's/arif_kernel_route/arif_route/g' \
  -e 's/arif_forge_execute/arif_forge/g' \
  <files>
```

### Phase 3: INDEX
Create `docs/README.md` with:
- Entry points (repo README, AGENTS.md, etc.)
- Cross-repo links to all 6 federation organs
- ATLAS333 paradox mapping
- Archive manifest (if any files archived)

### Phase 4: CROSS-LINK
- Wire top-level files into repo README
- Add cross-repo links between all federation organs
- Ensure ATLAS333_EVERGREEN.md is reachable from every repo
- Create WISDOM_DISTILLATION.md when archiving files

### Phase 5: VERIFY
```bash
# Verify no deprecated tool names remain
grep -rn "arif_judge_deliberate" --include="*.md" /root/<REPO>/ | grep -v archive | grep -v forge_work | grep -v memory

# Verify no wrong floor names remain
grep -rn "F2.*Haqq\|F3.*Shahada" --include="*.md" /root/<REPO>/ | grep -v archive

# Verify all repos clean
for r in arifOS A-FORGE AAA GEOX WEALTH WELL; do
  cd /root/$r && echo "$r: $(git status --porcelain | wc -l) dirty"
done
```

## CURRENT FLOOR CANON (DO NOT DEVIATE)
| F# | Name | Legacy (WRONG) |
|----|------|----------------|
| F1 | AMANAH | — |
| F2 | TRUTH | Haqq ❌ |
| F3 | WITNESS | Shahada ❌ |
| F4 | CLARITY | Nur ❌ |
| F5 | WISDOM | Hikmah ❌ |
| F6 | MARUAH | Adl ❌ |
| F7 | HUMILITY | Tawadu ❌ |
| F8 | PATIENCE | Sabr ❌ |
| F9 | ANTI-HANTU | Rahmah ❌ |
| F10 | ONTOLOGY | Ihsan ❌ |
| F11 | AUDIT | Aman ❌ |
| F12 | SECURITY | Hifz ❌ |
| F13 | SOVEREIGN | Khalifah ❌ |

## CURRENT CANONICAL TOOLS (DO NOT USE LEGACY NAMES)
| Current | Legacy (DEPRECATED) |
|---------|---------------------|
| `arif_init` | `arif_session_init` ❌ |
| `arif_observe` | `arif_sense_observe` ❌ |
| `arif_think` | `arif_mind_reason` ❌ |
| `arif_route` | `arif_kernel_route` ❌ |
| `arif_critique` | `arif_heart_critique` ❌ |
| `arif_judge` | `arif_judge_deliberate` ❌ |
| `arif_seal` | `arif_vault_seal` ❌ |
| `arif_forge` | `arif_forge_execute` ❌ |

## FEDERATION ORGAN MAP
| Organ | Port | Repo Path | Docs Index |
|-------|------|-----------|------------|
| arifOS | 8088 | /root/arifOS | arifOS/docs/README.md |
| A-FORGE | 7071 | /root/A-FORGE | A-FORGE/docs/README.md |
| AAA | 3001 | /root/AAA | AAA/docs/README.md |
| GEOX | 8081 | /root/GEOX | ⚠ PENDING |
| WEALTH | 18082 | /root/WEALTH | ⚠ PENDING |
| WELL | 18083 | /root/WELL | ⚠ PENDING |

---

*Forged: 2026-07-20 by FORGE (000Ω) · DITEMPA BUKAN DIBERI*
