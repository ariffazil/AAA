---
id: FORGE-cross-repo-doc-zen
name: FORGE-cross-repo-doc-zen
version: "2026.09.18"
description: >
  Audit and reconcile documentation across federation repositories, preserving
  canonical signals while removing stale references and graph fragmentation.
  Covers floor names, deprecated tools, and organizational role/topology drift.
owner: AAA
risk_tier: medium
autonomy_tier: T2
floor_scope:
  - F1
  - F2
  - F4
  - F11
---
# FORGE-cross-repo-doc-zen — Federation Documentation Graph-Connect

> **Skill Class:** Meta · **Axis:** Cross-Repo · **ATLAS333:** P9 Layer/Collapse, P22 Unity/Diversity
> **FORGED:** 2026-07-20 by FORGE (000Ω) · **Updated:** 2026-09-18 (topology drift class)

## USE WHEN
- Auditing documentation across multiple federation repos
- Finding orphan markdown files anywhere in the federation
- Fixing contradictory floor names or deprecated tool references
- Creating cross-repo documentation indexes
- Mapping docs to ATLAS333 cognitive geometry
- Reducing entropy in the documentation graph
- Fixing organizational role or topology claims that disagree across repos

## THE ZEN RULE
> **Delete the container, keep the signal.**
> Before archiving, extract eurekas. Before creating, measure entropy.

## CANONICAL SOT — Organ Registry

**ALL repo paths and ports come from `/root/AAA/federation/organs.yaml`.** Never hardcode them.

```bash
# Discover organ topology
python3 -c "
import yaml
with open('/root/AAA/federation/organs.yaml') as f:
    reg = yaml.safe_load(f)
for o in reg.get('organs', []):
    src = o.get('source_path', '')
    port = o.get('port', '')
    print(f'{o[\"id\"]:12s} src={src:20s} port={port}')
"
```

## WORKFLOW

### Phase 1: SCAN (per organ — paths from registry)

```bash
# Count MD files in an organ's source_path
ORG_PATH=$(python3 -c "import yaml;r=yaml.safe_load(open('/root/AAA/federation/organs.yaml'));print([o['source_path'] for o in r['organs'] if o['id']=='<ORGAN_ID>'][0])")
find "$ORG_PATH" -name "*.md" -not -path "*/.git/*" -not -path "*/node_modules/*" | wc -l

# Find wrong floor names
grep -rn "F2.*Haqq\|F3.*Shahada\|F5.*Hikmah\|F6.*Adl\|F9.*Rahmah\|F4.*Nur" --include="*.md" "$ORG_PATH" -l

# Find deprecated tool names
grep -rn "arif_judge_deliberate\|arif_vault_seal\|arif_session_init\|arif_sense_observe\|arif_mind_reason\|arif_kernel_route\|arif_forge_execute" --include="*.md" "$ORG_PATH" -l
```

### Phase 2: TOPOLOGY DRIFT SCAN

**When an external research document or cross-repo audit claims a role for a component, verify against AAA taxonomy before accepting.**

```bash
# Find all files claiming an organ number ("organ X of Y") across federation repos
for d in /root/{arifOS,AAA,A-FORGE,HERMES,GEOX,WEALTH,WELL,arifFlow}; do
  [ -d "$d" ] && grep -rn "organ [0-9] of [0-9]" --include="*.md" "$d" 2>/dev/null
done

# Find all role descriptions for a specific component (e.g., HERMES)
for d in /root/{arifOS,AAA,A-FORGE,HERMES,GEOX,WEALTH,WELL,arifFlow}; do
  [ -d "$d" ] && grep -rn -i "HERMES.*organ\|HERMES.*tier\|HERMES.*role\|HERMES.*bridge" --include="*.md" "$d" 2>/dev/null
done

# Find SOT manifests that embed role claims (lines 1-15 of READMEs)
for d in /root/{arifOS,AAA,A-FORGE,HERMES,GEOX,WEALTH,WELL,arifFlow}; do
  [ -d "$d" ] && head -15 "$d/README.md" 2>/dev/null | grep -n "role:\|organ:\|tier:"
done
```

**Drift classes to detect:**
- Conflicting organ numbers ("7 of 8" vs "8 of 8" vs actual count)
- Role claims that disagree with AAA taxonomy (constitutional organ vs interface)
- SOT manifests with stale dates or commit hashes
- README descriptions that reference deprecated topology

### Phase 3: FIX
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

**Topology drift fix pattern:**
1. Determine the canonical role from AAA taxonomy (Tier 1 = core runtime, Tier 3 = federation interface, etc.)
2. Update the SOT manifest `role:` field in the component's README
3. Update the `federation_release:` and `last_verified:` dates
4. Add a `topology_note:` if the role is non-obvious (e.g., "NOT a constitutional organ")
5. Do NOT touch quarantine or archived copies — they are frozen snapshots

### Phase 4: VERIFY (per organ from registry)

```bash
# Derive organ source_path from registry for each organ ID
# Verify no deprecated tool names remain
grep -rn "arif_judge_deliberate" --include="*.md" "$ORG_PATH" | grep -v archive | grep -v forge_work | grep -v memory

# Verify no wrong floor names remain
grep -rn "F2.*Haqq\|F3.*Shahada" --include="*.md" "$ORG_PATH" | grep -v archive

# Verify no stale organ numbers remain
grep -rn "organ [0-9] of [0-9]" --include="*.md" "$ORG_PATH" | grep -v archive | grep -v quarantine

# Verify all repos clean
python3 -c "
import yaml, subprocess
with open('/root/AAA/federation/organs.yaml') as f:
    reg = yaml.safe_load(f)
for o in reg.get('organs', []):
    src = o.get('source_path', '')
    if not src: continue
    r = subprocess.run(['git', '-C', src, 'status', '--porcelain'], capture_output=True, text=True)
    dirty = len(r.stdout.strip().split('\n')) if r.stdout.strip() else 0
    print(f'{o[\"id\"]}: {dirty} dirty files')
"
```

## CURRENT FLOOR CANON (DO NOT DEVIATE)

Floor names are authoritative at `/root/arifOS/GENESIS/FLOOR_TABLE.json`. Read from there.

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

## FEDERATION ORGAN MAP (EXAMPLE — probe registry for truth)

| Organ | Port | Repo Path | 
|-------|------|-----------|
| arifOS | from registry | from registry |
| A-FORGE | from registry | from registry |
| AAA | from registry | from registry |
| GEOX | from registry | from registry |
| WEALTH | from registry | from registry |
| WELL | from registry | from registry |

**Rule:** The table above is illustrative. The organ registry at `/root/AAA/federation/organs.yaml` is authoritative. Ports and paths change — this file does NOT.

## PITFALLS

- **Do not fix quarantine or archived copies.** They are frozen snapshots used for comparison. Fixing them destroys the baseline you audit against.
- **Do not change SOT manifest commit hashes by hand.** The `live_commit` field reflects `git log --oneline -1`. Use `git log` to get the real hash, or update it via the automated `scripts/update_readme_sot.py`.
- **Topology drift is constitutional, not cosmetic.** If a component's README says "organ 8 of 8" but AAA classifies it as Tier 3 Federation Interface, that is a governance disagreement — escalate to F13 if the role assignment is contested, do not just rewrite the README unilaterally.
- **External research documents are hypotheses, not canon.** Probe every factual claim (version numbers, file locations, service status) against live system state before accepting. The architecture may be sound even when specific facts are wrong.

---
*Forged: 2026-07-20 by FORGE (000Ω) · De-hardcoded: 2026-08-06 · Topology drift class: 2026-09-18 · DITEMPA BUKAN DIBERI*
