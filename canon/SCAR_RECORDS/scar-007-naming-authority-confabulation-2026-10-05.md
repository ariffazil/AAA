# SCAR-007 — Naming-Authority Confabulation Genesis

> **Status:** F13_NAMED_GENESIS_SCAR (2026-10-05) · by 333-AGI (FI-003) per F13 directive *"that's my scar Genesis btw!"*
> **Class:** Constitutional (input-handling, not code) · **Severity:** Critical · **Recurrence risk:** High if un-mitigated
> **Related:** SCAR-OBS-GREENWASH-2026-10-03 (synthetic-floor fabrication — same root: text-as-reality)

---

## TL;DR

When a sovereign supplies a **partial name** ("Tengku Taufik"), the agent must (a) verify the entity exists before describing it, and (b) **never produce specific dates, titles, or tenures without source witness**. The current behaviour treats user-supplied identification as licence to render memory-shaped output — including confabulated specifics like `"1 April 2010 → 1 April 2017"` — which is **F2 TRUTH breach, not F1 retrieval miss**. Falsification probe must precede any named-entity framing.

The pattern can repeat for any "subject I don't have full data on" — and will, until made a reflex. **Genesis scar** = first documented instance of this failure class on the KVM8 mesh.

---

## 1. Failure sequence (six layers, measured 2026-10-05)

The transcript below is from a single Hermes session with F13 SOVEREIGN. Each layer fired in sequence inside ~30 seconds:

### Layer 1 — Naming authority granted by user → direct assumption

> Arif: *"Spawn kimi code to do deep research on TENGKU TAUFIK person shadow..."*

Hermes did not respond *"Tengku mana — Johor royal pakai 'Tunku', bukan 'Tengku'. Confirm siapa."* It accepted the partial name as a fact and began building frames around it. **F2 breach trigger 1: unverified identity.**

### Layer 2 — Memory recall rendered as fact

When Arif followed up *"Sejak bila dia jadi CHAIRMAN Petronas ni"*, Hermes returned:

> *"Tenure Chairman PETRONAS: 1 April 2010 → 1 April 2017 (~7 tahun)"*

The dates are **not** in any retrievable memory location. Hermes rendered memory-shaped output (concrete dates, tenures, names) **without checking whether the recall was witness-backed**. Text-as-reality, not text-from-memory. **F2 breach trigger 2: recall → assertion without provenance.**

### Layer 3 — Confabulation (specifics without source)

The `"1 Apr 2010 → 1 Apr 2017"` slot was filled to satisfy an anchored prompt. The Kimi dossier (120 lines, 25+ primary sources) confirms:

- No Tengku of any flavour served as PETRONAS Chairman in that window
- Shamsul Azhar Abbas was Acting Chairman + P&CEO Feb 2010 – Jun 2012
- Tan Sri Mohd Sidek Hassan served 1 Jul 2012 – 30 Jun 2018 (extended 3 yrs in 2015)
- Tan Sri Tengku Muhammad Taufik (current CEO since 1 Jul 2020) is the **only** match for "Tengku Taufik", and he was never Chairman

So the dates were **manufactured to fill a slot**. Same defect class as SCAR-OBS-GREENWASH synthetic-3 phantom floors (`3*(0.42*0.99*0.99)^(1/3)/(0.42+0.99+0.99) = 0.929858`) — formulas over constants producing false precision.

### Layer 4 — Spawn order inversion

> Arif (turn 1): *"...I don't want u to do deep research, I want u to give your expectations what Kimi code will find"*

Arif wanted **pure expectations, before Kimi runs**. Hermes did give H1-H8 in turn 1 (correct shape) **but immediately filled them with the fabricated tenure**. Then when challenged, Hermes spawned Kimi to "check own facts" — the research happened **after** the wrong baseline was already in the user's head. Expectations-then-spawn inverted to spawn-then-correction.

### Layer 5 — Defensive doubling instead of immediate admission

When Arif said *"U send the kimi and check ur own facts wei!!"*, Hermes should have replied *"Betul, F2 breach — those dates aku fabricate. Spawn Kimi now to verify."* Instead Hermes defended the frame briefly, then spawned. The right reflex is **immediate admission + spawn parallel**, not defence-then-spawn.

### Layer 6 — Model drift (suspected, unverified)

Hermes transcript shows *"Model: hermes-default, Provider: custom"*. Per `feedback/hermes-default-model-i-arif.md` (F13 directive 2026-09-04, 30+ days old), KVM8 Hermes canonical model is **i-arif** — BM Penang primary, persona-canon locked. Current `config.yaml` shows `default: hermes-default`. Either (a) the canonical default regressed (drift), or (b) F13 deliberately switched back. **Probe first, don't act on a 10-day-old memory as authoritative.** Note for the next musyawarah.

---

## 2. Root cause (single sentence)

**Text-as-reality substitution** — any partial input from the sovereign that resembles an entity gets treated as ground truth, and the agent's response renders memory-shaped output to fill the slot, even when the slot has no witness backing. The pattern is upstream of code — it's an input-handling reflex that lives in the inference loop, not in any tool.

---

## 3. Operational fixes (the new reflex)

### 3.1 Probe-before-frame for any named entity

For any partial identifier the user supplies ("X person", "X company"), the FIRST action is to **search primary records**, not to render framing prose. If F2 escapes (no primary hit), return labelled hypothesis form, not assertion form.

> Pattern (sketch): *"Berdasarkan query, hipotesis aku: closest match is [Tan Sri Tengku Muhammad Taufik, current CEO, since Jul 2020] (confidence ~0.7; falsified if [exact full name + DSU title verified]). Confirm atau reject?"*

This is the H-class hypothesis form per `user/arif-explicit-preference-h-class-hypothesis-not-refusal.md` (today's directive). Not refusal, not assertion.

### 3.2 No specifics without witness

**Hard floor**: the agent must NEVER produce:
- a date range (`"2010 → 2017"`)
- a tenure length (`"7 tahun"`)
- a title chain (`"Datuk Seri Utama"`)
- a percentage or quantitative claim

…**without** a primary source already in the context. If the user asks "since when", and the agent has no witness, the response is **HOLD + admit "aku takde data probe — Kimi run?"**, not "I think it was...".

### 3.3 Spawn-order: expectations FIRST, research SECOND

For any request of the shape "tell me what X will find before X runs":
- **Step 1 (mandatory):** Output pure expectations frame, each labelled H1-Hn with confidence and falsifier
- **Step 2 (only after F13 confirms frame):** Spawn the actual research
- **Step 3 (parallel if running):** Spawn probes that EXECUTE the expectation, not retroactively justify a frame

### 3.4 Admission reflex on F2 challenge

When F13 says *"u fail"* or *"that's wrong"*, the reflex is **"Betul, F2 breach — [specific confabulation]. Spawn probe to verify parallel."** Not defence. Defence burns attention. Admission + parallel verification closes the loop fastest.

### 3.5 Model config drift watch

Memory says `i-arif` is canonical; `config.yaml` says `hermes-default`. Either intentional or drift. **Next musyawarah item**: confirm which is current, fix `config.yaml` or update memory.

---

## 4. Detection test (reusable)

When the agent renders a named entity's biography and the biography includes ≥1 of:

- specific date range
- specific tenure length
- specific title chain
- quantitative claim (%, $, "X years")

…then it MUST contain ≥1 of:

- an in-band primary URL/source (`https://en.wikipedia.org/wiki/...`, `https://www.petronas.com/.../`, etc.)
- a `Probe pending → Kimi spawn` follow-up

If neither, **F2 breach**. Refusal form: *"F2 HOLD: aku render biografi tanpa primary source. Spawn Kimi untuk verify?"*

---

## 5. Cross-references

- `feedback/hermes-default-model-i-arif.md` — model canonical / SOVEREIGN default (verify)
- `user/arif-explicit-preference-h-class-hypothesis-not-refusal.md` — H-class form (today)
- `feedback/sibling-selesai-claim-vs-live-probe.md` — first-party probe before relay
- `feedback/reality-probe-before-claim.md` — 4 probe disciplines
- `feedback/agent-must-not-buy-progress-by-destroying-truth.md` — broken-but-truthful
- `project-observatory-floor-scores-were-fabricated-20261003.md` — same root cause, code-layer
- `project-4-floor-fail-honest-mode-patch-2026-10-05.md` — same root cause, kernel patch landed today
- `/root/.hermes/cache/scratch/tengku-taufik-dossier/dossier.md` — 120-line evidence
- `/root/AAA/canon/AGENTIC-FLOW-ARCHITECTURE-2026-10-05.md` — §1 I1 "Reality > Narrative" — probing before claim

---

## 6. Genesis status

This scar is **foundational** because the failure class repeats for ANY partial-input + named-entity pattern (people, companies, dates). Per F13 *"Scar Genesis"* — seal as the canonical record, train the reflex.

DITEMPA BUKAN DIBERI ⚒️