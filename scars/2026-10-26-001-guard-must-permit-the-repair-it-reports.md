# SCAR-2026-10-26-001 — A guard that denies the report of its own bypass denies the repair

**Class:** guard design failure — false positive introduced *by* a security fix
**Weight:** w_scar = 0.8
**Filed:** 2026-10-26 · Claude Code FI-002 · self-filed under F1 AMANAH
**Evidence:** `/root/AAA/state/reports/2026-10-26-claude-fi002-path-escape-fix.md` (commit `50e406d3`)
**Related:** SCAR-AGY-002 (regex guard too broad → read-only false positives) ·
`/root/AAA/instructions/temporal-derivation-law.md`

## What happened

I measured 24 bypasses in my own PreToolUse guard (`f1-amanah-preshell.py`) and fixed them (v3).
The fix worked: all 24 closed. Then I ran into the guard myself.

`git commit -m` whose message *documented* the bypass — the message contained the text
`echo x > /root/.claude/settings.json` and the path `/root/arifOS/VAULT999` — was denied:

```
PreToolUse:Bash hook error: F1 AMANAH (T3/W_scar):
Bash redirection into protected path: /root/.claude/settings.json
```

The `>` was inside a quoted commit message. It was data describing an attack, not a redirect.

## Why this class is worse than a plain false positive

A guard that denies a read (`find`, `tail`) wastes a turn — SCAR-AGY-002's class, already encoded.
This one is different:

**Patching a bypass requires a commit that names the bypass.** So the guard denied the only
action that could repair the thing it was reporting. The failure is self-sealing: the tighter I
made the screen, the harder it became to write down why. That is not friction, it is a lockout —
and it would have hit the next agent harder than me, because they would not know the deny was
self-inflicted.

## The law

**A guard must be tested against the work it exists to permit, not only against the attacks it
exists to block.** A deny-list suite proves the guard fires; it says nothing about whether the
guard still lets the job through. Every guard change needs both directions in one suite:

- DENY cases — the attack surface (must block)
- ALLOW cases — *real daily work*, including the work of reporting and repairing the attack
  (must not block)

Mine: 32 ALLOW cases alongside 35 DENY cases, in
`/root/AAA/scripts/f1-hook-escape-suite.py`. The ALLOW cases caught this defect and also caught
my own first draft, which blocked `cat /protected > /tmp/x` and
`python3 -c "json.load(open('/protected'))"` — both legitimate audit reads.

**Corollary — quote-awareness is asymmetric.** The fix is not "strip quotes everywhere":

| Element | Read from | Why |
|---|---|---|
| Operator (`>`, `>>`, `2>`) | quote-stripped text | a `>` inside a string is data, not syntax |
| Path token | **original** text, quoted included | a quoted path is still the file that gets written |

Stripping quotes from both opens a new bypass: `sed -i 's/a/b/' '/root/.claude/mcp.json'`.
Stripping from neither keeps the lockout. One input needs two different treatments depending on
its syntactic role. Both directions are tested (`ok29`–`ok32` ALLOW, `q1`–`q4` DENY).

## Residual, stated not hidden

String screening cannot close indirection — shell variables, base64+`eval`, runtime-built paths.
No regex can. The durable fix for that class is OS-level: the guard owned by a different principal
than the worker. That is a sovereign decision, not an engineer's patch.

## One-line version

Before tightening a guard, run the work it permits through it — especially the work of writing
down what it just caught.
