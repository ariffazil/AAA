# ERRATUM — HERMES Sovereignty Declaration §4 (Heritage)

**Target record:** `/root/AAA/governance/HERMES_SOVEREIGNTY_DECLARATION_2026-09-18.md` (immutable, sealed 2026-09-18 — UNTOUCHED by this erratum)
**Ratification:** F13 "sah" 2026-09-28 (MYT, FI-003 trifecta session) · authored by FI-003 (333-AGI BUILD lane)
**Status:** F13_RATIFIED_CHAT 2026-09-28 — SEALED canonical correction. Original declaration remains the dated historical record; this file supersedes its §4 heritage finding only.

## Correction

§4 ("Heritage — fork, not inheritance") anchors its heritage finding on:

> `/root/.hermes/README.md` line 1: `forked_from: Hermes Agent (Nous Research)` — declares the heritage fork.

**That predicate is falsified by observation (2026-09-28, FI-003 trifecta probe):**

- GitHub fork network for `ariffazil/HERMES`: `isFork: false`, `parent: null`.
- Cross-repo compare `NousResearch:main...HERMES:main` → HTTP 404 (no shared object DB).
- HERMES commits probed in upstream → HTTP 422 "No commit found"; commit search → 0.
- HERMES root commit `68f42002` (2026-08-25) is an orphan "re-scrubbed clean tree"; 102 commits vs upstream 45,374; packages differ (`hermes-mcp` AGPL-3.0 vs `hermes-agent` MIT).

Therefore `ariffazil/HERMES` is **not a fork** of Hermes Agent and never was; the declaration's §4 conclusion ("heritage is fork") rests on an unprobed self-report — a claimed-equals-measured failure, the same class the federation prosecutes elsewhere.

## Corrected ontology (what is actually true)

1. `NousResearch/hermes-agent` (MIT) — upstream engine product.
2. `ariffazil/hermes-agent` — the **real engine overlay fork**; F13-signed merges onto upstream tags (`e814f5ab9f` = "sovereign federation overlay preserved", 2026-09-26; restored + sealed `50a7f8f798` after 2026-09-28 update-clobber; durable branch `sovereign/main-2026-09-28` + tag `hermes-sovereign-overlay-2026-09-28`).
3. `ariffazil/HERMES` = `~/.hermes` — **sovereign runtime home** (SOUL, lanes, hooks, `hermes_mcp` organ). Its AGPL-3.0 covers the governance layer only; nothing MIT-derived is duplicated inside it, so the §4 relicensing/consent analysis does not apply to it. For the engine overlay (item 2), MIT permits closed internal use; AGPL relicensing would need care — the original §4 caution remains valid **for item 2**, where it belongs.

## Consequences to re-derive

- "Maintenance debt / if upstream pivots, the fork becomes cost" (§4 bullet): still true for the engine overlay (item 2), and today's incident **strengthened** it: the update path actively clobbers sovereignty (R1 binary pending F13).
- Any downstream docs citing "HERMES is a fork of Hermes Agent" must be reworded to the three-entity ontology (README of `ariffazil/HERMES` already corrected, commit `09e7c03`, 2026-09-28).

**Evidence:** `/root/forge_work/2026-09-28-FI-003-HERMES-TRIFECTA-CONTRAST.md` §1, `/root/forge_work/2026-09-28-FI-003-hermes-trifecta-incident-recovery.md`, trace `trc-fi003-hermes-trifecta-20260928`.
