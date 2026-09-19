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

## The two eureka ledgers — one FROZEN RATIFIED REGISTRY, one LIVE FEED

Two ledgers exist **by design**, and neither is a stray: one was frozen as a ratified registry, the other
is the live feed. Attribute evidence, read with `lsattr` on 2026-09-19:

| path | status | attribute (`lsattr`) | rows · last written | shape |
|---|---|---|---|---|
| `/root/AAA/eurekas/eureka-entries.jsonl` | **LIVE FEED — the WRITE TARGET** | `--------------e-------` — writable, no immutable flag | 14 rows · 2026-09-18 (the newer of the two) | `{ts, agent, session, eureka, evidence, truth_class, actor, verdict}` |
| `/root/AAA/canon/eureka-entries.jsonl` | **FROZEN RATIFIED REGISTRY** — historical authority; **cite, never write** | `----i---------e-------` — **IMMUTABLE**; an append returns EPERM even as root unless the attribute is cleared, which is forbidden | 109 rows · 2026-09-16 | `{id, timestamp, type, title, source, summary, status}`, `id` = `EUREKA-<TOPIC>-<DATE>` |

**Append to the LIVE FEED: `/root/AAA/eurekas/eureka-entries.jsonl`.** The canon file is immutable by
design — it is the ratified historical record, cited by `canon/*.md` and `instructions/anti-calhoun.md`.
Cite it as authority; never use it as a write target, never unlock it, never clear its attribute.

Readers of the live feed (verified 2026-09-19) — so it is not an unread file:
`governance/durable-artifact-authoring/SKILL.md` (~line 87 instructs appending there), this
`commit-gates.md`, and `governance/AMENDMENT-6-REGISTER-LAW-RATIFICATION-2026-09-15.md`.

**Correction carried (do not re-import).** This section previously listed the canon file as the SOT and
instructed "append to canon", and labelled the live feed *"stray; no script reads it (only the `.ua`
scanner and git index see the path)"*. Both halves were wrong and the label was factually inverted: the
canon target cannot be written at all (immutable attribute → EPERM), and the "stray" is the live feed the
federation actually reads. **Never port entries between the two ledgers** — the frozen registry is a
historical snapshot; the live feed is the flowing record. The live feed is not under the canon lock
(writable, no immutable attribute); the canon-mutate cycle remains mandatory for anything under
`/root/AAA/canon`, `/root/AAA/governance`, `/root/arifOS/GENESIS`. If you find new eurekas, write to the
live feed.

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

Entry count sanity: `wc -l` the **live feed** before and after; all lines must parse as JSON:

```bash
wc -l /root/AAA/eurekas/eureka-entries.jsonl                                        # 14 rows before this write
python3 -c "import json;[json.loads(l) for l in open('/root/AAA/eurekas/eureka-entries.jsonl') if l.strip()];print('ok')"
```

Never run this against the frozen registry file — it is append-frozen and read-only by design; a parse
check there is harmless but implies it is a write target, which it is not.
