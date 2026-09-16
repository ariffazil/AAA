# detect_location() — patch history & future-venue template

## Status: KPJR detection applied 2026-08-17

**Applied, not pending.** Both `KPJR` (Rawang, green `#00b894`) and `KPJAP` (Ampang Puteri, orange `#e17055`) are now in the dict, and the loop uses `sorted(locations.keys(), key=len, reverse=True)` so the longest suffix wins over bare `KPJ`. Filenames like `16 AUG 2026 KPJR.xlsx` now print `Location: KPJ Rawang` in script output and `KPJ Rawang · 16 AUG 2026` in the PDF header. Verified live on 17/18 Aug 2026.

## Template for a new KPJ venue

When a new KPJ branch (e.g. KPJS Seremban, KPJB Bangi) goes live, the same patch is one line per venue. Add BEFORE the bare `KPJ` fallback, with its own folder + color:

```python
"KPJS": {"name": "KPJ Seremban", "short": "KPJS", "color": "#...something..."},
"KPJB": {"name": "KPJ Bangi",    "short": "KPJB", "color": "#...something..."},
```

Then update the `Multi-venue file discipline` table in SKILL.md (root folder, color, trial-launch date). Don't forget to create the output folder before generating the first PDF — the default root is reserved for KPJD.

Color palette convention (keep venues visually distinguishable):
- KPJD = blue `#0984e3` (mature, established)
- KPJR = green `#00b894` (trial/growing)
- KPJAP = orange `#e17055` (planned / launching)
- Future venues: pick a color not already in use. Suggested unused: pink `#fd79a8`, teal `#00cec9`, gold `#fdcb6e`.

## Why order matters

`detect_location()` iterates the dict and returns on the first match. Python dicts preserve insertion order, so listing `KPJR` before `KPJ` makes `KPJR` checked first. The explicit `sorted(..., key=len, reverse=True)` belt-and-braces makes it robust against future re-orderings.
