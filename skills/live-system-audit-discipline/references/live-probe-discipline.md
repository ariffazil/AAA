# Probing and patching a live, multi-writer system

Depth for audit work where the system keeps moving while you investigate.

## The served artifact is not the working checkout

A service runs what was built and installed, not what sits in the dev checkout. Before
concluding anything about deployed behaviour, resolve the path the process actually loads — the
unit's `ExecStart`, that interpreter, the installed root's site-packages — and compare it against
the repo tree. A patch applied to the checkout can be a silent no-op, and the checkout may be many
commits ahead of or behind the running build.

Cheapest confirmation that the running process executes the code you just read: find a log string
or literal that exists only in the new version, and confirm the process emitted it. Do this before
believing a fix is live.

`changed on disk` is not `serving`. Report the former; a reload is a separate, often gated, step.

## Cross-host: localhost is not federation

A claim of "written to the federation graph" is host-local until the bind address proves
otherwise. A Docker container publishing `127.0.0.1:6380` is reachable only from inside the same
host; another host on the same network cannot query it even if it has the same image. Two
hosts running identical FalkorDB / Qdrant / Redis images with identical graph names ("arifos",
"af_forge", "arif_l5_knowledge") are still **two independent graphs**, not one.

When the claim is "X is in the federation graph", probe four things before writing it:

1. Bind address of the store (NOT the port, NOT the image name). `ss -tlnp | grep <port>`.
3. Graph name actually written to (read it from the writer's own config or call site).
4. Network path from a different host to the store (curl from another box on the wire, not from
   the same host).

A write to `arifos` graph on `127.0.0.1:6380` of host A is invisible to host B even when B has
its own `arifos` graph — the namespaces are different stores. Two hosts can each independently
report "29 Episodes in arifos" without contradiction; the failure is to call this a federation
graph when neither side has network reachability.

A receipt that says "X written to federation graph" without these four probes is a receipt for
local action, not federation action. Demote the language: "written to host-local store
<host>:<graph>".

## Source read beats vision read when the file is local

A vision call on a PNG rendered from a text-format source costs more than opening the source
file. The vision pass can also hallucinate — a "truncated footer" claim that a 2-second
`read_file` shows is intact is exactly that. Read the source when:

- The artifact under inspection was generated locally (rendered card, compiled output, formatted
  log) and the source is on disk in the same session.
- The defect class is layout/string-specific (truncation, overflow, ordering) — vision's
  spatial reasoning is weaker than grep's lexical one for these.
- The user is in a tight loop and a hallucinated "defect" would trigger wasted investigation.

Reserve vision for cases where the source is unavailable (scanned doc, photo of physical
artifact, terminal rendered to canvas, agent cannot access the file directly) or where the
defect class is genuinely visual (misalignment, color clash, occlusion). If the choice between
"vision this" and "read the source" is open, read the source — vision is the more expensive
and the less reliable path for this class of claim.

## Same name, two stores

One logical name (vault, registry, ledger) can resolve to different physical locations on the same
host. Before designing a cleanup or migration, enumerate the candidate paths and determine which
one the consumer reads. Cleaning the path nobody reads fixes nothing while looking like progress.

### Writer and reader on different ledgers — the deferred-witness defect

The severe form is not two copies of the same data. It is two stores of the SAME OBJECT CLASS that
disagree about membership: the producer appends to one, the verifier reads the other, and neither
is wrong. Both report healthy; every receipt the loop exists to collect lands with no witness.

```bash
# the id sets, from every candidate store, before any conclusion about "verification exists"
python3 - <<'PY'
import json, pathlib
stores = [pathlib.Path(".../predictions.json"), pathlib.Path(".../predictions.jsonl")]
def ids(p):
    if not p.exists(): return set()
    raw = p.read_text()
    rows = ([json.loads(l) for l in raw.splitlines() if l.strip().startswith("{")]
            if p.suffix == ".jsonl" else json.loads(raw).get("predictions", []))
    return {r.get("prediction_id") for r in rows if r.get("prediction_id")}
sets = {str(p): ids(p) for p in stores}
for k, v in sets.items(): print(len(v), k)
a, b = sets.values()
print("overlap:", len(a & b), "| only-A:", len(a - b), "| only-B:", len(b - a))
PY
```

An overlap of **zero** is the finding. Report it as such — not as "the verifier is broken".

**Rule out the cheap alternative before naming a mechanism.** If a row looks overdue and the tool
says nothing is due, load the tool's own input and print the ids. A first, plausible story — the
row is being skipped on a stale field — is very often wrong: the tool reads a different ledger and
has never seen that row. The stale-field story and the disjoint-store story produce the same
symptom and only one of them is true.

**Silent skips: a caught exception is an absence.** A row loop wrapped in a bare `except: pass`
turns a key-name mismatch (`state` vs `status`), a missing date, or a bad format into a vanished
row. Accept both key spellings, mark anything unparseable on the row itself, and count it in the
output. "0 due" must always mean "0 of the rows I loaded", stated with the loaded count.

### Merging stores safely

If you fix it by reading a union, the merge is only half the repair — the other half is the write
path.

1. **Tag every row with the store it came from** at load time (`_store`), and write each row back
to its OWN ledger. Without this the union silently MIGRATES every row into whichever file is
written first — replacing a visible split with a hidden one.
2. **Key on a real id**, deduplicate on it, and keep the losing store addressable on the row
   (`_also_in`) so a genuine collision stays visible rather than being resolved by file order.
3. **Back up a line-oriented store before rewriting it**, and only rewrite the rows you own.
4. **Test the round trip without any verification in between:** `load → save → reload`, and assert
   the per-store counts are unchanged. Counts equal before and after is the proof that no migration
   happened; a total that matches while the split moved is the failure this test exists to catch.
5. **Report the residual, do not hide it.** The two stores are still two. Converging them is a
   data decision with an owner; until then, say that the union makes every receipt collectible and
   leave the ownership question open.

### Still-structural gaps to report alongside the fix

- **A due date with no named keeper.** The record carries a `verify_date` and no owner/witness
  field, so nothing survives the interval between the claim and its receipt. On any ledger of
  predictions, check for both and report the missing one as its own finding — a date is not a
  witness.
- **A private row in a public store.** Compare the store's schema against its sibling (e.g. events
  carry an `audience` field, predictions do not) and flag the mismatch, because it decides who is
  allowed to read the receipt when it lands.

## Working while others write

Assume other agents share the repo and are committing.

- Re-check the file's mtime/hash immediately before patching. If it moved, re-read before you
  edit, and redo any analysis built on the old content.
- Prefer additive edits — append a labelled correction and keep the other writer's text — over
  overwriting their section. It preserves attribution and avoids silent data loss.
- Do not plan a write against a moving target; either confirm the file is quiet or coordinate.

## Independent verification

Self-verification does not count. A fix is confirmed when a different client, seat, or method
re-probes the same input — not when the author re-runs their own probe. Where a second seat is
unavailable, say so and mark the claim author-verified.

A pre-committed prediction with declared outcomes, tested by a different seat, is the clean way to
promote a heuristic toward a predictor. One confirmed prediction is n=1, not an oracle.

## A blocked mutation is a result

A gate that refuses a write is an outcome to report, not an obstacle to route around. State the
exact blocked operation and the gate that refused it. Never hand the human a shell command to
apply on your behalf, and never describe a gated change as staged or done.

## Check the identifier before you mint it

Before introducing a symbol, prefix, or class number in a report or doctrine, check the live
symbol registry for reserved prefixes and run the namespace probe. A borrowed identifier that
collides with an existing ratified one is a high-severity defect, and it propagates: every
artifact that quotes you inherits it. Cite the source doctrine by name when you cannot verify its
number.

## When correcting another writer

Hold your own correction to the standard you are applying. Verify the specific claim before
asserting it is wrong, and check your own scoping — a correction that generalises from one probe
repeats the error it is correcting, one layer up.

## Reporting a fix you have not observed working

If a change is authored but not yet serving, say exactly that: authored, syntax-checked, on disk,
not live. Do not let "applied" or "done" describe a state the system has not reached.
