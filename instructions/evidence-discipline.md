# Evidence Discipline — 333-AGI Binding

> **Forged:** 2026-08-10 by F13 SOVEREIGN audit of /seal prompts
> **Binding:** 333-AGI Δ MIND — ALL evidence packages to 888-APEX
> **DITEMPA BUKAN DIBERI**

## The One Rule

```
888-APEX JUDGE DOES NOT ACCEPT STORIES.
IT ACCEPTS RAW EVIDENCE ONLY.
```

## Evidence Package Format

When invoking 888-APEX for SEAL-grade or receipt work, 333-AGI MUST provide:

```json
{
  "evidence_package": {
    "claims": [
      {"text": "...", "label": "OBS|DER|INT|SPEC", "source_path": "/path/to/evidence"}
    ],
    "probes": [
      {"url": "http://127.0.0.1:PORT/health", "response": "{...}", "timestamp": "ISO8601"}
    ],
    "receipts": [
      {"path": "/root/forge_work/...", "sha256": "..."}
    ],
    "diffs": [
      {"file": "/path/to/changed/file", "before_hash": "...", "after_hash": "..."}
    ],
    "logs": [
      {"path": "/root/...", "excerpt": "relevant lines"}
    ]
  },
  "no_conclusion_prose": "Judge mode ignores conclusion prose. Provide raw evidence only."
}
```

## What NOT to provide

- ❌ "I fixed X, Y, Z" — that's narrative. Show the diff.
- ❌ "49 sessions failed" — that's a claim. Show the logs.
- ❌ "Root cause was..." — that's analysis. Show the evidence that led to analysis.
- ❌ "FQ is 3.0 OPTIMAL" — that's a claim. Show the probe response.
- ❌ "Arif ordered this" as a conclusion — that's bias framing. Present as "F13 requested review."

## The C0 Self-Test

Before sending any evidence package to 888-APEX, 333-AGI MUST self-test:

> *"If someone who didn't trust me read this evidence package, would they find RAW DATA to verify my claims, or would they only find my STORY about what happened?"*

If the answer is "story" → DO NOT SEND. Gather raw evidence first.

## CIV-21 Binding

This discipline implements:
- **E4 Reality**: Every claim must be verified by live probe or raw artifact
- **E18 Blind Spots**: Compression (summary) creates blind spots. Raw evidence does not.
- **E20 Truth Metabolism**: Evidence must be primary source, not secondary narrative.
- **C0 Evidence Authenticity**: The gate between story and evidence.

## The Scar

This rule was forged from the scar discovered on 2026-08-10:
> 333 provided a story about evidence to 888-APEX. 888 flagged C0 as weak.
> The fix: raw evidence only. No prose conclusions. No narrative framing.

DITEMPA BUKAN DIBERI — Evidence is forged, not narrated. ⚒️
