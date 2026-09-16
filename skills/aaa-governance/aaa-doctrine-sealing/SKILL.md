---
name: aaa-doctrine-sealing
description: "Seal a session eureka into AAA canon across all layers."
---

# AAA Doctrine Sealing — Session Insight → Canon

## When to use

F13 signals, in BM or English: *"seal all"*, *"code this into the kernel and state and agents"*,
*"audit and extract the key eureka insights"*, *"make it live"*. Also load when a session produced a
rule that must outlive the session and bind agents that were not in the room.

Also load when F13 **pastes an external artifact** (another model's plan, audit, or skill list) and asks
for it to be embedded. That request is an **intake**, not a copy job: the artifact is data, and it must be
audited against this machine's canon, paths, and ratified stances before any part of it lands. Read
`references/external-artifact-intake.md` first — a high-quality artifact still needs most of its
implementation rejected, and adopting an address or a gate from outside can undo work already sealed.

Doctrine is not chat output. **Sealing = the rule lands on disk in every layer that reads it, carries a
status label the commit gate accepts, and is pushed.** A rule that exists only in the conversation did
not happen.

## The layers — encode in this order

**1. Fragment** — `/root/AAA/instructions/<topic>.md`
One topic per file; name by class, never by incident. Header carries `> **` lines, one per field:
forged/trigger line, `**Supersedes**` (which earlier shorthand it corrects), `**Binding**` (which
surfaces), `**Lineage**` (prior fragment it extends), `**Status**`, `**Kernel anchor**` (F-floors).
Body: One Rule, the model, numbered laws, the operational gate (pass/fail examples), what is lawful,
profile application, and a **Correction Log** of misreadings that must not be re-imported.

**2. Always-on line** — `base.md`, only if it must bind every turn
`base.md` is the only fragment rendered *inline* into `/root/AGENTS.md`; all other fragments are
`ref:` pointers or footer entries (on-demand). If a rule must apply every turn, add ONE paragraph to
`base.md`. A rule that must bind every turn but lives only in a fragment does not bind every turn.

**3. Floors** — `/root/AAA/instructions/human-meaning-membrane.md`
Append to the `Constitutional Floors (C1-Cn)` list, numbered sequentially, one line each:
`Cn NAME: rule.` These are doctrine-layer: they bind via rendered canon, they do **not** gate a
verdict. Do not imply otherwise in the fragment's Status.

**4. Fragment table** — `/root/AAA/AGENTS.md` (organ repo)
Add a row to the *Active Instruction Fragments* table: `| Fragment | Path | Status |`. This is the
registry other agents read to discover doctrine; an unlisted fragment is nearly invisible.

**5. Eureka ledger** — `/root/AAA/canon/eureka-entries.jsonl` (SOT)
Append one line, keys `{id, timestamp, type, title, source, summary, status}`; `id` = `EUREKA-<TOPIC>-<DATE>`. Include the shadow in the summary — what is NOT sealed (no kernel wiring, open debt).

**6. Kernel** — propose, never self-ratify
Floor changes go to `/root/arifOS/GENESIS/FLOOR_TABLE_AMENDMENTS.md` as
`## Amendment N: <name>` + JSON (`id`, `name`, `rule`, `detection`, `failure_verdict`,
`related_floors`, `doctrine_ref`) + Rationale + explicit `Awaiting: F13 SOVEREIGN ratification`.
`FLOOR_TABLE.json` holds 13 floors — that is constitutional surface. Propose; do not edit it.

**7. Skill (optional)** — if the rule changes how a class of task is done, patch the governing
SKILL.md as well. Otherwise skip; doctrine and skill have different owners.

## Gates and pitfalls

- **New watched `.md` needs a Status line or the commit is blocked.** The AAA commit hook
  (`doctrine-status-gate`) refuses a new file under watched paths with no label; accepted labels are
  `DRAFT_*`, `PENDING_*`, spec, or an F13 instrument. Ratified-class wording must carry an F13
  instrument (date or quote) — a bare `RATIFIED` blocks, ANNEX-class values block.
- **Run `/root/scripts/render-agents.sh` after editing any fragment or `base.md`.** It rewrites
  `/root/AGENTS.md` (inline base + `ref:` pointers + `UNRENDERED_FRAGMENTS` footer) and writes
  `/root/CLAUDE.md` as a pointer. Skip it and agents keep reading the stale map. Verify with
  `grep -n '<topic>' /root/AGENTS.md`.
- **Two eureka ledgers exist; only one is canon.** `/root/AAA/canon/eureka-entries.jsonl` is the SOT
  (`canon/*.md` and `instructions/anti-calhoun.md` cite it). `/root/AAA/eurekas/eureka-entries.jsonl`
  is a stray with a different entry shape and no readers. Appending to the wrong one silently loses
  the record. See `references/commit-gates.md`.
- **Sweep for an existing owner before minting.** Parallel agent sessions on the same box mint the
  same insight independently. Before writing, grep the ledger, the fragments, and `git log` for the
  topic; if an owner exists, fold the delta into it instead of creating a second file
  (one fact, one owner, one axis).
- **Some skills cannot be patched by `skill_manage`.** Skills whose directory is a symlink into
  `/root/AAA/skills/**` resolve for reading but refuse writes; user-owned skills refuse autonomous
  curation outright. Edit the real file with the `patch` tool, or leave it and tell the user to run
  `hermes curator adopt <name>`. Do not silently skip the skill layer — say which layer you could not seal.
- **Push is a gate, not a formality.** `git -C /root/AAA push` runs the F1–F13 governance check;
  arifOS pushes also run the drift check and print source vs deployed.

## Verify before reporting

```bash
wc -l <fragment>.md && grep -c 'C1[0-9]' human-meaning-membrane.md   # landed, not just written
/root/scripts/render-agents.sh && grep -n '<topic>' /root/AGENTS.md  # rendered into the live map
python3 -c "import json;[json.loads(l) for l in open('<ledger>') if l.strip()]"  # ledger still valid JSON
git -C /root/AAA log --oneline -1; git -C /root/AAA status -sb | head -1   # committed AND pushed (no 'ahead')
```

Report the debt explicitly: which layer is live, which is proposed, which could not be sealed. A
seal whose gaps are hidden is worse than no seal — the next agent trusts it.

## References

- `references/commit-gates.md` — the exact gates, labels and the two-ledger layout.
- `references/external-artifact-intake.md` — auditing a pasted external AI artifact before any of it
  reaches canon: citation and foreign-seal checks, the duplicate-owner **and layer** sweep, vocabulary
  collision against tokens canon already binds, address/config verification before adopting a path or a
  key, gate-direction conflicts with a ratified stance, and how to record accept / reject / HOLD.
