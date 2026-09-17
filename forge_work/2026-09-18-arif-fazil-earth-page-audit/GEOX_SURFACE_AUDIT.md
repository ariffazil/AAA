# AUDIT — third-party GEOX review (FI-003 / Qwen Code paste)
**Audited:** 2026-09-18 · **Node:** forge (KVM8) · **Auditor:** Hermes
**Method:** every checkable claim probed against live MCP + deployed source

---

## VERDICT

The paste is **substantially grounded** — it is not a hallucination and not connector-boilerplate.
Its tool enumeration is exactly right, its physics claims check out, and its read of the
governance gates matches what I verified myself. But it repeats **two advertisements as
architecture**, and one of those advertisements is a live silent-wrong-answer defect.

---

## 1. VERIFIED TRUE

| Claim | Check | Result |
|---|---|---|
| Tool list (31 named) | diff vs `CANONICAL_PUBLIC_TOOLS` | **EXACT — 31/31, zero invented, zero missed** |
| `geox_claim` HOLDs on OBSERVE_ONLY | I hit it myself this session | **TRUE** |
| `geox_well` rejects unknown probe_id (SABAR) | behavioural, consistent | **Plausible — see §4** |
| `ext_witness_ready: false` stamped | `geox_middleware.py:920-937` | **TRUE** |
| `_evidence_postcondition` spec `geox-evidence-postcondition-v1` | found in `dde_reason.py:130`, `basin_unified.py:130`, `seismic_compute_unified.py:133` | **TRUE** |
| Ricker / Butterworth wavelets | 31 / 2 files | **TRUE** |
| Zoeppritz / Shuey / LMR / Castagna | 19 / 14 / 10 / 18 files | **TRUE** |
| `geox_extract_display_proxy` "NOT for quantitative decisions" | manifest: *"NOT suitable for AVO, amplitude preservation, or native well-tie"*; code: *"This is DISPLAY_DERIVED_PROXY, not NATIVE_TRACE"* | **TRUE — and honestly labeled** |
| GLOF cascade pipeline (7 tools) | all 7 on the public surface | **TRUE** |

The display-proxy disclaimer is worth noting as a **positive**: the surface labels its own
weakest lane unprompted. That is the house doing exactly what this audit keeps asking for.

---

## 2. FINDING — "40+ tools" contradicts its own list, and the live server

**Paste says:** *"The 40+ tool surface (what the MCP exposes to me)"* … then lists **31**.
**Live `server/discover` says:**
```
"io.geox/surface": { "public_tools": 31,
                     "source": "geox_mcp.registry.CANONICAL_PUBLIC_TOOLS" }
```
`CANONICAL_PUBLIC_TOOLS` imports to exactly **31**.

**Paste also says:** *"The surface has grown since 2026-09-15"* — **no.** 31 is the same number
sealed in the repo SOT on 2026-09-15. Nothing grew.

The `tools_manifest.yaml` carries **85** entries, which is likely where 40+ came from — but
that is the full manifest (internal + public). The public surface is 31, and the paste's own
enumeration proved it.

**Self-contradiction within one message**: headline 40+, body 31. The body was right.

---

## 3. FINDING — the falsification loop is an advertisement, not an implemented mode

**Paste says:** *"geox_claim — Full lifecycle: create/validate/challenge/seal/falsify/discover/
synthesize/abduct/contradict/scan"* and calls it *"a genuine falsification loop, not a
confirmation machine."*

That string is the **manifest description**, verbatim:
> *"Claim lifecycle: create, validate, challenge, seal, evidence, falsify, synthesize, contradict.
> Modes: create, validate, challenge, seal, attach, falsify, discover, synthesize, abduct,
> contradict, scan."* — 11 modes advertised.

**The code implements 5:**
```python
mode: Literal["create", "validate", "challenge", "seal", "attach_evidence"]
```
And the dispatch is if/return for those, then:

```python
    # Default: create
    from geox_mcp.tools.claims import geox_claim_create as _impl
    return await _impl(...)
```

### The consequence — and this is the real defect

A caller who reads the advertised surface and sends `mode="falsify"`, `"discover"`,
`"synthesize"`, `"abduct"`, `"contradict"`, or `"scan"` **does not get an error.**
It falls through to the default and **CREATES A NEW CLAIM.**

An agent attempting to falsify a hypothesis gets a fresh claim written instead — with no
signal that the request was not honoured. That is a **silent-wrong-answer**, the failure class
this federation treats as worse than an error, because the caller has no way to notice.

**Confirmed identical in the DEPLOYED copy** (`/opt/geox`, commit `8c6c7f2d`):
same 5-mode Literal, same `# Default: create` fallthrough. Not a repo-only issue.

**And the capability itself exists — just unreachable.** `src/geox_mcp/tools/falsify.py`,
`evidence_reason.py` (`_phase_synthesize`, `_phase_abduct`, `_phase_contradict`,
`_contradiction_scan`) are real. But `registry.py` contains **zero** references to `falsify` or
`evidence_reason` — **none of it is on the public surface of 31.** So real falsification code
exists in the tree, cannot be called through the live MCP, while the tool description promises it
as a mode.

---

## 4. Unverified (flagged, not disputed)

- `geox_well` SABAR behaviour on an unknown `probe_id` — plausible and consistent with the house
  pattern, but I did not reproduce it myself; the paste's own session was OBSERVE_ONLY.
- `geox_basin` `claim_state: HYPOTHESIS`, `witness_type: AI` — the fields exist; the specific
  response was not re-run.
- The five-layer architecture table is the paste's own synthesis, not a surface claim. It reads
  correctly but is a model of GEOX, not evidence of GEOX.

---

## 5. The pattern, stated once

The paste read the surface and reported the surface — faithfully, competently, in good faith.
It did not invent anything. Its errors are all **reading declarations as implementations**:

- "40+ tools" ← a manifest count, not the public surface
- "genuine falsification loop" ← a tool description, not a dispatch table
- "the surface has grown" ← an assumption, not a measurement

That is the **same defect** as the Kinabalu dossier's *"The tool exists. The code is written."*
(2026-09-15) and the same defect as the earth-page images labeled `ACOUSTIC IMPEDANCE
CALIBRATION` (2026-09-18). Three artifacts, three authors, one shape:

> **A declaration of capability is not evidence of capability. The description is the claim,
> not the receipt.**

The difference this time: it is *live infrastructure* describing itself inaccurately, and the
inaccuracy routes real callers to the wrong behaviour silently.

---

## 6. Recommended fixes (one line each, cheaper than the audit)

1. `geox_claim` dispatch — either implement the six advertised modes, or raise an explicit
   unsupported-mode error instead of falling through to `create`. **Highest priority: silent
   wrong answer on a live governance tool.**
2. Manifest description for `geox_claim` — trim to the 5 implemented modes, or mark the rest
   `advertised_not_implemented`.
3. Either surface `falsify` / `evidence_reason` on the public registry, or state in the
   description that falsification is internal-only.

---

DITEMPA BUKAN DIBERI ⚒️
