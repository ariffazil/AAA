# Commit gates, labels, and ledgers

## doctrine-status-gate (AAA repo, runs at commit boundary)

Rules apply to `Status:` lines only — body prose is never blocked.

| situation | what the gate does |
|---|---|
| new watched `.md`, no `Status:` line | **blocks** (`R3 … new watched .md has no Status line`) |
| ratified-class value with no F13 instrument | **blocks** — needs a date or an F13 quote |
| bare self-label (`Status: RATIFIED`) | **blocks** |
| ANNEX-class values (`CONSTITUTIONAL_ANNEX`, …) | **blocks** |
| `DRAFT_*` / `PENDING_*` / spec labels | passes |

Accepted shape that passes on a first try:

```
> **Status:** F13_RATIFIED_CHAT (YYYY-MM-DD) — sovereign-directed in ARIF dm: *"<short quote of the order>"*
> **Kernel anchor:** F2 TRUTH, F6 EMPATHY ⇄ MARUAH, F7 HUMILITY, F9 ANTIHANTU.
```

Check before committing rather than guessing: grep a recently sealed fragment in
`/root/AAA/instructions/` for its `Status:` line and copy the register.

## Push gates

- `git -C /root/AAA push` — prints a governance banner and `Normal push — governance gate passed`.
  The remote may add `Bypassed rule violations …` for unrelated required checks; that is not your file.
- `git -C /root/arifOS push` — additionally runs the drift check and prints
  `deployed=<sha> HEAD=<sha> drift=<bool> status=<…>`.

Treat `drift=True` as a **question, not a verdict** — a commit-hash monitor over-reports when the
delta contains no runtime code. Check the diff for `.py/.ts/.js` changes before reporting a kernel
as broken; a hash is a proxy for behaviour, not behaviour.

## The two eureka ledgers

| path | status | shape |
|---|---|---|
| `/root/AAA/canon/eureka-entries.jsonl` | **SOT** — cited by `canon/*.md`, `instructions/anti-calhoun.md` | `{id, timestamp, type, title, source, summary, status}`, `id` = `EUREKA-<TOPIC>-<DATE>` |
| `/root/AAA/eurekas/eureka-entries.jsonl` | stray; no script reads it (only the `.ua` scanner and git index see the path) | `{ts, agent, session, eureka, evidence, truth_class, actor, verdict}` |

Append to **canon**. If the stray already holds an entry that canon lacks, port it (write a canon-shaped
entry preserving the original timestamp and naming the source as a port), then leave a short
non-canonical marker file in the stray's directory stating where the SOT is — so the next agent does not
repeat the split. Never delete the stray: it is still evidence of what was recorded when.

## Canon-mutate content injection pattern

JSON, multi-line text, or content with shell-special characters must NOT be passed inline in
`bash -c "echo '...' >> target"`. Shell parsing breaks on parentheses, quotes, and `$` signs;
the command reports `rc=0` but the content does not land — a silent failure.

Correct pattern:
```bash
# 1. Write content to temp file (any tool — write_file, python, heredoc)
python3 -c "import json; open('/tmp/entry.jsonl','w').write(json.dumps(entry))"

# 2. Append via canon-mutate using cat (not echo, not inline)
ARIFOS_TRACE_ID=trc-<id> /root/scripts/canon-mutate run <tree> -- \
  bash -c 'cat /tmp/entry.jsonl >> <target-file>'

# 3. Verify
grep '<unique-string>' <target-file>
```

`echo` with `-e` or heredocs inside `canon-mutate run ... -- bash -c` also break on complex
content. `cat` from a temp file is the only reliable path.

Entry count sanity: `wc -l` the ledger before and after; all lines must parse as JSON:

```bash
python3 -c "import json,sys;[json.loads(l) for l in open('/root/AAA/canon/eureka-entries.jsonl') if l.strip()];print('ok')"
```
