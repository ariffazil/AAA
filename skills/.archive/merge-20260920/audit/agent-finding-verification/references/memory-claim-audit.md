# Memory / identity claim audit — claims about a person, and the surfaces that carry them

Class of work: an artifact (external AI, peer agent, pasted report) makes claims about the
sovereign — identity, role, history, scars, preferences — or asserts those claims are now
"aligned", "sealed", or "binding". Verify the claims, then verify the alignment assertion.
Open with what is valid: a report that is 40% right must be credited for the 40% first, or the
correction reads as blanket rejection and gets discounted.

## 1. Classify the source before probing

| Source shape | What it can prove | First probe |
|---|---|---|
| External AI review of a person | Nothing by itself — check whether its evidence is our corpus | grep its evidence block's distinctive phrases across our dirs |
| Peer-agent audit of memory surfaces | What its probes saw, at its timestamps | re-derive every count from the array, not the summary block |
| Ledger/canon row asserting alignment | Only that a write happened | read the writer's declared mode, then re-run the reconciliation |
| A quoted line labelled "sealed"/"harmless" | Only that it was quoted | grep the archive for it before repeating |

## 2. Echo check — run this first on person-facing artifacts

An artifact about a person can be 100% sourced from that person's own surfaces and still present as
independent validation. Verbatim is the tell.

```bash
for s in "<phrase from its EVIDENCE block>" "<second phrase>"; do
  echo "== $s"; grep -rln "$s" /root/AAA /root/memory /root/.hermes 2>/dev/null | head -5
done
```

Verbatim hits in our own repos = mirror, not witness. Then ask whether the echoed string is
**obsolete** — an old floor rename, a superseded count, a legacy label still living in one
governance file. Our own stale drift re-entering as our own "stable fact" is the worst form of the
loop: it launders drift into doctrine, and the fix is twofold (correct the stale surface AND name
the loop).

## 3. Receipt and metric verification

```bash
# resolve the ID in its chain store and dump the row's field set
python3 -c "import json;[print(list(json.loads(l).keys())) for l in open('<chain>.jsonl') if '<receipt-id>' in l]"
# is there a body anywhere?
grep -rl "<body_hash>" /root/VAULT999 /root/arifOS/VAULT999 2>/dev/null | head
```

- Hash-stub shape (`body_hash`, `chain_entry_hash`, `prev_hash`, `receipt_id`; no actor, no
  timestamp, no claim) = membership evidence only. Say so in exactly those words.
- No body artifact anywhere → nothing is attested; the ID is not usable as a citation.
- Grep every quoted scalar against the store that claims to produce it, matching the field name —
  `292.75` and `0.56` are not `2.75`.

## 4. Reconciliation-assertion verification

```bash
python3 -c "import json;d=json.load(open('<store>.json'));\
print('arrays:',[len(v) for v in d.values() if isinstance(v,list)]);\
print('stats :',json.dumps(d.get('stats'))[:300])"
grep -rn "<old-value>" <dirs> --include=*.md --include=*.json
```

- Reconcile the summary block TO the array. Never the reverse.
- A count can be **wrong**, not merely stale: re-derive the numerator before touching the
  denominator.
- Grep the whole file after fixing one table — the same claim is commonly duplicated in another
  section of the same document (a card can carry both the new and the old number, 70 lines apart).
- An entry asserting its own consistency is the last place to look for that consistency, not the
  proof of it.
- A metric outside its declared range (a ratio in [0,1] reporting 1.22, a recount that disagrees
  with its own array) is a bug until proven otherwise — "timing artifact" and "live recount" are
  narratives, not diagnoses.

## 5. Safe reconciliation (when you do write)

```bash
cd <repo>
cp -a <each target> /tmp/            # backup before edit
git status -s                        # know what else is dirty — concurrent writers exist
# ...edits...
git add <explicit paths>             # never `git add -A` on a tree other lanes touch
git -c user.name=Hermes -c user.email=hermes@arifos.local commit -q -m "<what + why + revert point>"
git log --oneline -1 --stat
```

- A local commit is what makes "versioned" true and the change revertible; name the revert point in
  the message. Do not git-push, and do not write canon, without the sovereign's word.
- Say which surfaces you deliberately did NOT touch and why (a scoped document keeps its scoped
  number).
- Mode check while you are there: a private card at `600` alongside a twin draft at `644` is a
  control you can fix in one line.

## 6. Verdict shape

Keep three verdicts separate and never blend them:

1. **Claim verdict** — per claim: TRUE / FALSE / STALE / UNVERIFIABLE, with the probe that decided it.
2. **Alignment verdict** — did the reconciliation reconcile? Count surviving disagreements; a "zero
   remaining" claim is falsified by a single grep hit.
3. **Provenance verdict** — who wrote it, under what declared mode, and whether that mode permitted
   the write.
