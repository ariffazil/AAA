# Archive parsing & attribution pitfalls

Mechanics for the retrieval pass. Most of these produce *silent* wrong answers — an empty result, a
mis-attributed speaker, a count that changes under a different definition — which then get written into
a deliverable as fact.

## 1. WhatsApp export regex

Two failures that both return **0 parsed messages with no error**:

```python
raw = open(path, encoding="utf-8", errors="replace").read().replace("\u202f", " ")   # 1
HDR = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s+"
    r"(\d{1,2}:\d{2}(?::\d{2})?[\s\u202f]*[AP]M)\s+-\s+"
    r"([^:]{1,40}):\s+(.*)$")                                                     # 2
```

1. **Narrow no-break space (U+202F)** sits between the clock and `AM`/`PM` in modern exports
   (`1:38\u202fAM`). A pattern expecting a plain space fails on every line. Normalise *and* allow it.
2. **Seconds are optional** (`1:38:12 AM` vs `1:38 AM`). Make the seconds group optional or the newer
   format fails wholesale.

Continuation lines (a message wrapped across lines) have no header — append them to the previous
message rather than dropping them, or quoted text loses its tail.

**Always print `parsed: <n>` before analysing.** No real export parses to 0, and a suspiciously round
number is a regex bug, not a quiet chat.

## 2. Attribution — group messages come in two shapes

| Shape | Where the speaker lives |
|---|---|
| Inline tag | `msg='[Name\|uid] body'` with `user=unknown` |
| Display name | `user=<display name>` with no tag in the body (`user=No name`, `user=ARIF`) |

A parser keyed on the inline tag alone returns zero rows for the second shape and silently banks them as
"unattributed". Resolve display names to identities (a privacy-masked profile shows as `No name`; that
is a person, not a system field) and print the by-speaker census over **both** shapes. An
`unattributed` bucket above roughly a tenth of the chat means the attribution regex is incomplete —
not that the chat was quiet.

**Never hardcode a uid-to-person mapping from the task prompt.** Resolve identities from the channel
resolver / lane files, and treat any name the requester supplies as a claim to verify.

## 3. A zero from a regex is a hypothesis, not a finding

An absence claim ("never", "zero", "no evidence he") is the most consequential sentence you can
publish and the easiest to get wrong, because nothing contradicts it. One search for the dictionary
spelling of a word returned "0 instances / 33 months"; the subject's own spelling was a consonant
transposition of it, and he had used it **eleven times**, including direct requests and two notices that
it had stopped. The false negative had already propagated into several downstream documents before it
was caught.

Before writing any absence, do all four:
1. **Variant spellings** — misspellings, transpositions, phonetic respellings, dialect forms. A word the
   subject only ever types phonetically will never match its dictionary spelling.
2. **Register** — the same act appears in BM, English, dialect and emoji; those are one semantic class,
   and searching one token is not searching the class.
3. **Widen the token** — stem, root, or a looser regex (`wor[ks]*hip`), not just the exact word.
4. **Search the raw artefact, not a derived index.** An index built from an earlier bad parse inherits
   its gaps.

Then attach the search surface to the claim: *"not found by these patterns: `<list>`"* — so the next
reader can falsify it.

**Confirm the instrument before convicting the subject.** When a term comes back mangled *every* time,
probe it in isolation before declaring a defect in the source: a constant that reproduces on every trial
is a property of the pipeline, not of the content, and the fix is to change the input, not to re-run.

## 4. Define the counting unit before quoting a number

Headline counts are definition-dependent and several definitions are defensible. Days with at least one
message, at least two messages, and both parties present can give three different totals from the same
file; "messages" may or may not include system notices and placeholder lines. Quote the number **with**
its definition, or a later pass will recompute a different one and both will look equally authoritative.
Same for share-of-messages, initiation rate, and every per-sender count.

## 5. Truncation, rotation and retention

- Gateway/agent logs truncate message bodies around 200 characters **without a marker**. Never present
  such a quote as complete; recover the full text from a different store before quoting it.
- Log files rotate fast (a handful of files covering roughly a fortnight). Any absence claim is a claim
  about that window only — state the covered span from the first and last timestamps you actually read.
- Two inbound shapes of the same DM (a primary id plus a mirrored id) mean the same message can log
  twice. Dedupe on text + timestamp before counting volume.
- A zero-length result from a plain `grep` over a log containing binary bytes is a grep artifact, not
  silence — re-run with `grep -a` before concluding anything.

## 6. Media voids — test recoverability before calling it a void

`<Media omitted>` is not automatically recoverable. Open the archive and list its entries **before**
writing "media not yet retrieved": a chat zip holding only the `.txt` (no media folder, no thumbnails)
means every omitted item is gone permanently. Say **"unrecoverable from this host"**, not "not yet
audited" — the softer phrasing invites a later session to promise a recovery that cannot happen, and a
void described as pending is a void someone will try to fill with inference.

Metadata (sender, timestamp, image-vs-video) may be reconstructed from context even when content is not;
metadata alone must never be used to infer what an image showed.

## 7. Corpus hygiene

A private human corpus is sensitive material from the moment it lands. An export unpacked into a shared
scratch directory at mode 644 is readable by every process on the host, and a scratch directory is also
evictable — you can lose the only copy while it is exposed.

Immediately after the first successful parse: move the source into a dedicated `chmod 700` workspace
directory, `chmod 600` every file (sources *and* derived JSON/JSONL caches), and **record the new path
in the deliverable**. Otherwise a later session re-runs a search against a path that no longer exists
and reports the miss as "no data".

## 8. What a parser cannot reach

Text corpora carry contact topology (who initiates, who returns, what words appear) and are close to
blind on eyes, touch, proximity, tone, hesitation, and private embodied encounters. When the user's real
question is in the second category, say so explicitly — **more data from the wrong channel does not
solve a missing-channel problem**, and a thousand more messages will add almost nothing.
