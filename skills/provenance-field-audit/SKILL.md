---
name: provenance-field-audit
description: "Use when auditing provenance fields in an artifact."
version: 1.0.0
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Provenance Field Audit

Artifacts increasingly ship their own provenance: a DOI, a `sha256`, a runtime witness, a test count, a "verified" badge. Each of these is an **identifier**, and a generated identifier has the right shape and the wrong referent. Shape checks pass them; only a probe against the registry or the host catches them.

The failure mode is asymmetric. A visibly incomplete artifact invites scrutiny. An artifact that *looks* audited — every field populated, CI green — passes review and carries the error into a decision. **Rendered completeness is the disguise, not the evidence.**

## Procedure

1. **Inventory the provenance fields**, not the prose. List every DOI, hash, PID, OS string, git SHA, version literal, test count, and `±` value. Those are the load-bearing claims; the narrative around them is not.
2. **Classify each field** before probing: checkable against a registry (DOI, package version), against the filesystem (hash, path), against the host (OS, arch, PID, uptime), or against a command (test count, service state)?
3. **Probe each against its own authority.** Registry for DOIs, `sha256sum` for digests, `uname`/`ps` for witnesses, re-running the suite for test counts. Never accept one field on the strength of another field in the same record.
4. **Diff, do not spot-check.** For a DOI compare title, first-author surname, journal, volume, page range, year. For a witness compare kernel, arch, interpreter, PID start time. One mismatch = wrong entity, stop.
5. **Reproduce or retract.** If a hash cannot be reproduced, set it to `null` with an explicit `UNKNOWN` state — never invent a replacement. If a test count cannot be re-run, report the blocker, not the number.
6. **Report per field**: claimed → measured → verdict (HOLDS / WRONG-ENTITY / FABRICATED / UNVERIFIABLE). Name which failure class each one belongs to.

## The four provenance failure classes

| Class | Tell | What it means |
|---|---|---|
| **Wrong entity** | Identifier resolves, but metadata is a different subject entirely | Most dangerous: the link is healthy, so nothing signals the error. Only field comparison catches it. |
| **Fabricated digest** | A repeating unit inside the hex string | Typed, not computed. Test every divisor of the length; also slide a window over the tail, since a real prefix plus a tiled suffix evades the divisor test. |
| **Foreign witness** | Claimed OS/arch/PID belongs to another machine or another service | Provenance from a machine that is not the machine. Worse than absent provenance — it is checkable and fails in front of the reviewer it was meant to convince. |
| **Regression lock** | Green tests that assert outputs of inputs the author typed | Proves the gate runs, not that the tier assignment is honest. |

## Commands

```bash
# DOI → exact metadata; diff every field against the claim
curl -s -H 'User-Agent: verify/1.0 (mailto:you@example.com)' \
  "https://api.crossref.org/works/10.XXXX/YYYY" \
| python3 -c "import sys,json; d=json.load(sys.stdin)['message']; \
print('title  :',(d.get('title') or ['?'])[0]); \
print('author :',', '.join(a.get('family','') for a in (d.get('author') or [])[:4])); \
print('journal:',(d.get('container-title') or ['?'])[0]); \
print('vol/pg :',d.get('volume'),d.get('page')); \
print('year   :',(d.get('issued',{}).get('date-parts') or [[None]])[0][0])"

# Does the claimed paper exist at all? Search by author+title, twice, different phrasings.
curl -s -H 'User-Agent: verify/1.0 (mailto:you@example.com)' \
  "https://api.crossref.org/works?query.bibliographic=AUTHOR+TITLE+WORDS&rows=5&select=title,DOI,container-title,issued,page,author"

# Host identity — what a witness block must match
uname -srm
python3 -c 'import sys;print(sys.version)'
ps -o lstart=,cmd= -p <pid>
sha256sum <pre-image>        # patch gate: pre-image must equal live byte for byte
```

Fabricated-digest detector:

```python
def tiling(s):
    """Return (unit_len, unit) if s is a short unit tiled to length — typed, not hashed."""
    for n in range(2, len(s) // 2 + 1):
        if len(s) % n == 0 and s[:n] * (len(s) // n) == s:
            return n, s[:n]
    return None
```

OpenAlex carries abstracts as an inverted index when Crossref does not; rebuild by sorting `(position, word)` pairs. An abstract is `ABS`-tier evidence — it confirms what a paper claims to do, never that its numbers survive scrutiny.

## Epistemic tier is set by production method

A number's tier is fixed before anyone sees it. A smoothed, non-unique inversion of an indirect field is **DERIVED** no matter how many decimals or `±` symbols it carries. A single station measurement is **MEASURED** for the quantity it measured — and only that quantity.

Two corollaries that catch most real defects:

- **A value labelled `MEASURED` whose method field says `inversion`, `model`, `interpolated`, or `assumed` is an evidence-class error.** The method field and the tier field sit in the same record; when they disagree, the method wins.
- **A `±` with no source is manufactured precision.** Ask what produced it: a published range compressed to a point estimate, a filter parameter reused as an error bar, a hand-typed constant. All three are inventions wearing the shape of rigour. An interval derived from a published range must span that range — not a narrower number chosen because it makes a test resolve.

## Pitfalls

- **Verify the negative direction too.** A search returning nothing for an author-plus-topic combination is evidence the citation is invented. Run the direct lookup and the bibliographic search; disagreement between them is the finding.
- **A verdict that flips on a hand-drawn threshold is a tautology.** If a model passes because its prediction window was written to contain the observation, the correct label is `INDETERMINATE` with the missing measurement named — not `PASS` for one and `KILLED` for its rival. The absence of a measurement capable of breaking the tie is itself the result.
- **Beware the root/depth conflation in isostasy-style checks.** An Airy root is the thickness *added beneath the reference horizon*, not the depth of that horizon. Compare like with like before calling a mismatch.
- **A broken venv makes a test claim unverifiable, not false.** Find the interpreter the service actually runs under (`ps -o cmd= -p <service pid>`) and re-run there before accepting or rejecting.
- **One clean field does not clean the record.** Different surfaces of the same artifact drift independently — a rendered page can be corrected while the downloadable JSON still carries the retracted value. Check each served surface separately.
- **Do not launder an invented value into a corrected one.** Setting a fabricated hash to a fresh plausible digest preserves the lie in a new shape. `null` plus an explicit missing-state is the honest edit.

## Companion skills

- `identity-reference-verification` — identifier classes and the release ladder.
- `evidence-hierarchy` — MEASURED vs DERIVED ordering when sources contradict.
- `ground-relayed-agent-claims` — claim-by-claim grounding of another agent's report.

This skill covers the layer those three assume: the provenance fields *inside* a single artifact record, and whether each one was measured or manufactured.
