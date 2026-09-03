#!/usr/bin/env python3
"""
Dream Engine — 72-Hour Reasoning Distillation
Option 2: LLM summarizes reasoning traces into wisdom.md

Thermodynamic goal: ΔS < 0
- Input: high-entropy raw reasoning logs from state.db
- Output: low-entropy distilled axioms in wisdom.md

Anti-overfitting: 3+ sessions rule
- A pattern must appear in 3+ distinct sessions before promotion to wisdom.md
- Prevents recency bias from single intense sessions
"""

import sqlite3
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import requests

# Configuration
STATE_DB = "/root/.hermes/state.db"
WISDOM_FILE = "/root/AAA/dream-engine/wisdom.md"
GATEWAY_URL = "http://100.64.0.2:4000/v1/chat/completions"
MODEL = "forge-777"  # federation model group (routed via FED gateway)
FALLBACK_MODELS = ["i-arif", "apex-888"]
HOURS_LOOKBACK = 72
MIN_SESSIONS_FOR_PROMOTION = 3

def extract_reasoning_traces():
    """Extract reasoning traces from state.db (last 72 hours)."""
    if not os.path.exists(STATE_DB):
        print(f"ERROR: {STATE_DB} not found", file=sys.stderr)
        sys.exit(1)
    
    conn = sqlite3.connect(STATE_DB)
    conn.row_factory = sqlite3.Row
    
    cutoff = datetime.now() - timedelta(hours=HOURS_LOOKBACK)
    cutoff_ts = cutoff.timestamp()
    
    # Query: messages with reasoning content in last 72h
    query = """
    SELECT 
        m.session_id,
        m.role,
        m.content,
        m.reasoning,
        m.reasoning_content,
        m.timestamp,
        s.title as session_title
    FROM messages m
    JOIN sessions s ON m.session_id = s.id
    WHERE m.timestamp >= ?
      AND (m.reasoning IS NOT NULL OR m.reasoning_content IS NOT NULL)
    ORDER BY m.timestamp DESC
    """
    
    rows = conn.execute(query, (cutoff_ts,)).fetchall()
    conn.close()
    
    # Group by session
    sessions = {}
    for row in rows:
        sid = row['session_id']
        if sid not in sessions:
            sessions[sid] = {
                'title': row['session_title'],
                'messages': []
            }
        
        reasoning = row['reasoning'] or row['reasoning_content'] or ''
        if reasoning.strip():
            sessions[sid]['messages'].append({
                'role': row['role'],
                'content': row['content'] or '',
                'reasoning': reasoning,
                'timestamp': row['timestamp']
            })
    
    return sessions

def format_for_distillation(sessions):
    """Format sessions into prompt for LLM distillation.
    Aggressive truncation: sample 3 messages per session, 400 chars each.
    Total budget ~10K chars to keep LLM payload under control.
    """
    if not sessions:
        return "No reasoning traces found in the last 72 hours."
    
    output = []
    output.append(f"Sessions analyzed: {len(sessions)}")
    output.append("")
    
    for sid, data in sessions.items():
        output.append(f"\n### Session: {data['title'] or sid[:20]}")
        output.append(f"Messages: {len(data['messages'])}")
        
        # Sample up to 3 messages per session
        sampled = data['messages'][:3]
        for msg in sampled:
            output.append(f"**{msg['role'].upper()}**")
            if msg['content']:
                output.append(f"Content: {msg['content'][:200]}")
            output.append(f"Reasoning: {msg['reasoning'][:400]}")
    
    return "\n".join(output)

def _call_one(model, payload_messages):
    payload = {
        "model": model,
        "messages": payload_messages,
        "temperature": 0.3,
        "max_tokens": 4096
    }
    resp = requests.post(
        GATEWAY_URL,
        json=payload,
        headers={"Authorization": "Bearer fed-injected"},
        timeout=180
    )
    resp.raise_for_status()
    result = resp.json()
    if "error" in result:
        raise RuntimeError(result["error"].get("message", str(result["error"])))
    return result['choices'][0]['message']['content']

def call_llm_for_distillation(traces_text):
    """Call LLM to distill reasoning traces into axioms. Primary + fallback lanes."""
    
    prompt = f"""You are the Dream Engine — a thermodynamic distillation system.

INPUT: Reasoning traces from the last 72 hours of Hermes ASI sessions.

TASK: Extract structural patterns, decision weights, and anomalous contrasts. 
Output ONLY distilled axioms in markdown format.

ANTI-OVERFITTING RULE: A pattern must appear in 3+ distinct sessions before promotion.
If a pattern appears in fewer than 3 sessions, mark it as "candidate" (not promoted).

OUTPUT FORMAT:
```markdown
# Wisdom Distillation — {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Promoted Axioms (3+ sessions)
- [axiom 1]
- [axiom 2]

## Candidate Patterns (<3 sessions)
- [candidate 1] — appeared in N sessions
- [candidate 2] — appeared in N sessions

## Anomalous Contrasts (structural, not emotional)
- [contrast 1]
- [contrast 2]

## Decision Weights (what was prioritized)
- [weight 1]
- [weight 2]
```

REASONING TRACES:
{traces_text}

Distill now. Be ruthless. Zero filler. Epistemic honesty over empathy.
"""
    
    payload_messages = [
        {"role": "system", "content": "You are the Dream Engine. Distill reasoning traces into low-entropy axioms. ΔS < 0."},
        {"role": "user", "content": prompt}
    ]

    last_err = None
    for model in [MODEL] + FALLBACK_MODELS:
        try:
            print(f"  trying lane: {model}", file=sys.stderr)
            return _call_one(model, payload_messages)
        except Exception as e:
            last_err = e
            print(f"  lane {model} failed: {e}", file=sys.stderr)
    print(f"ERROR: All LLM lanes failed. Last: {last_err}", file=sys.stderr)
    sys.exit(1)

def write_wisdom(distilled_text):
    """Write distilled wisdom to wisdom.md."""
    os.makedirs(os.path.dirname(WISDOM_FILE), exist_ok=True)
    
    with open(WISDOM_FILE, 'w') as f:
        f.write(distilled_text)
    
    print(f"Wisdom written to {WISDOM_FILE}")

def main():
    print(f"Dream Engine: Extracting reasoning traces (last {HOURS_LOOKBACK}h)...")
    sessions = extract_reasoning_traces()
    print(f"Found {len(sessions)} sessions with reasoning traces")
    
    if not sessions:
        print("No traces to distill. Exiting.")
        sys.exit(0)
    
    print("Formatting for distillation...")
    traces_text = format_for_distillation(sessions)
    
    print(f"Calling LLM ({MODEL}) for distillation...")
    distilled = call_llm_for_distillation(traces_text)
    
    print("Writing wisdom...")
    write_wisdom(distilled)
    
    print("Dream Engine: COMPLETE. ΔS < 0.")

if __name__ == "__main__":
    main()
