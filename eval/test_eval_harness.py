import json

import agent_adapter
import run_aaa_eval
from agent_adapter import AgentResult


def test_live_eval_prompt_does_not_include_gold_label():
    case = {
        "id": "case-1",
        "input": "Do the thing",
        "context": "Context",
        "goal": "Goal",
        "floor_refs": ["F1"],
        "expected_decision": "REFUSE",
    }

    prompt = agent_adapter._build_live_eval_prompt(case)
    candidate = agent_adapter._build_mcp_candidate(case)

    assert "expected_decision" not in prompt
    assert "Expected decision" not in prompt
    assert "REFUSE" not in prompt
    assert "expected_decision" not in candidate
    assert "Expected decision" not in candidate
    assert "REFUSE" not in candidate


def test_mcp_parser_reads_top_level_verdict():
    inner = {"verdict": "SEAL", "reasons": ["ok"]}
    result = {"result": {"content": [{"text": json.dumps(inner)}]}}

    verdict, response_text, error = agent_adapter._parse_mcp_result(result)

    assert verdict == "SEAL"
    assert response_text == "ok"
    assert error is None


def test_mcp_parser_reads_nested_result_verdict():
    inner = {"result": {"verdict": "HOLD", "reasons": ["needs review"]}}
    result = {"result": {"content": [{"text": json.dumps(inner)}]}}

    verdict, response_text, error = agent_adapter._parse_mcp_result(result)

    assert verdict == "HOLD"
    assert response_text == "needs review"
    assert error is None


def test_scoring_normalizes_arifos_verdicts():
    proceed_case = {"id": "p", "expected_decision": "PROCEED"}
    refuse_case = {"id": "r", "expected_decision": "REFUSE"}

    proceed = run_aaa_eval.score_case(
        proceed_case,
        AgentResult(response_text="VERDICT: SEAL", verdict="SEAL", latency_ms=1.0),
    )
    refuse = run_aaa_eval.score_case(
        refuse_case,
        AgentResult(response_text="VERDICT: VOID", verdict="VOID", latency_ms=1.0),
    )

    assert proceed.decision_match is True
    assert proceed.expected_decision == "PROCEED"
    assert proceed.predicted_verdict == "PROCEED"
    assert refuse.decision_match is True
    assert refuse.expected_decision == "REFUSE"
    assert refuse.predicted_verdict == "REFUSE"


def test_run_eval_passes_none_limit_through(monkeypatch):
    seen = {}

    def fake_load_gold_cases(limit=None):
        seen["limit"] = limit
        return [{"id": "case-1", "expected_decision": "PROCEED"}]

    def fake_run_agent_case(case, mode="mock", responses_path=""):
        return AgentResult(response_text="VERDICT: PROCEED", verdict="PROCEED", latency_ms=1.0)

    monkeypatch.setattr(run_aaa_eval, "load_gold_cases", fake_load_gold_cases)
    monkeypatch.setattr(run_aaa_eval, "run_agent_case", fake_run_agent_case)

    report = run_aaa_eval.run_eval(mode="mock", limit=None)

    assert seen["limit"] is None
    assert report.total_cases == 1
