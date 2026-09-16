# Kinship Language + F5 PDF Patterns (2026-08-17)

Two session-anchored patterns extracted from the Nabilah court-case session.
These complement the pitfalls already in `SKILL.md`.

---

## Pattern 1 — Kinship Language Default

**The trap:** Arif talks about named family members (Nabilah, Fattah Nuqman,
others). I default to formal third-person voice — "adik hang", "isteri hang",
"anak hang" — instead of using the actual name + relationship.

**Correction:** Arif said: *"Cakap bahasa melayu. Nabilah tu adik aku."*
I was being overly formal. Penang family context demands direct naming.

**Rule:**

| Context | Use |
|---|---|
| Conversation about a NAMED family member already introduced | Name directly: "Nabilah", not "adik hang" |
| Conversation about a generic role ("a friend", "someone") | Third-person works |
| F5 family privacy still applies | Name + relationship in conversation, redact content details (IC numbers, addresses, intimate case details) |
| User says "[Name] tu [relationship]" after I use formal third-person | Apologize, switch to direct naming immediately, don't keep formal voice as "safer" |

**Output shape for Penang family context:**
```
[Use the person's name directly: "Nabilah", "Fattah Nuqman"]
[Address Arif as the relationship he claimed: "abang dia", "wali dia"]
[BM Penang, no formal voice, no "adik hang" / "isteri hang" pattern]
```

**Regression test:** If any reply to Arif discussing a named family member uses
"adik hang" / "isteri hang" / "ayah hang" / "mak hang" repeatedly instead of
the actual name, the kinship-language reflex fired. Strip formal voice, use
the name.

**Why this is in `response-format-fit` not memory:** This is HOW to talk to
Arif about family, not WHO family members are. The actual names and
relationships are in MEMORY.md lanes (private/nabilah/). The voice rule is
a response-format reflex.

---

## Pattern 2 — F5 Family-PDF Intake (Sensitive Court / Medical / Legal Docs)

**The trap:** Arif drops a PDF that is clearly family-sensitive (court case,
medical report, financial dispute). Default response was "extract then dump
into chat" — leaks family content into a multi-user Telegram context.

**Fix — the F5 chain is non-bypassable:**

1. **Acknowledge + clarify scope** before extracting. Never extract then ask.
   Use a 4-option menu:
   - (a) summary status (dates/milestones/action items) — no defendan name
     or case details
   - (b) procedural facts only — clean summary, no names in chat
   - (c) store in private lane — render nothing to chat
   - (d) discuss generic process — never touch PDF

2. **Default option (3) when unclear:** store in
   `lanes/private/<family-member>/` with `chmod 0600`, delete the cache
   copy, render zero content to chat. F5 privacy > informational utility.

3. **OCR pipeline for image-based PDFs (scans, court documents):**
   ```bash
   pdftoppm -r 220 <pdf> /tmp/<name>_pages/page -png
   for f in /tmp/<name>_pages/page-*.png; do
     tesseract "$f" "/tmp/<name>_txt/${f%.png}" -l eng 2>/dev/null
   done
   ```
   - `pdftotext -layout` first to catch text-layer PDFs; fall back to OCR
     if empty
   - `tesseract -l eng` works for Malay court docs well enough; `-l eng+msa`
     if precision needed

4. **Privacy-aware summary:** extract procedural facts — filing date, claim
   amount, breakdown structure, lawyer name, court division. NEVER render
   to chat: IC numbers, full addresses, defendan names, intimate case
   details, children's full names. The summary should give the advisor
   enough to give advice without exposing the family member's identity to
   anyone who reads the chat later.

5. **F6 dignity check:** if the case involves family trauma (custody,
   divorce, nafkah), lead the summary with "what they want" not "what
   they're claiming" — reframe from adversarial to aspirational.

**Detection checklist — sensitive PDF arrival:**
- Court filing / medical report / financial dispute / family matter?
  → default to F5 lane-store
- Filename hints at family matter ("kes nafkah", "medical report",
  "cerai")? → confirm scope first
- Multi-user chat / group context? → F5 privacy is harder, store + render
  zero
- Arif says "aku nak [advisor] tengok" or "explain kat [family member]"?
  → summary mode, not lane-store

**Why F5 chain is non-bypassable:** Even if Arif says "explain kat abang",
extract procedural facts only — never dump raw PDF text to chat. The
advisor doesn't need the IC number to give good advice.

---

## Pattern 3 — Letter to Family Member (Hawking-Quote-Anchored)

**The signal:** Arif asked for a letter to Nabilah twice in one session.
First version was clean. Second version, after a Hawking quote pivot,
became anchored to the quote — same emotional architecture but explicitly
tied to Hawking's "stars / work / love" frame.

**Letter shape that works:**
1. Acknowledge what the person did, concretely (filing breakdown, RM1,500
   calculation)
2. One line of witness — "abang nampak"
3. Three practical anchors (work / self / connection)
4. Direct offer of presence — "call abang, bukan emergency je"
5. Sign-off with relationship, not name: "Abang sayang hang" or "— Arif"

**Don't add:**
- Motivational cliches
- Religious framing Arif didn't request
- Advice they didn't ask for
- "You can do it" pep-talk

Adults going through hardship don't need cheerleading. They need witness +
practical anchor.

**Detection checklist for "letter to family" requests:**
- Is Arif requesting a letter to a family member going through hardship?
  → Lead with witness + care, no advice column
- Did Arif pivot to a thinker / quote / philosophy in the same session?
  → Anchor the letter to that frame, don't reset emotional context
- Is the letter explicitly requested as "give me one letter"? → Don't ask
  clarifying questions, deliver immediately

A reusable template is in
`decision-advisory/references/letter-to-family-member-template.md`.

---

## Cross-references

- `SKILL.md` — response format detection, mode 1/2/3, hard NO rules
- `decision-advisory/SKILL.md` — how to advise on life decisions
- `decision-advisory/references/letter-to-family-member-template.md` —
  letter scaffolding
- `memory.md` lanes — actual family member names and relationships
  (private, F5-protected)
