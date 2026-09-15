# KT-7 Claim Correction — the headline recommendation is not executable as stated

**Compiled:** 2026-09-15 · **Authority:** F13 ARIF
**Source claim:** Kinabalu dossier, Summary pt. 6, Issue 3, Figure 8, "What I would do next" (Week 1)

## The claim as published

> "The KT-7 reflector sits at 12–21 km depth on existing 2D seismic. Depth-converting it using
> existing velocity data would immediately tell us whether the deep crust is ophiolite (Vp 5.0–6.5
> km/s). The cost is zero — the data already exists. […] The tool has been built. The code is written."

This is the dossier's #1 recommendation and its strongest rhetorical point.

## What the federation's own code says

`/root/GEOX/geox/skills/subsurface/petro/sabah_prospect_discriminator.py`, `_default_pscs_filter()`:

```
kt7_result = "PENDING"                  # Vp profile unresolved
pscs_velocity_available = False         # KT-7: exact Vp sequence not published
"KT-7 PENDING: exact Vp inversion sequence (3200→3760→6041 m/s) not published"
```

And on geometry:

```
- KT-7: Franke et al. 2008 MPG 25, 606-624 — high-Vp body at 6-8 km, Vp unresolved (PENDING)
```

## The three discrepancies

| Item | Dossier | Federation code | Status |
|---|---|---|---|
| KT-7 depth | 12–21 km | 6–8 km | **Contradiction** |
| Vp data available | yes ("existing velocity data") | no (`pscs_velocity_available=False`) | **Contradiction** |
| Test status | "has not been run" (tool ready) | `PENDING` (velocity unresolved) | Materially different |

## Why this matters

The dossier's "zero cost, high information value" pitch depends on the velocity data already
existing. The code — written earlier, from the same literature — says that exact Vp sequence is
**not published**. If the code is right, KT-7 is not a free test; it is a test that first requires
acquiring or inverting a velocity profile. The cost and calendar change.

One of the two is wrong. Mine is not the authority to decide which — but the federation cannot
publish both.

## Second-order finding (external, directionally correct)

Peer review from the group flagged that ophiolite Vp 5.0–6.5 km/s overlaps lower-crustal
continental velocities at 12–21 km. **That holds.** Even if KT-7 depth-conversion succeeds, it
narrows H1-vs-H2 rather than resolving it. The dossier's own text claims KT-7 "would separate all
four deep-crustal hypotheses" — an overclaim on its face. The OBS refraction line remains the only
stated clean discriminator, which the dossier itself concedes elsewhere.

## Recommended correction (pending F13)

1. Reconcile the two KT-7 geometries (12–21 km vs 6–8 km) against Franke et al. 2008 before the
   claim is used in any decision pack.
2. Downgrade "would separate all four hypotheses" → "would narrow H1 vs H2"; the remaining
   discrimination requires the OBS line.
3. Restate cost honestly: free **if** velocity exists; otherwise not free.
4. Until reconciled, tag the KT-7 recommendation `CONTESTED` in the dossier and in any
   downstream artifact.

## What I did NOT do

Did not edit the dossier (external artifact, no build source on this host — see 03_ARTIFACT_LEDGER.md).
Did not edit the discriminator code — its `PENDING` verdict is the *conservative* one; the dossier
is the optimistic one. Correcting the code would be correcting the wrong side.
