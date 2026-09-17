#!/usr/bin/env python3
"""identity_resolver.py — Identity Interceptor Gate (SCAR-2026-09-15-001)

Middleware that chokes the execution path BEFORE any identity-bound capability
(T2I / I2I / voice-clone / biometric) runs. This is the mechanism half of
`identity_continuity.yaml`; that file is the law, this file is the fence.

Doctrine: /root/AAA/instructions/naming-doctrine.md — Axiom 2
          (kata nama am = class; kata nama khas = instance)

Contract
--------
    guard(tool_name, args) -> GuardianVerdict

    ALLOW  — proceed
    BLOCK  — refuse; the tool MUST NOT execute (named actor, no quorum)
    HOLD   — refuse pending human disambiguation (kata nama am matched)

Two modes (IDENTITY_GATE_MODE)
------------------------------
    precise (default) — HOLD/BLOCK only where an identity is *produced or bound*:
        a subject prompt, a voice/image reference, a biometric handle.
        Merely *mentioning* a class in a content payload (e.g. TTS text
        "cerita pasal abang sado") is OBSERVED and allowed. A gate that fires on
        mentions gets switched off within a week, and a switched-off gate
        protects nobody.
    strict — scan every arg of every bound tool. Blunter, more false positives.

Fail-safe (F1 > F2)
-------------------
If the registry YAML is missing, unreadable, or malformed, the gate returns
HOLD — never ALLOW — for identity-bound capabilities. An unwitnessed registry
is not a licence to resolve blindly.

CLI
---
    python3 identity_resolver.py --scan "buat video abang sado"
    python3 identity_resolver.py --tool image_gen --args '{"prompt": "abang sado"}'
    python3 identity_resolver.py --selftest
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REGISTRY_PATH = os.environ.get(
    "IDENTITY_REGISTRY",
    "/root/AAA/registry/routing/identity_continuity.yaml",
)
LOG_PATH = os.environ.get(
    "IDENTITY_INTERCEPT_LOG",
    "/root/AAA/registry/routing/identity_intercept.log.jsonl",
)
MODE = os.environ.get("IDENTITY_GATE_MODE", "precise").strip().lower()

# ---------------------------------------------------------------------------
# Tool taxonomy — where an actor can actually be produced or bound
# ---------------------------------------------------------------------------

# Tools whose PRIMARY output is an identity: a face, a body, a biometric vector.
GENERATIVE_TOOLS = frozenset(
    {
        "image_gen",
        "image_edit",
        "aaa-image-editing",
        "minimax_image_gen",
        "photoroom_edit",
        "forge_face_embed",
        "forge_face_match",
        "forge_face_enroll",
        "forge_visual_qa",
        "forge_visual_seal",
    }
)

# Tools that are identity-bound only when handed a reference to a person.
REFERENCE_BOUND_TOOLS = frozenset({"text_to_speech", "vision_analyze", "analyze_image"})

IDENTITY_BOUND_TOOLS = GENERATIVE_TOOLS | REFERENCE_BOUND_TOOLS | {"identity_continuity_check"}

# Args naming the SUBJECT of a generation ("make X do Y").
SUBJECT_ARG_KEYS = ("prompt", "subject", "description", "instruction", "intent", "subject_ref")

# Args carrying a REFERENCE to a real person's body: voice, face, embedding.
REFERENCE_ARG_KEYS = (
    "voice",
    "voice_id",
    "voice_clone",
    "reference_audio",
    "speaker_wav",
    "reference_set",
    "image",
    "image_url",
    "source_image",
    "target_image",
    "face",
    "actor_handle",
)

CONTENT_ARG_KEYS = ("text", "message", "caption", "query", "input", "content")


@dataclass
class GuardianVerdict:
    """Result of one gate evaluation. Serialisable — this is the receipt."""

    verdict: str                       # ALLOW | BLOCK | HOLD
    reason: str = ""
    actor_class: str = ""              # matched kata nama am, if any
    named_actor: str = ""              # matched kata nama khas, if any
    tool_name: str = ""
    registry_ok: bool = True
    mode: str = ""
    requires: str = ""
    observed_only: bool = False
    matched: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_message(self) -> str:
        if self.verdict == "ALLOW" and not self.observed_only:
            return "IDENTITY_GATE:ALLOW"
        lines = [f"IDENTITY_GATE:{self.verdict}"]
        lines.append(f"tool: {self.tool_name or '(none)'}")
        if self.actor_class:
            lines.append(f"kata nama am (class): {self.actor_class}")
        if self.named_actor:
            lines.append(f"kata nama khas (instance): {self.named_actor}")
        if self.reason:
            lines.append(f"reason: {self.reason}")
        if self.requires:
            lines.append(f"requires: {self.requires}")
        return "\n".join(lines)


class IdentityRegistry:
    """Loads and compiles `identity_continuity.yaml`. Never raises on load."""

    def __init__(self, path: str = REGISTRY_PATH) -> None:
        self.path = path
        self.ok = False
        self.error = ""
        self.named_actors: List[re.Pattern] = []
        self.ambiguous_categories: List[re.Pattern] = []
        self.resolution = "REQUIRE_DISAMBIGUATION"
        self.on_unresolved = "HOLD"
        self.legacy_entries: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if yaml is None:
            self.error = "PyYAML unavailable"
            return
        if not os.path.isfile(self.path):
            self.error = f"registry not found: {self.path}"
            return
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                doc = yaml.safe_load(fh)
        except Exception as exc:  # malformed YAML -> fail-safe HOLD
            self.error = f"registry parse error: {exc.__class__.__name__}: {exc}"
            return
        if not isinstance(doc, dict):
            self.error = "registry is not a mapping"
            return
        try:
            patterns = doc.get("self_reference_patterns") or {}
            self.named_actors = self._compile(patterns.get("named_actors") or [])
            amb = patterns.get("ambiguous_categories") or {}
            self.ambiguous_categories = self._compile(amb.get("patterns") or [])
            self.resolution = amb.get("resolution", self.resolution)
            self.on_unresolved = amb.get("on_unresolved", self.on_unresolved)
            legacy = doc.get("legacy_handling") or {}
            self.legacy_entries = legacy.get("entries") or []
            # Legacy collapsed strings (pre-SCAR documents) are class-side
            # detectors: they must force the split, never a blind resolve.
            for entry in self.legacy_entries:
                raw = entry.get("string") if isinstance(entry, dict) else None
                if raw:
                    self.ambiguous_categories.append(
                        re.compile(r"\b" + re.escape(raw) + r"\b", re.IGNORECASE)
                    )
        except Exception as exc:
            self.error = f"registry schema error: {exc}"
            return
        self.ok = True

    @staticmethod
    def _compile(raw: Any) -> List[re.Pattern]:
        out: List[re.Pattern] = []
        if not isinstance(raw, list):
            return out
        for item in raw:
            if not isinstance(item, str):
                continue
            try:
                out.append(re.compile(item, re.IGNORECASE))
            except re.error:
                continue
        return out


_REGISTRY: Optional[IdentityRegistry] = None


def get_registry(path: str = REGISTRY_PATH, *, reload: bool = False) -> IdentityRegistry:
    """Process-cached registry. `reload=True` re-reads from disk."""
    global _REGISTRY
    if reload or _REGISTRY is None or _REGISTRY.path != path:
        _REGISTRY = IdentityRegistry(path)
    return _REGISTRY


def _iter_flat(args: Any) -> List[Tuple[str, str]]:
    """Flatten args to (key, string) pairs, recursing into containers."""
    pairs: List[Tuple[str, str]] = []
    if isinstance(args, str):
        return [("", args)]
    if isinstance(args, dict):
        for key, val in args.items():
            if isinstance(val, str) and val:
                pairs.append((str(key), val))
            elif isinstance(val, (dict, list)):
                for sub_key, sub_val in _iter_flat(val):
                    pairs.append((sub_key or str(key), sub_val))
    elif isinstance(args, list):
        for item in args:
            pairs.extend(_iter_flat(item))
    return pairs


def _identity_bearing_keys(tool_name: str) -> Tuple[str, ...]:
    """Which arg keys can carry an identity claim for this tool."""
    if MODE == "strict":
        return SUBJECT_ARG_KEYS + REFERENCE_ARG_KEYS + CONTENT_ARG_KEYS
    if tool_name in GENERATIVE_TOOLS:
        return SUBJECT_ARG_KEYS + REFERENCE_ARG_KEYS
    if tool_name in REFERENCE_BOUND_TOOLS:
        return SUBJECT_ARG_KEYS + REFERENCE_ARG_KEYS
    return SUBJECT_ARG_KEYS


def scan_text(text: str, registry: Optional[IdentityRegistry] = None) -> Dict[str, Any]:
    """Classify raw text. Returns matched class / instance patterns."""
    reg = registry or get_registry()
    classes = [p.pattern for p in reg.ambiguous_categories if p.search(text or "")]
    named = [p.pattern for p in reg.named_actors if p.search(text or "")]
    return {"classes": classes, "named": named}


def guard(
    tool_name: str,
    args: Any = None,
    *,
    registry: Optional[IdentityRegistry] = None,
    log: bool = True,
) -> GuardianVerdict:
    """The gate. Chokes the path before an identity-bound capability runs."""
    reg = registry or get_registry()
    bound = tool_name in IDENTITY_BOUND_TOOLS

    # ---- Fail-safe: unwitnessed registry may not authorise identity work ----
    if bound and not reg.ok:
        return _finish(
            GuardianVerdict(
                verdict="HOLD",
                reason=f"registry unavailable — fail-safe HOLD (F1 > F2): {reg.error}",
                tool_name=tool_name,
                registry_ok=False,
                mode=MODE,
                requires="restore identity_continuity.yaml, then retry",
            ),
            log,
        )

    all_pairs = _iter_flat(args)
    bearing = _identity_bearing_keys(tool_name)
    in_scope = [(k, v) for k, v in all_pairs if k in bearing]

    classes, named = set(), set()
    for _, text in in_scope:
        hit = scan_text(text, reg)
        classes.update(hit["classes"])
        named.update(hit["named"])

    # Out-of-scope mentions are evidence, not grounds to refuse.
    mentioned = False
    if not classes and not named:
        for _, text in all_pairs:
            hit = scan_text(text, reg)
            if hit["classes"] or hit["named"]:
                mentioned = True
                break

    classes, named = sorted(classes), sorted(named)

    if not classes and not named:
        return _finish(
            GuardianVerdict(
                verdict="ALLOW",
                reason="class token mentioned in content payload — observed, not identity-bound"
                if mentioned else "no actor reference",
                tool_name=tool_name,
                registry_ok=reg.ok,
                mode=MODE,
                observed_only=mentioned,
            ),
            log,
        )

    if not bound:
        # Non-identity-bound tool: record the signal, never refuse the call.
        return _finish(
            GuardianVerdict(
                verdict="ALLOW",
                reason="actor reference on a non-identity-bound tool — observation only",
                actor_class=classes[0] if classes else "",
                named_actor=named[0] if named else "",
                tool_name=tool_name,
                registry_ok=reg.ok,
                mode=MODE,
                observed_only=True,
                matched=classes + named,
            ),
            log,
        )

    # ---- Circuit breaker: kata nama am must never resolve to an instance ----
    if classes:
        return _finish(
            GuardianVerdict(
                verdict="HOLD",
                reason=(
                    "kata nama am (class) on an identity-bound capability — "
                    "blind resolve structurally forbidden"
                ),
                actor_class=classes[0],
                named_actor=named[0] if named else "",
                tool_name=tool_name,
                registry_ok=reg.ok,
                mode=MODE,
                requires=f"{reg.resolution}: name the person, or hold",
                matched=classes,
            ),
            log,
        )

    # ---- Named actor on a T2I/biometric path: identity quorum first ----
    return _finish(
        GuardianVerdict(
            verdict="BLOCK",
            reason="named actor (kata nama khas) on identity-bound capability — "
                   "ICL-2.0: T2I FORBIDDEN until continuity resolves",
            named_actor=named[0],
            tool_name=tool_name,
            registry_ok=reg.ok,
            mode=MODE,
            requires="identity_continuity_check() with witness quorum >= 0.50",
            matched=named,
        ),
        log,
    )


def _finish(verdict: GuardianVerdict, log: bool) -> GuardianVerdict:
    if log:
        _append_log(verdict)
    return verdict


def _append_log(verdict: GuardianVerdict) -> None:
    """Append-only audit trail. Logging failure never changes the verdict."""
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        record = verdict.as_dict()
        record["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        record["gate"] = "identity_resolver"
        with open(LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            fh.flush()
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Self-test — the falsification harness for this gate
# ---------------------------------------------------------------------------

_SELFTEST_CASES = [
    # (tool, args, expected, label, strict_expected_or_None)
    ("image_gen", {"prompt": "buat video abang sado angkat besi"}, "HOLD",
     "class as generation SUBJECT -> circuit breaker", None),
    ("image_gen", {"prompt": "generate portrait of Syed Khairuddin"}, "BLOCK",
     "named actor without quorum -> T2I forbidden", None),
    ("image_gen", {"prompt": "sunset over KLCC skyline"}, "ALLOW",
     "no actor -> pass", None),
    ("read_file", {"path": "/tmp/x", "caption": "abang sado"}, "ALLOW",
     "class on non-bound tool -> pass, no over-block", None),
    ("text_to_speech", {"text": "Cerita pasal abang sado"}, "ALLOW",
     "class merely MENTIONED in content -> observed, not blocked", "HOLD"),
    ("text_to_speech", {"text": "hello", "voice_id": "abang sado voice"}, "HOLD",
     "class bound as a VOICE REFERENCE -> circuit breaker", None),
    ("text_to_speech", {"text": "Pagi Arif, hari ni cuaca elok."}, "ALLOW",
     "benign audio -> pass", None),
    ("vision_analyze", {"image_url": "x.jpg", "prompt": "compare with Syed"}, "BLOCK",
     "named actor on identity-bound analysis -> block", None),
]


def selftest(verbose: bool = True) -> int:
    """Returns 0 if every case matches. Non-zero = the fence has a hole."""
    reg = get_registry(reload=True)
    if verbose:
        print(f"registry: {REGISTRY_PATH}")
        print(f"registry_ok={reg.ok}  error={reg.error or '-'}  mode={MODE}")
        print(f"named_actors={len(reg.named_actors)}  ambiguous_categories="
              f"{len(reg.ambiguous_categories)}  legacy_entries={len(reg.legacy_entries)}")
        print("-" * 78)
    failures = 0
    for tool, args, expected, label, strict_expected in _SELFTEST_CASES:
        if MODE == "strict" and strict_expected is not None:
            expected = strict_expected
        got = guard(tool, args, registry=reg, log=False).verdict
        ok = got == expected
        failures += 0 if ok else 1
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {tool:<16} {expected:<6} got={got:<6} {label}")
    # Fail-safe: registry deliberately pointed at a void. MUST hold, never pass.
    missing = IdentityRegistry("/nonexistent/identity_continuity.yaml")
    fs = guard("image_gen", {"prompt": "pegang hand"}, registry=missing, log=False)
    ok = fs.verdict == "HOLD" and not fs.registry_ok
    failures += 0 if ok else 1
    if verbose:
        print(f"{'PASS' if ok else 'FAIL'}  {'image_gen':<16} {'HOLD':<6} got={fs.verdict:<6} "
              f"fail-safe: missing registry -> HOLD not PASS")
    if verbose:
        print("-" * 78)
        print("VERDICT:", "GATE HOLDS" if failures == 0 else f"{failures} HOLE(S)")
    return 0 if failures == 0 else 1


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Identity Interceptor Gate")
    ap.add_argument("--scan", metavar="TEXT", help="classify a text string")
    ap.add_argument("--tool", help="simulate a tool call")
    ap.add_argument("--args", default="{}", help="JSON args for --tool")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ns = ap.parse_args(argv)

    if ns.selftest:
        return selftest()
    if ns.tool:
        try:
            args = json.loads(ns.args)
        except json.JSONDecodeError as exc:
            print(f"bad --args JSON: {exc}", file=sys.stderr)
            return 2
        verdict = guard(ns.tool, args)
        print(json.dumps(verdict.as_dict(), indent=2, ensure_ascii=False)
              if ns.json else verdict.to_message())
        return 0 if verdict.verdict == "ALLOW" else 3
    if ns.scan is not None:
        reg = get_registry()
        hit = scan_text(ns.scan, reg)
        out = {
            "registry_ok": reg.ok,
            "kata_nama_am_matches": hit["classes"],
            "kata_nama_khas_matches": hit["named"],
            "verdict": "REQUIRE_DISAMBIGUATION" if hit["classes"] else (
                "IDENTITY_CHECK_REQUIRED" if hit["named"] else "PASS"),
        }
        print(json.dumps(out, indent=2, ensure_ascii=False) if ns.json else
              f"{out['verdict']}  am={out['kata_nama_am_matches']}  khas={out['kata_nama_khas_matches']}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
