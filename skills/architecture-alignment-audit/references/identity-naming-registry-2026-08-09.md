# Identity naming registry (sealed 2026-08-09, commit 085bff2e)

Live SOT: `/root/AAA/docs/IDENTITY_NAMING_REGISTRY.md`

Rule: **External standards may MAP; they do not RENAME the institution.**

## Locked decisions

| Domain | Decision | Wire / field |
|---|---|---|
| Session / action capability | **ACT only** — retire SCT as primary name | `act_v1.*` |
| Agent identity string | Keep `agentId` + `did:web` | cards, registry |
| Human→agent citizen proof | **warga_status / passport** (planned) | not W3C VC brand |
| Multi-hop delegation | **ACT chain / hop receipts** — no HDP/IBCT brand | defer build |
| Workload attestation stack | `arif_init` + ACT + organ Ed25519 keys | no SPIRE organ |

## Translation table (research → ours)

| Gemini / industry term | AAA name | Status |
|---|---|---|
| AIMS (IETF agent identity stack) | Landscape only — "AIMS-like" in prose if needed | Not adopted as name |
| SPIFFE ID / WIMSE URI | `agentId` + `did:web:…` | Already named — no rename |
| SPIRE / X.509-SVID | `arif_init` session mint + organ Ed25519 keys | Map; do not install SPIRE as doctrine |
| WIMSE Proof Token (WPT) | **ACT** (`act_v1.*`) | Already named (was SCT) |
| W3C Verifiable Credential | **warga passport** / `warga_status` | Already planned name |
| DID (W3C) | `did:web:arif-fazil.com` (+ organ DIDs) | Already named |
| HDP (Human Delegation Provenance) | Research alias only | No brand |
| IBCT (Invocation-Bound Capability Token) | **ACT** / future **ACT hop receipt** | No IBCT name |
| Delegation chain | **ACT chain** (multi-hop deferred) | Name reserved, build later |
| VC issuer/holder/verifier | Sovereign (Arif) / agent (holder) / counterparty (verifier) | Roles only, not VC product name |

## What we do NOT create

- No new AAA organ: SPIRE, AIMS server, VC issuer ministry
- No `spiffe://` as directory primary
- No HDP/IBCT identifiers in code until multi-hop is deliberately forged
- No replacement of Ed25519+ACT with X.509-SVID as **doctrine**

## Rename path (docs debt only)

SCT → ACT dies **by use, not by big-bang rewrite**. New docs use ACT / `act_v1.*`; dual-read during transition. When you touch identity docs next, prefer ACT so the dual name fades.

## Why this exists (context)

2026-08-09: Gemini Deep Research delivered a 12-page "Future AAA Agent Architecture" proposal recommending IETF AIMS, IBCT/HDP token replacement, and PEER protocol adoption. Sovereign sealed this registry instead: the research was landscape intelligence, not a rename mandate. Nothing in it earned a new brand.

## Related verified standards (for future Gate-1 claim checks)

- HDP: real — IETF `draft-helixar-hdp-agentic-delegation-01` (Ed25519, signed hop chain — conceptually converges with ACT, hence "research alias" not "replacement")
- AIMS: real — `draft-klrc-aiagent-auth-00` (Mar 2026, SPIFFE+WIMSE+OAuth2 composition); EU AI Act high-risk deadline Aug 2 2026
- x402: real — Coinbase+Cloudflare, May 2025 launch; ~119M Base + 35M Solana tx by Mar 2026 (~154M total — the PDF's "165M" was inflated, "69K agents" unverifiable)
