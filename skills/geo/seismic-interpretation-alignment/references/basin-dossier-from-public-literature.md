# Basin / Field Dossier from Public Literature

Use when the user asks for a basin, field or block dossier ("give me the updated <basin> seismic interpretations
dossier") and the federation holds no proprietary data for it. Produces an honest artifact instead of a stalled
request or a fabricated one.

## Step 0 — Decide which of the two requests you actually have

| Request | Path |
|---|---|
| "Compile what is known about <basin>" | this file — literature synthesis |
| "Interpret **my** volume / update **my** picks" | cannot be done without the volume. Ask for the SEG-Y, LAS, Petrel export or screenshots. Do not approximate. |

The two are easy to conflate. Answering the second with the first is the failure this file exists to prevent.

## Step 1 — Probe the organ, and read the coverage gap correctly

```python
mcp__geox__geox_basin(basin_name="<name>", mode="profile", profile_mode="overview")
```

- `Basin data not found for: <name>` = the catalog does not carry this basin. Try one near-equivalent name (regional,
  not spelling variants) and stop.
- `basin_name is required (non-empty string)` = lat/lng alone is not a query. The tool needs a name.
- Three consecutive rejections pause the server (~48 s). Switch lane instead of retrying.

Also worth one call: `geox_well` (mode `view`) and `geox_source` — if either resolves for the area, you have real
subsurface data and should lead with it rather than with literature.

## Step 2 — Literature sweep (semantic search beats keyword search here)

`mcp__exa__web_search_exa(query="<basin> basin seismic stratigraphy petroleum geology")`

Exa returns title, DOI, authors and a long highlight extract — often enough to write the tectonic and stratigraphic
sections without opening anything. Query shape that works: basin name + the three nouns you need
(`seismic` / `stratigraphy` / `petroleum system`). Add `field` or `discovery` when chasing a specific accumulation.

Keep the query short and plain — a long natural-language sentence returns noisier neighbours than four to six
keywords. One sweep on the basin plus one on the specific field/block (if named) is the useful pair.

**Anchor sources that pay off for Malaysian and SE Asian basins:** Geological Society of Malaysia Bulletin
(`gsm.org.my` — field geology, core descriptions, production history and development chronology all in one
paper), EAGE EarthDoc, SPE OnePetro, TGS/BGS workshop PDFs, and PETRONAS MPM's exploration pages for the
official basin list and play-type framing. A named field usually has one society-bulletin paper that carries
most of the subsurface section by itself — find it before sweeping further.

## Step 3 — Full text for the anchor paper

`mcp__zai_reader__webReader(url="<pdf url>")` returns the extracted text of a PDF. Works on geological society
bulletins, EAGE/TGS workshop papers and conference proceedings.

- Pass a plain `https://...pdf` URL. Encoded or query-string URLs return `Please Enter the Correct URL Format`.
- One or two anchor papers is usually enough; the abstracts from Step 2 carry the rest. The reader
  lane is quota-metered, so spend it on the anchor PDFs only — a speculative URL burns a call and may
  return nothing usable. If it answers with a quota message, stay on the search lane (Step 2 highlights
  often carry the tectonic and stratigraphic detail outright) rather than stalling the dossier.
- A 500 from the reader lane on a publisher PDF is worth exactly one retry with a different anchor URL,
  not a re-run: prefer society bulletins and workshop papers over vendor marketing pages.
- Society bulletin papers are the highest yield per call — field geology, core data, production history and
  development chronology in a single document.

## Step 4 — Assemble and deliver

Dark-theme reportlab script in the workspace, run via `terminal`, delivered as `MEDIA:/abs/path.pdf`. Structure that
works for a review-grade pack:

1. Cover — title, classification line, preparer, date
2. Regional tectonic setting — basin classification, tectonic evolution, structural style
3. Stratigraphic framework — stage classification table, key seismic markers, play intervals
4. Field subsurface geology — discovery, accumulations, reservoir properties, production challenges
5. Interpretation methodology — **data available**, framework, key observations
6. Petroleum systems — source / reservoir / seal / migration / prospectivity
7. Production and development chronology
8. Recommendations and risk assessment
9. References — every paper cited, full citation
10. Closing page carrying the provenance disclaimer

## Hard rules for the artifact

- **Label it a literature synthesis on the face of the document**, not in a footnote. The closing page states which
  proprietary inputs are absent (SEG-Y, LAS, Petrel interpretation, velocity model, well ties).
- **Attribute every factual claim to a source** by author and year in the text, full citation in the reference list.
  An unattributed geological statement in a review pack is indistinguishable from an invention.
- **Declare data vintage.** Production figures from a 2003 paper are 2003 figures. Say the year next to the number.
- **No interpretation verbs.** The dossier may say "published work identifies"; it may not say "the seismic shows" or
  "the trap contains". See the parent skill's reporting-language rules.
- **State what a reviewer can ask that this dossier cannot answer** — that sentence is the value-add of the caveat page.

## Transport pitfalls

- `web_search` / `web_extract` may be routed to a provider that is not registered; when they return a configuration
  error, go straight to the MCP search and reader lanes above rather than retrying the same tool.
- Delegating PDF generation to a subagent is blocked by the mutation gate when the brief names financial or
  consequential variables. Write and run the generator script yourself.
