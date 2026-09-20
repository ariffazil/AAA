---
name: aaa-doctrine-sealing
description: "Use when F13 says seal or code this into canon. Seal a session eureka into AAA canon across all layers."
---

# AAA Doctrine Sealing — Session Insight → Canon (canonical)

**One question, two old names:** *where does a settled finding actually land, and what proves it landed?*

This body is the collapse of two identities into one (2026-09-19; authority **ARIF —
SKILLSTORE_NAMESPACE_COLLAPSE_V2**). Nothing was dropped: the retired name `canon-doctrine-sealing` is
now MODES M1–M11 below, its body frozen at
`/root/AAA/skills-retired/2026-09-19-v2-doctrine-sealing/canon-doctrine-sealing/`. Mapping table, then
discovery anchors at the end of this file.

The survivor keeps the name `aaa-doctrine-sealing` because a live downstream skill names it as the owner:
`governance/symbol-namespace-integrity` cites *"`aaa-doctrine-sealing` | Owns the intake reference
(`references/external-artifact-intake.md`) the symbol probe is step 0 of."* This is a **namespace
collapse, not a rename**: no new identity was minted, and no capability was removed.

Siblings that stay **separate** — different questions, not merged here: `seal-ritual/arifos-kernel-seal-ritual`
(the kernel/VAULT999 mechanism: nonce binding, evidence-hash recipe, honest-HOLD taxonomy) and
`seal-discipline` (what a close-record may be CALLED: classes, evidence lattice).

## ⚒️ Canon Lock (F13 2026-09-16) — MANDATORY for protected trees

`/root/AAA/governance`, `/root/AAA/canon`, `/root/arifOS/GENESIS` are **chattr +i locked**.
Every write to these trees MUST go through the only legal mutation path:

```bash
ARIFOS_TRACE_ID=trc-<your-trace> /root/scripts/canon-mutate run <tree> -- <command...>
```

Direct writes fail with EPERM — **that failure is the lock working, not a bug.**
Cycle (unlock → mutate → relock → receipt) is crash-safe and receipted with verified
relock to `/var/lib/arifos/canon_mutations.jsonl`. Always set `ARIFOS_TRACE_ID`.
Never clear the immutable attribute by hand — an unlock outside the cycle is an unauthorized bypass.
Protocol: `/root/AAA/instructions/CANON-LOCK-PROTOCOL.md`.

## One Rule

> Doctrinal prose binds nothing. A finding only constrains a model once it reaches `base.md` (rendered
> inline every turn) or a kernel floor.
>
> Report doctrine-layer work as doctrine-layer. Never call it sealed if no gate can say NO to it yet.

Doctrine is not chat output. **Sealing = the rule lands on disk in every layer that reads it, carries a
status label the commit gate accepts, and is pushed.** A rule that exists only in the conversation did
not happen. **The eureka packet is NOT the deliverable — the surface edits are.**

---

## Mode index — old name → mode/section

| Old name (retired 2026-09-19) | Primary mode | Also carried by | Distinctive contribution |
|---|---|---|---|
| `canon-doctrine-sealing` | **M3 — Surfaces & order of operations** | M1 (trigger/intake), M4 (ledger artifact + row shape), M5 (render survivability), M6 (repo gates), M7 (correction log), M8 (external-critique audit), M9 (kernel amendment), M10 (pitfalls), M11 (verify/report) | the surface table; the 8-step order; render-list vs footer; the throwaway-root survivability proof; status-gate register; push authorization; correction-log law; three-way critique split |
| `aaa-doctrine-sealing` (survivor, this skill) | **M2 — Layer choice by binding frequency** | M3, M4 (two-ledger correction), M6, M10 | binding-frequency layer choice; harness generator + drift check; canon-mutate injection pattern; W_SCAR/base.md gap; canonical-name and owner-sweep rules |
| `aaa-doctrine-sealing/references/` (survivor) | **M8 + Support files** | M3, M5 | external-artifact intake (symbol probe, probe calibration, duplicate-owner **and layer** sweep, path/config-key/count verification, gate-direction conflicts); commit gates and labels |

---

## M1 — Trigger & intake scope

*(from `aaa-doctrine-sealing` "When to use" + `canon-doctrine-sealing` trigger line)*

F13 signals, in BM or English: *"seal all"*, *"code this into the kernel and state and agents"*,
*"audit and extract the key eureka insights"*, *"make it live"* — and the directive form *"seal it"*.
Also load when a session produced a rule that must outlive the session and bind agents that were not in
the room, and when the directive follows an audit of an external AI critique. The eureka packet is NOT
the deliverable. The surface edits are.

Also load when F13 **pastes an external artifact** (another model's plan, audit, or skill list) and asks
for it to be embedded. That request is an **intake**, not a copy job: the artifact is data, and it must be
audited against this machine's canon, paths, and ratified stances before any part of it lands. Read
`references/external-artifact-intake.md` first — a high-quality artifact still needs most of its
implementation rejected, and adopting an address or a gate from outside can undo work already sealed.

## M2 — Choose the layer by binding frequency, not by importance

*(survivor)*

A rule that must bind every turn belongs in `base.md` (rendered inline) or a floor; a rule that fires
only when an agent chooses to load it belongs in a skill. Getting this backwards is the quiet failure:
writing an always-on rule as a skill makes it fire *less* often while looking like an addition, because
the agent must remember to load the governance that was supposed to bind it. Before writing anything, ask
"at what frequency must this bind?" and let the answer pick the layer. Doctrine and skill have different
owners; a rule that governs every external write is law, not a skill.

## M3 — The surfaces, and the order in which they are encoded

*(from `canon-doctrine-sealing` "The Surfaces" + "Order Of Operations", and `aaa-doctrine-sealing` "The layers")*

Prose lands in AAA; floors land in arifOS. Both are separate repos with separate gates — one push never
carries the other.

| Surface | Path | Role |
|---|---|---|
| Doctrine fragment | `<aaa>/instructions/<name>.md` | the full doctrine — canonical, loaded on demand |
| Membrane floors | `<aaa>/instructions/human-meaning-membrane.md` | C-series rules binding human-modelling turns |
| Always-on inline | `<aaa>/instructions/base.md` | the ONLY fragment rendered inline into every context — the 2–3 line operative rule goes here |
| Fragment index | `<aaa>/AGENTS.md` | the Active Instruction Fragments table — add a row so the organ declares it |
| Lineage pointer | the fragment this one extends or supersedes | stops two half-truths living side by side |
| Eureka ledger | `<aaa>/eurekas/EUREKA-<slug>.md` + `eureka-entries.jsonl` | one markdown artifact **and** one appended JSONL row — see M4 for which ledger |
| Skill | the profile's `skills/<...>/SKILL.md` | the operating gate the agent actually runs |
| Kernel | `<arifos>/GENESIS/FLOOR_TABLE_AMENDMENTS.md` | numbered amendment — **never edit `FLOOR_TABLE.json` directly** |

Resolve `<aaa>` / `<arifos>` from the organ registry, not from memory.

**Order of operations.**

1. Write the fragment **with its correction log** (M7).
2. Patch the membrane floors (append the new C-numbers, bump the range in the heading) and add the lineage pointer to the older fragment.
3. Add the operative rule to `base.md` — this is what makes it bind every turn rather than on demand.
4. Add the `<aaa>/AGENTS.md` table row with its status.
5. Append the eureka artifact + the JSONL row (**M4: to the LIVE FEED**).
6. Patch the skill that governs the task class (the gate the agent runs).
7. Propose the kernel amendment (M9).
8. Render (M5), commit, push both repos, verify (M11).

Detail carried from the survivor's numbered layer list:

- **Fragment** — `/root/AAA/instructions/<topic>.md`. One topic per file; name by class, never by incident. Header carries `> **` lines, one per field: forged/trigger line, `**Supersedes**` (which earlier shorthand it corrects), `**Binding**` (which surfaces), `**Lineage**` (prior fragment it extends), `**Status**`, `**Kernel anchor**` (F-floors). Body: One Rule, the model, numbered laws, the operational gate (pass/fail examples), what is lawful, profile application, and a **Correction Log** of misreadings that must not be re-imported.
- **Always-on line** — `base.md`, only if it must bind every turn. `base.md` is the only fragment rendered *inline* into `/root/AGENTS.md`; all other fragments are `ref:` pointers or footer entries (on-demand). If a rule must apply every turn, add ONE paragraph to `base.md`. A rule that must bind every turn but lives only in a fragment does not bind every turn.
- **Floors** — `/root/AAA/instructions/human-meaning-membrane.md`. Append to the `Constitutional Floors (C1-Cn)` list, numbered sequentially, one line each: `Cn NAME: rule.` These are doctrine-layer: they bind via rendered canon, they do **not** gate a verdict. Do not imply otherwise in the fragment's Status.
- **Fragment table** — `/root/AAA/AGENTS.md` (organ repo). Add a row to the *Active Instruction Fragments* table: `| Fragment | Path | Status |`. This is the registry other agents read to discover doctrine; an unlisted fragment is nearly invisible.
- **Kernel** — propose, never self-ratify. Floor changes go to `/root/arifOS/GENESIS/FLOOR_TABLE_AMENDMENTS.md` as `## Amendment N: <name>` + JSON (`id`, `name`, `rule`, `detection`, `failure_verdict`, `related_floors`, `doctrine_ref`) + Rationale + explicit `Awaiting: F13 SOVEREIGN ratification`. `FLOOR_TABLE.json` holds 13 floors — that is constitutional surface. Propose; do not edit it.
- **Skill (optional)** — if the rule changes how a class of task is done, patch the governing SKILL.md as well. Otherwise skip; doctrine and skill have different owners.

## M4 — The eureka ledgers: one FROZEN RATIFIED REGISTRY, one LIVE FEED

*(ledger target corrected 2026-09-19 in the merge pass — read this before appending anything)*

**Two eureka ledgers exist by design. Neither is a stray.** One was frozen as a ratified registry; the
other is the live feed.

| path | status | attribute evidence (`lsattr`, 2026-09-19) | rows · last written | entry shape |
|---|---|---|---|---|
| `/root/AAA/eurekas/eureka-entries.jsonl` | **LIVE FEED — the write target** | `--------------e-------` — writable, no immutable flag | 14 rows · 2026-09-18 (the most recent of the two) | `{ts, agent, session, eureka, evidence, truth_class, actor, verdict}` |
| `/root/AAA/canon/eureka-entries.jsonl` | **FROZEN RATIFIED REGISTRY — historical authority. Cite it; never write it.** | `----i---------e-------` — **IMMUTABLE (chattr +i)**; an append returns EPERM even as root unless the attribute is first cleared, which is forbidden | 109 rows · 2026-09-16 | `{id, timestamp, type, title, source, summary, status}`, `id` = `EUREKA-<TOPIC>-<DATE>` |

**The instruction is ONE line:** append the new row to the **LIVE FEED**,
`/root/AAA/eurekas/eureka-entries.jsonl`. `/root/AAA/canon/eureka-entries.jsonl` is immutable by design —
it is the frozen ratified registry and is cited as historical authority by `canon/*.md` and
`instructions/anti-calhoun.md`. Cite it. Never use it as a write target, never unlock it, never clear its
attribute to append.

**Readers of the live feed (verified on disk 2026-09-19):** `/root/AAA/governance/durable-artifact-authoring/SKILL.md`
(~line 87 instructs appending there), this skill's `references/commit-gates.md`, and
`/root/AAA/governance/AMENDMENT-6-REGISTER-LAW-RATIFICATION-2026-09-15.md`. It is read.

**Correction — do not re-import the old text.** Earlier versions of this skill and of
`references/commit-gates.md` named `/root/AAA/canon/eureka-entries.jsonl` as the write target ("append to
canon") and called the live feed *"a stray with a different entry shape and no readers"*. Both halves were
wrong, and the label was factually inverted:

- the canon target **cannot be written at all** (immutable attribute → EPERM), so the instruction could
  never execute;
- the "stray" is in fact the live feed, with three readers, written most recently.

Appending to the wrong one silently loses the record. Keep the entry count honest: `wc -l` before and
after, and re-parse the file (M11). **Never port entries between the two ledgers** — the frozen registry is
a historical snapshot; the live feed is the flowing record. The live feed is not under the canon lock (it
carries no immutable attribute and is writable); the canon-mutate cycle is still mandatory for anything
under `/root/AAA/canon`, `/root/AAA/governance`, `/root/arifOS/GENESIS`.

## M5 — Render step & generated-surface survivability

*(from `canon-doctrine-sealing` "Render Step")*

```bash
/root/scripts/render-agents.sh      # regenerates /root/AGENTS.md from the fragments
```

- `/root/AGENTS.md` is a **generated file** — `render_one` rewrites it whole (`cat "$tmp" > "$target"`). Nothing appended by hand survives. A block added after the `<!-- Rendered: ... -->` stamp is the worst case: it reads as live in the file you just opened, and the next render deletes it, so the agent that appended it is the last one to ever see it.
- **Anything that must survive lives in a fragment.** Prose goes in `<aaa>/instructions/<name>.md`; loading it needs its bare name added to the `render_one "$ROOT/AGENTS.md" ...` list inside `/root/scripts/render-agents.sh`.
- Only `base` (and any other named fragment) renders in full; `ref:<name>` renders a one-line pointer; every remaining fragment is listed in the `UNRENDERED_FRAGMENTS` footer.
- **The footer is automatic; the render list is not.** A new fragment is *listed* in the footer with no edit anywhere — but listed is not loaded. If the doctrine must reach every turn, name it in the render list. Editing that list is editing the renderer, not hand-editing generated output.
- **Re-run the renderer after ANY fragment edit**, or agents keep reading the stale map. Confirm with `grep -n '<fragment>' /root/AGENTS.md` **and check the hit sits ABOVE the `<!-- Rendered:` stamp** — a hit below it is a delete-at-next-render claim.
- **Prove survivability without touching the real file** — render into a throwaway root and grep it:
  ```bash
  rm -rf /tmp/rt && mkdir -p /tmp/rt/AAA && ln -s <aaa>/instructions /tmp/rt/AAA/instructions
  ROOT=/tmp/rt bash /root/scripts/render-agents.sh >/dev/null
  grep -c '<Fragment Heading>' /tmp/rt/AGENTS.md    # 0 = this doctrine would be wiped
  ```
  Expect path-substitution noise in a direct `diff` (`/tmp/rt/...` vs `<aaa>/...` on `ref:` pointer lines) — read the diff for content hunks, not paths. Rendering twice must be a no-op; if `render-agents.sh --check` still reports changes, the fragment or the list is unstable.
- **A rule that must bind EVERY harness needs a generator and a drift check, not hand-copies.** Harness boot surfaces are not one file: `/root/AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `QWEN.md`, `.codex/AGENTS.md`, `.config/opencode/AGENTS.md`, `.kimi-code/{AGENTS,SYSTEM}.md`, `.qwen/instructions.md`, `.grok/AGENTS.md`, `.arifos/agents/*/AGENTS.md`, and on KVM4 the `.openclaw/{system.md,workspace*,agents/*/system.md}` set. Hand-copying a clause into them rots silently: surfaces drift, some end up with two copies while others get none, and a stale host can carry zero. Fix pattern — ONE writer script emitting a marker-delimited block (`<!-- BEGIN/END AAA-<TOPIC> -->`), idempotent, stripping pre-marker legacy sections so exactly one copy survives per surface, with `--check` exiting non-zero and a scheduled drift-check writing a receipt. Reference implementation: `/root/scripts/membrane-propagate.py` + `membrane-drift-check.sh`. A host whose `/root/AGENTS.md` is generated elsewhere (KVM8 → KVM4) gets the rendered file synced, never hand-edited on the stale side.

## M6 — Repo gates, staging, and push authorization

*(from both bodies: `canon-doctrine-sealing` "Repo Gates" + `aaa-doctrine-sealing` push pitfalls)*

### Doctrine-status gate (AAA)

AAA refuses a commit touching watched doctrine files without a compliant status line:

```
DOCTRINE-STATUS GATE: BLOCKED
  R3 instructions/<name>.md: new watched .md has no Status line — label it
```

- **Every new `.md` under `instructions/` must carry a `Status:` line** — `DRAFT_*` · `PENDING_*` · `spec` · or an F13 instrument. One unlabelled new file blocks the whole commit.
- **A ratified-class value needs an F13 instrument: a date or a verbatim quote.** A bare `Status: RATIFIED` blocks. Working form, as a blockquote near the top:

  ```
  > **Status:** F13_RATIFIED_CHAT (<date>) — sovereign-directed in ARIF dm: "<the words he actually used>"
  ```

- **ANNEX-class values are blocked outright** — never reach for `CONSTITUTIONAL_ANNEX` to get past the gate.
- Fix the status line and re-commit; do not `--no-verify` past it.

### Staging and pushing

```bash
git -C <repo> add <explicit paths>     # NOT `git add -A`
git -C <repo> commit -m "SEAL::<NAME>::<date> — <what>"
git -C <repo> push
git -C <repo> status -sb | head -2     # `## main...origin/main`, no ahead-count
```

**Stage explicit paths.** Both repos carry unrelated in-flight edits from other sessions; `git add -A` sweeps a sibling's half-finished work into your commit and through the gate.

**Push authorization.** The standing "ask before pushing to main" rule does NOT apply when F13's own instruction was the directive that produced the change (an imperative to seal / code it in): that instruction IS the authorization, and stopping to re-confirm collapses finished execution back onto the human (anti-collapse doctrine). Land it, then report commits and open debt. Re-ask only when the push is un-directed — you decided on your own to put it on main.

**Push is a gate, not a formality.** `git -C /root/AAA push` runs the F1–F13 governance check and prints
`Normal push — governance gate passed`; arifOS pushes also run the drift check and print source vs deployed.
**Check what a push publishes before running it.** A repo with a publish workflow on the default branch
turns `git push` into an external release, not a save: land the work on a named branch (or hold it) until
the commits in that push have been read. Dirty trees also drag unrelated commits along — scope the push to
the branch that carries the work and say so in the receipt.

**Remote lines that are not failures:**

```
remote: Bypassed rule violations for refs/heads/main:
remote: - Required status check "<check>" is expected.
```

The push landed. Required status checks evaluate server-side; this is informational.

## M7 — Correction log: carry the wrongness forward

*(from `canon-doctrine-sealing` "Correction Log")*

A fragment that codes a claim must also record the claims it CORRECTS so the next session cannot
re-import them. Mark each explicitly, including overclaims from the agent's own earlier output:

```
**Correction N — <claim> (upgraded).** <what was claimed> is not established. <correct form, with why>.
```

A correction log listing only the external critique's errors is half a log — the agent's own prior
overclaim in the same lineage is the one most likely to recur.

## M8 — Intake: pasted artifact, or audit of an external critique

*(from both bodies)*

Full intake protocol: `references/external-artifact-intake.md` (the symbol probe run on the artifact's own
words, and why CLEAR is a notation verdict, not a truth verdict; probe calibration against past cases;
citation and foreign-seal checks; the duplicate-owner **and layer** sweep; name resolution across every
skill root; vocabulary collision against tokens canon already binds; path / config-key /
count-unit-and-status verification; gate-direction conflicts with a ratified stance; the item-by-item
triage of an artifact's "here is what to seal" list; how to record accept / reject / HOLD).

- Split it three ways: what survives, what is overstated, and **what it MISSED**. The missed item is usually the highest-value addition — a mechanism error, not a degree error.
- **Refuse to code unbacked scalars.** Seal-style metadata (`dS`, `kappa`, `confidence`) with no computation behind it is false precision; keep it out of canon and say why.
- Code the correction, not the concession: agreement without a mechanism change is decoration.
- **"Seal all" authorises the layers of the rules in play — never a wholesale adoption.** When the same instruction also carries an outside artifact, the artifact's *items* are not automatically in scope: audit each one, fold the deltas into their owners, and leave the rest recorded as already-owned, rejected, or held. Sealing a list because it was attached to the order is how restatements become canon and how a dozen unnecessary files get minted in one turn.
- **Sweep for an existing owner before minting.** Parallel agent sessions on the same box mint the same insight independently. Before writing, grep the ledger, the fragments, and `git log` for the topic; if an owner exists, fold the delta into it instead of creating a second file (one fact, one owner, one axis).

## M9 — Kernel amendment shape

*(from both bodies)*

Append a numbered `## Amendment N:` to `GENESIS/FLOOR_TABLE_AMENDMENTS.md` with the proposed floor JSON
(`id`, `name`, `rule`, `detection`, `failure_verdict`, `related_floors`, `doctrine_ref`), a rationale, a
detection contract, and a "corrections carried" list. Close with its status — **proposed, awaiting F13
floor ratification** — and say so in the reply: doctrine binds by canon, only a floor can say NO. Never
edit `FLOOR_TABLE.json` (13 floors — constitutional surface); an amendment is a proposal, and reporting it
as live is a false receipt.

## M10 — Canon Refactoring Doctrine (F13 2026-09-20)

When canon files accumulate (69+ files = compression failure, not knowledge surplus), refactor using the Tier-2 Compression path:

```
Theories (69 files)
→ 13 Constitutional Floors (each floor = one facet of reality defended)
→ 1 Kernel (INIT::GODEL_LOCK)
→ 1 Invariant (Reality > Everything)
```

### The 13 Floors as 13 Defenses of Reality

Each floor protects one specific facet of reality from corruption:
F01=consequence, F02=observation, F03=attestation, F04=representation, F05=coexistence, F06=personhood, F07=reality-exceeds-model, F08=elegance, F09=no-ghost-reality, F10=structure, F11=identity, F12=origin, F13=authority.

### SEAL-REFRACTOR Audit Test

Every canon document must answer three questions:
```
Which floor?
Why that floor?
What invariant changes if the document disappears?
```
If answer is "None" → Archive.

### Compression Doctrine
```
Theories are abundant.
Constitutional surface area is expensive.
Compress. Do not add.
Do not add floors. Do not add doctrines. Do not add primitives.
```

### Blind Spot: Floor > Reality

If floors become sacred — if the constitution sits above reality — shadow reborn. The Gödel Lock Level 2: "Constitution cannot become authority above reality." If reality contradicts a floor, reality wins.

### What NOT to Refactor Into a Floor

- APEX Theory = runtime selector, not constitutional floor
- Theory of Paradox Conductance = F6 + F7 (dignity conflict or model limit)
- Master Paradox = F7 HUMILITY (limit statement, not sovereignty)

**Full reference:** `/root/AAA/canon/TIER-2-COMPRESSION-2026-09-20.md`, `/root/AAA/canon/CANON-FLOOR-INDEX-2026-09-20.md`

---

## M11 — Pitfalls (union of both bodies)

**Ledger and layer traps**

- **Two eureka ledgers exist; only ONE is writable, and it is the live feed.** See M4. Append to `/root/AAA/eurekas/eureka-entries.jsonl`. The canon file is a frozen ratified registry — immutable, cite-only. Appending to the wrong one silently loses the record.
- **Skipping `base.md`:** the fragment is now canonical and still binds nothing, because fragments render on demand. The inline line is the whole point.
- **Appending to the generated file instead of the source fragment:** the doctrine is correct in your session and gone at the next render. `/root/AGENTS.md` is output, never a place to write.
- **Forgetting the render:** the repo is correct and every agent is reading the previous map.
- **Unlabelled new fragment:** the commit dies at the status gate after all the work is written. Add the `Status:` line when the file is created, not after the first refusal.
- **Editing `FLOOR_TABLE.json` directly:** amendment file only; direct floor edits bypass ratification.
- **One commit for two repos:** AAA and arifOS gate independently.
- **Reporting the amendment as live:** an amendment is a proposal. Saying "sealed" for it is a false receipt.

**Embedding verification trap (F13 2026-09-20)**

When F13 asks "is X already embedded?" — do NOT check one surface and declare. "Embedded" means the principle reaches agents at boot time, not that a file exists somewhere. The correct probe is multi-surface — run all greps in parallel:

1. SOUL.md (Hermes identity — always loaded)
2. AGENTS.md / base.md (rendered inline every turn)
3. Boot sequences: `AAA/prompts/INIT_HERMES.md`, `UNIVERSAL_BOOT.md`, `ARIFOS_FEDERATION_INIT.md`
4. Agent cards: `AAA/a2a-server/agent-cards/` (what other agents see)
5. Skills: `AAA/skills/` (on-demand loading)
6. Canon floors: `AAA/canon/FLOORS/`, `AAA/canon/FLOORS/archive/`
7. The eureka ledgers

Report per-surface hit count. A principle that exists in canon/ but NOT in boot sequences or SOUL.md is **documented, not embedded**. The human-facing question is "will every agent load this?" — if the answer requires a manual `skill_view` call, it is NOT embedded for auto-loading.

"Principles exist" ≠ "Principles embedded" is a semantic trap. 69 files referencing a principle does not mean any single agent loads all 69. Compression into a boot artifact (one screen, one file, always-loaded) is the fix.

**Session closure receipt ≠ boot artifact.** When F13 pastes a compressed artifact and says "I would hand this to every coding agent" — check if it exists on disk AS THAT COMPRESSED FORM. A ceremony audit (gates status, filemap, open items) is a different file from the compressed boot artifact (the 13 Laws, Shadow Test questions, Final Zen). Do not conflate them.

**Tooling traps**

- **Canon-mutate + complex content: write to temp file first.** Shell parsing breaks on JSON parentheses, quotes, and interpolation inside `bash -c "echo '...' >> file"`. The command reports `rc=0` but the content does not land. Fix: write the content to `/tmp/<name>.ext` first, then `cat /tmp/<name>.ext >> <target>` via canon-mutate. `echo -e` and heredocs inside `canon-mutate run ... -- bash -c` break the same way; `cat` from a temp file is the only reliable path. Verify with `grep` after.
- **W_SCAR gate can block base.md edits.** The W_SCAR scar gate flags base.md edits as "touches critical variable" and holds the write across patch/write_file/terminal/execute_code. When this happens, seal all other layers (fragment, ledger, amendment, render, commit) and report the base.md gap explicitly — do not bypass the gate.
- **Some skills cannot be patched by `skill_manage`.** Skills whose directory is a symlink into `/root/AAA/skills/**` resolve for reading but refuse writes; user-owned skills refuse autonomous curation outright. Edit the real file with the `patch` tool, or leave it and tell the user to run `hermes curator adopt <name>`. Do not silently skip the skill layer — say which layer you could not seal. A skill symlinked from a federation repo is outside the profile's writable set (`skill_manage` reports "not found in active profile") — edit the resolved path directly and say so in the report.

## M11 — Verify before reporting

*(from both bodies)*

```bash
grep -c 'C1[0-9]' <membrane file>                      # floors actually landed
grep -n '<fragment>' /root/AGENTS.md                   # fragment is discoverable
/root/scripts/render-agents.sh                         # re-render, then confirm no drift
wc -l <fragment>.md                                    # landed, not just written
python3 -c "import json;[json.loads(l) for l in open('/root/AAA/eurekas/eureka-entries.jsonl') if l.strip()]"  # LIVE FEED still valid JSON
git -C <repo> log --oneline -1                         # per repo — both commits visible
git -C /root/AAA status -sb | head -1                  # pushed, no 'ahead' count
```

Report shape — four beats, no more: **what changed on which surface** → **commit hashes per repo** →
**what is proposed vs live** (the amendment is not wired until a floor exists) → **the one-line
compression**. The open debt belongs in the report, not in a footnote — a sealing report that hides the
unwired part is a false receipt. Report doctrine-layer work as doctrine-layer; never report "sealed" for
work that has no gate.

## Support files

All depth layers from both bodies are carried **live** in this skill (nothing here depends on a frozen
path):

| File | Carried from | Use it for |
|---|---|---|
| `references/commit-gates.md` | `aaa-doctrine-sealing` | the exact gates, labels and the two-ledger layout |
| `references/external-artifact-intake.md` | `aaa-doctrine-sealing` | auditing a pasted external AI artifact before any of it reaches canon |
| `references/doctrine-coding-surfaces.md` | `canon-doctrine-sealing` | worked surface-by-surface recipe: fragment skeleton, membrane floor append, always-on line, eureka artifact + JSONL row, verification sweep, report shape |
| `references/constitutional-compression-patterns.md` | 2026-09-20 session | Two proven compression patterns: Theory→Floor→Kernel→Invariant (69→13→1→1), and Intuition→Formalization (moral physics: constraint extraction → physics → math → code) |

---

## DISCOVERY ANCHORS — retired name, description and triggers (verbatim)

An agent that remembers an **old name** searches for that wording. These anchors keep the retired identity
findable from inside the surviving body, so the capability is never re-authored under a new name. Frozen
body (read-only): `/root/AAA/skills-retired/2026-09-19-v2-doctrine-sealing/canon-doctrine-sealing/`.

**Surviving identity (this skill):** `aaa-doctrine-sealing` — description: *"Seal a session eureka into
AAA canon across all layers."*

### 1. `canon-doctrine-sealing` → MODE M3 (also M1, M4, M5, M6, M7, M8, M9, M10, M11)
- old name: `canon-doctrine-sealing`
- frozen at: `/root/AAA/skills-retired/2026-09-19-v2-doctrine-sealing/canon-doctrine-sealing/`
- original description (verbatim): "Use when F13 says seal or code this into canon."
- original trigger wording (verbatim from the retired body): F13 gives a directive of the form *"seal it"*, *"seal all"*, *"code this into the kernel and state and agents"*, or *"make it live"* — usually after a session that produced a doctrine-shaped finding, often following an audit of an external AI critique.

### Terminology still live in this body
`seal all` · `seal it` · `code this into canon` · `code this into the kernel and state and agents` ·
`make it live` · `canon sealing` · `doctrine sealing` · `eureka packet` · `eureka ledger` ·
`live feed` · `frozen ratified registry` · `surfaces` · `fragment` · `membrane floors` · `base.md` ·
`correction log` · `kernel amendment` · `order of operations` · `render step` · `repo gates`.

DITEMPA BUKAN DIBERI.
