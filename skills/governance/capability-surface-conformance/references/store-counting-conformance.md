# Counting & Classification Conformance

How to produce a defensible count of any governed store (skills, tools, registries) — and why most
published counts are instruments answering the *adjacent* question. This is the measurement-side
companion to the false-affordance rules in SKILL.md.

## The law

> A count is a claim about a **scan configuration**, not about the world.
> Depth, symlink policy and the exact command go beside every number, or it is not a measurement.

Two audits of one store on the same day disagreed **14×** on "empty" — both instruments were internally
correct, they were answering different questions. The instrument was the finding, not the tree.

## 1. Classify before calling anything empty

A governed store mixes two directory kinds at the same level, nested many deep:

| Shape | Test | Verdict |
|---|---|---|
| SKILL / ENTRY | owns its manifest file (`SKILL.md`, `agent-card.json`, `*.sot.yaml`) | an entry |
| NAMESPACE | no own manifest, **≥1 entry nested below** | a category — **not a defect** |
| SHELL | no own manifest, no nested entry | a real defect |
|
"This directory has no manifest" is **not** a defect condition — it is the normal shape of a category.
An audit that reports it as an empty shell converts most of a healthy store into noise and buries the
handful of real shells.

Measured shape of the failure: 59 depth-1 dirs with no manifest → **54 namespaces** holding hundreds of
nested entries, **5** actually empty. The published claim was "70 empty shells"; the truth was 5.

Re-derive the count from the classification. Never from the raw depth-1 list.

## 2. Follow symlinks, dedupe by realpath

Every harness "view" in a multi-agent federation is a symlink or a symlinked tree. A walk that does not
follow links reports a container whose children are links as **empty**, and counts one entry once per
view.

```python
import os

def entries(root):
    """Every entry under root, symlinks followed, deduped by realpath."""
    seen = {}
    for dp, dn, fn in os.walk(root, followlinks=True):
        if "SKILL.md" not in fn:
            continue
        rp = os.path.realpath(dp)
        if rp in seen:          # reachable again through a second view
            continue
        seen[rp] = os.path.relpath(dp, root)
    return seen
```

The measured error this prevents: one pass with `followlinks=False` reported 31 empty dirs; the correct
pass reported 12. The wrong number was the more alarming one — false defects are how an audit loses
credibility.

## 3. Never quote a depth

Any `-maxdepth N` is wrong somewhere in a real store — entries nest deeper than any hand-picked N, so a
bounded scan returns a short count that reads like a finding. Use an unbounded walk. If a bounded scan is
unavoidable, publish the bound as part of the number.

## 4. Liveness is not ownership

`broken_symlinks: 0` measures that every link resolves. It says nothing about whether the canonical root
**owns** the bodies it serves. Links pointing **outward** (catalog → harness / profile / archive tree)
mean a second writer can silently change what every reader loads, and no liveness counter can see it.

Report them as two metrics, never one:

| Metric | Question | Class |
|---|---|---|
| `broken_symlinks` | does the target exist? | a bug |
| `outward_symlinks` | who owns the target? | a governance defect |

A store can score clean on the first while being a two-writer store on the second.

## 5. A basename collision is a load failure

Loaders resolve entries by **name**. Two directories sharing a basename mean exactly one is reachable and
*which* one wins is undefined per harness. Check after every migration that leaves a compatibility
symlink behind — the new flat home and the old nested home will both answer to the same name.

```bash
find "$ROOT" -name SKILL.md | sed 's|/SKILL.md||' | xargs -I{} basename {} \
  | sort | uniq -c | sort -rn | awk '$1>1'   # any count >1 is a collision candidate
```

## 6. Reporting shape

Every published count carries four things:

```
value · the exact command that produced it · scan depth · symlink policy
```

Plus, when the store is represented in more than one place, the **question** the number answers — two
counters can sit adjacent, look interchangeable, be numerically similar, and answer unrelated questions.
Quoting one under the other's heading manufactures a defect; the same confusion in the other direction
hides one.

## Adjacent instance — identity of a rendered artefact

Same invariant, one layer over: an instrument can answer the adjacent question about an artefact's
identity. A file checksum answers "same bytes", which is **neither necessary nor sufficient** for "same
image": two renders from one seed were pixel-identical (`max diff 0`) while their `sha256sum` differed,
because container metadata differs per download. Decide image identity on **decoded pixels**
(`numpy` diff over the RGB arrays), never on a hash — otherwise a hash-based check reports
non-determinism that does not exist.

Generalise: **before quoting any instrument, ask what question its parameters actually answer.** Depth,
link policy, checksum scope, and sampling window are all part of the question.

## From count to repair — a dead name usually has a renamed successor

A count tells you how many declared names no longer resolve. It does not tell you whether they are
**lost** or merely **renamed**, and those need opposite responses. Classify before repairing.

Match by **token overlap**, not substring distance. A rename changes a name's shape while keeping its
subject: `geo-basin` → `basin-charge-screening`, `well-readiness` → `well-substrate-readiness`,
`geox-basin-engines` → `geox-basin-evaluation`. Substring-plus-length guards miss every one of these
because the strings share no long common prefix; splitting into semantic tokens and scoring the
fraction of the declared name's tokens found in the candidate locates them.

```python
import re

def tokens(s):
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(s))            # split camelCase
    return [p for p in re.split(r"[-_\s./]+", s.lower())
            if p and p not in ("the", "a", "of", "and", "for", "to", "in", "on", "skill", "lane")]

# score = |tokens(declared) ∩ tokens(candidate)| / |tokens(declared)|
# >= 0.5 is worth reporting; >= 0.8 is usually a certain rename.
```

Strip harness/role prefixes (`forge-`, `aaa-`, `asi-`, `apex-`, `dev-`, `ops-`, …) before matching.
They carry no semantic load — the same skill renames its prefix each time it moves home, so leaving
them in hides real matches and manufactures false ones.

**Candidates are REPORTED, never auto-applied.** A 0.5 match is a lead for a human or a mapping pass,
not an automatic alias. Applying one silently converts a visible dead name into an invisible wrong
route, which is strictly worse than the dead name.

Report the split, because it decides the work: how many dead names have a candidate on disk (a
mapping exercise) versus none (each is a capability that may have silently disappeared, needing a
restore-or-retire decision). Observed on one store: **58% had a candidate**, so most of a 195-name
backlog was mechanical and only the remainder needed judgement.
