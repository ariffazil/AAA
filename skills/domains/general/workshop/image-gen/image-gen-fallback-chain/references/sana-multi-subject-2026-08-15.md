# SANA Multi-Subject Iteration Log (2026-08-15)

Context: full paid-stack outage same night — mmx image-01 HTTP 404 (both regions), mage_generate timeout then `{"status":"error","error":"unknown"}`, Qwen token-plan `Throttling.AllocationQuota`, MuleRouter Wan 2.6 T2I 402 negative balance. Pollinations (`model=flux` requested, SANA served per EXIF `manufacturer=sana`) was the only live lane.

Target composition (from user reference image): standing muscular man, unbuttoned shirt open, kneeling woman in black between his stance, amber chiaroscuro, shadow on wall.

| Version | Prompt strategy | Result |
|---|---|---|
| v1 | Full worship scene, silhouettes at frame edges | Man OK (shirt drifted white), worshipper missing, East-Asian phenotype |
| v2 | Same, worshipper re-emphasized | Shirt lost entirely — SANA drift |
| v3 | Low angle, worshipper as foreground anchor seen from behind | 2 kneeling figures + man rendered — first two-subject success |
| v5 | Woman described mid-prompt | Woman missing — single-subject ceiling |
| v6 | Woman FIRST in prompt | Woman rendered, man missing — subject-order weighting confirmed |
| v8 | Binding: woman hugging man's thighs, his hand on her head | Both subjects rendered with physical connection — best free-tier result, delivered |

Lessons:
1. SANA holds one subject reliably; two independent subjects → one silently dropped.
2. First-mentioned subject survives when one is dropped.
3. Binding via physical contact renders both figures as one unit.
4. Low-angle foreground anchor is a weaker but working alternative for the worshipper.
5. Vision-QC every render before delivery — silent subject-drop is the failure mode, and EXIF `manufacturer=sana` tells you which engine actually served even when flux was requested.
