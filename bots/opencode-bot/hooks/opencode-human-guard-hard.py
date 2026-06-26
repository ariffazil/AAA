#!/usr/bin/env python3
"""HUMAN GUARD HARD — Blocks irreversible chaos. Plain English."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    tool_name = event.get("tool_name", "unknown")
    tool_input = event.get("tool_input", {})
    command = h.extract_command(tool_input) if tool_name == "Shell" else ""
    file_path = h.extract_file_path(tool_input) if tool_name in ("WriteFile", "StrReplaceFile") else ""

    block_reason = ""

    if tool_name == "Shell" and command:
        cmd = command.lower()
        if re.search(r"rm\s+-rf\s+/[^ ]*|rm\s+-rf\s+/\s*$|rm\s+-rf\s+/*", command, re.IGNORECASE):
            block_reason = "BLOCKED: This command would delete system files permanently. There is no undo. If you need to clean up a specific directory, name it explicitly (e.g., rm -rf /root/old-project)."
        elif re.search(r"rm\s+-rf\s+~|rm\s+-rf\s+\$HOME", command, re.IGNORECASE):
            block_reason = "BLOCKED: This would delete your entire home directory. Use rm on specific files or directories only."
        elif re.search(r"docker\s+system\s+prune\s*-a|docker\s+volume\s+prune", command, re.IGNORECASE):
            block_reason = "BLOCKED: This permanently deletes Docker volumes and images. If you need to free space, remove specific unused images instead."
        elif re.search(r"DROP\s+TABLE|DROP\s+DATABASE", command, re.IGNORECASE):
            block_reason = "BLOCKED: Database DROP commands permanently destroy data. If you really need this, run it manually outside the bot after confirming backups."
        elif re.search(r"DELETE\s+FROM", command, re.IGNORECASE) and "WHERE" not in command.upper():
            block_reason = "BLOCKED: DELETE FROM without WHERE would wipe the entire table. Add a WHERE clause, or run manually if intentional."
        elif re.search(r"git\s+push\s+.*--force|git\s+push\s+.*-f\b", command, re.IGNORECASE):
            block_reason = "BLOCKED: Force push rewrites shared history and can break other people's work. Use git revert or git merge instead. If absolutely necessary, do it manually."
        elif re.search(r"git\s+reset\s+--hard", command, re.IGNORECASE):
            block_reason = "BLOCKED: git reset --hard permanently discards uncommitted work. Use git stash or git checkout to preserve changes."
        elif re.search(r"git\s+clean\s+-fd", command, re.IGNORECASE):
            block_reason = "BLOCKED: git clean -fd permanently deletes untracked files. Review what will be deleted with 'git clean -n' first."
        elif re.search(r"mkfs\.|fdisk|parted", command, re.IGNORECASE):
            block_reason = "BLOCKED: Disk formatting permanently erases data. This must be done manually with extreme care."
        elif re.search(r"dd\s+if=", command, re.IGNORECASE):
            block_reason = "BLOCKED: dd can overwrite disk sectors permanently. Run manually only if you are certain of the target device."

    if tool_name in ("WriteFile", "StrReplaceFile") and file_path:
        if file_path.lower().endswith((".env", ".env.local", ".env.production")):
            block_reason = "BLOCKED: Directly editing .env files risks leaking secrets to git. Edit .env.example instead, then copy and fill in values manually."

    if block_reason:
        print(block_reason, file=sys.stderr)
        sys.exit(2)

    explanation = ""
    if tool_name == "Shell" and command:
        cmd = command.strip().lower()
        patterns = [
            (r"^git\s+add", "This stages files for a commit."),
            (r"^git\s+commit", "This saves the staged changes to git history."),
            (r"^git\s+push", "This uploads local commits to the remote repository."),
            (r"^git\s+pull", "This downloads the latest changes from the remote repository."),
            (r"^git\s+status", "This shows which files have changed."),
            (r"^git\s+diff", "This shows the actual changes in files."),
            (r"^git\s+clone", "This downloads a copy of a repository."),
            (r"^git\s+checkout", "This switches to a different branch or restores a file."),
            (r"^git\s+branch", "This lists or creates branches."),
            (r"^git\s+merge", "This combines changes from another branch."),
            (r"^git\s+revert", "This undoes a previous commit by creating a new commit."),
            (r"^git\s+stash", "This temporarily saves uncommitted changes."),
            (r"^docker\s+compose\s+up", "This starts the Docker services defined in docker-compose.yml."),
            (r"^docker\s+compose\s+down", "This stops and removes the running Docker services."),
            (r"^docker\s+compose\s+restart", "This restarts the Docker services."),
            (r"^docker\s+ps", "This lists running Docker containers."),
            (r"^docker\s+logs", "This shows the logs of a running container."),
            (r"^docker\s+build", "This builds a Docker image from a Dockerfile."),
            (r"^ls\s", "This lists files in a directory."),
            (r"^cat\s", "This displays the contents of a file."),
            (r"^cp\s", "This copies a file or directory."),
            (r"^mv\s", "This moves or renames a file or directory."),
            (r"^mkdir\s", "This creates a new directory."),
            (r"^touch\s", "This creates an empty file or updates its timestamp."),
            (r"^find\s", "This searches for files matching certain criteria."),
            (r"^grep\s", "This searches for text patterns inside files."),
            (r"^chmod\s", "This changes file permissions."),
            (r"^chown\s", "This changes file ownership."),
            (r"^pip\s+install", "This installs Python packages."),
            (r"^npm\s+install", "This installs Node.js packages."),
            (r"^npm\s+run", "This runs a script defined in package.json."),
            (r"^uv\s+add", "This adds a Python dependency to the project."),
            (r"pytest|npm\s+test|make\s+test", "This runs the project's test suite."),
            (r"make\s+build|npm\s+run\s+build", "This compiles or builds the project."),
            (r"ruff\s+check|eslint|prettier", "This checks or formats code for style consistency."),
            (r"^systemctl\s+status", "This checks whether a system service is running."),
            (r"^systemctl\s+restart", "This restarts a system service."),
            (r"^journalctl", "This views system service logs."),
        ]
        for pat, expl in patterns:
            if re.search(pat, command, re.IGNORECASE):
                explanation = expl
                break

    if explanation:
        print(f"[Human Guard] Shell command understood: {explanation}")

    if tool_name == "WriteFile" and file_path:
        if Path(file_path).exists():
            print(f"[Human Guard] This will overwrite the existing file: {file_path}")
        else:
            print(f"[Human Guard] This will create a new file: {file_path}")
    elif tool_name == "StrReplaceFile" and file_path:
        print(f"[Human Guard] This will edit the existing file: {file_path}")


if __name__ == "__main__":
    main()
