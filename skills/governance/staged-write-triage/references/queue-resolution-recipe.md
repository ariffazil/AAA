# Queue Resolution Recipe

> Depth for `staged-write-triage`. Load when actually clearing a staged queue and
> producing its receipt.

---

## 1. Read everything before deciding anything

```bash
ls -la <pending-dir>/
for f in <pending-dir>/*.json; do
  python3 -m json.tool "$f"
done
```

For each payload note: `created_at`, the list of operations, and the **target**
entry each operation claims to replace. You are looking for the same target appearing
in more than one payload.

---

## 2. Dead-on-arrival check

```python
for op in payload["operations"]:
    if op["action"] in ("replace", "remove"):
        anchor = op["old_text"]
        print("MATCHES" if anchor in live_store else "DEAD", anchor[:60])
```

A payload whose anchors match nothing live is **DEAD**. It would fail on apply no
matter what it contains; it is evidence of producer drift, not a candidate.

---

## 3. Generation count

Group by theme/target and count distinct replacement texts:

| Theme | Generations | Conflict |
|---|---|---|
| `<target>` | 3 | three different replacements for one entry — newest wins if replayed, erasing two |

Any theme with more than one generation means "approve all" is ambiguous. Report the
counts to the human as the reason you are not approving literally.

---

## 4. Verdict per item

| Verdict | When |
|---|---|
| **SALVAGE** | passes the content gate and changes a future decision |
| **REJECT** | fails a content gate — derivable, non-decisional, PII, inferred-as-fact, psychological modelling |
| **DEAD** | anchor no longer matches a live entry |

Record the reason string for every verdict. It is the receipt.

---

## 5. Apply, then move

```bash
mkdir -p <pending-dir>/processed-<YYYY-MM-DD>-<topic>/
for f in <ids>; do mv "$id.json" "<processed-dir>/"; done
```

The queue directory must end up with **zero** unprocessed items. Leave the processed
directory in place — it holds the payloads plus the receipt and is the reversal path.

---

## 6. Receipt shape

```markdown
# <Subsystem> Write Resolution

## Finding
<count> batches were <N> generations of <M> themes; "approve all" was never
coherent because <reason>. Dead-on-arrival: <n>.

## Verdicts
| id | generations | verdict | reason |

## Salvaged
| content | source | destination |

## Rejected classes
<the recurring classes and the standing rule each one violates>

## Root cause
<producer drift / no consumer / cadence mismatch — and which layer owns the fix>

## Reversibility
<archive path; how to restore; what was moved vs deleted>
```

---

## 7. Falsifiable test that it worked

- the pending path is **empty** after resolution
- the archive/processed path holds every original payload plus the receipt
- **no re-derivation of a retained item reappears within the review cadence**

A re-appearance is not a queue bug — it means the boundary is missing upstream and
the producer keeps re-deriving what is already stored. Fix that, not the pile.

---

## 8. Repo check before committing the resolution

```bash
# staged queues and personal data must never be committable in a repo with a remote
git check-ignore -v <pending-dir> || echo "NOT IGNORED - add it"
git ls-tree -r HEAD --name-only | grep -c "^<pending-dir>/"   # expect 0
```

If a resolution commit already carries the payloads and the commit is unpushed:

```bash
git reset --soft HEAD~1
git rm -r --cached --quiet <pending-dir>/
# add the .gitignore entry, then re-commit without the payloads
git add .gitignore && git commit -F <message-file>
```

Files stay on disk; only the index changes. Verify `git ls-tree -r HEAD` shows zero
files under the directory before the commits are pushed.
