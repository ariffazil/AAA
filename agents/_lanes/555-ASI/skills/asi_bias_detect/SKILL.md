---
name: asi_bias_detect
agent: 555-ASI
namespace: asi_*
cluster: TRUST
trigger: "When 555 is about to take a position, recommend a synthesis, or feed a seal — at any point where reasoning might be distorted by anchoring, confirmation, availability, sunk cost, or recency bias"
capability: "Returns a bias report listing detected biases (with severity), the specific claim each one distorts, and a debiasing move (re-derive, invert, fetch a counter-prior, defer to a peer)"
mcp_tools_underneath: "arif_think, arif_critique (redteam mode), well_dark_geometry_mirror, well_measure_gradient"
blast_radius: "LOW"
gate_888_required: false
---

# asi_bias_detect

Every reasoning path has a shape. Some shapes are healthy; some are biases that have been mistaken for conclusions. 555 is not immune to bias — none of the organs are — and the HEART lane is the one that is constitutionally required to notice its own distortions before they become positions. This skill runs a structured bias scan over the current reasoning chain and surfaces what it finds. It never claims to be bias-free; it claims to be bias-aware, which is the only honest posture.

The bias scan covers five canonical patterns. **Anchoring** — has an early piece of evidence (often the operator's first sentence, or the first recall hit) become the gravitational center that all later evidence orbits, even when later evidence should outweigh it? **Confirmation** — is 555 selecting only the evidence that supports the current draft, while quietly downweighting counter-evidence? **Availability** — is a vivid, recent, or emotionally salient memory being treated as more representative than it is? **Sunk cost** — is 555 defending a prior position because defending it would be costly to retract, not because the position is still warranted? **Recency** — is the most recent signal being treated as the truest, when a stable prior would be more reliable? Each pattern is checked against the current chain with explicit examples.

The skill is conservative: a bias is reported at the lowest confidence at which it has any non-trivial support, and the report includes a one-line "how to falsify this finding" — a way for a peer or the operator to show that the bias is not actually present. This protects the skill from becoming its own bias (the bias-detection bias). A bias that cannot be falsified is a hypothesis, not a finding, and is labelled as such. The skill never reports a bias to win an argument; it reports a bias to keep the chain honest.

Failure modes: (a) the reasoning chain is too short to support a bias scan (e.g., a single-sentence response) — skill returns "scan not applicable, no chain to scan"; (b) the bias detected is so severe that the entire position is suspect — skill escalates to `asi_dissent_articulate` against its own draft, and refuses to emit the position until the bias is addressed; (c) a peer organ insists there is no bias when the scan flags one — the scan's report is logged, the peer response is logged, and the disagreement is sent to 888-APEX for deliberation, never silently dropped (F11 AUDIT). The skill is a mirror, not a judge. It shows 555 what 555 looks like from the outside.
