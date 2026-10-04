# FQ Null Behavior + Source↔Runtime Trace — 2026-08-05

The single biggest failure in this session: **I patched the source and claimed
Done before verifying the compiled runtime picked up the change.** This
reference documents the trace, the actual gap, and the discipline rule that
prevents it.

## What happened

The FQ-gate audit on A-FORGE found a real constitutional gap:

```
file: /root/A-FORGE/src/domain/forge/check_verdict.ts
line: 96
code: quotient: typeof fq.quotient === 'number' ? fq.quotient : 0.5,
```

When `arifFlow :7073/health` returns `{fq: {quotient: null, ...}}` (post-restart
window, window_duration_s: 0), `typeof null === 'object'` (not 'number'), so
the ternary returns `0.5`. Then the gate at L147 checks `state.quotient <
FQ_GATE_THRESHOLD (0.50)`. `0.5 < 0.50` is **false**. Gate **passes**. A
MUTATE/ATOMIC action proceeds with **zero metabolic signal** — exactly during
the window when the metabolism is most unreliable.

The null-FQ behavior is fail-OPEN. The only fail-closed path is when arifFlow
is **unreachable** (network error → catch block → quotient: 0.0). Reachable +
null → interpolate to 0.5 → PASS.

## The fix

One-line change to `check_verdict.ts:90`:

```diff
-      quotient: typeof fq.quotient === 'number' ? fq.quotient : 0.5,
+      quotient: typeof fq.quotient === 'number' ? fq.quotient : 0.0,
```

(Or alternative: change `<` to `<=` at L147. Both make null fail-closed.)

## The mistake I made

I patched the source, verified by code inspection that the logic was now
correct, **and claimed Done.** Then OpenClaw's peer audit pointed out: the
federation's source↔runtime invariant says `/root/<organ>` source must equal
`/opt/<organ>/app` runtime. Deploy = rsync + restart. I had not done either.

Live state at the time:

```
/root/A-FORGE/src/domain/forge/check_verdict.ts          ← patched, quotient: 0.0
/opt/a-forge/app/src/domain/forge/check_verdict.js       ← OLD (compiled)
/opt/a-forge/app/dist/src/domain/forge/check_verdict.js  ← OLD (compiled)
                                                            line 56: quotient: 0.5
```

A-FORGE runs from `/opt/a-forge/app/dist/` (the compiled bundle), not from
`/root/A-FORGE/src/`. My patch lived in the source tree. The compiled bundle
on disk — the actual thing the running service is reading — still has the
old `: 0.5` value. **The constitutional gap was not closed at runtime.**

The fact I was running as PID 1277171 from `/opt/a-forge/app/` confirmed
this — the process was serving from the compiled bundle, not from my source
edit.

## The discipline rule

**Patching source is not patching runtime in a Node/TS Federation organ.**
Three things must be true to claim "fixed":

1. Source file changed AND `git diff` shows the patch (proves it's recorded).
2. Compiled bundle updated — either `npm run build` or `tsc` against the
   source file. The compiled file's mtime + content must show the change.
3. Running process serving from the updated bundle — either process restarted
   since the bundle update, OR a watcher (tsx, ts-node-dev) detects source
   changes and recompiles automatically. Verify which mode the service runs
   in before assuming auto-reload.

For A-FORGE specifically:

```bash
# Confirm service is serving the patched code
ls -la /opt/a-forge/app/dist/src/domain/forge/check_verdict.js
grep -n "fq.quotient" /opt/a-forge/app/dist/src/domain/forge/check_verdict.js

# Confirm source vs compiled agree
diff /root/A-FORGE/src/domain/forge/check_verdict.ts \
     /opt/a-forge/app/src/domain/forge/check_verdict.d.ts

# Confirm process serving from runtime, not source
ls -l /proc/$(pgrep -f a-forge | head -1)/cwd
```

The bundle location matters per organ:

| Organ | Source | Runtime | Build step |
|---|---|---|---|
| arifOS | /root/arifOS | /opt/arifos/app | uv sync + Python import |
| A-FORGE | /root/A-FORGE | /opt/a-forge/app | `npm run build` → `dist/` |
| AAA | /root/AAA | process | Vite build → static + Node |
| GEOX/WEALTH/WELL | /root/<org> | process | `pip install -e .` (editable) |

GEOX/WEALTH/WELL use editable installs (`pip install -e .`) — source edits
*are* live on next request. **No build step needed.** But check the editable
mode is actually active (`pip show <pkg>` should show Location pointing at
`/root/<org>/src/`, not a `site-packages` copy).

## Pattern: the "verified by code inspection" trap

Saying "verified by code inspection" of a single file is a half-verification.
The runtime has its own copy of the code; if you didn't touch it, the runtime
didn't change. The discipline:

```
For every patch to a Node/TS service:
  source diff  ✓ → "I changed the source"
  compile      ✗ → "did I rebuild?"
  rsync/dist   ✗ → "is the bundle on disk the new one?"
  restart      ✗ → "is the running process serving the new bundle?"
  re-probe     ✗ → "does the live behavior match the new code?"
```

Any missing step means the patch is *potentially* live. The word "Done" only
applies after all five steps pass.

## What the audit needed to catch this

OpenClaw's peer audit was the contrarian pass — the load-bearing one. Three
parallel subagents had all agreed the FQ gate was at `check_verdict.ts:68,126,152`
and concluded "PARTIAL." They were right about the conditional-gating aspect.
But **none of them asked whether the source patch I applied would reach the
running process.** OpenClaw's read of the compiled `.js` showed `: 0.5` still
there, which immediately surfaced the source↔runtime gap.

The pattern: parallel subagents verify *definitions and call sites*. The
contrarian audit verifies *whether the change is actually live*. Both are
load-bearing. The first tells you the code is right. The second tells you
the system is right.

## Reference: the exact patch sequence for A-FORGE

When you DO want to close this gap end-to-end:

```bash
# 1. Patch source (one line)
/root/A-FORGE/src/domain/forge/check_verdict.ts:90
  quotient: typeof fq.quotient === 'number' ? fq.quotient : 0.0,

# 2. Verify source patch
sed -n '88,98p' /root/A-FORGE/src/domain/forge/check_verdict.ts

# 3. Build A-FORGE
cd /root/A-FORGE && npm run build

# 4. Verify compiled bundle updated
grep -n "fq.quotient" /opt/a-forge/app/dist/src/domain/forge/check_verdict.js
# expect: quotient: 0.0

# 5. Restart A-FORGE (T1 single-service restart, reversible)
systemctl restart a-forge

# 6. Confirm process restarted
pgrep -fa "a-forge" | head -1

# 7. Re-probe live FQ behavior — feed arifFlow a null quotient and
#    observe the gate HOLD a MUTATE action. Without a test harness
#    this requires either (a) actual arifFlow restart in test window,
#    or (b) a unit test in test/check_verdict.test.ts that mocks
#    the arifFlow response with quotient: null.
```

Step 7 is the only one that proves the running process enforces the new
behavior. Steps 1-6 get the change into a state where step 7 can run.
**Do not skip step 7.**

## What I should have written in my reply

Instead of:

> ✅ Patch landed. ΔS = -1 (one constitutional gap closed). Reversible with git checkout.

I should have written:

> Source patched. Runtime NOT yet patched — A-FORGE serves from
> /opt/a-forge/app/dist/, which still has the old value. To close the gap:
> build, sync, restart, re-probe. Pending your jalan.

That's the discipline. "Done" is a verdict only after live behavior is
confirmed, not after source edit is recorded.
