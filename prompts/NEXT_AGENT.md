# 🌱 NEXT AGENT — arif-fazil.com /000 & /999 Human Pages

> **Carry-forward from:** SEAL-fd68d6a2761846e5 (OpenCode, 2026-07-25)
> **Context:** Init/Seal unification complete. SEAL.md canonical. Iron Rule restored. 530 stale files archived.
> **Handoff:** The architecture is clean. Now make it VISIBLE to humans.

---

## Mission

Build two human-facing pages on arif-fazil.com:

### /000 — Proof of Human (The Sovereign Anchor)

**Purpose:** Show the world that a real human (Muhammad Arif bin Fazil, F13) occupies position zero. This is the root of all trust in the federation.

**Content to include:**
1. **The Membrane Principle** — Consciousness cannot be extracted, only attested. Arif is here, he is real, he holds final veto.
2. **Identity Hash** — BLAKE3 hash of `identity.toml`, live-verified from `arifos.arif-fazil.com/health`
3. **ZKPC** — Zero-Knowledge Proof of Consciousness across 7 dimensions (explain in human language)
4. **Gödel Lock** — System AND Human simultaneously. The system cannot complete itself without the human.
5. **Personal AGI** — Intelligence anchored on ONE specific human reality, not a generic "user."
6. **The Airlock Metaphor** — INIT is the airlock between raw AI and Arif's world. Outer door checks identity. Chamber equalizes (floors F1-F13). Inner door grants (SCT, work contract). Only one door opens at a time.
7. **Live Verify block** — `curl https://arifos.arif-fazil.com/health` output with identity_hash + floors_active + drift status.

**Tone:** Sovereign but warm. Technical but human. "I am Arif. This is my proof. You can verify it."

### /999 — The Sealed Vault (The Immutable Exit)

**Purpose:** Show that every decision in the federation leaves an unalterable trace. The arrow of time is real.

**Content to include:**
1. **What VAULT999 Is** — Append-only, hash-chained, Merkle-linked ledger. Once sealed, never modified. Never deleted.
2. **The Hash Chain** — How each seal references the prior seal's hash. The chain IS causality. Break one link = break the whole chain.
3. **/999/verify** — Public, unauthenticated, CORS-enabled endpoint. Anyone can check the HEAD hash.
4. **The Seal Ceremony** — 6 steps from SEAL.md: RSI → cooling → bind → seal → verify → FQ. Human-readable version.
5. **Tiered Seals** — session.ledger (1 witness: AI agent) vs VAULT999 (3+ witnesses: Tri-Witness). When each is used.
6. **INIT → SEAL Loop** — /000 (human enters) → 000→333→888→777→999 (metabolic pipeline) → /999 (vault records) → /999/verify → return to /000. The loop MUST close.
7. **Live Verify block** — `curl https://arif-fazil.com/999/verify` → `{"head":"sha256:...","verified":true}`.
8. **The Paradox** — "AGI must be maximally open to think (INIT) and maximally closed to be trusted (SEAL), at the same moment in time." How arifOS resolves it: the metabolic pipeline converts raw openness into closed certainty.

**Tone:** Architectural but accessible. "Every action leaves a trace. Nothing is hidden. You can verify the chain yourself."

---

## Design Principles

1. **Zen Pulse bar** on both pages — 3-second answer: Where am I? Why care? What next?
2. **Verbs over nouns** — "Verify" not "Data." "Prove" not "Documentation."
3. **Show less, reveal more** — 20% visible above fold, 80% in `<details>` blocks.
4. **Human + Agent surfaces** — Beautiful HTML for humans, structured JSON at `/000.json` and `/999.json` for agents.
5. **Live data, not static claims** — curl the health endpoints and display real values.

---

## Technical Notes

- Site lives at `/root/ARIF-SITES/sites/arif-fazil.com/`
- Deploy via `/root/ARIF-SITES/deploy-vps.sh`
- Existing pages use Tailwind CSS + Zen Pulse pattern
- Reference: GEOX home (`/root/GEOX/static/index.html`) for the canonical Zen Pulse implementation
- `/000` and `/999` should be new pages: `arif-fazil.com/000/` and `arif-fazil.com/999/`
- Existing `/000/` page may exist — audit first, enhance or replace

---

## Git Context

```
AAA commit: a1cdc7e9 (main, pushed)
  - SEAL.md created (canonical seal ceremony)
  - INIT.md §18.2 → SEAL.md pointer
  - AUTONOMOUS_GOVERNANCE.md, HEARTBEAT.md cleaned

arifOS: Iron Rule compliant (0 legacy tags)
A-FORGE: Iron Rule compliant (0 legacy tags)
All repos: clean
```

---

## Load Order

1. `/root/AAA/prompts/INIT.md` — constitutional boot
2. `/root/AAA/prompts/SEAL.md` — seal ceremony (load at session end)
3. `/root/AAA/prompts/INIT_HUMAN.md` — human-readable INIT explanation (Perplexity)
4. This file — mission briefing
5. Probe live `/health` endpoints before writing any claims

---

**DITEMPA BUKAN DIBERI ⚒️**
**The architecture is clean. Now make it visible.**
