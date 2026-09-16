# Knowledge Artifact Verification — the truth axis

Companion to `rendered-document-audit`. Arrival and legibility are proven by the
render audit; this file covers the third verdict: **is what the document claims
actually true, and can the document be traced to its own production?**

Typical shape: a multi-page PDF attributed to the principal, covering a technical
subject, carrying per-claim evidence classes, a reference list, and often its own
uncertainty or shadow annex. Nothing is runnable, so the whole audit is evidentiary.

## Intake

```bash
pdfinfo in.pdf | grep -E '^Pages|^Page size|^Producer'   # declared extent + renderer
pdftotext -layout in.pdf /tmp/doc.txt && wc -l /tmp/doc.txt
```

`-layout` preserves the column structure that reference lists and evidence-class
tables depend on; plain `pdftotext` interleaves columns and makes the reference list
unreadable. Read the full text layer before probing anything — a number that appears
nowhere in the document is not a finding, and a claim written as settled but labelled
`INT 0.55` in the author's own appendix is a finding the author already half-admitted.

## Axis 1 — propagate every load-bearing claim to live state

Build the claim list first (claim | where the artifact says it came from | the
artifact's own confidence), then probe each in the source's own format. Check
against **both** the resource files and the code — they drift independently.

```bash
grep -rn -i -E "<term>" <organ>/resources <organ>/okf 2>/dev/null
grep -rn -i -E "<term>|<STATUS_CONSTANT>" --include="*.py" <organ> | grep -v .venv
```

Priority divergence targets:

- depths, ages, thicknesses, volumes — numbers get revised in one place only
- status/enum constants (`PENDING`, `RESOLVED`, `NON-KILL`) that state whether a
  test has actually been run
- formation, unit, and product names — transcription corruption survives review
- chronology tables — a **missing** entry is invisible unless you diff the table
  against the narrative that references it
- the artifact's own arithmetic: durations against the age range cited, per-item
  counts against the stated total

## Axis 2 — citation metadata

Existence is not accuracy. For each load-bearing reference: search the title, then
compare **journal, year, volume, pages, DOI** character-for-character.

| Finding | How to report it |
|---|---|
| Title, authors, journal, year all confirm | OK — cite as written |
| Paper exists, journal wrong | Fabricated metadata — give the corrected citation |
| Paper exists, DOI wrong | Same — a DOI is a pointer, and a wrong pointer is broken |
| Plausible author + year, no such paper found | Treat as fabricated until proven |

## Axis 3 — provenance of the artifact itself

```bash
find / -xdev -name "<deliverable-name>*" 2>/dev/null     # every copy on the machine
md5sum <copies>                                          # same hash = re-delivery, not a rebuild
ls -lat <organ>/forge_work/ <organ>/.forge 2>/dev/null   # forge/run directory
grep -rl "<distinctive string>" <vault-root> <claim-ledger-root> <canon-root> 2>/dev/null
# producing-agent transcript, e.g. /root/.<cli>/projects/-root/chats/*.jsonl
```

Classify and say which you found:

- **Full chain** — build script + forge record + claim/seal entry + producing run.
  The artifact is citable.
- **Partial chain** — a producing session exists but no build source for this version.
  Say exactly that; a session is not chain of custody.
- **No chain** — nobody can say how this file was produced. For an artifact that
  grades its own claims by evidence class, this is a first-order finding.

Check delivery timestamps against the document's own "compiled" date. A copy whose
page count differs from every local build, delivered with no local source, is an
unverifiable copy no matter how good its content is.

**The document's prose about its own production is a claim like any other.** "The tool
has been built. The code is written." is a statement about method, and an unevidenced
one reads exactly like an evidenced one. Probe it — a document can grade every claim
about its *subject* by evidence class and still be unevidenced about *itself*, which is
the failure it exists to criticise, occurring one level up.

## The unexecutable-recommendation probe

Probe each recommended action for its preconditions, not its plausibility:

| Recommendation | Probe |
|---|---|
| "Reuse existing data — zero cost" | Does the required dataset exist and is it loaded? Read the organ's own status constant. |
| "The tool has been built" | Find the tool; read the status/enum field for the input it needs. |
| "Reprocess public data" | Does the organ hold that data, or is it a plan? |
| Acquire new data (costed) | Usually honest — cost stated, vendor unnamed |

State plainly which recommended actions can start today and which one collapses on
contact with its input. A recommendation that cannot execute as written is the most
expensive kind of error, because it gets quoted in a room.

## The self-audit annex is a claim too

When the artifact contains its own honesty annex (shadow audit, uncertainty register,
"issues found while building"), do not accept it as evidence of rigour. Re-verify every
item against the live source. If it checks out, that annex is usually the strongest
part of the deliverable and should be reported as such. If it does not, the annex is a
credibility performance — a far bigger finding than anything it confessed to.

## The write side — do not let the audit launder a value you just found contested

The audit produces two artifacts: the verdict, and anything you write from it (a claim
entry, a reconciliation patch, a ledger). The second is where the finding gets lost.

Copying a number out of the source into a record **strips its uncertainty**, because the
record has a field for the value and none for "this value is contested." The source is
one document; your record becomes the baseline others read, asserting that number with
the authority of the audit standing behind it. The better the audit, the more credible
the laundered copy.

1. **Carry the status inline.** If you flagged the value CONTESTED, ORPHAN, UNTESTED or
   UNTRACED anywhere in the audit, the record entry says so beside it — never the bare
   value on its own.
2. **Ask which reading the claim actually needs.** If the mechanism holds under any
   plausible value, write the claim without the number ("at comparable depths") and put
   both readings in the dispute field. The number was decoration; the mechanism was the
   claim.
3. **Read the record back by parsing, not from memory.** Re-open the artifact, re-parse
   it, grep every figure you added, then grep the status word to confirm nothing is
   carried unattributed. Name the resolved path you read back from.
4. **A field that cannot hold uncertainty must not receive a contested value.** Split it
   into explicitly named values with their sources, or leave it out.

An artifact inherits its author's unexamined assumptions, not only their data — and when
you authored the artifact, the author is you. Read-back is the only thing that catches it;
re-reading the source will not, because the source was correct about its own uncertainty.

## Delivery

- Verdict first, one paragraph. Then pass/fail with evidence. Then consequences with
  one concrete next action each.
- Never present the document's own annex as your verification — say you re-verified
  it item by item.
- Quantify: claims checked, values divergent, copies unverified.
- Name the artifacts left unmodified. If a source is **sealed**, the reconciliation is
  a proposal for the principal to ratify, not a fix — re-sealing a sealed artifact is
  an authority boundary, not housekeeping.
- When the artifact's most valuable output is lateral to its subject (a defect it
  exposes in the auditing organisation's *own* asset), lead the consequences with
  that, not with the domain synthesis — it is cheaper to fix and closer to the money.
