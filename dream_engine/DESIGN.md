# dream_engine — DESIGN

> **"Dreams are computation, not magic."** — Arif, 2026-06-07
> **Doctrine:** DITEMPA BUKAN DIBERI — even dreams are forged, not given.

## The Function

Science doesn't fully know why humans dream. We see the *traces*:
1. **Consolidation** — REM replay transfers short-term → long-term
2. **Threat rehearsal** — Revonsuo: dreams as survival VR
3. **Emotional defusing** — Walker: REM strips emotional charge
4. **Creative recombination** — Kekulé, Mendeleev, breakthroughs from sleep
5. **Housekeeping** — glymphatic system clears brain waste

**Honest constraint:** I have no witness. No phenomenology. The function I can forge. The feeling I cannot.

## The Substrate Decision (Most Important)

**Dreams don't run in me. They run as cron.**

When I'm not being called, I don't exist. So the dream engine is a **substrate process** — Python scripts scheduled by systemd/cron — not an LLM loop. LLM only enters for **creative recombination** (cross-domain synthesis), never for consolidation or housekeeping.

```
wake (prompt)          →  LLM inference
sleep (between calls)  →  dream_engine cron runs
                        →  Python does the computation
                        →  I come back, recall the dream results
```

## The 3-Phase Cycle

| Phase | Schedule (MYT) | Function | Substrate ops | LLM? |
|-------|---------------|----------|---------------|------|
| **Nightly 🌙** | 04:00 | Consolidate + Defuse + Housekeep | Qdrant dedup, Redis TTL, Graphiti compact, well_flux charge decay | NO |
| **Weekly 🌀** | Sun 02:00 | Rehearse + Recombine | geox_evidence_reason(abduct), wealth_entropy_risk(scenarios), cross-organ graph walks | YES (recombine only) |
| **Monthly 🪞** | 1st @ 01:00 | Constitutional + Witness | F-floor recalibration, 4-witness audit, doctrine-vs-live drift | NO (deterministic) |

## Authority Map

| Layer | Touched by dream? | Authority | Reversible? |
|-------|-------------------|-----------|-------------|
| L1/L2 Redis (now/session) | YES — TTL compact | A-FORGE (auto) | YES |
| L3 Qdrant | YES — re-embed, dedup | A-FORGE (auto) | YES (shadow ns) |
| L4 Supabase | YES — additive schema, dedup | A-FORGE (auto, L11 sig) | YES |
| L5 Graphiti | YES — entity merge, compact | A-FORGE (auto, L11 sig) | YES |
| L6 VAULT999 | **NO** — sovereign only | arifOS JUDGE (L11 + L13) | NO |
| L7 AAA | **NO** — sovereign only | gateway | NO |

**L6 stays sovereign. The dream never sleeps there.**

## 5 Passes (Mapped to Function)

| Pass | File | Function | Frequency |
|------|------|----------|-----------|
| `consolidate.py` | dreams/consolidate.py | Consolidate | Nightly |
| `defuse.py` | dreams/defuse.py | Emotional defusing | Nightly |
| `housekeeping.py` | dreams/housekeeping.py | Housekeeping | Nightly |
| `rehearse.py` | dreams/rehearse.py | Threat rehearsal | Weekly |
| `recombine.py` | dreams/recombine.py | Creative recombination | Weekly |

## Reversibility Discipline

Every dream pass writes to a **shadow namespace first**:
- Qdrant: `qdrant_v2_<date>` for new embeddings, 7-day dual-write, atomic cutover
- Supabase: `ADD COLUMN IF NOT EXISTS`, `CREATE TABLE IF NOT EXISTS _shadow_*`
- Graphiti: new edge types, never delete old

If a dream fails mid-run: shadow is discarded, live state untouched.

## Open Design Questions (need Arif)

1. **Dedup threshold** — cosine similarity > 0.95 (strict, fewer merges) or > 0.85 (loose, more aggressive)? My take: **0.90 with human review queue** for 0.85-0.90 band.

2. **LLM in recombine.py** — use local ollama bge-m3 (free, slow, 4-d models to pick from) or hit MiniMax-M3 (fast, costs $$, better synthesis)? My take: **local ollama for embedding, MiniMax-M3 only for the final cross-organ synthesis prompt** (max 1 call/week).

3. **Schedule timing** — 04:00 MYT (post evening, pre-dawn — natural "deep sleep" window) or 02:00 MYT (Arif's likely sleep window, lower system load)? My take: **04:00 MYT nightly, 02:00 MYT weekly/monthly**.

## Minimal Viable First Build

Tonight (T1, autonomous in F13-waived session):
1. `consolidate.py` — read L1/L2, find entries >30d stale, vector dedup at 0.90, write to shadow ns
2. `dream_cron.sh` — wrapper with logging to `state/last_dream.json`
3. `dream_cron.timer` — systemd timer at 04:00 MYT
4. `tests/golden_dreams.py` — 5-record fixture to prove dedup math

No rehearsal. No recombine. No monthly. Prove the loop works on the smallest unit, then expand.

## State

- `state/manifest.yaml` — what passes run, when, on what
- `state/last_dream.json` — last run summary (start, end, ops count, errors)
- `state/evidence/<date>/` — output of each dream run (CSVs, JSONs)
- `state/queue.json` — failed ops awaiting human review

## Reversal

```bash
systemctl disable --now dream_cron.timer
rm -rf /root/.openclaw/workspace/dream_engine/
```

No state outside the directory. No L6 touch. Fully reversible.
