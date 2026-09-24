---
name: sovereign-daily-brief
description: "Use when Arif asks 'apa kena buat'. Show F13 binaries."
---

# sovereign-daily-brief — Compose today's plate for F13

> **Doctrine:** Yang Arif nampak = apa yang perlu DIA decide. Bukan semua kerja federation.
> **Class:** Session-start synthesis (sits ON TOP OF session-ops + bijaksana-compile, never duplicates).
> **Trigger phrases:** "apa aku kena buat hari ini", "what do I do today", "what's on my plate", "any decision for me", "ada apa untuk aku?"

## The One Rule

Arif's attention is the most expensive thing in the federation (W₈₈₈). He does not
need a status report. He needs **a filter that returns N≤2 items requiring HIS
decision**, with everything else hidden behind a one-line "agents are doing X".

If the answer reads like a system status page, you have failed. Arif already has
the agents — he is asking what he cannot delegate.

## When to load

Load this skill the MOMENT the user asks any variant of "what do I do today?"
If unsure, ask **once**: *"Maksud hang — apa yang perlu hang decide, atau status
semua? Aku boleh bagi satu atau dua."* — then commit. Do not produce a menu.

## Procedure (do not skip)

**Step 1 — Reject the temptation to compile.** BIJAKSANA already ran (FI-003 / FI-009
overnight or last session). Its output is `/root/work/tasks.json` (v1 schema,
`metabolism.G`, `metabolism.W3`, `tertib_flow`, `tasks[]`). If it does not exist
or is >24h stale, run BIJAKSANA-compile first (delegate to a subagent or load
`bijaksana-compile` and follow its Rule 1-4). Do not silently rebuild it yourself.

**Step 2 — Triangulate three sources, in parallel:**

```
a) /root/.hermes/carry_forward.json       → entries with status='OPEN' (sorted ts desc)
b) /root/work/tasks.json                  → tasks[].outcome_state, tasks[].tier, tasks[].autonomy
c) date '+%H:%M %Z'                       → MANDAAT TEMPORAL — always ground "today"
```

`session-ops` already produced the human-first anchor and time; do not redo it.
`bijaksana-compile` already produced the entropy-ranked manifest; do not redo it.

**Step 3 — Filter with this exact triage before any output.**

For each item from (a) and (b), classify:

| Class | Test | Goes to Arif? |
|---|---|---|
| **F13-BINARY** | tier=T3 OR autonomy='F13 BINARY' OR has "F13 choose" / "F13 binary" / "one choice" in `how` | YES |
| **F13-CLASS** | mentions money, irreversible mutation, canonical record direction change, external port | YES |
| **DECISION-BLOCKED** | an agent is blocked on a human arbitration / 888 ruling / sovereignty question | YES |
| **AUTO** | tier≤T2 AND autonomy='auto-go' AND no human-witness gate | NO (one-line aggregate) |
| **DRAFT-READY** | outcome_state like 'DRAFT_READY*', 'ROOT_CAUSED_*' | NO unless F13-binary above |

A task that an agent can complete without a human in the loop is not on Arif's
plate. Even if it is P0 for the federation, it is invisible to him.

**Step 4 — Apply the count rule.**

If F13 items > 2: pick the **two that block the most downstream work** (highest
`blocks[]` fan-out + highest `entropy_delta`). Defer the rest to "bawah radar"
with the reason. Arif has said it explicitly: *"jika apa-apa arifos/komda
membuat hang membaca = bug middleware."* If your answer makes him read more
than 2 questions, you broke him.

If F13 items = 0: return a **single-line "all agent-lane"** + a SHADOW line for
anything that might become F13 later (heartbeat gaps, draft-ready queues, things
in HOLD). Do not pad with agent chores.

**Step 5 — Format the answer (Penang BM, dense, no ceremony).**

Shape:
```
[Brief one-liner about the federation's overall state — one sentence max]

[For each F13 item, ONE block:]
[Item tag — e.g. "T6 binary"]. [One-sentence context grounded in carry_forward
+ tasks.json]. [ONE binary question — no menu, no options listed unless one is
strictly better]. [Hint of consequence: what it blocks or opens].

[For everything else, ONE line:]
Auto-lane: [N tasks agents are running — list by P-tier if uneven]. [Optional:
one SHADOW line if something needs his eye later, not now.]
```

NEVER:
- list every task
- show G/W3 numbers unless they change the binary
- ask which task he wants to look at first
- produce a (a)(b)(c) menu of choices
- explain how you read the substrate
- restate his own previous orders back at him
- end with "nak handle satu dulu, atau dua-dua?" more than once per turn

**Step 6 — One probe, only if needed.**

If two readings of the substrate would lead to different answers (e.g. tasks.json
shows T6 awaiting F13 binary, but carry_forward shows Arif already chose B
yesterday), probe the older source before answering. Do not guess. If still
ambiguous, state the contradiction in one line and ask the binary.

## Pitfalls

**Pitfall 1 — Confusing the substrate's prioritization with Arif's.**
BIJAKSANA sorts by `entropy_delta` — what most reduces chaos in the federation.
Arif sorts by **what costs him a decision he cannot delegate**. A P0 heartbeat
gap is auto-rollable for an agent; a T3 binary on a disputed surface is not.
Always re-filter by the F13-class table above before listing.

**Pitfall 2 — Echoing the manifest's verdict field.**
`/root/work/tasks.json` carries `metabolism.effective_verdict` (`SABAR`,
`SEAL`, etc.). This is BIJAKSANA's constitutional verdict about the
federation's metabolism — not a judgment about what Arif owes today. Reproducing
it as if it tells Arif what to do is a vocabulary leak (see
`bijaksana-compile` Rule 2 + SCAR-KERNEL-LEGACY-VERDICT-LEAK-002).

**Pitfall 3 — Listing drafts as if they were decisions.**
"DRAFT_READY_AWAITING_JUDGE" looks urgent; the kernel's `arif_judge → arif_seal`
path will execute it without Arif touching anything. If the only blocker is
"agent will execute via judge path," it is AUTO, not F13. The tell: the task's
`autonomy` field says "draft done; execution = kernel judge path, NOT
self-witness." Trust that line.

**Pitfall 4 — Reading carry_forward OPEN-loops as today's queue.**
48 OPEN loops is the chronic backlog, not today's plate. Many are dormant (P3
phantoms, parked work, things awaiting a separate F13 session). Filter by `ts`
recency AND by the F13-class table — a 30-day-old OPEN loop with no F13 touch
is noise, not work.

**Pitfall 5 — Producing the answer from one source only.**
If you only read `tasks.json`, you miss the F13 ruling that landed in
carry_forward yesterday. If you only read carry_forward, you miss the
entropy-ranked order. Both must be read in parallel; the F13-class filter is
the join key.

**Pitfall 6 — Asking the human what he wants to hear.**
"nak handle satu dulu, atau dua-dua?" at the end of an answer is menu-asking in
disguise (violates `KALIBRASI PERBUALAN` item 3). If the answer surfaces 2
binaries, let him answer in any order or all at once — the order does not matter.
Phrase the closing as "Dua soalan tu je atas meja hang" if needed, not as a
choice prompt.

**Pitfall 7 — Missing the temporal dimension.**
"Today" means different things at 08:00 vs 22:00. At 08:00, Arif usually wants
the F13 binaries that block the day's work. At 22:00, he usually wants the
drain/shutdown items + anything blocking his sleep. Probe `date` first (Rule
MANDAAT TEMPORAL) — let the time of day influence the filter even if the
procedure is identical.

**Pitfall 8 — Reciting BIJAKSANA's "tertib_flow" back as if it were guidance.**
`tertib_flow` in tasks.json is the agent execution order. It tells Hermes's
workers what to do next; it tells Arif nothing. Translating it into a
"1-init/observe 2-judge 3-forge..." step list is a category error — those are
agent verbs, not sovereign verbs.

## Reference scars

- **SCAR-BRIEF-OVERFLOW-001** — An early "today's plate" answer listed 7 items
  with (a)(b)(c) menus; Arif's response was silence for 2 hours. The lesson:
  N>2 + menu = invisible. He does not read menus.
- **SCAR-KERNEL-LEGACY-VERDICT-LEAK-002** (inherited from bijaksana-compile) —
  `tasks.json`'s `effective_verdict` field does not tell Arif what to do.
- **SCAR-DRAFT-AS-DECISION-001** — Surfacing a DRAFT_READY item as if it required
  Arif's call, then he sat on it for hours; meanwhile the agent judge's path
  auto-rolled. Never again.

## Workflow

```
Arif: "apa aku kena buat hari ini?"
  ↓
1. date +H:%M (MANDAAT TEMPORAL — affects filter tone, not procedure)
2. Read /root/work/tasks.json  — entropy-ranked manifest
3. Read carry_forward.json     — F13 rulings + OPEN-LOOP filter
4. Apply F13-class table       — keep only F13-BINARY + DECISION-BLOCKED
5. Pick top-2 by blocks[] fan-out
6. Format per Step 5
7. One-line auto-lane summary for the rest
8. ≤ 200 words total in chat
```

## Output shape (canonical)

```
<time-grounded one-liner about federation state, e.g. "11:39 pagi. Malam tadi
FI-003 habis compile, /root/work/tasks.json baru.">

[Item-1 tag]. [Context sentence]. [Binary question]. [Consequence hint].
[Item-2 tag — same shape, OR "Auto-lane: N tasks agents running."]

[Optional one-line SHADOW if something might become F13 later.]
```

## Anti-patterns

- ❌ Listing all 10 tasks from tasks.json
- ❌ Showing G/W3 metrics (those are agent-internal)
- ❌ Producing options (a)/(b)(c) for the user to pick
- ❌ Padding with agent chores as if they were sovereign work
- ❌ Restating Arif's own orders back at him
- ❌ Asking which task to handle first
- ❌ Using "menu" or "soal" as a verb in the closing
- ❌ Re-running BIJAKSANA when a manifest already exists