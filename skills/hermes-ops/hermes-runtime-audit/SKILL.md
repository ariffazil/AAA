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
- **Enabled is not firing — never report the enabled count as the running count.** Cross-check each
  enabled job's `job_id` against the execution ledger (`cron/executions.db`) and against its own schedule
  period before saying a job runs. `last_status: "ok"` is written on completion, so a job that stopped
  firing keeps its last `ok` forever. Enabled-but-dark jobs are the most common way a runtime audit
  under-reports failure while every surface still reads green.
- A memory provider selected with no credential present makes the harness emit a false capability claim
  into the system prompt on every session. Check for the *credential*, not the selection.

### 4b. Behavioural record — what the harness actually did

Config and inventory answer "what exists". The state store answers "what is used", and it is the only
surface that can falsify an inventory claim. Probe it read-only (`file:...?mode=ro`) so a live gateway
keeps its write lock.

- **Tool-call frequency** from `messages.tool_name` is the exact usage table. Do not regex message
  `content` for `"name":` — that over-counts repeated mentions and silently skips calls whose payload
  was compacted away.
- **Session timeline**: `sessions.source` splits telegram / cron / subagent / cli, and `sessions.started_at`
  is a UNIX epoch string — `substr()` on it yields epoch digits and a garbage date axis.
- **Delivery**: group `delivery_obligations` by destination *before* concluding anything. One blocked
  bot-to-bot channel can hold every failure while human delivery is 100%; an aggregate rate is not a
  finding until the split is known.
- **Delegation outcomes** from `async_delegations` — counts and states only. Never `SELECT *`: its
  `event_json` / `result_json` hold whole subagent transcripts, and one row will flood the context window
  and end the session.

Two rules decide whether this section produces a finding or a fabrication:

- **A null sensor is not a measurement.** If a usage store carries an entry per skill and a null count, it
  is a presence list, not a sensor. Report *unmeasurable*, never *unused* — and never fill the gap with an
  estimate. A fabricated ranking is inherited as fact by the next session.
- **A capability built during the audit is still a finding.** Before proposing to build something the audit
  found missing, check the newest mtimes on the candidate surfaces; a sibling session may have built and
  scheduled it within the same hour. Timestamp every reading and re-read any count before publishing it.

Queries for all of the above: `references/state-store-queries.md`.

### 4b-bis. Session close is recorded but never propagated

The session store records the end of every conversation — an `ended_at` plus an `end_reason` such as
`session_reset` (a human typing `/new` on a chat surface) — and nothing consumes it. A federated
carry-forward file can therefore sit for days with an empty anchors list while every conversation has a
clean close recorded in the store. **The close exists; it is not propagated**, so the next session
starts with no temporal awareness at all and answers as if the last turn were seconds ago when the
human has slept and moved to a different part of their day.

The repair is **two agent-triggered scripts, no cron and no daemon**:

```bash
python3 /root/scripts/session-closer.py        # backfill close anchors from the store (idempotent)
python3 /root/scripts/temporal-briefing.py --compact   # gap + sleep/meal boundary + open loops
```

The closer reads ended sessions, dedupes against anchors already present, and writes a
`session/close:<id>` anchor plus an event entry plus an on-disk summary. Run it at session start; the
value is needed at exactly one instant, which is why a periodic scheduler is the wrong instrument (see
the standing objection in Pitfalls).

Pitfalls specific to this repair:

- **`sqlite3` rows are tuples.** `row.get()` and `row["col"]` both raise unless `row_factory` is set to
  `sqlite3.Row`; mixing a row_factory in one function and bare tuples in another is an `AttributeError`
  on the first run. Convert to dicts, or set the factory once and be consistent.
- **Dedupe by anchor name, not by recency.** The closer runs repeatedly; without a name-existence check
  it appends a duplicate anchor for every session on every run.
- **Skip zero- and one-message sessions.** They are reset artifacts, not conversations, and they pollute
  the briefing with empty closes.
- **Never infer the gap from the current clock.** Use the store's `started_at`/`ended_at` and the anchor
  timestamps. A `date` call reports now, not when the human last spoke.

### 4c. MCP surface truth — census, supervisor, and advertisement are three different things

The census and `hermes mcp list` answer *configured*. Neither answers *supervised* or *advertised*,
and the three disagree in ways that each produce a different defect.

```bash
ls ~/.hermes/mcp/                                 # what has an implementation directory
systemctl list-unit-files | grep -iE '<server>'   # what has a supervisor
ss -tlnp | grep -E ':<port>\b'                    # what is actually listening
```

- **An implementation directory and a listening port with NO systemd unit is the highest-severity
  shape here.** Its enforcement surface is unreachable after any restart, with no auto-recovery, and
  nothing in the census says so. Report "runs only when manually started" as a governance gap, not
  an ops nit — check the unit before believing any server is durable.
- **A server advertised somewhere but implemented nowhere.** Grep the whole config tree, not the
  census: a directory holding only a config file and a test, with no entrypoint, is a configured
  phantom. It may not appear in the census at all — absence from the census is not absence of the
  claim.
- **The census footer carries a timestamp; read it before quoting the census.** A stale census is a
  snapshot of *intent*, and its per-row `last_smoke_test` stamps are written per generation, so every
  row looks fresh while the file itself is hours old. **Freshness = the file's mtime, not the field
  inside it.** Then judge the mtime against the **producer's own period**, not against "now" — a census
  rebuilt four times a day is healthy at six hours old and broken at six hours *past its slot*. Quote
  the cron period beside the age so the reader can tell a normal gap from a dead schedule.
- **An advertisement inside a tool description is the worst case**, because it is served to every
  client rather than sitting in a file. A description claiming a source was "live-probed" while that
  service is down has the server lying on its own behalf. A census-based inventory is blind to
  this — read tool descriptions, not just the server list.

Two error shapes from one server is normal and worth naming separately: a doctrine/policy rejection
returned as an ordinary result (`ok: false`, `isError: false`) beside a schema rejection raised as a
protocol error (`isError: true`). A caller cannot branch on one field, so report the shape, not just
the instance.

Note on enum drift: a served mode enum narrower than the code constant (with a third number in a
source comment) is not "the schema lies" — the direction is *served ⊆ code*. Read the handler's mode
dispatch before recommending a prune; the number that matters is which modes the dispatcher actually
implements.

### 4d. Public exposure — three layers, and the fix is usually verified at the wrong one

§4c answers whether a server is *configured, supervised and advertised*. None of those answers whether
an outsider can **reach** it. Reachability has its own three layers, and they are read with three
different instruments:

```
origin vhost     curl -k --resolve <host>:443:127.0.0.1 https://<host>/<path>   # the machine's own answer
edge ingress     the tunnel config's hostname -> service mapping                  # what the tunnel claims
public hostname  curl https://<host>/<path>                                      # what the world gets
```

The `--resolve` SNI test is the only way to ask the origin directly; without it you are measuring the
edge and calling it the server. Read the response **headers**, not the status: a service that answers
`X-Organ: HERMES` at the origin is not the same service that answers at the public hostname.

- **A fix verified at the origin is not a fix.** Measured on this host: the ingress comment recorded
  *"Verified by SNI test: HTTP 200 + Mcp-Session-Id + X-Organ: HERMES"* — all true, **all at the
  origin**. Over the public hostname the same path returned **404**, and `/` returned a different
  organ's HTML entirely. Three layers, one of them working, and the receipt named the layer that
  passed. When you cite a reachability test, cite the layer it was run against.
- **Compare the public body against the organ it claims to be.** Fetch the hostname's `/` and read the
  description/`X-Organ` header; fetch a sibling hostname and compare. Two hostnames returning the same
  body means one of them is misrouted — a routing defect that no census, unit file or smoke test in
  §4c can surface.
- **A public `404` on an MCP path is a reachability defect, not an application defect.** The path
  either never arrives (wrong origin at the edge) or arrives and is not handled (wrong vhost). The
  origin probe separates those two, and they have opposite fixes.
- **Internal-only is a legitimate state; unrecorded internal-only is not.** A server bound to
  loopback with no ingress rule is fine *if the inventory says so*. What must never stand is a hostname,
  a comment, or a tool description implying external reachability that the edge does not provide.

### 4e. Doctrine-only capability — advertised in knowledge, absent in execution

§4c covers a server advertised but implemented nowhere. The inverse shape is more dangerous to an
agent: **implemented, advertised in the skill corpus, and not running.**

```bash
systemctl show <unit> -p LoadState,ActiveState,UnitFileState --value
ls -la $(systemctl show <unit> -p ExecStart --value | grep -oP 'path=\K[^ ;]+')
```

The signature is three readings that disagree in a specific way: an `ExecStart` path that **exists**,
`ActiveState=inactive` with `UnitFileState=disabled`, and **zero** references in the runtime config —
while N *skills* name the capability. Measured: a graph database server with a 4 KB start script on
disk, unit inactive and disabled, absent from both the runtime config and the MCP census, yet named in
8 skill files.

- Report this as a **knowledge/reality split**, not as an outage. Nothing is broken; the doctrine has
  outrun the substrate, and the cost lands on the next agent that reads the skill, believes the
  capability, and plans on it.
- The severity question is not "is it up" but **"does anything instruct an agent to depend on it"**.
  `grep -rl <name> ~/.hermes/skills/` is the blast-radius probe; config and census will both read clean.
- The fix is usually one of two opposite acts — wire the unit, or mark the skills as aspirational.
  Deciding which is an authority question, so put it to the principal as one binary, not a menu.

**The per-room / per-person instruction surface is the same shape.** Before writing a conduct rule,
person register or room limit into the layer that is *supposed* to inject it — a lane plugin, a
gateway hook, a persona module — read the layer's own liveness, then find the surface that actually
reaches the model:

```bash
grep -c <plugin_name> ~/.hermes/logs/gateway.log     # 0 = not in the loaded plugin set
hermes config get plugins                            # what the profile actually enables
```

Three readings decide it, and they fail independently: the plugin is listed under `plugins.enabled`; the
registry file the module loads actually exists; and exercising the module's own builder with a real lane
returns non-empty text. A module can sit on disk, be fully implemented, and still fail the second and
third — it then degrades *silently* (fallback lane, empty card) while the diff, the file listing and the
doctrine all say the wiring is done. Every rule written into it reaches no model. Report the layer as
inert and name which reading failed; never call such a wiring working because the code looks correct.

**The effective alternative for per-room rules is `telegram.extra.channel_prompts.<chat_id>`** in the
profile config — per-chat instruction text injected on arrival, independent of any plugin. Recipe,
verification and content rules: `references/room-scoped-instruction-prompts.md`. Prefer the surface you
can prove reaches the model over the layer that merely looks finished.

### 4f. The enforcement gate is a text classifier — audit it as one

The `pre_tool_call` shell hook is the harness's first runtime enforcement path, and it decides
allow/block by reading the tool payload. It is a classifier over **text**, so audit it by its two error
directions, never by its rule count:

```bash
grep -n "CLAIM_TEXT_FIELDS\|has_critical_claim\|def verify_provenance\|^T3_PATTERNS\|^W_SCAR_CRITICAL" <hook>.py
wc -l ~/.local/share/arifos/hermes_hook_receipts.jsonl      # is the gate deciding at all?
```

**False positive — STRUCTURE read as assertion.** The gate grepped `json.dumps(tool_input)` wholesale,
so a file *path* containing a trigger word was read as a claim: a doctrine patch was refused twice, and
a read-only `grep` naming the same file once, because a directory in the path was named `court`. The
payload asserted nothing. **Token-level matching over the serialized payload cannot tell a path, an
id, or an enum from prose** — and the file a claim is written into is not the claim.

**False negative — SHAPE read as witness.** Provenance passed if the payload merely *contained* the
token `url`/`source`/`evidence`. Any string satisfies that, so a fabricated figure with the word "url"
beside it cleared the gate. A check that asks whether a citation-shaped string is present is not a check
on whether the citation holds.

**The repair pattern — claim surface + verified provenance:**

1. Scan only claim-bearing fields (`content`, `new_string`, `command`, …) — never the whole payload.
2. Strip structure *before* matching: URLs, file paths, receipt ids, code spans. Collect the URLs first,
   then remove them.
3. Verify provenance instead of detecting its vocabulary: extract cited URLs and resolve them.
4. Three provenance fates, three decisions: `VERIFIED` (a URL resolves, or a receipt id / on-disk
   evidence path exists) → allow + witness receipt; `UNRESOLVED` (URLs present, none resolve) → block;
   `ABSENT` → block.
5. **A network fault must never become a blanket denial of service.** Timeout, TLS failure and refusal
   are `DEGRADED` → allow. NXDOMAIN is a fact about the *citation*; a timeout is a fact about *your
   link*. Collapsing them turns an outage into an enforced halt on all work.
6. Any widening — a path whitelist, an exempt tool class — is a bypass. Count every exempted call to
   telemetry so abuse is visible, and say in the receipt which widening you introduced and how to
   reverse it. A silent exemption is indistinguishable from a hole.

**Read-only detection:** split a compound command on `&& || | ;` and require EVERY segment to be a
probe. A single regex anchored at the start of the whole command reads `cd X && grep … | head` as a
mutation, which is the path false-positive one layer down.

**Implementation traps when a gate matches text over a serialized payload** (permanent language
behaviour, not environment state):

- `json.dumps` **escapes** quotes to `\"`. A regex written against plain text
  (`"receipt_id": "..."`) will not match the serialized form the gate actually receives. Unit-check the
  pattern against `json.dumps(...)` output, never the plain string.
- **Regex alternation is ordered.** `json|jsonl` truncates `evidence.jsonl` to `evidence.json`, and the
  bug is invisible because the truncated path simply fails to exist. Longest alternative first.
- `urllib.request.urlopen` **wraps socket faults in `URLError`** — `except socket.gaierror` never fires.
  Inspect `exc.reason` to tell NXDOMAIN from a timeout.

**Validate both directions, plus a negative control.** A fixture of three classes: previously-blocked
read-only cases (must allow), previously-passing fabrications (must block), true positives (must allow).
Then feed input that MUST be rejected and confirm it refuses. A check whose failure you have never
observed is decoration — and expect the fixture to find real bugs in the new code, including in the
receipt-id pattern the gate uses to read its own receipts.

**Tie the decision order to the constitution, not to convenience.** The circuit-breaker branch is
checked before every other rule and must fail *closed* when its authority cannot be loaded — an
unreadable brake is not an absent brake. Read-only observation stays available while the brake is
tripped: a brake that blinds the operator cannot be released safely. Preserve the exit-code semantics
(one code for a constitutional block, a distinct one for a circuit-breaker interrupt) and say so in the
receipt; collapsing them destroys the caller's ability to branch.

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

**Test the standalone caller separately from the daemon.** A gateway that is alive and answering proves
only that the *daemon* path resolves its credentials. CLI subcommands, cron jobs and scripts that reuse
the same config run as separate processes and can be dead while the gateway stays green — most often
because the daemon is surviving on a systemd drop-in that hardcodes a variable name the config only
*declares*. Probe each caller class once, for real:

```bash
systemctl cat <unit> | grep -E 'EnvironmentFile|^Environment='   # merged view, drop-ins included
<cli> send --to <platform>:<id> --json "probe"                   # the standalone path
```

Report a broken standalone path as a finding about *that* path. Never generalise it into "the platform is
down", and never let the daemon's health stand in for the CLI's — the two answer different questions.

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
- **Never select payload blobs while auditing storage.** `event_json`, `result_json` and large message
  bodies hold whole transcripts; a single careless `SELECT *` on a history table costs the working session.
  Counts, ids and scalar columns only.
- **Don't rank capability by a store that records no counts.** A usage file with one entry per skill and
  null counts invites a confident "most skills are unused" finding the sensor cannot support. Say which
  sensor was null, and what would have to be wired before the question is answerable.
- **A gate's hold ratio is not its error rate.** The telemetry file records holds over total decisions;
  a ratio near zero means either a working gate or one whose rules never match, and the number alone
  cannot tell you which. Read the recent receipt rows to see *which* rule fired and against what payload,
  then judge. An enforcement path with zero recorded blocks and a growing receipt count is a gate that
  runs, not a gate that catches — do not report it as either healthy or broken on the ratio alone.
- **A fix that unblocks your own audit is proven by the audit continuing.** When you cannot complete a
  review because a control refuses the work, repairing the control and then completing the review in the
  same pass is the test of the repair — and the refusal itself belongs in the finding, quoted with the
  payload that triggered it. Routing around the control instead supplies the incident rather than the
  audit.
- **No background scheduler for value needed at one instant.** The standing objection to periodic jobs is
  that they consume the box continuously for work whose value is only realised at a single moment. Prefer
  an agent-triggered script at the moment of use over a cron entry, and never add a daemon to watch for an
  event the store already records — the store plus a one-shot read is the whole mechanism.
- **A capability absent from the tool schema is not an absent capability.** CLI lanes that a *skill*
  documents are invisible to tool search, so "no matching tool" is a fact about the schema, not about the
  machine. Before telling the principal you cannot reach a resource, sweep the skill corpus and the
  installed binaries for a lane — a false "I have no access" pushes manual verification back onto the one
  person whose attention the whole system exists to protect, and it is usually wrong.

See `references/probe-cookbook.md` for the full one-shot command set, including the storage attribution
query and the surface-inventory sweep. See `references/state-store-queries.md` for the behavioural-record
probes (usage frequency, session timeline, scheduler book vs execution ledger, delivery split). See
`references/room-scoped-instruction-prompts.md` for the per-room conduct surface — how to set, verify and
activate `telegram.extra.channel_prompts`, and what belongs in one.
