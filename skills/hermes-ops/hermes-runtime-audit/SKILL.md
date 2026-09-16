---
name: hermes-runtime-audit
description: "Use when auditing or organizing the Hermes runtime itself."
version: 1.0.0
floors: [F2, F11]
triggers:
  - "apex swot on hermes"
  - "audit my hermes"
  - "organize the runtime"
  - "runtime is chaos"
  - "why is hermes slow"
  - "prompt too big"
  - "context window"
  - "hardening queue"
  - "hermes internal structure"
---

# Hermes Runtime Audit

Auditing the *harness itself* — its prompt budget, storage, surface inventory, and directory law — is a
different job from auditing work done inside it. The deliverable is measured findings plus a hardening
queue plus a forge list, not a narrative.

## Rule 0 — every claim carries a number

Do not answer a runtime question from config alone. Config describes intent; the runtime is the
reconciliation of config, process environment, and whatever sits in front of the process. Read the
number, quote the command, and mark anything you did not measure as UNKNOWN rather than plausible.

The three counts that must never be collapsed into one:

| Count | Meaning |
|---|---|
| **configured** | what a file declares |
| **loaded** | what the process actually resolved at boot |
| **credentialed** | what has a key/host/path present to function |

A provider selected but uncredentialed, an MCP server configured but parked, a tool whose availability
check fails and quietly vanishes from the schema — all three are *configured but not loaded*, and the
harness will describe itself as if they worked. That gap is the finding.

## Procedure

### 1. Fixed prompt tax — measure this first

```bash
hermes prompt-size          # add --json for machine-readable
```

Report: system-prompt total, the tier split (stable / context / volatile), skills-index size, tool-schema
size, and the top-N skills by SKILL.md bytes and index cost.

- The **skills index** is normally the single largest line item. Index bytes ÷ 4 ≈ tokens paid on every
turn of every session, forever. Say it that way — a per-turn figure lands; a byte count does not.
- Cross-check **tools loaded vs tools configured**: a small schema count against hundreds of deferred
tools means lazy tool loading is working and must not be touched. Never recommend a shrinking measure
  before confirming the deferred-loading path is what is keeping the estate alive.
- A large `SKILL.md` costs nothing until loaded; a large *index entry* costs every turn. Keep those two
  columns separate when ranking offenders.

### 2. Reconcile the context contract — three numbers, smallest wins

This is the highest-severity check in the audit, because a wrong window is self-consistent and silent.

```
harness config      model.context_length            (config.yaml)
proxy in front      the request-size clamp constant (grep the middleware source for the guard var)
upstream model      real window (provider /v1/models, or the local model registry cache)
truth               = min(all three)
```

Find the proxy by reading the harness process environment, not the CLI's:

```bash
tr '\0' '\n' < /proc/<gateway-pid>/environ | grep -iE 'BASE_URL|API_BASE|OPENAI'
ss -ltnp | grep -E ':<port>\b'          # who actually owns each hop
```

If the harness believes a window larger than the clamp, **its own compressor never reaches threshold, so
it never fires** — and the proxy drops older turns instead, with no line in the harness logs. The visible
semantics are a confident answer built on a truncated past. Fix by lowering the harness's declared window
to the binding floor so compression happens where you can see and log it: **compression you can read
beats truncation you cannot.**

A clamp that logs **zero** hits across a long window is unresolved, not healthy — either it is not firing
or it is not logged, and those need opposite fixes. Go read the drop path before calling it clean.

### 3. Storage and retention

```bash
du -sh ~/.hermes/* | sort -h | tail -20
df -h /
ls -la ~/.hermes/state.db*
hermes sessions stats
```

Then attribute the database by table rather than quoting one total:

```bash
python3 -c "import sqlite3;c=sqlite3.connect('state.db');\
[print('%-32s %8.1f MB'%r) for r in c.execute('select name,sum(pgsize)/1048576.0 m from dbstat group by name order by m desc limit 15')]"
```

Typical shape: message bodies dominate, FTS shadow tables are a large second, archived system prompts a
third. Call out **redundant copies** (state snapshots, `.bak-<timestamp>` databases, secret-file backups)
separately from live data — a backup of a database that is still live is not an archive, it is sediment.

Maintenance commands exist and are usually un-wired; check before recommending anything custom:
`hermes sessions optimize-storage`, `sessions optimize`, `sessions prune`, `sessions archive`.

### 4. Surface inventory

```bash
hermes doctor
hermes status
hermes curator status
hermes memory status
hermes mcp list
```

Pull four numbers out of these and report them side by side: **managed vs unmanaged skills**, **enabled
vs disabled cron jobs**, **enabled vs parked MCP servers**, **deliver-target spread** (how many scheduled
jobs deliver to a channel a human actually reads versus to `local`).

Two falsifiable health reads worth stating explicitly:
- A cron job that is disabled but still resident is the same failure as a directory nobody owns: it is
  inventory, not capability. Report the disabled count as a *triage queue*, not as a backlog.
- A memory provider selected with no credential present makes the harness emit a false capability claim
  into the system prompt on every session. Check for the *credential*, not the selection.

### 5. Directory sprawl and the ownership law

```bash
ls -d ~/.hermes/*/ | wc -l
for d in ~/.hermes/*/; do printf '%-22s %6s files\n' "$(basename $d)" "$(find $d -type f | wc -l)"; done
```

Split the top level into **harness-native** (sessions, cron, logs, memories, skills, plugins, cache,
workspace — the harness created and owns these) and **federation-invented** (everything added for
local doctrine and process). Then state the law the estate is missing:

> A directory without an owner, a retention rule, and a declared writer is not architecture. It is
> sediment.

The fix is not deletion, it is a **manifest**. One row per top-level path, and an unlisted path is a
governance defect rather than a feature:

```yaml
path: <relative path>
owner: <agent/organ>
writer: hermes|agent|cron|human
retention: permanent|<Nd>
mutability: append-only|read-only|read-write
delete_authority: F13
last_reviewed: <YYYY-MM-DD>
```

Pair it with a retirement law — every artifact class gets a scheduled death review:

| Class | Review | Default outcome |
|---|---|---|
| skill unused 30d | curator weekly | archive |
| cron job disabled >14d | monthly | delete or resurrect, never linger |
| top-level dir with no manifest row | monthly | merge into the declared federation namespace or archive |
| state snapshot >7d | weekly | delete, keep one |
| systemd drop-in `*.bak` | monthly | delete |
| secret-file backup | on rotation | delete prior copies |

### 6. Secret surface, by mode not by name

Do not list secret files — list the ones whose **mode** is wrong:

```bash
for f in $(grep -rlE '(API_KEY|TOKEN|SECRET|PASSWORD|_KEY)=[^$]' /etc/systemd/system/ 2>/dev/null); do
  p=$(stat -c '%a' "$f"); [ "$p" != "600" ] && echo "OPEN $p $f"
done
```

A world-readable unit or drop-in holding a plaintext key is a **fix, not a queue item** — tighten it
in-session and re-run the sweep to show the result. Note separately that the harness's own `.env` is
not inherited by a systemd-launched service, so any key present only there is absent from the gateway
process; verify against `/proc/<pid>/environ` rather than the file.

### 7. Config sprawl at the process layer

Count the systemd drop-ins for the gateway unit. Ordering-dependent names, inert `.bak` files sitting
beside live ones, and settings re-declared in two places are all the same defect: the effective
environment is no longer readable from one place. State the count and name the precedence trap
(a service-level `EnvironmentFile` outranks a drop-in) — that is the thing that costs a future session
an hour.

## Output shape Arif wants

- **Plain BM, compressed, decision-shaped.** Lead with the one-line verdict, then the findings that
  change a decision. No headers-in-chat, no receipt labels, no delta notation.
- **Land the long artifact in a file**, not in the reply: `/root/AAA/reports/HERMES-RUNTIME-<KIND>-<YYYY-MM-DD>.md`,
  structured as measured reality → SWOT → reflection → target structure → hardening queue (P0/P1/P2 with
  exact commands) → missing capabilities. Every figure in it must be re-derivable from a command printed
  in it.
- **Ship a staged script for anything destructive**, defaulting to dry-run, with `--apply` (and a
  separate opt-in tier for the restart batch). He runs it, you do not surprise him.
- **End on the binary decisions only he can make** — the ones that are architecture, money, or
  irreversible. Do the rest yourself and report it as done. "Aku dah buat X" beats "you could do X".
- When the finding is about the harness's own blindness, say it as blindness, not as error: a system
  that reports a window it does not have is not lying, it has a shadow — and shadows that live inside a
  self-report are worse than bugs, because they get reported *as* truth.

## Pitfalls

- **Don't rank findings by severity before probing substance.** A directory with 27 files and a directory
  with one file can matter equally; the audit's job is to distinguish *sediment* from *organ*, and size
  does not do that. Count the classes, then judge each class on its blast radius.
- **Never present a queue item you can safely finish.** Mode fixes, `.bak` deletion, stale-snapshot
  reclamation and DB compaction are all reversible; queueing them as "for your approval" converts your
  own work into his attention cost, which is the one resource the whole doctrine exists to protect.
- **A stale capability is more expensive than a missing one.** A tool an agent *believes* it has produces
  confident wrong output; a tool it knows it lacks produces a probe. When reporting the configured/loaded
  /credentialed split, mark the middle column as the dangerous one.
- **Re-measure after any fix.** `hermes prompt-size`, `hermes doctor`, `df -h /`, `hermes sessions stats`
  again — an audit that ends without a second reading has no evidence the fix landed.
- **Two sessions can mutate the same runtime.** Before attributing a change, check whether a concurrent
  session or a scheduled job touched the same files in the window; if you did not sweep every writer,
  report the change without naming an author.

See `references/probe-cookbook.md` for the full one-shot command set, including the storage attribution
query and the surface-inventory sweep.
