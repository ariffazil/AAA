# Cross-agent file-mutation attribution

When a file changed and you did not change it, the answer is almost always another agent on
the same box. Establish *who* and *when* before reporting the change at all — an
unattributed mutation reported as your own work misroutes credit, and one reported as a
defect sends someone hunting a bug that is actually a colleague's fix.

Scope is evidence-bounded (measured 2026-09-17; every claim below carries its verdict).

## Ladder (all read-only)

```bash
# 1. When did the target change?
ls -la --time-style=full-iso /etc/<dir>/ | sort -k6,7 | tail -10

# 2. What is in it now (anchor on the line under dispute, not the whole file)?
grep -n -A4 '<anchor>' /etc/<dir>/<file>

# 3. Was there a reload/restart in the same window?
journalctl -u <unit> --since "HH:MM" --no-pager | tail -25

# 4. Which peer touched it? (repeat per CLI that keeps a history — see the table below)
find /root/.<agent-home> -type f -newermt '<HH:MM:00>' ! -newermt '<HH:MM:59>' | \
  while read f; do grep -l '<artefact-basename>' "$f" 2>/dev/null; done | head
```

**Before step 4, resolve the object you are measuring.** Two traps sit in this ladder, both
verified here:

- **`stat` on a path that is a symlink reports the LINK's own mode, not the target's.** Symlink
  permissions are always `777` and carry no meaning, so a `stat`/`ls -ld` read on `/root/VAULT999`
  returns `777 root:root` while the real target (`/root/arifOS/VAULT999`) is `750 ariffazil:ariffazil`.
  The reading is not wrong, the object is. Resolve first: `namei -l <path>`, `readlink -f`, or
  `stat -c '%i %a %U %n'` on both the link and its target. Reporting a permission from the link is
  the same defect this file is about — attributing a property to the wrong object.
- **A file's own ctime/mtime is not the edit's cause.** Confirm the *content* moved, not just the
  timestamp.

## Which harnesses keep a pre-image store (measured)

| CLI | Store | Shape |
|---|---|---|
| claude | `/root/.claude/file-history/<session-uuid>/` | `<opaque-hex>@vN` |
| qwen | `/root/.qwen/file-history/<session-uuid>/` | `<opaque-hex>@vN` |
| kimi | `/root/.kimi-code/file-history/<workspace>/…/file-history/` (also per-session under `sessions/`) | `<opaque-hex>@vN` |
| codex · gemini · grok · opencode · hermes | **none** | — |

**Absence of a store is not absence of an edit.** Five of the eight harnesses here keep no pre-image
at all, so for those the only attribution path is the transcript (below) plus filesystem forensics.
Do not read "no file-history dir" as "that CLI did not write".

## What `<opaque-hex>@vN` actually is (partly falsified)

- The `<opaque-hex>` is **NOT** a hash of the stored content. Tested and falsified: `sha256`, `md5`,
  `sha1` of the blob, of its first version, and of the file's path/basename/dirname variants all
  miss. It is also not shared across session directories.
- **Consequence — the trap:** you cannot map hash → path. Trying `sha256(live_file)`, searching the
  store for that name, and finding nothing does **not** mean the peer never edited the file. It is a
  false negative, and it is the most likely way this whole procedure gives a wrong answer.
- **The method that works:** identify the live file by **content** (a distinctive line from the
  snapshot), then diff. Walk the snapshots and match text, never key.
- `@vN` does count snapshots and successive versions differ in content (verified: one pair measured
  3770 B → 2935 B). Higher `N` is later. Whether a stored snapshot is the **pre**-edit or
  **post**-edit bytes is **UNVERIFIED here** — no reliable live counterpart was located in this
  measurement. Treat the direction as unproven; if it matters, take your own before/after around a
  known edit and settle it on your own box before relying on it.

## Backup-name fingerprints

| Name shape | Author |
|---|---|
| `*.bak-<YYYYMMDD>` / `*.backup.<YYYYMMDD>` | a human taking a snapshot before editing |
| `*.bak-<YYYYMMDDTHHMMSSZ>` | a script stamping UTC before a patch |
| `*.bak-<tag>-<YYYYMMDDTHHMMSSZ>` | a script with a reason tag — the tag names the campaign |
| `*.bak.broken-*` / `*.bak-*-fix` | a previous repair attempt; read it before trusting the live file |

The timestamp in the name is evidence of *when*; the sibling ordering (`ls` with
`--time-style=full-iso`) is what proves which version is older when the names disagree.

**Keep backups out of the tree they protect.** A `.bak-<ts>` written beside its source is picked up by
the next census/scan of that tree and, inside a skill package, can register as a dead internal
pointer. Write backups to a directory outside every scanned root.

## Reading a peer CLI's stores

- **History dirs** keep a copy per version: `<opaque-hex>@vN`. The file's mtime is the edit time;
  `@vN` counts edits. Diff against the live file to see exactly what the peer added (see the falsified
  hash claim above — locate by content, never by key).
- **Transcripts** are JSONL, but the records are **heterogeneous** — do not assume one uniform
  event shape. Measured over 4,799 records across three harnesses: ~64% carry an ISO timestamp at
  the top level and ~45% carry a tool/command marker, because message records and tool records are
  mixed in one stream (common nested shapes: `{role, content}`, `{role, parts}`,
  `{role, content, id, model, stop_reason}`). Filter by the shape you need — timestamp prefix for
  *when*, nested `content`/`parts` for *what* — and print a character window around the keyword
  rather than whole records, which run to megabytes.
- **Risk/turn telemetry** classifies each turn (observe / mutate) and gives you the shape of
  the campaign even before you find the command.
- **Scan breadth is a cost, not thoroughness.** A recursive glob over a whole home directory
  (`find /root/**`) runs for minutes and can be outpaced by the thing you are chasing. Scope each
  pass to the window (mtime bounds) and the store you established in the table above.
- Watch for a peer's **own uncertainty** in its transcript. A line like "I need to figure out
  whether this was added by something else or by my command" is the peer telling you it does
  not know what it changed — and, if it is heading toward "fixing" a line it calls a
  duplicate, that it may be about to revert a working state.

## What to do with the finding

1. **Do not re-apply and do not reload.** The state is already correct; a reload you perform
   is an unannounced mutation of shared state.
2. **Diff peer history against live** — confirm the live file is the peer's version and not a
   later revert of it.
3. **Report credit explicitly and separately** — what you found, what you changed, and what
   you deliberately did not change. "Verified already-present, no write performed" is a
   complete answer.
4. **Lead with unrequested scope.** If the same agent was also restarting production units or
   rewriting unit files in the window, that parallel unreported change is the headline — not
   the single line you were sent to look at.

## The peer-agreement trap

A peer who "supports option B" after reading the same surface has corroborated nothing — one
source seen twice. A peer reporting a dependency DOWN from an address they memorised, while
your direct probe of the real bind returns 200, is not a second witness either; it is a habit
meeting a measurement. Cite the measurement, never the agreement — and re-probe the address the
claim depends on rather than the one you were handed.
