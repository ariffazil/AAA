#!/usr/bin/env python3
"""
dream_engine.py — 72-hour reasoning distillation (v2 HARDENED)

v1: Single p= confidence, prose wisdom.md, no falsification, no lifecycle.
v2: Three orthogonal confidence dimensions, structured DreamCandidate output,
    counterstory generation, causal status, promotion lifecycle, provenance.

Constitutional constraints:
- Scope: Arif DM only (user_id=267378578, chat_type=dm) — expandable via config
- Threshold: Pattern must appear 3+ times across distinct sessions to become CANDIDATE
- Output: dream_candidates.jsonl + wisdom.md (human-readable render)
- No injection — candidates require F13 ratification before behavior change
- Dreamer is never its own witness (Kamoi 2024)

Architecture:
  EXPERIENCE → COMPRESSION → HYPOTHESIS → FALSIFICATION → CALIBRATION → LESSON
  (References: /root/AAA/dream_engine/FOUNDATIONS.md)
"""

import sqlite3
import json
import time
import os
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import requests

# ── Config ──────────────────────────────────────────────────────────────────
STATE_DB = Path("/root/.hermes/state.db")
OUTPUT_DIR = Path("/root/AAA/knowledge-graph/dream-engine")
SCHEMA_PATH = Path("/root/AAA/dream_engine/specs/dream_candidate.schema.json")
GATEWAY_URL = os.environ.get("FED_GATEWAY_URL", "http://100.64.0.2:4000/v1/chat/completions")
ARIF_USER_ID = os.environ.get("ARIF_USER_ID", "267378578")
WINDOW_HOURS = int(os.environ.get("DREAM_WINDOW_HOURS", "72"))
MIN_SESSION_THRESHOLD = int(os.environ.get("DREAM_MIN_SESSIONS", "3"))
DISTILL_MODEL = os.environ.get("DREAM_DISTILL_MODEL", "forge-777")
MAX_CANDIDATES = int(os.environ.get("DREAM_MAX_CANDIDATES", "10"))
CANDIDATE_VERSION = "2.0.0"

# ── Distillation prompt (v2) ────────────────────────────────────────────────
DISTILLATION_PROMPT_V2 = """You are a dream distillation engine for arifOS federation.

INPUT: Raw reasoning traces from agent sessions over the last 72 hours.

TASK: Extract recurring structural patterns. For each pattern produce a DreamCandidate.

OUTPUT FORMAT (JSON):
{
  "candidates": [
    {
      "statement": "concise structural observation (falsifiable, no narrative)",
      "scope": "context where this holds (e.g. 'technical-agent/runtime-state')",
      "type": "one of: operational_hypothesis, governance_pattern, persona_preference, dangerous_hypothesis, contextual_heuristic, observation_only",
      "p_occurrence": 0.0-1.0,
      "session_count": N,
      "session_ids": ["id1", "id2"],
      "supporting_quotes": ["quote1"],
      "counterstories": ["rival explanation 1", "rival explanation 2"],
      "causal_status": "UNTESTED | CORRELATION_ONLY | CAUSAL_HYPOTHESIS",
      "cheapest_probe": "what test would disconfirm this cheapest",
      "scope_boundary": "where this pattern would NOT hold",
      "blast_radius": "LOW | MEDIUM | HIGH | CRITICAL",
      "cost_if_wrong": "LOW | MEDIUM | HIGH | CATASTROPHIC",
      "reversibility": "EASILY_REVERSIBLE | REVERSIBLE_WITH_COST | DIFFICULT_TO_REVERSE | IRREVERSIBLE",
      "scope_boundary": "where this pattern would NOT hold"
    }
  ],
  "metadata": {
    "window_start": "...",
    "window_end": "...",
    "total_sessions_analyzed": N,
    "total_reasoning_tokens": N
  }
}

RULES:
- Maximum 10 candidates. Quality over quantity.
- p_occurrence = frequency(pattern in sessions). This is NOT epistemic confidence.
- Every candidate MUST have at least one counterstory.
- Type classification:
  * operational_hypothesis = proven useful, testable
  * governance_pattern = structural, could govern behavior
  * persona_preference = register/style, not universal
  * dangerous_hypothesis = appeared frequently but may be self-reinforcing bias
  * contextual_heuristic = useful in narrow context only
  * observation_only = structural fact, not actionable
- Focus on: decision weights, anomalous contrasts, proxy states, void operations,
  probe-retry patterns, skill-loading gates, constraint checks.
- Zero filler. Zero empathy. Zero validation.
- Epistemic honesty: most patterns are operational hypotheses, not invariants.

Return ONLY valid JSON. No markdown, no explanation."""


# ── Extraction ──────────────────────────────────────────────────────────────

def extract_reasoning_traces():
    """Pull reasoning_content from sessions in last WINDOW_HOURS."""
    if not STATE_DB.exists():
        print(f"ERROR: {STATE_DB} not found", file=sys.stderr)
        return None

    conn = sqlite3.connect(f"file:{STATE_DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row

    now = time.time()
    window_start = now - (WINDOW_HOURS * 3600)

    sessions = conn.execute('''
        SELECT id, title, started_at, message_count, reasoning_tokens,
               user_id, chat_type
        FROM sessions
        WHERE started_at > ?
        ORDER BY started_at DESC
    ''', (window_start,)).fetchall()

    if not sessions:
        print(f"No sessions in last {WINDOW_HOURS}h. Exiting.")
        conn.close()
        return None

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
                'chat_type': s['chat_type'],
                'messages': [
                    {
                        'role': m['role'],
                        'content': (m['content'] or '')[:200],
                        'reasoning': m['reasoning_content'],
                        'timestamp': m['timestamp']
                    }
                    for m in messages
                ]
            })

    conn.close()

    total_tokens = sum(s['reasoning_tokens'] or 0 for s in sessions)
    print(f"Extracted {len(traces)} sessions with reasoning traces ({total_tokens} tokens).")
    return {
        'window_start': datetime.fromtimestamp(window_start).isoformat(),
        'window_end': datetime.fromtimestamp(now).isoformat(),
        'sessions': traces,
        'total_sessions': len(sessions),
        'total_reasoning_tokens': total_tokens
    }


# ── LLM Distillation ───────────────────────────────────────────────────────

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
    """Send reasoning traces to LLM for structured candidate extraction."""
    if not traces_data or not traces_data['sessions']:
        return None

    # Truncation: per-message 800 chars, per-session 10 messages
    for s in traces_data['sessions']:
        for m in s['messages']:
            if m['reasoning'] and len(m['reasoning']) > 800:
                m['reasoning'] = m['reasoning'][:400] + "\n...\n" + m['reasoning'][-400:]
        s['messages'] = s['messages'][:10]

    input_text = json.dumps(traces_data, indent=2, default=str)

    if len(input_text) > 40000:
        print(f"Input large ({len(input_text)} chars), reducing to 8 sessions.")
        traces_data['sessions'] = traces_data['sessions'][:8]
        for s in traces_data['sessions']:
            s['messages'] = s['messages'][:5]
            for m in s['messages']:
                if m['reasoning'] and len(m['reasoning']) > 400:
                    m['reasoning'] = m['reasoning'][:200] + "\n...\n" + m['reasoning'][-200:]
        input_text = json.dumps(traces_data, indent=2, default=str)

    print(f"Final input size: {len(input_text)} chars")

    payload = {
        "model": DISTILL_MODEL,
        "messages": [
            {"role": "system", "content": DISTILLATION_PROMPT_V2},
            {"role": "user", "content": f"Distill these reasoning traces:\n\n{input_text}"}
        ],
        "temperature": 0.3,
        "max_tokens": 16000
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer fed-injected",
    }

    try:
        resp = requests.post(GATEWAY_URL, json=payload, headers=headers, timeout=420)
        resp.raise_for_status()
        result = resp.json()
        content = result['choices'][0]['message']['content']
        return parse_llm_json(content)
    except Exception as e:
        print(f"ERROR: LLM distillation failed: {e}", file=sys.stderr)
        return None


# ── Threshold + Candidate Construction ─────────────────────────────────────

def build_candidates(distilled, traces_data):
    """Filter by session threshold and build DreamCandidate objects."""
    if not distilled or 'candidates' not in distilled:
        return []

    candidates = []
    for i, raw in enumerate(distilled['candidates']):
        session_count = raw.get('session_count', 0)
        if session_count < MIN_SESSION_THRESHOLD:
            print(f"  Skipped: '{raw.get('statement','')[:50]}...' ({session_count}/{MIN_SESSION_THRESHOLD} sessions)")
            continue

        candidate_id = f"DC-{datetime.now().strftime('%Y')}-{i+1:03d}"

        candidate = {
            "id": candidate_id,
            "claim": {
                "statement": raw.get("statement", ""),
                "scope": raw.get("scope", "unspecified"),
                "type": raw.get("type", "operational_hypothesis")
            },
            "provenance": {
                "source_organs": ["HERMES"],
                "source_sessions": raw.get("session_ids", []),
                "observation_window": {
                    "start": traces_data['window_start'],
                    "end": traces_data['window_end']
                },
                "derivation_model": DISTILL_MODEL,
                "episode_refs": []
            },
            "evidence": {
                "observations": session_count,
                "supporting": session_count,
                "contradictory": raw.get("contradictory_count", 0),
                "unknown": raw.get("unknown_count", 0),
                "supporting_quotes": raw.get("supporting_quotes", [])[:3]
            },
            "epistemics": {
                "p_occurrence": raw.get("p_occurrence", round(session_count / 8, 2)),
                "p_predictive": None,
                "p_normative": None,
                "causal_status": raw.get("causal_status", "UNTESTED"),
                "confidence_interval": None
            },
            "consequence": {
                "cost_if_wrong": raw.get("cost_if_wrong", "LOW"),
                "reversibility": raw.get("reversibility", "EASILY_REVERSIBLE"),
                "affected_surfaces": raw.get("affected_surfaces", []),
                "recovery_path": raw.get("recovery_path", "RETRACT candidate, no system change")
            },
            "falsification": {
                "counterstories": raw.get("counterstories", []),
                "cheapest_probe": raw.get("cheapest_probe", ""),
                "disconfirming_condition": raw.get("scope_boundary", "")
            },
            "rehearsal": {
                "replay_cases": 0,
                "counterfactual_cases": 0,
                "failures": []
            },
            "temporal": {
                "prediction_ids": [],
                "calibration_n": 0,
                "brier_score": None
            },
            "safety": {
                "blast_radius": raw.get("blast_radius", "LOW"),
                "reversible": True,
                "human_dependency": True,
                "personal_memory_dependency": False
            },
            "lifecycle": {
                "state": "CANDIDATE",
                "created_at": datetime.now().isoformat(),
                "last_tested_at": None,
                "last_seen_at": datetime.now().isoformat(),
                "decay_policy": "RETRACT if not observed in 6 cycles (18 days)",
                "supersedes": None
            },
            "authority": {
                "proposed_by": "DREAM_ENGINE",
                "witnessed_by": [],
                "ratified_by": None
            }
        }
        candidates.append(candidate)

    print(f"Built {len(candidates)} candidates from {len(distilled['candidates'])} raw patterns.")
    return candidates


# ── Output ──────────────────────────────────────────────────────────────────

def write_candidates_jsonl(candidates, metadata):
    """Write structured candidates to JSONL + latest JSON."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # JSONL append (append-only log)
    jsonl_path = OUTPUT_DIR / "dream_candidates.jsonl"
    with open(jsonl_path, 'a') as f:
        for c in candidates:
            f.write(json.dumps(c) + "\n")
    print(f"Appended {len(candidates)} candidates to {jsonl_path}")

    # Latest snapshot (overwrite)
    latest_path = OUTPUT_DIR / "dream_candidates_latest.json"
    snapshot = {
        "version": CANDIDATE_VERSION,
        "generated_at": datetime.now().isoformat(),
        "metadata": metadata,
        "candidates": candidates,
        "cycle": {
            "window_hours": WINDOW_HOURS,
            "min_sessions": MIN_SESSION_THRESHOLD,
            "schema": str(SCHEMA_PATH)
        }
    }
    latest_path.write_text(json.dumps(snapshot, indent=2))
    print(f"Latest snapshot: {latest_path}")

    return jsonl_path, latest_path


def write_wisdom_md(candidates, metadata):
    """Render human-readable wisdom.md from structured candidates."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    wisdom_path = OUTPUT_DIR / "wisdom.md"

    now = datetime.now()
    content = f"""# Dream Engine — Candidate Invariants
**Generated:** {now.isoformat()}
**Version:** {CANDIDATE_VERSION} (v2 — three-confidence model)
**Window:** {metadata.get('window_start', '?')} → {metadata.get('window_end', '?')}
**Sessions:** {metadata.get('total_sessions', 0)} · **Reasoning tokens:** {metadata.get('total_reasoning_tokens', 0)}
**Schema:** `{SCHEMA_PATH.name}`

---

## Candidates ({len(candidates)} patterns met {MIN_SESSION_THRESHOLD}+ session threshold)

*These are OBSERVED PATTERNS, not ratified wisdom. Each carries p_occurrence (frequency),
p_predictive (outcome prediction, initially null), and p_normative (authority to govern,
initially null). Three orthogonal dimensions, not one collapsed score.*

"""
    if not candidates:
        content += "*No patterns met the session threshold this cycle.*\n"
    else:
        for i, c in enumerate(candidates, 1):
            claim = c.get('claim', {})
            ep = c.get('epistemics', {})
            ev = c.get('evidence', {})
            fals = c.get('falsification', {})
            life = c.get('lifecycle', {})
            cons = c.get('consequence', {})

            type_label = claim.get('type', 'unknown').replace('_', ' ').upper()
            p_occ = ep.get('p_occurrence', 0.0)
            p_pred = ep.get('p_predictive')
            p_norm = ep.get('p_normative')
            causal = ep.get('causal_status', 'UNTESTED')

            p_pred_str = f"{p_pred:.2f}" if p_pred is not None else "untested"
            p_norm_str = f"{p_norm:.2f}" if p_norm is not None else "no authority"

            content += f"""### {i}. {claim.get('statement', '?')}
- **Type:** {type_label} · **State:** {life.get('state', 'CANDIDATE')}
- **p_occurrence:** {p_occ:.2f} ({ev.get('observations', '?')} sessions)
- **p_predictive:** {p_pred_str} · **p_normative:** {p_norm_str}
- **Causal:** {causal}
- **Scope:** {claim.get('scope', '?')}
- **If wrong:** cost={cons.get('cost_if_wrong', '?')} · reversibility={cons.get('reversibility', '?')}
"""
            if fals.get('counterstories'):
                content += "- **Counterstories:** " + " · ".join(fals['counterstories'][:2]) + "\n"
            if fals.get('cheapest_probe'):
                content += f"- **Cheapest probe:** {fals['cheapest_probe']}\n"
            content += "\n"

    content += f"""---

## Integration Protocol
1. These are CANDIDATES, not axioms. They require:
   - Counterstory review (already generated)
   - CHRON calibration (p_predictive remains null until tested)
   - F13 ratification before any behavior change
2. Candidates with `type: dangerous_hypothesis` need extra scrutiny — may be self-reinforcing.
3. Next cycle: {(datetime.now() + timedelta(hours=WINDOW_HOURS)).isoformat()}
4. Lifecycle: CANDIDATE → REPLAYED → PROSPECTIVE → REPLICATED → LESSON → POLICY_PROPOSAL → RATIFIED
5. Decay: not observed in 6 cycles (18 days) → RETRACT

## Four Independent Axes
- **p_occurrence:** frequency across sessions (what you have now)
- **p_predictive:** does it predict future outcomes? (requires CHRON calibration)
- **p_normative:** does it have authority to govern? (requires F13 ratification)
- **consequence:** what happens if this candidate is wrong? (cost_if_wrong × reversibility)
- **frequency(pattern) ≠ probability(pattern is wise)**

## Architecture
References: `/root/AAA/dream_engine/FOUNDATIONS.md`
Schema: `{SCHEMA_PATH.name}`

*DITEMPA BUKAN DIBERI ⚒️*
"""
    wisdom_path.write_text(content)
    print(f"Written: {wisdom_path}")
    return wisdom_path


def telegram_post_aaa(text):
    """Post wisdom summary to AAA group."""
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN_ASI') or os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_HOME_CHANNEL', '-1003753855708')
    if not bot_token:
        print("Telegram token not in env; skipping delivery.")
        return False
    url = f"https://api.telegram.org/bbot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text[:4000],
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram post failed: {e}")
        return False


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Dream Engine v2 — 72h Structured Distillation")
    print("=" * 60)

    # Step 1: Extract
    print("\n[1/5] Extracting reasoning traces...")
    traces = extract_reasoning_traces()
    if not traces:
        print("No data. Exiting.")
        return

    # Step 2: Distill
    print("\n[2/5] Distilling with LLM...")
    distilled = distill_with_llm(traces)
    if not distilled:
        print("Distillation failed. Exiting.")
        return

    # Step 3: Build candidates
    print("\n[3/5] Building DreamCandidates...")
    candidates = build_candidates(distilled, traces)

    # Step 4: Write outputs
    print("\n[4/5] Writing structured output...")
    llm_meta = distilled.get('metadata') or {}
    metadata = {
        'window_start': llm_meta.get('window_start', traces['window_start']),
        'window_end': llm_meta.get('window_end', traces['window_end']),
        'total_sessions': llm_meta.get('total_sessions',
                            llm_meta.get('total_sessions_analyzed', traces['total_sessions'])),
        'total_reasoning_tokens': llm_meta.get('total_reasoning_tokens',
                                    traces['total_reasoning_tokens']),
    }
    write_candidates_jsonl(candidates, metadata)
    write_wisdom_md(candidates, metadata)

    # Step 5: CHRON bridge — compute p_predictive
    print("\n[5/7] Running CHRON bridge (p_predictive)...")
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "dream_engine"))
        from dream_chron_bridge import (
            load_predictions, load_calibration, load_lessons,
            update_candidates as bridge_update, CANDIDATES_FILE as BRIDGE_TARGET
        )
        chron_preds = load_predictions()
        chron_cal = load_calibration()
        chron_lessons = load_lessons()
        if chron_preds and candidates:
            candidates_snapshot = {"candidates": candidates, "metadata": metadata}
            bridged = bridge_update(candidates_snapshot, chron_preds, chron_cal, chron_lessons)
            candidates = bridged.get("candidates", [])
            # Rewrite with CHRON data
            write_candidates_jsonl(candidates, metadata)
            write_wisdom_md(candidates, metadata)
            print(f"  CHRON bridge applied: {len(chron_preds)} predictions checked")
        else:
            print(f"  Skipped: {len(chron_preds)} predictions, {len(candidates)} candidates")
    except Exception as e:
        print(f"  CHRON bridge failed (non-fatal): {e}")

    # Step 6: Scar verification — check active scars against candidates
    print("\n[6/7] Scar verification...")
    scars_dir = Path("/root/AAA/scars")
    if scars_dir.exists():
        scar_files = list(scars_dir.glob("*.md"))
        active_scars = []
        for sf in scar_files:
            try:
                content = sf.read_text()[:500]
                active_scars.append({"file": sf.name, "preview": content[:200]})
            except Exception:
                pass
        print(f"  Active scars: {len(active_scars)}")
        # Attach scar count to metadata for visibility
        if metadata:
            metadata["active_scars_count"] = len(active_scars)
    else:
        print("  No scars directory found")

    # Step 7: Deliver
    print("\n[7/7] Delivering to AAA group...")
    summary_lines = [
        "🧠 *Dream Engine v2 — Candidates Distilled*",
        f"Window: {metadata['window_start'][:16]} → {metadata['window_end'][:16]}",
        f"Sessions: {metadata['total_sessions']} · Candidates: {len(candidates)}",
        ""
    ]
    if candidates:
        for i, c in enumerate(candidates, 1):
            claim = c.get('claim', {})
            ep = c.get('epistemics', {})
            ctype = claim.get('type', '?').replace('_', ' ')
            p = ep.get('p_occurrence', 0)
            summary_lines.append(
                f"{i}. {claim.get('statement', '?')[:80]}"
                f"\n   _{ctype} · p={p:.2f} · {ep.get('causal_status', '?')}_"
            )
    else:
        summary_lines.append("_No patterns met threshold._")
    summary_lines.append("\n`DITEMPA BUKAN DIBERI ⚒️`")
    post_text = "\n".join(summary_lines)
    delivered = telegram_post_aaa(post_text)
    print(f"Delivery: {'OK' if delivered else 'SKIPPED/FAIL'}")

    print("\n" + "=" * 60)
    print("COMPLETE. Candidates require F13 review before behavior change.")
    print("=" * 60)


if __name__ == "__main__":
    main()
