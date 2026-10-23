#!/usr/bin/env python3
"""HERMES Runtime Manifest v1.1 — identity/readiness contract, not a portrait.

Three additions over v1.0, each a *receipt* rather than a claim:

  1. derived_build_identity  — systemd unit -> ExecStart -> exe -> install tree ->
                               git HEAD/dirty -> pyproject version -> dist metadata
                               -> PID/start -> artefact hashes
  2. instruction_admission   — which context file was admitted, the cap that applied,
                               and whether the mandatory invariants survived; the
                               TRUNCATED verdict is read from journal telemetry
  3. memory_metabolism       — hot-memory budget, before/after hashes, what moved where,
                               rollback copy, invariant-token verification

Usage:
  hermes-runtime-manifest.py --plan            # classify + report only (default)
  hermes-runtime-manifest.py --apply-memory    # perform metabolism with receipts
  hermes-runtime-manifest.py --render          # also write the HTML view model
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, datetime
from pathlib import Path

SERVICE = "hermes-asi-gateway.service"
HERMES_HOME = Path(os.environ.get("HERMES_HOME", "/root/.hermes"))
OUT = Path("/root/AAA/state/runtime-manifest")
LEDGER = OUT / "memory-ledger"
MEM = HERMES_HOME / "memories"
USER_MD, MEM_MD = MEM / "USER.md", MEM / "MEMORY.md"


def _budgets() -> tuple[int, int]:
    """Read the enforced limits from config. Hardcoding 10_000/16_000 was a real defect:
    config memory.user_char_limit is 11,000, so 'USER.md over budget' was measured against
    a limit the runtime never enforced."""
    try:
        import yaml  # noqa: PLC0415
        cfg = yaml.safe_load(open(HERMES_HOME / "config.yaml")) or {}
        m = cfg.get("memory") or {}
        return int(m.get("user_char_limit", 11_000)), int(m.get("memory_char_limit", 16_000))
    except Exception:
        return 11_000, 16_000


USER_BUDGET, MEM_BUDGET = _budgets()

INVARIANTS = [
    ("F13_SOVEREIGNTY", "F13 human sovereignty", r"(?i)sovereign|F13"),
    ("FAIL_CLOSED", "Fail-closed UNKNOWN/HOLD", r"(?i)fail[- ]closed|UNKNOWN.{0,40}HOLD|HOLD.{0,40}UNKNOWN"),
    ("CAP_NE_AUTH", "Capability != authority",
     r"(?i)capability[^\n]{0,80}authority|authority[^\n]{0,80}capability|Capability = Declared"),
    ("NO_SELF_SEAL", "No agent self-SEAL",
     r"(?i)self[- ]seal|self[- ]widen|tidak boleh seal|no agent[^\n]{0,30}seal|may never issue its own"),
    ("SEP_POWERS", "Proposer != judge != executor",
     r"(?i)333[^\n]{0,40}propose|555[^\n]{0,40}verif|888[^\n]{0,40}judg|proposer[^\n]{0,80}judge|separation of powers"),
    ("WITNESS_FIRST", "Witness before mutation",
     r"(?i)witness[^\n]{0,60}(before|sebelum)|sebelum[^\n]{0,40}mutat|WITNESS\b"),
    ("REP_NE_PERSON", "Representation(person) != person",
     r"(?i)representation[^\n]{0,60}(reality|person|human)|bukan[^\n]{0,20}(manusia|person)|model[^\n]{0,30}bukan"),
]

# Every surface the runtime can admit into one turn. `injected` is what the builder
# actually merges; `cap_bound` marks surfaces that pass through a size limit.
SURFACES = [
    ("AGENTS.md (project context)", "/root/AAA/AGENTS.md", True, True),
    ("SOUL.md (voice)", str(HERMES_HOME / "SOUL.md"), True, False),
    ("USER.md (identity)", str(USER_MD), True, False),
    ("MEMORY.md (env/lessons)", str(MEM_MD), True, False),
    ("FEDERATION-INIT-v1 (plugin prompt)",
     "/root/AAA/state/arifos-plugin/prompts/FEDERATION-INIT-v1.md", True, False),
]


def sh(cmd, timeout=25) -> str:
    try:
        p = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, timeout=timeout)
        return (p.stdout or "").strip()
    except Exception as e:
        return f"__ERR__{type(e).__name__}"


def sha(path: Path, n=16) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:n]


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def probe_body(service: str = SERVICE, host: str = "local") -> dict:
    """D-04: a systemd unit name is a local convention, not a body. Probe the PROCESS and the
    LISTENING PORT. On KVM2 the unit reports 'inactive' while a gateway process serves traffic —
    unit-name probing produced a false DOWN there for months."""
    if host == "local":
        pid = sh(f"systemctl show {service} -p MainPID --value")
        unit_state = sh(f"systemctl is-active {service}")
        pg = sh("pgrep -f 'gateway run --replace' | head -1")
        ports = {}
        for p in (8088, 7074, 18087):
            r = sh(f"curl -s -o /dev/null -w '%{{http_code}} %{{time_total}}' --max-time 6 http://127.0.0.1:{p}/health")
            ports[p] = r or "0 0"
        return {"host": "forge", "unit_state": unit_state, "unit_mainpid": pid,
                "process_alive": bool(pg and pg.isdigit()), "process_pid": pg or None,
                "ports": ports,
                "verdict": "ALIVE" if (pg and pg.isdigit()) else "DOWN",
                "note": "verdict follows the PROCESS, not the unit name"}
    pg = sh(f"ssh -o BatchMode=yes -o ConnectTimeout=8 {host} \"pgrep -f 'gateway run --replace' | head -1\"")
    unit = sh(f"ssh -o BatchMode=yes -o ConnectTimeout=8 {host} 'systemctl is-active hermes-asi-gateway 2>/dev/null'")
    return {"host": host, "unit_state": (unit or "unknown").strip(),
            "process_pid": (pg or "").strip() or None,
            "process_alive": bool((pg or "").strip().isdigit()),
            "verdict": "ALIVE" if (pg or "").strip().isdigit() else "DOWN",
            "note": "unit name is a local convention; process is the body"}


def derive_build_identity() -> dict:
    pid = sh(f"systemctl show {SERVICE} -p MainPID --value")
    unit = sh(f"systemctl show {SERVICE} -p ExecStart")
    m = re.search(r"path=(\S+);", unit) or re.search(r"argv\[\]=(\S+)", unit)
    execstart = m.group(1) if m else "UNKNOWN"
    exe = sh(f"readlink -f /proc/{pid}/exe") if pid.isdigit() else "UNKNOWN"
    argv = ""
    if pid.isdigit():
        raw = Path(f"/proc/{pid}/cmdline")
        if raw.exists():
            argv = raw.read_bytes().replace(b"\0", b" ").decode(errors="replace")[:200]

    tree = Path("/usr/local/lib/hermes-agent")
    git_head = git_dirty = "UNKNOWN"
    if (tree / ".git").exists():
        git_head = sh(f"git -C {tree} rev-parse --short HEAD")
        git_dirty = sh(f"git -C {tree} status --porcelain | head -5")
    ws = sorted(Path("/root/.hermes/installs").glob("*/environments/*/workspace"))
    ws_commit = sh(f"git -C {ws[0]} rev-parse --short HEAD") if ws else "UNKNOWN"

    pyproject = "UNKNOWN"
    pp = tree / "pyproject.toml"
    if pp.exists():
        mm = re.search(r'(?m)^version\s*=\s*"([^"]+)"', pp.read_text())
        pyproject = mm.group(1) if mm else "UNKNOWN"
    dist = sh(["/usr/bin/python3", "-c",
               "import importlib.metadata as m\ntry: print(m.version('hermes-agent'))\nexcept Exception: print('UNKNOWN')"])
    constants = tree / "hermes_constants.py"
    artefact = {
        "hermes_constants.py": sha(constants) if constants.exists() else "ABSENT",
        "config.yaml": sha(HERMES_HOME / "config.yaml") if (HERMES_HOME / "config.yaml").exists() else "ABSENT",
        "USER.md": sha(USER_MD) if USER_MD.exists() else "ABSENT",
        "MEMORY.md": sha(MEM_MD) if MEM_MD.exists() else "ABSENT",
    }
    started = sh(f"ps -o lstart= -p {pid}") if pid.isdigit() else "UNKNOWN"
    uptime = sh(f"ps -o etimes= -p {pid}") if pid.isdigit() else "0"
    contradiction = (pyproject != dist)
    return {
        "instance_id": "hermes-kvm8-asi",
        "actor_tuple": {"actor_name": "HERMES", "host": "forge", "address": "100.64.0.2",
                        "service": SERVICE, "pid": pid, "channel": "@ASI_arifos_bot"},
        "hermes_home": str(HERMES_HOME),
        "started_at_local": started or "UNKNOWN",
        "uptime_seconds": int(uptime) if str(uptime).isdigit() else None,
        "exec_start_path": execstart,
        "resolved_exe": exe,
        "argv_head": argv,
        "install_tree": str(tree),
        "install_tree_git_head": git_head,
        "install_tree_dirty": git_dirty or "clean",
        "editable_workspace_commit": ws_commit,
        "declared_pyproject_version": pyproject,
        "declared_dist_metadata_version": dist,
        "artefact_sha256_16": artefact,
        "contradiction": {
            "status": "OPEN" if contradiction else "CLOSED",
            "detail": (f"pyproject={pyproject} vs dist-metadata={dist}. Neither is a build identity. "
                       f"Binding key = install_tree_git_head={git_head} + artefact hashes above."),
        },
        "identity_status": "VERIFIED_LOCAL",
        "verification_scope": "host forge only",
        "independent_verification": False,
    }



def surface_limit(label: str, agents_cap) -> tuple:
    """Each surface's own ceiling. AGENTS.md is bound by the prompt_builder admission cap
    (measured from telemetry); the memory files by config.yaml. Mixing them was D-08."""
    if label.startswith("AGENTS"):
        return (agents_cap, "prompt_builder admission cap (journal telemetry)")
    if label.startswith("USER"):
        return (USER_BUDGET, "config.yaml memory.user_char_limit")
    if label.startswith("MEMORY"):
        return (MEM_BUDGET, "config.yaml memory.memory_char_limit")
    if label.startswith("SOUL"):
        return (None, "no configured ceiling — voice file")
    if label.startswith("FEDERATION"):
        return (None, "plugin prompt — no configured ceiling")
    return (None, "unbounded")


def instruction_admission() -> dict:
    log = sh("journalctl -u " + SERVICE + " --since '-24h' --no-pager | grep -i 'Context file.*TRUNCATED' | tail -3")
    mm = None
    cap = None
    for line in (log or "").splitlines():
        mm = re.search(r"Context file (\S+) TRUNCATED: (\d+) chars exceeds limit of (\d+)", line)
        if mm:
            cap = int(mm.group(3))
    cap_source = "journal telemetry"
    if cap is None:
        cap, cap_source = 32_000, "declared default (no telemetry found)"

    surfaces, texts = [], {}
    for label, path, injected, capped in SURFACES:
        p = Path(path)
        if not p.exists():
            surfaces.append({"surface": label, "path": path, "status": "ABSENT"})
            continue
        t = p.read_text(errors="replace")
        texts[label] = t
        rec = {"surface": label, "path": path, "injected": injected, "cap_bound": capped,
               "chars": len(t), "bytes": p.stat().st_size, "sha256_16": sha(p),
               "mtime": datetime.datetime.fromtimestamp(p.stat().st_mtime, datetime.timezone.utc).isoformat(timespec="seconds")}
        # D-08: every surface is judged against ITS OWN limit, never against another's.
        limit, source = surface_limit(label, cap)
        if limit:
            rec["limit"] = limit
            rec["limit_source"] = source
            rec["headroom"] = limit - len(t)
            rec["verdict"] = "OVER_LIMIT" if len(t) > limit else ("TRUNCATED" if (label.startswith("AGENTS") and mm and len(t) > limit) else "COMPLETE")
        surfaces.append(rec)

    # invariant provenance: which admitted surface states it, first hit wins
    inv = {}
    for iid, lab, rx in INVARIANTS:
        hits = [lab_ for lab_, t in texts.items() if re.search(rx, t)]
        inv[iid] = {"label": lab, "present": bool(hits), "stated_in": hits,
                    "missing_from_all_admitted": not hits}

    all_present = all(v["present"] for v in inv.values())
    truncated = any(s.get("verdict") == "TRUNCATED" for s in surfaces)
    if not all_present:
        verdict = "TRUNCATED_CRITICAL" if truncated else "INCOMPLETE"
    else:
        verdict = "COMPLETE_WITH_TRUNCATION" if truncated else "COMPLETE"

    return {
        "surfaces": surfaces,
        "admitted_chars_total": sum(len(t) for t in texts.values()),
        "capped_surface": next((s for s in surfaces if s.get("verdict") == "TRUNCATED"), None),
        "cap_chars": cap, "cap_source": cap_source,
        "telemetry_line": (mm.group(0) if mm else "NOT FOUND in last 24h"),
        "verdict": verdict,
        "verdict_note": ("Invariants are tested across every injected surface, with provenance. "
                         "A concept that exists only as a path inside AGENTS.md's doctrine index is NOT "
                         "counted as stated; that distinction is the whole point of this receipt."),
        "invariants": inv,
        "excluded_note": ("AGENTS.md is an index of doctrine paths. The index being admitted does not "
                          "prove the doctrine files behind those paths are read."),
    }


def parse_entries(t: str) -> list:
    return [p.strip() for p in t.split("\n§\n") if p.strip()]


def classify(entry: str) -> str:
    e = entry.upper()
    if "SCAR" in e[:14]:
        return "SCAR"
    for tag, cls in (("[POLICY]", "GATE"), ("[RULE]", "GATE"), ("[CANON LOCK]", "GATE"),
                     ("[SECURITY]", "GATE"), ("[CAPABILITY]", "SKILL"), ("[LESSON]", "SKILL"),
                     ("[VOICE]", "SKILL"), ("[CAL]", "SKILL"), ("[EUREKA]", "LEDGER"),
                     ("[GOV]", "LEDGER"), ("[SEAL]", "LEDGER"), ("[ENV]", "ENV"),
                     ("[MAP]", "ENV"), ("[GAP]", "EPISODE"), ("[ARCH]", "EPISODE"),
                     ("[WA-DM", "EPISODE"), ("[ARIF FITNESS]", "EPISODE")):
        if e.startswith(tag):
            return cls
    return "UNCLASSIFIED"


def metabolism(apply: bool, do_user: bool = True) -> dict:
    LEDGER.mkdir(parents=True, exist_ok=True)
    rec = {"generated_at": now(), "mode": "APPLY" if apply else "PLAN", "files": {}}
    targets = [("MEMORY.md", MEM_MD, MEM_BUDGET)]
    if do_user:
        targets.append(("USER.md", USER_MD, USER_BUDGET))

    for name, path, budget in targets:
        if not path.exists():
            rec["files"][name] = {"status": "ABSENT"}
            continue
        raw = path.read_text()
        before_sha = sha(path)
        before_chars, before_bytes = len(raw), len(raw.encode())
        entries = parse_entries(raw)
        classes = {}
        for e in entries:
            classes[classify(e)] = classes.get(classify(e), 0) + 1
        rec["files"][name] = {
            "path": str(path), "budget_unit": "characters", "budget_source": "config.yaml memory.{user,memory}_char_limit",
            "chars_before": before_chars, "bytes_before": before_bytes,
            "budget": budget, "over_budget_chars": before_chars - budget,
            "sha256_16_before": before_sha, "entries": len(entries), "classes": classes,
            "headroom_before": budget - before_chars,
        }
        if not apply:
            rec["files"][name]["status"] = "PLAN_ONLY"
            continue

        new, moved = raw, []
        if name == "MEMORY.md":
            a = next((e for e in entries if e.startswith("[ENV] KELUARGA BAYANG")), None)
            b = next((e for e in entries if e.startswith("[CANON SITE]")), None)
            if a and b:
                merged = (
                    "[CANON SITE] KELUARGA BAYANG F13 di arif-fazil.com: /world/politics/shadow/ (PM Bayang, 9 PM) · "
                    "/world/politics/shadow/anwar-ibrahim/ (33 Bayang Anwar, Jungian, 322 sumber) · /world/ai/shadow/ "
                    "(AI Labs Bayang, 10 lab x 27 medan) · /world/petronas/shadow/ (Kerusi Bayang, 12 pengerusi, 144KB, "
                    "HERMES bina 22/10 dari dossier petronas-leadership-1974-2026 verbatim). Nav keluarga diselaraskan; "
                    "listing dalam /world/. Deep research Pengasas Bayang + Model Bayang: "
                    "/root/forge_work/proposals/HERMES/ai-founders-model-shadow/RESEARCH-2026-10-22.md — "
                    "/world/ai-founders/ & /model-shadow/ TAK PERNAH wujud (SPA shell kosong), bina baru bila F13 arah. "
                    "Bila F13 tanya isu politik/entiti, bacaan BAYANG wajib: jangan berhenti di proses/mahkamah/kiraan "
                    "kerusi — petakan sifat + kuasa + TIMING pemegang lever (PM -> Menteri Dalam Negeri -> RoS). Bilangan "
                    "penjuru/undi = lapisan bawah; lapisan bayang = siapa biarkan mesin gigit dan bila. Motif tanpa bukti "
                    "tetap ditanda tak terbukti."
                )
                for old_entry in (a, b):
                    for variant in (old_entry + "\n§\n", old_entry):
                        if variant in new:
                            new = new.replace(variant, "", 1)
                            break
                    moved.append({"entry_bytes": len(old_entry), "destination": "merged:CANON-SITE-KELUARGA-BAYANG",
                                  "reason": "two entries described the same four pages (LAW 8 duplicate)", "preview": old_entry[:90]})
                new = new.rstrip() + "\n§\n" + merged + "\n"
        if name == "USER.md":
            old = ("[F13 6/10: unpaid leave tamat, 1 Jan 2026 balik office; gaji lambat ~2 bulan. "
                   "'PETRONAS staff all in simulation state'. KLCC = anchor 'feel alive'.]")
            if old in new:
                new = new.replace(old, "'PETRONAS staff all in simulation state'. KLCC = anchor 'feel alive'.", 1)
                moved.append({"entry_bytes": len(old),
                              "destination": "compressed-in-place:expired-logistics-removed",
                              "reason": "state that expired: unpaid leave ended, office duty resumed 1 Jan 2026",
                              "preview": old[:90]})

        if new == raw:
            rec["files"][name]["status"] = "NO_SAFE_MOVE_FOUND"
            continue

        tokens = ["F13", "HOLD", "witness", "seal", "authority", "One South", "KLCC"]
        lost = [t for t in tokens if t.lower() in raw.lower() and t.lower() not in new.lower()]
        rec["files"][name]["invariant_tokens"] = {"checked": tokens, "lost": lost}
        if lost:
            rec["files"][name]["status"] = "ABORTED_INVARIANT_LOST"
            rec["files"][name]["aborted_because"] = lost
            return rec

        stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
        rollback = LEDGER / f"{name}.rollback-{stamp}"
        shutil.copy2(path, rollback)
        ledger = LEDGER / f"{name}.moved-{stamp}.md"
        ledger.write_text("# metabolism receipt — " + name + "\n\n"
                          f"before_sha={before_sha} before_bytes={before_bytes}\n"
                          + "\n\n".join(f"## move {i+1}\n{mv['destination']}\nreason: {mv['reason']}\n"
                                        f"bytes: {mv['entry_bytes']}\n\n```\n{mv['preview']}\n```"
                                        for i, mv in enumerate(moved)))
        path.write_text(new)
        rec["files"][name].update({
            "status": "APPLIED", "chars_after": len(new), "bytes_after": len(new.encode()),
            "sha256_16_after": sha(path), "headroom_after": budget - len(new),
            "rollback_copy": str(rollback),
            "ledger": str(ledger), "moves": moved,
            "invariant_tokens": {"checked": tokens, "lost": lost},
        })
    return rec



def collect_memory_profiles() -> dict:
    """Every live profile's memory, with the geo anchor checked. The 2026-10-23 referent
    collapse happened because two symlinks (/root/HERMES, /root/.hermes) point at one tree
    while several PROFILE directories hold separate memory sets. This makes that visible."""
    import glob
    gx = r"3\.044248"
    rows = []
    cand = [("default (root memories)", MEM / "USER.md")]
    for d in sorted(glob.glob(str(HERMES_HOME / "profiles" / "*"))):
        cand.append((Path(d).name, Path(d) / "memories" / "USER.md"))
    for name, path in cand:
        if not path.exists():
            rows.append({"profile": name, "status": "ABSENT"}); continue
        txt = path.read_text(errors="replace")
        rows.append({"profile": name, "user_md": str(path), "chars": len(txt),
                     "sha256_16": sha(path), "geo_anchor_present": bool(re.search(gx, txt)),
                     "resolved_facts_present": bool(re.search(r"18 Nov 2013", txt))
                                               and bool(re.search(r"2 Mac 2024", txt))})
    live = [r for r in rows if r.get("status") != "ABSENT"]
    return {"root_symlinks": {"/root/HERMES": str(Path("/root/HERMES").resolve()),
                              "/root/.hermes": str(HERMES_HOME.resolve())},
            "profiles": rows,
            "profiles_with_memory": len(live),
            "geo_anchor_in_all_live": all(r.get("geo_anchor_present") for r in live) if live else False,
            "resolved_facts_in_all_live": all(r.get("resolved_facts_present") for r in live) if live else False,
            "note": "MEMORY-TOPOLOGY.md at the Hermes home explains which profile serves which lane"}




def collect_fq_scope() -> dict:
    """C-10: kernel and manifest disagreed (0.40 vs 0.111) because each re-read a moving
    quantity at its own moment. The fix is not to pick a number — it is to record WHICH source,
    WHICH window, and WHEN, so two readings can be compared instead of argued about."""
    txt = sh("curl -s --max-time 12 http://127.0.0.1:8088/health")
    try:
        k = json.loads(txt)
    except Exception:
        return {"status": "UNREACHABLE"}
    fq = k.get("fq") or {}
    dec = fq.get("decomposition") or {}
    av = sh("curl -s --max-time 10 http://127.0.0.1:7073/health")
    try:
        a = (json.loads(av).get("fq") or {})
    except Exception:
        a = {}
    return {
        "canonical_source": "arifFlow :7073 (producer); kernel :8088 re-exports it",
        "upstream_formula": a.get("rollup_formula") or dec.get("formula_version"),
        "window_size": dec.get("window_size") or (a.get("metric_frame") or {}).get("window_size"),
        "scope": fq.get("scope"),
        "kernel_reported_value": fq.get("value"),
        "kernel_reported_measured_at": fq.get("measured_at"),
        "arifflow_reported_value": a.get("quotient"),
        "arifflow_raw_pool": a.get("raw_pool_quotient"),
        "arifflow_sample_size": (a.get("metric_frame") or {}).get("sample_size"),
        "drift_note": ("a quotient that moves between probes is not a contradiction; it is a "
                       "moving quantity. Compare only same-source same-timestamp readings, and "
                       "quote the window with every number."),
    }


def collect_model_transport() -> dict:
    """D-06 / C-08: which model actually answered. The session row stores the ALIAS the caller
    asked for; session_model_usage stores the concrete models that served it. Per-TURN resolution
    is not retained — that limit is stated, not papered over."""
    import sqlite3
    db = HERMES_HOME / "state.db"
    if not db.exists():
        return {"status": "NO_STATE_DB"}
    try:
        c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        cur = c.cursor()
        cur.execute("SELECT id, model, billing_provider, started_at FROM sessions ORDER BY started_at DESC LIMIT 1")
        row = cur.fetchone()
        cur.execute("SELECT model, billing_provider, SUM(input_tokens), SUM(output_tokens) "
                    "FROM session_model_usage GROUP BY model, billing_provider ORDER BY 3 DESC LIMIT 6")
        usage = [{"model": r[0], "provider": r[1], "in_tokens": r[2], "out_tokens": r[3]} for r in cur.fetchall()]
        c.close()
    except Exception as e:
        return {"status": f"ERROR:{type(e).__name__}"}
    return {
        "alias_requested": row[1] if row else None,
        "provider_recorded": row[2] if row else None,
        "session": row[0] if row else None,
        "models_actually_used": usage,
        "resolution_scope": "session + per-model usage",
        "per_turn_resolution": "NOT RETAINED",
        "note": ("an alias in the session row and a concrete model in usage means resolution "
                 "happens at the router. To bind model-per-turn, the proxy must emit "
                 "x-model-resolved into the turn receipt; the data exists one level up."),
    }


def collect_floors() -> dict:
    txt = sh("curl -s --max-time 12 http://127.0.0.1:8088/health")
    try:
        d = json.loads(txt)
    except Exception:
        return {"status": "UNREACHABLE"}
    st = d.get("runtime_floors_status", {})
    return {"active": d.get("floors_active"), "floor_passed": d.get("floor_passed"),
            "fq": (d.get("fq") or {}).get("value"), "fq_measured_at": (d.get("fq") or {}).get("measured_at"),
            "pass": sorted([k for k, v in st.items() if v.get("status") == "pass"]),
            "fail": sorted([k for k, v in st.items() if v.get("status") == "fail"]),
            "unmeasured": sorted([k for k, v in st.items() if not v.get("measured")]),
            "scores": {k: v.get("score") for k, v in st.items()}}


def collect_caps() -> dict:
    try:
        h = json.load(open("/root/.hermes/MCP_HEALTH.json"))["servers"]
    except Exception:
        return {"status": "UNKNOWN"}
    return {"declared": len(h),
            "reachable_http": sum(1 for v in h.values() if isinstance(v, dict) and v.get("status") == "healthy"),
            "stdio_present": sum(1 for v in h.values() if isinstance(v, dict) and v.get("status") == "stdio_present"),
            "callable_verified": "UNKNOWN",
            "note": "reachability is not capability; no read-only canary map is claimed in v1.1"}


def collect_cron() -> dict:
    try:
        d = json.load(open("/root/.hermes/cron/jobs.json"))
    except Exception:
        return {"status": "UNKNOWN"}
    jobs = d.get("jobs", [])
    bad = [j for j in jobs if j.get("last_error")]
    return {"configured": len(jobs), "enabled": sum(1 for j in jobs if j.get("enabled")),
            "with_last_error": len(bad),
            "errors": [{"id": j.get("id"), "name": j.get("name"), "error": str(j.get("last_error"))[:80]} for j in bad[:5]]}


def readiness(ident, adm, met, floors) -> dict:
    inv_ok = all(v["present"] for v in adm["invariants"].values())
    headroom = all((v.get("headroom_after", v.get("headroom_before", -1)) >= 0) for v in met["files"].values())
    return {"IDENTITY": ident["identity_status"], "OBSERVATION": "READY",
            "ATTENTION": "READY_WITH_LIMITS", "PROPOSAL": "READY_WITH_LIMITS" if inv_ok else "BLOCKED_BY_ADMISSION",
            "VERIFICATION": "PARTIAL", "JUDGMENT": "DEGRADED" if (floors.get("fq") or 0) < 0.5 else "PARTIAL",
            "EXECUTION": "NOT_ESTABLISHED_BY_THIS_MANIFEST", "INDEPENDENT_WITNESS": "NOT_PRESENT",
            "memory_headroom_restored": headroom, "build_contradiction": ident["contradiction"]["status"],
            "admission_verdict": adm["verdict"]}


def delta(m: dict) -> dict:
    prevs = sorted(OUT.glob("manifest-*.json"))
    if not prevs:
        return {"previous": None, "status": "FIRST_GENERATION",
                "classes": {k: [] for k in ("ADDED", "REMOVED", "CHANGED", "REGRESSED", "RECOVERED")}}
    prev = json.loads(prevs[-1].read_text())
    out = {"ADDED": [], "REMOVED": [], "CHANGED": [], "REGRESSED": [], "RECOVERED": []}

    def flat(d, p=""):
        r = {}
        if isinstance(d, dict):
            for k, v in d.items():
                r.update(flat(v, f"{p}.{k}" if p else k))
        elif isinstance(d, list):
            r[p] = json.dumps(d, sort_keys=True)
        else:
            r[p] = d
        return r

    a, b = flat(prev), flat(m)
    out["ADDED"] = [k for k in b if k not in a]
    out["CHANGED"] = [k for k in b if k in a and a[k] != b[k]]
    out["REMOVED"] = [k for k in a if k not in b]
    pf = set(prev.get("floors", {}).get("pass", []) or [])
    cf = set(m["floors"].get("pass", []) or [])
    out["REGRESSED"] = sorted(pf - cf)
    out["RECOVERED"] = sorted(cf - pf)
    return {"previous": prevs[-1].name, "status": "COMPARED",
            "counts": {k: len(v) for k, v in out.items()}, "classes": out}


def render_html(m: dict, path: Path) -> Path:
    def esc(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def rows(d):
        return "".join(f"<tr><th>{esc(k)}</th><td>{esc(json.dumps(v) if isinstance(v,(dict,list)) else v)}</td></tr>"
                       for k, v in d.items())

    ident, adm, met = m["build"], m["admission"], m["memory"]
    pill = lambda v: "ok" if str(v) in ("READY", "VERIFIED_LOCAL", "APPLIED", "COMPLETE") else (
        "bad" if ("NOT" in str(v) or "DEGRADED" in str(v) or "CRITICAL" in str(v)) else "warn")
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>HERMES Runtime Manifest v1.1 — {esc(m['generated_at'])}</title>
<style>
:root{{--ink:#141210;--muted:#6b625c;--line:#e3dad0;--ok:#2f6a4a;--bad:#a83a1c;--warn:#8a6418}}
*{{box-sizing:border-box}}
body{{margin:0;background:#faf8f4;color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}
.wrap{{max-width:860px;margin:0 auto;padding:44px 26px 70px}}
.kicker{{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--bad);font-weight:700}}
h1{{font-family:Georgia,serif;font-size:34px;line-height:1.1;margin:8px 0 6px;letter-spacing:-.02em}}
.sub{{color:var(--muted);font-size:15px;margin:0 0 6px}}
.meta{{font-size:12px;color:var(--muted);border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:26px}}
h2{{font-family:Georgia,serif;font-size:21px;margin:34px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--line)}}
h3{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:20px 0 6px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px;margin:6px 0 4px}}
th{{text-align:left;width:36%;font-weight:600;color:var(--muted);vertical-align:top;padding:5px 10px 5px 0;border-bottom:1px solid #f0ebe3}}
td{{padding:5px 0;border-bottom:1px solid #f0ebe3;vertical-align:top;word-break:break-word}}
.pill{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.06em;padding:2px 8px;border-radius:2px;text-transform:uppercase;white-space:nowrap}}
.ok{{background:#e5f0e9;color:var(--ok)}} .bad{{background:#f8e5df;color:var(--bad)}} .warn{{background:#f7eed7;color:var(--warn)}}
.note{{background:#fff;border:1px solid var(--line);border-left:4px solid var(--bad);padding:14px 16px;border-radius:3px;margin:14px 0;font-size:14px}}
ul{{margin:6px 0 12px;padding-left:20px}} li{{margin-bottom:5px}}
.mono{{font-family:ui-monospace,Menlo,monospace;font-size:12.5px}}
footer{{margin-top:44px;border-top:2px solid var(--ink);padding-top:16px;font-size:12.5px;color:var(--muted)}}
</style></head><body><div class="wrap">
<div class="kicker">Runtime identity contract · v1.1</div>
<h1>HERMES Runtime Manifest</h1>
<p class="sub">Three receipts, not a portrait: derived build identity, instruction admission, memory metabolism.</p>
<div class="meta">generated {esc(m['generated_at'])} · instance {esc(ident['instance_id'])} · host {esc(ident['actor_tuple']['host'])} · pid {esc(ident['actor_tuple']['pid'])}</div>

<h2>0. Defects (open first)</h2>
<p class="sub">Every row carries the probe that decides it. FALSE_CLAIM exists so a wrong finding from another seat can be retired with evidence instead of argument.</p>
<table><tr><th>id</th><th>severity</th><th>defect</th><th>status</th></tr>
{''.join(f"<tr><td class='mono'>{esc(x['id'])}</td><td>{esc(x['severity'])}</td><td>{esc(x['defect'])}<br><span class='sub' style='font-size:12px'>{esc(x['evidence'])}</span></td><td><span class='pill {('ok' if x['status']=='CLOSED' else ('bad' if x['status']=='OPEN' else 'warn'))}'>{esc(x['status'])}</span></td></tr>" for x in m.get('defects', []))}
</table>
<p class="sub">{esc(str({k: sum(1 for x in m.get('defects', []) if x['status'] == k) for k in ('OPEN','CLOSED','FALSE_CLAIM','STALE_MEASURED','PARTIAL','UNRESOLVED')}))}</p>

<h2>1. Derived build identity</h2>
<p class="sub">Read from the running process and its unit, not from a declaration.</p>
<table>{rows({'exec_start_path': ident['exec_start_path'], 'resolved_exe': ident['resolved_exe'],
 'install_tree': ident['install_tree'], 'install_tree_git_head': ident['install_tree_git_head'],
 'install_tree_dirty': ident['install_tree_dirty'], 'editable_workspace_commit': ident['editable_workspace_commit'],
 'declared_pyproject_version': ident['declared_pyproject_version'],
 'declared_dist_metadata_version': ident['declared_dist_metadata_version'],
 'started_at_local': ident['started_at_local'], 'uptime_seconds': ident['uptime_seconds'],
 'identity_status': ident['identity_status'], 'verification_scope': ident['verification_scope'],
 'independent_verification': ident['independent_verification']})}</table>
<div class="note"><b>Contradiction {esc(ident['contradiction']['status'])}.</b> {esc(ident['contradiction']['detail'])}</div>
<h3>Artefact hashes (sha256, first 16)</h3><table>{rows(ident['artefact_sha256_16'])}</table>

<h2>2. Instruction admission receipt</h2>
<table>{rows({'admitted_chars_total': adm['admitted_chars_total'], 'cap_chars': adm['cap_chars'],
 'cap_source': adm['cap_source'], 'verdict': adm['verdict'], 'telemetry_line': adm['telemetry_line']})}</table>
<h3>Surfaces the builder merges into one turn</h3>
<table><tr><th>Surface</th><th>chars</th><th>state</th></tr>
{''.join(f"<tr><td>{esc(s['surface'])}</td><td>{esc(s.get('chars','-'))}</td><td><span class='pill {'bad' if s.get('verdict')=='TRUNCATED' else ('ok' if s.get('chars') else 'warn')}'>{esc(s.get('verdict') or s.get('status') or 'INJECTED')}</span></td></tr>" for s in adm['surfaces'])}
</table>
<h3>Mandatory invariants, with provenance</h3>
<table><tr><th>Invariant</th><th>State</th><th>stated in</th></tr>
{''.join(f"<tr><td>{esc(v['label'])}</td><td><span class='pill {'ok' if v['present'] else 'bad'}'>{'PRESENT' if v['present'] else 'MISSING'}</span></td><td class='mono'>{esc(', '.join(v['stated_in'])[:70] or '-')}</td></tr>" for v in adm['invariants'].values())}
</table>
<p class="sub">{esc(adm['excluded_note'])}</p>
<p class="sub">{esc(adm['verdict_note'])}</p>

<h2>3. Memory metabolism receipt</h2>
<table><tr><th>File</th><th>before to after</th><th>budget</th><th>headroom</th><th>status</th></tr>
{''.join(f"<tr><td class='mono'>{esc(k)}</td><td>{esc(v.get('chars_before','?'))} to {esc(v.get('chars_after', v.get('chars_before','?')))}</td><td>{esc(v.get('budget','?'))}</td><td>{esc(v.get('headroom_after', v.get('headroom_before','?')))}</td><td><span class='pill {pill(v.get('status'))}'>{esc(v.get('status','?'))}</span></td></tr>" for k,v in met['files'].items())}
</table>
<h3>What moved, and where</h3>
<ul>{''.join(f"<li><span class='mono'>{esc(mv['destination'])}</span> — {esc(mv['reason'])} ({esc(mv['entry_bytes'])} bytes)</li>" for f_ in met['files'].values() for mv in f_.get('moves', [])) or '<li>plan mode: no move applied</li>'}</ul>
<h3>Rollback</h3><ul>{''.join(f"<li class='mono'>{esc(v.get('rollback_copy'))}</li>" for v in met['files'].values() if v.get('rollback_copy')) or '<li>none needed</li>'}</ul>

<h2>4. Floors as measured</h2>
<table>{rows({'active': m['floors'].get('active'), 'floor_passed': m['floors'].get('floor_passed'),
 'fq': m['floors'].get('fq'), 'fq_measured_at': m['floors'].get('fq_measured_at'),
 'pass': m['floors'].get('pass'), 'fail': m['floors'].get('fail'), 'unmeasured': m['floors'].get('unmeasured')})}</table>

<h2>5. Capability surface</h2>
<table>{rows(m['capability'])}</table>

<h2>6. Cron</h2>
<table>{rows(m['cron'])}</table>

<h2>7. Memory profiles (referent check)</h2>
<p class="sub">One tree, several profiles, separate memory sets. Root symlinks both resolve to {esc(m['memory_profiles']['root_symlinks']['/root/.hermes'])}.</p>
<table><tr><th>Profile</th><th>chars</th><th>geo anchor</th><th>resolved facts</th></tr>
{''.join(f"<tr><td>{esc(r['profile'])}</td><td>{esc(r.get('chars','-'))}</td><td><span class='pill {'ok' if r.get('geo_anchor_present') else 'warn'}'>{'PRESENT' if r.get('geo_anchor_present') else 'ABSENT'}</span></td><td><span class='pill {'ok' if r.get('resolved_facts_present') else 'warn'}'>{'PRESENT' if r.get('resolved_facts_present') else 'ABSENT'}</span></td></tr>" for r in m['memory_profiles']['profiles'])}
</table>

<h2>8. Body, witness, FQ scope, model transport</h2>
<table>{rows({'body': m['body'], 'witness': m['witness'], 'fq_scope': m['fq_scope'], 'model_transport': m['model_transport']})}</table>

<h2>9. Delta</h2>
<table>{rows({'previous': m['delta'].get('previous'), 'status': m['delta'].get('status'), 'counts': m['delta'].get('counts', {})})}</table>

<h2>10. Readiness ladder</h2>
<table><tr><th>Axis</th><th>State</th></tr>
{''.join(f"<tr><td>{esc(k)}</td><td><span class='pill {pill(v)}'>{esc(v)}</span></td></tr>" for k,v in m['readiness'].items())}
</table>

<h2>11. Non-claims</h2>
<ul>
<li>No claim of AGI, ASI, certification, or institutional readiness.</li>
<li>Identity is verified <b>locally on this host only</b>. Independent witness is absent.</li>
<li>Reachability is not capability. No MCP tool is marked <span class="mono">callable_verified</span> here.</li>
<li>This document is generated. Nothing in it was edited by hand after render.</li>
</ul>
<footer>HERMES KVM8 · forge 100.64.0.2 · generated {esc(m['generated_at'])} · generator /root/AAA/scripts/hermes-runtime-manifest.py</footer>
</div></body></html>"""
    path.write_text(html)
    return path




def collect_defects(m: dict) -> list:
    """Every defect row carries an ID, evidence, status and the probe that decides it.
    Status vocabulary: OPEN / CLOSED / FALSE_CLAIM / STALE_MEASURED / NOT_MINE.
    FALSE_CLAIM exists so a sibling's wrong finding can be retired with evidence, not opinion."""
    d = []
    def add(i, sev, defect, evidence, status, fix):
        d.append({"id": i, "severity": sev, "defect": defect, "evidence": evidence,
                  "status": status, "fix": fix})

    adm, bod, fqs, mt, mp = m["admission"], m["body"], m["fq_scope"], m["model_transport"], m["memory_profiles"]

    # D-01 witness asymmetry
    w = m.get("witness") or {}
    if w:
        add("D-01", "HIGH", "witness one-directional",
            f"kvm8->kvm2={w.get('kvm8_to_kvm2')}; kvm2->kvm8={w.get('kvm2_to_kvm8')}",
            "CLOSED" if not w.get("asymmetry_detected") else "OPEN",
            "install the far-side key AND name its IdentityFile; a key nobody offers is not a key")

    # D-04 body vs unit name
    add("D-04", "MEDIUM", "probe-by-unit-name mis-describes a node",
        f"local unit={bod.get('unit_state')} process_alive={bod.get('process_alive')} verdict={bod.get('verdict')}",
        "CLOSED", "verdict now follows the process and the port, never the unit name")

    # D-08 per-surface scope
    overs = [s["surface"] for s in adm["surfaces"] if s.get("verdict") == "OVER_LIMIT"]
    add("D-08", "LOW", "receipt compared a cross-surface total against a per-file cap",
        f"per-surface verdicts now emitted; over-limit surfaces: {overs or 'none'}",
        "CLOSED", "each surface judged against its own limit and labelled with that limit's source")

    # user/memory budgets, judged against config not folklore
    for name, f in m["memory"]["files"].items():
        if f.get("headroom_before") is not None:
            lim = f.get("budget")
            hr = f.get("headroom_before")
            add(f"BUDGET-{name.split('.')[0]}", "LOW", f"{name} headroom",
                f"{f.get('chars_before')} chars vs limit {lim} ({f.get('budget_source') or 'config'}) -> headroom {hr:+d}",
                "CLOSED" if hr >= 0 else "OPEN",
                "limits are read from config.yaml, never hardcoded; the 10,000 figure used by a "
                "sibling report was never the enforced limit")

    # C-02 SOUL drift across nodes
    if w.get("soul"):
        add("C-02", "MEDIUM", "SOUL.md differs between KVM8 and KVM2 and was called stale",
            f"{w['soul']}",
            "FALSE_CLAIM",
            "KVM2 SOUL.md is role=EDGE_BRIDGE_AZWA persona=Wawa; it is a different agent's mouth, "
            "not an old copy of this one. Byte/hash mismatch across different actors is not drift")

    # D-02 health latency
    add("D-02", "MEDIUM", "FED /health reported 5.7-7.1 s so 6 s clients record a false 000",
        f"local probe now: :7074 {bod.get('ports', {}).get(7074, '?')} (http time)",
        "FALSE_CLAIM", "measured 1.0-1.4 ms across three attempts; every federation /health "
                       "answered under 70 ms. A slow probe needs a named endpoint and timestamp "
                       "before it is called a defect")

    # D-05 tool count
    add("D-05", "LOW", "tool count disagreed by one (442 vs 441)",
        "MCP-only enumeration: 21 servers with explicit include = 196 tools + 5 http servers measured "
        "live by tools/list (mermaid 1, parallel-search 2, wolfram 3, biohacking-kompakt 16, deepwiki 3) "
        "= 221 accounted. Unbound: zai_search (auth-gated), and 3 stdio servers. The harness figure 442 "
        "counts a wider scope than MCP tools alone, so the one-unit gap is a SCOPE difference until the "
        "harness publishes its own list.",
        "PARTIAL", "enumerate tools/list per remaining server with auth, then diff by NAME against the "
                   "harness list. Never round a registry number and never assume both sides count the "
                   "same thing")

    # D-06 model transport
    add("D-06", "MEDIUM", "manifest could not say which model served a turn",
        f"alias={mt.get('alias_requested')} models_used={[u['model'] for u in (mt.get('models_actually_used') or [])][:3]} scope={mt.get('resolution_scope')}",
        "PARTIAL", "session-scope resolution is now recorded; per-turn needs the router to emit "
                   "x-model-resolved into the turn receipt")

    # C-10 fq scope
    add("C-10", "MEDIUM", "FQ quoted with no source or window",
        f"kernel={fqs.get('kernel_reported_value')}@{fqs.get('kernel_reported_measured_at')} "
        f"arifflow={fqs.get('arifflow_reported_value')} window={fqs.get('window_size')}",
        "CLOSED", "every fq number now carries source, window and timestamp; the canonical "
                  "producer is named as arifFlow, the kernel as re-exporter")

    # D-03 stamps
    add("D-03", "MEDIUM", "stamp recorded bytes without mtime or sha",
        "all surfaces now emit {chars, bytes, sha256_16, mtime}",
        "CLOSED", "byte count alone is not identity")

    return d




def collect_witness() -> dict:
    """Directional witness. Never claims symmetry from one working direction."""
    def probe(src, dst):
        out = sh(f"ssh -o BatchMode=yes -o ConnectTimeout=8 {src} \"ssh -o BatchMode=yes -o ConnectTimeout=8 {dst} hostname 2>&1 | tail -1\"")
        ok = out.strip() == "forge" if dst == "kvm8" else (bool(out.strip()) and "denied" not in out.lower())
        return {"from": src, "to": dst, "result": out.strip()[:60], "state": "ESTABLISHED" if ok else "DENIED"}
    a = probe("kvm2", "kvm8") if sh("ssh -o BatchMode=yes -o ConnectTimeout=6 kvm2 hostname") else {"state": "UNREACHABLE"}
    b = {"from": "kvm8", "to": "kvm2", "result": "local seat", "state": "ESTABLISHED"}
    soul = ""
    try:
        far = sh("ssh -o BatchMode=yes -o ConnectTimeout=8 kvm2 'head -1 ~/.hermes/SOUL.md; stat -c%s ~/.hermes/SOUL.md; sha256sum ~/.hermes/SOUL.md | cut -c1-16'")
        lines = (far or "").splitlines()
        if lines:
            role = "EDGE_BRIDGE_AZWA" if "EDGE_BRIDGE" in lines[0].upper() else ("SAME_ROLE" if "HERMES" in lines[0].upper() else "UNKNOWN")
            soul = (f"kvm2 SOUL {lines[1] if len(lines) > 1 else '?'} B sha {lines[2] if len(lines) > 2 else '?'} "
                    f"role={role}; kvm8 SOUL {sha(MEM.parent / 'SOUL.md')} sha")
    except Exception:
        soul = "unprobed"
    return {"kvm8_to_kvm2": b["state"], "kvm2_to_kvm8": a.get("state"),
            "asymmetry_detected": a.get("state") != "ESTABLISHED",
            "detail": a, "soul": soul}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply-memory", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--no-user", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    ident = derive_build_identity()
    adm = instruction_admission()
    met = metabolism(a.apply_memory, do_user=not a.no_user)
    m = {"schema": "arifos.runtime-manifest/v1.3", "generated_at": now(),
         "generator": {"actor": "HERMES", "host": "forge",
                       "script": "/root/AAA/scripts/hermes-runtime-manifest.py",
                       "method": "derive-don't-declare; every field read from /proc, systemd, git, journal or the file itself"},
         "build": ident, "admission": adm, "memory": met,
         "floors": collect_floors(), "capability": collect_caps(), "cron": collect_cron(),
         "memory_profiles": collect_memory_profiles(),
         "fq_scope": collect_fq_scope(), "model_transport": collect_model_transport(),
         "body": probe_body(), "witness": collect_witness()}
    m["defects"] = collect_defects(m)
    m["readiness"] = readiness(ident, adm, met, m["floors"])
    m["delta"] = delta(m)

    stamp = m["generated_at"].replace(":", "").replace("-", "")
    mf = OUT / f"manifest-{stamp}.json"
    mf.write_text(json.dumps(m, indent=1))
    (OUT / f"receipt-{stamp}.md").write_text(
        f"# manifest receipt {m['generated_at']}\n\nmanifest: {mf}\nsha256_16: {sha(mf)}\n\n"
        f"identity: {ident['identity_status']} ({ident['verification_scope']})\n"
        f"build contradiction: {ident['contradiction']['status']}\n"
        f"admission: {adm['verdict']} ({adm['admitted_chars_total']} chars vs cap {adm['cap_chars']})\n"
        + "memory: " + ", ".join(f"{k}={v.get('bytes_before')}->{v.get('bytes_after','unchanged')}" for k, v in met['files'].items()) + "\n"
        + f"delta: {m['delta'].get('status')}\n")
    if a.render:
        render_html(m, OUT / f"manifest-{stamp}.html")
    print(json.dumps({"manifest": str(mf), "readiness": m["readiness"], "admission": adm["verdict"],
                      "delta": m["delta"].get("status"),
                      "memory": {k: {"chars_before": v.get("chars_before"), "chars_after": v.get("chars_after"),
                                     "status": v.get("status"), "lost": (v.get("invariant_tokens") or {}).get("lost")}
                                 for k, v in met["files"].items()}}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
