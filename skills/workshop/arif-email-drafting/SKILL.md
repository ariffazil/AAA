---
name: arif-email-drafting
description: Use when drafting an English email reply for Arif.
---

# Drafting external English email for Arif

Class-level skill for "write the reply to this cold email / external party on my behalf." Distinct from `email-outbound` (sending mechanics) — this is the VOICE and the drafting workflow. Load when Arif pastes an email and says "reply / draft / bagi draft email."

## Voice (always-on)

- **Humble, human, honest — not a coder.** The opening that works: "I'm not a coder. I'm a geologist. I read rocks for a living." Arif wants the recipient to see the human, not the tech. No bravado, no roadmap-speak.
- **Short.** Two or three short paragraphs. Arif pushes back on verbosity every time — "Shorter and human sopan santun."
- **Sopan (well-mannered).** Gracious and restrained, not cold.

## Hard rules (learned from repeated corrections)

1. **NO promises, no future commitments to external parties.** Arif: "Jangan janji." Avoid "I'll contact you", "I'd be glad to speak", "we'll talk when X", "I'll know where to find you" — all of these are soft commitments an external party can hold him to. External parties are treated as guarded: keep the door closed until he is ready. The safe shape is "I'm not ready yet" with no forward commitment.
2. **End with "Terima Kasih, Arif" — no dashes, no animal handle.** Arif rejected "Badgers" and em-dash flourishes: "no dashes", "Badgers x payah letak." Plain sign-off only. (He has flip-flopped on sign-off handles before — default to no handle unless he names one THIS session.)
3. **Do NOT cross-promote unrelated projects.** Don't slip a makcikgpt / other-site link into an email about arifOS. A focused email reads as a conversation; adding another product turns it into marketing and weakens the closing line. Save other projects for a later, established exchange.
4. **Content must be Arif's words or explicitly approved.** Never invent his background or claims; only fill what he typed or confirmed.

## Workflow

1. Draft in plain English, fenced in a ``` code block (one-tap copy), sign-off as above.
2. Show the draft in chat and WAIT. Do not send on "draft".
3. Refine on his corrections (they will come: shorter, no promise, no handle).
4. Send ONLY on an explicit "hantar" / "send". Then report recipient + subject + messageId.

## Pitfalls

- **First-draft over-promise:** the natural draft says "I'd be glad to speak properly" or "when the time is right I'll know where to find you" — Arif reverses these as a promise. Write it closed from the start.
- **Adding a sign-off flourish:** any animal/identity handle is a risk; he has called it "mengada" (affected). Default plain.
- **Cross-promo temptation:** the user may ASK "should I include link X?" — advise no, and explain the email stays powerful because it is focused on one thing.

## Related

- `email-outbound` — the SENDING lane (Brevo / direct Gmail OAuth REST); external/protected, read-only to curation, but authoritative for mechanics.
- `principal-submission-authoring` — forms/letters the principal signs (different audience, different register).
