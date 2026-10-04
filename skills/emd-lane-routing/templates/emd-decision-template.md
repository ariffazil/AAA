# EMD Decision Template

> **Use:** drop into any "which model should I use for X?" request, technical spec, PR description, or architecture doc.
> **Format:** copy this template, fill the bracketed sections, attach to your ticket.

---

## Task

**What does the task do, in one sentence?**
[ e.g., "Migrate the legacy billing pipeline from Python 2 to Python 3 across 47 services." ]

**Will the task's success depend on:**

- [ ] What comes **IN** (broad context, retrieval, ingestion) → **SENSE**
- [ ] What goes **OUT** (long generation, code, structured output) → **ACT**
- [ ] Both, interleaved → **split into sub-tasks**

**Primary lane:** [ SENSE | ACT | MIXED ]

## Input Profile

**Estimated input size:** [ tokens or characters ]
**Modality:** [ text | text+image | text+audio | video | multimodal ]
**Maximum tolerable input window:** [ tokens ]

## Output Profile

**Estimated output size:** [ tokens ]
**Output stability requirement:** [ low | medium | high — can the user tolerate hallucination? ]
**Tool calling required:** [ yes | no ]
**Must compile / pass tests:** [ yes | no — affects Gödel Lock presence ]

## Lane Selection

```
Q1: Does success depend on what comes IN?         → SENSE
Q2: Does success depend on what goes OUT?         → ACT
Q3: max_input_tokens of chosen model ≥ input?     → ___
Q4: max_output_tokens of chosen model ≥ output?   → ___
Q5: Cost ratio ≤ 3× of lane-optimal model?       → ___
Q6: Will loop touch reality within 1-2 turns?    → ___
```

If Q3 or Q4 fails → **lane violation**, re-pick before requesting.
If Q5 fails → consider whether the EMD lane split is worth the cost premium.
If Q6 fails (SENSE-only loop without ACT validation) → add ACT validation step.

## Model Selection

| Lane | Primary | Fallback 1 | Fallback 2 | Free alternative |
|---|---|---|---|---|
| ACT | deepseek-v4-pro | deepseek-v4-flash | qwen3.7-plus | glm-5.2 (tokenrouter) |
| SENSE | MiniMax-M3 | qwen3.8-max | qwen-vl-max (vision) | — |
| Mixed | qwen3.8-max | deepseek-v4-pro + MiniMax subtask | — | — |

**Chosen model:** [ ____ ]
**Reason:** [ one sentence — match the lane, not the brand ]

## Cost Estimate

**Input cost:** [ tokens × $/M ] = $[ ___ ]
**Output cost:** [ tokens × $/M ] = $[ ___ ]
**Total:** $[ ___ ]
**Compared to lane-optimal:** [ ___× ratio ]

If ratio > 3×, justify why or re-pick.

## Constitutional Check

- Constitutional tier required: [ 333 | 555 | 666 | 999 ]
- Tier-eligible models (per federation-models.json): [ ____ ]
- If tier ≥ 666: route via FED :7074, never direct
- F13 sovereign ack needed: [ yes | no ]

## Sub-task Split (if MIXED)

```
[TASK ROOT]
  ├── SENSE subtask: [ model = ____, input = ____ tokens, output = digest ]
  └── ACT subtask:   [ model = ____, input = digest, output = ____ ]
```

If a single subtask exceeds 60% of total loop time → consider persistent split, not just subtask.

## Gödel Lock Check

**Will the loop touch reality?**

- [ ] Code → `try_compile()` after generation
- [ ] Test → `pytest` after code change
- [ ] API call → real HTTP request
- [ ] File write → disk verification (`stat`, `git status`)
- [ ] Document parse → checksum on actual content

**If none of the above:** the loop is sealed against reality. SENSE-only mode is acceptable for retrieval/embedding tasks, NOT for tasks claiming to "complete" something.

## Sign-off

**Picked by:** [ ____ ]
**Date:** [ ____ ]
**Live-probed?** [ yes — timestamp + curl output attached | no — DO NOT submit ]

---

**Note:** This template exists to make lane decisions explicit and falsifiable. A future engineer should be able to read your completed template and verify the model choice against the EMD lane table.
