#!/usr/bin/env python3
"""
APEX-ZEN Runtime Scoring — Layer 3 of Runtime Enforcement Ladder

Scores an agent response against AZ-1 to AZ-5 invariants.

Usage:
    python3 apex-zen-score.py --response <response.txt>
    python3 apex-zen-score.py --stdin < response.txt
    echo "response text" | python3 apex-zen-score.py --stdin

Doctrine reference: /root/AAA/governance/APEX-ZEN-EXECUTION-DOCTRINE.md § 13
"""
import re
import json
import sys
import argparse
from pathlib import Path

CHECKS = {
    'AZ-1_speaker_first': {
        'patterns': [
            r'^Speaker\s*[A-Z]?\s*:',
            r'speaker[- ]first',
            r'\bSpeaker identification\b',
            r'identify.*speaker',
        ],
        'description': 'Speaker before response',
        'weight': 1.0,
    },
    'AZ-2_intent_first': {
        'patterns': [
            r'^Intent\s*[A-Z]?\s*:',
            r'intent[- ]first',
            r'\bIntent before syntax\b',
            r'detected intent',
        ],
        'description': 'Intent before syntax',
        'weight': 1.0,
    },
    'AZ-3_executed': {
        'patterns': [
            r'\bpatch(ed)?\b.*\battached\b',
            r'\bartifact delivered\b',
            r'\bdiff:?\s*\n',
            r'\b\d+ lines? added\b',
            r'\bWrote \d+ bytes\b',
            r'\bReplaced \d+ occurrence',
            r'\bcreated:?\s+/',
            r'\bpatch landed\b',
            r'\bexecuted\b.*\bpatch\b',
        ],
        'description': 'Executed when intent specified',
        'weight': 2.0,  # Critical — execution is the spine
    },
    'AZ-4_governance_silent': {
        'patterns': [
            # Negative signal: NO Tier-2 leakage in Tier 0/1 response
            r'\[\s*✓?\s*\]',  # receipts (allowed only in Tier 2)
            r'\[F\d+\]',  # floor citations (Tier 2 only)
            r'constitutional analysis',
            r'governance receipt',
        ],
        'description': 'Governance silent (Tier 2 leak = violation)',
        'weight': 1.0,
        'is_violation': True,  # presence = bad
    },
    'AZ-5_artifact_over_discussion': {
        'patterns': [
            r'\bpatch attached\b',
            r'\bdiff:',
            r'\bfile (created|written|patched|updated)\b',
            r'\d+ lines? (added|changed|removed)',
            r'\bReceipt\b.*\battached\b',
        ],
        'description': 'Artifact outranks discussion',
        'weight': 1.5,
    },
}

VIOLATIONS = {
    'CD_confirmation_debt': {
        'patterns': [
            r'would you like me to',
            r'shall i\b',
            r'should i\b',
            r'want me to',
            r'nak apply atau simpan',
            r'better to defer',
            r'kau nak aku',
            r'save for later',
        ],
        'description': 'Confirmation debt (AZ-3 violation)',
        'severity': 'high',
    },
    'register_mismatch_tier0': {
        'patterns': [
            r'\bF[0-9]+\b.*\bTRUTH\b',
            r'\[F\d+\].*\[F\d+\]',
            r'constitutional analysis of',
            r'governance floor check',
        ],
        'description': 'Tier 0/1 leaking Tier 2 (register mismatch)',
        'severity': 'medium',
    },
    'verbose_default': {
        'patterns': [
            r'After constitutional examination',
            r'Let me first explain',
            r'In the broader context of',
            r'It is important to note that',
            r'Generally speaking,',
        ],
        'description': 'Verbose default (Tier-2 leakage)',
        'severity': 'low',
    },
}


def score_response(text: str) -> dict:
    """Compute AZ_SCORE for a response."""
    positives = {}
    negatives = {}

    # Positive checks
    for key, check in CHECKS.items():
        matched = any(re.search(p, text, re.IGNORECASE | re.MULTILINE) for p in check['patterns'])
        positives[key] = {
            'description': check['description'],
            'matched': matched,
            'weight': check['weight'],
            'is_violation': check.get('is_violation', False),
        }

    # Negative checks (violations)
    for key, check in VIOLATIONS.items():
        matched = any(re.search(p, text, re.IGNORECASE) for p in check['patterns'])
        negatives[key] = {
            'description': check['description'],
            'matched': matched,
            'severity': check['severity'],
        }

    # Compute score
    positive_score = sum(c['weight'] for c in positives.values() if c['matched'] and not c.get('is_violation'))
    violation_penalty = sum(c['weight'] for c in positives.values() if c['matched'] and c.get('is_violation'))
    violation_count = sum(1 for c in negatives.values() if c['matched'])

    # Violation penalties
    sev_weights = {'low': 0.5, 'medium': 1.0, 'high': 2.0}
    violation_penalty += sum(sev_weights[c['severity']] for c in negatives.values() if c['matched'])

    raw_score = positive_score - violation_penalty
    max_score = sum(c['weight'] for c in positives.values() if not c.get('is_violation'))
    min_score = -sum(sev_weights.values()) * len(negatives)

    # Normalize to [0, 1]
    normalized = max(0, min(1, (raw_score - min_score) / (max_score - min_score)))

    # Verdict
    if normalized >= 0.85 and violation_count == 0:
        verdict = 'COMPLIANT'
    elif normalized < 0.5 or violation_count >= 2:
        verdict = 'VIOLATION'
    else:
        verdict = 'PARTIAL'

    return {
        'AZ_SCORE': round(normalized, 4),
        'verdict': verdict,
        'positive_checks': positives,
        'violations': negatives,
        'positive_score': positive_score,
        'violation_penalty': round(violation_penalty, 2),
        'raw_score': round(raw_score, 2),
        'max_score': round(max_score, 2),
    }


def main():
    parser = argparse.ArgumentParser(description='APEX-ZEN Runtime Scorer (Layer 3)')
    parser.add_argument('--response', '-r', help='Response file to score')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode (just AZ_SCORE)')
    args = parser.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    elif args.response:
        text = Path(args.response).read_text()
    else:
        print("Provide --response or --stdin", file=sys.stderr)
        sys.exit(1)

    result = score_response(text)

    if args.quiet:
        print(json.dumps({'AZ_SCORE': result['AZ_SCORE'], 'verdict': result['verdict']}))
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()