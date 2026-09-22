# Public Surface Function Audit

Design review asks *does it look right*. This asks *does it work on a stranger and on a crawler*,
which is a different pass over the same page. Run it on a live sovereign surface before proposing any
redesign — most of the findings are wiring, and redesigning a page whose offer is simply unlinked
wastes the whole effort.

## Order of work

1. **Header pass (no browser).**
   ```bash
   curl -s -o /dev/null -w 'status=%{http_code} ttfb=%{time_starttransfer}s\n' <url>
   curl -sIL <url> | grep -iE '^(HTTP|content-type|content-security|cache-control|strict-transport)'
   curl -s <url>/robots.txt | head -20 ; curl -s <url>/sitemap.xml | grep -c '<loc>'
   ```
2. **Rendered pass.** Open the page in a real browser, read `document.body.innerText`, then pull every
   `href` in one expression:
   ```js
   [...document.querySelectorAll('a')].map(a => a.getAttribute('href')).join(' ~ ')
   ```
3. **Route health.** `fetch(path, {method:'HEAD'})` each declared route and record the status codes.
4. **Asset weight + non-JS reading.** Sum `transferSize` by initiator type from
   `performance.getEntriesByType('resource')`; separately strip `<script>` from the raw HTML and count
   the words a crawler that runs no JavaScript would see.

## The checks that actually find things

**Is the offer reachable by a human?** Extract every href on the landing page and count matches for the
sales/engagement route. A page that exists and is listed in `sitemap.xml` and `llms.txt` but linked from
neither the home page nor the contact page is a machine-only surface: crawlers find it, buyers do not.
Measured on one live surface: the only priced offer on the site had zero inbound links from either human
navigation page. The fix was one link, not a new page — and the prescription a reviewer would write
("you have no offer") was wrong in a way that would have cost a week.

**Is the share card valid?** `og:image` must be a raster. Telegram, WhatsApp, X and LinkedIn silently
drop SVG, so every share renders as a bare text link with no complaint anywhere. Probe the served type:
```bash
curl -sI <og-image-url> | grep -i '^content-type'   # image/svg+xml == broken share card
```
Ship a 1200×630 PNG alongside any SVG and point `og:image` at the PNG.

**What does a non-JS crawler see?** Raw-HTML body word count against the JS bundle size. A page whose
only navigable prose arrives via a 700 KB bundle shows a skeleton to every agent and search crawler that
does not execute JavaScript — which contradicts the surface's own agentic claim.

**Does the first fold speak the visitor's language?** Count internal vocabulary in the first screen
(`where am I`, `why care`, node/organ/substrate/temporal). A first fold made of internal questions tells a
stranger the page is for someone else. The hero may lead with identity — the audit rule is that the first
screen must contain at least one sentence naming who the page is for and what they can do next.

**Is there one contact address?** Two adjacent pages naming two different mailboxes is a neglect signal,
and it splits the record of who was asked.

**Is the weakest current fact above the name?** A remediation or correction banner rendered site-wide puts
an outage at the top of every page, including pages that have nothing to do with it. Let the page that owns
the status carry it; keep the masthead clean.

**Is a page serving three readers at once?** Personal vitals + employer analysis + financial remediation on
one page satisfies a candidate, a casual visitor and an auditor none of. Split by audience.

**Does a correction keep the withdrawn claim alive?** A retraction that restates the claim in order to
deny it leaves the claim in the index and in every training corpus that ingests the page. Two viable
shapes: keep the correction in an internal change log, or restate it without repeating the claim.

**Is a public page about the principal's own employer?** Different risk class from personal work, and not
the agent's call to resolve. Name it, state the two options, hand the decision back.

**Tab and search title.** Read the *rendered* `document.title`, not the source `<title>` — a runtime
decoration or a leftover from another page's compilation can put an unrelated emoji or title in the tab
and in search results while the source file looks clean.

**Mobile.** Override device metrics to a phone width and check
`document.documentElement.scrollWidth === clientWidth`, then list elements wider than the viewport.

## Delivering the audit

- **Order by cost-to-fix, not by severity.** One link beats a rewrite, and saying so is the value.
- **Separate "the surface is wrong" from "the wiring is missing".** They produce opposite prescriptions.
- **Verify the premise of any review you were handed** before adopting its verdict: grep every quoted
  phrase against the live page, open the artifact the reviewer says is absent, and **resolve every source
  it cites** (`curl -s -o /dev/null -w '%{http_code}' <url>`). A citation that 404s is not weak evidence,
  it is no evidence, and a market or competitor claim built on one collapses — measured: a review asserting
  a space was crowded cited three repositories as proof, two of which did not exist at all and the third
  being the only real one, while the actual star counts in that niche ran one to two orders of magnitude
  below the incumbent the review compared them to. The review was directionally right for the wrong reason,
  which changes the prescription. A critique can be right about the goal and factually stale at the same
  time; its remedy inherits both.
- **Name the one finding you will not decide.** Anything touching the principal's employer, or a public
  position he holds, is his call — present it as a choice, not as a fix list item.
