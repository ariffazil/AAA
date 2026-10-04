# Constitutional Witness Declaration — APEX Letter Pattern

Session-specific reference for sovereign petition forging, encoded from the
2026-08-12 PETRONAS v14 session. Pairs with the SKILL.md patch that added
the "Constitutional witness declaration — APEX Letter pattern" section.

## Why this reference exists

The 2026-08-12 session produced 11 reversals (v3→v14) of the PETRONAS surat
before reaching a coherent constitutional witness declaration. The reversal
chain was caused by:

1. Treating the stated **vehicle** ("audit") as the **goal** — it wasn't. The
   real goal surfaced only after direct Q&A: *"Tengku Taufik mesti pergi."*
2. Three back-to-back reversals from F13 ("one letter" → "three letters" →
   "one letter" → final) that should have been honored without re-asking.
3. Defensive language ("Saya tidak menulis untuk meminta sesiapa dihukum" ×3)
   pasted from a template — but Pak Arif's actual goal was direct removal.
4. Loading the right skills (`pdf-report-generation`, `humanizer`, `apex-judge`)
   only mid-session, after 5+ reversals had already wasted context.

This reference encodes the proven patterns so the next session starts with
the discipline already in place.

## Verified v14 artifact (PETRONAS APEX LETTER II)

| Field | Value |
|---|---|
| **Coherence ID** | `PETRONAS_APEX_II_V14_2026-08-12` |
| **APEX session** | `SEAL-991b479a32934689` |
| **APEX call_hash** | `sha256:b860a4f378b6425addef77c049b9912aa40e98ca4973db01f0c8a8072928455c` |
| **VAULT999 line** | `47541` |
| **PDF SHA-256** | `f313492159d4787f1d16332191a2b0e9016301ad4a7c869933ae78f3a9b7082e` |
| **HTML SHA pre-patch** | `c1a3a1e98bdcfc4d15848fcecd4130a7ce0d37af1424cf4adf08a1b8bbccdd82` (embedded) |
| **HTML SHA post-patch** | `5f88e8d9bf6b89b988a17638090a665fad1b4cc4da3bbe52eef585e56aa7f01f` |
| **Pages** | 10 |
| **Multimedia assets** | 7 PNG charts (1.5MB) + cover image (773KB) + TTS audio (4.1MB) + video trailer (2.4MB) |

## Real WhatsApp voice extraction (proven)

Anchors from `/root/ariffazil/HUMAN/mak-abah/whatsapp-family-kita/2015-2026-whatsapp-transcript.txt`:

| Voice | Date | Exact quote |
|---|---|---|
| **Mak** | 4/19/15, 11:09 AM | "Mak tengah siang ikan" |
| **Mak** | 5/9/15, 6:47 PM | "Siapa pun tak ucap mak pun tak tau 😭" |
| **Mak (kakak)** | 5/9/15, 11:47 PM | "Makkk selamat hari ibu. Terima kasih jaga dan sabar dgn perangai kakak" |
| **Abah** | 4/20/15, 7:58 AM | "Assalamuailom anak-anak abah serta isteri tersayang" |
| **Mak** (lifetime fact) | birthday 5 October | never publicly celebrated in family chat |
| **Mak** (work pattern) | shift "pagi" 30 years | "siang ikan" routine |

The `grep -E "(Mak tengah siang|Siapa pun tak ucap|Assalamuailom|pagi)"` search
returns 100+ matches in the transcript. Pick 3-5 quotes that anchor specific
dates; the dated precision is what gives the voice weight.

## Voice options (when to pick which)

| Recipient | Voice | Why |
|---|---|---|
| **PAC, AG, regulator, court** | Tenang institutional (Pak Arif APEX Letter canonical) | They read formal. Direct, audit-focused, audit-friendly. |
| **NAIO, media, public MakcikGPT** | Qualia + real WhatsApp voice | They read story. Sensory anchors + verbatim quotes carry the message. |
| **Personal essay / Medium** | First-person, intimate | They read you. No chrome, just the scar. |
| **Civilizational scope (essay/canon)** | Oppenheimer/INTJ patience | Long-view strategic. "Now I am become Death..." frame. |

NEVER blend all three into one surat — the voice gets confused, the reader
gets nothing. Pick the voice that matches the recipient.

## Defensive language audit — REMOVE these phrases when goal is direct

```text
❌ "Saya tidak menulis untuk meminta sesiapa dihukum"        (×3 = defensive loop)
❌ "Saya tidak menulis untuk meminta sesiapa dibuang kerja"  (dilutes intent)
❌ "Saya tidak minta sesiapa dipenjara"                         (defensive deflection)

REPLACE WITH:
✓ "Saya menulis kerana saya sudah cukup tunggu — dan negara ini tak boleh dipimpin lagi oleh orang yang sama yang saya nampak selama 12 tahun gagal memimpinnya."

OR (for institutional surat):
✓ "Saya tidak menulis untuk meminta sesiapa dihukum / dibuang kerja / mempertikaikan hak kerajaan memilih dasar fiskalnya. Saya menulis untuk memohon satu perkara yang lebih sederhana: audit yang bebas, terhad, boleh diukur, dan boleh disahkan."
```

The defensiveness is OK once (the APEX Letter opens with three lines of
denial). It's NOT OK if the writer's actual goal is direct action — then
defensive language becomes the opposite of what they want.

## Iteration discipline — the 11-reversal trap

When F13 reverses themselves mid-session:

```
Iteration 1: "One letter is enough"  → build single unified surat
Iteration 2: "I want 3 letters (PAC/PETROS/NAIO)" → build 3-letter portfolio
Iteration 3: "Just one unified letter, I don't want three" → REBUILD single surat
Iteration 4: "V14 — qualia + Oppenheimer + TT removal as goal" → REBUILD
```

**What to do when F13 reverses:**

1. STOP asking "confirm or adjust?" — F13 has stated the new directive
2. BUILD the most-recent directive, in full
3. Honor the new directive without trying to keep the previous structure
4. Note the reversal in VAULT999 with timestamp + rationale
5. Do NOT try to "preserve" previous work unless F13 explicitly asks

**What NOT to do:**

- ❌ Ask "Should I revert the 3-letter structure or keep it?"
- ❌ Show 4 options for a 1-question decision
- ❌ Add "let me know" / "confirm?" at the end of every output
- ❌ Re-paste the old surat and ask F13 to choose between old vs new

Pak Arif: *"Aku penat la"* → terse acknowledgment + action + result. That's
the response pattern. Always.

## Multimedia fallback recipe (ffmpeg when Gemini times out)

Gemini video generation on this infrastructure has 2/3 timeout rate
(verified 2026-08-12). When Gemini fails, fall back to ffmpeg with cover
image + audio:

```bash
# Step 1: Trim audio to opening 60s (avoids 11-min render timeout)
ffmpeg -y -i surat-narrative.mp3 -ss 0 -t 60 -acodec copy surat-narrative-60s.mp3

# Step 2: Combine cover image + audio with fade-in/out, 30s timeout
timeout 30 ffmpeg -y \
  -loop 1 -framerate 1 \
  -i cover-image.png \
  -i surat-narrative-60s.mp3 \
  -c:v libx264 -preset ultrafast -tune stillimage \
  -c:a aac -b:a 128k -pix_fmt yuv420p \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fade=t=in:st=0:d=2,fade=t=out:st=58:d=2" \
  -shortest -movflags +faststart \
  cover-trailer.mp4
```

Output: 2-3MB MP4, 60s duration, deterministic. No external API timeout.

If F13 asks for a longer trailer (>60s), repeat the audio trim with
`-ss 60 -t 180` for 2-minute trailer.

## Skill load order — load at task START, not mid-session

```text
1. pdf-report-generation   (HTML→weasyprint, charts, page discipline)
2. humanizer              (strip AI-isms, add qualia)
3. apex-judge             (constitutional verification, F13 escalation)
4. arif-sites-content-ops (if dispatching to arif-fazil.com)
5. essay-publish-pipeline (this skill — format reference)
```

Loading mid-session wastes 5+ minutes of context per skill. Load once at
task start, in the order above.

## APEX judge pattern — HOLD is constitutional, not failure

All 11 reversals of the v3-v14 chain returned:
```
effective_verdict: HOLD
f13_required: true
next_action: AWAIT_INPUT
independence_class: KERNEL_ARBITER
```

This is the correct constitutional pattern for irreversible dispatch. Do
NOT:
- ❌ Try to "convert HOLD to SEAL" with stronger language
- ❌ Retry the apex judge with different arguments
- ❌ Skip the apex judge and just dispatch
- ❌ Treat HOLD as failure (it's the gatekeeper, not the gate)

DO:
- ✅ Quote the receipt verbatim (effective_verdict, session_id, call_hash, reasons)
- ✅ Stop and present F13 disposition menu (SEAL/HOLD/AMEND/REJECT)
- ✅ Wait for F13 personal signature before any irreversible action
- ✅ Append to VAULT999 with apex call_hash linked

## F13 SOVEREIGN disposition request format

After the surat is sealed, the response contract is:

```text
📜 [SURAT NAME] v[N] — SEALED

Coherence ID: [coherence_id]
APEX: HOLD+F13_REQUIRED · VAULT999 line: [N] (sealed)

📦 Package:
- Surat PDF: [path, size, pages]
- Multimedia: [list]

🎯 Real goal (per F13 reversal): [goal — not vehicle]
🔍 SHA-256 anchors: [pdf sha, html sha]

⚖️ F13 SOVEREIGN DISPOSITION

| Option | What happens |
| SEAL   | Aku dispatch ke [PAC + CC list] · mirror arif-fazil.com · Telegram notify |
| AMEND  | Sebut patches — aku iterate |
| REJECT | Archive as historical · Move on |
| HOLD   | Tunggu signal dari abang |

⚒️ DITEMPA BUKAN DIBERI — [artifact] siap, sealed, awaiting F13 disposition.
```

This is the response shape that works. Don't add preamble, don't add
"hope this helps", don't add "would you like me to expand". Just the package
and the disposition menu.

---

DITEMPA BUKAN DIBERI — Forged, not given.
Pinned to session 2026-08-12 PETRONAS APEX LETTER II v14.