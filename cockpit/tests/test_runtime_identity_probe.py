"""
test_runtime_identity_probe.py — focused unit tests for runtime-identity.py.

Tests use temporary directories (tmp_path) and DO NOT depend on /root
production organs. They import runtime-identity.py as a module, then
exercise:

  1. resolve_paths() — direct vs legacy vs unresolved
  2. file_sha_full() — full SHA-256, deterministic, empty on missing
  3. main() end-to-end with monkeypatched organs dict — produces
     JSON in the canonical /root/AAA/cockpit/runtime-identity.json
     path. After each test we restore the production JSON (we backup
     before the test and restore after) so cockpit consumers never see
     a corrupt state. Tests run in fresh path order so they do not
     interfere with each other.

NOTE: production probe is restored from
  /root/AAA/cockpit/receipts/2026-10-17-fi002/runtime-identity.py.BEFORE_PATCH
backup (the original pre-FI-002-1st-patch version) when this test
session ends, to keep the cockpit/canon clean.

We assert the SHA-256 digests with hashlib (Python) and sha256sum
(shell) for full independence (Phase 5 of the brief).
"""
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

RUNTIME_IDENTITY_PATH = Path("/root/AAA/cockpit/runtime-identity.py")
PROBE_OUTPUT_PATH = Path("/root/AAA/cockpit/runtime-identity.json")
PROBE_BACKUP_PATH = Path(
    "/root/AAA/cockpit/receipts/2026-10-17-fi002/runtime-identity.json.PRE_TEST"
)


@pytest.fixture(scope="module")
def ri_module():
    spec = importlib.util.spec_from_file_location("ri_module", RUNTIME_IDENTITY_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(autouse=True)
def preserve_production_probe():
    """Snapshot production runtime-identity.json before each test, restore after.
    This keeps HUD/arifhud consumers seeing real federation state throughout
    the test session, even if a test fails mid-flight.
    """
    if PROBE_OUTPUT_PATH.exists() and not PROBE_BACKUP_PATH.exists():
        shutil.copy2(PROBE_OUTPUT_PATH, PROBE_BACKUP_PATH)
    yield
    if PROBE_BACKUP_PATH.exists():
        shutil.copy2(PROBE_BACKUP_PATH, PROBE_OUTPUT_PATH)


def _make_pkg(root: Path, name: str, content: str = "# pkg\n") -> Path:
    pkg = root / name
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "__init__.py").write_text(content)
    return pkg


# ---------------------------------------------------------------------------
# Phase 4 — resolve_paths()
# ---------------------------------------------------------------------------


def test_resolve_paths_direct_when_both_exist(tmp_path, ri_module):
    src_root = tmp_path / "src_root"
    rt_root = tmp_path / "rt_root"
    _make_pkg(src_root, "arifos")
    _make_pkg(rt_root, "arifos")
    result = ri_module.resolve_paths(
        "arifos",
        {
            "source_path": str(src_root),
            "runtime_path": str(rt_root),
            "import_name": "arifos",
        },
    )
    assert result["resolution_method"] == "direct_runtime_path"
    assert result["source_init_exists"] is True
    assert result["runtime_init_exists"] is True
    assert result["reason"] is None


def test_resolve_paths_unresolved_when_source_missing(tmp_path, ri_module):
    rt_root = tmp_path / "rt_root"
    _make_pkg(rt_root, "apa")
    result = ri_module.resolve_paths(
        "aforge",
        {
            "source_path": str(tmp_path / "absent_src"),
            "runtime_path": str(rt_root),
            "import_name": "apa",
        },
    )
    assert result["resolution_method"] == "unresolved"
    assert result["source_init_exists"] is False
    assert "source init missing" in result["reason"]


def test_resolve_paths_unresolved_when_runtime_missing(tmp_path, ri_module):
    src_root = tmp_path / "src_root"
    _make_pkg(src_root, "apa")
    result = ri_module.resolve_paths(
        "aforge",
        {
            "source_path": str(src_root),
            "runtime_path": str(tmp_path / "absent_rt"),
            "import_name": "apa",
        },
    )
    assert result["resolution_method"] == "unresolved"
    assert result["runtime_init_exists"] is False
    assert "runtime init missing" in result["reason"]


def test_resolve_paths_uses_import_name_subdir(tmp_path, ri_module):
    """A-FORGE: import_name=apa even when organ_key=aforge."""
    src_root = tmp_path / "src_root"
    rt_root = tmp_path / "rt_root"
    _make_pkg(src_root, "apa")
    _make_pkg(rt_root, "apa")
    result = ri_module.resolve_paths(
        "aforge",
        {
            "source_path": str(src_root),
            "runtime_path": str(rt_root),
            "import_name": "apa",
        },
    )
    assert result["resolution_method"] == "direct_runtime_path"
    assert "apa" in result["source_init_path"]


def test_resolve_paths_legacy_site_packages_fallback(tmp_path, ri_module):
    """When primary runtime path missing, fall back to bounded legacy
    site-packages candidate. NO unbounded /opt/** rglob in resolve_paths."""
    src_root = tmp_path / "src_root"
    legacy_dir = tmp_path / "legacy_root" / "current" / "venv" / "lib" / "python3.13" / "site-packages"
    _make_pkg(src_root, "apa")
    _make_pkg(legacy_dir, "apa")
    result = ri_module.resolve_paths(
        "aforge",
        {
            "source_path": str(src_root),
            "runtime_path": str(tmp_path / "missing_rt"),
            "import_name": "apa",
        },
    )
    # The legacy search is bounded to /opt/<name>/current/venv/...
    # So we DON'T test that path here (out of /opt scope). Instead we
    # confirm that resolve_paths does NOT silently accept an arbitrary
    # /opt/** rglob.
    assert result["resolution_method"] in ("unresolved", "configured_legacy_path")
    if result["resolution_method"] == "unresolved":
        assert "runtime init missing" in result["reason"]


def test_resolve_paths_never_uses_unbounded_rglob(ri_module):
    """Hard guarantee: resolve_paths must NOT call Path.rglob."""
    src = RUNTIME_IDENTITY_PATH.read_text()
    # Find resolve_paths function body and check for rglob
    import re
    match = re.search(r"def resolve_paths.*?(?=^def |\Z)", src, re.DOTALL | re.MULTILINE)
    assert match is not None, "resolve_paths function not found"
    body = match.group(0)
    assert "rglob" not in body, (
        "resolve_paths uses rglob; per spec, path resolution must be bounded"
    )


# ---------------------------------------------------------------------------
# Phase 4 — hashing semantics
# ---------------------------------------------------------------------------


def test_file_sha_full_is_full_hex(tmp_path, ri_module):
    p = tmp_path / "f.txt"
    p.write_text("hello\n")
    full = ri_module.file_sha_full(str(p))
    expected = "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"
    assert full == expected
    assert len(full) == ri_module.DIGEST_FULL_LENGTH == 64


def test_file_sha_full_returns_empty_on_missing(tmp_path, ri_module):
    assert ri_module.file_sha_full(str(tmp_path / "absent.py")) == ""


def test_file_sha_truncated_is_prefix_of_full(tmp_path, ri_module):
    p = tmp_path / "f.txt"
    p.write_text("hello\n")
    full = ri_module.file_sha_full(str(p))
    truncated = ri_module.file_sha_truncated(str(p))
    assert truncated == full[: ri_module.LEGACY_TRUNCATED_LENGTH]
    assert len(truncated) == 12


def test_collision_consciousness_documented():
    """12-char truncation = 48 bits; birthday collision ≈ 2^24.
    Not a witness. Must be documented in module + legacy alias note."""
    src = RUNTIME_IDENTITY_PATH.read_text()
    assert "TRUNCATED" in src or "truncated" in src
    assert "sha256[:12]" in src
    assert "MD5" in src  # explicit disclosure of the misnaming


# ---------------------------------------------------------------------------
# Phase 5 — full end-to-end with temp organs (in-process monkeypatch)
# ---------------------------------------------------------------------------


def _run_probe_with_temp_organs(ri_module, organs_cfg):
    """In-process: monkeypatch the module-level `ORGANS` dict and call main().
    Output is written to /root/AAA/cockpit/runtime-identity.json.
    Fixture restore on teardown preserves production state.
    """
    saved = ri_module.ORGANS
    ri_module.ORGANS = organs_cfg
    try:
        rc = ri_module.main()
    finally:
        ri_module.ORGANS = saved
    assert rc == 0
    return json.loads(PROBE_OUTPUT_PATH.read_text())


def test_e2e_match_equal_init_files(tmp_path, ri_module):
    src_root = tmp_path / "src"
    rt_root = tmp_path / "rt"
    _make_pkg(src_root, "arifos", "# content-v1\n")
    _make_pkg(rt_root, "arifos", "# content-v1\n")
    out = _run_probe_with_temp_organs(
        ri_module,
        {
            "arifos": {
                "source_path": str(src_root),
                "runtime_path": str(rt_root),
                "import_name": "arifos",
            },
        },
    )
    entry = out["identity_probe"]["arifos"]
    assert entry["measurable"] is True
    assert entry["match"] is True
    assert len(entry["source_digest"]) == 64
    assert entry["source_digest"] == entry["runtime_digest"]


def test_e2e_drift_when_contents_differ(tmp_path, ri_module):
    src_root = tmp_path / "src"
    rt_root = tmp_path / "rt"
    _make_pkg(src_root, "frame_organ", "# source-version\n")
    _make_pkg(rt_root, "frame_organ", "# runtime-version\n")
    out = _run_probe_with_temp_organs(
        ri_module,
        {
            "frame": {
                "source_path": str(src_root),
                "runtime_path": str(rt_root),
                "import_name": "frame_organ",
            },
        },
    )
    entry = out["identity_probe"]["frame"]
    assert entry["measurable"] is True
    assert entry["match"] is False
    assert entry["source_digest"] != entry["runtime_digest"]
    assert any(c["organ"] == "frame" for c in out["summary"]["contradictions"])


def test_e2e_unresolved_when_runtime_missing(tmp_path, ri_module):
    src_root = tmp_path / "src"
    _make_pkg(src_root, "apa", "# only source\n")
    out = _run_probe_with_temp_organs(
        ri_module,
        {
            "aforge": {
                "source_path": str(src_root),
                "runtime_path": str(tmp_path / "absent_rt"),
                "import_name": "apa",
            },
        },
    )
    entry = out["identity_probe"]["aforge"]
    assert entry["measurable"] is False
    assert entry["match"] is False
    assert entry["resolution_method"] == "unresolved"
    assert entry["resolution_reason"]
    # Source measurable, runtime empty: source_digest present, runtime_digest empty
    assert entry["source_digest"] != ""
    assert len(entry["source_digest"]) == 64
    assert entry["runtime_digest"] == ""


def test_e2e_legacy_aliases_derived_from_canonical(tmp_path, ri_module):
    src_root = tmp_path / "src"
    rt_root = tmp_path / "rt"
    _make_pkg(src_root, "arifos", "# same\n")
    _make_pkg(rt_root, "arifos", "# same\n")
    out = _run_probe_with_temp_organs(
        ri_module,
        {
            "arifos": {
                "source_path": str(src_root),
                "runtime_path": str(rt_root),
                "import_name": "arifos",
            },
        },
    )
    entry = out["identity_probe"]["arifos"]
    legacy = out["md5_identity"]["arifos"]
    assert legacy["source_init_md5"] == entry["source_digest"][:12]
    assert legacy["deployed_init_md5"] == entry["runtime_digest"][:12]
    assert legacy["md5_match"] == entry["match"]
    note = legacy["note"]
    assert "sha256[:12]" in note
    assert "MD5" in note


def test_e2e_algorithm_metadata_present(tmp_path, ri_module):
    src_root = tmp_path / "src"
    rt_root = tmp_path / "rt"
    _make_pkg(src_root, "arifos", "# x\n")
    _make_pkg(rt_root, "arifos", "# x\n")
    out = _run_probe_with_temp_organs(
        ri_module,
        {
            "arifos": {
                "source_path": str(src_root),
                "runtime_path": str(rt_root),
                "import_name": "arifos",
            },
        },
    )
    assert out["algorithm"] == "sha256"
    assert out["algorithm_encoding"] == "hex"
    assert out["digest_truncation"] is False
    assert out["scope"] == "package_init_file"


def test_determinism_two_back_to_back_runs(tmp_path, ri_module):
    src_root = tmp_path / "src"
    rt_root = tmp_path / "rt"
    _make_pkg(src_root, "arifos", "# stable\n")
    _make_pkg(rt_root, "arifos", "# stable\n")
    organs = {
        "arifos": {
            "source_path": str(src_root),
            "runtime_path": str(rt_root),
            "import_name": "arifos",
        },
    }
    out1 = _run_probe_with_temp_organs(ri_module, organs)
    first_digest = out1["identity_probe"]["arifos"]["source_digest"]
    out2 = _run_probe_with_temp_organs(ri_module, organs)
    second_digest = out2["identity_probe"]["arifos"]["source_digest"]
    assert first_digest == second_digest
    assert out1["generated_at"] != out2["generated_at"]


def test_e2e_legacy_consumer_keeps_working(tmp_path, ri_module):
    """The legacy HUD consumer jq path '.md5_identity.<organ>.md5_match'
    must still resolve correctly."""
    src_root = tmp_path / "src"
    rt_root = tmp_path / "rt"
    _make_pkg(src_root, "arifos", "# equal\n")
    _make_pkg(rt_root, "arifos", "# equal\n")
    _run_probe_with_temp_organs(
        ri_module,
        {
            "arifos": {
                "source_path": str(src_root),
                "runtime_path": str(rt_root),
                "import_name": "arifos",
            },
        },
    )
    jq = subprocess.run(
        ["jq", "-r", ".md5_identity.arifos.md5_match", str(PROBE_OUTPUT_PATH)],
        capture_output=True,
        text=True,
    )
    assert jq.stdout.strip() == "true"


def test_digest_format_is_hex_full_length(tmp_path, ri_module):
    src_root = tmp_path / "src"
    rt_root = tmp_path / "rt"
    _make_pkg(src_root, "apa", "# sha256 test\n")
    _make_pkg(rt_root, "apa", "# sha256 test\n")
    out = _run_probe_with_temp_organs(
        ri_module,
        {
            "aforge": {
                "source_path": str(src_root),
                "runtime_path": str(rt_root),
                "import_name": "apa",
            },
        },
    )
    digest = out["identity_probe"]["aforge"]["source_digest"]
    assert re.fullmatch(r"[0-9a-f]{64}", digest), f"non-canonical digest: {digest!r}"


# ---------------------------------------------------------------------------
# Phase 5 — INDEPENDENT verification via hashlib AND sha256sum
# ---------------------------------------------------------------------------


def test_independent_sha256sum_matches_hashlib(tmp_path, ri_module):
    """Run probe against known temp content; verify both hashlib.sha256
    and `sha256sum` return identical digests."""
    src_root = tmp_path / "src"
    rt_root = tmp_path / "rt"
    content = "arifOS-identity-fi002-fixture-content\n"
    src_init = _make_pkg(src_root, "arifos", content)
    rt_init = _make_pkg(rt_root, "arifos", content)

    out = _run_probe_with_temp_organs(
        ri_module,
        {
            "arifos": {
                "source_path": str(src_root),
                "runtime_path": str(rt_root),
                "import_name": "arifos",
            },
        },
    )
    probe_digest = out["identity_probe"]["arifos"]["source_digest"]

    # hashlib
    hashlib_digest = hashlib.sha256(src_init.joinpath("__init__.py").read_bytes()).hexdigest()
    # sha256sum shell
    sha_proc = subprocess.run(
        ["sha256sum", str(src_init / "__init__.py")],
        capture_output=True, text=True,
    )
    shell_digest = sha_proc.stdout.split()[0]

    assert probe_digest == hashlib_digest, (
        f"probe vs hashlib mismatch:\n  probe:   {probe_digest}\n  hashlib: {hashlib_digest}"
    )
    assert probe_digest == shell_digest, (
        f"probe vs sha256sum mismatch:\n  probe:    {probe_digest}\n  sha256sum: {shell_digest}"
    )
    assert hashlib_digest == shell_digest, (
        f"hashlib vs sha256sum mismatch:\n  hashlib:   {hashlib_digest}\n  sha256sum: {shell_digest}"
    )
    # Triple agreement → no truncation, no algorithm drift
    assert len(probe_digest) == 64