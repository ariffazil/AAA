#!/usr/bin/env python3
"""Tests for voice_gate.py -- the STYLE FIREWALL.

Case (a) is the measured blind spot this work exists for: a paragraph of PURE machine
register that used to return "mechanical verdict: PASS".

Run:   python3 -m pytest test_voice_gate.py -q

W_SCAR NOTE: every fixture in this file is neutral filler. There is no money, health or
legal claim anywhere in it -- deliberately, so the scar gate has nothing to trip on.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
GATE = HERE / "voice_gate.py"

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

# (a) THE BLIND SPOT. Verbatim, the paragraph that used to PASS.
MACHINE_REGISTER = (
    "PRIVATE_QUALIA. CAP_AUTHORITY_OR_STOP. The record requires UNKNOWN_UNCREATED. "
    "Do not diagnose. Return authority to the humans. "
    "quarantined_private_records_count is zero. RASA_HOLD engaged. "
    "DO_NOT_HALLUCINATE_CLOSURE applies."
)

# snake_case only, no shouting -- isolates the identifier rule from the caps rule.
SNAKE_ONLY = (
    "the draft carries claim_state and quarantine_count fields. "
    "the renderer drops them before send. "
    "the human sees prose."
)

# (b) A genuine receipt / code block. Correct register on the INTERNAL lane.
CODE_RECEIPT = (
    "$ python3 voice_gate.py --file reply.txt --json\n"
    "{\n"
    '  "mechanical_verdict": "PASS",\n'
    '  "trace_id": "8f3c1a9e",\n'
    '  "state": "SEALED"\n'
    "}"
)

# An identifier the author is TALKING ABOUT, not using. Mention, not use.
QUOTED_IDENTIFIER = (
    'Aku tanya dia apa maksud "PRIVATE_QUALIA" semalam, dia pun tak tahu. '
    "Aku rasa kita kena jelaskan sendiri."
)

# (c) Natural short human paragraph. Must still pass.
NATURAL_SHORT = (
    "Aku baru sampai rumah. "
    "Tadi jalan jam teruk, dekat sejam duduk dalam kereta. "
    "Dia mesej tanya aku ok ke tak. "
    "Aku belum balas lagi."
)

# Same register, but with real paragraph breaks so the structure ratio can be read.
PARAGRAPHED = (
    "Aku dah balik dari opis tadi, jalan jam teruk dekat sejam.\n\n"
    "Dia mesej tanya aku ok ke tak, aku belum balas. "
    "Aku rasa dia cuma nak tahu.\n\n"
    "Kalau kau nak, aku boleh tanya dia terus lepas ni."
)

# (d) Template-heavy: 'X bukan Y' three times + aphorism closer.
TEMPLATE_HEAVY = (
    "Bukan data yang penting, tapi makna. "
    "Kerja kita bukan menulis laporan, tapi memilih apa yang perlu dilihat. "
    "Sistem ini bukan mesin, tapi cermin. "
    "Kadang aku rasa kita terlalu sibuk membina. "
    "Kadang aku rasa kita lupa untuk berhenti. "
    "Kadang aku rasa mesin ini sudah cukup. "
    "Ketepatan bukan kebenaran."
)

# (e) Long prose, near-identical sentence lengths. A visible template.
LOW_VARIANCE = (
    "Aku duduk sini tengok skrin lama sangat. "
    "Kadang aku rasa benda ini jalan lambat. "
    "Malam tadi kami tunggu sampai pukul dua. "
    "Dia kata nak balas lepas habis kerja. "
    "Aku buka fail lama dan baca semula. "
    "Radio main lagu lama dari zaman dulu. "
    "Petang nanti kita cuba tanya dia balik. "
    "Sekarang aku tutup skrin dan diam."
)

# Pre-existing behaviour that must not have been broken by this work.
LEGACY_AI_SPEAK = "Saya rasa adalah penting untuk kita fikirkan semula perkara ini."


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def run(text: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GATE), *args],
        input=text, capture_output=True, text=True, timeout=60,
    )


def run_json(text: str, audience: str = "human") -> tuple[int, dict]:
    p = run(text, "--json", "--audience", audience)
    return p.returncode, json.loads(p.stdout)


def labels(data: dict) -> set[tuple[str, str]]:
    return {(f["gate"], f["label"]) for f in data["findings"]}


def severities(data: dict) -> list[str]:
    return [f["severity"] for f in data["findings"]]


# ---------------------------------------------------------------------------
# (a) THE BLIND SPOT
# ---------------------------------------------------------------------------


def test_a_machine_register_paragraph_is_no_longer_a_pass():
    """Was: 'mechanical verdict: PASS'. Must now be RE-DRAFT."""
    rc, data = run_json(MACHINE_REGISTER)
    assert data["mechanical_verdict"] == "RE-DRAFT", (
        "the machine-register paragraph is still passing -- the blind spot is back"
    )
    assert rc in (1, 2), f"expected a non-zero re-draft/cooldown code, got {rc}"


def test_a_machine_register_paragraph_is_flagged_for_identifiers():
    _, data = run_json(MACHINE_REGISTER)
    live = [f for f in data["findings"]
            if f["gate"] == "MachineToken" and f["severity"] == "FLAG"]
    assert live, "no MachineToken FLAG raised"
    found = live[0]["match"]
    for token in ("PRIVATE_QUALIA", "CAP_AUTHORITY_OR_STOP", "UNKNOWN_UNCREATED",
                  "RASA_HOLD", "quarantined_private_records_count"):
        assert token in found, f"{token} not reported as a live machine token"
    assert live[0]["count"] >= 5
    assert live[0]["suggestion"], "finding carries no rewrite hint"


def test_a_machine_register_paragraph_exit_code_is_sabar_because_it_also_shouts():
    """Documented precedence: SABAR (2) wins over RE-DRAFT (1). Not a regression --
    the caps ratio in that paragraph is genuinely shouting. The verdict is still
    RE-DRAFT; the exit code only orders which fix comes first."""
    rc, data = run_json(MACHINE_REGISTER)
    assert data["sabar_triggered"] is True
    assert rc == 2
    assert data["mechanical_verdict"] == "RE-DRAFT"


def test_a_snake_case_only_draft_exits_redraft():
    """Isolates the identifier rule from the caps/SABAR rule."""
    rc, data = run_json(SNAKE_ONLY)
    assert rc == 1, f"expected exit 1 (re-draft), got {rc}"
    assert ("MachineToken", "machine_identifier_in_prose") in labels(data)
    assert data["gates_mechanical"]["machine_tokens"].startswith("FLAG")


# ---------------------------------------------------------------------------
# (b) CODE / RECEIPT ON THE INTERNAL LANE
# ---------------------------------------------------------------------------


def test_b_code_and_receipt_pass_on_the_internal_lane():
    rc, data = run_json(CODE_RECEIPT, audience="internal")
    assert rc == 0, f"internal code receipt did not pass: rc={rc}, {data['findings']}"
    assert data["mechanical_verdict"] == "PASS"


def test_b_internal_lane_skips_the_style_firewall_and_says_so():
    _, data = run_json(CODE_RECEIPT, audience="internal")
    assert data["gates_mechanical"]["style_firewall"].startswith("SKIPPED")
    assert ("StyleFirewall", "style_checks_skipped") in labels(data)
    assert "machine_tokens" not in data["gates_mechanical"]


def test_b_machine_register_is_legitimate_on_the_internal_lane():
    """The same paragraph that must fail at the human boundary must NOT be failed
    behind it. Internal register is not human register."""
    _, data = run_json(MACHINE_REGISTER, audience="internal")
    assert data["mechanical_verdict"] == "PASS"
    assert not [f for f in data["findings"] if f["gate"] == "MachineToken"]


def test_b_identifiers_inside_a_code_fence_are_mention_not_use():
    _, data = run_json(CODE_RECEIPT, audience="human")
    assert ("MachineToken", "machine_identifier_in_prose") not in labels(data)


def test_b_quoted_identifier_is_info_only_human_lane():
    rc, data = run_json(QUOTED_IDENTIFIER)
    assert rc == 0, f"mention was treated as use: rc={rc} {data['findings']}"
    assert ("MachineToken", "identifier_in_code_or_quote") in labels(data)
    assert ("MachineToken", "machine_identifier_in_prose") not in labels(data)
    info = next(f for f in data["findings"] if f["label"] == "identifier_in_code_or_quote")
    assert "PRIVATE_QUALIA" in info["match"]
    assert data["gates_mechanical"]["machine_tokens"].startswith("PASS")
    assert "code-or-quoted 1" in data["gates_mechanical"]["machine_tokens"]


# ---------------------------------------------------------------------------
# (c) NATURAL SHORT HUMAN PARAGRAPH
# ---------------------------------------------------------------------------


def test_c_natural_short_paragraph_still_passes():
    rc, data = run_json(NATURAL_SHORT)
    assert rc == 0, f"natural reply was rejected: {data['findings']}"
    assert data["mechanical_verdict"] == "PASS"
    assert data["findings"] == [], f"false positives: {data['findings']}"


def test_c_natural_short_paragraph_is_short_enough_to_skip_entropy():
    _, data = run_json(NATURAL_SHORT)
    assert data["gates_mechanical"]["style_entropy"].startswith("SKIP")


# ---------------------------------------------------------------------------
# (d) TEMPLATE REPETITION
# ---------------------------------------------------------------------------


def test_d_template_heavy_draft_is_flagged():
    rc, data = run_json(TEMPLATE_HEAVY)
    assert rc == 1, f"template-heavy draft passed: {data['findings']}"
    assert data["mechanical_verdict"] == "RE-DRAFT"
    lab = labels(data)
    assert ("Template", "mirrored_construction_repeat") in lab
    assert ("Template", "aphorism_manufacturing") in lab
    assert ("Template", "aphorism_closer") in lab


def test_d_mirrored_construction_count_is_reported_not_vibed():
    _, data = run_json(TEMPLATE_HEAVY)
    f = next(x for x in data["findings"]
             if x["label"] == "mirrored_construction_repeat")
    assert f["count"] == 3, f"expected 3 mirrored constructions, counted {f['count']}"
    assert "3 konstruksi" in f["match"]
    assert "kontras_bukan" in f["match"]


def test_d_sentence_opener_repetition_is_counted():
    _, data = run_json(TEMPLATE_HEAVY)
    ops = [x for x in data["findings"] if x["label"] == "sentence_opener_repeat"]
    assert ops, "repeated 'Kadang' opener not reported"
    assert "'kadang' buka 3/" in ops[0]["match"]


# ---------------------------------------------------------------------------
# (e) STYLE ENTROPY
# ---------------------------------------------------------------------------


def test_e_low_sentence_length_variance_is_flagged():
    rc, data = run_json(LOW_VARIANCE)
    assert rc == 1, f"low-variance prose passed: {data['findings']}"
    assert ("Entropy", "low_sentence_variance") in labels(data)
    f = next(x for x in data["findings"] if x["label"] == "low_sentence_variance")
    assert f["severity"] == "FLAG"
    assert "cv" in f["match"]


def test_e_entropy_gate_reports_the_numbers():
    _, data = run_json(LOW_VARIANCE)
    gate = data["gates_mechanical"]["style_entropy"]
    assert "cv" in gate and "sd" in gate and "mean" in gate


def test_e_entropy_gate_does_not_fire_on_a_short_reply():
    """Variance is meaningless over 3 sentences; the gate must say SKIP, not guess."""
    _, data = run_json("Aku penat. Hari ni panjang sangat. Esok kita sambung.")
    assert data["gates_mechanical"]["style_entropy"].startswith("SKIP")


# ---------------------------------------------------------------------------
# (5) VERDICT-WORD LEAKAGE
# ---------------------------------------------------------------------------


def test_verdict_lexicon_fires_on_state_transition_vocabulary():
    rc, data = run_json(
        "Benda tu sekarang dalam keadaan HOLD sebab satu pihak belum jawab. "
        "Aku akan bagitau bila SEAL sudah siap."
    )
    assert rc == 1
    assert ("Verdict", "state_transition") in labels(data)


def test_verdict_lexicon_fires_on_receipt_language():
    _, data = run_json("Receipt untuk kerja tu sudah aku simpan. Verdict dia masih sama.")
    lab = labels(data)
    assert ("Verdict", "receipt_label") in lab
    assert ("Verdict", "verdict_word") in lab


def test_verdict_lexicon_does_not_fire_on_ordinary_words():
    _, data = run_json(NATURAL_SHORT)
    assert not [f for f in data["findings"] if f["gate"] == "Verdict"]


# ---------------------------------------------------------------------------
# (3) STRUCTURE HEAVINESS  /  (6) VOLUME CEILING
# ---------------------------------------------------------------------------


def test_structure_heaviness_flags_a_bullet_report():
    draft = (
        "# Status\n"
        "- benda satu sudah siap\n"
        "- benda dua masih jalan\n"
        "- benda tiga belum mula\n"
        "- benda empat tunggu orang\n"
        "Aku akan update kemudian bila semua sudah jelas.\n"
    )
    rc, data = run_json(draft)
    assert rc == 1, f"bullet report passed: {data['findings']}"
    assert any(f["gate"] == "Structure" for f in data["findings"])


def test_structure_ratio_is_reported():
    rc, data = run_json(PARAGRAPHED)
    assert rc == 0, f"natural multi-paragraph reply rejected: {data['findings']}"
    assert "struktur:prosa" in data["gates_mechanical"]["structure"]
    assert "3 perenggan" in data["gates_mechanical"]["structure"]


def test_volume_ceiling_flags_a_long_draft():
    long_draft = " ".join(
        f"Ayat nombor {i} ini ditulis dengan panjang yang sama supaya ia jadi tebal sekali."
        for i in range(1, 61)
    )
    rc, data = run_json(long_draft)
    assert rc == 1, f"long draft passed: {data['gates_mechanical']['volume']}"
    assert ("Volume", "volume_ceiling") in labels(data)
    assert data["gates_mechanical"]["volume"].startswith("FLAG")


def test_volume_ceiling_absent_on_a_short_turn():
    _, data = run_json(NATURAL_SHORT)
    assert data["gates_mechanical"]["volume"].startswith("PASS")


# ---------------------------------------------------------------------------
# WITNESS DISCIPLINE: the interface, the limits, and the old behaviour
# ---------------------------------------------------------------------------


def test_interface_exit_codes_unchanged():
    assert run(NATURAL_SHORT).returncode == 0
    assert run(TEMPLATE_HEAVY).returncode == 1
    assert run(MACHINE_REGISTER).returncode == 2
    assert run("", "--file", "/nonexistent/path/xyz.txt").returncode == 3


def test_empty_input_is_a_usage_error():
    p = run("   \n  ")
    assert p.returncode == 3
    assert "empty input" in p.stderr


def test_json_contract_is_intact():
    _, data = run_json(NATURAL_SHORT)
    for key in ("audience", "words", "sentences", "mechanical_verdict", "sabar_triggered",
                "sabar_reasons", "gates_mechanical", "judgment_only", "findings",
                "limits", "disclaimer"):
        assert key in data, f"json key {key!r} disappeared"
    assert data["audience"] == "human"
    for f in data["findings"]:
        for key in ("gate", "severity", "label", "match", "suggestion", "count"):
            assert key in f


def test_limits_are_stated_on_every_human_run():
    """A witness that hides its blindness is not a witness."""
    _, data = run_json(NATURAL_SHORT)
    assert len(data["limits"]) >= 8
    joined = " ".join(data["limits"]).lower()
    assert "honest compression" in joined
    assert "correctness" in joined
    assert "sarcasm" in joined
    assert "read" in joined


def test_limits_are_printed_in_text_mode():
    out = run(NATURAL_SHORT).stdout
    assert "LIMITS - WHAT THIS CHECKER CANNOT SEE" in out
    assert "PASS here means only" in out


def test_verdict_precedence_unchanged():
    """RE-DRAFT if any FLAG, or more than two WARNs. Existing contract, untouched."""
    _, data = run_json(MACHINE_REGISTER)
    assert any(f["severity"] == "FLAG" for f in data["findings"])
    assert data["mechanical_verdict"] == "RE-DRAFT"


def test_legacy_ai_speak_bank_still_fires():
    rc, data = run_json(LEGACY_AI_SPEAK)
    assert rc == 1
    lab = labels(data)
    assert ("Density", "pronoun_ban") in lab
    assert ("Density", "bm_formal_filler") in lab


def test_thermal_mode_still_works():
    p = run(NATURAL_SHORT, "--thermal")
    assert p.returncode == 0
    assert "SABAR: quiet" in p.stdout
    p2 = run(MACHINE_REGISTER, "--thermal")
    assert p2.returncode == 2
    assert "SABAR: TRIGGERED" in p2.stdout


def test_suggestion_is_present_on_every_flag():
    """A finding without a rewrite hint is a complaint, not a firewall."""
    _, data = run_json(TEMPLATE_HEAVY)
    for f in data["findings"]:
        if f["severity"] == "FLAG":
            assert f["suggestion"], f"FLAG {f['label']} has no rewrite hint"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
