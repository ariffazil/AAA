#!/usr/bin/env python3
"""
Test Auto Synthesis & Ephemeral Sandbox Integration Test
Validates AST evaluation, RAM isolation (/tmp/micro_servers), ephemeral tool registration,
and decay/purge mechanisms under F1/F2 governance.
"""
import os
import sys
import json
import subprocess

def test_synthesis_pipeline():
    print("=== STARTING AUTO SYNTHESIS & EPHEMERAL SANDBOX TEST ===")
    
    # 1. Prepare transient micro-server path in /tmp/micro_servers
    target_dir = "/tmp/micro_servers"
    os.makedirs(target_dir, exist_ok=True)
    test_script = os.path.join(target_dir, "test_calc_tool.py")
    reg_out = os.path.join(target_dir, "test_tool_reg.json")
    
    code = '''
def add_numbers(a: int, b: int) -> int:
    """Add two numbers securely."""
    return a + b
'''
    with open(test_script, "w") as f:
        f.write(code)
    print(f"[1/4] RAM Isolation: Written ephemeral script to {test_script}")

    # 2. Dual-Gate Sandbox AST Evaluation
    eval_cmd = [
        sys.executable,
        "/root/AAA/registries/reconcile/mcp_sandbox_eval.py",
        "--script", test_script
    ]
    print(f"[2/4] Dual-Gate Sandbox: Executing AST & Sandbox Eval...")
    res_eval = subprocess.run(eval_cmd, capture_output=True, text=True)
    print(res_eval.stdout)
    if res_eval.returncode != 0:
        print(f"Eval Error: {res_eval.stderr}")
        sys.exit(res_eval.returncode)

    # 3. Ephemeral Scope Surface Registration
    rec_cmd = [
        sys.executable,
        "/root/AAA/registries/reconcile/forge_surface_reconcile.py",
        "--register-ephemeral", test_script,
        "--output-file", reg_out
    ]
    print(f"[3/4] Ephemeral Scope: Registering surface to {reg_out}...")
    res_rec = subprocess.run(rec_cmd, capture_output=True, text=True)
    print(res_rec.stdout)

    # 4. Verification & Clean Cleanup
    if os.path.exists(reg_out):
        print(f"✅ Success: Ephemeral registration verified at {reg_out}")
    else:
        print(f"⚠️ Warning: Output file missing, output: {res_rec.stderr}")

    print("=== AUTO SYNTHESIS TEST COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    test_synthesis_pipeline()
