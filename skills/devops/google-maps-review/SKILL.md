---
name: google-maps-review
description: "Use when posting a Google Maps review agentically."
version: 1.0.0
author: hermes
license: MIT
metadata:
  hermes:
    category: devops
    tags: [google, maps, review, browser-automation, playwright]
    related_skills: [browser-playwright-runner, google-workspace-gws]
capability_tier: fed-realtime-voice
ecology_state: WARM
---

# Google Maps Review — agentic posting

## The hard truth (verified 2026-10-18, do not re-litigate)

Google has **NO API to post a review as a consumer**. Three independent facts:

1. **Google Issue Tracker #35820688** — a public API to post user reviews was requested 2011 and closed **"Won't Fix (Infeasible)"** 2016. Signed-in Maps API experiences are deprecated.
2. **Business Profile API** (`mybusiness.googleapis.com`) — `accounts.locations.reviews.updateReply` is **owner-only**: it replies to reviews on a business YOU own/verify, under the `business.manage` OAuth scope. It cannot post a consumer review on someone else's listing.
3. **Places API** — read-only. Returns reviews (hard cap 5), cannot write.

So there is **no API key, no OAuth scope, no MCP endpoint** that posts a Google Maps review as a user. Anyone selling one is either (a) browser automation, or (b) a scam.

## The right connection: browser automation

The ONLY agentic path is to drive a real browser, signed into a Google account, to the direct review-writing URL and submit the form.

- **Tool we already have:** the `browser_exec` tool (Browser Use).
- **Direct review URL** (bypasses all navigation):
  `https://search.google.com/local/writereview?placeid=<PLACE_ID>`
  where `<PLACE_ID>` is the **ChIJ** place id (also accepts the `0x…:0x…` FTID in many cases).
- **The account must be signed in in the browser.** There is no token shortcut: Maps reviews ride the web session cookie (SID/SAPISID), not an OAuth bearer token. The `google_token.json` OAuth scopes (gmail/drive/calendar/spreadsheets) do NOT cover Maps reviews, and Google exposes no such scope.

## One-time human gate (irreducible)

Posting requires Arif's OWN Google account to be signed into the browser. This is **authentication, not copy-paste**: password + 2FA are his and his alone — no agent may or should type them (CORE RULE: secrets never travel through the agent).

- Do this ONCE per persistent session, then the flow is fully agentic until the cookie expires.
- Use a **named persistent session** so the login survives across calls:
  `browser_exec(session="google", code=...)`

## Resolve place → place_id

Prefer passing a full Maps URL (the `!1s0x…:0x…` FTID inside it is usable). To convert a Maps URL to a clean review link without a Google API key:

```
POST https://productmate.com/api/v1/google-review-link
{"maps_url": "https://www.google.com/maps/place/..."}
→ { "place_id": "ChIJ…", "review_url": "https://search.google.com/local/writereview?placeid=ChIJ…" }
```

Or just open the Maps place page in the browser and read the place id from `window.location.href` / the `data:` payload. No key needed.

## LIVE BLOCKER (verified 2026-10-18) — Google rejects COLD headless login

A fresh headless login from the VPS is rejected by Google BotGuard at the
identifier step (`signin/rejected`) — BEFORE password/2FA is ever asked.
Adding a TOTP secret does NOT fix this (it never reaches that step).

**The browser path is NOT dead** — only cold login is. Two viable escapes:
1. **Cookie import (the real durable fix):** import an already-logged-in
   Google session (storageState.json / cookies exported from Arif's own
   trusted device) into the persistent browser profile via CDP
   `Network.setCookie` (or playwright storageState). Then the session skips
   login entirely — no BotGuard challenge. Still may be CAPTCHA-flagged for
   review posting specifically from a datacenter IP; test before claiming.
2. **Direct write-review URL** (for a one-off): `search.google.com/local/
   writereview?placeid=<FTID>` — one tap on his logged-in phone, straight to
the form.

Do NOT retry cold login in a loop (account-lock risk). After one
`signin/rejected`, stop.

## The posting flow (after login exists)

```python
# browser_exec, session="google"
new_tab("https://search.google.com/local/writereview?placeid=<PLACE_ID>")
wait_for_load()
# 1. click the star row for the rating (1-5)
# 2. type review text into the textarea
# 3. click "Post" (or "Posting" / "Publish")
# 4. VERIFY: the review now appears in the "Your reviews" list, or the page
#    shows it was posted. Do NOT trust the click — check the DOM/URL after.
```

Do not describe the plan to the user — execute it, then report what the DOM shows after posting.

## Verify (never self-report success)

- After clicking Post, re-read the page. A successful post either navigates to the place's review list with the new review, or shows a confirmation.
- If the button label is "Posting…" and nothing changes, the review did NOT land. Do not claim success.
- If a CAPTCHA or "Something went wrong" appears, the account is being challenged — stop and tell the human the review was blocked, do not retry in a loop.

## ToS note (fact, not moralizing)

Automated review posting is against Google's terms and may get the account flagged if done at volume. One review on Arif's own account of a place he genuinely visited is a normal user action; a fleet of accounts posting programmatically is review fraud. Keep this lane for Arif's personal, genuine reviews.
