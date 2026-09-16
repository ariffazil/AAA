# Vendor acknowledgment / credit reply — template

Fill the brackets from live probes, then send. Every bracket is a thing you must have verified this session; an unfilled bracket means the claim does not go in.

---

Subject: Re: <finding title>

Hi <researcher first name>,

Confirmed on our side:

- **The finding is valid.** <one or two sentences of mechanism — no exploit detail>. <If there is an accepted residual, name it here and say where it is documented.>
- **Fix shipped.** <repo>@<sha> — <what it changed>. Deployed <and how you know: deployed-vs-source hash match, live endpoint>. <N> paths now route through <guard>; <what the fallback does now>. <Additional commits with one line each.>
- **Credit.** You'll be named as reporter in the commit history and in any advisory. Handle to use: <handle / name>.

On the CVE: we have no CNA, so filing with MITRE directly as the reporter is the right path. Use this message as vendor acknowledgment — we will confirm the finding, the affected surface, and the fixed commit if they ask.

On publication: <green light after the fix / conditions>. Give us a heads-up before it goes up. <What stays out of the write-up: deployment topology, private surfaces, any unfixed detail.>

Thanks again — <one specific, true sentence about the report's quality>.

<Principal name>

---

## Rules bound to this template

- Do not assign a CVSS score, claim an independent audit, or claim a penetration test unless one happened on the record.
- Do not confirm a second-hand finding as yours; "the engineering side stood up the substrate and reproduced it" is the correct attribution when that is what happened.
- Do not promise a disclosure date you cannot control; ask for the heads-up instead.
- Anything the researcher will publish about the principal's organisation gets read twice before it goes out.
