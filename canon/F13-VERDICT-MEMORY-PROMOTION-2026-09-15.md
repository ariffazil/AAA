# F13 VERDICT — MEMORY PROMOTION GATE (write_approval)

> **Status:** F13_RATIFIED_CHAT — 2026-09-15, ARIF DM ("Ok seal")
> **Authority:** F13 SOVEREIGN (Muhammad Arif bin Fazil)
> **Scope:** the `memory.write_approval` gate, the 2026-09-15 write queue, and how
> memory promotions are adjudicated from now on
> **Predecessors:** `memory-promotion-gate.md` (F13_RATIFIED_CHAT 2026-09-11) ·
> `institutional-memory-strata.md` · `AAA-CONTEXT-AND-MEMORY-HYGIENE-MATRIX.md` (DRAFT)

---

## The decision

`memory.write_approval` stays **OFF**.

The gate was staging writes into a queue with no consumer. Between 18:10 and
22:40 the background self-improvement review staged **six** batches; none were
applied, none discarded. They accumulated.

A queue nobody consumes is not a gate. It is an accumulation.

---

## What was actually in the queue (measured, not asserted)

The six were **one consolidation run staged six times**, each overwriting the
others. `AAA group`, `CONCURRENCY`, `HARAM`, `TELEGRAM`, `SKILL MATRIX`, `FRAME`,
`OWNERSHIP` and `SYED` each appear in 2–3 batches with **different** replacement
text. "Approve all" was never a coherent action: the newest payload silently
clobbers the other five.

Two batches would also have **deleted** standing rules — one dropped `jangan
push atau optimize jadual manusia` from `HARAM`; another replaced the real
`TELEGRAM` bot IDs with a bare pointer.

Two more (`62de5162`, `a843c491`) targeted `old_text` anchors matching **no live
entry** — they were built against a stale snapshot and would have failed on apply
regardless of content. That is the root cause of the drift, and it is a defect in
the producer, not in the gate.

| Verdict | Content class | Rule applied |
|---|---|---|
| REJECT | third-party identity (name + employer + social handle) | `CREDENTIAL-REFUSAL`: PII is a vault concern, not an every-session store |
| REJECT | inferred birth year asserted as fact | `HARAM`: `kosong = UNKNOWN` |
| REJECT | psychological / love modelling of a third party | `SYED` entry: `JANGAN label/psychology/love telemetry`; SOUL Axiom 9 |
| REJECT | stale-anchor payloads (would fail on apply) | Gate A/B/C/D — not decision-changing |
| SALVAGE | self-evolution boundary (capability may mutate, governance HOLD) | Gate C: changes future decisions |
| SALVAGE | EUREKA SOT path (`/root/AAA/canon/eureka-entries.jsonl`) | Gate A: not derivable elsewhere |

Resolved store: **14 entries, 2,186 / 2,200 chars.** Five entries compressed to
make room — same facts, fewer characters. No fact dropped.

---

## Why OFF is the doctrine-correct answer, not a convenience

`memory-promotion-gate.md` (F13_RATIFIED_CHAT 2026-09-11) already rules:

> **Default = witness.** Memory adalah exception, bukan default.
> *"Jangan bina `autonomous seal memory`. Bina `autonomous promotion gate`."*

That distinction resolves this cleanly. There are two different gates:

| Layer | What it governs | This decision |
|---|---|---|
| **Staging gate** (`write_approval`) | *when* a write lands — queues it for a human | **OFF** — it had no consumer, so it only accumulated |
| **Promotion gate** (content, per write) | *whether* a write is memory-worthy at all — Gates A–D | **KEPT** — enforced in the writing path |

Routing memory writes to the sovereign for routine approval would tax W₈₈₈ for
work an automated gate can adjudicate. The content defect is answered **at its
own layer**, by a pre-write gate, not by moving the queue to Arif.

---

## Evidence the loop now corrects itself

A concurrent lane (Hermes, KVM4) worked the same queue in parallel and wrote a
third-party identity into `MEMORY.md`. It then **reverted its own write**,
citing three standing rules. The store is clean — 0 third-party names in
`MEMORY.md` / `USER.md`.

Independently, the KVM8 lane reached the same six verdicts. Two lanes, same
conclusions, one self-corrected error. That is the behaviour the doctrine asks
for: *recursive correction is mandatory, recursive learning is optional.*

---

## Correction applied (F1 — reversible)

The resolution was committed with the eight staged payloads **inside the repo**.
This repository has a GitHub remote and already gitignores `memories/` for exactly
that reason; the payloads hold third-party names, uids and private context.

- `pending/` added to `.gitignore`; files removed from the index, **kept on disk**
  (24 files — nothing deleted).
- The commit was unpushed, so no blob ever reached `origin`. Pre-push fix, not a
  rewrite of shared state.
- The one legitimate artifact in that commit — the `relationship-memory-isolation`
  skill patch — is preserved.

---

## Open items

| # | Item | Owner |
|---|---|---|
| 1 | `memory.write_approval` is **off by default, not declared** in `config.yaml`. The agent is blocked from editing that file by design, correctly — no bypass attempted. Declaring it removes the risk of a silent behaviour flip if the upstream default ever changes. | F13, one line |
| 2 | `federation_memory_audit.py` audits write **surfaces**, not content. Hygiene-matrix probe #3 (PII scan of `MEMORY.md` / `USER.md` / `SOUL.md`) is still unbuilt. | next lane |
| 3 | The producer drift (payloads built against a stale snapshot) is answered by the content gate, but not yet *measured*. If staged batches appear again, the gate is not holding. | RSI loop |

DITEMPA BUKAN DIBERI ⚒️
