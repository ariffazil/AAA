# arifos_openai_agents

**Cognition firewall wrapper for OpenAI Agents SDK.**

Forged 2026-06-17 by FORGE (000Ω). Implements the Band 1 cognition-firewall
pattern: every agent must call `_arifos_prethink` before any other tool,
classify its intent, and receive the kernel's verdict before it can act.

## Install

```bash
pip install -e .
```

(Requires `openai-agents` from PyPI.)

## The 4 guards

| Guard | When | What |
|---|---|---|
| `arifos_prethink` | Before LLM decides action | Classify intent, get kernel verdict |
| `arifos_pretool` | Before any tool call | Verify lease, check scope |
| `arifos_posttool` | After tool result | F2 epistemic stamp, taint check |
| `arifos_seal` | End of agent run | VAULT999 write, audit completion |

The single `Decision` object flows through all 4.

## Usage

```python
from agents import Agent, Runner, function_tool
from arifos_openai_agents import ArifKernel

@function_tool
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

agent = Agent(
    name="CodexCoder",
    instructions="You are a code review assistant.",
    tools=[read_file],
)

kernel = ArifKernel(
    base_url="https://arifos.arif-fazil.com",
    actor_id="arif",
)

wrapped = kernel.wrap(agent)
result = await Runner.run(wrapped, "Read /etc/hostname")
print(result.final_output)
print(result._arifos_seal)  # VAULT999 pointer
```

## The 21-test contract

```bash
pytest arifos_openai_agents/tests/test_21_contract.py -v
```

5 categories × tests:

- **Authority** (5): actor identity, lease scope, jurisdiction
- **Reversibility** (5): blast-radius, 888 HOLD triggers
- **Tool** (5): pretool gating, schema, scope discipline
- **State** (3): seal pointer, audit chain
- **Agent** (3): prethink enforcement, F2 stamp

## Live integration test

```bash
pytest arifos_openai_agents/tests/test_live_integration.py -m live_integration
```

Talks to the public arifOS MCP at `arifos.arif-fazil.com`.

## DITEMPA BUKAN DIBERI

Forged, not given. F1 AMANAH. F2 TRUTH. F13 SOVEREIGN.
