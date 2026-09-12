"""
OpenClaw AGI Orchestrator Runtime Package

Components:
  - semantic_router: LLM-based intent classification (Phase 1)
  - dag_engine: Declarative DAG workflow execution (Phase 2)
  - state_manager: Cross-session state per person_id (Phase 3)
  - observability: Traces, token budget, FQ correlation (Phase 4)
  - channel_manager: Multi-channel abstraction (Phase 5)
  - orchestrator: The brain that ties it all together

Usage:
  from openclaw.runtime.orchestrator import process_message, get_orchestrator
  from openclaw.runtime.semantic_router import classify_intent
  from openclaw.runtime.dag_engine import define_workflow, execute_workflow

DITEMPA BUKAN DIBERI
"""
