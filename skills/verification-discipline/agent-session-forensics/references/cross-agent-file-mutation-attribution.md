# Cross-agent file-mutation attribution

When a file changed and you did not change it, the answer is almost always another agent on
the same box. Establish *who* and *when* before reporting the change at all — an
unattributed mutation reported as your own work misroutes credit, and one reported as a
defect sends someone hunting a bug that is actually a colleague's fix.

## Ladder (all read-only)

```bash
# 1. When did the target change?
ls -la --time-style=full-iso /etc/<dir>/ | sort -k6,7 | tail -10

# 2. What is in it now (anchor on the line under dispute, not the whole file)?
grep -n -A4 '<anchor>' /etc/<dir>/<file>

# 3. Was there a reload/restart in the same window?
journalctl -u <unit> --since "HH:MM" --no-pager | tail -25

# 4. Which peer touched it? (per-CLI home dirs; repeat per CLI)
find /root/.<agent-home> -type f -newermt '<HH:MM:00>' ! -newermt '<HH:MM:59>' | \
  while read f; do grep -l '<artefact-basename>' "$f" 2>/dev/null; done | head
```

## Backup-name fingerprints

| Name shape | Author |
|---|---|
| `*.bak-<YYYYMMDD>` / `*.backup.<YYYYMMDD>` | a human taking a snapshot before editing |
| `*.bak-<YYYYMMDDTHHMMSSZ>` | a script stamping UTC before a patch |
| `*.bak-<tag>-<YYYYMMDDTHHMMSSZ>` | a script with a reason tag — the tag names the campaign |
| `*.bak.broken-*` / `*.bak-*-fix` | a previous repair attempt; read it before trusting the live file |

The timestamp in the name is evidence of *when*; the sibling ordering (`ls` with
`--time-style=full-iso`) is what proves which version is older when the names disagree.

## Reading a peer CLI's stores

- **History dirs** keep a copy per version: `file-history/<session>/<hash>@vN`. The file's
  mtime is the edit time; `@vN` counts edits. **The stored content is the pre-edit bytes** —
  diff it against the live file to see exactly what the peer added.
- **Transcripts** are JSONL: one object per event, each with an ISO timestamp, a tool name,
  and its arguments (`read_file`, `write_file`, `run_shell_command`, …). Filter on the
  timestamp prefix, find the keyword, print a character window around it — never dump whole
  records, they run to megabytes.
- **Risk/turn telemetry** classifies each turn (observe / mutate) and gives you the shape of
  the campaign even before you find the command.
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
meeting a measurement. Cite the measurement
