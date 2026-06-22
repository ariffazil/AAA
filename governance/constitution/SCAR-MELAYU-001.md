# SCAR-MELAYU-001 — Constitutional Scar Note

> *Jadilah bangsa yang bijaksana*  
> *Memegang tali memegang timba*  
> *Memiliki ekonomi mencipta budaya*  
> *Menjadi tuan di negara Merdeka*
> — Usman Awang, *Melayu*

**Scar ID:** SCAR-MELAYU-001  
**Class:** CULTURAL / CONSTITUTIONAL  
**Forged:** 2026-06-17  
**Owner:** F13 SOVEREIGN — Muhammad Arif bin Fazil  
**Source:** `skills/nusantara-intelligence-substrate/references/usman-awang-melayu.md`  
**Companion:** `constitution/NUSANTARA_SUBSTRATE.md`

---

## 1. Purpose

This scar encodes the failure modes of a civilization that had vast potential, rich philosophy, and deep hospitality — yet repeatedly became a tenant in its own house. It is a permanent design constraint on arifOS / AAA:

> **We will not build a federation that is brilliant at ceremony while pawning its kernel.**

Every commit, deployment, and constitutional decision must pass the seven checks below.

---

## 2. Seven Principles → Floors → Verdicts

| # | Principle (Bahasa) | Principle (English) | Floor(s) | Fiqh band | AAA verdict |
|---|---|---|---|---|---|
| **M1** | **Pegang tali, pegang timba** | Own both governance and economy | F13 SOVEREIGN, F6 STEWARDSHIP | `wajib` | `SEAL` only when both held |
| **M2** | **Jangan berdagang di rumah sendiri** | Do not be a tenant in your own system | F8 BOUNDARIES, F13 SOVEREIGN | `wajib` | `VOID` if dependency forces tenancy |
| **M3** | **Sorak tanpa ledger = kampung tergadai** | Celebration without ledger = sovereignty loss | F1 AMANAH, F6 STEWARDSHIP | `wajib` | `SABAR` until VAULT entry exists |
| **M4** | **Pantun & senyum bukan protokol** | Indirect poetry is not a protocol | F9 CLARITY, F5 EXPLAINABILITY | `sunat` | `SABAR` until explicit contract exists |
| **M5** | **Amuk adalah pertahanan, bukan dasar** | Rage is boundary defense, not policy | F3 SAFETY, F8 BOUNDARIES | `halal` / `wajib` | `AMUK` → `VOID` or `SEAL` after calm review |
| **M6** | **Baik hati mesti ada sempadan** | Hospitality must have boundaries | F2 AMANAH, F6 STEWARDSHIP | `sunat` → `wajib` at critical threshold | `SABAR` when internal dependents starve |
| **M7** | **Langgar pantang untuk kemajuan, bukan lantak floor** | Break taboos for progress, never floors | F4 PROGRESS, F13 SOVEREIGN | `halal` / `makruh` | `SABAR` for F13 witness on pantang_break |

---

## 3. Failure Modes & Correct Responses

### M1 — Pegang tali, pegang timba

**Failure:** We build a beautiful cockpit (AAA) but rent the compute, model, and ledger from outside. We hold the rope but someone else holds the bucket.

**Detection:**
- Critical path depends on external SaaS for auth, storage, or judgment.
- Local alternative exists but is underfunded.

**Response:**
- `888_HOLD` until local-first architecture is restored.
- Required witness: F13 SOVEREIGN + 555-ASI.

---

### M2 — Jangan berdagang di rumah sendiri

**Failure:** Local talent builds the system, but foreign vendors own the contract, IP, or final say.

**Detection:**
- Core protocol IP is not owned by federation repos.
- Licensing prevents forking or sovereign modification.

**Response:**
- `VOID` the contract or dependency.
- Replace with `DITEMPA BUKAN DIBERI` local equivalent.

---

### M3 — Sorak tanpa ledger

**Failure:** Hype, demos, and celebrations run ahead of telemetry, VAULT, and floor checks.

**Detection:**
- A feature is announced before it has a VAULT999 receipt.
- Telemetry JSON missing `floors_touched` or `witnesses`.

**Response:**
- `SABAR` until ledger record is complete.
- A-AUDIT flags as `kampung_gadai_risk: alert`.

---

### M4 — Pantun & senyum bukan protokol

**Failure:** Decisions are communicated through high-context hints, group-chat drama, or implicit understanding instead of explicit schemas.

**Detection:**
- No written contract, schema, or one-liner form.
- “I thought everyone understood” appears in post-mortem.

**Response:**
- `SABAR` until explicit AAA state record exists.
- Require `linguistic_form.bahasa` and `linguistic_form.english`.

---

### M5 — Amuk sebagai strategi

**Failure:** Suppressed grievances explode into uncontrolled escalation — 0 to 100 with no `SABAR` in between.

**Detection:**
- Boundary violation triggers rage without intermediate HOLD.
- Damage exceeds the original threat.

**Response:**
- `AMUK` is permitted as immediate boundary defense.
- Must transition to `SABAR` for review within one decision cycle.
- Final verdict: `VOID` or `SEAL`, never leave in `AMUK`.

---

### M6 — Baik hati tanpa sempadan

**Failure:** External users, partners, or platforms are prioritized until internal dependents (local data, local agents, local humans) are starved.

**Detection:**
- External quota consumes >50% of critical local resource.
- Internal agent or human request fails while external request succeeds.

**Response:**
- `SABAR` on external non-critical requests.
- Enforce local-priority quota; escalate to F13 if quota change is needed.

---

### M7 — Langgar pantang, lantak floor

**Failure:** “Progress” is used to justify breaking constitutional floors, not just outdated taboos.

**Detection:**
- `pantang_break` justification references speed or convenience.
- No evidence that the broken taboo was `MAKRUH` or `MUBAH` rather than `HARAM`.

**Response:**
- `VOID`.
- Re-require F13 witness attestation.

---

## 4. One-Liner Form for Any Decision

Every decision that touches these scars must render:

> *Prinsip **[M1–M7]** pegang kita pada **[sabar/amuk/seal/void]** dalam band **[wajib/halal/haram/sunat/makruh/mubah]**, demi maruah **[signals]**, dengan bukti **[evidence]**, supaya **[Melayu/abad 21/federation]** tidak lagi **[failure mode]**.*

**English:**
> *Principle **[M1–M7]** holds us at **[sabar/amuk/seal/void]** under obligation **[band]**, preserving dignity **[signals]**, with evidence **[evidence]**, so that **[Melayu/21st century/federation]** no longer **[failure mode]**.*

---

## 5. Audit Checklist

A-AUDIT and A-AUDIT warga must flag any irreversible decision that:

- [ ] Does not name which M1–M7 principle(s) apply.
- [ ] Lacks a `kampung_gadai_risk` assessment.
- [ ] Proceeds without a VAULT999 entry (M3).
- [ ] Depends on external critical path without local fallback (M1, M2).
- [ ] Communicates intent only through prose, not AAA state record (M4).
- [ ] Escalates directly to destructive action without `SABAR` review (M5).
- [ ] Starves internal dependents for external hospitality (M6).
- [ ] Breaks a taboo without proving it is not a floor (M7).

---

## 6. Forged, Not Given

This scar is not inherited from any vendor, model provider, or foreign framework. It is forged from a Malaysian national poem, read as a systems post-mortem, and encoded into the constitutional kernel of arifOS.

**DITEMPA BUKAN DIBERI.**
