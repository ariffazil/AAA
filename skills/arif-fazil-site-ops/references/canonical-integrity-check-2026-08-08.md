# Canonical Integrity Check — 2026-08-08 (session reference)

## What this is

A full-scope audit of every repo under `/root/` against `web-canon/canon/federation.json` assets list and `web-canon/canon/sites.yaml` surfaces list. Produces a list of (a) layer drift, (b) L4 archive discipline, (c) deltas (repos missing from canon).

Triggered by Arif: *"Keputusan: Option 3"* + EMD's canon-integrity-check.

## Audit recipe (reusable)

```bash
# 1. Pull GitHub repo list
gh repo list ariffazil --limit 50 --json name,description,isArchived,createdAt,updatedAt 2>&1 | head -50

# 2. Read canonical registries
cat /root/web-canon/canon/federation.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d['assets'], indent=2))"
cat /root/web-canon/canon/sites.yaml | head -5
cat /root/web-canon/canon/sites.yaml | tail -15

# 3. Diff GitHub vs canon
# For each repo: check github → does it have an [Lx] tag? is it in federation.json? is it in sites.yaml?
# Report: repo name, layer tag, creation date, delta status

# 4. Check for undeclared runtime services
for repo in <list>; do
  systemctl is-active "$repo-organ.service" 2>/dev/null && echo "RUNNING: $repo"
  grep -rn "Wants=$repo" /etc/systemd/system/*.service 2>/dev/null
done
```

## Findings (2026-08-08)

| Repo | Canon | Layer | Issue |
|---|---|---|---|
| FRAME | ❌ unregistered | — | Live service (frame-organ.service, 127.0.0.1:18085), Wants arifos+aforge, reads kunci-mas.flat.env. **F1 violation** until registered. |
| syedos | ❌ in federation.json but NOT in sites.yaml | L3 | Live VHost at syedos.arif-fazil.com. Needed both registries. Also had APEX name collision with archived ariffazil/APEX. |
| compose | L3 ASSET | L3 | Contains only sekrits/ — dead drop. Quarantined. |
| searxng | L3 ASSET | — | Docker container, not a git repo. Config in A-FORGE/deploy/searxng/. Live but not version-controlled. |
| arifOS-model-registry | L3 ASSET | L3 | Dormant data repo. No issues. |
| ariffazil (profile) | L3 ASSET | L3 | Identity root. No issues. |

## Resolution applied

1. **FRAME** registered in `federation.json` as L3 ASSET, COMPUTE_ONLY, port 18085, T2 restart-needs-888-SEAL. NOT a sovereign organ.
2. **syedos** added to `sites.yaml` surfaces list with VHost metadata. APEX renamed to GOLD in llms.txt (name collision cleared).
3. **compose** quarantined → `/root/_quarantine_compose_20260807/`.
4. `navigation.json` v7 drift left untouched (sibling's PR cycle, not blocking).

## Lesson

Two registry systems (federation.json + sites.yaml) exist for the same reason two ledgers exist in accounting: one tracks what lives (federation.json = assets), one tracks where it appears (sites.yaml = surfaces). A surface (syedos) can be registered in one and absent from the other, creating a partial-truth state. Always check BOTH registries when registering a new path or asset.
