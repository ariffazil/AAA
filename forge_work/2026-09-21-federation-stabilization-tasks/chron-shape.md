# CHRON SCHEMA OBSERVATION — 2026-09-21

> **Status:** observation only · T0 · FI-008
> **Source:** `/root/chron/data/episodes.jsonl` (live)
> **Trigger:** user noted "the field is `function`, not `step_type` — schema drift"

## Field reality (live, not memory)

The `function` field IS populated. Distribution from 55,794 episodes:

| `function` | count | % |
|---|---|---|
| `observe` | 55,770 | 99.96% |
| `predict` | 16 | 0.029% |
| `verify` | 6 | 0.011% |
| `learn` | 2 | 0.004% |

Compared to earlier report (this session's chat prior):
- Total: 55,794 (was reported 53,263 → grew by 2,531)
- predict: 16 (same)
- verify: 6 (was reported 5 → +1)
- learn: 2 (was reported 1 → +1)

**CHRON learning loop progress: real but tiny.** verify went 5→6, learn went 1→2. Two new lessons in this observation window.

## Sample fields per kind

```
observe  episode_id=chron-ep-...-observe-5188cff5
         fields=['actions','audience','claims','decisions','episode_id','function',
                 'known_at','observations','observed_at','outcomes','output_decision',
                 'predictions','principal','provenance','question','receipts',
                 'rejected_signals','renderer_used','selected_signals','valid_time']

predict  episode_id=chron-ep-...-predict-8b22b282
         (same field set as observe; `function='predict'` discriminator)

outcome  episode_id=chron-ep-...-verify-cd1fff27
         fields=same + causal_predecessor, parent_episode_ids, temporal_hash,
         valid_from (extra lineage anchors for verifications)
```

## Verdict on the "schema drift" question

**The data is already structured correctly by `function`.** The user's earlier "schema drift" observation was right that:
- The canonical lifecycle schema names `step_type`
- CHRON's actual schema names `function`
- These are aliases, not duplicate classifications

**No data migration needed.** The fix is documentation/semantic: rename the field (or add `step_type` as an alias view) so downstream tooling can use the canonical name.

## Migration proposal (T2 — requires user veto)

**Option A — Rename `function` → `step_type`:**
- Pros: canonical name matches doctrine
- Cons: touches every consumer of CHRON episodes
- Risk: medium (reversible via backup)

**Option B — Add `step_type` as derived/aliased field:**
- Pros: backward-compatible; consumers can adopt canonical name progressively
- Cons: temporary schema divergence
- Risk: low (additive)

**Recommendation: Option B.** Alias, not rename. Backward-compatible. Allows consumers to migrate on their own schedule.

## Next steps (gated)

- A5 (this observation) → COMPLETE
- B3 (migration) → ANNOUNCE with 10s veto window
- D-stream: temporal learning closure (G9) — deferred, needs many verified outcomes first
