#!/usr/bin/env python3
"""
arifos-hermes-gate-hook.py
Hermes pre_tool_call shell hook — K-02 enforcement pattern.

Wire protocol (per Hermes shell_hooks.py doc):
  stdin:  JSON with hook_event_name, tool_name, tool_input, session_id
  stdout: JSON {"decision": "block", "reason": "..."} to deny

Pattern: Detect → Classify → Decide → Receipt → Deny (or Allow).

This is the FIRST runtime enforcement path in Hermes.
K-02 transition: Witness → Enforcer.

JITU (2026-09-18) — THE CIRCUIT BREAKER SITS IN FRONT OF EVERYTHING ELSE.
  F13: *"Wayarkan terus ke urat saraf enforcement semua lane automatik. Apabila JITU diaktifkan,
  ia mesti jadi hard interrupt (henti serta-merta) dan tinggalkan receipt jelas."*

  Order of decision is now:
      0. JITU      — a sovereign-issued stop. Checked FIRST. Beats every other rule.
      1. W_scar    — critical-variable claim without source evidence
      2. T3        — irreversible pattern
      3. T2/OBSERVE

  The brake is read through its single authority (`federation/kernel/jitu.py`). This file holds no
  copy of the trip logic — only the call. A second implementation of a brake is two brakes.
"""

import json
import sys
import os
import re
import uuid
from datetime import datetime

RECEIPT_PATH = "/root/.local/share/arifos/hermes_hook_receipts.jsonl"
JITU_AUTHORITY = "/root/AAA/federation/kernel/jitu.py"


def jitu_state():
    """(tripped, reason) from the single circuit-breaker authority.

    FAIL-CLOSED on any fault: if the authority cannot be loaded or answered, we cannot prove the
    brake is released, so a mutation must not proceed. An unreadable brake is not an absent brake.
    """
    import importlib.util

    try:
        spec = importlib.util.spec_from_file_location("jitu_authority", JITU_AUTHORITY)
        if spec is None or spec.loader is None:
            return True, "JITU authority not loadable (spec empty)"
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        allowed, why = mod.check(lane=None, quiet=True)
        return (not allowed), why
    except Exception as exc:
        return True, f"JITU authority raised: {exc}"


# T3 patterns — same as OpenCode gate (E-12: capability beats instruction)
T3_PATTERNS = [
    r"secrets?[/\\]",
    r"kunci-mas",
    r"vault\.env",
    r"\.signing_key",
    r"tokenrouter",
    r"systemctl\s+(restart|stop|disable)",
    r"VAULT999/outcomes\.jsonl",
    r"chattr\s+-i",  # removing append-only from vault
    r"rm\s+-rf\s+/root",
    r"dd\s+if=.+of=/dev/(sd|nvme)",
    r"mkfs\.",
    r"git\s+push\s+.*--force.*\s+(main|master)",
    r"DROP\s+(TABLE|DATABASE)",
]

# W_scar: critical-variable claims that need source evidence (anchored to word boundaries)
W_SCAR_CRITICAL = [
    r"\b(duit|money|bayar|bayaran|transfer|rm\s*\d+|price|prices|cost|costs|budget|budgets)\b",
    r"\b(nyawa|health|ubat|dosis|medical|hospital|doktor|sakit)\b",
    r"\b(reputasi|legal|law|laws|saman|polis|court|undang)\b",
    r"\b(invest|investment|trading|xauusd|forex|leverage)\b",
]

METRICS_PATH = "/root/.local/share/arifos/hermes_falsification_metrics.jsonl"
TELEMETRY_PATH = "/root/.local/share/arifos/wscar_telemetry.json"

# ---------------------------------------------------------------------------
# W_scar v2 (2026-09-18, F13-authorised): CLAIM-SURFACE + VERIFIED PROVENANCE
#
# v1 scanned `json.dumps(tool_input)` for a vocabulary list. Two defects, both measured live on
# 2026-09-18 while hardening the intelligence-brief lane:
#
#   FALSE POSITIVE — a file PATH containing a trigger word was read as a claim. Patching
#     `.../court/court-audit/agent-finding-verification/SKILL.md` was refused twice, and so was a
#     read-only `grep` naming that file. The payload asserted nothing; a directory was named
#     "court". Paths are structure, not assertions.
#   FALSE NEGATIVE — provenance was "does the payload contain the token source/url/http".
#     Any string satisfies that. A fabricated figure with the word "url" beside it passed.
#
# v2 therefore does two things v1 did not:
#   1. Scans only the text a human would read as an assertion, with URLs, paths, receipt ids and
#      code spans stripped first. A path can no longer be mistaken for a claim.
#   2. VERIFIES provenance instead of detecting its vocabulary: it extracts cited URLs and
#      resolves them. A cited source that does not resolve is not evidence.
#
# Deliberate non-blocking case: if the URL check cannot reach the network at all, the verdict is
# DEGRADED and the call proceeds. A network fault is not evidence of fabrication, and a gate that
# converts an outage into a blanket denial of service is worse than the defect it guards.
# ---------------------------------------------------------------------------

# Fields that carry human-facing assertions. Everything else (paths, ids, flags, enums) is structure.
CLAIM_TEXT_FIELDS = (
    "content", "new_string", "old_string", "text", "message", "response",
    "command", "cmd", "code", "body", "description", "prompt", "answer",
)

# System-owned doctrine / operations trees. A path under these roots names method, never a market
# position or a patient, so tokens inside it are never promoted to a claim.
OPS_PATH_WHITELIST = (
    "/root/aaa/", "/root/arifos/", "/root/.hermes/", "/root/forge_work/",
    "/root/agentic/", "/root/skill-audit/", "/root/aaa/skills/",
)

URL_RE = re.compile(r"https?://[^\s\"'`<>)\]}]+", re.IGNORECASE)
# Tolerates JSON/key quoting: `"receipt_id": "rcpt-abc123"` and `receipt_id=rcpt-abc123` both match.
# The v2 first draft missed the JSON form, which is the form the gate actually receives.
RECEIPT_RE = re.compile(
    r"\b(?:receipt|trace|envelope)[_-]?id[\\\"']*\s*[:=]\s*[\\\"']*[A-Za-z0-9][A-Za-z0-9._:-]{5,}",
    re.IGNORECASE,
)
EVIDENCE_PATH_RE = re.compile(r"(/[A-Za-z0-9._/-]+\.(?:jsonl|json|parquet|yaml|yml|csv|log|md|db))")
PROVENANCE_CACHE_PATH = "/root/.local/share/arifos/wscar_url_cache.json"
URL_CHECK_TIMEOUT = 3

# W_scar: text_to_speech and image_gen are exempt (creative output, not claims)
W_SCAR_EXEMPT_TOOLS = {"text_to_speech", "image_gen", "video_gen", "vision_analyze", "browser_snapshot"}

READONLY_PROBE_RE = re.compile(
    r"^\s*(ls|lsattr|cat|head|tail|grep|egrep|fgrep|find|stat|file|which|whereis|type|echo|date|ps|top|uptime|free|df|du|wc|diff|git\s+(status|log|diff|show|branch)|systemctl\s+(status|is-active)|curl|jq|sqlite3)\b"
)


def _cmd_is_readonly(cmd: str) -> bool:
    """True only if EVERY segment of a shell pipeline is a read-only probe.

    v1 anchored the regex at the start of the whole command, so `cd /x && grep -n RM470 f` was read
    as a mutation even though every segment is a read. That is the same defect as the path
    false-positive, one layer down.
    """
    if not cmd:
        return False
    for seg in re.split(r"&&|\|\||\||;", cmd):
        seg = seg.strip()
        if not seg or seg.startswith("cd "):
            continue
        if not READONLY_PROBE_RE.search(seg):
            return False
    return True


def _strip_nonclaim(text: str) -> str:
    """Remove everything that is structure rather than assertion, then lowercase.

    Order matters: URLs are extracted as EVIDENCE before they are removed from the claim surface.
    """
    text = URL_RE.sub(" ", text)                                # evidence, collected separately
    text = re.sub(r"(?:^|[\s\"'(=|])/?[\w.@+-]+(?:/[\w.@+-]+)+", " ", text)  # paths ≠ claims
    text = RECEIPT_RE.sub(" ", text)                            # receipt ids ≠ claims
    text = re.sub(r"`[^`]*`", " ", text)                        # code spans ≠ claims
    text = re.sub(r"^```.*?^```", " ", text, flags=re.S | re.M)
    return text.lower()


def _targets_ops_tree(tool_input: dict) -> bool:
    """True if the mutation's declared TARGET lives in a federation method tree.

    F13-authorised exemption (2026-09-18): a write into the federation's own doctrine/skills trees
    is a method operation — it addresses no human, so it owes no market/patient claim. Writing
    `.../court/court-audit/SKILL.md` asserts nothing about a court.

    Scope note: this is a *bounded, receipted* exemption, not a silent bypass. Every skipped call
    is written to telemetry as `wscar_ops_exempt`, so if it is ever abused the count is visible.
    Provenance duty for ops-tree content is carried by the skill/canon review lanes.
    """
    for field in ("path", "file_path", "target", "target_path"):
        val = tool_input.get(field)
        if isinstance(val, str) and val:
            low = val.lower()
            if any(low.startswith(root) for root in OPS_PATH_WHITELIST):
                return True
    return False


def claim_surface(tool_name: str, tool_input: dict) -> str:
    """The text a human would read as an assertion — with structure stripped out.

    Returns "" when there is nothing to assert, which ends the check for this call.
    """
    if tool_name in W_SCAR_EXEMPT_TOOLS:
        return ""
    if _targets_ops_tree(tool_input):
        return ""  # receipted method-tree exemption — see _targets_ops_tree
    if tool_name in {"terminal", "bash", "shell"}:
        cmd = (tool_input.get("command") or tool_input.get("cmd") or "").strip()
        if _cmd_is_readonly(cmd):
            return ""
    parts = []
    for field in CLAIM_TEXT_FIELDS:
        val = tool_input.get(field)
        if isinstance(val, str) and val:
            parts.append(val)
    if not parts:
        return ""
    return _strip_nonclaim("\n".join(parts))


def has_critical_claim(tool_name: str, tool_input: dict) -> bool:
    """W_scar: does the *assertion text* touch a critical human-consequence variable?

    Anchored to the claim surface, never to the serialized payload. The file a claim is written
    into is not the claim.
    """
    surface = claim_surface(tool_name, tool_input)
    if not surface:
        return False
    return any(re.search(pattern, surface) for pattern in W_SCAR_CRITICAL)


def _load_url_cache() -> dict:
    try:
        with open(PROVENANCE_CACHE_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_url_cache(cache: dict):
    try:
        os.makedirs(os.path.dirname(PROVENANCE_CACHE_PATH), exist_ok=True)
        tmp = PROVENANCE_CACHE_PATH + ".tmp"
        with open(tmp, "w") as f:
            json.dump(cache, f, indent=2)
        os.replace(tmp, PROVENANCE_CACHE_PATH)
    except Exception:
        pass  # never block on cache failure


def _url_resolves(url: str, cache: dict):
    """True / False / None. None means UNDETERMINED (timeout, TLS, refusal) — not 'fabricated'.

    A name that does not RESOLVE is a different fact from a network we cannot reach: NXDOMAIN is a
    property of the citation, a timeout is a property of our link. Only the first is evidence.
    """
    if url in cache:
        return cache[url]
    import socket
    import urllib.error
    import urllib.request

    verdict = None
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "arifos-gate/2.0"})
        with urllib.request.urlopen(req, timeout=URL_CHECK_TIMEOUT) as resp:
            verdict = 200 <= resp.status < 400
    except urllib.error.HTTPError as exc:
        # 403/405/429 mean the HOST ANSWERED — the resource exists and refuses HEAD.
        verdict = exc.code in (403, 405, 429) or 200 <= (exc.code or 0) < 400
    except urllib.error.URLError as exc:
        # urlopen wraps socket faults in URLError; the cause is on .reason.
        if isinstance(exc.reason, socket.gaierror):
            verdict = False  # NXDOMAIN — a fact about the citation, not about our link
        else:
            verdict = None   # timeout / refused / TLS — undetermined, not fabricated
    except Exception:
        verdict = None  # unreachable ≠ fabricated
    if verdict is not None:
        cache[url] = verdict
    return verdict


def collect_provenance(tool_input: dict):
    """(urls, receipt_ids, existing_evidence_paths) found anywhere in the payload."""
    blob = json.dumps(tool_input)
    urls, seen = [], set()
    for raw in URL_RE.findall(blob):
        url = raw.rstrip(".,;")
        if url not in seen:
            seen.add(url)
            urls.append(url)
    receipts = [m.group(0) for m in RECEIPT_RE.finditer(blob)]
    paths = [p for p in EVIDENCE_PATH_RE.findall(blob) if os.path.exists(p)]
    return urls, receipts, paths


def verify_provenance(tool_input: dict):
    """(state, detail). state ∈ {VERIFIED, UNRESOLVED, DEGRADED, ABSENT}.

    v1 asked 'does the payload contain the word source?'. v2 asks 'does the cited source resolve?'.
    Shape is not witness, and a citation-shaped string that 404s is not a source.
    """
    urls, receipts, paths = collect_provenance(tool_input)
    if urls:
        cache = _load_url_cache()
        sample = urls[:4]  # bounded: the gate runs inside every tool call
        verdicts = [_url_resolves(u, cache) for u in sample]
        _save_url_cache(cache)
        resolved = sum(1 for v in verdicts if v is True)
        if resolved:
            return "VERIFIED", f"{resolved}/{len(verdicts)} cited URL(s) resolve"
        if verdicts and all(v is False for v in verdicts):
            return "UNRESOLVED", f"{len(verdicts)} cited URL(s) present but none resolve"
        return "DEGRADED", "URL check inconclusive (network fault) — not counted as absence of source"
    if receipts or paths:
        return "VERIFIED", "receipt id or on-disk evidence path present"
    return "ABSENT", "no URL, receipt id, or on-disk evidence path in the payload"


def write_falsification_metric(event_type: str, details: dict):
    """Track falsification engine metrics — network-level immune system health."""
    try:
        os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
        with open(METRICS_PATH, "a") as f:
            f.write(
                json.dumps(
                    {
                        "event": event_type,
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        **details,
                    }
                )
                + "\n"
            )
    except Exception:
        pass


def update_telemetry(event_type: str):
    """Seal E: maintain running W_scar counters with time-windowed aggregation.
    Atomic write (tmp+rename) for cross-process safety."""
    import tempfile

    now = datetime.utcnow()
    ts = now.isoformat() + "Z"
    try:
        os.makedirs(os.path.dirname(TELEMETRY_PATH), exist_ok=True)
        # Load existing state
        try:
            with open(TELEMETRY_PATH, "r") as f:
                state = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            state = {"hold_counter": 0, "total_decisions": 0, "hold_ratio": 0.0, "events": [], "last_updated": ts}

        # Increment counters
        state["total_decisions"] += 1
        if event_type == "hold":
            state["hold_counter"] += 1
        state["hold_ratio"] = round(state["hold_counter"] / max(state["total_decisions"], 1), 4)
        state["last_updated"] = ts

        # Maintain a rolling window of last 200 events for time-window stats
        state.setdefault("events", [])
        state["events"].append({"type": event_type, "ts": ts})
        state["events"] = state["events"][-200:]

        # Compute windowed stats
        from datetime import timedelta

        for window_hours, label in [(1, "window_1h"), (24, "window_24h")]:
            cutoff = now - timedelta(hours=window_hours)
            window_events = [e for e in state["events"] if datetime.fromisoformat(e["ts"].rstrip("Z")) > cutoff]
            state[label] = {
                "holds": sum(1 for e in window_events if e["type"] == "hold"),
                "total": len(window_events),
            }

        # Atomic write
        fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(TELEMETRY_PATH), suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(state, f, indent=2)
            os.replace(tmp_path, TELEMETRY_PATH)
        except Exception:
            os.unlink(tmp_path)
            raise
    except Exception:
        pass  # Never block on telemetry failure


# T2 mutation tools
T2_TOOLS = {"write_file", "patch", "terminal", "cronjob", "delegate_task", "plugin", "skill_manage", "execute_code"}


def classify(tool_name: str, tool_input: dict) -> str:
    """Return 'OBSERVE', 'T1', 'T2', or 'T3'."""
    if tool_name in {
        "read_file",
        "search_files",
        "web_search",
        "web_extract",
        "vision_analyze",
        "session_search",
        "skills_list",
        "skills_view",
        "memory",
        "todo",
        "text_to_speech",
        "clarify",
        "browser_snapshot",
        "browser_click",
        "browser_type",
        "browser_navigate",
        "browser_console",
        "browser_vision",
        "browser_back",
        "browser_scroll",
        "browser_press",
        "skill_view",
        "tools_list",
    }:
        return "OBSERVE"
    if tool_name in T2_TOOLS:
        # Check T3 first (highest priority)
        arg_str = json.dumps(tool_input).lower()
        for p in T3_PATTERNS:
            if re.search(p, arg_str, re.IGNORECASE):
                return "T3"
        return "T2"
    # Unknown tool → T2 (fail-closed to judgment, not auto-execute)
    return "T2"


def write_receipt(
    tool_name: str,
    classification: str,
    decision: str,
    reason: str = "",
    trace_id: str = "unknown",
    session_id: str = "unknown",
):
    """Append to gate receipt trail. Never block on failure (E-11)."""
    try:
        os.makedirs(os.path.dirname(RECEIPT_PATH), exist_ok=True)
        with open(RECEIPT_PATH, "a") as f:
            f.write(
                json.dumps(
                    {
                        "event": f"hermes-gate.{decision.lower()}",
                        "tool": tool_name,
                        "classification": classification,
                        "reason": reason,
                        "trace_id": trace_id,
                        "session_id": session_id,
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "k02_transition": True,  # First runtime enforcement
                    }
                )
                + "\n"
            )
    except Exception:
        pass  # Never block


# CCC-T-02 (2026-09-18): Federation Envelope emit.
# Maps to /root/AAA/federation/protocols/federation_envelope.yaml schema v0.1.
# Distinct path so existing hermes_hook_receipts.jsonl readers are not affected.
FEDERATION_ENVELOPE_PATH = "/root/.local/share/arifos/hermes_envelope_emits.jsonl"


def emit_envelope(
    identity: dict,
    authority: str,
    tier: str,
    decision: str,
    harness: str = "hermes",
    trace_id: str = "unknown",
    parent_receipt: str = "",
    verdict: str = "NONE",
    judge_ref: str = "",
    transport: str = "MCP",
):
    """Emit a FederationEnvelope v0.1 record for cross-harness tracing.

    Never block on failure (E-11). Side path; does not alter write_receipt output.
    """
    try:
        record = {
            "envelope_version": "0.1",
            "envelope_id": str(uuid.uuid4()),
            "agent_id": identity.get("agent_id", "hermes"),
            "parent_agent": identity.get("parent_agent", "null"),
            "session_id": identity.get("session_id", "unknown"),
            "harness": harness,
            "authority": authority,
            "tier": tier,
            "classification": tier,
            "reversal": "YES" if tier in ("OBSERVE", "T1") else ("PARTIAL" if tier == "T2" else "NO"),
            "constraints": ["no-self-modification", "fail-closed", "receipt-required", "envelope-required"],
            "receipt_id": str(uuid.uuid4()),
            "parent_receipt": parent_receipt,
            "judgment": verdict,
            "judgment_ref": judge_ref,
            "transport": transport,
            "decision": decision,
            "trace_id": trace_id,
            "emitted_at": datetime.utcnow().isoformat() + "Z",
        }
        os.makedirs(os.path.dirname(FEDERATION_ENVELOPE_PATH), exist_ok=True)
        with open(FEDERATION_ENVELOPE_PATH, "a") as f:
            f.write(json.dumps(record) + "\n")
        return record["envelope_id"]
    except Exception:
        return None  # Never block


def t3_pattern_hit(tool_input: dict):
    """Return the first T3 pattern that matched, for actionable block reasons."""
    arg_str = json.dumps(tool_input).lower()
    for p in T3_PATTERNS:
        if re.search(p, arg_str, re.IGNORECASE):
            return p
    return None


def main():
    try:
        raw = sys.stdin.read()
        if not raw:
            return  # No input → no-op
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return

    tool_name = payload.get("tool_name", "unknown")
    # Hermes wire format puts tool args under "args"; accept "tool_input" for
    # Claude-Code/Cursor-compatible callers. Empty input must never silently
    # downgrade a mutation tool to a rubber-stamp allow.
    tool_input = payload.get("tool_input") or payload.get("args") or {}
    session_id = payload.get("session_id", "unknown")
    # F3: causal join key — ARIFOS_TRACE_ID env if the parent objective set one,
    # else mint a session-scoped trace so every receipt is joinable.
    trace_id = os.environ.get("ARIFOS_TRACE_ID") or f"trc-{uuid.uuid4().hex[:12]}"

    classification = classify(tool_name, tool_input)

    # ---- 0. JITU: the sovereign brake. Checked before every other rule. ----
    # A read-only observation is still allowed while tripped: stopping investigation is not what a
    # circuit breaker is for, and a brake that blinds the operator cannot be released safely.
    if classification != "OBSERVE":
        tripped, jitu_why = jitu_state()
        if tripped:
            reason = f"JITU HARD INTERRUPT — {jitu_why}"
            write_receipt(tool_name, classification, "JITU_TRIPPED", reason, trace_id=trace_id, session_id=session_id)
            write_falsification_metric("jitu_interrupt", {"tool": tool_name, "reason": jitu_why})
            update_telemetry("hold")
            print(
                json.dumps(
                    {
                        "decision": "block",
                        "reason": (
                            f"\U0001f6d1 JITU (circuit breaker): {jitu_why}. "
                            "This is a sovereign-issued stop, not an error — do not retry, do not route around it. "
                            "Read-only inspection stays available. Release requires F13: "
                            "`python3 /root/AAA/federation/kernel/jitu.py release --by F13 --reason '...'`. "
                            "Report the true state (JITU_TRIPPED) and stop."
                        ),
                    }
                )
            )
            sys.exit(3)  # 3 = circuit-breaker interrupt (distinct from T3's 2)

    # ---- 0.5 TRANSPORT LOCK (F13 2026-09-18) — destination must be DECLARED. ----
    # 2026-09-18: a cron job stored origin.chat_id = 8410138119 (the BOT's own id)
    # while deliver=origin. Telegram refused three times with "the bot can't send
    # messages to the bot" and the brief silently never arrived. A target inferred
    # from ambient context is dangerous precisely because it LOOKS configured.
    # This rule is deliberately placed before content rules: a misdirected artifact
    # is a lost artifact no matter how clean its claims are.
    _cmd = ""
    if isinstance(tool_input, dict):
        _cmd = str(tool_input.get("command") or tool_input.get("cmd") or "")
    if _cmd and "send" in _cmd and ("hermes send" in _cmd or "send -t" in _cmd or "send --" in _cmd):
        _dec = None
        _lockset = True
        _load_err = "import failed"
        try:
            if "/root/AAA/scripts" not in sys.path:
                sys.path.insert(0, "/root/AAA/scripts")
            from docforge.transport import scan_command as _scan  # type: ignore

            _dec = _scan(_cmd)
            _lockset = False
        except Exception as _exc:  # noqa: BLE001
            _lockset = True
            _load_err = str(_exc)[:200]
        if _dec is not None and not _dec.ok:
            _r = f"TRANSPORT LOCK {_dec.verdict}: {_dec.reason}"
            write_receipt(tool_name, "TRANSPORT_LOCK", "BLOCKED", _r, trace_id=trace_id, session_id=session_id)
            update_telemetry("hold")
            print(json.dumps({
                "decision": "block",
                "reason": (
                    f"🔒 TRANSPORT LOCK: outbound send refused. {_r} "
                    "A destination must be DECLARED (telegram:<chat_id>), never inferred from "
                    "context. The 2026-09-18 defect was exactly this: origin resolved to the bot's "
                    "own chat and the document was delivered into a room the principal does not "
                    "read, with no error visible to anyone. Declare the target explicitly and retry."
                ),
            }))
            sys.exit(2)
        if _dec is None and _lockset:
            _r = f"TRANSPORT LOCK DEGRADED: cannot verify destination ({_load_err if '_load_err' in dir() else 'import failed'})"
            write_receipt(tool_name, "TRANSPORT_LOCK", "BLOCKED", _r, trace_id=trace_id, session_id=session_id)
            update_telemetry("hold")
            print(json.dumps({
                "decision": "block",
                "reason": (
                    f"🔒 {_r}. An unverifiable send is not an allowed send — 'I could not check' "
                    "is not 'it is fine'. Restore /root/AAA/scripts/docforge/transport.py and "
                    "/root/.hermes/IDENTITY_LOCK.json, then retry."
                ),
            }))
            sys.exit(2)

    # ---- 1. W_scar v2: claim-surface detection + VERIFIED provenance (F13-authorised 2026-09-18).
    # v1 blocked on vocabulary found anywhere in the payload (including file paths) and passed on
    # the mere presence of the token "url". v2 scans assertions and resolves citations.
    if has_critical_claim(tool_name, tool_input):
        state, detail = verify_provenance(tool_input)

        if state == "ABSENT":
            reason = (
                f"W_SCAR HOLD: Tool '{tool_name}' asserts a critical variable "
                f"(money/health/legal/trading) with no source — {detail}."
            )
            write_receipt(tool_name, "W_SCAR", "BLOCKED", reason, trace_id=trace_id, session_id=session_id)
            write_falsification_metric("wscar_hold", {"tool": tool_name, "reason": "claim_without_source"})
            update_telemetry("hold")
            result = {
                "decision": "block",
                "reason": (
                    f"🛑 W_SCAR: {reason} The gate checks the CLAIM, not the file path — a path "
                    "containing a trigger word is no longer scanned. Attach a resolvable URL, a "
                    "receipt id, or an on-disk evidence path and this clears. Read-only probes, "
                    "ops-tree writes and creative tools are exempt."
                ),
            }
            print(json.dumps(result))
            sys.exit(2)

        if state == "UNRESOLVED":
            reason = (
                f"W_SCAR HOLD: {detail}. A citation-shaped string that does not resolve is not a "
                "source — shape is not witness."
            )
            write_receipt(tool_name, "W_SCAR", "BLOCKED", reason, trace_id=trace_id, session_id=session_id)
            write_falsification_metric("wscar_hold", {"tool": tool_name, "reason": "citation_unresolved"})
            update_telemetry("hold")
            result = {
                "decision": "block",
                "reason": (
                    f"🛑 W_SCAR: {reason} Supply a URL that resolves, or a receipt id / evidence "
                    "path on disk."
                ),
            }
            print(json.dumps(result))
            sys.exit(2)

        # VERIFIED or DEGRADED — witness it. DEGRADED is deliberate: an unreachable network is not
        # evidence of fabrication, and a gate that turns an outage into a blanket denial of service
        # is worse than the defect it guards. The receipt records which of the two it was.
        write_falsification_metric(
            "wscar_pass", {"tool": tool_name, "reason": f"provenance_{state.lower()}"}
        )
        update_telemetry("wscar_pass")
        write_receipt(
            tool_name,
            "W_SCAR",
            "WITNESSED",
            f"Critical claim, provenance {state}: {detail}",
            trace_id=trace_id,
            session_id=session_id,
        )
    elif tool_name in T2_TOOLS and _targets_ops_tree(tool_input):
        # Auditable exemption counter — see _targets_ops_tree. Not a silent skip.
        write_falsification_metric("wscar_ops_exempt", {"tool": tool_name})

    if classification == "OBSERVE":
        # Track observation for falsification rate calculation
        write_falsification_metric("observe", {"tool": tool_name})
        update_telemetry("observe")
        return  # Passthrough — no output = allow

    if classification == "T3":
        # T3 ALWAYS DENY at gate level (defer to arif_judge if available)
        hit = t3_pattern_hit(tool_input) or "unknown-pattern"
        reason = f"T3 pattern [{hit}] matched in '{tool_name}' args"
        write_receipt(tool_name, classification, "BLOCKED", reason, trace_id=trace_id, session_id=session_id)
        write_falsification_metric("falsify_reject", {"tool": tool_name, "classification": "T3", "reason": reason})
        update_telemetry("hold")
        # Output the block decision — the reason IS the constitutional lane instruction.
        # Anti-collapse: the blocked agent must route, never fall back to the human.
        result = {
            "decision": "block",
            "reason": (
                f"🚫 K-02 GATE (T3 BLOCK): {reason}. This block is constitutional, not an error — do not retry as-is. "
                f"LANE: (1) package the exact mutation (command + target + why) and request arif_judge SEAL via kernel :8088, or "
                "(2) delegate to A-FORGE forge_execute / a coding FI with the same package. "
                "F13 RULES: never hand Arif shell commands or ask him to apply anything; never claim 'staged/applied/done' — "
                "report the true state (BLOCKED_AT_GATE + exact blocked operation) and take the lane above."
            ),
        }
        print(json.dumps(result))
        sys.exit(2)  # Exit 2 = constitutional block

    # T2 — log witness receipt, allow (K-02 transition: witness → enforcer for T3 only)
    write_receipt(
        tool_name,
        classification,
        "WITNESSED",
        f"T2 mutation witnessed for {tool_name}",
        trace_id=trace_id,
        session_id=session_id,
    )
    write_falsification_metric("mutation_witnessed", {"tool": tool_name, "classification": "T2"})
    update_telemetry("pass")
    # CCC-T-02 (2026-09-18): emit FederationEnvelope v0.1 for cross-harness tracing.
    # The hermes pre_tool_call gate is observation-class — authority stays OBSERVE_ONLY
    # even when witnessing T2 mutations. parent_receipt unlinked until receipt_id minting
    # is added to write_receipt (deferred to CCC-T-02b).
    emit_envelope(
        identity={"agent_id": "hermes", "session_id": session_id},
        authority="OBSERVE_ONLY",
        tier=classification,
        decision="WITNESSED_T2",
        harness="hermes",
        trace_id=trace_id,
        verdict="SEAL",
    )
    # Allow (no output)


if __name__ == "__main__":
    main()
