# Step 7: claude-video Assessment v0.1.0

> Read-only evaluation. NOT an integration. NOT an approval.
> DITEMPA BUKAN DIBERI.

## What it is

`bradautomates/claude-video` is an open-source plugin that:
- Downloads video via `yt-dlp`
- Extracts frames via `ffmpeg`
- Attempts captions, falls back to Whisper
- Provides aligned multimodal input to an agent
- Has `/watch` command for CLI use

GitHub: https://github.com/bradautomates/claude-video

## What we have built (independent)

| Component | arifOS implementation | claude-video equivalent |
|---|---|---|
| Transcript extraction | youtube-content + youtube-transcript-api | Captions API + Whisper fallback |
| Frame extraction | video-evidence-packager v0.1.0 (deterministic, hashed) | ffmpeg extract (no hashing, no manifest) |
| OCR/vision | video-ocr-adapter v0.1.0 (OBS-labeled, timestamped) | Whisper fallback (audio-only) |
| Evidence packaging | evidence-segments.jsonl (structured, provenance-bound) | Agent context injection (free-form) |
| Typed claims | claim_graph v0.1.0 (classified, epistemic labels) | None |
| Skill generation | video_skill v0.1.0 (procedure_candidate, 888_HOLD) | Plugin auto-injects into context |

## What claude-video imports that we have NOT ratified

| Import | Decision required | Risk |
|---|---|---|
| Automated yt-dlp download | Storage, copyright, bandwidth, retention | Medium |
| yt-dlp dependency | Supply-chain pinning, version pinning | Low |
| ffmpeg dependency | Host package lifecycle (already present on KVM8) | Low |
| Whisper/API fallback | Cost, vendor, data egress, audio privacy | Medium |
| Browser cookies | Credential handling, scope, secret storage, auditability | HIGH |
| Implicit multimodal output | Must be converted to evidence segments | Medium |
| Skill installation path | Foreign code review, pinning, update control | Medium |

## Assessment

**PLAUSIBLE** as a reference implementation for the artifact contract.
**NOT APPROVED** for wholesale integration.

Borrow:
- Artifact contract patterns (if any align with our evidence envelope)
- Frame extraction technique (we already have a superior implementation with hashing)
- Caption fallback logic (we already have a superior implementation with evidence labels)

Do NOT borrow:
- Cookie handling (account ban risk, credential storage)
- yt-dlp dependency (use only after supply-chain review)
- Whisper fallback (we have GLM-ASR-2512 with custom dictionary)
- Skill installation path (we have 888_HOLD governance)

## Verdict

```yaml
assessment_status: complete
integration_status: not_integrated
recommendation: "defer until local evidence pipeline is fully proven"
blocking_decisions:
  - "YouTube acquisition policy (F13)"
  - "Cookie/credential handling (F13 + 888_HOLD)"
  - "yt-dlp supply-chain review"
  - "Whisper vs GLM-ASR vendor decision"
next_review_trigger: "Steps 4-6 proven in local execution"
```
