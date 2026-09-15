"""
claim-ledger-mcp — SQLite-backed, append-only claim ledger for arifOS federation.

WHY THIS EXISTS
    Today the federation hashes artifacts but never claims. A forged brief has a
    SHA256 of the PDF, yet nothing binds the sentence "Bank Muamalat's retail
    funding is 12%" to the page it came from, the quote that backs it, the
    artifact it lives in, or a verification record. This server closes that gap.

MODEL (append-only, chain-linked)
    artifacts      one row per hashed source artifact (path -> sha256)
    claims         one row per claim: text + type + quote + locator + artifact hash
    verifications  one row per verification event against a claim
    ledger_chain   every write above also appends a row here with seq,
                   prev_hash and row_hash over the canonical payload.

    SQLite triggers RAISE(ABORT) on any UPDATE or DELETE of claims,
    verifications or ledger_chain. Corrections are made by appending a new
    claim with supersedes_claim_id set. Nothing is ever mutated in place.

CLAIM TYPES (federation vocabulary, as used inside the forged briefs)
    OBS  observed / sourced fact
    DER  derived (arithmetic, inference from stated inputs)
    INT  interpretation / judgement
    SPEC speculative
    VOID explicitly could-not-verify
    FIQH doctrinal question referred to scholars

VERDICTS
    CONFIRMED / PARTIAL / REFUTED / UNVERIFIED

AUTHORITY
    This organ witnesses claims. It does not judge them, does not seal
    VAULT999, and never writes outside its own ledger directory.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any

from fastmcp import FastMCP

LEDGER_DIR = "/root/AAA/claim_ledger"
DB_PATH = os.path.join(LEDGER_DIR, "claims.db")
GENESIS = "0" * 64

CLAIM_TYPES = {"OBS", "DER", "INT", "SPEC", "VOID", "FIQH"}
VERDICTS = {"CONFIRMED", "PARTIAL", "REFUTED", "UNVERIFIED"}

mcp = FastMCP(
    name="claim-ledger-mcp",
    version="2026.09.15",
    instructions=(
        "Append-only claim ledger for arifOS federation intelligence briefs. "
        "Traces every claim to source, quote, timestamp, artifact SHA256 and a "
        "verification record. Authority: WITNESS_ONLY — records and verifies, "
        "never judges, never writes VAULT999. All writes are hash-chained and "
        "UPDATE/DELETE are blocked at the schema level."
    ),
)

# ---------------------------------------------------------------- primitives


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _canon(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str,
                      ensure_ascii=False)


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _conn() -> sqlite3.Connection:
    os.makedirs(LEDGER_DIR, exist_ok=True)
    c = sqlite3.connect(DB_PATH, timeout=30, isolation_level=None)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA busy_timeout=30000")
    c.execute("PRAGMA foreign_keys=ON")
    return c


SCHEMA = """
CREATE TABLE IF NOT EXISTS artifacts (
  artifact_id   TEXT PRIMARY KEY,
  path          TEXT NOT NULL,
  sha256        TEXT NOT NULL,
  sha256_source TEXT NOT NULL,            -- 'computed' | 'declared+verified'
  bytes         INTEGER,
  media_type    TEXT,
  title         TEXT,
  pages         INTEGER,
  registered_at TEXT NOT NULL,
  registered_by TEXT NOT NULL,
  seq           INTEGER NOT NULL,
  prev_hash     TEXT NOT NULL,
  row_hash      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS claims (
  claim_id            TEXT PRIMARY KEY,
  brief_id            TEXT NOT NULL,
  claim_text          TEXT NOT NULL,
  claim_type          TEXT NOT NULL,
  source_quote         TEXT,
  source_ref          TEXT,               -- citation / URL / document name
  locator             TEXT,               -- page or section the quote sits on
  artifact_id         TEXT,
  artifact_sha256     TEXT,               -- hash snapshot at write time
  confidence          REAL,
  supersedes_claim_id TEXT,
  recorded_at         TEXT NOT NULL,
  recorded_by         TEXT NOT NULL,
  seq                 INTEGER NOT NULL,
  prev_hash           TEXT NOT NULL,
  row_hash            TEXT NOT NULL,
  FOREIGN KEY (artifact_id) REFERENCES artifacts(artifact_id)
);

CREATE TABLE IF NOT EXISTS verifications (
  verification_id   TEXT PRIMARY KEY,
  claim_id          TEXT NOT NULL,
  verdict           TEXT NOT NULL,
  method            TEXT,
  evidence          TEXT,
  artifact_sha256   TEXT,
  artifact_recheck  TEXT,                 -- 'match' | 'mismatch' | 'unavailable'
  live_sha256       TEXT,                 -- hash recomputed from disk at verify time
  verifier          TEXT NOT NULL,
  verified_at       TEXT NOT NULL,
  seq               INTEGER NOT NULL,
  prev_hash         TEXT NOT NULL,
  row_hash          TEXT NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES claims(claim_id)
);

CREATE TABLE IF NOT EXISTS ledger_chain (
  seq          INTEGER PRIMARY KEY AUTOINCREMENT,
  event_type   TEXT NOT NULL,
  event_id     TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  prev_hash    TEXT NOT NULL,
  row_hash     TEXT NOT NULL,
  written_at   TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_claims_brief   ON claims(brief_id);
CREATE INDEX IF NOT EXISTS idx_claims_type    ON claims(claim_type);
CREATE INDEX IF NOT EXISTS idx_verif_claim    ON verifications(claim_id);

-- APPEND-ONLY ENFORCEMENT: any mutation of the record tables aborts.
CREATE TRIGGER IF NOT EXISTS trg_claims_no_update BEFORE UPDATE ON claims
BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY: claims may not be updated; append a superseding claim'); END;
CREATE TRIGGER IF NOT EXISTS trg_claims_no_delete BEFORE DELETE ON claims
BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY: claims may not be deleted'); END;
CREATE TRIGGER IF NOT EXISTS trg_verif_no_update BEFORE UPDATE ON verifications
BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY: verifications may not be updated'); END;
CREATE TRIGGER IF NOT EXISTS trg_verif_no_delete BEFORE DELETE ON verifications
BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY: verifications may not be deleted'); END;
CREATE TRIGGER IF NOT EXISTS trg_art_no_update BEFORE UPDATE ON artifacts
BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY: artifacts may not be updated'); END;
CREATE TRIGGER IF NOT EXISTS trg_art_no_delete BEFORE DELETE ON artifacts
BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY: artifacts may not be deleted'); END;
CREATE TRIGGER IF NOT EXISTS trg_chain_no_update BEFORE UPDATE ON ledger_chain
BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY: ledger_chain may not be updated'); END;
CREATE TRIGGER IF NOT EXISTS trg_chain_no_delete BEFORE DELETE ON ledger_chain
BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY: ledger_chain may not be deleted'); END;
"""


def _ensure_schema(c: sqlite3.Connection) -> None:
    c.executescript(SCHEMA)
    cols = {r["name"] for r in c.execute("PRAGMA table_info(verifications)").fetchall()}
    if "live_sha256" not in cols:
        c.execute("ALTER TABLE verifications ADD COLUMN live_sha256 TEXT")


def _tail_hash(c: sqlite3.Connection) -> tuple[int, str]:
    row = c.execute("SELECT row_hash FROM ledger_chain ORDER BY seq DESC LIMIT 1").fetchone()
    if row is None:
        return 0, GENESIS
    last_seq = c.execute("SELECT COALESCE(MAX(seq),0) AS s FROM ledger_chain").fetchone()["s"]
    return int(last_seq), row["row_hash"]


def _append_event(c: sqlite3.Connection, event_type: str, event_id: str,
                  payload: dict) -> dict[str, Any]:
    """Append one row to the hash chain. prev_hash links to the previous row."""
    prev_seq, prev_hash = _tail_hash(c)
    seq = prev_seq + 1
    payload_json = _canon(payload)
    row_hash = _sha256_bytes(f"{prev_hash}|{event_type}|{payload_json}".encode())
    c.execute(
        "INSERT INTO ledger_chain (seq, event_type, event_id, payload_json, prev_hash, "
        "row_hash, written_at) VALUES (?,?,?,?,?,?,?)",
        (seq, event_type, event_id, payload_json, prev_hash, row_hash, _now()),
    )
    return {"seq": seq, "prev_hash": prev_hash, "row_hash": row_hash}


def _next_seq(c: sqlite3.Connection) -> int:
    return int(c.execute("SELECT COALESCE(MAX(seq),0)+1 AS s FROM ledger_chain").fetchone()["s"])


def _payload_claim(row: sqlite3.Row) -> dict:
    """Rebuild the exact payload dict written to the chain for a claims row."""
    return {
        "claim_id": row["claim_id"], "brief_id": row["brief_id"],
        "claim_text": row["claim_text"], "claim_type": row["claim_type"],
        "source_quote": row["source_quote"], "source_ref": row["source_ref"],
        "locator": row["locator"], "artifact_id": row["artifact_id"],
        "artifact_sha256": row["artifact_sha256"],
        "confidence": float(row["confidence"] or 0.0),
        "supersedes_claim_id": row["supersedes_claim_id"],
    }


def _payload_verification(row: sqlite3.Row, live_sha: str | None) -> dict:
    return {
        "verification_id": row["verification_id"], "claim_id": row["claim_id"],
        "verdict": row["verdict"], "method": row["method"], "evidence": row["evidence"],
        "verifier": row["verifier"], "artifact_sha256": row["artifact_sha256"],
        "artifact_recheck": row["artifact_recheck"], "live_sha256": live_sha,
    }


def _payload_artifact(row: sqlite3.Row) -> dict:
    return {"path": row["path"], "sha256": row["sha256"],
            "artifact_id": row["artifact_id"], "media_type": row["media_type"]}


def _chain_payloads(c: sqlite3.Connection, event_id: str) -> dict[int, str]:
    return {r["seq"]: r["payload_json"] for r in c.execute(
        "SELECT seq, payload_json FROM ledger_chain WHERE event_id=?", (event_id,)).fetchall()}



# ------------------------------------------------------------------- tools


@mcp.tool()
def claim_ledger_init() -> dict[str, Any]:
    """Create the append-only ledger schema if absent and report ledger identity:
    db path, tables, row counts, chain head, append-only triggers active.
    Idempotent. Call this before any other tool if unsure of state."""
    c = _conn()
    try:
        _ensure_schema(c)
        tables = [r["name"] for r in c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
            "ORDER BY name").fetchall()]
        triggers = [r["name"] for r in c.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger' ORDER BY name").fetchall()]
        counts = {t: c.execute(f"SELECT COUNT(*) AS n FROM {t}").fetchone()["n"] for t in tables}
        head = c.execute("SELECT seq, row_hash, written_at FROM ledger_chain "
                         "ORDER BY seq DESC LIMIT 1").fetchone()
        return {
            "ok": True,
            "db_path": DB_PATH,
            "tables": tables,
            "row_counts": counts,
            "triggers": len(triggers),
            "append_only_enforced": len(triggers) == 8,
            "chain_head": dict(head) if head else None,
            "claim_types": sorted(CLAIM_TYPES),
            "verdicts": sorted(VERDICTS),
            "authority": "WITNESS_ONLY",
        }
    finally:
        c.close()


@mcp.tool()
def claim_artifact_register(path: str, artifact_id: str = "", sha256: str = "",
                            media_type: str = "application/pdf", title: str = "",
                            pages: int = 0, registered_by: str = "i-ARIF") -> dict[str, Any]:
    """Register a source artifact: hash the file on disk, verify against any
    declared sha256, and append it to the ledger chain. Returns artifact_id,
    the computed sha256, and whether a declared hash matched. Claims reference
    this artifact_id so claim -> artifact -> hash is a real join, not a string."""
    c = _conn()
    try:
        _ensure_schema(c)
        if not os.path.isfile(path):
            return {"ok": False, "error": f"artifact not found: {path}"}
        computed = _sha256_file(path)
        source = "computed"
        declared_match = None
        if sha256:
            declared_match = (computed.lower() == sha256.strip().lower())
            source = "declared+verified" if declared_match else "declared+MISMATCH"
            if not declared_match:
                return {"ok": False, "error": "declared sha256 does not match file on disk",
                        "path": path, "computed": computed, "declared": sha256}
        aid = artifact_id or f"art-{computed[:16]}"
        existing = c.execute("SELECT * FROM artifacts WHERE artifact_id=?", (aid,)).fetchone()
        if existing:
            return {"ok": True, "already_registered": True, "artifact": dict(existing)}
        c.execute("BEGIN IMMEDIATE")
        try:
            ev = _append_event(c, "artifact_registered", aid, {
                "path": path, "sha256": computed, "artifact_id": aid, "media_type": media_type})
            c.execute(
                "INSERT INTO artifacts (artifact_id, path, sha256, sha256_source, bytes, "
                "media_type, title, pages, registered_at, registered_by, seq, prev_hash, row_hash)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (aid, path, computed, source, os.path.getsize(path), media_type, title,
                 pages, _now(), registered_by, ev["seq"], ev["prev_hash"], ev["row_hash"]))
        except Exception:
            c.execute("ROLLBACK")
            raise
        c.execute("COMMIT")
        return {"ok": True, "already_registered": False, "artifact_id": aid,
                "sha256": computed, "sha256_source": source, "bytes": os.path.getsize(path),
                "declared_hash_match": declared_match, "seq": ev["seq"],
                "row_hash": ev["row_hash"]}
    finally:
        c.close()


@mcp.tool()
def claim_record(brief_id: str, claim_text: str, claim_type: str = "OBS",
                 source_quote: str = "", source_ref: str = "", locator: str = "",
                 artifact_id: str = "", confidence: float = 0.0,
                 supersedes_claim_id: str = "", recorded_by: str = "i-ARIF",
                 claim_id: str = "") -> dict[str, Any]:
    """Record one claim against a brief. Binds claim text -> type -> source quote
    -> locator (page/section) -> source_ref -> artifact_id, snapshotting the
    artifact's sha256 at write time. claim_type must be OBS/DER/INT/SPEC/VOID/FIQH.
    Corrections are made by recording a new claim with supersedes_claim_id set —
    the original is never mutated."""
    if claim_type not in CLAIM_TYPES:
        return {"ok": False, "error": f"invalid claim_type {claim_type!r}",
                "allowed": sorted(CLAIM_TYPES)}
    if not claim_text.strip():
        return {"ok": False, "error": "claim_text is empty"}
    c = _conn()
    try:
        _ensure_schema(c)
        artifact_sha = None
        if artifact_id:
            a = c.execute("SELECT sha256 FROM artifacts WHERE artifact_id=?", (artifact_id,)).fetchone()
            if a is None:
                return {"ok": False, "error": f"unknown artifact_id {artifact_id!r}; "
                                              f"register it with claim_artifact_register first"}
            artifact_sha = a["sha256"]
        if supersedes_claim_id:
            s = c.execute("SELECT claim_id FROM claims WHERE claim_id=?",
                          (supersedes_claim_id,)).fetchone()
            if s is None:
                return {"ok": False, "error": f"unknown supersedes_claim_id {supersedes_claim_id!r}"}
        cid = claim_id or "clm-" + _sha256_bytes(
            f"{brief_id}|{claim_text}|{_now()}|{os.urandom(8).hex()}".encode())[:16]
        dup = c.execute("SELECT claim_id FROM claims WHERE claim_id=?", (cid,)).fetchone()
        if dup:
            return {"ok": False, "error": f"duplicate claim_id {cid} — ledger is append-only; "
                                          f"use supersedes_claim_id to correct", "claim_id": cid}
        payload = {
            "claim_id": cid, "brief_id": brief_id, "claim_text": claim_text,
            "claim_type": claim_type, "source_quote": source_quote, "source_ref": source_ref,
            "locator": locator, "artifact_id": artifact_id or None,
            "artifact_sha256": artifact_sha, "confidence": float(confidence),
            "supersedes_claim_id": supersedes_claim_id or None,
        }
        c.execute("BEGIN IMMEDIATE")
        try:
            ev = _append_event(c, "claim_recorded", cid, payload)
            c.execute(
                "INSERT INTO claims (claim_id, brief_id, claim_text, claim_type, source_quote, "
                "source_ref, locator, artifact_id, artifact_sha256, confidence, "
                "supersedes_claim_id, recorded_at, recorded_by, seq, prev_hash, row_hash) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (cid, brief_id, claim_text, claim_type, source_quote, source_ref, locator,
                 artifact_id or None, artifact_sha, confidence, supersedes_claim_id or None,
                 _now(), recorded_by, ev["seq"], ev["prev_hash"], ev["row_hash"]))
        except Exception:
            c.execute("ROLLBACK")
            raise
        c.execute("COMMIT")
        return {"ok": True, "claim_id": cid, "brief_id": brief_id, "claim_type": claim_type,
                "artifact_id": artifact_id or None, "artifact_sha256": artifact_sha,
                "seq": ev["seq"], "row_hash": ev["row_hash"], "recorded_at": _now()}
    finally:
        c.close()


@mcp.tool()
def claim_verify(claim_id: str, verdict: str, method: str = "", evidence: str = "",
                 verifier: str = "i-ARIF", recheck_artifact: bool = True,
                 verification_id: str = "") -> dict[str, Any]:
    """Append a verification record against a claim. verdict must be
    CONFIRMED/PARTIAL/REFUTED/UNVERIFIED. When recheck_artifact is true the
    artifact file is re-hashed on disk and compared to the hash the claim was
    recorded against — so 'verified' means the source still exists and matches,
    not merely that someone typed a verdict."""
    if verdict not in VERDICTS:
        return {"ok": False, "error": f"invalid verdict {verdict!r}", "allowed": sorted(VERDICTS)}
    c = _conn()
    try:
        _ensure_schema(c)
        cl = c.execute("SELECT * FROM claims WHERE claim_id=?", (claim_id,)).fetchone()
        if cl is None:
            return {"ok": False, "error": f"unknown claim_id {claim_id!r}"}
        stored = cl["artifact_sha256"]
        recheck = "no-artifact"
        live_sha = None
        if recheck_artifact and cl["artifact_id"]:
            a = c.execute("SELECT path, sha256 FROM artifacts WHERE artifact_id=?",
                          (cl["artifact_id"],)).fetchone()
            if a and os.path.isfile(a["path"]):
                live_sha = _sha256_file(a["path"])
                recheck = "match" if live_sha == stored else "mismatch"
            else:
                recheck = "unavailable"
        vid = verification_id or f"vrf-{_sha256_bytes((claim_id + verdict + _now()).encode())[:16]}"
        payload = {"verification_id": vid, "claim_id": claim_id, "verdict": verdict,
                   "method": method, "evidence": evidence, "verifier": verifier,
                   "artifact_sha256": stored, "artifact_recheck": recheck,
                   "live_sha256": live_sha}
        c.execute("BEGIN IMMEDIATE")
        try:
            ev = _append_event(c, "claim_verified", vid, payload)
            c.execute(
                "INSERT INTO verifications (verification_id, claim_id, verdict, method, evidence,"
                " artifact_sha256, artifact_recheck, live_sha256, verifier, verified_at, seq,"
                " prev_hash, row_hash) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (vid, claim_id, verdict, method, evidence, stored, recheck, live_sha, verifier,
                 _now(), ev["seq"], ev["prev_hash"], ev["row_hash"]))
        except Exception:
            c.execute("ROLLBACK")
            raise
        c.execute("COMMIT")
        return {"ok": True, "verification_id": vid, "claim_id": claim_id, "verdict": verdict,
                "artifact_sha256": stored, "artifact_recheck": recheck, "live_sha256": live_sha,
                "seq": ev["seq"], "row_hash": ev["row_hash"]}
    finally:
        c.close()


@mcp.tool()
def claim_get(claim_id: str) -> dict[str, Any]:
    """Fetch one claim with its artifact record (path + sha256), its full
    verification history, and any claim that supersedes it."""
    c = _conn()
    try:
        _ensure_schema(c)
        cl = c.execute("SELECT * FROM claims WHERE claim_id=?", (claim_id,)).fetchone()
        if cl is None:
            return {"ok": False, "error": f"unknown claim_id {claim_id!r}"}
        d = dict(cl)
        d["artifact"] = dict(c.execute("SELECT * FROM artifacts WHERE artifact_id=?",
                                       (cl["artifact_id"],)).fetchone() or {}) or None
        d["verifications"] = [dict(r) for r in c.execute(
            "SELECT * FROM verifications WHERE claim_id=? ORDER BY seq", (claim_id,)).fetchall()]
        sup = c.execute("SELECT claim_id, recorded_at, claim_text FROM claims "
                        "WHERE supersedes_claim_id=?", (claim_id,)).fetchall()
        d["superseded_by"] = [dict(r) for r in sup]
        d["ok"] = True
        return d
    finally:
        c.close()


@mcp.tool()
def claim_trace(claim_id: str, rehash_artifact: bool = True) -> dict[str, Any]:
    """Full provenance trace for one claim: chain position, source reference,
    quote, locator, artifact path, artifact sha256 as recorded, the live sha256
    recomputed from disk right now, verification records, and a machine verdict
    on whether the claim is currently traceable end-to-end."""
    c = _conn()
    try:
        _ensure_schema(c)
        cl = c.execute("SELECT * FROM claims WHERE claim_id=?", (claim_id,)).fetchone()
        if cl is None:
            return {"ok": False, "error": f"unknown claim_id {claim_id!r}", "traceable": False}
        art = c.execute("SELECT * FROM artifacts WHERE artifact_id=?",
                        (cl["artifact_id"],)).fetchone() if cl["artifact_id"] else None
        live = None
        disk_state = "no-artifact"
        if art:
            if os.path.isfile(art["path"]):
                live = _sha256_file(art["path"]) if rehash_artifact else art["sha256"]
                disk_state = "match" if live == cl["artifact_sha256"] else "mismatch"
            else:
                disk_state = "missing-on-disk"
        verifs = [dict(r) for r in c.execute(
            "SELECT verification_id, verdict, method, verifier, verified_at, artifact_recheck "
            "FROM verifications WHERE claim_id=? ORDER BY seq", (claim_id,)).fetchall()]
        chain = c.execute("SELECT seq, event_type, prev_hash, row_hash, written_at "
                          "FROM ledger_chain WHERE event_id=? ORDER BY seq", (claim_id,)).fetchall()
        has_quote = bool(cl["source_quote"])
        has_ref = bool(cl["source_ref"] or cl["locator"])
        traceable = bool(art) and disk_state == "match" and has_quote and has_ref
        return {
            "ok": True, "claim_id": claim_id, "brief_id": cl["brief_id"],
            "claim_text": cl["claim_text"], "claim_type": cl["claim_type"],
            "recorded_at": cl["recorded_at"], "recorded_by": cl["recorded_by"],
            "source_quote": cl["source_quote"], "source_ref": cl["source_ref"],
            "locator": cl["locator"],
            "artifact": ({"artifact_id": art["artifact_id"], "path": art["path"],
                          "sha256_recorded": cl["artifact_sha256"],
                          "sha256_live": live, "disk_state": disk_state}) if art else None,
            "chain": [dict(r) for r in chain],
            "verifications": verifs,
            "latest_verdict": verifs[-1]["verdict"] if verifs else "UNVERIFIED",
            "traceable": traceable,
            "trace_gaps": [g for g, ok in (
                ("no artifact bound", bool(art)),
                ("artifact missing/mismatched on disk", disk_state == "match"),
                ("no source quote", has_quote),
                ("no source_ref/locator", has_ref),
            ) if not ok] if art or True else [],
        }
    finally:
        c.close()


@mcp.tool()
def claim_list(brief_id: str = "", claim_type: str = "", limit: int = 200) -> dict[str, Any]:
    """List claims, optionally filtered by brief_id and/or claim_type. Each row
    carries its verification count and latest verdict so audit gaps are visible
    without a second call."""
    c = _conn()
    try:
        _ensure_schema(c)
        q = ("SELECT c.claim_id, c.brief_id, c.claim_type, c.claim_text, c.locator, "
             "c.artifact_sha256, c.recorded_at, "
             "(SELECT COUNT(*) FROM verifications v WHERE v.claim_id=c.claim_id) AS n_verif, "
             "(SELECT v.verdict FROM verifications v WHERE v.claim_id=c.claim_id "
             " ORDER BY v.seq DESC LIMIT 1) AS latest_verdict "
             "FROM claims c WHERE 1=1")
        args: list[Any] = []
        if brief_id:
            q += " AND c.brief_id=?"; args.append(brief_id)
        if claim_type:
            q += " AND c.claim_type=?"; args.append(claim_type)
        q += " ORDER BY c.seq LIMIT ?"; args.append(int(limit))
        rows = [dict(r) for r in c.execute(q, args).fetchall()]
        for r in rows:
            r["latest_verdict"] = r["latest_verdict"] or "UNVERIFIED"
        return {"ok": True, "count": len(rows), "claims": rows,
                "unverified": sum(1 for r in rows if r["n_verif"] == 0)}
    finally:
        c.close()


@mcp.tool()
def claim_ledger_verify_chain(recheck_artifacts: bool = True, db_path: str = "") -> dict[str, Any]:
    """Prove ledger integrity. Walks every row of the hash chain in seq order and
    recomputes prev_hash/row_hash links; rebuilds the canonical payload of every
    claim, verification and artifact row and compares it to the payload stored in
    the chain (so an edit to a record that bypassed the triggers is caught, not
    just a broken link); and (unless disabled) re-hashes every registered
    artifact on disk. Returns chain_ok, payload_ok, artifacts_ok and any broken
    seq. Pass db_path to audit a copy or backup without touching the live ledger."""
    path = db_path or DB_PATH
    c = _conn() if not db_path else sqlite3.connect(path, timeout=30)
    if db_path:
        c.row_factory = sqlite3.Row
    try:
        _ensure_schema(c)
        prev = GENESIS
        broken: list[dict[str, Any]] = []
        n = 0
        for r in c.execute("SELECT seq, event_type, event_id, payload_json, prev_hash, row_hash "
                           "FROM ledger_chain ORDER BY seq").fetchall():
            n += 1
            expect = _sha256_bytes(f"{prev}|{r['event_type']}|{r['payload_json']}".encode())
            if r["prev_hash"] != prev or r["row_hash"] != expect:
                broken.append({"seq": r["seq"], "event_type": r["event_type"],
                               "reason": "prev_hash mismatch" if r["prev_hash"] != prev
                                         else "row_hash mismatch",
                               "recorded": r["row_hash"], "expected": expect})
            prev = r["row_hash"]

        # cross-check: row_hash linkage AND rebuilt payload vs chain payload
        mismatched_rows = 0
        payload_mismatches: list[dict[str, Any]] = []
        work: list[tuple[str, str, dict]] = []
        for r in c.execute("SELECT * FROM claims").fetchall():
            work.append(("claim", r["claim_id"], {"seq": r["seq"], "row_hash": r["row_hash"],
                                                  "canon": _canon(_payload_claim(r))}))
        for r in c.execute("SELECT * FROM verifications").fetchall():
            work.append(("verification", r["verification_id"],
                         {"seq": r["seq"], "row_hash": r["row_hash"],
                          "canon": _canon(_payload_verification(r, r["live_sha256"]))}))
        for r in c.execute("SELECT * FROM artifacts").fetchall():
            work.append(("artifact", r["artifact_id"], {"seq": r["seq"], "row_hash": r["row_hash"],
                                                        "canon": _canon(_payload_artifact(r))}))
        for kind, rid, m in work:
            lc = c.execute("SELECT row_hash, payload_json FROM ledger_chain WHERE seq=?",
                           (m["seq"],)).fetchone()
            if lc is None or lc["row_hash"] != m["row_hash"]:
                mismatched_rows += 1
                continue
            if lc["payload_json"] != m["canon"]:
                payload_mismatches.append({"kind": kind, "id": rid, "seq": m["seq"],
                                           "reason": "record content differs from chained payload"})

        art_results = []
        if recheck_artifacts:
            for a in c.execute("SELECT artifact_id, path, sha256 FROM artifacts ORDER BY seq").fetchall():
                if os.path.isfile(a["path"]):
                    live = _sha256_file(a["path"])
                    art_results.append({"artifact_id": a["artifact_id"], "state":
                                        "match" if live == a["sha256"] else "MISMATCH",
                                        "sha256": a["sha256"], "live": live})
                else:
                    art_results.append({"artifact_id": a["artifact_id"], "state": "missing",
                                        "sha256": a["sha256"], "live": None})
        head = c.execute("SELECT seq, row_hash, written_at FROM ledger_chain "
                         "ORDER BY seq DESC LIMIT 1").fetchone()
        chain_ok = not broken
        payload_ok = not payload_mismatches and mismatched_rows == 0
        art_ok = all(a["state"] == "match" for a in art_results)
        return {"ok": True, "db_path": path, "chain_ok": chain_ok, "chain_length": n,
                "broken_links": broken, "payload_ok": payload_ok,
                "payload_mismatches": payload_mismatches,
                "record_chain_mismatches": mismatched_rows,
                "records_checked": len(work),
                "artifacts_ok": art_ok, "artifacts": art_results,
                "head": dict(head) if head else None,
                "ledger_verified": chain_ok and payload_ok and art_ok}
    finally:
        c.close()


@mcp.tool()
def claim_ledger_stats() -> dict[str, Any]:
    """Ledger census: claims by type, by brief, verification verdict distribution,
    and how many claims are still unverified. Use to see coverage at a glance."""
    c = _conn()
    try:
        _ensure_schema(c)
        by_type = {r["claim_type"]: r["n"] for r in c.execute(
            "SELECT claim_type, COUNT(*) n FROM claims GROUP BY claim_type").fetchall()}
        by_brief = {r["brief_id"]: r["n"] for r in c.execute(
            "SELECT brief_id, COUNT(*) n FROM claims GROUP BY brief_id").fetchall()}
        by_verdict = {r["verdict"]: r["n"] for r in c.execute(
            "SELECT verdict, COUNT(*) n FROM verifications GROUP BY verdict").fetchall()}
        total = c.execute("SELECT COUNT(*) n FROM claims").fetchone()["n"]
        verified = c.execute("SELECT COUNT(DISTINCT claim_id) n FROM verifications").fetchone()["n"]
        return {"ok": True, "db_path": DB_PATH, "claims_total": total,
                "claims_verified": verified, "claims_unverified": total - verified,
                "artifacts": c.execute("SELECT COUNT(*) n FROM artifacts").fetchone()["n"],
                "verifications": c.execute("SELECT COUNT(*) n FROM verifications").fetchone()["n"],
                "by_type": by_type, "by_brief": by_brief, "by_verdict": by_verdict}
    finally:
        c.close()


@mcp.tool()
def claim_export_brief(brief_id: str) -> dict[str, Any]:
    """Export every claim for a brief as an auditable bundle: each claim with
    quote, locator, artifact path, artifact sha256 and its verification history,
    plus a bundle_sha256 over the canonical export so the export itself is
    hashable. This is what attaches to a brief to make it claim-traceable."""
    c = _conn()
    try:
        _ensure_schema(c)
        rows = c.execute("SELECT * FROM claims WHERE brief_id=? ORDER BY seq", (brief_id,)).fetchall()
        if not rows:
            return {"ok": False, "error": f"no claims for brief_id {brief_id!r}"}
        bundle = []
        for cl in rows:
            art = c.execute("SELECT artifact_id, path, sha256 FROM artifacts WHERE artifact_id=?",
                            (cl["artifact_id"],)).fetchone() if cl["artifact_id"] else None
            verifs = [dict(r) for r in c.execute(
                "SELECT verdict, method, verifier, verified_at, artifact_recheck "
                "FROM verifications WHERE claim_id=? ORDER BY seq", (cl["claim_id"],)).fetchall()]
            bundle.append({
                "claim_id": cl["claim_id"], "claim_text": cl["claim_text"],
                "claim_type": cl["claim_type"], "source_quote": cl["source_quote"],
                "source_ref": cl["source_ref"], "locator": cl["locator"],
                "recorded_at": cl["recorded_at"], "ledger_seq": cl["seq"],
                "row_hash": cl["row_hash"],
                "artifact": ({"artifact_id": art["artifact_id"], "path": art["path"],
                              "sha256": art["sha256"]}) if art else None,
                "artifact_sha256_snapshot": cl["artifact_sha256"],
                "verifications": verifs,
                "latest_verdict": verifs[-1]["verdict"] if verifs else "UNVERIFIED",
            })
        export = {"brief_id": brief_id, "exported_at": _now(), "claim_count": len(bundle),
                  "claims": bundle}
        export["bundle_sha256"] = _sha256_bytes(_canon(export).encode())
        return {"ok": True, **export,
                "type_counts": {t: sum(1 for b in bundle if b["claim_type"] == t)
                                for t in sorted({b["claim_type"] for b in bundle})}}
    finally:
        c.close()


if __name__ == "__main__":
    _ensure_schema(_conn())
    mcp.run(transport="http", host="127.0.0.1", port=8791)
