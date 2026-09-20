# Sealing a control, and verifying a claimed result

Depth for the two parts of SKILL.md. Use when hardening a gate, hook, validator, watchdog or config
that other actors can also write to — or when deciding whether a report of completed work is true.

## 1 · Does the claimed result exist?

Before accepting any report about your own system's state:

```bash
# the artefact named in the report — does it resolve?
stat -c '%y  %s bytes  %n' <claimed-path>

# does the name appear ONLY in the session database? then it is chat text, not a deliverable
grep -rl "<claimed-artefact-name>" /root/AAA /root/.hermes 2>/dev/null
```

A hit confined to `state.db` / `state.db-wal` means the thing was discussed, not written. Report the
absence as the finding, then write the artefact.

## 2 · Harness shape (black box)

```python
CASES = [
    # (name, payload, expected_exit, why)
    ("A1 path carries a trigger word",  {...}, 0, "a path is not a claim"),
    ("A2 read-only chained pipeline",   {...}, 0, "every segment must be a probe"),
    ("B1 claim, no evidence pointer",   {...}, 2, "the defect being fixed"),
    ("C1 claim WITH resolvable source", {...}, 0, "NEGATIVE CONTROL — must allow"),
]

def run(subject, payload):
    p = subprocess.run([sys.executable, GATE], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=30)
    return p.returncode, p.stdout.strip()
```

Group the cases by what they prove: former false positives that must now allow, former false
negatives that must now block, then the negative control. Print `N/M passed` and exit non-zero on any
failure so the suite is usable from a scheduled job.

For unresolvable-citation cases use a reserved `.invalid` host (RFC 2606) so the case can never
accidentally become real.

## 3 · Manifest shape

```json
{
  "_meaning": "These hashes record the exact bytes of the control as SEALED.",
  "_limit":  "Detects DRIFT, not an adversary. Anyone who reads this and recomputes it passes.",
  "artifacts": [
    {"role": "enforcement-gate", "path": "<abs path>", "sha256": "<measured>",
     "size": 0, "mtime": "<iso8601>"},
    {"role": "conformance-suite", "path": "<abs path>", "sha256": "<measured>",
     "size": 0, "mtime": "<iso8601>", "expected_result": "11/11, 7/7"}
  ]
}
```

- Hash the **control and its test** together. A sealed gate with unsealed tests can be "verified"
  against tests that no longer exist.
- Put `_limit` in the file. Self-describing limits survive; limits held in memory do not.
- Never hand-write a hash. Measure, then paste.

## 4 · Verifier pattern (watchdog)

Silent on match; output only on drift, or on inability to witness.

```python
try:
    manifest = json.load(open(MANIFEST))
except (OSError, json.JSONDecodeError) as exc:
    print(f"cannot read manifest: {exc}")
    print("Cannot witness is NOT all-clear.")     # VOID GUARD
    return 1

for art in manifest["artifacts"]:
    if not os.path.exists(art["path"]):
        missing.append(art["role"]); continue
    got = sha256(art["path"])
    if got != art["sha256"]:
        drift.append((art["role"], art["sha256"], got))

if not drift and not missing:
    return 0            # silent all-clear — print NOTHING
# on drift, print BOTH the sealed and the current hash
```

The **VOID GUARD** matters more than the drift check: a verifier that cannot read its own manifest
must not exit clean, or a deleted manifest reads as a healthy control.

Run it unattended as a script-only job whose empty stdout means no delivery — absence of output is
the all-clear. Pair it with a low-frequency **unconditional heartbeat**, so a dead verifier cannot
impersonate a quiet one. A monitor that fails silently is worse than no monitor, because operators
read "no alert" as "all clear".

## 5 · Negative control — prove the verifier can fail

An alarm that has never sounded is untested. Run all three steps before calling the seal done:

1. **Clean** — verifier exits 0, no output.
2. **Inject drift** — append a single byte to one sealed artefact. Verifier must exit non-zero and
   print both the sealed and the current hash.
3. **Restore exactly** — truncate back to the sealed byte size, re-run, confirm exit 0 *and* confirm
   the hash matches the manifest again. Restore by size or from committed content; editing back by
   hand does not reproduce the bytes.

If step 2 does not fire, the seal is decoration. Fix the verifier before sealing anything else.

## 6 · Operating a control you share with another writer

- **mtime is the evidence you have.** `stat -c '%y %s %n'` on the control, its state and its tests
  tells you whether you are the only writer and whether the two of you are racing.
- **Check for a write-side race before repairing.** Cleaning a shared artefact while another writer
  is active loses work. Detect the race, report it, let the owner decide about freezing.
- **A second writer moving in the same direction is not a threat.** If their changes are additive and
  compatible, say so plainly and move on.
- **Freezing is a decision with a cost,** not a strict improvement — see the SKILL.md pitfall.

## 7 · Recursion guard

When the control you are testing starts refusing your own test payloads, that is the control working.
Fix the payload — attach a resolving URL, a receipt id, or an on-disk evidence path — rather than
shopping for an unguarded tool to run the same write. A bypass found to escape your own gate is the
finding, not the workaround.

## 8 · Report shape

Separate three things explicitly, because a graded report is the deliverable:

- **verified** — what was checked and how;
- **unverified** — claimed but no artefact, with what you did about it;
- **limits** — what the control does not cover (pointer existence vs support; payload vs prose;
  drift-visibility vs tamper-proofing).

A report that only lists successes is the thing this skill exists to prevent.
