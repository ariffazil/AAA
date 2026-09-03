#!/usr/bin/env python3
"""
Dream Engine — 72-hour reasoning distillation for arifOS
Extracts internal reasoning traces from Arif DM sessions, distills into wisdom vectors,
applies 3-session threshold to prevent overfitting, outputs wisdom.md.

Constitutional constraints:
- Scope: Arif DM only (user_id=267378578, chat_type=dm)
- Threshold: Pattern must appear 3+ times across distinct sessions to become axiom
- Output: wisdom.md with timestamp, source session IDs, confidence score
- No injection — Arif reviews manually before kernel integration
"""

import sqlite3
import json
import time
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import requests

# Config
STATE_DB = "/root/.hermes/state.db"
WISDOM_DIR = Path("/root/AAA/knowledge-graph/dream-engine")
GATEWAY_URL = "http://100.64.0.2:4000/v1/chat/completions"
ARIF_USER_ID = "267378578"
WINDOW_HOURS = 72
MIN_SESSION_THRESHOLD = 3

# Distillation prompt
DISTILLATION_PROMPT = """You are a pattern-extraction engine for arifOS.

INPUT: Raw reasoning traces from Arif's DM sessions over the last 72 hours.

TASK:
1. Identify recurring structural patterns in the reasoning (not surface topics).
2. Focus on: decision weights, anomalous contrasts, proxy states, void operations.
3. Group similar patterns across sessions.
4. For each pattern, count how many DISTINCT sessions support it.
5. Apply threshold: only patterns appearing in 3+ sessions become axioms.

OUTPUT FORMAT (JSON):
{
  "axioms": [
    {
      "pattern": "concise structural observation",
      "confidence": 0.0-1.0,
      "session_count": N,
      "session_ids": ["id1", "id2"],
      "evidence": "one short supporting quote"
    }
  ],
  "metadata": {
    "window_start": "...",
    "window_end": "...",
    "total_sessions_analyzed": N,
    "total_reasoning_tokens": N
  }
}
Keep output under 2000 words. Max 10 axioms.

RULES:
- Zero filler. Zero empathy. Zero validation.
- Epistemic honesty: if pattern is weak, confidence < 0.7.
- Anomalous contrast = what was NOT said but structurally implied.
- Proxy state = when machine is used as psychological buffer.
- Void operation = decoding silence as primary data.

Return ONLY valid JSON. No markdown, no explanation."""

def extract_reasoning_traces():
    """Pull reasoning_content from Arif DM sessions in last 72h."""
    conn = sqlite3.connect(f"file:{STATE_DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    
    now = time.time()
    window_start = now - (WINDOW_HOURS * 3600)
    
    # Get sessions
    sessions = conn.execute('''
        SELECT id, title, started_at, message_count, reasoning_tokens
        FROM sessions
        WHERE user_id = ? AND chat_type = 'dm'
        AND started_at > ?
        ORDER BY started_at DESC
    ''', (ARIF_USER_ID, window_start)).fetchall()
    
    if not sessions:
        print("No Arif DM sessions in last 72h. Exiting.")
        return None
    
    # Extract reasoning from messages
    traces = []
    for s in sessions:
        messages = conn.execute('''
            SELECT role, content, reasoning_content, timestamp
            FROM messages
            WHERE session_id = ? AND reasoning_content IS NOT NULL
            AND LENGTH(reasoning_content) > 50
            ORDER BY timestamp ASC
        ''', (s['id'],)).fetchall()
        
        if messages:
            traces.append({
                'session_id': s['id'],
                'title': s['title'],
                'started_at': s['started_at'],
                'messages': [
                    {
                        'role': m['role'],
                        'content': m['content'][:200] if m['content'] else '',
                        'reasoning': m['reasoning_content'],
                        'timestamp': m['timestamp']
                    }
                    for m in messages
                ]
            })
    
    conn.close()
    
    print(f"Extracted {len(traces)} sessions with reasoning traces.")
    return {
        'window_start': datetime.fromtimestamp(window_start).isoformat(),
        'window_end': datetime.fromtimestamp(now).isoformat(),
        'sessions': traces,
        'total_sessions': len(sessions),
        'total_reasoning_tokens': sum(s['reasoning_tokens'] for s in sessions)
    }

def parse_llm_json(content):
    """Parse LLM JSON output with fence-stripping and bracket-finding."""
    content = content.strip()
    if content.startswith("```"):
        content = content.strip("`")
        content = content.split("\n", 1)[-1]
    start = content.find("{")
    end = content.rfind("}")
    if start >= 0 and end > start:
        content = content[start:end + 1]
    return json.loads(content)

def distill_with_llm(traces_data):
    """Send reasoning traces to LLM for pattern extraction."""
    if not traces_data or not traces_data['sessions']:
        return None
    
    # Prepare input for LLM — aggressively truncate to stay under token budget
    # Per-message reasoning: max 800 chars; per-session: max 10 messages
    for s in traces_data['sessions']:
        for m in s['messages']:
            if m['reasoning'] and len(m['reasoning']) > 800:
                m['reasoning'] = m['reasoning'][:400] + "\n...\n" + m['reasoning'][-400:]
        s['messages'] = s['messages'][:10]
    
    input_text = json.dumps(traces_data, indent=2, default=str)
    
    # If still too large, reduce to top 8 sessions
    if len(input_text) > 40000:
        print(f"Input still large ({len(input_text)} chars), reducing to 8 sessions.")
        traces_data['sessions'] = traces_data['sessions'][:8]
        for s in traces_data['sessions']:
            s['messages'] = s['messages'][:5]
            for m in s['messages']:
                if m['reasoning'] and len(m['reasoning']) > 400:
                    m['reasoning'] = m['reasoning'][:200] + "\n...\n" + m['reasoning'][-200:]
        input_text = json.dumps(traces_data, indent=2, default=str)
    
    print(f"Final input size: {len(input_text)} chars")
    
    payload = {
        "model": "forge-777",  # deepseek-v4-flash quota exhausted; forge-777 = sovereign lane
        "messages": [
            {"role": "system", "content": DISTILLATION_PROMPT},
            {"role": "user", "content": f"Distill these reasoning traces:\n\n{input_text}"}
        ],
        "temperature": 0.3,
        "max_tokens": 16000  # generous headroom; JSON must not be truncated mid-stream
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer fed-injected",  # haproxy injects real key (per AGENTS.md)
    }

    try:
        resp = requests.post(GATEWAY_URL, json=payload, headers=headers, timeout=420)
        resp.raise_for_status()
        result = resp.json()

        content = result['choices'][0]['message']['content']
        distilled = parse_llm_json(content)
        return distilled
    except Exception as e:
        print(f"ERROR: LLM distillation failed: {e}", file=sys.stderr)
        return None

def apply_threshold(distilled):
    """Filter axioms by 3-session threshold."""
    if not distilled or 'axioms' not in distilled:
        return []
    
    validated = []
    for axiom in distilled['axioms']:
        if axiom.get('session_count', 0) >= MIN_SESSION_THRESHOLD:
            validated.append(axiom)
    
    print(f"Applied threshold: {len(validated)}/{len(distilled['axioms'])} axioms passed 3-session rule.")
    return validated

def write_wisdom_md(axioms, metadata):
    """Write wisdom.md with validated axioms."""
    WISDOM_DIR.mkdir(parents=True, exist_ok=True)
    wisdom_path = WISDOM_DIR / "wisdom.md"
    
    now = datetime.now()
    
    content = f"""# Dream Engine — Wisdom Vectors
**Generated:** {now.isoformat()}
**Window:** {metadata['window_start']} → {metadata['window_end']}
**Sessions Analyzed:** {metadata.get('total_sessions', metadata.get('total_sessions_analyzed', 0))}
**Reasoning Tokens:** {metadata.get('total_reasoning_tokens', 0)}

---

## Validated Axioms (3+ session threshold)

"""
    
    if not axioms:
        content += "*No patterns met the 3-session threshold this cycle.*\n"
    else:
        for i, axiom in enumerate(axioms, 1):
            content += f"""### {i}. {axiom['pattern']}
- **Confidence:** {axiom.get('confidence', 0.0):.2f}
- **Sessions:** {axiom.get('session_count', 0)} ({', '.join(axiom.get('session_ids', []))})
- **Evidence:** `{str(axiom.get('evidence', ''))[:200]}`

"""
    
    content += f"""---

## Integration Protocol
1. Review axioms above.
2. If valid, inject into system prompt as `§ Dream Engine Wisdom`.
3. If invalid, delete or annotate with correction.
4. Next cycle: {(datetime.now() + timedelta(hours=WINDOW_HOURS)).isoformat()}

---
*DITEMPA BUKAN DIBERI ⚒️*
"""
    
    wisdom_path.write_text(content)
    print(f"Written: {wisdom_path}")
    return wisdom_path

def main():
    print("=" * 60)
    print("Dream Engine — 72h Reasoning Distillation")
    print("=" * 60)
    
    # Step 1: Extract
    print("\n[1/4] Extracting reasoning traces...")
    traces = extract_reasoning_traces()
    if not traces:
        print("No data. Exiting.")
        return
    
    # Step 2: Distill
    print("\n[2/4] Distilling with LLM...")
    distilled = distill_with_llm(traces)
    if not distilled:
        print("Distillation failed. Exiting.")
        return
    
    # Step 3: Threshold
    print("\n[3/4] Applying 3-session threshold...")
    axioms = apply_threshold(distilled)
    
    # Step 4: Write
    print("\n[4/4] Writing wisdom.md...")
    metadata = distilled.get('metadata', {
        'window_start': traces['window_start'],
        'window_end': traces['window_end'],
        'total_sessions': traces['total_sessions'],
        'total_reasoning_tokens': traces['total_reasoning_tokens']
    })
    write_wisdom_md(axioms, metadata)
    
    print("\n" + "=" * 60)
    print("COMPLETE. Review wisdom.md before kernel injection.")
    print("=" * 60)

if __name__ == "__main__":
    main()
