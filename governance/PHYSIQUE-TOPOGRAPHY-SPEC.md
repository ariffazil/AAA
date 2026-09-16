# Physique Topography — Layer Spec & Invariant Catalogue
> Forged 2026-09-16 (KVM8). Authority: F13 (Arif) — "map the topography + invariants to be coded".
> Status: IMPLEMENTED (module + tests) · GOVERNANCE ITEMS OPEN (see §6).

## 0. The one architectural decision this doc exists to enforce

**Identity and physique are two different stores. Never one.**

| | Identity store | Topography store |
|---|---|---|
| Question | "Is this the consenting person?" | "What is this body doing / how has it changed?" |
| Anchors | face template + name + history + relations | pose-normalised bone ratios |
| Permanence | name/history/relations permanent; biometric rented (90d) | state drifts weekly; invariants drift over years |
| Failure if wrong | names the wrong human (worst possible) | mis-describes a body (recoverable) |
| Verdict power | may assert identity (with quorum) | may **corroborate** only, never assert |

Bodies change with cut/bulk, pump, flexion, clothing, lens and viewpoint. A body is the
least permanent thing about a person, so it must never carry the identity load. If the two
stores merge, every gym photo becomes a name — and the first failure mode is the
2026-09-01 scar (context-prior overreach → wrong person named).

## 1. What already exists on this host (probed 2026-09-16, not assumed)

| Component | Path | State |
|---|---|---|
| Face verify policy engine | `/root/arifOS/arifosmcp/biometric/face_verify.py` | PRESENT (14.5 KB) |
| Air-gapped embedder bridge | `.../biometric/extract_edge.py` + `/root/faceid-venv` | PRESENT, separate venv (insightface isolated here) |
| Engine↔policy bridge | `.../biometric/verify_from_image.py` | PRESENT — "no biometric material on output" |
| Face model weights | `/opt/insightface/models/buffalo_l` (326 MB, 5 onnx) | DOWNLOADED |
| Vector store | Qdrant `identity_vault`, 512-d Cosine | LIVE, **2 points** |
| Consent registry | `/opt/well/well_triad/consent_scopes.py` (`biometric.full`) | PRESENT — scope **not_granted** |
| Identity card | `/root/AAA/registry/identity_cards/syed_khairuddin.yaml` | W1_face status **NOT_ENROLLED** |
| Name/class gate | `/root/AAA/registry/routing/identity_resolver.py` + `identity_continuity.yaml` | ACTIVE |
| Receipts | `/root/arifOS/VAULT999/arifos/RECEIPTS/biometric-*.json` | PRESENT (11/11 + 13/13 tests) |
| **Body / topography layer** | — | **DID NOT EXIST → this doc + module** |
| Pose estimator | — | **MISSING (no cv2-keypoint model installed)** |

Measured face band (F13 option 3): `t_accept 0.42`, `t_reject 0.25`, middle = ESCALATE step-up.

## 2. Topography map — the layers, in extraction order

```
media ingest (media-ingest MCP — frames + contact sheet)
  → frame selection        (whole-timeline sample, de-duplicated)
  → person detection       [MISSING: no detector installed]
  → pose keypoints         [MISSING: no pose model installed]
  → pose normalisation     [BUILT: physique_topography.normalize]
  → relation extraction    [BUILT: ratio + symmetry catalogue]
  → evidence classification[BUILT: RATIO_INVARIANT | STATE_OBSERVATION | UNUSABLE]
  → cross-session compare  [BUILT: corroboration only, never identity]
  → topography record      (append-only, per subject, separate from identity)
```

| Layer | What it holds | Evidence class | Status |
|---|---|---|---|
| Pose frame | pelvic origin, shoulder axis, robust scale | scaffolding | BUILT |
| Bone relations | arm span/torso, upper/lower arm, femur/tibia, torso/femur | RATIO_INVARIANT | BUILT |
| Shape state | shoulder/hip, neck/shoulder, width profiles | STATE_OBSERVATION | BUILT (partial) |
| Symmetry | bilateral height + reach deltas | accumulate only | BUILT |
| Surface marks | scars, tattoos, permanent asymmetry | conditional, consent-gated | NOT BUILT |
| Gait | cycle-normalised joint trajectories | needs ≥3 clean cycles | NOT BUILT — gym footage cannot supply this |

## 3. The correction that matters (vs the common recipe)

The widely-quoted normalisation divides by **shoulder width**. On a physique subject that is
the pair that moves MOST with lat spread, flexion, pump and camera elevation — so it injects
pose noise into every derived ratio. The implemented scale is the **median usable long-bone
length** across 8 bone segments: a single bad landmark perturbs one term and the median
absorbs it. Verified by test `test_scale_ignores_shoulder_breadth`.

Second correction, found by failing test: a **half-body read must not qualify as good**.
Arms-and-torso-only is the normal gym framing, and it previously passed. Coverage now requires
an anchor in BOTH an UPPER and a LOWER invariant group, or the read is FAIR and abstains.
Verified by `test_upper_only_read_is_not_good`.

## 4. Invariant catalogue (code: `physique_topography.py`)

| Invariant | Definition | Class |
|---|---|---|
| `arm_span_to_torso` | (L sh→wrist + R sh→wrist) / (L sh→hip + R sh→hip) | RATIO_INVARIANT |
| `upper_to_lower_arm` | (L sh→elbow + R sh→elbow) / (L elbow→wrist + R elbow→wrist) | RATIO_INVARIANT |
| `femur_to_tibia` | (L hip→knee + R hip→knee) / (L knee→ankle + R knee→ankle) | RATIO_INVARIANT |
| `torso_to_femur` | (sh→hip) / (hip→knee) | RATIO_INVARIANT |
| `shoulder_to_hip` | shoulder breadth / hip breadth | STATE_OBSERVATION |
| `neck_to_shoulder` | nose→shoulder / shoulder breadth | STATE_OBSERVATION |
| `*_height_delta`, `*_reach_delta` | bilateral asymmetry, mirrored axes | accumulate only |

Every read carries: `ratios`, `ratio_evidence_class`, `coverage_groups`, `scale_reference`,
`scale_segments_used`, `frame_quality`, `evidence_class`, `abstained`, `abstain_reasons`,
`warnings`, `provenance`. A ratio without its acquisition conditions is not comparable to
the same ratio measured another way — provenance is mandatory, not decorative.

## 5. Hard gates (binding on any caller)

1. **G1 — corroborate, never identify.** `compare()` returns CORROBORATES / DIVERGES /
   AMBIGUOUS / INSUFFICIENT. There is no "MATCH" verdict. Naming requires the face witness
   plus the permanent W3/W4/W5/W6 witnesses.
2. **G2 — abstain upward.** Occlusion, foreshortening, half-body coverage, or missing scale
   segments → `abstained=True`. Never estimate through it.
3. **G3 — no single witness is authority.** Per the identity card: quorum ≥3, geometric mean
   ≥0.50, `single_witness_authority: NEVER`.
4. **G4 — consent before template.** `biometric.full` must be `granted`. Topography records
   about a third party are consent-gated the same as biometrics.
5. **G5 — no 1:N, ever.** Verify a known, consenting subject. No population search, no
   scraping, no name inference from an image.
6. **G6 — templates not photos.** Store derived values + provenance. Raw media deleted after
   extraction unless the subject asks for an archive.
7. **G7 — mismatch escalates.** Face says X, body says Y → `ESCALATE_TO_F13`, never resolve
   silently toward the more confident-looking signal.
8. **G8 — state ≠ identity, permanently.** Pumped volume, leanness, posture under load,
   clothing, tan, hairstyle, jewellery, background, watermark, location, camera focal length
   are EXCLUDED from identity-class evidence. Ask: "would this still hold in a different
   photo, six months later?" If no → STATE_OBSERVATION.

## 6. Open governance items (surface, do not silently fix)

| # | Finding | Severity |
|---|---|---|
| O1 | Qdrant `identity_vault` holds **2 vectors** (`syed_khairuddin`, `syed_khairuddin_melbourne`) while `syed_khairuddin.yaml` says `W1_face.status: NOT_ENROLLED` and `refs/` is empty — reality and doctrine disagree about whether a template exists | HIGH |
| O2 | `biometric.full` consent scope reads `not_granted`, while the biometric receipt records "consent recorded (F13 gate 2026-09-05)" — two consent records disagree | HIGH |
| O3 | `forge_face_embed` / `forge_face_match` are named as capabilities in an **ACTIVE sealed** identity card and in the resolver fallback, but are **never implemented**. The working code uses different names (`extract_edge`, `FaceVerifyService`). A sealed doctrine pointing at ghost tools | HIGH |
| O4 | Thresholds 0.42/0.25 rest on `n=1 condition` (`0.47/0.0`). The receipt itself flags it: FRR/FAR drill with 5–10 genuine + consented impostors outstanding | MEDIUM |
| O5 | No pose estimator installed → the topography module has no live keypoint source. Landmarks must come from a governed install decision, not an import | MEDIUM |
| O6 | 2026-09-01 mis-ID scar is unaddressed by any biometric infrastructure — that failure was context-prior overreach with no anchor comparison, which thresholds cannot fix | MEDIUM |

## 7. How this changes behaviour tomorrow

When a photo or video arrives and the question is "who is this":
1. Face lane (consent + enrolled template) → may assert identity, with quorum.
2. Topography lane → may only say "consistent with" or "not consistent with" and must
   abstain when the frame is half-body.
3. No anchor match or no consent → **"aku tak pasti siapa"**. A wrong name is worse than
   no name (scar 2026-09-01).

When the question is "how has he changed":
topography is the right tool, and only the RATIO_INVARIANT family is comparable across
sessions — everything else is a dated state observation.

## Evidence
- Module: `/root/AAA/registry/topography/physique_topography.py`
- Tests: `/root/AAA/registry/topography/test_physique_topography.py` — 14 passed
- Doctrine: `/root/AAA/instructions/identity-continuity.md` · identity card + resolver as cited

DITEMPA BUKAN DIBERI ⚒️
