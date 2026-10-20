---
name: evidence-artifact-forensics
description: "Use when a report carries DOIs, hashes, or witnesses."
version: 1.0.0
---

# Evidence artifact forensics

## When to use

A report presents itself as an **evidence artifact**: it carries citations, file digests, an execution
witness (os / pid / commit), and a verdict, and it asks to be treated as having verified something.
Run this before repeating, acting on, or publishing any of it.

It fires when the artifact is machine-checkable — you can resolve the DOI, fold the hash, run
`uname`, or call the engine yourself.

## The law

**A shape-valid carrier is not a verified referent.** Each carrier fails in its own way, and a defect
in one is invisible in the others. Check them separately and report them separately. A report can be
internally consistent end to end and still rest on something invented.

```
VERIFIED_CARRIER = resolves AND matches_the_claim AND generated_on_this_host
```

Resolving is necessary and never sufficient. A DOI that lands on a real, unrelated paper resolves.

## Procedure

1. **List the carriers.** Citations, digests, witness block, quantifier ("6/6 pass"), verdict.
2. **Resolve each citation** and diff title, journal, volume/pages, first author — plus the method
   named in the title when the claim is a method claim.
3. **Fold each digest** and count unique chunks; check the named algorithm is one you can run.
4. **Compare the witness** fields against the actual host and process.
5. **Test "live" by mutation**, not by HTTP status: change one input, see whether output moves.
6. **Score engine and record as two verdicts**, then deliver both in the same breath.
7. **Write what you could not check**, one line, naming the missing capability.

## Commands

**DOI** — diff five fields, not just resolution:

```
curl -s "https://api.crossref.org/works/<DOI>" | jq '.message |
  {title, container: .["container-title"], volume, page, authors: [.author[].family]}'
```

**Digest — typed or computed:**

```
echo "<hash>" | fold -w16 | sort -u | wc -l      # 1 == one chunk repeated == typed
```

A 64-char value whose tail is a short unit repeated is hand-authored. Use `b3sum` for a BLAKE3
claim; if the binary is absent the digest is `UNVERIFIED`, not verified-by-substitution.

**Witness — the host is the referent:**

```
uname -srm ; python3 -V ; ps -o pid=,lstart=,cmd= -p <pid>
```

An ARM / Raspberry Pi OS string on x86_64, or a PID owned by another service, means the witness was
written rather than generated. Then re-run the engine and diff its fresh witness against the
published one.

**"Live" — mutation test, non-destructive:**

```python
import copy
for v in (published, published + 8, published + 14):
    o = copy.deepcopy(obs); o["measurement"]["value"] = v
    print(v, Engine.run(evidence, o, copy.deepcopy(a), copy.deepcopy(b)))
```

Verdict flips → engine real. Verdict constant → panel is hand-written text.

**Abstract from OpenAlex** — stored as an inverted index, rebuild before reading:

```python
pos = [(i, w) for w, idxs in inv.items() for i in idxs]
abstract = " ".join(w for _, w in sorted(pos))
```

Read it for method and scope: authors often state there the limit that defeats the claim.

**Prior-art check** — search the claim's vocabulary, not the citation's; report database, keywords,
and hit count. No hit means "no hit for these keywords", never "unpublished".

## Standing rules

- **Resolve is not correct.** A DOI opening a real paper from the wrong field is a fabricated
  citation. Multiple mismatches on one identifier is not a typo; the referent does not exist.
- **A digest with internal repetition was typed.** One unique fold-chunk means no hash function ran.
- **A witness names a host.** Wrong architecture or a borrowed PID means it was not generated there.
- **HTTP 200 proves a file is served, not that an engine runs.** Only mutation distinguishes them.
- **A typed prediction window makes the verdict a tautology.** If the expected range is a literal in
  the runner rather than derived from physics, "model X killed" is a property of the input, not of
  the subject. Say which windows were typed.
- **A test asserting `A=PASS, B=FAIL` locks a constant.** It proves the number has not changed; it
  says nothing about whether the number is right. State which proposition the suite proves.
- **Class every bibliography entry.** Primary literature / preprint / vendor page / own artifact /
  chat log / search-result page are six evidence classes. Only the first carries a technical claim.
  Your own earlier write-up is evidence, never a source; a bibliography citing itself is a loop.
- **When the artifact's own documents contradict it, the older one usually wins.** A system that
  already recorded the correction upstream outranks a newer summary that skips it. Grep the corpus
  for the method or class name first — the correction is often already on disk.
- **Deliverable is a verdict, never a silent repair.** Name the defect, rank the cheapest real fix;
  applying it needs the owner's word, especially on a public surface.

## Pitfalls

- **Do not generalise one file's state to a sibling.** Two files under one heading can disagree: one
  cleaned, one still stale. Probe each by its own hash before reporting on the set.
- **Do not let a green suite end the audit.** Schema gates (required fields present) cannot catch a
  field that is present and false. Name completeness and provenance as separate gates.
- **Do not average two conflicting uncertainty figures.** If a published range and the artifact's
  plus/minus sigma disagree, the sigma was likely chosen to make a test pass. Show both and say which
  one has a source.
- **"Verifier missing on this host" is not "digest is fake".** Missing verifier is `UNVERIFIED`;
  missing referent is `FABRICATED`. Different verdicts, different follow-up.
- **Do not substitute metadata for content you could not read.** File size, mtime, codec, or EXIF is
  not the paper. Say what you could not open.

## Companion skills

- `identity-reference-verification` — emitting your own identifiers without fabricating them.
- `audit-ops` — routing a pasted report to the right verification branch.
