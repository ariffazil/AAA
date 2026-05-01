"""
ACP Server — FastAPI-based ACP endpoint that wraps Hermes as an ACP agent.
Runs on port 8082. Implements the ACP protocol from agentcommunicationprotocol.dev.

Routes:
    GET  /                   → discovery info
    GET  /agents             → list agent cards
    GET  /agents/{id}        → get agent card
    POST /runs               → create a new task run
    GET  /runs/{id}          → get run status + result
    GET  /runs/{id}/events   → SSE stream of run events
    DELETE /runs/{id}        → cancel a run
    GET  /health             → health check
"""

from __future__ import annotations

import asyncio
import uuid
import threading
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn

from AAA.acp.models import AgentCard, ACPTask, ACPMessage, ACPSkill, ACPCapabilities, ACPProvider


# ─── Hermes Agent Card ─────────────────────────────────────────────────────────

HERMES_CARD = AgentCard(
    id="hermes",
    name="Hermes",
    description="Memory engine + deep reasoning specialist. Manages AAA institutional memory, recall, and reasoning chains.",
    url="http://localhost:8082",
    preferred_transport="jsonrpc-sse",
    provider=ACPProvider(organization="arifOS", system="AAA", runtime="ollama"),
    version="1.0.0",
    capabilities=ACPCapabilities(
        streaming=True,
        push_notifications=False,
        authenticated_extended_card=False,
        input_modes=["text/plain", "application/json"],
        output_modes=["text/plain", "application/json"],
    ),
    skills=[
        ACPSkill(
            id="memory-recall",
            name="Memory Recall",
            description="Retrieve past session context, decisions, and accumulated knowledge",
            tags=["recall", "memory", "search"],
            examples=["what was decided about the MCP server config last week", "find all mentions of GEOX in memory"],
        ),
        ACPSkill(
            id="reasoning-chain",
            name="Reasoning Chains",
            description="Structured step-by-step reasoning for complex problems",
            tags=["reason", "infer", "analyze"],
            examples=["trace the logic behind this architectural decision", "what are the implications of this change"],
        ),
        ACPSkill(
            id="memory-curation",
            name="Memory Curation",
            description="Maintain and update the institutional memory index",
            tags=["curate", "organize", "index"],
            examples=["update memory with today's decisions", "rebuild the memory index"],
        ),
    ],
)


# ─── In-memory run store ───────────────────────────────────────────────────────

class RunStore:
    """Thread-safe in-memory store for ACP runs."""
    
    def __init__(self):
        self._runs: dict[str, ACPTask] = {}
        self._lock = threading.Lock()

    def create(self, task: ACPTask) -> ACPTask:
        with self._lock:
            self._runs[task.id] = task
        return task

    def get(self, run_id: str) -> Optional[ACPTask]:
        with self._lock:
            return self._runs.get(run_id)

    def update(self, run_id: str, **fields) -> Optional[ACPTask]:
        with self._lock:
            if run_id not in self._runs:
                return None
            task = self._runs[run_id]
            for k, v in fields.items():
                if hasattr(task, k):
                    setattr(task, k, v)
            task.updated_at = datetime.utcnow()
            return task

    def delete(self, run_id: str) -> bool:
        with self._lock:
            if run_id in self._runs:
                del self._runs[run_id]
                return True
            return False

    def list(self) -> list[ACPTask]:
        with self._lock:
            return list(self._runs.values())


RUNS = RunStore()


# ─── Hermes execution engine ───────────────────────────────────────────────────

async def execute_hermes(task: ACPTask) -> ACPTask:
    """
    Execute a Hermes ACP task.
    This is the bridge between ACP and Hermes agent runtime.
    Currently delegates to Hermes recall and reasoning via subprocess.
    """
    import subprocess, json, sys
    
    skill_id = task.skill_id or "memory-recall"
    content = task.message.content

    # Map ACP skill → Hermes command
    if skill_id == "memory-recall":
        cmd = ["python3", "-m", "hermes_tools", "recall", content]
    elif skill_id == "reasoning-chain":
        cmd = ["python3", "-m", "hermes_tools", "reason", content]
    elif skill_id == "memory-curation":
        cmd = ["python3", "-m", "hermes_tools", "curate", content]
    else:
        # Default: send to Hermes for general reasoning
        cmd = ["python3", "-m", "hermes_tools", "invoke", content, "--agent", "hermes"]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=55,
        )
        output = result.stdout.strip() or result.stderr.strip() or "(no output)"
        task.result = output
        task.status = "completed"
    except subprocess.TimeoutExpired:
        task.error = "Execution timed out after 55s"
        task.status = "failed"
    except Exception as e:
        task.error = f"Execution error: {str(e)}"
        task.status = "failed"

    task.updated_at = datetime.utcnow()
    return task


# ─── ACP Request/Response models ───────────────────────────────────────────────

class RunCreatePayload(BaseModel):
    agent_id: str
    message: dict
    skill_id: Optional[str] = None
    session_id: Optional[str] = None


class AgentsListResponse(BaseModel):
    agents: list[dict]


# ─── SSE event streaming ───────────────────────────────────────────────────────

async def run_event_stream(run_id: str):
    """SSE generator for run status changes."""
    import time
    
    last_status = None
    for _ in range(300):  # ~60s max
        task = RUNS.get(run_id)
        if task is None:
            yield "data: {\"error\": \"run not found\"}\n\n"
            break
        
        if task.status != last_status:
            last_status = task.status
            event_type = f"run.{task.status}"
            data = {
                "type": event_type,
                "run_id": task.id,
                "status": task.status,
                "result": task.result,
                "error": task.error,
                "timestamp": task.updated_at.isoformat(),
            }
            yield f"data: {json.dumps(data)}\n\n"
        
        if task.status in ("completed", "failed", "cancelled"):
            break
        
        await asyncio.sleep(0.2)
    
    yield "data: [DONE]\n\n"


# ─── FastAPI app ───────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[ACP/Hermes] Starting Hermes ACP server on :8082")
    yield
    print("[ACP/Hermes] Shutting down")


app = FastAPI(
    title="Hermes ACP Agent",
    description="ACP-compliant agent endpoint for Hermes (AAA Memory Engine)",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {
        "name": "Hermes ACP Agent",
        "version": "1.0.0",
        "protocol": "ACP (agentcommunicationprotocol.dev)",
        "agent_id": "hermes",
        "status": "operational",
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "hermes", "timestamp": datetime.utcnow().isoformat()}


@app.get("/agents")
async def list_agents():
    return AgentsListResponse(agents=[HERMES_CARD.model_dump()])


@app.get("/agents/{agent_id}")
async def get_agent_card(agent_id: str):
    if agent_id == "hermes":
        return HERMES_CARD
    raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")


@app.post("/runs", status_code=201)
async def create_run(payload: RunCreatePayload, background: BackgroundTasks):
    if payload.agent_id != "hermes":
        raise HTTPException(status_code=400, detail=f"Unknown agent: {payload.agent_id}")

    task = ACPTask(
        id=str(uuid.uuid4()),
        agent_id=payload.agent_id,
        session_id=payload.session_id,
        skill_id=payload.skill_id,
        message=ACPMessage(content=payload.message.get("content", "")),
        status="pending",
    )
    RUNS.create(task)

    # Execute asynchronously
    background.add_task(execute_hermes, task)

    return task


@app.get("/runs/{run_id}")
async def get_run(run_id: str):
    task = RUNS.get(run_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")
    return task


@app.get("/runs/{run_id}/events")
async def stream_run_events(run_id: str):
    task = RUNS.get(run_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")
    return StreamingResponse(
        run_event_stream(run_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.delete("/runs/{run_id}")
async def cancel_run(run_id: str):
    task = RUNS.get(run_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")
    if task.status in ("completed", "failed", "cancelled"):
        raise HTTPException(status_code=409, detail=f"Run already in terminal state: {task.status}")
    RUNS.update(run_id, status="cancelled")
    return {"status": "cancelled", "run_id": run_id}


# ─── CLI launcher ──────────────────────────────────────────────────────────────

def main():
    uvicorn.run(app, host="0.0.0.0", port=8082, log_level="info")


if __name__ == "__main__":
    main()
