---
name: shadow-fdp-authoring
description: Use when building a shadow FDP review pack.
tags: [fdp, upstream, review-pack, governance, artifacts]
---

# Shadow FDP authoring

Arif builds independent ("shadow") field development plans on employer assets. The artifact must be **harder to dismiss than the official one**, not prettier. These rules are his, stated explicitly — follow them without being asked.

## Non-negotiables

- **Open conflicts stay visible.** Red banner in every affected section + a register table (conflict, positions, value at stake, owner, next action, tag). Never resolve silently, never average two estimates to make a table look finished.
- **Every number carries a tag**: VERIFIED (cited public source) / REPORTED (project synthesis, not public — e.g. a BOD the agent issued) / DERIVED (formula shown) / ASSUMED (author judgement + reason) / OPEN (unknown or disputed, no value offered).
- **Ranges stay ranges.** If two workstreams disagree, carry the range and tag it OPEN. A point value presented as fact is the failure mode the whole exercise exists to prevent.
- **No number exists only in prose.** Every value in a section resolves to a ledger row (JSON or table) with ID, value, unit, basis, tag, source.
- **Do not compute what you cannot defend.** If the fiscal engine or cost basis is unresolved, state no NPV and no economic limit rather than borrowing one from a model under reconciliation.
- **Public sources only.** Never internal PETRONAS/PCSB data (logs, DST, PVT, MISC costs). Never sign as Arif — author line "Prepared by HERMES (arifOS) for review". No employer logos, branding or document numbering.

## Entity resolution — the trap that cost a wrong conclusion

**Resolve vessels by IMO number before comparing specs.** Two names for one hull will silently corrupt a whole analysis.

Worked example (Limbayong): Excalibur is **IMO 9417103**, the same vessel as *Sevan Hummingbird / Hummingbird Spirit* — **not** a sister ship. The BOD even said "ex-Sevan Hummingbird" and the agent still treated it as a different vessel because it found a Teekay datasheet under the old name.

Also: a publicly quoted capacity may belong to a **cancelled tender**, not the actual asset. Limbayong's 40k bopd / 60k liquids / 75k bwpd figures are the 2020 cancelled FPSO tender; the real hull is 25,000 bopd / 30,000 bpd liquids / 20,000 bwpd WI / 270,000 bbl. Mixing the two inverted the waterflood conclusion (apparent over-injection became 38% under-injection).

Same rule for fields (block + discovery well) and companies (registry).

## Coupling check — do this before publishing

Ask what each number *depends on* that lives in another section. The class of error this catches is bigger than arithmetic bugs:

- Facility injection capacity → achievable VRR → recovery factor. If the vessel injects 20,000 bwpd, a 35–40% waterflood RF is unsupported. Nobody in ten workstreams connected these.
- GOR → gas-train binding → plateau limit. A "field GOR" from total gas ÷ total oil mixes free and solution gas and is circular if used to size voidage.
- Plateau rate is a *facility* constraint, not a subsurface uncertainty — do not put it in a PRMS range.

## PRMS discipline

Either probabilistic (P90/P50/P10 must be probabilities, with dependencies) or deterministic scenarios (each internally consistent). **Corner products are neither** — `OOIP_high × RF_high` is not a P10, it overstates the range. Calibrating to a published number is a check, not a case.

## Environment

- Typst: `/root/.local/bin/typst` (v0.13.x). Prefer it over HTML→PDF for long reports.
- `numpy`, `matplotlib`, `pyshp` are **not installed by default** — `pip install` first.
- `weasyprint` binary exists at `/usr/local/bin/weasyprint` but the Python module does not.
- Natural Earth shapefiles already on disk: `/root/.local/share/cartopy/shapefiles/natural_earth/physical/ne_10m_coastline.shp`.
- Bare `firecrawl` is not on PATH inside `execute_code` subprocesses; use `/root/.npm-global/bin/firecrawl` via terminal, or just use `web_search`/`web_extract`.
- Typst `Page X of Y` needs a **second compile pass** to settle.

## Delivery

PDF in chat via `MEDIA:/abs/path`, then a short note: pages built, tag counts, failed checks, next blocking input. No receipt theatre.
