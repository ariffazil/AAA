---
name: inbound-mail-verification
description: Use when an email or attachment must be trusted.
tags: [email, authenticity, attachment, vendor, forensics, intake]
capability_tier: fed-agent
---

# Inbound Mail Verification

An email from an outside party is a **carrier**, not a claim. Before its content is judged, decide whether
the carrier can be trusted at all — and keep the carrier verdict and the content verdict separate.

## Use when

- A vendor, auditor, researcher, recruiter or stranger sends findings, an offer, an invoice, or a
  disclosure.
- Arif forwards or pastes a mail whose sender you do not already know.
- Any download, install, payment or reply would follow from the message.

## Procedure

1. **Read the headers, not the signature block.** Pull the message as metadata from the Gmail API
   (`messages.get` with `format='metadata'`) and read `Authentication-Results` (DKIM, SPF and DMARC all
   `pass`), the `DKIM-Signature` `d=` domain, `Return-Path`, and the first `Received` hop.
   All three must pass **and** the signing domain must equal the domain the sender claims to represent:
   a clean pass for a lookalike domain is a forgery with good hygiene. A display name is not an identity —
   read the address.
2. **Check the entity, not the branding.** Company registration number, registered address, and an
   organisation surface whose history is real (GitHub org repos with commits over months, domain age).
   "Exists but one month old" is a real-but-new vendor; say that, rather than implying either legitimacy
   or fraud.
3. **Treat the attachment as executable until proven otherwise.** For PDFs: no JavaScript in the catalog,
   zero embedded files, no `/Launch` actions, and a link list containing only hosts you expected. Producer
   metadata (`HeadlessChrome`, `Skia`, Word) tells you how it was made, not whether it is honest. Extract
   text with a parser and read it; never open it in a viewer first.
4. **Keep the three verdicts separate in the write-up:** (a) is the sender who they say, (b) is the
   content true, (c) is the offer worth anything. Conflating them produces the two classic errors —
   dismissing a real finding because the sender is selling, or trusting a forged mail because it reads
   well.
5. **Hand the content verdict to the skill that owns it.** Defect claims → reproduce before replying
   (`claimed-defect-verification`). Vendor access, quota or beta notice → `provider-notice-triage`. A tool
   or standard offered for adoption → `external-technology-evaluation`.

## Pitfalls

- **Passing DKIM does not mean a human wrote it.** Machine-generated and AI-assisted mail signs
  identically. Authenticity answers *who sent it*, never *whether it is right*.
- **Bulk-mail infrastructure is normal.** A real company can send through a marketing ESP; judge the
  signing domain and the entity, not the SMTP hostname.
- **Do not restate the body back to Arif.** He has read it. The reply carries what the mail does *not*
  say: whether it is real, whether it is true, and what (if anything) he must do.
- **"Self-hosted" in an offer does not mean nothing leaves the machine.** Read what the tool's publisher
  hooks actually transmit before repeating the vendor's locality claim.
