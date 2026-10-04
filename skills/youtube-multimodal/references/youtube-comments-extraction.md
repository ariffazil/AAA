# YouTube Comments Extraction via InnerTube (logged-out, proven 2026-08-08)

When the user wants **community reception / comments / sentiment** on a video (not the transcript),
this is the route that works on the VPS even while `yt-dlp --write-comments` dies on the bot wall.

**Proven on EVjOukIg_bQ** (TegapTV, 31.9k views, reported "46 comments"): recovered **28 comments
(20 top-level + 8 more on page 2)** — about 60–70% of the reported count. The rest live in reply
threads that logged-out InnerTube won't paginate.

## Recipe

### 1. Curl the watch page (works logged-out)

```bash
curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
  "https://www.youtube.com/watch?v=VIDEO_ID" -o watch.html
```

Extract `ytInitialData`:

```python
import re, json
html = open('watch.html', encoding='utf-8').read()
m = re.search(r'var ytInitialData = ({.*?});</script>', html, re.S)
data = json.loads(m.group(1))
```

Comments are **not** in the initial payload. The engagement panel only carries a continuation token:

```python
# panel id == 'engagement-panel-comments-section'
token = data['engagementPanels'][0]['engagementPanelSectionListRenderer']['content'] \
        ['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0] \
        ['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
```

### 2. POST the continuation to InnerTube

```python
payload = {"context": {"client": {"clientName": "WEB", "clientVersion": "2.20231219.04.00",
           "hl": "en", "gl": "US"}}, "continuation": token}
req = urllib.request.Request("https://www.youtube.com/youtubei/v1/next",
      data=json.dumps(payload).encode(),
      headers={"Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 ... Chrome/120 ...",
               "Origin": "https://www.youtube.com",
               "Referer": "https://www.youtube.com/watch?v=VIDEO_ID"})
resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
```

### 3. Parse the NEW schema — `commentEntityPayload`, not `commentRenderer`

The old `commentRenderer` / `backstageCommentThreadRenderer` keys are **gone** in the modern
watch response. Comments arrive as `commentEntityPayload` inside
`frameworkUpdates.entityBatchUpdate.mutations[].payload`. Walk the whole tree and grab:

| Field | Path |
|---|---|
| text | `properties.content.content` |
| author | `properties.authorButtonA11y` (or `author.displayName`) |
| time | `properties.publishedTime` |
| likes | `toolbar.likeCountNotliked` (string; `" "`/`""` = 0) |
| replies | `toolbar.replyCount` (string; `""` = none) |
| id | `properties.commentId` (dedupe key) |

The view models (`commentViewModel`) reference comment keys but carry **no content** — only the
entity payloads in `frameworkUpdates` do. `commentThreadRenderer` still appears (21× on the
test video) but only as scaffolding; don't parse text from it.

### 4. Paginate with the next top-level token

After page 1, find the *next* continuation token directly under
`onResponseReceivedEndpoints[].appendContinuationItemsAction.continuationItems[]` — a
`continuationItemRenderer` whose token starts `Eg0SC0VWak...` and is NOT nested inside a
`commentRepliesRenderer`. POST it the same way.

**Dead ends (do not burn round-trips):**
- Reply-thread tokens (`.../commentThreadRenderer/replies/commentRepliesRenderer/...`) only load
  replies for ONE thread, logged-out — not more top-level comments.
- `/youtubei/v1/next` with a stale/raw token returns `{"backgroundPromoRenderer": "This video
  isn't available anymore"}` — misleading; it's a token/context problem, not a deleted video.
- `comment_service_ajax` POST → HTTP 400 Oops page.
- transcriptapi.com "comments" endpoints → 404 (don't exist).

**Cap honestly:** reported comment count in the description (e.g. "46 comments") includes hidden
and reply-thread comments. Logged-out recovery ≈ 60–70%. Say so; never pad.

## Deliverable QA pattern (learned the hard way)

When handing back extracted comments as a JSON deliverable, verify **verbatim fidelity** against
the raw extraction, not just schema:

- `text` must match byte-for-byte (smart quotes `’` preserved; do NOT replace emoji runs with
  shorthand like `[emoji barrage]` — the deliverable lost content and a diff caught it).
- `likes`/`replies` from InnerTube are **strings**; `""`/`" "` means none. Normalize to `null` in
  the deliverable, never `0` (a strict `==` check flagged `''` vs `0` as drift).
- Keep `id` on every comment — the dedupe key across pages.
- Write a throwaway verifier (`/tmp/hermes-verify-*.py`) comparing deliverable vs raw extraction
  per-comment on `author/text/time/likes/replies` (type-lenient: `int()`-normalize both sides),
  then delete it. Structural JSON checks alone missed two content drifts.

## Related

- Comment timestamps come back as relative strings ("5 years ago") — fine for sentiment work;
  if absolute dates matter, cross-check `publishedTime` against the upload date from oEmbed.
- Some commenters post timestamp-linked physique notes (`"4:38 die Schultern..."`) — those map to
  real `startTimeSeconds` in `commandRuns`; surface them as user-tagged moments.
