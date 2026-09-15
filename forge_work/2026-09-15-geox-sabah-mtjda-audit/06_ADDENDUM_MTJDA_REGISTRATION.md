# ADDENDUM — Malay Basin / MTJDA claim registration (execution pass 2)

**Authority:** F13 ARIF — *"Ok do all"*
**Executor:** Hermes (edge bridge, KVM4) · 2026-09-15

---

## 1. Executed

Target: `/root/GEOX/resources/basins/malay_basin/claims.json`

Added 7 claims — `CLM-MTJ-001` … `CLM-MTJ-007`. Store now holds **24**.

```
git diff --numstat → 194  1
```
The single deletion is the closing `]` moved onto a combined line. Verified: the original 17
claims are **content-identical** (parsed + canonical-JSON compared), and the only deleted line
is `-]`. Zero content loss.

| ID | Claim | Class | Conf |
|---|---|---|---|
| CLM-MTJ-001 | PSC 35 yr, eff. 1 Jan 2026, PC JDA + PTTEP JDX 50/50, ceremony 14 Sep Bangkok | observed | HIGH 0.95 |
| CLM-MTJ-002 | CO₂ risk framework; 40–90 mol% only on basement-rooting trends; open area LOW–MOD by analogue, not measurement | interpreted | MED 0.62 |
| CLM-MTJ-003 | Dual overpressure compartment; MTJDA = **flank** model 2,600–3,000 m under Group L | derived | HIGH 0.85 |
| CLM-MTJ-004 | Deep syn-rift fairway; Group K dual reservoir+source; binding uncertainty = reservoir quality <3,000 m | hypothesis | LOW 0.30 |
| CLM-MTJ-005 | Two trap families: inversion anticlines (SGR-dependent) vs stratigraphic pinchouts (emerging) | interpreted | MED 0.68 |
| CLM-MTJ-006 | Malay Basin failed rift; MTJDA on northern ramp margin | observed | HIGH 0.88 |
| CLM-MTJ-007 | **Internal inconsistency** — capacity figures (see §3) | interpreted | MED 0.60 |

---

## 2. Independently verified (not taken from the dossier)

**50/50 equity and company identity — CONFIRMED.**
`PC JDA Ltd` (Petronas Carigali wholly-owned subsidiary) + `PTTEP JDX Thailand Ltd Co` and
`PTTEP JDX Thailand (JDA) Ltd` — each holding **50% participating interest**, 35-year term
effective retroactively from 1 January 2026. Sources: PTTEP release, The Star, offshore-energy,
offshore-technology, Reuters.

**Note for the record:** the dossier itself does **not** state the company equity split. Its
"split equally between the two countries" refers to country gas distribution, not participating
interest. The 50/50 figure came from the second reviewer and is correct — registered here as a
verified external addition, not a dossier claim.

---

## 3. New defect found — internal capacity inconsistency

The MTJDA dossier states two figures that cannot both be current physical throughput:

| Location | Figure |
|---|---|
| §2.2 (Fig. 2 discussion) | "combined contracted capacity of about **700** mmscf/d" across both blocks |
| §2.2 (development) | Block A-18 **alone**: "approximately **790** mmscf/d at the riser" |
| §2.2 (Block B-17/C-19) | declining DCQ **335 → 250** mmscf/d, ran to 1 Jan 2026 |

A-18 alone (790) exceeds the stated combined total (700). Reconcilable **only** if one is a
contractual DCQ and the other a physical riser capacity — which the document never says.

Same discipline the Kinabalu dossier applied to itself: a document that complains about
ambiguity should be audited for its own. Registered as `CLM-MTJ-007`, not resolved — resolution
requires the MTJA/operator capacity basis.

---

## 4. Cumulative state after both passes

| Store | Before | After | Added |
|---|---|---|---|
| `sabah_basin/claims.json` | 3 | 7 | CLM-NWS-004..007 (H1–H4 deep crustal) |
| `malay_basin/claims.json` | 17 | 24 | CLM-MTJ-001..007 |

Mutation footprint: **two files**, additive, git-tracked, reversible. No deletions of content.

---

## 5. Still held (unchanged)

- `sabah_two_oceanics.yaml` patch — sealed-ledger representation, F13 boundary
- `basin_profile.yaml` deprecation — untraced code path
- `/opt/geox` deployment — separate mutation; repo `6d55a682` vs deployed `8c6c7f2d`
- Live MCP claim write — `AUTHORITY_GATE · HOLD` (OBSERVE_ONLY, actor unverified)
- Formation-name correction — corruption confirmed, correction unsourced

---

DITEMPA BUKAN DIBERI ⚒️
