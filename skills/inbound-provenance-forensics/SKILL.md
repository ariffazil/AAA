---
name: inbound-provenance-forensics
description: "Use when tracing who a stranger is and how they found you."
version: 1.0.0
owner: HERMES
risk_tier: T1
floor_scope: [F2, F4, F7]
autonomy_tier: T1
capability_tier: fed-reasoning-heavy
ecology_state: WARM
triggers:
  - "how did they find me"
  - "who is this person / company that emailed me"
  - "cold outreach from a lab, vendor, recruiter or journalist"
  - "unsolicited audit offer"
  - "is this outreach automated"
  - "did an agent find my repo"
  - "trace this email back"
metadata:
  hermes:
    related_skills: [vendor-evaluation-intake, audit-ops, person-dossier-from-public-sources, online-vendor-legitimacy-check]
---

# Inbound provenance forensics

**Scope boundary.** This skill answers two questions: *who is the sender* and *how did they find you*.
Whether their report's findings are true is a separate job — reproduce them against live code
(`vendor-evaluation-intake`, `audit-ops`). A clean provenance trail never grades the findings, and a
correct finding never launders an unclear sender.

Automation is the finding. Integrity is graded separately.

## 1. Pull the whole thread yourself, not the pasted summary

The latest message is rarely the story. Fetch the thread, its prior replies and its attachments. Use the
Gmail REST API through the local OAuth token; `format='metadata'` for headers, `format='full'` for bodies,
`messages/<id>/attachments/<attachmentId>` (base64url, pad with `==`) for files. Read every message in the
chain before treating the newest one as news — a follow-up is a cadence step inside an exchange that
already exists.

## 2. Authenticate the sender before reading the content

From the metadata headers read `Authentication-Results`, `Return-Path`, `Received`, `Message-ID`.

- `dkim=pass` + `spf=pass` + `dmarc=pass` with `header.from=<their domain>` → that domain really sent it.
- `dmarc=p=NONE` → the domain publishes no enforcement policy. Pass proves authorship of the domain,
  not that the domain is reputable. Say which of the two you established.
- The `Received` chain names the real relay host and IP. A branded lab mailing through consumer-grade
  relays is a size signal, not a fraud signal.
- Auth absent or failing → every claim in the body is unverified until the entity check passes.

## 3. Triage an unsolicited attachment before reading it

```python
import pymupdf
d = pymupdf.open(path)
d.metadata            # producer, creationDate, modDate
d.embfile_count()     # >0 = embedded files; inspect before opening
[l.get('uri') or l.get('file') for pg in d for l in pg.get_links()]
d.xref_get_keys(d.pdf_catalog())   # look for /JS, /OpenAction, /AA
```

HeadlessChrome or Skia producer plus a `creationDate` minutes before the email `Date` means the document
was assembled at send time by a pipeline. State the mechanism; do not convert it into an accusation.

## 4. Find the beacon string

Ask which of the principal's public strings is unique, then check whether the outreach quotes it.

```bash
gh api -X GET search/repositories -f q='"<exact phrase>" in:description' \
  --jq '.total_count, (.items[] | .full_name)'
```

`total_count: 1` returning the principal's own repo, while the message quotes that same phrase, is
strong evidence of keyword monitoring rather than referral. Confirm the quoted words against
`gh api repos/<owner>/<repo> --jq .description` — outreach often paraphrases punctuation, which is
itself a sign of text processing rather than a human quote.

## 5. Read the repo's own traffic as machine-vs-human evidence

Traffic data is authenticated-only and covers a 14-day window, so capture and date it the day you look.

```bash
gh api repos/<o>/<r>/traffic/clones --jq '.count, .uniques'
gh api repos/<o>/<r>/traffic/views  --jq '.count, .uniques'
gh api repos/<o>/<r>/traffic/popular/paths --jq '.[] | "\(.path) \(.uniques)"'
gh api repos/<o>/<r>/traffic/popular/referrers --jq '.[] | "\(.referrer) \(.uniques)"'
```

- **clones ÷ views** approximates machines ÷ humans. Above roughly 10:1 the discovery is crawler-driven.
  Quote both numbers with the window; neither alone means anything.
- **`popular/paths` naming `/blob/main/CLAUDE.md`, `AGENTS.md`, `SKILL.md`** means agents are reading the
  agent-instruction files. Humans land on the repo root.
- **`referrers`** naming a search engine, subreddit or aggregator identifies the human-facing path. Its
  absence while clones stay high confirms the machine path.

Also check the distribution surfaces a crawler reaches: the package index
(`https://pypi.org/pypi/<pkg>/json` for releases, `https://pypistats.org/api/packages/<pkg>/recent`), the
principal's own blog or Medium posts, and third-party content-farm articles about the project. A
content-farm post still counts as a discovery surface.

## 6. Date the institution, not just the company

Lay every founding stamp on one line:

- Companies House: `/company/<NUMBER>` (incorporation, SIC, status) and `/officers` (legal name, birth
  month/year, appointment date, identity-verification flag). Search by number, not by name.
- `whois <domain>` → Creation Date.
- `gh api users/<org> --jq .created_at`, then `gh api users/<org>/repos` for count, stars and last push.
- `curl -s https://zenodo.org/api/records/<id>` → creators, `publication_date`, license.

A young company with a real methodology is a one-person lab. Report the age as context for an authority
claim; do not report it as fraud.

## 7. Assemble the timeline in one timezone

Convert every stamp before comparing — `+0100` mail headers against `+0800` commit logs is a one-hour
trap that silently invents or destroys a gap. The decisive intervals:

- commit pushed → first cold email (hours = monitoring, not reading),
- attachment `creationDate` → email `Date` (minutes = generated on demand),
- first contact → the free artifact (the funnel's real entry point).

## 8. What the evidence supports

| Supported | Not supported |
|---|---|
| Discovery was automated or keyword-driven | That the sender is dishonest |
| The document was assembled by a pipeline | That the findings are fabricated |
| The lab is young and small | That the work is incompetent |
| The approach is a funnel with a price ladder | That the free contribution was a trap |

A correct negative finding is the cheapest credible opening a stranger can make: praise is discounted,
abuse is ignored, a real defect is not. Treat a correct defect as evidence of *method*, never of
goodwill — and say so when the principal asks whether the sender is trustworthy.

## Pitfalls

- **Do not answer a provenance question with a character judgement.** The principal asked how they found
  him; "he seems legit" is not an answer. Give the mechanism and the dates.
- **Do not quote a traffic number without its window and both counts.** The API returns 14 days and
  expires; a bare clone total is unreproducible by tomorrow.
- **Do not treat `dmarc=pass` as a trust signal.** It authenticates the domain, not the entity.
- **Do not let a headless-generated PDF imply fabrication.** It implies a document pipeline. Those are
  different sentences and only one of them is defensible.
- **Do not skip the earlier messages in a thread.** A "small contribution" email lands very differently
  once you have read the two messages before it.
- **Do not paste the vendor's own marketing into the timeline.** Their site dates are claims; registry,
  WHOIS, GitHub and Zenodo timestamps are evidence.
