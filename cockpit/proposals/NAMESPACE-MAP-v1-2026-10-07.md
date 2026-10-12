<!-- PROPOSAL — staged in cockpit/proposals/ — promotion to /root/AAA/canon/ requires F13 SAH -->
<!-- Host gets canon from /root/AAA/canon/ ; this file lives in scratch only -->

# NAMESPACE-MAP-v1.md — "HERMES" Disambiguation

| field | value |
|---|---|
| **status** | `PROPOSAL` — staged in `/root/AAA/cockpit/proposals/`, awaiting F13 review for promotion to `/root/AAA/canon/` |
| **author** | HERMES (audit agent) |
| **date** | 2026-10-07 |
| **draft path** | `/root/.hermes/cache/scratch/draft-namespace-map-v1.md` |
| **intended canon home** | `/root/AAA/canon/NAMESPACE-MAP-v1.md` (on F13 SAH) |
| **kernel provenance** | `arifOS` @ `/root/arifOS`, package `arifos` version `1!2026.10.1`, license `AGPL-3.0-only` |
| **guard** | host read-only to canon; this file is a proposal, not a source of truth |
| **metric** | SemanticOwnerAmbiguity → 0 |

> Write **canonical (alias)**, never alias alone. A bare `HERMES` outside a declared
> coordinate is a naming violation (F10, cf. `namespace-fatwa-k1.md`).

---

## 1 · The problem

`HERMES` is one string bound to four different objects. Spoken alone it is
**ambiguous by default**, and ambiguity at the identity layer is ontology
corruption, not a typo (`CANONICAL_GLOSSARY.md`).

The failure is not "people sometimes confuse names." The failure is that a
correct sentence becomes false when the referent silently changes:

- "Hermes owns the skills directory" — true of **E3**, false of **E2**.
- "Hermes is MIT-licensed" — true of **E2**, false of **E1/E4** (E4 is AGPL-shaded via arifOS; downstream redistribution differs).
- "Restart Hermes to reload the tools" — true of **E4** (a daemon), false of **E1** (weights, un-restartable).
- "Hermes said the claim failed validation" — the claim was adjudicated by **E4**, which runs *inside* an instance hosted by **E2** and *on* a model from **E1**. Four referents, three of them stacked in one act.

Since the four entities *stack* in a single operation, an audit that logs "HERMES"
cannot later separate which layer produced a claim, which layer was mutated, or
which license governs the artifact. That is the defect this map closes.

---

## 2 · The four-entity map

| # | Name | What it is | Path / handle | License / ID |
|---|---|---|---|---|
| **E1** | **Hermes** (Nous model family) | Language-model **weights** — the reasoning substrate. Hermes 3 / Hermes 4 line. Not software, not a running thing. | model handle at inference backend (weights, no path) | Nous Research model card; **weights, not code** |
| **E2** | **Hermes Agent** (Nous software) | The agent **runtime** — CLI, gateway, tool loop, skill loader. Upstream software, vendored into arifOS. | `/usr/local/lib/hermes-agent/` · package `name = "hermes-agent"`, `version = "0.0.0"` | **MIT** (`pyproject.toml`) |
| **E3** | **HERMES** (Arif instance) | The **personal overlay** — this operator's identity, skills, lanes, carry-forward, config. Stateful, private, host-specific. | `/root/.hermes/` (canonical lowercase) · `/root/HERMES` → symlink to `/root/.hermes` | private overlay; no public license; `HERMES_HOME` env root |
| **E4** | **arifOS HERMES MCP** | The **semantic organ layer** — governed intelligence for human meaning / perspective / claims / qualia. A running **daemon**. | module `/root/.hermes/hermes_mcp/` · served `python3 -m hermes_mcp` · handle `hermes-mcp` → `http://127.0.0.1:18087/mcp` · scheme `hermes://` | `AGPL-3.0-only` (via arifOS) |

### E4 canonical tool surface (six — from `hermes_mcp/_canon.py`)

`hermes_claim_validate` · `hermes_perspective_scope` · `hermes_qualia_boundary` ·
`hermes_contradiction_scan` · `hermes_counterstory_test` · `hermes_handoff_package`

> The organ's own design metric is `SemanticOwnerAmbiguity → 0` — an ambiguity
> *resolver* that was itself an ambiguity *source*. This map is that metric applied
> to the organ's own name.

### Adjacent surfaces — named, but NOT part of the four

Probed 2026-10-07; recorded so future readers do not fold them into the map:

| surface | what | path / handle | relation |
|---|---|---|---|
| `hermes-rasa` | second, distinct MCP server (RASA/shadow tools) | stdio `/root/.hermes/mcp/hermes-rasa/server.py` | separate server, **not** the E4 six-tool surface |
| `arifosmcp/tools/hermes.py` | in-kernel diagnostic tools (`hermes_system_status`, `hermes_fact_check`, `hermes_vault_query`, …) | inside `/opt/arifos/current/.../arifosmcp/tools/` | E4-lane names, kernel host — not the organ daemon |
| Azwa Hermes | a **different bot** | (external) | "Do not kill — different bot" (`CANONICAL_GLOSSARY.md`) |
| OpenClaw / IRFANCLAW | execution surface, `@irfanclaw_arifos_bot` | KVM4 `openclaw-gateway` | explicitly **"Not Hermes"** (`AAA/names/OPENCLAW.md`) |
| `1!2026.x` numerals | arifOS epoch versioning | `pyproject.toml` | coordinate system, not identity |

---

## 3 · Naming convention — use this, not that

| Write this | Not this | Why |
|---|---|---|
| `Hermes 3` / `Hermes 4` (Nous model) | `Hermes` alone | pins the **weights** layer; "Hermes" bare cannot tell weights from software |
| `Hermes Agent` · package `hermes-agent` | `Hermes` | pins the **MIT runtime** (E2) |
| `HERMES (instance)` · `HERMES overlay` | `Hermes` / `HERMES` alone | pins the **personal overlay** (E3) |
| `HERMES MCP` · `hermes_mcp` · `arifOS HERMES` | `HERMES` alone | pins the **semantic organ / daemon** (E4) |
| `hermes://` (scheme) | naked `hermes` | E4's internal address space (canon, organs, rrr) |
| path `/root/.hermes/`, alias `/root/HERMES` | `~/.hermes` unqualified | E3 canonical is lowercase; `/root/HERMES` is a symlink, not a second instance |
| handle `hermes-mcp` (port 18087) | `hermes` in config | E4 wiring key in `config.yaml` |
| handle `hermes-rasa` | `hermes` | distinct stdio server — never collapse onto E4 |

### Proposed coordinate marker (mirrors FATWA K1)

To keep prose and logs machine-auditable, qualify the bare token when no context
exists. One form:

```
HERMES:model     → E1
HERMES:agent     → E2
HERMES:instance  → E3
HERMES:mcp       → E4
```

`HERMES` unqualified is legal **only** inside a section that has already declared
its coordinate. Everywhere else it is a violation. (This is the same law as
`888` → must be written `888-APEX`: bare mark, missing coordinate.)

### The one-line fallback

When a downstream audience needs one word, the resolution rule is:

> **default `HERMES` = E3, the instance** — because that is the one the operator
> is talking to. E4 is `HERMES MCP`; E2 is `Hermes Agent`; E1 is the model.
> State the default explicitly so the mapping is not silent.

---

## 4 · Provenance one-liner

> **Built on Nous Research Hermes Agent, with arifOS-specific integrations.**

Expanded provenance receipts (all OBS at probe):

- E2: `/usr/local/lib/hermes-agent/pyproject.toml` → `name = "hermes-agent"`, `version = "0.0.0"`, `license = "MIT"`.
- E3: `/root/.hermes/` present; `/root/HERMES` → `/root/.hermes` (symlink, created 2026-09-04).
- E4: module `/root/.hermes/hermes_mcp/` (`__main__.py` default `http` on `127.0.0.1:18087`); live process `python3 -m hermes_mcp`, cwd `/root/.hermes`.
- E4 canon home: `hermes_mcp/CANON.md` is tagged `NOT_CANONICAL`; canonical stays `/root/AAA/canon/`.
- Kernel: `/root/arifOS/pyproject.toml` → `name = "arifos"`, `version = "1!2026.10.1"`, `license = "AGPL-3.0-only"`.

---

## 5 · Rationale

**5.1 False-claim risk (F2/F9).** The four entities carry *different licenses* and
*different truth obligations*. A verification claim that says "Hermes attests X"
without the coordinate cannot be audited: was X generated by weights (E1, no
git history), by the runtime (E2, upstream code), by the overlay (E3, private
state), or by the organ (E4, receipt-bound)? Collapsing them may attach an
arifOS-AGPL receipt to an MIT-runtime action, or attribute a private-overlay
decision to public upstream code. Both are false claims.

**5.2 Audit cross-input.** Because the layers **stack** in one act (E2 hosts E3,
E3 runs E4, E4 ingests E1 output), any audit log whose actor field is just
"HERMES" merges four consequence-domains into one. Provenance must be *tracked*,
not averaged (APEX Reality Kernel, Prime Invariant 2). The marker in §3 makes the
actor field separable at the moment of writing, not reconstructed later.

**5.3 Probe receipts — the ambiguity already fired.**

| claim source | claim | probe result | class |
|---|---|---|---|
| prior session (2026-10-07 ~15:48) | E4 daemon = `mcp_server.py` **pid 338427** | pid 338427 cwd = `/root/chron` — it is the **chron** MCP, not HERMES | **CONTESTED → corrected** |
| this session (2026-10-07) | live E4 daemon | `python3 -m hermes_mcp`, cwd `/root/.hermes` | OBS |
| `AAA/names/OPENCLAW.md` comment | NAMING DECREE v2 2026-09-25 | text reads *"agent name IRFANCLAW; runtime HERMES ialah KVM8, bukan ini"* | REPORTED (source unclear) |

> The pid in the prior probe did not resolve to HERMES. A bare "HERMES pid" recorded
> into an audit trail would have pointed a future operator at the **chron** organ.
> That is exactly the class of error this map exists to prevent.

**5.4 Floor.** `CAR(NAMES.md) §4` test: with this map, a reader with no context can,
in under one minute, tell the four apart from one line of prose. That is the
acceptance bar. If a future reader still cannot, this file has failed and must be
compressed.

---

## 6 · Open questions for F13

These are **constitutional** (identity/direction-of-record) and are staged as a
binary, per the attention membrane. Not resolvable by the agent from evidence alone.

**Q1 — Is the "irfanclaw → HERMES" rename on 2026-09-25 verified?**
Evidence is contradictory and I will not smooth it:

- The direction *"irfanclaw → HERMES"* implies the agent formerly named IRFANCLAW
  became HERMES.
- The only artifact found (`/root/AAA/names/OPENCLAW.md`, comment dated 2026-09-25)
  reads the **opposite** way: *agent name = IRFANCLAW; runtime HERMES = KVM8; OpenClaw
  is **not** Hermes.* It names IRFANCLAW as the agent and HERMES as the runtime host.
- No "NAMING DECREE v2 (2026-09-25)" document was located as a standalone canon —
  the date survives only in that comment.

**Ask (binary):** is the 2026-09-25 decree `(a)` *IRFANCLAW → HERMES* (agent renamed
to HERMES), or `(b)` *agent = IRFANCLAW, HERMES = the KVM8 runtime* — i.e. the
`OPENCLAW.md` reading? One word: `a` or `b`. If `a`, §2 E3/E4 absorb the IRFANCLAW
lineage and this map must say so; if `b`, `OPENCLAW.md` is correct and the phrase
"irfanclaw → HERMES" is retired as a misreading.

**Q2 — External-audience policy: what do we say?**
When the audience is outside the federation (blog, third party, another org),
which form is the standing answer?

- `(a)` **Collapse upward**: always "Nous Research Hermes Agent" and drop the
  internal four-way split (simplest; risks under-declaring arifOS layering).
- `(b)` **Provenance one-liner**: §4 verbatim — "Built on Nous Research Hermes Agent,
  with arifOS-specific integrations."
- `(c)` **Full four-entity disclosure** on any claim that touches license or truth.

**Ask (binary):** default external form = `b`? (I recommend `b`; `c` reserved for
license/attestation contexts, `a` for casual references only.)

**Q3 (lower priority).** Do E3 and E4 — both currently uppercase `HERMES` — need
distinct canonical forms (e.g. `HERMES-overlay` vs `HERMES-MCP`), or is the §3
marker sufficient? Confirm whether bare uppercase `HERMES` should resolve to E3 by
default (§3 fallback) in all surfaces, including VAULT999 receipts.

---

## 7 · Ratification path

- This file is **DRAFT**. It changes no runtime, no config, no canon.
- On F13 **SAH**: copy to `/root/AAA/canon/NAMESPACE-MAP-v1.md`, add the standard
  canon header, and register the marker in `CANONICAL_GLOSSARY.md` (identities table).
- Until SAH: treat as the working disambiguation note; do not cite as canon.
- A bare `HERMES` in a new artifact is acceptable **only** under §3's declared-coordinate
  rule; otherwise it inherits this map's default (E3) or must be qualified.

DITEMPA BUKAN DIBERI — forged, not given.
