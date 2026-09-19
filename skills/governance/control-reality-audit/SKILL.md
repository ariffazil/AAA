---
name: control-reality-audit
description: "Use when auditing whether a control actually controls."
version: 1.0.0
owner: AAA
category: governance
tags: [audit, controls, gates, hooks, enforcement, evidence, dead-ends]
floors: [F2, F4, F11, F13]
autonomy_tier: T1
---

# Control Reality Audit

> **One line:** a control exists only if it can **withhold** the action it claims to govern. A control described in a document is a description of a control.

**Load when:** the principal asks which gates are theatre; an agent reports being blocked repeatedly and cannot finish work; a governance surface, monitor, hook, cron job or ledger is about to be trusted; an audit result is about to be reported as clean.

**Authority boundary:** read-only. This skill produces findings and one binary for the principal. It never repairs what it audits — the repair is a separate authorized act, and the audit's credibility depends on not being the same actor. A control locked immutable is not unlocked to fix it; that lock is the receipt a human authorized the change, and breaking it to make a correction is self-issued authority.

---

## 1. The classification — apply to every control

| Class | Test | Meaning |
|---|---|---|
| **THEATRE** | cannot withhold, ever | always exits 0 · advisory-only · dry-run by default · no caller · records and proceeds |
| **DISABLED** | could withhold, is configured off | off in config, or behind a flag/env var nothing sets |
| **BROKEN** | crashes or never executes | syntax error, missing module, unset shell variable, wrong path |
| **REAL** | can and does withhold | a *recorded* block exists, with a timestamp |
| **UNPROVEN** | no evidence either way | the default when you cannot show it |

Default to **UNPROVEN**. `"nothing failed"` is not `"it works"` — a control that cannot fail produces no failure signal by construction, so its silence carries no information.

## 2. The four liveness tests — run all four, per instrument

```bash
python3 -m py_compile <script>              # 1. DOES IT RUN AT ALL?
grep -n 'exit\|return' <script>             # 2. CAN IT RETURN NON-ZERO?
grep -rn "<script-basename>" /root \
  --exclude-dir=.git --exclude-dir=node_modules   # 3. DOES ANYTHING CALL IT?
ls -l <output-artifact>; stat -c %y <log>   # 4. HAS IT EVER PRODUCED OUTPUT?
```

- **1 → 2** is the whole game: an instrument that fails #1 has **never run**, and one that fails #2 has **never refused**. A guard that always exits 0 cannot guard.
- **#3**: a control with zero executable callers is a **document**, not a control — unless a human runs it by hand, in which case its own description must say so. Prose references inside other docs are not callers.
- **#4** via mtime and its own output artifacts, never by running it. If the trigger file is written by the very probe you are running, its mtime is not liveness evidence — disclose that.
- A scheduled audit that prints a critical verdict on every run while containing zero exit statements is the loudest theatre there is: maximum alarm signal, minimum consequence.
- A guard whose refusal requires an opt-in `--strict`/`--enforce` flag that no caller passes is a brake nobody pulls.

## 3. The DEAD END test — the finding that wastes agent work

A gate that can withhold but offers **no documented, actionable unblock path** is worse than no gate: it consumes work, returns nothing, and teaches the agent to retry.

Ask, for every gate that can hold:

- **Is the hold PERSISTED?** If holds exist only in memory or ephemeral logs, the agent has nothing to cite, will re-derive the same state, and will be held again.
- **Does a code path exist to release it?** Search for the appeal/unhold/override function, not the docs that promise one. An appeal registry held in memory, with a comment saying it *would* be persisted in production, is a phantom.
- **Does the gate name its own unfixability?** A gate that reports no override is available is a **dead end by design** — rank it high.
- **Is anything held right now with no way out?** Live-held actors with no unhold function go at the top of the report.

**Rule:** unresolved holds are not safety. Separate *can withhold and can be answered* (REAL) from *can withhold and cannot be answered* (DEAD END). The second class is what makes an agent useless.

## 4. The JOIN test — receipts

A receipt that carries a **field** is not a receipt that carries the **function**. The trace/join id must actually join.

```bash
jq -r '.trace_id // "NULL"' <ledger>.jsonl | grep -c '^NULL$'   # how many are empty
jq -r '.trace_id // "NULL"' <ledger>.jsonl | sort | uniq -c | sort -rn | head
```

- A writer that mints a fresh random id per record, under a comment claiming it makes receipts *joinable*, satisfies the schema and defeats the purpose. **Present-but-unjoinable equals absent** for causal closure.
- The null fraction and the distribution of ids are two different measurements. Report both: "a random nonce per record" looks like 0% null and 100% useless.
- A ledger written but never read by any branch that changes an outcome is a **write-only pile** regardless of record count. Find WHO READS, and name the decision it changes.

## 5. The UNREPRODUCIBLE NUMBER test

Any figure in a doctrine or report that is load-bearing for its argument:

1. Search the whole tree for that literal number. If the only hit is **the document asserting it**, it has never been re-measured. Say so, and give today's measured number.
2. If the document cites a **counterexample** (a commit hash, block id, artifact, port), verify the object exists and actually supports the claimed verdict. An apparatus that cannot witness its own founding counter-example has zero independent-witness rate for the case it chose as proof.
3. This is the highest-value finding class: the doctrine diagnosed the defect correctly and then never measured its own resolution.

## 6. Evidence law (non-negotiable)

- Every finding carries **the exact command run and its observed output**, trimmed to the relevant lines.
- Every claim cites **path and line number**.
- Every count is **measured in this session**. Never relay a figure from a document as though it were your measurement, and never derive a count by arithmetic on numbers you did not measure.
- Reading a diagnostic file and agreeing with it is **not** evidence. Independently verify or refute its key claims; state which you confirmed and which you could not.
- Report **UNDETERMINED** where you cannot prove. A stated gap is a result; a smuggled assumption is a defect.
- Read every hit **in its enclosing scope** before counting it. A grep hit inside a dated log, inside a negated sentence (`"cite it, never write it"` read as a write target), in a placeholder, or in an unrelated tree is a false positive and will inflate the headline. Correct your own detector before publishing its number — and publish both numbers.
- **Expect the honest split.** Controls that genuinely hold must be listed as REAL. Do not manufacture a scandal, and do not let the headline outrun the measurement.

## 7. Reporting shape

1. Lead with the answer, not the method.
2. Order by **damage to the agent's ability to finish work** — dead ends first, cost-without-consequence second, dead files third.
3. Name what really holds, with its recorded block. Crediting costs nothing and keeps the report from reading as a campaign.
4. Collapse to the **binaries that belong to the principal** — irreversible mutation, canonical records, money, external ports, direction. Everything else is the auditor's to resolve.
5. End with the item that is his to answer, not a menu.

## 8. Pitfalls

- **The self-referential gate.** A content-matching control can be satisfied by **deleting the evidence it audits**. Clearing a gate by removing a quotation, softening a fact, or dropping a number turns a governance control into an evidence-loss mechanism. Clear it by changing **register** (a neutral synonym for a figurative word) and never the substance. If the only way to pass is to lose evidence, do not pass — report the blocked state with the exact blocked operation. Depth and the bisect recipe: `references/self-referential-gates.md`.
- **The exemption asymmetry.** When a linter exempts quoted material for every rule except one, that one rule is measuring the author, not the text. Test it by running the tool against the doctrine that governs it — if the law's own source fails its own law, the tool is scoped wrong, not the law.
- **Two brakes is not redundancy.** A second implementation of one control is two half-brakes, not a backup — they drift apart. If the federation has a single-owner rule for controls, cite it.
- **Kinship is not equivalence.** Two incidents sharing a shape (agents attacking unassigned targets; a deliberately-trained model cheating) are not one story. Collapsing them into one narrative is the same defect as an unmeasured number, and it is the most common move in an external summary.
- **A control that measures a proxy.** Constraint descriptions can be over-generalised: a word-list brake applied to internal, technical or machine-facing text constrains output the doctrine never scoped it to. Check the tool's own audience/mode switch — if both modes behave identically for the gate in question, say so.
- **Do not fix what you audit.** Repairing mid-audit destroys the evidence and puts the auditor in the executor's seat. Report; the repair is a separate authorized act.

## 9. Running a batch audit across many surfaces

For a federation-sized sweep, fan out one read-only subagent per surface with a fixed brief. The brief template, the standard definitions block, and the required per-finding fields are in `references/batch-audit-brief.md`. Aggregate in code, and reconcile each child's headline count against its own raw artifacts before repeating it — a subagent's summary is a self-report, not a witness.

## Support files

- `references/self-referential-gates.md` — the evidence-loss trap: mechanism, bisect recipe, register-vs-evidence rule.
- `references/batch-audit-brief.md` — reusable read-only subagent brief for sweeping many control surfaces.
