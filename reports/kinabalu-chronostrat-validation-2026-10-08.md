# Kinabalu Chronostrat v2 — Independent Validation & Falsification (FI-008)
**Date:** 2026-10-08 · **Subject:** Claude Code forge (chronostrat chart v2 + east-sabah models page, Windows session) · **Validator:** FI-008 on VPS, own arithmetic, against GEOX registered claims
**Outcome landed:** kin_clm_12–16 appended to `/root/GEOX/resources/basins/kinabalu_basin/claims.json`; validation note in `tectonic_history.md`; three-model set forged to `/root/GEOX/resources/basins/east_sabah_dg_models/models.json`.

## VALIDATED (independently re-verified)
1. **SRU inboard ≈ 9.36–9.41 Ma; "8.6 Ma" rejected inboard.** I recomputed all three interpolations myself (Gajah Hitam-1 9.41, Tiga Papan-2 9.36, Maligan-1 9.38; pick inside NN10, NN9 8.5–46 m below). At Gajah Hitam-1, 8.6 Ma would sit ~700 m up-section — not a subtle miss. Caveats kept: constant-rate assumption (INT), pen-chart NN intervals not raw occurrences, Solisip-1 outlier (NN11 below pick) = transition toward N Sabah, Rotan deepwater candidate ~8.29–8.50 remains — the family-vs-two-surfaces fork stays OPEN. This **narrows kin_clm_10's age HOLD**.
2. **TOP≡BASE convention + composite-pick exclusion rule.** Top III=Base IVA=DRU … Top IVF=Base IVG=Horizon I. Consistent with the pack; Copilot v1.1's mixed-convention labels are the defect. → kin_clm_13.
3. **DRU 41% calibration artefact.** Legacy 15.4–15.6 = BKSA95 base NN5 → GTS2012 14.91; residual 0.71 Myr real. Arithmetic checks. → kin_clm_14.
4. **Inboard Stage III bathyal; diachronous NW-stepping shoaling.** Deluar-1/Ketam-1/South Lokan-1 bathyal below DRU; coastal on highs post-DRU; outer shelf bathyal to SRU–IVE. Falsifies Copilot v1.1's uniform inboard picture. → kin_clm_15.
5. **Crocker = source, not depocentre; MMU(DG) ≠ DRU(Sabah).** Matches sys_clm_8/9 and the turn-1 adjudication. Project DRU 14.2 ≡ two-oceanics MMU 14.2 — convergence noted as a fork, not merged.
6. **C11 editorial errors in endorsed decks — all four confirmed** (NN9 is Tortonian/Late Miocene; Bunguran is Natuna-Indonesia; Priabonian is Late Eocene; IVA is Langhian–Serravallian). Fix before IRS#1 (Oct 2026).
7. **Build discipline** (render-only-from-data, validation gate 0 issues, SHA256 ledger, contradiction register with tests) — sound engineering.

## FALSIFIED / SUPERSEDED
1. Copilot v0.1/v1.1 charts (undeclared non-linear time axis, Crocker drawn as depocentre, diapirs coloured as hiatus, "Base NN4 at 15.5 Ma", mixed stage conventions) — superseded by v2.
2. "SRU = 8.6 Ma" as a single regional age — falsified inboard; survives only as the deepwater/younger candidate (Rotan ~8.3–8.5).
3. "DRU/MMU" as one surface — falsified (two physics, two domains).

## FLAGGED (corrections before public/persistent use)
1. **Granite age stated as bare fact 7.85–7.22 Ma (Cottam 2010)** — sys_clm_6 holds the intrusion age UNVERIFIED (K-Ar to ~14 Ma contested; forbidden: cite as 8–7 Ma). Plausible + consistent with 360 °C/Myr cooling, but the public PDF/page must carry the contest note "~7–8 Ma U-Pb; older K-Ar contested". → kin_clm_16.
2. **Claude Code's source ledger omitted the GEOX packs** — its DRU candidate set {15.4, 14.91, 14.2} missed the federation's F13-settled ladder window **13.5–12.5 Ma** (kin_clm_2/sys_clm_9). Four candidates now registered, none averaged. → kin_clm_14.
3. **IVE–IVG definitional split** (project vs legacy, 1.7–2.4 Myr — two schemes under same names) needs an F13 naming decision before Phase II mapping.
4. **Well witness rests on pen-chart derived NN intervals** — raw occurrence charts with reworking/caving control still required (Claude Code flagged this itself; keep as gate, esp. Maligan-1 NN10D-above-NN11D reversal, Kudat-1 "?Crocker" with NN9a, Imbok-1 datum conflict).
5. **Kinarut fan stage (IVC vs IVE Atlas claim)** still unverified — Atlas Chapter 5 not read.
6. **PDF fixes already planned by Claude Code are correct**: granite age caveat (see flag 1) and Sabah Trough = NW (not eastern) boundary of Kinabalu Basin.

## Arif's ridge theory (Model A) — current machine verdict
Unchanged from the morning adjudication: **strong form tensed by three registered facts** (DG = attenuated continental crust; spreading dead ≥16 Ma while magmatism is multi-generation 7–14 Ma; H3 volcanic-basement weakest at p50 0.18). New consistency note from the chronostrat witness: **zero trough-axis volcanic bodies anywhere in the 0–66 Ma record** (weak evidence — record is interpretive). Kinematic note: ridge push NW–SE perpendicular to a NE–SW trough axis is geometrically coherent for pushing toward both Kinabalu and DG — but an ACTIVE Miocene ridge has no home in the LOADING_DOMINANT (4.25×) regime; A survives as an INHERITED ≥16 Ma feature, which converges on C. **Cheapest discriminator stands: public mag/grav reprocessing along the strike line (near-zero cost) before any acquisition spend.**

## Site lane (not touched from VPS — dual-writer hazard)
Claude Code's Windows worktree (`feat/kinabalu-xsection-models` off arif-sites origin/main) is mid-flight on the same files the VPS deploy serves (`/root/arif-fazil.com`, branch `site/harden`; `/root/arif-sites` mirror). VPS made **no site edits**; landing flows through the GitHub PR → deploy. Public-safe corrections for that PR are flags 1 and 6 above. Chronostrat v2 package stays PETRONAS INTERNAL — never enters the public site.

## Receipts
- Claims: kin_clm_12–16 (`/root/GEOX/resources/basins/kinabalu_basin/claims.json`, JSON-validated)
- Model pack: `/root/GEOX/resources/basins/east_sabah_dg_models/models.json`
- Turn-1 adjudication: GEOX clm_1d43072344d54ec5 / clm_da9c21d8c3e54874 / clm_bebd2c76b29049dd + `/root/AAA/reports/east-sabah-three-model-adjudication-2026-10-08.md`
- Kernel judge lane: BLOCKED (L11 SCT alias defect, documented, no machine seal possible) — this validation is warga analysis grounded in registered claims.
