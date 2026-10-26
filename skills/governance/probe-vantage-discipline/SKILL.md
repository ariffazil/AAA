---
name: probe-vantage-discipline
description: "Use when two probes of runtime state disagree."
---

# Probe Vantage Discipline

Two observers can both be honest and still disagree: they measured different **vantages** of
the same system. Before weighing either claim, pin four axes on both sides — host, **path**,
window, identity. Most "contradictions" resolve on one of these, and the ones that survive are
the real defects.

## Always-on rules

- Every claim and every denial carries `host + path + window`.
- Resolve the reader's path **in code**, never from prose, a README, or a peer's description.
- A count without its window is not a measurement. Print the window beside every number.
- A timestamp without a proven timezone is not a timestamp.
- A shared credential is identified by hash prefix, never by balance or spend.
- A field named `idempotency_key` is a claim, not an enforcement — count distinct keys.

## Step 1 — Producer path ≠ consumer path

The commonest false defect: two files with the same **name** and the same **schema**, at two
paths. The producer writes one (its cwd), the consumer reads the other (a profile dir). Editing
the producer's copy never reaches the consumer.

Tell: a **subset** of targets/entries resolves and the rest are refused. If the config were
genuinely wrong, nothing would pass; a partial pass means two directories.

```bash
grep -n "_ROOT\|_DIR\|profile" <module>.py      # what the reader actually joins
cat <profile-selector-file>                      # which root is active
stat -c '%y %s' <writer-file> <reader-file>      # frozen mtime on the reader = proof
```

Then call the consumer's own resolver instead of predicting it — one call answers every entry:

```bash
python3 -c "
import sys; sys.path.insert(0,'<package-root>')
from <module> import <resolver>
for x in ['<case1>','<case2>']: print(x, <resolver>(x))"
```

Fix is **one directory** (symlink, or point the consumer at the canonical path). Adding entries
to the wrong file fixes nothing — the same single-writer defect as a duplicated store, one layer
down. Concrete instance: Hermes `delivery_guard` reads
`/usr/local/lib/hermes-agent/profiles/<active_profile>/channel_directory.json` while the gateway
writes `/root/.hermes/channel_directory.json`; the profile copy froze weeks earlier and returns
`DELIVERY_TARGET_BLOCKED … is not a known human/group` for ids that exist in the live file.

**Read the reason string before calling a block a fault.** One refusal class is the guard
*working* (a bot id, an unknown destination) and a different one is the guard reading a stale
file. Same error text family, opposite fixes.

## Step 2 — Record count vs distinct idempotency keys

An append-only event bus with an `idempotency_key` field may enforce nothing: the writer emits
the key and never compares it. Then every re-fire of one condition lands as a fresh row.

```bash
python3 - <<'EOF'
import json, collections
c = collections.Counter()
for line in open('<events.jsonl>'):
    try: c[json.loads(line).get('idempotency_key')] += 1
    except Exception: pass
print('records:', sum(c.values()), 'distinct keys:', len(c))
print(c.most_common(3))
EOF
```

A ratio in the thousands means the stream is **one condition repeated**, not thousands of
findings. Before reporting "N breaches", group by key **and** inspect the `state` transitions:
if there is no `ACK`/`RESOLVED` row, the condition never closed — it is one open item regardless
of how many rows carry it. A file growing to tens of megabytes for a handful of keys is a
dedupe contract declared but not enforced.

## Step 3 — Window pinning

"Zero in all windows" is true only if the widest window was queried. A ten-minute burst that
ended twenty minutes ago reads `0` at 15m/1h/2h and `44` at 6h — same command, four answers, and
both sides can be honest while disagreeing.

```bash
for w in 15m 1h 2h 6h 24h; do printf '%s ' $w; <logs> --since $w | grep -c '<text>'; done
<logs> --timestamps --since 24h | grep '<text>' | awk '{print $1}' | cut -c1-13 | sort | uniq -c
```

- Print windows **and** hit timestamps. A clustered distribution = episodic; a flat one =
  continuous. Different fixes, different urgency.
- **Episodic ≠ absent.** A burst that repeats hours later means the trigger is still live. A
  rejection that costs nothing today (empty balance, exhausted quota) becomes a **paid burn** the
  moment the resource is restored — so the free mitigation goes before the spend, and "it
  stopped" is a different finding from "it is fixed".

## Step 4 — A log string is host-specific

Container log vocabulary differs per build and per seat. A phrase yielding hundreds of hits on
one box can be exactly `0` on another because that model group, rung, or module is dormant or
absent there. Never transfer a grep count across hosts; re-grep on the host you are about to
make the claim about, and name the host in the number. Test two or three string variants before
concluding zero — the same event is often logged under a different sentence on a different build.

## Step 5 — Timezone before staleness

A receipt is not "eight hours old" until both clocks are reconciled. A peer that labels local
time as UTC will manufacture a staleness verdict that does not exist. Print `date -u`, the local
`TZ` equivalent, and the receipt's own offset side by side before accepting any age claim — the
clock is the cheapest thing to falsify and the most persuasive when wrong.

## Step 6 — Shared credential identity

Two seats reading different balances, quotas, or spend are usually **one resource at two read
times**, not two of it. Compare a `sha256` prefix of the key — never the value, never the
balance:

```bash
docker exec <container> sh -c 'printf "%s" "$KEY" | sha256sum' | cut -c1-16
```

Matching prefixes = one wallet; the numbers differ because the reads were minutes apart. Only
after a hash mismatch is "two accounts" a supportable claim.

## Reporting shape

- Lead with what is verified and the command that verified it.
- Mark `UNKNOWN` explicitly; never let an unread measurement render as zero.
- Name the host, the path you read, and the window, inside the claim.
- Correct your own error in place, in the same message, naming the misread — do not append a
  hedge under a retracted line.
- If the disagreement resolves to two vantages, say so plainly: nobody lied, and the contradiction
  itself is the finding.

## Pitfalls

- **Quoting a peer's number back as your own verification.** Re-running the same grep on the same
  host reproduces the string, not the reality. A second vantage means a different path, window,
  host, or resolver — otherwise it is one witness with two mouths.
- **Assuming a health endpoint and a config file measure the same thing.** One can be `null` while
  the other reports a value; that is two surfaces, not a contradiction, until you establish that a
  consumer reads both.
- **Treating a restart as settling a defect.** Count errors *after* the restart for a full cycle;
  a drop inside the same boot window is a queue drain.

*DITEMPA BUKAN DIBERI*
