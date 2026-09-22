---
name: layered-perspective-brief
description: "Use when asked what you/they/the public think of X."
version: 1.0.0
tags: [intelligence, perspective-layers, stakeholder-read, falsifiers, sovereign-read]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Layered Perspective Brief

> **Trigger:** one request asks for the same situation read from several positions at once — what I
> think · what you think I think · what [a group] think · what the public think. Surface forms:
> "use full agentic intelligence state", "what do staff really think", "what does the rakyat think".
> **Not this skill:** a request for what one person feels (`hermes-rasa`), or a PDF deliverable
> (`intelligence-brief-forge`).

## Procedure

1. **Load the domain router and its canon before writing.** Memory is not evidence. Anything that
   could have moved since the canon was written gets fetched this session; anything you carry
   without fetching is named as carried, never presented as current.
2. **Label each layer's evidence class.** Say which figures you verified now and which you are
   holding unverified — and say the second one out loud ("I hold this, I am not weighting it").
   Letting the two mix silently is the failure the whole structure exists to prevent.
3. **Institution layer.** Separate near-term cash from structural trend, then run the **timing
   test**: does the timing of the action contradict the stated cause? An action taken while the
   stated cause is absent (cuts announced while profits are healthy, an asset sold while it
   performs) means the stated cause is not the cause — name the real one and show the timing that
   proves it.
4. **Sovereign layer** ("what do you think I think"). You know him only through what he built.
   Say that. Present the read AS a reading, name a second possible reading and say which you trust
   more, and invite correction. Never a psychological verdict; never "the silence means X".
5. **Group layer.** Refuse one mood. Segment by **mechanism**: who is targeted, who is insulated,
   and which instrument changes individual behaviour. A form, scheme or policy that makes the
   person's answer strategic is a mechanism, not a measurement — read it as one. Name each source's
   bias in a clause (self-selected, advocacy, dated, pre-event).
6. **Public layer.** Say what the public actually sees — usually not the institution but a price, a
   region, an identity. Then give the **transmission channel** from institution to household and
   say which link is doing the damage. That channel, not the headline, is the stake. Note when the
   discourse has gone quiet, and say quiet is not resolved.
7. **Close with falsifiers.** Two to four observable events, outside anyone's control, that would
   break the read. Then at most ONE question, and only if the answer changes what you bring next.

## Pitfalls

- **A group read without a mechanism is a stereotype.** The mechanism is the evidence; sentiment is
  the thing you refuse to assert.
- **Never let a convenient number ride free.** A figure from a weak source that points the way you
  already believe gets named as unverified, not quietly used.
- **Do not close with a menu.** The read is the deliverable; a list of options he must pick from
  hands the work back to him.
- **Check the canon's and router's pointers before trusting them.** A path that has since moved is
  the most expensive kind of stale — it looks like evidence and returns a 404.
- **Do not restate the actor's own framing as your finding.** "Rightsizing", "strategic
  partnership", "for the good of the country" are the actor's words; if you repeat them, mark them
  as the actor's.
- **Do not answer the layer he did not ask about at length.** Four short layers beat one long one
  plus three stubs.

## Output shape

Plain prose, one block per layer, opening with the frame sentence. Tables and bullets only where the
content is genuinely enumerable. The human-facing register, the no-labels rule and the no-receipts
rule belong to `bridge-protocol` — this skill adds layer discipline, not a second output contract.

## Related

- `bridge-protocol` — output contract for anything human-facing.
- `governed-uncertainty` · `hermes-rasa` — the sovereign layer in more depth: ambiguity, witness, modes.
- `intelligence-brief-forge` — the document form of the same ground/synthesis separation, when the
  deliverable is a PDF rather than a reply.
