# 02 — G3 Package Draft: Federation Inbox (Corrected)

> Judge sequence item 2 · **DRAFT for 888_HOLD review** · 2026-09-12 · 333-AGI
> Status: **NOT approved for build.** No daemon · no cadence mutation · no autonomous expansion. G4 remains HOLD (item 3).

## 0. Record correction (evidence)

An endorsement claimed *"OpenCode already has auto-dream.ts producing dream_proposal.jsonl; the gap is ingest-only."* **Falsified by probe (2026-09-12):**

| Claim | Ground truth |
|---|---|
| `auto-dream.ts` exists | Not found anywhere; the dream-engine skill itself tags it `# ARCHIVED (mimocode never built)` |
| `dream_proposal.jsonl` is produced | No such file on disk |
| A producer exists | Only `/root/A-FORGE/scripts/auto-dream-spool.ts` — a **33-line stub**: its comment claims a Supabase read; the body reads nothing and writes `{facts_count: 0, proposals: []}` |
| Inbox ready | `/var/spool/arifos/dream-proposals/` exists, **empty** (created 2026-07-25) |

**Consequence:** Phase 1 = **producer + ingest**, not "wire an inbox." Sequencing corrected accordingly. This is the fourth same-session instance of prose-exceeding-filesystem; see `03-DREAM-ADMISSIBILITY-BRIEF.md` §3.

## 1. Deliverable chain (corrected)

| Step | Deliverable | Definition of done | Gate |
|---|---|---|---|
| **P1 (blocking)** | **Schema alignment** | `dream_engine/dreams/consolidate.py` (L232/250/251) references table `arifosmcp_memory_records`; canonical migration `arifOS/arifosmcp/migrations/001_memory_schema.sql` defines `memory_records` (PK `memory_id`). Align code ↔ schema (or document an intentional view). | dry-run verified; no prod write |
| **P2** | **Producer (replace stub)** | Real producer: read `memory_records` (24h window) → emit schema-valid `dream_proposal.jsonl` → spool. Recommended: upgrade `/root/A-FORGE/scripts/auto-dream-spool.ts` (existing iron). OpenCode emitter deferred — there is no `auto-dream.ts` to extend. | dry-run emits valid JSONL; zero canon writes |
| **P3** | **Inbox ingest (read-side)** | Nightly coordinator reads spool → validates → dedupes → **stages** (Supabase `dream_proposals` staging table OR filesystem staging) → **arifFlow receipt** → surfaces for human/888 review. **Never auto-promotes to canon.** | ingest of a fixture file; receipt minted; rollback confined to spool + staging |
| — | Phase 1 complete | P1+P2+P3 green under review | 888_HOLD cleared by F13 |

## 2. Proposal record schema (draft v0.1)

```json lines
{"proposal_id":"dp-<producer>-<ts>","producer":"aforge/auto-dream-spool","created_at":"ISO-8601","cycle":"dream-<id>","source_refs":["<memory_id>"],"statement":"<one falsifiable sentence>","evidence":["..."],"counterfactual":"<what would falsify>","confidence":0.0,"floors_touched":["F2","F7"],"reversibility":"reversible","status":"proposed"}
```

Rules: one proposal per line · `statement` must be falsifiable (F2) · no raw user content beyond `source_refs` (F6/F12) · producer identity mandatory (F11).

## 3. Ingest contract (draft)

1. Read spool files atomically; move to `processed/` only after receipt. Never delete unprocessed input.
2. Validate: schema + size caps + dedupe against staging.
3. Stage only; mark `status=staged`; emit one arifFlow receipt per batch.
4. Review surface: 888 / human queue. Promotion to canon = the existing F13-locked path only.
5. **Fail-closed:** schema-invalid → quarantine + alert. Never silent drop.

## 4. Non-goals (HOLD constraints)

- No new daemon; no timer/cadence changes; no OpenCode/OpenClaw wiring this phase.
- No direct canon writes by any dream pipeline.
- No Supabase mutations beyond staging (and only after P1 verified).
- G4 (multi-agent dream ecology) untouched.

## 5. Acceptance tests (for the future build — none executed now)

- **T1** fixture JSONL → ingest → receipt + staging entry; spool file moved.
- **T2** malformed line → quarantined, run continues, alert raised.
- **T3** duplicate proposal → single staging entry.
- **T4** rollback drill → staging + spool artifacts removed; no residue.
- **T5** schema-hash match between producer output and validator schema.

## 6. Rollback

- Spool: filesystem move/delete of spool entries only.
- Staging: delete staging rows (staging only) or drop staging table.
- Zero canon/vault interaction in scope → no vault rollback needed.

## 7. Open decisions for reviewer (recommendations, not bounced back)

1. **Producer location:** A-FORGE script (recommended — existing stub, existing iron) vs OpenCode-native (deferred).
2. **Staging store:** filesystem spool + receipt (recommended, Phase 1) vs Supabase staging table.
3. **Daily cap:** reuse dream-engine global cap; producer emits, coordinator enforces. Numbers = F13 territory.

---
*Correction provenance: FI-003 endorsement falsified by filesystem probe (§0); consistent with the judge memo's "the map exceeding the territory" and the APEX-audit "write-price collapse" pattern. This draft is a candidate package only — no authority claimed, no hold cleared.*
