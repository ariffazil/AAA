# Delivery-state probe — extract the artifact, then prove it left

Both halves are cheap. Run them before composing any answer about an artifact's human impact.

## 1. Extract the text (and diff versions)

```bash
python3 - <<'PY'
import pymupdf
p = '/root/.hermes/cache/documents/doc_XXXX_name.pdf'
d = pymupdf.open(p)
t = '\n'.join(pg.get_text() for pg in d)
print('pages', len(d), 'chars', len(t))
print(t)
PY
```

Two files with the same title are two drafts. Diff the extracted text, not the PDFs:

```bash
python3 - <<'PY'
import pymupdf, difflib
a = '\n'.join(p.get_text() for p in pymupdf.open('A.pdf'))
b = '\n'.join(p.get_text() for p in pymupdf.open('B.pdf'))
d = list(difflib.unified_diff(a.split('\n'), b.split('\n'), lineterm='', n=0))
print('DIFF LINES', len(d))
print('\n'.join(d[:120]))
PY
```

Read the delta first. In this class of artifact the last page often differs — that is the author's
real decision (whose voice closes the document) and it is usually the thing they actually want to talk
about.

Pitfall when extracting: `fitz` is the deprecated alias — `import pymupdf`. Uploaded files land under
`/root/.hermes/cache/documents/` with a `doc_<hash>_<originalname>` prefix; the original filename is
preserved, so listing that directory with a name filter finds every version.

## 2. Prove whether it was sent

The gateway log is the delivery witness. Grep by the recipient's chat id, then by attachment events:

```bash
# every inbound/outbound event tied to one address
grep -a "<CHAT_ID>" /root/.hermes/logs/gateway.log | tail -25

# attachment/document events — uploads land as "Cached user document at ..."
grep -a "<CHAT_ID>" /root/.hermes/logs/gateway.log | grep -aiE "document|pdf|media|photo|attachment"

# any event mentioning the artifact by name across the log
grep -ai "<slug-or-title>" /root/.hermes/logs/gateway.log | tail -5
```

What the lines mean:

- `inbound message: ... chat=<id> msg='...'` — the human sent something to that address.
- `Cached user document at <path> (<mime>)` — an **inbound** file arrived and was cached. Note that the
  path prefix runs `doc_<hash>_<name>`, so this is also how you find which drafts exist and when each
  arrived — arrival timestamps are the cheapest version history available.
- `Sending response (<n> chars) to <id>` — the transport accepted an **outbound** text message.
  That is `SENT`, not `DELIVERED` and not `READ`.

If there is no outbound event for the recipient's chat id, the artifact has not left. Say so.

## 3. Reading the result honestly

| Evidence found | State you may claim |
|---|---|
| draft file exists in the cache | `WRITTEN` |
| outbound send line for that chat id | `SENT` |
| per-message delivery receipt / read acknowledgement | `DELIVERED` / `READ` |
| nothing | `UNKNOWN — cannot witness` |

`"No record of a send"` is a **negative claim** and needs the same warrant as a positive one: name the
lane you searched and the window you searched. Do not upgrade "I did not find it" into "it never
happened" — and do not upgrade "the transport accepted it" into "he read it".

## 4. Companion probe — is the artifact ours at all

When it is unclear whether the artifact originated inside the federation or arrived from outside, sweep
the local source trees for its title or a distinctive line before narrating its origin. An empty sweep
is itself a finding: the artifact came in from a lane you do not produce, which changes who owns the
decision about it.
