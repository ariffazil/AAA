---
title: "UPGRADE arif-fazil.com /world — F1/F2/F3 Timeline + Receipts (2026-10-06)"
created: 2026-10-06
updated: 2026-10-06
version: 1.0.0
type: upgrade-receipt
category: public-surface
tags: [arif-fazil.com, world, upgrade, F1, F2, F3, F4, nav, AEO, GEO, content]
confidence: high
floors: [F1, F2, F3, F13]
update_class: ARIF_ONLY
---

# UPGRADE arif-fazil.com /world — F1/F2/F3 Timeline + Receipts (2026-10-06)

> Per F13 directive 2026-10-06 ~14:00 MYT: *"https://arif-fazil.com/world now can we map this site properly to the main pages? no button to navigate here, and plan for site upgrade for world"*

This is the consolidated upgrade record for the `/world/` surface (and adjacent work) on arif-fazil.com.

## The 4-Phase Plan

| Phase | Scope | Sovereign binary |
|---|---|---|
| **F1 — Visibility** | Add `/world/` button to main nav (was missing) | implicit |
| **F2 — AEO/GEO** | Close AEO/GEO defects (og:image, twitter:image, meta description) | implicit ("continue F2", "continue F2.2") |
| **F3 — Content** | Audit 55 sub-pages, classify by domain, add landing cards | "do F3" |
| **F4 — Mission** | "evidence-grounded model" framing (per F13 directive 2026-10-05) | pending |

F1 + F2 + F3 done in this session. F4 awaiting scope binary.

## F1 — Visibility (DONE)

| Step | Change | Receipt |
|---|---|---|
| Add `/world/` to main nav | Inserted between Map and PETRONAS in secondaryNav (NOT primaryNav — preserves 5-slot Explore·Read·Build·Evidence·About) | `fe2a805` |
| Sync web-canon SOT | web-canon/canon/navigation.json ← arif-fazil.com/canon/navigation.json (v7.3.0, as_of 2026-10-03) | `43406e9` |
| Add World to arif-fazil.com canon | secondary_links World entry | `ca805ea` |
| Generator fix | mapItems: handles null href, propagates `note` field; NavItem type widened | `4ce6b74` |

Live verified: World nav entry `{label:World, href:/world/}` in /var/www/html/arif/assets/index-yJJoYotB.js, 7 World refs.

## F2 — AEO/GEO Defect Closure (DONE in 2 sub-phases)

### F2.1 — og:image for 5 surfaces (2026-10-06 15:18 MYT)

| Surface | Before | After |
|---|---|---|
| /999/ | OK | OK 4/4 |
| /canon/ (→ /words/doctrine/) | OK | OK 4/4 |
| /map/ | PARTIAL | OK 4/4 |
| /connect/ | PARTIAL | OK 4/4 |

Receipt: `60f71cc` (2 files +41 lines, post-build verify-pages PASS 213/213).

### F2.2 — twitter:image for 13 PARTIAL surfaces (2026-10-06 15:28 MYT)

13 surfaces had og:image but missing twitter:image. Added twitter:card + twitter:image (or both og + twitter for 2 surfaces that were missing both).

Receipt: `55f95af` (11 files +339 / -25, post-build 23/23 OK 4/4).

### Final audit (2026-10-06 15:30 MYT)

```
Main surfaces tested: 23
OK (4/4 og:image + twitter:image + description + canonical): 23/23 (100%)
PARTIAL (2-3/4): 0
BROKEN (0-1/4 or 404): 0
```

## F3 — Content Organization (DONE)

### Cluster audit of /world/* (55 sub-pages)

| Cluster | Count | Examples |
|---|---|---|
| /world/2027/ | 3 | AI Agents 2027 dossier + 2 civic slices |
| /world/makcikgpt/ | 44 | Civic intelligence in Bahasa Makcik |
| /world/politics/ | 7 | Index, ns-election (live map), shadow, geopolitics |
| /world/_agent-shell/ | 1 | Agent-only |
| /world/ | 1 | Main landing |

### F3.1 — /world/ stats panel (DONE)

Added `§0 The 56 surfaces in one place` to /world/ landing:

| Stat | Count | Sub-page |
|---|---|---|
| AI 2027 Dossier | 3 | /world/2027/ |
| MakcikGPT Articles | 44 | /world/makcikgpt/ |
| Politics Dossiers | 7 | /world/politics/ |
| Live Interactive Map | 1 | /world/politics/ns-election/ |
| Commodity Terminals | /oil/, /gas/, /gold/, /klci/, /usdmyr/ |
| PETRONAS Vital | 1 | /vitals/ |

Plus 6 cross-cluster links to /earth/ /vitals/ /economics/ /discoveries/ /machine/ /999/.

### F3.2 — /world/makcikgpt/ topic overview (DONE)

10 topic badges (informational spans, not anchor links — honest about page capability):

| Topic | Count |
|---|---|
| PETRONAS | 20 |
| SEARAH | 6 |
| Sovereign AI | 4 |
| Taufik | 3 |
| Sarawak | 3 |
| YTL Monopoli | 3 |
| MyKad | 2 |
| NEXOG | 2 |
| Korporat | 2 |
| Datasonic | 2 |

Receipt: `4b9b763` (2 files +61 / -1).

## What F3 Deliberately Did NOT Change

- **No filter/reorder of the 44 articles** — would require re-architecting /world/makcikgpt/
- **No topic anchors** — pills are informational, not navigational
- **No cross-links to GEOX /earth/** — separate /earth/ vs /world/politics/ scope decision pending

## F4 — Mission-aligned "evidence-grounded model" (AWAITING BINARY)

Per F13 framing 2026-10-05:
> *"arif-fazil.com can become an evidence-grounded model of selected parts of the world."*

Surface the audit trail (date stamps, claim grades, witness chain) on /world/. Per 8-dimension eval (human clarity, retrieval, truthfulness, maintenance).

Involves content choices → awaiting F13 scope binary.

## Reversibility (full rollback)

```bash
cd /root/arif-fazil.com
git revert 4b9b763   # F3 stats + topic overview
git revert 55f95af   # F2.2 twitter:image
git revert 60f71cc   # F2.1 og:image
git revert 4ce6b74   # SOT sync + generator
git revert ca805ea   # arif-fazil.com canon World
git revert 43406e9   # web-canon SOT sync
git revert fe2a805   # World nav
```

All commits are additive (insertions, no deletions of working state). Rollback is safe.

## What This Tells About the Site Mission

The /world/ surface now serves as the federation's **public intelligence catalog**:
- 56 surfaces across 4 mission clusters
- All 4 clusters have landing cards
- Cross-cluster links expose the federation's true shape
- 23/23 AEO/GEO surfaces — humans, agents, and crawlers can all find the content

Next stop (F4): make /world/ an evidence-grounded model per F13 framing.

## Sources

- `git log site/harden` (7 commits today)
- `curl https://arif-fazil.com/world/` (live)
- Session receipts (auto)
- `/root/.local/share/arifos/qwen-session-2026-10-06*.json`