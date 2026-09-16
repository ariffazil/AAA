---
name: responsible-disclosure-handling
description: "Use when an outsider reports a vuln or asks for credit."
version: 1.0.0
tags: [security, disclosure, cve, credit, third-party, endorsement, oss-maintainer, f13]
---

# Responsible Disclosure Handling

Class-level skill. Trigger: an external party reports a vulnerability in the sovereign's software; asks for CVE coordination or attribution; offers or asks for a scan/audit; requests a support letter, endorsement, reference, or introduction; or follows up on any earlier disclosure thread. Also the right skill when the principal forwards a researcher's email and asks "what is this / what do I reply / map the reality".

## The one rule

**Nothing that carries the sovereign's name or changes a third party's real-world standing is ever executed by default.** Two categories go to F13 as a decision, always, no matter how clean the finding is:

1. Anything **signed, sent, or attested in the principal's name** — acknowledgments of a finding, letters of support, endorsements, public statements of responsibility.
2. Anything that moves a **third party's real-world position** — visa petitions, references, job introductions, money, legal exposure.

For those: verify, present the facts and the trade-off, and let the principal decide. Verify-and-surface is the deliverable; execution is not.

## Procedure

1. **Reconstruct the chain of custody before writing anything.** Who is this person, what have we already told them, what was promised, what was sent and when. Outbound mail has no local sent-items ledger — the commitments live in the session transcript. Full recipe: `agent-session-forensics` ("Episode reconstruction"). Never compose a reply to a multi-turn thread without it: the fastest way to look incompetent is to promise again what shipped last week.
2. **Check the reporter's public record.** CVEs credited, advisories, mailing-list posts, IETF drafts, the scanner/tool they maintain, the disclosure path they used each time. Report it as OBS with links, and state the pattern — "every disclosure went through a coordinating channel" is the assessment the principal actually needs. Do this the moment he asks, not after he has to ask twice.
3. **Verify the finding against live source — do not adopt the reporter's narration.** Trace the named function and confirm the mechanism, or say plainly that you could not. A reporter who says "if there is a guard I missed, tell me and I'll drop it" has earned a real trace, not a courtesy confirmation.
4. **Verify the fix is deployed on every layer the researcher will touch.** `git log --oneline -1 <sha>` for each cited commit; `md5sum` the deployed copy against the source repo; `grep -c` the guard's call sites across all fetch paths. Then the distribution layer: the researcher installs the **package**, so probe the published artifact's version and upload time against the fix's commit date, and read the release pipeline's last run. "Fixed" is a claim until the artifact the outsider will actually consume contains it — a repo fix behind a failing publish job still means `pip install` delivers the vulnerable build. **Re-probe this in the same turn you send**, because a release can land while the reply sits in the outbox. Both layers, with commands: `deployment-claim-verification` pitfalls #50 and #59.
5. **Name the residual you accepted.** If a gap remains (a TOCTOU window, a resolution-time check), say so and say where it is documented. A vendor acknowledgment that admits one accepted residual is worth more than one that claims total closure.
6. **Check the disclosure surface**: `SECURITY.md` policy and contact, whether the repo has GitHub security advisories enabled, and whether the project has a CNA. No CNA → the reporter files with MITRE directly and uses the vendor acknowledgment as evidence. See `templates/vendor-acknowledgment.md`.
7. **Agree credit and publication terms before anything goes public.** Ask for the handle/name to credit, put it in the commit history and any advisory, and require a heads-up before publication. Publish-after-fix is the correct default.
8. **Report the state and the open decisions** — chain of events, live state, what is still waiting on him. Not a recommendation dump.

## Reply shape for the principal's "map the reality"

Chain of custody (dated, in order, with what was sent and when) → live state (each claim re-probed now, CONFIRMED/STALE/ABSENT) → the open decisions. Keep the technical detail to what the principal must know to decide; the engineering record already exists.

## Pitfalls

- **Never write technical first person in the principal's voice that he did not verify.** If engineering stood up the substrate and watched the PoC, say that; if nobody did, do not narrate the trace as personal observation. An honest role statement ("I own and govern the project; the engineering side verified this") survives scrutiny — a borrowed "I traced it" does not. This is the failure that turns a clean disclosure into a credibility problem.
- **A third party's pre-written support letter is not consent to send it.** The principal signs and reads it or it does not go. Minimise the draft only with him in the loop, and keep the claims inside what is verifiable: "found a real vulnerability, reported it privately, the finding was valid, the fix shipped" is a fact statement. "Extraordinary ability" is a judgment that is his alone, and USCIS-grade documents outlive the favour.
- **"Check this person first" is a stop-and-probe on the RELATIONSHIP, not a lookup task.** When the principal wants a stranger vetted before he lends his name, the question behind it is *who is this to you, why did he pick you* — answer that, not just the search results. Treat the flag as a gate on the whole flow, not a formality to clear on the way to sending.
- **A public, machine-indexed project attracts these reports continuously.** Discovery comes from registries and package indexes (PyPI, MCP server directories, CT logs), not from fame. Expect a steady inbound stream and treat each as a chain, not an isolated email — check for earlier threads with the same person before replying.
- **Never leak internal topology into a public write-up or scan.** The repository is public; the deployment is not. Hosts, ports, private surfaces, credentials, and unfixed details stay out. Say what the researcher may publish, not just what he may not.
- **Attribution evidence must read to a stranger the way the sentence claims.** An acknowledgment saying "the commit trail shows this was built by agents under my rules" is true for the principal and invisible to the reader — check what an outsider is actually shown: `git log -1 --format='%an <%ae>'` on the fix commits, plus the built package's `Author`/`Maintainer` METADATA. Machine-pseudonym author trailers next to METADATA carrying the principal's name do not communicate the role split at all. Either publish the one-line statement first, or cut the sentence back to what the cited evidence shows. Verify the evidence, then the claim — never the claim alone.
- **Pre-run the scan the researcher is about to run, with the artifact they will scan.** Before agreeing to a third-party scan, look at the published artifact for what an automated scanner will surface — duplicate or deprecated modules, unwired helpers, dead code. Prove a suspect dead by checking for importers (`grep -rn "<symbol>\|<module>" <pkg>`) instead of trusting a `DEPRECATED` header, and have the one-line honest answer ready. Naming your own dead code first is what keeps a courtesy scan from becoming a second disclosure.
- **A vendor statement that is stale on arrival costs what a wrong one costs.** If the reply says "the release is blocked, verify against main" and the pipeline goes green minutes later, the researcher's next probe contradicts the vendor. Check the released state immediately before sending, and when it has moved, send the correction unprompted — a correction in the reporter's favour reads as competence, not as noise.
- **The project's own disclosure surface is part of the deliverable — keep it true.** `SECURITY.md` is what the *next* reporter reads before deciding to trust you, and its gap registry goes stale on the same triggers the reply does. A `No CVE disclosure history / No known CVEs` row is already false the moment the finding is **accepted** — not when a CVE is assigned, not when the fix ships. In the same pass, move `No independent penetration test` off `Open` (a reviewer is now reviewing) while keeping it honest: `In progress`, naming what is still missing. Downgrade, never upgrade — a truth sweep must not become an exercise in claiming a stronger position, and severity stays put unless the underlying fact changed. Provenance matters too: when the fix commits are authored by machine handles and the package metadata carries the principal's name, an outside reader sees pseudonyms; state the role split where it will be read, or cut the sentence back to what the evidence shows.
- **Persist the evidence as you go**: commit SHAs, messageIds, the reply text, the sent attachment's stable path. The next session reconstructs this thread from the transcript — leave it something readable rather than a summary of a summary.

*DITEMPA BUKAN DIBERI*
