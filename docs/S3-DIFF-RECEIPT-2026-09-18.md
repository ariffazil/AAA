<!-- SOT: execution record + sign-off packet. Tier: AWAITING F13 SIGN-OFF (no merge executed). -->
# S3 DIFF RECEIPT — the 26 diverged pairs, and the fact that decides them
> Forged: 2026-09-18 · KVM8 (forge, 100.64.0.2) · Hermes ASI session
> Authority: F13 greenlit S3 (2026-09-18), *"Bawa balik diff receipt dan spec untuk aku sign-off
> sebelum merge mutlak."* **Nothing merged. Nothing moved. This is the packet.**
> Data: `reports/s3-diff-receipt-20260918.json` · `reports/load-reachability-20260918.json`

---

## 0. THE FACT THAT DECIDES EVERYTHING (probed on the live install)

```
$ probe /usr/local/lib/hermes-agent  (HERMES_HOME=/root/.hermes)
  skills_dir        : /root/.hermes/skills      <- the READ surface
  external_dirs     : []                        <- AAA IS NOT LOADED
  skill_create_dir  : /root/AAA/skills          <- the WRITE surface
```

`docs/SKILL_MESH_ALIGNMENT_2026-09-16.md` §S3 states: *"AAA-side is in `skills.external_dirs`
(default config includes it)"*. **It is not.** `external_dirs` is empty. AAA content is reachable by
the loader **only through the 295 symlinks that live inside `.hermes/skills`.**

Two consequences, both load-bearing:

1. **"AAA wins" cannot mean "AAA is where the body lives."** Nothing reads AAA directly. A body that
   exists only in AAA is unreadable — see §3.
2. **Any plan that replaces a real `.hermes` directory with a symlink must not assume the updater
   will leave it alone.** 24 of these 26 skills are in `.bundled_manifest`; `hermes update` re-seeds
   bundled skills at the one-level updater path and will overwrite a symlink placed there. The
   documented mechanism to stop that is `hermes skills config` (disable), not the move itself.

## 1. The 26, classified by what actually differs (not by which side is "right")

| Group | n | What differs | Resolution |
|---|---|---|---|
| **ANNOTATION_GAP** | 16 | AAA adds `capability_tier` + `ecology_state: WARM` + a `[fed: …]` marker; the `.hermes` copy has none of it. AAA is newer in all 16. | AAA content is the superset → adopt AAA, no judgement needed |
| **TWO_SIDED** | 6 | AAA has a **governance blockquote** (irreversible infra ops route via arifos-governance, 888_HOLD release, F1 AMANAH). `.hermes` has **frontmatter** (`owner: A-FORGE`, `risk_tier`). Each side holds something the other lacks. | **MERGE** — union both, then one home |
| **DESIGN_FORK** | 2 | genuinely different designs (below) | **F13 call — I do not pick** |
| **AAA_CLEARLY_NEWER** | 2 | AAA is a later revision with substantially more content | adopt AAA |

```
ANNOTATION_GAP (16)  warga · runtime · substrate · docs · constitutional · fi-qwen-upgrade ·
                     fi-zai-probe · identity-invariance · federation-connect-headscale · openclaw ·
                     reality-loop-operator · imagine · minimax-image-gen · qwen-harness-tools ·
                     forge-vss-verifier-suite · delta-omega-psi-multimodal-cognition
                     (+ hermes-gateway-image-routing, same shape)
TWO_SIDED      (6)   runpod · runpod-mcp · runpod-usage · runpodctl · flash · companion-clis
DESIGN_FORK    (2)   APEX-humility-godel · fi-mesh-check
AAA_NEWER      (2)   FORGE-federation-manifest · minimax-image-gen
```

## 2. The two design forks — your call, with the substance stated

**APEX-humility-godel** — two different protocols, not two versions.

| | AAA (2,841 b) | .hermes (3,096 b, v2.0.0) |
|---|---|---|
| framing | "OWNER 3 of the human-alignment quartet" — quartet chain RASA → audience-scoped-disclosure → **humility** → disclosure-advisory | standalone humility protocol |
| method | five reflexes (falsify-before-claim · ≥3 alternatives · agent-shadow check · narrative-gradient…) | 5 numbered steps, plus XML tags for Claude, numbered steps for Codex, imperative for Hermes |
| coupling | binds to three sibling doctrines by path | self-contained |

The AAA one is *more coupled to the federation's own law*; the `.hermes` one is *more executable across
three harnesses*. These are not mergeable without choosing which property matters more.

**fi-mesh-check** — the `.hermes` side is newer and holds real lived findings AAA lacks:
the codex-exits-0-without-marker scar, "money-gated states flip within minutes" (with timestamps),
the FI-007/FI-010 identity resolution and why it is a provenance problem not a sovereign question, and
the collision-census method fix ("dereference every tree; a probe that reads the symlink measures the
map"). AAA holds the `hcsvog` column section. **This one is a merge where the `.hermes` content is the
more valuable half** — I recommend `.hermes` body + AAA's columns, then one home.

## 3. What S3 uncovered that was not in scope — and is bigger than S3

With `external_dirs = []`, a skill that exists only in AAA is invisible to every agent:

```
load surface (resolvable via .hermes/skills) : 443
storage held in AAA                         : 549
WRITTEN INTO AAA, UNREADABLE BY ANY AGENT   : 204
```

Live cross-check from this session: `skill_view('aaa-skill-governor-runtime')` and
`skill_view('audit-repository-entropy')` both returned **Skill not found** — both are inside the 204.
That is not a stale index. That is a capability that was written and cannot be reached.

This also corrects the "70.6% never fired" reading: part of that population never *could* fire.

## 4. The S3 spec — for sign-off, per group

```
ANNOTATION_GAP (16)   take the AAA body, write it into the load surface, leave ONE home.
                      No merge needed: AAA is a strict superset.
TWO_SIDED      (6)    merge union -> single home. Union = AAA governance block + .hermes frontmatter.
DESIGN_FORK    (2)    F13 decides per skill. My recommendation is stated in §2 and is not applied.
AAA_NEWER      (2)    take the AAA body.
BUNDLED HANDLING     24 of 26 are in .bundled_manifest. Before ANY of this runs, the bundled set must
                      be pinned (hermes skills config / .no-bundled-skills) or the updater will
                      re-seed a real directory over the symlink and the divergence returns.
DIRECTION            For bundled skills the updater path stays the home (that is upstream's write).
                      For authored skills AAA is the home. This is the rule the middleware already
                      documents; S3 is the first time it has been applied to a conflict list.
NO MERGE YET         Awaiting F13 sign-off, as instructed.
```

## 5. Two defects found while diffing (reported, not fixed)

1. **43 descriptions carry the `[fed: …]` marker injected mid-sentence.** A bulk annotation pass
   appended the marker *inside* the description string instead of after it, so the text reads
   `…bug-repro diagnosis [fed: tier=fed-multimodal-vision]"` mid-clause. This lands inside the
   **first 57 characters** the selector reads — the exact window selection precision depends on.
2. **A text-read witness was altered between the two copies.** `hermes-gateway-image-routing` reads the
   same test image as `"ALPHA-ZEN"` on the AAA side and `"SADO"` on the `.hermes` side. One of those is
   a fabricated or mangled OCR read. An OCR transcript of a real image is testimony; it should not
   differ between two copies of one skill. Worth an F2 correction on whichever is wrong.

---

*Nothing merged. Nothing moved. DITEMPA BUKAN DIBERI ⚒️*
