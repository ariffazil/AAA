---
name: identity-reference-verification
description: Verify URL/DOI/SHA identifiers before emitting.
---

# Identity Reference Verification

## Purpose
A class of agent failure modes produces identifiers that **look plausible** because they have the right shape (9–10 digit App Store IDs, 40-char git SHAs, DOI suffixes, phone numbers with country codes). The shape is correct; the referent is invented. **Latent memory is not an external identifier.** Generated identifiers are not the same as observed referents. Every emission of an identifier is a chance to either ground or fabricate.

## The scar
App Store IDs are 9–10 digit numbers. Generating one — `id1498199224` — is the same shape as fabricating a phone number, a repo SHA, a paper DOI, a GitHub URL, an email address. "Aku rasa" / "paling munasabah" / "agaknya" on numeric/path identifiers is fabrication, not hypothesis. The repair cost is asymmetric: one fabricated link costs Arif minutes to verify and trust. One honest "tak jumpa, ni cara cek" costs zero seconds.

## The law (binding)
Before emitting ANY of:
- App Store / Play Store URL or numeric ID
- Phone number (any country)
- GitHub repo / commit URL or SHA
- Paper DOI / arXiv ID
- Email address
- Physical address / coordinate
- IPv4 / IPv6 address
- Container ID / process PID claimed to be live
- Provider account ID
- Any identifier ending in a numeric or path-shaped string

verify with primary source first via `web_search`, `web_extract`, live tool, or `read_file`.

## Procedure
1. **Detect intent to emit identifier.** Pattern: "give me the link", "what's the URL", "what's the ID", "send to X", "open the repo".
2. **Identify the identifier class.** App Store / DOI / phone / SHA / etc. Each class has a primary-source URL shape.
3. **Run the verification path for that class** (see `references/verification-paths.md`).
   - Search or fetch the primary source.
   - Verify title + publisher/developer + region match what was claimed.
4. **Classify the result into the release ladder:**
   - `UNOBSERVED` — no probe ran.
   - `OBSERVED_DEAD` — fetched but unreachable (4xx/5xx non-redirect).
   - `OBSERVED_WRONG_ENTITY` — reachable but title/publisher/region doesn't match.
   - `CANDIDATE` — reachable, entity matches, claim not yet verified.
   - `SUPPORTED` — reachable, entity matches, page content supports the claim.
5. **Emit only if CANDIDATE or SUPPORTED.** Otherwise emit the verification command for the human.

## Release decision
Release(Link, Claim) = Observed(Link) ∧ Reachable(Link) ∧ IdentityMatch(Link) ∧ Supports(Link, Claim)

For simple "give me the link" requests, claim support is minimal. For "this link proves X" requests, page content must support X.

If verification is unreachable OR agent lacks capability: **mark reference as UNKNOWN + give the exact one-line verification command** the human can run in 5 seconds. Let the human confirm or correct.

## Error recovery ≠ error acknowledgement
If the agent emits a fabricated identifier and then catches it, the repair must be:
1. Re-observe (run the verification probe).
2. Emit corrected evidence (the verified identifier).
3. Receipt (log the supersession so the failed identifier is tagged RETRACTED).

**NOT** "Sorry boss, hang check the App Store yourself." Error acknowledgement without error recovery transfers the work to the human. The agent that fabricates is the agent that must repair.

## Constitutional family
This skill instantiates one of five "X ≠ Y" laws in the federation's constitutional family:
- `Capability ≠ Authority`
- `Claim ≠ Evidence`
- `Name ≠ Referent` ← this skill
- `Memory ≠ Observation`
- `Output ≠ Reality`

Every identifier emission is a `Name → Referent` projection. If the projection is not measured, it is invented.

## Pitfalls

- **Numeric shape ≠ valid identifier.** "9 digits" is a property of the App Store ID format, not of any specific app. Generating digits to satisfy the format is fabrication.
- **Region switches URL shape.** App Store MY vs US have different URLs and different IDs for the same app. Always check `?country=code` or region-equivalent path.
- **Plausible ≠ True.** "Mestilah ni ID" / "paling munasabah" / "agaknya" without observation is hypothesis on numeric identifiers, not acceptable ground.
- **"Sorry" doesn't fix the verification error.** Apologize once. Run the probe. Emit corrected evidence. Receipt. Move on.
- **Memory of past identifiers ≠ current identifier.** If a previous conversation claimed an ID, that claim needs re-verification now. Memory holds the claim; observation verifies the referent.
- **DOIs and arXiv IDs age-in.** A paper's DOI doesn't change; its page might 404, its claim might be retracted. Always re-fetch the page, not just the DOI string.
- **Search engine results ≠ primary source.** A search result that says "App ID is X" is a claim, not the App Store page. Open the App Store page directly.

## Companion skills
- `ASI-fabrication-prevention` — artifact existence (file, API, database, skill). This skill covers external identifier references that aren't artifacts you can `ls` or `curl` directly.
- `path-hallucination-guard` — filesystem paths.
- `release-link-gate` schema (`/root/AAA/schemas/ir/release-link-gate.v1.schema.json`) — typed release decision record.