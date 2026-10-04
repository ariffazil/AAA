# 5-Page Artifact Fit Map — all content has a home

**Locked 2026-08-06.** Every artifact on arif-fazil.com must live under one of
the 5 top-level pages. No orphans. No root-dangling routes.

## The 5 homes

| # | Nav | Home URL | Content type | Organ |
|---|-----|----------|-------------|-------|
| 1 | HOME | `/` | identity, cockpit, portfolio | AAA |
| 2 | EARTH | `/earth` | geology, seismic, basins, wells | GEOX |
| 3 | WORDS | `/writing` | essays, doctrine, law, MakcikGPT | arifOS |
| 4 | WORLD | `/world` | commodities, vitals, politics, organs portal | WEALTH |
| 5 | WORK | `/missions` | exploration wells, missions, resume | WELL |

## Current artifact → home mapping (verified 2026-08-06)

### Under HOME (/)
- Brand strip: "ARIF FAZIL" + live clock — sovereign identity, always visible.
- No other artifacts. HOME is the cockpit, not a content page.

### Under EARTH (/earth)
| Artifact | Status | Notes |
|----------|--------|-------|
| `/earth/` | live | SPA route (Earth.tsx) — globe + basin data |
| `/earth/kinabalu-basin/` | live | static HTML |
| `/earth/kinabalu-cross-section.html` | live | static HTML |
| `/earth/malay-basin/` | live | static HTML |
| `/earth/malay-basin-cross-section.html` | live | static HTML |

### Under WORDS (/writing)
| Artifact | Status | Notes |
|----------|--------|-------|
| `/writing/` | live | SPA route — essays hub |
| `/doctrine` | live | SPA route — arifOS F1–F13 canon |
| `/world/makcikgpt/` | live | 22 BM civic journalism articles — URL stays at /world/ for stability |
| `/world/makcikgpt/<slug>` | live | individual articles (OG+JSON-LD+theme-color added 2026-08-06) |
| `/000/` | live | Genesis / sovereign origin — constitutional artifact, secondary nav |
| `/999/` | live | Sealed receipts / proof — constitutional artifact, secondary nav |

### Under WORLD (/world)
| Artifact | Status | Notes |
|----------|--------|-------|
| `/world/` | live | static hub — cards: Words, Atlas, Commodities, Politics |
| `/world/sot/` | live | State of the World atlas (D3+GDELT+WorldBank) |
| `/world/llms.txt` | live | machine-readable section overview (fixed 2026-08-06) |
| `/world/page.json` | live | structured section metadata (fixed 2026-08-06) |
| `/oil/` | live | Brent dashboard — live API from WEALTH |
| `/gas/` | live | NatGas dashboard — live API from WEALTH |
| `/gold/` | live | XAUUSD dashboard — live API from WEALTH |
| `/klci/` | live | FBMKLCI dashboard — live API from WEALTH |
| `/usdmyr/` | live | USD/MYR dashboard — live API from WEALTH |
| `/economics` | live | SPA route — old Capital label, redirects to WORLD in nav |
| `/politics/` | live | geopolitics hub |
| `/politics/ns-election/` | live | NS election map |
| `/politics/shadow/` | live | Shadow PMs |
| `/propa/` | live | PETRONAS VITALS (v3 live model, 8 sliders) — root-level organ door, portal card on WORLD |
| `/malaysia/` | live | Sovereign VITALS (v3 live model, 4 sliders) — root-level organ door, portal card on WORLD |
| `/map/` | live | navigation map — secondary nav / footer |

### Under WORK (/missions)
| Artifact | Status | Notes |
|----------|--------|-------|
| `/missions/` | live | SPA route — missions registry |
| `/resume/` | **404** | NOT BUILT — identified during 2026-08-06 fit audit. Needs static shell or SPA page. |

## Audit recipe: find dangling artifacts

```bash
# 1. Get all sitemap routes
curl -sf https://arif-fazil.com/sitemap.xml | grep -oP '(?<=<loc>)[^<]+' \
  | sed 's|https://arif-fazil.com||' | sort > /tmp/routes.txt

# 2. Check each route against the 5 homes
for r in $(cat /tmp/routes.txt); do
  matched=false
  for home in "/" "/earth" "/writing" "/world" "/missions"; do
    case "$r" in
      "$home"|"$home/"*|"/000"*/|"/999"*/|"/map"*/) matched=true; break ;;
    esac
  done
  $matched || echo "DANGLING: $r"
done

# 3. Also check root-level routes not in sitemap (live but unmapped)
for r in oil gas gold klci usdmyr propa malaysia politics; do
  curl -sf -o /dev/null -w "$r: %{http_code}\n" "https://arif-fazil.com/$r/"
done
```

## Decision rule for new artifacts

1. Does it fit under an existing 5-page home? → put it there.
2. Does it fit under WORLD (the catch-all for "what's happening")? → put it there.
3. Is it a new organ? → escalate to F13 for 6th nav item OR make it an organ door
   in machine_links + portal card on the closest page.
4. Is it a one-off experiment? → forge_work/proposals/, not public/.
5. Is it a PDF/report? → forge_work/out/, not public/. PDFs are artifacts, not pages.

**Never put a new artifact at root (`/new-thing/`) without routing it under one of the 5.**
