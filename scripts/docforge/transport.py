#!/usr/bin/env python3
"""docforge.transport — destination verification before any send leaves the box.

THE BUG THIS EXISTS FOR (proven, not theorised)
  Gateway log, three times on 2026-09-18:

      Queued-lane final send to 8410138119 failed:
      Forbidden: the bot can't send messages to the bot

  8410138119 is the bot's OWN id (IDENTITY_LOCK.bots.hermes.id). A cron job had
  origin.chat_id = 8410138119 while origin.user_id = 267378578. Delivering with
  `deliver: origin` would resolve to the bot's own id, Telegram refuses, and the
  brief never arrives. The failure is a WARNING in a log nobody reads — from the
  reader's side it is indistinguishable from "the system is quiet today".

  That is the worst class of failure: a scheduled promise that silently stops
  being kept.

WHY THE ALLOWED SET IS READ, NOT HARDCODED
  Hardcoding `telegram:267378578` into a gate makes the gate wrong the moment a
  human's id changes, and a wrong gate that cannot be checked is worse than no
  gate. The authority is /root/.hermes/IDENTITY_LOCK.json — it already declares
  which ids are humans, which are groups, and which are bots. This module READS
  that file and fails CLOSED if it cannot.

  Fail-closed matters here: if the lock is unreadable, we do not know whether a
  target is a bot, so we must not send. "I could not verify" is not "it is fine".

THREE OUTCOMES, NOT TWO
  ALLOW   destination verified against the lock
  HOLD    destination is provably wrong (a bot id, or an unlisted id)
  DEGRADED the lock could not be read — refuse to send, state the reason
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

LOCK_PATH = Path("/root/.hermes/IDENTITY_LOCK.json")

# a target is "<platform>:<id>" or "<platform>:<id>:<thread>"
TARGET_RE = re.compile(r"^(?P<platform>[a-z0-9_]+):(?P<id>-?\d+)(?::(?P<thread>\d+))?$")

# Outbound-send shapes that must be intercepted BEFORE execution. A send whose
# destination never appears still gets verified — see scan_command().
_SEND_PATTERNS = (
    re.compile(r"\bhermes\s+send\b[^\n]*?(?:-t|--to)\s+([^\s'\"]+)"),
    re.compile(r"\bhermes\s+send\b[^\n]*?--target[= ]([^\s'\"]+)"),
)


@dataclass
class Decision:
    verdict: str            # ALLOW | HOLD | DEGRADED
    target: str
    reason: str
    resolved_id: str = ""
    role: str = ""

    @property
    def ok(self) -> bool:
        return self.verdict == "ALLOW"

    def __str__(self) -> str:
        return f"[{self.verdict}] {self.target} — {self.reason}"


def load_lock(path: Path = LOCK_PATH) -> dict | None:
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def _classification(lock: dict) -> dict[str, tuple[str, str]]:
    """id -> (kind, role). Built from the lock file, not from memory."""
    out: dict[str, tuple[str, str]] = {}
    for name, rec in (lock.get("humans") or {}).items():
        uid = str(rec.get("telegram_user_id") or "").strip()
        if uid:
            out[uid] = ("human", name)
    for name, gid in (lock.get("groups") or {}).items():
        gid = str(gid).strip()
        if gid:
            out[gid] = ("group", name)
    for name, rec in (lock.get("bots") or {}).items():
        bid = str(rec.get("id") or "").strip()
        if bid:
            out[bid] = ("bot", name)
    return out


def verify(target: str, *, expect_role: str | None = "arif",
           lock_path: Path = LOCK_PATH) -> Decision:
    """Verify one destination before dispatch.

    expect_role: which human this send is FOR. Defaults to arif because an
    accidental cross-send to Syed (or the reverse) is the mirror of the bot bug:
    a correct-looking id aimed at the wrong person.
    """
    lock = load_lock(lock_path)
    if lock is None:
        return Decision("DEGRADED", target,
                        f"cannot read the identity lock at {lock_path} — "
                        "without it a bot id cannot be distinguished from a "
                        "human id, so the send is refused rather than guessed")

    m = TARGET_RE.match(target.strip())
    if not m:
        # bare "origin", "local", "all", a channel name, etc. — none of these
        # are verifiable destinations, so none may carry a delivery
        hint = ("bare name, not a verifiable destination — resolve it to "
                "platform:id first")
        return Decision("HOLD", target, hint)

    platform, tid, thread = m.group("platform"), m.group("id"), m.group("thread")
    if platform != "telegram":
        return Decision("DEGRADED", target,
                        f"platform {platform!r} has no entry in the identity lock; "
                        "only telegram ids are verifiable here")

    cls = _classification(lock)
    kind, role = cls.get(tid, ("unknown", ""))

    if kind == "bot":
        return Decision("HOLD", target,
                        f"{tid} is the BOT {role!r} own id — Telegram refuses with "
                        "'the bot can't send messages to the bot'. This is the "
                        "2026-09-18 silent-delivery defect.",
                        resolved_id=tid, role=role)

    if kind == "unknown":
        known = ", ".join(sorted(cls))[:200]
        return Decision("HOLD", target,
                        f"{tid} appears in no human/group/bot entry of the lock; "
                        f"known ids: {known}", resolved_id=tid)

    if kind == "human" and expect_role and role != expect_role:
        return Decision("HOLD", target,
                        f"{tid} is human {role!r} but this send expects {expect_role!r} "
                        "— a correctly-formed id aimed at the wrong person",
                        resolved_id=tid, role=role)

    extra = f" (thread {thread})" if thread else ""
    return Decision("ALLOW", target,
                    f"verified {kind} {role!r}{extra}",
                    resolved_id=tid, role=role)


def scan_command(command: str, *, expect_role: str | None = "arif",
                 lock_path: Path = LOCK_PATH) -> Decision | None:
    """Inspect a shell command string for an outbound send with a bad destination.

    For the pre-tool-call hook. Returns None when the command is not an outbound
    send — the overwhelmingly common case, which must stay cheap and silent.

    A send with NO resolvable destination returns a HOLD rather than None: an
    absent target is not a clean command, it is an unverifiable one.
    """
    if not command or "send" not in command:
        return None
    for pat in _SEND_PATTERNS:
        m = pat.search(command)
        if m:
            return verify(m.group(1), expect_role=expect_role, lock_path=lock_path)
    if re.search(r"\bhermes\s+send\b", command):
        return Decision("HOLD", "", "outbound send with no explicit destination "
                                    "— the target cannot be verified, so the send "
                                    "cannot be allowed")
    return None


def scan_origins(jobs_path: Path = Path("/root/.hermes/cron/jobs.json"),
                 lock_path: Path = LOCK_PATH) -> list[dict]:
    """Systemic sweep: any job whose stored origin id is a bot id.

    This is the batch version of the same defect. It runs over the whole
    scheduler so the next instance is found before it fires, not after a reader
    notices a quiet week.
    """
    lock = load_lock(lock_path)
    if lock is None:
        return [{"job_id": "?", "name": "?", "verdict": "DEGRADED",
                 "reason": f"identity lock unreadable at {lock_path}"}]
    bot_ids = {str(r.get("id")) for r in (lock.get("bots") or {}).values() if r.get("id")}

    try:
        d = json.loads(jobs_path.read_text())
    except Exception as exc:
        return [{"job_id": "?", "name": "?", "verdict": "DEGRADED",
                 "reason": f"jobs file unreadable: {exc}"}]

    jobs = d if isinstance(d, list) else d.get("jobs", d)
    items = jobs.items() if isinstance(jobs, dict) else [(j.get("id"), j) for j in jobs]

    findings = []
    for k, v in items:
        deliver = str(v.get("deliver") or "")
        origin = v.get("origin") or {}
        ocid = str(origin.get("chat_id") or "")
        enabled = bool(v.get("enabled"))

        if not enabled:
            continue

        if deliver == "origin" and ocid in bot_ids:
            findings.append({
                "job_id": k, "name": v.get("name"), "verdict": "HOLD",
                "reason": f"deliver=origin resolves to origin.chat_id={ocid}, "
                          f"which is a BOT id — this job cannot deliver",
            })
        elif deliver.startswith("telegram:"):
            dec = verify(deliver, expect_role=None, lock_path=lock_path)
            if not dec.ok:
                findings.append({
                    "job_id": k, "name": v.get("name"), "verdict": dec.verdict,
                    "reason": dec.reason,
                })
    return findings
