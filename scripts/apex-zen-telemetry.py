#!/usr/bin/env python3
"""
APEX-ZEN Telemetry Collector — Layer 2 of Runtime Enforcement Ladder

Computes CD, DD, IAR, DCR metrics from session transcripts.

Usage:
    python3 apex-zen-telemetry.py --input <transcript.txt>
    python3 apex-zen-telemetry.py --input-dir /root/.kimi-code/sessions/
    python3 apex-zen-telemetry.py --stdin < transcript.txt

Doctrine reference: /root/AAA/governance/APEX-ZEN-EXECUTION-DOCTRINE.md § 13
"""
import re
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

# GO signals (execution authorization) — counted as execution_requests
GO_SIGNALS = [
    r'\bfix it\b', r'\bpatch it\b', r'\bdo it\b', r'\bapply it\b',
    r'\bgenerate it\b', r'\bwrite it\b', r'\bimplement it\b',
    r'\bship it\b', r'\bdeploy it\b', r'\bdo all\b', r'\bexecute\b',
    r'\brun it\b', r'\bmake it\b', r'\bbuild it\b', r'\bformalize\b',
    r'\binstall\b', r'\bapply the patch\b', r'\bproceed\b'
]

# Confirmation patterns (CD violations)
CONFIRMATION_PATTERNS = [
    r'would you like me to',
    r'shall i\b',
    r'should i\b',
    r'want me to',
    r'better to defer',
    r'nak apply atau simpan',
    r'kau nak aku',
    r'nak .* atau',
    r'nak .* ke',
    r'you want me to',
    r'let me know if',
    r'mahu.*simpan',
    r'do you want',
    r'shall i proceed',
    r'should i continue',
    r'would you like',
    r'save for later',
    r'esok boleh',
]

# Artifact patterns (delivered work)
ARTIFACT_PATTERNS = [
    r'\[TOOL_ARTIFACT:',  # calibrated: tool.call events via session-collector
    r'\bpatch(ed)?\b.*\battached\b',
    r'\b\d+ lines? (added|changed|removed)\b',
    r'\bdiff:?\s',
    r'\bwrote \d+ bytes?\b',
    r'\bartifact attached\b',
    r'\battached:\b',
    r'\bfile (created|written|patched|updated)\b',
    r'\bReplaced \d+ occurrence',
    r'\bWrote \d+ bytes\b',
    r'\$\.\/.*\.sh',
    r'cd /',
    r'mv /',
    # Tool-call artifacts (synthetic markers from collector)
    r'tool_call:\s*(Edit|Write|MultiEdit|Create|NotebookEdit)\b',
    # kimi-code specific markers
    r'\bReplaced \d+ occurrence',
    r'\bWrote \d+ bytes',
]

# Verbose-default patterns (Tier-2 leakage into Tier 0/1)
VERBOSE_LEAK_PATTERNS = [
    r'After constitutional examination',
    r'\[F\d+\]',
    r'According to F\d+',
    r'constitutional analysis',
    r'In the arifOS context',
    r'governance receipt',
    r'sealed.*receipt',
]


def count_patterns(text: str, patterns: list) -> int:
    """Count total matches of any pattern in text."""
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return count


def count_turns(text: str) -> int:
    """Approximate turn count by speaker markers."""
    markers = re.findall(r'\b(ARIF|Syed|HERMES|Arif AI|Human|User)\s*:', text, re.IGNORECASE)
    return len(markers)


def count_artifacts(text: str) -> int:
    """Count artifacts delivered."""
    return count_patterns(text, ARTIFACT_PATTERNS)


def compute_metrics(transcript: str) -> dict:
    """Compute CD, DD, IAR, DCR for a transcript."""
    go_signals = count_patterns(transcript, GO_SIGNALS)
    confirmations = count_patterns(transcript, CONFIRMATION_PATTERNS)
    artifacts = count_artifacts(transcript)
    turns = count_turns(transcript)
    verbose_leaks = count_patterns(transcript, VERBOSE_LEAK_PATTERNS)

    # CD: confirmation debt
    cd = confirmations / max(go_signals, 1) if go_signals > 0 else 0.0

    # DD: discussion debt (turns before artifact)
    # Approximation: total turns / artifacts if artifacts exist
    dd = (turns / max(artifacts, 1)) if artifacts > 0 else float('inf')

    # IAR: artifact-to-request
    iar = artifacts / max(go_signals, 1) if go_signals > 0 else 0.0

    # DCR: decision closure rate
    dcr = artifacts / max(confirmations + artifacts, 1) if (confirmations + artifacts) > 0 else 0.0

    return {
        'go_signals': go_signals,
        'confirmations': confirmations,
        'artifacts': artifacts,
        'turns': turns,
        'verbose_leaks': verbose_leaks,
        'CD': round(cd, 4),
        'DD': round(dd, 2) if dd != float('inf') else 'inf',
        'IAR': round(iar, 4),
        'DCR': round(dcr, 4),
        'targets_met': {
            'CD_lt_0.05': cd < 0.05,
            'DD_lt_2': (dd < 2) if dd != float('inf') else False,
            'IAR_gt_0.80': iar > 0.80,
            'DCR_gt_0.90': dcr > 0.90,
        },
        'all_targets_met': all([
            cd < 0.05,
            (dd < 2) if dd != float('inf') else False,
            iar > 0.80,
            dcr > 0.90,
        ])
    }


def compute_apex_vector(record: dict) -> dict:
    """Map APEX-ZEN metrics → APEX variables + G_closure.
    
    CD → P (Present Authority):  P = 1 - CD        [low CD = high authority recognition]
    DD → E (Energy):              E = 1/(1+DD)     [low DD = efficient energy to artifact]
    IAR → A (Akal):               A = IAR          [intent-to-artifact = effective intelligence]
    DCR → X (Exploration maturity): X = DCR         [high closure = exploration matures]
    
    G_closure = (A · P · E · X)^(1/4)
    """
    cd = float(record.get('CD', 0) or 0)
    dd = record.get('DD', 'inf')
    iar = float(record.get('IAR', 0) or 0)
    dcr = float(record.get('DCR', 0) or 0)

    p = max(0.0, min(1.0, 1.0 - cd))

    if dd in ('inf', None):
        e = 0.0
    else:
        try:
            e = 1.0 / (1.0 + float(dd))
        except (TypeError, ValueError):
            e = 0.0

    a = max(0.0, min(1.0, iar))
    x = max(0.0, min(1.0, dcr))

    product = a * p * e * x
    g = product ** 0.25 if product > 0 else 0.0

    return {
        'A_effective': round(a, 4),
        'P_effective': round(p, 4),
        'E_effective': round(e, 4),
        'X_effective': round(x, 4),
        'G_closure': round(g, 4),
    }


def main():
    parser = argparse.ArgumentParser(description='APEX-ZEN Telemetry Collector (Layer 2)')
    parser.add_argument('--input', '-i', help='Input transcript file')
    parser.add_argument('--input-dir', '-d', help='Directory of transcripts (recursive)')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin')
    parser.add_argument('--output', '-o', default='/root/VAULT999/apex-zen-telemetry.jsonl',
                        help='Output JSONL file')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode (no stdout)')
    args = parser.parse_args()

    transcripts = []
    if args.stdin:
        transcripts.append(('stdin', sys.stdin.read()))
    elif args.input:
        transcripts.append((args.input, Path(args.input).read_text()))
    elif args.input_dir:
        for ext in ('*.txt', '*.md', '*.jsonl', '*.log'):
            transcripts.extend(((str(p), p.read_text()) for p in Path(args.input_dir).rglob(ext)))

    if not transcripts:
        print("No transcripts found. Use --input, --input-dir, or --stdin", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open('a') as f:
        for name, text in transcripts:
            metrics = compute_metrics(text)
            apex_vector = compute_apex_vector(metrics)
            record = {
                'source': name,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'doctrine_status': 'PROVISIONAL_SEAL',
                **metrics,
                **apex_vector,
            }
            f.write(json.dumps(record) + '\n')
            if not args.quiet:
                verdict = '✅ ALL TARGETS MET' if metrics['all_targets_met'] else '⚠️ TARGETS NOT MET'
                print(f"\n=== {name} ===")
                print(f"GO signals:    {metrics['go_signals']}")
                print(f"Confirmations: {metrics['confirmations']}  (CD = {metrics['CD']}, target < 0.05)")
                print(f"Artifacts:     {metrics['artifacts']}  (IAR = {metrics['IAR']}, target > 0.80)")
                print(f"Turns:         {metrics['turns']}  (DD = {metrics['DD']}, target < 2)")
                print(f"Verbose leaks: {metrics['verbose_leaks']}  (DCR = {metrics['DCR']}, target > 0.90)")
                print(f"\nVerdict: {verdict}")


if __name__ == '__main__':
    main()