# Gate-estate audit — brief, probes, schema

Copy-paste kit for §4g. The brief is the contract every child reads; the probes are the ones that
produced findings rather than opinions; the schema is what makes the results aggregable.

---

## The brief (fill the angle brackets, pass the PATH to every child)

```markdown
# BRIEF — <target class> audit

## The target class
<One sentence: "X that <does the harmful thing>". Name it so a child can recognise an instance
nobody listed.>
<CODENAME> — it looks like a control, reads like a control, and blocks nothing it claims to block.

## Verdict codes — exactly one per finding
GHOST            nothing invokes it
DECORATION       cannot fail (no nonzero path, no refusing branch)
ADVISORY-AS-LAW  binding prose with no mechanism behind it
OVER-BROAD       trigger wider than its authority basis, or a hold with no lane
DEAD-BODY        names a path/flag/ledger/tool that cannot execute
REAL GATE        counter-class: independent trigger + failing exit + named authority — REPORT THESE TOO

## Before classifying, answer in writing
1. What invokes it? (exact path, or none-found + the search command + the roots covered)
2. Who issued the authority? (principal / named floor / kernel module / nobody)
Missing answer = the finding. Say which one is missing.

## Two honesty rules
- A negative needs the same warrant as a positive: the command and its scope travel with the claim.
- Read every hit in its enclosing scope: docstring mention, dated report, NEGATED line, hash-manifest
  entry and template placeholder are NOT invocations and NOT write targets. Quote the enclosing line.

## Non-negotiables
READ-ONLY. Write nothing except your own JSON. No deletion proposals — classify, and name the one-line
mechanical fix where one exists. Removal belongs to the principal. UNKNOWN is an acceptable result;
a guess is not. Report transitions, not Booleans.

## Output
Write to <workspace>/<task-name>.json AND return the same JSON.
{ status, task_name, scope_searched[], counts{}, findings[], evidence[], top3_by_cost[], recommendation }

## Environment facts a child cannot see
<host, role, doctrine, live services/ports, source-of-truth paths, and any claim from an earlier
session that must be RE-VERIFIED rather than inherited>
```

---

## Probes that produced findings

### Does it execute at all?
```bash
python3 -m py_compile <file>          # SyntaxError => every prior invocation failed
grep -c 'sys.exit\|SystemExit' <file> # 0 => its exit status carries no verdict
<file> --help 2>&1 | head
```

### Who invokes it? (report the roots you covered)
```bash
crontab -l; ls /etc/cron.d/; grep -n '<name>' /etc/crontab
systemctl list-timers --all; grep -rln '<name>' /etc/systemd/system/
grep -rn '<name>' /root/*/.git/hooks/ ; git -C <repo> config core.hooksPath
grep -rln '<name>' /root/*/.github/workflows/ ; grep -n '<name>' <scheduler>.json
```
Then classify every hit: self / own test / companion docstring / dated report / hash-manifest /
negated line / genuine call site. Only the last is an invocation.

### Can the claimed effect reach the caller?
Read the allowlist or exemption against the schema the caller actually sends. Look for the field names
in the tool schema before believing an exemption can fire.

### Schedulers and units
```bash
systemctl is-enabled <unit>; systemctl is-active <unit>
grep -n 'SuccessExitStatus\|ExecStart' /etc/systemd/system/<unit>
ls -la $(systemctl show <unit> -p ExecStart --value | grep -oP 'path=\K[^ ;]+')   # does the path exist?
```

### Markers that assert freshness
```bash
stat -c '%y %n' <artifact> <script>     # artifact older than its producer = stale
# find the line that recomputes the field; if none, the "refreshed" field is a claim with no witness
```

---

## Findings schema (aggregate with jq, not by eye)

```json
{
  "status": "DONE|BLOCKED|ERROR",
  "task_name": "<surface>-audit",
  "scope_searched": ["path or command per surface"],
  "counts": {"GHOST": 0, "DECORATION": 0, "ADVISORY-AS-LAW": 0, "OVER-BROAD": 0, "DEAD-BODY": 0, "REAL": 0},
  "findings": [{
    "name": "dotted.name",
    "location": "/abs/path:LINE",
    "verdict": "<one code>",
    "claims": "what it says it does",
    "actually_does": "what was measured",
    "invoked_by": "path, or none-found + the search command",
    "authority_basis": "principal | floor | kernel | none",
    "cost_to_agent": "concrete blocked action, or NO_MEASURED_COST",
    "evidence": "command + observed output, or file:line",
    "mechanical_fix": "one line, or NONE"
  }],
  "evidence": ["every command that produced a claim"],
  "top3_by_cost": ["names"],
  "recommendation": "2 sentences maximum"
}
```

Aggregate:
```bash
jq -s '[.[].findings[]] | group_by(.verdict) | map({v:.[0].verdict, n:length})' <workspace>/*.json
```

---

## Reporting to the principal

Lead with the population, not the worst example: `N findings — X theatre, Y real gates`. Then the
top-by-cost, then what stayed up (the real gates are the reason the estate is usable at all).
Every figure re-derivable from a command you printed. End with the binaries only the principal can
decide — deletion, adoption, or wiring — and finish the reversible ones yourself.

When a control under audit refuses your own review, that refusal is a finding: quote the payload that
triggered it and the exempt verb that got you through. Do not route around it silently, and do not
report the workaround as the repair.
