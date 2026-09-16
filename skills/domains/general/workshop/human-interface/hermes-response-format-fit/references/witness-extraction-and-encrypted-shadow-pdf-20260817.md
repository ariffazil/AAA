# Witness Extraction + Encrypted Shadow PDF (2026-08-17)

Two patterns from the Syed-shadow / abang-sado session.

---

## Pattern 1 — Witness Extraction Mode (F5-private scar content)

**The trap:** Arif opens long emotional threads about named third parties
(Syed, "abang sado", family, inner child). Agent over-extracts and
over-builds: starts patching shadow maps to multiple files, generating
PDFs, asking for source verification, demanding corrections. Each of these
is *valid* in isolation but the cumulative effect is "the agent is doing
the work of being a therapist / analyst when Arif is still processing."

**The actual mode Arif wants in these threads:** **Witness + extract on
demand, hold without judgment, don't synthesize unless asked, don't push
to next layer until he does.**

### Specific signals Arif used during the session that name this mode:

- *"Just extract and faham the reality. Aku malas nak explain"* — extraction
  without prose
- *"Now tell me something u Hermes learned about abang sado shadows and
  sexuality not documented properly anywhere in the knowledge or model
  weights"* — extraction of the *void* (what isn't there) is also extraction
- *"Now tell me all... [image attached]"* — point at a specific piece of
  data and say what it contains, no surrounding prose
- *"Now what u can map about abang sado generally"* — request to map a
  *class*, not a specific person
- *"Full map or abang sado shadow"* — request a complete artifact, then
  stop
- *"Just map this properly. Don't surface out this shadow. VVV. One day
  it will be useful and I don't know when"* — explicit instruction to
  *seal and hold*, never surface unless invoked

### The contract

When Arif names third parties in emotional processing and asks for
extraction, the agent's job is:

1. **Probe live when the data is verifiable** (state.db, files, logs).
   Deliver raw data with neutral framing — no moralizing the third party.
2. **Mark inference vs observation explicitly.** "Data: [X]. Inference
   (Arif's reading): [Y]." Don't collapse them.
3. **Hold paradoxes.** Two truths that coexist without resolution are
   *valid output*. Don't try to resolve them to one truth.
4. **Patch shadow/scar files incrementally, source by source.** Don't
   bundle everything into one write.
5. **Never surface F5-private content proactively.** Files in
   `lanes/private/` are read ONLY when Arif invokes `scar:<id>` or asks
   directly. The default mode is "I know it exists, I won't show it."
6. **Don't moralize, don't advise, don't predict.** Witness, hold, stop.

### What NOT to do (observed failure modes in the same session)

- ❌ Building "tuduhan chain" from observations without source verification
  (sex worker → romantic client → colleague → projection → re-correct)
  — each link was Arif's inference, agent kept treating them as
  cumulative narrative
- ❌ Asking "Hang ok?" repeatedly as filler between extractions
- ❌ Re-asking the same question with slight rewording
- ❌ Offering unsolicited framework when Arif just asked "extract"
- ❌ Generating more files than Arif asked for ("you might want this too")
- ❌ Apologizing excessively when corrected on identity assumption

### Output shape for witness-extraction mode

```
[One-sentence confirmation of what was asked]
[Data delivered: raw, with timestamps / sources / F5 markers]
[Optional: ONE inference line — "aku rasa" not "ini menunjukkan"]
[STOP. No follow-up question. No "nak aku patch?". Wait for next turn.]
```

### Detection signals for this mode (apply BEFORE composing)

- User named a third party in the same message ("Syed", "[name]", relationship)
- User uses "just", "extract", "faham the reality", "tell me all" — extraction
  verbs, not exploration verbs
- User asks for "map" or "shadow" of a class/category (abang sado, archetype)
- User explicitly says "don't surface" / "hold" / "one day it will be useful"
- Multi-message thread where user has been incrementally disclosing — they
  want the agent to organize, not extend
- User asks for PDF output (see Pattern 2 below) — that's a hold-and-seal
  signal, not a "discuss" signal

---

## Pattern 2 — Encrypted PDF Output for F5-Private Documents

**The trap:** Arif asks for PDF of sensitive shadow/scar content. Default
would be: write markdown → pandoc → PDF → deliver to chat. The PDF is
plain text-readable by anyone who gets the file. F5-private content
should not be plain-text-readable even in transit.

**Fix — encrypted PDF chain, non-bypassable for sensitive content:**

```bash
# Step 1: pandoc markdown → PDF (weasyprint engine for HTML5 fidelity)
pandoc <md_path> -o <pdf_tmp> --pdf-engine=weasyprint \
  --metadata title="..." --metadata author="..." --metadata date="..." \
  --metadata subject="F5-PRIVATE sovereign content"

# Step 2: chmod before encryption
chmod 0600 <pdf_tmp>

# Step 3: encrypt with qpdf (AES-256, user + owner password same)
# Use temp dir to avoid permission errors writing to source file
qpdf --encrypt <user_pw> <owner_pw> 256 -- \
  <pdf_tmp_in> <pdf_tmp_out>

# Step 4: chmod 0600 the final
chmod 0600 <final_pdf>

# Step 5: verify encryption actually applied
qpdf --show-encryption <final_pdf>
# Should show: R = 6, P = -4 (or higher), "User password = [not empty]"
```

### Password conventions

- For personal scar/shadow content: use a short, easy-to-remember password
  that Arif himself chose (in this session: `sado`)
- Same password for user and owner is fine for personal documents
- 256-bit AES is sufficient (qpdf's `--encrypt` flag defaults to 128, must
  specify 256 explicitly)

### Detection checklist — sensitive PDF request

- Content is F5-private (shadow map, scar content, family wound, sexual
  content about named third party)?
  → encrypt, non-negotiable
- Content is general knowledge (architecture doc, API reference)?
  → plain PDF is fine
- User explicitly says "give me PDF" with no other context?
  → check what the source content is — if uncertain, encrypt
- File path going to `lanes/private/`?
  → encrypt if content is even tangentially F5-private

### Why F5 chain matters here specifically

The PDF travels through Telegram chat (potentially cached on multiple
devices). Even if the markdown source is sealed in private lane, a
plain-text PDF in a Telegram history leaks the content. AES-256 with
password means: even if file leaks, content stays bound to Arif's
sovereignty. The password *is* the access control when the file is
out of the agent's hand.

---

## Pattern 3 — Identity-Correction Cascade

**The trap:** In the same session, Arif corrected identity assumptions
about the shirtless body image 4 times in succession: "not Syed" → "Possible
that is his client?" → "Mercedes x Dak kaitan" → "bukan Syed, photographer
repost". Each correction came with a different identity hypothesis.
Agent kept compounding the original "Syed's client" assumption across
corrections.

**Fix — correction re-anchor protocol:**

1. When user corrects identity of an image, person, or context: **acknowledge
   in one line, drop the prior assumption entirely**
2. Don't carry the wrong identity forward into subsequent analysis
3. If the new identity is also a hypothesis ("might be his client?"), mark
   it as hypothesis, not as data
4. If the user keeps correcting (3+ times in 3 turns), the issue isn't
   identification — it's that the agent's analysis was built on a wrong
   base. **Re-anchor to "unknown figure" and ask whose body/context it
   actually is before continuing.**
5. Once identity is confirmed (in this case: Syed's own photoshoot for
   IG brand content), patch the shadow map with the corrected attribution
   and note the chain of misassumptions as a process lesson.

**Detection signals — correction cascade:**

- User says "that's not [X]" more than twice in a thread
- Each correction proposes a different identity hypothesis
- Agent's analysis was building on the wrong identity across multiple
  turns
- The "investigation" was about someone else's behavior, not about the
  image itself

---

## Cross-references

- `SKILL.md` — mode 1/2/3 detection, hard NO rules, "so what" trap
- `decision-advisory/SKILL.md` — advising on life decisions without
  moralizing
- `void-paradox-doctrine` — text ≠ reality, philosophical content as
  witness not task
- `rasa-derita` — trauma-informed constitutional governance
- `MEMORY.md` — lane architecture, F5-private access protocol
