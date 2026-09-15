# Artifact Ledger — two GEOX documents received 2026-09-15

**Purpose:** give both PDFs a chain of custody. They arrived with none.

## Artifact 1 — GEOX_Kinabalu_Basin_Geologist_Dossier.pdf

| Field | Value |
|---|---|
| Pages | 29 · A4 · WeasyPrint 69.0 |
| Bytes | 4,172,847 · md5 `aa2cb0031c…` |
| Hash stable? | **Yes** — 3 independent deliveries on 2026-09-15 (14:43, 15:29, 23:42) are byte-identical |
| Declared authorship | M Arif bin Fazil (F13 Sovereign) + GEOX Federation |
| Declared compiled | 15 September 2026 |
| Declared evidence base | "60+ internal artifacts across 6 organs · 45+ peer-reviewed papers" |
| **Provenance found on host** | **Partial** — HTML/PDF build lane in `/root/.qwen/tmp/` (kinabalu-dossier.html, build_slides.py). Qwen CLI session `caaa4509-…`, model `mimo-v2.5-pro`, 04:05–07:06 UTC 2026-09-15 |
| **This exact 29-page build** | **NOT FOUND on host.** Qwen lane produced 3 other Kinabalu PDFs (12:18, 12:25, 14:20/14:35). No 4,172,847-byte source. |
| forge_work entry | **None** |
| Claim/vault entry | **None** |
| Verdict | `PROVENANCE_PARTIAL` — authorship declared, build not traceable |

## Artifact 2 — GEOX_MTJDA_A18-01_Regional_Geology.pdf

| Field | Value |
|---|---|
| Pages | 23 · A4 · WeasyPrint 69.0 |
| Bytes | 2,726,719 · md5 `69e37ac324…` |
| Hash stable? | **Yes** — 2 deliveries (15:29, 23:42) byte-identical |
| Declared produced by | GEOX organ — arifOS Federation |
| Declared compiled | 15 September 2026 |
| Declared sources | public-domain literature + PETRONAS/PTT announcements + MTJA disclosures |
| **Provenance found on host** | **None** |
| forge_work entry | **None** |
| Claim/vault entry | **None** |
| Verdict | `PROVENANCE_ABSENT` — no build source on this host |

## External verification performed (not taken on trust)

| Claim | Verified? | Source |
|---|---|---|
| New PSC, 35 yr, eff. 1 Jan 2026, A-18-01 + open area | **CONFIRMED** | Reuters, The Star, NST — all 14 Sep 2026 |
| Morley 2024, Earth-Sci Rev 249:104663, syn-collisional wedge | **CONFIRMED** | journal reference matches |
| Cottam 2013, JGS 170(5) 805–816, DOI 10.1144/jgs2011-130 | **CONFIRMED** | Lyell Collection |
| Choi & Hand, Oligocene play, Layang-Layang (TGS/EAGE 2026) | **CONFIRMED** | TGS technical library |
| Pilia 2023 detached Proto-SCS slab | **CONFIRMED paper · METADATA WRONG** | dossier says *Nature Geoscience*; actual: *Gondwana Research* |
| Madon 2025 Moho depth beneath Sabah | **CONFIRMED paper · METADATA WRONG** | dossier DOI 230589; actual DOI 10.1016/j.tecto.2025.230916 |
| Malay Basin figures (Group K dual role, HI 137–403, Group L HI 300–400, Group F 50–150 m, flank OP 2600–3000 m) | **CONFIRMED INTERNAL** | `/root/GEOX/resources/basins/malay_basin/` (repo + deployed) |

## Deployment state at time of ledger

| Surface | Commit |
|---|---|
| `/root/GEOX` (repo) | `6d55a682` |
| `/opt/geox` (deployed, WorkingDirectory of live geox-mcp.service) | `8c6c7f2d` |
| Live service self-report | `geox-8c6c7f2d`, version `v2026.08.26`, kernel_verdict SEAL |

Basin resource files verified **identical** between repo and deployment.

## Standing caveats attached to both artifacts

1. Neither has a build source on this host. Treat as external submissions, not federation-forged artifacts.
2. Two citation metadata fields are wrong (Pilia journal, Madon DOI). Shape ≠ witness — a correctly
   formatted reference line is not evidence the underlying claim was checked.
3. Kinabalu dossier: no seismic volume loaded; all interpretations rest on published cross-sections.
   Verified still true — the SEG-Y evidence lane exists in deployed source but no volume is ingested.
4. Kinabalu dossier: KT-7 recommendation is contested against federation code — see `02_KT7_CLAIM_CORRECTION.md`.
5. MTJDA document is public-domain synthesis with no MTJA/PETRONAS/PTT proprietary data. Not a
   prospect evaluation. Do not use for coordinates, volumetrics or well planning.
