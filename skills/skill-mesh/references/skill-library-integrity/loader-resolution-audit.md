# Loader-Resolution Audit — worked method and exemplar

Companion depth for this skill's audit doctrine. Read this when a skill store *looks* broken and you
need to find out whether it is, or whether your instrument is.

## The three questions

A store answers three **independent** questions. Most audits answer only #1, find it ugly, and report
the store as broken — when the defect lives in #2 and #3.

| # | Question | Instrument |
|---|---|---|
| 1 INVENTORY | what is on disk? | symlink-aware walk, realpath-deduped |
| 2 OWNERSHIP | who may **write** each body? | count links whose realpath leaves the canonical tree |
| 3 RESOLUTION | does every name a **consumer declares** actually load? | parse the consumer's own declaration; resolve against the store THAT consumer loads |

Run them in order. Do not publish a #1 number until #1 is depth-aware and link-aware.

## The shape of the mistake

Three instruments were pointed at one store and returned three different verdicts:

| Instrument | Verdict | Question it actually answered |
|---|---|---|
| depth-1 dir listing | "~70 empty shells, 27% of the store is rot" | which top-level dirs lack an own `SKILL.md` |
| symlink-blind walk | "31 empty dirs in the mirror store" | the same question, with links not followed |
| symlink-aware walk + realpath dedup | "5 truly empty; 54 namespaces holding 397 skills" | which dirs hold no skill at any depth |

All three were honest. Two answered a question nobody had asked. **The store was not 27% rot; the
instrument was depth-blind.** When a store reads as chaotic, suspect the counter before the store —
and expect the rot claim to come from the coarsest instrument.

## 1 — Inventory (depth-aware, link-aware)

```python
# A dir is a SHELL only when no SKILL.md exists beneath it at any depth.
nested = sum(1 for dp, _, fn in os.walk(p, followlinks=True) if "SKILL.md" in fn)
kind = "skill" if os.path.exists(p + "/SKILL.md") else ("namespace" if nested else "empty")
```

A directory with no own `SKILL.md` is usually a **namespace** — it holds skills, it is not one. Run a
depth-1 count to size the job, never to publish a defect count.

## 2 — Ownership (the second-writer check)

`broken_symlinks: 0` answers "does every link resolve?", never "who may write the target?" Count the
opposite: links whose realpath leaves the canonical tree. Each one is a second writer — an edit
outside the canonical tree that silently changes what every view loads — and the store passes every
existing sensor clean while it holds them.

## 3 — Resolution

For each consumer, parse its own declaration and resolve each name against **the store that consumer
loads**. Report per-store, because the interesting result is the disagreement:

```
consumer            declared   storeA   storeB   dead-in-all
333-agi.md                 5      1/5      4/5       1
555-asi.md                 5      1/5      4/5       1
888-apex.md                7      2/7      3/7       4
```

One declaration, two loaders, two verdicts. Naming that pattern is the whole point — a single-store
check reports "live" for one seat and "missing" for its neighbour, and both are wrong about the
system. A name that resolves in store A but not B is a **cross-loader false affordance**; a name
that resolves in neither is genuinely dead.

Consumers worth testing: subagent definition `skills:` lists (`.claude/agents/*.md`),
agent-profile JSON (`*_SKILL_PROFILE.json`), the Hermes injected index
(`.hermes/.skills_prompt_snapshot.json`), and every `layers:` block in the registry.

Report **declared / resolved / dead** per set, never one global percentage — a set that is 100% clean
sitting beside one that is 76% dead averages to a number that hides both. And a resolution report is
only actionable if it can fail: exit non-zero when any declared name is unresolved, or it is a
narrative rather than a gate.

## Indirection layers: test for CALLERS, not for content

```bash
grep -rl "SKILL_ALIAS_TABLE" /root/.claude /root/.config/opencode /root/.hermes/config.yaml 2>/dev/null | head
```

A registry, an alias table, an ownership map and a placement manifest all have exactly one job:
resolve a name before something loads it. So test whether anything reads the file's *name*, not
whether its rows look confident. Shape of the failure: a layer can read
`status: SEALED_TABLE_AUDITED` on every row while its paths no longer exist and no consumer consults
it. Both properties fail independently. When a whole naming layer is hand-written, declares itself
sealed, and is called by nothing, every name any agent declares resolves **on faith**.

**The self-refutation tell.** A machine-derived witness block sitting directly above an authored block
in the same file (a real `disk_reconciliation` above an invented `layers:`): the truthful numbers lend
authority to the invented names. Anyone auditing the file reads the top, believes the bottom. Keep the
derived half; regenerate or delete the authored half.

**One generated manifest beats many hand-kept layers.** Measured on one store, same day, same method:

| artifact | declared | dead |
|---|---|---|
| index derived from disk | full library | **0%** |
| hand-written registry | 112 | 71% |
| hand-written alias table | 258 | 76% |
| hand-written consumer lists | 17 | 35% |

The derived artifact was not merely better — it had *zero* dead entries, because no human had a chance
to write a name the disk does not hold. Before auditing a hand-maintained inventory for errors, ask
whether it should be hand-maintained at all: replace the authored list with a generator reading the
source of truth, and keep human intent (classification, ownership, load order) as **annotations keyed
to generated names**, never as a parallel list of names.

**Declaring an artifact replaced is not replacing it.** After a migration, grep the consumers for the
superseded file's NAME. If the tool that replaced it still reads it, and other layers still import it,
the old layer is live and the new one is merely a sibling. A replacement is complete when the old file
has zero readers, never when the new file exists.

## Auditing a generated artifact

The generator inherits every census error, so audit the artifact and not its provenance:

- **Path must be absolute.** A manifest of cwd-relative paths is correct only when read from one
  directory.
- **Nested skills must be entries, not bare strings.** A namespace record listing
  `"children": ["some-skill"]` hands a loader a name with no path, no hash and no authority —
  unresolvable by definition. Flat entries plus a `namespace` field keeps the taxonomy *and*
  resolvability.
- **Per-entry fields must vary.** A field reading the same token on every entry
  (`harnesses: ["a","a","a","a","a"]`) is a constant wearing a field's name.
- **The generator must exist.** If the manifest names a writer script, that file must be findable on
  disk by that name. A provenance line naming an absent tool describes a one-time bake — and it will
  be trusted precisely because it says *machine-generated*.
- **The declared count must equal the entry count.** A summary that disagrees with its own array is
  the first thing a downstream consumer trusts.
- **Histogram the entries by depth.** A manifest whose entries all sit at depth 0 has a depth-1 walk
  and cannot see what it claims to index — this is how an earlier census error gets baked into
  something now called the source of truth.
- **Two files, one name, differing only by case** — one is unreachable. Same defect class as two
  directories with one basename.

## Grading a gate

Print the class of every finding before quoting the exit code:

```bash
python3 /root/scripts/skill-entropy-gate.py --json \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print({k:v['class'] for k,v in d['checks'].items()})"
```

A store can carry hundreds of real collisions, be checked four times a day on a schedule, and still
exit 0 — because they are classified `WARN`. The gate is not broken; it is **decoration by
classification**. Fix the class, not the schedule. A severity tier that no defect can ever escalate
out of is a boundary that was never load-bearing.

**A gate must not skip the defect class it exists to catch.** Three shapes, one defect — the gate runs,
reports, and cannot refuse:

- **skip-by-marker** — the parser is written to skip commented or `TODO`-marked entries, which are
  exactly the unresolved names the gate was built to find. A marker is a **label for a failure**, never
  an exemption from reporting it. Test such a gate by feeding it a known-bad entry in its *marked* form
  and requiring it to fail.
- **wrong class** — a real defect emitted as `INFO` or `WARN` while the verdict is computed from a
  different check entirely.
- **self-listed defect** — the gate's own output names the defect and it still exits 0.

**Reporter first, FAIL second.** A gate that fails on every run trains every reader to ignore it — the
"cannot fail" defect reached from the other direction, and harder to notice because the exit code looks
disciplined.

1. Ship it as a **reporter**: always exit 0, write the receipt, establish the tracked baseline.
2. Watch the dead-count down to its target.
3. **Flip to non-zero at zero**, and hold it there.

The flip is the deliverable; the reporting phase is how the gate earns the right to refuse. Give the
flip a kill condition — if the count has not moved in ~30 days, the reporter is decoration and should
be demoted, the way any honest-but-unmeasured criterion already in the tree should be.

## A name marked missing that resolves is a regression

When resolution work suppresses names — marks them `missing`, or deletes them from a seat's declared
list — verify each one is genuinely unresolvable **in the store that seat loads** before suppressing
it.

- **Cross-store miss is not absence.** A name resolving in one store and not the one a given loader
  reads is a **visibility** defect in that loader. Fix it by making the skill visible to the consumer,
  never by commenting it out.
- **A working entry removed so a gate goes green is a capability loss caused by the fix.** Worse than
  the findings it silenced: the seat silently knows one fewer thing and the gate now reports health.
- Prefer a **redirect** (`# alias-to:<owner>`) over a removal marker — a redirect is resolvable and
  tells the next reader where the capability went.
- Never write suppression markers into a structured field another loader parses: a comment inside a
  YAML list becomes a name some other harness tries to load, turning a silent defect into a loud one
  every other consumer must absorb.

## Mapping dead names to successors

For each dead name, search for a successor and **report** it; never auto-apply.

- Score by **token overlap**, not substring-and-length. A rename changes shape, not subject —
  `geo-basin` to a basin-evaluation skill is a rename, not a loss, and substring guards miss it
  entirely. Segment on kebab/snake/camel boundaries, drop stop-tokens, require a minimum overlap.
- Normalise harness prefixes (`forge-`, `aaa-`, `asi-`, `apex-`, `hermes-`, `dev-`, `ops-`) before
  matching; they carry no semantic load.
- Emit `(score, path)` and let a human decide. Roughly **58%** of dead names in a real store had a
  plausible successor already on disk — which turns the repair from archaeology into a mapping pass —
  and the remainder are the decisions that actually need judgement.

## Own-instrument discipline

Two of the wrong numbers in the exemplar run were produced by the auditor, not the store. Before
believing any count the probe prints:

- did the walk follow symlinks? (`os.walk(..., followlinks=True)`, `find -L`)
- did it dedupe by realpath? (mirror views share inodes; one body counted once per view)
- did the parser actually split the field? (a regex swallowing a YAML array reports a fake 0%)
- is the count plausible against a second, independent command?

Run one cheap independent command per headline number. Two instruments agreeing is a measurement; one
instrument repeated is a claim. And record your own corrections beside the findings they replaced —
the corrected number is more useful to the next reader than a clean one, because it names the trap.

**Prove a new instrument in BOTH directions before trusting either verdict.** A fixture set containing
only defects yields a check that always fires; one containing only healthy inputs yields a check that
can never fire. Run known-good inputs (must all pass) **and** known-bad inputs (must all be rejected)
as one self-test, and treat a check that cannot produce both outcomes as unshipped. The first execution
of a new meter is a test of the meter, never a finding about its subject — and a check authored during
an audit of unenforced controls is the likeliest place for this defect to land, because everyone is
looking at the subject.

## Verifying a peer's audit

A peer's claimed fix can be true while the sentence wrapped around it is false, and both halves arrive
in one paragraph. Measure the before/after delta yourself, per claim:

| claim shape | how to falsify it |
|---|---|
| "X is fixed / replaced / removed" | run the sensor before and after; grep for surviving consumers |
| "N entries / N things" | count them; check the declared count against its own array |
| "the gate now returns FAIL" | run it and read the **exit code**, not its output text |
| "generated, regenerable" | find the generator by name on disk |
| "missing / dead / absent" | resolve the name in every store the consumer can reach |

Report each claim as verified / false / partial with the measurement beside it. Passing the true half
through unexamined is how the false half acquires authority — a report that is 80% verified earns trust
for the 20% nobody checked.

**One-writer applies to the auditor.** Before adding your own file to a tree you just audited, confirm
no writer is live in it (`git status`, recent mtimes, an agent process still holding the directory). If
one is, **stand down and hand over**: name the blocker and the sequence, hold the artifact in a
scratch path, do not install. Dropping a file into a tree another agent is mid-write on makes you the
second writer you just documented — and the collision lands on whoever commits next. An unwired gate
plus a named handover beats a wired gate that conflicts.

## Namespace markers

Namespace directories carry a `NAMESPACE.md` declaring "I hold skills, I am not one." Respect the
marker when classifying; do not re-derive the namespace list by hand, and do not report the absence of
a `SKILL.md` in such a dir as a defect.

**Sweep every view when retiring a name.** Retiring a name leaves dangling links in every mirror tree.
For each: **repoint** where a live successor exists, **remove** where the name itself is retired, and
record an **undo line per link**. Freeze bodies outside every mirror root — a freeze directory inside
a synced tree can be pruned by the sync that propagates the removal.
