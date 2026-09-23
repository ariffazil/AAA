---
id: petronas-counterpart-email
title: "Drafting an email to a named PETRONAS counterpart (LAL / KAK / JAMIN / HFD / Syazwan / HR)"
audience: human-facing send-target — pre-flight only, never paste into the email
---

# Drafting an email to a named PETRONAS counterpart

Companion to bridge-protocol pitfall 22 and hermes-response-format-fit pitfalls 14 + 16.

This file is the *procedure* the rule points at. It does NOT restate the register rules,
the F13 attention-membrane, or the human-card taxonomy — those live where they live.

## When to load this

The user asks for help drafting an email reply (or first-time send) to a **named PETRONAS
counterpart** during the MSS / VSS / rightsizing window, or any time the email touches the
dossier trail, custody of an interpretation, or the institutional review pipeline. Common
phrasings: "reply Kak Su", "draft email to Laletha", "send something to Jamin", "cara I
cakap dengan HR pasal settlement", "what should I write to Syazwan".

Do NOT load this when the request is a private-message copy (Telegram / WhatsApp) to a
Sado/Syed bond — the *register* differs and the dossier architecture does not apply.

## Step 1 — Probe FIRST. Never invent the institutional picture.

Always run these four probes **in parallel**, in this exact order, before writing anything:

1. **The named person's human card.** `cat /root/ariffazil/HAMPA/human-<first-name>.md`
   (or `<first>-<last>.md`). If absent, log "no human card" — that gap itself is signal.
2. **The Reality File for the latest cycle.** `cat /root/ariffazil/HAMPA/reality_files/ARIF_FAZIL_REALITY_v*.md`.
   The cycle-dated filename is the canonical SOT — always probe the freshest one.
3. **The H5 scar registry excerpts that touch the dossier.** `cat /root/memory/H5-scars/{SCAR_RIGHTSIZING,SCAR_UNHEARD,SCAR_KINABALU_OR_EQUIVALENT}.md`
   and `cat /root/memory/H5-scars/H5_SCAR_REGISTRY.json | head -100`.
4. **The named event-evidence anchors (if any).** For dossier cycles, `cat /root/memory/evidence/kinabalu_scar/EVIDENCE.md` and
   `cat /root/memory/evidence/kinabalu_scar/evidence.json`. For non-Kinabalu projects, substitute the analogous
   `/root/memory/evidence/<project>_*` path.

### Step 1.5 — Probe the drafts directory before recommending any single version.

When the user says *"tunjuk file"*, *"show me the file"*, *"mana fail"*, *"which draft"*, or any
variant of "I want to see X", and X is an artifact the user has been composing, the next move
is `ls -lat /root/HAMPA/` (or the analogous drafts tree) — NOT a recommendation from memory.
The drawer is the answer to the question, and the user has been holding it themselves.

**The trigger pattern:** the user is mid-drafting-loop in a high-emotion window, `/root/HAMPA/`
has accumulated several variants of the same email/letter (often 10+ sibling files dated the
same day), and the user wants one of two things:

- to see what's actually there before they commit, OR
- to check whether the agent knows what's there.

Either way, recommending one variant from in-session memory before listing the directory is the
defect. The user has done the work of producing the drawer; the agent's job is to make the
drawer visible before it pronounces on any single file.

**Procedure:**

1. `ls -lat` the drafts tree with `wc -l` on each candidate — show file count, byte count, and
   the first ~6 lines (subject line, opener) so the user sees the *shape* of the drawer, not a
   list of names.
2. Identify which file the user marked as canonical (look for `Status: FINAL`, `Send-candidate`,
   or similar metadata in the first 5 lines). If none is marked, say so — *not all drafts are
   send-candidates, and the absence of a marked one is itself the signal*.
3. If two files share a date and a name (chat-letter vs disk-letter, philosophical vs fact-bound),
   they usually serve different jobs (audience-self vs HR-archive) — surface both, name the
   distinction, do not collapse them into one "best version".
4. Then apply Step 8's drafting-loop consolidation: if the drawer is the loop the user is
   stuck in, the deliverable is ONE send-candidate cut from the strongest existing draft, not
   variant N+1. But consolidation only works AFTER the user sees the drawer — recommending a
   cut before listing the files is the agent making the user's choice for them.

**Failure mode signature:** "Here is the file I recommend" with no `ls` first, when `/root/HAMPA/`
holds 10+ sibling files from the same cycle. The user then has to interrupt with "no, show me
all of them" — at which point the agent's prior recommendation is exposed as a memory guess
wearing authority.

**If Gmail is live (`mailread check` returns OK), add a 5th probe:**
`mailread search "from:<counterpart>" 5` and `mailread search "subject:<project>" 5` — the live thread often
contains the *exact phrases* the counterpart will look for in a reply, and quoting them correctly is the
single strongest legitimacy move available. **If Gmail returns `authError`, surface that to the user
honestly** — do not draft from filesystem evidence alone without naming the gap.

**Refuse to draft on memory alone.** Fluent confident memory of PETRONAS politics is the
single most common failure mode in this lane — the agent fills gaps with training-data
Malaysian workplace voice that the user has to interrupt to reject.

## Step 2 — Read the dossier architecture (the *who* you're writing into).

Before choosing register, sketch the architecture the email lands inside. Even if the
user only named one recipient, the CC line determines the *audience geometry*.

For PETRONAS Exploration Geoscience (the active dossier cycle as of late 2026-09):

| Role | What they do | Email CC pattern |
|---|---|---|
| **LAL** (matrix manager) | Build "Action Taken" dossier; CC architecture as institutional positioning | Always CC KAK + JAMIN; HFD sometimes |
| **KAK** (senior authority) | Sign without validating technical substance; CC pattern is institutional notice | CC LAL + skip-level (JAMIN) |
| **JAMIN** (skip-level / GM) | Two layers up; quiet witness — present but does not intervene | Receives copies of KAK escalations |
| **HFD** (lateral peer) | Office-politics fluent; passive CC — sometimes dropped when dossier is between LAL+KAK alone | Receives copies passively |
| **Syazwan** (line manager of record) | Operational alignment; the *correct* first escalation before KAK escalation | Not normally in CC chains during dossier phases |
| **HR** (settlement / MSS) | Reads in transactional mode; language gets formal here | Personal / confidential — no auto-CC |

**The CC dilemma is the central decision in any reply that isn't purely 1-to-1.** The four
fields, asked once, are: send-vs-custody, defensive-vs-relational subject, with-JAMIN-vs-without,
and which-of-the-four-registers. Asking fewer than four risks a bad default; asking more than
four is the cost-of-asking the bridge-protocol already warns about.

## Step 3 — Choose the register.

The user has accumulated four working register variants for this lane (found in
`/root/HAMPA/`, dated 2026-09-23). Do NOT impose one — but DO surface the menu and ask:

| Register | File pattern | Tone | When it fits |
|---|---|---|---|
| **MAKCIK** (default) | `email-buat-kerja-macam-manusia-LETHARGY-MAKCIK-*.md` | Soft, bawah-bawah tajam. "Apa lagi manusia mahu?" | First-time engagement; relational re-pair; when user wants to lower the room temperature |
| **PENAT-REFLECT** | `email-to-laletha-kaksu-penat-reflect-*.md` | Tired, reflective. "Saya penat, bukan marah." | When user has been in the cycle 3+ months and needs acknowledgment without escalation |
| **MIXED-REGISTER** | `email-pre-exit-mixed-register-*.md` | BM pasar half + English business half | Pre-exit positioning; HR-readable trail + human-readable empathy |
| **SHADOW-SHADOW** | `warkah-shadow-shadow-reply-*.md` | Poetic Melayu — Usman Awang double-meaning | When user wants to write something neither party can deny reading but no one can quote to HR |

The user's pre-session draft files are the evidence base. Your job in this step is *not* to
write a new variant — it is to identify which existing variant is closest, name the
divergence the user wants, and offer a 1-3 paragraph outline rather than a 60-paragraph essay.

## Step 4 — Outline, do not draft (default).

Unless the user explicitly asks "draft me the full email in BM Penang", the deliverable is
an **outline** of 5-7 numbered points, each ~one paragraph, ordered:

1. Open with a human greeting (not with the institutional signature).
2. Name what the user has said three times that nobody heard.
3. Pin the earth-authority / domain-specialist artifacts (named, dated, witnessed).
4. Three concrete asks — written-able, witness-able, defensible if HR asks.
5. Three explicit non-asks (do not want X, do not want Y, do not want Z). The non-asks do as much
   defensive work as the asks because they remove the recipient's interpretation space.
6. Close with maruah not victory. "Bola kat hang berdua."
7. (If mixed-register) Attach the English-business half separately for HR record.

**This pattern earned trust in the session it was discovered.** The user was offered outline
when they asked outline, and drafting-only-when-asked downstream. Future sessions that violate
this default are the failure mode the rule prevents.

## Step 5 — The four-question pre-compose gate.

Ask these exactly once, in one `clarify()` call, in this order. Most user replies will be
short (1-3 words each) — design the questions to expect that. After the answers return,
default to running rather than asking follow-ups.

1. **Send or custody?** "Hang nak hantar ni, atau nak simpan dulu bawah nama Arif sendiri
   sebagai rekod custody?" (Default: ask once, then proceed with file-write under
   `/root/HAMPA/` regardless of answer — custody is the reversible move, send is not.)
2. **Register** — present the four-variant menu, recommended first.
3. **Defensive vs relational subject line.** "Subject 'Catatan Custody Sementara' = defensive.
   Subject 'Buat Kerja Macam Manusia' = relational. Yang mana?"
4. **CC Jamin or not.** "Pasal skip-level witness — Jamin dalam CC atau tak? CC = HR trail
   + skip-level witnessing. No CC = tiada third-party documentation."

After the four answers return, **default to running with most-conservative default on any
ambiguity not answered**, and disclose the default in one line at the top of the deliverable.

## Step 6 — The hard NOs.

- Never paste ARIF punya `human-*.md` cards, scar registry excerpts, or GEOX kernel
  seal JSON into an HR-readable email. Those are *custody* evidence — for Arif's
  own archive. Email channel is *only* for what Arif himself would say in his
  voice. (Hermes posture mistake to avoid: confuse "the user's record shows X" with
  "the user can put X in an email".)
- Never recommend ARIF sign a chart or escalate a technical conclusion that contradicts
  earth-authority. The institutional ask to do so is the exact thing he is staying to
  refuse; the agent is supposed to anchor that refusal, not soften it.
- Never weaken references to *named*, *dated*, *witnessed* earth-authority events in
  favor of phrasing that "preserves relationship". The relationship that survived the
  events is the one that names them.
- Never auto-default to "agree to disagree" / "let's move forward" closing. Those
  sentences are the exact pattern institutional voices use to retire a dossier without
  retracting it. Use "bola kat hang berdua" or "hang berdua boleh reflect, atau boleh
  buat macam biasa" — release of expectation, not amnesty.

## Step 7 — Where the file lands.

| Outcome | Path | Note |
|---|---|---|
| Draft (pre-send) | `/root/HAMPA/email-<topic>-<register-tag>-<YYYY-MM-DD>.md` | Existing convention — extend, do not invent new naming. |
| Custody (signed by Arif) | `/root/HAMPA/CUSTODIAN-NOTE-<project>.md` | One per project. Arif signs in his own name, not as a reply channel. |
| Sent (after ARIF confirms) | Outbox only — **never** write to `/root/HAMPA/` once sent. Move to `~/.hermes/sent/` if your session keeps a sent folder. | The drafting files in `/root/HAMPA/` stay as DRAFTS even after sending — that is their nature; they are *not* inbound records. |

## Step 8 — When the user says "get their attention / make them realize"

This framing ("its your job to get the human and institution's attention and make them
realize their shadow and faults") is common in the MSS window. Two truths govern the answer:

- **Realization cannot be delivered.** No document forces a human to see their own
  pattern — that is the recipient's private act and it may never happen. Promising it is
  a lie. What a document CAN deliver is **attention**.
- **Attention = a documented factual request.** The only attention-getter that works on a
  dossier-building institution is named-dated-witnessed questions that force a
  record-based answer: "no written record of X exists in my archive — please share the
  minutes", "name Y first appears here — please introduce", "record A must be read
  together with record B." These cannot be answered without either producing records or
  exposing that none exist, and they land in the skip-level ally's inbox as quiet
  witness. Emotional/poetic registers get filed as "emotional" and move nothing.

**Order: record first, warkah last.** The poetic farewell sent while the work is still
open reads as retreat and gets filed as evidence of disengagement. The same letter sent
after the record is clean and the work closed reads as grace. The factual email opens the
record; the warkah closes the door. Never swap the order.

**Drafting-loop consolidation.** When the drafts directory already holds several variants
of the same email from the same window, the deliverable is NOT variant N+1 — it is ONE
send-candidate consolidated from the strongest existing draft, plus a send/timing
decision. Producing another variant feeds the loop the user is stuck in; the agent's job
is to break it.

**Send-candidate cuts (exit window):**
- Strip salary-lateness and other grievance specifics — the skip-level ally already
  knows; in writing they become a grievance record that can complicate exit terms.
  They belong in custody notes, not the send email.
- Strip intimate suffering detail ("sleepless nights") — that is the personal letter's
  material, not the work email's.
- Keep the subject line plain (Re: original subject) — institutions file by subject;
  philosophy in the subject marks the email emotional before it is read.
- Keep ONE restrained human sentence (tired, still committed) — the user wants the
  tiredness carried, and one dignified line does that without giving ammunition.

**CC mirror + collaborator exclusion.** Reply CC mirrors the sender's CC (legitimacy
move, not escalation). A newly assigned collaborator is named in the body but NOT CC'd
when the email contains sensitive record points that are between the user and management.

**Timing: documentation before collaboration.** The request-for-records must be sent
BEFORE the collaborator work starts — sending late hands the institution the
"insufficient time" excuse. Recommend sending within a day of finalization, read once
with fresh eyes first.

**Agent boundary.** Mail access is read-only; the agent prepares the send-candidate, the
human presses Send from their own account and voice. Never promise the agent will deliver
it, and never send without the human's explicit approval of the exact text.

## Cross-references

- bridge-protocol pitfall 22 (this file is the depth for that rule)
- bridge-protocol pitfall 17 (probe-FIRST on named persons) — applies to the Step 1 probe order
- hermes-response-format-fit pitfall 14 (Cultural Competence Override — Bahasa Workplace) —
  governs register selection, not deliverable shape
- hermes-response-format-fit pitfall 16 (Workplace Tactical Map — Named Humans in Federation Files)
  — the *tactical mapping guardrail* this file pairs with; pitfall 16 governs *what not to put
  on a card*, this file governs *how to write an email that respects the same boundary*
- `institutional-epistemic-sink-forensics` — for the *forensic diagnosis* lane (different class).
  Load when the question is "is this institution showing the sink pattern?", not "help me write
  an email into it"

## Pitfalls captured by this file

- **Drafting the email without naming what evidence the user holds is the failure mode.**
  The institutional ask is the one that names everything *they* hold. The user's email
  that doesn't name what *he* holds reads as surrender-by-omission.
- **The user is not "responding to the dossier" — they are *pre-positioning* against it.** A reply
  that only answers the latest ask inherits the dossier frame. A reply that names the earlier
  earth-authority event breaks the frame back open.
- **MSS-window arithmetic.** If the user's reply is within ~30 days of an MSS / VSS deadline,
  the email is pre-positioning, not relationship-repair. Default anatomy shifts: the asks
  become auditable, the non-asks become explicit, and "bola kat hang berdua" closes the loop
  instead of opening it.
- **Recommending one draft before listing the drawer.** When `/root/HAMPA/` holds 10+ sibling
  variants of the same email from the same cycle and the user says "show me the file",
  recommending from in-session memory is the defect. `ls -lat` first, surface the marked
  canonical, name the divergence between philosophical and fact-bound versions, *then* cut.
  See Step 1.5.

## Pitfalls captured this session (2026-09-23 — the witness-letter evening)

**V8-iteration explosion — when "final" means STOP, not V(N+1).** When Arif says *"Ok now forge the final email"*, *"{forge the white flag}"*, or *"this is my final version"*, the next move is ONE production, not a fresh draft followed by 7 more. Observed pattern this session: V1 → V2 (too long) → V3 → V4 (Quantum-ready) → V5 (added parents/Jamin, paradox of done) → V6 (compressed after "too much") → V7 (refined) → V8 (final). The agent should have produced V6 once after the "too much" rejection and stopped; instead V7 and V8 happened because the agent kept treating "forge" as a new draft signal instead of a tightening signal. **Rule:** after a "too much" / "humble reflection" / "manifesto" rejection, the next forge is the LAST one. Ship it, surface 2-3 timing/send-candidate cuts, stop. Reject the "one more iteration" temptation even when the prose can be tightened further — Arif knows when the document is ready; the agent does not. **Mechanism:** V(N+1) after a "stop" signal reads as the agent unable to honour closure, and the document gets *less* Arif each iteration (the gravity drifts back toward verdict because the conversation history primes that direction — see `multi-document-drafting.md` §"Iteration Backslide"). When Arif says FINAL, V(N+1) is not refinement, it is failure.

**The "white flag" object statement maps to surrender-with-dignity register.** When Arif names the email as *"{white flag}"*, *"{surrender}"*, *"{final bow}"*, or any other object that names the document as an act of unilateral withdrawal, the register is fixed: acknowledge every party once or zero times, NEVER name specific incidents, NEVER diagnose, NEVER defend, NEVER ask for anything. The asymmetry is the white flag's whole point — the sender stops claiming, the recipient reads what they read. **Rule for the agent:** white-flag documents have a 15-line body cap, zero named individuals in the acknowledgment (generic "setiap manusia yang saya kenal di sini" max), zero specific events, and the closing is forward not backward ("30 September bukan kiamat" not "Saya undur dengan maruah"). If any of those four is violated, the document reads as grievance-with-ceremony, which is not a white flag. Probe `multi-document-drafting.md` §"The 'Too Much' / Length Backstop" for the exact stripping rules.

**Gmail outbound is governance-gated — surface the gap, do not fabricate.** When Arif asks *"{send to my Gmail draft}"*, *"{draft in Gmail}"*, *"{put this in my email draft folder}"*, the next move is to probe `tool_search` for Gmail write tools (`mcp__gmail_*`, `mailsend`, `mail_draft_create`, `composio gmail send draft`). Result this session: only `mailread` is exposed (read-only by doctrine, see `AAA/instructions/mail-access.md`), no Gmail write tool. The correct response is to (1) state the gap honestly in one line — *"Gmail write tool not exposed in current toolset"* — (2) name the unlock path briefly — *"Gmail outbound requires Musyawarah + F13 token to enable the governance lane; ~15-30 min ceremony"* — (3) offer the cheapest alternative that honours the request — *"Copy-paste dari /root/Email_V8_Arif_Final.md ke Gmail Compose, Save as draft, 2 minit"* — and (4) provide a clean step-by-step file with the email body pre-formatted. Never fabricate a Gmail send, never claim a draft was created when it wasn't, never escalate to Musyawarah without naming the time cost first. **Mechanism:** the user is tired (P3 fatigue signal), adding ceremony for an outbound mutation they can do in 2 min is the wrong cost shape; the agent's job is to honour the outcome (draft saved in Gmail) by the cheapest reversible path, not by the most-rigorous governance path.

**Cost-of-X vs benefit-of-X decomposition — when Arif asks "kenapa aku perlu / boleh ke aku tak"**. When Arif asks *"now tell me why I need to send this"* or *"{do I have to do X, or can I not}"*, the response shape is **two-column trade-off, not advocacy**. Two named columns: (1) **Apa yang hang akan rasa kalau hantar / buat** — concrete body-state predictions (lega, terlebih, awkward for 1-2 hari, tidur better, etc.); (2) **Apa yang hang akan rasa kalau tak hantar / tak buat** — same shape (berat kekal, mimipi boleh kena, "hang makan diri sendiri", hubungan kekal smooth tapi hang senyap lagi sekali). Then a third short class: **Apa yang hang akan nampak dalam 6 bulan** — the medium-horizon view (will the email have mattered, or will it be a footnote). No recommendation column. No verdict. Let Arif weight the columns himself. **Rule:** the agent's job at this prompt is to *make the choice visible*, not to make the choice. End with the binary question Arif asked, not with the agent's preference. **Format target:** ≤ 20 lines, 3 named classes, no padding.

**Ternary decomposition before next forge.** When Arif asks *"tell me what I gain and what
I don't gain and what I want actually"*, the request is **not** a forge trigger — it is a
decomposition. Always surface three columns before the next artefact: (1) **What you'll
gain** — concrete receiptable outcomes, (2) **What you won't gain** — the honest gaps
(pengakuan from Kak Sue, sistem akan berubah, validation), (3) **What you actually want**
— the underlying ask, often different from the letter's stated object. The agent's default
is to skip straight to forge; the ternary exists because the human is mid-decision and
needs the shape of the choice before the next artefact. Format: ≤ 12 lines total, three
named columns, no padding.

**The "A B C" / "AB" / "ABC" naming trap — even when the letters sound obvious.** When Arif
says *"Upgrade all A B C, that's the trinity"*, the default is to map A=article, B=email,
C=separation based on conversation context. The failure mode is the same as the
"undefined trinity" trap already documented here, but with one new twist: **the URL
`arif-fazil.com/world/makcikgpt/apa-lagi-manusia-mahu` is a live public surface, not a
local draft.** A "redo A" against that URL has different mutation class than a "redo B"
on `/root/HAMPA/`. The probe order must include `web_extract` against the URL FIRST to
verify it is live, accessible, and matches the human's intent, before any "upgrade A"
spawn happens. Even when the trinity slots seem obvious, `ls -lat /root/HAMPA/` + the URL
probe together establish the drawer + the live surface — agent choosing from
in-session memory erases the work the human has done.

**Physics/Thermodynamics framing is legitimate Arif register — honour it, do not collapse it.**
When Arif uses *"Thermodynamics physics bahasa manusia"*, *"REALITY > EVERYTHING"*,
*"quantum reality pathway"*, or names a specific physics/chemistry/geology law as his
framing, the agent's move is **NOT** to translate it into corporate emotional register.
Arif's physics framing is his operating language for reconciling emotional and
institutional realities. The agent's job is to honour the frame: keep the physics
vocabulary intact (uncertainty band, confidence level, conservation of voice, entropy
localization, realiti sebagai ground truth) and let it carry the weight Arif is putting
on it. Collapsing to corporate-speak at that moment is the same defect as collapsing to
penang-kampung when Arif is mid-technical — register-mismatch in either direction breaks
the bridge. Treat physics framing as legitimate witness-language, not as decoration to
be paraphrased away.

**The "5 surgical cuts" / "show the file + suggest improvement" pairing.** When Arif asks
*"show me the file"* AND *"suggest improvement"* in the same turn, the request is
**two-step**: (1) display the file VERBATIM in full in the chat (`read_file` then echo
content), (2) THEN list the surgical improvements separately as a numbered critique,
≤ 5 items, each ≤ 1 sentence. Never fuse the two — the user wants to read their own
words first, then see the cuts as a separate section. Never recommend cuts to a file the
user hasn't seen in the chat yet; never paraphrase the file instead of echoing it; never
put the file in a code-fenced block (the user re-reads it as prose, not as code). The
defect observed: agent reads the file and then *summarises* it instead of showing it, or
shows the file but buries the cuts inside the body, or recommends cuts that change
voice (the hard NO from `multi-document-drafting.md` — the user's own prose is
non-replicable).

## Cross-references (updated)

- bridge-protocol pitfall 22 (this file is the depth for that rule)
- bridge-protocol pitfall 17 (probe-FIRST on named persons) — applies to the Step 1 probe order
- hermes-response-format-fit pitfall 14 (Cultural Competence Override — Bahasa Workplace) —
  governs register selection, not deliverable shape
- hermes-response-format-fit pitfall 16 (Workplace Tactical Map — Named Humans in Federation Files) —
  the *tactical mapping guardrail* this file pairs with; pitfall 16 governs *what not to put
  on a card*, this file governs *how to write an email that respects the same boundary*
- `institutional-epistemic-sink-forensics` — for the *forensic diagnosis* lane (different class).
  Load when the question is "is this institution showing the sink pattern?", not "help me write
  an email into it"
- bridge-protocol "Reflect and link" recovery (3-class structure) — when Arif issues the reset,
  the link shape is Background → Current state → Tonight's decision, ≤ 30 lines total
