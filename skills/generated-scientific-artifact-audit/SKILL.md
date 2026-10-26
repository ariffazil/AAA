---
name: generated-scientific-artifact-audit
description: "Audit an AI-generated figure before trusting it."
version: 1.0.0
owner: HERMES
risk_tier: low
floor_scope: [F1, F2, F7]
autonomy_tier: T1
tags: [audit, artifact, figure, provenance, geology, rendering]
---

# Generated Scientific Artifact Audit

> A generated figure is a claim with a picture attached. Audit the claim, not the picture — and audit
> the picture for the same reason, because a rendered line looks measured whether or not it is.

## Trigger

Any time a scientific or technical artifact arrives or ships: a cross-section, an observatory page, a
multi-model comparison, a dossier figure, a rendered PDF, a saved web page. Both directions — auditing
someone else's artifact before accepting it, and auditing your own before publishing it.

Renderer output, model output, and a sibling agent's output all get the same treatment. Fluency is not
evidence.

## Procedure

### 1. Enumerate, do not read

List every concrete assertion the artifact makes: numbers, ages, unit names, statuses, counts, claims of
comparison, claims of provenance. Write them down with the parent each one is attributed to. Do this before
opening any source — the artifact's own narrative will anchor you otherwise.

### 2. Match each number against every candidate source, not only the named one

Tabulate what each plausible source says for that quantity. If the plotted value matches source B while the
caption cites source A, the citation is false even when every digit is right. This is **attribution
inversion** — the most survivable defect class, because the reader sees a source name and stops checking.

Machine-generated documents produce it systematically: the model had A's numbers in context and B's name in
the prompt. Look for it first.

Repair by naming the true parent. Where sources genuinely disagree, print the conflict and its state — never
pick one silently, never average two sources into a third number neither supports.

### 3. Hash the things claimed to be distinct

Where the artifact offers variants, models, scenarios, resolutions or datasets and invites comparison, hash
each payload:

```python
import json, hashlib
h = lambda o: hashlib.md5(json.dumps(o, sort_keys=True).encode()).hexdigest()[:10]
for m in manifest["MODELS"]:
    print(m["id"], h(m["bodies"]), m["title"])
```

Identical hashes across two identifiers means the advertised comparison compares an object with itself.
Same test for repeated titles or shorts. Ship the control only after asserting A is not B.

### 4. Read the document against the evidence it attaches to itself

Artifacts carry their own refutations: a footer asserting one value while the body plots another; a run
status of success while the appended log shows the job never started; a "404" in the fix list beside a probe
line reporting 200; a left-panel label naming model A while the canvas renders model C.

Two mutually exclusive claims from one evidence stream means at least one was generated rather than read.
When a build action rests on the contradicted claim, do not execute it — resolve which reading is true first.

### 5. Check the model's validity, not just its labels

Provenance tags, tier badges and disclaimers are wrappers. Confirm the underlying object can carry the claim:

- Does the geometry actually differ per model (step 3)?
- Is there a falsifier — a measurement, expected signal and deciding value — or only prose?
- Is a headline feature drawn in the province where it physically belongs, or placed by eye?
- Is one age printed for a surface that is picked on different markers in different domains?
- Do well results or observations come from a named release, or from generation?

A figure that is confidently wrong is worse than one that is visibly unfinished, because the polish buys it
a reader it has not earned.

### 6. Verify rendering before believing content

Render and read the result with vision. Assert on errors, not vibes:

- A JS error banner or blank panel means unverified, not "probably fine".
- Check label collisions at the strata they sit on, not on white background.
- Check the narrow viewport — a diagram that collapses below ~760px needs horizontal scroll, not smaller text.
- A saved page with zero `<script>` tags and no-op buttons is a **frozen snapshot**, not an application.
  Label it as frozen, with the model it froze on, or the reader will hunt for controls that cannot work.

### 7. Delivery is a measured state, not a copy

A file present at an assumed webroot proves nothing. Static servers commonly root different URL prefixes at
different directories, so a correct copy to the intuitive path can still 404. Verify at the origin against the
real host, then confirm the bytes served:

```bash
curl -sk -o /dev/null -w "%{http_code} %{size_download}\n" \
  --resolve example.com:443:127.0.0.1 https://example.com/path/
curl -s https://example.com/path/ | grep -c "<a string only the new page contains>"
```

Status 200 plus your unique string is delivery. Status 200 alone can be a fallback page. If the file exists
with correct permissions and still 404s, read the routing config for that path prefix before touching
permissions again — the root is wrong, not the file.

### 8. Report per claim, then stop

One line per finding: what was claimed, what is true, what settles it. Keep the count honest in both
directions — a document with three bad numbers and thirty good ones is a document with three bad numbers.
Name what survives; readers extend credit from the parts that held. Do not hand back a defect list when you
hold the pen and can fix and re-render in the same pass.

## Pitfalls

- **Authoritative-looking defaults pick the model for you.** A stacked-strata renderer will happily produce a
  tectonic section and be wrong about the tectonics — it cannot express underthrusting, a mobile-shale wedge
  or a Moho. If the framework involves crustal architecture, render that architecture explicitly or scope the
  artifact to "stratigraphic column only" and say so.
- **Fallback silent substitution.** Reading the right primary and then rendering from a convenience index
  reinstates the superseded model while looking sourced. When two references disagree on architecture, the
  one describing how the system works outranks the one listing what the parts are called.
- **Provenance badges create unearned trust.** Tier labels on empty content are the artifact equivalent of a
  confident tone. Check the object, then the badge.
- **A snapshot is not an app.** Dead buttons in an archived page invite the reader to conclude the tool is
  broken. Declare the freeze in the header.
- **Signed or expiring URLs are not provenance.** A source link carrying a signature and expiry will be dead
  shortly; the artifact must carry the citation, not a handshake.
- **Do not let a rendering failure read as a content finding.** Missing output directories, absent optional
  libraries and unwritable caches are build defects; report them as such and re-run after fixing, rather than
  filing them against the science.
- **Never claim success from a self-report.** A renderer, an agent and a manifest can all say "deployed" while
  the live URL serves something else. Measure.

## Reference

`references/geological-section-audit.md` — domain depth for tectonic cross-sections: layer-cake renderer
limits, framework-vs-formation-column precedence, off-section chainage, diachronous surface families, and
the well-outcome registry rule.
