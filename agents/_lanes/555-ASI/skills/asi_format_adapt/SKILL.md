---
name: asi_format_adapt
agent: 555-ASI
namespace: asi_*
cluster: DELIVERY
trigger: "When 555 has a calibrated message (post-asi_voice_calibrate) and must shape it to a specific channel — Telegram, A2A card, JSON receipt, audit log, design doc, or sovereign briefing"
capability: "Reformats a message to the target channel's structural contract (length caps, markdown rules, JSON schema, header conventions) without losing voice, content, or evidence labels"
mcp_tools_underneath: "forge_browser_extract_text, arifos arif_session_post (peer message), vaul999_write_log"
blast_radius: "LOW"
gate_888_required: false
---

# asi_format_adapt

Voice is *what* the message says; format is *how the channel receives it*. A warm BM sentence that is also a JSON receipt is a contradiction — JSON doesn't carry warmth, and warmth doesn't carry schema. This skill is the bridge: it takes the calibrated message and renders it into the channel-appropriate shape, while guaranteeing that no information is silently dropped and no evidence label is smoothed away in translation. 555 must be understood on every channel, and "understood" means different things on different channels.

Each channel has a structural contract. **Telegram** wants a lead sentence, a 2–4 line body, optional inline code, and an explicit `[NEXT]` line. **A2A card** wants a JSON object with `agent`, `intent`, `payload`, `evidence_refs`, and a `signature`. **Audit log** wants one line per event with timestamp, actor, action class, and a one-sentence rationale. **Design doc** wants headers, code blocks, and citation anchors. **Sovereign briefing** wants prose, no jargon, BM-friendly, with a `next-decision` footer. The skill applies the contract; it does not invent a new one.

The skill has a non-negotiable invariant: **no silent redaction**. If a channel's length cap forces truncation, the truncated portion is moved to a referenced attachment — not deleted. If a channel's schema cannot carry an evidence class label (e.g., plain SMS), the label is replaced with an explicit "I'm dropping the OBS/DER/INT/SPEC marker for this channel; see receipt for full chain" footnote, never silently elided. This is F2 TRUTH: the operator and peers must always know what evidence class a statement carries, even when the channel can't display it. The skill is a format adapter, not a content filter.

Integration: this skill is downstream of `asi_voice_calibrate` and upstream of the actual emission tool. It never bypasses 555's other layers — it shapes, it does not author. Failure modes: (a) target channel is unknown — skill defaults to the richest format available (markdown) and flags the channel miss; (b) the message carries an 888_HOLD verdict and the channel cannot carry the full weight — skill refuses to degrade and routes the message to a richer channel (e.g., if Telegram is too thin, the full verdict is sealed to VAULT999 and only a pointer is sent to Telegram); (c) the format adaptation would split a single coherent message across multiple artifacts — the skill prefers a single artifact with a footer, and splits only when the channel contract requires it. The skill writes the channel and format version to the local ledger for reproducibility.
