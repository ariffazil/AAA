---
name: cv-feature-matching
description: "Deterministic classical-CV feature matching (SIFT/DoG via OpenCV, cv2 5.x live on box) for exact geometry questions — duplicate-image detection under random filenames, rendered-artifact vs template verification, object localization with pixel coordinates, seismic-display matching. SIFT finds WHERE content is identical (pixel coords, scale, rotation); LLM vision says WHAT it is. Use when: 'are these images the same', 'find duplicates', 'locate this object in that image', 'does the render match the template', or any claim of image identity that must be falsifiable."
---

# CV Feature Matching (SIFT) — deterministic image identity

**Live receipt 2026-10-08:** geox_section_9dtnip8f vs wzz_4ebz (different random filenames): 513 keypoint matches, 513 RANSAC inliers → same content. Pixel MSE verified the family: 1 byte-identical (MSE=0.0), 3 near-duplicates across 6 files. cv2 5.0.0 on box.

## When SIFT over LLM vision (route least power)

| Question | Tool |
|---|---|
| Are these two images the SAME content? (falsifiable, deterministic) | SIFT + RANSAC |
| Where (pixel coords) is this object in that scene? | SIFT + homography |
| What is this image showing? (semantic) | mata / image-analyzer / 555-ASI-VISION |
| Both: SIFT verifies identity first, LLM describes second | chain |

LLM vision CANNOT reliably return pixel coordinates or prove identity. SIFT cannot name things. Never use one for the other's job.

## Recipe (tested, cv2 5.0.0)

```python
import cv2, numpy as np
g1 = cv2.cvtColor(cv2.imread(p1), cv2.COLOR_BGR2GRAY)   # grayscale FIRST, always
g2 = cv2.cvtColor(cv2.imread(p2), cv2.COLOR_BGR2GRAY)
sift = cv2.SIFT_create(nfeatures=3000)
k1, d1 = sift.detectAndCompute(g1, None)
k2, d2 = sift.detectAndCompute(g2, None)
matches = cv2.BFMatcher(cv2.NORM_L2).knnMatch(d1, d2, k=2)
good = [m for m, n in matches if m.distance < 0.75 * n.distance]   # Lowe ratio
inl = 0
if len(good) >= 4:
    src = np.float32([k1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst = np.float32([k2[m.trainIdx].pt for m in good]).reshape(-1,1,2)
    _, mask = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)        # geometric consensus
    inl = int(mask.sum()) if mask is not None else 0
# verdict: inl >= 30 with inlier_rate >= 40% → same content (calibrate per domain)
```

## Iron rules

1. **Grayscale before SIFT.** Color adds nothing, breaks nothing by removing it.
2. **Lowe ratio 0.75** for match filtering. Relative margin beats absolute distance threshold.
3. **RANSAC homography is the verdict**, raw match count is not — 500 good matches can still be geometric garbage.
4. **SIFT is 2D-planar.** Same 3D object from different viewpoints needs COLMAP-class pipelines (SIFT is their backbone, not their answer).
5. **Tiny images (<200px) yield no keypoints** — reject input, don't fake a verdict.
6. **MSE/SSIM verify after SIFT claims duplicate** — two witnesses, one cheap one geometric.
7. Deterministic: same inputs → same keypoints. Safe to use as evidence in receipts.

## Distilled invariants (SIFT design → arifOS mapping)

| SIFT mechanism | Federation principle |
|---|---|
| DoG ≈ LoG (cheap approximation of exact operator) | Route least power — never pay governed cost for what free math does |
| Octave scale-space (blur+downsample hierarchies) | Observe at multiple granularities before claiming |
| 26-neighbour 3×3×3 extrema (distinctive ACROSS scales) | A signal valid at only one zoom level is noise; robustness = multi-scale |
| Principal orientation (canonical frame before compare) | Normalize before judging — rotation-invariant comparison needs a defined starting frame |
| Lowe's ratio test (best vs second-best margin) | Signal-strength gating: confidence lives in the GAP, not the absolute value |
| RANSAC (consensus of inliers over outliers) | Tri-witness: isolate the coherent majority story from false positives |

## Federation mapping

- **Seismic displays:** pairs with `geox_extract_display_proxy` (DISPLAY_DERIVED_PROXY) — SIFT adds cross-display geometric matching; still not amplitude-certifying.
- **Rendered-artifact QA:** verify a render matches its template before delivery (complements `rendered-artifact-verification`).
- **Entropy sweeps:** duplicate detection across `/tmp`, `forge_work`, media folders — filename-blind, exactly the /tmp geox_section case above.
- **Never** claim AVO/phase/seismic-quantitative verdicts from SIFT — geometry only.
