---
name: civic-article-publishing
description: Use when writing or publishing a public civic article.
---

# Civic Article Publishing

The full life of a public article on the federation's own web property: draft → register → deploy → verify → extract. Technical deploy mechanics live in `FORGE-agentic-web-builder` (user-owned; load it alongside, but note its gates are status-code only).

## 1. Draft for a ZERO-CONTEXT reader — non-negotiable

The reader did not follow the news. Assume they know none of the entities, none of the history, none of the stakes.

Order the piece:

1. **Hook** — one line, plain, present tense
2. **Context block** ("DULU" / background) — who the parties are, the history, the numbers at stake, why now
3. **Argument** — only after the reader can follow it
4. **Closing invariant** — one sentence the reader can repeat

A draft that opens on the argument without defining the parties is not "tight" — it is incomplete. It will be sent back.

## 2. Match the user's compression

When the user states a point in a few words, do not restate it at length. If they compressed it, they want it compressed.

- One line beats a list; a list beats a section; a section beats a report.
- When asked for "one line I can forward", give literally one sentence: no preamble, no options, no labels, no framing.
- Do not append a summary of what you just said.

## 3. Never emit an unsourced statistic

Percentages, counts, base rates, "most", "typically", "textbook" — if you cannot name the source, you do not have the number. Omit it, or label it UNVERIFIED.

- When a fabricated number surfaces, retract it explicitly in the same thread. Restating it with a hedge ("roughly", "around") is a second fabrication.
- A confident invented figure is the most damaging thing that can go into a published piece: it gets quoted, forwarded, and cited back at you.
- Corollary for audits: an argument is only as strong as its weakest cited number. Offer the *stronger true* version of the claim using verified figures rather than the larger invented one.

## 4. Verify the RENDER, never the status code

**An SPA catch-all answers a missing slug with HTTP 200 and the section hub.** The page looks live, the crawler records success, and the section's own title appears in the body — so a naive text check also passes.

A page-inventory gate that asserts only HTTP 200 cannot see this failure class at all. A PASS from such a gate is not a content check.

### Verification sequence

1. **Render and read the text.** Assert on an article body marker (`.cover`, `article` class, the headline) AND assert the hub marker is *absent* (`"N articles · updated"`). Checking for the title alone is not enough — the hub also lists article titles.
2. **Is the served bundle the one you built?**
   ```bash
   curl -s "$URL" | grep -o 'assets/index-[A-Za-z0-9_-]*\.js'   # which bundle is live
   md5sum <live_bundle> /var/www/html/<site>/assets/index-*.js  # built == served?
   ```
   Mismatch = build or sync gap. Match = the page is not being routed at all.
3. **Is the article in the bundle?** `grep -c "<Headline>" <bundle>`. Absent = never compiled in.
4. **Registration parity.** Count source article files and count entries in the generated manifest. **They must match.**

### Root-cause class: the second registration gate

Content can be fully present in the app's module index *and its meta table* while being absent from a **second, generated manifest** (a build-time JSON registry). Route resolution needs the manifest entry; without it the slug never matches and the catch-all serves the hub. One gate satisfied, the other not — and nothing warns you.

- The manifest generator can stop running silently. Check whether the build pipeline actually invokes it, and whether it can even execute against the current runtime. A generator that `require()`s a `.ts` source under a Node ESM runtime fails instantly, and if the build step never calls it, the failure never surfaces.
- A stale manifest explains a *narrow* breakage: articles added after the manifest's last write are unreachable while older ones keep working. That pattern is the tell.
- Also diff the article source's **export shape** against a working sibling. A file that exports a bare `html` binding and then shorthand-references it behaves differently from one exporting a single typed content object; keep the canon shape.

## 5. Pitfalls

- **Do not declare an article broken from one probe.** Confirm the hub-fallback reproducibly, and test a known-good article from a different date as a control. If the control also fails, the deploy is broken — not the article.
- **Never hand-edit the live tree.** Fix source, rebuild, redeploy. `rsync --delete` without an orphan preview destroys anything living only in the deployed tree.
- **Public-surface mutation is a HOLD until the user names it.** Rebuilding and deploying a public site is a different authority class from writing the draft. Draft freely; deploy on instruction.
- **Keep the evidence.** Save the article source, the rendered-page PDF/screenshot, the registration counts and the bundle hashes into one dated evidence directory before reporting.

## 6. Extraction

End user-facing publish work with the one thing they will actually use: a single forwardable sentence. Not a summary of the article, not the headline — the compressed invariant.
