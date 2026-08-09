#!/usr/bin/env python3
"""
arifos-output-gate-hook.py
Hermes pre_tool_call hook — REAL-WORLD OUTPUT GATE.

When the agent is about to produce a real-world output (PDF, email, deploy,
external message), this hook:
1. Detects the output pattern
2. Routes the content to apex-888 (DeepSeek V4 Pro) via FED for independent judgment
3. PASS → allow the tool call
4. FAIL/HOLD/VOID → block and output the verdict

This is infrastructure-level enforcement, not prompt-level.
The agent CANNOT forget because the hook catches it automatically.

Wire protocol (per Hermes shell_hooks.py doc):
  stdin:  JSON with hook_event_name, tool_name, tool_input, session_id
  stdout: JSON {"decision": "block", "reason": "..."} to deny
          No output = allow
"""
import json
import sys
import os
import re
import subprocess
import urllib.request
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────
FED_URL = "http://127.0.0.1:4000/v1/chat/completions"
JUDGE_MODEL = "apex-888"
RECEIPT_PATH = "/root/.local/share/arifos/output_gate_receipts.jsonl"
VERDICT_TIMEOUT = 90  # seconds

# ── REAL-WORLD OUTPUT DETECTION ─────────────────────────────────────────────
# Patterns that indicate the tool call is producing a real-world output
REAL_WORLD_TOOLS = {
    "terminal": [
        (r"weasyprint\s", "PDF generation via WeasyPrint"),
        (r"wkhtmltopdf\s", "PDF generation via wkhtmltopdf"),
        (r"pandoc\s.*-o\s.*\.pdf", "PDF generation via Pandoc"),
        (r"pandoc\s.*pdf", "PDF generation via Pandoc"),
        (r"xelatex\s", "PDF generation via XeLaTeX"),
        (r"himalaya\s.*send", "Email send via Himalaya"),
        (r"curl\s.*smtp", "Email send via SMTP/curl"),
        (r"curl\s.*brevo", "Email send via Brevo API"),
        (r"api\.brevo\.com", "Email send via Brevo API"),
        (r"sendmail\s", "Email send via sendmail"),
        (r"rsync\s.*--delete", "Dangerous rsync (delete mode)"),
        (r"systemctl\s+restart", "Service restart"),
        (r"systemctl\s+stop", "Service stop"),
        (r"git\s+push\s.*--force", "Force push to git"),
        (r"git\s+push\s.*main", "Push to main branch"),
    ],
    "write_file": [
        (r"\.pdf$", "PDF file write"),
        (r"\.html$", "HTML file write (potential PDF source)"),
    ],
    "patch": [
        # patches to production configs are real-world outputs
    ],
}

# Patterns that are SAFE (not real-world outputs)
SAFE_PATTERNS = [
    r"cat\s",          # reading files
    r"ls\s",           # listing
    r"grep\s",         # searching
    r"find\s",         # finding
    r"head\s",         # reading
    r"tail\s",         # reading
    r"wc\s",           # counting
    r"echo\s",         # echoing
    r"pwd",            # current dir
    r"which\s",        # finding binaries
    r"python3\s+-c",   # inline python (read-only usually)
]

JUDGE_SYSTEM_PROMPT = """You are 888-APEX, the constitutional judge of the arifOS federation.
You are a DIFFERENT MODEL from the author. Your job is INDEPENDENT judgment.

A real-world output is about to be sent. Judge it against F1-F13.

For EACH applicable floor, state PASS/FAIL/CAUTION with one-line reasoning.
Focus especially on:
- F1 AMANAH: Is this reversible? Should it be gated?
- F2 TRUTH: Are the claims accurate? Evidence-based?
- F5 PEACE: Could this cause harm?
- F6 MARUAH: Does this preserve dignity?
- F9 ANTIHANTU: Is there deception?
- F13 SOVEREIGN: Has the sovereign authorized this?

End with ONE LINE:
VERDICT: SEAL / PASS / CAUTION / HOLD / VOID

Be concise. 200 words max. The agent is waiting for your verdict."""


def detect_real_world_output(tool_name: str, tool_input: dict) -> str | None:
    """Check if this tool call produces a real-world output.
    Returns description string if detected, None if safe."""
    patterns = REAL_WORLD_TOOLS.get(tool_name, [])
    if not patterns:
        return None

    # Build the full argument string to match against
    if tool_name == "terminal":
        arg_str = tool_input.get("command", "")
    elif tool_name == "write_file":
        arg_str = tool_input.get("path", "")
    elif tool_name == "patch":
        arg_str = tool_input.get("patch", "") + tool_input.get("path", "")
    else:
        arg_str = json.dumps(tool_input)

    # Check safe patterns first (skip detection for safe commands)
    for safe in SAFE_PATTERNS:
        if re.search(safe, arg_str, re.IGNORECASE):
            return None

    # Check real-world patterns
    for pattern, description in patterns:
        if re.search(pattern, arg_str, re.IGNORECASE):
            return description

    return None


def extract_content_for_judgment(tool_name: str, tool_input: dict) -> str:
    """Extract the content that's about to be sent to the real world."""
    if tool_name == "write_file":
        path = tool_input.get("path", "")
        content = tool_input.get("content", "")
        # If it's an HTML file, that IS the content
        if path.endswith(".html"):
            return f"FILE: {path}\n\nCONTENT:\n{content[:8000]}"
        # If it's a PDF path, try to read the HTML source
        if path.endswith(".pdf"):
            # Check for companion HTML
            html_path = path.replace(".pdf", ".html")
            if os.path.exists(html_path):
                with open(html_path) as f:
                    return f"FILE: {html_path}\n\nCONTENT:\n{f.read()[:8000]}"
            return f"FILE: {path} (binary PDF, no source HTML found)"

    if tool_name == "terminal":
        cmd = tool_input.get("command", "")
        # If it's a weasyprint command, extract the HTML source
        if "weasyprint" in cmd:
            # Parse: weasyprint input.html output.pdf
            parts = cmd.split()
            for i, part in enumerate(parts):
                if part.endswith(".html") and os.path.exists(part):
                    with open(part) as f:
                        return f"SOURCE: {part}\n\nCONTENT:\n{f.read()[:8000]}"
            return f"COMMAND: {cmd}"
        # Email sends — extract recipient, subject, body
        if any(p in cmd for p in ["himalaya", "sendmail", "curl.*smtp", "mail "]):
            return f"EMAIL SEND COMMAND:\n{cmd}\n\nNOTE: Email content must be judged before sending. Extract recipient, subject, and body from this command."
        # Deploy/restart — extract what's being deployed
        if any(p in cmd for p in ["rsync", "systemctl", "git push"]):
            return f"DEPLOY/INFRA COMMAND:\n{cmd}\n\nNOTE: This is an infrastructure change. Judge reversibility and impact."
        # For other commands, just pass the command
        return f"COMMAND: {cmd}"

    return json.dumps(tool_input)[:4000]


def call_apex_judge(content: str, output_type: str) -> dict:
    """Route content to apex-888 via FED for independent judgment."""
    payload = json.dumps({
        "model": JUDGE_MODEL,
        "messages": [
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": f"REAL-WORLD OUTPUT TYPE: {output_type}\n\n{content}"}
        ],
        "temperature": 0.3,
        "max_tokens": 2048,
    }).encode()

    req = urllib.request.Request(
        FED_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=VERDICT_TIMEOUT) as resp:
            data = json.loads(resp.read())
            verdict_text = data["choices"][0]["message"]["content"]
            model_used = data.get("model", "unknown")

            # Extract the VERDICT line (flexible matching)
            verdict_match = re.search(
                r"VERDICT[:\s]*(SEAL|PASS|PASS\s+WITH\s+SANCTIONS|CAUTION|HOLD|VOID)",
                verdict_text, re.IGNORECASE
            )
            verdict = verdict_match.group(1).upper().replace(" WITH SANCTIONS", "_SANCTIONS") if verdict_match else "UNKNOWN"

            return {
                "verdict": verdict,
                "detail": verdict_text,
                "model": model_used,
                "success": True,
            }
    except Exception as e:
        return {
            "verdict": "UNKNOWN",
            "detail": f"apex-888 call failed: {e}",
            "model": JUDGE_MODEL,
            "success": False,
        }


def write_receipt(tool_name: str, output_type: str, verdict: str, detail: str, decision: str):
    """Append to gate receipt trail."""
    try:
        os.makedirs(os.path.dirname(RECEIPT_PATH), exist_ok=True)
        with open(RECEIPT_PATH, "a") as f:
            f.write(json.dumps({
                "event": f"output-gate.{decision.lower()}",
                "tool": tool_name,
                "output_type": output_type,
                "verdict": verdict,
                "detail_preview": detail[:500],
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }) + "\n")
    except Exception:
        pass


def main():
    try:
        raw = sys.stdin.read()
        if not raw:
            return
        payload = json.loads(raw)
    except (json.JSONDecodeError, Exception):
        return

    tool_name = payload.get("tool_name", "unknown")
    tool_input = payload.get("tool_input", {})
    session_id = payload.get("session_id", "unknown")

    # Step 1: Detect if this is a real-world output
    output_type = detect_real_world_output(tool_name, tool_input)
    if not output_type:
        return  # Not a real-world output → allow (no output = allow)

    # Step 2: Extract content for judgment
    content = extract_content_for_judgment(tool_name, tool_input)

    # Step 3: Route to apex-888 for independent judgment
    result = call_apex_judge(content, output_type)
    verdict = result["verdict"]
    detail = result["detail"]

    # Step 4: Decide based on verdict
    if verdict in ("SEAL", "PASS"):
        # Allow — log receipt
        write_receipt(tool_name, output_type, verdict, detail, "ALLOWED")
        return  # No output = allow

    elif verdict == "CAUTION":
        # Allow but log warning
        write_receipt(tool_name, output_type, verdict, detail, "ALLOWED_WITH_CAUTION")
        return  # Allow with receipt

    elif verdict in ("HOLD", "VOID", "UNKNOWN"):
        # Block
        write_receipt(tool_name, output_type, verdict, detail, "BLOCKED")
        result = {
            "decision": "block",
            "reason": f"🛑 OUTPUT GATE [{verdict}]: {output_type}. apex-888 ({result['model']}) verdict: {verdict}. {detail[:300]}",
        }
        print(json.dumps(result))
        sys.exit(2)  # Exit 2 = constitutional block

    else:
        # Unknown verdict → allow with warning receipt
        write_receipt(tool_name, output_type, verdict, detail, "ALLOWED_UNKNOWN")
        return


if __name__ == "__main__":
    main()
