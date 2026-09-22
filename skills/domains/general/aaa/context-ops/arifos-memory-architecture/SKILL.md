---
name: arifos-memory-architecture
description: "How memory flows across the arifOS federation — arif_memory (kernel L1–L6 governor), forge_memory (A-FORGE VAULT999 read), and HANG INGAT BALIK / PRL (precedent recall injected into reasoning)."
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# arifOS Memory Architecture

Understand and answer how the federation remembers. Three systems, one spine:
VAULT999 (L6) is always the terminal surface; the judge is always the court;
F1–F13 gate every write/read once. **No organ writes the memory substrate
directly** — every organ calls the kernel's single interface, and the kernel
fans out.

## 1. arif_memory — kernel memory governor (:8088, 555_MEMORY, alias arif_memory_recall)

- SINGLE write interface for ALL organs (doctrine: `FEDERATION_MEMORY_CONTRACT.md`).
  GEOX/WEALTH/WELL/A-FORGE call `arif_memory(mode="store", actor_id, session_id, ...)`.
  Provenance actor_id+session_id is MANDATORY (F11) — missing → hard-block.
- Three-leg write (mode="store"): L3 Qdrant (`bge-m3` 1024-d, coll `arifos_memory`)
  = REQUIRED, failure ⇒ `stored=False`; L4 Postgres/Supabase = durable, warns only;
  L5 Graphiti = advisory, never blocks, never auto-woken (888 owns).
- M-modes: recall, inspect, attest, remember, promote, revise, forget, audit.
  **forget = IRREVERSIBLE → F13** (soft-delete for M0–M2, tombstone for M3/M4).
- M-tiers M0–M4 computed, not caller-set. M3/M4 (sacred) require 888. Hard law:
  `can_authorize_action` ALWAYS false at store — authority granted at recall by
  sovereign/judge, never by memory itself. No secrets in L3 vectors.

## 2. forge_memory — A-FORGE VAULT999 read (:7071, OBSERVE)

- NOT a memory governor. Read-only recall into L6 VAULT999 (the immutable log).
- mode=recall reads VAULT999 local ledger files, falls back to vault999-api.
- Reads *sealed receipts* (done, hash-chained), not semantic vectors.
  No M-tier, no fan-out, no governance — raw ledger retrieval.

## 3. HANG INGAT BALIK — PRL / Precedent Recall Layer

PRL is NOT ordinary recall — it's structural constraint injection BEFORE
reasoning. F9-compliant: the model does not "remember"; a governing variable
is force-injected ahead of the LLM.

Pipeline:
```
VAULT999 (outcomes.jsonl, ~255 seals)
  → vault_vectorizer.py  (parse action/metadata/verdict/blast_radius → embed bge-m3 768-d)
  → Qdrant collection arifos_precedent
  → PrlGate.interrogate()  (dual gate, prl_gate.py)
  → prl_emd_hook → arif_think mind_reason.py (~line 348, "PRL Phase 1")
```
Dual-Gate:
1. Payload-filtered cosine search — precedent must share the query's blast_radius
   (L1_LOCAL/L2_SYSTEM/L3_CRITICAL) ⇒ autoimmune, L1 never sees L3.
2. Ω₀ ambiguity failsafe — geometric match + contextual ambiguity ("but also",
   "depending on", "maybe") ⇒ F1 HOLD (PRL_OMEGA0_HOLD).
Output: `[PRL CONSTRAINT]` block (blast radius, seal_id, governing rule) prepended
at END of the reasoning prompt (recency-bias hardening).

### Zen memory names (map to layers)
- VAULT999 = HANG SIMPAN (stored) · Qdrant = HANG LETAK (placed) ·
  telemetry = HANG TIMBUN · Judge = HANG FIKIR DULU ·
  A-FORGE = HANG BUAT · PRL = HANG INGAT BALIK (remember back)

## Verification recipe (run in kernel env — NOT /root python)
```bash
cd /opt/arifos/app && /opt/arifos/venv/bin/python - <<'PY'
import json, asyncio
from arifosmcp.prl import PrlGate
g = PrlGate()
print(json.dumps(g.health(), indent=2))
r = asyncio.run(g.interrogate("deploy migration to prod", enable_omega0=False))
print("verdict=", r.verdict, "count=", r.match_count, "br=", r.query_blast_radius, "ms=", round(r.search_ms,1))
PY
```
Live 2026-08-13: collection arifos_precedent, point_count=255, tau=0.35,
interrogate("deploy migration to prod") → PRL_MATCH, 3 constraints, L2_SYSTEM, ~21ms.

## Pitfalls / drift notes
- **PATH DRIFT:** Dream Engine outputs exist at two paths — `/root/AAA/dream-engine/wisdom.md` (stale, 18 days old) and `/root/AAA/knowledge-graph/dream-engine/wisdom.md` (canonical, fresh). The old path is now a symlink. Always `stat` or `ls -la` before claiming a file's date. Path drift is a recurring federation pattern: docs point to archived locations while the real file moved. The 2026-09-12 normalization report fixed dream-engine skill references but missed the distiller output path.
- **TAU DISCREPANCY:** prl_gate.py docstring says "τ ≥ 0.95" but the constant
  `PRL_TAU_THRESHOLD = 0.35` (vault_vectorizer.py:46) is what the gate import uses.
  Doc is stale; code value wins. Report the live value, flag the drift.
- **DORMANCY IS RESOLVED:** old scar said "PrlGate auto-applies blast_radius filter
  but points have blast_radius=<NONE> → zero silent matches." The gate now has a
  Step-2b fallback (filtered 0 → retry unfiltered) and points carry blast_radius.
  Do NOT re-claim "PRL dormant/broken" — probe before asserting (F2 TRUTH).
- mind_reason.py swallows PRL exceptions (`except Exception: pass`) — PRL failure
  degrades to standard reasoning silently; don't read it as an outage.
- Probe style lesson (scar 'hantu audit'): answer arifOS "how does X work"
  questions by reading code + live probe in `/opt/arifos/app` with
  `/opt/arifos/venv/bin/python`, not by reciting memory or /root python.
  The probe corrected a stale "dormant" belief this session.

## The pending-proposal redemption (apex-zen execution, proven 2026-09-15)

Hermes stages background-review memory writes for approval (`~/.hermes/pending/memory/*.json`);
they accumulate silently — 122 proposals / 279 operations in 5 days on KVM8, ~10 of them being
the SAME consolidation re-derived. **Never replay the pile.** Replaying N generations of the same
edit is not curation, it is entropy: later batches reference `old_text` that earlier batches
rewrote, so order-dependent replay corrupts memory while reporting partial success.

The procedure that works, in order:

1. **Archive verbatim first.** `memory-promotion-gate` forbids silent discard — a failed gate
   means *compress to a ledger*, not delete. Dump every proposal to a dated registry file
   before touching anything. (Discarding deletes the JSON files; the archive is the only proof.)
2. **Measure the redundancy, then say it out loud.** Group by theme; if one line is proposed
   N times, the transfer is distillation, not accumulation. Count before you curate.
3. **Distill ONE final state** against the four gates (Derivation · Deletion · Decision ·
   Novelty). Write it with the memory tool (which enforces the char budgets: MEMORY 2200, USER 1375,
   config `memory.memory_char_limit` / `user_char_limit`).
4. **Apply the memory map boundary:** MEMORY.md = agent behaviour/scars/governance; USER.md =
   the sovereign's substrate. An agent rule that lands in USER.md, or vice-versa, drifts.
5. **Discard** the staged rows through the sanctioned path (`tools.write_approval.discard_pending`,
   the same call `/memory reject` makes) — after step 1, never before.

**The filter that makes it "wisdom" rather than "facts":** drop-duplicate consolidations (gate A),
doctrine that already lives in canon fragments or a skill (gate A — canon auto-loads; memory rent
is not paid twice), transient session state (gate C — wallet totals, appointment logistics, a
board snapshot), raw PII as prompt-injected text (F1 leak surface — the vault is its home), and
psychological interpretation of the sovereign or his people (SOUL + relationship-kernel: state is
not fact, no love telemetry). Keep the ACTIONABLE RULE, drop the DIAGNOSIS: "witness only, never
pry" survives; "his grief is unresolved" does not.

**Falsifiable test:** the staged store is empty AND no re-consolidation of a retained line
re-appears within 7 days. A re-appearance is not a memory bug — it means the boundary is missing
upstream (the review re-deriving what canon already holds). Fix that, not the pile.

Receipts of record: `/root/AAA/registries/memory-redemption-ledger-2026-09-15.md` +
`memory-pending-archive-2026-09-15.json`.

## Support files