# Capability absence audit — missing, unwired, or present?

An audit's most damaging output is a **false gap**. A gap reads as work to do, so it gets built — and
the build duplicates something that already existed while the real defect (unwired, unreached,
unnamed) survives untouched. Run this before writing "not implemented", "no capability owns this",
"spec only, no actuator", or any gap table.

## 0. The three verdicts — decide which one before proposing a remedy

| verdict | test | remedy | who owns it |
|---|---|---|---|
| **ABSENT** | source trees, registry/manifest, AND tests are all silent | build it | the builder |
| **BUILT_NEVER_WIRED** | the implementation exists and has **zero callers** | a wiring decision | owner of the enforcement path |
| **PRESENT** | it exists and something calls it | nothing — say where it is | — |

Collapsing `BUILT_NEVER_WIRED` into `ABSENT` produces duplicate implementations. Collapsing it into
`PRESENT` hides an unenforced control. Both are the same error: the caller count was never measured.

## 1. Falsify the instrument before you quote it

A measurement tool is a claim, not an observation. Two flag choices produce opposite, confident, and
both-wrong verdicts about one object:

- a **depth-bounded** directory walk cannot refute existence below its bound;
- walking **with** link-following merges two trees into one uninterpretable count;
- walking **without** it hides symlinked entries entirely — listed in the child-name set, never entered.

- Test the probe against an input whose answer you already know before trusting its number.
- State the root you searched and the boundedness/flag you used **in the claim**. An absence claim with
  no stated root is unfalsifiable.
- For any path claim, test the exact path for existence in EVERY candidate root, not in one of them.

## 2. Search order — every layer a consumer reads, prose LAST

```
1  source trees            where a mechanism actually runs
2  registry + manifest     what is registered and callable
3  tests                   an implementation with a test file is not a rumour
4  the index the consumer sees   the names + descriptions a loader or selector actually reads
5  prose docs              README / SKILL.md / reports — LAST, and never alone
```

The expensive error is stopping at layer 5. Prose describes intent; it is the layer most likely to be
stale and the least likely to be the mechanism. **The absence of a mention is not the absence of a
capability.** Equally, a hit at layer 5 is not presence: several competing implementations can be
described in prose while only one is registered.

## 3. Wiring census — for anything that claims to enforce

Do not search prose for this. Count four things per mechanism, and name the count:

| question | what to count |
|---|---|
| is it scheduled? | schedule entries that name it |
| is it a service? | service-manager unit definitions that name it |
| is it called at runtime? | imports of its module from the code that actually runs |
| has it ever run? | does the state file it writes exist? does its state directory hold evidence of use, or a single stale fixture? |

Three zeros plus an absent state file is `BUILT_NEVER_WIRED` — it has never tripped, not because
nothing needed stopping, but because nothing calls it. That is the finding, and it is the interesting
one. Restrict the runtime-import count to live code: build outputs, packaged distributions, generated
docs and caches all report callers that are not callers.

## 4. Check the index claim the consumer actually uses

Two opposite failures, and they need opposite reports:

- **Listed but unresolvable** — the catalogue names a capability that no longer opens. A broken
  pointer; report it, do not restate the catalogue.
- **Present but unlisted** — the body is on disk, fully formed, and no surface will open it. A
  resolution gap. Before concluding a capability does not exist, resolve it **by path** as well as by
  name; a body under a nested category path can be absent from the flat listing while sitting on disk,
  editable, loaded by nothing.

**Selection precision is part of the index.** A selector reads a small leading window of each
description (order of the first 57 characters). Verify the discriminating word sits inside it, and
watch for a bulk annotation pass that injected a metadata stamp **mid-description** instead of after
it — that pushes the discriminating word out of the window and makes two capabilities
indistinguishable at selection time. Detect it by locating the stamp's offset and testing whether the
preceding character is a sentence terminator; fix by moving the stamp, never by rewording the
description around it.

## 5. Reporting rules

- **Never quote a usage/firing metric without the unreachable count beside it.** A firing count measures
  *loads*. Bodies that cannot load are never counted, so "N% never fired" silently absorbs them and
  reads as a pruning licence. Reduce the denominator first, or the number justifies deleting
  capabilities that were only unreachable.
- **Never re-publish a load-bearing number you have not probed this session.** One unverified sentence
  ("the store is included by default") propagates into every decision built on it. When you find such a
  sentence, correct the document **in place** rather than appending a correcting report — a corrected
  finding is worth more than a defended one.
- **A store on the write path is not necessarily on the read path.** Probe the loader
  (`get_skills_dir()` / `get_external_skills_dirs()` / `get_skill_create_dir()`) before treating a
  configured directory as readable. See `address-vs-storage.md` §5.
- **Label the layer in the claim.** "not implemented in source" and "not mentioned in the docs" are
  different statements; publishing either as "missing" swaps the quantifier.
