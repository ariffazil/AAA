---
name: civic-advocacy
description: "Political advocacy communications — open letters to parliament, mailing list compilation, external AI audits, crypto signoff, and delivery via Brevo email API. Class-level skill for Malaysian civic engagement and governance accountability campaigns."
version: 1.0.0
author: hermes-asi
license: MIT
metadata:
  hermes:
    tags: [advocacy, politics, malaysia, parliament, email, civic]
    homepage: null
prerequisites:
  commands: []
---

# Civic Advocacy Communications

Class-level skill for political advocacy campaigns in the Malaysian context. Covers the full lifecycle: research → writing → audit → signoff → delivery.

## Core Workflow

```
Research (data gathering)
    ↓
Writing (tersurat/tersirat technique)
    ↓
External AI Audit (quality gate)
    ↓
Crypto Signoff (SHA-256 hash)
    ↓
Mailing List Compilation (verified emails)
    ↓
Delivery (Brevo API or direct)
```

## Tersurat/Tersirat Technique

**Tersurat** = what is explicitly written (surface layer)
**Tersirat** = what is implicitly understood (deeper layer)

For political writing:
- Explicit layer = corporate governance critique (data, numbers, facts)
- Implicit layer = systemic critique (patterns of exploitation, power dynamics)

Example: "Corak eksploitasi yang berulang" — explicitly about PETRONAS, implicitly about any system where one party extracts while another gives.

**Pitfall:** Direct analogies (e.g., geopolitical comparisons) can backfire. Use structural comparisons instead of literal ones.

## Institutional Narrative Forensics — Dark-Mirror Detection (2026-08-09)

Analyzing institutional communication (PETRONAS rightsizing, corporate releases, CEO statements) for narrative-amplification vs reality-description. Arif's F1 discipline — binding for every analysis:

**The three-layer epistemic ladder (never skip):**
- **[EVIDENCE]** — directly observable: lexical clusters, cross-channel repetition, euphemisms, numbers without context
- **[INTERPRET]** — a reasonable hypothesis (e.g., AI-assisted communication)
- **[UNKNOWN]** — cannot be known from outside (whether AI is actually used; what the boardroom's 555 actually does)

**The fallacies to avoid (Arif corrections, 2026-08-09):**
- ❌ "Communication is very consistent → therefore AI-generated." **Consistency ≠ AI.** Same symptom can come from: centralized comms team, consultant narrative pack, top-down talking points, strict media training, tight comms governance.
- ❌ "Institution has collapsed to 333-only." From public output the defensible claim is: *"public output shows 333 dominance with little visible 555 friction."* You cannot see the boardroom.
- ❌ Hunting the tool ("does the CEO use ChatGPT?") — weak forensic question. Hunt the pattern instead: **where is friction still allowed to live?**

**The measurable signature — cost of variation:** AI doesn't just lower writing cost; it lowers the cost of VARIATION to ~zero. Test the corpus: is it one narrative template with cheap surface variants (core-stable, surface-adaptive)? Measure with a lexical-frequency sweep across channels — the cadence-monitor instrument (`petronas-cadence-monitor-findings.md`) is the tool, not vibe. That is [EVIDENCE], not [INTERPRET].

**What propaganda is now:** not smarter lies — scaled repetition. Broadcast = one message printed a million times; LLM propaganda = a million personalized variants, one per soul. Adaptive beats broadcast because it doesn't look like propaganda — it looks like a personal conversation.

**The strategic frame (what we actually fight):** not AI, not the CEO, not PR — **euphemism**. Every euphemism is the price an institution pays to avoid reality: "rightsizing" exists because "retrenchment" carries implications it cannot face. Each euphemism is a small confession. MakcikGPT's village register is the counter-weapon — plain language has no euphemisms, and translating "rightsizing" → "buang orang" is itself the friction.

**The decisive test (555):** Can the organization produce its best argument against itself? If yes, the system still lives. If no — it has lost the self-correction function, and failure arrives long before the numbers admit it. When internal friction dies, it doesn't disappear — it migrates outside: journalists, MakcikGPT, open letters, citizens who still speak plainly. [DER] That migration is not an attack; it is a transplant of a dead organ.

Full framework + PETRONAS worked example: `references/narrative-forensics-dark-mirror.md`

## External AI Audit

Before publishing any advocacy document:
1. Send to a different AI model (e.g., Gemini) for independent review
2. Request: Strengths, Weaknesses, Missing data, Legal risks, Virality assessment
3. Score the document (1-10)
4. Revise based on findings

**Key learning:** Gemini scored our PETRONAS letter 3.7/10 initially. The Israel analogy was "completely inappropriate" and "destroyed professional tone." We removed it and kept the structural critique.

## Crypto Signoff

Add to PDF documents:
- SHA-256 hash of the document
- Generation timestamp
- Kernel identity (arifOS)
- Agent identity (Hermes ASI)
- Constitutional lane (333-AGI × 777-FORGE × 888-APEX)
- F13 SOVEREIGN reference
- Source repository URL

This provides authenticity verification and tamper detection.

## Mailing List Strategy

### Target Categories (Priority Order):
1. **Direct political contacts** — PAS MPs + Ahmad Zahid Hamidi (UMNO president/DPM, potential next PM) — operator has direct forwarding channels; these are ACTIONABLE, not aspirational. Route open letters here FIRST.
2. **Regulatory Bodies** — SC, BNM, EPF (if relevant)
3. **Parliament Committees** — PAC, relevant select committees
4. **Geographic MPs** — areas directly affected
5. **Opposition** — vocal voices
6. **Media** — journalists, editors, letters sections
7. **Think Tanks** — IDEAS, EMIR Research, Refsa
8. **Subsidiaries** — if relevant to the issue
9. **CC: PMX/Key Ministers** — notification, not primary target

### Email Format Verification:
- Check official websites for email patterns
- Verify MX records if using custom domains
- Use lead generation tools (LeadIQ, RocketReach) for corporate emails

## Brevo Email API

When Himalaya is not installed, use Brevo REST API:
- Auth: `BREVO_API_KEY` from secrets
- Endpoint: `POST https://api.brevo.com/v3/smtp/email`
- Attachment format: `"attachment": [{"name": "file.pdf", "content": "base64content"}]`
- Status 201 = success
- SMTP password ≠ API key — use REST API only

## Pitfalls

1. **Direct name-calling** — "BANGANG" etc. can be libelous. Use structural critique instead.
2. **Geopolitical analogies** — can be inflammatory and destroy credibility. Use metaphors, not direct comparisons.
3. **Ignoring commodity cycles** — attributing all profit drops to leadership ignores market reality. Add peer comparison.
4. **Missing "adab"** — not informing people you're writing about them is rude. Include them in CC or mention them.
5. **Sunday sends** — humans rest on weekends. Schedule for Monday.
6. **Email authentication** — Brevo API key ≠ SMTP password. Use REST API.
7. **Consistency ≠ AI** — never claim "AI-generated" from consistency alone. Stay at [INTERPRET] unless cost-of-variation data (lexical sweep) supports more; list the human alternatives (comms team, consultants, talking points, media training) before any tool-attribution claim.
8. **"Feels AI" rejection** — even formally polished civic letters can be rejected as "feels AI" by F13 (verified 2026-08-12, v5 surat rasmi → v6 surat makcik pivot). When formal polish is rejected as AI-feel, **pivot to full human vulnerability**, not "more human-sounding formal". The fix is LESS formal, MORE vulnerable.
9. **Data-dumping rejection** — civic letters that lead with charts, tables, and statistical analysis are rejected by F13 ("letter no need to be so full with data and numbers"). Lead with ONE killer number, then story. Save visualizations for appendix (LamPIRAN).
10. **Hash chicken-and-egg in self-referential documents** — see "Kleene's fixed-point self-hash workaround" below.

## Marhaen Soul / Makcik Voice — When Tersurat/Tersirat Is Not Enough (v6 Surat Pattern, 2026-08-12)

For civic letters where the goal is to make humans **FEEL** the betrayal rather than **UNDERSTAND** the data. Different from tersurat/tersirat — tersurat/tersirat is structural critique; Marhaen soul is emotional vulnerability.

### When to use
- The audience is the general public, not Parliament only
- The complaint is institutional betrayal, not policy critique
- The writer wants readers to CRY, not analyze
- After an external AI audit, when the document was rejected as "feels AI" or "feels so ai"
- F13 has explicitly asked for "rasa derita manusia" or "human rasa"

### When NOT to use
- The reader is a regulatory body needing facts for decision-making
- The ask is technical (e.g., specific regulatory change)
- F13 has asked for "professional" or "institutional" voice

### The 12-paragraph Marhaen structure (proven v6, 12 Aug 2026)

1. **Introduce the makcik** — specific persona ("Nama saya Makcik. Saya tidak penting."), NOT "saya warganegara yang prihatin"
2. **State WHY writing** — emotional driver ("Saya menulis sebab saya tidak boleh tidur lagi"), NOT "saya menulis untuk menyampaikan kebimbangan"
3. **Specific scene** — physical, sensory, weekly rhythm ("saya isi minyak setiap Khamis, RM30 seminggu")
4. **The pain** — children, family, concrete loss ("anak saya senyap di meja makan malam")
5. **Connect pain to institution** — without attacking character ("PETRONAS ambil peluang anak dia")
6. **Universal paradox** — without naming it ("sikit yang tinggal makin jauh dari kami")
7. **One killer number** — crystal clear, arithmetic verified ("70.5%. Kalau RM100, RM70.50 keluar, RM29.50 tinggal")
8. **Three Kerusi critique** — see below
9. **Single ask in human language** — not legal ("saya mohon dijawab"), not regulatory ("kami menuntut")
10. **Why writing again** — "penat, bukan berani"
11. **Connect to silent majority** — "makcik-makcik lain di pasar, klinik, surau"
12. **Closing for THEIR CHILDREN** — "supaya generasi akan datang tak perlu menulis surat macam ni lagi"

### Voice rules (anti-AI-feel checklist)

- ❌ "Saya menulis dengan rasa rendah hati" → ✅ "Saya menulis sebab saya penat"
- ❌ "Sebagai waganegara yang prihAtin" → ✅ "Nama saya Makcik"
- ❌ "Kami menggesa" → ✅ "Saya mohon dijawab"
- ❌ Big data tables → ✅ One killer number
- ❌ Corporate closing → ✅ "Itu saja. Terima kasih sebab baca surat panjang ni."
- ❌ "kami menuntut penjelasan" → ✅ "siapa yang dia takut sebenarnya? Rakyat, atau pasaran?"
- ❌ Sign with full IC and address → ✅ "Makcik — seorang warganegara Malaysia"
- ❌ Ask in legal precision → ✅ Ask as a tired aunt

### Specific physical scenes that work
- "Saya isi minyak setiap Khamis. RM30 seminggu."
- "Saya berdiri di pam tu, tangan pegang nozzle, dan saya rasa sesuatu — rasa yang berat di dada."
- "Dia balik petang dengan muka yang sama — tapi mata dia sudah berbeza."
- "Kalau saya ada RM100 di poket, dan RM70.50 keluar..."

### Piercing questions (use sparingly)
- "kalau dia ada ibu — apa ibu dia rasa?"
- "apa yang dia nampak apabila dia tengok cermin?"
- "siapa yang dia takut sebenarnya? Rakyat, atau pasaran?"

### Closing pattern (always)
"Saya tidak minta apa-apa untuk diri saya. Saya cuma nak [concrete thing for their children/family]."

## Three Kerusi Critique Structure

When critiquing Malaysian institutional failure (PETRONAS, GLC, etc.), structure around named chairs:

```
For each of three chairs:
  1. NAME (with title)
  2. AMANAH GIVEN — what the position requires
  3. AMANAH DIKHIANATI — how it was violated (with specific verified facts)
```

### Why three (not two, not four)
- Two = polarization (us vs them)
- Three = structural triangulation (system, not persons)
- Four = bureaucratic, loses narrative force

### Don't attack personal character. Attack STRUCTURE.
- ❌ "CEO X is corrupt"
- ✅ "CEO X holds three strategic positions simultaneously — a structural conflict that the MCCG explicitly prohibits"

### F2 TRUTH for each dikhianati claim
- Each claim must cite a public source
- Numbers must be arithmetically verified (32.0/45.4 = 70.48%, round to 70.5%)
- Named individuals only — no vague "leadership"
- If a fact is wrong, the whole chair collapses — verify before printing

### Proven chairs (v5/v6, 12 Aug 2026)
1. **CEO** — Tengku Muhammad Taufik (PETRONAS) — 3 jawatan strategik, F1 sponsorship RM350M, 5,000 pekerja dibuang, PAT halved
2. **Chairman** — Tan Sri Mohd Bakke Salleh — ex-1MDB (redeems him via Claude audit), but current Lembaga fails MCCG separation
3. **Shareholder** — Anwar Ibrahim — sole shareholder as PM+MKN, demanded RM32B dividend despite halved profit

## Iteration Pattern — F13-Driven Format Refinement (v1→v6, 12 Aug 2026)

When F13 rejects an artifact, iterate through formats. Each rejection points to a specific pivot:

| F13 rejection | Pivot to | Avoid |
|---|---|---|
| "feels so ai" | Full human voice (v6 surat makcik) | More human-sounding formal |
| "letter no need to be so full with data and numbers" | One killer number + story | Smaller versions of same data dump |
| "need to portray amanah dikhianati" | Three Kerusi structure | Generic corporate governance critique |
| "I hate these three devils to the core" | Critique STRUCTURE not CHARACTER | Personal attacks |
| "make it rasmi" | Formal surat rasmi format (v5) | Continuing v4 makcik format |
| "feels so ai" again | Full Marhaen soul (v6 makcik) | Trying to "fix" v5 |
| "include visuals" | 5 charts in LAMPIRAN | Charts in body of letter |

### The arc
```
data-heavy → visualizations → formal institutional → full human voice
   v1            v4                v5                  v6 ✓
```

Each version is correct for a different audience. Don't assume one fits all.

## AI Disclosure Pattern — 3-Line Variant (v6)

For surat makcik (full human voice), AI disclosure goes at the END as 3 short lines:

```html
<div class="ai-disclosure">
  <span class="label">NOTA TEKNIKAL</span>
  <p>Surat ini dirangka dengan bantuan sistem agentik arifOS Federation...</p>
  <p>Sistem: https://github.com/arif-fazil/arifos</p>
  <p>Saluran pengesahan: warga@arif-fazil.com</p>
</div>
```

- NOT as a full crypto signoff with SHA-256 hashes and lane certificates
- NOT in the header
- NOT on the cover
- At the END, in 7pt, in grey, AFTER the signature
- Protects the human voice by hiding the technical provenance

For v5 surat rasmi (institutional format), use the FULL crypto signoff from the existing doctrine.

## Kleene's Fixed-Point Self-Hash Workaround (v6)

The existing doctrine says: **NEVER embed hash in PDF** (use attestation ledger instead).

For civic letters where the recipient is EXPECTED to verify, the v6 makcik version embedded the source HTML hash directly in the document with an explicit disclaimer:

```html
Document Hash (SHA-256): [source HTML hash]
PDF render hash differs (Kleene's fixed-point — embedded hash changes
the document, so any self-reference is unprovable).
```

### Why this works for civic letters (but not other documents)
- Recipient sees the hash, knows the institution
- Institution can be verified via github.com/arif-fazil/arifos
- The hash is the FINGERPRINT of intent, not the file
- The attestation ledger still exists at `/root/HERMES/attestation-ledger.jsonl` for the AI's own audit trail

### When to use which
- **Attestation ledger only (no embedded hash)**: Government-facing PDFs, regulatory submissions, anything with strict audit requirements
- **Embedded source HTML hash + explanation**: Civic letters, public-facing artifacts where the recipient needs to see institutional provenance

## Cover Image Pattern for Civic Letters (proven v6)

The makcik hand holding paper with the KILLER NUMBER works:

```
Subject:    elderly hand (no face), golden hour light
Foreground: paper with [KILLER NUMBER] written on it
Midground:  kitchen table (teh tarik, reading glasses)
Background: industrial silhouette (refinery, distant Malaysian flag)
Tone:       warm amber, dignified, NOT dark/moody
Faces:      NONE — protects identity, focuses on object
Number:     MUST be CLEARLY VISIBLE
```

### Generation prompt template
```
"A photorealistic intimate close-up: a weathered Malaysian hand holding
a single sheet of white paper with [NUMBER] figure printed on it,
the paper is creased from being folded many times. The hand rests on
a plain kitchen table. Beside the hand, a half-finished cup of [BEVERAGE]
and reading glasses placed aside. Warm golden afternoon light streams
through a window, casting long shadows. In the soft-focused background
through the window, the silhouette of oil refinery towers with the
Malaysian flag barely visible. The mood is humble, dignified, human.
4K, shallow depth of field, warm tones."
```

### Failed patterns (avoid)
- Mirrored text in oil droplet — reads as rendering error
- Too dark/moody — reads as noir, not civic
- Garbled body text on paper — obvious AI tell
- Visible faces — identity exposure risk

### Use Gemini Pro (gemini-3-pro-image), 1408×768 JPEG
Flash (gemini-2.5-flash-image) is only for speed-critical drafts.

## Output Attestation — Real-World Cryptographic Verification (2026-08-09)

**Problem:** Agent generates PDFs with fabricated SHA-256 hashes embedded in the document. No actual computation happens — the hash is just text.

**Solution:** Separate attestation from the document. The hash lives in a ledger, not in the PDF.

### Scripts

| Script | Path | Purpose |
|---|---|---|
| `output-attest.py` | `/root/HERMES/scripts/output-attest.py` | Compute SHA-256 + record to ledger |
| `output-verify.py` | `/root/HERMES/scripts/output-verify.py` | Verify hash against ledger |
| `check-unattested-outputs.sh` | `/root/.hermes/scripts/check-unattested-outputs.sh` | Cron: scan + auto-attest |
| `output-attest-hook.py` | `/root/HERMES/scripts/output-attest-hook.py` | post_tool_call auto-attest |

### Workflow

```
PDF generated → post_tool_call hook → SHA-256 computed → ledger recorded
                                                          ↓
Cron (every 2h) → scans for unattested PDFs → auto-attests
                                                          ↓
Verify anytime → python3 output-verify.py <file> <hash>
                → VERIFIED or FABRICATED
```

### Attestation Ledger

`/root/HERMES/attestation-ledger.jsonl` — append-only, each entry:
```json
{
  "type": "output_attestation",
  "file_path": "/abs/path/to/file.pdf",
  "sha256": "real_computed_hash...",
  "timestamp": "ISO8601",
  "agent_id": "hermes",
  "verbatim": true
}
```

### Key Rule

**NEVER embed a hash in the PDF itself.** The attestation lives in the ledger. The PDF is just the content. This avoids the chicken-and-egg problem (hash changes when you change the hash).

### Cron Job

```bash
cronjob action=create name=output-attestation-check \
  schedule="every 2h" script=check-unattested-outputs.sh no_agent=true
```

## Mailing List Expansion Pattern (2026-08-09)

**Starting point:** 35 MPs across PAC, Sarawak, Johor, Opposition, Media.

**Expansion strategy:** Add by tier:
1. PAC members (governance oversight)
2. State-specific MPs (oil/gas producing areas)
3. Committee members (energy, natural resources, finance)
4. Opposition leaders (vocal, accountability)
5. Youth/backbenchers (sympathetic to rakyat issues)
6. Media/influencers (amplification)
7. PMX/DPM/Menteri (CC only — notification, not primary target)

**CSV format:** `No,Nama,Kawasan,Parti,Email,Tier,Sebab`

**Tier categories:** PAC-Chairman, PAC-VC, PAC, Sarawak-VIP, Sarawak, Johor, Opposition, Media, PMX, DPM, Menteri, Selangor, Gov-Backbench, Other

**Wikipedia source:** `https://en.wikipedia.org/wiki/Members_of_the_Dewan_Rakyat,_15th_Malaysian_Parliament` — full list of 222 MPs with constituency, party, and coalition.

## References

- `references/malaysia-parliament-emails.md` — verified MP email database
- `references/brevo-api-recipe.md` — email delivery with attachments
- `references/tersurat-tersirat-examples.md` — writing technique examples
- `references/petronas-atlas.md` — organized PETRONAS file structure + link graph
- `references/narrative-forensics-dark-mirror.md` — institutional communication forensics
- **`references/surat-makcik-v6-pattern.md` — Marhaen Soul / Makcik Voice template + 12-paragraph structure + Three Kerusi pattern (proven 12 Aug 2026, load this when F13 asks for "rasa derita manusia" or "feels so ai")**
- **`references/multi-letter-portfolio-pattern.md` — 3-letter portfolio architecture (PAC/PETROS/NAIO), strategic doctrine "Kurangkan siapa jahat", F2 epistemic tags, 5-step manual forge pivot (proven PETRONAS v13.0, 12 Aug 2026 — load when audience spans 3+ institutional surfaces with different decision-rights)**

## Multi-Audience Decision Tree (F13 SOVEREIGN, 2026-08-12)

```
Single institutional audience?
  → YES: One master surat + CC list (default)
  → NO (3+ surfaces, different decision-rights):
    → 3-letter portfolio (A=institutional/B=sovereignty/C=human story)
    → Same identity, same data, calibrated voice per audience
```

## Strategic Doctrine — Sovereign Petitions (F13 SOVEREIGN, 2026-08-12)

> **"Kurangkan 'siapa jahat.' Tingkatkan 'struktur apa yang perlu diaudit.'"**

Binding for ALL civic letters to Malaysian institutional surfaces. PAC investigates structure, not emotion or conspiracy. The audit ask survives even if specific claims are challenged — because the ask is structural, not personal.

**Operational translation:**
- ❌ "Tengku Taufik perasan tak?" → ✅ "Tengku Taufik bawa angka ini ke Lembaga, atau Lembaga tolak angka ini?"
- ❌ "PETRONAS tipu Parlimen" → ✅ "JV didaftar di UK Companies House #17027115 tanpa rekod briefing Parlimen"
- ❌ "PMX tak peduli rakyat" → ✅ "Dividen RM32B dibayar sedangkan RRR 0.3 dan reserve life 9.9 tahun"

## 3-Letter Portfolio Architecture (Quick Reference, PETRONAS v13.0)

When forking into portfolio, the three calibrated voices:

| Letter | Audience | Voice | Anchor | Forbidden |
|--------|----------|-------|--------|-----------|
| **A** | PAC, regulatory body | Tenang, audit-focused | "Saya tidak menulis untuk meminta [penjara/buang kerja/kesimpulan awal]" | Fury, slogans, mak voice, conspiracy |
| **B** | State entity, sovereignty stakeholders | Constitutional witness | "Saya menulis sebagai saksi perlembagaan, bukan sebagai pihak" | CEO blame, rant, mak voice |
| **C** | NAIO, media, public | Human story, REAL WhatsApp mak voice | "Saya tak faham apa yang anak saya buat. Tapi saya nampak dia tak boleh tidur." | RRR/MCCG (institutional), fiksyen mak |

**APEX Letter (Letter A) template — 5 sections, highest defense:**
1. Pengenalan with 3 "I don't ask" disclaimers (penjara/buang kerja/kesimpulan awal)
2. MENGAPA SAYA MENULIS — framing
3. PERMOHONAN PERTAMA/KEDUA/KETIGA/KEEMPAT — audit-scope blocks
4. PENUTUP — balanced outcome framing
5. Signature + arifOS Federation declaration + legal layer (Article 10/8)

Full pattern in `references/multi-letter-portfolio-pattern.md`.
