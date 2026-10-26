"""Phase 1 — aaa-mcp READ-ONLY kill-switch tests (2026-10-24 · kimi-code/FI-008).

Contract: aaa-mcp (:3002) exposes ONLY read-class tools. Any non-read-class
tool must be refused at startup (fail closed). Mutation belongs to the F13
signing lane (:18900) + judge/seal — never MCP.

TRUTH-CORRECTION (2026-10-24): the "3 tests green" claim inside commit
441ca6d0 was PREMATURE — the module path was wrong (parents[1] vs parents[2])
and all three tests errored on FileNotFoundError. Fixed here; verified green
under /usr/bin/python3 3.13.7 + fastmcp 4.0.4. Claim discipline: run tests
BEFORE the commit message asserts them.
"""
import importlib.util
import pathlib

MOD_PATH = pathlib.Path(__file__).resolve().parents[2] / "mcp" / "aaa_mcp_fastmcp.py"


def _load():
    spec = importlib.util.spec_from_file_location("aaa_mcp_fastmcp", MOD_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_allowlist_passes():
    mod = _load()
    assert mod._assert_read_class(mod.READ_CLASS_ALLOWLIST) is True


def test_offender_refused_fail_closed():
    mod = _load()
    try:
        mod._assert_read_class(["aaa_health", "aaa_register_agent"])
        raise AssertionError("kill-switch did not fire")
    except RuntimeError as exc:
        assert "READ-ONLY KILL-SWITCH" in str(exc)
        assert "aaa_register_agent" in str(exc)


def test_live_registry_is_read_class():
    mod = _load()
    assert mod._kill_switch_audit() is True


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
