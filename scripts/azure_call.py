#!/usr/bin/env python3
"""
azure_call — Call Azure AI Foundry directly, bypassing OpenCode's tool system.

Usage:
    azure_call.py "What is the current oil price?"
    azure_call.py --tools "Calculate NPV of [-100, 30, 40, 50, 60] at 10%"
    azure_call.py --search "Latest PETRONAS news"

Options:
    --tools     Use web_search + code_interpreter (Responses API)
    --search    Use web_search only (Responses API)
    --raw       Use Chat Completions (no tools, fastest)
    (default)   Chat Completions, no tools

Env: AZURE_OPENAI_KEY from /root/.secrets/vault.env
"""

import json
import sys
import os
import subprocess

import dotenv
dotenv.load_dotenv("/root/.secrets/vault.env", override=False)
KEY = os.environ.get("AZURE_OPENAI_KEY", "")
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "https://ariffazil-7416-resource.services.ai.azure.com/openai/v1")
MODEL = os.environ.get("AZURE_OPENAI_MODEL", "gpt-4.1-mini")


def call_chat_completions(prompt, max_tokens=1000):
    """Plain Chat Completions — no tools, fastest."""
    payload = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens})
    result = subprocess.run(
        [
            "curl",
            "-s",
            "-H",
            f"api-key: {KEY}",
            "-H",
            "Content-Type: application/json",
            "-d",
            payload,
            f"{ENDPOINT}/chat/completions",
        ],
        capture_output=True,
        text=True,
    )

    d = json.loads(result.stdout)
    if "error" in d and d["error"]:
        return {"error": d["error"].get("message", str(d["error"]))}
    return {
        "reply": d["choices"][0]["message"]["content"],
        "tokens": d.get("usage", {}),
        "model": d.get("model", MODEL),
    }


def call_responses(prompt, tools=None, max_tokens=2000):
    """Responses API with optional builtin tools."""
    if tools is None:
        tools = [{"type": "web_search"}]

    payload = json.dumps({"model": MODEL, "input": prompt, "tools": tools})
    result = subprocess.run(
        [
            "curl",
            "-s",
            "-H",
            f"api-key: {KEY}",
            "-H",
            "Content-Type: application/json",
            "-d",
            payload,
            f"{ENDPOINT}/responses",
        ],
        capture_output=True,
        text=True,
    )

    d = json.loads(result.stdout)
    if "error" in d and d["error"]:
        return {"error": d["error"].get("message", str(d["error"]))}

    output = {"status": d.get("status"), "tokens": d.get("usage", {})}

    for item in d.get("output", []):
        t = item.get("type")
        if t == "web_search_call":
            output["web_search_query"] = item.get("action", {}).get("query", "?")
        elif t == "code_interpreter_call":
            output["code_executed"] = item.get("code", "")
        elif t == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    output["reply"] = c["text"]

    return output


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: azure_call.py [--tools|--search|--raw] <prompt>")
        sys.exit(1)

    mode = "raw"
    prompt_parts = []

    for arg in args:
        if arg == "--tools":
            mode = "tools"
        elif arg == "--search":
            mode = "search"
        elif arg == "--raw":
            mode = "raw"
        else:
            prompt_parts.append(arg)

    prompt = " ".join(prompt_parts)
    if not prompt:
        print("Error: no prompt provided")
        sys.exit(1)

    if mode == "tools":
        tools = [{"type": "web_search"}, {"type": "code_interpreter", "container": {"type": "auto"}}]
        result = call_responses(prompt, tools)
    elif mode == "search":
        result = call_responses(prompt, [{"type": "web_search"}])
    else:
        result = call_chat_completions(prompt)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
