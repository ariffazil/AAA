---
name: federation-memory-writeback
description: "Use when persisting session findings to memory."
version: 1.0.0
author: hermes
metadata:
  hermes:
    tags: [memory, carry-forward, eureka, qdrant, arifflow, session-close, federation]
    related_skills: [arifos-memory-architecture, memory-manage]
---

# Federation Memory Writeback

Where a session's **own findings** get written. This is not `arif_memory` (that is the
kernel's organ-state governor) — these are the four surfaces for working output: decisions,
scars, retrieval knowledge, and causal chains.

Choose the surface by the **kind** of thing you produced. They are not ranked substitutes.

| What you produced | Surface | Durability |
|---|---|---|
| Work state, decisions, scars, open loops | generational carry-forward | permanent for `decision`/`scar`/`eureka`/`directive`; 7-day prune for `event` |
| A ratified insight worth canon | eureka SOT — **sealed, stage instead** | pending F13 |
| Domain knowledge to retrieve by meaning | Qdrant collection | permanent |
| Causal chain of what led to what | arifFlow reality graph | append-only ledger |

## 1. Carry-forward — the default surface

`/root/scripts/carry_forward.py` (schema `arifos.carry_forward.v3`). Never hand-edit the JSON:
the writer takes `flock` and snapshots a backup on every mutation. Two concurrent sessions
overwrote each other once — that is why the lock exists.

```bash
python3 /root/scripts/carry_forward.py show          # schema, generation, kind counts, open loops, writers
python3 /root/scripts/carry_forward.py append --agent hermes --kind decision --content "..." --tags a,b
python3 /root/scripts/carry_forward.py anchor --name "session/close" --agent hermes --state '{"k":"v"}'
python3 /root/scripts/carry_forward.py loop --list
python3 /root/scripts/carry_forward.py loop --close SUBSTRING --by hermes --note "..."
```

- Kinds: `decision` · `scar` · `open_loop` · `eureka` · `directive` · `event`.
- `decision`/`scar`/`eureka`/`directive` are permanent; `event` auto-prunes after 7 days. Anything
  that must survive goes in a permanent kind — events keep only the narrative.
- Your writer id must be in the `writers.allowlist` or the append is refused. Check `show` first.
- Put an entry's topic in `--tags` so the next session can filter instead of reading the whole file.

**`open_loop` is the load-bearing kind.** One entry per unresolved question, carrying *why it
matters* — not a summary of what happened. Writing the entry is cheap; the whole value is that
the next session picks up the unfinished item without re-deriving it.

**Close with an anchor.** `anchor --name "session/close"` is the ritual. Put artifact paths, the
open loops handed forward, and the skills you patched into its `--state` JSON. An anchor without
the open-loop list is half a close.

## 2. Eureka — the ratified registry is sealed; the live feed is where you write

**Two ledgers exist. Write to exactly one of them.** Verified on disk 2026-09-19 with `lsattr`:

| ledger | what it is | attribute | rows · last written |
|---|---|---|---|
| `/root/AAA/eurekas/eureka-entries.jsonl` | **LIVE FEED — the write target** | writable, no immutable flag | 14 rows · 2026-09-18 |
| `/root/AAA/canon/eureka-entries.jsonl` | **FROZEN RATIFIED REGISTRY** — historical authority; cite it, never write it | immutable; a plain append raises `PermissionError: [Errno 1] Operation not permitted` even as root | 109 rows · 2026-09-16 |

Do not lift that lock. It is a deliberate governance boundary, and the constitutional gate will
block any shell command referencing a lock-modifying operation before it reaches the shell. That is
correct behaviour, not a bug — and it is also why the canon ledger cannot be the write target: an
instruction that names it can never execute, no matter how often it is retried. Promotion into the
canon tree, where it ever happens, runs through the kernel seal lane, not an agent action.
Treat the block as an instruction, not an obstacle.

Stage the candidate instead:

- Write `/root/AAA/eurekas/<EUREKA-ID>.md` with a status header naming the blocker, the canon
  target path, and the fact that the lock is untouched.
- Report the true state to the human: `STAGED — PENDING F13 CANON PROMOTION`. Promotion runs
  through the kernel seal lane; it is not an agent action.
- Prefer `eurekas/` over `okf/`, `docs/eureka/`, or a second `eureka-entries.jsonl`. If you find a
  second ledger beside a `NON-CANONICAL.md`, read that marker before writing: it states which ledger
  is the frozen registry and which is the live feed. The one in `eurekas/` is the live feed and the
  correct target; the one in `canon/` is immutable.

## 3. Qdrant — retrieval by meaning

`bge-m3` (1024-d) is served by Ollama on the **inference node**, not the truth node:
`http://100.64.0.5:11434/api/embed`. Confirm the collection's vector size with
`GET /collections/<name>` first — a dimension mismatch fails the whole batch.

Two shape traps on the REST API:

```bash
# Upsert MUST be PUT. A POST to the same path returns 400 "missing field `ids`".
curl -X PUT 'http://127.0.0.1:6333/collections/<c>/points?wait=true' \
  -H 'Content-Type: application/json' \
  -d '{"points":[{"id":N,"vector":[...],"payload":{...}}]}'

# Read points back by explicit id to verify — never assume the batch landed.
curl -X POST 'http://127.0.0.1:6333/collections/<c>/points' -H 'Content-Type: application/json' \
  -d '{"ids":[N,N+1],"with_payload":true,"with_vector":false}'
```

- Allocate ids above the current max (`scroll` with a limit, take the max). Do not reuse ids.
- Include `epoch` and `organ` in every payload so a later audit can tell which session wrote a point.
- **Delete your own probes.** A test vector inserted while debugging a 400 is indistinguishable
  from canon content on the next read. Delete it explicitly
  (`POST /collections/<c>/points/delete?wait=true`) and confirm the count — do not leave a
  `"category":"test"` point in a collection the human will search.

## 4. arifFlow reality graph — causal edges

`POST http://127.0.0.1:7073/ingest`. `GET /health` returns the Flow Quotient and per-actor
verdicts — useful as a self-audit at close.

- `receipt_id` must be a **UUID**. A readable string is rejected with `UUID parsing failed`.
- Required fields: `receipt_id`, `created_at`, `actor_id`, `session_id`, `step_type`,
  `step_number`, `cost_ns`, `epistemic_label`, `floor_verdict`, `cooling_decision`, `summary`,
  `routed_organ`, `entry_kind`.
- **`step_type` is a closed enum**: `Execute` · `Verify` · `Cool` · `Seal` · `Barrier` · `Merge` ·
  `Route` · `Abort`. Intuitive words — `Observe`, `Analyze`, `Decide`, `Act`, `Plan` — all return
  400 `unknown variant`. Map onto the real verbs: `Execute` for work produced, `Verify` for each
  audit pass, `Merge` for consolidation, `Route` for a decision handed onward.
- **Chain the edges** by passing the previous `receipt_id` in `parent_receipt_ids`. The parent
  link is the entire point: a pile of receipts with no parents is an event log, not a causal
  ledger, and cannot answer "what led to this".

**Read the Flow Quotient back.** `GET /health` returns a per-actor `quotient` and a `verdict`
(`FLOWING` / `STUCK`). Many `Execute` steps against few `Verify` steps reports execution
dominance — the meter telling you the work went out unverified. Treat it as a finding about your
own process, not as telemetry to skip.

## Close-out order

1. `carry_forward.py append` the typed entries (permanent kinds first), then the anchor.
2. Stage the eureka candidate if the session produced one.
3. Upsert retrieval points; read them back; delete any probe.
4. Write the reality-graph chain last, so it can reference the artifacts by path.
5. Re-read every surface (`carry_forward.py show`, flow `/health`, the Qdrant count) and report
   the true state of each — **including any that is down or was refused**.

## Pitfalls

- **Never report a surface as written when the write was refused or partial.** A blocked surface
  reported as done is worse than one reported as blocked. Name the surface, the operation, and
  the blocker.
- **Do not replay a backlog of staged memory proposals.** Replaying N generations of the same
  edit is entropy, not curation — later batches reference text earlier batches already rewrote,
  so order-dependent replay corrupts while reporting partial success. Archive, distil ONE final
  state, then discard through the sanctioned path.
- **Do not write the same fact to two surfaces "for safety".** One fact, one owner. Pick the
  surface by kind and let the others alone.
- **Do not ".last"-stamp state you did not verify.** The arifFlow edge state file records the
  receipt id and body hash of an accepted ingest; writing it on a failed call makes a subsequent
  parent-link resolve to nothing.

## Related

- `arifos-memory-architecture` — the kernel-facing model (`arif_memory` L1–L6, `forge_memory`,
  PRL precedent recall). This skill covers session writeback; that one covers how the federation
  recalls.
