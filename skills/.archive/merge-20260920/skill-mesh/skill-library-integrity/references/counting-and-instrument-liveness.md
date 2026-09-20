# Counting the Store, and Proving an Instrument Is Alive

Two audits that fail in the same way: a number produced by a method nobody chose, and a control
trusted because it exists rather than because it has ever acted. Both failures are silent — the
output looks exactly like a correct one.

---

## 1. Counting a skill store — which question does the number answer?

The store is a **view tree**: a small number of physical bodies reached through many addresses
(symlinks, bands, mirrors). Any count is therefore correct only relative to a question. State the
question with the number.

| The question | The method | Why other methods disagree |
|---|---|---|
| How many capabilities exist? | walk **following symlinks**, dedupe by `realpath` of each `SKILL.md` | a non-following walk sees only first-party bodies and reports a fraction of the library |
| How many doors can an agent enter by? | walk following symlinks, **count addresses** (no dedupe) | always ≥ the body count; the gap is the view tree, not duplication |
| What does a harness actually serve? | read that harness's **rendered/cached snapshot**, not the filesystem | the loader may hold a stale snapshot, and the filesystem may hold skills the loader never resolves |
| Is one capability wearing several identities? | group by declared `name:`, compare **body digests** within each group | groups whose digests match are address bands, not collisions |

**Rules**

- **Never count with a walk that does not follow symlinks.** `os.walk(followlinks=False)` and bare
  `find` are the tooling default, and in a symlink-first store they under-report by an order of
  magnitude while looking entirely plausible.
- **A directory without `SKILL.md` is not empty.** Namespace and category directories hold sub-skills
  beneath them. Classify each before condemning it: `HAS_BODY` · `CONTAINER (holds sub-skills)` ·
  `TRULY_EMPTY`. Reporting a container as an empty shell invents a defect and buries the real one.
- **A count is a claim.** It carries the method that produced it. Two audits that disagree about the
  same store are usually both right about different questions — find which question each answered
  before concluding either is wrong.
- **A stale manifest is a number, not a source.** Check its generation date before citing it. A
  self-auditing script that writes its output to a dated file will happily re-serve an old answer.

---

## 2. Proving an instrument is alive

A guard that has never run, or that cannot return non-zero, is not a control. It is a document with
execute permission. Four tests, in order — each is cheap, and each alone is insufficient:

1. **Does it compile / parse?** `python3 -m py_compile <file>`, or the language equivalent. A syntax
   error means it has never once produced a result, while sitting in a governance directory looking
   authoritative.
2. **Does anything call it?** Search its filename across the whole federation — other scripts,
   hooks, cron definitions, skills, docs. Zero executable callers means a human runs it by hand or
   it never runs. Separate *prose references* (a skill describing it) from *actual call sites*.
3. **Can it fail?** Read the exit logic. A guard with only `return 0` / `sys.exit(0)` paths cannot
   guard; a strict flag that nothing passes is a gate nobody closes. Quote the exit branch as the
   evidence.
4. **Has it ever produced output?** Check for artifacts and their mtimes. The absence of any output
   artifact is the strongest single signal of a dead instrument.

**Additional signals**

- **Tracked vs untracked** on the file itself: an untracked script in a governance directory was
  never reviewed, and citing it in a report is an unchecked claim.
- **Self-refuting output** proves the instrument is not reading reality: figures that cannot all be
  true at once (a subset larger than its superset, a rate above 100%, a total that moves backwards
  between runs when the underlying set did not).
- **A deployed copy is not the canonical source.** Compare the deployed artifact against its declared
  source by digest; a drift guard that only checks the declared path *exists* will report clean while
  the live file is a stub. Declaring a path in a manifest is not the same as that path being wired.
- **Search for the rule before adding a second implementation.** Two brakes on one wheel is one too
  many, and they will drift. Keep one canonical owner and point the other at it.

---

## 3. The control that exists but cannot be answered

A control that *can* withhold is not automatically sound. The next question is whether the withheld
party has an **actionable, documented way out**. A gate that blocks with no unblock path is an
unanswerable refusal: work stops, nothing records why, and the same work is retried and stopped
again.

Judge every blocking control on three measured properties:

- **Can it withhold?** Evidence is a real refusal in a receipt or log — not the capability to refuse.
- **Is the refusal persisted?** A hold that is never written down cannot be cited, appealed, or
  counted. Measure: blocked count, distinct actors, and how many carry a recorded acknowledgement.
- **Is there a documented unblock?** Find the procedure by name and quote it. If the only path is
  "escalate to the human", say so — that is a terminal path, and a system whose every refusal ends at
  one person has exactly one available action.

Rank findings **dead ends first**: holds with no recorded state and no unblock path cost the most,
because they consume work without producing a decision. A control that fails loudly and names its
own remedy is in better health than one that quietly accumulates unresolved holds.

---

## 4. Auditing a control without deforming the record

A content or keyword gate will eventually block the very report that describes it — the report
quotes the trigger, and the matcher cannot tell a quotation from an assertion. Expect this and plan
for it; it is a property of lexical controls, not a malfunction to route around silently.

- **Bisect, do not guess.** When a write is refused with a vague reason, split the payload and write
  the halves separately until the smallest refusing fragment is isolated. Convert the report to
  plain words, then re-assemble. This turns a blocked write into a named trigger in a few steps.
- **Change register, never evidence.** Substituting a synonym, or expressing a figure in words, is
  allowed and must be disclosed. Deleting a quotation, softening what a person actually said, or
  dropping a number to satisfy a matcher is not — that is a control being satisfied by editing what
  it reads, and it destroys the audit trail it was meant to protect.
- **Report the false positive next to the finding.** A blocked draft is itself evidence about the
  control; record it in the report rather than absorbing it as friction.
- **Never take a lock you are auditing.** When a gate that blocked you is itself `chattr`-locked or
  otherwise receipted, repairing it requires lifting that receipt. Report the defect, the exact
  one-command repair, and hand the decision to the human — an agent that may break any lock it
  believes is wrong has destroyed the property the lock existed to provide.
