---
name: venture-positioning-advisory
description: "Use when asked what the principal's project sells."
version: 1.0.0
owner: Hermes (arifOS federation)
risk_tier: low
autonomy_tier: T1
triggers:
  - "how marketable is X"
  - "what am I selling"
  - "what is this worth"
  - "how do I make money from this"
  - "is my repo worth anything"
  - "should I sell this as a product or service"
  - "what should I build next to sell"
  - "how do I become marketable"
tags: [positioning, monetisation, market, offer-design, distribution, pricing, github, governance]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Venture Positioning & Offer Design

For the question "what is this actually worth to someone else, and what exactly am I selling?" —
asked about the principal's own project (kernel, platform, repo, service, or self). The output is
**one offer sentence plus the arithmetic that checks it**, never a menu of five options.

## When to use

- "How marketable is X as of now? And how do I make it marketable if it isn't?"
- "What am I selling — myself, infra, a chatbot, a repo, a runtime?"
- Deciding whether an asset becomes a **service** (sell now), a **product** (sell later), or a
  **portfolio piece** (never sells, opens doors).
- Any question where the honest answer changes what the principal does next quarter.

## Rule 0 — the deliverable is one offer, not a menu

Enumerate the candidate shapes only to kill them. Each shape gets one reason, stated as a
mechanism, then it is off the table. Five live options means the adviser did not decide, and the
principal has to do the collapsing they hired you for.

## Procedure

1. **Inventory before theorising.** Probe what the asset actually is, publicly, before assessing it.
   - `curl -s https://api.github.com/repos/OWNER/REPO` → read `stargazers_count`, `forks_count`,
     `subscribers_count`, `open_issues_count`, `license`, `pushed_at`, `archived`, `homepage`,
     `topics`. **`archived: true` is the first thing to check** — a listed-but-archived repo is a
     shelf pointing at an empty house.
   - `curl -s 'https://api.github.com/users/OWNER/repos?per_page=100'` → the real portfolio, sorted
     by stars, each with an activity stamp.
   - Live surface: `curl -s -o /dev/null -w '%{http_code} %{time_total}s' https://<homepage>`.
   - Registry/distribution: `curl -s 'https://registry.modelcontextprotocol.io/v0/servers?search=<name>'`
     (or the relevant app store/registry) and `curl -s https://pypi.org/pypi/<pkg>/json` for the
     published version and summary.
   - Local reality: commit count, last commit date, file/LOC counts of the repo the claim rests on.
   Record each number **with the observation date**. An undated market number is unusable in the
   next session and unquotable in front of a buyer.
2. **Map the category in the buyer's words.** Search the exact phrases a buyer would type — the
   category noun plus "governance", "kernel", "framework", "platform". For each, name the #1
   result and its scale, probed the same way as step 1 so the comparison is like-for-like.
3. **Name the incumbent and the incumbent's weapon.** Free, permissive licence, and vendor
   distribution beat a better design every time. Say the weapon out loud; it is what the offer has
   to route around.
4. **Kill the shape menu** — one mechanism per shape:
   - *Infra / the VPS*: cost centre, not a product; nobody buys someone's compose files.
   - *Chatbot*: cheapest and most crowded, and it contradicts a governance pitch (a chatbot is the
     ungoverned thing the offer claims to replace).
   - *Repo*: a discovery surface, not revenue — it buys the meeting, not the contract. Say this
     plainly when the principal conflates stars with customers.
   - *Runtime / platform*: the only genuinely product-shaped option, and the one where an unbranded
     entrant loses to the incumbent on distribution. It wins only **loaded with one real use case**.
   - *Self*: today's actual revenue channel — and not a product. A domain expert who can build the
     runtime is rare; that combination is the channel, not the goods.
5. **Find the moat: the domain the incumbent does not have.** Generic governance is being taken by
   the platform vendors. A governance layer wired to a real high-consequence reasoning domain
   (a technical/regulatory field where wrong answers cost money) can sell *provable decisions with
   receipts*; a vendor selling an empty policy toolkit cannot credibly sell that. Write the offer
   sentence around that, not around the feature list.
6. **Price it against the principal's monthly need — this is the step that converts opinion into a
   decision.** Take the monthly income the asset must eventually replace:
   - Service: `need ÷ hourly rate` = hours per month, then ÷ 8 for days per month. Compare against
     available days; the gap is the honest statement about whether the offer can carry them.
   - Product: `need × 12 ÷ seat fee` = seats required. Four-figure seat counts read very differently
     than one consulting week, and saying so is the answer to "is this sellable?".
   - Never quote a market-size figure as evidence for a small entrant's price. Total market,
     funding rounds and platform spend are lookups, not pricing.
7. **Ladder the first 90 days.** One fixed-scope, fixed-price engagement whose output is a decision
   plus an evidence trail plus a replicable kit; then take that exact artefact to named humans
   already in the principal's network (never cold); then, only after one reference customer and an
   explicit licence decision, consider product.

## Pitfalls

- **Never present a licence change as a technical recommendation.** Permissive (Apache/MIT) buys
  adoption; copyleft (AGPL) protects against a larger firm absorbing the work into a paid product.
  Both are legitimate and mutually exclusive. Put it to the principal as one binary and stop — it is
  an authority decision, not an engineering one.
- **Check third-party listings point at a live repo.** Aggregator and directory entries routinely
  survive the repo they were written for; a prospect who follows one lands on a read-only archive.
  Fix the shelf (manifests, registry entry, listing description) in the same pass as the numbers.
- **Do not sell doctrine.** Policy prose and philosophy are saturated in every governance category;
  buyers purchase outcomes, compliance evidence and failure modes. Where proof assets are missing,
  incident post-mortems with receipts are the highest-value content to write — treat that as a
  hypothesis to test with the first audience, not a proven channel.
- **Separate "the market is real" from "this entrant is in it".** A growing category with one
  dominant incumbent and thousands of self-described participants supports the first claim and not
  the second; state which one the evidence covers.
- **Express the answer as something sendable.** Finish by offering to build the artefact the
  principal can actually put in front of a buyer — a one-page offer: scope, price, deliverables,
  who pays. Analysis that ends without it leaves the decision where it started.

## Related

- `internal-holdings-locate` — sweep the local and public surfaces before answering "what do we have".
- `external-technology-evaluation` — the inbound direction (evaluating someone else's tool).
- `human-apps-roadmap-2026` — the ranked application list this offer should be consistent with.
