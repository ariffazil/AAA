# Worked Example: Canon Audit 2026-08-07/08

DATE: 2026-08-08

## Audit scope
EMD/Gemini external audit of 29 repos under ariffazil vs web-canon.

## What EMD found (initial claims)
- 6 L3 assets "absent from all canon registries" (searxng, A2B, EEE, compose, arifOS-model-registry, ariffazil)
- HERMES posture drift (REFLECT_ONLY vs live gateway)
- FRAME = undeclared organ, F12 injection concern
- syedos = undeclared live surface, APEX name collision

## What probe revealed

### 6 "deltas" = ALL Class 4 (ghost audit premise)
```python
# federation.json schema uses {asset: "x"} not {id: "x"}
for a in d['assets']:
    print(a.get('asset'), '|', a.get('github').split('/')[-1] if a.get('github') else '?', '|', a.get('posture', '?'))
# All 6 repos present — auditor was looking for wrong key
```

| Auditor claim | Schema key auditor used | Actual registry key | Delta real? |
|---|---|---|---|
| "arifOS-model-registry absent" | `id` | `asset` | No — present |
| "searxng absent" | `id` | `asset` | No — present |
| "compose absent" | `id` | `asset` | No — present |
| "EEE absent" | `id` | `asset` | No — present |
| "A2B absent" | `id` | `asset` | No — present |
| "ariffazil absent" | `id` | `asset` | No — present |

### HERMES posture drift = CONFIRMED (Class 2)
sites.yaml had: `posture: REFLECT_ONLY, deployable: false, port: 8644`
Live reality: `posture: LIVE, deployable: true, port: 18089`
Fix: `git diff` + commit + push branch → PR.

### FRAME = CONFIRMED undeclared organ (Class 1)
- systemd unit: frame-organ.service (port 18085, 7 chambers, running 24h+)
- source at /root/FRAME (recovered from quarantine)
- was NOT in federation.json `organs[]` (was in `assets[]` by sibling agent)
- Fix: added to `organs[]` with L1 classification, deduplicated from assets[]

### syedos = Already declared (Class 4)
Already in federation.json as `{asset: "syedos", role: "sovereign_dashboard"}`
Doctrine extended with APEX-name-collision note.

## Commits shipped
- `91ceb09` fix(canon): HERMES posture — REFLECT_ONLY → LIVE
- `8105d22` fix(canon): FRAME L1 organ registration + syedos APEX collision note

## Key lesson
Always probe the registry schema before computing deltas. One `python3`
command saved this session from shipping 6 phantom registrations.